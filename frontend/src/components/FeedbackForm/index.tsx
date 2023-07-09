import { useState } from 'preact/hooks';

import { FeedbackType, submitFeedback } from './api';
import NoSubscribeFeedbackForm from './forms/NoSubscribeForm';
import PulseForm from './forms/PulseForm';

export type FeedbackFormProps = {
    type: FeedbackType;
    onSuccess: () => void;
}

const FeedbackForm = (props: FeedbackFormProps) => {
    const [ response, setResponse ] = useState<string>("");
    const [ isLoading, setIsLoading ] = useState<boolean>(false);

    const handleSubmit = (extraInfo: string[]) => {
        let strippedResponse = response.trim();
        if (extraInfo.length) {
            strippedResponse = `${extraInfo.join(', ')} ${strippedResponse}`;
        }
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

    } else if (props.type === FeedbackType.Pulse) {
        return (
            <PulseForm
                response={response}
                disabled={isLoading}
                handleResponseChange={setResponse}
                handleSubmit={handleSubmit} />
        )
    }
    throw Error(`Unimplemented feedback type ${props.type}`);
}

export default FeedbackForm;
