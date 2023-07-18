import { makeGetRequest, PaginatedResponse } from '../../util/gfetch';

import {
    GrammarRule,
} from '../../common/api';

export function searchForGrammarRule(
    search_query: string[],
    pageNumber: number | null,
    onSuccess: (resp: PaginatedResponse<GrammarRule>) => void,
    onError: (err: Error) => void
) {
    const encodedSearchQuery = search_query.map((q: string) => {
        return encodeURIComponent(q)
    }).join(",");
    const pageComponent = !pageNumber ? "" : `&page=${pageNumber}`;
    makeGetRequest<PaginatedResponse<GrammarRule>>(
        `/api/grammarrules/v1/?search_query=${encodedSearchQuery}${pageComponent}&format=json`,
        onSuccess,
        onError
    );
}
