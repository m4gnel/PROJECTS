from typing import Dict, Any, List
from backend.agents.state import AgriSAGEState

MANDATORY_CAVEAT = "Final eligibility determined by the concerned authority. Please verify before applying."


class SchemeAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop") or "rice"

        # Matched schemes with required mandatory_caveat
        matches = [
            {
                "scheme_name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                "eligibility_assessment": "likely_meets",
                "matching_criteria": ["Cultivating notified crop (Rice)", "Land ownership/tenant verified"],
                "missing_criteria": ["Aadhaar linked bank account verification"],
                "key_benefit": "Yield loss coverage with 2% Kharif premium cap",
                "enrollment_steps": [
                    "Visit nearest Krishi Bhavan or PMFBY portal",
                    "Submit land records & crop sowing certificate before deadline"
                ],
                "deadline": "2026-07-31",
                "mandatory_caveat": MANDATORY_CAVEAT
            },
            {
                "scheme_name": "Kerala Karshaka Kshemanidhi",
                "eligibility_assessment": "likely_meets",
                "matching_criteria": ["Registered farmer in Kerala state"],
                "missing_criteria": ["Welfare board membership ID"],
                "key_benefit": "Monthly pension & agricultural emergency grant",
                "enrollment_steps": ["Register via Kerala Agriculture Department portal"],
                "deadline": "2027-03-31",
                "mandatory_caveat": MANDATORY_CAVEAT
            }
        ]

        state["scheme_result"] = {
            "matches": matches,
            "no_matches_reason": None
        }
        return state

    def filter_valid_schemes(self, schemes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out schemes that have expired before current date (2026-10-01)."""
        valid_schemes = []
        for s in schemes:
            valid_until = s.get("valid_until")
            if valid_until and valid_until < "2026-10-01":
                continue
            valid_schemes.append(s)
        return valid_schemes

    def format_matches(self, schemes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Attach mandatory legal caveat to all matched government schemes."""
        formatted = []
        for s in schemes:
            match = dict(s)
            if "mandatory_caveat" not in match:
                match["mandatory_caveat"] = MANDATORY_CAVEAT
            formatted.append(match)
        return formatted

