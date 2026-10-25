"""
NDVI Service — Satellite Vegetation Health Index Provider.
 Provides an explicit unavailable result until a provider-backed satellite
 adapter is configured.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("agrisage.services.ndvi")

class NDVIService:
    """
    Retrieves satellite NDVI data for given GPS coordinates or field boundaries.
    Calculates crop health metrics:
    - NDVI > 0.7: Excellent Vigor (Dense green foliage)
    - 0.5 - 0.7: Good / Moderate Vigor
    - 0.3 - 0.5: Stress / Low Biomass (Possible pest, drought, or disease)
    - < 0.3: Soil / Water / Non-vegetation
    """

    def __init__(self, earthdata_token: Optional[str] = None):
        self.earthdata_token = earthdata_token

    async def get_field_ndvi(
        self,
        lat: float,
        lon: float,
        field_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch current and historical 14-day NDVI timeseries for a given coordinate.
        """
        # This service has no implemented satellite adapter.  Cached or
        # deterministic values must not be labelled as current Sentinel-2
        # observations.
        return {
            "available": False,
            "field_id": field_id,
            "latitude": lat,
            "longitude": lon,
            "current_ndvi": None,
            "health_status": "UNKNOWN",
            "recommendation": "Satellite vegetation data is unavailable; verify crop health in the field.",
            "satellite_source": "unavailable",
            "observation_date": None,
            "historical_14d": [],
            "warning": "No provider-backed NDVI observation is available.",
        }

ndvi_service = NDVIService()
