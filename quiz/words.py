from typing import Optional
import datetime

from django.db.models import QuerySet, Count, Q
from django.utils import timezone

from users.models import User
from practicesession.models import PracticeSessionQuestion

from .models import QuizQuestion, QuestionType
from uservocabulary.models import UserVocabularyEntry

def get_queryset_from_user_vocabulary(user: User, practice_session_id: Optional[str]) -> Optional[QuerySet]:
    _ensure_all_possible_quiz_records(user)
    question_set = QuizQuestion.objects.filter(
        user=user,
        user_vocabulary_entry__isnull=False
    )
    if practice_session_id:
        question_set = question_set.filter(
            user_vocabulary_entry__in=PracticeSessionQuestion.objects.filter(
                practice_session_id=practice_session_id,
                user_vocabulary_entry__isnull=False
            ).values_list("user_vocabulary_entry", flat=True)
        )
    unasked_questions = question_set.filter(
        number_of_times_displayed=0
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
        questions = get_questions_by_asking_date(
            user, days_since_asked_lower_bound, days_since_asked_upper_bound, question_set
        )
        if questions:
            return questions
    return question_set.order_by("?")


def get_questions_by_asking_date(
    user: User,
    days_since_asked_lower_bound: int,
    days_since_asked_upper_bound: int,
    include_not_asked: bool = False,
    question_set: Optional[QuerySet] = None
) -> Optional[QuerySet]:
    if not question_set:
        _ensure_all_possible_quiz_records(user)
        question_set = QuizQuestion.objects.filter(
            user=user,
            user_vocabulary_entry__isnull=False
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
        user_vocabulary_entry__isnull=False
    ).order_by("?")
    if questions:
        return questions
    return None



def _ensure_all_possible_quiz_records(user: User) -> None:
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
