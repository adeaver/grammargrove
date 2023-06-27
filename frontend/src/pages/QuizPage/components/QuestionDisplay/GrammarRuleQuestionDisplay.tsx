import Text from '../../../../components/Text';
import Card from '../../../../components/Card';

import { Question, Display } from '../../api';

type GrammarRuleQuestionDisplayProps = {
    question: Question;
}

const GrammarRuleQuestionDisplay = (props: GrammarRuleQuestionDisplayProps) => {
    return (
        <div>
            <div class="flex space-x-2">
            {
                props.question.display.map((d: Display, idx: number) => (
                    <Card key={`question-${props.question.id}-${idx}`}>
                        <Text>
                            {d.display}
                        </Text>
                    </Card>
                ))
            }
            </div>
        </div>
    );
}

export default GrammarRuleQuestionDisplay;
