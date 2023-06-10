import { makePostRequest } from '../../util/gfetch';

export type SearchByEmailRequest = {
    email: string;
}

export type SearchByEmailResponse = {
    action: SearchByEmailAction;
}

export enum SearchByEmailAction {
    RequireLogin = 'require-login',
    RequireSignup = 'require-signup',
    Redirect = 'redirect'
}

export function searchByEmail(
    email: string,
    onSuccess: (resp: SearchByEmailResponse) => void,
    onError: (err: Error) => void
) {
    makePostRequest<SearchByEmailRequest, SearchByEmailResponse>(
        "/api/users/v1/search_by_email/",
        {
            email: email,
        },
        onSuccess,
        onError
    );
}
