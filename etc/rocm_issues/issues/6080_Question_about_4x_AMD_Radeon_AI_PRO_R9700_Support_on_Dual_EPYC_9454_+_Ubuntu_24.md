# Question about 4x AMD Radeon AI PRO R9700 Support on Dual EPYC 9454 + Ubuntu 24.04 + ROCm 7.1.1

> **Issue #6080**
> **状态**: closed
> **创建时间**: 2026-03-30T02:48:06Z
> **更新时间**: 2026-04-20T14:08:05Z
> **关闭时间**: 2026-04-20T14:08:04Z
> **作者**: ninggadadad
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6080

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

Hello,
I plan to build two workstations with identical configurations:
Hardware: 2×AMD EPYC™ 9454, 256GB RAM, 2×SSD RAID 1, 4×AMD Radeon AI PRO R9700, requiring 8 PCIe 16x slots
Machine 1: Ubuntu 24.04 + ROCm 7.1.1 for AI development
Machine 2: Windows for rendering tasks
Questions:
1.Can this hardware platform properly detect all 4 R9700 GPUs under both Ubuntu 24.04 + ROCm 7.1.1 and Windows?
2.Is this software and hardware combination officially supported by ROCm 7.1.1? Are there any required BIOS/PCIe settings?
3.Please recommend compatible motherboard models from the official perspective.
Thank you for your support.







Can I use this hardware and software combination for machine learning tasks?
Are there any specific BIOS settings I need to configure for this hardware and software combination?
What is the maximum number of GPUs that can be supported by this motherboard?


---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2026-04-10T15:15:32Z)

Hey @ninggadadad,

With ROCm 7.1.1, your 4xR9700 GPU setup will be correctly detected in both Windows and Ubuntu, however; only the latter has full mGPU support currently. We're working on bringing more mGPU support over to Windows but this is still a WIP. The [mGPU setup and configuration page](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/mgpu.html#mgpu-setup-and-configuration) has more information on this including best practices and BIOS/PCIe setup. As for motherboards, anything that supports more modern ThreadRipper or EPYC CPUs should be sufficient for your setup - for info on exact models and recommendations, you can fill out this form to get connected with a sales rep https://www.amd.com/en/forms/product-inquiry/commercial-contact-sales.html.

---
