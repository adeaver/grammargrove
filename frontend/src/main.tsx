import { render } from 'preact'
import IndexPage from './pages/IndexPage'
import './index.css'

const App = () => {
    return (
        <div>
            <IndexPage />
        </div>
    );
}

render(<App />, document.getElementById('app') as HTMLElement)
