import asyncio
import feedparser
from .state import AgriState


async def pest_node(state: AgriState) -> dict:
    """
    Fetches NBAIR RSS feed for pest/disease alerts.
    Returns: {"pest_alerts": [<alert strings>], "agents_completed": ["pest"]}
    """
    try:
        from ..config import settings
        loop = asyncio.get_event_loop()
        feed = await loop.run_in_executor(None, feedparser.parse, settings.NBAIR_RSS_URL)
        crop_name = ""
        if state.get("crop_info"):
            crop_name = (state["crop_info"] or {}).get("crop_name", "").lower()

        alerts = []
        for entry in feed.entries[:10]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            if not crop_name or crop_name in title.lower() or crop_name in summary.lower():
                alerts.append(f"{title}: {summary[:200]}")
        return {"pest_alerts": alerts, "agents_completed": ["pest"]}
    except Exception as e:
        return {"error_messages": [f"pest: {str(e)}"], "agents_completed": ["pest"]}
