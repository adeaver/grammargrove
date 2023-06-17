from typing import NamedTuple, List, Tuple, Optional

import logging

import csv
import jieba

from django.db import transaction

from grammargrove.pinyin_utils import PinyinSplitter, convert_to_numeric_form
from .models import (
    GrammarRuleExampleParseVersion,
    GrammarRuleExamplePrompt,
    GrammarRuleExample,
    GrammarRuleExampleComponent,
)
from words.models import Word, LanguageCode
from words.utils import make_word_id_with_pinyin_list

class ParseOutput(NamedTuple):
    grammar_rule_examples: List[GrammarRuleExample]
    retryable: bool

def parse_example_prompt(
    example_prompt_id: str,
    reparse_non_errored: bool = False
) -> ParseOutput:
    prompts = GrammarRuleExamplePrompt.objects.filter(id=example_prompt_id)
    if not prompts:
        return ParseOutput(grammar_rule_examples=[], retryable=False)
    prompt = prompts[0]
    prompt.parse_version = GrammarRuleExampleParseVersion.current_version()
    splitter = PinyinSplitter()
    reader = csv.reader(prompt.response.split("\n"))
    for idx, row in enumerate(reader):
        if idx == 0:
            continue
        hanzi, pinyin, english_definition = row
        examples = GrammarRuleExample.objects.filter(grammar_rule=prompt.grammar_rule, grammar_rule_example_prompt=prompt, line_idx=idx)
        if examples:
            example = examples[0]
            if not reparse_non_errored and example.parse_error is None:
                logging.warn(f"Grammar rule example {example.id} has no errors, not reparsing")
                continue
            example.parse_version = GrammarRuleExampleParseVersion.current_version()
        else:
            logging.warn("Attempting to create new grammar rule example record")
            examples = GrammarRuleExample.objects.filter(grammar_rule=prompt.grammar_rule, hanzi_display=hanzi).all()
            if examples:
                logging.warn(f"Example {hanzi} for grammar rule {prompt.grammar_rule.id} already exists. Skipping...")
                continue
            example = GrammarRuleExample(
                grammar_rule = prompt.grammar_rule,
                grammar_rule_example_prompt=prompt,
                line_idx=idx,
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
            continue
        elif len(pinyin_parts.result) > 1:
            example.parse_error = (
                f"Could not parse pinyin because there are {len(pinyin_parts.result)} parse results"
            )
            logging.warn(example.parse_error)
            example.save()
            continue
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
            continue
        words: List[Word] = []
        errors: List[str] = []
        for idx, (hanzi, pinyin) in enumerate(lookup):
            pronunciation = [ convert_to_numeric_form(p) for p in pinyin ]
            language_code = _fix_language_code(prompt.language_code)
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
            continue
        with transaction.atomic():
            example.save()
            GrammarRuleExampleComponent.objects.filter(grammar_rule_example=example).delete()
            for idx, word in enumerate(words):
                GrammarRuleExampleComponent(
                    grammar_rule_example=example,
                    example_index=idx,
                    word=word
                ).save()
        logging.warn(f"Saved {example.id}")



def _fix_language_code(l: str) -> Optional[LanguageCode]:
    possible_name_parts = l.split(".")
    possible_name = possible_name_parts[-1]
    for code in LanguageCode:
        if code.name == possible_name:
            return code
    return None





