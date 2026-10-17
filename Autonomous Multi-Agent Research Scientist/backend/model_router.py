"""
Model Router — Multi-provider fallback with circuit breaker.

Implements TRD §3.2: every agent call is wrapped in this router, never a
direct hardcoded API call. If a provider fails (rate-limit or unavailable),
it is marked "open" (skipped) and the next provider in the chain is tried.

If ALL providers in a chain are exhausted, the call raises
AllProvidersExhaustedError rather than silently failing.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class RateLimitError(Exception):
    """Raised when a provider returns a rate-limit response (e.g., 429)."""


class ProviderUnavailableError(Exception):
    """Raised when a provider is down or unreachable."""


class AllProvidersExhaustedError(Exception):
    """Raised when every provider in the fallback chain has failed."""

    def __init__(self, role: str, last_error: Exception | None = None) -> None:
        self.role = role
        self.last_error = last_error
        super().__init__(
            f"All providers exhausted for role '{role}'. "
            f"Last error: {last_error}"
        )


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ModelResponse:
    """Structured response from a model provider."""

    text: str
    provider_name: str
    was_fallback: bool


# ---------------------------------------------------------------------------
# Provider protocol
# ---------------------------------------------------------------------------

class ModelProvider(ABC):
    """Abstract base for an LLM provider that the router can call."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this provider (e.g., 'gemini', 'groq')."""
        ...

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: Any) -> ModelResponse:
        """
        Send a prompt to the provider and return a ModelResponse.

        Must raise RateLimitError or ProviderUnavailableError on failure —
        the router catches these to trigger fallback.
        """
        ...


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

@dataclass
class ModelRouter:
    """
    Circuit-breaker router that walks an ordered provider chain.

    Each agent role is mapped to a primary model + ordered fallback list.
    On RateLimitError or ProviderUnavailableError the failing provider is
    marked "open" (skipped) and the next provider is tried.
    """

    role: str
    chain: list[ModelProvider]
    breaker_state: dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        self.breaker_state = {p.name: "closed" for p in self.chain}

    async def call(self, prompt: str, **kwargs: Any) -> ModelResponse:
        """
        Try each provider in order, skipping those whose circuit is open.

        Returns a ModelResponse on success.
        Raises AllProvidersExhaustedError if every provider fails.
        """
        last_error: Exception | None = None
        is_fallback = False

        for provider in self.chain:
            if self.breaker_state[provider.name] == "open":
                is_fallback = True
                continue

            try:
                response = await provider.complete(prompt, **kwargs)
                # Successful call — ensure breaker stays closed and tag
                # whether a fallback served this request.
                self.breaker_state[provider.name] = "closed"
                response.was_fallback = is_fallback
                return response

            except (RateLimitError, ProviderUnavailableError) as exc:
                last_error = exc
                self.breaker_state[provider.name] = "open"
                is_fallback = True
                continue

        raise AllProvidersExhaustedError(self.role, last_error)
