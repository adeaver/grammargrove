import { makeGetRequest, makePostRequest } from '../../util/gfetch';
import { UserVocabulary, UserGrammarRule } from '../../common/api/uservocabulary';

export type PracticeSession = {
    user: string;
    id: string;
    created_at: Date,
    is_complete: boolean,
    terms_mastered: number,
    total_number_of_terms: number,
    questions: Array<PracticeSessionQuestion>;
}

export type PracticeSessionQuestion = {
    id: string;
    practice_session: string;
    user_vocabulary_entry: UserVocabulary;
    user_grammar_rule_entry: UserGrammarRule;
    grammar_rule_example: string;
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

export function getPracticeSession(
    id: string,
    onSuccess: (resp: PracticeSession) => void,
    onError: (err: Error) => void
) {
    makeGetRequest<PracticeSession>(
        `/api/practicesession/v1/${id}/?format=json`,
        onSuccess,
        onError,
    )
}
