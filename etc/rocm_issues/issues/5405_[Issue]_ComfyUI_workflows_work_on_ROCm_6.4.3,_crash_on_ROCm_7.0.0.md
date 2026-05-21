# [Issue]: ComfyUI workflows work on ROCm 6.4.3, crash on ROCm 7.0.0

> **Issue #5405**
> **状态**: open
> **创建时间**: 2025-09-21T02:49:23Z
> **更新时间**: 2025-10-22T13:46:51Z
> **作者**: Lonceg
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5405

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- adityas-amd

## 描述

### Problem Description

I have noticed worse performance when compared to my previous experience with WSL2 with ROCm 6.4.2

ComfyUI becomes very slow on VAE Decode, almost always there is a warning about running out of memory: 
```Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.```

Before I managed to even use WAN 2.2 with Q4 quantized model, now I would get
```Memory access fault by GPU node-1 (Agent handle: 0x629f9f9dae60) on address 0x7cb3770e0000. Reason: Page not present or supervisor privilege.```

I haven't managed to generate a single 5s video.

Generating an image with SD3.5 Large FP8 takes like 300 seconds. The same for Flux dev fp8. Performance way worse than in following video: https://youtu.be/7qDlHpeTmC0?si=EFxnUA3qRprUL1hD

### Operating System

Linux Mint 22.2 (Zara)

### CPU

AMD Ryzen 7 5700X3D 8-Core Processor

### GPU

RX 9070 XT

### ROCm Version

ROCm 7.0.0

### ROCm Component

_No response_

### Steps to Reproduce

Linux Mint 22.2

Instructions as here: https://github.com/Lonceg/comfyui_for_amd_docker

Or Pull the original https://hub.docker.com/r/rocm/pytorch make a container, download ComfyUI and custom nodes.




### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — Anghammar (2025-09-21T08:22:45Z)

I have had problems with the VAE encode/decode in previous ROCm versions as well. I made this hack to force tiled VAE encoding for nodes that lacks tiled VAE options: https://github.com/comfyanonymous/ComfyUI/pull/7924

It will at least help you skip the first failing non-tiled VAE encoding.

Also I noticed that ``--reserve-vram`` option will help with some memory issues, since it will make ComfyUI unload more stuff when loading new stuff.

With that said -- I have no experience with ROCm 7 yet since I'm waiting for WSL support.

---

### 评论 #2 — Lonceg (2025-09-21T14:56:09Z)

I have tried both as well as few several flags.

Thanks @mordekai2009 

Adding 
```
import torch
torch.backends.cudnn.enabled = False
```
to main.py made the template flux dev fp8 template go down to 50s. 

Still 20 seconds slower than the exactly same template on this video: https://youtu.be/7qDlHpeTmC0?si=ZZ1hOeGZNjN8V3JF&t=172

I might experiment more with the flags and other settings. But if you have any ideas what else could be there, please let me know.

Running image to image with SD3.5 fp8 for example cause following
```
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Memory access fault by GPU node-1 (Agent handle: 0x351b3c00) on address 0x708f88fff000. Reason: Page not present or supervisor privilege.
^C
Stopped server
Failed to read GPU memory: Input/output error
GPU core dump failed
Aborted (core dumped)
```
Offloading VAE to cpu with ```--cpu-vae``` flag seemed to help with memory errors on image to image. I don't recall using this flag in WSL2 though. 

Wan still doesn't work with cpu offload. And it worked before on WSL pre rocm 7.0 with workflow I have sent in the attachment.
```
Memory access fault by GPU node-1 (Agent handle: 0x283c3d20) on address 0x7356fd9fd000. Reason: Page not present or supervisor privilege.
GPU core dump created: gpucore.1067
Aborted (core dumped)
```
[wan2.2-i2v-rapid-aio-gguf-example.json](https://github.com/user-attachments/files/22452674/wan2.2-i2v-rapid-aio-gguf-example.json)



---

### 评论 #3 — Lonceg (2025-09-23T09:46:07Z)

Just an update. Installed ROCm on host os is 7.0 (from this link https://repo.radeon.com/amdgpu-install/7.0/ubuntu/noble/amdgpu-install_7.0.70000-1_all.deb)

The wan workflow works on Docker image rocm/pytorch:rocm6.4.3_ubuntu24.04_py3.12_pytorch_release_2.6.0 

Ran with the same command
```
sudo docker run -it \
  --name comfy-rocm-test \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  --ipc=host \
  --shm-size 8G \
  -p 8188:8188 \
  -v /home/cez/comfyui:/workspace \
  rocm/pytorch:rocm6.4.3_ubuntu24.04_py3.12_pytorch_release_2.6.0
```

```
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Requested to load CLIPVisionModelProjection
loaded completely 14668.8 1208.09814453125 True
gguf qtypes: Q6_K (169), F32 (73)
Attempting to recreate sentencepiece tokenizer from GGUF file metadata...
Created tokenizer with vocab size of 256384
Dequantizing token_embd.weight to prevent runtime OOM.
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load WanTEModel
loaded completely 13444.6349609375 5626.453125 True
Requested to load WanVAE
loaded completely 5546.38134765625 242.02829551696777 True
Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
gguf qtypes: F16 (821), Q4_K (360), Q6_K (120), F32 (2)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
0 models unloaded.
loaded partially 6347.999804687501 6347.9981689453125 0
Attempting to release mmap (393)
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6/6 [04:50<00:00, 48.38s/it]
Requested to load WanVAE
loaded completely 5716.59521484375 242.02829551696777 True
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Prompt executed in 390.51 seconds
```

Stable diffusion 3.5 Large also works although it takes 122 seconds for 1 Megapx image.

Seems like VAE still enters tiled VAE but it is not as slow as with ROCm 7.0, and doesn't crash with memory errors.

---

### 评论 #4 — Lonceg (2025-09-23T09:49:02Z)

Also the image seems not to have torchaudio package installed in it?
```
root@6c61fc0610b9:/workspace/ComfyUI# python main.py --listen 0.0.0.0 --port 8188 

Prestartup times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy

Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 32019 MB
pytorch version: 2.6.0+gitdbfe118
AMD arch: gfx1201
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
/opt/conda/envs/py_3.12/lib/python3.12/site-packages/redis/connection.py:77: UserWarning: redis-py works best with hiredis. Please consider installing
  warnings.warn(msg)
Using sub quadratic optimization for attention, if you have memory or speed issues try using: --use-split-cross-attention
torchaudio missing, ACE model will be broken
torchaudio missing, ACE model will be broken
Python version: 3.12.11 | packaged by conda-forge | (main, Jun  4 2025, 14:45:31) [GCC 13.3.0]
ComfyUI version: 0.3.59
ComfyUI frontend version: 1.26.13
[Prompt Server] web root: /opt/conda/envs/py_3.12/lib/python3.12/site-packages/comfyui_frontend_package/static
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio.py module for custom nodes: No module named 'torchaudio'
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py", line 2, in <module>
    import comfy.audio_encoders.audio_encoders
  File "/workspace/ComfyUI/comfy/audio_encoders/audio_encoders.py", line 2, in <module>
    from .whisper import WhisperLargeV3
  File "/workspace/ComfyUI/comfy/audio_encoders/whisper.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py module for custom nodes: No module named 'torchaudio'

[rgthree-comfy] Loaded 48 fantastic nodes. 🎉

ComfyUI-GGUF: Partial torch compile only, consider updating pytorch

Import times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/websocket_image_save.py
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-KJNodes
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-GGUF
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite

WARNING: some comfy_extras/ nodes did not import correctly. This may be because they are missing some dependencies.

IMPORT FAILED: nodes_audio.py
IMPORT FAILED: nodes_audio_encoder.py

This issue might be caused by new missing dependencies added the last time you updated ComfyUI.
Please do a: pip install -r requirements.txt

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://0.0.0.0:8188
```

---

### 评论 #5 — adityas-amd (2025-10-13T23:55:25Z)

@Lonceg I am unable to reproduced the crash with `lonceg/comfyui_for_amd:rocm7.0_pytorch2.8_py3.12`. Have you tried with https://github.com/comfyanonymous/ComfyUI/pull/7924 patch? 

<img width="1280" height="616" alt="Image" src="https://github.com/user-attachments/assets/4b0de831-7cd2-4640-b67c-bbbd77a7069e" />
<img width="1891" height="861" alt="Image" src="https://github.com/user-attachments/assets/bc9c6e04-67c7-4e2f-b3f9-d8e00a2cdba1" />

---

### 评论 #6 — Lonceg (2025-10-20T12:11:04Z)

@adityas-amd The crashes happened with Wan 2.2 quantized model. It would work on 6.4.3 albeit slow, and completely not work on 7.0.0

It's been a while since I've done any gen AI but I believe these were the following models:
https://huggingface.co/befox/WAN2.2-14B-Rapid-AllInOne-GGUF/tree/main/v10

Example of workflows are here:
https://huggingface.co/befox/WAN2.2-14B-Rapid-AllInOne-GGUF/tree/main

Here is the original non quantized model:
https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne

All the necessary custom nodes are in the image from what I see from the screenshot. But if you need I am also adding all nodes here:
https://github.com/rgthree/rgthree-comfy
https://github.com/kijai/ComfyUI-KJNodes
https://github.com/city96/ComfyUI-GGUF
https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite

Maybe RX9070XT 16GB VRAM is too little for these models. But then would 6.4.3 manage VRAM better than 7.0.0, I have no idea, I was just testing ComfyUI with my GPU. I'm not that advanced in this. I just read people running these models with NVIDIA with as little as 8GB of VRAM.

edit: I have not tried https://github.com/comfyanonymous/ComfyUI/pull/7924 patch yet

edit2: 
here is clip loader: https://huggingface.co/city96/umt5-xxl-encoder-gguf
here is VAE (2.1 is fine apparently): https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/tree/main/split_files/vae
here is clip vision: https://huggingface.co/ratoenien/clip_vision_h

Here is how my workflow looks like on 6.4.4 now:

<img width="1885" height="1209" alt="Image" src="https://github.com/user-attachments/assets/83fea57c-24da-47c4-ae46-45d8fc4f3d47" />

I should mention that to quickly move between the versions I started keeping entire comfyui as a volume. I download official pytorch images from docker, start a container, install requirements from the volume (they are exactly the same as in ```lonceg/comfyui_for_amd:rocm7.0_pytorch2.8_py3.1```

> sudo docker run -it \
>   --name comfy-rocm \
>   --cap-add=SYS_PTRACE \
>   --security-opt seccomp=unconfined \
>   --device=/dev/kfd \
>   --device=/dev/dri \
>   --group-add video \
>   --ipc=host \
>   --shm-size 8G \
>   -p 8188:8188 \
>   -v /home/cez/comfyui:/workspace \
>   rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1 
> 
> cd &&
> cd / &&
> cd workspace &&
> cd ComfyUI &&
> pip install -r requirements.txt &&
> cd custom_nodes &&
> cd ComfyUI-GGUF &&
> pip install -r requirements.txt &&
> cd .. &&
> cd ComfyUI-KJNodes &&
> pip install -r requirements.txt &&
> cd .. &&
> cd ComfyUI-VideoHelperSuite &&
> pip install -r requirements.txt &&
> cd .. &&
> cd rgthree-comfy &&
> pip install -r requirements.txt &&
> cd .. &&
> cd ..
> 
> TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python main.py --use-pytorch-cross-attention --listen 0.0.0.0 --port 8188

```root@44f3147565be:/workspace/ComfyUI# TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python main.py --use-pytorch-cross-attention --listen 0.0.0.0 --port 8188

Prestartup times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy

Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 32019 MB
pytorch version: 2.7.1+git99ccf24
AMD arch: gfx1201
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Using pytorch attention
torchaudio missing, ACE model will be broken
torchaudio missing, ACE model will be broken
Python version: 3.12.11 | packaged by conda-forge | (main, Jun  4 2025, 14:45:31) [GCC 13.3.0]
ComfyUI version: 0.3.59
ComfyUI frontend version: 1.26.13
[Prompt Server] web root: /opt/conda/envs/py_3.12/lib/python3.12/site-packages/comfyui_frontend_package/static
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio.py module for custom nodes: No module named 'torchaudio'
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py", line 2, in <module>
    import comfy.audio_encoders.audio_encoders
  File "/workspace/ComfyUI/comfy/audio_encoders/audio_encoders.py", line 2, in <module>
    from .whisper import WhisperLargeV3
  File "/workspace/ComfyUI/comfy/audio_encoders/whisper.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py module for custom nodes: No module named 'torchaudio'

[rgthree-comfy] Loaded 48 fantastic nodes. 🎉

ComfyUI-GGUF: Partial torch compile only, consider updating pytorch

Import times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/websocket_image_save.py
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-KJNodes
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-GGUF
   0.1 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite

WARNING: some comfy_extras/ nodes did not import correctly. This may be because they are missing some dependencies.

IMPORT FAILED: nodes_audio.py
IMPORT FAILED: nodes_audio_encoder.py

This issue might be caused by new missing dependencies added the last time you updated ComfyUI.
Please do a: pip install -r requirements.txt

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://0.0.0.0:8188
```

result:

<img width="1916" height="1221" alt="Image" src="https://github.com/user-attachments/assets/6b428c3e-bafd-4d23-bced-f7fcf1038d1d" />

loaded completely 3075.7666015625 242.02829551696777 True
Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.
Prompt executed in 470.41 seconds

https://github.com/user-attachments/assets/2a76d7c9-a5df-496e-8b89-5d678fa8fa2c

Other silly gen AI thing made with this workflow. Please don't judge me, I just wanted to make a meme.

<img width="1013" height="630" alt="Image" src="https://github.com/user-attachments/assets/a5fe23c2-3435-4ccb-a587-6e29cc2be114" />

https://github.com/user-attachments/assets/42edc8eb-83bc-401b-a165-23609f53e57a

On 7.0.0 this wouldn't work for me with the exact same volume/comfyui/custom_nodes. I would have the same errors with: ```Memory access fault by GPU node-1 (Agent handle: 0x629f9f9dae60) on address 0x7cb3770e0000. Reason: Page not present or supervisor privilege.```

Only change was the base image I have used from docker. 6.4.3 would even work if I installed 7.0.0 ROCm on host and just run 6.4.3 docker image.

edit3: I have not tested the most recent docker image 7.0.2; I just haven't done any gen AI recently. I just kind of wish it was reliable like 6.4.4 but also faster. Doing anything longer that 5s is either too long or workflow runs out of VRAM. And in general generating 5s videos with this workflow takes about 10 minutes which also feels way too long. Models are quantized too.


---

### 评论 #7 — Lonceg (2025-10-21T11:10:55Z)

I downloaded 7.0.2 and tried the exact same workflow without any changes and it crashed again:

> sudo docker run -it \
>   --name comfy-rocm-test2 \
>   --cap-add=SYS_PTRACE \
>   --security-opt seccomp=unconfined \
>   --device=/dev/kfd \
>   --device=/dev/dri \
>   --group-add video \
>   --ipc=host \
>   --shm-size 8G \
>   -p 8188:8188 \
>   -v /home/cez/comfyui:/workspace \
>   rocm/pytorch:rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.8.0
> 
> cd workspace &&
> cd ComfyUI &&
> pip install -r requirements.txt &&
> cd custom_nodes &&
> cd ComfyUI-GGUF &&
> pip install -r requirements.txt &&
> cd .. &&
> cd ComfyUI-KJNodes &&
> pip install -r requirements.txt &&
> cd .. &&
> cd ComfyUI-VideoHelperSuite &&
> pip install -r requirements.txt &&
> cd .. &&
> cd rgthree-comfy &&
> pip install -r requirements.txt &&
> cd .. &&
> cd ..
> 
> 
> TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python main.py --use-pytorch-cross-attention --listen 0.0.0.0 --port 8188

```root@d52a6e519f71:/workspace/ComfyUI# TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python main.py --use-pytorch-cross-attention --listen 0.0.0.0 --port 8188

Prestartup times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy

Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 32019 MB
pytorch version: 2.8.0+rocm7.0.2.git245bf6ed
AMD arch: gfx1201
ROCm version: (7, 0)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Using pytorch attention
Python version: 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0]
ComfyUI version: 0.3.59
ComfyUI frontend version: 1.26.13
[Prompt Server] web root: /opt/venv/lib/python3.12/site-packages/comfyui_frontend_package/static

[rgthree-comfy] Loaded 48 magnificent nodes. 🎉

ComfyUI-GGUF: Allowing full torch compile

Import times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/websocket_image_save.py
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-KJNodes
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-GGUF
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://0.0.0.0:8188
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Requested to load CLIPVisionModelProjection
loaded completely 15002.8 1208.09814453125 True
gguf qtypes: Q6_K (169), F32 (73)
Attempting to recreate sentencepiece tokenizer from GGUF file metadata...
Created tokenizer with vocab size of 256384
Dequantizing token_embd.weight to prevent runtime OOM.
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load WanTEModel
loaded completely 13420.6349609375 5626.453125 True
Requested to load WanVAE
loaded completely 5466.13134765625 242.02829551696777 True
Warning: Ran out of memory when regular VAE encoding, retrying with tiled VAE encoding.
gguf qtypes: F16 (821), Q4_K (360), Q6_K (120), F32 (2)
model weight dtype torch.float16, manual cast: None
model_type FLOW
Requested to load WAN21
loaded partially 8758.82831171875 8758.825805664062 0
Attempting to release mmap (347)
  0%|                                                                                                                                                   | 0/6 [00:00<?, ?it/s]Memory access fault by GPU node-1 (Agent handle: 0x452c6810) on address 0x7c8d48246000. Reason: Page not present or supervisor privilege.
GPU core dump created: gpucore.125
Aborted (core dumped)
```

<img width="2559" height="1292" alt="Image" src="https://github.com/user-attachments/assets/0aa052c8-39fe-4b94-8433-19d9331aad61" />

---

### 评论 #8 — Lonceg (2025-10-21T11:33:01Z)

Also I am not sure how important that is but I found it weird that 6.4 containers start in some directory
```cez@Kruz:~$ sudo docker run -it \
  --name comfy-rocm-test4 \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  --ipc=host \
  --shm-size 8G \
  -p 8188:8188 \
  -v /home/cez/comfyui:/workspace \
  rocm/pytorch:rocm6.4.4_ubuntu24.04_py3.12_pytorch_release_2.7.1 
root@f00606c6fe00:/var/lib/jenkins# 
```

While 7.0 containers start in root directory.
```cez@Kruz:~$ sudo docker run -it \
  --name comfy-rocm-test3 \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  --ipc=host \
  --shm-size 8G \
  -p 8188:8188 \
  -v /home/cez/comfyui:/workspace \
  rocm/pytorch:rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.8.0
root@f1475094727b:/# 
```

Also 6.4 images seem to lack torchaudio, as I have already disabled the install of these packages in my volume:
```
comfyui-frontend-package==1.26.13
comfyui-workflow-templates==0.1.81
comfyui-embedded-docs==0.2.6
#torch
torchsde
#torchvision
#torchaudio
numpy>=1.25.0
einops
transformers>=4.37.2
tokenizers>=0.13.3
sentencepiece
safetensors>=0.4.2
aiohttp>=3.11.8
yarl>=1.18.0
pyyaml
Pillow
scipy
tqdm
psutil
alembic
SQLAlchemy
av>=14.2.0

#non essential dependencies:
kornia>=0.7.1
spandrel
soundfile
pydantic~=2.0
pydantic-settings~=2.0
```

You can see it here and I have also pasted it above. Still ComfyUI seems to be working without it:
```
Prestartup times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy

Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 32019 MB
pytorch version: 2.7.1+git99ccf24
AMD arch: gfx1201
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Using pytorch attention
torchaudio missing, ACE model will be broken
torchaudio missing, ACE model will be broken
Python version: 3.12.11 | packaged by conda-forge | (main, Jun  4 2025, 14:45:31) [GCC 13.3.0]
ComfyUI version: 0.3.59
ComfyUI frontend version: 1.26.13
[Prompt Server] web root: /opt/conda/envs/py_3.12/lib/python3.12/site-packages/comfyui_frontend_package/static
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio.py module for custom nodes: No module named 'torchaudio'
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py", line 2, in <module>
    import comfy.audio_encoders.audio_encoders
  File "/workspace/ComfyUI/comfy/audio_encoders/audio_encoders.py", line 2, in <module>
    from .whisper import WhisperLargeV3
  File "/workspace/ComfyUI/comfy/audio_encoders/whisper.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py module for custom nodes: No module named 'torchaudio'

[rgthree-comfy] Loaded 48 fantastic nodes. 🎉

ComfyUI-GGUF: Partial torch compile only, consider updating pytorch

Import times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/websocket_image_save.py
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-KJNodes
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-GGUF
   0.1 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite

WARNING: some comfy_extras/ nodes did not import correctly. This may be because they are missing some dependencies.

IMPORT FAILED: nodes_audio.py
IMPORT FAILED: nodes_audio_encoder.py

This issue might be caused by new missing dependencies added the last time you updated ComfyUI.
Please do a: pip install -r requirements.txt

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://0.0.0.0:8188
```

---

### 评论 #9 — Lonceg (2025-10-22T13:46:51Z)

Same thing with Hunyuan3d 2.0

<img width="2131" height="1133" alt="Image" src="https://github.com/user-attachments/assets/b00ebf38-8ccb-4685-bd49-00d8c361bb4b" />

Workflow fails with 7.0.2, either core dump
```
root@db32702f8ab2:/workspace/ComfyUI# TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python main.py --use-pytorch-cross-attention --listen 0.0.0.0 --port 8188

Prestartup times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy

Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 32019 MB
pytorch version: 2.8.0+rocm7.0.2.git245bf6ed
AMD arch: gfx1201
ROCm version: (7, 0)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Using pytorch attention
Python version: 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0]
ComfyUI version: 0.3.59
ComfyUI frontend version: 1.26.13
[Prompt Server] web root: /opt/venv/lib/python3.12/site-packages/comfyui_frontend_package/static

[rgthree-comfy] Loaded 48 epic nodes. 🎉

ComfyUI-GGUF: Allowing full torch compile

Import times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/websocket_image_save.py
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-Unload-Model
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-KJNodes
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-GGUF
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://0.0.0.0:8188
got prompt

VAE load device: cuda:0, offload device: cpu, dtype: torch.float16
Requested to load Dinov2Model
loaded completely 15002.8 2163.6455078125 True
Requested to load Hunyuan3Dv2
loaded completely 12440.85712890625 2123.4024658203125 True
  2%|██▌                                                                                                     | 1/40 [00:01<01:04,  1.64s/it]Memory access fault by GPU node-1 (Agent handle: 0x409e4270) on address 0x7ab077a0c000. Reason: Page not present or supervisor privilege.
GPU core dump created: gpucore.124
Aborted (core dumped)
```

or some other error

```
got prompt
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 60/60 [02:24<00:00,  2.40s/it]
Volume Decoding: 100%|██████████████████████████████████████████████████████████████████████████████████| 4340/4340 [01:37<00:00, 44.68it/s]
!!! Exception during processing !!! zero-size array to reduction operation maximum which has no identity
Traceback (most recent call last):
  File "/workspace/ComfyUI/execution.py", line 496, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/ComfyUI/execution.py", line 315, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, hidden_inputs=hidden_inputs)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/ComfyUI/execution.py", line 289, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "/workspace/ComfyUI/execution.py", line 277, in process_inputs
    result = f(**inputs)
             ^^^^^^^^^^^
  File "/workspace/ComfyUI/comfy_extras/nodes_hunyuan3d.py", line 612, in save
    save_glb(mesh.vertices[i], mesh.faces[i], os.path.join(full_output_folder, f), metadata)
  File "/workspace/ComfyUI/comfy_extras/nodes_hunyuan3d.py", line 514, in save_glb
    "max": vertices_np.max(axis=0).tolist(),
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/numpy/_core/_methods.py", line 44, in _amax
    return umr_maximum(a, axis, None, out, keepdims, initial, where)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: zero-size array to reduction operation maximum which has no identity

Prompt executed in 249.62 seconds
```


Meanwhile 6.4.4

<img width="2379" height="1240" alt="Image" src="https://github.com/user-attachments/assets/1005f4b1-e4e5-49cf-bf3d-5e4a856cf12e" />

```
root@44f3147565be:/workspace/ComfyUI# TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 python main.py --use-pytorch-cross-attention --listen 0.0.0.0 --port 8188

Prestartup times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy

Checkpoint files will always be loaded safely.
Total VRAM 16304 MB, total RAM 32019 MB
pytorch version: 2.7.1+git99ccf24
AMD arch: gfx1201
ROCm version: (6, 4)
Set vram state to: NORMAL_VRAM
Device: cuda:0 AMD Radeon RX 9070 XT : native
Using pytorch attention
torchaudio missing, ACE model will be broken
torchaudio missing, ACE model will be broken
Python version: 3.12.11 | packaged by conda-forge | (main, Jun  4 2025, 14:45:31) [GCC 13.3.0]
ComfyUI version: 0.3.59
ComfyUI frontend version: 1.26.13
[Prompt Server] web root: /opt/conda/envs/py_3.12/lib/python3.12/site-packages/comfyui_frontend_package/static
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio.py module for custom nodes: No module named 'torchaudio'
Traceback (most recent call last):
  File "/workspace/ComfyUI/nodes.py", line 2133, in load_custom_node
    module_spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py", line 2, in <module>
    import comfy.audio_encoders.audio_encoders
  File "/workspace/ComfyUI/comfy/audio_encoders/audio_encoders.py", line 2, in <module>
    from .whisper import WhisperLargeV3
  File "/workspace/ComfyUI/comfy/audio_encoders/whisper.py", line 4, in <module>
    import torchaudio
ModuleNotFoundError: No module named 'torchaudio'

Cannot import /workspace/ComfyUI/comfy_extras/nodes_audio_encoder.py module for custom nodes: No module named 'torchaudio'

[rgthree-comfy] Loaded 48 magnificent nodes. 🎉

ComfyUI-GGUF: Partial torch compile only, consider updating pytorch

Import times for custom nodes:
   0.0 seconds: /workspace/ComfyUI/custom_nodes/websocket_image_save.py
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-Unload-Model
   0.0 seconds: /workspace/ComfyUI/custom_nodes/rgthree-comfy
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-KJNodes
   0.0 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-GGUF
   0.2 seconds: /workspace/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite

WARNING: some comfy_extras/ nodes did not import correctly. This may be because they are missing some dependencies.

IMPORT FAILED: nodes_audio.py
IMPORT FAILED: nodes_audio_encoder.py

This issue might be caused by new missing dependencies added the last time you updated ComfyUI.
Please do a: pip install -r requirements.txt

Context impl SQLiteImpl.
Will assume non-transactional DDL.
No target revision found.
Starting server

To see the GUI go to: http://0.0.0.0:8188
got prompt
model weight dtype torch.float16, manual cast: None
model_type FLOW
Missing VAE keys ['encoder.input_proj.weight', 'encoder.input_proj.bias', 'encoder.cross_attn.attn.c_q.weight', 'encoder.cross_attn.attn.c_kv.weight', 'encoder.cross_attn.attn.c_proj.weight', 'encoder.cross_attn.attn.c_proj.bias', 'encoder.cross_attn.attn.attention.q_norm.weight', 'encoder.cross_attn.attn.attention.q_norm.bias', 'encoder.cross_attn.attn.attention.k_norm.weight', 'encoder.cross_attn.attn.attention.k_norm.bias', 'encoder.cross_attn.ln_1.weight', 'encoder.cross_attn.ln_1.bias', 'encoder.cross_attn.ln_2.weight', 'encoder.cross_attn.ln_2.bias', 'encoder.cross_attn.ln_3.weight', 'encoder.cross_attn.ln_3.bias', 'encoder.cross_attn.mlp.c_fc.weight', 'encoder.cross_attn.mlp.c_fc.bias', 'encoder.cross_attn.mlp.c_proj.weight', 'encoder.cross_attn.mlp.c_proj.bias', 'encoder.self_attn.resblocks.0.attn.c_qkv.weight', 'encoder.self_attn.resblocks.0.attn.c_proj.weight', 'encoder.self_attn.resblocks.0.attn.c_proj.bias', 'encoder.self_attn.resblocks.0.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.0.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.0.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.0.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.0.ln_1.weight', 'encoder.self_attn.resblocks.0.ln_1.bias', 'encoder.self_attn.resblocks.0.mlp.c_fc.weight', 'encoder.self_attn.resblocks.0.mlp.c_fc.bias', 'encoder.self_attn.resblocks.0.mlp.c_proj.weight', 'encoder.self_attn.resblocks.0.mlp.c_proj.bias', 'encoder.self_attn.resblocks.0.ln_2.weight', 'encoder.self_attn.resblocks.0.ln_2.bias', 'encoder.self_attn.resblocks.1.attn.c_qkv.weight', 'encoder.self_attn.resblocks.1.attn.c_proj.weight', 'encoder.self_attn.resblocks.1.attn.c_proj.bias', 'encoder.self_attn.resblocks.1.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.1.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.1.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.1.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.1.ln_1.weight', 'encoder.self_attn.resblocks.1.ln_1.bias', 'encoder.self_attn.resblocks.1.mlp.c_fc.weight', 'encoder.self_attn.resblocks.1.mlp.c_fc.bias', 'encoder.self_attn.resblocks.1.mlp.c_proj.weight', 'encoder.self_attn.resblocks.1.mlp.c_proj.bias', 'encoder.self_attn.resblocks.1.ln_2.weight', 'encoder.self_attn.resblocks.1.ln_2.bias', 'encoder.self_attn.resblocks.2.attn.c_qkv.weight', 'encoder.self_attn.resblocks.2.attn.c_proj.weight', 'encoder.self_attn.resblocks.2.attn.c_proj.bias', 'encoder.self_attn.resblocks.2.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.2.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.2.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.2.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.2.ln_1.weight', 'encoder.self_attn.resblocks.2.ln_1.bias', 'encoder.self_attn.resblocks.2.mlp.c_fc.weight', 'encoder.self_attn.resblocks.2.mlp.c_fc.bias', 'encoder.self_attn.resblocks.2.mlp.c_proj.weight', 'encoder.self_attn.resblocks.2.mlp.c_proj.bias', 'encoder.self_attn.resblocks.2.ln_2.weight', 'encoder.self_attn.resblocks.2.ln_2.bias', 'encoder.self_attn.resblocks.3.attn.c_qkv.weight', 'encoder.self_attn.resblocks.3.attn.c_proj.weight', 'encoder.self_attn.resblocks.3.attn.c_proj.bias', 'encoder.self_attn.resblocks.3.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.3.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.3.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.3.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.3.ln_1.weight', 'encoder.self_attn.resblocks.3.ln_1.bias', 'encoder.self_attn.resblocks.3.mlp.c_fc.weight', 'encoder.self_attn.resblocks.3.mlp.c_fc.bias', 'encoder.self_attn.resblocks.3.mlp.c_proj.weight', 'encoder.self_attn.resblocks.3.mlp.c_proj.bias', 'encoder.self_attn.resblocks.3.ln_2.weight', 'encoder.self_attn.resblocks.3.ln_2.bias', 'encoder.self_attn.resblocks.4.attn.c_qkv.weight', 'encoder.self_attn.resblocks.4.attn.c_proj.weight', 'encoder.self_attn.resblocks.4.attn.c_proj.bias', 'encoder.self_attn.resblocks.4.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.4.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.4.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.4.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.4.ln_1.weight', 'encoder.self_attn.resblocks.4.ln_1.bias', 'encoder.self_attn.resblocks.4.mlp.c_fc.weight', 'encoder.self_attn.resblocks.4.mlp.c_fc.bias', 'encoder.self_attn.resblocks.4.mlp.c_proj.weight', 'encoder.self_attn.resblocks.4.mlp.c_proj.bias', 'encoder.self_attn.resblocks.4.ln_2.weight', 'encoder.self_attn.resblocks.4.ln_2.bias', 'encoder.self_attn.resblocks.5.attn.c_qkv.weight', 'encoder.self_attn.resblocks.5.attn.c_proj.weight', 'encoder.self_attn.resblocks.5.attn.c_proj.bias', 'encoder.self_attn.resblocks.5.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.5.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.5.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.5.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.5.ln_1.weight', 'encoder.self_attn.resblocks.5.ln_1.bias', 'encoder.self_attn.resblocks.5.mlp.c_fc.weight', 'encoder.self_attn.resblocks.5.mlp.c_fc.bias', 'encoder.self_attn.resblocks.5.mlp.c_proj.weight', 'encoder.self_attn.resblocks.5.mlp.c_proj.bias', 'encoder.self_attn.resblocks.5.ln_2.weight', 'encoder.self_attn.resblocks.5.ln_2.bias', 'encoder.self_attn.resblocks.6.attn.c_qkv.weight', 'encoder.self_attn.resblocks.6.attn.c_proj.weight', 'encoder.self_attn.resblocks.6.attn.c_proj.bias', 'encoder.self_attn.resblocks.6.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.6.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.6.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.6.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.6.ln_1.weight', 'encoder.self_attn.resblocks.6.ln_1.bias', 'encoder.self_attn.resblocks.6.mlp.c_fc.weight', 'encoder.self_attn.resblocks.6.mlp.c_fc.bias', 'encoder.self_attn.resblocks.6.mlp.c_proj.weight', 'encoder.self_attn.resblocks.6.mlp.c_proj.bias', 'encoder.self_attn.resblocks.6.ln_2.weight', 'encoder.self_attn.resblocks.6.ln_2.bias', 'encoder.self_attn.resblocks.7.attn.c_qkv.weight', 'encoder.self_attn.resblocks.7.attn.c_proj.weight', 'encoder.self_attn.resblocks.7.attn.c_proj.bias', 'encoder.self_attn.resblocks.7.attn.attention.q_norm.weight', 'encoder.self_attn.resblocks.7.attn.attention.q_norm.bias', 'encoder.self_attn.resblocks.7.attn.attention.k_norm.weight', 'encoder.self_attn.resblocks.7.attn.attention.k_norm.bias', 'encoder.self_attn.resblocks.7.ln_1.weight', 'encoder.self_attn.resblocks.7.ln_1.bias', 'encoder.self_attn.resblocks.7.mlp.c_fc.weight', 'encoder.self_attn.resblocks.7.mlp.c_fc.bias', 'encoder.self_attn.resblocks.7.mlp.c_proj.weight', 'encoder.self_attn.resblocks.7.mlp.c_proj.bias', 'encoder.self_attn.resblocks.7.ln_2.weight', 'encoder.self_attn.resblocks.7.ln_2.bias', 'encoder.ln_post.weight', 'encoder.ln_post.bias']
VAE load device: cuda:0, offload device: cpu, dtype: torch.float16
Requested to load Dinov2Model
loaded completely 15002.8 2163.6455078125 True
Requested to load Hunyuan3Dv2
loaded completely 12522.85712890625 2123.4024658203125 True
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 60/60 [02:36<00:00,  2.60s/it]
Requested to load ShapeVAE
loaded completely 10333.90400390625 624.8759784698486 True
Volume Decoding: 100%|██████████████████████████████████████████████████████████████████████████████████| 4340/4340 [01:52<00:00, 38.57it/s]
Prompt executed in 310.07 seconds
```



---
