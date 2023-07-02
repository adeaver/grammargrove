import { useState, useEffect } from 'preact/hooks';

import Header from '../../components/Header';
import Text, { TextFunction } from '../../components/Text';
import LoadingIcon from '../../components/LoadingIcon';

import {
    SubscriptionStatus,
    getSubscriptionStatus,
} from './api';
import AvailablePlanDisplay from './components/AvailablePlanDisplay';

const SubscriptionPage = () => {
    const [ isLoading, setIsLoading ] = useState<boolean>(true);
    const [ subscriptionStatus, setSubscriptionStatus ] = useState<SubscriptionStatus | null>(null);
    const [ error, setError ] = useState<Error | null>(null);

    useEffect(() => {
        getSubscriptionStatus(
            (resp: SubscriptionStatus) => {
                setIsLoading(false);
                setSubscriptionStatus(resp);
            },
            (err: Error) => {
                setIsLoading(false);
                setError(err);
            }
        );
    }, []);

    let body;
    if (isLoading) {
        body = <LoadingIcon />;
    } else if (!!error || !subscriptionStatus) {
        body = (
            <Text function={TextFunction.Warning}>
                Something went wrong, please check back later.
            </Text>
        )
    } else if (
        !!subscriptionStatus.available_plans &&
        !!subscriptionStatus.available_plans.length
    ) {
        body = (
            <AvailablePlanDisplay
                availablePlans={subscriptionStatus.available_plans} />
        );
    }
    return (
        <div>
            <Header />
            { body }
        </div>
    );
}

export default SubscriptionPage;
