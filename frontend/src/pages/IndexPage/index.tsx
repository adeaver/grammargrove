import Header from '../../components/Header';
import Text, { TextType } from '../../components/Text';

import LoginComponent from './LoginComponent';

const IndexPage = () => {
    return (
        <div>
            <Header />
            <div class="w-full h-screen grid grid-cols-5">
                <div class="p-6 md:py-24 col-span-5 md:col-span-3 md:col-start-2 h-full flex flex-col items-center space-y-4">
                    <Text type={TextType.Title}>
                        Achieve your Mandarin goals
                    </Text>
                    <Text type={TextType.Subtitle}>
                        Better practice means better results faster.
                    </Text>
                    <Text>
                        GrammarGrove’s powerful flashcard system is designed specifically for Mandarin to help you practice better no matter how you’re learning Mandarin.
                    </Text>
                    <LoginComponent />
                </div>
            </div>
        </div>
    )
}

export default IndexPage;
