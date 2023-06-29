import {
    Question,
    QuestionType,
} from '../../api';

import {
    HanziFromDefinitionDisplay,
    DefinitionFromHanziDisplay,
    AccentsFromHanziDisplay
} from './common';

type GrammarRuleQuestionDisplayProps = {
    question: Question;

    handleSubmitAnswer: (answer: string[], example_id: string | null | undefined) => void;
}

const GrammarRuleQuestionDisplay = (props: GrammarRuleQuestionDisplayProps) => {
    if (props.question.question_type === QuestionType.HanziFromEnglish) {
        return (
            <HanziFromDefinitionDisplay
                title="Translate the following sentence into Mandarin:"
                question={props.question}
                handleSubmitAnswer={props.handleSubmitAnswer} />
        );
    } else if (props.question.question_type === QuestionType.DefinitionsFromHanzi) {
        return (
            <DefinitionFromHanziDisplay
                title="Translate the following sentence into English:"
                question={props.question}
                handleSubmitAnswer={props.handleSubmitAnswer} />
        );
    } else if (props.question.question_type === QuestionType.AccentsFromHanzi) {
        return (
            <AccentsFromHanziDisplay
                title="Mark the accent numbers for the following words:"
                question={props.question}
                handleSubmitAnswer={props.handleSubmitAnswer} />

        );
    }
    throw Error(`Unrecognized question type ${props.question.question_type}`);
}

export default GrammarRuleQuestionDisplay;
