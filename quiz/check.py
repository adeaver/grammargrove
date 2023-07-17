from typing import List

import logging

from grammargrove.pinyin_utils import (
    get_tone_number_from_numeric_form,
    get_tone_number_from_display_form,
    convert_to_display_form
)
from grammargrove.text_utils import remove_punctuation, remove_punctuation_from_hanzi

from grammarrules.models import GrammarRuleExample
from grammarrules.serializers import GrammarRuleExampleSerializer

from uservocabulary.models import UserVocabularyEntry
from uservocabulary.serializers import UserVocabularyEntrySerializer

from .models import QuestionType
from .serializers import CheckResponse

def check_grammar_rule(
    question_type: QuestionType,
    example: GrammarRuleExample,
    answer: List[str]
) -> CheckResponse:
    serialized_example = GrammarRuleExampleSerializer(example).data
    correct_answer = []
    extra_context = []
    if question_type == QuestionType.HanziFromEnglish:
        correct_answer = [
            remove_punctuation_from_hanzi(
                ''.join([
                    c["word"]["display"] for c in serialized_example["grammar_rule_example_components"]
                ])
            )
        ]
        answer = [ remove_punctuation_from_hanzi(a) for a in answer ]
    elif question_type == QuestionType.AccentsFromHanzi:
        for c in serialized_example["grammar_rule_example_components"]:
            pronunciation = c["word"]["pronunciation"].split(" ")
            correct_answer += [
                str(get_tone_number_from_display_form(p)) for p in pronunciation
            ]
            extra_context.append(
                ''.join(pronunciation)
            )
    elif question_type == QuestionType.DefinitionsFromHanzi:
        correct_answer = [
            remove_punctuation(serialized_example["english_definition"].lower().strip())
        ]
    else:
        raise ValueError(f"Unrecognized question type {question_type}")
    return CheckResponse(
        is_correct=correct_answer == answer,
        correct_answer=correct_answer,
        extra_context=extra_context,
        words=[],
    )


def check_vocabulary_word(
    question_type: QuestionType,
    user_vocabulary_entry_id: str,
    answer: List[str]
) -> CheckResponse:
    entries = UserVocabularyEntry.objects.filter(
        id=user_vocabulary_entry_id
    )
    if not entries:
        raise ValueError(f"User vocabulary entry {user_vocabulary_entry_id} does not exist")
    entry = UserVocabularyEntrySerializer(entries[0])
    word = entry.instance.word
    is_correct = False
    correct_answer = []
    extra_context = []
    words = [word]
    if question_type == QuestionType.HanziFromEnglish:
        correct_answer = [
            word.display
        ]
        is_correct = correct_answer == answer
    elif question_type == QuestionType.DefinitionsFromHanzi:
        for d in word.definitions.all():
            flattened_definition = d.definition.lower().strip()
            if not flattened_definition:
                continue
            correct_answer += [ d.strip() for d in flattened_definition.split(";") ]
        is_correct = answer[0].lower().strip() in correct_answer
        extra_context = [ a for a in correct_answer if a != answer[0].lower().strip() ]
    elif question_type == QuestionType.AccentsFromHanzi:
        pronunciation = word.pronunciation.split(" ")
        correct_answer = [
            str(get_tone_number_from_numeric_form(p)) for p in pronunciation
        ]
        extra_context = [
            ''.join([convert_to_display_form(p) for p in pronunciation])
        ]
        is_correct = answer == correct_answer
    else:
        raise ValueError(f"Unrecognized question type {question_type}")
    return CheckResponse(
        is_correct=is_correct,
        correct_answer=correct_answer,
        extra_context=extra_context,
        words=words,
    )
