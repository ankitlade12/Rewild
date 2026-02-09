---
phase: 1
plan: 2
wave: 1
---

# Plan 1.2: API Endpoints & Site Profile

## Objective
Create FastAPI endpoints to serve the data layer, and build the backend models for site profiles and interventions. This enables the frontend to query data and submit user inputs.

## Context
- .gsd/SPEC.md
- .gsd/phases/1/1-PLAN.md (data layer it depends on)
- backend/app/main.py
- backend/app/routes/

## Tasks

<task type="auto">
  <name>Create API endpoints for data lookups</name>
  <files>backend/app/routes/lookup.py, backend/app/main.py</files>
  <action>
    Create lookup routes and register them with FastAPI:

    1. GET /api/lookup/{zip_code}
       - Returns: { zone, ecoregion, last_frost_date, first_frost_date, state }
       - Combines usda_zones + ecoregions modules
       - Returns 404 for invalid/unknown zip codes

    2. GET /api/plants/{ecoregion}
       - Query params: sun (optional), soil (optional)  
       - Returns: list of native plants filtered by params

    3. GET /api/pollinators/{ecoregion}
       - Returns: list of pollinators + plant-pollinator interaction matrix

    4. GET /api/interventions
       - Returns: list of 8 intervention options with metadata (name, description, effort_level, icon, habitat_classes)

    Register all routes in main.py with APIRouter prefix "/api"
    
    - Use Pydantic models for response schemas
    - Include proper error handling (422 for bad input, 404 for not found)
  </action>
  <verify>cd backend && uv run uvicorn app.main:app --port 8000 & sleep 2 && curl -s http://localhost:8000/api/lookup/75201 | python3 -m json.tool && curl -s http://localhost:8000/api/interventions | python3 -m json.tool && kill %1</verify>
  <done>All 4 endpoints return valid JSON with correct data</done>
</task>

<task type="auto">
  <name>Define intervention models and data</name>
  <files>backend/app/data/interventions.py, backend/app/models.py</files>
  <action>
    Create Pydantic models and intervention data:

    1. models.py — Pydantic schemas:
       - SiteProfile(zip_code, area_sqft, current_state, sun_exposure, soil_type, goals)
       - Intervention(id, name, description, effort_level, icon, habitat_classes)
       - LookupResponse(zone, ecoregion, last_frost, first_frost, state)

    2. interventions.py — The 8 interventions from SPEC:
       - Native Wildflower Meadow
       - Native Shrub Border
       - Rain Garden
       - Stop Mowing Zone
       - Habitat Structures
       - Pollinator Nesting
       - Leave the Leaves
       - Native Grass Conversion
       
       Each with: id, name, description, effort_level (Very Low/Low/Medium/High), 
       icon emoji, applicable habitat_classes, typical_timeline_years
  </action>
  <verify>cd backend && uv run python -c "from app.data.interventions import INTERVENTIONS; print(f'{len(INTERVENTIONS)} interventions'); assert len(INTERVENTIONS) == 8"</verify>
  <done>8 interventions defined with all required fields, Pydantic models validate correctly</done>
</task>

## Success Criteria
- [ ] GET /api/lookup/75201 returns zone + ecoregion + frost dates
- [ ] GET /api/plants/Eastern%20Temperate%20Forests returns native plant list
- [ ] GET /api/interventions returns all 8 interventions
- [ ] Pydantic models validate input/output correctly
- [ ] Invalid zip codes return proper 404 errors
