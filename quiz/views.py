from typing import List, Optional

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

from .words import get_queryset_from_user_vocabulary
from .grammarrules import get_queryset_from_user_grammar

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
        if randrange(100) > 50:
            queryset = get_queryset_from_user_grammar(self.request.user)
            if queryset:
                return queryset
            return get_queryset_from_user_vocabulary(self.request.user)
        queryset = get_queryset_from_user_vocabulary(self.request.user)
        if queryset:
            return queryset
        return get_queryset_from_user_grammar(self.request.user)

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
            resp = check_vocabulary_word(question.question_type, question.user_vocabulary_entry.id, answer)
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
            resp = check_grammar_rule(question.question_type, example, answer)
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
        ).save()
        question.number_of_times_displayed += 1
        question.last_displayed_at = timezone.now()
        question.save()
        resp_serializer = CheckResponseSerializer(resp)
        return Response(resp_serializer.data)
