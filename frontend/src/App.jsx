import { useState } from 'react'
import SiteProfileWizard from './SiteProfileWizard'
import InterventionPanel from './InterventionPanel'
import './App.css'

function App() {
  const [screen, setScreen] = useState('wizard')
  const [profile, setProfile] = useState(null)

  const handleWizardComplete = (profileData) => {
    setProfile(profileData)
    setScreen('interventions')
  }

  return (
    <div className="app">
      <nav className="navbar glass">
        <div className="nav-brand" onClick={() => { setScreen('wizard'); setProfile(null) }}>
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
          <InterventionPanel profile={profile} onBack={() => setScreen('wizard')} />
        )}
      </main>
    </div>
  )
}

export default App
