"""Bloom calendar generator for REWILD scenario engine.

Provides:
- Month-by-month bloom calendar from native plant data.
- **Bloom continuity score** (0–1): measures how evenly bloom coverage
  is distributed across the growing season.
- **Succession-aware projections**: year-by-year bloom calendars that
  model which species establish in each successional year.
- **Gap-filling recommendations**: suggests plant additions to fill
  months with no or low bloom coverage.
"""

from __future__ import annotations

import math
from app.data.native_plants import get_native_plants

MONTHS: list[str] = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

# ---------------------------------------------------------------------------
# Succession-awareness: fraction of species pool established by each year.
# Fast-establishing forbs arrive early; slow shrubs/trees arrive later.
# Values are tuples of (forb_fraction, shrub_fraction) by successional year.
# Height ≤ 3 ft → forb, > 3 ft → shrub.
# ---------------------------------------------------------------------------
_FORB_HEIGHT_THRESHOLD_FT = 3.0

_ESTABLISHMENT_RATE: list[tuple[float, float]] = [
    (0.15, 0.05),  # Y0: just planted, very few blooming
    (0.40, 0.15),  # Y1: forbs establishing
    (0.65, 0.35),  # Y2: good forb coverage, some shrubs
    (0.85, 0.55),  # Y3: mature forbs, shrubs growing
    (0.95, 0.75),  # Y4: near-full forb coverage
    (1.00, 0.90),  # Y5: full establishment
]


def _bloom_intensity(bloom_month: int, bloom_nums: list[int]) -> str:
    """Classify bloom intensity for a given month within a species' bloom range.

    Args:
        bloom_month: Month number (1–12) being evaluated.
        bloom_nums: Sorted list of all bloom months for the species.

    Returns:
        ``"high"`` for peak months, ``"low"`` for edge months,
        ``"medium"`` otherwise.
    """
    if len(bloom_nums) <= 2:
        return "high"
    if bloom_month == bloom_nums[0] or bloom_month == bloom_nums[-1]:
        return "low"
    return "high" if bloom_month in bloom_nums[1:-1] else "medium"


def _build_calendar(plants: list[dict]) -> dict[str, list[dict]]:
    """Build a month-keyed calendar from a list of plant dicts.

    Args:
        plants: Expanded plant dicts (from ``get_native_plants``).

    Returns:
        Dict mapping month name → list of plant bloom entries.
    """
    calendar: dict[str, list[dict]] = {m: [] for m in MONTHS}
    for plant in plants:
        bloom_nums = plant.get("bloom_month_nums", [])
        for m_num in bloom_nums:
            if 1 <= m_num <= 12:
                month_name = MONTHS[m_num - 1]
                calendar[month_name].append({
                    "plant": plant["common_name"],
                    "scientific_name": plant["scientific_name"],
                    "intensity": _bloom_intensity(m_num, bloom_nums),
                    "value": plant["ecological_value"],
                })
    return calendar


def compute_bloom_continuity(calendar: dict[str, list[dict]]) -> float:
    """Compute a bloom continuity score in ``[0.0, 1.0]``.

    Uses a normalised Shannon-entropy metric over the 12 months:

    .. math::

        H = -\\sum_{i=1}^{12} p_i \\, \\ln(p_i)

    where :math:`p_i = c_i / \\sum c_i` and :math:`c_i` is the weighted
    species count in month *i* (``"high"`` = 1.0, ``"medium"`` = 0.6,
    ``"low"`` = 0.3).

    Perfect continuity (equal coverage every month) yields 1.0.  A single
    bloom month yields ~0.0.

    Args:
        calendar: Month-keyed calendar from ``_build_calendar``.

    Returns:
        Continuity score rounded to 3 decimals.
    """
    intensity_weight = {"high": 1.0, "medium": 0.6, "low": 0.3}
    counts: list[float] = []
    for month in MONTHS:
        entries = calendar.get(month, [])
        weighted = sum(intensity_weight.get(e.get("intensity", "high"), 1.0)
                       for e in entries)
        counts.append(weighted)

    total = sum(counts)
    if total == 0:
        return 0.0

    max_entropy = math.log(12)  # ln(12), max when perfectly uniform
    if max_entropy == 0:
        return 0.0

    entropy = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            entropy -= p * math.log(p)

    return round(entropy / max_entropy, 3)


def _gap_filling_recommendations(
    calendar: dict[str, list[dict]],
    all_plants: list[dict],
    current_plant_names: set[str],
) -> list[dict]:
    """Suggest plants that would fill bloom gaps.

    For each gap month (zero blooming species), finds candidate species
    from the full ecoregion pool that bloom in that month and are not
    already selected.

    Args:
        calendar: Current bloom calendar.
        all_plants: Full (unfiltered) plant list for the ecoregion.
        current_plant_names: Names of species already in the calendar.

    Returns:
        List of recommendation dicts with ``month``, ``plant``,
        ``scientific_name``, and ``ecological_value``.
    """
    gap_months = [m for m in MONTHS if len(calendar.get(m, [])) == 0]
    if not gap_months:
        return []

    recommendations: list[dict] = []
    seen: set[str] = set()

    for month in gap_months:
        m_num = MONTHS.index(month) + 1
        for plant in all_plants:
            name = plant["common_name"]
            if name in current_plant_names or name in seen:
                continue
            if m_num in plant.get("bloom_month_nums", []):
                recommendations.append({
                    "month": month,
                    "plant": name,
                    "scientific_name": plant["scientific_name"],
                    "ecological_value": plant["ecological_value"],
                })
                seen.add(name)

    return recommendations


def generate_bloom_calendar(
    ecoregion: str,
    sun: str | None = None,
    soil: str | None = None,
) -> dict:
    """Generate month-by-month bloom calendar for a site.

    Returns a summary dict with the calendar, peak months, gap months,
    a **bloom continuity score**, and gap-filling recommendations.

    Args:
        ecoregion: Ecoregion name (must match ``native_plants`` keys).
        sun: Optional sun filter (``"full"`` | ``"partial"`` | ``"shade"``).
        soil: Optional soil filter (``"well_drained"`` | ``"clay"`` etc.).

    Returns:
        Dict with keys: ``calendar``, ``peak_months``, ``total_species``,
        ``bloom_gap_months``, ``bloom_continuity_score``,
        ``gap_filling_recommendations``, ``no_matching_species``, ``note``.
    """
    plants = get_native_plants(ecoregion, sun=sun, soil=soil)
    empty_calendar: dict[str, list[dict]] = {m: [] for m in MONTHS}

    if not plants:
        return {
            "calendar": empty_calendar,
            "peak_months": [],
            "total_species": 0,
            "bloom_gap_months": list(MONTHS),
            "bloom_continuity_score": 0.0,
            "gap_filling_recommendations": [],
            "no_matching_species": True,
            "note": "No species matched the current site filters for this ecoregion.",
        }

    calendar = _build_calendar(plants)
    continuity = compute_bloom_continuity(calendar)

    # Full (unfiltered) pool for gap recommendations
    all_plants = get_native_plants(ecoregion)
    current_names = {p["common_name"] for p in plants}
    gap_recs = _gap_filling_recommendations(calendar, all_plants, current_names)

    return {
        "calendar": calendar,
        "peak_months": sorted(
            [(m, len(ps)) for m, ps in calendar.items()],
            key=lambda x: -x[1],
        )[:3],
        "total_species": len(plants),
        "bloom_gap_months": [m for m, ps in calendar.items() if len(ps) == 0],
        "bloom_continuity_score": continuity,
        "gap_filling_recommendations": gap_recs,
        "no_matching_species": False,
        "note": "",
    }


def generate_succession_bloom(
    ecoregion: str,
    sun: str | None = None,
    soil: str | None = None,
) -> list[dict]:
    """Generate year-by-year bloom calendars modelling ecological succession.

    In Year 0, only a fraction of species have established.  By Year 5,
    nearly all species are blooming.  Forbs (height ≤ 3 ft) establish
    faster than shrubs/trees.

    Args:
        ecoregion: Ecoregion name.
        sun: Optional sun filter.
        soil: Optional soil filter.

    Returns:
        List of 6 dicts (Y0–Y5), each containing ``year``,
        ``calendar``, ``bloom_continuity_score``,
        ``established_species_count``, and ``total_pool_size``.
    """
    plants = get_native_plants(ecoregion, sun=sun, soil=soil)
    if not plants:
        empty_cal: dict[str, list[dict]] = {m: [] for m in MONTHS}
        return [
            {
                "year": y,
                "calendar": empty_cal,
                "bloom_continuity_score": 0.0,
                "established_species_count": 0,
                "total_pool_size": 0,
            }
            for y in range(6)
        ]

    # Partition species into forbs and shrubs by height
    forbs = [p for p in plants if p.get("height_ft", 1) <= _FORB_HEIGHT_THRESHOLD_FT]
    shrubs = [p for p in plants if p.get("height_ft", 1) > _FORB_HEIGHT_THRESHOLD_FT]

    # Sort within each group: higher ecological value establishes first
    value_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    forbs.sort(key=lambda p: value_order.get(p.get("ecological_value", "medium"), 2))
    shrubs.sort(key=lambda p: value_order.get(p.get("ecological_value", "medium"), 2))

    results: list[dict] = []
    for year in range(6):
        forb_frac, shrub_frac = _ESTABLISHMENT_RATE[year]
        n_forbs = max(1, round(len(forbs) * forb_frac)) if forbs else 0
        n_shrubs = max(0, round(len(shrubs) * shrub_frac)) if shrubs else 0

        established = forbs[:n_forbs] + shrubs[:n_shrubs]
        cal = _build_calendar(established)
        continuity = compute_bloom_continuity(cal)

        results.append({
            "year": year,
            "calendar": cal,
            "bloom_continuity_score": continuity,
            "established_species_count": len(established),
            "total_pool_size": len(plants),
        })

    return results
