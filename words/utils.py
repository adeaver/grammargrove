from typing import List

from .models import LanguageCode

def make_word_id(
    language_code: LanguageCode,
    hanzi: str,
    pinyin: str,
) -> str:
    return make_word_id_with_pinyin_list(
        language_code,
        hanzi,
        pinyin.split(" ")
    )

def make_word_id_with_pinyin_list(
    language_code: LanguageCode,
    hanzi: str,
    pinyin: List[str],
) -> str:
    character_component = ":".join([
        str(ord(c))
        for c in hanzi
    ])
    pinyin_component = (":".join(pinyin)).lower()
    return f"{language_code}c{character_component}::{pinyin_component}"
