"""Read-only deployment smoke checks for the backend HTTP surface."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable

import httpx


DEFAULT_TIMEOUT_SECONDS = 5.0


def _check_endpoint(
    client: httpx.Client,
    path: str,
    expected_status: int,
    expected_status_value: str,
) -> None:
    response = client.get(path)
    if response.status_code != expected_status:
        raise RuntimeError(f"expected HTTP {expected_status}, got {response.status_code}")
    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("response was not valid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("response JSON was not an object")
    if payload.get("status") != expected_status_value:
        raise RuntimeError(f"expected status={expected_status_value!r}, got {payload.get('status')!r}")


def run_smoke_tests(base_url: str = "http://localhost:8000", timeout: float = DEFAULT_TIMEOUT_SECONDS) -> int:
    """Return a process exit code after checking liveness and readiness.

    Both checks are GET requests.  The smoke gate deliberately does not call
    authentication, payment, provider, or other mutating endpoints.
    """

    base_url = base_url.rstrip("/")
    if not base_url.startswith(("http://", "https://")):
        print("✗ Smoke tests require an http:// or https:// base URL", file=sys.stderr)
        return 1

    checks: tuple[tuple[str, Callable[[], None]], ...]
    print(f"Running deployment smoke tests against {base_url}...")
    try:
        with httpx.Client(base_url=base_url, timeout=timeout, follow_redirects=False) as client:
            checks = (
                ("Health", lambda: _check_endpoint(client, "/health", 200, "ok")),
                ("Readiness", lambda: _check_endpoint(client, "/ready", 200, "ready")),
            )
            for name, check in checks:
                try:
                    check()
                except (httpx.HTTPError, RuntimeError) as exc:
                    print(f"✗ {name} Check Failed: {exc}", file=sys.stderr)
                    return 1
                print(f"✓ {name} Check Passed")
    except httpx.HTTPError as exc:
        print(f"✗ Smoke checks could not reach the service: {exc}", file=sys.stderr)
        return 1

    print("ALL SMOKE TESTS PASSED.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=os.environ.get("SMOKE_BASE_URL", "http://localhost:8000"),
        help="Backend base URL (default: SMOKE_BASE_URL or http://localhost:8000)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Per-request timeout in seconds",
    )
    args = parser.parse_args()
    return run_smoke_tests(args.base_url, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
