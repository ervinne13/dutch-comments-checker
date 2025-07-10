IMAGE_NAME = dutch_comment_checker
CONTAINER_NAME = dutch_comment_checker
PORT = 8000
TORCH_ZIP = prebuilt-torch-271.zip
TORCH_DIR = prebuilt-torch-271
GDRIVE_FILE_ID = your-google-drive-file-id-here

build: $(TORCH_ZIP)
	docker build -t $(IMAGE_NAME) .

$(TORCH_ZIP):
	@echo "Downloading $(TORCH_ZIP) from Google Drive..."
	@if [ ! -f $(TORCH_ZIP) ]; then \
		curl -L -o $(TORCH_ZIP) "https://drive.google.com/uc?export=download&id=$(GDRIVE_FILE_ID)"; \
	fi
	@unzip -n $(TORCH_ZIP)

run:
	docker run --rm --gpus all -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true

zip:
	zip -r $(IMAGE_NAME).zip Dockerfile Makefile requirements.txt $(TORCH_DIR)/ app/
