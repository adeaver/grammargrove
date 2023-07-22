import { makePostRequest } from '../../util/gfetch';

export type PracticeSession = {
    user: string;
    id: string;
    created_at: Date,
    is_complete: boolean,
}

export function createPracticeSession(
    onSuccess: (resp: PracticeSession) => void,
    onError: (err: Error) => void
) {
    makePostRequest<{}, PracticeSession>(
        "/api/practicesession/v1/?format=json",
        {},
        onSuccess,
        onError,
    );
}
