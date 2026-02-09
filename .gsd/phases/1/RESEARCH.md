# RESEARCH.md — Phase 1: Foundation & Data Layer

## Data Sources Analysis

### USDA Hardiness Zone Lookup
- **Best option**: Frostline project (GitHub: `kgjenkins/frostline`) — provides static JSON files per zip code via `phzmapi.org`
- **Alternative**: We'll embed a simplified zip-prefix → zone mapping as JSON (first 3 digits of zip → zone)
- **Decision**: Pre-build a JSON lookup of ~900 3-digit zip prefixes → hardiness zones. Covers all continental US.

### EPA Ecoregion Mapping
- **Source**: EPA Level III Ecoregions shapefiles
- **Challenge**: No direct zip → ecoregion API exists
- **Decision**: Pre-build a zip-prefix → ecoregion mapping using spatial analysis. For MVP, use a curated mapping of ~20 major ecoregions covering the most common US zip codes.
- **Fallback**: Claude API can reason about ecoregion from state + zone combo

### Plant-Pollinator Interactions
- **DoPI**: Primarily British data — NOT suitable for US-focused MVP
- **Decision**: Curate our own US plant-pollinator interaction dataset from:
  - Pollinator.org regional planting guides (top 20 ecoregions)
  - USDA PLANTS database (native plant traits)
  - Published literature on native bee-plant associations
- **Format**: JSON with plant species → pollinator species → interaction strength

### Native Plant Data
- **Source**: Pollinator.org ecoregional guides + USDA PLANTS
- **Decision**: Pre-extract recommended native plants for top 20 US ecoregions with traits (bloom time, height, sun/soil needs, pollinator associations)

## Architecture Decisions
- All lookup data embedded as JSON in `backend/app/data/`
- FastAPI serves data via REST endpoints
- Frontend calls backend for lookups, keeps UI state in React
