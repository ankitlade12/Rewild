import { useState, useEffect } from 'react'
import TrajectoryChart, { METRIC_CONFIG } from './TrajectoryChart'
import FoodWebGraph from './FoodWebGraph'
import ConfidencePanel from './ConfidencePanel'

const API = '/api'

export default function Dashboard({ profile, onBack, onGetActionPlan }) {
    const [scenarios, setScenarios] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [activeMetric, setActiveMetric] = useState('pollinator_diversity_index')
    const [activeScenarioIdx, setActiveScenarioIdx] = useState(0)
    const [viewMode, setViewMode] = useState('overlay') // overlay | side-by-side

    useEffect(() => {
        const runSimulation = async () => {
            try {
                const res = await fetch(`${API}/simulate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        site_profile: {
                            zip_code: profile.zip_code,
                            area_sqft: profile.area_sqft,
                            current_state: profile.current_state,
                            sun_exposure: profile.sun_exposure,
                            soil_type: profile.soil_type,
                            goals: profile.goals,
                        },
                        interventions: profile.selectedInterventions,
                    }),
                })
                if (!res.ok) {
                    const body = await res.json().catch(() => ({}))
                    throw new Error(body.detail || 'Simulation failed')
                }
                const data = await res.json()
                setScenarios(data.scenarios)
            } catch (err) {
                setError(err?.message || 'Simulation failed')
            }
            setLoading(false)
        }
        runSimulation()
    }, [profile])

    if (loading) {
        return (
            <div className="loading-screen animate-fade">
                <div className="loading-spinner" />
                <h2>Running Ecological Simulation</h2>
                <p>Modeling 5-year trajectories for {profile.selectedInterventions?.length || 0} intervention{profile.selectedInterventions?.length > 1 ? 's' : ''}...</p>
                <div className="loading-steps">
                    <span className="loading-step active">🌱 Succession model</span>
                    <span className="loading-step">🕸️ Food web analysis</span>
                    <span className="loading-step">📊 Uncertainty bands</span>
                    <span className="loading-step">✨ AI narrative</span>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="error-screen animate-fade">
                <h2>⚠️ Simulation Error</h2>
                <p>{error}</p>
                <button className="btn-primary" onClick={onBack}>← Back</button>
            </div>
        )
    }

    if (!scenarios?.length) {
        return (
            <div className="error-screen animate-fade">
                <h2>⚠️ No Scenarios Returned</h2>
                <p>Try selecting at least one intervention and rerun the simulation.</p>
                <button className="btn-primary" onClick={onBack}>← Back</button>
            </div>
        )
    }
    const activeScenario = scenarios[activeScenarioIdx]

    return (
        <div className="dashboard animate-in">
            <div className="dashboard-header">
                <button className="btn-secondary btn-sm" onClick={onBack}>← Back</button>
                <div className="header-info">
                    <h1>🌿 Ecological Trajectory Dashboard</h1>
                    <div className="site-summary">
                        <span className="badge badge-green">Zone {profile.locationData?.zone}</span>
                        <span className="badge badge-teal">{profile.locationData?.ecoregion}</span>
                        <span className="badge badge-sky">{profile.area_sqft} sq ft</span>
                        <span className="badge badge-amber">{scenarios.length} scenario{scenarios.length > 1 ? 's' : ''}</span>
                    </div>
                </div>
            </div>

            {/* Scenario tabs */}
            {scenarios.length > 1 && (
                <div className="scenario-tabs">
                    <div className="tab-group">
                        {scenarios.map((s, i) => (
                            <button
                                key={i}
                                className={`scenario-tab ${activeScenarioIdx === i ? 'active' : ''}`}
                                onClick={() => setActiveScenarioIdx(i)}
                            >
                                {s.intervention.replace(/_/g, ' ')}
                            </button>
                        ))}
                    </div>
                    <div className="view-toggle">
                        <button
                            className={`toggle-btn ${viewMode === 'overlay' ? 'active' : ''}`}
                            onClick={() => setViewMode('overlay')}
                        >Overlay</button>
                        <button
                            className={`toggle-btn ${viewMode === 'side-by-side' ? 'active' : ''}`}
                            onClick={() => setViewMode('side-by-side')}
                        >Side by Side</button>
                    </div>
                </div>
            )}

            {/* Metric selector */}
            <div className="metric-tabs">
                {Object.entries(METRIC_CONFIG).map(([key, cfg]) => (
                    <button
                        key={key}
                        className={`metric-tab ${activeMetric === key ? 'active' : ''}`}
                        onClick={() => setActiveMetric(key)}
                    >
                        {cfg.icon} {cfg.label}
                    </button>
                ))}
            </div>

            <div className="dashboard-grid">
                {/* Charts area */}
                <div className="charts-area">
                    {viewMode === 'overlay' ? (
                        <TrajectoryChart scenarios={scenarios} activeMetric={activeMetric} />
                    ) : (
                        <div className="side-by-side-grid">
                            {scenarios.map((s, i) => (
                                <div key={i} className="sbs-chart">
                                    <h3 className="sbs-title">{s.intervention.replace(/_/g, ' ')}</h3>
                                    <TrajectoryChart scenarios={[s]} activeMetric={activeMetric} />
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Food Web */}
                    <FoodWebGraph
                        foodWeb={activeScenario.food_web}
                        year={0}
                    />
                </div>

                {/* Sidebar */}
                <div className="dashboard-sidebar">
                    <ConfidencePanel scenarios={[activeScenario]} />

                    {/* Bloom Calendar Summary */}
                    {activeScenario.bloom_calendar && (
                        <div className="bloom-panel glass animate-in" style={{ animationDelay: '200ms' }}>
                            <h3>🌸 Bloom Calendar</h3>
                            <div className="bloom-grid">
                                {Object.entries(activeScenario.bloom_calendar.calendar).map(([month, plants]) => (
                                    <div key={month} className={`bloom-month ${plants.length > 0 ? 'has-bloom' : ''}`}>
                                        <span className="month-label">{month.slice(0, 3)}</span>
                                        <div className="bloom-bar" style={{ height: `${Math.min(plants.length * 12, 60)}px` }} />
                                        <span className="bloom-count">{plants.length || ''}</span>
                                    </div>
                                ))}
                            </div>
                            {activeScenario.bloom_calendar.no_matching_species ? (
                                <p className="bloom-gap">
                                    ℹ️ No species matched your current sun/soil filters for this ecoregion.
                                </p>
                            ) : activeScenario.bloom_calendar.bloom_gap_months?.length > 0 && (
                                <p className="bloom-gap">
                                    ⚠️ Bloom gap: {activeScenario.bloom_calendar.bloom_gap_months.join(', ')}
                                </p>
                            )}
                        </div>
                    )}

                    {/* Action Plan CTA */}
                    <div className="action-cta glass glow-border animate-in" style={{ animationDelay: '300ms' }}>
                        <div className="cta-content">
                            <h3>📋 Ready to Start?</h3>
                            <p>Get a personalized planting calendar, shopping list, and step-by-step guide.</p>
                        </div>
                        <button
                            className="btn-primary btn-lg"
                            onClick={() => onGetActionPlan && onGetActionPlan(activeScenario.intervention)}
                        >
                            Get Your Action Plan →
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
