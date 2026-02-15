"""Bloom calendar generator for REWILD scenario engine."""
from app.data.native_plants import get_native_plants

_MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def generate_bloom_calendar(
    ecoregion: str,
    sun: str | None = None,
    soil: str | None = None,
) -> dict:
    """Generate month-by-month bloom calendar for a site.
    
    Returns: {month_name: [{plant_name, scientific_name, intensity}]}
    """
    plants = get_native_plants(ecoregion, sun=sun, soil=soil)
    
    calendar: dict[str, list] = {m: [] for m in _MONTHS}

    if not plants:
        return {
            "calendar": calendar,
            "peak_months": [],
            "total_species": 0,
            "bloom_gap_months": [],
            "no_matching_species": True,
            "note": "No species matched the current site filters for this ecoregion.",
        }
    
    for plant in plants:
        bloom_nums = plant.get("bloom_month_nums", [])
        for m_num in bloom_nums:
            if 1 <= m_num <= 12:
                month_name = _MONTHS[m_num - 1]
                # Intensity: peak months are mid-range, edges are lower
                if len(bloom_nums) <= 2:
                    intensity = "high"
                elif m_num == bloom_nums[0] or m_num == bloom_nums[-1]:
                    intensity = "low"
                else:
                    intensity = "high" if m_num in bloom_nums[1:-1] else "medium"
                
                calendar[month_name].append({
                    "plant": plant["common_name"],
                    "scientific_name": plant["scientific_name"],
                    "intensity": intensity,
                    "value": plant["ecological_value"],
                })
    
    # Add summary stats
    summary = {
        "calendar": calendar,
        "peak_months": sorted(
            [(m, len(ps)) for m, ps in calendar.items()],
            key=lambda x: -x[1]
        )[:3],
        "total_species": len(plants),
        "bloom_gap_months": [m for m, ps in calendar.items() if len(ps) == 0],
        "no_matching_species": False,
        "note": "",
    }
    
    return summary
