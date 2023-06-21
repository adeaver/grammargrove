import './index.css'

import { render } from 'preact'

import IndexPage from './pages/IndexPage'
import DashboardPage from './pages/DashboardPage'
import QuizPage from './pages/QuizPage'

enum Routes {
    Index = '/',
    Dashboard = '/dashboard/',
    Quiz = '/quiz/',
}

const App = () => {
    switch (window.location.pathname) {
        case Routes.Index:
            return <IndexPage />
        case Routes.Dashboard:
            return <DashboardPage />
        case Routes.Quiz:
            return <QuizPage />
        default:
            return <p>Not Found: { window.location.pathname }</p>
    }
}

render(<App />, document.getElementById('app') as HTMLElement)
