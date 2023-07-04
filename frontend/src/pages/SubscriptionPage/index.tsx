import { useState, useEffect } from 'preact/hooks';

import Header from '../../components/Header';
import Text, { TextFunction, TextType } from '../../components/Text';
import Link from '../../components/Link';
import Button from '../../components/Button';
import LoadingIcon from '../../components/LoadingIcon';

import { setLocation } from '../../util/window';

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
    } else if (
        !!subscriptionStatus.management_url
    ) {
        body = (
            <div class="w-full p-12 flex flex-col items-center justify-center space-y-4">
                <Text type={TextType.Subtitle}>
                    You already have a subscription to GrammarGrove.
                </Text>
                <Link href={subscriptionStatus.management_url}>
                    Click here to manage it
                </Link>
                <Button className="max-w-lg" onClick={() => setLocation('/dashboard/')}>
                    Get back to practicing
                </Button>
            </div>
        )
    }
    return (
        <div>
            <Header />
            { body }
        </div>
    );
}

export default SubscriptionPage;
