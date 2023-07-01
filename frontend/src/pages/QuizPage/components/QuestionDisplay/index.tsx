import { useState } from 'preact/hooks';

import Text, { TextFunction } from '../../../../components/Text';
import LoadingIcon from '../../../../components/LoadingIcon';

import {
    Question,

    checkAnswer,
    CheckAnswerResponse
} from '../../api';

import GrammarRuleQuestionDisplay from './GrammarRuleQuestionDisplay';
import VocabularyQuestionDisplay from './VocabularyQuestionDisplay';

type QuestionDisplayProps = {
    question: Question;
}

const QuestionDisplay = (props: QuestionDisplayProps) => {
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const [ correctAnswer, setCorrectAnswer ] = useState<string[] | null>(null);
    const [ isCorrect, setIsCorrect ] = useState<boolean | null>(null);
    const [ extraContext, setExtraContext ] = useState<string[] | null>(null);

    const handleSubmitAnswer = (answer: string[], example_id: string | null | undefined) => {
        setIsLoading(true);
        checkAnswer(
            props.question.id, answer, example_id ? example_id : null,
            (resp: CheckAnswerResponse) => {
                setIsLoading(false);
                setIsCorrect(resp.is_correct);
                setCorrectAnswer(resp.correct_answer);
                setExtraContext(resp.extra_context);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }

    let body;
    if (isLoading) {
        body = <LoadingIcon />;
    } else if (!!error) {
        body = (
            <Text function={TextFunction.Warning}>
                Something went wrong, please try again later.
            </Text>
        );
    } else if (!!props.question.user_grammar_rule_entry) {
        body = (
            <GrammarRuleQuestionDisplay
                question={props.question}
                isCorrect={isCorrect}
                correctAnswer={correctAnswer}
                extraContext={extraContext}
                handleSubmitAnswer={handleSubmitAnswer} />
        );
    } else if (!!props.question.user_vocabulary_entry) {
        body = (
            <VocabularyQuestionDisplay
                question={props.question}
                isCorrect={isCorrect}
                correctAnswer={correctAnswer}
                extraContext={extraContext}
                handleSubmitAnswer={handleSubmitAnswer} />
        );
    }
    return (
        <div class="w-full flex items-center justify-center">
            { body }
        </div>
    );
}

export default QuestionDisplay;
