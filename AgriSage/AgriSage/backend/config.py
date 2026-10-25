import os
from typing import List, Literal, Union
from urllib.parse import urlparse
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database Configuration
    # The development URL intentionally has no embedded password.  Compose and
    # deployment environments must provide the complete URL explicitly.
    DATABASE_URL: str = "postgresql+asyncpg://agrisage@localhost:5432/agrisage_dev"
    DB_PASSWORD: str = ""

    # Authentication & Security
    SECRET_KEY: str = "dev-only-insecure-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Environment & Operational Settings
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    MAX_IMAGE_SIZE_MB: int = 5
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Object Storage (Cloudflare R2)
    R2_BUCKET: str = ""
    R2_ACCESS_KEY: str = ""
    R2_SECRET_KEY: str = ""
    R2_ACCOUNT_ID: str = ""
    PUBLIC_BASE_URL: str = "http://localhost:8000"

    # Push Notifications & Speech & SMS APIs
    FCM_KEY: str = ""
    BHASHINI_API_KEY: str = ""
    OTP_PROVIDER_KEY: str = ""
    OTP_PROVIDER: Literal["disabled", "generic_http"] = "disabled"
    OTP_PROVIDER_URL: str = ""
    OTP_PROVIDER_SENDER: str = "Agri-SAGE"
    OTP_PROVIDER_TIMEOUT_SECONDS: float = 8.0
    # Console OTPs are an explicit local-development escape hatch only.  The
    # production validator rejects this setting so sign-in cannot silently
    # become unusable or expose OTPs in a deployed log stream.
    OTP_DEV_MODE: bool = False

    # Payment provider. Payment endpoints fail closed until both values exist.
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""

    # Weather & AI Model Services
    WEATHER_PROVIDER: str = "open_meteo"
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"
    GEMINI_API_KEY: str = ""
    DATA_GOV_IN_KEY: str = ""
    NASA_EARTHDATA_TOKEN: str = ""
    RAILWAY_TOKEN: str = ""
    RAILWAY_API_URL: str = ""
    OLLAMA_URL: str = "http://localhost:11434"
    LLM_PROVIDER: Literal["disabled", "gemini", "ollama"] = "gemini"
    LLM_MODEL: str = "gemini-2.5-flash"
    ENABLE_EMBEDDINGS: bool = False
    EMBEDDING_MODEL_PATH: str = ""

    # Local-only storage fallback.  A production deployment must use R2 and
    # must never return a local:// object key that no other process can read.
    ALLOW_LOCAL_STORAGE: bool = False

    # Model & Knowledge Versioning
    MODEL_VERSION: str = "v1.0.0"
    KNOWLEDGE_VERSION: str = "2026-09-01"

    # Crop Simulation Engine
    DSSAT_BIN_PATH: str = "/usr/local/bin/dscsm048"

    def validate_runtime(self) -> None:
        """Reject unsafe defaults before the service enters production."""
        if self.ENVIRONMENT.lower() != "production":
            return

        errors = []
        secret_lower = self.SECRET_KEY.casefold()
        if (
            self.SECRET_KEY == "dev-only-insecure-key-change-me"
            or len(self.SECRET_KEY) < 32
            or secret_lower.startswith(("your-", "change-", "test-"))
        ):
            errors.append("SECRET_KEY must be a unique value of at least 32 characters")
        if not self.DATABASE_URL.strip() or "localhost" in self.DATABASE_URL or "agrisage_dev" in self.DATABASE_URL:
            errors.append("DATABASE_URL must point to a production database")
        parsed_database_url = urlparse(self.DATABASE_URL)
        if parsed_database_url.scheme != "postgresql+asyncpg" or not parsed_database_url.hostname:
            errors.append("DATABASE_URL must use a valid postgresql+asyncpg URL")
        url_has_password = bool(parsed_database_url.password)
        if self.DB_PASSWORD in {"devpassword", "testpassword", "local-only-change-me", "change-me"}:
            errors.append("DB_PASSWORD must be supplied by the production secret manager")
        elif not self.DB_PASSWORD and not url_has_password:
            errors.append("DB_PASSWORD must be supplied by the production secret manager")
        parsed_public_base_url = urlparse(self.PUBLIC_BASE_URL)
        if parsed_public_base_url.scheme != "https" or not parsed_public_base_url.netloc:
            errors.append("PUBLIC_BASE_URL must use HTTPS in production")
        if not self.CORS_ORIGINS or "*" in self.CORS_ORIGINS:
            errors.append("CORS_ORIGINS must explicitly list trusted HTTPS origins in production")
        elif any(
            urlparse(origin).scheme != "https" or not urlparse(origin).netloc
            for origin in self.CORS_ORIGINS
        ):
            errors.append("CORS_ORIGINS must use HTTPS origins in production")
        if self.ACCESS_TOKEN_EXPIRE_MINUTES <= 0 or self.REFRESH_TOKEN_EXPIRE_DAYS <= 0:
            errors.append("Token expiry settings must be positive")
        if self.ALGORITHM not in {"HS256", "HS384", "HS512"}:
            errors.append("ALGORITHM must be an approved HMAC algorithm")

        if self.OTP_DEV_MODE:
            errors.append("OTP_DEV_MODE must be disabled in production")
        if self.OTP_PROVIDER != "generic_http":
            errors.append("OTP_PROVIDER must be generic_http in production")
        elif (
            urlparse(self.OTP_PROVIDER_URL).scheme != "https"
            or not urlparse(self.OTP_PROVIDER_URL).netloc
        ):
            errors.append("OTP_PROVIDER_URL must use HTTPS in production")
        if not self.OTP_PROVIDER_KEY:
            errors.append("OTP_PROVIDER_KEY must be configured in production")

        if self.WEATHER_PROVIDER != "open_meteo":
            errors.append("WEATHER_PROVIDER must be the supported open_meteo adapter")
        parsed_weather_url = urlparse(self.OPEN_METEO_BASE_URL)
        if parsed_weather_url.scheme != "https" or not parsed_weather_url.netloc:
            errors.append("OPEN_METEO_BASE_URL must use HTTPS in production")

        if self.LLM_PROVIDER == "disabled":
            errors.append("LLM_PROVIDER must be configured in production")
        elif self.LLM_PROVIDER == "gemini" and not self.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")
        elif self.LLM_PROVIDER == "ollama":
            parsed_ollama_url = urlparse(self.OLLAMA_URL)
            if not parsed_ollama_url.scheme or not parsed_ollama_url.netloc:
                errors.append("OLLAMA_URL must be a valid URL when LLM_PROVIDER=ollama")
            elif parsed_ollama_url.hostname in {"localhost", "127.0.0.1", "::1"}:
                errors.append("OLLAMA_URL must not point to loopback in production")
        if self.ENABLE_EMBEDDINGS and not self.EMBEDDING_MODEL_PATH:
            errors.append("EMBEDDING_MODEL_PATH is required when ENABLE_EMBEDDINGS is true")
        elif self.ENABLE_EMBEDDINGS and not os.path.exists(self.EMBEDDING_MODEL_PATH):
            errors.append("EMBEDDING_MODEL_PATH must point to an existing local model")
        if self.ALLOW_LOCAL_STORAGE:
            errors.append("ALLOW_LOCAL_STORAGE must be disabled in production")
        if any(not value for value in (self.R2_BUCKET, self.R2_ACCESS_KEY, self.R2_SECRET_KEY, self.R2_ACCOUNT_ID)):
            errors.append("R2_BUCKET, R2_ACCOUNT_ID, R2_ACCESS_KEY, and R2_SECRET_KEY are required in production")
        if errors:
            raise RuntimeError("Unsafe production configuration: " + "; ".join(errors))

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
