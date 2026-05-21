# [Feature]: Increase ROCm/OpenCL Support for iGPUs (Scientific Compute usecase)

> **Issue #6002**
> **状态**: open
> **创建时间**: 2026-02-26T03:40:50Z
> **更新时间**: 2026-04-06T18:48:03Z
> **作者**: Ncard00123
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6002

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Suggestion Description

AMD is a leader in efficiency-per-watt, but the lack of official, out-of-the-box support for iGPU compute in projects like Folding@Home and BOINC is allowing competitors to close the gap.

While the community has attempted to use ROCm on some APUs, it remains fragmented. In contrast, I have spent the last month in a dedicated thread with Qualcomm developers. They have confirmed they are officially reviewing the implementation of OpenCL 3.0, SYCL, and high-precision math pathways for the Snapdragon X2 specifically to support the scientific community.

If Qualcomm enables their Adreno iGPU for research while AMD's Radeon iGPUs remain difficult to configure, AMD will lose its competitive edge in the "Pro" mobile workstation market.

I urge AMD to provide first-party collaboration with FAH and BOINC to ensure RDNA 3 and 4 iGPUs are whitelisted and optimized. High-precision scientific compute should be accessible on every efficient AMD-powered laptop.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (3 条)

### 评论 #1 — schung-amd (2026-03-03T16:02:19Z)

Hi @Ncard00123, thanks for the interest and the suggestion! Historically ROCm has been strictly incompatible with APUs, but that has changed with ROCm on Ryzen adding support for Strix and Strix Halo. There are two important aspects of your suggestion: extending our APU support to cover more products, and working with ecosystem partners to ensure that we have support on their end as well. The former is the big bottleneck here, we need to get ROCm support for the products first and foremost, and once an APU has ROCm support it should be relatively simple to have it supported in the ecosystem.

I don't currently have info on our plans for broader APU support. I'll reach out to see if we have anything in the works for existing APUs and use this as a signal boost, and I'll update when I have more info. 

---

### 评论 #2 — schung-amd (2026-04-06T17:53:23Z)

@Ncard00123 Can you submit separate issues for specific APU/usecases? You've mentioned RDNA3/4 and FAH, but we'd like more granular and specific issues so we can give each request proper attention.

---

### 评论 #3 — Ncard00123 (2026-04-06T18:48:03Z)

> [@Ncard00123](https://github.com/Ncard00123) Can you submit separate issues for specific APU/usecases? You've mentioned RDNA3/4 and FAH, but we'd like more granular and specific issues so we can give each request proper attention.

The RDNA3 architecture found in Phoenix (7040 series) and Strix Point (8040/9000 series) APUs possesses the necessary hardware specifications for high-efficiency FP32 scientific compute.

However, the current software stack lacks the official whitelisting and driver stability required for Folding@Home (FAH) Core 22/23 to operate without frequent TDR (Timeout Detection and Recovery) resets.

We need a validated OpenCL path that ensures consistent memory management between the unified system RAM and the iGPU to prevent kernel crashes during long-duration simulation runs.

A major technical hurdle is the current driver's tendency to prioritize display preemption over long-running compute kernels, which often results in the "Bad State" error within the FAH client.

Specifically, the OpenCL compiler for RDNA3 must be optimized to handle the dual-issue wave32 instructions correctly for scientific math rather than just gaming shaders.

Providing a dedicated "Compute" toggle or a stable profile for these mobile chips would allow the distributed computing community to utilize AMD’s efficiency-per-watt advantage over competitor mobile solutions.

To move forward, we request that AMD provides first-party collaboration with the Folding@Home team to ensure these iGPUs are recognized as valid OpenCL devices in their hardware database.

This includes providing the necessary ISA (Instruction Set Architecture) documentation and compiler fixes to resolve the fragmentation between ROCm and the standard Adrenalin drivers.

Establishing this support for RDNA3 is a critical prerequisite before addressing the upcoming RDNA4 cycle and maintaining a competitive edge in the mobile workstation market.

---
