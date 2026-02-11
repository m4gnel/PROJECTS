import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useBlinkAuth } from '@blinkdotnew/react'
import { Navbar } from './components/layout/Navbar'
import { LandingPage } from './pages/LandingPage'
import { Dashboard } from './pages/Dashboard'
import { InterviewSession } from './pages/InterviewSession'
import { FeedbackView } from './pages/FeedbackView'
import { Spinner } from './components/ui/spinner'
import { Toaster } from 'react-hot-toast'

function App() {
  const { isAuthenticated, isLoading } = useBlinkAuth()

  if (isLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-background">
        <Spinner className="h-10 w-10 text-primary" />
      </div>
    )
  }

  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Toaster position="top-center" reverseOrder={false} />
        {!window.location.pathname.startsWith('/interview/') && !window.location.pathname.startsWith('/feedback/') && <Navbar />}
        <main>
          <Routes>
            <Route path="/" element={!isAuthenticated ? <LandingPage /> : <Navigate to="/dashboard" />} />
            <Route 
              path="/dashboard" 
              element={isAuthenticated ? <Dashboard /> : <Navigate to="/" />} 
            />
            <Route 
              path="/interview/:id" 
              element={isAuthenticated ? <InterviewSession /> : <Navigate to="/" />} 
            />
            <Route 
              path="/feedback/:id" 
              element={isAuthenticated ? <FeedbackView /> : <Navigate to="/" />} 
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

