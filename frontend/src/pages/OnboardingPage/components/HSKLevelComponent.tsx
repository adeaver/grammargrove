import { useState } from 'preact/hooks';

import LoadingIcon from '../../../components/LoadingIcon';
import Text, { TextType, TextFunction } from '../../../components/Text';
import Button from '../../../components/Button';

import HSKLevelDisplay from '../../../common/userpreferences/hskLevel';

import {
    UserPreferences,

    updateUserVocabularyAndGrammarLists,
    UpdateUserVocabularyAndGrammarListsResponse,
} from '../../../common/api/userpreferences';
import {
    getUserPreferencesBody,
    getUserPreferencesUpdateOrCreateFunc
} from '../../../common/userpreferences';

import { Step, StepProps } from '../common';

const HSKLevelComponent = (props: StepProps) => {
    const [ currentHSKLevel, setCurrentHSKLevel ] = useState<number>(
        !!props.userPreferences && props.userPreferences.hsk_level != null ? (
            props.userPreferences.hsk_level
        ) : 0
    );
    const [ isLoading, setIsLoading ] = useState<boolean>(false);
    const [ error, setError ] = useState<Error | null>(null);

    const updateFunc = getUserPreferencesUpdateOrCreateFunc(
        props.userPreferences,
        (resp: UserPreferences) => {
            updateUserVocabularyAndGrammarLists(
                resp.id,
                (_: UpdateUserVocabularyAndGrammarListsResponse) => {
                    setIsLoading(false);
                    props.updateUserPreferences(resp);
                    props.advanceToNextStep(Step.CurrentLearning);
                },
                (err: Error) => {
                    setIsLoading(false);
                    setError(err);
                }
            );
        },
        (err: Error) => {
            setIsLoading(false);
            setError(err);
        }
    );
    const handleSubmit = () => {
        setIsLoading(true);
        updateFunc({
            ...getUserPreferencesBody(props.userPreferences),
            hsk_level: currentHSKLevel,
        })
    }


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
            <HSKLevelDisplay
                currentHSKLevel={currentHSKLevel}
                setCurrentHSKLevel={setCurrentHSKLevel} />
            <Button onClick={handleSubmit}>
                Submit
            </Button>
        </div>
    );
}

export default HSKLevelComponent;
