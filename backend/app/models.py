"""Pydantic models for REWILD API."""
from pydantic import BaseModel


class LookupResponse(BaseModel):
    zip_code: str
    zone: str
    min_temp_f_low: int
    min_temp_f_high: int
    last_frost: str
    first_frost: str
    state: str
    ecoregion: str
    ecoregion_id: str
    ecoregion_description: str
    climate: str
    typical_soil: str
    key_habitats: list[str]


class SiteProfile(BaseModel):
    zip_code: str
    area_sqft: int
    current_state: str  # maintained_lawn | weedy | partial_garden | bare_soil
    sun_exposure: str   # full | partial | shade
    soil_type: str      # well_drained | clay | sandy | unknown
    goals: list[str]    # pollinators | birds | water | carbon | education | beauty


class Intervention(BaseModel):
    id: str
    name: str
    description: str
    effort_level: str
    icon: str
    habitat_classes: list[str]
    typical_timeline_years: int


class NativePlant(BaseModel):
    common_name: str
    scientific_name: str
    bloom_months: list[str]
    height_ft: float
    sun_requirement: str
    soil_preference: str
    ecological_value: str
    pollinator_associations: list[str]


class Pollinator(BaseModel):
    name: str
    type: str
    flight_months: list[str]
    nesting_type: str
    plants_visited: list[str]
    conservation_status: str
