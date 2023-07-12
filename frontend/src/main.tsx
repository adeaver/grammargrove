import './index.css'

import { render } from 'preact'

import IndexPage from './pages/IndexPage'
import DashboardPage from './pages/DashboardPage'
import QuizPage from './pages/QuizPage'
import SubscriptionPage from './pages/SubscriptionPage';
import OnboardingPage from './pages/OnboardingPage';
import PrivacyPolicyPage from './pages/PrivacyPolicyPage';
import PreferencesPage from './pages/PreferencesPage';

enum Routes {
    Index = '/',
    Dashboard = '/dashboard/',
    Quiz = '/quiz/',
    Subscription = '/subscription/',
    Onboarding = '/onboarding/',
    PrivacyPolicy = '/privacy-policy/',
    Preferences = '/preferences/'
}

const App = () => {
    switch (window.location.pathname) {
        case Routes.Index:
            return <IndexPage />
        case Routes.Dashboard:
            return <DashboardPage />
        case Routes.Quiz:
            return <QuizPage />
        case Routes.Subscription:
            return <SubscriptionPage />
        case Routes.Onboarding:
            return <OnboardingPage />
        case Routes.PrivacyPolicy:
            return <PrivacyPolicyPage />
        case Routes.Preferences:
            return <PreferencesPage />
        default:
            return <p>Not Found: { window.location.pathname }</p>
    }
}

render(<App />, document.getElementById('app') as HTMLElement)
