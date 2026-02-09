export default function ConfidencePanel({ scenarios }) {
    if (!scenarios?.length) return null

    const scenario = scenarios[0]
    const reducers = scenario.uncertainty_reducers || []
    const narrative = scenario.narrative || {}

    return (
        <div className="confidence-panel glass animate-in">
            <h3>📊 Confidence Analysis</h3>

            {/* Narrative */}
            <div className="narrative-section">
                <p className="narrative-text">{narrative.narrative}</p>
                {narrative.season_tip && (
                    <p className="season-tip">💡 {narrative.season_tip}</p>
                )}
                {narrative.uncertainty_note && (
                    <p className="uncertainty-note">⚠️ {narrative.uncertainty_note}</p>
                )}
                {narrative.source === 'openai' && (
                    <span className="ai-badge">✨ AI-enhanced narrative</span>
                )}
            </div>

            {/* Species recommendations */}
            {narrative.species_recommendations?.length > 0 && (
                <div className="species-recs">
                    <h4>🌱 Recommended Species</h4>
                    {narrative.species_recommendations.map((sp, i) => (
                        <div key={i} className="rec-item">
                            <strong>{sp.name}</strong>
                            <span>{sp.reason}</span>
                        </div>
                    ))}
                </div>
            )}

            {/* Uncertainty reducers */}
            {reducers.length > 0 && (
                <div className="reducers-section">
                    <h4>🎯 Narrow Your Uncertainty</h4>
                    <p className="reducer-desc">These actions would tighten prediction bands:</p>
                    {reducers.map((r, i) => (
                        <div key={i} className="reducer-card">
                            <span className="reducer-icon">{r.icon}</span>
                            <div>
                                <strong>{r.action}</strong>
                                <span className="reducer-impact">{r.impact}</span>
                                <span className="reducer-effort">{r.effort} effort</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
