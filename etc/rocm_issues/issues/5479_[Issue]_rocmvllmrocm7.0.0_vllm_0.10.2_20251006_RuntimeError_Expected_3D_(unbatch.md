# [Issue]: rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006 RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d

> **Issue #5479**
> **状态**: closed
> **创建时间**: 2025-10-08T03:42:41Z
> **更新时间**: 2025-10-22T18:51:47Z
> **关闭时间**: 2025-10-22T18:51:47Z
> **作者**: tobing
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5479

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- zichguan-amd

## 描述

### Problem Description

I ran rocm/vllm docker image with **AIDC-AI/Ovis2-8B-GPTQ-Int4** model

With **rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006** version, I got error **RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d**

With previous version **rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909** I have no issue.

The logs attached

[vllm-rocm6.4.1_vllm_0.10.1_20250909.txt](https://github.com/user-attachments/files/22758273/vllm-rocm6.4.1_vllm_0.10.1_20250909.txt)
[vllm-rocm7.0.0_vllm_0.10.2_20251006.txt](https://github.com/user-attachments/files/22758274/vllm-rocm7.0.0_vllm_0.10.2_20251006.txt)

### Operating System

CachyOS Linux

### CPU

AMD Ryzen 7 5700X3D 8-Core Processor

### GPU

AMD Radeon RX 7800 XT

### ROCm Version

ROCm 7

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2025-10-08T14:35:02Z)

Hi @tobing. Internal ticket has been created to investigate this issue. Thank!

---

### 评论 #2 — tobing (2025-10-08T14:39:04Z)

> Hi [@tobing](https://github.com/tobing). Internal ticket has been created to investigate this issue. Thank!

Thanks

---

### 评论 #3 — zichguan-amd (2025-10-16T14:29:30Z)

Hi @tobing, images in `rocm/vllm` are currently focused on Instinct series and the 7.0.0 image does not support Radeon. Please try the navi images in `rocm/vllm-dev` like `rocm/vllm-dev:rocm7.0.2_navi_ubuntu22.04_py3.10_pytorch_2.8_vllm_0.10.2rc1`. The navi images are tested and optimized for Radeon GPUs.

---

### 评论 #4 — tobing (2025-10-17T01:58:56Z)

> Hi [@tobing](https://github.com/tobing), images in `rocm/vllm` are currently focused on Instinct series and the 7.0.0 image does not support Radeon. Please try the navi images in `rocm/vllm-dev` like `rocm/vllm-dev:rocm7.0.2_navi_ubuntu22.04_py3.10_pytorch_2.8_vllm_0.10.2rc1`. The navi images are tested and optimized for Radeon GPUs.

Hi **@zichguan-amd**,

I have tried `rocm⁄vllm-dev:rocm7.0.2_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1` and it is working. 

I just realized 
`rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909` same as 
`rocm⁄vllm-dev:rocm7.0.2_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1`. Both using `vllm 0.10.x`

For `rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006`, it is using `vllm 0.11.x` not `vllm 0.10.x`

I tried to build `vllm 0.11.0` manually using this command
`docker build --build-arg ARG_PYTORCH_ROCM_ARCH=gfx1101 -f docker/Dockerfile.rocm -t vllm-rocm .`
and I got same error

Seems like `vllm 0.11.x` backward compatibility issue

[rocm⁄vllm-dev:rocm7.0.2_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1.txt](https://github.com/user-attachments/files/22961664/rocm.vllm-dev.rocm7.0.2_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1.txt)
[vllm-manual-build.txt](https://github.com/user-attachments/files/22961665/vllm-manual-build.txt)

---

### 评论 #5 — zichguan-amd (2025-10-20T16:09:32Z)

Good to hear that it's working for you. And thanks for testing with `vllm 0.11.x`, I've tried `rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006` and building `v0.11.0` on MI300 and it seems that the model `AIDC-AI/Ovis2-8B-GPTQ-Int4` is not compatible with vllm `v0.11.x`. I was able to run other models like `Qwen/Qwen2.5-1.5B-Instruct` and `deepseek-ai/deepseek-llm-7b-chat` without any problems.
torch versions when building docker image from source (vllm 0.11.0+rocm700):
```
# pip freeze | grep torch
torch @ file:///install/torch-2.8.0%2Bgitb2fb688-cp312-cp312-linux_x86_64.whl#sha256=5c9cd11c61141f5fbcbcfd4b821d9209b95cf183f5e4bdacd29ead9dfd1fdc4f
torchvision @ file:///install/torchvision-0.23.0a0%2B824e8c8-cp312-cp312-linux_x86_64.whl#sha256=db9eafa759223583e8f7e234e22a058583ff90ab4ca4092ef0256263ffbe5926
```
torch versions in `rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006`:
```
#  pip freeze | grep torch
torch @ file:///install/torch-2.9.0a0%2Bgit1c57644-cp312-cp312-linux_x86_64.whl#sha256=b278e8de81124d117ccfba2114ea2ed18a8e4a336b411edcd1e73af316c0d33e
torchvision @ file:///install/torchvision-0.23.0a0%2B824e8c8-cp312-cp312-linux_x86_64.whl#sha256=2114a0a9fed67bd1e56830cf24115bdd85832918a63747e32044bdbb7aa28bf4
```

---

### 评论 #6 — tobing (2025-10-21T00:26:55Z)

I have tested if set ```--limit-mm-per-prompt.image 0``` I can run **AIDC-AI/Ovis2-8B-GPTQ-Int4** model. 

[vllm-rocm7.0.0_vllm_0.10.2_20251006_image0.txt](https://github.com/user-attachments/files/23010755/vllm-rocm7.0.0_vllm_0.10.2_20251006_image0.txt)

When I set ```--limit-mm-per-prompt.image 1``` I got this error.


No issue for these vision models
**OpenGVLab/InternVL3_5-2B
openbmb/MiniCPM-V-4_5-AWQ**

Seems vllm 0.11.x support for **AIDC-AI/Ovis2-8B-GPTQ-Int4** model is broken

 

---

### 评论 #7 — zichguan-amd (2025-10-21T13:39:22Z)

Good find, you can maybe file an issue against vllm or Ovis.

---

### 评论 #8 — tobing (2025-10-21T13:53:56Z)

Yes. I will do that.
Thanks 

---
