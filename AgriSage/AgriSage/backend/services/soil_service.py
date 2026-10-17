import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class SoilContext:
    district: str
    ph_min: float
    ph_max: float
    texture: str
    organic_carbon: str
    n_status: str
    p_status: str
    k_status: str
    suitable_crops: List[str]


class SoilService:
    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}
        self._load_soil_data()

    def _load_soil_data(self):
        # Locate brain/kerala_soil_data.json relative to project root
        possible_paths = [
            Path(__file__).parent.parent.parent / "brain" / "kerala_soil_data.json",
            Path(__file__).parent.parent / "brain" / "kerala_soil_data.json",
            Path("brain/kerala_soil_data.json")
        ]
        for p in possible_paths:
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        self._data = json.load(f)
                    logger.info("loaded_kerala_soil_data", count=len(self._data), path=str(p))
                    return
                except Exception as e:
                    logger.warning("error_reading_kerala_soil_data", path=str(p), error=str(e))

        logger.warning("kerala_soil_data_json_not_found")

    def get_soil_by_district(self, district: str) -> Optional[SoilContext]:
        if not district:
            return None

        # Case-insensitive matching
        d_lower = district.strip().lower()
        matched_key = None
        for key in self._data:
            if key.lower() == d_lower:
                matched_key = key
                break

        if not matched_key:
            logger.warning(f"soil_service_district_not_found: {district}")
            return None

        info = self._data[matched_key]
        return SoilContext(
            district=matched_key,
            ph_min=float(info.get("ph_min", 5.5)),
            ph_max=float(info.get("ph_max", 6.5)),
            texture=str(info.get("texture", "laterite")),
            organic_carbon=str(info.get("organic_carbon", "medium")),
            n_status=str(info.get("n_status", "medium")),
            p_status=str(info.get("p_status", "medium")),
            k_status=str(info.get("k_status", "medium")),
            suitable_crops=list(info.get("suitable_crops", []))
        )


soil_service = SoilService()


def get_soil_by_district(district: str) -> Optional[SoilContext]:
    return soil_service.get_soil_by_district(district)
