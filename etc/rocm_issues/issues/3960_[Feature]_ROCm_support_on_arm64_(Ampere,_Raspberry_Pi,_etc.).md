# [Feature]: ROCm support on arm64 (Ampere, Raspberry Pi, etc.)

> **Issue #3960**
> **状态**: closed
> **创建时间**: 2024-10-30T15:01:18Z
> **更新时间**: 2025-03-05T06:43:24Z
> **关闭时间**: 2024-11-04T14:44:37Z
> **作者**: geerlingguy
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3960

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

I have gotten various generation AMD graphics cards working on the Raspberry Pi 5 (see https://github.com/geerlingguy/raspberry-pi-pcie-devices/issues/222), as well as on Ampere Altra and AmpereOne workstations and servers (see https://community.amperecomputing.com/t/amd-gpus-on-the-altra-devkit-and-other-altras-patches-available-now/336).

For many of these systems, running software like Ollama or other LLMs would be beneficial, and having an alternative to Nvidia graphics cards would provide more options for vendors (and more cash to AMD, since Pro/RX/Enterprise cards could be justified on these systems).

As of 2021, [ROCm was not supported on arm64](https://github.com/ROCm/ROCm/issues/1052), but a few years later, we have much better `amdgpu` driver support (though still requiring some fixes for Arm PCIe implementations where cache coherency is different than amd64).

Is it possible for arm64 support to be explored for AMD GPUs?

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (4 条)

### 评论 #1 — geerlingguy (2024-10-30T15:04:38Z)

Extending this line of thinking: RISC-V is finally exiting the 'development only' mode, and is a viable platform with some servers and desktops coming on the market—which *also* work with AMD GPUs, albeit with similar driver fixups.

Going multi-arch would be useful to allow AMD GPUs to be a standard across any architecture, and building for arm64 would likely introduce fixes that _also_ make it easier to work with RISC-V, as many of the code paths that are broken are due to x86/amd64-isms.

---

### 评论 #2 — sohaibnd (2024-11-04T14:44:37Z)

Hi @geerlingguy, your points are valid and we have been listening to the demand there is for ARM support, but this is not something that is planned yet. If this changes, rest assured that AMD will officially announce this!

---

### 评论 #3 — geerlingguy (2024-11-18T21:45:13Z)

At least I can get Vulkan to work since ROCm won't (and bonus, with llama.cpp at least, this enables a lot of older or lower power cards too, like the 6500 and 7600 XT I'm testing now!).

---

### 评论 #4 — yuningliang (2025-03-05T06:43:22Z)

@geerlingguy you absolutely correct on ROCm of RISC-V. we @deepcomputing are putting effort in porting them too. but we got stuck as lots of hardcoded x86 stuffs. 

---
