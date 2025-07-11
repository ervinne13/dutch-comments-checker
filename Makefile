IMAGE_NAME = dutch_comment_checker
CONTAINER_NAME = dutch_comment_checker
PORT = 8000
# TODO: Move away from using prebuilt torch wheels later
PREBUILT_ZIP = prebuilt-torch-271.zip
PREBUILT_DIR = prebuilt-torch-271
GDRIVE_URL = https://drive.google.com/uc?export=download&id=1t2UqKx8kVta0DaAj8IHPBr7AWF34wA64

.PHONY: all download build run start stop clean models up down logs

download:
	@echo "Checking for existing prebuilt directory..."
	@if [ ! -d "$(PREBUILT_DIR)" ]; then \
		echo "Downloading prebuilt torch wheel..."; \
		curl -L -o $(PREBUILT_ZIP) "$(GDRIVE_URL)"; \
		unzip -o $(PREBUILT_ZIP) -d $(PREBUILT_DIR); \
	else \
		echo "$(PREBUILT_DIR) already exists, skipping download."; \
	fi

build:
	docker compose build

models:
	docker compose run --rm --no-deps api python3 app/load_models.py

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down --volumes --remove-orphans
	rm -rf $(PREBUILT_ZIP) $(PREBUILT_DIR) hf_cache

# Aliases


run: up
start: up
stop: down