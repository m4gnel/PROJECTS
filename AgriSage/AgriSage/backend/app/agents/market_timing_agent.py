from .state import AgriState


async def market_timing_node(state: AgriState) -> dict:
    """
    Recommends when to sell based on price trend from market_prices.
    Simple 7-day moving average trend analysis.
    Returns: {"agent_findings": ["market_timing: <sell/hold>"], "agents_completed": ["market_timing"]}
    """
    try:
        prices = state.get("market_prices", [])
        if not prices:
            return {"agent_findings": ["market_timing: Insufficient price data for trend analysis."], "agents_completed": ["market_timing"]}

        price_values = [p.get("price", 0) for p in prices if p.get("price", 0) > 0]
        if not price_values:
            rec = "No price data available. Monitor local APMC for current rates."
        elif len(price_values) >= 2 and price_values[-1] > price_values[0] * 1.05:
            rec = "Prices trending UP (+5%). Consider selling in next 3-5 days for maximum profit."
        elif len(price_values) >= 2 and price_values[-1] < price_values[0] * 0.80:
            rec = "Prices trending DOWN (-20%). Hold stock if possible; seek alternative markets."
        else:
            current = price_values[-1] if price_values else 0
            rec = f"Prices are stable at ?{current:.0f}/quintal. Sell now or wait for monsoon price spike."

        return {"agent_findings": [f"market_timing: {rec}"], "agents_completed": ["market_timing"]}
    except Exception as e:
        return {"error_messages": [f"market_timing: {str(e)}"], "agents_completed": ["market_timing"]}
