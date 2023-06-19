from typing import Optional
import logging
import datetime

from random import randrange, choices

from django.db.models import Count
from django.http import HttpRequest

from .models import QuizQuestion, QuestionType
from django.utils import timezone
from usergrammarrules.models import UserGrammarRuleEntry

def select_next_grammar_rule_question(request: HttpRequest) -> Optional[QuizQuestion]:
    question = _maybe_get_unasked_grammar_rule(request)
    if question:
        return question
    question = _maybe_get_unasked_grammar_question(request)
    if question:
        return question
    return get_grammar_rule_question_from_all(request)

def _maybe_get_unasked_grammar_rule(request: HttpRequest) -> Optional[QuizQuestion]:
    question_type_choices = QuestionType.choices()
    question_type_index = randrange(0, len(question_type_choices), 1)
    unasked_questions = UserGrammarRuleEntry.objects.filter(user=request.user).exclude(
        id__in=QuizQuestion.objects.filter(
            user=request.user,
            user_grammar_rule_entry__isnull=False
        ).values_list('user_grammar_rule_entry', flat=True)
    )
    if not len(unasked_questions):
        return None
    next_question_index: int = randrange(0, len(unasked_questions), 1)
    next_question: UserGrammarRuleEntry = unasked_questions[next_question_index]
    return QuizQuestion(
        user=request.user,
        user_grammar_rule_entry=next_question,
        question_type=question_type_choices[question_type_index][0],
        number_of_times_displayed=0
    )


def _maybe_get_unasked_grammar_question(request: HttpRequest) -> Optional[QuizQuestion]:
    """There is a bit of nuance between this function and _maybe_get_unasked_grammar_rule

    _maybe_get_unasked_grammar_rule will pick a grammar rule that has never been asked
    and this will pick a word that does not have all the question types
    """
    question_type_choices = QuestionType.choices()
    questions_by_type = (
        QuizQuestion.objects.filter(user=request.user, user_grammar_rule_entry__isnull=False)
            .values('user_grammar_rule_entry')
            .annotate(dcount=Count('user_grammar_rule_entry'))
            .order_by()
    )
    potential_rules = []
    for q in questions_by_type:
        if q['dcount'] == len(question_type_choices):
            continue
        potential_rules.append(q['user_grammar_rule_entry'])
    if not potential_rules:
        return None
    potential_rule_index = randrange(0, len(potential_rules), 1)
    next_potential_rule = potential_rules[potential_rule_index]
    questions_for_rule = (
        QuizQuestion.objects.filter(
            user=request.user, user_grammar_rule_entry=next_potential_rule).all()
    )
    for q in questions_for_rule:
        question_type_choices = list(filter(lambda x: x[0] != q.question_type, question_type_choices))
    logging.warn(questions_for_rule)
    logging.warn(question_type_choices)
    if not question_type_choices:
        logging.warn("Question types are exhausted")
        return None
    next_question_type_index = randrange(0, len(question_type_choices), 1)
    user_grammar_rule_entry = UserGrammarRuleEntry.objects.filter(id=next_potential_rule)
    return QuizQuestion(
        user=request.user,
        user_grammar_rule_entry=user_grammar_rule_entry[0],
        question_type=question_type_choices[next_question_type_index][0],
        number_of_times_displayed=0
    )


def get_grammar_rule_question_from_all(request: HttpRequest, bound_by_time: bool = True) -> Optional[QuizQuestion]:
    bounding_time = timezone.now() + datetime.timedelta(hours=1)
    if bound_by_time:
        bounding_time = timezone.now() - datetime.timedelta(hours=1)
    questions = list(
        QuizQuestion.objects.filter(user=request.user, last_displayed_at__lt=bounding_time, user_grammar_rule_entry__isnull=False)
            .order_by("-number_of_times_displayed")
            .all()
    )
    if not questions:
        return None
    weights = []
    max_display: Optional[int] = None
    for q in questions:
        if max_display is None:
            max_display = q.number_of_times_displayed + 1
        weights.append(max_display - q.number_of_times_displayed)
    return choices(questions, weights, k=1)[0]

