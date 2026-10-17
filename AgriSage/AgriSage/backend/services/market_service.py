import httpx
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from backend.config import settings

logger = logging.getLogger(__name__)


@dataclass
class MarketContext:
    crop_name: str
    variety: str
    district: str
    min_price: float
    max_price: float
    modal_price: float
    date: str
    trend: str  # UP | DOWN | STABLE
    sell_recommendation: str  # SELL | HOLD | MONITOR


# In-memory storage for market records (useful in dev/testing environments)
_MARKET_DB: List[Dict[str, Any]] = []


class MarketService:
    def calculate_trend(self, today_price: float, avg_7day: float) -> str:
        if avg_7day <= 0:
            return "STABLE"
        if today_price > avg_7day * 1.05:
            return "UP"
        if today_price < avg_7day * 0.95:
            return "DOWN"
        return "STABLE"

    def calculate_recommendation(self, trend: str) -> str:
        if trend == "UP":
            return "SELL"
        if trend == "DOWN":
            return "HOLD"
        return "MONITOR"

    async def fetch_and_upsert_prices(self) -> List[Dict[str, Any]]:
        api_key = getattr(settings, "DATA_GOV_IN_KEY", None)
        if not api_key:
            logger.warning("market_service_missing_api_key")
            return _MARKET_DB

        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        headers = {"api-key": api_key}
        params = {
            "filters[state]": "Kerala",
            "format": "json",
            "limit": 100,
            "offset": 0
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url, headers=headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    records = data.get("records", [])
                    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    for rec in records:
                        item = {
                            "crop_name": rec.get("commodity", "").lower(),
                            "variety": rec.get("variety", "local"),
                            "district": rec.get("district", "Ernakulam"),
                            "min_price": float(rec.get("min_price", 0.0)),
                            "max_price": float(rec.get("max_price", 0.0)),
                            "modal_price": float(rec.get("modal_price", 0.0)),
                            "date": rec.get("arrival_date", today_str)
                        }
                        _MARKET_DB.append(item)
                    return _MARKET_DB
                elif resp.status_code in (401, 403):
                    logger.warning("market_service_unauthorized_key", status=resp.status_code)
        except Exception as e:
            logger.warning("market_service_fetch_error", error=str(e))

        return _MARKET_DB

    async def get_market_data(self, crop: str = "coconut", district: str = "Ernakulam") -> MarketContext:
        crop_lower = crop.lower()
        district_lower = district.lower()
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Search in _MARKET_DB
        matching = [
            m for m in _MARKET_DB
            if crop_lower in m["crop_name"].lower() and district_lower in m["district"].lower()
        ]

        if matching:
            latest = matching[-1]
            avg_7day = sum(m["modal_price"] for m in matching) / len(matching)
            trend = self.calculate_trend(latest["modal_price"], avg_7day)
            rec = self.calculate_recommendation(trend)
            return MarketContext(
                crop_name=latest["crop_name"],
                variety=latest["variety"],
                district=latest["district"],
                min_price=latest["min_price"],
                max_price=latest["max_price"],
                modal_price=latest["modal_price"],
                date=latest["date"],
                trend=trend,
                sell_recommendation=rec
            )

        # Default fallback values for Kerala markets
        default_prices = {
            "coconut": (28.0, 34.0, 31.0),
            "rice": (32.0, 42.0, 38.0),
            "banana": (35.0, 48.0, 42.0),
            "rubber": (160.0, 185.0, 175.0),
            "pepper": (520.0, 580.0, 550.0),
            "cardamom": (1400.0, 1900.0, 1650.0)
        }
        prices = default_prices.get(crop_lower, (30.0, 45.0, 38.0))
        return MarketContext(
            crop_name=crop,
            variety="local",
            district=district,
            min_price=prices[0],
            max_price=prices[1],
            modal_price=prices[2],
            date=today_str,
            trend="STABLE",
            sell_recommendation="MONITOR"
        )


market_service = MarketService()
