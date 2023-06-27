from random import randrange

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .words import get_queryset_from_user_vocabulary
from .grammarrules import get_queryset_from_user_grammar

from .serializers import QuizQuestionSerializer

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizQuestionSerializer

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
