import {
    UserPreferences,
    UserPreferencesBody,
    getDefaultUserPreferencesBody,
    updateUserPreferences,
    createUserPreferences,
} from '../../common/api/userpreferences';

export function getUserPreferencesBody(
    userPreferences: UserPreferences | null
) {
    if (!userPreferences) {
        return getDefaultUserPreferencesBody();
    }
    return {
        hsk_level: userPreferences.hsk_level,
        daily_practice_reminders_enabled: userPreferences.daily_practice_reminders_enabled,
    }
}

export function getUserPreferencesUpdateOrCreateFunc(
    userPreferences: UserPreferences | null,
    onSuccess: (u: UserPreferences) => void,
    onError: (err: Error) => void,
) {
    return (body: UserPreferencesBody) => {
        if (!userPreferences) {
            createUserPreferences(
                body, onSuccess, onError
            );
        } else {
            updateUserPreferences(userPreferences.id, body, onSuccess, onError)
        }
    }
}
