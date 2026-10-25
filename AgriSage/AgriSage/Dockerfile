FROM python:3.11.9-slim-bookworm AS builder
WORKDIR /build
COPY requirements.lock .
RUN python -m pip install --no-cache-dir --require-hashes --user --requirement requirements.lock \
    && python -m pip check

FROM python:3.11.9-slim-bookworm
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl libmagic1 postgresql-client && rm -rf /var/lib/apt/lists/*
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -fsS --max-time 5 http://localhost:8000/ready || exit 1
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 2 --log-level info"]
