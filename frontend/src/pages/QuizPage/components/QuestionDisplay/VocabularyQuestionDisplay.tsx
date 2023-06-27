import Text from '../../../../components/Text';

import { Question, Display } from '../../api';

type VocabularyQuestionDisplayProps = {
    question: Question;
}

const VocabularyQuestionDisplay = (props: VocabularyQuestionDisplayProps) => {
    return (
        <div>
            {
                props.question.display.map((d: Display) => (
                    <Text>
                        {d.display}
                    </Text>
                ))
            }
        </div>
    );
}

export default VocabularyQuestionDisplay;
