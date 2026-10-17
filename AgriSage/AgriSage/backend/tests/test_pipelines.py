import pytest
from app.pipelines.scheduler import setup_scheduler


def test_scheduler_jobs():
    sched = setup_scheduler()
    job_ids = [job.id for job in sched.get_jobs()]
    assert "weather" in job_ids
    assert "pest" in job_ids
    assert "market" in job_ids
    assert "soil" in job_ids
    assert "satellite" in job_ids
