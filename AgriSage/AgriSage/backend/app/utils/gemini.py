try:
    import google.generativeai as genai
    _USE_LEGACY = True
except ImportError:
    from google import genai
    _USE_LEGACY = False

from ..config import settings

if _USE_LEGACY:
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    except Exception:
        pass


async def ask_gemini(prompt: str, system_prompt: str = "") -> str:
    """Call Gemini Flash. Returns text. On error returns fallback string."""
    try:
        if _USE_LEGACY:
            model = genai.GenerativeModel(
                model_name=getattr(settings, "LLM_MODEL", "gemini-2.5-flash"),
                system_instruction=system_prompt if system_prompt else None
            )
            response = await model.generate_content_async(prompt)
            return response.text
        else:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            config = {"system_instruction": system_prompt} if system_prompt else None
            response = client.models.generate_content(
                model=getattr(settings, "LLM_MODEL", "gemini-2.5-flash"),
                contents=prompt,
                config=config
            )
            return response.text
    except Exception as e:
        return f"Advisory unavailable: {str(e)}"
