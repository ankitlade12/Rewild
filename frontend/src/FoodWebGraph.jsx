import { useRef, useEffect, useState } from 'react'

export default function FoodWebGraph({ foodWeb, year: initialYear }) {
    const canvasRef = useRef(null)
    const [year, setYear] = useState(initialYear || 0)
    const [isPlaying, setIsPlaying] = useState(false)
    const timerRef = useRef(null)

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
        if (!foodWeb || !canvasRef.current) return
        const data = foodWeb[year]
        if (!data) return

        const canvas = canvasRef.current
        const ctx = canvas.getContext('2d')
        const dpr = window.devicePixelRatio || 1
        const w = canvas.clientWidth
        const h = 400
        canvas.width = w * dpr
        canvas.height = h * dpr
        ctx.scale(dpr, dpr)
        ctx.clearRect(0, 0, w, h)

        if (data.nodes.length === 0) {
            ctx.fillStyle = '#64748b'
            ctx.font = '14px Inter, sans-serif'
            ctx.textAlign = 'center'
            ctx.fillText(`Year ${year}: No supported food-web species for current site filters`, w / 2, h / 2)
            return
        }

        const TYPE_COLORS = {
            plant: '#22c55e', bee: '#fbbf24', butterfly: '#fb7185',
            moth: '#c084fc', hummingbird: '#f43f5e', fly: '#94a3b8',
            wasp: '#f97316', beetle: '#a78bfa', bird: '#38bdf8',
        }

        // Separate into trophic layers
        const plants = data.nodes.filter(n => n.group === 'producer')
        const pollinators = data.nodes.filter(n => n.group === 'consumer')
        const birds = data.nodes.filter(n => n.group === 'top_consumer')

        // Position nodes in clean rows
        const padding = 50
        const usableW = w - padding * 2

        const positionRow = (items, rowY) => {
            const gap = items.length > 1 ? usableW / (items.length - 1) : 0
            const startX = items.length > 1 ? padding : w / 2
            items.forEach((item, i) => {
                item._x = startX + i * gap
                item._y = rowY
            })
        }

        positionRow(birds, 60)
        positionRow(pollinators, h / 2)
        positionRow(plants, h - 60)

        // Build position map
        const posMap = {}
        data.nodes.forEach(n => { posMap[n.id] = n })

        // Draw edges as curved lines
        data.edges.forEach(edge => {
            const src = posMap[typeof edge.source === 'object' ? edge.source.id : edge.source]
            const tgt = posMap[typeof edge.target === 'object' ? edge.target.id : edge.target]
            if (!src || !tgt || src._x == null || tgt._x == null) return

            ctx.beginPath()
            const midY = (src._y + tgt._y) / 2
            const cpxOffset = (Math.random() - 0.5) * 30
            ctx.moveTo(src._x, src._y)
            ctx.quadraticCurveTo(
                (src._x + tgt._x) / 2 + cpxOffset,
                midY,
                tgt._x, tgt._y
            )
            ctx.strokeStyle = edge.type === 'pollination'
                ? 'rgba(34,197,94,0.12)'
                : 'rgba(56,189,248,0.10)'
            ctx.lineWidth = 1
            ctx.stroke()
        })

        // Draw nodes
        data.nodes.forEach(n => {
            if (n._x == null) return
            const r = Math.min(n.size || 5, 10)
            ctx.beginPath()
            ctx.arc(n._x, n._y, r, 0, Math.PI * 2)
            ctx.fillStyle = TYPE_COLORS[n.type] || '#64748b'
            ctx.fill()

            if (n.conservation === 'declining' || n.conservation === 'vulnerable') {
                ctx.strokeStyle = '#f43f5e'
                ctx.lineWidth = 2
                ctx.stroke()
            }
        })

        // Labels: row headers
        ctx.fillStyle = '#475569'
        ctx.font = 'bold 10px Inter, sans-serif'
        ctx.textAlign = 'left'
        ctx.fillText('🐦 BIRDS', 8, 30)
        ctx.fillText('🐝 POLLINATORS', 8, h / 2 - 25)
        ctx.fillText('🌿 PLANTS', 8, h - 25)

        // Labels: top 4 per row
        ctx.font = '9px Inter, sans-serif'
        ctx.fillStyle = '#8b9dc3'
        ctx.textAlign = 'center'

        const labelTop = (items, offsetY) => {
            const sorted = [...items].sort((a, b) => (b.size || 5) - (a.size || 5))
            sorted.slice(0, Math.min(5, items.length)).forEach(n => {
                if (n._x == null) return
                const name = (n.label || n.id)
                const short = name.length > 10 ? name.slice(0, 9) + '…' : name
                ctx.fillText(short, n._x, n._y + offsetY)
            })
        }
        labelTop(birds, -16)
        labelTop(pollinators, -14)
        labelTop(plants, 18)

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
            <canvas ref={canvasRef} className="food-web-svg" style={{ width: '100%', height: 400 }} />
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
