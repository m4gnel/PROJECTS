# 📊 Agri-SAGE — Grafana Cloud Monitoring Setup

> **Production Telemetry & Performance Dashboard Guide**
> Free Tier: Grafana Cloud (50 GB metrics/logs included)

---

## Quick Setup Guide

1. Create a free account at [grafana.com](https://grafana.com).
2. Navigate to **Connections -> Data Sources -> Add data source**.
3. Select **Prometheus**.
4. Set Prometheus Server URL to your deployment endpoint:
   `https://<your-railway-url>.railway.app/metrics`
5. Save & Test connection.

---

## 5 Core Dashboard Panels

### Panel 1: API Response Time (P95 Latency)
- **Target**: < 3000ms
- **PromQL Query**:
  ```promql
  histogram_quantile(0.95, http_request_duration_seconds_bucket)
  ```

### Panel 2: Gemini Calls Per Minute
- **Target**: Alert if rate > 13 calls/min (approaching 15 RPM free tier limit)
- **PromQL Query**:
  ```promql
  rate(agrisage_gemini_calls_total[1m]) * 60
  ```

### Panel 3: Agent Error Rate
- **Target**: Alert if error rate > 2%
- **PromQL Query**:
  ```promql
  rate(agrisage_agent_errors_total[5m]) / rate(agrisage_agent_calls_total[5m])
  ```

### Panel 4: Weather & Market Cache Hit Rate
- **Target**: > 70% cache hit ratio
- **PromQL Query**:
  ```promql
  rate(agrisage_cache_hits_total[5m]) / rate(agrisage_cache_requests_total[5m])
  ```

### Panel 5: Active Farmers Today
- **Target**: Realtime active user count
- **PromQL Query**:
  ```promql
  agrisage_active_farmers_today
  ```
