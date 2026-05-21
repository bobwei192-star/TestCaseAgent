# Hardware support documentation and gfx1031

> **Issue #2353**
> **状态**: closed
> **创建时间**: 2023-07-29T14:54:41Z
> **更新时间**: 2025-08-26T15:41:32Z
> **关闭时间**: 2024-02-14T08:28:57Z
> **作者**: theAeon
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2353

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- Maetveis

## 描述

Hi! I was checking out the new HIP SDK for windows and I noticed that the hardware support page refers to the 67xx GPUs as gfx1032. I'm pretty sure this is incorrect? All other documentation I can find refers to Navi 22 GPUs as target gfx1031-and there _are_ reports of success compiling HIP for that target on the linux side of things. Is this an error, and if so can the documentation be corrected and support clarified? Appreciate it.

---

## 评论 (6 条)

### 评论 #1 — saadrahim (2023-07-31T16:49:43Z)

@Maetveis can you double check the tables? I think we probably made a typo.

---

### 评论 #2 — berinaniesh (2023-08-02T08:37:39Z)

gfx1031 is not yet supported AFAIK. 
Tensorflow says "Ignoring visible gpu device (device: 0, name: , pci bus id: 0000:03:00.0) with AMDGPU version : gfx1031. The supported AMDGPU versions are gfx1030, gfx900, gfx906, gfx908, gfx90a."
Pytorch recognizes the GPU, but seg faults if any operation is done on the tensors stored on the GPU. 
My device is 6800m (Asus G513QY laptop). 

---

### 评论 #3 — cgmb (2023-08-23T17:41:45Z)

The RX 67XX GPUs are indeed gfx1031. I own an RX 6750 XT myself. You might have some troubles building libraries for gfx1031, so you're usually better off either:
1. Using OS packages from third-parties like Arch or Debian which have enabled gfx1031 support, or
2. On Linux, setting your environment with `export HSA_OVERRIDE_GFX_VERSION=10.3.0` to use gfx1030 code objects on gfx1031.

---

### 评论 #4 — berinaniesh (2023-08-23T18:28:38Z)

@cgmb `HSA_OVERRIDE_GFX_VERSION` works BTW. 

---

### 评论 #5 — parbenc (2024-02-14T08:28:57Z)

I double checked the architecture targets on both the windows and linux sides of the documentation. They are accurate and need no further changes

---

### 评论 #6 — ai-nikolai (2025-08-26T15:41:31Z)

@parbenc - we are running into interesting issues on our vllm inference on multi MI210, on the latest pytorch+rocm. Specifically, we see:

```
[1;36m(VllmWorker TP0 pid=931083)[0;0m /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/utils.py:98: UserWarning: failed to open file '/app/afo_tune_device_0_full.csv' for writing; your tuning results will not be saved (Triggered internally at /app/pytorch/aten/src/ATen/hip/tunable/Tunable.cpp:645.)
[1;36m(VllmWorker TP0 pid=931083)[0;0m   return torch.nn.functional.linear(x, weight, bias)
Memory access fault by GPU node-4 (Agent handle: 0x4419e6b0) on address 0x7f74a1400000. Reason: Unknown.
```

---

Some sources suggested using `HSA_OVERRIDE_GFX_VERSION`. Do you think so too? If so, where can we look up the versions to use.

---
