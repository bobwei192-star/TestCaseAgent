# [SOLVED] Strix Halo (gfx1151) - ROCm only seeing 15.5GB instead of allocated VRAM

> **Issue #5444**
> **状态**: closed
> **创建时间**: 2025-09-29T14:18:30Z
> **更新时间**: 2026-04-27T06:56:17Z
> **关闭时间**: 2025-10-07T20:50:39Z
> **作者**: saross
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5444

## 描述

### Problem Description
Strix Halo systems (gfx1151) with large VRAM allocations are limited to only ~15.5GB visible memory in the ROCm/HIP runtime, despite the kernel correctly seeing the full allocation. This is affecting all users with Ryzen AI MAX+ processors trying to use the unified memory architecture for LLM workloads.

### Affected Configuration
- **Hardware:** AMD Ryzen AI MAX+ (Strix Halo) with Radeon 8060S (gfx1151)
- **Memory:** Any system with >16GB VRAM allocated (tested with 96GB allocation)
- **ROCm versions:** Affects 6.4.1 through 7.0 RC
- **Symptom:** ROCm applications can only allocate ~15.5GB despite larger VRAM allocation

### Reproduction
On any affected system with kernel ≤6.15:
```bash
# Check kernel sees full VRAM (example: 96GB)
$ cat /sys/class/drm/card*/device/mem_info_vram_total
103079215104  # 96GB in bytes

# But ROCm only sees 15.5GB
$ rocminfo | grep -A3 "Pool" | grep Size
Size:    16651264(0x3e2000) KB  # Only 15.5GB!

# HIP applications fail to allocate beyond 15.5GB
$ hipMemGetInfo  # Returns ~15.5GB total
```

### Solution
**Upgrade to kernel 6.16.9 or later.** This is a kernel-level fix, not a ROCm issue.

```bash
# Ubuntu/Debian users can use mainline kernel:
sudo add-apt-repository ppa:cappelikan/ppa
sudo apt update && sudo apt install mainline
sudo mainline --install 6.16.9
sudo update-initramfs -c -k 6.16.9-061609-generic
sudo reboot

# Fedora users:
# Install kernel 6.16.9 from rawhide or testing repos
```

### Verification After Fix
```bash
# After kernel 6.16.9:
$ uname -r
6.16.9-061609-generic

# NO kernel parameters needed!
$ cat /proc/cmdline
root=UUID=72998fb2-b0eb-4676-97c9-31ac53b5e2a5 ro quiet splash rd.luks.options=tpm2-device=auto
# Note: No amdgpu.gttsize, no ttm.pages_limit, no amd_iommu=off

$ rocminfo | grep "Size:" | grep "100663296"
      Size:                    100663296(0x6000000) KB   # 96GB visible!

# Ollama now uses full memory
$ OLLAMA_GPU_MEMORY=96GB ollama run llama3.3:70b  # Works!
```

### Technical Details
The kernel 6.16.x series appears to include fixes for:
- Unified memory architecture (UMA) handling for APUs  
- HSA memory pool detection on gfx1151
- Proper VRAM aperture mapping for Strix Halo

### Testing Configuration
- **System:** HP ZBook Ultra G1a with Ryzen AI MAX+ PRO 395
- **VRAM allocation:** 96GB (not yet tested with other allocations)
- **ROCm version:** 6.4.1 (ROCm 7.0 not yet tested)
- **Kernel tested:** 6.16.9-061609-generic on Ubuntu 24.04.1 LTS

### Expected Impact
This fix enables:
- Running 70B+ parameter models that require >15GB VRAM
- Full utilization of Strix Halo's unified memory architecture
- No performance penalties from GTT workarounds
- Native ROCm performance without hacks

### Related Discussions
- Performance issues (separate): #4748
- Community workarounds: https://strixhalo-homelab.d7.wtf/
- Framework forum: https://community.frame.work/t/amd-strix-halo-ryzen-ai-max-395-gpu-llm-performance-tests/72521

### Notes
- Kernel 6.15.x and earlier: Issue persists
- Kernel 6.16.9+: Issue resolved
- ROCm 6.4.1 works perfectly with the new kernel (7.0 not required)
- No GTT expansion parameters needed

### Community Testing Needed
Please test and report back with:
- Different VRAM allocations (32GB, 64GB, 128GB)
- Different Strix Halo systems (Framework, GMKtec, ASUS, etc.)
- ROCm 7.0 compatibility
- Other distributions (Fedora, Arch, etc.)

This fix should theoretically work for all configurations, but more testing will help confirm.

---
*System verified working: HP ZBook Ultra G1a, 128GB RAM (96GB VRAM), Ubuntu 24.04.1, ROCm 6.4.1*

---

## 评论 (8 条)

### 评论 #1 — mixer3d (2025-10-04T11:29:19Z)

It also works on `Debian 13 trixie` with kernel `6.16.3` from _backports_, tested on `Framework Max+ 395 - 128GB` (with 96GB allocation):

**6.12.48+deb13-amd64** `default`

```
$  cat /sys/class/drm/card*/device/mem_info_vram_total
103079215104
```

```
$  rocminfo | grep -A3 "Pool" | grep Size
      Size:                    32646368(0x1f224e0) KB             
      Size:                    32646368(0x1f224e0) KB             
      Size:                    32646368(0x1f224e0) KB             
      Size:                    16323184(0xf91270) KB              
      Size:                    16323184(0xf91270) KB              
      Size:                    64(0x40) KB  
```

**6.16.3+deb13-amd64** `backports`
```
$ cat /sys/class/drm/card*/device/mem_info_vram_total
103079215104
```
```
$ rocminfo | grep -A3 "Pool" | grep Size
      Size:                    32644240(0x1f21c90) KB             
      Size:                    32644240(0x1f21c90) KB             
      Size:                    32644240(0x1f21c90) KB             
      Size:                    100663296(0x6000000) KB            
      Size:                    100663296(0x6000000) KB            
      Size:                    64(0x40) KB
```

---

### 评论 #2 — harkgill-amd (2025-10-07T20:40:20Z)

Hi @saross and @mixer3d, thanks for sharing your experiments and findings! It was indeed a kernel-level fix from the changes below.

https://git.kernel.org/torvalds/c/8b0d068e7dd17
https://git.kernel.org/torvalds/c/759e764f7d587

These changes were first introduced in 6.15-rc1 but have also been backported into the 6.14 OEM kernel recommended for the ROCm on Ryzen preview release https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#prepare-the-system.

---

### 评论 #3 — harkgill-amd (2025-10-07T20:50:39Z)

Will close this out but if anyone does encounter issues with reported VRAM/GTT, feel free to leave a comment and I'll reopen this issue.

---

### 评论 #4 — ulope (2025-10-08T09:44:47Z)

@saross How did you manage to get amdgpu module working with the 6.16 kernel? The amdgpu dkms package refuses to build on anything else but the official 6.14 kernel for me.

---

### 评论 #5 — harkgill-amd (2025-10-08T14:26:55Z)

@ulope, with ROCm on Ryzen, it's recommended users run with the inbox drivers rather than with `amdgpu-dkms`.  While the 6.14 OEM kernel is technically supported, the 6.16 kernel's inbox amdgpu driver should also have the aforementioned fixes as well.

---

### 评论 #6 — MartinKuhne (2026-03-18T22:47:11Z)

I have this issue on a Corsair machine (128gb) with Fedora 43

```bash
mkuhne@localhost:~$ uname -r
6.19.8-200.fc43.x86_64
mkuhne@localhost:~$ amd-smi version
AMDSMI Tool: 26.2.1+fc0010cf6a | AMDSMI Library version: 26.2.1 | ROCm version: 7.2.0 | amdgpu version: Linuxversion6.19.8-200.fc43.x86_64(mockbuild@18ffb6c38e5a42008437d0b88e2dfd4e)(gcc(GCC)15.2.120260123(RedHat15.2.1-7),GNUldversion2.45.1-4.fc43)#1SMPPREEMPT_DYNAMICFriMar1322:06:06UTC2026 | hsmp version: N/A
mkuhne@localhost:~$ amd-ttm
💻 Current TTM pages limit: 4058844 pages (15.48 GB)
💻 Total system memory: 30.97 GB
```

---

### 评论 #7 — hephaex (2026-04-27T05:14:40Z)

## hipMemGetInfo still reports wrong `total` on kernel 6.18 — HIP runtime issue persists

@harkgill-amd The kernel-level fix (6.15-rc1 backport) resolved `rocminfo` pool reporting, but `hipMemGetInfo()` **still returns the wrong `total` value** on newer kernels. This appears to be a separate HIP runtime bug.

### Environment

| Component | Value |
|-----------|-------|
| CPU/APU | AMD Ryzen AI MAX+ 395 (Strix Halo), gfx1151 |
| System RAM | 128 GB LPDDR5x (96 GB UMA to GPU) |
| OS | Debian 13 (trixie) |
| Kernel | 6.18.12+deb13-amd64 |
| ROCm | 7.13.0 |
| amdgpu params | `gttsize=98304 iommu=pt` |

### Kernel sysfs — CORRECT (96 GiB)

```
/sys/class/drm/card0/device/mem_info_vram_total:     103079215104   (96 GiB)
/sys/class/drm/card0/device/mem_info_gtt_total:      103079215104   (96 GiB)
/sys/class/drm/card0/device/mem_info_vis_vram_total:  103079215104   (96 GiB)
```

### rocminfo pool — CORRECT (96 GiB)

```
Pool 1
  Segment: GLOBAL; FLAGS: COARSE GRAINED
  Size: 100663296(0x6000000) KB   (= 96 GiB)
```

### hipMemGetInfo — WRONG

```c
hipMemGetInfo(&free, &total);
// free  = 102907248640 bytes = 95.84 GiB   ← correct (GTT/unified)
// total = 16636528640  bytes = 15.49 GiB   ← WRONG (VRAM aperture only)
```

`hipDeviceGetAttribute(hipDeviceAttributeTotalGlobalMem)` returns the same incorrect 15.49 GiB.

### What this breaks

`free > total` is semantically impossible, so frameworks that sanity-check this (or compute `used = total - free`) get confused. More importantly:

- **vLLM** calculates KV-cache budget from `hipMemGetInfo` total → thinks only 15.49 GiB available → OOM on models that should fit.
- **PyTorch** `torch.cuda.mem_get_info()` wraps `hipMemGetInfo` → same wrong total.
- `hipMalloc` itself works fine for allocations >15.49 GiB (it goes through GTT), so the allocator is correct — only the reporting API is wrong.

### Root cause hypothesis

The kernel patches ([8b0d068e7dd17](https://git.kernel.org/torvalds/c/8b0d068e7dd17), [759e764f7d587](https://git.kernel.org/torvalds/c/759e764f7d587)) fixed HSA memory pool enumeration, which is why `rocminfo` now shows the correct 96 GiB. However, `hipMemGetInfo` in the HIP runtime appears to query `total` via a different code path — likely reading the VRAM aperture size from KFD rather than the actual usable memory pool size. On discrete GPUs these are the same value; on APUs with unified memory they diverge.

### Confirmation this is not kernel-only

@MartinKuhne's comment above confirms the same issue on Fedora 43 with kernel **6.19.8** and ROCm 7.2.0 — TTM pages limit still shows 15.48 GB. This is consistent with a HIP/KFD runtime bug that the kernel patches did not address.

### Workaround

Read total from sysfs instead of `hipMemGetInfo`:
```bash
cat /sys/class/drm/card0/device/mem_info_gtt_total
# 103079215104
```

For vLLM specifically, patching `_get_device_memory` to read sysfs total works.

### Request

Could this issue be **reopened**? The kernel fix was necessary but not sufficient — there is a remaining bug in the HIP runtime's `hipMemGetInfo` / `hipDeviceGetAttribute(hipDeviceAttributeTotalGlobalMem)` that still reports only the VRAM aperture size (~15.5 GiB) instead of the actual usable unified memory on Strix Halo APUs.

cc @mixer3d @MartinKuhne

---

### 评论 #8 — hephaex (2026-04-27T06:56:17Z)

## Update: Full LD_PRELOAD workaround verified — vLLM serving 27B model on Strix Halo

Building on the earlier workaround, I've developed a complete solution and filed a dedicated HIP runtime bug at ROCm/hip#3892.

### What works now

With the LD_PRELOAD C shim (intercepts 5 HIP APIs) + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`:

- `torch.cuda.get_device_properties(0).total_memory` reports **88.0 GiB** (was 15.49)
- `torch.zeros(50 GiB, device="cuda:0")` **succeeds**
- **vLLM serves Qwen3.6-27B** (51.75 GiB bf16) at ~4.4 tok/s with `--num-gpu-blocks-override 512`

### Key discoveries since last comment

1. **`hipGetDevicePropertiesR0600` uses offset 288** — PyTorch ROCm 7.x calls the R0600 variant where `totalGlobalMem` is at byte offset 288 (not 256). Patching only `hipGetDeviceProperties` at offset 256 doesn't fix PyTorch's `device_properties.total_memory`.

2. **`expandable_segments:True` is mandatory** — Without this PyTorch flag, GTT-backed allocations fail even after the shim reports 88 GiB. The caching allocator needs segment-based expansion for non-contiguous GTT pages.

3. **`mem_info_gtt_used` does NOT track `hipMalloc`** — After loading 51.75 GiB of model weights, sysfs `gtt_used` remains near 0. This makes memory profiling impossible for ML frameworks (vLLM's `--gpu-memory-utilization` is broken on APU).

### Docker one-liner

```bash
docker run -d --name vllm --device /dev/kfd --device /dev/dri \
  --group-add video --group-add render --network host --shm-size 16g \
  -v /path/to/models:/root/.cache/huggingface \
  -v /path/to/hip_mem_override.c:/tmp/src.c:ro \
  -e PYTORCH_ROCM_ARCH=gfx1151 \
  -e HSA_OVERRIDE_GFX_VERSION=11.5.1 \
  -e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  -e TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 \
  -e HIP_FORCE_DEV_KERNARG=1 \
  -e HSA_NO_SCRATCH_RECLAIM=1 \
  kyuz0/vllm-therock-gfx1151:stable bash -c \
  "gcc -shared -fPIC -o /tmp/override.so /tmp/src.c -ldl && \
   LD_PRELOAD=/tmp/override.so python3 -m vllm.entrypoints.openai.api_server \
   --model Qwen/Qwen3.6-27B --enforce-eager --max-model-len 4096 \
   --num-gpu-blocks-override 512 --port 8000 --trust-remote-code"
```

### Cross-references
- HIP runtime bug: ROCm/hip#3892
- PyTorch issue update: pytorch/pytorch#107605
- vLLM APU PR: vllm-project/vllm#40963

---
