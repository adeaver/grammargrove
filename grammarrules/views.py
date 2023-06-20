from typing import Any, List, Dict, NamedTuple, Optional

import logging

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError

from grammargrove import pinyin_utils
from words.models import Word, LanguageCode
from grammarrules.models import GrammarRule, GrammarRuleComponent, PartOfSpeech

from .serializers import GrammarRuleSerializer, GrammarRuleComponentSerializer

class SearchQuery(NamedTuple):
    is_pinyin: bool
    query: str

class GrammarRuleViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'search':
            return [IsAuthenticated(),]
        return []

    def _get_numeric_form_pinyin(self, s: str) -> Optional[str]:
        if pinyin_utils.is_display_form(s.lower()):
            return pinyin_utils.convert_to_numeric_form(s.lower())
        elif pinyin_utils.is_numeric_form(s.lower()):
            return s.lower()
        return None

    def _parse_search_query(self, search_query: List[str]) -> Optional[List[SearchQuery]]:
        parts_of_speech_by_name = { p.name.lower(): p for p in PartOfSpeech }
        words_to_search: SearchQuery = []
        for s in search_query:
            parts = s.split(" ")
            if len(parts) > 1:
                pinyin_parts = []
                for p in parts:
                    numeric_form = self._get_numeric_form_pinyin(p)
                    if not numeric_form:
                        return None
                    pinyin_parts.append(numeric_form)
                words_to_search.append(
                    SearchQuery(
                        is_pinyin=True,
                        query = " ".join(pinyin_parts),
                    )
                )
            numeric_pinyin_form: Optional[str] = (
                self._get_numeric_form_pinyin(parts[0])
            )
            if numeric_pinyin_form is not None:
                words_to_search.append(
                    SearchQuery(
                        is_pinyin=True,
                        query = numeric_pinyin_form,
                    )
                )
            elif parts[0].lower() in parts_of_speech_by_name:
                continue
            else:
                words_to_search.append(
                    SearchQuery(
                        is_pinyin=False,
                        query = parts[0],
                    )
                )
        return words_to_search

    @action(detail=False, methods=['post'])
    def search(self, request: HttpRequest) -> HttpResponse:
        search_query = request.data["search_query"]
        # TODO: support Traditional
        parsed_query = self._parse_search_query(search_query)
        if not parsed_query:
            return HttpResponseBadRequest()
        components_by_grammar_id: Dict[str, int] = {}
        for q in parsed_query:
            components = _get_grammar_components_for_query_part(q)
            if not components:
                logging.warn(f"Components length is {q.query} produced no results")
                return Response([])
            for c in components:
                current_words_length = components_by_grammar_id.get(c.grammar_rule.id, 0)
                components_by_grammar_id[c.grammar_rule.id] = current_words_length + 1
        results: List[GrammarRule] = []
        for grammar_rule_id, components_length in components_by_grammar_id.items():
            if components_length != len(parsed_query):
                logging.warn(f"Components length is {components_length} and words length is {len(parsed_query)}")
                continue
            rules = GrammarRule.objects.filter(id=grammar_rule_id)
            if not rules:
                raise AssertionError(f"Grammar Rule {grammar_rule_id} does not exist but has components")
            results.append(rules[0])
        logging.warn(results)
        return Response(GrammarRuleSerializer(results, many=True).data)

def _get_grammar_components_for_query_part(q: SearchQuery) -> List[GrammarRuleComponent]:
    word_list = []
    if q.is_pinyin:
        word_list = Word.objects.filter(language_code=LanguageCode.SIMPLIFIED_MANDARIN, pronunciation=q.query).all()
    else:
        word_list = Word.objects.filter(language_code=LanguageCode.SIMPLIFIED_MANDARIN, display=q.query).all()
    if not word_list:
        return []
    return list(
        GrammarRuleComponent.objects.filter(
            word__in=[word.id for word in word_list]
        ).all()
    )

