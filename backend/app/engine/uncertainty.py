"""Uncertainty propagation layer for REWILD scenario engine."""

# Ecoregion study confidence (well-studied = tighter bands)
_ECO_CONFIDENCE = {
    "Eastern Temperate Forests": 0.80,
    "Southeastern Plains": 0.75,
    "Mediterranean California": 0.78,
    "Great Plains": 0.72,
    "Central USA Plains": 0.76,
    "Pacific Northwest Forests": 0.74,
    "Northern Forests": 0.70,
    "Ozark/Ouachita Highlands": 0.68,
    "Gulf Coast Plains": 0.72,
    "Western Mountains": 0.65,
    "North American Deserts": 0.60,
    "Tropical/Subtropical Florida": 0.70,
}

# Intervention confidence (well-documented = tighter bands)
_INTERVENTION_CONFIDENCE = {
    "native_meadow": 0.80,
    "rain_garden": 0.75,
    "shrub_border": 0.70,
    "pollinator_nesting": 0.72,
    "stop_mowing": 0.60,  # Less studied
    "leave_leaves": 0.55,
    "habitat_structures": 0.65,
    "native_grass": 0.68,
}


def apply_uncertainty(
    base_value: float,
    year: int,
    ecoregion: str,
    intervention: str,
    soil_known: bool = True,
) -> dict:
    """Wrap a metric value in uncertainty bands."""
    eco_conf = _ECO_CONFIDENCE.get(ecoregion, 0.65)
    intv_conf = _INTERVENTION_CONFIDENCE.get(intervention, 0.65)

    # Time decay: uncertainty grows with years
    time_factor = 1.0 - (year * 0.06)  # Lose 6% confidence per year

    # Soil knowledge bonus
    soil_factor = 1.0 if soil_known else 0.85

    # Composite confidence
    confidence = eco_conf * intv_conf * time_factor * soil_factor * 100
    confidence = max(20, min(95, round(confidence)))

    # Band width inversely proportional to confidence
    band_width = (100 - confidence) / 100 * 0.4  # Max ±0.2 at low confidence

    optimistic = min(1.0, round(base_value + band_width * 0.6, 3))
    conservative = max(0.0, round(base_value - band_width * 0.4, 3))

    return {
        "optimistic": optimistic,
        "likely": round(base_value, 3),
        "conservative": conservative,
        "confidence": confidence,
    }


def wrap_trajectory_with_uncertainty(
    trajectory: dict,
    intervention: str,
    soil_known: bool = True,
) -> dict:
    """Add uncertainty bands to an entire trajectory."""
    ecoregion = trajectory.get("ecoregion", "Eastern Temperate Forests")
    metrics = ["pollinator_diversity_index", "bird_activity_score",
               "food_web_complexity", "ecosystem_services_score"]

    enriched_years = []
    for year_data in trajectory["years"]:
        year = year_data["year"]
        enriched = {"year": year}
        for metric in metrics:
            base = year_data[metric]
            enriched[metric] = apply_uncertainty(
                base, year, ecoregion, intervention, soil_known
            )
        enriched_years.append(enriched)

    # Generate uncertainty reducers
    reducers = _get_uncertainty_reducers(
        intervention, ecoregion, soil_known
    )

    return {
        **trajectory,
        "years": enriched_years,
        "uncertainty_reducers": reducers,
    }


def _get_uncertainty_reducers(
    intervention: str,
    ecoregion: str,
    soil_known: bool,
) -> list[dict]:
    """Generate actionable suggestions to reduce uncertainty."""
    reducers = []

    if not soil_known:
        reducers.append({
            "action": "Get a soil test",
            "impact": "Narrows plant survival predictions by ~15%",
            "effort": "Low",
            "icon": "🧪",
        })

    eco_conf = _ECO_CONFIDENCE.get(ecoregion, 0.65)
    if eco_conf < 0.70:
        reducers.append({
            "action": "Contact local native plant society",
            "impact": "Region-specific advice tightens predictions by ~10%",
            "effort": "Low",
            "icon": "🌿",
        })

    intv_conf = _INTERVENTION_CONFIDENCE.get(intervention, 0.65)
    if intv_conf < 0.70:
        reducers.append({
            "action": "Start with a small test plot",
            "impact": "Year 1 observations will calibrate Year 2-5 predictions",
            "effort": "Medium",
            "icon": "📐",
        })

    reducers.append({
        "action": "Log seasonal observations",
        "impact": "Each observation tightens future year predictions by ~5%",
        "effort": "Low",
        "icon": "📝",
    })

    reducers.append({
        "action": "Photograph monthly for species ID",
        "impact": "Photo records enable model recalibration over time",
        "effort": "Low",
        "icon": "📸",
    })

    return reducers
