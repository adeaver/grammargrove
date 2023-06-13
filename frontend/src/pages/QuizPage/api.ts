import {
    makeGetRequest,
    makePostRequest,
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
    answer_spaces: number | null;
    vocabulary_entry_id: string;
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

export type CheckAnswerRequest = {
    question_id: string;
    answer: string;
}

export type CheckAnswerResponse = {
    correct: boolean;
    correct_answer: string | null;
}

export function checkAnswer(
    question_id: string,
    answer: string,
    onSuccess: (resp: CheckAnswerResponse) => void,
    onError: (err: Error) => void,
) {
    makePostRequest<CheckAnswerRequest, CheckAnswerResponse>(
        "/api/quiz/v1/check/?format=json",
        {
            question_id: question_id,
            answer: answer,
        },
        onSuccess,
        onError
    )
}
