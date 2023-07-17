import { useState } from 'preact/hooks';

import Form from '../../../../components/Form';
import Text, { TextFunction, TextType } from '../../../../components/Text';
import Card from '../../../../components/Card';

import Input, { InputType } from '../../../../components/Input';
import Button, { ButtonType } from '../../../../components/Button';

import { Word } from '../../../../common/api';

import {
    Question,
    Display
} from '../../api';

export type QuestionDisplayControllerProps = {
    question: Question;
    isCorrect: boolean | null;
    correctAnswer: string[] | null;
    extraContext: string[] | null;
    words: Word[] | null;
    originalAnswer: string[] | null;

    handleSubmitAnswer: (answer: string[], example_id: string | null | undefined) => void;
    handleGetNextQuestion: () => void;
}

type QuestionDisplayProps = {
    title: string;
    question: Question;
    isCorrect: boolean | null;
    correctAnswer: string[] | null;
    extraContext: string[] | null;
    words: Word[] | null;
    originalAnswer: string[] | null;

    handleSubmitAnswer: (answer: string[], example_id: string | null | undefined) => void;
    handleGetNextQuestion: () => void;
}

export const HanziFromDefinitionDisplay = (props: QuestionDisplayProps) => {
    const [ hanzi, setHanzi ] = useState<string>(
        !!props.originalAnswer && !!props.originalAnswer.length ? props.originalAnswer[0] : ""
    );

    const handleSubmitAnswer = () => {
        props.handleSubmitAnswer([hanzi], props.question.example_id);
    }

    const getExtraContext = () => {
        if (props.isCorrect == null) {
            return null
        }
        const correctAnswer: string | null = !!props.correctAnswer && !!props.correctAnswer.length ? (
            props.correctAnswer.join("")
        ) : null;
        const wordDisplay: string | null = !!props.words && !!props.words.length ? (
            props.words.map((w: Word) => w.display).join("")
        ) : null;
        const wordPronunciation: string | null = !!props.words && !!props.words.length ? (
            props.words.map((w: Word) => w.pronunciation.replace(" ", "")).join(" ")
        ) : null;
        const word: string | null = !!wordDisplay && !!wordPronunciation ? (
            `${wordDisplay} (${wordPronunciation})`
        ) : correctAnswer;

        if (!word) {
            return null;
        } else if (props.isCorrect) {
            return `${word} is the correct translation!`;
        } else {
            return `The correct translation is ${word}`;
        }
    }

    let handleSubmit: () => void = handleSubmitAnswer;
    const extraContext = getExtraContext();
    let action;
    if (props.isCorrect == null) {
        action = (
            <Button isSubmit>
                Submit
            </Button>
        );
    } else if (props.isCorrect) {
        handleSubmit = props.handleGetNextQuestion;
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Confirmation}>
                    That’s correct!
                </Text>
                {
                    !!extraContext && (
                        <Text>
                            {extraContext}
                        </Text>
                    )
                }
                <Button type={ButtonType.Secondary} isSubmit>
                    Next question
                </Button>
            </div>
        );
    } else if (!props.isCorrect) {
        handleSubmit = props.handleGetNextQuestion;
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Warning}>
                     Looks like this one needs some more practice.
                </Text>
                {
                    !!extraContext && (
                        <Text>
                            {extraContext}
                        </Text>
                    )
                }
                <Button type={ButtonType.Secondary} isSubmit>
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
            <Form className="w-full flex flex-col space-y-2" handleSubmit={handleSubmit}>
                <Input
                    type={InputType.Text}
                    value={hanzi}
                    onChange={setHanzi}
                    disabled={props.isCorrect != null}
                    placeholder="Translation"
                    name="answer" />
                {action}
            </Form>
        </div>
    );
}


export const DefinitionFromHanziDisplay = (props: QuestionDisplayProps) => {
    const [ definition, setDefinition ] = useState<string>(
        !!props.originalAnswer && !!props.originalAnswer.length ? props.originalAnswer[0] : ""
    );

    const handleSubmitAnswer = () => {
        props.handleSubmitAnswer([definition], props.question.example_id);
    }

    const getExtraContext = () => {
        if (props.isCorrect == null) {
            return null
        }
        const wordDisplay: string | null = !!props.words && !!props.words.length ? (
            props.words.map((w: Word) => w.display).join("")
        ) : null;
        const wordPronunciation: string | null = !!props.words && !!props.words.length ? (
            props.words.map((w: Word) => w.pronunciation.replace(" ", "")).join(" ")
        ) : null;
        const word: string | null = !!wordDisplay && !!wordPronunciation ? (
            `${wordDisplay} (${wordPronunciation})`
        ) : null;

        if (props.isCorrect) {
            const definition: string | null = !!props.extraContext && !!props.extraContext.length ? (
                props.extraContext.join("; ")
            ) : null;
            if (!!definition && !!word) {
                return `${word} can also mean ${definition}`;
            } else if (!definition && !!word) {
                return `That’s the correct translation of ${word}`;
            } else if (!!definition && !word) {
                return `This can also mean ${definition}`;
            } else {
                return null
            }
        } else {
            const definition: string | null = !!props.correctAnswer && !!props.correctAnswer.length ? (
                props.correctAnswer.join("; ")
            ) : null;
            if (!!definition && !!word) {
                return `${word} means ${definition}`;
            } else if (!definition && !!word) {
                return `That’s the correct translation of ${word}`;
            } else if (!!definition && !word) {
                return `The correct translation is ${definition}`;
            } else {
                return null
            }
        }
    }

    let handleSubmit = handleSubmitAnswer;
    let action;
    const extraContext = getExtraContext();
    if (props.isCorrect == null) {
        action = (
            <Button isSubmit>
                Submit
            </Button>
        );
    } else if (props.isCorrect) {
        handleSubmit = props.handleGetNextQuestion;
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Confirmation}>
                    That’s correct!
                </Text>
                {
                    !!extraContext && (
                        <Text>
                            {extraContext}
                        </Text>
                    )
                }
                <Button type={ButtonType.Secondary} isSubmit>
                    Next question
                </Button>
            </div>
        );
    } else if (!props.isCorrect) {
        handleSubmit = props.handleGetNextQuestion;
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Warning}>
                     Looks like this one needs some more practice.
                </Text>
                {
                    !!extraContext && (
                        <div>
                            <Text>
                                {extraContext}
                            </Text>
                        </div>
                    )
                }
                <Button type={ButtonType.Secondary} isSubmit>
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
            <Form className="w-full flex flex-col space-y-4" handleSubmit={handleSubmit}>
                <Input
                    type={InputType.Text}
                    value={definition}
                    disabled={props.isCorrect != null}
                    onChange={setDefinition}
                    placeholder="Translation"
                    name="answer" />
                { action }
            </Form>
        </div>
    );
}

export const AccentsFromHanziDisplay = (props: QuestionDisplayProps) => {
    const originalAnswer = !!props.originalAnswer && !!props.originalAnswer.length ? [ ...props.originalAnswer ] : null;
    const shiftN = (n: number) => {
        let out: Array<string | undefined> = [];
        if (!originalAnswer) {
            return Array(n).fill("")
        }
        for (let i = 0; i < n; i++) {
            const val = originalAnswer.shift()
            out = out.concat(!!val ? val : "")
        }
        return out
    }

    const [ accents, setAccents ] = useState<string[][]>(
        props.question.display.map((d: Display) => (
            shiftN(d.input_length)
        ))
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

    let handleSubmit = handleSubmitAnswer;
    let action;
    if (props.isCorrect == null) {
        action = (
            <Button isSubmit>
                Submit
            </Button>
        );
    } else if (props.isCorrect) {
        handleSubmit = props.handleGetNextQuestion;
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Confirmation}>
                    That’s correct!
                </Text>
                <Button type={ButtonType.Secondary} isSubmit>
                    Next question
                </Button>
            </div>
        );
    } else if (!props.isCorrect) {
        handleSubmit = props.handleGetNextQuestion;
        action = (
            <div class="flex flex-col space-y-4">
                <Text type={TextType.Subtitle} function={TextFunction.Warning}>
                     Looks like this one needs some more practice.
                </Text>
                {
                    !!props.extraContext && !!props.extraContext.length && (
                        <div>
                            <Text>
                                {`The right answer is ${ props.extraContext.join(' ') }.`}
                            </Text>
                            {
                                !!props.correctAnswer && !!props.correctAnswer.length && (
                                    <Text type={TextType.FinePrint}>
                                        {`(${ props.correctAnswer.join(' ')})`}
                                    </Text>
                                )
                            }
                        </div>
                    )
                }
                <Button type={ButtonType.Secondary} isSubmit>
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
                                        disabled={props.isCorrect != null}
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
            <Form className="w-full flex flex-col space-y-4" handleSubmit={handleSubmit}>
                { action }
            </Form>
        </div>
    );
}
