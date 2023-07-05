import Header from '../../components/Header';
import Text, { TextType } from '../../components/Text';
import Link, { LinkTarget } from '../../components/Link';

import LoginComponent from './LoginComponent';

const IndexPage = () => {
    return (
        <div>
            <Header />
            <IntroSection />
            <HowItWorksSection />
        </div>
    )
}

const IntroSection = () => {
    return (
        <div class="w-full h-screen grid grid-cols-5">
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
        <div id="how-it-works" class="w-full h-screen grid grid-cols-5">
            <div class="p-6 md:py-24 col-span-5 md:col-span-3 md:col-start-2 h-full flex flex-col items-center justify-center space-y-4">
                <Text type={TextType.Title}>
                    How it works
                </Text>
                <HowItWorksFlashcards />
                <HowItWorksGrammarRules />
                <HowItWorksQuizzes />
                <Text type={TextType.Subtitle}>
                    Sound exciting? Try it today.
                </Text>
                <LoginComponent />
            </div>
        </div>
    )
}

const HowItWorksFlashcards = () => {
    return (
        <div class="flex flex-col items-center space-y-2">
            <Text type={TextType.Subtitle}>
                GrammarGrove has flashcards specifically for Mandarin.
            </Text>
            <Text>
                Save time by searching for words and adding them directly to your vocabulary list. Unlike most flashcard apps, you won’t waste time filling out both sides of the cards that you want to study.
            </Text>
        </div>
    )
}

const HowItWorksGrammarRules = () => {
    return (
        <div class="flex flex-col items-center space-y-2">
            <Text type={TextType.Subtitle}>
                Don’t just study words. Study grammar rules.
            </Text>
            <Text>
                Search through Grammar rules to find the ones that you’re learning. Add them to your list and GrammarGrove will quiz you using examples of your grammar rules.
            </Text>
        </div>
    )
}

const HowItWorksQuizzes = () => {
    return (
        <div class="flex flex-col items-center space-y-2">
            <Text type={TextType.Subtitle}>
                Unlimited quizzes. Questions designed for learning Mandarin.
            </Text>
            <Text>
                Quiz yourself to test your knowledge as much as you’d like. The quizzes are designed to test Mandarin specifically. You’ll be quizzed on accents, hanzi, and definitions.
            </Text>
        </div>
    )
}

export default IndexPage;
