import React from 'react'
import ReactDOM from 'react-dom/client'
import { Toaster } from 'react-hot-toast'
import { BlinkProvider, BlinkAuthProvider } from '@blinkdotnew/react'
import App from './App'
import './index.css'

const projectId = import.meta.env.VITE_BLINK_PROJECT_ID || 'ai-interview-coach-kwauxn5v'
const publishableKey = import.meta.env.VITE_BLINK_PUBLISHABLE_KEY

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BlinkProvider projectId={projectId} publishableKey={publishableKey}>
      <BlinkAuthProvider>
        <Toaster position="top-right" />
        <App />
      </BlinkAuthProvider>
    </BlinkProvider>
  </React.StrictMode>,
)