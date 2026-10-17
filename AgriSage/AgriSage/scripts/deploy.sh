#!/bin/bash
set -e
echo "Deploying Agri-SAGE..."
cd /home/ubuntu/agrisage
git pull origin main
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --no-deps backend
sleep 5
alembic upgrade head
python scripts/smoke_tests.py
echo "Deployment complete"
