import { useState } from 'react'
import SiteProfileWizard from './SiteProfileWizard'
import InterventionPanel from './InterventionPanel'
import Dashboard from './Dashboard'
import ActionPlan from './ActionPlan'
import './App.css'

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

export default App
