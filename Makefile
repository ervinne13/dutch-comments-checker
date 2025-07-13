IMAGE_NAME = dcc_api
CONTAINER_NAME = dcc_api
PORT = 8000

.PHONY: all build run start stop clean models up down logs

build:
	docker compose build

models:
	docker compose run --rm --no-deps $(CONTAINER_NAME) python3 app/ai/load_models.py

dev:
	docker compose up -d dcc_db dcc_redis dcc_ollama
	DEV_MODE=1 docker compose up -d dcc_api

up:
	docker compose up -d

down:
	docker compose down

migrate-revise:
	docker exec -e PYTHONPATH=/dcc $(CONTAINER_NAME) alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrate:
	docker exec -e PYTHONPATH=/dcc $(CONTAINER_NAME) alembic upgrade head

logs:
	docker compose logs -f $(filter-out $@,$(MAKECMDGOALS))

clean:
	docker compose down --volumes --remove-orphans
	rm -rf $(PREBUILT_ZIP) $(PREBUILT_DIR) hf_cache

shell:
	docker exec -it $(CONTAINER_NAME) bash

# Aliases


run: up
start: up
stop: down