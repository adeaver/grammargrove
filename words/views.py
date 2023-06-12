from typing import Any, Dict, List, NamedTuple

from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpRequest, JsonResponse

from words.models import Word, Definition, LanguageCode

class WordsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def search(self, request: HttpRequest) -> JsonResponse:

        class SearchResult(NamedTuple):
            word_id: str
            display: str
            pronunciation: str
            language_code: str
            definitions: List[str]

        class SearchResponse(NamedTuple):
            success: bool
            results: List[SearchResult]

            def to_response(self) -> Dict[str, Any]:
                res: Dict[str, Any] = self._asdict()
                res["results"] = [
                    r._asdict() for r in self.results
                ]
                return res

        search_query = request.data.get("search_query", None)
        try:
            query_language_code = LanguageCode(request.data.get("query_language_code", LanguageCode.SIMPLIFIED_MANDARIN.value))
        except ValueError:
            return JsonResponse(SearchResponse(success=False, results=[]).to_response())


        hanzi_results = Word.objects.filter(language_code=query_language_code, display=search_query).all()
        pinyin_results = Word.objects.filter(language_code=query_language_code, pronunciation=search_query).all()

        all_words = {
            r.id: r for r in hanzi_results
        }
        all_words.update({
            r.id: r for r in pinyin_results
        })
        results: List[SearchResult] = []
        for word in all_words.values():
            definitions = Definition.objects.filter(language_code=LanguageCode.ENGLISH, word=word).all()
            results.append(
                SearchResult(
                    word_id=word.id,
                    display=word.display,
                    pronunciation=word.pronunciation,
                    language_code=word.language_code,
                    definitions=[ d.definition for d in definitions]
                )
            )
        return JsonResponse(SearchResponse(success=True, results=results).to_response())

