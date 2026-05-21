# amdgpu queue eviction cascade kills display compositor with 4+ concurrent GPU processes on gfx1151 APU

> **Issue #6012**
> **状态**: closed
> **创建时间**: 2026-03-02T19:22:33Z
> **更新时间**: 2026-03-17T15:57:01Z
> **关闭时间**: 2026-03-17T15:57:01Z
> **作者**: ripley2298
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6012

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

# Bug report: amdgpu queue eviction cascade kills display compositor on gfx1151 APU

## Summary

Running 4 concurrent PyTorch/ROCm GPU inference processes on an AMD Ryzen
AI Max+ 395 APU (Radeon 8060S, gfx1151) triggers repeated
`amdgpu: Freeing queue vital buffer, queue evicted` kernel messages.
After 30-60 minutes, evictions cascade (6+ in <1 second), killing the
Wayland display compositor (KWin) and leaving the GPU in a hung state
(100% busy, 0 compute) that requires `rocm-smi --gpureset` to recover.

Three concurrent processes run indefinitely without issue. The problem
occurs exclusively at 4+ concurrent GPU consumers.

## System information

| Component | Version |
|-----------|---------|
| CPU | AMD Ryzen AI Max+ 395 w/ Radeon 8060S |
| GPU | Radeon 8060S Graphics (gfx1151), integrated APU |
| VRAM | 512 MB dedicated + 105.5 GB GTT (unified memory) |
| OS | Fedora Linux 43 (Workstation Edition) |
| Kernel | 6.18.13-200.fc43.x86_64 |
| ROCm runtime | rocm-runtime-6.4.2-3.fc43 |
| rocm-smi | 6.4.3-1.fc43 |
| PyTorch | 2.9.1+rocm7.12.0a20260204 |
| Display server | KWin (Wayland) |
| RAM | 128 GB LPDDR5X-8000 (unified with GPU) |

## Reproducer

### Workload

Each process runs PyTorch neural network inference (protein structure
prediction) using `torch.cuda` on the integrated GPU. Each process
allocates approximately 5 GB GTT memory. The workload is sequential
inference calls (not training), each lasting 30-60 seconds.

### Minimal reproduction

```bash
# Launch 4 concurrent PyTorch GPU inference processes
# (any sustained PyTorch GPU workload will trigger this)
for i in $(seq 1 4); do
    python -c "
import torch
import time
while True:
    x = torch.randn(4096, 4096, device='cuda')
    y = torch.matmul(x, x)
    torch.cuda.synchronize()
" &
done

# Monitor kernel log:
# journalctl -kf | grep amdgpu

# After 30-60 minutes, display compositor will crash.
# GPU becomes unresponsive (100% busy, no actual compute).
```

### Working vs crashing configurations

| Workers | GTT used | Duration | Result |
|---------|----------|----------|--------|
| 3 | ~15 GB | 24+ hours | Stable, no issues |
| 4 | ~20 GB | 30-60 min | Queue eviction cascade, display crash |
| 4+ (any) | ~20+ GB | <60 min | Same crash |

Note: GTT capacity is 105.5 GB. Memory is **not** the bottleneck — only
~19% is used at the time of crash.

## Observed behavior

### Phase 1: Periodic evictions (non-fatal)

With 4 workers running, queue evictions begin immediately and occur at
regular intervals (~10 minutes apart):

```
Mar 02 10:00:31 kernel: amdgpu: Freeing queue vital buffer 0x7f0a97600000, queue evicted
Mar 02 10:02:01 kernel: amdgpu: Freeing queue vital buffer 0x7f639fa00000, queue evicted
Mar 02 10:03:07 kernel: amdgpu: Freeing queue vital buffer 0x7f09ef000000, queue evicted
Mar 02 10:03:27 kernel: amdgpu: Freeing queue vital buffer 0x7f3a9fa00000, queue evicted
[... pattern repeats every ~10 minutes ...]
```

During this phase, inference continues to make progress. Processes recover
from individual evictions.

### Phase 2: Cascade (fatal)

After 30-60 minutes, evictions suddenly cascade — 6 evictions within the
same second:

```
Mar 02 10:54:05 kernel: amdgpu: Freeing queue vital buffer 0x7fc5e1600000, queue evicted
Mar 02 10:54:05 kernel: amdgpu: Freeing queue vital buffer 0x7fc869400000, queue evicted
Mar 02 10:54:05 kernel: amdgpu: Freeing queue vital buffer 0x7f16c4200000, queue evicted
Mar 02 10:54:05 kernel: amdgpu: Freeing queue vital buffer 0x7fe1db000000, queue evicted
Mar 02 10:54:05 kernel: amdgpu: Freeing queue vital buffer 0x7fc5e2a00000, queue evicted
Mar 02 10:54:05 kernel: amdgpu: Freeing queue vital buffer 0x7feea3400000, queue evicted
```

### Phase 3: Aftermath

After the cascade:

1. KWin (Wayland compositor) loses its GPU context and crashes.
2. The GPU enters a hung state: `rocm-smi --showuse` reports 100% busy,
   but no compute queues are active.
3. All PyTorch processes hang on any GPU operation
   (even `torch.tensor([1.0], device='cuda')`).
4. Recovery requires `sudo rocm-smi -d 0 --gpureset` or a full reboot.

## Expected behavior

With 105.5 GB GTT available and only ~20 GB in use, 4 concurrent GPU
processes should not trigger queue evictions. The GPU queue scheduler
should be able to manage 4-5 concurrent compute contexts without
evicting the display compositor's queue.

At minimum, the display compositor's queue should be protected from
eviction (higher priority) so that compute workload issues do not crash
the user's desktop session.

## Additional context

### Confirmed across multiple workloads

This is not specific to one application. The same crash pattern has been
reproduced with:

- 4x RoseTTAFold3 inference processes (protein structure prediction)
- 3x RoseTTAFold3 + 1x Ollama LLM inference (mixed workload)
- The common factor is 4+ concurrent processes using `torch.cuda`
  operations via ROCm/HIP

### Three workers is a hard limit

Extensive testing over 100+ hours of cumulative runtime confirms that
3 concurrent GPU inference processes are stable indefinitely. The 4th
process is the breaking point regardless of per-process memory usage
(tested with workloads ranging from 4-8 GB GTT per process).

### The evictions correlate with queue count, not memory

- 3 workers + display = 4 GPU contexts: **0 evictions** in kernel log
- 4 workers + display = 5 GPU contexts: **evictions begin immediately**
- GTT usage at crash time: 18-20 GB of 105 GB (< 20%)

This suggests a limit on concurrent GPU queue/context count rather than
a memory pressure issue.

## Impact

This is a significant usability issue for the Ryzen AI Max APU product
line, which is marketed for AI workloads. The integrated GPU architecture
means there is no way to offload the display to a separate GPU — the
compute and display share the same device. A hard limit of 3 concurrent
GPU inference processes substantially limits the throughput of multi-
process AI workloads on this hardware.

## Suggested investigation areas

1. **Queue scheduler priority**: Can the display compositor's queue be
   given higher eviction priority to prevent desktop crashes even if
   compute queues are under pressure?
2. **Concurrent queue limit on gfx1151**: Is there a hardware or firmware
   limit on the number of concurrent compute queues for this GPU IP?
3. **Eviction cascade mechanism**: Why do individual recoverable evictions
   (Phase 1) eventually cascade into an unrecoverable state (Phase 2)?
4. **GTT-backed queue buffers**: The eviction message references "queue
   vital buffer" addresses in GTT space. Is there a separate pool or
   limit for queue metadata that is smaller than the GTT pool itself?


---

## 评论 (4 条)

### 评论 #1 — chejh-amd (2026-03-03T01:26:51Z)

Hi @ripley2298 Have you tried setting amdgpu.cwsr_enable=0 to see if the issue still happens?

---

### 评论 #2 — darren-amd (2026-03-04T21:32:06Z)

Hi @ripley2298,

Thanks for reporting the issue. I gave this a try with your reproduction script on the latest PyTorch/ROCm wheels with 8 concurrent processes overnight and was unable to reproduce the issue. I noticed that you are on an older version of ROCm, could you try upgrading by following the instructions for [ROCm](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#rocm-for-gfx1151) and [torch](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#torch-for-gfx1151) inside of a fresh environment and see if the issue persists? Thanks!

---

### 评论 #3 — ripley2298 (2026-03-10T19:24:29Z)

> Hi [@ripley2298](https://github.com/ripley2298) Have you tried setting amdgpu.cwsr_enable=0 to see if the issue still happens?

This seems to resolve the issue, maybe at a slight performance penalty (55 outputs per hr instead of 60).

---

### 评论 #4 — darren-amd (2026-03-10T19:33:51Z)

Awesome, thanks for confirming! I'd still recommend updating your ROCm/torch packages to latest as ROCm 7.2 is a lot more stable on `gfx1151`. If there's nothing else, I will close this ticket.

---
