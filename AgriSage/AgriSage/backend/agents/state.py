from typing import TypedDict, Optional, Annotated, List, Dict, Any
import operator


class AgriSAGEState(TypedDict, total=False):
    # Core farmer & query input
    farmer_id: str
    user_id: str
    observation_id: str
    farmer_query: str
    language: str
    location: Dict[str, Any]
    crop: Optional[str]
    crop_stage: Optional[str]
    query_intent: List[str]
    images: List[Dict[str, Any]]
    farm_state: Optional[Dict[str, Any]]

    # Contexts & Realtime Data
    weather_context: Dict[str, Any]
    soil_context: Dict[str, Any]
    pest_alerts: List[Dict[str, Any]]
    market_data: Dict[str, Any]
    kau_rag_results: List[str]
    dssat_output: Dict[str, Any]

    # Agent results
    vision_result: Optional[Dict[str, Any]]
    weather_result: Optional[Dict[str, Any]]
    crop_stage_result: Optional[Dict[str, Any]]
    knowledge_result: Optional[Dict[str, Any]]
    critic_result: Optional[Dict[str, Any]]
    scheme_result: Optional[Dict[str, Any]]
    simulation_result: Optional[Dict[str, Any]]
    decision_result: Optional[Dict[str, Any]]
    advisory: Optional[Dict[str, Any]]

    # Merged output dict for parallel agents
    agent_outputs: Annotated[Dict[str, Any], operator.ior]

    # Final synthesized outputs
    final_answer_en: str
    final_answer_ml: str
    fcm_triggered: bool
    error: Optional[str]

    # Control flags
    run_simulation: bool
    confidence_state: Optional[str]

    # Telemetry & Accumulators
    warnings: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]
    pipeline_start_ms: Optional[int]
    generation_ms: Optional[int]


# Alias for prompt convention compatibility
AgriSageState = AgriSAGEState
