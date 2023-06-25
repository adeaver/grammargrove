from typing import Optional
import logging
import datetime

from django.db.models import QuerySet

from random import randrange, choices

from django.db.models import Count
from django.utils import timezone
from django.http import HttpRequest

from users.models import User

from .models import QuizQuestion, QuestionType, get_word_from_question
from uservocabulary.models import UserVocabularyEntry

def get_queryset_from_user_vocabulary(user: User) -> Optional[QuerySet]:
    _ensure_all_possible_quiz_records(user)
    unasked_questions = QuizQuestion.objects.filter(
        user=user, number_of_times_displayed=0
    )
    if unasked_questions:
        return unasked_questions
    for number_of_days_since_asked in [ 30, 7, 1 ]:
        bounding_time = timezone.now() - datetime.timedelta(
            days=number_of_days_since_asked
        )
        questions = QuizQuestion.objects.filter(
            user=user, last_displayed_at__lt=bounding_time, user_vocabulary_entry__isnull=False).order_by("?")
        if questions:
            return questions
    return QuizQuestion.objects.filter(
            user=user, user_vocabulary_entry__isnull=False
    ).order_by("?")



def _ensure_all_possible_quiz_records(user: User) -> None:
    user_vocabulary_entries = UserVocabularyEntry.objects.exclude(
        id__in=QuizQuestion.objects.filter(
            user=user, user_vocabulary_entry__isnull=False).
            values_list("user_vocabulary_entry", flat=True)
    )
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
        for potential_question in questions_by_type:
            user_vocabulary_entry_id = potential_question["user_vocabulary_entry"]
            questions_for_word = set(
                list(
                    QuizQuestion.objects.filter(
                        user=user, user_vocabulary_entry=user_vocabulary_entry_id).values_list("question_type", flat=True)
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
