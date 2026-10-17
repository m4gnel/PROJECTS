from .state import AgriState


async def irrigation_node(state: AgriState) -> dict:
    """
    Calculates irrigation schedule from ETo (Penman-Monteith simplified).
    Returns: {"agent_findings": ["irrigation: <schedule>"], "agents_completed": ["irrigation"]}
    """
    try:
        weather = state.get("weather_data") or {}
        temp = weather.get("temperature", 28.0)
        humidity = weather.get("humidity", 70.0)
        wind = weather.get("wind_speed", 10.0)
        rain = weather.get("rainfall_mm", 0.0)

        # Simplified ETo: Hargreaves approximation
        eto = max(0, 0.0023 * (temp + 17.8) * (35 - temp) ** 0.5 * 2.0)
        net_water_need = max(0, eto - rain)

        if net_water_need < 2:
            schedule = "No irrigation needed today — rainfall is sufficient."
        elif net_water_need < 5:
            schedule = f"Irrigate 20-25 mm every 3 days for next 7 days."
        else:
            schedule = f"Irrigate {int(net_water_need * 3):.0f} mm every 2 days for next 7 days."

        return {"agent_findings": [f"irrigation: {schedule}"], "agents_completed": ["irrigation"]}
    except Exception as e:
        return {"error_messages": [f"irrigation: {str(e)}"], "agents_completed": ["irrigation"]}
