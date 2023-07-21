import './index.css'

import { render } from 'preact'

import IndexPage from './pages/IndexPage'
import DashboardPage from './pages/DashboardPage'
import QuizPage from './pages/QuizPage'
import SubscriptionPage from './pages/SubscriptionPage';
import OnboardingPage from './pages/OnboardingPage';
import PrivacyPolicyPage from './pages/PrivacyPolicyPage';
import PreferencesPage from './pages/PreferencesPage';
import UserVocabularyPage from './pages/UserVocabularyPage';
import UserGrammarRulesPage from './pages/UserGrammarRulesPage';

enum Routes {
    // Accessible by everyone
    Index = '/',
    PrivacyPolicy = '/privacy-policy/',

    // Requires Auth
    Subscription = '/subscription/',

    // Requires Auth and Valid Subscription
    Dashboard = '/dashboard/',
    Quiz = '/quiz/',
    Onboarding = '/onboarding/',
    UserVocabulary = '/vocabulary/',
    UserGrammar = '/grammar/',
    Preferences = '/preferences/'
}

const App = () => {
    switch (window.location.pathname) {
        case Routes.Index:
            return <IndexPage />
        case Routes.PrivacyPolicy:
            return <PrivacyPolicyPage />
        case Routes.Subscription:
            return <SubscriptionPage />
        case Routes.Dashboard:
            return <DashboardPage />
        case Routes.Quiz:
            return <QuizPage />
        case Routes.Onboarding:
            return <OnboardingPage />
        case Routes.Preferences:
            return <PreferencesPage />
        case Routes.UserVocabulary:
            return <UserVocabularyPage />
        case Routes.UserGrammar:
            return <UserGrammarRulesPage />
        default:
            return <p>Not Found: { window.location.pathname }</p>
    }
}

render(<App />, document.getElementById('app') as HTMLElement)
