import { useEffect, useState } from 'preact/hooks';

import Header from '../../components/Header';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';

import {
    UserPreferences,
    getUserPreferences,
} from '../../common/api/userpreferences';

import { setLocation } from '../../util/window';

import { Step } from './common';
import WelcomeComponent from './components/WelcomeComponent';
import HSKLevelComponent from './components/HSKLevelComponent';
import CurrentLearningComponent from './components/CurrentLearningComponent';

const OnboardingPage = () => {
    const [ currentStep, setCurrentStep ] = useState<Step>(Step.Welcome);

    const [ userPreferences, setUserPreferences ] = useState<UserPreferences | null>(null);
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ error, setError ] = useState<Error | null>(null);

    useEffect(() => {
        getUserPreferences(
            (resp: UserPreferences[]) => {
                setIsLoading(false);
                setUserPreferences(
                    resp.length ? resp[0] : null
                )
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }, []);

    let body;
    if (isLoading) {
        body = (
            <LoadingIcon />
        );
    } else if (!!error) {
        body = (
            <Text function={TextFunction.Warning}>
                Something went wrong, try again later.
            </Text>
        );
    } else if (currentStep === Step.Welcome) {
        body = (
            <WelcomeComponent
                userPreferences={userPreferences}
                updateUserPreferences={setUserPreferences}
                advanceToNextStep={setCurrentStep} />
        );
    } else if (currentStep === Step.HSKLevel) {
        body = (
            <HSKLevelComponent
                userPreferences={userPreferences}
                updateUserPreferences={setUserPreferences}
                advanceToNextStep={setCurrentStep} />
        );
    } else if (currentStep === Step.CurrentLearning) {
        body = (
            <CurrentLearningComponent
                userPreferences={userPreferences}
                updateUserPreferences={setUserPreferences}
                advanceToNextStep={setCurrentStep} />
        );
    } else if (currentStep === Step.Complete) {
        setLocation("/dashboard/");
    } else {
        throw Error(`Unrecognized onboarding step ${currentStep}`);
    }

    return (
        <div>
            <Header />
            <div class="w-full flex items-center justify-center">
                { body }
            </div>
        </div>
    );
}



export default OnboardingPage;
