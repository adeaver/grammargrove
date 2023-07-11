import { useState } from 'preact/hooks';

import LoadingIcon from '../../../components/LoadingIcon';
import Text, { TextType, TextFunction } from '../../../components/Text';
import RadioButton from '../../../components/RadioButton';
import Button from '../../../components/Button';

import {
    UserPreferences,
    updateUserPreferences,
    createUserPreferences,
} from '../../../common/api/userpreferences';

import { Step, StepProps } from '../common';

type Option = {
    hskLevel: number;
    text: string;
}

const HSKLevelComponent = (props: StepProps) => {
    const [ currentHSKLevel, setCurrentHSKLevel ] = useState<number>(
        !!props.userPreferences && props.userPreferences.hsk_level != null ? (
            props.userPreferences.hsk_level
        ) : 0
    );
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const handleSubmit = () => {
        setIsLoading(true);
        if (!props.userPreferences) {
            createUserPreferences({
                hsk_level: currentHSKLevel,
            },
            (resp: UserPreferences) => {
                setIsLoading(false);
                props.updateUserPreferences(resp);
                props.advanceToNextStep(Step.CurrentLearning);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            });
        } else {
            updateUserPreferences(
                props.userPreferences!.id, {
                ...props.userPreferences!,
                hsk_level: currentHSKLevel,
            },
            (resp: UserPreferences) => {
                setIsLoading(false);
                props.updateUserPreferences(resp);
                props.advanceToNextStep(Step.CurrentLearning);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            })
        }
    }

    const options: Option[] = [
        { hskLevel: 0, text: "Just starting out (Not quite HSK 1)" },
        { hskLevel: 1, text: "Beginner (HSK 1)" },
        { hskLevel: 2, text: "Lower Intermediate (HSK 2)" },
        { hskLevel: 3, text: "Intermediate (HSK 3)" },
        { hskLevel: 4, text: "Upper Intermediate (HSK 4)" },
        { hskLevel: 5, text: "Lower Advanced (HSK 5)" },
        { hskLevel: 6, text: "Advanced (HSK 6)" },
    ]

    if (isLoading) {
        return (
            <div class="w-full max-w-2xl flex flex-col space-y-4">
                <LoadingIcon />
            </div>
        );
    } else if (!!error) {
        return (
            <div class="w-full max-w-2xl flex flex-col space-y-4">
                <Text function={TextFunction.Warning}>
                    Something went wrong, try again later!
                </Text>
            </div>
        );
    }

    return (
        <div class="w-full max-w-2xl flex flex-col space-y-4">
            <Text type={TextType.Title}>
                What’s your current level of Mandarin?
            </Text>
            {
                options.map((o: Option) => (
                    <div class="flex flex-row space-x-2" onClick={() => setCurrentHSKLevel(o.hskLevel)}>
                        <RadioButton isSelected={currentHSKLevel === o.hskLevel} />
                        <Text>
                            { o.text }
                        </Text>
                    </div>
                ))
            }
            <Button onClick={handleSubmit}>
                Submit
            </Button>
        </div>
    );
}

export default HSKLevelComponent;
