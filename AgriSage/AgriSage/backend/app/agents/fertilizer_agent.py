from .state import AgriState

# Kerala crop NPK requirements (kg/ha)
CROP_NPK = {
    "rice":    {"N": 100, "P": 50, "K": 50},
    "coconut": {"N": 500, "P": 320, "K": 1200},
    "banana":  {"N": 200, "P": 60, "K": 300},
    "pepper":  {"N": 100, "P": 40, "K": 140},
    "tapioca": {"N": 100, "P": 50, "K": 100},
    "default": {"N": 80,  "P": 40, "K": 80},
}


async def fertilizer_node(state: AgriState) -> dict:
    """
    Recommends fertilizer based on soil_data NPK deficit + crop requirement.
    Returns: {"agent_findings": ["fertilizer: <recommendation>"], "agents_completed": ["fertilizer"]}
    """
    try:
        soil = state.get("soil_data") or {}
        crop_name = ""
        if state.get("crop_info"):
            crop_name = (state["crop_info"] or {}).get("crop_name", "").lower()

        required = CROP_NPK.get(crop_name, CROP_NPK["default"])
        soil_n = soil.get("nitrogen_kg_ha", 280)
        soil_p = soil.get("phosphorus_kg_ha", 18)
        soil_k = soil.get("potassium_kg_ha", 110)

        n_deficit = max(0, required["N"] - soil_n * 0.05)
        p_deficit = max(0, required["P"] - soil_p)
        k_deficit = max(0, required["K"] - soil_k)

        rec = (
            f"For {crop_name or 'your crop'}: Apply Urea {n_deficit:.0f}kg/ha, "
            f"SSP {p_deficit:.0f}kg/ha, MOP {k_deficit:.0f}kg/ha. "
            f"Split urea into 3 doses at planting, 30 days, and 60 days after transplanting."
        )
        return {"agent_findings": [f"fertilizer: {rec}"], "agents_completed": ["fertilizer"]}
    except Exception as e:
        return {"error_messages": [f"fertilizer: {str(e)}"], "agents_completed": ["fertilizer"]}
