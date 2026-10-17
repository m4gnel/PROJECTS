from .state import AgriState
from ..utils.gemini import ask_gemini

LANGUAGE_NAMES = {"ml": "Malayalam", "ta": "Tamil", "hi": "Hindi", "en": "English"}


async def translator_node(state: AgriState) -> dict:
    """
    Translates advisory_text to state.language using Gemini Flash.
    Only runs if state.language != "en"
    Returns: {"advisory_text": "<translated text>", "agents_completed": ["translator"]}
    """
    try:
        language = state.get("language", "en")
        advisory = state.get("advisory_text", "")

        if language == "en" or not advisory:
            return {"agents_completed": ["translator"]}

        lang_name = LANGUAGE_NAMES.get(language, "Malayalam")
        system_prompt = (
            f"You are an agricultural translator. Translate to {lang_name}. "
            f"Use simple words that farmers understand. Keep technical terms in English. Be concise."
        )
        translated = await ask_gemini(advisory, system_prompt)
        return {"advisory_text": translated, "agents_completed": ["translator"]}
    except Exception as e:
        return {"error_messages": [f"translator: {str(e)}"], "agents_completed": ["translator"]}
