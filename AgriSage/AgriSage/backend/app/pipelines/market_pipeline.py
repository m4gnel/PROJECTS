import httpx
import uuid
import logging
from datetime import date
from sqlalchemy import text
from ..database import AsyncSessionLocal
from ..config import settings

logger = logging.getLogger(__name__)

# Default sample commodity price data for Kerala markets if external API is unreachable
DEFAULT_MARKET_DATA = [
    {"commodity": "Rice", "market_name": "Aluva", "district": "Ernakulam", "min_price": 32.0, "max_price": 38.0, "modal_price": 35.0},
    {"commodity": "Coconut", "market_name": "Nedumangad", "district": "Thiruvananthapuram", "min_price": 28.0, "max_price": 34.0, "modal_price": 31.0},
    {"commodity": "Black Pepper", "market_name": "Nedumkandam", "district": "Idukki", "min_price": 580.0, "max_price": 620.0, "modal_price": 600.0},
    {"commodity": "Banana (Nendran)", "market_name": "Thrissur", "district": "Thrissur", "min_price": 42.0, "max_price": 50.0, "modal_price": 46.0},
]


async def run_market_pipeline():
    """Fetch commodity prices from data.gov.in and store in market_prices."""
    try:
        today = date.today()
        records_to_insert = []

        if settings.DATA_GOV_IN_API_KEY:
            try:
                url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
                params = {
                    "api-key": settings.DATA_GOV_IN_API_KEY,
                    "format": "json",
                    "filters[state]": "Kerala",
                    "limit": 50
                }
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        records = resp.json().get("records", [])
                        for r in records:
                            records_to_insert.append({
                                "commodity": r.get("commodity", "Paddy"),
                                "market_name": r.get("market", "Local"),
                                "district": r.get("district", "Ernakulam"),
                                "min_price": float(r.get("min_price", 0.0)),
                                "max_price": float(r.get("max_price", 0.0)),
                                "modal_price": float(r.get("modal_price", 0.0)),
                            })
            except Exception as ex:
                logger.warning("data.gov.in fetch failed: %s, using defaults", ex)

        if not records_to_insert:
            records_to_insert = DEFAULT_MARKET_DATA

        async with AsyncSessionLocal() as session:
            for item in records_to_insert:
                await session.execute(text("""
                    INSERT INTO market_prices (id, commodity, market_name, district, min_price, max_price, modal_price, price_date, fetched_at)
                    VALUES (:id, :commodity, :market_name, :district, :min_price, :max_price, :modal_price, :price_date, NOW())
                """), {
                    "id": str(uuid.uuid4()),
                    "commodity": item["commodity"],
                    "market_name": item["market_name"],
                    "district": item["district"],
                    "min_price": item["min_price"],
                    "max_price": item["max_price"],
                    "modal_price": item["modal_price"],
                    "price_date": today,
                })
            await session.commit()
            logger.info("market_pipeline: inserted %d market records", len(records_to_insert))
    except Exception as e:
        logger.error("market_pipeline error: %s", str(e))
