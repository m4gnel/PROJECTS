"""
SchedulerAgent (Agent 12) — Generates today's farming task list from all agent outputs.
Produces a prioritised, time-aware list of actionable tasks for the farmer's day.
"""
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List

from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)


def _get_time_context() -> Dict[str, Any]:
    """Returns current IST time context for scheduling."""
    now_utc = datetime.now(timezone.utc)
    # IST = UTC + 5:30
    hour_ist = (now_utc.hour + 5) % 24 + (1 if now_utc.minute >= 30 else 0)
    return {
        "hour_ist": hour_ist,
        "is_morning": 5 <= hour_ist < 12,
        "is_afternoon": 12 <= hour_ist < 17,
        "is_evening": 17 <= hour_ist < 21,
    }


async def scheduler_node(state: AgriSageState) -> Dict[str, Any]:
    """
    SchedulerAgent: Generates today's prioritised task list from all agent outputs.

    Task priority:
      P1 — Critical (CRITICAL pest/weather alert)
      P2 — Time-sensitive (spray window, irrigation)
      P3 — Standard (fertilizer, monitoring)
      P4 — Advisory (market, crop stage check)
    """
    agent_outputs = state.get("agent_outputs", {})
    weather = state.get("weather_context", {})
    pest_alerts = state.get("pest_alerts", [])
    crop = state.get("crop", "crop")
    time_ctx = _get_time_context()

    tasks: List[Dict[str, Any]] = []
    task_id = 1

    # ─── P1: Critical Alerts ───
    if any(a.get("severity") == "HIGH" for a in pest_alerts):
        tasks.append({
            "id": task_id,
            "priority": 1,
            "title": "Inspect field for pest outbreak",
            "detail": "High-severity pest alert detected. Inspect crops immediately and document affected area.",
            "time_suggestion": "Before 10:00 AM",
            "category": "PEST",
            "icon": "🐛",
        })
        task_id += 1

    advice_flag = weather.get("advice_flag", "NORMAL")
    if advice_flag == "FLOOD_RISK":
        tasks.append({
            "id": task_id,
            "priority": 1,
            "title": "Clear drainage channels",
            "detail": "Heavy rain (>50mm) forecast. Clear field drainage to prevent waterlogging.",
            "time_suggestion": "Immediately",
            "category": "WEATHER",
            "icon": "⛈️",
        })
        task_id += 1

    # ─── P2: Spray Window ───
    if advice_flag == "SPRAY_RISK" and time_ctx["is_morning"]:
        tasks.append({
            "id": task_id,
            "priority": 2,
            "title": "Delay chemical spraying today",
            "detail": "Humidity >85% — spraying will be ineffective. Reschedule for a drier day.",
            "time_suggestion": "All day",
            "category": "SPRAY",
            "icon": "💧",
        })
        task_id += 1
    elif advice_flag == "NORMAL" and time_ctx["is_morning"]:
        # Spray window open
        tasks.append({
            "id": task_id,
            "priority": 2,
            "title": "Optimal spray window open",
            "detail": "Weather conditions are ideal for pesticide/fungicide application (low humidity, low wind).",
            "time_suggestion": "07:00 AM – 11:00 AM",
            "category": "SPRAY",
            "icon": "✅",
        })
        task_id += 1

    # ─── P2: Irrigation ───
    irrigation = (agent_outputs.get("irrigation") or {})
    if irrigation.get("irrigation_mm", 0) > 0:
        tasks.append({
            "id": task_id,
            "priority": 2,
            "title": f"Irrigate {crop}",
            "detail": irrigation.get("recommendation", "Irrigate as per schedule."),
            "time_suggestion": "Morning or Evening",
            "category": "IRRIGATION",
            "icon": "💧",
        })
        task_id += 1

    # ─── P3: Fertilizer ───
    fertilizer = (agent_outputs.get("fertilizer") or {})
    if fertilizer and fertilizer.get("nitrogen_g"):
        tasks.append({
            "id": task_id,
            "priority": 3,
            "title": f"Check fertilizer schedule for {fertilizer.get('crop', crop)}",
            "detail": (
                f"Recommended dose: N={fertilizer.get('nitrogen_g')}g, "
                f"P={fertilizer.get('phosphorus_g')}g, "
                f"K={fertilizer.get('potassium_g')}g. "
                f"{fertilizer.get('advice', '')}"
            ),
            "time_suggestion": "This week",
            "category": "FERTILIZER",
            "icon": "🌿",
        })
        task_id += 1

    # ─── P4: Market Check ───
    market = (agent_outputs.get("market") or {})
    if market and market.get("sell_recommendation") == "SELL":
        tasks.append({
            "id": task_id,
            "priority": 4,
            "title": f"Market price alert for {market.get('crop', crop)}",
            "detail": (
                f"Current price: ₹{market.get('modal_price', 'N/A')}/qtl "
                f"(Trend: {market.get('trend', 'STABLE')}). "
                f"Recommendation: {market.get('sell_recommendation', 'HOLD')}."
            ),
            "time_suggestion": "Today",
            "category": "MARKET",
            "icon": "💰",
        })
        task_id += 1

    # ─── P4: Weather Advisory ───
    weather_advice = (agent_outputs.get("weather") or {})
    if weather_advice:
        tasks.append({
            "id": task_id,
            "priority": 4,
            "title": "Daily weather check",
            "detail": (
                f"Current: {weather.get('temp_c', 'N/A')}°C, "
                f"Humidity: {weather.get('humidity_pct', 'N/A')}%, "
                f"Rain: {weather.get('rain_mm_24h', 0)}mm. "
                f"Flag: {advice_flag}."
            ),
            "time_suggestion": "Morning",
            "category": "WEATHER",
            "icon": "🌤️",
        })
        task_id += 1

    # Always include a general monitoring task if nothing else critical
    if not tasks:
        tasks.append({
            "id": 1,
            "priority": 3,
            "title": f"Monitor {crop} field",
            "detail": "Regular inspection of plants for any signs of disease, pest, or stress.",
            "time_suggestion": "Morning",
            "category": "MONITORING",
            "icon": "👁️",
        })

    # Sort by priority ascending (P1 first)
    tasks.sort(key=lambda t: t["priority"])

    scheduler_result = {
        "tasks": tasks,
        "task_count": len(tasks),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "generated_at_ist_hour": time_ctx["hour_ist"],
    }

    logger.info("scheduler_agent_complete", task_count=len(tasks))

    return {
        "agent_outputs": {"scheduler": scheduler_result}
    }
