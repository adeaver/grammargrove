from typing import List, Tuple

import re
import requests

import logging

from bs4 import BeautifulSoup

from grammargrove.pinyin_utils import convert_to_numeric_form
from words.models import Word, LanguageCode
from words.utils import make_word_id_with_pinyin_list

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


BASE_URL = "https://hsk.academy"

class Command(BaseCommand):
    help = "Labels words with HSK levels"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            help="Which level to update",
        )

    def handle(self, *args, **options):
        level = 1 if not options["level"] else int(options.get("level"))
        html = _get_html(level)
        words = _get_words(html)
        _label_words(level, words)


def _get_html(level: int) -> BeautifulSoup:
    resp = requests.get(f"{BASE_URL}/en/hsk-{level}-vocabulary-list")
    return BeautifulSoup(resp.content)


def _get_words(html: BeautifulSoup) -> List[Tuple[str, str, LanguageCode]]:
    out: List[Tuple[str, str, LanguageCode]] = []
    words = html.find_all("button", attrs = { "class": "hsk-tile" })
    for w in words:
        out += _process_word(w)
    return out


def _process_word(word: BeautifulSoup) -> List[Tuple[str, str, LanguageCode]]:
    out: List[Tuple[str, str, LanguageCode]] = []
    simplified_element = word.find("span", attrs = { "class": "hsk-simplified" })
    traditional_element = word.find("span", attrs = { "class": "hsk-traditional" })
    pinyin_element = word.find("span", attrs = { "class": "hsk-pinyin" })

    if not pinyin_element:
        logging.warn(f"Word {word} does not have pinyin element")
        return []

    pinyin = re.sub("\n", "", pinyin_element.string.strip())
    if simplified_element:
        simplified = re.sub("\n", "", simplified_element.string.strip())
        out.append((simplified, pinyin, LanguageCode.SIMPLIFIED_MANDARIN))
    if traditional_element:
        traditional = re.sub("\n", "", traditional_element.string.strip())
        out.append((traditional, pinyin, LanguageCode.TRADITIONAL_MANDARIN))
    return out


def _label_words(level: int, words: List[Tuple[str, str, LanguageCode]]):
    for (hanzi, pinyin, language_code) in words:
        try:
            numeric_pinyin = [ convert_to_numeric_form(p) for p in pinyin.split(" ") ]
        except Exception as e:
            logging.warn(f"Error on {pinyin}: {e}")
            continue
        word_id = make_word_id_with_pinyin_list(language_code, hanzi, numeric_pinyin)
        word_objects = Word.objects.filter(
            id=word_id,
        ).all()
        if len(word_objects) != 1:
            logging.warn(f"Found {len(word_objects)} for word {hanzi} ({pinyin}) but expected exactly one")
            continue
        word = word_objects[0]
        word.hsk_level = level
        word.save()
