import os
import json

try:
    import onnxruntime as ort
except ImportError:
    ort = None

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from backend.agents.state import AgriSAGEState

# Module-level class definitions load
CLASSES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "disease_classes.json")
if os.path.exists(CLASSES_PATH):
    with open(CLASSES_PATH, "r", encoding="utf-8") as f:
        DISEASE_CLASSES = json.load(f)
else:
    DISEASE_CLASSES = []


class VisionAgent:
    _session = None

    @classmethod
    def get_session(cls):

        """Class-level singleton for ONNX inference session."""
        if cls._session is None and ort is not None:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "ml",
                "vision_int8.onnx",
            )
            if os.path.isfile(model_path):
                try:
                    cls._session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
                except Exception as e:
                    logger.warning(f"failed_loading_onnx_model: {e}")
        return cls._session

    @staticmethod
    def _unavailable_result(reason: str) -> dict:
        """Return an explicit no-evidence result instead of a guessed diagnosis."""
        return {
            "label": "out_of_distribution",
            "common_name": "Diagnosis unavailable",
            "ml_name": "രോഗനിർണയം ലഭ്യമല്ല",
            "confidence_score": 0.0,
            "severity": "unknown",
            "affected_area_pct": 0.0,
            "top_predictions": [],
            "quality_score": 0.0,
            "out_of_distribution": True,
            "available": False,
            "quality_rejection_reason": reason,
        }

    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        images = state.get("images", [])

        if not images:
            state["vision_result"] = self._unavailable_result("No image provided")
            return state

        # An object key is not image evidence.  The current API passes storage
        # keys to this agent and does not provide a download/decode adapter.
        # Refuse to manufacture a disease label until a real inference path is
        # configured and the model artifact is present.
        session = self.get_session()
        if session is None:
            state["vision_result"] = self._unavailable_result(
                "Vision model artifact is unavailable"
            )
            return state

        state["vision_result"] = self._unavailable_result(
            "Vision inference adapter is not configured for stored image keys"
        )
        return state
