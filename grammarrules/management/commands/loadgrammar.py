from typing import List, Dict, NamedTuple, Optional

import logging
import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from grammargrove.pinyin_utils import convert_to_numeric_form, PinyinSplitter
from grammarrules.models import (
    GrammarRule,
    GrammarRuleComponent,
    PartOfSpeech,
    GrammarRuleHumanVerifiedPromptExample,
    GrammarRuleHumanVerifiedPromptExampleComponent
)
from words.models import Word, LanguageCode
from words.utils import make_word_id_with_pinyin_list

class Command(BaseCommand):
    help = "Loads the grammar rules"

    def handle(self, *args, **options):
        sp = PinyinSplitter()
        parts_of_speech_by_name = { p.name.lower(): p for p in PartOfSpeech }
        with open(f"{settings.BASE_DIR}/grammarrules/data/grammarrules.csv", "r") as f:
            with open(f"{settings.BASE_DIR}/grammarrules/data/grammarruleexamples.csv", "r") as e:
                grammar_rule_reader = csv.reader(f)
                grammar_rule_example_reader = csv.reader(e)
                current_grammar_rule_example = next(grammar_rule_example_reader)
                current_grammar_rule_example = next(grammar_rule_example_reader)
                for idx, row in enumerate(grammar_rule_reader):
                    if idx == 0:
                        continue
                    to_insert = _process_row(parts_of_speech_by_name, row)
                    if to_insert is not None and current_grammar_rule_example is not None:
                        logging.warn(f"{current_grammar_rule_example}")
                        grammar_rule_line_number, structure, use, hanzi, pinyin, explanation = current_grammar_rule_example
                        while current_grammar_rule_example is not None and int(grammar_rule_line_number) <= idx+1:
                            if int(grammar_rule_line_number) == idx+1:
                                _process_example(
                                    sp, parts_of_speech_by_name, to_insert.rule, structure, use, hanzi, pinyin, explanation
                                )
                            try:
                                current_grammar_rule_example = next(grammar_rule_example_reader)
                                grammar_rule_line_number, structure, use, hanzi, pinyin, explanation = current_grammar_rule_example
                            except StopIteration:
                                current_grammar_rule_example = None


class GrammarRuleToInsert(NamedTuple):
    rule: GrammarRule
    component: List[GrammarRuleComponent]

def _process_row(
    parts_of_speech_by_name: Dict[str, PartOfSpeech],
    row: str
) -> Optional[GrammarRuleToInsert]:
    title, definition, rule, pinyin = row
    components = _process_components(parts_of_speech_by_name, rule, pinyin)
    if not components:
        return None
    grammar_rule = GrammarRule(
        title=title,
        definition=definition,
        language_code=LanguageCode.SIMPLIFIED_MANDARIN,
    )
    grammar_rule.save()
    for c in components:
        if c.word is not None:
            logging.warn(f"Saving {c.word} to {grammar_rule.id}")
        else:
            logging.warn(f"Saving {c.part_of_speech} to {grammar_rule.id}")
        c.grammar_rule = grammar_rule
        c.save()
    return GrammarRuleToInsert(
        rule=grammar_rule,
        component=components
    )

def _process_components(
    parts_of_speech_by_name: Dict[str, PartOfSpeech],
    rule: str,
    pinyin: str
) -> Optional[List[GrammarRuleComponent]]:
    out = []
    rules = rule.split(" ")
    pinyin = pinyin.split(" ")
    pinyin_idx = 0
    for idx, r in enumerate(rules):
        optional = (
            len(r) > 1 and
            r[0] == "(" and
            r[-1] == ")"
        )
        if optional:
            r = r[1:len(r)-1]
        if r.lower() in parts_of_speech_by_name:
            pinyin_idx += 1
            out.append(
                GrammarRuleComponent(
                    part_of_speech=parts_of_speech_by_name[r.lower()],
                    rule_index=idx,
                    optional=optional,
                )
            )
        else:
            rule_pinyin = pinyin[pinyin_idx:pinyin_idx+len(r)]
            pinyin_idx += len(r)
            search_pinyin = [
                convert_to_numeric_form(p)
                for p in rule_pinyin
            ]
            search_display = r
            word_id = make_word_id_with_pinyin_list(LanguageCode.SIMPLIFIED_MANDARIN, r, search_pinyin)
            word = Word.objects.filter(id=word_id)
            if not word:
                logging.warn(f"{r} ({search_pinyin}) does not exist as word")
                return None
            out.append(
                GrammarRuleComponent(
                    word=word[0],
                    rule_index=idx,
                    optional=optional
                )
            )
    return out


def _process_example(
    sp: PinyinSplitter,
    parts_of_speech_by_name: Dict[str, PartOfSpeech],
    grammar_rule: GrammarRule,
    structure: str,
    use: str,
    hanzi: str,
    pinyin: str,
    explanation: str,
):
    logging.warn("Adding example {structure}")
    # TODO: make this whole thing atomic
    example = GrammarRuleHumanVerifiedPromptExample(
        grammar_rule=grammar_rule,
        language_code=LanguageCode.SIMPLIFIED_MANDARIN,
        hanzi_display=hanzi,
        pinyin_display=pinyin,
        structure_use=use,
        explanation=explanation,
    )
    example.save()
    structure_parts = structure.split(" ")
    pinyin_parts = pinyin.split(" ")
    for idx, s in enumerate(structure_parts):
        if s in parts_of_speech_by_name:
            GrammarRuleHumanVerifiedPromptExampleComponent(
                prompt_example=example,
                part_of_speech=parts_of_speech_by_name[s],
                rule_index=idx,
            ).save()
        else:
            pinyin_for_word = pinyin_parts[idx]
            parts = []
            if len(s) > 1:
                split_result = sp.split(pinyin_for_word, len(s))
                if split_result.error_reason:
                    return
                parts = split_result.result[0]
            else:
                parts = [pinyin_for_word]
            word_id = make_word_id_with_pinyin_list(
                LanguageCode.SIMPLIFIED_MANDARIN,
                s,
                [ convert_to_numeric_form(p) for p in parts ]
            )
            w = Word.objects.filter(id=word_id)
            if not w:
                return
            GrammarRuleHumanVerifiedPromptExampleComponent(
                prompt_example=example,
                word=w[0],
                rule_index=idx,
            ).save()
