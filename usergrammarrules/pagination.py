from grammargrove.pagination import DefaultPaginator

class UserGrammarRuleEntryPaginator(DefaultPaginator):
    page_size = 10
    page_size_query_param = 'created_at'
    max_page_size = 10
