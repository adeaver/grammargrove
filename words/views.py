from typing import Any, Dict, List, NamedTuple

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpRequest, JsonResponse

from grammargrove.pinyin_utils import is_numeric_form, is_display_form, convert_to_numeric_form

from words.models import Word, Definition, LanguageCode
from words.serializers import WordSerializer

class WordsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def search(self, request: HttpRequest) -> Response:
        search_query = request.data.get("search_query", None)
        try:
            query_language_code = LanguageCode(request.data.get("query_language_code", LanguageCode.SIMPLIFIED_MANDARIN.value))
        except ValueError:
            return Response([])

        results: List[Word] = []
        are_all_parts_numeric_form = all([ is_numeric_form(p) for p in search_query.split(" ") ])
        are_all_parts_display_form = all([ is_display_form(p) for p in search_query.split(" ") ])
        if are_all_parts_numeric_form:
            results = list(Word.objects.filter(language_code=query_language_code, pronunciation=search_query).all())
        elif are_all_parts_display_form:
            numeric_form_pronunciation = " ".join([ convert_to_numeric_form(p) for p in search_query.split(" ") ])
            results = list(Word.objects.filter(language_code=query_language_code, pronunciation=numeric_form_pronunciation).all())
        else:
            results = list(Word.objects.filter(language_code=query_language_code, display=search_query).all())
        return Response(WordSerializer(results, many=True).data)

