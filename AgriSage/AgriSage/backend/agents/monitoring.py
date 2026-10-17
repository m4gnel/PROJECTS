from typing import Dict, Any
from backend.agents.state import AgriSAGEState
from backend.services.llm_service import llm_service

MONITORING_SYSTEM_PROMPT = """
You are Agri-SAGE Morning Briefing Generator.

RULES:
1. Maximum 4 items — one per category.
2. Simple language — farmer acts on this immediately.
3. Specific: 'Check lower leaves' not 'Monitor crop health'.
4. If no significant risk: say 'All clear today'.
5. One recommended action only — most important for today.
6. Language: {language_name}.

OUTPUT: Valid JSON only.
{"stage_summary":"<crop+stage+days>","top_risk":{"risk_type":"disease|pest|water|heat|none",
"level":"high|medium|low|none","description":"<1 sentence>","is_urgent":false},
"weather_today":"<2 words>","recommended_action":"<one action>",
"market_note":null,"all_clear":false}
"""


class MonitoringAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop") or "rice"
        lang_code = state.get("language", "ml")
        lang_name = "Malayalam" if lang_code == "ml" else "English"

        sys_prompt = MONITORING_SYSTEM_PROMPT.format(language_name=lang_name)
        user_prompt = f"Generate morning briefing for crop={crop} at 45 DAS in Palakkad, Kerala."

        res = await llm_service.generate(sys_prompt, user_prompt, temperature=0.3, max_tokens=500)

        if not res:
            res = {
                "stage_summary": f"{crop.title()} Tillering (45 days)",
                "top_risk": {
                    "risk_type": "disease",
                    "level": "medium",
                    "description": "High humidity increases blast risk today.",
                    "is_urgent": False
                },
                "weather_today": "Humid Warm",
                "recommended_action": "Inspect lower leaves for diamond-shaped blast spots during morning walk.",
                "market_note": None,
                "all_clear": False
            }

        state["advisory"] = state.get("advisory") or {}
        state["advisory"]["morning_briefing"] = res
        return state
