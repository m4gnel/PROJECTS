import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)


async def analytics_node(state: AgriSageState) -> Dict[str, Any]:
    farmer_id = state.get("farmer_id") or state.get("user_id") or "anonymous"
    intents = state.get("query_intent", [])
    gen_ms = state.get("generation_ms", 0)

    logger.info(
        "farm_analytics_logged",
        farmer_id=farmer_id,
        intents=intents,
        generation_ms=gen_ms,
        fcm_triggered=state.get("fcm_triggered", False)
    )

    return {
        "logged": True
    }
