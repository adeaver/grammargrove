import {
    makeGetRequest,
    makePostRequest,
    makePutRequest,
} from '../../util/gfetch';

export type UserPreferences = {
    user: string;
    id: string;
    hsk_level: number | null;
    daily_practice_reminders_enabled: boolean;
}

export type UserPreferencesBody = Omit<UserPreferences, "user" | "id">;

export function getDefaultUserPreferencesBody() {
    return {
        hsk_level: null,
        daily_practice_reminders_enabled: true,
    }
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

export function createUserPreferences(
    req: UserPreferencesBody,
    onSuccess: (resp: UserPreferences) => void,
    onError: (err: Error) => void,
) {
    makePostRequest<UserPreferencesBody, UserPreferences>(
        "/api/userpreferences/v1/?format=json",
        req,
        onSuccess,
        onError,
    );
}

export function updateUserPreferences(
    id: string,
    req: UserPreferencesBody,
    onSuccess: (resp: UserPreferences) => void,
    onError: (err: Error) => void
) {
    makePutRequest<UserPreferencesBody, UserPreferences>(
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
