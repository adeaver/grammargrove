import Text, { TextType } from '../../../../components/Text';
import Card from '../../../../components/Card';

import Input, { InputType } from '../../../../components/Input';
import Button from '../../../../components/Button';

import {
    Question,
    QuestionType,
    Display
} from '../../api';

type GrammarRuleQuestionDisplayProps = {
    question: Question;
}

const GrammarRuleQuestionDisplay = (props: GrammarRuleQuestionDisplayProps) => {
    if (props.question.question_type === QuestionType.HanziFromEnglish) {
        return <GrammarRuleHanziFromDefinitionDisplay question={props.question} />
    } else if (props.question.question_type === QuestionType.DefinitionsFromHanzi) {
        return <GrammarRuleDefinitionFromHanziDisplay question={props.question} />
    } else if (props.question.question_type === QuestionType.AccentsFromHanzi) {
        return <GrammarRuleAccentsFromHanziDisplay question={props.question} />
    }
    throw Error(`Unrecognized question type ${props.question.question_type}`);
}

type GrammarRuleQuestionTypeDisplayProps = {
    question: Question;
}

const GrammarRuleHanziFromDefinitionDisplay = (props: GrammarRuleQuestionTypeDisplayProps) => {
    return (
        <div class="p-12 w-full flex flex-col justify-center items-center space-y-2">
            <Text>
                Translate the following sentence into Mandarin:
            </Text>
            <Text type={TextType.Subtitle}>
                {props.question.display[0].display}
            </Text>
            <div class="max-w-xl flex flex-col space-y-2">
                <Input
                    type={InputType.Text}
                    value=""
                    onChange={(v: string) => console.log(v) }
                    placeholder="Translation"
                    name="answer" />
                <Button onClick={() => {}}>
                    Submit
                </Button>
            </div>
        </div>
    );
}

const GrammarRuleDefinitionFromHanziDisplay = (props: GrammarRuleQuestionTypeDisplayProps) => {
    return (
        <div class="p-12 w-full flex flex-col justify-center items-center space-y-2">
            <Text>
                Translate the following sentence into Mandarin:
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
                    value=""
                    onChange={(v: string) => console.log(v) }
                    placeholder="Translation"
                    name="answer" />
                <Button onClick={() => {}}>
                    Submit
                </Button>
            </div>
        </div>
    );
}

const GrammarRuleAccentsFromHanziDisplay = (props: GrammarRuleQuestionTypeDisplayProps) => {
    return (
        <div class="p-12 w-full flex flex-col justify-center items-center space-y-2">
            <Text>
                Mark the accent numbers for the following words:
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
                                        type={InputType.Text}
                                        value=""
                                        onChange={(v: string) => console.log(v) }
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
                <Button onClick={() => {}}>
                    Submit
                </Button>
            </div>
        </div>
    );
}

export default GrammarRuleQuestionDisplay;
