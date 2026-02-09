# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
Rewild is a consumer ecological scenario engine for micro-habitats. Users enter their location and site description, select interventions (native meadow, rain garden, stop mowing, etc.), and see likely ecological trajectories over 1-5 years with honest uncertainty bands. No consumer product does intervention → trajectory simulation at yard scale. We fill that gap for homeowners and schools.

## Goals
1. **Scenario Comparison Engine** — Users compare 2-3 interventions side-by-side and see diverging ecological trajectories (pollinator diversity, bird activity, food web complexity, ecosystem services) over 5 years
2. **Uncertainty-First Outputs** — Every metric shows confidence bands (optimistic/likely/conservative), confidence indicators, and actionable uncertainty-reducers ("Adding a soil test would narrow this range")
3. **Actionable Plans** — Generate month-by-month planting calendars, species recommendations, "what NOT to do" lists, and observation milestones tied to the user's specific ecoregion
4. **Calibration Hooks** — Users report observations ("I saw a monarch today") that update trajectory confidence, creating a data flywheel

## Non-Goals (Out of Scope)
- High-fidelity precision ecological forecasting (we are scenario comparison, not forecasting)
- Global coverage (MVP is Continental US only)
- Freeform interventions (pre-defined menu of 8 interventions only)
- IoT/sensor integration
- Social/community features (post-hackathon)
- Photo-based site assessment (post-hackathon)

## Users
- **Homeowners** in the native gardening movement (83M US households with yards)
- **K-12 schools** needing hands-on STEM ecology tools
- **Municipal planners** exploring residential rewilding programs (stretch)

## Constraints
- **Timeline**: 11 days (DevDash 2026 hackathon)
- **Tech Stack**: React SPA + Python backend (uv) + Claude API
- **Data**: Pre-embedded USDA zones, EPA ecoregions, Pollinator.org guides, DoPI interactions, USDA PLANTS
- **MVP Habitat Classes**: Lawn-to-meadow, pollinator garden, rain garden (3 only)
- **Regions**: Continental US (USDA zones + EPA ecoregions)
- **Temporal**: Annual snapshots, Years 0-5

## Success Criteria
- [ ] User enters zip code + site profile in < 2 minutes via progressive wizard
- [ ] System generates side-by-side trajectory comparison for 2+ interventions
- [ ] All outputs show uncertainty bands / confidence indicators
- [ ] Food web network animation grows over simulated 5-year timeline (the "wow" moment)
- [ ] Action plan with month-by-month calendar is downloadable
- [ ] Demo works reliably for 5+ diverse US zip codes
- [ ] 3-minute demo video tells a compelling story
