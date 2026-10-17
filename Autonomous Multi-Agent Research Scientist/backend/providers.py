"""
Concrete ModelProvider implementations for the AMRS model router.
Implements Google (Gemini), Groq, and OpenRouter (via OpenAI SDK).
"""
import os
import time
from typing import Any

from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types

import groq
import openai

from model_router import ModelProvider, ModelResponse, RateLimitError, ProviderUnavailableError
from config import settings

class GeminiProvider(ModelProvider):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self._name = "gemini"
        self.model_name = model_name
        self.client = genai.Client(api_key=settings.gemini_api_key or "DUMMY")

    @property
    def name(self) -> str:
        return self._name

    async def complete(self, prompt: str, **kwargs: Any) -> ModelResponse:
        # Check for FI-01 artificial failure
        if os.getenv("FI_01_FORCE_FAIL_PRIMARY", "false").lower() == "true":
            raise RateLimitError("Artificially triggered RateLimitError for FI-01 testing.")

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return ModelResponse(
                text=response.text or "",
                provider_name=self.name,
                was_fallback=False
            )
        except genai_errors.APIError as e:
            if e.code == 429:
                raise RateLimitError(str(e))
            elif e.code >= 500:
                raise ProviderUnavailableError(str(e))
            raise


class GroqProvider(ModelProvider):
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self._name = "groq"
        self.model_name = model_name
        self.client = groq.AsyncGroq(api_key=settings.groq_api_key or "DUMMY")

    @property
    def name(self) -> str:
        return self._name

    async def complete(self, prompt: str, **kwargs: Any) -> ModelResponse:
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7)
            )
            return ModelResponse(
                text=response.choices[0].message.content or "",
                provider_name=self.name,
                was_fallback=False
            )
        except groq.RateLimitError as e:
            raise RateLimitError(str(e))
        except groq.APIConnectionError as e:
            raise ProviderUnavailableError(str(e))
        except groq.InternalServerError as e:
            raise ProviderUnavailableError(str(e))


class OpenRouterProvider(ModelProvider):
    def __init__(self, model_name: str = "google/gemini-2.5-flash:free"):
        self._name = "openrouter"
        self.model_name = model_name
        self.client = openai.AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key or "DUMMY",
        )

    @property
    def name(self) -> str:
        return self._name

    async def complete(self, prompt: str, **kwargs: Any) -> ModelResponse:
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7)
            )
            return ModelResponse(
                text=response.choices[0].message.content or "",
                provider_name=self.name,
                was_fallback=False
            )
        except openai.RateLimitError as e:
            raise RateLimitError(str(e))
        except openai.APIConnectionError as e:
            raise ProviderUnavailableError(str(e))
        except openai.InternalServerError as e:
            raise ProviderUnavailableError(str(e))

def get_router(role: str, primary: str = "gemini", fallback1: str = "groq", fallback2: str = "openrouter"):
    # Helper to build chains
    from model_router import ModelRouter
    
    mapping = {
        "gemini": GeminiProvider(),
        "groq": GroqProvider(),
        "openrouter": OpenRouterProvider()
    }
    
    chain = []
    if primary in mapping: chain.append(mapping[primary])
    if fallback1 in mapping: chain.append(mapping[fallback1])
    if fallback2 in mapping: chain.append(mapping[fallback2])
    
    return ModelRouter(role=role, chain=chain)
