"""Explicit OTP delivery adapters for the canonical authentication flow.

The generic HTTP adapter is intentionally small and provider-neutral.  Its
contract is documented here rather than inferred from a vendor SDK:

* ``POST OTP_PROVIDER_URL`` over HTTPS
* ``Authorization: Bearer OTP_PROVIDER_KEY``
* JSON body ``{"to": <E.164 phone>, "otp": <six digits>,
  "message": <human-readable text>, "sender": <configured sender>}``
* any 2xx response means the provider accepted the message

Vendor-specific gateways can be implemented behind this adapter without
changing the mobile/API contract.  The raw OTP is never logged by this module.
"""

from __future__ import annotations

from typing import Any

import httpx

from backend.config import Settings, settings


class OTPProviderError(RuntimeError):
    """Raised when a configured provider cannot accept an OTP."""


class GenericHTTPOTPProvider:
    """Deliver OTPs through the documented provider-neutral HTTP contract."""

    def __init__(self, configuration: Settings = settings) -> None:
        self.url = configuration.OTP_PROVIDER_URL.rstrip("/")
        self.api_key = configuration.OTP_PROVIDER_KEY
        self.sender = configuration.OTP_PROVIDER_SENDER
        self.timeout = configuration.OTP_PROVIDER_TIMEOUT_SECONDS

    async def deliver(self, *, phone: str, otp: str) -> None:
        if not self.url or not self.api_key:
            raise OTPProviderError("OTP provider is not configured")

        payload: dict[str, Any] = {
            "to": phone,
            "otp": otp,
            "message": f"Your Agri-SAGE verification code is {otp}.",
            "sender": self.sender,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise OTPProviderError("OTP provider request failed") from exc

        if not 200 <= response.status_code < 300:
            raise OTPProviderError("OTP provider rejected the request")


def configured_otp_provider(configuration: Settings = settings) -> GenericHTTPOTPProvider | None:
    """Return the configured adapter, or ``None`` for an explicit disabled mode."""

    if configuration.OTP_PROVIDER == "generic_http":
        return GenericHTTPOTPProvider(configuration)
    return None
