import { makePostRequest } from '../../util/gfetch'

import { Word } from '../../common/api';

export type SearchForWordRequest = {
    search_query: string;
    query_language_code?: string;
}

export function searchForWord(
    query: string,
    query_language_code: string | undefined,
    onSuccess: (resp: Word[]) => void,
    onError: (err: Error) => void
) {
    makePostRequest<SearchForWordRequest, Word[]>(
        "/api/words/v1/search/?format=json",
        {
            search_query: query,
            query_language_code: query_language_code
        },
        onSuccess,
        onError
    );
}
