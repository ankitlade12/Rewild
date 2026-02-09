---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Ecological Data Layer

## Objective
Build the embedded data layer that powers all downstream features: zip → USDA zone, zip → ecoregion, native plants by ecoregion, and plant-pollinator interactions. This is the foundation everything else depends on.

## Context
- .gsd/SPEC.md
- .gsd/phases/1/RESEARCH.md
- backend/app/data/

## Tasks

<task type="auto">
  <name>Create USDA Hardiness Zone lookup</name>
  <files>backend/app/data/usda_zones.py</files>
  <action>
    Create a Python module with a dict mapping 3-digit zip prefixes to USDA hardiness zones.
    - Cover all continental US 3-digit prefixes (~900 entries)
    - Format: {"010": "6a", "011": "5b", ...}
    - Include a lookup function: get_zone(zip_code: str) -> dict with zone, min_temp_f range
    - Source data from USDA 2023 hardiness zone map
    - Do NOT use external API calls — this must be fully embedded
  </action>
  <verify>cd backend && uv run python -c "from app.data.usda_zones import get_zone; r = get_zone('75201'); assert r['zone'], f'Got {r}'; print(f'75201 → Zone {r[\"zone\"]}')"</verify>
  <done>get_zone() returns correct hardiness zone for any valid US zip code</done>
</task>

<task type="auto">
  <name>Create EPA Ecoregion lookup</name>
  <files>backend/app/data/ecoregions.py</files>
  <action>
    Create a Python module mapping 3-digit zip prefixes to EPA Level III ecoregion names.
    - Cover top 20+ ecoregions (Eastern Temperate Forests, Great Plains, Mediterranean California, etc.)
    - Format: {"010": {"ecoregion": "Southeastern Plains", "description": "...", "climate": "..."}, ...}
    - Include function: get_ecoregion(zip_code: str) -> dict with ecoregion name, description, typical climate
    - Where multiple ecoregions exist for a prefix, pick the dominant one
    - Do NOT require GIS processing — use pre-curated manual mapping
  </action>
  <verify>cd backend && uv run python -c "from app.data.ecoregions import get_ecoregion; r = get_ecoregion('75201'); assert r['ecoregion'], f'Got {r}'; print(f'75201 → {r[\"ecoregion\"]}')"</verify>
  <done>get_ecoregion() returns correct ecoregion for any valid US zip code</done>
</task>

<task type="auto">
  <name>Create native plants + pollinator interaction data</name>
  <files>backend/app/data/native_plants.py, backend/app/data/pollinators.py</files>
  <action>
    Create two modules:
    
    1. native_plants.py:
    - Dict of native plants per ecoregion, each with: common_name, scientific_name, bloom_months (list), height_ft, sun_requirement, soil_preference, ecological_value, pollinator_associations (list)
    - At least 15-20 plants per ecoregion for top 10 ecoregions
    - Function: get_native_plants(ecoregion: str, sun: str = None, soil: str = None) -> list[dict]
    
    2. pollinators.py:
    - Dict of pollinators commonly found per ecoregion with: name, type (bee/butterfly/moth/hummingbird), flight_months, nesting_type, plants_visited (list), conservation_status
    - Function: get_pollinators(ecoregion: str) -> list[dict]
    - Function: get_plant_pollinator_matrix(ecoregion: str) -> dict mapping plant→list[pollinators]
    
    - Do NOT attempt to download DoPI — curate US-focused data from Pollinator.org guides
    - Include common species: monarchs, various native bees, swallowtails, hummingbirds
  </action>
  <verify>cd backend && uv run python -c "from app.data.native_plants import get_native_plants; from app.data.pollinators import get_pollinators; plants = get_native_plants('Eastern Temperate Forests'); pollinators = get_pollinators('Eastern Temperate Forests'); print(f'{len(plants)} plants, {len(pollinators)} pollinators')"</verify>
  <done>Both modules return species data for at least 10 ecoregions with 15+ plants and 10+ pollinators each</done>
</task>

## Success Criteria
- [ ] get_zone() works for 5+ diverse zip codes (75201, 10001, 90210, 60601, 33101)
- [ ] get_ecoregion() returns meaningful ecoregion data for same zip codes
- [ ] get_native_plants() returns 15+ plants for at least 10 ecoregions
- [ ] get_pollinators() returns 10+ pollinators for at least 10 ecoregions
- [ ] All data is embedded — zero external API calls required
