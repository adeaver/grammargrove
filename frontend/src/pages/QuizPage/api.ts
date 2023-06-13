import {
    makeGetRequest
} from '../../util/gfetch';

export enum QuestionType {
    AccentsFromHanzi = 1,
    DefinitionsFromHanzi = 2,
    HanziFromEnglish = 3,
}

export type Question = {
    question_id: string;
    display: string;
    question_type: QuestionType;
}

export function getNextQuestion(
    onSuccess: (resp: Question) => void,
    onError: (err: Error) => void
) {
    makeGetRequest<Question>(
        "/api/quiz/v1/next?format=json",
        onSuccess,
        onError,
    )
}
