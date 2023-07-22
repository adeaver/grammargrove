from typing import Optional
import datetime
import logging

from django.db.models import Q, Count, QuerySet

from users.models import User
from practicesession.models import PracticeSessionQuestion

from .models import QuizQuestion, QuestionType
from django.utils import timezone
from usergrammarrules.models import UserGrammarRuleEntry
from grammarrules.models import GrammarRuleExample, GrammarRuleExamplePrompt
from userpreferences.models import UserPreferences

def get_queryset_from_user_grammar(user: User, practice_session_id: Optional[str]) -> Optional[QuerySet]:
    _ensure_all_possible_quiz_records(user)
    usable_grammar_rules = get_usable_grammar_rule_examples(user)
    user_grammar_rules_with_examples = UserGrammarRuleEntry.objects.filter(
        user=user,
        grammar_rule__in=usable_grammar_rules.values_list("grammar_rule", flat=True)
    ).values_list("id", flat=True)
    if not user_grammar_rules_with_examples:
        return None
    question_set = QuizQuestion.objects.filter(
        user=user,
        user_grammar_rule_entry__isnull=False,
        user_grammar_rule_entry__in=user_grammar_rules_with_examples
    )
    if practice_session_id:
        question_set = question_set.filter(
            user_grammar_rule_entry__in=PracticeSessionQuestion.objects.filter(
                practice_session_id=practice_session_id,
                user_grammar_rule_entry__isnull=False
            ).values_list("user_grammar_rule_entry", flat=True)
        )
    unasked_questions = question_set.filter(
        number_of_times_displayed=0,
    ).order_by("?")
    if unasked_questions:
        return unasked_questions
    for (
        days_since_asked_lower_bound,
        days_since_asked_upper_bound
    ) in [
        (1, 3),
        (3, 5),
        (20, 30),
        (10, 20),
        (5, 10),
    ]:
        questions = get_questions_by_asking_date(user, days_since_asked_lower_bound, days_since_asked_upper_bound)
        if questions:
            return questions
    return QuizQuestion.objects.filter(
            user=user,
            user_grammar_rule_entry__isnull=False,
            user_grammar_rule_entry__in=user_grammar_rules_with_examples
    ).order_by("?")


def get_grammar_rule_questions_queryset_for_user(user: User) -> QuerySet:
    usable_grammar_rules = get_usable_grammar_rule_examples(user)
    user_grammar_rules_with_examples = UserGrammarRuleEntry.objects.filter(
        user=user,
        grammar_rule__in=usable_grammar_rules.values_list("grammar_rule", flat=True)
    ).values_list("id", flat=True)
    return QuizQuestion.objects.filter(
            user=user,
            user_grammar_rule_entry__isnull=False,
            user_grammar_rule_entry__in=user_grammar_rules_with_examples
    ).order_by("?")


def get_questions_by_asking_date(
    user: User,
    days_since_asked_lower_bound: int,
    days_since_asked_upper_bound: int,
    include_not_asked: bool = False,
    question_set: Optional[QuerySet] = None
) -> Optional[QuerySet]:
    if not question_set:
        _ensure_all_possible_quiz_records(user)
        usable_grammar_rules = get_usable_grammar_rule_examples(user)
        user_grammar_rules_with_examples = UserGrammarRuleEntry.objects.filter(
            user=user,
            grammar_rule__in=usable_grammar_rules.values_list("grammar_rule", flat=True)
        ).values_list("id", flat=True)
        question_set = QuizQuestion.objects.filter(
            user=user,
            user_grammar_rule_entry__isnull=False,
            user_grammar_rule_entry__in=user_grammar_rules_with_examples
        )
    upper_bound = timezone.now() - datetime.timedelta(
        days=days_since_asked_lower_bound
    )
    lower_bound = timezone.now() - datetime.timedelta(
        days=days_since_asked_upper_bound
    )
    if include_not_asked:
        questions = question_set.filter(
            Q(number_of_times_displayed=0) | Q(last_displayed_at__gt=lower_bound, last_displayed_at__lt=upper_bound)
        ).order_by("?")
        if not questions:
            return None
        return questions
    questions = question_set.filter(
        last_displayed_at__lt=upper_bound,
        last_displayed_at__gt=lower_bound,
    ).order_by("?")
    if questions:
        return questions
    return None


def _ensure_all_possible_quiz_records(user: User) -> None:
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


def get_usable_grammar_rule_examples(user: User) -> None:
    queryset = GrammarRuleExample.objects.filter(
        parse_error__isnull=True,
        grammar_rule_example_prompt__in=GrammarRuleExamplePrompt.objects.filter(
            is_usable=True
        ),
        grammar_rule__in=UserGrammarRuleEntry.objects.filter(
            user=user
        ).values_list("grammar_rule", flat=True)
    )
    user_preferences = UserPreferences.objects.filter(user=user)
    if user_preferences and user_preferences[0].hsk_level:
       return queryset.filter(max_hsk_level__lte=user_preferences[0].hsk_level)
    return queryset
