# 🌿 REWILD — Consumer Ecological Scenario Engine for Micro-Habitats
## DevDash 2026 | Complete Project Plan

---

## Positioning (Final)

> **"Rewild is a consumer ecological scenario engine for micro-habitats: compare interventions and see likely ecological trajectories over time, with uncertainty — built for homeowners and schools."**

Not "we predict your ecosystem." Instead: **"Compare what happens under different intervention scenarios, see the likely range of outcomes, and learn what to observe."**

---

## Why This Wins DevDash

| Judging Criteria | Score | Rationale |
|---|---|---|
| **Creativity** | ★★★★★ | No consumer product does intervention → trajectory simulation at yard scale (validated Jan 2026) |
| **Real World Use** | ★★★★★ | 83M US households w/ yards + native planting movement + STEM education demand |
| **Technologies Used** | ★★★★☆ | LLM ecological reasoning + structured simulation + interactive viz + citizen-science calibration hooks |

---

## Strategic Differentiation (Post-Validation)

### What exists in 2026 and what we're NOT competing with:

| Category | Examples | Why We're Different |
|---|---|---|
| Research-scale biodiversity digital twins | BioDT prototypes, Nature 2026 bird migration DT | They're national/regional, require institutional data pipelines. We're yard-scale, consumer-facing. |
| Pollinator garden plant selectors | BeeSmart, Pollinator Partner, Pollinator.org guides | They output **static plant lists by zip code**. We simulate **what happens over time** after planting. |
| AI landscape visualization | DreamzAR, AI Landscape Design | They show how it **looks**. We show how the **ecology evolves**. |
| Research ecosystem simulators | Ecotwin (Unity-based), APSIM | Research-grade tools requiring technical expertise. Not consumer products. |
| Agricultural digital twins | CropX, greenhouse DTs | Industrial precision farming with IoT. Different domain entirely. |

### The gap (still open as of Feb 2026):

No mainstream consumer product that: **(1)** ingests location + site description, **(2)** builds a localized habitat model, and **(3)** simulates ecological trajectories and intervention deltas over 1-5 years (succession, pollinator attraction curves, food-web proxies) for homeowners/schools.

---

## Critical Design Decisions

### 1. Scope Discipline (The Most Important Decision)

We do NOT promise "high-fidelity ecological forecast for any backyard anywhere."

We promise: **"Scenario comparison with uncertainty bands for a defined micro-habitat class, in defined regions, with defined interventions."**

**MVP Scope Constraints:**
- **Habitat classes**: Lawn-to-meadow conversion, pollinator garden, rain garden (3 classes only)
- **Regions**: Continental US only (leveraging USDA zones, ecoregion data, Pollinator.org guides)
- **Interventions**: Pre-defined menu of 8-10 interventions (not freeform)
- **Temporal resolution**: Annual snapshots, Years 0-5

### 2. Uncertainty-First Outputs (Non-Negotiable)

Every projection shows:
- **Range bands** (optimistic / likely / conservative scenarios)
- **Confidence indicators** per metric (high/medium/low based on data availability for that ecoregion)
- **"What would reduce uncertainty"** prompts: "Adding a soil test would narrow this range" / "Confirming your sun hours would improve accuracy"
- **Explicit caveats**: "This is a scenario comparison tool, not a precision forecast"

### 3. Calibration Hooks (Differentiator + Data Flywheel)

Users can return and report observations:
- "I saw a monarch butterfly today" → system updates trajectory confidence
- "My coneflowers bloomed in June" → adjusts phenology model for their microclimate
- Quick photo check-ins for ground-truth validation

This is inspired by how large-scale citizen science systems (like the Finland MK bird app) power forecasting — just localized. In the MVP, this is a simple observation logger. Over time, it becomes a training signal.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React SPA)                     │
│                                                              │
│  ┌────────────┐  ┌───────────────┐  ┌─────────────────────┐ │
│  │ Site       │  │ Intervention  │  │ Trajectory          │ │
│  │ Profile    │  │ Comparison    │  │ Dashboard           │ │
│  │ Wizard     │  │ Panel         │  │ (Recharts + D3)     │ │
│  └─────┬──────┘  └───────┬───────┘  └─────────────────────┘ │
│        │                 │                                    │
│  ┌─────┴─────────────────┴──────────────────────────────────┐│
│  │              Scenario Engine (Client-side)                ││
│  │  • Deterministic rules layer (bloom timing, zone logic)  ││
│  │  • LLM reasoning layer (Claude API for complex ecology)  ││
│  │  • Uncertainty propagation (confidence bands per metric)  ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘

Scenario Engine Detail:
┌──────────────────────────────────────────────────────────────┐
│  FAST LAYER (Deterministic / Rules-Based)                    │
│  • Zip code → USDA Zone + Ecoregion lookup                  │
│  • Native plant filtering by zone/sun/soil                   │
│  • Bloom phenology calendar (month-by-month)                 │
│  • Basic succession model (grass → shrub → canopy timeline)  │
│  • Pollinator-plant interaction matrix (from DoPI data)      │
│                                                              │
│  REASONING LAYER (Claude API)                                │
│  • Synthesizes site-specific ecological dynamics              │
│  • Generates species arrival probability narratives          │
│  • Computes food web complexity changes                      │
│  • Produces "what to watch for" observational milestones     │
│  • Handles edge cases and unusual site descriptions          │
│                                                              │
│  UNCERTAINTY LAYER                                           │
│  • Propagates confidence from data sparsity per ecoregion    │
│  • Widens bands for unusual soil/microclimate combos         │
│  • Narrows bands when user provides calibration observations │
└──────────────────────────────────────────────────────────────┘
```

---

## Core User Flow

### Screen 1: Site Profile Wizard

**Inputs collected (progressive disclosure — not a wall of fields):**

Step 1 - Location:
- Zip code (auto-resolves: USDA Hardiness Zone, EPA Ecoregion Level III, state)
- "We've identified your ecoregion as [X]. Average last frost: [date]."

Step 2 - Your Site:
- Area size slider (100 sq ft → 5000+ sq ft)
- Current state (multiple choice): Maintained lawn | Weedy/neglected | Partial garden | Bare soil | Paved with removable surfaces
- Sun exposure: Full sun (6+ hrs) | Partial shade (3-6 hrs) | Full shade (<3 hrs)
- Soil: Well-drained | Clay-heavy | Sandy | Don't know (→ triggers "What would reduce uncertainty" prompt later)

Step 3 - Your Goals (multi-select):
- 🦋 Attract pollinators (butterflies, bees)
- 🐦 Support bird habitat
- 💧 Improve water management
- 🌍 Maximize carbon capture
- 🎓 Educational / school project
- 🌸 I just want it to be beautiful AND ecological

### Screen 2: Intervention Comparison Panel

User selects 1-3 interventions to compare side-by-side:

| Intervention | Description | Effort Level |
|---|---|---|
| 🌱 Native Wildflower Meadow | Replace lawn section with native wildflower seed mix | Medium |
| 🌳 Native Shrub Border | Plant 3-5 native shrub species along edges | Medium |
| 💧 Rain Garden | Create a shallow depression with water-loving natives | High |
| 🚫 Stop Mowing Zone | Simply stop mowing a section and let it naturalize | Very Low |
| 🪵 Habitat Structures | Add log piles, rock walls, brush piles | Low |
| 🐝 Pollinator Nesting | Install bee hotels, leave bare soil patches | Low |
| 🍂 Leave the Leaves | Stop fall cleanup, let leaf litter accumulate | Very Low |
| 🌾 Native Grass Conversion | Replace turf grass with native bunch grasses | Medium |

Each intervention generates a parallel 5-year trajectory → user sees them side by side.

### Screen 3: Trajectory Dashboard

**The hero screen. This is what nobody else builds.**

Layout: Timeline (Year 0 → Year 5) across X-axis, with multiple metric tracks:

**Track 1: Pollinator Diversity Index**
- Area chart with confidence bands (light fill = range, line = likely)
- Shows: "By Year 3, expect 4-8 native bee species visiting regularly (currently: ~1)"
- Icons appear on timeline when specific species become likely (monarch at Year 2, native bumblebee at Year 1, etc.)

**Track 2: Bird Activity Score**
- Similar band chart
- "Shrub border attracts first nesting birds by Year 3-4"

**Track 3: Food Web Complexity**
- Network graph that grows over time (animated)
- Year 0: just grass → Year 5: dozens of nodes (plants, insects, birds, soil organisms) with connections
- This is the "wow" visualization for the demo video

**Track 4: Ecosystem Services**
- Stacked bar: Carbon sequestration (kg/yr), Water retention (gallons/storm), Soil health score
- Each with ± range bands

**Confidence Panel (always visible):**
- Overall confidence: "Medium — based on [X] data points for your ecoregion"
- "What would improve this": list of actionable uncertainty-reducers
- "These projections compare scenarios relative to each other. Absolute values are estimates with significant uncertainty."

### Screen 4: Action Plan Generator

Downloadable output:
- Month-by-month planting calendar for their specific ecoregion
- Specific species recommendations (common name, scientific name, where to buy locally)
- "What NOT to do" list (equally important: don't mulch everything, don't deadhead in fall, etc.)
- Observation milestones: "When you see [X], it means [Y] is working — log it!"
- QR code linking back to their Rewild profile for calibration check-ins

---

## Data Sources & Knowledge Base

### Pre-Embedded Data (baked into the app at build time)

| Data | Source | How We Use It |
|---|---|---|
| Zip → Ecoregion mapping | EPA Level III Ecoregions | Route users to correct plant/species pools |
| Zip → USDA Hardiness Zone | USDA Plant Hardiness Map | Filter plants by cold tolerance |
| Native plants by ecoregion | Pollinator.org Ecoregional Guides (pre-extracted) | Core plant recommendation engine |
| Plant traits (bloom time, height, sun/soil needs) | USDA PLANTS Database | Phenology calendar, filtering |
| Plant ↔ Pollinator interactions | DoPI (320K+ records, open CSV) | Interaction matrix powering pollinator predictions |
| Ecological succession timelines | Synthesized from restoration ecology literature | Temporal model backbone |

### Runtime API Calls (via Claude API with web search)

- GBIF Species API: "What species have been observed within 50km of this zip code?" → calibrates local species pool
- Claude reasoning: Synthesizes all data into coherent ecological narrative with uncertainty

### Embedded Ecological Models (Rule-Based Layer)

**Succession Model (simplified for MVP):**
```
Lawn → Year 1: Pioneer annuals (if seeded) or weedy colonizers (if unmowed)
     → Year 2: Perennial establishment, first-year blooms attract generalist pollinators
     → Year 3: Root systems deepening, soil biology recovering, specialist pollinators arriving
     → Year 4: Structural complexity increasing, bird nesting potential if shrubs present
     → Year 5: Self-sustaining meadow with reduced maintenance needs
```

**Pollinator Attraction Model (probability-based):**
```
P(species_X visits) = f(
  plant_species_present,        # from DoPI interaction matrix
  bloom_overlap_with_flight,    # phenology alignment
  nesting_habitat_available,    # from intervention choices
  regional_occurrence,          # from GBIF observation density
  site_area                     # larger area = more species
)
```

Output as ranges, not point estimates.

---

## Tech Stack (Detailed)

### Frontend
- **React** (single .jsx file for hackathon, artifact-compatible)
- **Recharts** — timeline charts with confidence band areas
- **D3.js** — food web network graph animation
- **Tailwind CSS** — styling
- **No localStorage** — all state in React useState/useReducer

### Simulation Backend
- **Claude API** (claude-sonnet-4-20250514) called from the React artifact
  - Structured JSON output mode for simulation data
  - System prompt contains condensed ecological knowledge base (~2000 tokens)
  - Web search tool enabled for GBIF species lookups
- **Client-side rules engine** — deterministic calculations (zone lookups, bloom calendars, interaction matrix queries) run in-browser, no server needed

### Data Pipeline (Pre-Hackathon Prep)
- Download DoPI CSV → extract US-relevant plant-pollinator pairs → embed as JSON
- Extract Pollinator.org guide data for top 20 US ecoregions → embed as JSON
- USDA zone lookup table by zip code prefix → embed as JSON
- Pre-compute "archetype trajectories" for each intervention × habitat class combo

---

## MVP Build Plan (11 Days Remaining)

### Days 1-2: Foundation
- [ ] Set up React project structure
- [ ] Build Site Profile Wizard (3-step progressive form)
- [ ] Implement zip → ecoregion → zone lookup (embedded data)
- [ ] Create intervention selection UI with comparison mode

### Days 3-5: Simulation Engine
- [ ] Build deterministic rules layer (succession timelines, bloom calendars)
- [ ] Embed plant-pollinator interaction matrix (DoPI subset)
- [ ] Implement Claude API integration with structured ecological prompts
- [ ] Build uncertainty propagation logic (confidence bands per metric)
- [ ] Test with 3-5 representative zip codes across different ecoregions

### Days 6-8: Trajectory Dashboard (The Hero Screen)
- [ ] Pollinator diversity timeline with Recharts (area chart + confidence bands)
- [ ] Bird activity timeline
- [ ] Food web network animation (D3 force-directed graph growing over time)
- [ ] Ecosystem services stacked bars
- [ ] Confidence panel with uncertainty-reducer prompts
- [ ] Side-by-side comparison view for 2-3 interventions

### Days 9-10: Action Plan + Polish
- [ ] Action plan generator (downloadable markdown/PDF)
- [ ] Observation logger / calibration hook UI (simple "I saw X today" input)
- [ ] Visual polish, animations, loading states
- [ ] Mobile responsiveness
- [ ] Edge case handling (unknown ecoregions, insufficient data)

### Day 11: Submission Package
- [ ] 3-minute demo video (screen recording + narration)
- [ ] README with architecture diagram
- [ ] Devpost submission with all required fields
- [ ] Source code on GitHub with setup instructions

---

## Demo Video Script (3 minutes)

**[0:00-0:30] The Problem**
"83 million American households have yards. Millions want to help pollinators and local ecosystems. But when they search 'what should I plant?', they get a static list. Nobody tells them: what actually HAPPENS over the next 5 years if you do this? How does the ecology change? What species arrive? What does your land become?"

**[0:30-1:00] The Product**
"Rewild is a consumer ecological scenario engine. Enter your zip code and describe your site. Pick interventions you're considering. And see — for the first time — what your land is likely to become over 1 to 5 years."

**[1:00-2:15] Live Demo**
- Enter a real zip code (e.g., 75201 Dallas, TX)
- Walk through site profile
- Select two interventions: "Native wildflower meadow" vs "Stop mowing + leave the leaves"
- Show the trajectory dashboard side by side
- Highlight: "Look — the meadow attracts specialist pollinators faster, but the stop-mowing approach has lower effort and still reaches good biodiversity by Year 4"
- Show confidence bands: "These ranges are honest — we tell you what we're confident about and what would reduce uncertainty"
- Show the food web animation growing over time (the "wow" moment)
- Show the action plan with month-by-month calendar

**[2:15-2:45] Technical Depth**
"Under the hood, Rewild combines a deterministic rules engine with LLM ecological reasoning. We embed data from the USDA PLANTS database, the Database of Pollinator Interactions, and GBIF species occurrence data. Uncertainty propagation ensures we never overclaim. And calibration hooks let users report observations that improve projections over time."

**[2:45-3:00] Vision**
"Existing tools tell you what to plant. Rewild shows you what your land becomes. And it's honest about what it doesn't know."

---

## Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| **Overclaiming precision** | CRITICAL | Uncertainty-first design; explicit caveats everywhere; ranges not points |
| LLM hallucinating species/interactions | High | Constrain to pre-embedded data where possible; LLM reasons over structured data, not from scratch |
| Demo breaks with unusual zip codes | Medium | Pre-test 10 diverse zips; graceful fallback for unknown ecoregions |
| Judges find it "not technical enough" | Low | Food web visualization + multi-layer architecture + structured uncertainty shows depth |
| "Just a wrapper around Claude" perception | Medium | Emphasize the deterministic rules layer, embedded data, and hybrid architecture |

---

## Expansion Roadmap (Post-Hackathon, for Devpost "Future Scope" Section)

1. **More habitat classes**: Woodland, wetland, urban balcony, schoolyard, farm edge
2. **Global coverage**: UK, EU, Australia (leveraging GBIF's global data)
3. **Photo-based site assessment**: Computer vision to estimate current plant cover, canopy, soil exposure
4. **Community layer**: "See what other Rewild users in your ecoregion are growing and observing"
5. **Calibration flywheel**: User observations training improved regional models over time
6. **Partner integrations**: Native plant nursery sourcing, local conservation organizations, school STEM curricula
7. **Municipal/HOA version**: "What if our entire neighborhood rewilded 20% of lawn area?"

---

## Key Messaging for Judges

**If asked "How is this different from a gardening app?"**
→ "Gardening apps help you choose plants. We simulate ecological outcomes over time. The question we answer isn't 'what should I plant' — it's 'what will my land become?'"

**If asked "How accurate is this?"**
→ "We're uncertainty-first by design. Every output shows confidence bands and tells users what would reduce uncertainty. We're a scenario comparison tool, not a precision forecast — and we're transparent about that."

**If asked "What's the technical complexity?"**
→ "Three-layer hybrid engine: deterministic rules for known ecology (bloom timing, zone logic), LLM reasoning for complex dynamics (succession, food web emergence), and uncertainty propagation that widens bands where data is sparse. Plus we embed 320,000+ plant-pollinator interaction records from peer-reviewed databases."

**If asked "Who uses this?"**
→ "Three audiences: homeowners in the native gardening movement (fastest-growing segment in residential gardening), K-12 schools needing hands-on STEM ecology tools, and municipal planners exploring residential rewilding programs."
