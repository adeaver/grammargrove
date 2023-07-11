import { useState } from 'preact/hooks';

import Form from '../../../components/Form';
import Input, { InputType } from '../../../components/Input';
import Checkbox from '../../../components/Checkbox';
import Button from '../../../components/Button';
import Text, { TextType } from '../../../components/Text';

type JoinFormProps = {
    response: string;
    placeholder?: string;
    disabled?: boolean;

    handleResponseChange: (v: string) => void;
    handleSubmit: (extraInfo: string[]) => void;
}

type Option = {
    text: string;
    value: string;
}

const options: Option[] = [
    { text: "YoYo Chinese", value: "yoyo-chinese" },
    { text: "Duolingo", value: "duolingo" },
    { text: "Hello Chinese", value: "hello-chinese" },
    { text: "In Person Class", value: "in-person-class" },
    { text: "Language Tutor (including italki)", value: "italki" },
    { text: "YouTube Courses", value: "youtube" },
    { text: "Textbook", value: "textbook" },
]

const JoinForm = (props: JoinFormProps) => {
    const [ checkedValues, setCheckedValues ] = useState<string[]>([]);

    const handleChange = (value: string, isChecked: boolean) => {
        let newCheckedValues = checkedValues.filter((v: string) => v !== value);
        if (isChecked) {
            newCheckedValues = newCheckedValues.concat(value)
        }
        setCheckedValues(newCheckedValues);
    }

    const handleSubmit = () => {
        props.handleSubmit(checkedValues);
    }

    return (
        <Form className="flex flex-col space-y-4" handleSubmit={handleSubmit}>
            <Text type={TextType.Title}>
                How are you currently learning Mandarin?
            </Text>
            <Text type={TextType.SectionHeader}>
                Check all that apply.
            </Text>
            <div class="grid grid-cols-2">
            {
                options.map((o: Option) => (
                    <Checkbox
                        className="col-span-2 md:col-span-1"
                        name={o.value}
                        label={o.text}
                        value={o.value}
                        onChange={handleChange}
                        isChecked={checkedValues.some((v: string) => v === o.value)} />
                ))
            }
            </div>
            <Input
                type={InputType.Text}
                name="other"
                placeholder="Other:"
                value={props.response}
                disabled={props.disabled}
                onChange={props.handleResponseChange} />
            <Button isDisabled={props.disabled} isSubmit>
                Submit
            </Button>
        </Form>
    );
}

export default JoinForm;
