import json
import httpx
from typing import Optional, Dict, Any
from backend.config import settings

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)



class LLMService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        self.ollama_url = settings.OLLAMA_URL

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1500
    ) -> Optional[Dict[str, Any]]:
        """
        Generate structured JSON response using Gemini 1.5 Pro or Ollama fallback.
        Retries once if response is not valid JSON. Returns None on persistent failure.
        """
        prompt = user_prompt
        for attempt in range(2):
            try:
                raw_response = await self._call_llm(system_prompt, prompt, temperature, max_tokens)
                if not raw_response:
                    continue

                # Strip markdown code blocks if present
                clean = raw_response.strip()
                if clean.startswith("```json"):
                    clean = clean[7:]
                if clean.startswith("```"):
                    clean = clean[3:]
                if clean.endswith("```"):
                    clean = clean[:-3]
                clean = clean.strip()

                parsed = json.loads(clean)
                if isinstance(parsed, dict):
                    return parsed
            except Exception as e:
                logger.warning("llm_parse_error", attempt=attempt + 1, error=str(e))
                prompt = user_prompt + "\n\nCRITICAL: Output ONLY valid JSON. No other text."

        return None

    async def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        async with httpx.AsyncClient(timeout=15.0) as client:
            if self.gemini_key:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
                payload = {
                    "system_instruction": {
                        "parts": [{"text": system_prompt}]
                    },
                    "contents": [
                        {"parts": [{"text": user_prompt}]}
                    ],
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": max_tokens,
                        "responseMimeType": "application/json"
                    }
                }
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
            else:
                # Ollama API fallback
                url = f"{self.ollama_url.rstrip('/')}/api/chat"
                payload = {
                    "model": "llama3",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "format": "json",
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    },
                    "stream": False
                }
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("message", {}).get("content", "")

        return None


llm_service = LLMService()
