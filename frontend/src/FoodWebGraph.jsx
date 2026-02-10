import { useRef, useEffect, useState } from 'react'
import * as d3 from 'd3'

export default function FoodWebGraph({ foodWeb, year: initialYear }) {
    const svgRef = useRef(null)
    const [year, setYear] = useState(initialYear || 0)
    const [isPlaying, setIsPlaying] = useState(false)
    const timerRef = useRef(null)

    // Auto-play animation
    useEffect(() => {
        if (isPlaying) {
            timerRef.current = setInterval(() => {
                setYear(y => {
                    if (y >= 5) { setIsPlaying(false); return 5 }
                    return y + 1
                })
            }, 1500)
        }
        return () => clearInterval(timerRef.current)
    }, [isPlaying])

    useEffect(() => {
        if (!foodWeb || !svgRef.current) return
        const data = foodWeb[year]
        if (!data) return

        const svg = d3.select(svgRef.current)
        const width = svgRef.current.clientWidth || 600
        const height = 420

        svg.selectAll('*').remove()
        svg.attr('viewBox', `0 0 ${width} ${height}`)

        if (data.nodes.length === 0) {
            svg.append('text')
                .attr('x', width / 2).attr('y', height / 2)
                .attr('text-anchor', 'middle')
                .attr('fill', '#64748b')
                .attr('font-size', '14px')
                .text('Year 0: Starting point — no established food web yet')
            return
        }

        const TYPE_COLORS = {
            plant: '#22c55e',
            bee: '#fbbf24',
            butterfly: '#fb7185',
            moth: '#c084fc',
            hummingbird: '#f43f5e',
            fly: '#94a3b8',
            wasp: '#f97316',
            beetle: '#a78bfa',
            bird: '#38bdf8',
        }

        // Trophic layers spread vertically
        const GROUP_Y = {
            producer: height * 0.8,
            consumer: height * 0.45,
            top_consumer: height * 0.15,
        }

        // Deep-clone nodes and edges so D3 doesn't mutate React state
        const nodes = data.nodes.map(n => ({ ...n }))
        const edges = data.edges.map(e => ({ ...e }))

        // Create force simulation with strong repulsion
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(edges).id(d => d.id).distance(100).strength(0.15))
            .force('charge', d3.forceManyBody().strength(-200))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('y', d3.forceY(d => GROUP_Y[d.group] || height / 2).strength(0.4))
            .force('x', d3.forceX(width / 2).strength(0.05))
            .force('collision', d3.forceCollide().radius(d => (d.size || 6) + 12))

        // Run simulation synchronously for stability
        simulation.alpha(1).alphaDecay(0.02)
        for (let i = 0; i < 200; i++) simulation.tick()
        simulation.stop()

        // Clamp positions
        nodes.forEach(d => {
            d.x = Math.max(40, Math.min(width - 40, d.x))
            d.y = Math.max(20, Math.min(height - 20, d.y))
        })

        // Draw links with gradient
        svg.append('g')
            .selectAll('line')
            .data(edges)
            .enter().append('line')
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y)
            .attr('stroke', d => d.type === 'pollination' ? 'rgba(34,197,94,0.2)' : 'rgba(56,189,248,0.15)')
            .attr('stroke-width', 1)
            .attr('opacity', 0)
            .transition().duration(400)
            .attr('opacity', 1)

        // Draw nodes
        svg.append('g')
            .selectAll('circle')
            .data(nodes)
            .enter().append('circle')
            .attr('cx', d => d.x)
            .attr('cy', d => d.y)
            .attr('r', 0)
            .attr('fill', d => TYPE_COLORS[d.type] || '#64748b')
            .attr('stroke', d => d.conservation === 'declining' || d.conservation === 'vulnerable'
                ? '#f43f5e' : 'rgba(255,255,255,0.15)')
            .attr('stroke-width', d => d.conservation === 'declining' ? 2.5 : 1)
            .attr('filter', 'drop-shadow(0 0 3px rgba(0,0,0,0.3))')
            .transition().duration(500).delay((d, i) => i * 20)
            .attr('r', d => d.size || 5)

        // Labels: only show for top ~10 biggest nodes to avoid clutter
        const sortedNodes = [...nodes].sort((a, b) => (b.size || 5) - (a.size || 5))
        const labelNodes = sortedNodes.slice(0, Math.min(10, nodes.length))

        svg.append('g')
            .selectAll('text')
            .data(labelNodes)
            .enter().append('text')
            .text(d => {
                const name = d.label || d.id
                return name.length > 12 ? name.slice(0, 11) + '…' : name
            })
            .attr('x', d => d.x)
            .attr('y', d => d.y - (d.size || 5) - 6)
            .attr('font-size', '8px')
            .attr('fill', '#8b9dc3')
            .attr('text-anchor', 'middle')
            .attr('pointer-events', 'none')
            .attr('opacity', 0)
            .transition().duration(400).delay(400)
            .attr('opacity', 0.8)

    }, [foodWeb, year])

    if (!foodWeb) return null
    const stats = foodWeb[year]?.stats || {}

    return (
        <div className="food-web-container animate-in">
            <div className="food-web-header">
                <h3>🕸️ Food Web Network</h3>
                <div className="food-web-controls">
                    <button
                        className={`play-btn ${isPlaying ? 'playing' : ''}`}
                        onClick={() => { setIsPlaying(!isPlaying); if (year >= 5) setYear(0) }}
                    >
                        {isPlaying ? '⏸' : '▶'} {isPlaying ? 'Pause' : 'Play 5-Year Animation'}
                    </button>
                </div>
            </div>
            <div className="year-slider">
                {[0, 1, 2, 3, 4, 5].map(y => (
                    <button
                        key={y}
                        className={`year-btn ${y === year ? 'active' : ''}`}
                        onClick={() => { setYear(y); setIsPlaying(false) }}
                    >
                        Y{y}
                    </button>
                ))}
            </div>
            <svg ref={svgRef} className="food-web-svg" />
            <div className="food-web-stats">
                <div className="stat-pill"><span className="stat-dot" style={{ background: '#22c55e' }} /> {stats.plant_count || 0} plants</div>
                <div className="stat-pill"><span className="stat-dot" style={{ background: '#fbbf24' }} /> {stats.pollinator_count || 0} pollinators</div>
                <div className="stat-pill"><span className="stat-dot" style={{ background: '#38bdf8' }} /> {stats.bird_count || 0} birds</div>
                <div className="stat-pill">{stats.total_edges || 0} connections</div>
            </div>
            <div className="food-web-legend">
                <span className="legend-item"><span className="legend-dot" style={{ background: '#22c55e' }} /> Plants</span>
                <span className="legend-item"><span className="legend-dot" style={{ background: '#fbbf24' }} /> Bees</span>
                <span className="legend-item"><span className="legend-dot" style={{ background: '#fb7185' }} /> Butterflies</span>
                <span className="legend-item"><span className="legend-dot" style={{ background: '#38bdf8' }} /> Birds</span>
            </div>
        </div>
    )
}
