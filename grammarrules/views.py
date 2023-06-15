from typing import Any, List, Dict, NamedTuple, Optional

import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError

from grammargrove import pinyin_utils
from words.models import Word
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
        class SearchResult(NamedTuple):
            grammar_rule: GrammarRule
            components: List[GrammarRuleComponent]

            def to_json(self) -> Dict[str, Any]:
                return {
                    "grammar_rule": GrammarRuleSerializer(self.grammar_rule).data,
                    "components": [
                        GrammarRuleComponentSerializer(c).data for c in components
                    ]
                }

        class ResultResponse(NamedTuple):
            results: List[SearchResult]

            def to_json(self):
                return { "results": [ r.to_json() for r in self.results ] }

        search_query = request.data["search_query"]
        parsed_query = self._parse_search_query(search_query)
        if not parsed_query:
            return HttpResponseBadRequest()
        words: List[List[Word]] = []
        for q in parsed_query:
            w = None
            if q.is_pinyin:
                w = Word.objects.filter(pronunciation=q.query).all()
            else:
                w = Word.objects.filter(display=q.query).all()
            if not w:
                logging.warn(f"Components length is {q.query} produced no results")
                return JsonResponse(ResultResponse(results=[]).to_json())
            words.append(list(w.all()))
        components_by_grammar_id: Dict[str, int] = {}
        for word_list in words:
            ids = [w.id for w in word_list]
            components = GrammarRuleComponent.objects.filter(
                word__in=ids
            ).all()
            for c in components:
                current_words_length = components_by_grammar_id.get(c.grammar_rule.id, 0)
                components_by_grammar_id[c.grammar_rule.id] = current_words_length + 1
        results: List[SearchResult] = []
        for grammar_rule_id, components_length in components_by_grammar_id.items():
            if components_length != len(words):
                logging.warn(f"Components length is {components_length} and words length is {len(words)}")
                continue
            rules = GrammarRule.objects.filter(id=grammar_rule_id)
            if not rules:
                raise AssertionError(f"Grammar Rule {grammar_rule_id} does not exist but has components")
            rule = rules[0]
            components = list(GrammarRuleComponent.objects.filter(grammar_rule=rule).all())
            results.append(
                SearchResult(
                    grammar_rule=rule,
                    components=components,
                )
            )
        return JsonResponse(ResultResponse(results=results).to_json())
