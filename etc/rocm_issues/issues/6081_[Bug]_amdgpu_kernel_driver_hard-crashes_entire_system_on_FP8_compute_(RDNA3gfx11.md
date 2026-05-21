# [Bug] amdgpu kernel driver hard-crashes entire system on FP8 compute (RDNA3/gfx1100) - no graceful error

> **Issue #6081**
> **状态**: closed
> **创建时间**: 2026-03-30T02:48:16Z
> **更新时间**: 2026-03-30T14:14:25Z
> **关闭时间**: 2026-03-30T14:14:25Z
> **作者**: Albaloola
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6081

## 描述

## Summary

Running FP8 (fp8_e4m3fn) model inference on an AMD Radeon RX 7900 XTX (gfx1100, RDNA3) causes a complete system hang requiring a hard power cycle. The amdgpu kernel driver does not return an error or gracefully reject the unsupported operation — instead, the GPU MES scheduler hangs and takes the entire system down.

This is a critical driver-level bug. Userspace applications should never be able to hard-crash the kernel.

## Hardware

- **GPU:** AMD Radeon RX 7900 XTX (24GB VRAM)
- **GPU Architecture:** RDNA3 / gfx1100
- **CPU:** AMD Ryzen 7 5800X
- **RAM:** 32GB
- **Motherboard:** Gigabyte B550 AORUS Pro V2

## Software

- **OS:** Arch Linux (rolling)
- **Kernels tested:** linux-zen 6.19.9, linux 6.13.8 (standard)
- **ROCm versions tested:** 7.2.0 (system), 6.4, 6.2 (via PyTorch bundled libs and Docker)
- **PyTorch versions tested:** 2.11.0+rocm7.2, 2.8.0+rocm6.4, 2.6.0+rocm6.2.4
- **Application:** ComfyUI (image generation)
- **Model:** Qwen-Image-Edit (fp8_e4m3fn quantized safetensors)

## Steps to Reproduce

1. Install PyTorch with ROCm support on a system with RX 7900 XTX
2. Load an FP8 (fp8_e4m3fn) diffusion model in ComfyUI (or any PyTorch application)
3. Attempt inference (e.g., queue an image generation)
4. **System completely freezes** — no mouse, no keyboard, no SSH, no TTY. Only a hard power reset recovers the machine.

## Expected Behavior

The driver should either:
1. **Return a proper error** (e.g., "FP8 compute not supported on this device"), or
2. **Fall back to a supported precision** automatically, or
3. At minimum, **kill the offending process** without crashing the entire system

## Actual Behavior

The amdgpu kernel driver hangs completely. The GPU MES (Micro Engine Scheduler) becomes unresponsive. The entire system locks up. No kernel panic, no OOM kill, no dmesg output — just a complete freeze requiring physical power cycle.

## What Was Tried (All Crashed)

Over the course of several hours, the following were systematically tested. **All resulted in the same hard system crash:**

- 3 different PyTorch versions (2.6.0, 2.8.0, 2.11.0)
- 3 different ROCm versions (6.2, 6.4, 7.2)
- 2 different kernels (linux-zen 6.19.9, linux 6.13.8)
- Docker isolation (ROCm 6.2 container on ROCm 7.2 host)
- Every ComfyUI VRAM mode: `--normalvram`, `--lowvram`, `--novram`
- Environment variables: `HSA_ENABLE_SDMA=0`, `AMD_DIRECT_DISPATCH=0`, `AMD_SERIALIZE_KERNEL=3`, `GPU_MAX_HW_QUEUES=1`
- Complete removal of system ROCm (using only PyTorch bundled ROCm libs)
- `LD_LIBRARY_PATH` overrides to prevent library conflicts

## Resolution (Workaround)

The crash **only** occurs with FP8 models. Replacing the FP8 models with:
- **GGUF quantized** (Q8_0) diffusion model
- **BF16** text encoder

immediately resolved the issue. The same workflow, same GPU, same driver — zero crashes. This confirms the root cause is specifically FP8 compute on RDNA3.

## Impact

- **~10 hard power cycles** were required during debugging
- Risk of filesystem corruption, NVMe wear, and data loss from repeated unclean shutdowns
- Users with RDNA3 GPUs have no warning that FP8 models will crash their system
- Many popular AI models (Stable Diffusion, Qwen, Flux) ship FP8 variants as default/recommended downloads
- This affects every RDNA3 consumer GPU user attempting to run FP8 AI models

## Request

1. The amdgpu kernel driver must never allow a userspace compute operation to hang the entire system
2. FP8 operations on hardware that does not fully support them should fail gracefully with a clear error message
3. If RDNA3 has partial FP8 silicon support, the ROCm stack should properly expose (or explicitly block) it rather than crashing silently

This is not a performance bug or a feature request. This is a **system stability and data safety issue**.

---

## 评论 (1 条)

### 评论 #1 — Albaloola (2026-03-30T14:14:25Z)

Closing this - the root cause turned out to be a btrfs swap deadlock, not an amdgpu/FP8 issue. We had swap running through a loop device on a btrfs filesystem (copy-on-write), which caused a kernel deadlock under memory pressure during model loading. Replacing it with a raw LVM swap partition fixed the crashes entirely. FP8 compute works fine on RDNA3/gfx1100 with both ROCm 6.4 and 7.2. Apologies for the noise.

---
