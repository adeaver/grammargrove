import { Step, StepProps } from '../common';

import FeedbackForm from '../../../components/FeedbackForm';
import { FeedbackType } from '../../../components/FeedbackForm/api';

const CurrentLearningComponent = (props: StepProps) => {
    const handleSubmit = () => {
        props.advanceToNextStep(Step.Complete);
    }

    return (
        <div class="w-full max-w-2xl flex flex-col space-y-4">
            <FeedbackForm
                type={FeedbackType.Join}
                onSuccess={handleSubmit} />
        </div>
    );
}

export default CurrentLearningComponent;
