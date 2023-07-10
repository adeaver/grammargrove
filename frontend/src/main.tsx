import './index.css'

import { render } from 'preact'

import IndexPage from './pages/IndexPage'
import DashboardPage from './pages/DashboardPage'
import QuizPage from './pages/QuizPage'
import SubscriptionPage from './pages/SubscriptionPage';
import OnboardingPage from './pages/OnboardingPage';

enum Routes {
    Index = '/',
    Dashboard = '/dashboard/',
    Quiz = '/quiz/',
    Subscription = '/subscription/',
    Onboarding = '/onboarding/',
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
        default:
            return <p>Not Found: { window.location.pathname }</p>
    }
}

render(<App />, document.getElementById('app') as HTMLElement)
