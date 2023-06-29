import { useState } from 'preact/hooks';

import Text, { TextType } from '../../../../components/Text';
import Card from '../../../../components/Card';

import Input, { InputType } from '../../../../components/Input';
import Button from '../../../../components/Button';

import {
    Question,
    Display
} from '../../api';

type QuestionDisplayProps = {
    title: string;
    question: Question;

    handleSubmitAnswer: (answer: string[], example_id: string | null | undefined) => void;
}

export const HanziFromDefinitionDisplay = (props: QuestionDisplayProps) => {
    const [ hanzi, setHanzi ] = useState<string>("");

    const handleSubmitAnswer = () => {
        props.handleSubmitAnswer([hanzi], props.question.example_id);
    }

    return (
        <div class="p-12 w-full flex flex-col justify-center items-center space-y-2">
            <Text>
                {props.title}
            </Text>
            <Text type={TextType.Subtitle}>
                {props.question.display[0].display}
            </Text>
            <div class="max-w-xl flex flex-col space-y-2">
                <Input
                    type={InputType.Text}
                    value={hanzi}
                    onChange={setHanzi}
                    placeholder="Translation"
                    name="answer" />
                <Button onClick={handleSubmitAnswer}>
                    Submit
                </Button>
            </div>
        </div>
    );
}


export const DefinitionFromHanziDisplay = (props: QuestionDisplayProps) => {
    const [ definition, setDefinition ] = useState<string>("");

    const handleSubmitAnswer = () => {
        props.handleSubmitAnswer([definition], props.question.example_id);
    }

    return (
        <div class="p-12 w-full flex flex-col justify-center items-center space-y-2">
            <Text>
                {props.title}
            </Text>
            <div class="flex flex-col md:flex-row md:space-x-2">
            {
                props.question.display.map((d: Display, idx: number) => (
                    <Card key={`question-${props.question.id}-${idx}`}>
                        <Text type={TextType.Subtitle}>
                            {d.display}
                        </Text>
                    </Card>
                ))
            }
            </div>
            <div class="max-w-xl flex flex-col space-y-2">
                <Input
                    type={InputType.Text}
                    value={definition}
                    onChange={setDefinition}
                    placeholder="Translation"
                    name="answer" />
                <Button onClick={handleSubmitAnswer}>
                    Submit
                </Button>
            </div>
        </div>
    );
}

export const AccentsFromHanziDisplay = (props: QuestionDisplayProps) => {
    const [ accents, setAccents ] = useState<string[][]>(
        props.question.display.map((d: Display) => Array(d.input_length).fill(""))
    );

    const handleUpdateAccent = (idx: number, subIdx: number, value: string) => {
        setAccents(
            accents.map((currValue: string[], currIdx: number) => {
                if (currIdx === idx) {
                    currValue[subIdx] = value
                }
                return currValue;
            })
        )
    }

    const handleSubmitAnswer = () => {
        props.handleSubmitAnswer(accents.flat(), props.question.example_id);
    }

    return (
        <div class="p-12 w-full flex flex-col justify-center items-center space-y-2">
            <Text>
                {props.title}
            </Text>
            <div class="flex flex-col md:flex-row md:space-x-2">
            {
                props.question.display.map((d: Display, idx: number) => (
                    <Card key={`question-${props.question.id}-${idx}`}>
                        <div class="flex flex-row md:flex-col md:space-y-2 items-center justify-center space-x-2 md:space-x-0">
                            <Text type={TextType.Subtitle}>
                                {d.display}
                            </Text>
                            <div class="flex flex-col md:flex-row md:space-x-2 items-center justify-center">
                            {
                                Array(d.input_length).fill(0).map((_, inputIdx: number) => (
                                    <Input
                                        type={InputType.Number}
                                        value={accents[idx][inputIdx]}
                                        onChange={(v: string) => handleUpdateAccent(idx, inputIdx, v)}
                                        key={`answer-${inputIdx}-${idx}`}
                                        name={`answer-${inputIdx}-${idx}`} />
                                ))
                            }
                            </div>
                        </div>
                    </Card>
                ))
            }
            </div>
            <div class="max-w-xl flex flex-col space-y-2">
                <Button onClick={handleSubmitAnswer}>
                    Submit
                </Button>
            </div>
        </div>
    );
}
