from typing import List

import logging
import re

from grammargrove.pinyin_utils import (
    get_tone_number_from_numeric_form,
    get_tone_number_from_display_form,
    convert_to_display_form
)
from grammargrove.text_utils import remove_punctuation, remove_punctuation_from_hanzi

from users.models import User

from usergrammarrules.models import UserGrammarRuleNote
from grammarrules.models import GrammarRuleExample
from grammarrules.serializers import GrammarRuleExampleSerializer

from uservocabulary.models import UserVocabularyEntry, UserVocabularyNote
from uservocabulary.serializers import UserVocabularyEntrySerializer

from .models import QuestionType
from .serializers import CheckResponse

def check_grammar_rule(
    user: User,
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
        is_correct = correct_answer == answer
    elif question_type == QuestionType.AccentsFromHanzi:
        for c in serialized_example["grammar_rule_example_components"]:
            pronunciation = c["word"]["pronunciation"].split(" ")
            correct_answer += [
                str(get_tone_number_from_display_form(p)) for p in pronunciation
            ]
            extra_context.append(
                ''.join(pronunciation)
            )
        is_correct = correct_answer == answer
    elif question_type == QuestionType.DefinitionsFromHanzi:
        correct_answer = [
            remove_punctuation(serialized_example["english_definition"].lower().strip())
        ]
        is_correct = correct_answer == answer
        if not is_correct:
            notes = UserGrammarRuleNote.objects.filter(user=user, example_id=example.id)
            for n in notes:
                stripped_note = [ re.sub("\s\s+" , " ", n.note.lower().strip()) ]
                if answer == stripped_note:
                    is_correct = True
                    break
    else:
        raise ValueError(f"Unrecognized question type {question_type}")
    return CheckResponse(
        is_correct=is_correct,
        correct_answer=correct_answer,
        extra_context=extra_context,
        words=[],
        is_practice_session_complete=False,
        terms_mastered=None,
        total_number_of_terms=None,
        total_number_of_questions=None,
        number_of_questions_answered_correctly=None,
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
            if not flattened_definition or d.contains_hanzi:
                continue
            correct_answer += [ re.sub("\s\s+" , " ", d.strip()) for d in flattened_definition.split(";") ]
        user_answer = re.sub("\s\s+" , " ", answer[0].lower().strip())
        for acceptable_answer in correct_answer:
            if user_answer == acceptable_answer:
                is_correct = True
            else:
                alternate_answer: List[str] = []
                answer_parts = acceptable_answer.split(" ")
                for a in answer_parts:
                    if not re.match("\(.*\)", a.strip()):
                        alternate_answer.append(a.strip())
                if len(alternate_answer) and user_answer == " ".join(alternate_answer):
                    is_correct = True
                else:
                    extra_context.append(acceptable_answer)
        if not is_correct:
            notes = UserVocabularyNote.objects.filter(
                user_vocabulary_entry=entries[0]
            ).all()
            logging.warn(notes)
            for n in notes:
                stripped_note = re.sub("\s\s+" , " ", n.note.lower().strip())
                if user_answer == stripped_note:
                    is_correct = True
                    break
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
        is_practice_session_complete=False,
        terms_mastered=None,
        total_number_of_terms=None,
        total_number_of_questions=None,
        number_of_questions_answered_correctly=None,
    )
