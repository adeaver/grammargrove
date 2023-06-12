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
