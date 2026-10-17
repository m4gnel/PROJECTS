"""
MemoryAgent — LangGraph MemorySaver conversation context per farmer_id.
Retrieves and injects prior conversation summary into the pipeline state.
"""
import logging
from typing import Dict, Any

from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)

# In-memory conversation history store keyed by farmer_id
# In production, this is backed by LangGraph's MemorySaver checkpointer.
# The checkpointer is configured at graph compile time in graph.py.
_CONVERSATION_SUMMARIES: Dict[str, str] = {}


async def memory_node(state: AgriSageState) -> Dict[str, Any]:
    """
    MemoryAgent: Loads prior conversation context for the farmer.
    Injects a conversation_summary into the state so the Synthesizer
    can personalise responses based on prior interactions.

    LangGraph MemorySaver handles per-thread persistence automatically via
    the thread_id config passed to graph.ainvoke(). This node adds an
    explicit in-memory lookup as a fast-path supplement for the advisory
    pipeline.
    """
    farmer_id = state.get("farmer_id") or state.get("user_id", "")

    if not farmer_id:
        return {"agent_outputs": {"memory": {"summary": "", "interaction_count": 0}}}

    prior_summary = _CONVERSATION_SUMMARIES.get(farmer_id, "")
    interaction_count = len([k for k in _CONVERSATION_SUMMARIES if k.startswith(farmer_id)])

    mem_dict: Dict[str, Any] = {
        "summary": prior_summary,
        "interaction_count": interaction_count,
        "farmer_id": farmer_id,
    }

    logger.debug("memory_agent_loaded", farmer_id=farmer_id, has_prior=bool(prior_summary))

    return {
        "agent_outputs": {"memory": mem_dict}
    }


def store_memory(farmer_id: str, query: str, answer: str) -> None:
    """
    Called after advisory pipeline completes to update the in-memory summary.
    Keeps a rolling 200-char summary of the last interaction.
    """
    summary = f"Last asked: '{query[:80]}...' Advisory given about {answer[:80]}."
    _CONVERSATION_SUMMARIES[farmer_id] = summary
