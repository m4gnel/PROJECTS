import sys
sys.path.insert(0, ".")

from backend.main import app

def test_routes():
    routes = [route.path for route in app.routes]
    print("Registered routes count:", len(routes))
    assert "/health" in routes
    assert "/api/v1/auth/send-otp" in routes
    assert "/api/v1/auth/verify-otp" in routes
    assert "/api/v1/farms" in routes
    assert "/api/v1/observations" in routes
    assert "/api/v1/diagnose" in routes
    print("PASS: All core FastAPI endpoints registered successfully.")

if __name__ == "__main__":
    test_routes()
