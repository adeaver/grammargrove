from typing import Dict, List, NamedTuple, Set
from uuid import UUID

from django.db.models import Count

from users.models import User
from quiz.models import QuizQuestion, QuestionType, QuizResponse

# If a question is correctly answered
# this number of times, it is taken out of the stack
FINISHED_CORRECT_TIMES = 2

def get_finished_quiz_question_ids(
    practice_session_id: UUID
) -> List[UUID]:
    return list(
        QuizResponse.objects.filter(
            practice_session_id=practice_session_id,
            is_correct=True
        )
        .values('quiz_question')
        .annotate(dcount=Count('quiz_question'))
        .exclude(dcount__lt=FINISHED_CORRECT_TIMES)
        .values_list('quiz_question', flat=True)
    )
