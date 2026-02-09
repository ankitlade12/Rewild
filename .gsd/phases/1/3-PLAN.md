---
phase: 1
plan: 3
wave: 2
---

# Plan 1.3: Frontend — Site Profile Wizard & Intervention Selection

## Objective
Build the first two screens of the user flow: the 3-step Site Profile Wizard and the Intervention Comparison Panel. This is what users interact with first.

## Context
- .gsd/SPEC.md (Screen 1 & 2 specs)
- .gsd/phases/1/2-PLAN.md (API endpoints this consumes)
- frontend/src/App.jsx
- frontend/src/index.css

## Tasks

<task type="auto">
  <name>Install frontend dependencies and set up design system</name>
  <files>frontend/package.json, frontend/src/index.css, frontend/vite.config.js</files>
  <action>
    Install dependencies:
    - recharts (for future trajectory charts)
    - d3 (for future food web animation)
    - Add Google Font: Inter
    
    Set up CSS design system in index.css:
    - CSS custom properties for color palette (earthy greens, warm golds, soft grays)
    - Dark mode support
    - Typography scale using Inter
    - Glassmorphism card styles
    - Smooth transition/animation utilities
    - Responsive breakpoints
    
    Configure vite.config.js with proxy to backend (localhost:8000)
    
    - Use vanilla CSS, NOT Tailwind
    - Design should feel premium, nature-inspired, modern
  </action>
  <verify>cd frontend && npm run build 2>&1 | tail -5</verify>
  <done>Frontend builds successfully with all dependencies and design system</done>
</task>

<task type="auto">
  <name>Build Site Profile Wizard (3-step progressive form)</name>
  <files>frontend/src/components/SiteProfileWizard.jsx, frontend/src/components/SiteProfileWizard.css</files>
  <action>
    Create a 3-step progressive disclosure wizard:
    
    Step 1 — Location:
    - Zip code input with auto-lookup (calls /api/lookup/{zip})
    - On valid zip: show ecoregion name, hardiness zone, frost dates
    - Animated confirmation: "We've identified your ecoregion as [X]"
    
    Step 2 — Your Site:
    - Area size slider (100 sq ft → 5000+ sq ft)
    - Current state radio: Maintained lawn | Weedy/neglected | Partial garden | Bare soil
    - Sun exposure radio: Full sun (6+ hrs) | Partial shade (3-6 hrs) | Full shade (<3 hrs)
    - Soil dropdown: Well-drained | Clay-heavy | Sandy | Don't know
    
    Step 3 — Your Goals (multi-select with icons):
    - 🦋 Attract pollinators
    - 🐦 Support bird habitat
    - 💧 Improve water management
    - 🌍 Maximize carbon capture
    - 🎓 Educational / school project
    - 🌸 Beautiful AND ecological
    
    Each step has smooth slide-in animation.
    Progress indicator at top (step 1/2/3).
    "Continue" button advances, "Back" button returns.
    Final step → "Compare Interventions" button.
    
    - All state managed with useState/useReducer
    - Must be responsive (mobile-friendly)
    - Premium, nature-inspired aesthetics
  </action>
  <verify>cd frontend && npm run dev & sleep 3 && curl -s http://localhost:5173 | head -20 && kill %1</verify>
  <done>3-step wizard renders with all fields, validates zip code via backend, stores profile state</done>
</task>

<task type="auto">
  <name>Build Intervention Comparison Panel</name>
  <files>frontend/src/components/InterventionPanel.jsx, frontend/src/components/InterventionPanel.css</files>
  <action>
    Create screen that appears after wizard completion:
    
    - Fetch interventions from /api/interventions
    - Display 8 intervention cards in a grid (2x4 or responsive)
    - Each card shows: icon, name, description, effort level badge
    - User can select 1-3 interventions (checkbox/toggle style)
    - Selected cards get highlighted border + glow effect
    - Show count: "2 of 3 selected"
    - Disabled selection when 3 already chosen (with tooltip)
    - "Generate Trajectories" button (enabled when ≥1 selected)
    
    - Cards should have hover animations (subtle lift + shadow)
    - Effort level badges color-coded (green=Very Low, yellow=Low, orange=Medium, red=High)
    - Premium card design with glassmorphism effect
  </action>
  <verify>cd frontend && npm run build 2>&1 | tail -5</verify>
  <done>Intervention panel displays all 8 options, user can select 1-3, navigates to trajectory view</done>
</task>

## Success Criteria
- [ ] Frontend builds and runs without errors
- [ ] Wizard step 1 calls backend and shows ecoregion info
- [ ] Wizard completes all 3 steps with smooth transitions
- [ ] Intervention panel shows 8 cards with correct data
- [ ] User can select 1-3 interventions
- [ ] Mobile responsive layout works
- [ ] Design feels premium and nature-inspired
