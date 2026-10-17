from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    GEMINI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"
    NASA_EARTHDATA_BASE_URL: str = "https://appeears.earthdatacloud.nasa.gov"
    DATA_GOV_IN_API_KEY: str = ""
    NBAIR_RSS_URL: str = "https://www.nbair.res.in/rss/pest-alerts.xml"
    NBSS_API_URL: str = "https://www.nbsslup.in/api"
    KAU_PDF_DIR: str = "./kau_pdfs"
    RAILWAY_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"


settings = Settings()
