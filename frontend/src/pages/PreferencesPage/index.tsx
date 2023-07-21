import { useState, useEffect } from 'preact/hooks';

import Header from '../../components/Header';
import LoadingIcon from '../../components/LoadingIcon';
import Text, { TextFunction } from '../../components/Text';

import {
    UserPreferences,

    getUserPreferences,
} from '../../common/api/userpreferences';

import UserPreferencesBody from './components/UserPreferencesBody';

const PreferencesPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ error, setError ] = useState<Error | null>(null);

    const [ userPreferences, setUserPreferences ] = useState<UserPreferences | null>(null);

    useEffect(() => {
        getUserPreferences(
            (resp: UserPreferences[]) => {
                setIsLoading(false);
                if (!!resp.length) {
                    setUserPreferences(resp[0]);
                } else {
                    setUserPreferences(null);
                }
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
        )
    } else {
        body = (
            <UserPreferencesBody
                userPreferences={userPreferences}
                setUserPreferences={setUserPreferences}
                setIsLoading={setIsLoading}
                setError={setError} />
        );
    }

    return (
        <div class="w-full min-h-screen">
            <Header />
            <div class="p-6 max-w-full flex flex-col space-y-4 items-center justify-center">
                { body }
            </div>
        </div>
    );
}

export default PreferencesPage;
