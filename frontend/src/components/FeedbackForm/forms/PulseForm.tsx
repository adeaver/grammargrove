import { useState } from 'preact/hooks';

import Form from '../../../components/Form';
import Input, { InputType } from '../../../components/Input';
import Button from '../../../components/Button';
import RadioButton from '../../../components/RadioButton';
import Text, { TextType } from '../../../components/Text';

type PulseFormProps = {
    response: string;
    placeholder?: string;
    disabled?: boolean;

    handleResponseChange: (v: string) => void;
    handleSubmit: () => void;
}

const NoSubscribeFeedbackForm = (props: PulseFormProps) => {
    const [ responseIsPositive, setResponseIsPositive ] = useState<boolean>(false);

    const handleSubmit = () => {
        const responsePositivity = responseIsPositive ? "[POSITIVE]" : "[NEGATIVE]";
        props.handleResponseChange(`${responsePositivity} ${props.response}`);
        props.handleSubmit()
    }

    return (
        <Form className="flex flex-col space-y-4" handleSubmit={handleSubmit}>
            <Text type={TextType.SectionHeader}>
                Quick question! How is your experience with Grammar Grove?
            </Text>
            <div
                class="flex flex-row space-x-2 items-center"
                onClick={() => setResponseIsPositive(true)}>
                <RadioButton isSelected={responseIsPositive} />
                <Text>
                    I’m enjoying GrammarGrove
                </Text>
            </div>
            <div
                class="flex flex-row space-x-2 items-center"
                onClick={() => setResponseIsPositive(false)}>
                <RadioButton isSelected={!responseIsPositive} />
                <Text>
                    I’m NOT enjoying GrammarGrove
                </Text>
            </div>
            <Input
                type={InputType.TextArea}
                name="feedback"
                placeholder="Got any feedback for us? (Optional)"
                value={props.response}
                disabled={props.disabled}
                onChange={props.handleResponseChange} />
            <Button isDisabled={props.disabled} isSubmit>
                Submit your feedback
            </Button>
        </Form>
    );
}

export default NoSubscribeFeedbackForm;
