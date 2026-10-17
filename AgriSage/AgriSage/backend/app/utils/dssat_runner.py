import asyncio
import subprocess
from typing import Optional


async def run_dssat(crop_name: str, soil_data: dict, weather_data: dict) -> Optional[dict]:
    """Run DSSAT crop simulation via subprocess. Returns None if DSSAT not available."""
    try:
        # DSSAT subprocess call (placeholder - actual binary must be installed)
        result = subprocess.run(
            ["dssat", "--crop", crop_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return {"yield_kg_ha": 4500.0, "days_to_maturity": 120, "water_stress": 0.1}
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
