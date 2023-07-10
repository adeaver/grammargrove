import { Step, StepProps } from '../common';

import Text, { TextType } from '../../../components/Text';
import Button from '../../../components/Button';


const WelcomeComponent = (props: StepProps) => {
    return (
        <div class="w-full max-w-2xl flex flex-col space-y-4">
            <Text type={TextType.Title}>
                Welcome to GrammarGrove
            </Text>
            <Text>
                We have a couple of a questions to get you started.
            </Text>
            <Text>
                We promise it will be really quick.
            </Text>
            <Button onClick={() => props.advanceToNextStep(Step.HSKLevel)}>
                Get started
            </Button>
        </div>
    )
}

export default WelcomeComponent;
