import { makeGetRequest } from '../../util/gfetch';

import {
    GrammarRule,
} from '../../common/api';

export function searchForGrammarRule(
    search_query: string[],
    onSuccess: (resp: Array<GrammarRule>) => void,
    onError: (err: Error) => void
) {
    const encodedSearchQuery = search_query.map((q: string) => {
        return encodeURIComponent(q)
    }).join(",");
    makeGetRequest<GrammarRule[]>(
        `/api/grammarrules/v1/?search_query=${encodedSearchQuery}&format=json`,
        onSuccess,
        onError
    );
}
