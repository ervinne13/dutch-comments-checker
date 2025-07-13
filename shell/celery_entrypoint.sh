#!/bin/bash
set -e

# Deprecated, but kept for now.
# Originally intended so that we have separate processes for the 
# API and background tasks (Celery), building is too slow though
# so we're sticking to just one container for now.
if [ "$DEV_MODE" = "1" ]; then
    echo "[Celery Entrypoint] Running in DEV mode (hot-reload)"
    exec watchmedo auto-restart --directory=./app --pattern=*.py --recursive -- celery -A app.tasks worker --loglevel=info --concurrency=1
else
    echo "[Celery Entrypoint] Running in PROD mode"
    exec celery -A app.tasks worker --loglevel=info --concurrency=1
fi
