import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.agents.llm_util import call_gemini_safe

logger = logging.getLogger(__name__)


def is_malayalam(text: str) -> bool:
    """Check if string contains Malayalam Unicode characters (U+0D00 - U+0D7F)."""
    return any('\u0d00' <= char <= '\u0d7f' for char in text)


def is_tamil(text: str) -> bool:
    """Check if string contains Tamil Unicode characters (U+0B80 - U+0BFF)."""
    return any('\u0b80' <= char <= '\u0bff' for char in text)


async def translator_pre_node(state: AgriSageState) -> Dict[str, Any]:
    raw_query = state.get("farmer_query", "")
    if not raw_query:
        return {"language": "en", "farmer_query": ""}

    if is_malayalam(raw_query):
        detected_lang = "ml"
    elif is_tamil(raw_query):
        detected_lang = "ta"
    else:
        detected_lang = "en"

    if detected_lang == "en":
        return {"language": "en", "farmer_query": raw_query}

    # Translate ML/TA query to English for internal agents
    prompt = f"Translate this Malayalam/Tamil text to English. Return ONLY the English translation. No explanation. Text: {raw_query}"
    translated_en = await call_gemini_safe(prompt)
    
    # Fallback heuristic if Gemini key not configured
    if not translated_en:
        translated_en = raw_query

    return {
        "language": detected_lang,
        "farmer_query": translated_en
    }


async def translator_post_node(state: AgriSageState) -> Dict[str, Any]:
    lang = state.get("language", "en")
    answer_en = state.get("final_answer_en", "")

    if lang == "en" or not answer_en:
        return {"final_answer_ml": answer_en}

    prompt = f"Translate this agricultural advice to natural Malayalam. Use simple words a Kerala farmer would understand. Do not translate: specific numbers, crop names, chemical names. Text: {answer_en}"
    answer_ml = await call_gemini_safe(prompt)

    if not answer_ml:
        # Fallback to English if translation service unavailable
        answer_ml = answer_en

    return {"final_answer_ml": answer_ml}
