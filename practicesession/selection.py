from typing import Dict, List, Set, NamedTuple, Optional
from uuid import UUID

import random

from django.db.models import QuerySet

from users.models import User
from quiz.models import QuizQuestion
from quiz.query import QuerySetType, get_queryset, get_queryset_for_user_and_type, filter_queryset_by_asking_date
from quiz.utils import get_usable_grammar_rule_examples

class _QuestionSelectionBucket(NamedTuple):
    question_ids: List[UUID]
    bucket_weight: int


class SelectionOutput(NamedTuple):
    question_id: UUID
    example_id: Optional[UUID]


def get_user_vocabulary_questions(
    user: User,
    number_of_questions: int = 6
) -> List[SelectionOutput]:
    return _make_selection_for_type(user, QuerySetType.Vocabulary, number_of_questions)


def get_grammar_rule_questions(
    user: User,
    number_of_questions: int = 6
) -> List[SelectionOutput]:
    return _make_selection_for_type(user, QuerySetType.GrammarRule, number_of_questions)

def _make_selection_for_type(
    user: User,
    queryset_type: QuerySetType,
    number_of_questions: int
) -> List[SelectionOutput]:
    queryset = get_queryset(queryset_type, user)
    selections: List[_QuestionSelectionBucket] = []
    for (
        days_since_asked_lower_bound,
        days_since_asked_upper_bound,
        should_include_unasked
    ) in [
        (10, 30, True),
        (5, 10, False),
        (1, 5, False),
    ]:
        questions = filter_queryset_by_asking_date(
            queryset,
            days_since_asked_lower_bound,
            days_since_asked_upper_bound,
            should_include_unasked
        ).order_by("number_of_times_displayed")
        selections.append(_get_questions(queryset_type, questions, number_of_questions))
    out = _select_questions(queryset_type, user, set(), selections, number_of_questions)
    if len(out) < number_of_questions:
        number_of_questions_left = number_of_questions - len(out)
        all_questions = QuizQuestion.objects.filter(
            user=user)
        if queryset_type == QuerySetType.Vocabulary:
            all_questions = all_questions.filter(user_vocabulary_entry__isnull=False)
        elif queryset_type == QuerySetType.GrammarRule:
            all_questions = all_questions.filter(user_grammar_rule_entry__isnull=False)
        out = _select_questions(queryset_type, user, out, [_get_questions(queryset_type, all_questions, number_of_questions_left)], number_of_questions_left)
    return list(out.values())


def _get_questions(
    queryset_type: QuerySetType,
    questions: QuerySet,
    stopping_length: int
) -> _QuestionSelectionBucket:
    out: Set[str] = set()
    while (
        len(out) < stopping_length and
        questions
    ):
        question = questions[0]
        if queryset_type == QuerySetType.Vocabulary and not question.user_vocabulary_entry in out:
            out.add(question.user_vocabulary_entry.id)
        elif queryset_type == QuerySetType.GrammarRule and not question.user_grammar_rule_entry in out:
            out.add(question.user_grammar_rule_entry.id)
        questions = questions[1:]
    weight = len(questions) + len(out)
    return _QuestionSelectionBucket(question_ids=list(out), bucket_weight=weight)


def _select_questions(
    queryset_type: QuerySetType,
    user: User,
    current_set: Dict[UUID, SelectionOutput],
    selections: List[_QuestionSelectionBucket],
    number_of_questions: int
) -> Dict[UUID, SelectionOutput]:
    out: Dict[UUID, SelectionOutput] = {}
    while len(selections) and len(out) < number_of_questions:
        choice_idx = random.choices(range(len(selections)), weights=[s.bucket_weight for s in selections])[0]
        question_id = selections[choice_idx].question_ids[0]
        if question_id in current_set or question_id in out:
            continue
        elif queryset_type == QuerySetType.Vocabulary:
            out[question_id] = SelectionOutput(
                question_id=question_id,
                example_id=None
            )
        elif queryset_type == QuerySetType.GrammarRule:
            example = (
                get_usable_grammar_rule_examples(user).filter(
                    grammar_rule=QuizQuestion.objects.filter(id=question_id).first().user_grammar_rule_entry.grammar_rule
                )
                .order_by("?")
                .first()
            )
            if not example:
                continue
            out[question_id] = SelectionOutput(
                question_id=question_id,
                example_id=example.id,
            )
        else:
            raise ValueError(f"Unsupported queryset type {queryset_type}")
        next_question_ids = selections[choice_idx].question_ids[1:]
        if len(next_question_ids):
            selections[choice_idx] = _QuestionSelectionBucket(
                bucket_weight=selections[choice_idx].bucket_weight,
                question_ids=next_question_ids,
            )
        else:
            selections = [ s for idx, s in enumerate(selections) if idx != choice_idx ]
    return out
