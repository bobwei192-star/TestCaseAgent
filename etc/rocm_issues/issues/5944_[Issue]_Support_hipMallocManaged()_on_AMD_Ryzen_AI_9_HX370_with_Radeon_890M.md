# [Issue]: Support hipMallocManaged() on AMD Ryzen AI 9 HX370 with Radeon 890M

> **Issue #5944**
> **状态**: open
> **创建时间**: 2026-02-09T11:46:29Z
> **更新时间**: 2026-02-11T21:55:36Z
> **作者**: iz0eyj
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5944

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

# GFX1150 (RDNA 3.5 APU): hipMallocManaged not supported, VMM disabled - cannot use GTT memory

## Summary

On AMD Ryzen AI 9 HX370 with Radeon 890M integrated graphics (GFX1150/RDNA 3.5), several HIP memory features are disabled or unsupported, preventing efficient use of the unified memory architecture.

## Environment

- **CPU/APU:** AMD Ryzen AI 9 HX370
- **iGPU:** AMD Radeon 890M (GFX1150, RDNA 3.5)
- **ROCm Version:** 7.2.26015
- **OS:** Linux (kernel 6.x)
- **Driver:** amdgpu

## Issues Observed

### 1. hipMallocManaged returns "not supported"

When calling `hipMallocManaged()`, it fails with `hipErrorNotSupported`, forcing fallback to `hipMalloc()`.

```cpp
hipError_t err = hipMallocManaged(&ptr, size);
// Returns hipErrorNotSupported on GFX1150
```

### 2. VMM (Virtual Memory Management) disabled

The device reports VMM as unavailable:

```
Device 0: AMD Radeon 890M Graphics, gfx1150 (0x1150), VMM: no, Wave Size: 32
```

### 3. hipMalloc limited to VRAM only

`hipMalloc()` can only allocate within dedicated VRAM (~48GB configured in BIOS), not in GTT (Graphics Translation Table) memory (~43GB available).

**Memory available (from sysfs):**
```
/sys/class/drm/card0/device/mem_info_vram_total: 51539607552 (48GB)
/sys/class/drm/card0/device/mem_info_gtt_total:  42949672960 (40GB)
Total available for GPU:                          94489280512 (88GB)
```

But `hipMalloc` can only use the 48GB VRAM portion.

## Impact

This significantly impacts workloads that need more memory than VRAM alone. For example, in llama.cpp:

- **Vulkan backend:** Allocates 80GB on GPU using `VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT` (VRAM + GTT)
- **ROCm/HIP backend:** Allocates only 39GB on GPU, rest falls back to CPU

This results in **60% slower inference** on ROCm compared to Vulkan on the same hardware.

## Feature Request

Please enable on GFX1150 (RDNA 3.5 APU):

1. **`hipMallocManaged`** - Allow managed memory allocation that can use both VRAM and GTT
2. **VMM support** - Enable Virtual Memory Management for dynamic memory paging
3. **Alternative:** Provide a way to allocate in GTT via `hipHostMalloc` with `hipHostMallocMapped` that performs well for GPU compute

## Additional Context

- The Vulkan driver on the same hardware correctly handles unified memory
- `hipMemGetInfo()` only reports VRAM, not the total addressable memory
- `prop.integrated` returns correctly for this iGPU

## Related

- llama.cpp performance regression on AMD APU
- Similar UMA systems (like NVIDIA DGX Spark) have workarounds in place

### Operating System

Debian 13

### CPU

Ryzen AI 9 HX370

### GPU

Radeon 890M

### ROCm Version

ROCm 7.2.26015

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — huanrwan-amd (2026-02-11T21:54:27Z)

Hi @iz0eyj, thanks for posting. AFAK, the support for gfx1150 is limited and work in progress. There are some good discussions on https://github.com/ROCm/ROCm/issues/5108


---
