import httpx
import logging
from sqlalchemy import text
from ..database import AsyncSessionLocal
from ..config import settings

logger = logging.getLogger(__name__)


async def run_soil_pipeline():
    """Update fields soil_type from NBSS API or default laterite."""
    try:
        async with AsyncSessionLocal() as session:
            # Fetch fields that have null or empty soil_type
            result = await session.execute(text("SELECT id, latitude, longitude FROM fields WHERE soil_type IS NULL"))
            fields = result.fetchall()

            for f in fields:
                field_id, lat, lon = f[0], f[1], f[2]
                soil_type = "laterite"  # Kerala predominant soil
                try:
                    async with httpx.AsyncClient(timeout=5) as client:
                        resp = await client.get(f"{settings.NBSS_API_URL}/soil", params={"lat": lat, "lon": lon})
                        if resp.status_code == 200:
                            data = resp.json()
                            soil_type = data.get("soil_type", "laterite")
                except Exception:
                    pass

                await session.execute(
                    text("UPDATE fields SET soil_type = :soil_type, updated_at = NOW() WHERE id = :id"),
                    {"soil_type": soil_type, "id": field_id}
                )
            await session.commit()
            logger.info("soil_pipeline: processed %d fields", len(fields))
    except Exception as e:
        logger.error("soil_pipeline error: %s", str(e))
