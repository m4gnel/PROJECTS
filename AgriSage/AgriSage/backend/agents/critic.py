from typing import Dict, Any, List
from backend.agents.state import AgriSAGEState

VALID_CROPS = {"rice", "banana", "coconut", "tomato", "maize"}


class CriticAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop")
        vision = state.get("vision_result") or {}
        weather = state.get("weather_result") or {}
        crop_stage = state.get("crop_stage_result") or {}
        knowledge = state.get("knowledge_result") or {}

        conflicts: List[str] = []
        warnings: List[str] = state.get("warnings", [])

        # 1. Check Out of Scope
        if not crop or crop not in VALID_CROPS:
            confidence_state = "OUT_OF_SCOPE"
            confidence_score = 0.0
        elif vision.get("out_of_distribution", False):
            confidence_state = "INSUFFICIENT_DATA"
            confidence_score = vision.get("confidence_score", 0.0)
        else:
            v_conf = vision.get("confidence_score", 0.0)
            dfi = weather.get("dfi", 0.5)
            wet_days = weather.get("consecutive_wet_days", 0)

            # Check Conflicting Evidence: Vision says disease, but weather is dry/unfavorable
            if v_conf > 0.50 and dfi < 0.25 and wet_days < 2 and "healthy" not in vision.get("label", ""):
                conflicts.append("Weather DFI unfavorable for diagnosed fungal/bacterial disease")
                confidence_state = "CONFLICTING_EVIDENCE"
                confidence_score = v_conf * 0.5
            elif v_conf > 0.80 and dfi >= 0.50 and len(conflicts) == 0:
                confidence_state = "CONFIRMED"
                confidence_score = v_conf
            elif 0.60 <= v_conf <= 0.80 and len(conflicts) == 0:
                confidence_state = "LIKELY"
                confidence_score = v_conf
            elif 0.40 <= v_conf < 0.60 or len(conflicts) == 1:
                confidence_state = "POSSIBLE"
                confidence_score = v_conf
            else:
                confidence_state = "UNCERTAIN"
                confidence_score = v_conf

        # Safety blocks check
        safe_to_act = True
        if confidence_state in ["UNCERTAIN", "INSUFFICIENT_DATA", "CONFLICTING_EVIDENCE", "OUT_OF_SCOPE"]:
            safe_to_act = False

        # Image quality suspicious mismatch check
        q_score = vision.get("quality_score", 1.0)
        v_conf = vision.get("confidence_score", 0.0)
        if q_score < 0.3 and v_conf > 0.85:
            conflicts.append("Suspicious mismatch: low image quality with high vision confidence")
            safe_to_act = False

        # Determine if simulation should run
        run_simulation = (
            confidence_score > 0.65
            and len(conflicts) == 0
            and confidence_state in ["CONFIRMED", "LIKELY"]
        )

        critic_result = {
            "confidence_state": confidence_state,
            "confidence_score": confidence_score,
            "conflicts": conflicts,
            "safe_to_act": safe_to_act,
            "run_simulation": run_simulation,
        }

        state["critic_result"] = critic_result
        state["confidence_state"] = confidence_state
        state["run_simulation"] = run_simulation
        return state

    async def evaluate(self, state: AgriSAGEState) -> Dict[str, Any]:
        """Convenience method to evaluate state and return critic_result dict."""
        updated_state = await self.run(state)
        return updated_state["critic_result"]

    async def run_safety_checks(self, recommendation: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validates chemical recommendation against official CIB&RC registration database.
        Returns (is_safe: bool, issues: List[str]).
        """
        cib_rc_database = {
            "Tricyclazole 75 WP": {"crops": {"rice"}, "max_dosage": 1.0},
            "Azoxystrobin 23% SC": {"crops": {"rice", "tomato"}, "max_dosage": 1.0},
            "Carbendazim 50% WP": {"crops": {"rice", "banana"}, "max_dosage": 1.0},
            "Mancozeb 75% WP": {"crops": {"tomato", "banana"}, "max_dosage": 2.5},
            "Copper Oxychloride 50% WP": {"crops": {"coconut", "banana"}, "max_dosage": 3.0},
        }

        product = recommendation.get("product_name")
        crop = recommendation.get("crop")
        dosage = recommendation.get("dosage", 0.0)

        if not product or product not in cib_rc_database:
            return False, ["BLOCK: Unregistered chemical product in CIB&RC registry"]

        reg = cib_rc_database[product]
        if crop not in reg["crops"]:
            return False, [f"BLOCK: {product} is not registered for use on crop '{crop}'"]

        if dosage > reg["max_dosage"]:
            return False, [f"BLOCK: Dosage {dosage} exceeds CIB&RC maximum limit of {reg['max_dosage']}"]

        return True, []

