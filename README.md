# 🌿 REWILD — Ecological Scenario Engine for Micro-Habitats

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Compare ecological interventions and visualize likely habitat trajectories over 5 years — built for homeowners and schools.**

## Quick Highlights

- **Scenario Comparison**: Compare native meadow vs rain garden vs shrub border side-by-side
- **5-Year Trajectories**: Pollinator diversity, carbon sequestration, ecosystem services, habitat complexity
- **Uncertainty-First**: Every projection shows optimistic / likely / conservative bands with confidence scores
- **AI-Powered Narratives**: OpenAI explains ecological outcomes and recommends species
- **Interactive Food Web**: Watch your ecosystem grow from bare soil to a thriving network
- **Actionable Output**: Printable planting calendars, shopping lists, and month-by-month guides

## The Problem

When homeowners want to rewild their yard:
- Pollinator garden selectors give **static plant lists** — no trajectory over time
- AI landscape tools show how it **looks** — not how the **ecology evolves**
- Research simulators require **institutional expertise** to operate
- No tool answers: *"If I plant a native meadow vs a rain garden, what happens to pollinators in Year 3?"*

## The Solution

REWILD is a **consumer ecological scenario engine** that:
1. **Ingests** your location + site description (ZIP → USDA zone + EPA ecoregion)
2. **Simulates** ecological trajectories for each intervention over 5 years
3. **Compares** scenarios with uncertainty bands so you see the range of outcomes
4. **Generates** personalized planting calendars and action plans

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  FRONTEND (React + Vite)                  │
│                                                          │
│  SiteProfileWizard → InterventionPanel → Dashboard       │
│  TrajectoryChart (Recharts) │ FoodWebGraph (Canvas)      │
│  ConfidencePanel │ BloomCalendar │ ActionPlan             │
└──────────────────────┬───────────────────────────────────┘
                       │ /api/* (Vite proxy)
┌──────────────────────▼───────────────────────────────────┐
│                  BACKEND (FastAPI + Uvicorn)              │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Data Layer   │  │ Engine Layer │  │ AI Layer       │  │
│  │ ─────────── │  │ ──────────── │  │ ────────────── │  │
│  │ USDA Zones   │  │ Succession   │  │ OpenAI GPT-4o  │  │
│  │ EPA Ecoregn  │  │ Bloom Cal    │  │ Fallback narr  │  │
│  │ Native Plant │  │ Food Web     │  │                │  │
│  │ Pollinators  │  │ Uncertainty  │  │                │  │
│  │ Interventns  │  │ Action Plan  │  │                │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite | 4-screen wizard → dashboard flow |
| **Charts** | Recharts | Trajectory timelines with confidence bands |
| **Visualization** | Canvas 2D | Animated food web network |
| **Backend** | FastAPI + Python | REST API and simulation engine |
| **AI** | OpenAI GPT-4o-mini | Ecological narratives + species recommendations |
| **Data** | Curated JSON datasets | USDA zones, EPA ecoregions, native plants, pollinators |

## Features

### 🧙 Site Profile Wizard
- ZIP code → automatic USDA hardiness zone + EPA ecoregion lookup
- Site conditions: current state, sun exposure, soil type
- Goal selection: pollinators, birds, water management, carbon, beauty

### 🔬 Scenario Engine
- **Deterministic succession model**: 5-year trajectories for 4 key metrics
- **Uncertainty propagation**: Confidence bands widen with time, narrow with data
- **Food web builder**: Plant → pollinator → bird trophic network grows over time
- **Bloom calendar**: Month-by-month flowering schedule for continuous pollinator support

### 📊 Trajectory Dashboard
- **Overlay mode**: Compare all scenarios on one chart
- **Side-by-side mode**: Individual charts per intervention
- **Metric tabs**: Pollinator diversity, carbon sequestration, ecosystem services, habitat complexity
- **Food web animation**: Play 5-year growth from bare soil to complex ecosystem

### 📋 Action Plan
- **Planting calendar**: Month-by-month tasks tied to your frost dates
- **Shopping list**: Species with quantities calculated for your area
- **Prep tasks**: Week-by-week site preparation guide
- **Seasonal maintenance**: Spring / summer / fall / winter checklists
- **Common mistakes**: What NOT to do (and why)
- **Print to PDF**: Take your planting calendar to the garden center

## Quick Start

### Prerequisites

- Python 3.11+ with [uv](https://docs.astral.sh/uv/)
- Node.js 20+
- OpenAI API key (optional — works without it via fallback narratives)

### Step 1: Clone and Setup

```bash
git clone https://github.com/your-repo/rewild.git
cd rewild
```

### Step 2: Install Dependencies

```bash
# Backend
cd backend
uv sync

# Frontend
cd ../frontend
npm install
```

### Step 3: Configure Environment

```bash
# Optional: Add OpenAI key for AI-powered narratives
cp backend/.env.example backend/.env
# Edit backend/.env and add: OPENAI_API_KEY=your_key_here
```

### Step 4: Start Servers

```bash
# Terminal 1 — Backend
cd backend
uv run uvicorn app.main:app --port 8000

# Terminal 2 — Frontend
cd frontend
npm run dev
```

### Step 5: Open the App

| Service | URL |
|---------|-----|
| **App** | http://localhost:5173 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

## Demo Walkthrough

1. Enter ZIP **75254** → Look Up → Area **1000** sq ft → Continue
2. Select **Maintained Lawn** · **Full Sun** · **Well-drained** → Continue
3. Check **Support Pollinators** + **Natural Beauty** → See Interventions
4. Select **Native Meadow** + **Rain Garden** → **Run Scenario Engine**
5. Toggle **Side by Side** → switch metrics → play food web animation
6. Click **Get Your Action Plan →** → browse 5 tabs → 🖨️ Print

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/lookup/{zip}` | USDA zone + EPA ecoregion lookup |
| `GET` | `/api/interventions` | List available interventions |
| `GET` | `/api/plants/{ecoregion}` | Native plants for ecoregion |
| `GET` | `/api/pollinators/{ecoregion}` | Pollinators for ecoregion |
| `POST` | `/api/simulate` | Run full simulation pipeline |
| `POST` | `/api/action-plan` | Generate planting calendar + action plan |

## Project Structure

```
rewild/
├── backend/
│   ├── app/
│   │   ├── data/                  # Curated ecological datasets
│   │   │   ├── usda_zones.py      # Hardiness zone lookup (3-digit ZIP)
│   │   │   ├── ecoregions.py      # EPA Level III ecoregion mapping
│   │   │   ├── native_plants.py   # Native species by ecoregion
│   │   │   ├── pollinators.py     # Pollinator species data
│   │   │   └── interventions.py   # Intervention definitions
│   │   ├── engine/                # Simulation engine
│   │   │   ├── succession.py      # 5-year trajectory model
│   │   │   ├── bloom_calendar.py  # Month-by-month bloom schedule
│   │   │   ├── interactions.py    # Food web graph builder
│   │   │   ├── uncertainty.py     # Confidence bands + reducers
│   │   │   ├── claude_reasoner.py # OpenAI narrative generator
│   │   │   └── action_plan.py     # Planting calendar generator
│   │   ├── routes/                # API endpoints
│   │   │   ├── lookup.py          # Location lookup routes
│   │   │   └── simulate.py        # Simulation + action plan routes
│   │   └── main.py               # FastAPI app entry point
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── SiteProfileWizard.jsx  # 3-step site profile wizard
│   │   ├── InterventionPanel.jsx  # Intervention selection + scoring
│   │   ├── Dashboard.jsx          # Main dashboard orchestrator
│   │   ├── TrajectoryChart.jsx    # Recharts trajectory visualization
│   │   ├── FoodWebGraph.jsx       # Canvas food web network
│   │   ├── ConfidencePanel.jsx    # AI narrative + uncertainty panel
│   │   ├── ActionPlan.jsx         # 5-tab action plan with print
│   │   ├── App.jsx                # Root component with routing
│   │   └── App.css                # Complete design system
│   ├── package.json
│   └── vite.config.js             # Proxy config for /api/*
├── .env.example
├── .gitignore
├── LICENSE                        # MIT
└── README.md
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | No | OpenAI API key for AI narratives (falls back to templates) |

## Design Decisions

- **Uncertainty-first**: Every metric shows range bands, not point predictions
- **Offline-capable AI**: Works fully without an API key using template narratives
- **Ecoregion-aware**: All data is localized to EPA Level III ecoregions
- **Intervention comparison**: Side-by-side comparison is a first-class feature
- **Printable output**: Action plans designed for printing and taking to the garden

## License

MIT License — see [LICENSE](LICENSE) file for details.

---

**Built for DevDash 2026**

*Compare what happens under different scenarios, see the likely range of outcomes, and learn what to observe.*
