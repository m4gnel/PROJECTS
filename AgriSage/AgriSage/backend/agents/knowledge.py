from typing import Dict, Any, List
from backend.agents.state import AgriSAGEState
from backend.services.embedding_service import embed_service


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

        # Generate embedding vector with 'query: ' prefix
        query_vec = embed_service.embed_query(query_text)

        # Fallback / Initial curated knowledge chunks
        chunks = [
            {
                "chunk_id": "chunk-101",
                "content": "For Rice Blast control, spray Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L at early tillering stage.",
                "source_authority": "ICAR - National Rice Research Institute",
                "source_tier": 1,
                "rrf_score": 0.85
            },
            {
                "chunk_id": "chunk-102",
                "content": "Maintain field water depth at 2-5 cm to suppress rice blast spore germination.",
                "source_authority": "Kerala Agricultural University (KAU)",
                "source_tier": 1,
                "rrf_score": 0.72
            }
        ]

        state["knowledge_result"] = {
            "query_text": query_text,
            "top_chunks": chunks,
            "count": len(chunks)
        }
        return state
