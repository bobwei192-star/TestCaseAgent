# [gfx1151 / Strix Halo] ROCm reports VRAM + GTT as total available memory on APU, but pools have different allocation semantics — causes downstream overcounting

> **Issue #6004**
> **状态**: open
> **创建时间**: 2026-02-27T07:11:33Z
> **更新时间**: 2026-02-27T14:47:08Z
> **作者**: NickAllmende
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6004

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- benrichard-amd

## 描述

Title: [gfx1151 / Strix Halo] ROCm reports VRAM + GTT as total available memory on APU, but pools have different allocation semantics — causes downstream overcounting

---

## Note
This issue is created by claude code on my framework machine. It all sounds correct to me, but this is way over my head...

## System Information

| Component | Details |
|---|---|
| GPU | AMD Radeon Graphics (gfx1151, Ryzen AI MAX 300 / Strix Halo) |
| Type | APU / iGPU (unified memory, LPDDR5X) |
| Physical RAM | 128 GiB (shared CPU+GPU) |
| BIOS VRAM carve-out | 8 GiB |
| Kernel | 6.17.0-14-generic |
| ROCm driver | 60342.13 |
| rocm-smi | 5.7.0-1 |

## Observed Behavior

`rocm-smi` reports:

```
GPU[0] VRAM Total Memory (B): 8,589,934,592    (~8 GiB)
GPU[0] GTT  Total Memory (B): 133,143,986,176  (~124 GiB)
```

Ollama (and other ROCm-aware tools) sum these to report **~132 GiB** available GPU memory:

```
inference compute: total="132.0 GiB" available="131.8 GiB"
```

## Problem

On a **discrete GPU**, VRAM and GTT are two separate physical memory pools — adding them is correct.

On an **APU with unified memory** (gfx1151), this is misleading:

- **VRAM pool** (8 GiB): a fixed BIOS carve-out of shared LPDDR5X. Accessible via `hipMalloc` (coarse-grained), but subject to ~8 GiB single-allocation limit on this hardware.
- **GTT pool** (~124 GiB): the remaining system RAM, accessible by the GPU via unified memory. Used by `hipMallocManaged`.

These pools come from the **same physical hardware** — adding them implies 132 GiB of independently usable GPU memory, which is incorrect. The two pools have completely different allocation semantics:

| Pool | Allocator | Practical limit |
|---|---|---|
| VRAM (8 GiB) | `hipMalloc` | ~8 GiB per allocation (coarse-grained limit on gfx1151) |
| GTT (~124 GiB) | `hipMallocManaged` | ~117 GiB (actual system RAM available) |

## Downstream Impact

With 96 GiB BIOS VRAM (previous configuration), ROCm reported **~220 GiB** "available" (96 GiB VRAM + 128 GiB GTT), while `hipMallocManaged` could only use ~32 GiB (system RAM). Ollama allocated based on the inflated 220 GiB figure → OOM-killed by Linux kernel.

After reducing BIOS VRAM to 8 GiB, ROCm now reports ~132 GiB. Ollama calculates default `num_ctx=262144` from this figure — technically manageable, but still inflated.

## Expected Behavior

On APU, ROCm should either:
1. Report the total as `max(VRAM, GTT)` rather than `VRAM + GTT`, since they share physical hardware, or
2. Clearly distinguish VRAM vs. GTT with separate metrics and a "unified_memory=true" flag, so consumers can make correct decisions

## Workaround

- Set BIOS VRAM to minimum (8 GiB) to minimize overcounting
- Use `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` (hipMallocManaged) to bypass the hipMalloc 8 GiB limit
- Set `OLLAMA_MAX_VRAM` to cap what Ollama allocates (note: broken in Ollama 0.17.x)

## Related Issues

- ROCm #5444 — Strix Halo: ROCm only seeing 15.5 GB (kernel fix in 6.15+)
- ROCm #5595 — Strix Halo: ROCm only seeing 62.2 GB
- ollama/ollama #5471 — GTT not counted in Ollama memory calculation

---

## 评论 (1 条)

### 评论 #1 — chejh-amd (2026-02-27T08:42:45Z)

Hi @NickAllmende We noticed there are actionable solutions in the comments of another similar ROCm memory reporting [issue,](https://github.com/ROCm/ROCm/issues/5595#issuecomment-3461534125) and we’d appreciate it if you could try them to see if resolve your APU memory overcounting problem.

---
