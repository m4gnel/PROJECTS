from typing import Dict, Any
from backend.agents.state import AgriSAGEState


class SoilAgent:
    def __init__(self):
        # District-level NBSS&LUP Kerala soil profile baselines
        self.district_soil_map = {
            "Palakkad": {
                "soil_type": "Laterite Soil",
                "pH": 5.8,
                "texture": "Clay Loam",
                "nitrogen_status": "Medium",
                "phosphorus_status": "Low",
                "potassium_status": "Medium",
                "organic_carbon_pct": 0.85,
                "field_capacity_pct": 28.5,
                "wilting_point_pct": 14.2,
                "drainage": "Moderately well drained",
                "recommendation": "Acidic soil. Apply lime / dolomite @ 250 kg/acre prior to sowing."
            },
            "Kuttanad": {
                "soil_type": "Kari / Acid Saline Soil",
                "pH": 4.5,
                "texture": "Silty Clay",
                "nitrogen_status": "High",
                "phosphorus_status": "Low",
                "potassium_status": "Low",
                "organic_carbon_pct": 2.1,
                "field_capacity_pct": 35.0,
                "wilting_point_pct": 18.0,
                "drainage": "Poorly drained",
                "recommendation": "Highly acidic soil. Apply agricultural lime and ensure proper subsurface drainage."
            },
            "Wayand": {
                "soil_type": "Forest Loam & Red Soil",
                "pH": 5.6,
                "texture": "Sandy Loam",
                "nitrogen_status": "High",
                "phosphorus_status": "Medium",
                "potassium_status": "High",
                "organic_carbon_pct": 1.4,
                "field_capacity_pct": 24.0,
                "wilting_point_pct": 11.5,
                "drainage": "Well drained",
                "recommendation": "Rich organic content. Maintain mulch cover to prevent erosion on sloped fields."
            },
            "Thrissur": {
                "soil_type": "Alluvial & Laterite",
                "pH": 5.7,
                "texture": "Sandy Clay Loam",
                "nitrogen_status": "Medium",
                "phosphorus_status": "Medium",
                "potassium_status": "Medium",
                "organic_carbon_pct": 0.95,
                "field_capacity_pct": 26.0,
                "wilting_point_pct": 13.0,
                "drainage": "Moderately well drained",
                "recommendation": "Balanced alluvial soil. Suitable for wetland paddy-pulse crop rotation."
            },
            "Ernakulam": {
                "soil_type": "Coastal Alluvium & Laterite",
                "pH": 5.9,
                "texture": "Loamy Sand",
                "nitrogen_status": "Medium",
                "phosphorus_status": "Medium",
                "potassium_status": "Medium",
                "organic_carbon_pct": 0.90,
                "field_capacity_pct": 25.0,
                "wilting_point_pct": 12.0,
                "drainage": "Well drained",
                "recommendation": "Apply organic manure @ 5 tonnes/acre to enhance cation exchange capacity."
            }
        }

    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        farm_state = state.get("farm_state") or {}
        district = farm_state.get("district") or "Palakkad"

        profile = self.district_soil_map.get(district, self.district_soil_map["Palakkad"])
        soil_context = {
            "district": district,
            "soil_profile": profile,
            "source": "NBSS&LUP Kerala Soil Resource Database"
        }

        state["soil_context"] = soil_context
        return state


soil_agent = SoilAgent()
