import { useState } from 'preact/hooks';

import Text, { TextFunction, TextType } from '../../../../components/Text';
import Card from '../../../../components/Card';

import Input, { InputType } from '../../../../components/Input';
import Button, { ButtonType } from '../../../../components/Button';

import {
    Question,
    Display
} from '../../api';

export type QuestionDisplayControllerProps = {
    question: Question;
    isCorrect: boolean | null;
    correctAnswer: string[] | null;
    extraContext: string[] | null;

    handleSubmitAnswer: (answer: string[], example_id: string | null | undefined) => void;
}

type QuestionDisplayProps = {
    title: string;
    question: Question;
    isCorrect: boolean | null;
    correctAnswer: string[] | null;
    extraContext: string[] | null;

    handleSubmitAnswer: (answer: string[], example_id: string | null | undefined) => void;
}

export const HanziFromDefinitionDisplay = (props: QuestionDisplayProps) => {
    const [ hanzi, setHanzi ] = useState<string>("");

    const handleSubmitAnswer = () => {
        props.handleSubmitAnswer([hanzi], props.question.example_id);
    }

    let action;
    if (props.isCorrect == null) {
        action = (
            <Button onClick={handleSubmitAnswer}>
                Submit
            </Button>
        );
    } else if (props.isCorrect) {
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Confirmation}>
                    That’s correct!
                </Text>
                <Button type={ButtonType.Secondary} onClick={() => console.log("next")}>
                    Next question
                </Button>
            </div>
        );
    } else if (!props.isCorrect) {
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Warning}>
                     Looks like this one needs some more practice.
                </Text>
                {
                    !!props.correctAnswer && (
                        <Text>
                            {`The right answer is ${ props.correctAnswer.join('') }.`}
                        </Text>
                    )
                }
                <Button type={ButtonType.Secondary} onClick={() => console.log("next")}>
                    Next question
                </Button>
            </div>
        );
    }
    return (
        <div class="p-12 w-full max-w-2xl flex flex-col justify-center items-center space-y-4">
            <Text>
                {props.title}
            </Text>
            <Text type={TextType.Subtitle}>
                {props.question.display[0].display}
            </Text>
            <div class="w-full flex flex-col space-y-2">
                <Input
                    type={InputType.Text}
                    value={hanzi}
                    onChange={setHanzi}
                    disabled={props.isCorrect != null}
                    placeholder="Translation"
                    name="answer" />
                {action}
            </div>
        </div>
    );
}


export const DefinitionFromHanziDisplay = (props: QuestionDisplayProps) => {
    const [ definition, setDefinition ] = useState<string>("");

    const handleSubmitAnswer = () => {
        props.handleSubmitAnswer([definition], props.question.example_id);
    }

    let action;
    if (props.isCorrect == null) {
        action = (
            <Button onClick={handleSubmitAnswer}>
                Submit
            </Button>
        );
    } else if (props.isCorrect) {
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Confirmation}>
                    That’s correct!
                </Text>
                {
                    !!props.extraContext && (
                        <Text>
                            {`This can also mean: ${props.extraContext.join('; ')}`}
                        </Text>
                    )
                }
                <Button type={ButtonType.Secondary} onClick={() => console.log("next")}>
                    Next question
                </Button>
            </div>
        );
    } else if (!props.isCorrect) {
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Warning}>
                     Looks like this one needs some more practice.
                </Text>
                {
                    !!props.correctAnswer && (
                        <div>
                            <Text>
                                {`The right answer is ${ props.correctAnswer.join('; ') }.`}
                            </Text>
                        </div>
                    )
                }
                <Button type={ButtonType.Secondary} onClick={() => console.log("next")}>
                    Next question
                </Button>
            </div>
        );
    }

    return (
        <div class="p-12 w-full max-w-2xl flex flex-col justify-center items-center space-y-4">
            <Text>
                {props.title}
            </Text>
            <Text type={TextType.Subtitle}>
                {props.question.display.map((d: Display) => d.display).join('')}
            </Text>
            <div class="w-full flex flex-col space-y-4">
                <Input
                    type={InputType.Text}
                    value={definition}
                    onChange={setDefinition}
                    placeholder="Translation"
                    name="answer" />
                { action }
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

    let action;
    if (props.isCorrect == null) {
        action = (
            <Button onClick={handleSubmitAnswer}>
                Submit
            </Button>
        );
    } else if (props.isCorrect) {
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Confirmation}>
                    That’s correct!
                </Text>
                <Button type={ButtonType.Secondary} onClick={() => console.log("next")}>
                    Next question
                </Button>
            </div>
        );
    } else if (!props.isCorrect) {
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Warning}>
                     Looks like this one needs some more practice.
                </Text>
                {
                    !!props.extraContext && (
                        <div>
                            <Text>
                                {`The right answer is ${ props.extraContext.join(' ') }.`}
                            </Text>
                            {
                                !!props.correctAnswer && (
                                    <Text type={TextType.FinePrint}>
                                        {`(${ props.correctAnswer.join(' ')}.)`}
                                    </Text>
                                )
                            }
                        </div>
                    )
                }
                <Button type={ButtonType.Secondary} onClick={() => console.log("next")}>
                    Next question
                </Button>
            </div>
        );
    }
    return (
        <div class="p-12 w-full max-w-2xl flex flex-col justify-center items-center space-y-4">
            <Text>
                {props.title}
            </Text>
            <div class="flex flex-col">
            {
                props.question.display.map((d: Display, idx: number) => (
                    <Card key={`question-${props.question.id}-${idx}`}>
                        <div class="flex flex-row items-center justify-center space-x-2">
                            <Text type={TextType.Subtitle}>
                                {d.display}
                            </Text>
                            <div class="flex flex-col items-center justify-center">
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
            <div class="w-full flex flex-col space-y-4">
                { action }
            </div>
        </div>
    );
}
