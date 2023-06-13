from random import randrange, choices
from typing import Optional
import datetime

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError
)

from .models import QuizQuestion, QuestionType
from uservocabulary.models import UserVocabularyEntry
from words.models import Word, Definition

class QuizViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def next(self, request: HttpRequest) -> HttpResponse:
        class QuestionResponse(NamedTuple):
            question_id: str
            display: str

        if not request.user:
            return HttpResponseForbidden()
        question = _select_next_word_question(request)
        if not question:
            # TODO: gracefully handle this case
            return HttpResponseBadRequest()
        question.number_of_times_displayed += 1
        question.save()
        display = _get_display_from_question(question)
        return JsonResponse(QuestionResponse(question_id=question.id, display=display)._asdict())

    @action(detail=True, methods=['post'])
    def check(self, request: HttpRequest) -> HttpResponse:
        return HttpResponseBadRequest()


def _select_next_word_question(request: HttpRequest) -> Optional[QuizQuestion]:
    question = _maybe_get_unasked_word(request)
    if question:
        return question
    question = _maybe_get_unasked_question(request)
    if question:
        return question
    question = _get_question_from_all(request)
    if question:
        return question
    return _get_question_from_all(request, False)

def _maybe_get_unasked_word(request: HttpRequest) -> Optional[QuizQuestion]:
    question_type_choices = QuestionType.choices()
    question_type_index = randrange(0, len(question_type_choices), 1)
    unasked_questions = UserVocabularyEntry.objects.exclude(
        id__in=QuizQuestion.objects.filter(user=request.user).values_list('id', flat=True)
    )
    if not len(unasked_questions):
        return None
    next_question_index: int = randrange(0, len(unasked_questions), 1)
    next_question: UserVocabularyEntry = unasked_questions[next_question_index]
    return QuizQuestion(
        user=request.user,
        user_vocabulary_entry=next_question,
        question_type=question_type_choices[question_type_index],
        number_of_times_displayed=0
    )

def _maybe_get_unasked_question(request: HttpRequest) -> Optional[QuizQuestion]:
    """There is a bit of nuance between this function and _maybe_get_unasked_word

    _maybe_get_unasked_word will pick a word that has never been asked
    and this will pick a word that does not have all the question types
    """
    question_type_choices = QuestionType.choices()
    questions_by_type = (
        QuizQuestion.objects.filter(user=request.user)
            .values('uservocabularyentry')
            .annotate(dcount=Count('count'))
            .order_by('count')
    )
    potential_words = []
    for q in questions_by_type:
        if q['count'] == len(question_type_choices):
            break
        potential_words.append(q['uservocabularyentry'])
    if not potential_words:
        return None
    potential_word_index = randrange(0, len(potential_words), 1)
    next_potential_word = potential_words[potential_word_index]
    questions_for_word = (
        QuizQuestion.objects.filter(
            user=request.user, user_vocabulary_entry=next_potential_word).all()
    )
    for q in questions_for_word:
        question_type_choices = list(filter(question_type_choices, lambda x: x != q.question_type))
    if not question_type_choices:
        logging.warn("Question types are exhausted")
        return None
    next_question_type_index = randrange(0, len(question_type_choices), 1)
    return QuizQuestion(
        user=request.user,
        user_vocabulary_entry=next_potential_word,
        question_type=question_type_choices[next_question_type_index],
        number_of_times_displayed=0
    )

def _get_question_from_all(request: HttpRequest, bound_by_time: bool = True) -> Optional[QuizQuestion]:
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
    return choices(questions, weights)

def _get_display_from_question(question: QuizQuestion) -> str:
    vocabulary_entry = UserVocabularyEntry.objects.filter(question.user_vocabulary_entry).all()[0]
    word: Word = Word.objects.filter(id=vocabulary_entry.word).all()[0]
    if question.question_type in [QuestionType.AccentsFromHanzi, QuestionType.DefinitionsFromHanzi]:
        return word.display
    elif question.question_type == QuestionType.HanziFromEnglish:
        if vocabulary_entry.notes:
            return vocabulary_entry.notes
        definitions = Definition.objects.filter(word=word, language_code=LanguageCode.ENGLISH).all()
        return "\n".join([ d.definition for d in definition ])
    else:
        raise AssertionError(f"Unsupported Question Type {question.question_type}")




