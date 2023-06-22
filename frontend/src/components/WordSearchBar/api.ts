import { makeGetRequest, PaginatedResponse } from '../../util/gfetch'

import { Word } from '../../common/api';

export type SearchForWordRequest = {
    search_query: string;
    query_language_code?: string;
}

export function searchForWord(
    query: string,
    query_language_code: string | undefined,
    onSuccess: (resp: PaginatedResponse<Word>) => void,
    onError: (err: Error) => void
) {
    const languageCodeQuery = !!query_language_code ? `&language_code=${query_language_code}` : ""
    makeGetRequest<PaginatedResponse<Word>>(
        `/api/words/v1/?search_query=${query}${languageCodeQuery}&format=json`,
        onSuccess,
        onError
    );
}
