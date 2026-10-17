import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.agents.llm_util import call_gemini_safe

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_TEMPLATE = """You are the SynthesizerAgent for Agri-SAGE Kerala.
Combine the following expert reports into one clear, actionable answer for a Kerala farmer.
Rules:
- Start with the most urgent recommendation
- Use simple language (farmer may have 8th grade education)
- Cite which data source each recommendation comes from
- If any data is null or unavailable, skip that section
- Maximum 150 words
- Never contradict KAU (Kerala Agricultural University) Package of Practices
Expert reports: {agent_outputs}
"""


async def synthesizer_node(state: AgriSageState) -> Dict[str, Any]:
    outputs = state.get("agent_outputs", {})

    # Try LLM synthesis if key available
    if outputs:
        prompt = SYSTEM_PROMPT_TEMPLATE.format(agent_outputs=str(outputs))
        llm_answer = await call_gemini_safe(prompt)
        if llm_answer:
            return {"final_answer_en": llm_answer}

    # Deterministic fallback synthesis
    parts = []
    if "weather" in outputs:
        w = outputs["weather"]
        parts.append(f"Weather alert: {w.get('advice_flag', 'NORMAL')} ({w.get('temp_c')}°C, humidity {w.get('humidity_pct')}%).")

    if "pest" in outputs:
        p = outputs["pest"]
        if p.get("highest_severity") != "NONE":
            parts.append(f"Pest alert ({p.get('highest_severity')} severity): Check crop for active infestation.")

    if "market" in outputs:
        m = outputs["market"]
        parts.append(f"Market update ({m.get('crop')}): ₹{m.get('modal_price')}/qtl ({m.get('trend')} trend). Recommendation: {m.get('sell_recommendation')}.")

    if "crop_advisor" in outputs:
        parts.append(outputs["crop_advisor"].get("recommendation", ""))

    if "fertilizer" in outputs:
        f = outputs["fertilizer"]
        parts.append(f"Fertilizer dose for {f.get('crop')}: N: {f.get('nitrogen_g')}g, P: {f.get('phosphorus_g')}g, K: {f.get('potassium_g')}g per plant.")

    if not parts:
        parts.append("Agri-SAGE Advisory: Maintain regular irrigation and monitor your farm for pest signs. Consult Krishi Vigyan Kendra for localized help.")

    summary = " ".join(parts)[:600]
    return {"final_answer_en": summary}
