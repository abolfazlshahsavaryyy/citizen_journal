#!/bin/bash

echo "🔄 Starting Docker containers (including RabbitMQ)..."
docker-compose up --build -d

echo "⏳ Waiting for RabbitMQ to be ready..."
# Basic wait loop to ensure RabbitMQ is listening before Celery starts
RETRIES=15
until nc -z localhost 5672 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for RabbitMQ... $RETRIES remaining attempts"
  sleep 2
  RETRIES=$((RETRIES - 1))
done

echo "🚀 Starting FastAPI (on port 8002)..."
cd /home/abolfazl/Documents/CitizenJournal/citizen_journal/backend/fastapi_backend/HateSpeech/fast_api
uvicorn main:app --host 0.0.0.0 --port 8002 &

echo "🛰️ Starting Celery worker for FastAPI..."
celery -A celery_app worker --loglevel=info -Q prediction &
