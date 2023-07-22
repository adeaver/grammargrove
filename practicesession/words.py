from typing import List, Set
from uuid import UUID

from django.db.models import QuerySet

from users.models import User
from quiz.models import QuizQuestion
from quiz.query import QuerySetType, get_queryset, filter_queryset_by_asking_date

def get_user_vocabulary_questions(
    user: User,
    number_of_questions: int = 6
) -> List[UUID]:
    num_questions_for_group = number_of_questions // 3
    queryset = get_queryset(QuerySetType.Vocabulary, user)
    out: Set[UUID] = set([])
    for (
        days_since_asked_lower_bound,
        days_since_asked_upper_bound,
        should_include_unasked
    ) in [
        (1, 5, True),
        (5, 10, False),
        (10, 30, False)
    ]:
        questions = filter_queryset_by_asking_date(
            queryset,
            days_since_asked_lower_bound,
            days_since_asked_upper_bound,
            should_include_unasked
        )
        out = _get_questions(out, questions, num_questions_for_group)
    all_questions = QuizQuestion.objects.filter(
            user=user, user_vocabulary_entry__isnull=False)
    return list(
        _get_questions(out, all_questions, number_of_questions - len(out))
    )


def _get_questions(
    current_set: Set[UUID],
    questions: QuerySet,
    number_of_questions_per_group: int
) -> Set[UUID]:
    stopping_length = len(current_set) + number_of_questions_per_group
    out: Set[str] = current_set
    while (
        len(out) < stopping_length and
        questions
    ):
        question = questions[0]
        if not question.user_vocabulary_entry in out:
            out.add(question.user_vocabulary_entry.id)
        questions = questions[1:]
    return out
