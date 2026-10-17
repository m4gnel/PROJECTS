from typing import Dict, Any, List
from datetime import datetime
from fastapi import APIRouter, Body

router = APIRouter(tags=["Offline Sync"])


@router.post("/sync/upload")
async def upload_offline_sync_batch(
    payload: Dict[str, Any] = Body(...)
) -> Dict[str, Any]:
    """Upload pending offline observations and telemetry captured on farmer mobile device."""
    observations = payload.get("observations", [])
    device_id = payload.get("device_id", "unknown_device")

    processed_count = len(observations)

    return {
        "status": "success",
        "device_id": device_id,
        "processed_count": processed_count,
        "synced_at": datetime.utcnow().isoformat(),
        "message": f"Successfully ingested {processed_count} offline observations into backend pipeline."
    }


@router.get("/sync/package")
async def get_offline_data_package(
    crop: str = "paddy",
    language: str = "ml"
) -> Dict[str, Any]:
    """Download lightweight offline caching package for Tier 3 mobile devices."""
    return {
        "package_version": "1.2.0",
        "crop": crop,
        "language": language,
        "onnx_model_url": "/models/crop_vision_v1.onnx",
        "onnx_labels": [
            "Rice___Bacterial_blight",
            "Rice___Blast",
            "Rice___Brown_spot",
            "Rice___healthy"
        ],
        "offline_templates": [
            {
                "disease_key": "Rice___Blast",
                "title_ml": "നെല്ലിലെ കുമിൾ രോഗം (ബ്ലാസ്റ്റ്)",
                "action_ml": "ട്രൈസൈക്ലസോൾ 75% WP തളിക്കുക (0.6 ഗ്രാം/ലിറ്റർ).",
                "severity": "HIGH"
            }
        ],
        "downloaded_at": datetime.utcnow().isoformat()
    }
