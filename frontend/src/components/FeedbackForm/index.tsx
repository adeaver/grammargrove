import { useState } from 'preact/hooks';

import { FeedbackType, submitFeedback } from './api';
import NoSubscribeFeedbackForm from './forms/NoSubscribeForm';

export type FeedbackFormProps = {
    type: FeedbackType;
    onSuccess: () => void;
}

const FeedbackForm = (props: FeedbackFormProps) => {
    const [ response, setResponse ] = useState<string>("");
    const [ isLoading, setIsLoading ] = useState<boolean>(false);

    const handleSubmit = () => {
        const strippedResponse = response.trim();
        if (strippedResponse) {
            setIsLoading(true);
             submitFeedback(
                props.type,
                strippedResponse,
                (_) => {
                    setIsLoading(false);
                    props.onSuccess();
                },
                (_) => {
                    setIsLoading(false);
                    props.onSuccess();
                }
             )
        } else {
            props.onSuccess();
        }
    }

    if (props.type === FeedbackType.NoSubscribe) {
        return (
            <NoSubscribeFeedbackForm
                response={response}
                disabled={isLoading}
                handleResponseChange={setResponse}
                handleSubmit={handleSubmit} />
        );

    }
    throw Error(`Unimplemented feedback type ${props.type}`);
}

export default FeedbackForm;
