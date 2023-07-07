from typing import List, Union, NamedTuple, Dict, Optional

import logging

import re
import requests
import codecs
import string
import csv

from words.models import Word, LanguageCode
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


    def handle(self, *args, **options):
        level = 1 if not options["level"] else int(options.get("level"))
        html = _get_html_for_hsk_level(level)
        rules = _get_rules_from_html(html)
        for r in rules:
            _process_rule(r)



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


def _process_rule(rule: Rule):
    html = _get_rule_html(rule)
    description = _get_rule_description(html)
    structures = _get_structures(html)
    logging.warn(structures)

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

class Structure(NamedTuple):
    parts: List[StructurePart]

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
        structure_parts = p.split("+")
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
    out = structure_text.strip()
    out = out.replace("(+ ", "+ (")
    out = out.replace(".", "")
    bad_characters_with_replacement = {
        ",": "+ , + ",
        "?": "+ ? + ",
        "，": "+ , + ",
        "[", "",
        "]", "",
    }
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

