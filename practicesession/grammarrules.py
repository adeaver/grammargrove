from uuid import UUID

from django.db.models import QuerySet

from .models import PracticeSessionQuestion

from users.models import User
from quiz.query import QuerySetType, get_queryset_for_user_and_type

def get_grammar_rule_questions_for_practice_session(
    user: User,
    practice_session_id: UUID
) -> QuerySet:
    practice_session_questions = PracticeSessionQuestion.objects.filter(
        practice_session_id=practice_session_id,
        user_grammar_rule_entry__isnull=False,
    ).values_list("user_grammar_rule_entry", flat=True)
    queryset = get_queryset_for_user_and_type(QuerySetType.GrammarRule, user)
    return queryset.filter(
        user_grammar_rule_entry__in=practice_session_questions
    )
