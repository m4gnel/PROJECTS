import httpx
from .state import AgriState


async def market_node(state: AgriState) -> dict:
    """
    Fetches commodity prices from data.gov.in API.
    Returns: {"market_prices": [{commodity, market, price, date}], "agents_completed": ["market"]}
    """
    try:
        from ..config import settings
        crop_name = ""
        if state.get("crop_info"):
            crop_name = (state["crop_info"] or {}).get("crop_name", "")

        if not settings.DATA_GOV_IN_API_KEY:
            return {
                "market_prices": [],
                "error_messages": ["market: DATA_GOV_IN_API_KEY is not configured"],
                "agents_completed": ["market"],
            }

        params = {
            "api-key": settings.DATA_GOV_IN_API_KEY,
            "format": "json",
            "limit": 10,
            "filters[State]": "Kerala",
        }
        if crop_name:
            params["filters[Commodity]"] = crop_name.capitalize()

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
                params=params
            )
            data = resp.json()

        prices = []
        for record in data.get("records", []):
            prices.append({
                "commodity": record.get("Commodity", ""),
                "market": record.get("Market", ""),
                "price": float(record.get("Modal_Price", 0)),
                "date": record.get("Arrival_Date", ""),
            })
        return {"market_prices": prices, "agents_completed": ["market"]}
    except Exception as e:
        return {"error_messages": [f"market: {str(e)}"], "agents_completed": ["market"]}
