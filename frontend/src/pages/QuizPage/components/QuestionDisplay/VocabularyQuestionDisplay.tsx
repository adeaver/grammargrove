import {
    Question,
    QuestionType,
} from '../../api';

import {
    HanziFromDefinitionDisplay,
    DefinitionFromHanziDisplay,
    AccentsFromHanziDisplay
} from './common';

type VocabularyQuestionDisplayProps = {
    question: Question;
}

const VocabularyQuestionDisplay = (props: VocabularyQuestionDisplayProps) => {
    if (props.question.question_type === QuestionType.HanziFromEnglish) {
        return (
            <HanziFromDefinitionDisplay
                title="What is the Mandarin word that means the following:"
                question={props.question} />
        );
    } else if (props.question.question_type === QuestionType.DefinitionsFromHanzi) {
        return (
            <DefinitionFromHanziDisplay
                title="Translate the following word into English:"
                question={props.question} />
        );
    } else if (props.question.question_type === QuestionType.AccentsFromHanzi) {
        return (
            <AccentsFromHanziDisplay
                title="Mark the accent numbers for the following word:"
                question={props.question} />
        );
    }
    throw Error(`Unrecognized question type ${props.question.question_type}`);
}

export default VocabularyQuestionDisplay;
