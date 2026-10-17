# AGRI-SAGE — API CONTRACT

## Base URL
Dev: http://localhost:8000 | Prod: https://api.agrisage.in

## Auth: Bearer <access_token> on all except /health and /auth/*
JWT HS256 | 15min access | 7day refresh

## Endpoints
POST /api/v1/auth/send-otp          {phone}
POST /api/v1/auth/verify-otp        {phone, otp} → {access_token, refresh_token, user}
POST /api/v1/auth/refresh            {refresh_token}
POST /api/v1/auth/logout             {refresh_token}
POST /api/v1/farms                   Create farm
GET  /api/v1/farms                   List user farms
GET  /api/v1/farms/{id}              Get farm (404 if not owned)
PUT  /api/v1/farms/{id}
DELETE /api/v1/farms/{id}           Soft delete
POST /api/v1/farms/{id}/fields
POST /api/v1/crop-cycles
POST /api/v1/observations            Multipart: image upload
POST /api/v1/diagnose               {observation_id} → AdvisoryResponse
GET  /api/v1/weather/{lat}/{lon}     WeatherResult + indicators
GET  /api/v1/risk/{farm_id}         6 risk scores
GET  /api/v1/schemes?state=&crop=   Scheme matches
GET  /api/v1/markets/{crop}         e-NAM prices
POST /api/v1/simulate               {SimulationParams} → scenarios
GET  /api/v1/farms/{id}/timeline
GET  /api/v1/farms/{id}/season-summary
POST /api/v1/interventions
POST /api/v1/outcomes
GET  /api/v1/sync/delta?last_sync=
POST /api/v1/voice/transcribe       Audio → {transcript, structured_intent}

## AdvisoryResponse Key Fields
confidence_state: one of 7 states
diagnosis: {label, common_name:{ml,en}, confidence_score, severity, affected_area_pct}
risk: {level, horizon_days, factors}
scenarios: [{id:A/B/C, label, action, expected_yield_kgha, modelled_estimate:true, expected_cost_inr, expected_net_return_inr, risk_level}]
recommended_scenario: "B"
recommended_action: {what, when, how, spray_window, cost_estimate_inr:{min,max}}
evidence: {items:[{type,label,confidence}], contradictions:[], missing_data:[]}
what_would_change_this: [string]
safe_to_act: boolean
scheme_matches: []
sources: [{title, authority, tier}]
generation_ms: integer

## Errors
400: Bad request | 401: Auth failure | 404: Not found
413: File too large | 422: Validation | 429: Rate limited
500: {"detail":"Internal server error"} — NEVER expose more

## Rate Limits
General: 20r/s | /diagnose: 2r/s | /send-otp: 5r/10min
