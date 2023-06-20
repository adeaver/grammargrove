import './index.css'

import { render } from 'preact'

import IndexPage from './pages/IndexPage'
import DashboardPage from './pages/DashboardPage'
import QuizPage from './pages/QuizPage'
import UserVocabularyPage from './pages/UserVocabularyPage';

enum Routes {
    Index = '/',
    Dashboard = '/dashboard/',
    Quiz = '/quiz/',
    UserVocabulary = '/user-vocabulary/'
}

const App = () => {
    switch (window.location.pathname) {
        case Routes.Index:
            return <IndexPage />
        case Routes.Dashboard:
            return <DashboardPage />
        case Routes.Quiz:
            return <QuizPage />
        case Routes.UserVocabulary:
            return <UserVocabularyPage />
        default:
            return <p>Not Found: { window.location.pathname }</p>
    }
}

render(<App />, document.getElementById('app') as HTMLElement)
