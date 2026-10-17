import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)


async def alert_node(state: AgriSageState) -> Dict[str, Any]:
    weather = state.get("weather_context", {})
    pest = state.get("pest_alerts", [])
    market = state.get("market_data", {})

    rain = weather.get("rain_mm_24h", 0.0)
    temp = weather.get("temp_c", 28.0)
    flag = weather.get("advice_flag", "NORMAL")
    trend = market.get("trend", "STABLE")

    should_trigger_fcm = False
    reasons = []

    if rain > 50.0:
        should_trigger_fcm = True
        reasons.append("RAIN_ALERT (>50mm)")
    if temp > 38.0:
        should_trigger_fcm = True
        reasons.append("HEAT_ALERT (>38C)")
    if any(p.get("severity") == "HIGH" for p in pest):
        should_trigger_fcm = True
        reasons.append("PEST_ALERT (HIGH severity)")
    if trend == "DOWN":
        should_trigger_fcm = True
        reasons.append("PRICE_DROP")
    if flag == "SPRAY_RISK":
        should_trigger_fcm = True
        reasons.append("SPRAY_RISK")

    if should_trigger_fcm:
        logger.info(f"alert_agent_fcm_triggered: {reasons}")

    return {
        "fcm_triggered": should_trigger_fcm
    }
