from typing import Optional
import logging
import datetime

from random import randrange, choices

from django.db.models import Count
from django.utils import timezone
from django.http import HttpRequest

from .models import QuizQuestion, QuestionType, get_word_from_question
from uservocabulary.models import UserVocabularyEntry
from words.models import Word, Definition, LanguageCode

def select_next_word_question(request: HttpRequest) -> Optional[QuizQuestion]:
    question = _maybe_get_unasked_word(request)
    if question:
        return question
    question = _maybe_get_unasked_word_question(request)
    if question:
        return question
    question = get_word_question_from_all(request)
    if question:
        return question
    return None

def _maybe_get_unasked_word(request: HttpRequest) -> Optional[QuizQuestion]:
    question_type_choices = QuestionType.choices()
    question_type_index = randrange(0, len(question_type_choices), 1)
    unasked_questions = UserVocabularyEntry.objects.exclude(
        id__in=QuizQuestion.objects.filter(user=request.user).values_list('user_vocabulary_entry', flat=True)
    )
    if not len(unasked_questions):
        return None
    next_question_index: int = randrange(0, len(unasked_questions), 1)
    next_question: UserVocabularyEntry = unasked_questions[next_question_index]
    return QuizQuestion(
        user=request.user,
        user_vocabulary_entry=next_question,
        question_type=question_type_choices[question_type_index][0],
        number_of_times_displayed=0
    )

def _maybe_get_unasked_word_question(request: HttpRequest) -> Optional[QuizQuestion]:
    """There is a bit of nuance between this function and _maybe_get_unasked_word

    _maybe_get_unasked_word will pick a word that has never been asked
    and this will pick a word that does not have all the question types
    """
    question_type_choices = QuestionType.choices()
    questions_by_type = (
        QuizQuestion.objects.filter(user=request.user)
            .values('user_vocabulary_entry')
            .annotate(dcount=Count('user_vocabulary_entry'))
            .order_by()
    )
    potential_words = []
    for q in questions_by_type:
        if q['dcount'] == len(question_type_choices):
            break
        potential_words.append(q['user_vocabulary_entry'])
    if not potential_words:
        return None
    potential_word_index = randrange(0, len(potential_words), 1)
    next_potential_word = potential_words[potential_word_index]
    questions_for_word = (
        QuizQuestion.objects.filter(
            user=request.user, user_vocabulary_entry=next_potential_word).all()
    )
    for q in questions_for_word:
        question_type_choices = list(filter(lambda x: x[0] != q.question_type, question_type_choices))
    logging.warn(questions_for_word)
    logging.warn(question_type_choices)
    if not question_type_choices:
        logging.warn("Question types are exhausted")
        return None
    next_question_type_index = randrange(0, len(question_type_choices), 1)
    user_vocabulary_entry = UserVocabularyEntry.objects.filter(id=next_potential_word)
    return QuizQuestion(
        user=request.user,
        user_vocabulary_entry=user_vocabulary_entry[0],
        question_type=question_type_choices[next_question_type_index][0],
        number_of_times_displayed=0
    )

def get_word_question_from_all(request: HttpRequest, bound_by_time: bool = True) -> Optional[QuizQuestion]:
    bounding_time = timezone.now() + datetime.timedelta(hours=1)
    if bound_by_time:
        bounding_time = timezone.now() - datetime.timedelta(hours=1)
    questions = list(
        QuizQuestion.objects.filter(user=request.user, last_displayed_at__lt=bounding_time)
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

