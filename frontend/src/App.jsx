import { useState } from 'react'
import SiteProfileWizard from './SiteProfileWizard'
import InterventionPanel from './InterventionPanel'
import Dashboard from './Dashboard'
import './App.css'

function App() {
  const [screen, setScreen] = useState('wizard')
  const [profile, setProfile] = useState(null)

  const handleWizardComplete = (profileData) => {
    setProfile(profileData)
    setScreen('interventions')
  }

  const handleRunSimulation = (selectedInterventions) => {
    setProfile(prev => ({ ...prev, selectedInterventions }))
    setScreen('dashboard')
  }

  const handleBack = (target) => {
    if (target === 'wizard') {
      setScreen('wizard')
      setProfile(null)
    } else if (target === 'interventions') {
      setScreen('interventions')
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
          />
        )}
      </main>
    </div>
  )
}

export default App
