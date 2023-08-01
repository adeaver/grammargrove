from typing import Optional
from enum import Enum

import datetime

from django.db.models import Q, QuerySet, Count
from django.utils import timezone

from users.models import User
from practicesession.models import PracticeSessionQuestion
from uservocabulary.models import UserVocabularyEntry
from usergrammarrules.models import UserGrammarRuleEntry

from practicesession.utils import get_finished_quiz_question_ids

from .models import QuizQuestion, QuestionType
from .utils import get_user_grammar_rules_with_valid_examples, get_user_vocabulary_entries_with_valid_definitions

class QuerySetType(Enum):
    GrammarRule = 'grammar-rule'
    Vocabulary = 'vocabulary'

def get_queryset(
    queryset_type: QuerySetType,
    user: User,
    practice_session_id: Optional[str] = None
) -> Optional[QuerySet]:
    queryset = get_queryset_for_user_and_type(
        queryset_type,
        user
    )
    if practice_session_id:
        return _filter_queryset_for_practice_session_id(
            queryset_type, practice_session_id, queryset
        ).order_by("-last_displayed_at")
    for (
        days_since_asked_lower_bound,
        days_since_asked_upper_bound,
        should_include_unasked
    ) in [
        (1, 3, True),
        (3, 5, False),
        (20, 30, False),
        (10, 20, False),
        (5, 10, False),
    ]:
        filtered_queryset = filter_queryset_by_asking_date(
            queryset, days_since_asked_lower_bound, days_since_asked_upper_bound, should_include_unasked
        )
        if filtered_queryset:
            return filtered_queryset.order_by("?")
    return queryset.order_by("?")

def _filter_question_set_by_type(
    user: User,
    current_queryset: QuerySet,
    queryset_type: QuerySetType,
) -> QuerySet:
    if queryset_type == QuerySetType.GrammarRule:
        usable_grammar_rules = get_user_grammar_rules_with_valid_examples(
            user
        ).values_list("id", flat=True)
        return current_queryset.filter(
            user_grammar_rule_entry__isnull=False,
            user_grammar_rule_entry__in=usable_grammar_rules,
        )
    elif queryset_type == QuerySetType.Vocabulary:
        usable_vocabulary_entries = get_user_vocabulary_entries_with_valid_definitions(
            user
        ).values_list("id", flat=True)
        return current_queryset.filter(
            user_vocabulary_entry__isnull=False
        )
    else:
        raise AssertionError(
            f"QuerySet type {queryset_type} is unrecognized"
        )

def _filter_queryset_for_practice_session_id(
    queryset_type: QuerySetType,
    practice_session_id: str,
    current_queryset: QuerySet
) -> QuerySet:
    current_queryset = current_queryset.exclude(
        id__in=get_finished_quiz_question_ids(practice_session_id)
    )
    if queryset_type == QuerySetType.GrammarRule:
        return current_queryset.filter(
            user_grammar_rule_entry__in=PracticeSessionQuestion.objects.filter(
                practice_session_id=practice_session_id,
                user_grammar_rule_entry__isnull=False,
            ).values_list("user_grammar_rule_entry", flat=True)
        )
    elif queryset_type == QuerySetType.Vocabulary:
        return current_queryset.filter(
            user_vocabulary_entry__in=PracticeSessionQuestion.objects.filter(
                practice_session_id=practice_session_id,
                user_vocabulary_entry__isnull=False,
            ).values_list("user_vocabulary_entry", flat=True)
        )
    else:
        raise AssertionError(
            f"QuerySet type {queryset_type} is unrecognized"
        )

def get_queryset_for_user_and_type(
    queryset_type: QuerySetType,
    user: User,
) -> QuerySet:
    build_complete_queryset(user)
    question_set = QuizQuestion.objects.filter(
        user=user
    )
    return _filter_question_set_by_type(
        user, question_set, queryset_type
    )


def filter_queryset_by_asking_date(
    current_queryset: QuerySet,
    days_since_asked_lower_bound: int,
    days_since_asked_upper_bound: int,
    include_not_asked: bool = False,
) -> QuerySet:
    upper_bound = timezone.now() - datetime.timedelta(
        days=days_since_asked_upper_bound
    )
    lower_bound = timezone.now() - datetime.timedelta(
        days=days_since_asked_lower_bound
    )
    filter_query = (
        Q(number_of_times_displayed=0) | (Q(last_displayed_at__lt=lower_bound) & Q(last_displayed_at__gt=upper_bound))
    ) if include_not_asked else (
        (Q(last_displayed_at__lt=lower_bound) & Q(last_displayed_at__gt=upper_bound))
    )
    return current_queryset.filter(filter_query)

def build_complete_queryset(user: User) -> None:
    _ensure_all_possible_user_vocabulary_quiz_records(user)
    _ensure_all_possible_grammar_rule_quiz_records(user)

def _ensure_all_possible_user_vocabulary_quiz_records(user: User) -> None:
    user_vocabulary_entries = UserVocabularyEntry.objects.exclude(
        id__in=QuizQuestion.objects.filter(
            user=user, user_vocabulary_entry__isnull=False).
            values_list("user_vocabulary_entry", flat=True)
    ).filter(user=user)
    if user_vocabulary_entries:
        for entry in user_vocabulary_entries:
            for k, v in QuestionType.choices():
                q = QuizQuestion(
                    question_type=k,
                    user=user,
                    user_vocabulary_entry=entry,
                )
                q.save()
    questions_by_type = (
        QuizQuestion.objects.filter(user=user, user_vocabulary_entry__isnull=False)
            .values('user_vocabulary_entry')
            .annotate(dcount=Count('user_vocabulary_entry'))
            .exclude(dcount=len(QuestionType.choices()))
    )
    if questions_by_type:
        user_vocabulary_entries = UserVocabularyEntry.objects.filter(id__in=[q["user_vocabulary_entry"] for q in questions_by_type])
        for entry in user_vocabulary_entries:
            questions_for_word = set(
                list(
                    QuizQuestion.objects.filter(
                        user=user, user_vocabulary_entry=entry).values_list("question_type", flat=True)
                )
            )
            for k, v in QuestionType.choices():
                if k not in questions_for_word:
                    q = QuizQuestion(
                        question_type=k,
                        user=user,
                        user_vocabulary_entry=entry,
                    )
                    q.save()

def _ensure_all_possible_grammar_rule_quiz_records(user: User) -> None:
    user_grammar_rule_entries = UserGrammarRuleEntry.objects.exclude(
        id__in=QuizQuestion.objects.filter(
            user=user, user_grammar_rule_entry__isnull=False
        ).values_list("user_grammar_rule_entry", flat=True)
    ).filter(user=user)
    if user_grammar_rule_entries:
        for entry in user_grammar_rule_entries:
            for k, v in QuestionType.choices():
                q = QuizQuestion(
                    question_type=k,
                    user=user,
                    user_grammar_rule_entry=entry
                )
                q.save()
    questions_by_type = (
        QuizQuestion.objects.filter(user=user, user_grammar_rule_entry__isnull=False)
            .values('user_grammar_rule_entry')
            .annotate(dcount=Count('user_grammar_rule_entry'))
            .exclude(dcount=len(QuestionType.choices()))
    )
    if questions_by_type:
        user_grammar_rule_entries = UserGrammarRuleEntry.objects.filter(
            id__in=[ q["user_grammar_rule_entry"] for q in questions_by_type ]
        )
        for entry in user_grammar_rule_entries:
            questions_for_word = set(
                list(
                    QuizQuestion.objects.filter(
                        user=user, user_grammar_rule_entry=entry).values_list("question_type", flat=True)
                )
            )
            for k, v in QuestionType.choices():
                if k not in questions_for_word:
                    q = QuizQuestion(
                        question_type=k,
                        user=user,
                        user_grammar_rule_entry=entry,
                    )
                    q.save()
