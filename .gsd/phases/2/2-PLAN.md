---
phase: 2
plan: 2
wave: 1
---

# Plan 2.2: Claude API Integration & Uncertainty Layer

## Objective
Integrate Claude API for ecological reasoning and build the uncertainty propagation layer that wraps all engine outputs in confidence bands.

## Tasks

### Task 1: Claude Ecological Reasoner
**File**: `backend/app/engine/claude_reasoner.py`

Build structured prompts for Claude to enhance scenario narratives:

- **Narrative generation**: Given a site profile + intervention + deterministic metrics, Claude generates a natural-language ecological narrative explaining what's happening and why
- **Species recommendations**: Claude suggests specific species for the site beyond our data layer (with citations to general ecology)
- **Uncertainty commentary**: Claude explains what sources of uncertainty apply and what would reduce them
- **Structured output**: Use system prompt to enforce JSON-compatible responses
- **Fallback**: If API fails or no key, return placeholder text (engine must work without Claude)
- **Rate limiting**: Cache responses, avoid redundant calls

### Task 2: Uncertainty Propagation
**File**: `backend/app/engine/uncertainty.py`

Wrap all engine outputs in uncertainty bands:

- Each metric gets `{optimistic, likely, conservative}` values
- Uncertainty width varies by:
  - **Ecoregion**: Better-studied regions have tighter bands
  - **Intervention**: Well-documented interventions (meadow) vs. novel (stop mowing)
  - **Time horizon**: Uncertainty grows with years (Y1 tight, Y5 wide)
  - **Site factors**: Unknown soil = wider bands
- Compute confidence level (0-100%) for each metric
- Generate "uncertainty reducers": actionable suggestions that would tighten bands

### Task 3: Simulation API Endpoint
**File**: `backend/app/routes/simulate.py`

Create the main simulation endpoint that orchestrates all engine layers:

- `POST /api/simulate` accepts `{site_profile, interventions[]}`
- Returns: `{scenarios: [{intervention, timeline[], narrative, bloom_calendar, food_web, confidence}]}`
- Orchestrates: succession → interactions → bloom → uncertainty → (optional) Claude narrative
- Register route in `main.py`

## Verification
```bash
# Test without Claude (should work with fallback)
cd backend && uv run python -c "
import asyncio
from app.engine.claude_reasoner import get_narrative
result = asyncio.run(get_narrative(
    ecoregion='Great Plains',
    intervention='native_meadow',
    metrics={'pollinator_diversity_index': 0.4},
    use_claude=False
))
assert 'narrative' in result
print('✅ Claude fallback works')
"

# Test uncertainty
cd backend && uv run python -c "
from app.engine.uncertainty import apply_uncertainty
bands = apply_uncertainty(
    base_value=0.5, year=3, ecoregion='Great Plains',
    intervention='native_meadow', soil_known=True
)
assert bands['optimistic'] > bands['likely'] > bands['conservative']
assert 0 <= bands['confidence'] <= 100
print('✅ Uncertainty propagation works')
"

# Test full simulation endpoint
cd backend && uv run uvicorn app.main:app --port 8000 &
sleep 2
curl -X POST http://localhost:8000/api/simulate \
  -H 'Content-Type: application/json' \
  -d '{"site_profile":{"zip_code":"75201","area_sqft":500,"current_state":"maintained_lawn","sun_exposure":"full","soil_type":"well_drained","goals":["pollinators"]},"interventions":["native_meadow","stop_mowing"]}' \
  | python3 -m json.tool | head -40
kill %1
echo "✅ Simulation endpoint works"
```
