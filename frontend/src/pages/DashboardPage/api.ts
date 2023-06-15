import {
    makeDeleteRequest,
    makeGetRequest,
    makePostRequest
} from '../../util/gfetch';

export type UserVocabulary = {
    word: string;
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
    onSuccess: (resp: UserVocabulary[]) => void,
    onError: (err: Error) => void
) {
    makeGetRequest<UserVocabulary[]>(
        "/api/uservocabulary/v1/?format=json",
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
    grammar_rule: string;
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
    onSuccess: (resp: UserGrammarRule[]) => void,
    onError: (err: Error) => void
) {
    makeGetRequest<UserGrammarRule[]>(
        "/api/usergrammarrules/v1/?format=json",
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
        `/api/usergrammarrule/v1/${id}/?format=json`,
        onSuccess,
        onError,
    )
}
