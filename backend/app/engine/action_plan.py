"""Action plan generator for REWILD.
Produces month-by-month planting calendars and to-do lists.
"""
from app.data.native_plants import get_native_plants
from app.data.usda_zones import get_zone
from app.data.ecoregions import get_ecoregion

_MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# What NOT to do, grouped by intervention
_DONT_DO = {
    "native_meadow": [
        "Don't use herbicides — they'll kill establishing native plants",
        "Don't mow below 6 inches in the first 2 years",
        "Don't add fertilizer — natives are adapted to lean soils",
        "Don't water after the first growing season (except drought)",
    ],
    "rain_garden": [
        "Don't plant species that need dry soil in the basin",
        "Don't connect downspout directly — use a splash pad",
        "Don't mulch with dyed mulch — use undyed hardwood",
        "Don't compact the soil in the rain garden basin",
    ],
    "stop_mowing": [
        "Don't remove all vegetation if you decide to restart",
        "Don't spray broadleaf herbicide — you'll kill the wildflowers",
        "Don't worry about a 'messy' look in Year 1 — it's normal",
    ],
    "shrub_border": [
        "Don't prune native shrubs into formal shapes",
        "Don't plant too close to the house foundation (3ft min)",
        "Don't remove leaf litter from under shrubs — it's habitat",
    ],
}

# Observation milestones
_MILESTONES = {
    1: [
        {"month": "Apr", "event": "First native seedlings emerging", "icon": "🌱"},
        {"month": "Jun", "event": "First pollinator visitors spotted", "icon": "🐝"},
        {"month": "Sep", "event": "Seed heads forming — leave for birds!", "icon": "🌾"},
    ],
    2: [
        {"month": "Mar", "event": "Returning perennials breaking dormancy", "icon": "🌿"},
        {"month": "May", "event": "Noticeably more butterfly species", "icon": "🦋"},
        {"month": "Jul", "event": "Peak bloom — photograph for records!", "icon": "📸"},
    ],
    3: [
        {"month": "Apr", "event": "Native bees nesting in your site", "icon": "🐝"},
        {"month": "Jun", "event": "First bird nesting activity possible", "icon": "🐦"},
        {"month": "Aug", "event": "Food web visibly complex — insects everywhere", "icon": "🕸️"},
    ],
    5: [
        {"month": "Year-round", "event": "Self-sustaining ecosystem achieved!", "icon": "🎉"},
    ],
}


def generate_action_plan(
    zip_code: str,
    intervention: str,
    area_sqft: int,
    sun: str,
    soil: str,
) -> dict:
    """Generate a comprehensive action plan with planting calendar."""
    zone_data = get_zone(zip_code)
    eco_data = get_ecoregion(zip_code)
    ecoregion = eco_data.get("ecoregion", "Eastern Temperate Forests")
    last_frost = zone_data.get("last_frost", "Apr 1")
    first_frost = zone_data.get("first_frost", "Oct 15")

    plants = get_native_plants(ecoregion, sun=sun, soil=soil)

    # Build planting calendar
    calendar = _build_planting_calendar(plants, last_frost, first_frost, intervention)

    # Prep tasks (before planting)
    prep_tasks = _get_prep_tasks(intervention, area_sqft, soil)

    # Maintenance schedule
    maintenance = _get_maintenance(intervention)

    # Shopping list
    shopping = _build_shopping_list(plants, area_sqft, intervention)

    return {
        "intervention": intervention,
        "ecoregion": ecoregion,
        "zone": zone_data.get("zone"),
        "last_frost": last_frost,
        "first_frost": first_frost,
        "planting_calendar": calendar,
        "prep_tasks": prep_tasks,
        "maintenance": maintenance,
        "shopping_list": shopping,
        "dont_do": _DONT_DO.get(intervention, [
            "Don't use chemicals — they harm the ecosystem you're building",
            "Don't expect instant results — nature takes 2-3 years",
        ]),
        "milestones": _MILESTONES,
        "total_species": len(plants),
    }


def _build_planting_calendar(plants, last_frost, first_frost, intervention):
    """Create month-by-month planting schedule."""
    # Parse frost month
    frost_month_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                       "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    last_frost_label = (last_frost or "").strip().lower()
    frost_free = last_frost_label.startswith("frost-free")
    last_frost_month = None if frost_free else frost_month_map.get(last_frost.split()[0], 4)

    calendar = {}
    for month_num, month_name in enumerate(_MONTHS, 1):
        tasks = []

        if frost_free:
            if month_num in [1, 2]:
                tasks.append({
                    "task": "Frost-free climate: primary planting window for establishing natives",
                    "type": "plant",
                    "icon": "🌿",
                })
            elif month_num in [9, 10]:
                tasks.append({
                    "task": "Frost-free climate: secondary planting window for cool-season establishment",
                    "type": "plant",
                    "icon": "🌱",
                })
        else:
            if month_num == last_frost_month - 1:
                tasks.append({"task": "Start seeds indoors for early bloomers", "type": "seed", "icon": "🌱"})
            elif month_num == last_frost_month:
                tasks.append({"task": "Last frost — start hardening off seedlings", "type": "prep", "icon": "❄️"})
            elif month_num == last_frost_month + 1:
                # Main planting month
                early = [p for p in plants if any(b <= 6 for b in p.get("bloom_month_nums", []))]
                tasks.append({
                    "task": f"Plant early bloomers: {', '.join(p['common_name'] for p in early[:4])}",
                    "type": "plant", "icon": "🌿",
                    "species": [p["common_name"] for p in early[:4]],
                })
            elif month_num == last_frost_month + 2:
                mid = [p for p in plants if any(6 <= b <= 8 for b in p.get("bloom_month_nums", []))]
                tasks.append({
                    "task": f"Plant summer bloomers: {', '.join(p['common_name'] for p in mid[:4])}",
                    "type": "plant", "icon": "🌸",
                    "species": [p["common_name"] for p in mid[:4]],
                })
            elif month_num == last_frost_month + 3:
                late = [p for p in plants if any(b >= 8 for b in p.get("bloom_month_nums", []))]
                tasks.append({
                    "task": f"Plant late-season species: {', '.join(p['common_name'] for p in late[:3])}",
                    "type": "plant", "icon": "🌻",
                    "species": [p["common_name"] for p in late[:3]],
                })

        if 5 <= month_num <= 9:
            tasks.append({"task": "Water new plantings if no rain for 7+ days", "type": "care", "icon": "💧"})
        if month_num in [6, 7, 8]:
            tasks.append({"task": "Log pollinator observations", "type": "observe", "icon": "📝"})
        if month_num == 10:
            tasks.append({"task": "Leave seed heads standing for winter birds", "type": "care", "icon": "🐦"})
        if month_num == 11:
            tasks.append({"task": "Leave leaf litter in place — overwintering habitat!", "type": "care", "icon": "🍂"})
        if month_num in [12, 1, 2]:
            tasks.append({"task": "Plan next season's additions", "type": "plan", "icon": "📋"})

        calendar[month_name] = tasks

    return calendar


def _get_prep_tasks(intervention, area_sqft, soil):
    """Pre-planting preparation tasks."""
    tasks = [
        {"task": "Mark out your site boundaries with stakes or string", "week": 1, "icon": "📐"},
        {"task": f"Measure and confirm area (~{area_sqft} sq ft)", "week": 1, "icon": "📏"},
    ]
    if intervention == "native_meadow":
        tasks += [
            {"task": "Smother existing lawn with cardboard + 4\" mulch (sheet mulching)", "week": 2, "icon": "📦"},
            {"task": "Wait 4-6 weeks for lawn to die back", "week": 3, "icon": "⏳"},
            {"task": "Remove cardboard, rake soil smooth", "week": 8, "icon": "🧹"},
        ]
    elif intervention == "rain_garden":
        tasks += [
            {"task": "Identify low point where water naturally collects", "week": 1, "icon": "💧"},
            {"task": "Dig basin 6-8 inches deep, slope sides gently", "week": 2, "icon": "⛏️"},
            {"task": "Amend basin soil with 50% coarse sand for drainage", "week": 3, "icon": "🏖️"},
            {"task": "Create overflow path for heavy rains", "week": 3, "icon": "🌊"},
        ]
    elif intervention == "stop_mowing":
        tasks += [
            {"task": "Do one final mow at 3\" height", "week": 1, "icon": "🌿"},
            {"task": "Post a small sign explaining your rewilding project", "week": 1, "icon": "📋"},
        ]

    if soil == "unknown":
        tasks.insert(1, {"task": "Get a soil test from your county extension office ($15-20)", "week": 1, "icon": "🧪"})

    return tasks


def _get_maintenance(intervention):
    """Year-round maintenance schedule."""
    base = {
        "spring": [
            "Remove any invasive species (learn to identify them!)",
            "Add new native plants to fill gaps",
        ],
        "summer": [
            "Water only during extended drought (7+ dry days)",
            "Photograph blooms and pollinators monthly",
            "Remove invasive species as they appear",
        ],
        "fall": [
            "Leave seed heads standing — do NOT deadhead",
            "Leave leaf litter in place",
            "Note which species thrived for next year's planning",
        ],
        "winter": [
            "Leave everything standing — habitat for overwintering insects",
            "Order seeds/plants for spring",
            "Review yearly photos to track progress",
        ],
    }
    if intervention == "native_meadow":
        base["spring"].append("One annual mow in late winter (before March) at 6\" height — returns nutrients")
    if intervention == "rain_garden":
        base["spring"].append("Clear any debris from the basin inlet")
        base["fall"].append("Check that drainage is still functioning")
    return base


def _build_shopping_list(plants, area_sqft, intervention):
    """Generate a shopping list with quantities."""
    # Rough plant spacing: 1 plant per 2-4 sq ft for meadow
    density = {"native_meadow": 3, "rain_garden": 2, "shrub_border": 8, "stop_mowing": 0}.get(intervention, 4)
    if density == 0:
        return [{"item": "Patience", "qty": "Unlimited", "note": "This intervention is free!", "icon": "🆓"}]

    total_plants = max(5, area_sqft // density)
    items = []

    # Group by plant type
    for i, p in enumerate(plants[:8]):
        qty = max(1, total_plants // min(len(plants), 8))
        items.append({
            "item": p["common_name"],
            "scientific": p["scientific_name"],
            "qty": qty,
            "note": f"Blooms {', '.join(p.get('bloom_months', [])[:2])}",
            "icon": "🌿",
        })

    items.append({"item": "Undyed hardwood mulch", "qty": f"{area_sqft // 20} bags", "note": "2-3\" depth", "icon": "🪵"})
    items.append({"item": "Cardboard sheets", "qty": f"~{area_sqft // 10} sq ft", "note": "For sheet mulching (remove tape/staples)", "icon": "📦"})

    return items
