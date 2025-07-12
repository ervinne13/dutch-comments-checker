IMAGE_NAME = dcc_api
CONTAINER_NAME = dcc_api
PORT = 8000

.PHONY: all build run start stop clean models up down logs

build:
	docker compose build

models:
	docker compose run --rm --no-deps api python3 app/load_models.py

dev:
	docker compose run --rm -p $(PORT):$(PORT) api uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT) --reload-dir /dcc/app

up:
	docker compose up -d

down:
	docker compose down

migrate-revise:
	docker exec -e PYTHONPATH=/dcc $(CONTAINER_NAME) alembic revision --autogenerate -m "$(msg)"

migrate:
	docker exec -e PYTHONPATH=/dcc $(CONTAINER_NAME) alembic upgrade head

logs:
	docker compose logs -f

clean:
	docker compose down --volumes --remove-orphans
	rm -rf $(PREBUILT_ZIP) $(PREBUILT_DIR) hf_cache

bash:
	docker exec -it $(CONTAINER_NAME) bash

# Aliases


run: up
start: up
stop: down