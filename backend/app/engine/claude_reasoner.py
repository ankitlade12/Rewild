"""OpenAI-based ecological reasoner for REWILD scenario engine."""
import os
import json
from openai import AsyncOpenAI


_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI | None:
    global _client
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    if _client is None:
        _client = AsyncOpenAI(api_key=key)
    return _client


_SYSTEM_PROMPT = """You are an ecological advisor for a micro-habitat rewilding tool.
Given a site profile and intervention scenario, provide:
1. A concise ecological narrative (2-3 sentences) explaining what will likely happen over 5 years
2. 2-3 specific species recommendations for the site
3. A brief uncertainty note explaining what could affect outcomes

Respond in JSON format:
{
  "narrative": "string",
  "species_recommendations": [{"name": "string", "reason": "string"}],
  "uncertainty_note": "string",
  "season_tip": "string"
}

Keep it conversational, honest about uncertainty, and actionable. No jargon."""


async def get_narrative(
    ecoregion: str,
    intervention: str,
    metrics: dict,
    site_info: dict | None = None,
    use_openai: bool = True,
) -> dict:
    """Get AI-enhanced ecological narrative for a scenario.
    
    Falls back to template-based narrative if OpenAI unavailable.
    """
    if use_openai:
        client = _get_client()
        if client:
            try:
                return await _call_openai(client, ecoregion, intervention, metrics, site_info)
            except Exception as e:
                print(f"OpenAI call failed, using fallback: {e}")
    
    return _fallback_narrative(ecoregion, intervention, metrics)


async def _call_openai(
    client: AsyncOpenAI,
    ecoregion: str,
    intervention: str,
    metrics: dict,
    site_info: dict | None,
) -> dict:
    """Call OpenAI API for ecological narrative."""
    user_prompt = f"""Site: {ecoregion} ecoregion
Intervention: {intervention.replace('_', ' ')}
Year 3 metrics: {json.dumps(metrics)}
Site details: {json.dumps(site_info or {})}

Generate an ecological narrative for this rewilding scenario."""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=500,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {"narrative": content, "species_recommendations": [], "uncertainty_note": "", "season_tip": ""}

    result["source"] = "openai"
    return result


_INTERVENTION_NARRATIVES = {
    "native_meadow": "Converting to a native wildflower meadow creates one of the most biodiverse micro-habitats possible. Within 2-3 years, expect a rich tapestry of native grasses and wildflowers supporting dozens of pollinator species.",
    "stop_mowing": "Simply stopping mowing allows dormant seed banks to express themselves. It's the lowest-effort intervention with surprisingly good results, though it takes longer to see dramatic changes — patience is the key ingredient.",
    "rain_garden": "Rain gardens provide immediate water management benefits while creating wetland-edge habitat that's increasingly rare in suburban landscapes. Expect rapid establishment of water-loving natives and unique pollinator communities.",
    "shrub_border": "Native shrubs form the structural backbone of a healthy ecosystem. While they're slower to establish, by years 4-5 they provide irreplaceable nesting habitat for birds and overwintering sites for beneficial insects.",
    "habitat_structures": "Log piles, rock features, and brush piles create sheltered micro-habitats that dramatically increase the number of species your site can support, especially overwintering insects and small mammals.",
    "pollinator_nesting": "Dedicated nesting sites dramatically accelerate pollinator colonization. Native bees are often more effective pollinators than honeybees, and most are solitary and non-aggressive.",
    "leave_leaves": "Leaf litter is nature's mulch and insect nursery. Fireflies, moths, and many native bees rely on leaf litter for overwintering. This simple change supports an invisible but crucial part of the food web.",
    "native_grass": "Deep-rooted native grasses transform soil biology within 2-3 years, sequestering carbon, improving water infiltration, and providing habitat structure for ground-nesting birds and insects.",
}


def _fallback_narrative(ecoregion: str, intervention: str, metrics: dict) -> dict:
    """Template-based fallback when OpenAI is not available."""
    narrative = _INTERVENTION_NARRATIVES.get(
        intervention,
        f"This intervention will gradually transform your site into a more ecologically productive habitat within the {ecoregion} ecoregion."
    )

    return {
        "narrative": narrative,
        "species_recommendations": [
            {"name": "See native plants list", "reason": "Filtered for your ecoregion and site conditions"},
        ],
        "uncertainty_note": f"Predictions for the {ecoregion} are based on regional ecological studies. Actual results will vary based on local soil, microclimate, and neighborhood ecology.",
        "season_tip": "Start planting in spring after the last frost date for your zone.",
        "source": "fallback",
    }
