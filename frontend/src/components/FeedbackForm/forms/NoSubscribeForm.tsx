import Input, { InputType } from '../../../components/Input';
import Button from '../../../components/Button';

type NoSubscribeFeedbackFormProps = {
    response: string;
    placeholder?: string;
    disabled?: boolean;

    handleResponseChange: (v: string) => void;
    handleSubmit: (extraInfo: string[]) => void;
}

const NoSubscribeFeedbackForm = (props: NoSubscribeFeedbackFormProps) => {
    return (
        <div class="flex flex-col space-y-4">
            <Input
                type={InputType.TextArea}
                name="feedback"
                placeholder="Tell us why you’re leaving? (optional)"
                value={props.response}
                disabled={props.disabled}
                onChange={props.handleResponseChange} />
            <Button isDisabled={props.disabled} onClick={() => { props.handleSubmit([]) }}>
                Decline a GrammarGrove Plan
            </Button>
        </div>
    );
}

export default NoSubscribeFeedbackForm;
