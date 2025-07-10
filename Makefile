IMAGE_NAME = dutch_comment_checker
CONTAINER_NAME = dutch_comment_checker
PORT = 8000
PREBUILT_ZIP = prebuilt-torch-271.zip
PREBUILT_DIR = prebuilt-torch-271
GDRIVE_URL = https://drive.google.com/uc?export=download&id=1t2UqKx8kVta0DaAj8IHPBr7AWF34wA64

.PHONY: all download build run start stop clean

download:
	@echo "Checking for existing prebuilt directory..."
	@if [ ! -d "$(PREBUILT_DIR)" ]; then \
		echo "Downloading prebuilt torch wheel..."; \
		curl -L -o $(PREBUILT_ZIP) "$(GDRIVE_URL)"; \
		unzip -o $(PREBUILT_ZIP) -d $(PREBUILT_DIR); \
	else \
		echo "$(PREBUILT_DIR) already exists, skipping download."; \
	fi

build: download
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --gpus all \
		--name $(CONTAINER_NAME) \
		-v $(CURDIR)/$(PREBUILT_DIR):/app/$(PREBUILT_DIR) \
		-v ~/.cache/huggingface:/root/.cache/huggingface \
		-p $(PORT):$(PORT) \
		$(IMAGE_NAME)

start:
	docker start $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)

logs:
	docker logs -f $(CONTAINER_NAME)

clean:
	docker rm -f $(CONTAINER_NAME) || true
	rm -rf $(PREBUILT_ZIP) $(PREBUILT_DIR)
