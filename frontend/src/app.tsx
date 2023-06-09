import { useState } from 'preact/hooks'
import './app.css'

export function App() {
  const [count, setCount] = useState<number>(0)

  return (
    <div>
      <div>
        <a href="https://vitejs.dev" target="_blank">
        </a>
      </div>
      <h1 className="text-6xl">Vite + Preact = +2</h1>
      <div className="card">
        <button onClick={() => setCount((count: number) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/app.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and Preact logos to learn more
      </p>
    </div>
  )
}
