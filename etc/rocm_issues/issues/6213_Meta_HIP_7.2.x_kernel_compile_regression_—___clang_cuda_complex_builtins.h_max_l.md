# Meta: HIP 7.2.x kernel compile regression — __clang_cuda_complex_builtins.h ::max lookup fails on Linux

> **Issue #6213**
> **状态**: closed
> **创建时间**: 2026-05-10T09:54:17Z
> **更新时间**: 2026-05-12T13:38:50Z
> **关闭时间**: 2026-05-12T13:38:50Z
> **作者**: Kaden-Schutt
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6213

## 描述

# HIP 7.2.x kernel compile regression on Linux: `__clang_cuda_complex_builtins.h` references undeclared `::max`

Cross-posting to the meta-tracker for routing visibility. Primary issue with full repro, root-cause, and proposed fix is at:

**https://github.com/ROCm/HIP/issues/3894**

## TL;DR

Any HIP kernel compile under ROCm 7.2.0 / 7.2.1 / 7.2.2 on Ubuntu 24.04 and 26.04 (`https://repo.radeon.com/rocm/apt/7.2`) fails immediately with:

```
/usr/include/hip/amd_detail/amd_hip_runtime.h:374:
__clang_cuda_complex_builtins.h:194:27: error: use of undeclared identifier 'max'; did you mean 'fmax'?
```

Cause is an include-order issue in `libamdhip64-dev`'s `amd_hip_runtime.h` (pulls `__clang_cuda_complex_builtins.h` BEFORE `cuda_wrappers/algorithm`). Reproduces on both gfx1151 (Strix Halo iGPU) and gfx1201 (RX 9070 XT, Navi 48) from the same toolchain, so this is host-side, not arch-specific. Confirmed across two distro upgrades (24.04 → 26.04) and two patchlevel bumps (7.2.0 → 7.2.2).

Workaround that compiles cleanly: `-include /opt/rocm-7.2.2/lib/llvm/lib/clang/22/include/__clang_hip_runtime_wrapper.h`.

Full environment, minimal repro, root cause analysis, and three suggested upstream fixes are in the linked HIP issue.


---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2026-05-12T13:38:50Z)

Thanks for the report @Kaden-Schutt. We can continue to work off of https://github.com/ROCm/hip/issues/3894 for this.

---
