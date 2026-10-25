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


def is_hindi(text: str) -> bool:
    return any('\u0900' <= char <= '\u097f' for char in text)


def is_telugu(text: str) -> bool:
    return any('\u0c00' <= char <= '\u0c7f' for char in text)


def is_punjabi(text: str) -> bool:
    return any('\u0a00' <= char <= '\u0a7f' for char in text)


async def translator_pre_node(state: AgriSageState) -> Dict[str, Any]:
    raw_query = state.get("farmer_query", "")
    if not raw_query:
        return {"language": "en", "farmer_query": ""}

    if is_malayalam(raw_query):
        detected_lang = "ml"
    elif is_tamil(raw_query):
        detected_lang = "ta"
    elif is_hindi(raw_query):
        detected_lang = "hi"
    elif is_telugu(raw_query):
        detected_lang = "te"
    elif is_punjabi(raw_query):
        detected_lang = "pa"
    else:
        detected_lang = "en"

    if detected_lang == "en":
        return {"language": "en", "farmer_query": raw_query}

    # Translate ML/TA query to English for internal agents
    prompt = f"Translate this {detected_lang} farmer question to English. Return ONLY the English translation. No explanation. Text: {raw_query}"
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

    language_names = {"ml": "Malayalam", "ta": "Tamil", "hi": "Hindi", "te": "Telugu", "pa": "Punjabi"}
    target_language = language_names.get(lang, "the farmer's selected language")
    prompt = f"Translate this agricultural advice to natural {target_language}. Use simple words a farmer would understand. Do not translate specific numbers, crop names, or chemical names. Text: {answer_en}"
    answer_ml = await call_gemini_safe(prompt)

    if not answer_ml:
        # Fallback to English if translation service unavailable
        answer_ml = answer_en

    return {"final_answer_ml": answer_ml}
