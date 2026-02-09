"""
EPA Level III Ecoregion lookup by zip code.

Maps 3-digit zip prefixes to EPA Level III ecoregions.
Covers the most common US ecoregions with descriptions and climate info.
"""

# Ecoregion definitions
ECOREGIONS: dict[str, dict] = {
    "Eastern Temperate Forests": {
        "id": "etf",
        "description": "Deciduous and mixed forests covering the eastern US. Rich biodiversity with distinct four seasons.",
        "climate": "Humid continental to subtropical, 30-60 inches annual precipitation",
        "typical_soil": "Well-drained loams and clay loams",
        "key_habitats": ["deciduous forest", "meadow", "riparian corridor", "wetland edge"],
    },
    "Southeastern Plains": {
        "id": "sep",
        "description": "Flat to rolling coastal plains with pine-hardwood forests. Warm, humid climate supports high biodiversity.",
        "climate": "Humid subtropical, 45-65 inches annual precipitation",
        "typical_soil": "Sandy loams, clay subsoils common",
        "key_habitats": ["longleaf pine savanna", "bottomland hardwood", "coastal marsh", "sandhill"],
    },
    "Great Plains": {
        "id": "gp",
        "description": "Vast grasslands stretching from Texas to the Dakotas. Once dominated by tallgrass and shortgrass prairies.",
        "climate": "Semi-arid to subhumid, 15-35 inches annual precipitation",
        "typical_soil": "Deep, fertile mollisols",
        "key_habitats": ["tallgrass prairie", "mixed-grass prairie", "riparian woodland", "playa wetland"],
    },
    "Mediterranean California": {
        "id": "mc",
        "description": "Dry summers and mild, wet winters. Unique flora adapted to fire and drought cycles.",
        "climate": "Mediterranean, 10-30 inches precipitation (mostly winter)",
        "typical_soil": "Well-drained, often rocky or sandy",
        "key_habitats": ["chaparral", "oak woodland", "coastal sage scrub", "riparian corridor"],
    },
    "North American Deserts": {
        "id": "nad",
        "description": "Hot, arid landscapes including the Sonoran, Chihuahuan, and Mojave deserts. Specialized drought-adapted flora.",
        "climate": "Arid, 3-15 inches annual precipitation, extreme heat",
        "typical_soil": "Sandy, alkaline, often caliche layer",
        "key_habitats": ["desert scrub", "wash corridor", "desert grassland", "oasis"],
    },
    "Northern Forests": {
        "id": "nf",
        "description": "Boreal and mixed forests of the northern tier. Cold winters with conifer-dominated landscapes.",
        "climate": "Humid continental, cold winters, 25-45 inches precipitation",
        "typical_soil": "Acidic, often thin over bedrock",
        "key_habitats": ["boreal forest", "bog", "northern hardwood", "lakeside meadow"],
    },
    "Central USA Plains": {
        "id": "cup",
        "description": "Formerly tallgrass prairie, now largely agricultural. Rich soils support diverse native plantings.",
        "climate": "Humid continental, 30-40 inches annual precipitation",
        "typical_soil": "Deep, fertile prairie soils (mollisols)",
        "key_habitats": ["tallgrass prairie remnant", "oak savanna", "fen", "sedge meadow"],
    },
    "Ozark/Ouachita Highlands": {
        "id": "ooh",
        "description": "Upland forests and glades in the Interior Highlands. Diverse mix of eastern and western species.",
        "climate": "Humid subtropical, 40-55 inches annual precipitation",
        "typical_soil": "Thin, rocky, well-drained over limestone/chert",
        "key_habitats": ["oak-hickory forest", "glade", "bluff", "seep spring"],
    },
    "Western Mountains": {
        "id": "wm",
        "description": "Rocky Mountain and Pacific mountain ranges with elevation-driven ecosystems from grassland to alpine.",
        "climate": "Varies by elevation: semi-arid to alpine, 15-60+ inches precipitation",
        "typical_soil": "Rocky, well-drained, often thin",
        "key_habitats": ["mountain meadow", "aspen grove", "subalpine forest", "riparian corridor"],
    },
    "Pacific Northwest Forests": {
        "id": "pnw",
        "description": "Lush temperate rainforests and mixed conifer forests. High rainfall supports dense vegetation and moss-covered canopies.",
        "climate": "Marine west coast, 40-100+ inches annual precipitation",
        "typical_soil": "Deep, acidic, rich in organic matter",
        "key_habitats": ["temperate rainforest", "wetland prairie", "stream corridor", "forest edge"],
    },
    "Tropical/Subtropical Florida": {
        "id": "tsf",
        "description": "Subtropical to tropical ecosystems including mangroves, sawgrass, and hammocks. Year-round growing season.",
        "climate": "Tropical/subtropical, 50-65 inches precipitation, minimal frost",
        "typical_soil": "Sandy, calcareous, often with high water table",
        "key_habitats": ["pine flatwood", "tropical hammock", "marsh", "coastal dune"],
    },
    "Gulf Coast Plains": {
        "id": "gcp",
        "description": "Low-lying coastal regions along the Gulf of Mexico. Warm, humid climate with diverse wetland habitats.",
        "climate": "Humid subtropical, 50-65 inches annual precipitation",
        "typical_soil": "Alluvial clays, sandy loams near coast",
        "key_habitats": ["coastal prairie", "bottomland forest", "salt marsh", "barrier island"],
    },
}

# 3-digit zip prefix → ecoregion name
ZIP_TO_ECOREGION: dict[str, str] = {
    # Massachusetts / New England → Eastern Temperate Forests
    **{f"0{i:02d}": "Eastern Temperate Forests" for i in range(10, 30)},
    # Maine → Northern Forests
    **{f"0{i:02d}": "Northern Forests" for i in range(30, 50)},
    # Vermont → Northern Forests
    **{f"0{i:02d}": "Northern Forests" for i in range(50, 60)},
    # Connecticut → Eastern Temperate Forests
    **{f"0{i:02d}": "Eastern Temperate Forests" for i in range(60, 70)},
    # New Jersey → Eastern Temperate Forests
    **{f"0{i:02d}": "Eastern Temperate Forests" for i in range(70, 80)},
    # New York
    **{str(i): "Eastern Temperate Forests" for i in range(100, 150)},
    # Pennsylvania
    **{str(i): "Eastern Temperate Forests" for i in range(150, 197)},
    # Delaware & Maryland
    **{str(i): "Eastern Temperate Forests" for i in range(197, 220)},
    # Virginia
    **{str(i): "Eastern Temperate Forests" for i in range(220, 247)},
    # West Virginia
    **{str(i): "Eastern Temperate Forests" for i in range(247, 269)},
    # North Carolina — mix of Southeastern Plains and Eastern Temperate Forests
    **{str(i): "Southeastern Plains" for i in range(270, 280)},
    **{str(i): "Eastern Temperate Forests" for i in range(280, 290)},
    # South Carolina → Southeastern Plains
    **{str(i): "Southeastern Plains" for i in range(290, 300)},
    # Georgia → Southeastern Plains
    **{str(i): "Southeastern Plains" for i in range(300, 320)},
    # Florida → Tropical/Subtropical Florida (south) and Southeastern Plains (north)
    **{str(i): "Southeastern Plains" for i in range(320, 325)},
    **{str(i): "Tropical/Subtropical Florida" for i in range(325, 350)},
    # Alabama → Southeastern Plains
    **{str(i): "Southeastern Plains" for i in range(350, 370)},
    # Tennessee → Eastern Temperate Forests
    **{str(i): "Eastern Temperate Forests" for i in range(370, 386)},
    # Mississippi → Gulf Coast Plains
    **{str(i): "Gulf Coast Plains" for i in range(386, 398)},
    # Kentucky → Eastern Temperate Forests
    **{str(i): "Eastern Temperate Forests" for i in range(400, 428)},
    # Ohio → Eastern Temperate Forests
    **{str(i): "Eastern Temperate Forests" for i in range(430, 459)},
    # Indiana → Central USA Plains / Eastern Temperate Forests
    **{str(i): "Central USA Plains" for i in range(460, 480)},
    # Michigan → Northern Forests (north) / Eastern Temperate Forests (south)
    **{str(i): "Eastern Temperate Forests" for i in range(480, 493)},
    **{str(i): "Northern Forests" for i in range(493, 500)},
    # Iowa → Central USA Plains
    **{str(i): "Central USA Plains" for i in range(500, 529)},
    # Wisconsin → Northern Forests (north) / Central USA Plains (south)
    **{str(i): "Central USA Plains" for i in range(520, 535)},
    **{str(i): "Northern Forests" for i in range(535, 550)},
    # Minnesota → Northern Forests (north) / Central USA Plains (south)
    **{str(i): "Central USA Plains" for i in range(550, 560)},
    **{str(i): "Northern Forests" for i in range(560, 568)},
    # South Dakota → Great Plains
    **{str(i): "Great Plains" for i in range(570, 578)},
    # North Dakota → Great Plains
    **{str(i): "Great Plains" for i in range(580, 589)},
    # Montana → Western Mountains / Great Plains
    **{str(i): "Great Plains" for i in range(590, 596)},
    **{str(i): "Western Mountains" for i in range(596, 600)},
    # Illinois → Central USA Plains
    **{str(i): "Central USA Plains" for i in range(600, 630)},
    # Missouri → Central USA Plains / Ozark Highlands
    **{str(i): "Central USA Plains" for i in range(630, 640)},
    **{str(i): "Ozark/Ouachita Highlands" for i in range(640, 659)},
    # Kansas → Great Plains
    **{str(i): "Great Plains" for i in range(660, 680)},
    # Nebraska → Great Plains
    **{str(i): "Great Plains" for i in range(680, 694)},
    # Louisiana → Gulf Coast Plains
    **{str(i): "Gulf Coast Plains" for i in range(700, 715)},
    # Arkansas → Ozark/Ouachita Highlands
    **{str(i): "Ozark/Ouachita Highlands" for i in range(716, 730)},
    # Oklahoma → Great Plains
    **{str(i): "Great Plains" for i in range(730, 750)},
    # Texas — multiple ecoregions
    **{str(i): "Great Plains" for i in range(750, 770)},  # North/Central TX
    **{str(i): "Gulf Coast Plains" for i in range(770, 780)},  # Houston area
    **{str(i): "Great Plains" for i in range(780, 790)},  # San Antonio/Central
    **{str(i): "North American Deserts" for i in range(790, 800)},  # West TX
    # Colorado → Western Mountains
    **{str(i): "Western Mountains" for i in range(800, 817)},
    # Wyoming → Western Mountains
    **{str(i): "Western Mountains" for i in range(820, 832)},
    # Idaho → Western Mountains
    **{str(i): "Western Mountains" for i in range(832, 839)},
    # Utah → Western Mountains / North American Deserts
    **{str(i): "Western Mountains" for i in range(840, 848)},
    # Arizona → North American Deserts
    **{str(i): "North American Deserts" for i in range(850, 866)},
    # New Mexico → North American Deserts
    **{str(i): "North American Deserts" for i in range(870, 885)},
    # Nevada → North American Deserts
    **{str(i): "North American Deserts" for i in range(889, 899)},
    # California — multiple ecoregions
    **{str(i): "Mediterranean California" for i in range(900, 935)},  # SoCal + Central Valley
    **{str(i): "Mediterranean California" for i in range(935, 960)},  # NorCal
    **{str(i): "Pacific Northwest Forests" for i in range(960, 962)},  # Far NorCal
    # Oregon → Pacific Northwest Forests
    **{str(i): "Pacific Northwest Forests" for i in range(970, 980)},
    # Washington → Pacific Northwest Forests
    **{str(i): "Pacific Northwest Forests" for i in range(980, 995)},
}


def get_ecoregion(zip_code: str) -> dict:
    """Look up EPA Level III ecoregion for a US zip code.
    
    Returns dict with: ecoregion name, description, climate, typical_soil, key_habitats
    """
    prefix = zip_code[:3]
    
    ecoregion_name = ZIP_TO_ECOREGION.get(prefix)
    if not ecoregion_name:
        return {"error": f"Unknown zip prefix: {prefix}", "ecoregion": None}
    
    eco_data = ECOREGIONS.get(ecoregion_name, {})
    
    return {
        "ecoregion": ecoregion_name,
        "ecoregion_id": eco_data.get("id", ""),
        "description": eco_data.get("description", ""),
        "climate": eco_data.get("climate", ""),
        "typical_soil": eco_data.get("typical_soil", ""),
        "key_habitats": eco_data.get("key_habitats", []),
    }


def list_ecoregions() -> list[dict]:
    """Return all supported ecoregions."""
    return [
        {"name": name, **data}
        for name, data in ECOREGIONS.items()
    ]
