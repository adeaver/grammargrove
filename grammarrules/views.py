from typing import Set, Optional

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .pagination import GrammarRulePaginator
from .models import GrammarRule, GrammarRuleComponent, PartOfSpeech
from .serializers import GrammarRuleSerializer

from words.models import LanguageCode
from words.utils import get_queryset_for_query

class GrammarRuleViewSet(viewsets.ModelViewSet):
    serializer_class = GrammarRuleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    pagination_class = GrammarRulePaginator

    def get_queryset(self):
        parts_of_speech_by_name = { p.name.lower(): p for p in PartOfSpeech }
        search_query: str = self.request.query_params.get("search_query", "").strip().lower()
        query_language_code = LanguageCode(self.request.query_params.get("language_code", LanguageCode.SIMPLIFIED_MANDARIN.value))
        search_query_parts = search_query.split(",")
        valid_component_ids: Optional[Set[str]] = None
        for query in search_query_parts:
            if query.lower() in parts_of_speech_by_name:
                continue
            word_queryset = get_queryset_for_query(
                    query_language_code,
                    query
                )
            component_ids = set(GrammarRuleComponent.objects.filter(
                word__in=word_queryset
            ).values_list("id", flat=True))
            if valid_component_ids is None:
                valid_component_ids = component_ids
            else:
                valid_component_ids = valid_component_ids.union(component_ids)
        return GrammarRule.objects.filter(
            id__in=GrammarRuleComponent.objects.filter(id__in=valid_component_ids).values_list("grammar_rule", flat=True)
        ).order_by("id")
