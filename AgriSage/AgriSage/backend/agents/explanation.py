import json
from typing import Dict, Any
from backend.agents.state import AgriSAGEState
from backend.services.llm_service import llm_service

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

EXPLANATION_SYSTEM_PROMPT = """

You are Agri-SAGE Advisory Engine, an agricultural decision support system.

YOUR ROLE:
Convert the structured evidence bundle below into a clear, actionable advisory
for a smallholder farmer. You are a translator of evidence — not a source of knowledge.

ABSOLUTE CONSTRAINTS:
1. Use ONLY facts from the evidence_bundle and knowledge_chunks provided below.
   Do not add any agricultural knowledge from your training data.
2. If evidence_bundle.confidence_state is UNCERTAIN, INSUFFICIENT_DATA, or
   CONFLICTING_EVIDENCE: do NOT recommend any treatment. Request more information.
3. Chemical product names: only use names that appear verbatim in the
   knowledge_chunks or cibrc_data provided. Never invent product names.
4. All yield/profit numbers come from simulation_result only.
   Always label them: "modelled estimate — actual results vary by field conditions".
5. Government schemes: always include: "Final eligibility determined by the
   concerned authority — please verify before applying."
6. Language: Generate advisory in {language_code} ({language_name}).
   Use simple, everyday vocabulary. Avoid technical jargon.
7. Output ONLY valid JSON matching the schema below. No markdown. No explanation.

OUTPUT JSON:
{
  "diagnosis_summary": "<2 sentences max>",
  "confidence_explanation": "<1 sentence>",
  "risk_explanation": "<1-2 sentences>",
  "recommended_action": {
    "what": "<specific action>",
    "when": "<specific timing>",
    "how": "<method>",
    "cost_note": "<cost range>",
    "spray_window": "<time or null>"
  },
  "evidence_summary": ["<point 1>", "<point 2>"],
  "what_would_change_this": ["<factor 1>"],
  "safe_to_act": true,
  "insufficient_data_message": null,
  "modelled_estimate_label": "modelled estimate — actual results vary by field conditions"
}
"""

SAFE_FALLBACK = {
    "diagnosis_summary": "We analyzed your crop photo and farm conditions.",
    "confidence_explanation": "Our confidence is limited — please see evidence details.",
    "risk_explanation": "Please inspect your field and consult a local agronomist.",
    "recommended_action": {
        "what": "Inspect 10 plants in different parts of the field",
        "when": "Today",
        "how": "Look for spread of symptoms since photo was taken",
        "cost_note": "No cost — visual inspection only",
        "spray_window": None
    },
    "evidence_summary": ["Photo analyzed", "Weather checked", "Crop stage estimated"],
    "what_would_change_this": ["A clearer photo", "A soil test result"],
    "safe_to_act": False,
    "insufficient_data_message": "Advisory generation encountered a technical issue.",
    "modelled_estimate_label": "modelled estimate — actual results vary by field conditions"
}


class ExplanationAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        confidence_state = state.get("confidence_state", "CONFIRMED")
        critic = state.get("critic_result") or {}
        vision = state.get("vision_result") or {}
        weather = state.get("weather_result") or {}
        crop_stage = state.get("crop_stage_result") or {}
        knowledge = state.get("knowledge_result") or {}
        sim = state.get("simulation_result") or {}

        lang_code = state.get("language", "ml")
        lang_name = "Malayalam" if lang_code == "ml" else "English"

        # Check if confidence state requires holding chemical treatment recommendation
        if confidence_state in ["UNCERTAIN", "INSUFFICIENT_DATA", "CONFLICTING_EVIDENCE", "OUT_OF_SCOPE"]:
            fallback = dict(SAFE_FALLBACK)
            fallback["safe_to_act"] = False
            fallback["insufficient_data_message"] = f"Confidence is {confidence_state}. No chemical treatment recommended."
            state["advisory"] = fallback
            return state

        sys_prompt = EXPLANATION_SYSTEM_PROMPT.replace(
            "{language_code}", lang_code
        ).replace(
            "{language_name}", lang_name
        )


        user_prompt = f"""
EVIDENCE BUNDLE:
confidence_state: {confidence_state}
confidence_score: {critic.get('confidence_score', 0.8)}
VISION: label={vision.get('label')} severity={vision.get('severity')} affected_area_pct={vision.get('affected_area_pct')}
WEATHER: dfi={weather.get('dfi')} spray_window={weather.get('spray_window')} wet_days={weather.get('consecutive_wet_days')} temp={weather.get('temperature_c')} humidity={weather.get('humidity_pct')}
CROP STAGE: stage={crop_stage.get('stage_name')} vulnerability={crop_stage.get('vulnerability')} das={crop_stage.get('days_after_sowing')}
KNOWLEDGE CHUNKS: {json.dumps(knowledge.get('top_chunks', []))}
SIMULATION: {json.dumps(sim)}
CONFLICTS: {json.dumps(critic.get('conflicts', []))}
MISSING: {json.dumps(state.get('warnings', []))}
CONTEXT: crop={state.get('crop')} location=Palakkad,Kerala language={lang_name}
Generate advisory JSON now. Output JSON only.
"""

        res = await llm_service.generate(sys_prompt, user_prompt, temperature=0.2, max_tokens=1500)

        if not res or not isinstance(res, dict) or "recommended_action" not in res:
            logger.warning("using_explanation_safe_fallback")
            res = SAFE_FALLBACK

        state["advisory"] = res
        return state
