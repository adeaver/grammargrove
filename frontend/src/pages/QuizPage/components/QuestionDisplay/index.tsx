import Text, { TextFunction } from '../../../../components/Text';

import { Question } from '../../api';

import GrammarRuleQuestionDisplay from './GrammarRuleQuestionDisplay';
import VocabularyQuestionDisplay from './VocabularyQuestionDisplay';

type QuestionDisplayProps = {
    question: Question;
}

const QuestionDisplay = (props: QuestionDisplayProps) => {
    if (!!props.question.user_grammar_rule_entry) {
        return <GrammarRuleQuestionDisplay question={props.question} />
    } else if (!!props.question.user_vocabulary_entry) {
        return <VocabularyQuestionDisplay question={props.question} />
    }
    return (
        <Text function={TextFunction.Warning}>
            Something went wrong
        </Text>
    );
}

export default QuestionDisplay;
