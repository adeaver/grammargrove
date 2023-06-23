from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Word, LanguageCode
from .serializers import WordSerializer
from .pagination import WordPaginator

from .utils import get_queryset_for_query

class WordsViewSet(viewsets.ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    pagination_class = WordPaginator

    def get_queryset(self):
        search_query: str = self.request.query_params.get("search_query", "").strip().lower()
        query_language_code = LanguageCode(self.request.query_params.get("language_code", LanguageCode.SIMPLIFIED_MANDARIN.value))
        if not search_query:
            return Word.objects.filter(language_code=query_language_code).order_by("id")
        return get_queryset_for_query(query_language_code, search_query).order_by("id")
