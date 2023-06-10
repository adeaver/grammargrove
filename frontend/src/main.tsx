import { render } from 'preact'
import IndexPage from './pages/IndexPage'
import './index.css'

render(<IndexPage />, document.getElementById('app') as HTMLElement)
