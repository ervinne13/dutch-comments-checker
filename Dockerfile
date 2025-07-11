# Should be faster to build than python:3.10 or python:3.10-slim
# I haven't tested but we may need a different base image for anything that can't run CUDA (CPU only)
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /dcc

# Install Python and system dependencies + clean up
RUN apt update && apt install -y python3-pip python3-dev git \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies from PyPI 
# no prebuilt torch this time, but this thing can only run now on CUDA 12.1
# This has to be revisited later.
COPY requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt
RUN pip install torch==2.7.1+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]