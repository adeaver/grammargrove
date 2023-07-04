import { useState } from 'preact/hooks';

import Text, { TextFunction, TextType, TextAlignment } from '../../../components/Text';
import Input, { InputType } from '../../../components/Input';
import Button, { ButtonType } from '../../../components/Button';
import RadioButton from '../../../components/RadioButton';
import { getCSRFToken } from '../../../util/gfetch';

import {
    AvailablePlan,
} from '../api';

type AvailablePlanDisplayProps = {
    availablePlans: Array<AvailablePlan>;
}

const AvailablePlanDisplay = (props: AvailablePlanDisplayProps) => {
    const [ selectedPlan, setSelectedPlan ] = useState<string>(props.availablePlans[0].external_price_ref);

    return (
        <div class="p-6 w-full flex flex-col justify-center items-center">
            <div class="my-12 flex flex-col max-w-lg space-y-4">
                <Text type={TextType.Title}>
                    Let’s get you back on your way to practicing Mandarin
                </Text>
                <Text type={TextType.SectionHeader}>
                    To keep using Grammar Grove, you’re going to need a subscription. There are a couple of options below!
                </Text>
            </div>
            <div className="px-12 md:px-24 py-12 flex flex-col space-y-4 border border-primary-600 rounded-md">
                <Text type={TextType.Subtitle} alignment={TextAlignment.Left}>
                    Two plans that fit your needs
                </Text>
                {
                    props.availablePlans.map((a: AvailablePlan) => (
                        <div class="cursor-pointer flex flex-row items-center space-x-2" onClick={() => setSelectedPlan(a.external_price_ref)}>
                            <RadioButton isSelected={selectedPlan === a.external_price_ref} />
                            <div>
                                <Text alignment={TextAlignment.Left}>
                                    Billed {a.interval}ly (${a.price_cents_usd/100}/{a.interval})
                                </Text>
                                <Text type={TextType.FinePrint} function={TextFunction.Primary} alignment={TextAlignment.Left}>
                                    { a.interval === "year" ? "Best Deal" : "Most Flexible" }
                                </Text>
                            </div>
                        </div>
                    ))
                }
                <div>
                    <Text className="mt-8" type={TextType.SectionHeader} alignment={TextAlignment.Left}>
                        Both plans include:
                    </Text>
                    <ul class="list-disc">
                        <li class="py-2">
                            <Text type={TextType.FinePrint} alignment={TextAlignment.Left}>
                                Unlimited Quizzes
                            </Text>
                        </li>
                        <li class="py-2">
                            <Text type={TextType.FinePrint} alignment={TextAlignment.Left}>
                                Get quizzed on Mandarin-specific questions
                            </Text>
                        </li>
                        <li class="py-2">
                            <Text type={TextType.FinePrint} alignment={TextAlignment.Left}>
                                Study Unlimited Grammar Rules + Vocabulary Words
                            </Text>
                        </li>
                        <li class="py-2">
                            <Text type={TextType.FinePrint} alignment={TextAlignment.Left}>
                                Cancel at any time
                            </Text>
                        </li>
                    </ul>
                </div>
                <div class="w-full flex flex-col space-y-2">
                    <form method="POST" action="/api/billing/v1/checkout/">
                        <Input
                            type={InputType.Hidden}
                            value={getCSRFToken() || ""}
                            name="csrfmiddlewaretoken"
                            onChange={() => {}} />
                        <Input
                            type={InputType.Hidden}
                            value={selectedPlan}
                            name="price_id"
                            onChange={() => {}} />
                        <Button type={ButtonType.Primary} isSubmit>
                            Checkout
                        </Button>
                    </form>
                    <Button type={ButtonType.Secondary} onClick={() => {}}>
                        No, Thanks
                    </Button>
                </div>
            </div>
        </div>
    );
}

export default AvailablePlanDisplay;
