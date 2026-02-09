"""
Deterministic succession timeline model for REWILD.
Models ecological metrics over 5 years based on rules, intervention, and site context.
"""
import math
from app.data.usda_zones import get_zone
from app.data.ecoregions import get_ecoregion
from app.data.native_plants import get_native_plants
from app.data.pollinators import get_pollinators

# Base trajectories per intervention: (pollinator, bird, food_web, services) at each year
# Values are for "likely" scenario on maintained_lawn, full sun, zone 7, temperate forest
_BASE = {
    "native_meadow": [
        (0.05, 0.05, 0.03, 0.05),  # Y0
        (0.20, 0.10, 0.12, 0.15),  # Y1
        (0.40, 0.22, 0.28, 0.30),  # Y2
        (0.58, 0.35, 0.42, 0.45),  # Y3
        (0.68, 0.45, 0.52, 0.55),  # Y4
        (0.75, 0.52, 0.60, 0.62),  # Y5
    ],
    "shrub_border": [
        (0.05, 0.05, 0.03, 0.05),
        (0.10, 0.08, 0.06, 0.10),
        (0.18, 0.15, 0.12, 0.18),
        (0.28, 0.28, 0.22, 0.30),
        (0.42, 0.45, 0.38, 0.45),
        (0.55, 0.58, 0.50, 0.55),
    ],
    "rain_garden": [
        (0.05, 0.05, 0.03, 0.10),
        (0.18, 0.12, 0.10, 0.35),
        (0.32, 0.22, 0.22, 0.50),
        (0.45, 0.30, 0.35, 0.60),
        (0.52, 0.38, 0.42, 0.68),
        (0.58, 0.42, 0.48, 0.72),
    ],
    "stop_mowing": [
        (0.05, 0.05, 0.03, 0.05),
        (0.08, 0.06, 0.05, 0.08),
        (0.15, 0.10, 0.10, 0.15),
        (0.25, 0.18, 0.18, 0.25),
        (0.35, 0.28, 0.28, 0.35),
        (0.45, 0.35, 0.38, 0.42),
    ],
    "habitat_structures": [
        (0.05, 0.05, 0.03, 0.05),
        (0.15, 0.18, 0.12, 0.10),
        (0.25, 0.30, 0.22, 0.18),
        (0.32, 0.38, 0.30, 0.25),
        (0.38, 0.45, 0.35, 0.30),
        (0.42, 0.50, 0.40, 0.35),
    ],
    "pollinator_nesting": [
        (0.05, 0.05, 0.03, 0.05),
        (0.25, 0.08, 0.15, 0.08),
        (0.35, 0.12, 0.22, 0.12),
        (0.42, 0.15, 0.28, 0.15),
        (0.48, 0.18, 0.32, 0.18),
        (0.50, 0.20, 0.35, 0.20),
    ],
    "leave_leaves": [
        (0.05, 0.05, 0.03, 0.05),
        (0.10, 0.10, 0.08, 0.12),
        (0.18, 0.18, 0.15, 0.22),
        (0.25, 0.25, 0.22, 0.32),
        (0.32, 0.30, 0.28, 0.40),
        (0.38, 0.35, 0.32, 0.45),
    ],
    "native_grass": [
        (0.05, 0.05, 0.03, 0.05),
        (0.12, 0.08, 0.08, 0.15),
        (0.25, 0.15, 0.18, 0.28),
        (0.38, 0.25, 0.28, 0.40),
        (0.48, 0.32, 0.38, 0.50),
        (0.55, 0.38, 0.45, 0.58),
    ],
}

# Modifiers by current site state (multiplied)
_STATE_MOD = {
    "maintained_lawn": 1.0,
    "weedy": 1.15,       # Already has some ecological value
    "partial_garden": 1.25,
    "bare_soil": 0.85,    # Starts from nothing
}

# Ecoregion speed modifiers (some ecosystems respond faster)
_ECO_SPEED = {
    "Tropical/Subtropical Florida": 1.3,
    "Gulf Coast Plains": 1.2,
    "Southeastern Plains": 1.15,
    "Mediterranean California": 0.95,
    "Eastern Temperate Forests": 1.0,
    "Central USA Plains": 1.0,
    "Ozark/Ouachita Highlands": 1.0,
    "Great Plains": 0.95,
    "Pacific Northwest Forests": 1.1,
    "Northern Forests": 0.85,
    "Western Mountains": 0.80,
    "North American Deserts": 0.70,
}

_METRICS = ["pollinator_diversity_index", "bird_activity_score", "food_web_complexity", "ecosystem_services_score"]


def _clamp(v: float) -> float:
    return max(0.0, min(1.0, round(v, 3)))


def simulate_trajectory(
    zip_code: str,
    intervention: str,
    area_sqft: int,
    current_state: str,
    sun: str,
    soil: str,
) -> dict:
    """Simulate a 5-year ecological trajectory for a given intervention."""
    zone_data = get_zone(zip_code)
    eco_data = get_ecoregion(zip_code)
    ecoregion = eco_data.get("ecoregion", "Eastern Temperate Forests")

    base = _BASE.get(intervention, _BASE["native_meadow"])
    state_mod = _STATE_MOD.get(current_state, 1.0)
    eco_speed = _ECO_SPEED.get(ecoregion, 1.0)

    # Area bonus: larger areas are slightly more effective
    area_mod = 1.0 + math.log10(max(area_sqft, 100) / 500) * 0.1

    # Sun/shade penalty
    sun_mod = {"full": 1.0, "partial": 0.85, "shade": 0.65}.get(sun, 1.0)

    years = []
    for y in range(6):
        p, b, f, s = base[y]
        mod = state_mod * eco_speed * area_mod * sun_mod

        # Apply modifier (diminishing at high values to keep 0-1 bounded)
        vals = [_clamp(v * mod) for v in (p, b, f, s)]
        years.append({
            "year": y,
            _METRICS[0]: vals[0],
            _METRICS[1]: vals[1],
            _METRICS[2]: vals[2],
            _METRICS[3]: vals[3],
        })

    return {
        "intervention": intervention,
        "zip_code": zip_code,
        "zone": zone_data.get("zone", "Unknown"),
        "ecoregion": ecoregion,
        "years": years,
    }
