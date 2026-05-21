# [Issue]: When comfyui uses the ComfyUI-WanVideoWrapper plug-in to generate a video, the driver timeout occurs 100% in the WanVideo Decode node

> **Issue #4453**
> **状态**: closed
> **创建时间**: 2025-03-06T08:57:59Z
> **更新时间**: 2025-04-03T15:11:45Z
> **关闭时间**: 2025-04-03T15:11:44Z
> **作者**: githust66
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4453

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.3.2** (颜色: #ededed)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

When comfyui uses the Universal Vientiane plug-in to generate a video, the driver timeout occurs 100% in the WanVideo Decode node  

![Image](https://github.com/user-attachments/assets/8df602a4-cd38-459d-a36e-1e3a32e9dd8f)

### Operating System

NAME="Ubuntu" VERSION="22.04.5 LTS (Jammy Jellyfish)"

### CPU

AMD Ryzen 7 7700 8-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.3.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — githust66 (2025-03-06T09:10:47Z)

[Unsaved Workflow (1).json](https://github.com/user-attachments/files/19104963/Unsaved.Workflow.1.json)
The above is the comfyui workflow being used, with a memory size of 3 * 16G.

---

### 评论 #2 — ppanchad-amd (2025-03-06T15:48:06Z)

Hi @githust66. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — githust66 (2025-03-06T16:36:37Z)

> Hi [@githust66](https://github.com/githust66). Internal ticket has been created to investigate this issue. Thanks!

Thank you. After updating the latest 25.3.1 driver, there was no timeout, but it took more than 800 seconds on this node

---

### 评论 #4 — githust66 (2025-03-07T01:24:18Z)

When running to the WanVideo Decode node, the GPU utilization is consistently at 1%-2%

---

### 评论 #5 — githust66 (2025-04-03T05:52:41Z)

After updating to the latest ComfyUI, ComfyUI-WanVideoWrapper plug, and the 2025.3.2 driver, this issue no longer exists, However, the WanVideo ImageClip Encode  node Or the Wan Image to Video or WanVideo VACE Encode node in ComfyUI runs very slowly. It takes about 500 seconds to execute this node. he GPU utilization is consistently at 5%-8%
The decoding works fine, but there is a problem with the encoding.

![Image](https://github.com/user-attachments/assets/bbcedbc0-ddad-4c11-aa69-6a3500d68110)

![Image](https://github.com/user-attachments/assets/f93fc01a-bbc0-4097-b1d8-89bf25dfb83a)

---

### 评论 #6 — githust66 (2025-04-03T15:11:40Z)

After updating to the latest ComfyUI, ComfyUI-WanVideoWrapper plug, and the 2025.3.2 driver, this issue no longer exists, The new issue is not related to the title of this issue and has been created as a separate issue.
https://github.com/ROCm/ROCm/issues/4559

---
