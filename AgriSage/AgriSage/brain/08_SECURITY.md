# AGRI-SAGE — SECURITY

## 10 Hard Rules
1. OTP only — no passwords. bcrypt for OTP hashes only.
2. No secrets in source code — env vars only
3. User input is data, never instruction — never in LLM system prompt
4. All 500 errors: {"detail":"Internal server error"} only
5. Every endpoint requires JWT except /health and /auth/*
6. PostgreSQL RLS at DB level — not only application level
7. File uploads: MIME from content (python-magic), size check, strip EXIF
8. All LLM output validated against Pydantic schema before use
9. SimulationParams typed struct only — never free text to DSSAT
10. Sensitive data encrypted at rest — pgcrypto for farm locations

## JWT
ALGORITHM='HS256' | ACCESS=15min | REFRESH=7days
payload: sub=user_id, tier=subscription_tier, exp, iat, jti=uuid4()

## OTP
otp = str(secrets.randbelow(1000000)).zfill(6)
hash = bcrypt.hash(otp, rounds=10) — store hash only
expires_at = now + 300s | max_attempts = 5 per phone per 10min

## Auth Dependency (before EVERY DB query)
```python
async def require_auth(token=Depends(oauth2_scheme), db=Depends(get_db)):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get('sub')
    await db.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))
    return payload
```

## Image Upload Pipeline
```python
ALLOWED_MIME = {'image/jpeg','image/png','image/webp'} | MAX_SIZE = 5*1024*1024
def process_uploaded_image(file_bytes):
    if len(file_bytes) > MAX_SIZE: raise ValueError('Too large')
    mime = magic.from_buffer(file_bytes[:2048], mime=True)
    if mime not in ALLOWED_MIME: raise ValueError(f'Not allowed: {mime}')
    img = Image.open(io.BytesIO(file_bytes)); img.verify()
    img = Image.open(io.BytesIO(file_bytes))
    clean = Image.new(img.mode, img.size); clean.putdata(list(img.getdata()))
    if max(clean.size) > 1200:
        clean.thumbnail((1200,1200), Image.Resampling.LANCZOS)  # Pillow 11.0
    out = io.BytesIO(); clean.save(out, format='JPEG', quality=85)
    return out.getvalue()
```

## Input Sanitization
```python
@field_validator('name')
def sanitize(cls, v):
    v = re.sub(r'<[^>]+>','',v)          # strip HTML
    v = re.sub(r'[\x00-\x1f\x7f]','',v) # strip control chars
    return v.strip()
```

## nginx Rate Limits
limit_req_zone $binary_remote_addr zone=general:10m rate=20r/s;
limit_req_zone $binary_remote_addr zone=diagnose:10m rate=2r/s;
limit_req_zone $binary_remote_addr zone=otp:10m rate=5r/10m;

## Android
EncryptedSharedPreferences for JWT — never plain SharedPreferences
network_security_config.xml: cleartextTrafficPermitted="false"

## RLS: Return 404 not 403 for unauthorized — never reveal resource exists

## CI Security Gates
- grep for hardcoded secrets pattern
- pip-audit --fail-on CRITICAL
- bandit -r backend/ -lll (HIGH severity fails build)
- verify .env not in git history
