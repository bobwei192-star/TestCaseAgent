# [Issue]: ComfyUI randomly but consistently causing driver crash on gfx1030 (RX 6950 XT) and torch==2.8.0+rocm6.4

> **Issue #5195**
> **状态**: closed
> **创建时间**: 2025-08-14T11:54:28Z
> **更新时间**: 2025-10-23T21:17:20Z
> **关闭时间**: 2025-10-21T18:15:44Z
> **作者**: chaserhkj
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5195

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

ComfyUI has been causing driver crash on my setup w/ RX 6950 XT randomly and consistently. The crash can happen if I tried to infer a number of images with smaller resolutions (512x512) consecutively. It can also just immediately crash the system upon my first attempt to infer an image with larger resolution (1024x1024). All crashes seem to be hard crashes where the whole system is automatically rendered a soft reset, and the GPU cannot be seen through the bus after the reboot unless a hard reset is performed. No kernel logs were collectable most of the time since the hang seems to happen too fast for kernel to write any logs.

I doubted this might be an instance of #4729 , since I do have some crashes happening when the flow was in VAE decoding. But further test with `--cpu-vae` still crashes and most of the crashes happen in the process of UNET inference anyway.

**This also seems to be strongly connected to comfyui and/or PyTorch. Since I have been running ggml-based applications without any problems.** Both [llama.cpp](https://github.com/ggml-org/llama.cpp) and [sd.cpp](https://github.com/leejet/stable-diffusion.cpp) run with ROCm without any problems on my setup. Especially on `sd.cpp`, where exact same image inference tasks causing crashes in `comfyui` completed without even a single issue there. However I have not tested any other torch application on this setup so if there is any suggested small test snippets/benchmarks I could use for replicating the issue please do let me know.

Currently my runtime setup for comfyui looks like this 
```
podman run --device /dev/kfd --device /dev/dri --security-opt seccomp=unconfined -d --name comfyui \
    <volume and port flags> --replace \
    -e HIP_VISIBLE_DEVICES=0 \
    -e TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 \
    -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
    comfyui-rocm:latest --port 8818 --cpu-vae --listen
```

I am right now trying to go through the various different flags from ComfyUI and different ROCm configuration envs to see if any of them could help mitigate the issue. I have tried these and they don't seem to work:
```
--disable-cuda-malloc
--use-pytorch-cross-attention
--f16-vae
MIOPEN_FIND_MODE=2
 PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:6144
 PYTORCH_HIP_ALLOC_CONF=backend:native
 PYTORCH_HIP_ALLOC_CONF=backend:native,expandable_segments=True
```
Any suggestions for me to try would be appreciated.

### Operating System

Fedora CoreOS 42.20250623.3.1, Kernel 6.15.8-200.fc42.x86_64, Container Debian GNU/Linux 12 (bookworm)

### CPU

AMD Ryzen 9 7950X3D 16-Core Processor

### GPU

AMD Radeon RX 6950 XT

### ROCm Version

ROCm 6.4 from PyTorch Pip Package

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — lucbruni-amd (2025-08-14T15:08:57Z)

Hi @chaserhkj, thank you for opening an issue with us and sorry to hear you are encountering this.

Just wanted to let you know an internal ticket has been opened and we are investigating. Thanks for your patience.

---

### 评论 #2 — chaserhkj (2025-08-18T11:34:46Z)

Some updates, this is the minimal snippet I was able to reproduce the behavior on my platform:

```python
import torch
from diffusers import StableDiffusionXLPipeline
from diffusers import EulerAncestralDiscreteScheduler
model_path = "<Path to model checkpoint safetensors>"
pipe = StableDiffusionXLPipeline.from_single_file(
    model_path, torch_dtype=torch.float16, local_files_only=True, use_safetensors=True,
    scheduler=EulerAncestralDiscreteScheduler(),
)
pipe.to("cuda")
pipe.vae.to("cpu")

prompt= "<test prompt here>"

img = pipe(prompt=prompt, height=1536, width=1024,
            num_inference_steps=25, strength=0.75).images[0]
img.save("./result.png")
```
I had to move vae to CPU since without doing this it will just create a OOM. I assume both comfyui and sd.cpp are doing some smart memory management on their end to still let this work completely within VRAM.

Behavior is still not very consistent. I have really consistent crashes on ComfyUI but for this one only like one in three or four-ish. 

Edit: Above test script is tested under the default environmental settings, without any alterations to ROCM or TORCH related env settings

---

### 评论 #3 — chaserhkj (2025-08-19T01:01:04Z)

I just dug a bit more into the infrastructures of `torch` and `ggml`, it seems high likely to me that this is a problem linked to MIOpen library.

`ggml` reuses all their cuda kernels on HIP over AMD GPUs and have no code path into MIOpen, but `torch` makes extended uses of it. That is the only reason I could figure why this works perfectly fine with `stable-diffusion.cpp` but utterly unusable with anything related to `torch`

---

### 评论 #4 — chaserhkj (2025-08-20T06:41:46Z)

After a lot of trial and error I am able to produce a reliable working profile: 

```bash
export MIOPEN_DEBUG_CONV_GEMM=0
export MIOPEN_DEBUG_CONV_WINOGRAD=0
```

It seems the triggering bugs should be in MIOpen's Winograd kernels, as well as in rocBLAS through the GEMM algorithms. (hipBLASLt does not support my card so it must be rocBLAS)

For Direct convolution algorithms, I did explicitly restrict MIOpen to pick them only and they seem to work fine, just on my platform and workload they are much slower than Implicit GEMM so they are not picked by MIOpen.

I am not sure about FFT algorithms, since they seem to be unfit for my workload and are just never picked up. I might just keep them around and change it if some other crashes happen.




---

### 评论 #5 — lucbruni-amd (2025-09-30T18:28:24Z)

Hi @chaserhkj, thanks for your thorough investigation thus far. It is helpful and is much appreciated.

I just successfully inferred a few 1024x1536 images (per your minimal reproducer) on gfx1030 + ComfyUI without reproducing the crashes.

Here is my setup. Please let me know if there's anything else you'd like me to provide.

```
ROCm version: (7, 0) # 7.0.1, installed via quick-start guide 
Platform: Linux (Ubuntu 24.04.3 LTS Noble Numbat baremetal)
Python version: 3.12.3
pytorch version: 2.8.0+rocm7.0.0.git64359f59 # installed via https://repo.radeon.com/
AMD arch: gfx1030
Device: AMD Radeon PRO W6800
ComfyUI version: 0.3.61 (v0.3.61-2-gf48d7230) # installed via comfy-cli, run with HSA_OVERRIDE_GFX_VERSION=10.3.0 python main.py
```

Could you try on ROCm 7 with a later torch+ROCm as above? If you are still hitting the issue, please let me know and I'll raise this to MIOpen/rocBLAS folks thanks to your deductions.

Thanks!

---

### 评论 #6 — lucbruni-amd (2025-10-21T18:15:44Z)

Closing this issue as it has fallen inactive.

If you are still encountering the issue with a later stack as I've posted above, please feel free to reopen the issue and reaffirm the reproducer. Thanks for opening and finding issues with ROCm!

---

### 评论 #7 — chaserhkj (2025-10-22T14:31:56Z)

Sorry my AMD workstation was allocated for other loads earlier this month so I wasn't able to test it. And I have been traveling since 15th. I'll test with ROCm 7 again on this issue when I'm back early November and give feedback.

---

### 评论 #8 — lucbruni-amd (2025-10-22T14:40:35Z)

No worries @chaserhkj! Always feel free to reopen issues or open new ones if you encounter anything. We appreciate your efforts. Enjoy your travels!

---

### 评论 #9 — cursiv3 (2025-10-23T21:17:20Z)

Just thought I'd drop that I had the same crashes with same card on certain SDXL models in comfyui and uninstalling pytorch rocm6.4 -> installing pytorch rocm7.0 fixed it for me (already had rocm 7.0 installed)  thanks!

---
