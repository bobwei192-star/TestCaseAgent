# ROCm for koboldai hipErrorNoBinaryForGpu: Unable to find code object for all current devices!

> **Issue #2061**
> **状态**: closed
> **创建时间**: 2023-04-18T12:18:30Z
> **更新时间**: 2023-04-19T19:53:27Z
> **关闭时间**: 2023-04-19T19:53:27Z
> **作者**: Colon101
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2061

## 描述

i have an rx 6600 and a i5 8400 i just want to try an old model for gpu test and it just spits out hipErrorNoBinaryForGpu: Unable to find code object for all current devices! every time i dont know much about ROCm or anything and would like to know  if i did something wrong im using arch and installed rocm with AUR like this 
yay -S rocm-hip-sdk rocm-opencl-sdk
if you need to see any hardware just tell me

---

## 评论 (3 条)

### 评论 #1 — SurnameLiu (2023-04-19T17:43:56Z)

gpus below navi 21 is not officially supported unfortunately.
i don't know if this will work for you but i managed to get my 6700xt detected by putting "export HSA_OVERRIDE_GFX_VERSION=10.3.0" in the terminal before running koboldai.

---

### 评论 #2 — Colon101 (2023-04-19T19:46:26Z)

just export HSA_OVERRIDE_GFX_VERSION=10.3.0
like nothing else?


---

### 评论 #3 — Colon101 (2023-04-19T19:53:27Z)

oh wow it actually works for me now kinda weird how just a wine liner can fix it thank you i guess it is as simple as export HSA_OVERRIDE_GFX_VERSION=10.3.0

---
