import { makeGetRequest, PaginatedResponse } from '../../util/gfetch'

import { Word } from '../../common/api';

export type SearchForWordRequest = {
    search_query: string;
    query_language_code?: string;
}

export function searchForWord(
    query: string,
    queryLanguageCode: string | undefined,
    pageNumber: number | null,
    onSuccess: (resp: PaginatedResponse<Word>) => void,
    onError: (err: Error) => void
) {
    const encodedQuery = encodeURIComponent(query)
    const languageCodeQuery = !!queryLanguageCode ? `&language_code=${encodeURIComponent(queryLanguageCode)}` : ""
    const pageNumberQuery = pageNumber != null ? `&page=${encodeURIComponent(pageNumber)}` : ""
    makeGetRequest<PaginatedResponse<Word>>(
        `/api/words/v1/?search_query=${encodedQuery}${languageCodeQuery}${pageNumberQuery}&format=json`,
        onSuccess,
        onError
    );
}
