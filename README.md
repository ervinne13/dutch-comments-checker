# Dutch Comments Checker

Uses a prebuilt pytorch 2.7.1. 
Without the prebuilds, `pip install --no-cache-dir -r requirements.txt` will probably run for more than an hour. I stopped trying at 1hr 40 minutes so I'm unsure if it would take more than 2. I just rebuilt the *.whl files from an existing venv i have locally and ran `pip wheel torch -w ~/torch-wheel`. The contents of that is what you see on `prebuilds` folder.


## Instructions

Build and run with with
```
make build
make run
```

This should output something like:

```
ervinne-sodusta@ervinne-ubuntu:~/AI/Projects/dutch-comments-checker$ make run
docker run --rm --gpus all -p 8000:8000 --name dutch_comment_checker dutch_comment_checker

==========
== CUDA ==
==========

CUDA Version 11.8.0

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.

/usr/local/lib/python3.10/dist-packages/transformers/models/marian/tokenization_marian.py:175: UserWarning: Recommended: pip install sacremoses.
  warnings.warn("Recommended: pip install sacremoses.")
Device set to use cuda:0
Device set to use cuda:0

Device set to use cuda:0
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:50020 - "POST /check HTTP/1.1" 200 OK

```

### Test it with:

```
curl -X POST http://localhost:8000/check -H "Content-Type: application/json" -d '{"comment": "Je bent dom"}'
```

Which should output something like:
```
{
  "original": "Je bent dom",
  "translated": "You're stupid.",
  "spam": {
    "label": "LABEL_0",
    "score": 0.9382461905479431
  },
  "toxicity": {
    "label": "toxic",
    "score": 0.9870408177375793
  }
}
```

## Help

### Connection reset by peer

Depending on your GPU (or how loaded it is), `Device set to use cuda:0` might take a few seconds to display, `INFO:     Started server process [1]` even more so (If I have Stable Diffusion running at the same time this thing takes 30-60s to startup).

Just await for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:50020 - "POST /check HTTP/1.1" 200 OK
```

... and it should be fine. If it takes more than 3 minutes though then start checking the logs.

### Could not select driver

`make run` fails with error:

```
> make run
docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]]
```

### 1. Add NVIDIA package repositories
```
sudo apt update
sudo apt install -y curl gnupg ca-certificates
```

```
sudo mkdir -p /etc/apt/keyrings
```
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /etc/apt/keyrings/nvidia-container-toolkit.gpg
```

```
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb #deb [signed-by=/etc/apt/keyrings/nvidia-container-toolkit.gpg] #' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

```
sudo apt update
sudo apt install -y nvidia-container-toolkit
```

### Update Docker so it can run the thing with a GPU

```
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

