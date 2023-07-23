import { useState } from 'preact/hooks';

import Text, { TextType } from '../../../components/Text';
import Button from '../../../components/Button';
import Checkbox from '../../../components/Checkbox';
import Link from '../../../components/Link';

import {
    UserPreferences,
    UserPreferencesBody,

    updateUserVocabularyAndGrammarLists,
    UpdateUserVocabularyAndGrammarListsResponse,
} from '../../../common/api/userpreferences';
import {
    getUserPreferencesBody,
    getUserPreferencesUpdateOrCreateFunc
} from '../../../common/userpreferences';

import HSKLevelDisplay from '../../../common/userpreferences/hskLevel';

type UserPreferencesBodyComponentProps = {
    userPreferences: UserPreferences | null;

    setIsLoading: (isLoading: boolean) => void;
    setUserPreferences: (u: UserPreferences) => void;
    setError: (err: Error) => void;
}

const UserPreferencesBodyComponent = (props: UserPreferencesBodyComponentProps) => {
    const [ shouldUpdateUserLists, setShouldUpdateUserLists ] = useState<boolean>(false);
    const [ userPreferencesBody, setUserPreferencesBody ] = useState<UserPreferencesBody>(
        getUserPreferencesBody(props.userPreferences)
    )

    const update = getUserPreferencesUpdateOrCreateFunc(
        props.userPreferences,
        (resp: UserPreferences) => {
            props.setUserPreferences(resp);
            if (shouldUpdateUserLists) {
                updateUserVocabularyAndGrammarLists(
                    resp.id,
                    (_: UpdateUserVocabularyAndGrammarListsResponse) => {
                        props.setIsLoading(false);
                        setShouldUpdateUserLists(false);
                        props.setUserPreferences(resp);
                    },
                    (err: Error) => {
                        props.setIsLoading(false);
                        props.setError(err);
                    }
                );
            } else {
                props.setIsLoading(false);
            }
        },
        (err: Error) => {
            props.setIsLoading(false);
            props.setError(err);
        }
    )

    const handleSubmit = () => {
        props.setIsLoading(true);
        update(userPreferencesBody)
    }

    const handleUpdateHSKLevel = (i: number) => {
        setUserPreferencesBody({
            ...userPreferencesBody,
            hsk_level: i,
        });
        setShouldUpdateUserLists(true);
    }

    const handleUpdateEmailUpdate = (name: string, isChecked: boolean) => {
        setUserPreferencesBody({
            ...userPreferencesBody,
            [name]: isChecked,
        });
    }

    return (
        <div class="w-full max-w-2xl flex flex-col items-center justify-center space-y-4">
            <Text type={TextType.Title}>
                Update your preferences
            </Text>
            <hr />
            <Text type={TextType.Subtitle}>
                Your current Mandarin level
            </Text>
            <HSKLevelDisplay
                currentHSKLevel={userPreferencesBody.hsk_level}
                setCurrentHSKLevel={handleUpdateHSKLevel} />
            <Text type={TextType.FinePrint}>
                This will update your grammar and vocabulary lists
            </Text>
            <hr />
            <Text type={TextType.Subtitle}>
                Email Preferences
            </Text>
            <Checkbox
                name="daily-email"
                label="Enable Daily Practice Reminder Email"
                isChecked={userPreferencesBody.daily_practice_reminders_enabled}
                value="daily_practice_reminders_enabled"
                onChange={handleUpdateEmailUpdate} />
            <hr />
            {
                !!props.userPreferences && !!props.userPreferences.subscription_management_link && (
                    <div class="py-2 w-full flex flex-col space-y-4">
                        <Text type={TextType.Subtitle}>
                            Subscription & Payment
                        </Text>
                        <Link href={props.userPreferences.subscription_management_link}>
                            Click here to manage your payment information
                        </Link>
                    </div>
                )
            }
            <Button onClick={handleSubmit}>
                Update your preferences
            </Button>
        </div>
    )
}

export default UserPreferencesBodyComponent;
