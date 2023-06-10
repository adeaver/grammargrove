import './index.css'

import { render } from 'preact'

import IndexPage from './pages/IndexPage'
import DashboardPage from './pages/DashboardPage'

enum Routes {
    Index = '/',
    Dashboard = '/dashboard/'
}

const App = () => {
    switch (window.location.pathname) {
        case Routes.Index:
            return <IndexPage />
        case Routes.Dashboard:
            return <DashboardPage />
        default:
            return <p>Not Found: { window.location.pathname }</p>
    }
}

render(<App />, document.getElementById('app') as HTMLElement)
