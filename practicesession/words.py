from uuid import UUID

from django.db.models import QuerySet

from .models import PracticeSessionQuestion

from users.models import User
from quiz.models import QuizQuestion
from quiz.query import QuerySetType, get_queryset_for_user_and_type


def get_word_questions_for_practice_session(
    user: User,
    practice_session_id: UUID
) -> QuerySet:
    user_vocabulary_questions = PracticeSessionQuestion.objects.filter(
        practice_session_id=practice_session_id,
        user_vocabulary_entry__isnull=False,
    ).values_list("user_vocabulary_entry", flat=True)
    queryset = get_queryset_for_user_and_type(QuerySetType.Vocabulary, user)
    return queryset.filter(
        user_vocabulary_entry__in=user_vocabulary_questions
    )
