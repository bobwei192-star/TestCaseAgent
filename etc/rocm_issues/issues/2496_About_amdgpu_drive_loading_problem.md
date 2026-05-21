# About amdgpu drive loading problem

> **Issue #2496**
> **状态**: closed
> **创建时间**: 2023-09-23T15:46:29Z
> **更新时间**: 2024-07-19T19:32:22Z
> **关闭时间**: 2024-07-19T19:32:21Z
> **作者**: BiliMiku
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2496

## 描述

Loading the amdgpu module in ubuntu 20.04 failed. Procedure
Hardware :Instinct MI250X
After the GPU is powered off, check the dmesg and find the following information:
[  103.397287] [drm] amdgpu: 4294967295M of VRAM memory ready
[  103.397290] [drm] amdgpu: 48114M of GTT memory ready.
[  103.397304] [drm] GART: num cpu pages 131072, num gpu pages 131072
[  103.397313] ioremap: invalid physical address 1000efff0000000
[  103.397316] amdgpu 0000:0a:00.0: amdgpu: (-12) kernel bo map failed
[  103.397319] [drm:amdgpu_fill_buffer [amdgpu]] *ERROR* Trying to clear memory with ring turned off.
Is such VRAM size recognition a hardware problem?
I've tried the vramlimit parameter, but it doesn't seem to work.

---

## 评论 (4 条)

### 评论 #1 — kentrussell (2023-11-10T15:50:07Z)

Is it possible to attach a full dmesg? I haven't seen that error before, but I'll see if I can find anything. It seems to have the right memory/page info. Which ROCm release are you using? Thanks!

---

### 评论 #2 — LunaeRadiance (2024-03-19T12:13:07Z)

It seemed that the number of VRAM is identical to that of the whole Frontier system.Try flashing the firmware？


---

### 评论 #3 — ppanchad-amd (2024-05-14T19:25:06Z)

@BiliMiku Were you able to resolve your issue? Thanks!

---

### 评论 #4 — ppanchad-amd (2024-07-19T19:32:21Z)

@BiliMiku Closing ticket since there is no response for a while. If you still require assistance or believe this issue needs to remain open, please re-open the ticket. Thanks! 

---
