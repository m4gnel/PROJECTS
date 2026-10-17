from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


@dataclass
class SimulationParams:
    crop: str
    stage_code: str
    gdd_accumulated: float
    soil_type: str = "clay_loam"
    soil_nitrogen_ppm: float = 25.0
    daily_temp_c: float = 28.0
    daily_rainfall_mm: float = 5.0
    relative_humidity_pct: float = 75.0
    disease_severity: float = 0.20


@dataclass
class ScenarioResult:
    id: str
    label: str
    action: str
    expected_yield_kgha: float
    expected_cost_inr: float
    expected_net_return_inr: float
    risk_level: str
    water_stress_index: float
    nitrogen_stress_index: float
    modelled_estimate: bool = True


class SimulationEngineInterface(ABC):
    @abstractmethod
    async def run_simulation(self, params: SimulationParams) -> Dict[str, Any]:
        """Run crop simulation and return 3-way scenarios."""
        pass
