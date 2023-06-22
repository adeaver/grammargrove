from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from grammargrove.pinyin_utils import (
    PinyinSplitter,
    is_numeric_form,
    is_display_form,
    convert_to_numeric_form
)

from .models import Word, LanguageCode
from .serializers import WordSerializer
from .pagination import WordPaginator

class WordsViewSet(viewsets.ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    pagination_class = WordPaginator

    def get_queryset(self):
        search_query: str = self.request.query_params.get("search_query", "").strip().lower()
        query_language_code = LanguageCode(self.request.query_params.get("language_code", LanguageCode.SIMPLIFIED_MANDARIN.value))
        are_all_parts_numeric_form = all([ is_numeric_form(p) for p in search_query.split(" ") ])
        are_all_parts_display_form = all([ is_display_form(p) for p in search_query.split(" ") ])
        if are_all_parts_numeric_form:
            return Word.objects.filter(
                language_code=query_language_code, pronunciation=search_query)
        elif are_all_parts_display_form:
            split_results = search_query.split(" ")
            if len(split_results) == 1:
                sp = PinyinSplitter()
                as_split = sp.split(search_query, expected_output_length=None)
                if as_split.error_reason:
                    split_results = []
                else:
                    split_results = [
                        " ".join([ convert_to_numeric_form(p) for p in split ])
                        for split in as_split.result
                    ]
            else:
                split_results = [ " ".join([ convert_to_numeric_form(p) for p in split_results ]) ]
            return Word.objects.filter(
                language_code=query_language_code, pronunciation__in=split_results)
        return Word.objects.filter(
            language_code=query_language_code, display=search_query)
