"""Food web interaction graph builder for REWILD scenario engine."""
from app.data.native_plants import get_native_plants
from app.data.pollinators import get_pollinators
import math


# Bird guilds attracted by different habitat features
_BIRD_GUILDS = {
    "seed_eaters": {
        "species": ["American Goldfinch", "House Finch", "Dark-eyed Junco", "Song Sparrow"],
        "attracted_by": ["goldenrod", "coneflower", "sunflower", "grass"],
        "min_food_web": 0.2,
    },
    "insectivores": {
        "species": ["Eastern Bluebird", "Tree Swallow", "Chickadee", "Wren"],
        "attracted_by": ["insect-rich habitat", "shrub cover"],
        "min_food_web": 0.3,
    },
    "hummingbirds": {
        "species": ["Ruby-throated Hummingbird", "Anna's Hummingbird", "Rufous Hummingbird"],
        "attracted_by": ["cardinal flower", "bee balm", "sage", "columbine", "fuchsia"],
        "min_food_web": 0.15,
    },
    "ground_nesters": {
        "species": ["Killdeer", "Meadowlark", "Bobolink"],
        "attracted_by": ["meadow", "prairie", "grassland"],
        "min_food_web": 0.4,
    },
}


def build_food_web(
    ecoregion: str,
    interventions: list[str],
    sun: str | None = None,
    soil: str | None = None,
) -> dict:
    """Build year-by-year food web graph for D3 force-directed visualization.
    
    Returns: {year: {nodes: [...], edges: [...], stats: {...}}}
    """
    plants = get_native_plants(ecoregion, sun=sun, soil=soil)
    polls = get_pollinators(ecoregion)
    
    web = {}
    
    for year in range(6):
        # Scale factor: how much of the ecosystem has established
        # Simplified: linear-ish growth, faster at start for active interventions
        t = year / 5.0
        
        # How many plants are established by this year
        if "native_meadow" in interventions or "rain_garden" in interventions:
            plant_frac = min(1.0, 0.1 + t * 0.9)
        elif "stop_mowing" in interventions:
            plant_frac = min(1.0, 0.05 + t * 0.6)
        else:
            plant_frac = min(1.0, 0.08 + t * 0.75)
        
        n_plants = max(1, int(len(plants) * plant_frac))
        active_plants = plants[:n_plants]
        
        nodes = []
        edges = []
        node_ids = set()
        
        # Add plant nodes
        for p in active_plants:
            pid = f"plant_{p['common_name'].replace(' ', '_').lower()}"
            if pid not in node_ids:
                nodes.append({
                    "id": pid,
                    "label": p["common_name"],
                    "type": "plant",
                    "group": "producer",
                    "value": p["ecological_value"],
                    "size": 8 + (3 if p["ecological_value"] == "critical" else 0),
                })
                node_ids.add(pid)
        
        # Add pollinator nodes (attracted by current plants)
        active_plant_names = {p["common_name"].lower() for p in active_plants}
        for pol in polls:
            # Check if any of this pollinator's food plants are present
            overlap = [pv for pv in pol["plants_visited"] if any(pv.lower() in pn for pn in active_plant_names)]
            # Also check based on year (some arrive later)
            arrival_threshold = 0.1 + (0.15 * year)
            
            if overlap or (year >= 2 and plant_frac > 0.3):
                polid = f"poll_{pol['name'].replace(' ', '_').lower()}"
                if polid not in node_ids:
                    nodes.append({
                        "id": polid,
                        "label": pol["name"],
                        "type": pol["type"],
                        "group": "consumer",
                        "conservation": pol["conservation_status"],
                        "size": 10 if pol["conservation_status"] != "stable" else 6,
                    })
                    node_ids.add(polid)
                    
                    # Add edges from plants to this pollinator
                    for pv in overlap[:3]:  # Limit edges per pollinator
                        for p in active_plants:
                            if pv.lower() in p["common_name"].lower():
                                pid = f"plant_{p['common_name'].replace(' ', '_').lower()}"
                                edges.append({
                                    "source": pid,
                                    "target": polid,
                                    "type": "pollination",
                                    "strength": 0.5 + (0.1 * year),
                                })
                                break
        
        # Add birds based on food web complexity
        food_web_score = len(edges) / max(len(polls) * 2, 1)
        for guild_name, guild in _BIRD_GUILDS.items():
            if food_web_score >= guild["min_food_web"] and year >= 1:
                # Add 1-2 species from the guild
                n_species = min(len(guild["species"]), 1 + (year // 2))
                for sp in guild["species"][:n_species]:
                    bid = f"bird_{sp.replace(' ', '_').lower()}"
                    if bid not in node_ids:
                        nodes.append({
                            "id": bid,
                            "label": sp,
                            "type": "bird",
                            "group": "top_consumer",
                            "size": 12,
                        })
                        node_ids.add(bid)
                        
                        # Connect birds to pollinators (insectivores eat insects)
                        poll_nodes = [n for n in nodes if n["group"] == "consumer"]
                        for pn in poll_nodes[:2]:
                            if pn["type"] in ["bee", "butterfly", "moth"]:
                                edges.append({
                                    "source": pn["id"],
                                    "target": bid,
                                    "type": "trophic",
                                    "strength": 0.3 + (0.1 * year),
                                })
        
        # Stats
        n_types = len(set(n["type"] for n in nodes))
        connectance = len(edges) / max(len(nodes) * (len(nodes) - 1) / 2, 1) if nodes else 0
        
        web[year] = {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "trophic_levels": n_types,
                "connectance": round(connectance, 3),
                "plant_count": sum(1 for n in nodes if n["type"] == "plant"),
                "pollinator_count": sum(1 for n in nodes if n["group"] == "consumer"),
                "bird_count": sum(1 for n in nodes if n["type"] == "bird"),
            }
        }
    
    return web
