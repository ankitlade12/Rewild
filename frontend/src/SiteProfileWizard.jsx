import { useState, useCallback } from 'react'

const API = '/api'

const CURRENT_STATES = [
    { id: 'maintained_lawn', label: 'Maintained Lawn', icon: '🏡', desc: 'Mowed regularly, mostly turf grass' },
    { id: 'weedy', label: 'Weedy / Neglected', icon: '🌿', desc: 'Overgrown with some wild plants' },
    { id: 'partial_garden', label: 'Partial Garden', icon: '🌻', desc: 'Some existing flower beds or plantings' },
    { id: 'bare_soil', label: 'Bare Soil', icon: '🟤', desc: 'Recently cleared or construction site' },
]

const SUN_OPTIONS = [
    { id: 'full', label: 'Full Sun', icon: '☀️', desc: '6+ hours direct sunlight' },
    { id: 'partial', label: 'Partial Sun', icon: '⛅', desc: '3-6 hours direct sunlight' },
    { id: 'shade', label: 'Mostly Shade', icon: '🌥️', desc: 'Less than 3 hours direct sunlight' },
]

const SOIL_OPTIONS = [
    { id: 'well_drained', label: 'Well-drained', icon: '🏖️' },
    { id: 'clay', label: 'Clay-heavy', icon: '🧱' },
    { id: 'sandy', label: 'Sandy', icon: '🏝️' },
    { id: 'unknown', label: "Don't know", icon: '❓' },
]

const GOALS = [
    { id: 'pollinators', label: 'Support Pollinators', icon: '🐝' },
    { id: 'birds', label: 'Attract Birds', icon: '🐦' },
    { id: 'water', label: 'Water Management', icon: '💧' },
    { id: 'carbon', label: 'Carbon Capture', icon: '🌍' },
    { id: 'education', label: 'Education / Learning', icon: '📚' },
    { id: 'beauty', label: 'Natural Beauty', icon: '🌸' },
]

export default function SiteProfileWizard({ onComplete }) {
    const [step, setStep] = useState(0)
    const [loading, setLoading] = useState(false)
    const [locationData, setLocationData] = useState(null)
    const [profile, setProfile] = useState({
        zip_code: '',
        area_sqft: '',
        current_state: '',
        sun_exposure: '',
        soil_type: '',
        goals: [],
    })

    const updateProfile = useCallback((key, value) => {
        setProfile(prev => ({ ...prev, [key]: value }))
    }, [])

    const toggleGoal = useCallback((goalId) => {
        setProfile(prev => ({
            ...prev,
            goals: prev.goals.includes(goalId)
                ? prev.goals.filter(g => g !== goalId)
                : [...prev.goals, goalId]
        }))
    }, [])

    const lookupZip = async () => {
        if (profile.zip_code.length !== 5) return
        setLoading(true)
        try {
            const res = await fetch(`${API}/lookup/${profile.zip_code}`)
            if (!res.ok) throw new Error('Invalid zip')
            const data = await res.json()
            setLocationData(data)
        } catch {
            setLocationData({ error: true })
        }
        setLoading(false)
    }

    const canAdvance = () => {
        if (step === 0) return locationData && !locationData.error && profile.area_sqft
        if (step === 1) return profile.current_state && profile.sun_exposure && profile.soil_type
        if (step === 2) return profile.goals.length > 0
        return false
    }

    const finish = () => {
        onComplete({ ...profile, area_sqft: parseInt(profile.area_sqft), locationData })
    }

    return (
        <div className="wizard-container animate-in">
            <div className="wizard-header">
                <h1>🌿 Tell us about your site</h1>
                <p>We'll use this to model ecological outcomes specific to your location.</p>
            </div>
            <div className="wizard-progress">
                {['Location', 'Conditions', 'Goals'].map((label, i) => (
                    <div key={label} className={`wizard-step ${i <= step ? 'active' : ''} ${i < step ? 'done' : ''}`}>
                        <div className="step-dot">{i < step ? '✓' : i + 1}</div>
                        <span>{label}</span>
                    </div>
                ))}
            </div>

            <div className="wizard-content animate-fade" key={step}>
                {step === 0 && (
                    <div className="step-content">
                        <h2>📍 Where is your site?</h2>
                        <div className="input-group">
                            <label>ZIP Code</label>
                            <div className="zip-input-row">
                                <input
                                    type="text" maxLength={5} placeholder="e.g. 75201"
                                    value={profile.zip_code}
                                    onChange={e => { updateProfile('zip_code', e.target.value.replace(/\D/g, '')); setLocationData(null) }}
                                />
                                <button className="btn-primary" onClick={lookupZip} disabled={profile.zip_code.length !== 5 || loading}>
                                    {loading ? '...' : 'Look Up'}
                                </button>
                            </div>
                            {locationData && !locationData.error && (
                                <div className="location-result glass glow-border animate-in">
                                    <div className="result-badges">
                                        <span className="badge badge-green">Zone {locationData.zone}</span>
                                        <span className="badge badge-teal">{locationData.state}</span>
                                        <span className="badge badge-sky">{locationData.ecoregion}</span>
                                    </div>
                                    <p className="result-desc">{locationData.ecoregion_description}</p>
                                    <div className="result-meta">
                                        <span>🌡️ Min: {locationData.min_temp_f_low}°F to {locationData.min_temp_f_high}°F</span>
                                        <span>❄️ Last frost: {locationData.last_frost}</span>
                                        <span>🍂 First frost: {locationData.first_frost}</span>
                                    </div>
                                </div>
                            )}
                            {locationData?.error && <p className="error-text">Couldn't find that zip code. Try another?</p>}
                        </div>
                        <div className="input-group">
                            <label>Approximate area (sq ft)</label>
                            <input
                                type="number" placeholder="e.g. 500" min={10} max={100000}
                                value={profile.area_sqft}
                                onChange={e => updateProfile('area_sqft', e.target.value)}
                            />
                            <span className="input-hint">
                                {profile.area_sqft > 0 && `≈ ${Math.round(profile.area_sqft / 43560 * 1000) / 1000} acres`}
                            </span>
                        </div>
                    </div>
                )}

                {step === 1 && (
                    <div className="step-content">
                        <h2>🌱 Current conditions</h2>
                        <div className="input-group">
                            <label>What's there now?</label>
                            <div className="option-grid">
                                {CURRENT_STATES.map(opt => (
                                    <button key={opt.id}
                                        className={`option-card ${profile.current_state === opt.id ? 'selected' : ''}`}
                                        onClick={() => updateProfile('current_state', opt.id)}>
                                        <span className="option-icon">{opt.icon}</span>
                                        <span className="option-label">{opt.label}</span>
                                        <span className="option-desc">{opt.desc}</span>
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="input-group">
                            <label>Sun exposure</label>
                            <div className="option-grid three-col">
                                {SUN_OPTIONS.map(opt => (
                                    <button key={opt.id}
                                        className={`option-card ${profile.sun_exposure === opt.id ? 'selected' : ''}`}
                                        onClick={() => updateProfile('sun_exposure', opt.id)}>
                                        <span className="option-icon">{opt.icon}</span>
                                        <span className="option-label">{opt.label}</span>
                                        <span className="option-desc">{opt.desc}</span>
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="input-group">
                            <label>Soil type</label>
                            <div className="option-grid four-col">
                                {SOIL_OPTIONS.map(opt => (
                                    <button key={opt.id}
                                        className={`option-card compact ${profile.soil_type === opt.id ? 'selected' : ''}`}
                                        onClick={() => updateProfile('soil_type', opt.id)}>
                                        <span className="option-icon">{opt.icon}</span>
                                        <span className="option-label">{opt.label}</span>
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="step-content">
                        <h2>🎯 What are your goals?</h2>
                        <p className="step-subtitle">Select all that apply — we'll prioritize interventions accordingly.</p>
                        <div className="option-grid three-col">
                            {GOALS.map(g => (
                                <button key={g.id}
                                    className={`option-card ${profile.goals.includes(g.id) ? 'selected' : ''}`}
                                    onClick={() => toggleGoal(g.id)}>
                                    <span className="option-icon">{g.icon}</span>
                                    <span className="option-label">{g.label}</span>
                                </button>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            <div className="wizard-footer">
                {step > 0 && <button className="btn-secondary" onClick={() => setStep(s => s - 1)}>← Back</button>}
                <div style={{ flex: 1 }} />
                {step < 2 ? (
                    <button className="btn-primary" disabled={!canAdvance()} onClick={() => setStep(s => s + 1)}>
                        Continue →
                    </button>
                ) : (
                    <button className="btn-primary" disabled={!canAdvance()} onClick={finish}>
                        See Interventions →
                    </button>
                )}
            </div>
        </div>
    )
}
