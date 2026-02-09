# ROADMAP.md

> **Current Phase**: Not started
> **Milestone**: v1.0 — DevDash 2026 Submission

## Must-Haves (from SPEC)
- [ ] Site Profile Wizard (zip → ecoregion → site details → goals)
- [ ] Intervention selection with comparison mode (2-3 side-by-side)
- [ ] Trajectory Dashboard with confidence bands (pollinator, birds, food web, services)
- [ ] Food web network animation (D3 force-directed, growing over 5 years)
- [ ] Action plan generator with planting calendar
- [ ] Uncertainty-first design everywhere
- [ ] Working demo for 5+ US zip codes

## Phases

### Phase 1: Foundation & Data Layer
**Status**: ⬜ Not Started
**Objective**: Project scaffolding, embedded data pipeline, and Site Profile Wizard
- React + Vite frontend setup
- Python backend with uv (FastAPI)
- Embed zip→zone, zip→ecoregion, plant-pollinator (DoPI) data as JSON
- Site Profile Wizard (3-step progressive form)
- Intervention selection UI

### Phase 2: Scenario Engine
**Status**: ⬜ Not Started
**Objective**: Build the 3-layer simulation engine (rules + LLM + uncertainty)
- Deterministic rules layer (succession timelines, bloom calendars, zone logic)
- Plant-pollinator interaction matrix queries
- Claude API integration with structured ecological prompts
- Uncertainty propagation (confidence bands per metric per ecoregion)
- Python API endpoints for simulation

### Phase 3: Trajectory Dashboard
**Status**: ⬜ Not Started
**Objective**: Build the hero visualization screen
- Pollinator diversity timeline (Recharts area chart + confidence bands)
- Bird activity timeline
- Food web network animation (D3 force-directed graph)
- Ecosystem services stacked bars
- Confidence panel with uncertainty-reducer prompts
- Side-by-side comparison view

### Phase 4: Action Plan & Polish
**Status**: ⬜ Not Started
**Objective**: Action plan generation, calibration hooks, visual polish, submission
- Action plan generator (downloadable planting calendar)
- Observation logger UI (calibration hooks)
- Visual polish, animations, loading states
- Mobile responsiveness
- Edge case handling
- 3-minute demo video
- README + Devpost submission
