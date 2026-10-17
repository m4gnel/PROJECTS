import httpx
from typing import Dict, Any
from backend.agents.state import AgriSAGEState
from backend.config import settings


class MarketAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop") or "rice"
        farm_state = state.get("farm_state") or {}
        district = farm_state.get("district") or "Ernakulam"

        market_data = await self.fetch_apmc_prices(crop=crop, district=district)
        state["market_data"] = market_data
        return state

    async def fetch_apmc_prices(self, crop: str, district: str) -> Dict[str, Any]:
        api_key = settings.DATA_GOV_IN_KEY
        if api_key:
            url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            params = {
                "api-key": api_key,
                "format": "json",
                "filters[state]": "Kerala",
                "filters[district]": district,
                "limit": 50
            }
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        data = resp.json()
                        records = data.get("records", [])
                        for r in records:
                            commodity = r.get("commodity", "").lower()
                            if crop.lower() in commodity:
                                return {
                                    "crop": crop,
                                    "district": district,
                                    "min_price": float(r.get("min_price", 2800)),
                                    "max_price": float(r.get("max_price", 3400)),
                                    "modal_price": float(r.get("modal_price", 3200)),
                                    "trend": "stable",
                                    "unit": "Quintal",
                                    "recommendation": f"Current APMC market price in {district} is ₹{r.get('modal_price')}/Quintal.",
                                    "source": "data.gov.in"
                                }
            except Exception:
                pass

        # Fallback Kerala APMC benchmark prices
        benchmarks = {
            "rice": {"min": 2400, "max": 2900, "modal": 2750, "unit": "Quintal"},
            "coconut": {"min": 2800, "max": 3500, "modal": 3200, "unit": "100 nuts"},
            "banana": {"min": 3200, "max": 4200, "modal": 3800, "unit": "Quintal"},
            "rubber": {"min": 16000, "max": 18500, "modal": 17800, "unit": "Quintal"},
            "pepper": {"min": 52000, "max": 58000, "modal": 55000, "unit": "Quintal"},
        }
        b = benchmarks.get(crop.lower(), {"min": 2500, "max": 3200, "modal": 2900, "unit": "Quintal"})

        return {
            "crop": crop,
            "district": district,
            "min_price": b["min"],
            "max_price": b["max"],
            "modal_price": b["modal"],
            "trend": "upward",
            "unit": b["unit"],
            "recommendation": f"Market price for {crop} in {district} is ₹{b['modal']}/{b['unit']}. Recommended to sell.",
            "source": "kerala_apmc_benchmark"
        }


market_agent = MarketAgent()
