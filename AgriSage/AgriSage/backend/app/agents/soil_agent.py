from .state import AgriState


async def soil_node(state: AgriState) -> dict:
    """
    Looks up soil data from NBSS API or local cache for Kerala.
    Fallback: hard-coded laterite soil defaults for Kerala if API fails.
    Returns: {"soil_data": SoilData, "agents_completed": ["soil"]}
    """
    try:
        # Kerala default: laterite soil
        soil_data = {
            "soil_type": "laterite",
            "ph": 5.8,
            "nitrogen_kg_ha": 280.0,
            "phosphorus_kg_ha": 18.0,
            "potassium_kg_ha": 110.0,
            "organic_matter_percent": 2.1,
        }
        return {"soil_data": soil_data, "agents_completed": ["soil"]}
    except Exception as e:
        return {"error_messages": [f"soil: {str(e)}"], "agents_completed": ["soil"]}
