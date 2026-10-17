from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://agrisage:agrisage_secure_password_2026@localhost:5432/agrisage_dev"

    # Authentication & Security
    SECRET_KEY: str = "super_secret_jwt_key_agrisage_2026_minimum_32_chars_long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Environment & Operational Settings
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    MAX_IMAGE_SIZE_MB: int = 5
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Object Storage (Cloudflare R2)
    R2_BUCKET: str = ""
    R2_ACCESS_KEY: str = ""
    R2_SECRET_KEY: str = ""
    R2_ACCOUNT_ID: str = ""

    # Push Notifications & Speech & SMS APIs
    FCM_KEY: str = ""
    BHASHINI_API_KEY: str = ""
    OTP_PROVIDER_KEY: str = ""

    # Weather & AI Model Services
    WEATHER_PROVIDER: str = "open_meteo"
    GEMINI_API_KEY: str = ""
    DATA_GOV_IN_KEY: str = ""
    NASA_EARTHDATA_TOKEN: str = ""
    RAILWAY_TOKEN: str = ""
    RAILWAY_API_URL: str = ""
    OLLAMA_URL: str = "http://localhost:11434"

    # Model & Knowledge Versioning
    MODEL_VERSION: str = "v1.0.0"
    KNOWLEDGE_VERSION: str = "2026-09-01"

    # Crop Simulation Engine
    DSSAT_BIN_PATH: str = "/usr/local/bin/dscsm048"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
