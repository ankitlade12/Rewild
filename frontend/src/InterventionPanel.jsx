import { useState, useEffect } from 'react'

const API = '/api'

const EFFORT_COLORS = {
    'Very Low': '#22c55e',
    'Low': '#4ade80',
    'Medium': '#fbbf24',
    'High': '#f97316',
}

export default function InterventionPanel({ profile, onBack, onRunSimulation }) {
    const [interventions, setInterventions] = useState([])
    const [selected, setSelected] = useState([])
    const [plants, setPlants] = useState([])
    const [pollinators, setPollinators] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const load = async () => {
            setLoading(true)
            setError(null)
            try {
                const [intRes, plantRes, pollRes] = await Promise.all([
                    fetch(`${API}/interventions`),
                    fetch(`${API}/plants/${encodeURIComponent(profile.locationData.ecoregion)}`),
                    fetch(`${API}/pollinators/${encodeURIComponent(profile.locationData.ecoregion)}`),
                ])

                if (!intRes.ok || !plantRes.ok || !pollRes.ok) {
                    throw new Error('Failed to load intervention data for this ecoregion')
                }

                const intData = await intRes.json()
                const plantData = await plantRes.json()
                const pollData = await pollRes.json()
                setInterventions(intData.interventions || [])
                setPlants(plantData.plants || [])
                setPollinators(pollData.pollinators || [])
            } catch (err) {
                console.error('Failed to load data:', err)
                setError(err?.message || 'Could not load data')
            }
            setLoading(false)
        }
        load()
    }, [profile])

    const toggleSelect = (id) => {
        setSelected(prev =>
            prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
        )
    }

    const selectedInterventions = interventions.filter(i => selected.includes(i.id))

    if (loading) {
        return (
            <div className="loading-screen animate-fade">
                <div className="loading-spinner" />
                <p>Loading ecological data for <strong>{profile.locationData.ecoregion}</strong>...</p>
            </div>
        )
    }

    if (error) {
        return (
            <div className="error-screen animate-fade">
                <h2>⚠️ Data Load Error</h2>
                <p>{error}</p>
                <button className="btn-primary" onClick={onBack}>← Back</button>
            </div>
        )
    }

    return (
        <div className="intervention-container animate-in">
            <div className="intervention-header">
                <button className="btn-secondary btn-sm" onClick={onBack}>← Back to Profile</button>
                <div className="header-info">
                    <h1>🌿 Choose Your Interventions</h1>
                    <div className="site-summary">
                        <span className="badge badge-green">Zone {profile.locationData.zone}</span>
                        <span className="badge badge-teal">{profile.locationData.ecoregion}</span>
                        <span className="badge badge-sky">{profile.area_sqft} sq ft</span>
                    </div>
                </div>
            </div>

            <div className="intervention-layout">
                <div className="intervention-list">
                    <h2>Available Interventions</h2>
                    <p className="section-desc">Select interventions to compare their ecological impact over time.</p>
                    <div className="intervention-cards">
                        {interventions.map((intv, idx) => (
                            <button
                                key={intv.id}
                                className={`intervention-card ${selected.includes(intv.id) ? 'selected' : ''}`}
                                onClick={() => toggleSelect(intv.id)}
                                style={{ animationDelay: `${idx * 60}ms` }}
                            >
                                <div className="intv-top">
                                    <span className="intv-icon">{intv.icon}</span>
                                    <div className="intv-effort" style={{ color: EFFORT_COLORS[intv.effort_level] }}>
                                        {intv.effort_level}
                                    </div>
                                </div>
                                <h3>{intv.name}</h3>
                                <p>{intv.description}</p>
                                <div className="intv-meta">
                                    <span>⏱️ {intv.typical_timeline_years} year{intv.typical_timeline_years > 1 ? 's' : ''}</span>
                                    <span className="intv-check">{selected.includes(intv.id) ? '✓ Selected' : '+ Add'}</span>
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="sidebar">
                    {selected.length > 0 && (
                        <div className="comparison-panel glass glow-border animate-in">
                            <h2>📊 Comparison</h2>
                            <p className="section-desc">{selected.length} intervention{selected.length > 1 ? 's' : ''} selected</p>
                            <div className="comparison-items">
                                {selectedInterventions.map(intv => (
                                    <div key={intv.id} className="comparison-item">
                                        <span className="intv-icon">{intv.icon}</span>
                                        <div>
                                            <strong>{intv.name}</strong>
                                            <span className="effort-tag" style={{ color: EFFORT_COLORS[intv.effort_level] }}>
                                                {intv.effort_level} effort
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <button className="btn-primary" style={{ width: '100%', marginTop: 16 }} onClick={() => onRunSimulation(selected)}>
                                Run Scenario Engine →
                            </button>
                        </div>
                    )}

                    <div className="eco-panel glass animate-in" style={{ animationDelay: '200ms' }}>
                        <h3>🌸 Native Plants ({plants.length})</h3>
                        <div className="eco-scroll">
                            {plants.slice(0, 8).map(p => (
                                <div key={p.common_name} className="eco-item">
                                    <div className="eco-item-header">
                                        <strong>{p.common_name}</strong>
                                        <span className={`value-tag ${p.ecological_value}`}>{p.ecological_value}</span>
                                    </div>
                                    <span className="eco-sci">{p.scientific_name}</span>
                                    <span className="eco-meta">{p.bloom_months.join(', ')}</span>
                                </div>
                            ))}
                            {plants.length > 8 && <p className="eco-more">+{plants.length - 8} more species</p>}
                        </div>
                    </div>

                    <div className="eco-panel glass animate-in" style={{ animationDelay: '350ms' }}>
                        <h3>🐝 Pollinators ({pollinators.length})</h3>
                        <div className="eco-scroll">
                            {pollinators.map(p => (
                                <div key={p.name} className="eco-item">
                                    <div className="eco-item-header">
                                        <strong>{p.name}</strong>
                                        <span className={`status-tag ${p.conservation_status}`}>{p.conservation_status}</span>
                                    </div>
                                    <span className="eco-meta">{p.type} · {p.flight_months.slice(0, 3).join(', ')}...</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
