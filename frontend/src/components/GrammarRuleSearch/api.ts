import { makePostRequest } from '../../util/gfetch';

import {
    GrammarRule,
} from '../../common/api';

export type SearchForGrammarRuleRequest = {
    search_query: Array<string>;
}

export function searchForGrammarRule(
    search_query: string[],
    onSuccess: (resp: Array<GrammarRule>) => void,
    onError: (err: Error) => void
) {
    makePostRequest<SearchForGrammarRuleRequest, GrammarRule[]>(
        "/api/grammarrules/v1/search/?format=json",
        {
            search_query: search_query,
        },
        onSuccess,
        onError
    );
}
