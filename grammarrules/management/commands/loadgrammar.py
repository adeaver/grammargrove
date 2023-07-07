from typing import List, Union, NamedTuple, Dict, Optional, Tuple

import logging

import uuid
import re
import requests
import codecs
import string
import csv

from grammarrules.models import GrammarRule, GrammarRuleComponent, GrammarRuleHumanVerifiedPromptExample
from words.models import Word, LanguageCode
from words.utils import make_word_id_with_pinyin_list
from grammargrove.pinyin_utils import PinyinSplitter, convert_to_numeric_form

from bs4 import BeautifulSoup, Tag

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

DESCRIPTION_SUFFIX = " in Mandarin Chinese. Get clear explanations and lots of examples here!"
BASE_URL = "https://resources.allsetlearning.com"

REPLACEMENTS = {
    "subj": "subject",
    "verb": "verb",
    "adj": "adjective",
    "obj": "object",
    "adv": "adverb",
    "noun": "noun",
}

class Command(BaseCommand):
    help = "Loads the grammar rules"


    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            help="Which level to update",
        )
        parser.add_argument(
            "--dry_run",
            help="Whether or not this is a dry run",
        )


    def handle(self, *args, **options):
        level = 1 if not options["level"] else int(options.get("level"))
        is_dry_run = not options.get("dry_run") or options["dry_run"].lower() != "false"
        if is_dry_run:
            logging.warn("This is a dry run")
        html = _get_html_for_hsk_level(level)
        rules = _get_rules_from_html(html)
        with open(f"{settings.BASE_DIR}/grammarrules/data/grammarrules_{level}_errors.csv", "w") as rules_file:
            rules_writer = csv.DictWriter(rules_file, fieldnames=["rule_url", "title", "error"])
            rules_writer.writeheader()
            for r in rules:
                try:
                    _process_rule(r, level, is_dry_run)
                except KeyboardInterrupt:
                    return
                except Exception as e:
                    rules_writer.writerow({
                        "rule_url": r.next_url,
                        "title": r.title,
                        "error": e,
                    })





def _make_text(encoded_text: str) -> str:
    hex_str, _ = codecs.escape_decode(encoded_text, 'hex')
    return hex_str.decode("utf-8")


def _get_text_from_element_list(contents: List[Union[str, Tag]]) -> str:
    elements = ' '.join([ _get_text_from_element_list(c.contents) if isinstance(c, Tag) else c for c in contents ])
    return _make_text(elements).replace("\n", "").strip()


def _get_html_for_hsk_level(level: int) -> str:
    request_url = f"{BASE_URL}/chinese/grammar/HSK_{level}_grammar_points"
    resp = requests.get(request_url)
    return resp.content


class Rule(NamedTuple):
    title: str
    next_url: str
    structure: str
    example: str


def _get_rules_from_html(html: str) -> List[Rule]:
    out: List[Rule] = []
    soup = BeautifulSoup(html)
    tables = soup.find_all('table', attrs = { 'class': 'wikitable' })
    for t in tables:
        rows = t.find_all('tr')
        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            cells = row.find_all('td')
            title, structure, example = cells
            title_anchor = title.find('a')
            next_url = title_anchor["href"]
            out.append(
                Rule(
                    title=_get_text_from_element_list(title_anchor),
                    next_url=f"{BASE_URL}{next_url}",
                    structure=_get_text_from_element_list(structure),
                    example=_get_text_from_element_list(example.contents),
                )
            )
    return out


def _process_rule(rule: Rule, level: int, is_dry_run: bool):
    html = _get_rule_html(rule)
    description = _get_rule_description(html)
    structures = _get_structures(html)
    verified_structures = {
        s.get_hashable(): s
        for s in structures
        if any([ p.word is not None for p in s.parts ])
    }
    assert len(verified_structures), (
        f"Rule {rule.title} has no word structures"
    )
    examples_by_structure = _get_examples(html, list(verified_structures.values()))
    for idx, s in enumerate(list(verified_structures.values())):
        examples = examples_by_structure[idx]
        if not examples:
            logging.warn(f"Structure {s} has no examples")
        g = GrammarRule(
            title=rule.title,
            definition=description,
            language_code=LanguageCode.SIMPLIFIED_MANDARIN,
            hsk_level=level,
        )
        if not is_dry_run:
            g.save()
        else:
            logging.warn(f"Is dry run, but would save: {g}")
        components = [
            GrammarRuleComponent(
                grammar_rule=(g if g.id is not None else uuid.uuid4()),
                word=p.word,
                part_of_speech=p.part_of_speech,
                rule_index=idx
            )
            for idx, p in enumerate(s.parts)
        ]
        for c in components:
            if not is_dry_run:
                c.save()
            else:
                logging.warn(f"Is dry run, but would save: {c}")
        for e in examples:
            ex = GrammarRuleHumanVerifiedPromptExample(
                grammar_rule=(g if g.id is not None else uuid.uuid4()),
                language_code=LanguageCode.SIMPLIFIED_MANDARIN,
                hanzi_display=e.hanzi,
                pinyin_display=e.pinyin,
                structure_use=description,
                explanation=e.definition,
            )
            if not is_dry_run:
                ex.save()
            else:
                logging.warn(f"Is dry run, but would save: {ex}")



def _get_rule_html(rule: Rule) -> BeautifulSoup:
    resp = requests.get(rule.next_url)
    return BeautifulSoup(resp.content)

def _get_rule_description(rule_html: BeautifulSoup) -> str:
    tag = rule_html.find("meta", attrs = { "property": "og:description" })
    contents = tag["content"]
    contents = contents.removeprefix("This grammar point is ")
    contents = contents[:-len(DESCRIPTION_SUFFIX)]
    contents = contents.strip().lower()
    return contents

class StructurePart(NamedTuple):
    part_of_speech: Optional[str]
    word: Optional[Word]

    def get_hashable(self) -> str:
        if self.part_of_speech is not None:
            return f"part_of_speech:{self.part_of_speech}"
        return f"word:{self.word.id}"

class Structure(NamedTuple):
    parts: List[StructurePart]

    def get_keywords(self) -> Dict[str, bool]:
        return {
            p.word.id: True
            for p in self.parts
            if p.word is not None
        }

    def get_hashable(self) -> str:
        return " ".join([ p.get_hashable() for p in self.parts ])

def _get_structures(rule_html: BeautifulSoup) -> List[Structure]:
    splitter = PinyinSplitter()
    pinyin = _get_pinyin(rule_html)
    structures = rule_html.find_all("div", attrs = { 'class': 'jiegou' })
    processed_structures = [
        _get_text_from_element_list(s)
        for s in structures
    ]
    out: List[Structure] = []
    for p in processed_structures:
        out_parts: List[List[StructurePart]] = [[]]
        processed = _process_input(p)
        structure_parts = processed.split("+")
        for sp in structure_parts:
            stripped = sp.strip()
            slash_parts = stripped.split("/")
            if len(slash_parts) > 1:
                words = [ _process_word(splitter, pinyin, p.strip()) for p in slash_parts ]
                if all([ w is not None for w in words ]):
                    # Copy every part of out_parts for each word
                    temp = []
                    for w in words:
                        for p in out_parts:
                            p = p + [ w ]
                            temp.append(p)
                    out_parts = temp
                    continue
                elif any([w is not None for w in words ]):
                    # Copy every part of out_parts for each word
                    for idx, w in enumerate(words):
                        structure_part = (
                            _process_structure_part(splitter, pinyin, slash_parts[idx].strip())
                            if w is None else w
                        )
                        temp = []
                        for p in out_parts:
                            p = p + [ structure_part ]
                            temp.append(p)
                    out_parts = temp
                    continue
            structure_part = _process_structure_part(splitter, pinyin, stripped)
            for p in out_parts:
                p.append(structure_part)
        out += [ Structure(parts=parts) for parts in out_parts ]
    return out

def _process_input(structure_text: str) -> str:
    bad_characters_with_replacement = {
        ",": "+ , + ",
        "?": "+ ? + ",
        "，": "+ , + ",
        "[": "",
        "]": "",
        ".": "",
        "(+ ": "+ (",
    }
    out = structure_text.strip()
    for c, r in bad_characters_with_replacement.items():
        out = out.replace(c, r)
    if out[-1] == "+ ":
        out = out[:len(out)-2]
    return out.strip()

def _process_structure_part(splitter: PinyinSplitter, pinyin: Dict[str, str], stripped: str) -> StructurePart:
    if stripped.lower() in REPLACEMENTS:
        replacement = REPLACEMENTS[stripped.lower()]
        return StructurePart(part_of_speech=replacement.title(), word=None)
    else:
        maybe_word = _process_word(splitter, pinyin, stripped)
        if maybe_word:
            return maybe_word
    return StructurePart(part_of_speech=stripped, word=None)


def _process_word(splitter: PinyinSplitter, pinyin: Dict[str, str], stripped: str) -> Optional[StructurePart]:
    maybe_hanzi = ''.join(stripped.split(" "))
    word: Optional[Word] = None
    if maybe_hanzi in pinyin:
        hanzi_for_pinyin = pinyin[maybe_hanzi]
        pinyin_parts = splitter.split(hanzi_for_pinyin, len(maybe_hanzi))
        if pinyin_parts.error_reason:
            raise ValueError(f"Could not parse {hanzi_for_pinyin} for pinyin {maybe_hanzi}")
        pronunciation = " ".join([ convert_to_numeric_form(p) for p in pinyin_parts.result[0] ])
        word = Word.objects.filter(
            language_code=LanguageCode.SIMPLIFIED_MANDARIN,
            pronunciation=pronunciation,
            display=maybe_hanzi
        )
        if not word:
            logging.warn(f"{maybe_hanzi} ({pronunciation}) has no word")
            return None
        word = word[0]
    else:
        word = Word.objects.filter(
            language_code=LanguageCode.SIMPLIFIED_MANDARIN,
            display=maybe_hanzi
        ).all()
        if len(word) != 1:
            return None
        word = word[0]
    return StructurePart(part_of_speech=None, word=word)


def _get_pinyin(rule_html: BeautifulSoup) -> Dict[str, str]:
    tag = rule_html.find("meta", attrs = { "name": "keywords" })
    contents = tag["content"].split(",")
    out = {}
    for idx in range(0, len(contents), 3):
        if idx+1 >= len(contents):
            break
        maybe_hanzi = contents[idx]
        maybe_pinyin = contents[idx+1]
        if re.search(u'[\u4e00-\u9fff]', maybe_hanzi):
            out[maybe_hanzi] = maybe_pinyin
    return out

class ScrapedExample(NamedTuple):
    hanzi: str
    pinyin: str
    definition: str
    explanation: Optional[str]
    keywords: List[Tuple[str, str]]

def _process_example(e: BeautifulSoup) -> Optional[ScrapedExample]:
    all_text = _get_text_from_element_list(e)
    speaker_element = e.find("span", attrs = { 'class': 'speaker' })
    pinyin_element = e.find("span", attrs = { 'class': 'pinyin' })
    translation_element = e.find("span", attrs = { 'class': 'trans' })
    explanation_element = e.find("span", attrs = { 'class': 'expl' })
    if not pinyin_element or not translation_element:
        return None
    pinyin = _get_text_from_element_list(pinyin_element)
    translation = _get_text_from_element_list(translation_element)
    explanation: Optional[str] = None
    if explanation_element:
        explanation = _get_text_from_element_list(explanation_element)
    speaker: str = ""
    if speaker_element:
        speaker = _get_text_from_element_list(speaker_element)
    pinyin_keywords = [
        _get_text_from_element_list(keyword)
        for keyword in pinyin_element.find_all("em")
    ]
    all_keywords = [
        _get_text_from_element_list(keyword)
        for keyword in e.find_all("em")
    ][:-len(pinyin_keywords)]
    keywords = []
    if all_keywords and pinyin_keywords:
        keywords = list(zip(all_keywords, pinyin_keywords))
    hanzi = all_text.removeprefix(speaker)
    hanzi = hanzi.replace(translation, "")
    hanzi = hanzi.replace(pinyin, "")
    if explanation is not None:
        hanzi = hanzi.replace(explanation, "")
    return ScrapedExample(
        hanzi=hanzi.strip(),
        pinyin=pinyin.strip(),
        definition=translation.strip(),
        explanation=explanation,
        keywords=keywords,
    )

def _get_examples(rule_html: BeautifulSoup, structures: List[Structure]) -> List[List[ScrapedExample]]:
    out: List[List[ScrapedExample]] = [ [] for s in structures ]
    splitter = PinyinSplitter()
    example_containers = rule_html.find_all("div", attrs = { 'class': 'liju' })
    examples = []
    for ec in example_containers:
        examples += ec.find_all("li")

    processed_examples: List[ScrapedExample] = []
    for e in examples:
        processed = _process_example(e)
        if processed:
            processed_examples.append(processed)

    for p in processed_examples:
        keyword_ids = []
        for (hanzi, pinyin) in p.keywords:
            pinyin_split = splitter.split("".join(pinyin.split(" ")), len("".join(hanzi.split(" "))))
            if pinyin_split.error_reason:
                logging.warn(f"Could not split pinyin {pinyin} because {pinyin_split.error_reason}")
            else:
                numeric_pinyin = [
                    convert_to_numeric_form(p)
                    for p in pinyin_split.result[0]
                ]
                keyword_ids.append(
                    make_word_id_with_pinyin_list(
                        LanguageCode.SIMPLIFIED_MANDARIN,
                        hanzi.strip(),
                        numeric_pinyin,
                    )
                )
        for idx, s in enumerate(structures):
            structure_keyword_ids = list(s.get_keywords().keys())
            if structure_keyword_ids == keyword_ids:
                out[idx].append(p)
                break

    return out
