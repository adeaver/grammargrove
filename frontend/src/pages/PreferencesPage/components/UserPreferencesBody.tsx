import {
    UserPreferences
} from '../../../common/api/userpreferences';

type UsserPreferencesBodyProps = {
    userPreferences: UserPreferences | null;

    setUserPreferences: (u: UserPreferences) => void;
}

const UserPreferencesBody = (props: UsserPreferencesBodyProps) => {
    return (
        <div>
            {
                props.userPreferences && props.userPreferences.daily_practice_reminders_enabled && (
                    'Enabled'
                )
            }
        </div>
    )
}

export default UserPreferencesBody;
