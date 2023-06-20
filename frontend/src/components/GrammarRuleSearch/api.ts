import { makePostRequest } from '../../util/gfetch';

import {
    GrammarRule,
    GrammarRuleComponent
} from '../../common/api';

export type SearchForGrammarRuleRequest = {
    search_query: Array<string>;
}

export type SearchResult = {
    grammar_rule: GrammarRule;
    components: Array<GrammarRuleComponent>;
}

export type SearchForGrammarRuleResponse = {
    results: SearchResult[];
}

export function searchForGrammarRule(
    search_query: string[],
    onSuccess: (resp: SearchForGrammarRuleResponse) => void,
    onError: (err: Error) => void
) {
    makePostRequest<SearchForGrammarRuleRequest, SearchForGrammarRuleResponse>(
        "/api/grammarrules/v1/search/?format=json",
        {
            search_query: search_query,
        },
        onSuccess,
        onError
    );
}
