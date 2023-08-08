from typing import Set
from uuid import UUID

from random import shuffle

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from billing.permissions import HasValidSubscription

from .models import PracticeSession, PracticeSessionQuestion
from .serializers import PracticeSessionSerializer

from .selection import get_user_vocabulary_questions, get_grammar_rule_questions

TOTAL_NUMBER_OF_QUESTIONS = 6

class PracticeSessionViewSet(viewsets.ModelViewSet):
    serializer_class = PracticeSessionSerializer
    permission_classes = [IsAuthenticated, HasValidSubscription]

    def get_queryset(self):
        return PracticeSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        practice_session = serializer.save(user=self.request.user)
        user_vocabulary_questions = get_user_vocabulary_questions(
            self.request.user, TOTAL_NUMBER_OF_QUESTIONS
        )
        num_used = 0
        used: Set[UUID] = set([])
        for idx in range(0, len(user_vocabulary_questions), 2):
            u = user_vocabulary_questions[idx].question_id
            used.add(u)
            PracticeSessionQuestion(
                practice_session=practice_session,
                user_vocabulary_entry_id=u
            ).save()
            num_used += 1
        user_grammar_rule_questions = get_grammar_rule_questions(
            self.request.user, TOTAL_NUMBER_OF_QUESTIONS
        )
        for idx in range(0, len(user_grammar_rule_questions), 2):
            grammar_rule = user_grammar_rule_questions[idx]
            used.add(grammar_rule.question_id)
            PracticeSessionQuestion(
                practice_session=practice_session,
                user_grammar_rule_entry_id=grammar_rule.question_id,
                grammar_rule_example_id=grammar_rule.example_id
            ).save()
            num_used += 1
        if num_used < TOTAL_NUMBER_OF_QUESTIONS:
            unused: List[Tuple[UUID, Optional[UUID]]] = []
            for u in user_vocabulary_questions:
                if u not in used:
                    unused.append((u.question_id, None))
            for g in user_grammar_rule_questions:
                if g.question_id not in used:
                    unused.append((g.question_id, g.example_id))
            shuffle(unused)
            for i, example in unused:
                if num_used >= TOTAL_NUMBER_OF_QUESTIONS:
                    break
                elif example is None:
                    PracticeSessionQuestion(
                        practice_session=practice_session,
                        user_vocabulary_entry_id=i,
                    ).save()
                else:
                    PracticeSessionQuestion(
                        practice_session=practice_session,
                        user_grammar_rule_entry_id=i,
                        grammar_rule_example_id=example,
                    ).save()
                num_used += 1
