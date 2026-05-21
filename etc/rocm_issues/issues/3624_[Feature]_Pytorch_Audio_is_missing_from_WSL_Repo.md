# [Feature]: Pytorch Audio is missing from WSL Repo

> **Issue #3624**
> **状态**: closed
> **创建时间**: 2024-08-20T20:33:21Z
> **更新时间**: 2024-11-27T15:22:17Z
> **关闭时间**: 2024-11-27T15:22:17Z
> **作者**: xCentral
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3624

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

I'm having trouble finding a PyTorch Audio version that is compatible with the current PyTorch version provided in the WSL ROCM repo. I'd appreciate if the maintainers could look into providing a compatible PyTorch Audio version that I can use. Alternatively, if there's already a compatible PyTorch Audio version available, please let me know so I can use that. I'm happy to provide any additional details about my setup to help resolve this issue.
The Repo in question: https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/

### Operating System

Ubuntu

### GPU

7900XTX

### ROCm Component

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2024-08-22T13:52:05Z)

Hi @xCentral, let me confirm the compatible Torchaudio version and get back to you. 

---

### 评论 #2 — evshiron (2024-09-05T16:48:25Z)

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1

# replace libhsa-runtime64.so so torch.cuda.is_available() returns True
location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
```

---

### 评论 #3 — xCentral (2024-09-06T16:19:54Z)

> ```shell
> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
> 
> # replace libhsa-runtime64.so so torch.cuda.is_available() returns True
> location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
> cd ${location}/torch/lib/
> rm libhsa-runtime64.so*
> cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> ```

Hiya, my goal was to stick with AMD's repo, and in hopes they would actually update their repo for WSL. As it's recommended by themselves on their page. However I've been using that in the mean time.  It seems like WSL is being kind of overlooked, atleast in terms of upkeep sadly.

---

### 评论 #4 — evshiron (2024-09-06T17:05:20Z)

Well, in my opinion the wheels in AMD repo are the wheels they have extensively tested against WSL. It's not necessary to stick with those as long as the official ones actually work.

Honestly speaking, it's a smart strategy to release a support for WSL. Although it's still in beta, it already allows many AI applications to work pretty well.

Ultimately, working with WSL should be like Linux: it will no longer need to manually patch anything, and the official wheels should just work. Just like today's NVIDIA experience.

---

### 评论 #5 — harkgill-amd (2024-11-27T15:22:17Z)

Hi @xCentral, torchaudio wheels will be uploaded to [https://repo.radeon.com/rocm/manylinux/](https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1.3/) starting with ROCm 6.3. 

In the meantime, you can use the generic wheels from [download.pytorch.org/whl/rocm6.1](https://download.pytorch.org/whl/rocm6.1) as highlighted by @evshiron.

---
