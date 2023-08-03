from typing import NamedTuple, List, Tuple, Optional

import logging

import string
import re
import csv
import jieba

from django.db import transaction
from django.db.models import QuerySet

from grammargrove.pinyin_utils import PinyinSplitter, convert_to_numeric_form
from .models import (
    GrammarRuleComponent,
    GrammarRuleExampleParseVersion,
    GrammarRuleExamplePrompt,
    GrammarRuleExample,
    GrammarRuleExampleComponent,
)
from .utils import ensure_normalized_hanzi
from words.models import Word, LanguageCode
from words.utils import make_word_id_with_pinyin_list

def get_unparsed_examples() -> QuerySet:
    return GrammarRuleExample.objects.exclude(parse_version=GrammarRuleExampleParseVersion.current_version())

class ParseOutput(NamedTuple):
    grammar_rule_examples: List[GrammarRuleExample]
    retryable: bool

def parse_example_prompt(
    example_prompt_id: str,
    reparse_non_errored: bool = False
) -> ParseOutput:
    prompt = GrammarRuleExamplePrompt.objects.filter(id=example_prompt_id).first()
    if not prompt:
        return ParseOutput(grammar_rule_examples=[], retryable=False)
    prompt.parse_version = GrammarRuleExampleParseVersion.current_version()
    reader = csv.reader(prompt.response.split("\n"))
    examples: List[GrammarRuleExample] = []
    for idx, row in enumerate(reader):
        if idx == 0:
            continue
        example = _parse_example_prompt_line(prompt, row, idx, reparse_non_errored)
        examples.append(example)
    return ParseOutput(
        grammar_rule_examples=examples,
        retryable=False
    )



def reparse_example_prompt_line_number(
    example_prompt_id: str,
    line_idx: int
) -> None:
    prompt = GrammarRuleExamplePrompt.objects.filter(id=example_prompt_id).first()
    if not prompt:
        logging.warning(f"Prompt {example_prompt_id} does not exist")
        return None
    reader = csv.reader(prompt.response.split("\n"))
    for idx, row in enumerate(reader):
        if idx == line_idx:
            example = _parse_example_prompt_line(prompt, row, line_idx, reparse_non_errored=True)
            if not example:
                logging.warning(f"There was an error reparsing line {line_idx} for prompt {example_prompt_id}")




def _parse_example_prompt_line(
    prompt: GrammarRuleExamplePrompt,
    row: Tuple[str, str, str],
    line_idx: int,
    reparse_non_errored: bool = False
) -> Optional[GrammarRuleExample]:
    number_of_components = len(
        GrammarRuleComponent.objects.filter(
            grammar_rule=prompt.grammar_rule
        )
    )
    splitter = PinyinSplitter()
    try:
        hanzi, pinyin, english_definition = row
    except ValueError:
        logging.warn(f"Error on row {row}")
        return None
    hanzi = ensure_normalized_hanzi(hanzi)
    pinyin = _ensure_normalized_pinyin(pinyin)
    example = GrammarRuleExample.objects.filter(
        grammar_rule=prompt.grammar_rule,
        grammar_rule_example_prompt=prompt,
        line_idx=line_idx
    ).first()
    if example and (not reparse_non_errored and example.parse_error is None):
        logging.warn(f"Grammar rule example {example.id} has no errors, not reparsing")
        return None
    elif example:
        example.parse_version = GrammarRuleExampleParseVersion.current_version()
        example.parse_error = None
    else:
        logging.warn("Attempting to create new grammar rule example record")
        example = GrammarRuleExample.objects.filter(grammar_rule=prompt.grammar_rule, hanzi_display=hanzi).first()
        if example:
            logging.warn(f"Example {hanzi} for grammar rule {prompt.grammar_rule.id} already exists. Skipping...")
            return None
        example = GrammarRuleExample(
            grammar_rule = prompt.grammar_rule,
            grammar_rule_example_prompt=prompt,
            line_idx=line_idx,
            hanzi_display=hanzi,
            pinyin_display=pinyin,
            english_definition=english_definition,
            parse_version=GrammarRuleExampleParseVersion.current_version()
        )
    pinyin_parts = splitter.split(
        "".join(pinyin.split(" ")),
        len(hanzi)
    )
    if pinyin_parts.error_reason is not None:
        example.parse_error = (
            f"Could not parse pinyin because {pinyin_parts.error_reason}"
        )
        logging.warn(example.parse_error)
        example.save()
        return example
    elif len(pinyin_parts.result) > 1:
        example.parse_error = (
            f"Could not parse pinyin because there are {len(pinyin_parts.result)} parse results"
        )
        logging.warn(example.parse_error)
        example.save()
        return example
    hanzi_parts = jieba.cut(hanzi, cut_all=False)
    pinyin_idx = 0
    lookup: List[Tuple[str, List[str]]] = []
    for h in hanzi_parts:
        lookup.append((
            h,
            pinyin_parts.result[0][pinyin_idx:pinyin_idx+len(h)]
        ))
        pinyin_idx += len(h)
    if pinyin_idx != len(pinyin_parts.result[0]):
        example.parse_error = (
            f"Could not parse line because there are {len(pinyin_parts.result) - pinyin_idx} "
            f"missing pinyin parts in result"
        )
        logging.warn(example.parse_error)
        example.save()
        return None
    words: List[Word] = []
    errors: List[str] = []
    for idx, (hanzi, pinyin) in enumerate(lookup):
        pronunciation = [ convert_to_numeric_form(p) for p in pinyin ]
        language_code = prompt.language_code
        if not language_code:
            errors.append(f"Language code {prompt.language_code} does not exist")
            break
        word_id = make_word_id_with_pinyin_list(
            language_code,
            hanzi,
            pronunciation
        )
        w = Word.objects.filter(id=word_id)
        if not w:
            errors.append(f"Word {hanzi} with pronunciation {pronunciation} has no word record")
        elif len(w) > 1:
            errors.append(f"Word {hanzi} with pronunciation {pronunciation} has {len(w)} word records, but expected at most 1")
        else:
            words.append(w[0])
    if errors:
        example.parse_error = "; ".join(errors)
        logging.warn(example.parse_error)
        example.save()
        return example
    if len(words) < number_of_components:
        example.parse_error = f"The response is too short. It only includes {len(words)} but the rule has {number_of_components} components"
        logging.warn(example.parse_error)
        example.save()
        return example
    max_hsk_level: Optional[int] = None
    contains_non_labeled_words: bool = False
    with transaction.atomic():
        example.save()
        GrammarRuleExampleComponent.objects.filter(grammar_rule_example=example).delete()
        for idx, word in enumerate(words):
            max_hsk_level = (
                word.hsk_level
                if max_hsk_level is None or word.hsk_level is not None and word.hsk_level > max_hsk_level
                else max_hsk_level
            )
            contains_non_labeled_words = contains_non_labeled_words or word.hsk_level is None
            GrammarRuleExampleComponent(
                grammar_rule_example=example,
                example_index=idx,
                word=word
            ).save()
        example.max_hsk_level = max_hsk_level
        example.contains_non_labeled_words = contains_non_labeled_words
        example.save()
    logging.warn(f"Saved {example.id}")
    return example


def _ensure_normalized_pinyin(pinyin: str) -> str:
    for punc in string.punctuation:
        pinyin = pinyin.replace(punc, "")
    return pinyin.lower()

def _fix_language_code(l: str) -> Optional[LanguageCode]:
    possible_name_parts = l.split(".")
    possible_name = possible_name_parts[-1]
    for code in LanguageCode:
        if code.name == possible_name:
            return code
    return None
