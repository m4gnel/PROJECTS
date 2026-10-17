"""
Health endpoint test — verifies GET /health returns 200 with {"status": "ok"}.
"""

from __future__ import annotations

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from fastapi.testclient import TestClient
# pyrefly: ignore [missing-import]
from main import app


client = TestClient(app)


def test_health_returns_ok():
    """Exit check #2: /health returns 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}
