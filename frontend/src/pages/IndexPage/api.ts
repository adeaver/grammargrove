import { makePostRequest } from '../../util/gfetch';

export type SearchByEmailRequest = {
    email: string;
    token: string;
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
    token: string,
    onSuccess: (resp: SearchByEmailResponse) => void,
    onError: (err: Error) => void
) {
    makePostRequest<SearchByEmailRequest, SearchByEmailResponse>(
        "/api/users/v1/search_by_email/",
        {
            email: email,
            token: token,
        },
        onSuccess,
        onError
    );
}
