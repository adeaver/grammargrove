import Text from '../../../../components/Text';

import { Question, Display } from '../../api';

type GrammarRuleQuestionDisplayProps = {
    question: Question;
}

const GrammarRuleQuestionDisplay = (props: GrammarRuleQuestionDisplayProps) => {
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

export default GrammarRuleQuestionDisplay;
