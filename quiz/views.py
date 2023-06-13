import logging
from random import randrange, choices
from typing import Optional, NamedTuple
import datetime

from django.db.models import Count
from django.utils import timezone
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

from .models import QuizQuestion, QuestionType, get_word_from_question
from uservocabulary.models import UserVocabularyEntry
from words.models import Word, Definition, LanguageCode

class QuizViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def next(self, request: HttpRequest) -> HttpResponse:
        class QuestionResponse(NamedTuple):
            question_id: str
            vocabulary_entry_id: Optional[str]
            display: str
            question_type: int
            answer_spaces: Optional[int]

        if not request.user:
            return HttpResponseForbidden()
        question = _select_next_word_question(request)
        if not question:
            # TODO: gracefully handle this case
            return HttpResponseBadRequest()
        question.number_of_times_displayed += 1
        question.last_displayed_at = timezone.now()
        question.save()
        display = _get_display_from_question(question)
        return JsonResponse(
            QuestionResponse(
                question_id=question.id,
                display=display.display,
                question_type=question.question_type,
                answer_spaces=display.answer_spaces,
                vocabulary_entry_id=display.vocabulary_entry_id
            )._asdict()
        )

    @action(detail=False, methods=['post'])
    def check(self, request: HttpRequest) -> HttpResponse:
        class CheckQuestionResponse(NamedTuple):
            correct: bool
            correct_answer: Optional[str]

        if not request.user:
            return HttpResponseForbidden()
        question_id = request.data.get("question_id")
        if not question_id:
            return HttpResponseBadRequest()
        answer = request.data.get("answer")
        if not answer:
            return HttpResponseBadRequest()
        question = QuizQuestion.objects.filter(
            user=request.user, id=question_id
        )
        if not question:
            return HttpResponseBadRequest()
        if question.user_vocabulary_entry:
            word_payload = get_word_from_question(question, LanguageCode.ENGLISH)
            if question.question_type == QuestionType.HanziFromEnglish:

            elif question.question_type == QuestionType.AccentsFromHanzi:

            elif question.question_type == QuestionType.DefinitionsFromHanzi:

            else:
                return HttpResponseServerError()
        else:
            return HttpResponseServerError()




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

def _maybe_get_unasked_question(request: HttpRequest) -> Optional[QuizQuestion]:
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
    return choices(questions, weights, k=1)[0]

class QuestionDisplay(NamedTuple):
    answer_spaces: Optional[int]
    display: str
    vocabulary_entry_id: str

def _get_display_from_question(question: QuizQuestion) -> QuestionDisplay:
    vocabulary_entry = UserVocabularyEntry.objects.filter(id=question.user_vocabulary_entry.id).all()
    if not vocabulary_entry:
        raise AssertionError(f"User vocabulary {question.user_vocabulary_entry.id} does not exist")
    word: Word = Word.objects.filter(id=vocabulary_entry[0].word.id)
    if not word:
        raise AssertionError(f"Word {vocabulary_entry.word.id} does not exist")
    display: str = ""
    answer_spaces: Optional[int] = None
    if question.question_type in [QuestionType.AccentsFromHanzi, QuestionType.DefinitionsFromHanzi]:
        # Some words are displayed with fewer characters than they are said with
        # So the normal pronunciation screen won't work
        answer_spaces = None if (
            question.question_type != QuestionType.AccentsFromHanzi or
            len(word[0].pronunciation.split(" ")) == len(word[0].display)
        ) else len(word[0].pronunciation.split(" "))
        display = word[0].display
    elif question.question_type == QuestionType.HanziFromEnglish:
        answer_spaces = None
        if vocabulary_entry[0].notes:
            display = vocabulary_entry.notes
        else:
            definitions = Definition.objects.filter(word=word[0].id, language_code=LanguageCode.ENGLISH).all()
            display = "\n".join([ d.definition for d in definitions ]), None
    else:
        raise AssertionError(f"Unsupported Question Type {question.question_type}")
    return QuestionDisplay(
        answer_spaces=answer_spaces,
        display=display,
        vocabulary_entry_id=vocabulary_entry[0].id
    )
