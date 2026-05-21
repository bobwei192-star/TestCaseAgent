# gfx1151 (Strix Halo / Bosgame M5 / Sixunited AXB35-02) — HSA `Memory critical error by agent node-0 ... Reason: Memory in use` on first GGUF model upload, persists on kernel 7.0.1 (KFD ABI 1.22) across all software combinations

> **Issue #6182**
> **状态**: open
> **创建时间**: 2026-04-25T04:56:42Z
> **更新时间**: 2026-05-11T21:20:05Z
> **作者**: dkzv
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6182

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述


## TL;DR

On a Bosgame M5 (Sixunited AXB35-02 board, AMI BIOS 1.07 / 2025-09-12), every PyTorch/HIP workload that loads a sizeable model into `cuda:0` reproduces a non-recoverable HSA fault:

```
Memory critical error by agent node-0 (Agent handle: 0x...) on address 0x7f.... Reason: Memory in use.
```

The crash fires at `hsaKmtFreeMemory` of a 4 KB host-mapped page allocated on node 1 during HSA queue/scratch setup. **Software is fully exhausted**: 4 kernels (incl. mainline 7.0.1 with KFD ABI 1.22), 4 ROCm versions (incl. stable 7.2.2), 5 HSA env-var levers, 8 kernel cmdline variants, two firmware revisions, two BIOS UMA settings, two containers (incl. AMD official `rocm/pytorch:rocm7.2.2`). A simple `hipMalloc/hipMemset/hipDeviceSynchronize/hipFree` cycle works; only the model-load pattern fails. ~~llama.cpp + ROCm runs end-to-end on the same GPU with identical kernel/firmware.~~ *(Edit 2026-04-27: corrected — my llama.cpp here is Vulkan RADV, not ROCm; see What works section.)* Filing because the matrix is now tight enough to be diagnostic.

## Hardware

| | |
|---|---|
| Mini-PC | Bosgame M5 (BeyondMax Series) |
| Mainboard | Sixunited AXB35-02 |
| SoC | AMD Ryzen AI MAX+ 395 w/ Radeon 8060S (Strix Halo) |
| GPU target | `gfx1151`, 40 CUs, wavefront 32 |
| RAM | 128 GB unified |
| BIOS | AMI 1.07 / 2025-09-12 (Bosgame has shipped no updates since launch) |
| BIOS UMA "Dedicated Graphics Memory" | 0.5 GB (also tested 64 GB — same crash) |
| Secure Boot | disabled |

The same physical board (AXB35-02) is rebadged by GMKtec as the EVO-X2, which has BIOS v1.12 (2025-12-09) — community-confirmed safe for cross-flash on Bosgame M5 ([strixhalo.wiki AXB35 firmware page](https://strixhalo.wiki/Hardware/Boards/Sixunited_AXB35/Firmware)). I have not cross-flashed (yet); leaving that as a separate hardware-side variable.

## Software stack

| | |
|---|---|
| OS | Fedora 43 Workstation |
| Kernel | `7.0.1-262.vanilla.fc43.x86_64` (`@kernel-vanilla/stable` Copr) |
| KFD ABI | MAJOR=1, MINOR=22 (`/usr/src/kernels/.../include/uapi/linux/kfd_ioctl.h`) |
| Mainline kernel fixes confirmed in tree | b42f3bf9 VGPR save-restore, 71776e0965f9 CWSR export, 7a5fb05b ABI 1.20→1.22 |
| firmware | `linux-firmware-20260110-1.fc43` (also tested 20260309) |
| Kernel cmdline | `rhgb quiet iommu=pt ttm.pages_limit=32505856` (also tried with `amd_iommu=off`, `amdgpu.cwsr_enable=0`, `amdgpu.sched_policy=2`, `amdgpu.vm_fragment_size=9`, `amdgpu.gttsize=126976`, `amdttm.*`, `ttm.page_pool_size`) |

**ROCm userspace stacks tested (all crash identically):**
- AMD official `docker.io/rocm/pytorch:rocm7.2.2_ubuntu24.04_py3.12_pytorch_release_2.10.0` (2026-04-15) — torch 2.10.0+rocm7.2.2.git40d237bf, hip 7.2.53211
- TheRock nightly `kyuz0/amd-strix-halo-comfyui:latest` — torch 2.11.0a0+rocm7.12.0a20260211, hip 7.3.53390
- TheRock pinned `7.11.0a20260106`
- Direct `repo.radeon.com` torch wheel `2.10.0+rocm7.2.0.lw.gitb6ee5fde`

## Symptom

```
:0:rocdevice.cpp:... Memory critical error by agent node-0 (Agent handle: 0x...) on address 0x7f.... Reason: Memory in use.
```

Reproduces in any process that loads a transformer-style text encoder or large UNet onto `cuda:0`. Consistent across:
- **WAN 2.2 ti2v 5B fp16 (Q5_K_M GGUF)** at 512×384×17 frames — fires at `Requested to load WanTEModel` (the umt5-xxl text encoder)
- WAN 2.2 i2v 14B fp8+fp16
- SeedVR2 video upscaler (any size)
- Flux 2 dev (fp8 mixed + bf16 Mistral)
- Plain `torch.zeros(N, dtype=torch.float32, device='cuda:0')` for any N **once the process has done some prior `cuda` work, in some cases** — but see "Negative" below

Non-recoverable: HSA runtime can't free more memory after, process effectively dead.

## What works

- **`hipMalloc(64 MB) + hipMemset + hipDeviceSynchronize + hipFree`** on kernel 7.0.1 (KFD ABI 1.22) — passes cleanly. Source:
  ```c
  #include <hip/hip_runtime.h>
  #include <cstdio>
  int main() {
    void *p; hipError_t e;
    e = hipMalloc(&p, 64*1024*1024); printf("hipMalloc: %s\n", hipGetErrorString(e));
    e = hipMemset(p, 0, 64*1024*1024); printf("hipMemset: %s\n", hipGetErrorString(e));
    e = hipDeviceSynchronize(); printf("sync: %s\n", hipGetErrorString(e));
    hipFree(p); printf("OK\n"); return 0;
  }
  // hipcc t.cpp -o t --offload-arch=gfx1151 && ./t  →  OK
  ```
  This same reproducer crashed identically on kernel 6.18.5 (KFD ABI 1.18). The kernel-side ABI bump fixed the simple allocator path.

- **Synthetic torch alloc loops** in a fresh process — pass:
  ```python
  for size in [64*1024*1024, 256*1024*1024, 1024*1024*1024, 5*1024*1024*1024]:
      t = torch.zeros(size//4, dtype=torch.float32, device="cuda:0")
      torch.cuda.synchronize()
      del t; torch.cuda.empty_cache()
  ```
  Also: 200 iterations of `4096×4096 fp16` matmul + free + empty_cache in 1.6s, no crash.

- **llama.cpp + Vulkan RADV** — runs Qwen3.6-35B-A3B-UD-Q4_K_XL end-to-end on this same GPU, no crashes. Vulkan path only, no HIP exercised. *(Edit 2026-04-27: original report incorrectly said "llama.cpp + ROCm" — build here is `GGML_HIP=OFF / GGML_VULKAN=ON`. I have not verified a HIP-built llama.cpp on this hardware. The implication "distinct HIP allocator path from torch's" therefore does not follow from this data point.)*

- **sd.cpp Vulkan** — runs Flux 2 / WAN 2.2 GGUF end-to-end. Confirms hardware + power + VRAM partitioning are healthy.

## Failing trace (`AMD_LOG_LEVEL=4 AMD_LOG_MASK=0x60000 HSAKMT_DEBUG_LEVEL=7`)

Full trace at `comfyui_extended_trace.log` (192 lines, kernel 7.0.1 + ROCm 7.12 nightly), attached. Failing sequence at `Requested to load WanTEModel`:

```
[hsaKmtAllocMemoryAlignCtx] node 1 address 0x7f0417800000 size 2101346304 from device
[hsaKmtMapMemoryToGPUNodesCtx] address 0x7f0417800000 number of nodes 1
[hsaKmtAllocMemoryAlignCtx] node 1 address 0x7f091de3f000 size 4096 from host    ← 4 KB scratch on node 1, host-mapped
[hsaKmtMapMemoryToGPUNodesCtx] address 0x7f091de3f000 number of nodes 1
[hsaKmtAllocMemoryAlignCtx] node 0 address 0x7f07ae407000 size 4096 from host
[hsaKmtMapMemoryToGPUNodesCtx] address 0x7f07ae407000
[hsaKmtMapMemoryToGPUNodesCtx] address 0x7f07adc0d000
"Allocating VRAM for EOP"
[hsaKmtMapMemoryToGPUNodesCtx] address 0x7f073b23d000
"Allocating GTT for CWSR"
hsaKmtSVMSetAttrCtx: address 0x7f0678600000 size 0x1256000
[hsaKmtUnmapMemoryToGPUCtx] address 0x7f091de3f000   ← ioctl returns success
[hsaKmtFreeMemoryCtx] address 0x7f091de3f000          ← ioctl returns success
Memory critical error by agent node-0 (Agent handle: 0x560304d08f00) on address 0x7f091de3f000. Reason: Memory in use.
```

**Object identity**: the failing 4 KB page on node 1 is allocated `from host` early in HSA queue setup. Best matching candidate from rocr-runtime sources: `AqlQueue::pm4_ib_buf_` (4 KB, AllocateExecutable via `system_allocator()`) — but `HSA_ALLOCATE_QUEUE_DEV_MEM=1` did not change behavior, so it's either not pm4_ib_buf_ or that env var is not honored in either of the userspace builds tested. CWSR is documented as a related setup region but **disabling CWSR at the kernel level (`amdgpu.cwsr_enable=0`) does not fix the crash**, so the CWSR teardown is correlation, not causation.

## What's been ruled out (so we don't have to round-trip)

**Kernels** (all crash):
- 6.18.3-200.fc43 (last known-good per pytorch#173367)
- 6.18.5-200.fc43 (ChristianKniep's working baseline on his Framework)
- 6.19.12-200.fc43
- **7.0.1-262.vanilla.fc43 (KFD ABI 1.22)** — the libhsakmt warning `gfx1151 requires KFD ABI ≥ 1.20` is silenced; same crash

**Kernel cmdline** (none change behavior):
- `amdgpu.cwsr_enable=0`
- `amdgpu.sched_policy=2` (no MES HWS)
- `amdgpu.vm_fragment_size=9`
- `amdgpu.gttsize=126976`
- `amdttm.pages_limit=32768000` + `amdttm.page_pool_size=32768000` + `ttm.page_pool_size=32768000`
- `amd_iommu=off` (and conversely `iommu=pt` alone)

**HSA env vars** (none change behavior; tested via `kyuz0/amd-strix-halo-comfyui` on kernel 7.0.1 — `AMD_LOG_LEVEL=4` IS honored so at least some env vars reach the runtime):
- `HSA_ALLOCATE_QUEUE_DEV_MEM=1`
- `HSA_DISABLE_FRAGMENT_ALLOCATOR=1`
- `HSA_ENABLE_INTERRUPT=0`
- `HSA_ENABLE_SCRATCH_ASYNC_RECLAIM=0` + `HSA_NO_SCRATCH_RECLAIM=1`
- `HSA_MAX_QUEUES=1`
- `HSA_USE_SVM=0` + `HSA_ENABLE_SDMA=0`
- `HSA_OVERRIDE_GFX_VERSION=11.5.1` (and unset)
- `HSA_XNACK=1`
- `PYTORCH_HIP_ALLOC_CONF=backend:native,expandable_segments:True,garbage_collection_threshold:0.9,max_split_size_mb:512`

**Container privilege** (no change):
- rootless podman with `--device=/dev/kfd --device=/dev/dri --group-add 39 --group-add 105`
- `--security-opt seccomp=unconfined --security-opt label=disable`
- **`--privileged`** (falsifies the sdnext#4652 IOMMU/DMABUF hypothesis)

**Firmware**: 20260110 vs 20260309 — same crash on both.
**BIOS UMA**: 0.5 GB vs 64 GB — same crash on both.

## Negative / non-trigger

- The crash does **not** show "Memory access fault by GPU agent on address X / Page not present" — that's the #6118/#6146 class which the kernel-side fixes addressed. We are not in that class.
- `dmesg` is **clean** during the crash — no GPU VM faults, no ring resets, no KFD errors. Failure is entirely userspace-visible from the HSA runtime.
- Synthetic `torch.zeros(...)` and the 15-line `hipMalloc/Free` pure C reproducer pass on kernel 7.0.1. The crash is gated on the specific HSA queue/scratch setup pattern that PyTorch + ComfyUI's `model_management.load_models_gpu()` triggers when uploading a transformer text encoder or UNet.
- This is the same hardware that ChristianKniep ran WAN 2.2 T2V-A14B on successfully on 2026-01-16 with kernel 6.18.5 — BUT his hardware was a different OEM (Framework). Filing supports a board/BIOS-class delta hypothesis.

## Closely related but distinct tickets (please correlate, not duplicate)

| Ticket | Status | Why it's not this |
|---|---|---|
| ROCm/ROCm#6118 (`hsa_queue_create causes GPU page fault on gfx1151`) | closed | Different signature ("Page not present"), fixed by kernel `cwsr_size`/`ctl_stack_size` export which IS in this kernel |
| ROCm/ROCm#6146 (`Page Fault on hipMemcpy() in ROCm 7.2.1`) | closed 2026-04-16 | Same fix as #6118, doesn't cover this signature |
| ROCm/ROCm#5824 (`gfx1151 segfault`) | closed 2026-01-23 | Closed for inactivity; original reporter still saw issues post-FW upgrade |
| ROCm/TheRock#2991 (canonical gfx1151 VGPR fix summary) | closed 2026-02-23 | Userspace `hsakmt: Expose and use CWSR and Control stack sizes` shipped in TheRock Dec 19 2025+; we've tested that build; it fixes simple alloc but not this signature |
| sdnext#4652 (`Memory critical error by agent` on Bazzite Strix Halo) | open | Reporter fixed via `--privileged`; we tested `--privileged`, no effect — IOMMU/DMABUF hypothesis falsified for this hardware |
| pytorch/pytorch#173367 (`Strix Halo HSA crashes 6.18.4+`) | open since 2026-01-26 | Profile matches but the kernel-version differentiator they describe (6.18.3 vs 6.18.4) does not apply here — both crash |
| ROCm/rocm-systems#2200 (`hsakmt: Expose and use CWSR and Control stack sizes`) | merged | The userspace part of the fix that #2991 tracks; in the wheels we've tested |

## Questions / requests for triage

1. Is the failing 4 KB host-mapped node-1 page identifiable from the trace alone — pm4_ib_buf_ or something else? Does AMD have a known list of HSA queue setup objects that allocate `from host` on node 1 in this size?
2. Is `node-0` the CPU agent, or a separate GPU partition node? The error reports node-0 owns the in-use mapping while the alloc/unmap/free were on node 1.
3. Has any AMD engineer correlated bugs against AMI BIOS 1.07 / Bosgame M5 / Sixunited AXB35-02 specifically? GMKtec EVO-X2 (same physical board, BIOS 1.12) reports are absent from this signature in our search; if AMD has internal data showing this is BIOS-version-gated, that would close the case.
4. Is there a flag combination — kernel cmdline, HSA env, SMU/IOMMU policy — that we have NOT tried that's known to bypass the HSA queue setup pattern shown in the trace? Particularly anything that would change whether a 4 KB allocation lands `from host` vs `from device` on node 1.
5. Should we cross-flash GMK 1.12 BIOS as the recommended diagnostic, or RMA?

## Artifacts

All bundled in this gist: **https://gist.github.com/dkzv/bcc864bc91e1f35e3879ba06707f5bb0**

Files in the gist:
- `comfyui_extended_trace.log` — full extended HSA/KFD trace at the failing model load (~200 lines, captured with `AMD_LOG_LEVEL=4 AMD_LOG_MASK=0x60000 HSAKMT_DEBUG_LEVEL=7 HSA_XNACK=1`)
- `repro_hip.cpp` — 15-line C reproducer (passes on 7.0.1, crashed on 6.18.5)
- `repro_smoke.py` — synthetic torch alloc smoke (passes)
- `repro_matmul.py` — 200-iter matmul + free loop (passes)
- `comfyui_smoke_api.json` — exact `/prompt` POST body used (WAN 2.2 ti2v 5B Q5_K_M, 512×384×17, 20 steps, euler/simple)
- `rocminfo.txt`, `rocm-smi.txt`, `cmdline.txt`, `dmi.txt`, `kernel.txt`, `rpms.txt` — environment snapshots
- `test_hsa_levers.sh` — driver script used to test the 5 HSA env-var levers in sequence

`dmesg` is clean of GPU driver errors during the crash (no VM faults, ring resets, KFD errors); omitted to avoid attaching unrelated USB/Bluetooth host metadata. Available on request to triage.

Cross-link: pytorch/pytorch#173367, ROCm/TheRock#2991 closure, vladmandic/sdnext#4652, invoke-ai/InvokeAI#9053.



---

## 评论 (8 条)

### 评论 #1 — valeriy-idatica (2026-04-27T08:34:26Z)

Hi @dkzv! I'm on a similar setup (Minisforum ai-server, Ryzen AI MAX+ 395, 128GB RAM). I noticed you mentioned that llama.cpp runs end-to-end for you on ROCm without crashes, while I'm getting constant [gfxhub] page fault (PERMISSION_FAULTS: 0x3) even with -dio and iommu=pt.

Could you please share:

- Which specific ROCm version/libraries are you using?
- What is your llama.cpp build (version/commit)?
- Your exact kernel version (uname -a) and any specific amdgpu module parameters?
- Are you using a specific Docker image or running bare-metal?
- Your working configuration would be a lifesaver for the community. Thanks!

---

### 评论 #2 — dkzv (2026-04-27T15:27:05Z)

That line in the issue body is wrong, my working llama.cpp is Vulkan RADV, not ROCm (editing the body now). So I can't speak to the HIP path, but here's the Vulkan setup that works end-to-end if it's useful as a fallback:

- llama.cpp commit `23b8cc499` ("version: 8838"), bare-metal cmake: `-DGGML_VULKAN=ON -DGGML_HIP=OFF -DGGML_NATIVE=ON -DCMAKE_BUILD_TYPE=Release`
- Runtime: `AMD_VULKAN_ICD=RADV`
- Flags: `-ngl 999 -fa on --no-mmap --no-context-shift --ctx-size 262144 --cache-type-k q8_0 --cache-type-v q8_0 --batch-size 2048 --ubatch-size 512`
- Model: `Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf` (~22 GB)
- Mesa `25.3.6-3.fc43`, vulkan-loader `1.4.341.0`
- Kernel `7.0.1-262.vanilla.fc43.x86_64`, cmdline: `iommu=pt ttm.pages_limit=32505856 amdgpu.cwsr_enable=0 amdgpu.sched_policy=2`
- Bare-metal user systemd unit, no container

Your `[gfxhub] PERMISSION_FAULTS:0x3` is a different fault class than the HSA "Memory in use" here.


---

### 评论 #3 — valeriy-idatica (2026-04-28T09:17:12Z)

Thanks for the clarification, @dkzv! That explains the PERMISSION_FAULTS I was seeing with the HIP path. Since ROCm is still a bit of a moving target on Strix Halo, your Vulkan (RADV) success is a great roadmap.

I'm currently on Ubuntu 24.04 with Kernel 6.8, so seeing your Fedora/Kernel 7.0 and Mesa 25.3 setup is very helpful for context. I'll try replicating your GRUB parameters (especially ttm.pages_limit) and Vulkan flags to see how far I can push my setup. Cheers!

---

### 评论 #4 — harkgill-amd (2026-05-01T13:50:26Z)

Hey @dkzv, thanks for the comprehensive report. I'd like to capture a couple different baselines so we can narrow down exactly what's failing here.

First and foremost, you mentioned workloads that loads a sizeable model into cuda:0 trigger the `Memory critical error`. Do you have a minimal reproducer that can consistently hit this? Does moving a single layer onto the GPU with something like `m = torch.nn.Linear(4096, 4096).cuda()` reproduce this or does the model have to be magnitudes larger in size? A strace log here would also be helpful to get a better idea of what went wrong right before the error's thrown, 

`strace -e ioctl -f -o trace.log <reproducer command>`

It might be a bit long but you should be able to drop it into your comment as an attachment. The last thing that'd help is a clean baseline on Ubuntu with ROCm 7.2.1 and the OEM kernel if possible - install instructions for both of these can be found [here](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#prepare-the-system).

---

### 评论 #5 — dkzv (2026-05-01T15:27:56Z)

@harkgill-amd  — results:

### 1. Minimal reproducer (Linear bisection)

`torch.nn.Linear(4096, 4096).cuda()` with and without `forward()` passes cleanly. Stayed clean scaling to width 16384 and depth 4× Linear(8192). What I found is more interesting than a clean threshold:

- **TE-equiv ~2.56 GB (emb 50k×4096 + 8× MLP blocks), no warmup → flaky hang at `.cuda()`.**
- **Same model + a 1 MB `torch.zeros` warmup before the move → 0.31s pass.**

Hang is race-shaped: at ~2.02 GB I got **1/10 hangs** over 10 fresh-subprocess runs. dmesg clean across both passing and hanging runs. Symptom is a silent hang (no HSA error message, just SIGTERM by timeout) — different surface from the `Memory in use` print but same "no kernel fault, userspace-only" class.

`repro_linear.py` + grid + flaky-d6 in the gist.

### 2. strace ioctl on the ComfyUI WAN ti2v 5B path

Reproduced the original signature at `Requested to load WanTEModel`:

```
Memory critical error by agent node-0 (Agent handle: 0x56097224d8a0)
on address 0x7fb8bb018000. Reason: Memory in use.
```

The KFD-relevant flow on the loader thread (TID 3015117) is just **24 ioctl lines**, full sequence:

```
ioctl(4, AMDKFD_IOC_AVAILABLE_MEMORY)           = 0    (×4)
ioctl(4, AMDKFD_IOC_ALLOC_MEMORY_OF_GPU)        = 0    alloc 1
ioctl(4, AMDKFD_IOC_MAP_MEMORY_TO_GPU)          = 0    map   1
ioctl(4, AMDKFD_IOC_ALLOC_MEMORY_OF_GPU)        = 0    alloc 2
ioctl(4, AMDKFD_IOC_MAP_MEMORY_TO_GPU)          = 0    map   2
ioctl(4, AMDKFD_IOC_ALLOC_MEMORY_OF_GPU)        = 0    alloc 3
ioctl(4, AMDKFD_IOC_MAP_MEMORY_TO_GPU)          = 0    map   3
ioctl(4, AMDKFD_IOC_CREATE_EVENT)               = 0
ioctl(4, AMDKFD_IOC_ALLOC_MEMORY_OF_GPU)        = 0    alloc 4
ioctl(4, AMDKFD_IOC_MAP_MEMORY_TO_GPU)          = 0    map   4
ioctl(4, AMDKFD_IOC_ALLOC_MEMORY_OF_GPU)        = 0    alloc 5
ioctl(4, AMDKFD_IOC_MAP_MEMORY_TO_GPU)          = 0    map   5
ioctl(4, _IOC(R|W, 0x4b, 0x20, 0x48))           = 0    AMDKFD_IOC_SVM (set attrs, 72B args)
ioctl(4, AMDKFD_IOC_CREATE_QUEUE)               = 0
ioctl(4, AMDKFD_IOC_ALLOC_MEMORY_OF_GPU)        = 0    alloc 6 (no map -- queue ring/scratch?)
ioctl(4, AMDKFD_IOC_FREE_MEMORY_OF_GPU)         = 0    (frees the SVM-args region)
ioctl(4, AMDKFD_IOC_SET_EVENT)                  = 0
ioctl(4, AMDKFD_IOC_DESTROY_EVENT)              = 0
ioctl(4, AMDKFD_IOC_UNMAP_MEMORY_FROM_GPU)      = -1 EBUSY    <<< FAILS
ioctl(4, AMDKFD_IOC_FREE_MEMORY_OF_GPU)         = -1 EBUSY    <<< FAILS
--- SIGABRT ---
```

So the kernel-side origin of the userspace `Memory in use` text is **`AMDKFD_IOC_UNMAP_MEMORY_FROM_GPU` returning `-EBUSY`** immediately after a `CREATE_QUEUE`, then `FREE_MEMORY_OF_GPU` also `-EBUSY`. Suggestive shape: alloc-6 has no MAP (queue ring/scratch?) and the SVM op right before CREATE_QUEUE may set an attribute that creates the refcount the later UNMAP trips on.

### Artifacts

Updated gist: https://gist.github.com/dkzv/bcc864bc91e1f35e3879ba06707f5bb0

New files include `strace_comfy_window.log` (annotated 24-line crash window — start here), `strace_comfy.part00–03.txt` (full 35 MB strace split for the 10 MB/file gist limit; part00 has the actionable KFD flow), `repro_linear.py` + bisection logs, and the synthetic-hang HSAKMT/strace traces. README in `strace_comfy.README.txt`.


---

### 评论 #6 — cdanis (2026-05-04T23:58:10Z)

Watching for Strix Halo Coherent Host Access fixes.

---

### 评论 #7 — dkzv (2026-05-10T11:26:44Z)

@harkgill-amd — Ubuntu baseline done. Same hardware crashes on the very first GPU dispatch, with a cleaner kernel-side fault signature than the Fedora surface.

## Environment

| | |
|---|---|
| Board | Bosgame AXB35-02 (BeyondMax Series) |
| BIOS | AMI v1.07, 2025-09-12 |
| GPU | gfx1151 — AMD Radeon 8060S (Ryzen AI MAX+ 395) |
| OS | Ubuntu 24.04 LTS |
| Kernel | `6.17.0-1020-oem` |
| ROCm | 7.2.1 (`rocm-core 7.2.1.70201-81~24.04`, ROCk module 6.16.13, HIP 7.2.26015) |
| PyTorch | `2.11.0+rocm7.2` (gfx1151 in `torch.cuda.get_arch_list()`) |
| XNACK | NO (per `AMDKFD_IOC_SET_XNACK_MODE` and rocminfo) |

Installed per [the official Ryzen AI install guide](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#prepare-the-system) you linked.

## What happens

`repro_torch_alloc.py` (the 64 MB / 256 MB / 1 GB / 5 GB `torch.zeros` smoke from the original report) reaches the first `torch.zeros(64MB, device='cuda:0')`. `hipMalloc` succeeds, the runtime loads the native gfx1151 fill kernel, launches it, and the GPU immediately page-faults. The Python process then hangs in HSA error handling at 99% CPU (no syscalls, flat RSS) and never returns.

### HIP runtime (excerpt)

```
hipMalloc ( ..., 67108864 )                           → hipSuccess
__hipPushCallConfiguration ( {16384,1,1}, {256,1,1} )
hipLaunchKernel ( ..., {16384,1,1}, {256,1,1}, ... )
hip_fatbin: Using native code object for device: amdgcn-amd-amdhsa--gfx1151
:1:rocdevice.cpp:3327: Memory Fault Error
```

### Kernel (dmesg)

```
amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32773)
  Process python3 pid 16613 thread python3 pid 16613
  in page starting at address 0x00007e412d471000 from client 10
  GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
    Faulty UTCL2 client ID: CPF (0x4)
    MORE_FAULTS:        0x0
    WALKER_ERROR:       0x1
    PERMISSION_FAULTS:  0x3
    MAPPING_ERROR:      0x1
    RW:                 0x0
```

The faulting client is **CPF (Command Processor Frontend)** with `WALKER_ERROR | MAPPING_ERROR | PERMISSION_FAULTS:0x3` — the page-table walker hit an invalid mapping while CPF was fetching the dispatch packet itself. **Reproduced four times** in this session (pids 15443, 15807, 16613, and one more) with identical fault status bits.

### KFD ioctl trace (summary, from `strace -e ioctl -f`)

```
 23  AMDKFD_IOC_ALLOC_MEMORY_OF_GPU
 23  AMDKFD_IOC_MAP_MEMORY_TO_GPU
  8  AMDKFD_IOC_WAIT_EVENTS
  7  AMDKFD_IOC_CREATE_EVENT
  4  AMDKFD_IOC_SET_EVENT
  2  AMDKFD_IOC_SET_MEMORY_POLICY
  2  AMDKFD_IOC_GET_PROCESS_APERTURES_NEW
  2  AMDKFD_IOC_ACQUIRE_VM
  1  AMDKFD_IOC_SET_XNACK_MODE
  1  AMDKFD_IOC_SET_TRAP_HANDLER
  1  AMDKFD_IOC_RUNTIME_ENABLE
```

ALLOC and MAP counts are balanced. **No `EBUSY` from `UNMAP_MEMORY_FROM_GPU` like in the Fedora trace.** The trace ends mid-burst of ALLOC+MAP pairs (scratch buffers being prepared for the first dispatch); the dispatch itself goes via mmap'd doorbell writes and isn't visible to `strace -e ioctl`.

## Compared to the Fedora surface

| | Fedora 44 / kernel 6.19.14 / TheRock 7.12 | Ubuntu 24.04 / OEM 6.17 / ROCm 7.2.1 |
|---|---|---|
| Userspace symptom | HSA `Memory critical error ... Memory in use` | HIP `Memory Fault Error` + Python hang at 99% CPU |
| KFD ioctl signal | `AMDKFD_IOC_UNMAP_MEMORY_FROM_GPU → -EBUSY` after `CREATE_QUEUE` | clean ALLOC+MAP pairs until SIGTERM by timeout |
| dmesg | clean (no GPU fault logged) | **CPF page fault** with `WALKER_ERROR \| MAPPING_ERROR \| PERMISSION_FAULTS:0x3`, ×4 |
| Phase | HSA queue setup during model load | First `hipLaunchKernel` (the fill kernel for `torch.zeros(64MB)`) |

Both surfaces fail at the very-first-GPU-dispatch / queue-bringup phase, on identical hardware. The Ubuntu kernel just logs the underlying GPU page fault directly where Fedora's KFD swallows it and only the userspace HSA "Memory in use" surfaces.

## Conclusion

Switching from Fedora 44 / linux-vanilla 7.0.1 (KFD ABI 1.22) / TheRock 7.12 to Ubuntu 24.04 / linux-oem 6.17 / ROCm 7.2.1 stable **does not change the failure**. The fault occurs in `GCVM_L2_PROTECTION_FAULT_STATUS` with CPF as the faulting client on the very first GPU dispatch, regardless of OS or kernel.

This places the bug in the **hardware/firmware class** (Bosgame M5 / AXB35-02 BIOS, AMI v1.07, 2025-09-12), not the Fedora-kernel/KFD-ABI class.

The same `[gfxhub] PERMISSION_FAULTS:0x3` fault class was reported by @valeriy-idatica on a Minisforum ai-server (different vendor, also Strix Halo) — possibly the same root cause is reachable from multiple OEM BIOSes.


---

### 评论 #8 — harkgill-amd (2026-05-11T21:00:45Z)

Thanks for getting the baseline with Ubuntu, this is very helpful. Narrowing it down to the same error as https://github.com/ROCm/ROCm/issues/6186 with fail signature
```
  GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
    Faulty UTCL2 client ID: CPF (0x4)
```
is a good step forward. I haven't been able to repro this on my end yet with the same configuration as what you've reported this on (Ubuntu 24.04 + 6.17.0-1020-oem + ROCm 7.2.1) though I do see a couple reports of this exact same failure internally. Working with those teams to isolate what the exact discrepancy is between failing and passing systems - once we have better picture of this we can get started with scoping out a potential solution. Will share any updates on the investigation in this thread.

EDIT - Do you have `amdpgpu-dkms` installed by any chance? The [7.2.1 installation for Ryzen](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#set-up-rocm-usecase) avoids amdgpu-dkms entirely as it can cause conflicts. For reference, I installed it just to get an idea of what the failure would look like and ran in to the exact same hangs with `Faulty UTCL2 client ID: CPF (0x4)` in dmesg reported. See https://github.com/ROCm/ROCm/issues/6143 for a similar issue that had this root cause as well.

---
