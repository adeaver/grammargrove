from typing import List, Optional
from uuid import UUID

import logging
from random import randrange

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpRequest
from django.utils import timezone

from billing.permissions import HasValidSubscription

from grammargrove.text_utils import remove_punctuation
from grammarrules.models import GrammarRuleExample

from users.models import User
from practicesession.mastery import get_mastery_for_session_id

from .query import get_queryset, QuerySetType

from .models import QuizQuestion, QuizResponse
from .serializers import (
    QuizQuestionSerializer,
    CheckRequestSerializer,
    CheckResponseSerializer,
    CheckResponse,
)
from .pagination import QuizQuestionPaginator
from .check import check_grammar_rule, check_vocabulary_word

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizQuestionSerializer
    pagination_class = QuizQuestionPaginator
    permission_classes = [IsAuthenticated, HasValidSubscription]

    def get_queryset(self):
        practice_session_id = self.request.GET.get("practice_session_id")
        queryset_types_ordered = [ QuerySetType.GrammarRule, QuerySetType.Vocabulary ] if randrange(100) > 50 else (
            [ QuerySetType.Vocabulary, QuerySetType.GrammarRule ]
        )
        for qt in queryset_types_ordered:
            queryset = get_queryset(qt, self.request.user, practice_session_id)
            if queryset:
                return queryset
        return get_queryset(QuerySetType.Vocabulary, self.request.user, practice_session_id)

    @action(detail=False, methods=["POST"])
    def check(self, request: HttpRequest) -> Response:
        serializer = CheckRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        req = serializer.data
        questions = QuizQuestion.objects.filter(user=request.user, id=req["quiz_question_id"])
        if not questions:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        question: QuizQuestion = questions[0]
        answer: List[str] = [ remove_punctuation(p.lower().strip()) for p in req["answer"] ]
        resp: Optional[CheckResponse] = None
        example: Optional[GrammarRuleExample] = None
        if question.user_vocabulary_entry:
            resp = check_vocabulary_word(
                question.question_type,
                question.user_vocabulary_entry.id,
                answer
            )
        elif question.user_grammar_rule_entry:
            if not req.get("example_id"):
                return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            examples = GrammarRuleExample.objects.filter(
                id=req["example_id"]
            )
            if not examples:
                raise ValueError(f"Example {example_id} does not exist")
            example = examples[0]
            resp = check_grammar_rule(
                question.question_type,
                example,
                answer
            )
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        if not resp:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        QuizResponse(
            user=request.user,
            quiz_question=question,
            grammar_rule_example=example,
            is_correct=resp.is_correct,
            practice_session_id=req.get("practice_session_id"),
        ).save()
        question.number_of_times_displayed += 1
        question.last_displayed_at = timezone.now()
        question.save()
        resp_serializer = _get_check_response_serializer(request.user, req.get("practice_session_id"), resp)
        return Response(resp_serializer.data)


    @action(detail=True, methods=["POST"])
    def add_note(self, request: HttpRequest, pk: Optional[UUID] = None) -> Response:
        return Response({"success": True})

def _get_check_response_serializer(
    user: User,
    practice_session_id: Optional[UUID],
    resp: CheckResponse
) -> CheckResponseSerializer:
    if practice_session_id is None:
        return CheckResponseSerializer(resp)
    mastery = get_mastery_for_session_id(user, practice_session_id)
    is_complete = mastery.terms_mastered == mastery.total_number_of_terms
    return CheckResponseSerializer(
        CheckResponse(
            is_correct=resp.is_correct,
            correct_answer=resp.correct_answer,
            extra_context=resp.extra_context,
            words=resp.words,
            is_practice_session_complete=is_complete,
            terms_mastered=mastery.terms_mastered,
            total_number_of_terms=mastery.total_number_of_terms
        )
    )
