import feedparser
import uuid
import logging
from sqlalchemy import text
from ..database import AsyncSessionLocal
from ..config import settings

logger = logging.getLogger(__name__)


async def run_pest_pipeline():
    """Parse NBAIR RSS feed and generate alerts for farmers."""
    try:
        feed = feedparser.parse(settings.NBAIR_RSS_URL)
        entries = feed.entries[:5] if feed.entries else []

        async with AsyncSessionLocal() as session:
            # Get active farmers
            result = await session.execute(text("SELECT id, district FROM farmers WHERE is_active = true"))
            farmers = result.fetchall()

            for entry in entries:
                title = getattr(entry, "title", "Pest Alert")
                summary = getattr(entry, "summary", "Pest warning reported for Kerala.")

                for farmer in farmers:
                    farmer_id = farmer[0]
                    alert_id = str(uuid.uuid4())
                    await session.execute(text("""
                        INSERT INTO alerts (id, farmer_id, severity, title, message, source_agent, is_read, created_at)
                        VALUES (:id, :farmer_id, 'WARNING', :title, :msg, 'pest_pipeline', false, NOW())
                    """), {
                        "id": alert_id,
                        "farmer_id": farmer_id,
                        "title": title[:200],
                        "msg": summary,
                    })

            await session.commit()
            logger.info("pest_pipeline: generated alerts from %d feed items", len(entries))
    except Exception as e:
        logger.error("pest_pipeline error: %s", str(e))
