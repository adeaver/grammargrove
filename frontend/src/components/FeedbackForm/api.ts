import { makePostRequest } from '../../util/gfetch';

export enum FeedbackType {
    Join = 'join',
    Pulse = 'pulse',
    NoSubscribe = 'no-sub',
}

export type FeedbackResponse = {
    created_at: Date;
    response_type: FeedbackType;
    response: string;
    user: string;
}

type FeedbackRequest = {
    response: string;
    response_type: FeedbackType;
}

export function submitFeedback(
    feedbackType: FeedbackType,
    feedback: string,
    onSuccess: (resp: FeedbackResponse) => void,
    onError: (error: Error) => void,
) {
    makePostRequest<FeedbackRequest, FeedbackResponse>(
        "/api/feedback/v1/?format=json",
        {
            response: feedback,
            response_type: feedbackType,
        },
        onSuccess,
        onError,
    );
}
