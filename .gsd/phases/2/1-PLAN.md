---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Deterministic Rules Engine

## Objective
Build the core simulation engine that models ecological succession over 5 years using deterministic rules. No LLM dependency — this layer runs fast and provides baseline trajectories.

## Tasks

### Task 1: Succession Timeline Model
**File**: `backend/app/engine/succession.py`

Create a rules-based succession model that computes year-by-year ecological metrics for each intervention type:

- **Input**: SiteProfile + Intervention + ecoregion/zone data
- **Output**: 5-year timeline of ecological metrics per intervention
- **Metrics to model** (each returns `{optimistic, likely, conservative}` per year):
  - `pollinator_diversity_index` (0-1 scale, species richness relative to regional max)
  - `bird_activity_score` (0-1 scale, habitat suitability for local bird guilds)
  - `food_web_complexity` (0-1 scale, connectance of plant-pollinator-bird network)
  - `ecosystem_services_score` (0-1 scale, composite of carbon, water, soil)
- **Rules by intervention**:
  - `stop_mowing`: Slow start (Y1: 0.1), accelerating Y3-5
  - `native_meadow`: Moderate start (Y1: 0.2), peak by Y3
  - `rain_garden`: Fast water benefit, moderate bio benefit
  - `shrub_border`: Slow (woody plants), high Y4-5 payoff
  - Each modified by `current_state` (weedy starts higher than lawn)
  - Each modified by ecoregion (tropical faster, northern slower)

### Task 2: Bloom Calendar Generator
**File**: `backend/app/engine/bloom_calendar.py`

Generate a month-by-month bloom calendar for a site based on selected interventions:

- Cross-reference intervention type with ecoregion native plants
- Filter plants by sun/soil compatibility
- Output: `{month: [plant1, plant2, ...]}` with bloom intensity

### Task 3: Interaction Matrix Builder
**File**: `backend/app/engine/interactions.py`

Build the plant-pollinator-bird food web graph for a site over time:

- **Year 0**: Empty (just site current state)
- **Year 1-5**: Growing network based on succession model
- Nodes: plants, pollinators, birds (from data layer)
- Edges: plant→pollinator, pollinator→bird (trophic links)
- Output: `{year: {nodes: [...], edges: [...]}}` for D3 consumption

## Verification
```bash
cd backend && uv run python -c "
from app.engine.succession import simulate_trajectory
from app.engine.bloom_calendar import generate_bloom_calendar
from app.engine.interactions import build_food_web

# Test succession
result = simulate_trajectory(
    zip_code='75201', intervention='native_meadow',
    area_sqft=500, current_state='maintained_lawn',
    sun='full', soil='well_drained'
)
assert len(result['years']) == 6  # Y0-Y5
assert all(k in result['years'][3] for k in ['pollinator_diversity_index','bird_activity_score','food_web_complexity','ecosystem_services_score'])
print('✅ Succession model works')

# Test bloom calendar
cal = generate_bloom_calendar('Great Plains', 'full', 'well_drained')
assert len(cal) > 0
print('✅ Bloom calendar works')

# Test food web
web = build_food_web('Great Plains', ['native_meadow'], 'full', 'well_drained')
assert 3 in web  # Year 3 exists
assert len(web[3]['nodes']) > 0
print('✅ Food web works')
"
```
