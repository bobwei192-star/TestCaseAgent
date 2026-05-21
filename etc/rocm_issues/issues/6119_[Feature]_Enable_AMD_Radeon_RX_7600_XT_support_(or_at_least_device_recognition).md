# [Feature]: Enable AMD Radeon RX 7600 XT support (or at least device recognition) for ROCm on WSL2

> **Issue #6119**
> **状态**: closed
> **创建时间**: 2026-04-04T11:48:18Z
> **更新时间**: 2026-05-13T18:17:22Z
> **关闭时间**: 2026-05-13T18:17:22Z
> **作者**: junarwohn
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6119

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Suggestion Description

I would like to formally suggest official support, or at least basic device recognition, for the AMD Radeon RX 7600 XT on WSL2.

Currently, many users (including myself) are successfully using the RX 7600 XT on native Ubuntu environments by utilizing the HSA_OVERRIDE_GFX_VERSION=11.0.0 environment variable. While I understand this specific SKU is not on the official support list, it is proven to be functionally capable of running ROCm workloads with the override.

The primary issue is that on WSL2, the device is not recognized or passed through correctly to the ROCm stack, making it impossible to even attempt the override.

### Operating System

Windows

### GPU

7600XT

### ROCm Component

_No response_

---

## 评论 (4 条)

### 评论 #1 — schung-amd (2026-04-10T15:06:04Z)

Thanks for the report, I'll take a look.

---

### 评论 #2 — schung-amd (2026-04-14T14:09:09Z)

First of all, thanks for your interest in using ROCm! We're aware that historically our support for older/less performant cards has been lacking, and while we have clawed back a lot of that space with expanded device support in TheRock there is still work to be done.

We're planning to expose the device list in librocdxg to allow users to enable unsupported devices. Note that of course as these devices will still be unsupported there is no expectation or guarantee of functionality or performance. That being said, as gfx1102 in particular is already supported via TheRock (see https://github.com/ROCm/TheRock/blob/main/SUPPORTED_GPUS.md), I'd expect it to work in WSL eventually; if not immediately via librocdxg enablement then further down the line in future ROCm versions.

If everything goes smoothly the device enablement might be possible in the next few weeks. As a side note, I'd encourage anyone currently using a 7600 with the HSA override to try TheRock.

---

### 评论 #3 — junarwohn (2026-04-14T14:27:09Z)

Thanks again for the update.

Even if full support is still incomplete, I would really appreciate it if WSL device recognition could be enabled as soon as possible. Just being able to detect and try the card there would already be a big help.

I understand unsupported devices come with no guarantees, but even that first step would mean a lot. In the meantime, I will also give TheRock a try as you suggested.

Thanks again for the transparency and for the work on expanding support.


---

### 评论 #4 — schung-amd (2026-05-13T18:17:20Z)

Hi, sorry for the delay on this! We have exposed the supported device list in https://github.com/ROCm/librocdxg/blob/develop/shared/src/utils.cpp, so you can try adding the 7600 yourself. The new entry to the gfxip table for the 7600 should look like `{ DEVICE_ID, 11, 0, 2 }` where DEVICE_ID is the identifier for your device; you can get this in Windows in the Device Manager > Display adapters > Right click your GPU and go to properties > Details tab > Hardware IDs. For example, on an 840M:

<img width="587" height="684" alt="Image" src="https://github.com/user-attachments/assets/ff45d125-811b-4405-95b7-688cbc2ff52b" />

DEVICE_ID in this case would be 0x1114.

I'll close this for now as this is our current path to hardware enablement, we can reopen at a later date if necessary. If you run into any difficulties feel free to comment, and we'd be excited to see updates as to how well this works on your system!

---
