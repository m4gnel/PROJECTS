from .state import AgriState
from ..utils.gemini import ask_gemini


async def crop_node(state: AgriState) -> dict:
    """
    Analyzes crop health from state.crop_info + weather + soil data.
    Uses Gemini Flash to generate crop health assessment.
    Returns: {"agent_findings": ["crop: <assessment>"], "agents_completed": ["crop"]}
    """
    try:
        crop_info = state.get("crop_info") or {}
        weather = state.get("weather_data") or {}
        soil = state.get("soil_data") or {}
        crop_name = crop_info.get("crop_name", "unknown crop") if crop_info else "unknown crop"
        stage = crop_info.get("current_growth_stage", "unknown") if crop_info else "unknown"
        temp = weather.get("temperature", 28) if weather else 28
        humidity = weather.get("humidity", 70) if weather else 70
        prompt = (
            f"Crop: {crop_name}, Stage: {stage}, Temperature: {temp}°C, Humidity: {humidity}%.\n"
            f"Soil: {soil}.\n"
            f"Provide a brief crop health assessment and any concerns in 2-3 sentences."
        )
        assessment = await ask_gemini(prompt, "You are an expert Kerala agricultural advisor.")
        return {"agent_findings": [f"crop: {assessment}"], "agents_completed": ["crop"]}
    except Exception as e:
        return {"error_messages": [f"crop: {str(e)}"], "agents_completed": ["crop"]}
