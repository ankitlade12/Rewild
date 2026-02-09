# DECISIONS.md — Architecture Decision Records

## ADR-001: Hybrid Client-Server Architecture
**Date**: 2026-02-09
**Status**: Accepted
**Decision**: React SPA frontend + Python (uv/FastAPI) backend instead of pure client-side
**Rationale**: Python backend enables better data processing, Claude API key security, and pre-computation of ecological models. `uv` for fast dependency management.

## ADR-002: Uncertainty-First Design
**Date**: 2026-02-09
**Status**: Accepted
**Decision**: Every output shows range bands (optimistic/likely/conservative), never point estimates
**Rationale**: Overclaiming ecological precision is the #1 risk. Honest uncertainty is also a differentiator.

## ADR-003: Pre-Embedded Data Strategy
**Date**: 2026-02-09
**Status**: Accepted
**Decision**: Bake DoPI, USDA zones, ecoregion data into the app at build time rather than live API calls
**Rationale**: Reduces latency, eliminates external API dependencies during demo, ensures reliability.
