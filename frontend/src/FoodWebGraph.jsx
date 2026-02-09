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
        const width = svgRef.current.clientWidth || 500
        const height = 400

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

        const GROUP_Y = {
            producer: height * 0.75,
            consumer: height * 0.45,
            top_consumer: height * 0.15,
        }

        // Create force simulation
        const simulation = d3.forceSimulation(data.nodes)
            .force('link', d3.forceLink(data.edges).id(d => d.id).distance(60).strength(0.3))
            .force('charge', d3.forceManyBody().strength(-80))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('y', d3.forceY(d => GROUP_Y[d.group] || height / 2).strength(0.15))
            .force('collision', d3.forceCollide().radius(d => (d.size || 6) + 4))

        // Links
        const link = svg.append('g')
            .selectAll('line')
            .data(data.edges)
            .enter().append('line')
            .attr('stroke', d => d.type === 'pollination' ? 'rgba(34,197,94,0.25)' : 'rgba(56,189,248,0.2)')
            .attr('stroke-width', d => Math.max(1, (d.strength || 0.5) * 2))

        // Nodes
        const node = svg.append('g')
            .selectAll('circle')
            .data(data.nodes)
            .enter().append('circle')
            .attr('r', d => d.size || 6)
            .attr('fill', d => TYPE_COLORS[d.type] || '#64748b')
            .attr('stroke', d => d.conservation === 'declining' || d.conservation === 'vulnerable'
                ? '#f43f5e' : 'rgba(255,255,255,0.1)')
            .attr('stroke-width', d => d.conservation === 'declining' ? 2 : 1)
            .attr('opacity', 0)
            .transition().duration(600).delay((d, i) => i * 30)
            .attr('opacity', 0.9)

        // Labels for larger nodes
        const label = svg.append('g')
            .selectAll('text')
            .data(data.nodes.filter(n => (n.size || 6) >= 8))
            .enter().append('text')
            .text(d => d.label.length > 15 ? d.label.slice(0, 13) + '…' : d.label)
            .attr('font-size', '9px')
            .attr('fill', '#94a3b8')
            .attr('text-anchor', 'middle')
            .attr('dy', d => -(d.size || 6) - 4)

        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y)
            node
                .attr('cx', d => d.x = Math.max(10, Math.min(width - 10, d.x)))
                .attr('cy', d => d.y = Math.max(10, Math.min(height - 10, d.y)))
            label
                .attr('x', d => d.x)
                .attr('y', d => d.y)
        })

        return () => simulation.stop()
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
