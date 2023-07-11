import {
    makeGetRequest,
    makePostRequest,
    makePutRequest,
} from '../../util/gfetch';

export type UserPreferences = {
    user: string;
    id: string;
    hsk_level: number | null;
}

export function getUserPreferences(
    onSuccess: (resp: UserPreferences[]) => void,
    onError: (err: Error) => void
) {
    makeGetRequest<UserPreferences[]>(
        "/api/userpreferences/v1/?format=json",
        onSuccess,
        onError,
    )
}

export type CreateUserPreferencesRequest = {
    hsk_level: number,
}

export function createUserPreferences(
    req: CreateUserPreferencesRequest,
    onSuccess: (resp: UserPreferences) => void,
    onError: (err: Error) => void,
) {
    makePostRequest<CreateUserPreferencesRequest, UserPreferences>(
        "/api/userpreferences/v1/?format=json",
        req,
        onSuccess,
        onError,
    );
}

export type UpdateUserPreferencesRequest = Omit<UserPreferences, 'user' | 'id'>;

export function updateUserPreferences(
    id: string,
    req: UpdateUserPreferencesRequest,
    onSuccess: (resp: UserPreferences) => void,
    onError: (err: Error) => void
) {
    makePutRequest<UpdateUserPreferencesRequest, UserPreferences>(
        `/api/userpreferences/v1/${id}/?format=json`,
        req,
        onSuccess,
        onError,
    )
}

export type UpdateUserVocabularyAndGrammarListsRequests = {}

export type UpdateUserVocabularyAndGrammarListsResponse = {}

export function updateUserVocabularyAndGrammarLists(
    id: string,
    onSuccess: (resp: UpdateUserVocabularyAndGrammarListsResponse) => void,
    onError: (err: Error) => void,
) {
    makePostRequest<UpdateUserVocabularyAndGrammarListsRequests, UpdateUserVocabularyAndGrammarListsResponse>(
        `/api/userpreferences/v1/${id}/update_user_list/?format=json`,
        {},
        onSuccess,
        onError,
    )
}
