# Rewild Backend

FastAPI backend for REWILD's ecological scenario engine.

## Requirements
- Python 3.13+
- `uv` (recommended) or an equivalent virtualenv workflow

## Setup
```bash
cd backend
uv sync
```

## Run
```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

## API
- Health: `GET /health`
- Lookup: `GET /api/lookup/{zip_code}`
- Interventions: `GET /api/interventions`
- Plants: `GET /api/plants/{ecoregion}`
- Pollinators: `GET /api/pollinators/{ecoregion}`
- Simulate: `POST /api/simulate`
- Action plan: `POST /api/action-plan`

## Engine Modules

| Module | Purpose | Key Enhancement |
|--------|---------|-----------------|
| `succession.py` | 5-year trajectory model | Logistic growth curves, soil cross-effects, multi-intervention synergy |
| `bloom_calendar.py` | Monthly bloom schedule | Bloom continuity score (Shannon entropy), succession-aware projections, gap-filling recommendations |
| `interactions.py` | Food web graph builder | Shannon-Wiener diversity index (H'), Pielou evenness (J'), directed connectance |
| `uncertainty.py` | Confidence bands | Optimistic/likely/conservative ranges with reducers |
| `claude_reasoner.py` | AI narratives | OpenAI GPT-4o-mini with template fallback |
| `action_plan.py` | Planting calendar | Frost-date-aware scheduling with shopping lists |

## Testing
```bash
cd backend
uv run python -m pytest tests/ -v
```

**89 tests** covering:
- `test_succession.py` — logistic curves, synergy, soil effects, per-metric weights, trajectory boundaries (37 tests)
- `test_bloom_calendar.py` — continuity score, gap recommendations, succession bloom (22 tests)
- `test_interactions.py` — Shannon-Wiener, evenness, directed connectance, food web integration (16 tests)
- `test_api_routes.py` — endpoint integration tests (7 tests)
- `test_ecology_outputs.py` — bloom calendar + food web edge cases (3 tests)
- `test_native_plants.py`, `test_usda_zones.py`, `test_action_plan.py` — data layer tests (4 tests)
