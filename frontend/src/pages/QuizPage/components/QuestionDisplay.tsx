import { useState } from 'preact/hooks';
import Input, { InputType } from '../../../components/Input';

import { Question, QuestionType } from '../api';

type QuestionDisplayProps = {
    question: Question
}

const QuestionDisplay = (props: QuestionDisplayProps) => {
    switch (props.question.question_type) {
        case QuestionType.AccentsFromHanzi:
            return <AccentsFromHanziDisplay {...props} />
        case QuestionType.DefinitionsFromHanzi:
            return <DefinitionsFromHanziDisplay {...props} />
        case QuestionType.HanziFromEnglish:
            return <HanziFromDefinitionDisplay {...props} />
        default:
            throw new Error("Unrecognized question type");
    }
}

const AccentsFromHanziDisplay = (props: QuestionDisplayProps) => {
    const characters = props.question.display.split('');
    const [ accentsByCharacter, setAccentsByCharacter ] = useState<(number | null)[]>(characters.map((_) => null));

    const handleSetAccentsByCharacter = (idx: number) => {
        return (v: string) => {
            const value = parseInt(v, 10)
            setAccentsByCharacter(
                accentsByCharacter.map((currValue: number | null, currIdx: number) => {
                    if (idx !== currIdx) {
                        return currValue;
                    } else if (isNaN(value)) {
                        return null
                    } else {
                        return value
                    }
                })
            )
        }
    }

    // TODO: handle case in which the pinyin is not the same as the number of characters
    return (
        <div>
            <p>What are the accents of these characters?</p>
            { /* TODO: add tooltips here */ }
            <p>Type the accent numbers in the boxes below</p>
            {
                characters.map((c: string, idx: number) => {
                    return (
                        <div>
                            <Input
                                type={InputType.Number}
                                name={`hanzi-accent-${props.question.question_id}-${idx}`}
                                value={accentsByCharacter[idx] != null ? `${accentsByCharacter[idx]}` : ""}
                                placeholder=""
                                onChange={handleSetAccentsByCharacter(idx)} />
                            <p>{c}</p>
                        </div>
                    );
                })
            }
        </div>
    )
}

const DefinitionsFromHanziDisplay = (props: QuestionDisplayProps) => {
    const [ definition, setDefinition ] = useState<string>("");

    return (
        <div>
            <p>What is the definition of {props.question.display}?</p>
            <Input
                type={InputType.Text}
                name={`hanzi-definition-${props.question.question_id}`}
                value={definition}
                placeholder="Definition"
                onChange={setDefinition} />
        </div>
    );
}

const HanziFromDefinitionDisplay = (props: QuestionDisplayProps) => {
    const [ hanzi, setHanzi ] = useState<string>("");

    return (
        <div>
            { /* TODO: allow both hanzi and pinyin here */ }
            <p>What is the Hanzi that means {props.question.display}?</p>
            <Input
                type={InputType.Text}
                name={`hanzi-${props.question.question_id}`}
                value={hanzi}
                placeholder="Hanzi"
                onChange={setHanzi} />
        </div>
    );
}

export default QuestionDisplay;
