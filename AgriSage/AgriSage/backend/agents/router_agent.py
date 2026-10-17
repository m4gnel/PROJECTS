import json
import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.agents.llm_util import call_gemini_safe

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the RouterAgent for Agri-SAGE Kerala.
Classify the farmer's query into one or more of these intents ONLY:
WEATHER, PEST, MARKET, FERTILIZER, IRRIGATION, SOWING, CROP_ADVICE, GENERAL
Return ONLY valid JSON matching this schema:
{"intents": ["INTENT1", "INTENT2"], "crop": "detected_crop", "crop_stage": "detected_stage"}

crop: one of [coconut,rice,banana,rubber,tapioca,pepper,cardamom,ginger,turmeric,arecanut,unknown]
crop_stage: one of [seedling,vegetative,flowering,harvest,unknown]
Never return anything except the JSON object.
"""


async def router_node(state: AgriSageState) -> Dict[str, Any]:
    query = state.get("farmer_query", "")
    if not query:
        return {"query_intent": ["GENERAL"], "crop": "unknown", "crop_stage": "unknown"}

    # Keyword fallback for instant local classification
    q_lower = query.lower()
    local_intents = []
    if any(w in q_lower for w in ["rain", "weather", "temperature", "cloud", "storm", "sun"]):
        local_intents.append("WEATHER")
        
    if any(w in q_lower for w in ["pest", "disease", "spot", "bug", "insect", "worm", "whitefly"]):
        local_intents.append("PEST")
        
    if any(w in q_lower for w in ["price", "market", "rate", "cost", "sell", "apmc"]):
        local_intents.append("MARKET")
        
    if any(w in q_lower for w in ["fertilizer", "npk", "urea", "manure", "dose"]):
        local_intents.append("FERTILIZER")
        
    if any(w in q_lower for w in ["water", "irrigation", "drip", "drought"]):
        local_intents.append("IRRIGATION")
        
    if any(w in q_lower for w in ["sow", "plant", "season", "seed"]):
        local_intents.append("SOWING")

    # Detect crop locally
    crop = "unknown"
    for c in ["coconut", "rice", "banana", "rubber", "tapioca", "pepper", "cardamom", "ginger", "turmeric", "arecanut"]:
        if c in q_lower:
            crop = c
            break

    # If LLM key available, try LLM classification
    llm_resp = await call_gemini_safe(query, SYSTEM_PROMPT)
    if llm_resp:
        try:
            clean = llm_resp.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.startswith("```"):
                clean = clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            data = json.loads(clean.strip())
            intents = data.get("intents", [])
            if intents:
                return {
                    "query_intent": intents,
                    "crop": data.get("crop", crop),
                    "crop_stage": data.get("crop_stage", "unknown")
                }
        except Exception as e:
            logger.warning(f"router_agent_json_parse_error: {e}")

    # Fallback to keyword classification
    final_intents = local_intents if local_intents else ["GENERAL"]
    return {
        "query_intent": final_intents,
        "crop": crop,
        "crop_stage": "unknown"
    }
