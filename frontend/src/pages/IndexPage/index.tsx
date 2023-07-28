import { useEffect, useState } from 'preact/hooks';

import Header from '../../components/Header';
import Text, { TextType } from '../../components/Text';
import Link, { LinkTarget } from '../../components/Link';
import LoadingIcon from '../../components/LoadingIcon';

import { loadCaptchaScript } from '../../util/grecaptcha';

import LoginComponent from './LoginComponent';

import RadioButton from '../../components/RadioButton';

const IndexPage = () => {
    const [ hasLoadedCaptcha, setHasLoadedCaptcha ] = useState<boolean>(false);

    useEffect(() => {
        loadCaptchaScript();
        setHasLoadedCaptcha(true);
    }, []);

    let body = (
        <div class="w-full flex flex-row justify-center items-center">
            <LoadingIcon />
        </div>
    )
    if (hasLoadedCaptcha) {
        body = (
            <div>
                <IntroSection />
                <HowItWorksSection />
            </div>
        );
    }
    return (
        <div>
            <Header />
            { body }
        </div>
    )
}

const IntroSection = () => {
    return (
        <div class="w-full min-h-screen grid grid-cols-5">
            <div class="p-6 md:py-24 col-span-5 md:col-span-3 md:col-start-2 h-full flex flex-col items-center justify-center space-y-4">
                <Text type={TextType.Title}>
                    Achieve your Mandarin goals
                </Text>
                <Text type={TextType.Subtitle}>
                    Better practice means better results faster.
                </Text>
                <Text>
                    GrammarGrove’s powerful flashcard system is designed specifically for Mandarin to help you practice better no matter how you’re learning Mandarin.
                </Text>
                <div className="flex flex-col">
                    <Text>
                        Want to see how it works?
                    </Text>
                    <Link href="#how-it-works" target={LinkTarget.Self}>
                        Click here to learn more
                    </Link>
                </div>
                <LoginComponent />
                <Text type={TextType.FinePrint}>
                    Try it free for 14 days. No credit card required.
                </Text>
            </div>
        </div>
    )
}

const HowItWorksSection = () => {
    return (
        <div id="how-it-works" class="w-full min-h-screen grid grid-cols-5">
            <div class="p-6 md:py-24 col-span-5 md:col-span-3 md:col-start-2 h-full flex flex-col items-center justify-center space-y-8">
                <div class="flex flex-col space-y-4">
                    <Text type={TextType.Title}>
                        We set out to create the most powerful Mandarin flashcard system
                    </Text>
                    <Text>
                        We didn’t want a whole course like Duolingo or HelloChinese. We didn’t want just flashcards like Quizlet. We wanted something in between.
                    </Text>
                </div>
                <div class="flex flex-col space-y-4">
                    <Text type={TextType.Subtitle}>
                        Existing flashcard systems required a lot of user input.
                    </Text>
                    <div class="w-full flex flex-row space-x-2 items-center justify-center">
                        <RadioButton isSelected />
                        <Text>
                            Ours just works.
                        </Text>
                    </div>
                </div>
                <div class="flex flex-col space-y-4">
                    <Text type={TextType.Subtitle}>
                        Courses include grammar rules, but you have to go through the whole course to study the rules that you want
                    </Text>
                    <div class="w-full flex flex-row space-x-2 items-center justify-center">
                        <RadioButton isSelected />
                        <Text>
                            Customize your practice experience with GrammarGrove’s grammar rule flashcards.
                        </Text>
                    </div>
                    <Text>
                        You’ll get practice sentences that use the grammar rules that you’re studying
                    </Text>
                </div>
                <div class="flex flex-col space-y-4">
                    <Text type={TextType.Subtitle}>
                        Some flashcard systems try to limit you to one or two quizzes.
                    </Text>
                    <div class="w-full flex flex-row space-x-2 items-center justify-center">
                        <RadioButton isSelected />
                        <Text>
                            With GrammarGrove, you can practice as much as you’d like
                        </Text>
                    </div>
                </div>
                <Text type={TextType.Subtitle}>
                    Sound interesting? Give it a try.
                </Text>
                <LoginComponent />
            </div>
        </div>
    )
}

export default IndexPage;
