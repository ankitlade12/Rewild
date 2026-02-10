"""Simulation API endpoint for REWILD scenario engine."""
import asyncio
from fastapi import APIRouter
from pydantic import BaseModel

from app.engine.succession import simulate_trajectory
from app.engine.bloom_calendar import generate_bloom_calendar
from app.engine.interactions import build_food_web
from app.engine.uncertainty import wrap_trajectory_with_uncertainty
from app.engine.claude_reasoner import get_narrative

router = APIRouter(prefix="/api")


class SimulationRequest(BaseModel):
    site_profile: dict
    interventions: list[str]


@router.post("/simulate")
async def run_simulation(req: SimulationRequest):
    """Run the full simulation pipeline for selected interventions."""
    sp = req.site_profile
    zip_code = sp["zip_code"]
    area = sp.get("area_sqft", 500)
    state = sp.get("current_state", "maintained_lawn")
    sun = sp.get("sun_exposure", "full")
    soil = sp.get("soil_type", "well_drained")
    soil_known = soil != "unknown"
    
    # Get ecoregion for shared lookups
    from app.data.ecoregions import get_ecoregion
    eco = get_ecoregion(zip_code)
    ecoregion = eco.get("ecoregion", "Eastern Temperate Forests")
    
    scenarios = []
    for intervention in req.interventions:
        # 1. Deterministic succession
        trajectory = simulate_trajectory(zip_code, intervention, area, state, sun, soil)
        
        # 2. Uncertainty bands
        trajectory = wrap_trajectory_with_uncertainty(trajectory, intervention, soil_known)
        
        # 3. Bloom calendar
        bloom = generate_bloom_calendar(ecoregion, sun, soil if soil_known else None)
        
        # 4. Food web
        food_web = build_food_web(ecoregion, [intervention], sun, soil if soil_known else None)
        
        # 5. AI narrative (async, uses Y3 metrics as input)
        y3 = trajectory["years"][3] if len(trajectory["years"]) > 3 else {}
        y3_metrics = {}
        for k, v in y3.items():
            if isinstance(v, dict) and "likely" in v:
                y3_metrics[k] = v["likely"]
            elif k != "year":
                y3_metrics[k] = v
        
        narrative = await get_narrative(
            ecoregion=ecoregion,
            intervention=intervention,
            metrics=y3_metrics,
            site_info={"zip": zip_code, "area": area, "sun": sun, "soil": soil},
        )
        
        scenarios.append({
            "intervention": intervention,
            "timeline": trajectory["years"],
            "uncertainty_reducers": trajectory.get("uncertainty_reducers", []),
            "bloom_calendar": bloom,
            "food_web": {int(k): v for k, v in food_web.items()},
            "narrative": narrative,
            "zone": trajectory.get("zone"),
            "ecoregion": ecoregion,
        })
    
    return {
        "site": sp,
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
    }


class ActionPlanRequest(BaseModel):
    zip_code: str
    intervention: str
    area_sqft: int = 500
    sun: str = "full"
    soil: str = "well_drained"


@router.post("/action-plan")
async def get_action_plan(req: ActionPlanRequest):
    """Generate a detailed action plan with planting calendar."""
    from app.engine.action_plan import generate_action_plan
    plan = generate_action_plan(
        zip_code=req.zip_code,
        intervention=req.intervention,
        area_sqft=req.area_sqft,
        sun=req.sun,
        soil=req.soil,
    )
    return plan
