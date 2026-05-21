# ** When the ROCm 7.0 released for windows + AMD APU (AI MAX Pro 395) ? **

> **Issue #5421**
> **状态**: closed
> **创建时间**: 2025-09-24T07:32:45Z
> **更新时间**: 2025-09-29T16:06:34Z
> **关闭时间**: 2025-09-29T16:06:34Z
> **作者**: Bear-Beer
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5421

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

Currently the available version for windows is : **ROCm-6.4.2**
https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html

Where can I get the introduction about the new features & performance uplift in 7.0 for **Radeon and APU**? 



---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2025-09-24T18:46:18Z)

Hi @Bear-Beer, ROCm 6.4.4 has support for the AI MAX APUs + PyTorch on native windows https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx1151. This release does not cover all the features of ROCm 7.0 but is a stepping stone in getting there.

For an overview of the changes and features introduced in ROCm 7.0, please see the release notes over at https://github.com/ROCm/ROCm/releases/tag/rocm-7.0.0.

---

### 评论 #2 — Bear-Beer (2025-09-25T03:22:22Z)

Thanks for the reply. 
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html
From this link, seems Pytorch-2.8+ROCm-6.4.4+Python-3.12 started to support AI Max 395. 
Let me search first to see if there is a existing docker image for this combination.

---

### 评论 #3 — harkgill-amd (2025-09-25T17:12:23Z)

There should be docker images for the 6.4.4 release published within the next couple days.

---

### 评论 #4 — harkgill-amd (2025-09-29T16:06:34Z)

> https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html
From this link, seems Pytorch-2.8+ROCm-6.4.4+Python-3.12 started to support AI Max 395.
Let me search first to see if there is a existing docker image for this combination.

The docker images are starting to trickle in. https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-pytorch.html#use-docker-image-with-pre-installed-pytorch. The one specified here is intended for Radeon as it ships with PyTorch 2.6. You can replace the torch installation with the Ryzen PyTorch on Linux preview in the image for Ryzen support. 

---
