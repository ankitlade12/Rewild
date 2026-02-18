"""Food web interaction graph builder for REWILD scenario engine.

Provides:
- Year-by-year food web graph (plants → pollinators → birds) for D3
  force-directed visualisation.
- **Shannon-Wiener diversity index** (H') computed from species
  abundances within functional groups.
- **Connectance** corrected for directed-graph topology.
"""

from __future__ import annotations

import math
from app.data.native_plants import get_native_plants
from app.data.pollinators import get_pollinators


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


def compute_shannon_wiener(counts: list[int]) -> float:
    """Compute the Shannon-Wiener diversity index H'.

    .. math::

        H' = -\\sum_{i=1}^{S} p_i \\, \\ln(p_i)

    where :math:`S` is the number of species and
    :math:`p_i = n_i / N` is the proportional abundance of species *i*.

    A higher value indicates greater diversity.  A community with one
    species returns 0.0.  A community with ``S`` equally-abundant species
    returns ``ln(S)``.

    Args:
        counts: List of individual counts (or proxy weights) per species.

    Returns:
        H' rounded to 3 decimal places; 0.0 when ≤ 1 species.
    """
    total = sum(counts)
    if total == 0 or len(counts) <= 1:
        return 0.0

    h = 0.0
    for n in counts:
        if n > 0:
            p = n / total
            h -= p * math.log(p)
    return round(h, 3)


def compute_evenness(h_prime: float, species_count: int) -> float:
    """Compute Pielou's evenness index J' = H' / ln(S).

    Normalises diversity to ``[0, 1]`` where 1.0 means all species are
    equally abundant.

    Args:
        h_prime: Shannon-Wiener index value.
        species_count: Number of species (S).

    Returns:
        J' rounded to 3 decimals; 0.0 when S ≤ 1.
    """
    if species_count <= 1:
        return 0.0
    max_h = math.log(species_count)
    if max_h == 0:
        return 0.0
    return round(h_prime / max_h, 3)


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
        
        if plants:
            n_plants = max(1, int(len(plants) * plant_frac))
        else:
            n_plants = 0
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
        for pol_idx, pol in enumerate(polls):
            # Check if any of this pollinator's food plants are present
            overlap = [pv for pv in pol["plants_visited"] if any(pv.lower() in pn for pn in active_plant_names)]
            if not overlap:
                continue

            # Gradual colonization: larger/more mature plant communities support more pollinator species.
            rank = pol_idx / max(len(polls) - 1, 1)
            colonization_gate = min(1.0, plant_frac + (year * 0.05))
            if rank > colonization_gate:
                continue

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
        
        # Stats — diversity indices and corrected connectance
        n_types = len(set(n["type"] for n in nodes))
        n_nodes = len(nodes)
        n_edges = len(edges)

        # Connectance: directed graph → max edges = n*(n-1), not n*(n-1)/2
        max_directed_edges = n_nodes * (n_nodes - 1) if n_nodes > 1 else 1
        connectance = n_edges / max_directed_edges if n_nodes > 1 else 0.0

        # Shannon-Wiener over functional groups (proxy abundance = edge count)
        plant_nodes = [n for n in nodes if n["type"] == "plant"]
        poll_nodes_all = [n for n in nodes if n["group"] == "consumer"]
        bird_nodes = [n for n in nodes if n["type"] == "bird"]

        # Per-species abundance proxy: number of edges touching each node
        edge_ids = set()
        for e in edges:
            edge_ids.add(e["source"])
            edge_ids.add(e["target"])

        species_counts: list[int] = []
        for n in nodes:
            count = sum(1 for e in edges
                        if e["source"] == n["id"] or e["target"] == n["id"])
            species_counts.append(max(count, 1))  # at least 1 (present)

        h_prime = compute_shannon_wiener(species_counts)
        evenness = compute_evenness(h_prime, len(nodes))

        web[year] = {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": n_nodes,
                "total_edges": n_edges,
                "trophic_levels": n_types,
                "connectance": round(connectance, 3),
                "plant_count": len(plant_nodes),
                "pollinator_count": len(poll_nodes_all),
                "bird_count": len(bird_nodes),
                "shannon_wiener_index": h_prime,
                "evenness": evenness,
            },
        }
    
    return web
