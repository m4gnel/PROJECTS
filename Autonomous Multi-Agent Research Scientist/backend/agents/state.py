from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    session_id: str
    query: str
    plan: list[str]  # e.g., ["research", "report"]
    sources: list[dict]
    claims: list[dict]
    critic_notes: list[dict]
    market_analysis: dict | None
    startup_concepts: list[dict]
    technical_architecture: str | None
    data_analysis: str | None
    confidence_score: int | None
    toggles: dict  # Tracks which optional stages are enabled
    report: str
    status: str  # 'running', 'completed', 'degraded', 'failed'
    errors: Annotated[list[str], operator.add]
