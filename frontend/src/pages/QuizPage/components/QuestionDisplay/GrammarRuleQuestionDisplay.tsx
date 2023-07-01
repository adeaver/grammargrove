import {
    QuestionType,
} from '../../api';

import {
    QuestionDisplayControllerProps,

    HanziFromDefinitionDisplay,
    DefinitionFromHanziDisplay,
    AccentsFromHanziDisplay
} from './common';

const GrammarRuleQuestionDisplay = (props: QuestionDisplayControllerProps) => {
    if (props.question.question_type === QuestionType.HanziFromEnglish) {
        return (
            <HanziFromDefinitionDisplay
                title="Translate the following sentence into Mandarin:"
                question={props.question}
                isCorrect={props.isCorrect}
                correctAnswer={props.correctAnswer}
                extraContext={props.extraContext}
                handleSubmitAnswer={props.handleSubmitAnswer} />
        );
    } else if (props.question.question_type === QuestionType.DefinitionsFromHanzi) {
        return (
            <DefinitionFromHanziDisplay
                title="Translate the following sentence into English:"
                question={props.question}
                isCorrect={props.isCorrect}
                correctAnswer={props.correctAnswer}
                extraContext={props.extraContext}
                handleSubmitAnswer={props.handleSubmitAnswer} />
        );
    } else if (props.question.question_type === QuestionType.AccentsFromHanzi) {
        return (
            <AccentsFromHanziDisplay
                title="Mark the accent numbers for the following words:"
                question={props.question}
                isCorrect={props.isCorrect}
                correctAnswer={props.correctAnswer}
                extraContext={props.extraContext}
                handleSubmitAnswer={props.handleSubmitAnswer} />

        );
    }
    throw Error(`Unrecognized question type ${props.question.question_type}`);
}

export default GrammarRuleQuestionDisplay;
