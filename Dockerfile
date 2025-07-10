# Should be faster to build than python:3.10 or python:3.10-slim
# I haven't tested but we may need a different base image for anything that can't run CUDA (CPU only)
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

# Install Python and system dependencies + clean up
RUN apt update && apt install -y python3-pip python3-dev git \
    && rm -rf /var/lib/apt/lists/*

# Using a prebuilt files
# Should reduce build time from almost 2 hours to just under 1 minute
COPY prebuilt-torch-271/*.whl ./prebuilt-torch-271/
COPY requirements.txt .
RUN pip install prebuilt-torch-271/*.whl \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]