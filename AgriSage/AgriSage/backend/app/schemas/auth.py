from pydantic import BaseModel


class RegisterRequest(BaseModel):
    phone: str
    name: str
    password: str
    village: str | None = None
    district: str | None = None
    preferred_language: str = "ml"
    latitude: float | None = None
    longitude: float | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400
    farmer_id: str
