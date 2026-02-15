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

## Validation
```bash
cd backend
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall app tests
```
