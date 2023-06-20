import logging
from typing import List, NamedTuple, Optional

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from words.models import LanguageCode, Word, Definition

class Command(BaseCommand):
    help = "Loads the dictionary from CEDICT"

    def handle(self, *args, **options):
        Definition.objects.all().delete()
        Word.objects.all().delete()
        with open(f"{settings.BASE_DIR}/words/data/cedict.txt", "r") as f:
            for line in f.readlines():
                _process_line(line)


class WordParts(NamedTuple):
    traditional: str
    simplified: str
    pinyin: str
    definitions: List[str]

    def get_traditional_id(self) -> str:
        character_component = ":".join([
            str(ord(c))
            for c in self.traditional
        ])
        pinyin_component = ":".join(self.pinyin.split(" "))
        return f"{LanguageCode.TRADITIONAL_MANDARIN.value}c{character_component}::{pinyin_component}"

    def get_simplified_id(self) -> str:
        character_component = ":".join([
            str(ord(c))
            for c in self.simplified
        ])
        pinyin_component = ":".join(self.pinyin.split(" "))
        return f"{LanguageCode.SIMPLIFIED_MANDARIN.value}c{character_component}::{pinyin_component}"

def _process_line(line: str) -> None:
    if line.startswith("#"):
        return
    parts: WordParts = _get_parts_from_line(line)
    with transaction.atomic():
        traditional = Word(
            id=parts.get_traditional_id(),
            language_code=LanguageCode.TRADITIONAL_MANDARIN,
            display=parts.traditional,
            pronunciation=parts.pinyin
        )
        traditional.save()
        simplified = Word(
            id=parts.get_simplified_id(),
            language_code=LanguageCode.SIMPLIFIED_MANDARIN,
            display=parts.simplified,
            pronunciation=parts.pinyin
        )
        simplified.save()
        for definition in parts.definitions:
            Definition(
                language_code=LanguageCode.ENGLISH,
                word=traditional,
                definition=definition,
            ).save()
            Definition(
                language_code=LanguageCode.ENGLISH,
                word=simplified,
                definition=definition,
            ).save()

def _get_parts_from_line(line: str) -> WordParts:
    traditional: Optional[str] = None
    simplified: Optional[str] = None
    pinyin: Optional[str] = None
    definitions: List[str] = []

    current_word = []

    for c in line:
        if c == " ":
            if traditional is None:
                traditional = ''.join(current_word)
                current_word = []
            elif simplified is None:
                simplified = ''.join(current_word)
                current_word = []
            else:
                current_word.append(c)
        elif c == "[" and pinyin is None:
            pass
        elif c == "]" and pinyin is None:
            pinyin = ''.join(current_word)
            current_word = []
        elif c == "/":
            definitions.append(''.join(current_word))
            current_word = []
        else:
            current_word.append(c)
    assert traditional, (
        f"Line {line} has no traditional"
    )
    assert simplified, (
        f"Line {line} has no simplified"
    )
    assert pinyin, (
        f"Line {line} has no pinyin"
    )
    assert definitions, (
        f"Line {line} has no definitions"
    )
    return WordParts(
        traditional=traditional,
        simplified=simplified,
        pinyin=pinyin.lower(),
        definitions=definitions,
    )
