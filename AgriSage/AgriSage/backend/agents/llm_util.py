import asyncio
import logging
from typing import List, Optional
from backend.config import settings

logger = logging.getLogger(__name__)


async def call_gemini_safe(prompt: str, system_prompt: str = "", max_retries: int = 2) -> str:
    """
    Rate-limit safe (15 RPM free tier) Gemini Flash invocation.
    Includes exponential backoff retries on rate limit / 429 status codes.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        logger.warning("call_gemini_safe: GEMINI_API_KEY missing, using fallback response")
        return ""

    import httpx
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    if system_prompt:
        payload["system_instruction"] = {"parts": [{"text": system_prompt}]}

    for attempt in range(max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "").strip()
                elif resp.status_code == 429:
                    wait_sec = 4 * (attempt + 1)
                    logger.warning(f"Gemini 429 rate limit hit, backing off {wait_sec}s...")
                    await asyncio.sleep(wait_sec)
                    continue
                else:
                    logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.warning(f"Gemini call error on attempt {attempt+1}: {e}")
            if attempt < max_retries:
                await asyncio.sleep(2 * (attempt + 1))
                continue

    return ""
