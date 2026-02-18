"""
Deterministic succession timeline model for REWILD.

Models ecological metrics over 5 years using logistic growth curves,
per-metric modifier weights, soil-type cross-effects, and multi-intervention
synergy scoring.
"""
import math
from app.data.usda_zones import get_zone
from app.data.ecoregions import get_ecoregion
from app.data.native_plants import get_native_plants
from app.data.pollinators import get_pollinators

# ---------------------------------------------------------------------------
# Metric index constants
# ---------------------------------------------------------------------------
POLLINATOR = 0
BIRD = 1
FOOD_WEB = 2
SERVICES = 3

_METRICS = [
    "pollinator_diversity_index",
    "bird_activity_score",
    "food_web_complexity",
    "ecosystem_services_score",
]

# ---------------------------------------------------------------------------
# Base trajectories per intervention: (pollinator, bird, food_web, services)
# Values are for "likely" scenario on maintained_lawn, full sun, zone 7,
# Eastern Temperate Forests, well-drained soil.
# ---------------------------------------------------------------------------
_BASE = {
    "native_meadow": [
        (0.05, 0.05, 0.03, 0.05),
        (0.20, 0.10, 0.12, 0.15),
        (0.40, 0.22, 0.28, 0.30),
        (0.58, 0.35, 0.42, 0.45),
        (0.68, 0.45, 0.52, 0.55),
        (0.75, 0.52, 0.60, 0.62),
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

# ---------------------------------------------------------------------------
# Modifiers by current site state
# ---------------------------------------------------------------------------
_STATE_MOD = {
    "maintained_lawn": 1.0,
    "weedy": 1.15,
    "partial_garden": 1.25,
    "bare_soil": 0.85,
}

# ---------------------------------------------------------------------------
# Ecoregion speed modifiers
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Per-metric modifier exponents: how strongly each factor influences each
# metric.  Values >1.0 amplify the factor, <1.0 dampen it.
#   Order: [pollinator, bird, food_web, services]
# ---------------------------------------------------------------------------
_AREA_WEIGHT = [0.8, 1.4, 1.0, 1.2]   # Birds care more about area
_SUN_WEIGHT = [1.3, 0.8, 1.0, 0.9]    # Pollinators care more about sun
_SOIL_WEIGHT = [0.9, 0.7, 0.8, 1.4]   # Services care more about soil

# ---------------------------------------------------------------------------
# Soil-type modifiers per intervention (row=soil, col=intervention).
# Captures how soil type interacts with each intervention differently.
#   Order: (pollinator, bird, food_web, services) multiplier
# ---------------------------------------------------------------------------
_SOIL_MOD: dict[str, dict[str, tuple[float, float, float, float]]] = {
    "well_drained": {
        "native_meadow":      (1.00, 1.00, 1.00, 1.00),
        "rain_garden":        (0.90, 0.90, 0.90, 0.85),
        "shrub_border":       (1.00, 1.00, 1.00, 1.00),
        "stop_mowing":        (1.00, 1.00, 1.00, 1.00),
        "habitat_structures": (1.00, 1.00, 1.00, 1.00),
        "pollinator_nesting": (1.00, 1.00, 1.00, 1.00),
        "leave_leaves":       (1.00, 1.00, 1.00, 1.00),
        "native_grass":       (1.00, 1.00, 1.00, 1.00),
    },
    "clay": {
        "native_meadow":      (0.88, 0.90, 0.85, 0.90),
        "rain_garden":        (1.10, 1.05, 1.08, 1.15),
        "shrub_border":       (0.92, 0.95, 0.90, 0.92),
        "stop_mowing":        (0.90, 0.92, 0.88, 0.90),
        "habitat_structures": (1.00, 1.00, 0.95, 0.95),
        "pollinator_nesting": (0.95, 0.95, 0.92, 0.95),
        "leave_leaves":       (1.05, 1.02, 1.00, 1.08),
        "native_grass":       (0.85, 0.90, 0.85, 0.92),
    },
    "sandy": {
        "native_meadow":      (0.92, 0.90, 0.88, 0.85),
        "rain_garden":        (0.82, 0.85, 0.80, 0.78),
        "shrub_border":       (0.90, 0.88, 0.85, 0.85),
        "stop_mowing":        (0.95, 0.95, 0.90, 0.88),
        "habitat_structures": (1.00, 1.00, 0.95, 0.90),
        "pollinator_nesting": (1.05, 1.00, 1.00, 0.95),
        "leave_leaves":       (0.95, 0.95, 0.92, 0.90),
        "native_grass":       (0.95, 0.92, 0.90, 0.88),
    },
    "unknown": {
        "native_meadow":      (1.00, 1.00, 1.00, 1.00),
        "rain_garden":        (1.00, 1.00, 1.00, 1.00),
        "shrub_border":       (1.00, 1.00, 1.00, 1.00),
        "stop_mowing":        (1.00, 1.00, 1.00, 1.00),
        "habitat_structures": (1.00, 1.00, 1.00, 1.00),
        "pollinator_nesting": (1.00, 1.00, 1.00, 1.00),
        "leave_leaves":       (1.00, 1.00, 1.00, 1.00),
        "native_grass":       (1.00, 1.00, 1.00, 1.00),
    },
}

# ---------------------------------------------------------------------------
# Multi-intervention synergy matrix.
# Key = frozenset of two intervention IDs → per-metric synergy coefficient.
# A coefficient of 1.20 means a 20% boost when both are combined.
# ---------------------------------------------------------------------------
_SYNERGY: dict[frozenset[str], tuple[float, float, float, float]] = {
    frozenset({"native_meadow", "pollinator_nesting"}): (1.25, 1.05, 1.18, 1.08),
    frozenset({"native_meadow", "habitat_structures"}): (1.10, 1.20, 1.15, 1.12),
    frozenset({"native_meadow", "leave_leaves"}):       (1.12, 1.10, 1.15, 1.18),
    frozenset({"native_meadow", "shrub_border"}):       (1.15, 1.18, 1.15, 1.12),
    frozenset({"native_meadow", "rain_garden"}):        (1.10, 1.08, 1.12, 1.15),
    frozenset({"native_meadow", "native_grass"}):       (1.08, 1.05, 1.10, 1.15),
    frozenset({"shrub_border", "habitat_structures"}):  (1.08, 1.22, 1.15, 1.10),
    frozenset({"shrub_border", "leave_leaves"}):        (1.08, 1.15, 1.12, 1.18),
    frozenset({"shrub_border", "pollinator_nesting"}):  (1.12, 1.10, 1.10, 1.05),
    frozenset({"rain_garden", "leave_leaves"}):         (1.08, 1.05, 1.10, 1.20),
    frozenset({"rain_garden", "native_grass"}):         (1.05, 1.05, 1.08, 1.18),
    frozenset({"rain_garden", "habitat_structures"}):   (1.05, 1.12, 1.10, 1.15),
    frozenset({"stop_mowing", "leave_leaves"}):         (1.10, 1.12, 1.10, 1.15),
    frozenset({"stop_mowing", "habitat_structures"}):   (1.08, 1.15, 1.12, 1.08),
    frozenset({"pollinator_nesting", "leave_leaves"}):  (1.15, 1.05, 1.12, 1.10),
    frozenset({"pollinator_nesting", "habitat_structures"}): (1.18, 1.15, 1.15, 1.08),
    frozenset({"native_grass", "leave_leaves"}):        (1.05, 1.08, 1.08, 1.18),
    frozenset({"native_grass", "habitat_structures"}):  (1.05, 1.15, 1.10, 1.10),
}


def _clamp(v: float) -> float:
    """Clamp a value to the [0.0, 1.0] range, rounded to 3 decimals."""
    return max(0.0, min(1.0, round(v, 3)))


def _logistic_scale(base_value: float, modifier: float) -> float:
    """Apply a modifier using a logistic (sigmoid) curve.

    Unlike linear multiplication, this naturally compresses near 1.0,
    preventing unrealistic scores from stacked modifiers:

        v' = (v * m) / (v * m + (1 - v))

    When base_value is 0 the result is 0 regardless of modifier.
    """
    vm = base_value * modifier
    denominator = vm + (1.0 - base_value)
    if denominator <= 0:
        return 0.0
    return vm / denominator


def compute_synergy(interventions: list[str]) -> tuple[float, float, float, float]:
    """Compute aggregate synergy coefficient for a set of interventions.

    Examines all pairwise combinations in the selected interventions and
    multiplies their synergy coefficients.  Interventions with no known
    synergy contribute a neutral 1.0.

    Returns:
        4-tuple of per-metric synergy multipliers (pollinator, bird,
        food_web, services).
    """
    result = [1.0, 1.0, 1.0, 1.0]
    seen: set[frozenset[str]] = set()

    for i, a in enumerate(interventions):
        for b in interventions[i + 1:]:
            pair = frozenset({a, b})
            if pair in seen:
                continue
            seen.add(pair)
            coeffs = _SYNERGY.get(pair, (1.0, 1.0, 1.0, 1.0))
            for k in range(4):
                result[k] *= coeffs[k]

    return (result[0], result[1], result[2], result[3])


def simulate_trajectory(
    zip_code: str,
    intervention: str,
    area_sqft: int,
    current_state: str,
    sun: str,
    soil: str,
    synergy: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
) -> dict:
    """Simulate a 5-year ecological trajectory for a given intervention.

    Uses logistic growth curves with per-metric modifier weights, soil-type
    cross-effects, and optional multi-intervention synergy coefficients.

    Args:
        zip_code: 5-digit US zip code.
        intervention: Intervention ID (e.g. ``"native_meadow"``).
        area_sqft: Site area in square feet.
        current_state: Current site state (e.g. ``"maintained_lawn"``).
        sun: Sun exposure (``"full"`` | ``"partial"`` | ``"shade"``).
        soil: Soil type (``"well_drained"`` | ``"clay"`` | ``"sandy"`` |
              ``"unknown"``).
        synergy: Per-metric synergy multipliers from ``compute_synergy()``.

    Returns:
        Trajectory dict with ``years`` list (Y0–Y5) and site metadata.
    """
    zone_data = get_zone(zip_code)
    eco_data = get_ecoregion(zip_code)
    ecoregion = eco_data.get("ecoregion", "Eastern Temperate Forests")

    base = _BASE.get(intervention, _BASE["native_meadow"])
    state_mod = _STATE_MOD.get(current_state, 1.0)
    eco_speed = _ECO_SPEED.get(ecoregion, 1.0)

    # Area bonus: larger areas are slightly more effective (log-scaled)
    area_raw = 1.0 + math.log10(max(area_sqft, 100) / 500) * 0.1

    # Sun/shade penalty
    sun_raw = {"full": 1.0, "partial": 0.85, "shade": 0.65}.get(sun, 1.0)

    # Soil-type × intervention cross-effect (per-metric)
    soil_mods = _SOIL_MOD.get(soil, _SOIL_MOD["unknown"]).get(
        intervention, (1.0, 1.0, 1.0, 1.0)
    )

    years = []
    for y in range(6):
        raw = base[y]
        vals = []
        for metric_idx in range(4):
            # Per-metric weighted modifiers
            area_mod = area_raw ** _AREA_WEIGHT[metric_idx]
            sun_mod = sun_raw ** _SUN_WEIGHT[metric_idx]

            composite_mod = (
                state_mod
                * eco_speed
                * area_mod
                * sun_mod
                * soil_mods[metric_idx]
                * synergy[metric_idx]
            )

            # Logistic scaling prevents runaway values near 1.0
            scaled = _logistic_scale(raw[metric_idx], composite_mod)
            vals.append(_clamp(scaled))

        years.append({
            "year": y,
            _METRICS[0]: vals[POLLINATOR],
            _METRICS[1]: vals[BIRD],
            _METRICS[2]: vals[FOOD_WEB],
            _METRICS[3]: vals[SERVICES],
        })

    return {
        "intervention": intervention,
        "zip_code": zip_code,
        "zone": zone_data.get("zone", "Unknown"),
        "ecoregion": ecoregion,
        "years": years,
    }
