# Legacy models
from backend.models.db.farms import (
    User, OTPSession, RefreshToken, Farm, Field, SoilProfile, CropCycle, Observation, Image
)

# Core schema models
from backend.models.db.core import (
    Farmer as CoreFarmer,
    FCMToken as CoreFCMToken,
    CoreFarm,
    CoreField
)

# Realtime schema models
from backend.models.db.realtime import (
    WeatherCache, WeatherForecast, MarketPrice, PestAlert, PestAlertCrop,
    SoilZone, IMDRainfall, NDVIReading, MSPReference
)

# Agents schema models
from backend.models.db.agents import (
    AdvisorySession, AdvisoryMessage, AgentInvocation, KauDocument,
    LangGraphCheckpoint, LangGraphCheckpointWrite
)

# Intelligence schema models
from backend.models.db.intelligence import (
    FieldObservation, CropStage, IrrigationSchedule, FertiliserPlan
)

# Alerts schema models
from backend.models.db.alerts import (
    FarmerAlert, FCMDeliveryLog
)

# Market schema models
from backend.models.db.market import (
    MarketRecommendation, PriceSubscription
)

# Analytics schema models
from backend.models.db.analytics import (
    FarmSeasonAnalytics, AgentPerformance, PlatformMetrics, AdvisoryFeedback
)

# System schema models
from backend.models.db.system import (
    AuditLog, APIRateLimit
)

__all__ = [
    # Legacy
    "User",
    "OTPSession",
    "RefreshToken",
    "Farm",
    "Field",
    "SoilProfile",
    "CropCycle",
    "Observation",
    "Image",

    # Core
    "CoreFarmer",
    "CoreFCMToken",
    "CoreFarm",
    "CoreField",

    # Realtime
    "WeatherCache",
    "WeatherForecast",
    "MarketPrice",
    "PestAlert",
    "PestAlertCrop",
    "SoilZone",
    "IMDRainfall",
    "NDVIReading",
    "MSPReference",

    # Agents
    "AdvisorySession",
    "AdvisoryMessage",
    "AgentInvocation",
    "KauDocument",
    "LangGraphCheckpoint",
    "LangGraphCheckpointWrite",

    # Intelligence
    "FieldObservation",
    "CropStage",
    "IrrigationSchedule",
    "FertiliserPlan",

    # Alerts
    "FarmerAlert",
    "FCMDeliveryLog",

    # Market
    "MarketRecommendation",
    "PriceSubscription",

    # Analytics
    "FarmSeasonAnalytics",
    "AgentPerformance",
    "PlatformMetrics",
    "AdvisoryFeedback",

    # System
    "AuditLog",
    "APIRateLimit",
]
