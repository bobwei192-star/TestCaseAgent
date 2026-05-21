# [Feature]: NVMe <---> GPU VRAM DMA/RDMA

> **Issue #5837**
> **状态**: closed
> **创建时间**: 2026-01-07T10:05:45Z
> **更新时间**: 2026-01-10T04:37:14Z
> **关闭时间**: 2026-01-10T04:37:14Z
> **作者**: maifeeulasad
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5837

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Suggestion Description

I’d like to propose adding GPU-direct storage support to ROCm - specifically, the ability for storage devices (e.g., NVMe SSDs) to DMA directly into GPU memory (VRAM) without staging data through host memory.

This would be conceptually similar to NVIDIA GPUDirect Storage (GDS), where data can flow:
```
NVMe <---> GPU VRAM
```
instead of:
```
NVMe <---> CPU RAM <---> GPU VRAM
```

Such a capability would significantly reduce CPU overhead, memory bandwidth pressure, and end-to-end latency for data-intensive GPU workloads.

Adding it like a flag will be really awesome, with a fallback to the default old path.

**And willing to work on this one.**

Good reads:
 - https://github.com/NVIDIA/gds-nvidia-fs
 - https://developer.nvidia.com/gpudirect
 - https://forums.developer.nvidia.com/t/example-codes-and-reffrence-for-rdma-gpudirect/284591
 - https://github.com/NVIDIA/gdrcopy
 - https://docs.nvidia.com/gpudirect-storage/

### Operating System

*

### GPU

*

### ROCm Component

*

---

## 评论 (6 条)

### 评论 #1 — NairoDorian (2026-01-07T13:11:30Z)

Yes please

---

### 评论 #2 — maifeeulasad (2026-01-07T15:24:03Z)

I just found something interesting, mori (Modular RDMA Interface). It would be nicer if someone from core team could shade some light into this. I am really looking forward to this.

ref:
 - https://github.com/ROCm/mori

---

### 评论 #3 — schung-amd (2026-01-09T16:22:31Z)

Hi @maifeeulasad, thanks for the suggestion. It sounds like mori will provide what you want here; if you have any specific questions I can forward them to the team.

Also see hipFile, although it is early still: https://github.com/ROCm/hipFile. I don't think there is any public-facing documentation on that yet, but again if you have any questions I can check in with the team to see what we can share at the moment.

---

### 评论 #4 — sbates130272 (2026-01-09T22:43:07Z)

@maifeeulasad I suggest you put a watch on https://github.com/ROCm/hipFile. I think a lot of the things you are looking for are going to appear there pretty soon ;-). Thanks for taking an interest! Note that the MORI project is a bit different as it is more concerned with ephemeral RDMA and not storage related (i.e. NVMe and NVMe-oF etc).

---

### 评论 #5 — gaoikawa (2026-01-09T23:51:45Z)

@maifeeulasad - I'll add that 'coming soon' we will have support in RIXL (https://github.com/ROCm/RIXL - AMD's version of NIXL) for hipFile as one of the RIXL plugins ('cuda_gds' equivalent.)

https://github.com/ROCm/RIXL/blob/develop/README_rocm.md

Thanks.

---

### 评论 #6 — maifeeulasad (2026-01-10T04:37:14Z)

Thanks! I think we can close this as we are already doing this.

Thanks @sbates130272 , for suggesting me this awesome `hipFile` project. I would love to contribute there. If you think I am worthy of implementing anything there, or just something with needs more hands, let me know.

Thanks @gaoikawa , for suggesting this `rixl` plugin. I would love to contribute there. If you need some extra support, please let me know.

I have created an issue in the `hipFile` repo, if someone could answer that, that would be helpful: https://github.com/ROCm/hipFile/issues/153. In the `install.md` file I just found that device supported by ROCm.

Good day everyone! Keep me in your prayer.

---
