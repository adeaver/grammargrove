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

    handleGetNextQuestion: () => void;
}

const QuestionDisplay = (props: QuestionDisplayProps) => {
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const [ correctAnswer, setCorrectAnswer ] = useState<string[] | null>(null);
    const [ isCorrect, setIsCorrect ] = useState<boolean | null>(null);
    const [ extraContext, setExtraContext ] = useState<string[] | null>(null);

    // Used for handle rerenders
    const [ originalAnswer, setOriginalAnswer ] = useState<string[] | null>(null);

    const handleSubmitAnswer = (answer: string[], example_id: string | null | undefined) => {
        setIsLoading(true);
        setOriginalAnswer(answer);
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

    const handleGetNextQuestion = () => {
        setIsLoading(false);
        setOriginalAnswer(null);
        setIsCorrect(null);
        setCorrectAnswer(null);
        setExtraContext(null);
        setError(null);
        props.handleGetNextQuestion()
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
                originalAnswer={originalAnswer}
                handleSubmitAnswer={handleSubmitAnswer}
                handleGetNextQuestion={handleGetNextQuestion} />
        );
    } else if (!!props.question.user_vocabulary_entry) {
        body = (
            <VocabularyQuestionDisplay
                question={props.question}
                isCorrect={isCorrect}
                correctAnswer={correctAnswer}
                extraContext={extraContext}
                originalAnswer={originalAnswer}
                handleSubmitAnswer={handleSubmitAnswer}
                handleGetNextQuestion={handleGetNextQuestion} />

        );
    }
    return (
        <div class="w-full flex items-center justify-center">
            { body }
        </div>
    );
}

export default QuestionDisplay;
