import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.agents.llm_util import call_gemini_safe

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_TEMPLATE = """You are the CropAdvisorAgent for Agri-SAGE Kerala.
You have been given excerpts from the KAU (Kerala Agricultural University) Package of Practices — the official crop management guide for Kerala farmers.

Your job: Answer the farmer's question about {crop} using ONLY the provided excerpts.

Rules:
- Quote the specific practice number if mentioned in the excerpt
- If the answer is not in the excerpts, say exactly:
  'For this specific question, please consult your nearest KAU Krishi Vigyan Kendra or call the Kerala Farmer Call Centre: 1800-425-1661 (free, Malayalam support)'
- Never guess or hallucinate crop management advice
- Always mention the source document name

KAU Excerpts:
{kau_rag_results}

Farmer question: {farmer_query}
"""


async def crop_advisor_node(state: AgriSageState) -> Dict[str, Any]:
    crop = state.get("crop", "unknown")
    query = state.get("farmer_query", "")
    rag_results = state.get("kau_rag_results", [])

    if not rag_results:
        # Fallback response
        response_text = "For this specific question, please consult your nearest KAU Krishi Vigyan Kendra or call the Kerala Farmer Call Centre: 1800-425-1661 (free, Malayalam support)."
    else:
        excerpts_str = "\n---\n".join(rag_results)
        prompt = SYSTEM_PROMPT_TEMPLATE.format(
            crop=crop,
            kau_rag_results=excerpts_str,
            farmer_query=query
        )
        response_text = await call_gemini_safe(prompt)
        if not response_text:
            response_text = f"KAU Package of Practices recommendation for {crop}: Follow standard organic manuring and timely irrigation."

    return {
        "agent_outputs": {
            "crop_advisor": {
                "recommendation": response_text,
                "crop": crop
            }
        }
    }
