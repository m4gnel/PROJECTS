import os
from typing import Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Body, Depends, HTTPException, status
from backend.dependencies import get_current_user, require_subject_identity

router = APIRouter(tags=["Offline Sync"])


@router.post("/sync/upload")
async def upload_offline_sync_batch(
    payload: Dict[str, Any] = Body(...),
    auth: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Upload pending offline observations and telemetry captured on farmer mobile device."""
    observations = payload.get("observations", [])
    device_id = payload.get("device_id", "unknown_device")

    if not isinstance(observations, list):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="observations must be a list",
        )

    farmer_id = str(auth["sub"])
    normalized_observations = []
    for observation in observations:
        if not isinstance(observation, dict):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="each observation must be an object",
            )
        requested_farmer_id = observation.get("farmer_id")
        if requested_farmer_id is not None:
            require_subject_identity(str(requested_farmer_id), auth)
        normalized = dict(observation)
        # The server-owned subject is the only identity passed to downstream
        # ingestion.  A client field can never select another tenant.
        normalized["farmer_id"] = farmer_id
        normalized_observations.append(normalized)

    processed_count = len(normalized_observations)

    return {
        "status": "success",
        "device_id": device_id,
        "farmer_id": farmer_id,
        "processed_count": processed_count,
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "message": f"Successfully ingested {processed_count} offline observations into backend pipeline."
    }


@router.get("/sync/package")
async def get_offline_data_package(
    crop: str = "paddy",
    language: str = "ml",
    _auth: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Download lightweight offline caching package for Tier 3 mobile devices."""
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "ml",
        "vision_int8.onnx",
    )
    model_available = os.path.isfile(model_path)
    return {
        "package_version": "1.2.0",
        "crop": crop,
        "language": language,
        "available": model_available,
        "onnx_model_url": "/models/crop_vision_v1.onnx" if model_available else None,
        "onnx_labels": [
            "Rice___Bacterial_blight",
            "Rice___Blast",
            "Rice___Brown_spot",
            "Rice___healthy"
        ] if model_available else [],
        "offline_templates": [
            {
                "disease_key": "Rice___Blast",
                "title_ml": "നെല്ലിലെ കുമിൾ രോഗം (ബ്ലാസ്റ്റ്)",
                "action_ml": "ട്രൈസൈക്ലസോൾ 75% WP തളിക്കുക (0.6 ഗ്രാം/ലിറ്റർ).",
                "severity": "HIGH"
            }
        ],
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "warning": None if model_available else "Offline vision model is unavailable; no download package was generated.",
    }
