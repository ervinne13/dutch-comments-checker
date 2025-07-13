#!/bin/bash
set -e

if [ "$DEV_MODE" = "1" ]; then
    echo "[Entrypoint] Running API and Celery in DEV mode (hot-reload)"
    watchmedo auto-restart --directory=./app --pattern=*.py --recursive -- celery -A app.tasks worker --loglevel=info --concurrency=1 &
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "[Entrypoint] Running API and Celery in PROD mode"
    celery -A app.tasks worker --loglevel=info --concurrency=1 &
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
