import {
    makeGetRequest,
    makePostRequest,
    PaginatedResponse
} from '../../util/gfetch';

export enum QuestionType {
    AccentsFromHanzi = 1,
    DefinitionsFromHanzi = 2,
    HanziFromEnglish = 3,
}

export type Question = {
    id: string;
    question_type: QuestionType;
    user_vocabulary_entry: string | null;
    user_grammar_rule_entry: string | null;
    display: Array<Display>;
    example_id?: string | null;
}

export type Display = {
    display: string;
    input_length: number;
}

export function getNextQuestion(
    onSuccess: (resp: PaginatedResponse<Question>) => void,
    onError: (err: Error) => void
) {
    makeGetRequest<PaginatedResponse<Question>>(
        "/api/quiz/v1/?format=json",
        onSuccess,
        onError,
    )
}

export type CheckAnswerRequest = {
    question_id: string;
    answer: Array<string>;
    example_id: string | null;
}

export type CheckAnswerResponse = {
    is_correct: boolean;
    correct_answer: Array<string>;
}

export function checkAnswer(
    question_id: string,
    answer: Array<string>,
    example_id: string | null,
    onSuccess: (resp: CheckAnswerResponse) => void,
    onError: (err: Error) => void,
) {
    makePostRequest<CheckAnswerRequest, CheckAnswerResponse>(
        "/api/quiz/v1/check/?format=json",
        {
            question_id: question_id,
            answer: answer,
            example_id: example_id,
        },
        onSuccess,
        onError
    )
}
