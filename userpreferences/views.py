from typing import Optional

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpRequest

from django.db import transaction

from billing.permissions import HasValidSubscription

from .models import UserPreferences
from .serializers import UserPreferencesSerializer

from grammarrules.models import GrammarRule
from usergrammarrules.models import UserGrammarRuleEntry, AddedByMethod as user_grammar_rule_added_by

from words.models import Word, LanguageCode
from uservocabulary.models import UserVocabularyEntry, AddedByMethod as user_vocabulary_added_by

class UserPreferencesViewSet(viewsets.ModelViewSet):
    serializer_class = UserPreferencesSerializer
    permission_classes = [IsAuthenticated, HasValidSubscription]

    def get_queryset(self):
        return UserPreferences.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def update_user_list(self, request: HttpRequest, pk: Optional[str] = None) -> Response:
        preferences = self.get_queryset().filter(id=pk)
        if not preferences:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        hsk_level = preferences[0].hsk_level
        if hsk_level is None:
            return Response({}, status=status.HTTP_200_OK)
        # TODO: handle HSK level 0
        with transaction.atomic():
            UserGrammarRuleEntry.objects.filter(
                user=self.request.user,
                added_by=user_grammar_rule_added_by.Onboarding,
                grammar_rule__in=GrammarRule.objects.filter(
                    hsk_level__gt=hsk_level
                ).values_list("id", flat=True)
            ).delete()
            valid_grammar_rules = GrammarRule.objects.filter(
                hsk_level__lte=hsk_level
            ).exclude(
                id__in=UserGrammarRuleEntry.objects.filter(
                    user=self.request.user
                ).values_list("grammar_rule", flat=True)
            )
            for g in valid_grammar_rules:
                UserGrammarRuleEntry(
                    user=self.request.user,
                    grammar_rule=g,
                    added_by=user_grammar_rule_added_by.Onboarding
                ).save()

            UserVocabularyEntry.objects.filter(
                user=self.request.user,
                added_by=user_vocabulary_added_by.Onboarding,
                word__in=Word.objects.filter(
                    hsk_level__gt=hsk_level,
                    language_code=LanguageCode.SIMPLIFIED_MANDARIN,
                ).values_list("id", flat=True)
            ).delete()
            valid_words = Word.objects.filter(
                hsk_level__lte=hsk_level,
                language_code=LanguageCode.SIMPLIFIED_MANDARIN,
            ).exclude(
                id__in=UserVocabularyEntry.objects.filter(
                    user=self.request.user
                ).values_list("word", flat=True)
            )
            for w in valid_words:
                UserVocabularyEntry(
                    user=self.request.user,
                    added_by=user_vocabulary_added_by.Onboarding,
                    word=w,
                ).save()
        return Response({}, status=status.HTTP_200_OK)
