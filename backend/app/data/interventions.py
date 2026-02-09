"""Pre-defined interventions for REWILD scenario engine."""

INTERVENTIONS = [
    {
        "id": "native_meadow",
        "name": "Native Wildflower Meadow",
        "description": "Replace a lawn section with a native wildflower seed mix. Creates a diverse, low-maintenance habitat that blooms from spring through fall.",
        "effort_level": "Medium",
        "icon": "🌱",
        "habitat_classes": ["lawn_to_meadow", "pollinator_garden"],
        "typical_timeline_years": 3,
    },
    {
        "id": "shrub_border",
        "name": "Native Shrub Border",
        "description": "Plant 3-5 native shrub species along yard edges. Provides structure for nesting birds and year-round habitat.",
        "effort_level": "Medium",
        "icon": "🌳",
        "habitat_classes": ["lawn_to_meadow", "pollinator_garden"],
        "typical_timeline_years": 4,
    },
    {
        "id": "rain_garden",
        "name": "Rain Garden",
        "description": "Create a shallow depression planted with water-loving natives. Captures runoff, filters water, and creates unique wetland-edge habitat.",
        "effort_level": "High",
        "icon": "💧",
        "habitat_classes": ["rain_garden"],
        "typical_timeline_years": 3,
    },
    {
        "id": "stop_mowing",
        "name": "Stop Mowing Zone",
        "description": "Simply stop mowing a section of lawn and let it naturalize. The lowest-effort intervention with surprisingly good ecological outcomes.",
        "effort_level": "Very Low",
        "icon": "🚫",
        "habitat_classes": ["lawn_to_meadow"],
        "typical_timeline_years": 5,
    },
    {
        "id": "habitat_structures",
        "name": "Habitat Structures",
        "description": "Add log piles, rock walls, and brush piles to create sheltered micro-habitats for insects, amphibians, and small mammals.",
        "effort_level": "Low",
        "icon": "🪵",
        "habitat_classes": ["lawn_to_meadow", "pollinator_garden", "rain_garden"],
        "typical_timeline_years": 2,
    },
    {
        "id": "pollinator_nesting",
        "name": "Pollinator Nesting",
        "description": "Install bee hotels, leave bare soil patches, and create nesting sites for native bees and other pollinators.",
        "effort_level": "Low",
        "icon": "🐝",
        "habitat_classes": ["pollinator_garden", "lawn_to_meadow"],
        "typical_timeline_years": 1,
    },
    {
        "id": "leave_leaves",
        "name": "Leave the Leaves",
        "description": "Stop fall cleanup and let leaf litter accumulate. Protects overwintering insects, feeds soil biology, and creates natural mulch.",
        "effort_level": "Very Low",
        "icon": "🍂",
        "habitat_classes": ["lawn_to_meadow", "pollinator_garden", "rain_garden"],
        "typical_timeline_years": 2,
    },
    {
        "id": "native_grass",
        "name": "Native Grass Conversion",
        "description": "Replace turf grass with native bunch grasses. Deep roots improve soil, reduce runoff, and provide habitat structure.",
        "effort_level": "Medium",
        "icon": "🌾",
        "habitat_classes": ["lawn_to_meadow"],
        "typical_timeline_years": 3,
    },
]


def get_interventions() -> list[dict]:
    return INTERVENTIONS


def get_intervention(intervention_id: str) -> dict | None:
    for i in INTERVENTIONS:
        if i["id"] == intervention_id:
            return i
    return None
