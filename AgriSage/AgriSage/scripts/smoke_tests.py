import sys
import httpx


def run_smoke_tests(base_url="http://localhost:8000"):
    print("Running deployment smoke tests...")
    
    # 1. Health check
    try:
        r = httpx.get(f"{base_url}/health", timeout=5.0)
        assert r.status_code == 200, f"Health check status: {r.status_code}"
        assert r.json().get("status") == "ok", "Health status not ok"
        print("✓ Health Check Passed")
    except Exception as e:
        print(f"✗ Health Check Failed: {e}")
        sys.exit(1)

    # 2. OTP endpoint check
    try:
        r = httpx.post(f"{base_url}/api/v1/auth/send-otp", json={"phone": "+919999999999"}, timeout=5.0)
        assert r.status_code in [200, 429], f"OTP endpoint status: {r.status_code}"
        print("✓ Auth OTP Endpoint Passed")
    except Exception as e:
        print(f"✗ Auth OTP Endpoint Failed: {e}")
        sys.exit(1)

    print("ALL SMOKE TESTS PASSED.")


if __name__ == "__main__":
    run_smoke_tests()
