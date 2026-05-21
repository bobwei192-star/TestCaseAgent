# [Issue]: amdgpu_cs_ioctl returns -ENOMEM under sustained ROCm churn — TTM eviction LRU candidates transiently busy; fixable with bounded caller-level retry

> **Issue #6215**
> **状态**: open
> **创建时间**: 2026-05-10T10:25:22Z
> **更新时间**: 2026-05-12T13:37:17Z
> **作者**: Deaththegrim
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6215

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述


### Summary

`amdgpu_cs_ioctl` returns `-ENOMEM` to userspace on ~0.01% of CS submissions during sustained ROCm workloads with `--lowvram`-style per-layer model paging (e.g. ComfyUI on 16 GB VRAM running SDXL + multi-pass detailer). The kernel emits `Not enough memory for command submission!` via un-ratelimited `drm_err`, flooding dmesg.

bpftrace traces show the failure originates in `ttm_bo_validate → ttm_bo_alloc_resource` returning `-ENOSPC` even with `force_space=true` (eviction allowed). After ~1 ms wait the eviction LRU candidates have completed their in-flight CS / fence-pending references and a re-attempt succeeds.

This is **not** the GPU-VM-exhaustion class (which freezes the system); this is a steady-state throughput regression where Comfy retries the failed submit and the system keeps running, but kworker time and CS latency climb sharply during high-churn periods (~7× throughput drop observed in our test).

### Reproduction (RX 9070 XT, gfx1201)

- DKMS `amdgpu/6.18.4-2286447.24.04` (graphics 7.2.3, ROCm 7.2.3), kernel `6.17.0-1020-oem`
- ComfyUI 0.20.1 + PyTorch 2.10.0.dev (rocm6.3)
- Comfy launched with `--lowvram --async-offload --fp8_e4m3fn-text-enc --reserve-vram 2.0 --cache-none --no-cache-models --use-pytorch-cross-attention`
- `PYTORCH_HIP_ALLOC_CONF=max_split_size_mb:256,garbage_collection_threshold:0.4`
- Workload: SDXL + SmartDetailer 3-pass, 16 back-to-back workflows in 30 min

Result: ~1.86 M total CS submissions, **173 -ENOMEM returns from `cs_ioctl` (0.0093 %)** observable via `kretprobe:amdgpu_cs_ioctl`. Underlying `amdttm_bo_validate` failure rate is higher (1841 / 36 M = 0.0051 %) because most placement failures are absorbed internally; the rest propagate to userspace.

### Proposed fix

Caller-level bounded-time retry around `amdgpu_cs_parser_bos` in `amdgpu_cs_ioctl`, modelled on Intel Xe's `xe_vm_validate_should_retry` pattern. Caller-level retry is the correct layer per upstream TTM maintainer guidance — TTM core changes for this class are off-limits.

- 28 net-new lines
- 50 ms total budget per submission
- Signal-aware (bails on pending signal so user-mode SIGINT still works)

Patch + full bug report with bpftrace numbers, dmesg traces, and diff context available locally — happy to post the full text in a follow-up comment or email.

### Environment

- AMD RX 9070 XT (RDNA4, gfx1201, 17.1 GB VRAM)
- AMD Ryzen 9 9950X3D, 32 GB DDR5
- Linux 6.17.0-1020-oem
- DKMS `amdgpu/6.18.4-2286447.24.04`, ROCm 7.2.3

Mirroring this to gitlab.fd.o/drm/amd issues for the kernel maintainers.

