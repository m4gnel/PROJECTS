from backend.agents.state import AgriSAGEState
from backend.services.embedding_service import embed_service
from backend.config import settings


class KnowledgeAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop") or "rice"
        vision = state.get("vision_result") or {}
        crop_stage = state.get("crop_stage_result") or {}
        farm_state = state.get("farm_state") or {}

        vision_label = vision.get("label", "")
        stage_name = crop_stage.get("stage_name", "")
        district = farm_state.get("district", "")

        query_text = f"{crop} {vision_label} {stage_name} {district}"

        # This agent has no database-backed retrieval connection.  Returning
        # bundled treatment doses here would present unverified text as live
        # evidence, so provider/model unavailability must remain explicit.
        if not settings.ENABLE_EMBEDDINGS:
            warning = "Authoritative knowledge retrieval is disabled; no treatment guidance was generated."
        elif embed_service.get_model() is None:
            warning = "Authoritative knowledge embedding model is unavailable; no treatment guidance was generated."
        else:
            warning = "Authoritative knowledge database is unavailable; no treatment guidance was generated."

        state.setdefault("warnings", []).append(warning)
        state["knowledge_result"] = {
            "query_text": query_text,
            "top_chunks": [],
            "count": 0,
            "available": False,
            "warning": warning,
        }
        return state
