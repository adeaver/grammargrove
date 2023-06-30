from typing import List

from random import randrange

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpRequest

from .words import get_queryset_from_user_vocabulary
from .grammarrules import get_queryset_from_user_grammar

from .models import QuizQuestion
from .serializers import (
    QuizQuestionSerializer,
    CheckRequestSerializer,
    CheckResponseSerializer
)
from .pagination import QuizQuestionPaginator
from .check import check_grammar_rule, check_vocabulary_word

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizQuestionSerializer
    pagination_class = QuizQuestionPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if randrange(100) > 50:
            queryset = get_queryset_from_user_grammar(self.request.user)
            if queryset:
                return queryset
            return get_queryset_from_user_vocabulary(self.request.user)
        queryset = get_queryset_from_user_vocabulary(self.request.user)
        if queryset:
            return queryset
        return get_queryset_from_user_grammar(self.request_user)

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
        question = questions[0]
        answer: List[str] = [ p.lower().strip() for p in req["answer"] ]
        if question.user_vocabulary_entry:
            resp = check_vocabulary_word(question.question_type, question.user_vocabulary_entry.id, answer)
            resp_serializer = CheckResponseSerializer(resp)
            return Response(resp_serializer.data)
        elif question.user_grammar_rule_entry:
            if not req.get("example_id"):
                return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            resp = check_grammar_rule(question.question_type, req["example_id"], answer)
            resp_serializer = CheckResponseSerializer(resp)
            return Response(resp_serializer.data)
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
