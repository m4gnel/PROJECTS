import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)

# KAU NPK dose recommendations per palm / acre per year
KAU_FERTILIZER_DOSES = {
    "coconut": {"n_g": 500, "p_g": 320, "k_g": 1200, "organic_kg": 50},
    "rice": {"n_g": 90, "p_g": 45, "k_g": 45, "organic_kg": 5000},
    "banana": {"n_g": 200, "p_g": 200, "k_g": 400, "organic_kg": 10},
    "rubber": {"n_g": 30, "p_g": 30, "k_g": 30, "organic_kg": 12},
    "pepper": {"n_g": 50, "p_g": 50, "k_g": 150, "organic_kg": 10}
}


async def fertilizer_node(state: AgriSageState) -> Dict[str, Any]:
    crop = (state.get("crop") or "coconut").lower()
    soil = state.get("soil_context", {})

    dose = KAU_FERTILIZER_DOSES.get(crop, {"n_g": 100, "p_g": 50, "k_g": 100, "organic_kg": 20})

    # Adjust dose if soil status is low/high
    npk_status = soil.get("npk_status", {})
    if npk_status.get("n") == "low":
        dose["n_g"] = int(dose["n_g"] * 1.15)
    if npk_status.get("p") == "low":
        dose["p_g"] = int(dose["p_g"] * 1.15)
    if npk_status.get("k") == "low":
        dose["k_g"] = int(dose["k_g"] * 1.15)

    res_dict = {
        "crop": crop,
        "nitrogen_g": dose["n_g"],
        "phosphorus_g": dose["p_g"],
        "potassium_g": dose["k_g"],
        "organic_amendment_kg": dose["organic_kg"],
        "advice": f"Apply split doses during May-June and September-October for best uptake in Kerala soils."
    }

    return {
        "agent_outputs": {"fertilizer": res_dict}
    }
