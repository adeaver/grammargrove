import Text, { TextType } from '../../../components/Text';
import Card from '../../../components/Card';

import {
    AvailablePlan,
} from '../api';

type AvailablePlanDisplayProps = {
    availablePlans: Array<AvailablePlan>;
}

const AvailablePlanDisplay = (props: AvailablePlanDisplayProps) => {
    return (
        <div class="w-full flex flex-col justify-center items-center">
            <div class="my-12 flex flex-col max-w-lg space-y-4">
                <Text type={TextType.Title}>
                    Let’s get you back on your way to practicing Mandarin
                </Text>
                <Text type={TextType.SectionHeader}>
                    To keep using Grammar Grove, you’re going to need a subscription. There are a couple of options below!
                </Text>
            </div>
            <div class="flex flex-col md:flex-row space-y-2 md:space-x-2">
            {
                props.availablePlans.map((p: AvailablePlan) => ( <PlanView plan={p} /> ))
            }
            </div>
        </div>
    );
}

type PlanViewProps = {
    plan: AvailablePlan;
}

const PlanView = (props: PlanViewProps) => {
    return (
        <Card>
            <div>
                <Text type={TextType.Subtitle}>
                    {`$${props.plan.price_cents_usd / 100} / ${props.plan.interval}`}
                </Text>
            </div>
        </Card>
    );
}

export default AvailablePlanDisplay;
