import {
    QuestionType,
} from '../../api';

import {
    QuestionDisplayControllerProps,

    HanziFromDefinitionDisplay,
    DefinitionFromHanziDisplay,
    AccentsFromHanziDisplay
} from './common';

const VocabularyQuestionDisplay = (props: QuestionDisplayControllerProps) => {
    if (props.question.question_type === QuestionType.HanziFromEnglish) {
        return (
            <HanziFromDefinitionDisplay
                title="What is the Mandarin word that means the following:"
                question={props.question}
                isCorrect={props.isCorrect}
                correctAnswer={props.correctAnswer}
                extraContext={props.extraContext}
                handleSubmitAnswer={props.handleSubmitAnswer} />
        );
    } else if (props.question.question_type === QuestionType.DefinitionsFromHanzi) {
        return (
            <DefinitionFromHanziDisplay
                title="Translate the following word into English:"
                question={props.question}
                isCorrect={props.isCorrect}
                correctAnswer={props.correctAnswer}
                extraContext={props.extraContext}
                handleSubmitAnswer={props.handleSubmitAnswer} />

        );
    } else if (props.question.question_type === QuestionType.AccentsFromHanzi) {
        return (
            <AccentsFromHanziDisplay
                title="Mark the accent numbers for the following word:"
                question={props.question}
                isCorrect={props.isCorrect}
                correctAnswer={props.correctAnswer}
                extraContext={props.extraContext}
                handleSubmitAnswer={props.handleSubmitAnswer} />
        );
    }
    throw Error(`Unrecognized question type ${props.question.question_type}`);
}

export default VocabularyQuestionDisplay;
