# Dutch Comments Checker

Uses a prebuilt pytorch 2.7.1. 
Without the prebuilds, `pip install --no-cache-dir -r requirements.txt` will probably run for more than an hour. I stopped trying at 1hr 40 minutes so I'm unsure if it would take more than 2. I just rebuilt the *.whl files from an existing venv i have locally and ran `pip wheel torch -w ~/torch-wheel`. The contents of that is what you see on `prebuilds` folder.


## Instructions

Build and run with with
```
make build && make models
```

Build will take a long time, about 15-20 minutes.
- Build mostly takes time when downloading and building torch. Would take about `[+] Building 736.5s (14/14) FINISHED ` in my case.
- Downloading the models for the classifiers takes another 5 or so minutes

Once built and models downloaded, run the thing:
```
make run
```


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

