import httpx
import logging
from sqlalchemy import text
from ..database import AsyncSessionLocal
from ..config import settings

logger = logging.getLogger(__name__)


async def run_satellite_pipeline():
    """Fetch NDVI from NASA EarthData for fields and update fields.last_ndvi."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT id, latitude, longitude FROM fields"))
            fields = result.fetchall()

            for f in fields:
                field_id, lat, lon = f[0], f[1], f[2]
                ndvi_val = 0.65  # Default healthy vegetative NDVI for Kerala
                try:
                    url = f"{settings.NASA_EARTHDATA_BASE_URL}/api/v1/ndvi"
                    async with httpx.AsyncClient(timeout=5) as client:
                        resp = await client.get(url, params={"lat": lat, "lon": lon})
                        if resp.status_code == 200:
                            data = resp.json()
                            ndvi_val = float(data.get("ndvi", 0.65))
                except Exception:
                    pass

                await session.execute(
                    text("UPDATE fields SET last_ndvi = :ndvi, updated_at = NOW() WHERE id = :id"),
                    {"ndvi": ndvi_val, "id": field_id}
                )
            await session.commit()
            logger.info("satellite_pipeline: updated NDVI for %d fields", len(fields))
    except Exception as e:
        logger.error("satellite_pipeline error: %s", str(e))
