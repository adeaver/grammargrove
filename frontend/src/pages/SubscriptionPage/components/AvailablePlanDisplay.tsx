import { useState } from 'preact/hooks';

import Text, { TextFunction, TextType, TextAlignment } from '../../../components/Text';
import Input, { InputType } from '../../../components/Input';
import Button, { ButtonType } from '../../../components/Button';
import RadioButton from '../../../components/RadioButton';
import FeedbackForm from '../../../components/FeedbackForm';
import { FeedbackType } from '../../../components/FeedbackForm/api';
import { getCSRFToken } from '../../../util/gfetch';
import { setLocation } from '../../../util/window';

import {
    AvailablePlan,
} from '../api';

type AvailablePlanDisplayProps = {
    availablePlans: Array<AvailablePlan>;
}

const AvailablePlanDisplay = (props: AvailablePlanDisplayProps) => {
    const [ selectedPlan, setSelectedPlan ] = useState<string>(props.availablePlans[0].external_price_ref);
    const [ showFeedbackForm, setShowFeedbackForm ] = useState<boolean>(false);

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
                {
                    !showFeedbackForm ? (
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
                            <Button type={ButtonType.Secondary} onClick={() => setShowFeedbackForm(true)}>
                                No, Thanks
                            </Button>
                        </div>
                    ) : (
                        <NoSubscribeFeedbackForm goBack={() => setShowFeedbackForm(false)} />
                    )
                }
            </div>
            <div>
                <div class="max-w-lg my-12 flex flex-col space-y-4">
                    <Text type={TextType.Subtitle}>
                        Why is there no free plan?
                    </Text>
                    <Text>
                        Hello! I’m Andrew, the developer who built (and is still building) GrammarGrove by myself. Software requires money to maintain and run, so every website and app needs to find a way to get money from its users. My thought is that if my users are my customers, then my incentive is to make GrammarGrove better so more people sign up and stay signed up.
                    </Text>
                    <Text>
                        Other websites and apps use ads, which works well if you have a lot of users. But I felt this would change my incentive from building the best product for my users to building the best product for advertisers. I think we all know of some websites that ended up having to do that.
                    </Text>
                    <Text>
                        Another route is getting funding from venture capitalists. A lot of websites do this, but I believe it also changes the incentive from being about the users to being about the investors.
                    </Text>
                    <Text>
                        In short, if you pay me, I work for you! I think this is the best setup.
                    </Text>
                </div>
            </div>
        </div>
    );
}

type NoSubscribeFeedbackFormProps = {
    goBack: () => void;
}

const NoSubscribeFeedbackForm = (props: NoSubscribeFeedbackFormProps) => {
    const onSuccess = () => {
        setLocation("/api/billing/v1/deny/")
    }

    return (
        <div class="max-w-lg flex flex-col space-y-4">
            <FeedbackForm
                type={FeedbackType.NoSubscribe}
                onSuccess={onSuccess} />
            <Button type={ButtonType.Secondary} onClick={props.goBack}>
                Go Back
            </Button>
        </div>
    );
}

export default AvailablePlanDisplay;
