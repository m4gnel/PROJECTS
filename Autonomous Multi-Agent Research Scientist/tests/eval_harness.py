"""
AMRS Evaluation Harness for Fact Checker
"""
import sys
import os
import asyncio
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from agents.fact_checker import fact_checker_node
from agents.state import AgentState
from model_router import ModelRouter, ModelProvider, ModelResponse

class DummyEvaluatorProvider(ModelProvider):
    def __init__(self):
        self._name = "dummy"

    @property
    def name(self) -> str:
        return self._name

    async def complete(self, prompt: str, **kwargs) -> ModelResponse:
        # Just return a mock JSON response based on what Fact Checker expects
        mock_json = '''
        [
            {
                "claim_text": "Water boils at 100 degrees Celsius at sea level.",
                "verification_status": "verified",
                "supporting_source_ids": ["src-123", "src-456"],
                "conflicting_source_ids": []
            }
        ]
        '''
        return ModelResponse(text=mock_json, provider_name=self.name, was_fallback=False)


async def run_eval_harness():
    print("Running Fact Checker Evaluation Harness...")
    router = ModelRouter(role="fact_checker", chain=[DummyEvaluatorProvider()])
    
    # Mock supabase client
    supabase_mock = MagicMock()
    supabase_mock.table().insert().execute.return_value.data = [{"id": "claim-999"}]
    
    config = {
        "configurable": {
            "supabase": supabase_mock,
            "fact_checker_router": router
        }
    }
    
    state = AgentState(
        session_id="test-session-001",
        query="Boiling point of water",
        plan=[],
        sources=[
            {"id": "src-123", "title": "Physics 101", "url": "http://physics.org"},
            {"id": "src-456", "title": "Chemistry Basics", "url": "http://chem.org"}
        ],
        claims=[],
        critic_notes=[],
        market_analysis=None,
        startup_concepts=[],
        technical_architecture=None,
        data_analysis=None,
        confidence_score=None,
        toggles={},
        report="",
        status="running",
        errors=[]
    )
    
    result = await fact_checker_node(state, config)
    print("Evaluation Result:", result)
    
    assert len(result["claims"]) == 1
    assert result["claims"][0]["id"] == "claim-999"
    print("Fact Checker golden path evaluation passed.")

if __name__ == "__main__":
    asyncio.run(run_eval_harness())
