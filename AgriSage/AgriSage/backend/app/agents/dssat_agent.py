from .state import AgriState


DSSAT_SUPPORTED = ["rice", "maize", "wheat", "soybean"]


async def dssat_node(state: AgriState) -> dict:
    """
    Runs DSSAT crop simulation. Only for supported crops.
    Returns: {"dssat_result": {yield_kg_ha, days_to_maturity, water_stress}, "agents_completed": ["dssat"]}
    """
    try:
        crop_name = ""
        if state.get("crop_info"):
            crop_name = (state["crop_info"] or {}).get("crop_name", "").lower()

        if crop_name not in DSSAT_SUPPORTED:
            return {"dssat_result": None, "agents_completed": ["dssat"]}

        from ..utils.dssat_runner import run_dssat
        result = await run_dssat(
            crop_name,
            state.get("soil_data") or {},
            state.get("weather_data") or {},
        )
        return {"dssat_result": result, "agents_completed": ["dssat"]}
    except Exception as e:
        return {"error_messages": [f"dssat: {str(e)}"], "agents_completed": ["dssat"]}
