import { useState } from 'preact/hooks';

import Text, { TextFunction } from '../../../../components/Text';
import LoadingIcon from '../../../../components/LoadingIcon';

import {
    Question,
    // checkAnswer,
} from '../../api';

import GrammarRuleQuestionDisplay from './GrammarRuleQuestionDisplay';
import VocabularyQuestionDisplay from './VocabularyQuestionDisplay';

type QuestionDisplayProps = {
    question: Question;
}

const QuestionDisplay = (props: QuestionDisplayProps) => {
    const [ isLoading, setIsLoading ] = useState<boolean>(false);

    const handleSubmitAnswer = (answer: string[], example_id: string | null | undefined) => {
        setIsLoading(true);
        console.log(answer, example_id);
    }

    if (isLoading) {
        return <LoadingIcon />
    } else if (!!props.question.user_grammar_rule_entry) {
        return (
            <GrammarRuleQuestionDisplay
                question={props.question}
                handleSubmitAnswer={handleSubmitAnswer} />
        );
    } else if (!!props.question.user_vocabulary_entry) {
        return (
            <VocabularyQuestionDisplay
                question={props.question}
                handleSubmitAnswer={handleSubmitAnswer} />
        );
    }
    return (
        <Text function={TextFunction.Warning}>
            Something went wrong
        </Text>
    );
}

export default QuestionDisplay;
