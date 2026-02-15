import { Fragment } from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Line } from 'recharts'

const METRIC_CONFIG = {
    pollinator_diversity_index: { label: 'Pollinator Diversity', color: '#fbbf24', icon: '🐝' },
    bird_activity_score: { label: 'Bird Activity', color: '#38bdf8', icon: '🐦' },
    food_web_complexity: { label: 'Food Web Complexity', color: '#22c55e', icon: '🕸️' },
    ecosystem_services_score: { label: 'Ecosystem Services', color: '#a78bfa', icon: '🌍' },
}

function CustomTooltip({ active, payload, label, scenarios }) {
    if (!active || !payload?.length || !scenarios?.length) return null

    const row = payload[0]?.payload || {}
    const points = scenarios.map((s, idx) => {
        const suffix = scenarios.length > 1 ? `_${idx}` : ''
        const likely = row[`likely${suffix}`]
        const conservative = row[`conservative${suffix}`]
        const optimistic = row[`optimistic${suffix}`]
        if (likely == null || conservative == null || optimistic == null) return null
        return {
            key: s.intervention,
            name: s.intervention.replace(/_/g, ' '),
            color: ['#22c55e', '#38bdf8', '#fbbf24', '#a78bfa'][idx],
            likely,
            conservative,
            optimistic,
        }
    }).filter(Boolean)

    if (!points.length) return null

    return (
        <div className="chart-tooltip glass">
            <strong>Year {label}</strong>
            {points.map(point => (
                <div key={point.key} style={{ color: point.color, fontSize: '0.85rem' }}>
                    {point.name}: {(point.likely * 100).toFixed(0)}%
                    {' '}({(point.conservative * 100).toFixed(0)}%-{(point.optimistic * 100).toFixed(0)}%)
                </div>
            ))}
        </div>
    )
}

export default function TrajectoryChart({ scenarios, activeMetric }) {
    if (!scenarios?.length) return null

    const metric = activeMetric || 'pollinator_diversity_index'
    const config = METRIC_CONFIG[metric]

    // Build chart data: one entry per year with each scenario's bands
    const chartData = Array.from({ length: 6 }, (_, year) => {
        const row = { year }
        scenarios.forEach((s, idx) => {
            const yData = s.timeline[year]?.[metric]
            if (yData) {
                const suffix = scenarios.length > 1 ? `_${idx}` : ''
                row[`optimistic${suffix}`] = yData.optimistic
                row[`likely${suffix}`] = yData.likely
                row[`conservative${suffix}`] = yData.conservative
                row[`uncertainty${suffix}`] = Math.max(0, yData.optimistic - yData.conservative)
            }
        })
        return row
    })

    const COLORS = ['#22c55e', '#38bdf8', '#fbbf24', '#a78bfa']

    return (
        <div className="trajectory-chart animate-in">
            <div className="chart-header">
                <h3>{config.icon} {config.label}</h3>
                <span className="chart-unit">0–100% of regional potential</span>
            </div>
            <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                    <defs>
                        {scenarios.map((s, idx) => (
                            <linearGradient key={idx} id={`grad_${idx}`} x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor={COLORS[idx]} stopOpacity={0.3} />
                                <stop offset="100%" stopColor={COLORS[idx]} stopOpacity={0.03} />
                            </linearGradient>
                        ))}
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis
                        dataKey="year" stroke="#64748b" fontSize={12}
                        tickFormatter={v => `Y${v}`}
                    />
                    <YAxis stroke="#64748b" fontSize={12} domain={[0, 1]} tickFormatter={v => `${(v * 100).toFixed(0)}%`} />
                    <Tooltip content={<CustomTooltip scenarios={scenarios} />} />
                    {scenarios.length > 1 && <Legend />}
                    {scenarios.map((s, idx) => {
                        const suffix = scenarios.length > 1 ? `_${idx}` : ''
                        const name = s.intervention.replace(/_/g, ' ')
                        return (
                            <Fragment key={idx}>
                                <Area
                                    key={`baseline_${idx}`}
                                    type="monotone"
                                    dataKey={`conservative${suffix}`}
                                    stackId={`band_${idx}`}
                                    stroke="none"
                                    fill="transparent"
                                    legendType="none"
                                    isAnimationActive={false}
                                />
                                <Area
                                    key={`band_${idx}`}
                                    type="monotone"
                                    dataKey={`uncertainty${suffix}`}
                                    stackId={`band_${idx}`}
                                    stroke="none"
                                    fill={COLORS[idx]}
                                    fillOpacity={0.14}
                                    name={`${name} range`}
                                />
                                <Line
                                    key={`likely_${idx}`}
                                    type="monotone"
                                    dataKey={`likely${suffix}`}
                                    stroke={COLORS[idx]}
                                    strokeWidth={2.5}
                                    name={`${name} likely`}
                                    dot={{ r: 3, fill: COLORS[idx] }}
                                    activeDot={{ r: 5, stroke: COLORS[idx], strokeWidth: 2, fill: '#0a0f1a' }}
                                />
                            </Fragment>
                        )
                    })}
                </AreaChart>
            </ResponsiveContainer>
            {/* Confidence bands legend */}
            {scenarios.length === 1 && scenarios[0].timeline[3]?.[metric] && (
                <div className="confidence-footer">
                    <span className="conf-label">
                        Y3 confidence: {scenarios[0].timeline[3][metric].confidence}%
                    </span>
                    <span className="conf-range">
                        Range: {(scenarios[0].timeline[3][metric].conservative * 100).toFixed(0)}%
                        – {(scenarios[0].timeline[3][metric].optimistic * 100).toFixed(0)}%
                    </span>
                </div>
            )}
            {scenarios.length > 1 && (
                <div className="confidence-footer">
                    <span className="conf-label">Shaded areas show uncertainty bands</span>
                    <span className="conf-range">Tooltip shows likely value and conservative-optimistic range</span>
                </div>
            )}
        </div>
    )
}

export { METRIC_CONFIG }
