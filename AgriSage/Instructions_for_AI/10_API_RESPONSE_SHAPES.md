# 10_API_RESPONSE_SHAPES.md — Exact JSON Request/Response Shapes
# ⚠️ EVERY API ENDPOINT MUST RETURN EXACTLY THIS JSON. DO NOT ADD OR REMOVE FIELDS.

Base URL: https://your-app.up.railway.app  (set via RAILWAY_URL env var)
All timestamps: ISO 8601 format (e.g., "2026-10-01T08:30:00+05:30")
All dates: ISO 8601 date (e.g., "2026-10-01")

---

## Health Check
```
GET /health

Response 200:
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2026-10-01T08:30:00+05:30"
}
```

---

## Auth Endpoints

### POST /auth/register
```
Request:
{
  "phone": "9876543210",
  "name": "Rajan K",
  "password": "securepass123",
  "village": "Kalady",
  "district": "Ernakulam",
  "preferred_language": "ml",
  "latitude": 10.1632,
  "longitude": 76.3986
}

Response 201:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "farmer_id": "uuid-string-here"
}

Response 409 (phone already registered):
{
  "detail": "Phone number already registered"
}
```

### POST /auth/token
```
Request (x-www-form-urlencoded):
username=9876543210&password=securepass123

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "farmer_id": "uuid-string-here"
}

Response 401:
{
  "detail": "Incorrect phone or password"
}
```

---

## Farmer Endpoints

### GET /farmers/me
```
Headers: Authorization: Bearer <token>

Response 200:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "phone": "9876543210",
  "name": "Rajan K",
  "village": "Kalady",
  "district": "Ernakulam",
  "state": "Kerala",
  "preferred_language": "ml",
  "latitude": 10.1632,
  "longitude": 76.3986,
  "is_active": true,
  "created_at": "2026-10-01T08:30:00+05:30",
  "updated_at": "2026-10-01T08:30:00+05:30"
}
```

### PUT /farmers/me
```
Request:
{
  "name": "Rajan Kumar",
  "village": "Kalady",
  "district": "Ernakulam",
  "preferred_language": "ml",
  "latitude": 10.1632,
  "longitude": 76.3986
}

Response 200: (same shape as GET /farmers/me)
```

---

## Field Endpoints

### GET /fields/
```
Response 200:
[
  {
    "id": "field-uuid-1",
    "farmer_id": "farmer-uuid-1",
    "name": "South Paddy Field",
    "area_sq_m": 5000.0,
    "latitude": 10.165,
    "longitude": 76.401,
    "soil_type": "laterite",
    "irrigation_type": "flood",
    "last_ndvi": 0.62,
    "active_crop": {
      "id": "crop-uuid-1",
      "crop_name": "rice",
      "variety": "Jyothi",
      "sowing_date": "2026-07-15",
      "growth_stage": "vegetative",
      "expected_harvest_date": "2026-11-20"
    },
    "created_at": "2026-08-01T10:00:00+05:30",
    "updated_at": "2026-10-01T08:30:00+05:30"
  }
]
```

### POST /fields/
```
Request:
{
  "name": "North Coconut Grove",
  "area_sq_m": 2000.0,
  "latitude": 10.167,
  "longitude": 76.399,
  "soil_type": "laterite",
  "irrigation_type": "drip",
  "crop_name": "coconut",
  "crop_variety": "Hybrid",
  "sowing_date": "2024-06-01"
}

Response 201: (same shape as single field in GET /fields/)
```

### DELETE /fields/{fieldId}
```
Response 204: (no body)

Response 404:
{
  "detail": "Field not found"
}
```

---

## Chat Endpoint

### POST /chat/
```
Request:
{
  "session_id": "session-uuid-or-new",
  "message": "ഇന്ന് നെൽകൃഷിക്ക് വളം ഇടണോ?",
  "language": "ml",
  "farmer_id": "farmer-uuid-1",
  "field_id": "field-uuid-1",
  "latitude": 10.165,
  "longitude": 76.401,
  "crop_info": {
    "crop_name": "rice",
    "variety": "Jyothi",
    "sowing_date": "2026-07-15",
    "current_growth_stage": "vegetative",
    "field_area_hectares": 0.5
  }
}

Response 200:
{
  "session_id": "session-uuid-1",
  "message": "ഇന്നത്തെ കാലാവസ്ഥ നല്ലതാണ്. NPK 14-14-14 ഫോർമുലേഷൻ ഹെക്ടറിന് 25 കിലോഗ്രാം നൽകാം...",
  "language": "ml",
  "confidence": 0.87,
  "alerts": [
    {
      "id": "alert-uuid-1",
      "severity": "WARNING",
      "title": "ബ്ലാസ്റ്റ് രോഗ സാദ്ധ്യത",
      "message": "ഈ ആഴ്ച ബ്ലാസ്റ്റ് രോഗം ഉണ്ടാകാനുള്ള സാദ്ധ്യതയുണ്ട്...",
      "created_at": "2026-10-01T08:30:00+05:30"
    }
  ],
  "agents_used": ["weather", "soil", "fertilizer", "rag", "translator"],
  "created_at": "2026-10-01T08:30:00+05:30"
}
```

---

## Weather Endpoints

### GET /weather/current?lat=10.165&lon=76.401
```
Response 200:
{
  "latitude": 10.165,
  "longitude": 76.401,
  "temperature_c": 29.5,
  "humidity_percent": 78,
  "rainfall_mm": 2.3,
  "wind_kmh": 12.4,
  "uv_index": 7.2,
  "weather_condition": "Partly Cloudy",
  "agri_advisory": "Moderate humidity — monitor for fungal disease. Good day for spraying.",
  "fetched_at": "2026-10-01T08:30:00+05:30"
}
```

### GET /weather/forecast?lat=10.165&lon=76.401
```
Response 200:
{
  "latitude": 10.165,
  "longitude": 76.401,
  "forecast": [
    {
      "date": "2026-10-01",
      "max_temp_c": 32.1,
      "min_temp_c": 24.8,
      "rainfall_mm": 5.0,
      "weather_condition": "Rain",
      "uv_index": 5.0,
      "agri_note": "Avoid harvesting — rain expected"
    },
    {
      "date": "2026-10-02",
      "max_temp_c": 31.0,
      "min_temp_c": 25.2,
      "rainfall_mm": 0.0,
      "weather_condition": "Sunny",
      "uv_index": 8.5,
      "agri_note": "Good for field work"
    }
  ],
  "fetched_at": "2026-10-01T08:30:00+05:30"
}
```

---

## Alerts Endpoints

### GET /alerts/?unread_only=false
```
Response 200:
[
  {
    "id": "alert-uuid-1",
    "farmer_id": "farmer-uuid-1",
    "field_id": "field-uuid-1",
    "severity": "CRITICAL",
    "title": "Severe Rainfall Warning",
    "message": "Heavy rainfall (>50mm) expected in next 24 hours. Secure crops.",
    "source_agent": "weather_agent",
    "is_read": false,
    "created_at": "2026-10-01T08:30:00+05:30"
  },
  {
    "id": "alert-uuid-2",
    "farmer_id": "farmer-uuid-1",
    "field_id": null,
    "severity": "WARNING",
    "title": "Pest Alert: Brown Planthopper",
    "message": "NBAIR reports BPH outbreak in Ernakulam district. Monitor your rice fields.",
    "source_agent": "pest_agent",
    "is_read": false,
    "created_at": "2026-10-01T06:00:00+05:30"
  }
]
```

### POST /alerts/mark-read
```
Request:
{
  "alert_ids": ["alert-uuid-1", "alert-uuid-2"]
}

Response 200:
{
  "marked_count": 2
}
```

---

## Advisory Endpoint

### POST /advisory/ask
```
Request:
{
  "question": "When should I apply second dose of urea for my rice?",
  "language": "en",
  "farmer_id": "farmer-uuid-1",
  "field_id": "field-uuid-1"
}

Response 200:
{
  "question": "When should I apply second dose of urea for my rice?",
  "answer": "For Jyothi rice at vegetative stage, apply second urea dose (60kg/ha) at 45-50 days after transplanting. Current date suggests you apply within the next 5-7 days. Avoid applying before rain.",
  "language": "en",
  "confidence": 0.91,
  "sources": [
    "KAU Package of Practices 2024 — Rice, p.45",
    "Real-time weather forecast"
  ],
  "agents_used": ["crop", "weather", "rag"],
  "created_at": "2026-10-01T08:30:00+05:30"
}
```

---

## WebSocket: Chat Streaming — WS /chat/ws/{session_id}
```
Client sends:
{
  "type": "message",
  "content": "ഇന്ന് മഴ ഉണ്ടാകുമോ?",
  "language": "ml",
  "farmer_id": "farmer-uuid-1"
}

Server streams (multiple JSON messages):
// 1. Typing indicator
{"type": "status", "content": "Checking weather data..."}

// 2. Partial agent result
{"type": "partial", "agent": "weather", "content": "Weather data retrieved"}

// 3. Final answer
{
  "type": "response",
  "content": "ഇന്ന് ഉച്ചതിരിഞ്ഞ് 15-20mm മഴ ഉണ്ടാകാൻ സാദ്ധ്യതയുണ്ട്...",
  "alerts": [],
  "confidence": 0.88,
  "session_id": "session-uuid-1"
}

// 4. Error (if any)
{"type": "error", "content": "Could not reach weather service. Showing cached data."}
```

---

## Standard Error Responses
```
400 Bad Request:
{"detail": "Invalid input: [specific field] [specific issue]"}

401 Unauthorized:
{"detail": "Not authenticated"}

403 Forbidden:
{"detail": "Not authorized to access this resource"}

404 Not Found:
{"detail": "[Resource] not found"}

422 Validation Error:
{
  "detail": [
    {
      "loc": ["body", "phone"],
      "msg": "String should have at most 15 characters",
      "type": "string_too_long"
    }
  ]
}

429 Rate Limit:
{"detail": "Too many requests. Please wait 60 seconds."}

500 Internal Server Error:
{"detail": "Internal server error. Please try again."}
```

---

## HTTP Status Code Rules
- 200: successful GET or PUT
- 201: successful POST (created resource)
- 204: successful DELETE (no body)
- 400: invalid input format
- 401: missing or invalid JWT token
- 403: valid token but wrong farmer
- 404: resource does not exist
- 409: conflict (duplicate phone, duplicate field name)
- 422: Pydantic validation error (FastAPI default)
- 429: rate limit exceeded (Gemini API limit)
- 500: unhandled exception
