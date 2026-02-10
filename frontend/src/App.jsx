import { useState, Component } from 'react'
import SiteProfileWizard from './SiteProfileWizard'
import InterventionPanel from './InterventionPanel'
import Dashboard from './Dashboard'
import ActionPlan from './ActionPlan'
import './App.css'

// Error boundary to catch and display runtime errors
class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }
  componentDidCatch(error, info) {
    console.error('React Error:', error, info)
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 40, color: '#ff6b6b', background: '#1a1a2e', minHeight: '100vh', fontFamily: 'monospace' }}>
          <h1>⚠️ Rendering Error</h1>
          <pre style={{ whiteSpace: 'pre-wrap', color: '#ffd93d' }}>{this.state.error?.message}</pre>
          <pre style={{ whiteSpace: 'pre-wrap', color: '#aaa', fontSize: 12 }}>{this.state.error?.stack}</pre>
          <button onClick={() => window.location.reload()} style={{ marginTop: 20, padding: '10px 20px', background: '#22c55e', color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer' }}>
            Reload
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

function App() {
  const [screen, setScreen] = useState('wizard')
  const [profile, setProfile] = useState(null)
  const [actionIntervention, setActionIntervention] = useState(null)

  const handleWizardComplete = (profileData) => {
    setProfile(profileData)
    setScreen('interventions')
  }

  const handleRunSimulation = (selectedInterventions) => {
    setProfile(prev => ({ ...prev, selectedInterventions }))
    setScreen('dashboard')
  }

  const handleGetActionPlan = (intervention) => {
    setActionIntervention(intervention)
    setScreen('actionplan')
  }

  const handleBack = (target) => {
    if (target === 'wizard') {
      setScreen('wizard')
      setProfile(null)
    } else if (target === 'interventions') {
      setScreen('interventions')
    } else if (target === 'dashboard') {
      setScreen('dashboard')
    }
  }

  return (
    <div className="app">
      <nav className="navbar glass">
        <div className="nav-brand" onClick={() => handleBack('wizard')}>
          <span className="brand-icon">🌿</span>
          <span className="brand-text">REWILD</span>
        </div>
        <span className="nav-tagline">Ecological Scenario Engine</span>
      </nav>
      <main className="main-content">
        {screen === 'wizard' && (
          <SiteProfileWizard onComplete={handleWizardComplete} />
        )}
        {screen === 'interventions' && profile && (
          <InterventionPanel
            profile={profile}
            onBack={() => handleBack('wizard')}
            onRunSimulation={handleRunSimulation}
          />
        )}
        {screen === 'dashboard' && profile && (
          <Dashboard
            profile={profile}
            onBack={() => handleBack('interventions')}
            onGetActionPlan={handleGetActionPlan}
          />
        )}
        {screen === 'actionplan' && profile && actionIntervention && (
          <ActionPlan
            profile={profile}
            intervention={actionIntervention}
            onBack={() => handleBack('dashboard')}
          />
        )}
      </main>
    </div>
  )
}

export default function AppWithErrorBoundary() {
  return (
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  )
}
