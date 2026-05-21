# Support using the Visual Studio generators when CMake HIP language is enabled

> **Issue #2359**
> **状态**: open
> **创建时间**: 2023-07-31T11:27:28Z
> **更新时间**: 2025-05-28T19:50:06Z
> **作者**: MathiasMagnus
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2359

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

Currently, trying to use the Visual Studio generators with CMake when the HIP language is enables results in a hardcoded error. This workflow should be enabled either via the VS extensions or some other method.

[Relevant Kitware ticket.](https://gitlab.kitware.com/cmake/cmake/-/issues/24245)

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-05-14T15:24:36Z)

@MathiasMagnus Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

---

### 评论 #2 — MathiasMagnus (2024-05-14T16:39:55Z)

@ppanchad-amd This is an issue on Windows. As soon as [AMD HIP SDK for Windows](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html) 6.1.1 is released, sure. It's also not strictly speaking a ROCm issue, because the hard configuration error is within the CMake codebase, but it's probably AMD who would need to take action in implementing it, because implementation requires coordination with the HIP Visual Studio extension, which is closed source and changes from ROCm version to version. (The Kitware issue is not a candidate for community contribution.)

---
