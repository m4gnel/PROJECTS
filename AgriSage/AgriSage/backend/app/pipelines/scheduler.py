from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .weather_pipeline import run_weather_pipeline
from .pest_pipeline import run_pest_pipeline
from .market_pipeline import run_market_pipeline
from .soil_pipeline import run_soil_pipeline
from .satellite_pipeline import run_satellite_pipeline

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")


def setup_scheduler() -> AsyncIOScheduler:
    scheduler.add_job(run_weather_pipeline, "interval", hours=1, id="weather")
    scheduler.add_job(run_pest_pipeline, "interval", hours=6, id="pest")
    scheduler.add_job(run_market_pipeline, "interval", hours=12, id="market")
    scheduler.add_job(run_soil_pipeline, "interval", hours=24, id="soil")
    scheduler.add_job(run_satellite_pipeline, "interval", hours=24, id="satellite")
    return scheduler
