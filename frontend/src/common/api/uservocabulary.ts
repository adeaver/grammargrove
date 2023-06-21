import {
    makeDeleteRequest,
    makeGetRequest,
    makePostRequest,

    PaginatedResponse,
} from '../../util/gfetch';

import {
    GrammarRule,
    Word
} from './index';

export type UserVocabulary = {
    word: Word;
    user: string;
    id: string;
    notes: string | null;
}

export type AddUserVocabularyRequest = {
    word: string;
    notes: string | null;
}

export function addUserVocabulary(
    word: string,
    notes: string | null,
    onSuccess: (resp: UserVocabulary) => void,
    onError: (err: Error) => void
) {
    makePostRequest<AddUserVocabularyRequest, UserVocabulary>(
        "/api/uservocabulary/v1/?format=json",
        {
            word: word,
            notes: notes
        },
        onSuccess,
        onError
    );
}

export function getUserVocabulary(
    pageNumber: number | undefined,
    onSuccess: (resp: PaginatedResponse<UserVocabulary>) => void,
    onError: (err: Error) => void
) {
    const pageNumberQuery = !pageNumber ? "" : `&page=${pageNumber}`;
    makeGetRequest<PaginatedResponse<UserVocabulary>>(
        `/api/uservocabulary/v1/?format=json${pageNumberQuery}`,
        onSuccess,
        onError,
    )
}

export function deleteUserVocabulary(
    id: string,
    onSuccess: () => void,
    onError: (err: Error) => void
) {
    makeDeleteRequest(
        `/api/uservocabulary/v1/${id}/?format=json`,
        onSuccess,
        onError,
    )
}

export type UserGrammarRule = {
    grammar_rule: GrammarRule;
    user: string;
    id: string;
    notes: string | null;
}

export type AddUserGrammarRuleRequest = {
    grammar_rule: string;
    notes: string | null;
}

export function addUserGrammarRule(
    grammar_rule: string,
    notes: string | null,
    onSuccess: (resp: UserGrammarRule) => void,
    onError: (err: Error) => void
) {
    makePostRequest<AddUserGrammarRuleRequest, UserGrammarRule>(
        "/api/usergrammarrules/v1/?format=json",
        {
            grammar_rule: grammar_rule,
            notes: notes
        },
        onSuccess,
        onError
    );
}

export function getUserGrammarRules(
    pageNumber: number | undefined,
    onSuccess: (resp: PaginatedResponse<UserGrammarRule>) => void,
    onError: (err: Error) => void
) {
    const pageNumberQuery = !pageNumber ? "" : `&page=${pageNumber}`;
    makeGetRequest<PaginatedResponse<UserGrammarRule>>(
        `/api/usergrammarrules/v1/?format=json${pageNumberQuery}`,
        onSuccess,
        onError,
    )
}

export function deleteUserGrammarRule(
    id: string,
    onSuccess: () => void,
    onError: (err: Error) => void
) {
    makeDeleteRequest(
        `/api/usergrammarrules/v1/${id}/?format=json`,
        onSuccess,
        onError,
    )
}
