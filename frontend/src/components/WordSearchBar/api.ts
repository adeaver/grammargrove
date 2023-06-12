import { makePostRequest } from '../../util/gfetch';

export type SearchForWordRequest = {
    search_query: string;
    query_language_code?: string;
}

export type SearchForWordResponse = {
    success: boolean;
    results: SearchResult[];
}

export type SearchResult = {
    word_id: string;
    display: string;
    pronunciation: string;
    language_code: string;
    definitions: string[];
}

export function searchForWord(
    query: string,
    query_language_code: string | undefined,
    onSuccess: (resp: SearchForWordResponse) => void,
    onError: (err: Error) => void
) {
    makePostRequest<SearchForWordRequest, SearchForWordResponse>(
        "/api/words/v1/search/",
        {
            search_query: query,
            query_language_code: query_language_code
        },
        onSuccess,
        onError
    );
}
