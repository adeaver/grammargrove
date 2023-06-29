from typing import List

from grammarrules.models import GrammarRuleExample
from grammarrules.serializers import GrammarRuleExampleSerializer

from uservocabulary.models import UserVocabularyEntry
from uservocabulary.serializers import UserVocabularyEntrySerializer

from .models import QuestionType
from .serializers import CheckResponse

def check_grammar_rule(
    question_type: QuestionType,
    example_id: str,
    answer: List[str]
) -> CheckResponse:
    examples = GrammarRuleExample.objects.filter(
        id=example_id
    )
    if not examples:
        raise ValueError(f"Example {example_id} does not exist")
    example = GrammarRuleExampleSerializer(examples[0]).data
    correct_answer = []
    if question_type == QuestionType.HanziFromEnglish:
        correct_answer = [
            ''.join([
                c["word"]["display"] for c in example["grammar_rule_example_components"]
            ])
        ]
    elif question_type == QuestionType.AccentsFromHanzi:
        for c in example["grammar_rule_example_components"]:
            pronunciation = c["word"]["pronunciation"].split(" ")
            correct_answer += [
                p[-1] for p in pronunciation
            ]
    elif question_type == QuestionType.DefinitionsFromHanzi:
        correct_answer = [
            example["english_definition"].lower()
        ]
    else:
        raise ValueError(f"Unrecognized question type {question_type}")
    return CheckResponse(
        is_correct=correct_answer == answer,
        correct_answer=correct_answer
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
    entry = UserVocabularyEntrySerializer(entries[0]).data
    is_correct = False
    correct_answer = []
    if question_type == QuestionType.HanziFromEnglish:
        correct_answer = [
            entry["word"]["display"]
        ]
        is_correct = correct_answer == answer
    elif question_type == QuestionType.DefinitionsFromHanzi:
        correct_answer = [
            d.lower().strip() for d in entry["word"]["definitions"] if len(d.strip())
        ]
        is_correct = answer[0].lower().strip() in correct_answer
    elif question_type == QuestionType.AccentsFromHanzi:
        correct_answer = [
            p[-1] for p in entry["word"]["pronunciation"].split(" ")
        ]
        is_correct = answer == correct_answer
    else:
        raise ValueError(f"Unrecognized question type {question_type}")
    return CheckResponse(
        is_correct=is_correct,
        correct_answer=correct_answer,
    )
