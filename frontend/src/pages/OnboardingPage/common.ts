import {
    UserPreferences,
} from '../../common/api/userpreferences';

export type StepProps = {
    userPreferences: UserPreferences | null;

    advanceToNextStep: (s: Step) => void;
    updateUserPreferences: (userPreferences: UserPreferences) => void;
}

export enum Step {
    Welcome = 'welcome',
    HSKLevel = 'hsk-level',
    CurrentLearning = 'current-learning',
    Complete = 'complete'
}
