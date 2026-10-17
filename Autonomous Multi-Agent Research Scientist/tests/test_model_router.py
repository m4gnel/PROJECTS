import pytest
import asyncio
import sys
import os

# Add backend to path so we can import model_router
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from model_router import ModelRouter, ModelResponse, RateLimitError, ProviderUnavailableError, AllProvidersExhaustedError, ModelProvider

class MockProvider(ModelProvider):
    def __init__(self, name: str, behavior: str):
        self._name = name
        self.behavior = behavior # 'success', 'rate_limit', 'unavailable'
        
    @property
    def name(self) -> str:
        return self._name

    async def complete(self, prompt: str, **kwargs) -> ModelResponse:
        if self.behavior == 'rate_limit':
            raise RateLimitError("Mock Rate Limit")
        elif self.behavior == 'unavailable':
            raise ProviderUnavailableError("Mock Unavailable")
        else:
            return ModelResponse(text=f"Success from {self.name}", provider_name=self.name, was_fallback=False)

@pytest.mark.asyncio
async def test_router_success_primary():
    router = ModelRouter(role="test", chain=[
        MockProvider("p1", "success"),
        MockProvider("p2", "success")
    ])
    
    resp = await router.call("hello")
    assert resp.provider_name == "p1"
    assert not resp.was_fallback

@pytest.mark.asyncio
async def test_router_fallback_on_rate_limit():
    router = ModelRouter(role="test", chain=[
        MockProvider("p1", "rate_limit"),
        MockProvider("p2", "success")
    ])
    
    resp = await router.call("hello")
    assert resp.provider_name == "p2"
    assert resp.was_fallback
    assert router.breaker_state["p1"] == "open"

@pytest.mark.asyncio
async def test_router_all_exhausted():
    router = ModelRouter(role="test", chain=[
        MockProvider("p1", "rate_limit"),
        MockProvider("p2", "unavailable")
    ])
    
    with pytest.raises(AllProvidersExhaustedError):
        await router.call("hello")
