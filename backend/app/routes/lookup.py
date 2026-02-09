"""API routes for REWILD data lookups."""
from fastapi import APIRouter, HTTPException

from app.data.usda_zones import get_zone
from app.data.ecoregions import get_ecoregion
from app.data.native_plants import get_native_plants
from app.data.pollinators import get_pollinators, get_plant_pollinator_matrix
from app.data.interventions import get_interventions

router = APIRouter(prefix="/api")


@router.get("/lookup/{zip_code}")
async def lookup_location(zip_code: str):
    """Look up USDA zone + ecoregion for a zip code."""
    if not zip_code.isdigit() or len(zip_code) != 5:
        raise HTTPException(status_code=422, detail="Zip code must be 5 digits")

    zone_data = get_zone(zip_code)
    eco_data = get_ecoregion(zip_code)

    if not zone_data.get("zone"):
        raise HTTPException(status_code=404, detail=f"Unknown zip code: {zip_code}")

    return {
        "zip_code": zip_code,
        "zone": zone_data["zone"],
        "min_temp_f_low": zone_data["min_temp_f_low"],
        "min_temp_f_high": zone_data["min_temp_f_high"],
        "last_frost": zone_data["last_frost"],
        "first_frost": zone_data["first_frost"],
        "state": zone_data["state"],
        "ecoregion": eco_data.get("ecoregion", "Unknown"),
        "ecoregion_id": eco_data.get("ecoregion_id", ""),
        "ecoregion_description": eco_data.get("description", ""),
        "climate": eco_data.get("climate", ""),
        "typical_soil": eco_data.get("typical_soil", ""),
        "key_habitats": eco_data.get("key_habitats", []),
    }


@router.get("/plants/{ecoregion}")
async def list_plants(ecoregion: str, sun: str | None = None, soil: str | None = None):
    """Get native plants for an ecoregion."""
    plants = get_native_plants(ecoregion, sun=sun, soil=soil)
    if not plants:
        raise HTTPException(status_code=404, detail=f"No plants found for ecoregion: {ecoregion}")
    return {"ecoregion": ecoregion, "count": len(plants), "plants": plants}


@router.get("/pollinators/{ecoregion}")
async def list_pollinators(ecoregion: str):
    """Get pollinators and interaction matrix for an ecoregion."""
    polls = get_pollinators(ecoregion)
    matrix = get_plant_pollinator_matrix(ecoregion)
    if not polls:
        raise HTTPException(status_code=404, detail=f"No pollinators found for ecoregion: {ecoregion}")
    return {
        "ecoregion": ecoregion,
        "count": len(polls),
        "pollinators": polls,
        "plant_pollinator_matrix": matrix,
    }


@router.get("/interventions")
async def list_interventions():
    """Get all available interventions."""
    interventions = get_interventions()
    return {"count": len(interventions), "interventions": interventions}
