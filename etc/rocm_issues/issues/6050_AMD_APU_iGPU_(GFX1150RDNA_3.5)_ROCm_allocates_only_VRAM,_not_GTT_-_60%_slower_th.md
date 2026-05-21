# AMD APU iGPU (GFX1150/RDNA 3.5): ROCm allocates only VRAM, not GTT - 60% slower than Vulkan

> **Issue #6050**
> **状态**: open
> **创建时间**: 2026-03-20T17:34:38Z
> **更新时间**: 2026-05-14T14:06:53Z
> **作者**: benrichard-amd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6050

## 负责人

- benrichard-amd

## 描述

## Description

(Original ticket: https://github.com/lemonade-sdk/llamacpp-rocm/issues/57)

On AMD Ryzen AI 9 HX370 with Radeon 890M integrated graphics (GFX1150/RDNA 3.5), the ROCm backend is significantly slower than Vulkan due to memory allocation limitations.

### Hardware
- **CPU:** AMD Ryzen AI 9 HX370
- **iGPU:** AMD Radeon 890M (GFX1150, RDNA 3.5)
- **Memory:** 96GB system RAM
- **VRAM:** ~48GB (from BIOS)
- **GTT:** ~43GB
- **ROCm:** 7.2

### Benchmark Results

| Backend | pp512 (tokens/s) | tg128 (tokens/s) |
|---------|------------------|------------------|
| Vulkan  | 370              | 23               |
| ROCm    | 150              | 18               |

**ROCm is 60% slower on prompt processing.**

### Root Cause: Buffer Allocation

| Backend | GPU Buffer | CPU Buffer | Graph Splits |
|---------|-----------|------------|--------------|
| Vulkan  | 80,562 MiB | 315 MiB | ~1-2 |
| ROCm    | 39,217 MiB | 41,660 MiB | **94** |

The 94 graph splits cause:
- 400ms `sched_reserve` delay after model loading
- High first token latency
- Constant GPU↔CPU data transfers during inference

### Analysis

**Vulkan** uses `vkAllocateMemory` with `VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT`, accessing both VRAM (48GB) and GTT (43GB) = ~88GB total.

**ROCm** uses `hipMalloc` which only allocates in dedicated VRAM (~48GB). The `hipMallocManaged` path (enabled via `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1`) falls back to `hipMalloc` with "not supported" on this hardware.

```
Device 0: AMD Radeon 890M Graphics, gfx1150 (0x1150), VMM: no, Wave Size: 32
```

### Memory Available (from sysfs)

```
/sys/class/drm/card0/device/mem_info_vram_total: 51539607552 (48GB)
/sys/class/drm/card0/device/mem_info_gtt_total:  42949672960 (40GB)
Total available:                                  94489280512 (88GB)
```

### Possible Solutions

1. **Use `hipHostMalloc` with `hipHostMallocMapped`** for GTT access (similar to Vulkan's HOST_VISIBLE)
2. **Request AMD/ROCm** to enable `hipMallocManaged` support on GFX1150
3. **Hybrid allocation strategy** - VRAM for hot tensors, pinned host memory for overflow

### Related

- llama.cpp #17368 (UMA support for DGX Spark)
- The `integrated` detection is disabled in upstream ggml-cuda.cu line 233
