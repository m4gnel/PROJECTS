"""
AMRS Backend Configuration.

Reads all environment variables from .env via pydantic-settings.
Warns (does not crash) if keys are empty — they may not be set yet in Milestone 0.
"""

from __future__ import annotations

import warnings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Provider Keys
    gemini_api_key: str = ""
    groq_api_key: str = ""
    openrouter_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    # Qdrant
    qdrant_url: str = ""
    qdrant_api_key: str = ""

    # Neo4j
    neo4j_uri: str = ""
    neo4j_username: str = ""
    neo4j_password: str = ""

    # App
    backend_cors_origins: str = "http://localhost:3000"

    def warn_if_missing(self) -> None:
        """Emit warnings for any empty keys. Called at startup."""
        key_fields = [
            "gemini_api_key",
            "groq_api_key",
            "openrouter_api_key",
            "supabase_url",
            "supabase_anon_key",
            "supabase_service_role_key",
            "qdrant_url",
            "qdrant_api_key",
            "neo4j_uri",
            "neo4j_username",
            "neo4j_password",
        ]
        for field in key_fields:
            if not getattr(self, field):
                warnings.warn(
                    f"Environment variable {field.upper()} is not set. "
                    f"Some features will be unavailable.",
                    stacklevel=2,
                )


settings = Settings()
