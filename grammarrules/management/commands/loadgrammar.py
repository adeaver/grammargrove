from typing import List, Dict, NamedTuple, Optional

import logging
import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from grammargrove import pinyin_utils
from grammarrules.models import GrammarRule, GrammarRuleComponent, PartOfSpeech
from words.models import Word

class Command(BaseCommand):
    help = "Loads the grammar rules"

    def handle(self, *args, **options):
        parts_of_speech_by_name = { p.name.lower(): p for p in PartOfSpeech }
        with open(f"{settings.BASE_DIR}/grammarrules/data/grammarrules.csv", "r") as f:
            grammar_rule_reader = csv.reader(f)
            for idx, row in enumerate(grammar_rule_reader):
                if idx == 0:
                    continue
                _process_row(parts_of_speech_by_name, row)


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
    )
    grammar_rule.save()
    for c in components:
        c.grammar_rule = grammar_rule
        c.save()

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
            search_pinyin = " ".join([
                pinyin_utils.convert_to_numeric_form(p)
                for p in rule_pinyin
            ])
            search_display = r
            word = Word.objects.filter(display=r, pronunciation=search_pinyin)
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


