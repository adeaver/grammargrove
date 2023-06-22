from typing import List

from django.db.models import QuerySet

from .models import LanguageCode, Word

from grammargrove.pinyin_utils import (
    PinyinSplitter,
    is_numeric_form,
    is_display_form,
    convert_to_numeric_form
)

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


def get_queryset_for_query(query_language_code: LanguageCode, search_query: str) -> QuerySet:
    are_all_parts_numeric_form = all([ is_numeric_form(p) for p in search_query.split(" ") ])
    are_all_parts_display_form = all([ is_display_form(p) for p in search_query.split(" ") ])
    if are_all_parts_numeric_form:
        return Word.objects.filter(
            language_code=query_language_code, pronunciation=search_query)
    elif are_all_parts_display_form:
        split_results = search_query.split(" ")
        if len(split_results) == 1:
            sp = PinyinSplitter()
            as_split = sp.split(search_query, expected_output_length=None)
            if as_split.error_reason:
                split_results = []
            else:
                split_results = [
                    " ".join([ convert_to_numeric_form(p) for p in split ])
                    for split in as_split.result
                ]
        else:
            split_results = [ " ".join([ convert_to_numeric_form(p) for p in split_results ]) ]
        return Word.objects.filter(
            language_code=query_language_code, pronunciation__in=split_results)
    return Word.objects.filter(
        language_code=query_language_code, display=search_query)
