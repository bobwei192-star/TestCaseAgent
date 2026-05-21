# [gfx1151] Silent hard hang under sustained vLLM inference with MES 0x86 — amdgpu hangcheck never fires

> **Issue #6165**
> **状态**: open
> **创建时间**: 2026-04-20T16:23:58Z
> **更新时间**: 2026-05-12T14:57:57Z
> **作者**: Lafunamor
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6165

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

Follow-up to [ROCm/ROCm#5724](https://github.com/ROCm/ROCm/issues/5724) and [ROCm/ROCm#5991](https://github.com/ROCm/ROCm/issues/5991). The MES 0x83 page-fault class was resolved for us by upgrading to MES 0x86 (upstream `linux-firmware` tag `20260410`). A **distinct, silent hang** remains on the same node under sustained compute — no page fault, no GPU reset, no MCE, no kernel log. Filing because the fence-ring evidence below narrows it beyond what dmesg shows and may be useful for triage.

## System

| | |
|---|---|
| Machine | Framework Desktop (2025) |
| SoC | AMD Ryzen AI MAX+ 395 (Strix Halo) |
| GPU | Radeon 8060S, gfx1151, PCI `0000:c1:00.0` `[1002:1586]` |
| BIOS | 03.04 (2025-11-19), LVFS latest |
| Distro | Ubuntu Questing (25.10 / 26.04-preLTS) |
| Kernel | `7.0.0-070000-generic` (mainline, `#202604122140 SMP PREEMPT_DYNAMIC Sun Apr 12 22:05:40 UTC 2026`) |
| Kernel cmdline (relevant) | `iommu=pt amdgpu.gttsize=126976 ttm.pages_limit=32505856 amd_iommu=on amdgpu.cwsr_enable=0` |
| `linux-firmware` in use | Ubuntu `20250901` + upstream `20260410` override at `/lib/firmware/updates/amdgpu/` |
| **MES firmware** | `MES feature version: 1, firmware version: 0x00000086` |

### Container / runtime

- Image: `docker.io/kyuz0/vllm-therock-gfx1151:latest` (built 2026-04-19 21:31 UTC)
- vLLM: `0.19.2rc1.dev14+gf150107ef.d20260419`
- PyTorch: `2.13.0a0+rocm7.13.0a20260419`
- HIP: `7.13.26154`

## Symptom

Running vLLM with `cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit` (MoE 35B/3B active, AWQ-4bit, ~20 GiB weights), `--enforce-eager`, `--max-num-seqs 1`, `--max-model-len 262144`, `--gpu-memory-utilization 0.75`, vision encoder disabled.

Under sustained prefill load (agentic client sending back-to-back long-context requests), the engine wedges after **20–90 seconds**:

```
Engine 000: Avg prompt throughput: 0.0 tokens/s,
            Avg generation throughput: 0.0 tokens/s,
            Running: 1 reqs, Waiting: 1 reqs,
            GPU KV cache usage: 0.9%
```

From that point:

1. CPU-only services (systemd-cron, sysstat, tailscaled, journald) keep heartbeating for **2–4 minutes**.
2. The whole box then fully freezes. Only a hard reboot recovers it.
3. After reboot: `EXT4-fs (dm-0): orphan cleanup on readonly fs` + `system.journal … corrupted or uncleanly shut down` (hard-hang confirmation).

### What is NOT present in dmesg

- No `amdgpu … page fault`, no `GCVM_L2_PROTECTION_FAULT_STATUS`.
- No `GPU reset` / `device wedged`.
- No MCE / `hardware error` / `machine check`.
- No OOM / `Killed process`.
- No thermal / throttling / `under-voltage` / `brown-out`.
- No panic / Oops / Call Trace.

The **only** kernel tell on the crashing boot is `pcieport 0000:00:08.1: PME: Spurious native interrupt!`, typically 30–60 s after the engine wedges, consistently present across every reproduction on this node.

## Reproduction

1. Kernel ≥ 6.18-rc6 (or mainline as above), `amdgpu.cwsr_enable=0`.
2. Upstream `linux-firmware 20260410` installed to `/lib/firmware/updates/amdgpu/`, MES reports `0x86`.
3. vLLM via `docker.io/kyuz0/vllm-therock-gfx1151:latest`, settings above.
4. Drive concurrent long-context prefill load (~20 k-token prompts, back-to-back).
5. Hang within 20–90 s.

Short conversational requests do **not** trigger it. A ≥10 k-token prefill burst or sustained decode does.

## Fence-ring evidence (new this round)

### How it was collected

A 2-second-cadence sampler of `/sys/kernel/debug/dri/0000:c1:00.0/amdgpu_fence_info` running as a systemd service on the host, log rotated on each service start so the file active at the moment the box freezes survives the reboot.

Sampler (`/usr/local/bin/gpu-fence-sampler.sh`):

```bash
#!/bin/bash
# Fence-info sampler: 2s cadence, timestamped.
# Rotates on service start so prior-boot data is preserved across crash+reboot.
set -u
LOG=/var/log/gpu-fences.log
if [ -s "$LOG" ]; then
  for i in 4 3 2 1; do
    [ -f "$LOG.$i" ] && mv "$LOG.$i" "$LOG.$((i+1))"
  done
  mv "$LOG" "$LOG.1"
fi
: > "$LOG"
printf '=== boot $(uname -r) start %s ===\n' "$(date -u +%F\ %T)" >> "$LOG"
while true; do
  ts=$(date -u +%H:%M:%S.%3N)
  {
    printf '=== %s ===\n' "$ts"
    cat /sys/kernel/debug/dri/0000:c1:00.0/amdgpu_fence_info
  } >> "$LOG"
  sleep 2
done
```

systemd unit (`/etc/systemd/system/gpu-fence-sampler.service`):

```
[Unit]
Description=amdgpu fence sampler (2s) for hang investigation
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/local/bin/gpu-fence-sampler.sh
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### MES scheduler ring (`mes_3.0.0`) across the wedge

Projected from one representative crash boot (full log attached below as `gpu-fences.log.2`). Each row is a 2 s sample; columns are `Last signaled fence` / `Last emitted`.

| UTC | mes_3.0.0 sig / em | interpretation |
|---|---|---|
| 15:36:00.409 | `0x3ef` / `0x3ef` | normal advance |
| 15:36:46.633 | `0x559` / `0x559` | first request just submitted |
| 15:36:48.641 | `0x561` / `0x561` | advance |
| 15:36:50.648 | `0x561` / `0x561` | advance |
| **15:36:52.666** | **`0x570`** / **`0x570`** | **last observed advance** |
| 15:36:54.675 | `0x570` / `0x570` | frozen |
| 15:37:08.731 | `0x570` / `0x570` | **vLLM reports first `0.0 tok/s`** (≈16 s after MES last advanced) |
| 15:37:46.907 | `0x570` / `0x570` | first `pcieport … PME: Spurious native interrupt!` fires |
| 15:39:39.403 | `0x570` / `0x570` | CPU-only services still heartbeating |
| 15:41:07.794 | `0x570` / `0x570` | **last sampler read before full box freeze** (4 min 14 s of MES freeze captured) |

Across every post-freeze snapshot:

- `Last signaled fence == Last emitted` — host and device agree the ring is idle; host is *not* queuing new MES work.
- `Last reset = 0x00000000` — amdgpu's GPU reset path is **never** invoked.
- `Last preempted = 0x00000000` — no preemption attempts.

### What this rules in / out

- **Rules in:** amdgpu hangcheck/watchdog never fires for this failure mode — that's the reason the crash is silent in dmesg.
- **Rules in:** MES firmware is not fully dead on the bus — the debugfs node is still readable throughout the 2.5–4 min window, i.e. PCIe config space is alive. But the MES ring is not being driven.
- **Does not resolve:** whether the root cause is in MES firmware itself (wedged on chip) or in the amdgpu MES command path (deadlocked on host). `amdgpu_fence_info` is blind to KFD user-mode compute queues (doorbell-driven), which is where vLLM's actual compute submissions live.
- **Does not resolve:** whether a compute shader is still running on the CUs, or the CUs are idle.

## Ruled out (single-variable probes, all exonerated on this node)

| Probe | Result |
|---|---|
| `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1` dropped | still crashed |
| `amdgpu.noretry=1` | still crashed |
| `ATTENTION_BACKEND=ROCM_ATTN` (vs default `TRITON_ATTN`) | still crashed — note `chunked_prefill_paged_decode.py:398 Cannot use ROCm custom paged attention kernel, falling back to Triton implementation`, so this override is a no-op for the AWQ decode path |
| `VLLM_V1_USE_PREFILL_DECODE_ATTENTION=1` | crashed ~40 s |
| `VLLM_USE_TRITON_FLASH_ATTN=0` | crashed ~23 s |
| `VLLM_ROCM_USE_MMAP_FOR_TRITON=0` | crashed (~60 s) |
| BIOS upgrade | already on latest (03.04, 2025-11-19) |
| Thermal / RAM / GTT pressure | all flat at values well below any threshold during the whole repro window |
| PSU sag | inconsistent with symptom — CPU + NVMe + net keep running 2–4 min after GPU wedge; no under-voltage/MCE/throttle events |

## Known workaround (not a fix)

`VLLM_LOGGING_LEVEL=DEBUG` prevents the hang. The mechanism appears to be that per-step stderr writes throttle the Python submission loop enough that GPU utilisation drops from ~100% to ~70%, which dodges the timing window that triggers the hang. This is consistent with the `pcieport 0000:00:08.1: PME: Spurious native interrupt!` precursor pointing at root-complex bursty-submission stress.

## Questions for AMD

1. Is there a recommended debugfs / sysfs observable for **KFD user-mode compute queue** state that would let us see whether a shader is wedged vs the doorbell path itself? `amdgpu_fence_info` is blind to the actual vLLM compute work.
2. Why does the MES ring freeze while the amdgpu hangcheck never fires? Is the watchdog not armed for MES-ring idleness, or is it armed but the recovery path itself deadlocks before logging?
3. Is the `pcieport 0000:00:08.1: PME: Spurious native interrupt!` signal on Strix Halo (GPU root-complex, `00:08.0`) a known accompanying symptom, and does it point to a specific layer (SMU, PCIe AER, MES)?

---

## Attachments

### `amdgpu_firmware_info` (full)

```
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 35, firmware version: 0x00000020
PFP feature version: 35, firmware version: 0x00000031
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x11530506
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x11530506
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 35, firmware version: 0x00000022
IMU feature version: 0, firmware version: 0x0b352300
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 10, firmware version: 0x0a640600 (100.6.0)
SDMA0 feature version: 60, firmware version: 0x00000012
VCN feature version: 0, firmware version: 0x09118010
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x09004100
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000086
VPE feature version: 60, firmware version: 0x00000017
VBIOS version: 113-STRXLGEN-001
```

### GPU `lspci -vvv` (relevant sections)

```
c1:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Strix Halo
        [Radeon Graphics / Radeon 8050S Graphics / Radeon 8060S Graphics] (rev c1)
    Subsystem: Framework Computer Inc. Device 000a
    IOMMU group: 17
    Region 0: Memory at 6800000000 (64-bit, prefetchable) [size=512M]
    Region 2: Memory at b0000000  (64-bit, prefetchable) [size=2M]
    Region 5: Memory at b0400000  (32-bit, non-prefetchable) [size=1M]
    Capabilities: [50] Power Management version 3
        Flags: PMEClk- DSI- D1- D2- AuxCurrent=0mA
               PME(D0-,D1+,D2+,D3hot+,D3cold+)
    Capabilities: [64] Express (v2) Legacy Endpoint
        LnkCap: Port #0, Speed 16GT/s, Width x16
        LnkSta: Speed 16GT/s, Width x16
                TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
    Capabilities: [2a0 v1] Access Control Services
    Capabilities: [2b0 v1] Address Translation Service (ATS)   Enable+
    Capabilities: [2c0 v1] Page Request Interface (PRI)
```

(Link is at its target 16 GT/s × 16 with no training errors, ATS enabled, PRI capability present. No AER errors.)

### vLLM log — transition into wedge

Selected lines from the vLLM server stdout for the probe-2 crash (`VLLM_USE_TRITON_FLASH_ATTN=0`). Client IPs redacted.

```
15:36:28  INFO: Application startup complete.
15:36:45  WARNING chunked_prefill_paged_decode.py:398
          Cannot use ROCm custom paged attention kernel,
          falling back to Triton implementation.
15:36:46  INFO: 127.0.0.1:45814 - "POST /v1/chat/completions HTTP/1.1" 200 OK
15:36:47  INFO: 127.0.0.1:45814 - "POST /v1/chat/completions HTTP/1.1" 200 OK
15:36:48  Engine 000: Avg prompt throughput: 6.9 tokens/s,
                     Avg generation throughput: 0.2 tokens/s,
                     Running: 0 reqs, Waiting: 0 reqs
15:36:48..:51   several 200 OK responses, both localhost and remote client
15:36:58  Engine 000: Avg prompt throughput: 207.4 tokens/s,
                     Avg generation throughput: 3.4 tokens/s,
                     Running: 1 reqs, Waiting: 1 reqs,
                     GPU KV cache usage: 0.6%
15:37:08  Engine 000: Avg prompt throughput: 0.0 tokens/s,    ← wedge
                     Avg generation throughput: 0.0 tokens/s,
                     Running: 1 reqs, Waiting: 1 reqs,
                     GPU KV cache usage: 0.9%
(from this point no further engine log lines are emitted)
15:37:46  kernel: pcieport 0000:00:08.1: PME: Spurious native interrupt!
(cron/sysstat keep running until ~15:40:29, then full box freeze)
```

### Full fence-info sampler log (crash boot)

> Attached as `gpu-fences.log.2` (≈ 820 KB, gzipped). Contents are 2 s-cadence snapshots of `/sys/kernel/debug/dri/0000:c1:00.0/amdgpu_fence_info` covering 9 min 8 s spanning pre-wedge, wedge, and sampler death at full box freeze. No sensitive data.
[gpu-fences.log.2.gz](https://github.com/user-attachments/files/26903760/gpu-fences.log.2.gz)

[amdgpu_firmware_info.txt](https://github.com/user-attachments/files/26903759/amdgpu_firmware_info.txt)

### Also available on request

- `journalctl -b -1` for each of 4 crashing boots on 2026-04-20 (will redact hostnames/IPs before sharing if preferred).
- vLLM full stdout/stderr for each reproduction.
- `gpu-fences.log.1`, `.log.3` — fence-info sampler logs for the other crashing boots on 2026-04-20 (similar signature, same 0x570-class freeze on a different last-fence value each run).

---

## 评论 (9 条)

### 评论 #1 — Lafunamor (2026-04-20T21:16:54Z)

Reproduced the same silent hang on the same node with a **completely different userspace stack**: llama.cpp + Vulkan (Mesa RADV), no ROCm in the picture. Different failure characteristics but **identical end-state**, which changes how ROCm-specific this is.

## Setup

- Same host, same kernel (`7.0.0-070000-generic`), same firmware (MES `0x86`), same cmdline (`amdgpu.cwsr_enable=0`).
- Container: `docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-radv` (Mesa RADV, Vulkan 1.4).
- Model: `unsloth/Qwen3.6-35B-A3B-GGUF` (`UD-Q4_K_M`, ~22 GiB).
- llama-server settings: `--parallel 1 --ctx-size 262144 --jinja`. Same agentic client load as the vLLM repros.

## Symptom

- Ran stable under sustained 100 k+-token prefill load for **71 minutes** (vLLM wedges at 20–90 s).
- No deceleration, no stall, no `0 tok/s` plateau — the last request completed normally and the box froze seconds later:

```
17:12:11  prompt eval time =  1225.91 ms /  317 tokens (258.58 tok/s)
17:12:11  eval   time    = 28568.44 ms /  914 tokens  ( 31.99 tok/s)
17:12:11  slot release:  stop processing: n_tokens = 136706, truncated = 0
17:12:12  new request accepted, prompt processing progress = 0.999971
17:12:14  done request: POST /v1/chat/completions 200
(no further llama-server log lines)
(journal ends at 17:12:38 — full box freeze, same orphan-cleanup / corrupted-journal markers on next boot)
```

- `dmesg` from the crashing boot: **no** `PME: Spurious native interrupt`, no fault, no reset, no MCE. The vLLM repros always have 2–3 PME Spurious events in the 30–60 s before freeze; this boot has **zero**.

## Fence-ring evidence (llama.cpp/Vulkan)

Same 2 s-cadence sampler as before, covering the full 71-minute run (2109 snapshots). Key rings, selected across the run:

| UTC | `gfx_0.0.0` | `comp_1.1.0` | `sdma0` | `mes_3.0.0` |
|---|---|---|---|---|
| 16:01:52 (boot) | `0x1` | `0x1` | `0x1a` | `0xf` |
| 16:11:55 (idle) | `0x1` | `0x1` | `0x1a` | `0xf` |
| 16:32:00 (warmup) | `0xb874` | `0x6b07` | `0x2a578` | `0x15` |
| 16:42:03 | `0xeb37` | `0xb2be` | `0x2a5a2` | `0x15` |
| 16:52:06 | `0x1d39b` | `0x276bb` | `0x2a5a2` | `0x15` |
| 17:02:09 | `0x1edcc` | `0x2a6b3` | `0x2a5ae` | `0x15` |
| 17:12:13 | `0x35c02` | `0x5715a` | `0x2a5ba` | `0x15` |
| 17:12:21 | `0x36314` | `0x57f07` | `0x2a5ba` | `0x15` |
| 17:12:23 | `0x364d4` | `0x5828a` | `0x2a5ba` | `0x15` |
| 17:12:25 | `0x36694` | `0x585ff` | `0x2a5ba` | `0x15` |
| **17:12:27 (last sample)** | **`0x36854`** | **`0x5897e`** | **`0x2a5ba`** | **`0x15`** |

(journal cuts off at `17:12:38`, ~11 s after the last sampler write)

Two things jump out:

1. **MES scheduler ring (`mes_3.0.0`) is barely used.** Across the entire 71-minute run the sampled value takes only 4 distinct values total: `0xf` (boot/idle), `0x11`, `0x13`, `0x15`. The ring is *not* the driven path for Vulkan/RADV, which makes sense — RADV submits via `amdgpu_cs_ioctl`, doorbells go through the kernel, MES isn't brokering compute like it does for KFD user-mode queues. Contrast with the vLLM crash logs where MES advances every sample (`0x3ef → 0x559 → 0x570`) then freezes there.
2. **`gfx` and `comp` rings were advancing normally right up to the last sample.** `gfx_0.0.0` advanced `0x36314 → 0x36854` (~1.3 k fences) in the last 6 seconds — no deceleration, no unsignaled-fence gap between `Last signaled` and `Last emitted`. Then silence. Whatever kills the box does it between one 2 s tick and the next, with no ring-level warning visible to amdgpu.

## Comparison

| | vLLM (ROCm/HSA) | llama.cpp (Vulkan/RADV) |
|---|---|---|
| Time to wedge under load | 20–90 s | ~71 min |
| Last-fence state | MES frozen at `0x570`, gfx idle | MES at `0x15` (barely used), gfx actively advancing |
| `amdgpu_fence_info` pre-freeze trajectory | MES ring freezes ~14 s *before* engine reports `0 tok/s` | No freeze visible at all — cliff edge between samples |
| `pcieport 00:08.1: PME: Spurious native interrupt!` | consistently present (2–3 events, 30–60 s window) | **not present** |
| User-space symptom | engine reports `0 tok/s`, requests hang | last request completes normally, then box freezes |
| Orphan-cleanup / corrupted-journal on next boot | yes | yes |
| Recovery | hard reboot only | hard reboot only |

## Implication

The hang reproduces on a userspace stack that does not go through ROCm, HIP, MES user-mode queues, Triton, PyTorch, or KFD. Both stacks end in the same silent-wedge / orphan-cleanup failure state. The intersection is small:

- amdgpu kernel driver
- MES firmware (even when Vulkan barely touches it — `0xf → 0x15` is still 6 scheduler advances it can get wrong)
- SMU / PMFW (`0x0a640600`)
- PCIe root-complex / SoC path `0000:00:08.1 → 0000:c1:00.0`

The `PME: Spurious native interrupt` precursor on the ROCm path may just be a faster trigger on the same underlying bug, not a separate class. The Vulkan reproduction doesn't produce that event but ends at the same failure.

## Addendum to ruled-out list

| Probe | Result |
|---|---|
| Swap userspace to Vulkan/RADV (llama.cpp, no ROCm) | **still crashes** (71 min under sustained prefill load) |

## Also available on request

- `gpu-fences.log.1` for this boot (full 71-minute run, ~4.5 MB uncompressed, ~40 KB gzipped). Same non-sensitive format as the one already attached.
- llama-server full stdout covering the 71-minute run.


---

### 评论 #2 — Lafunamor (2026-04-21T11:15:05Z)

Second llama.cpp/Vulkan reproduction on the same node — one correction to my earlier comment, one new data point.

## Correction

In the previous comment I said the Vulkan crash had **no** `pcieport 0000:00:08.1: PME: Spurious native interrupt!` event. That was n=1. This second repro fired **one** PME Spurious event at 09:25:55, ~9 min before the hard hang at 09:34:18. So the precursor signal is *reduced* on the Vulkan path, not absent: vLLM crashes reliably carry 2–3; Vulkan carries 0–1 over vastly longer uptimes. I'll hold that refined claim at n=2.

## This run

- Same host/kernel/firmware (`7.0.0-070000-generic`, MES `0x86`, `amdgpu.cwsr_enable=0`).
- Same container: `docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-radv`. Same model: `unsloth/Qwen3.6-35B-A3B-GGUF` `UD-Q4_K_M`. Added `--chat-template-kwargs '{"enable_thinking":false}'` between runs (template-only change; doesn't affect kernel submission path).
- Uptime before hang: **12 h 31 m** (previously 71 min). Agentic workload (opencode) driving long-context prefill bursts as before.
- Same end-state: `EXT4 orphan cleanup on readonly fs`, `system.journal corrupted or uncleanly shut down`, empty pstore, `tainted=0`, no panic, no fault, no reset, no MCE.

## Telemetry at cutoff (100 ms-granularity context)

`gpu-telemetry.service` samples every 2 s, last sample 09:34:29 UTC — **11 s past journald cutoff**, consistent with the prior crashes where CPU-only services outlive journald by seconds.

Last ~40 s of samples, all flat:

```
09:33:48Z busy=100 gpuT=66000 gpuP= 99096000 gpuF=2615 gtt=28907798528/133143986176 memA=94465180
09:34:00Z busy=100 gpuT=69000 gpuP=100015000 gpuF=2622 gtt=28907798528/133143986176 memA=94429284
09:34:10Z busy=100 gpuT=67000 gpuP= 99087000 gpuF=2615 gtt=28907798528/133143986176 memA=94430948
09:34:20Z busy=100 gpuT=68000 gpuP=100033000 gpuF=2629 gtt=28907798528/133143986176 memA=94366500
09:34:29Z busy=100 gpuT=69000 gpuP=100013000 gpuF=2630 gtt=28907798528/133143986176 memA=94370268
```

- GPU busy pinned at 100 %, clock at boost (~2.6 GHz), power ~99–100 W.
- Temperature 66–69 °C — cool.
- GTT 28.9 GB / 124 GB, VRAM 236 MB / 512 MB, MemAvailable 94 GB — nothing near a pressure threshold, nothing drifting.
- Textbook "firmware hang below the logging layer" fingerprint.

## Fence-ring trajectory

Sampler died at 09:34:06.967 UTC (about 22 s before telemetry). Across the full 12.5-hour run (22 426 samples):

- `mes_3.0.0` distinct signaled values: `{0xf, 0x11, 0x15}` — **three** unique values across 12.5 hours. RADV does not drive MES; "barely used" is its normal state on this path.
- `gfx_0.0.0` advancing smoothly right up to the last sample:

| UTC | `gfx_0.0.0` | `comp_1.1.0` | `comp_1.2.0` | `sdma0` | `mes_3.0.0` |
|---|---|---|---|---|---|
| 09:33:48 | `0x1392b` | `0x16652` | `0x166ce` | `0x2a59b` | `0x15` |
| 09:33:56 | `0x13985` | `0x1668e` | `0x16718` | `0x2a59b` | `0x15` |
| 09:34:02 | `0x13997` | `0x166be` | `0x1674d` | `0x2a59b` | `0x15` |
| **09:34:06 (last)** | **`0x139a9`** | **`0x166e3`** | **`0x16769`** | **`0x2a59b`** | **`0x15`** |

`Last signaled == Last emitted` everywhere. No unsignaled-fence gap developing. No preemption, no reset. Then silence.

## Summary of the two repros side by side

| | llama.cpp repro #1 (2026-04-20) | llama.cpp repro #2 (2026-04-21) |
|---|---|---|
| Time-to-hang | 71 min | **12 h 31 m** |
| `mes_3.0.0` at cutoff | `0x15` (3 distinct values in 71 min) | `0x15` (3 distinct values in 12.5 h) |
| `gfx_0.0.0` at cutoff | advancing (~1.3 k fences/6 s) | advancing (~80 fences/6 s, lighter load) |
| PME Spurious precursors | 0 | **1** (09:25:55, 9 min before crash) |
| Telemetry at cutoff | (not captured for that run) | busy=100, 66–69 °C, flat GTT/mem |
| End-state | orphan cleanup + corrupted journal | identical |

## Full fence log (this repro)

Available on request — `/var/log/gpu-fences.log.1` covering 21:02:55 → 09:34:06 (~48 MB uncompressed; gzips to a few hundred KB). Same format as the one attached to the top-level ticket.


---

### 评论 #3 — Lafunamor (2026-04-21T13:47:09Z)

Short update — third llama.cpp/Vulkan repro on the same node, and a further correction on the PME claim.

**Run**: same stack, same firmware (MES `0x86`). Bumped llama.cpp `-b 2048 -ub 2048` (from default `-ub 512`) between runs to increase per-kernel submission size — wanted to see if heavier submission bursts shorten time-to-hang. Uptime **2 h 31 m** before hard hang (vs 12 h 31 m previous run, 71 min first run).

**PME Spurious on Vulkan — refined claim, n=3 runs**

| Run | Uptime | `PME: Spurious native interrupt!` events |
|---|---|---|
| llama.cpp #1 | 71 min | 0 |
| llama.cpp #2 | 12 h 31 m | 1 (9 min before crash) |
| llama.cpp #3 (heavier submissions) | 2 h 31 m | **3** (11:19, 11:21, 13:20; last was 17 min pre-crash) |

Walks back both earlier framings: the Vulkan path is not "PME-free" and not even reliably "PME-reduced." Precursor count looks correlated with submission intensity rather than userspace stack. Count, relative spacing, and crash-proximity timing are all within the vLLM distribution (vLLM runs show 2–3 events in 30–60 s windows; this run had 3 events spread over the 2.5 h uptime). Please discount my earlier "signature differs" framing for the PME line specifically — it doesn't.

**Everything else holds**

- Same cliff-edge fence signature: `mes_3.0.0` took only `{0xf, 0x11, 0x15}` across the full run (RADV doesn't drive MES), `gfx_0.0.0` actively advancing right up to the last fence sample (13:37:01, 3 s before journald cutoff), `Last reset = 0x0` / `Last preempted = 0x0` throughout.
- Telemetry flat at cutoff: `busy=100`, `gpuT=60–68 °C`, `gpuP=87–96 W`, `gpuF=2.85 GHz`, GTT 32.9 GB / 124 GB, MemAvail 88 GB.
- Same end-state: orphan cleanup, corrupted journal, empty pstore, `tainted=0`, no fault / reset / MCE / panic.

**Time-to-hang vs load shape (all n=3 Vulkan runs):** heavy-sustained prefill reproduces in 71 min and 2.5 h; bursty-agentic lasts 12.5 h. Shape of the load drives when, not whether.

Available on request: `/var/log/gpu-fences.log.1` for this run (~10 MB uncompressed), telemetry for the same window, llama-server stdout.


---

### 评论 #4 — Lafunamor (2026-04-21T14:18:39Z)

New data point that partially contradicts this ticket's framing — worth flagging.

## Summary

Pushed llama.cpp's physical micro-batch further (`-b 4096 -ub 4096`, up from 2048 in my previous comment) to see whether even heavier per-kernel submissions would change time-to-hang. Instead of accelerating the silent hang, it pushed the failure into **a different class that amdgpu can actually detect and recover from**. Same host / kernel / firmware / container / model / workload as the prior n=3 Vulkan repros.

**n=2 in one boot.** Both under `-b 4096 -ub 4096`, both on a compute ring, both recovered via ring reset. Node stayed up both times.

## The two crashes

| | Crash #1 | Crash #2 |
|---|---|---|
| Time | 13:55:29 UTC | 14:14:22 UTC (same boot) |
| Time since previous llama-server start | ~10 min | ~14 min |
| Failing ring | `comp_1.1.0` | `comp_1.2.0` |
| Ring fence state at timeout | signaled 12263, emitted 12265 | signaled 24613, emitted 24615 |
| Signal/emit gap | **2 fences** | **2 fences** |
| Fence-fallback-timer precursor | 13:51:07 on `comp_1.2.0`, 4m22s before reset | **none** |
| Ring reset outcome | `Ring comp_1.1.0 reset succeeded` | `Ring comp_1.2.0 reset succeeded` |
| Devcoredump | generated (not preserved) | **generated, preserved — 6.1 MB on request** |
| PME Spurious events before crash | 0 | 0 |

Representative dmesg for crash #2 (crash #1 is identical modulo ring/seq numbers):

```
amdgpu 0000:c1:00.0: Dumping IP State
amdgpu 0000:c1:00.0: Dumping IP State Completed
amdgpu 0000:c1:00.0: [drm] AMDGPU device coredump file has been created
amdgpu 0000:c1:00.0: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:c1:00.0: ring comp_1.2.0 timeout, signaled seq=24613, emitted seq=24615
amdgpu 0000:c1:00.0:  Process llama-server pid 26186 thread llama-server pid 26186
amdgpu 0000:c1:00.0: Starting comp_1.2.0 ring reset
amdgpu 0000:c1:00.0: reset compute queue (1:2:0)
amdgpu 0000:c1:00.0: Ring comp_1.2.0 reset succeeded
amdgpu 0000:c1:00.0: [drm] device wedged, but recovered through reset
```

Container side, both crashes: `radv/amdgpu: The CS has been cancelled because the context is lost. This context is innocent.` → `vk::DeviceLostError` → llama-server exit 139. Node stayed up; `uptime` is unbroken since boot.

## How this differs from the silent-hang class (this ticket's n=3+ cases)

- **amdgpu observes it.** Silent-hang runs all had `gfx_0.0.0` advancing right up to journal cutoff, no ring timeout ever fired, no reset, no devcoredump — kernel/firmware hang below the logging layer. This class fires the ring-timeout hangcheck and recovers.
- **Compute ring, not gfx.** Both `comp_1.x.0`. Silent-hang runs all had gfx active at cutoff.
- **Zero PME Spurious across the boot.** Prior Vulkan runs: 0 / 1 / 3 events. vLLM runs: 2–3 consistently. This class has none so far (n=2).
- **Consistent 2-fence gap** between signaled and emitted on the failing ring at timeout. Small, specific, reproducible.

Unclear yet whether this is the same underlying bug pushed into an observable regime by heavier submissions, or a different bug exposed at the same threshold.

## Correction to my prior comments — `amdgpu_fence_info` is blind to per-ring resets

I've been citing `Last reset = 0x0` in `amdgpu_fence_info` as evidence that the hangcheck never fired. That claim is weaker than I stated: after both successful ring resets above, `Last reset` is still `0x0` on every ring. Per-ring (queue-level) resets don't increment that counter — only device-level resets do. The stronger evidence for the silent-hang class remains the absence of any `ring timeout` / `reset` / `device wedged` kernel messages, not the fence_info field.

## What I'm offering

- The preserved devcoredump (6.1 MB, crash #2) — happy to attach if useful. Contains IP state dump, HWIP versions, firmware versions, and presumably the submission/queue state at timeout.
- Full `/var/log/gpu-fences.log` for the boot (both crashes included).
- `podman logs qwen3.6` showing the RADV `context is lost` → DeviceLostError stack.
- Telemetry for the crash windows.

Let me know what's most useful to attach. Happy to reproduce again with additional instrumentation if there's something specific you'd like captured.

## Reproducer

```bash
# Host: Framework Desktop, AMD Strix Halo gfx1151, kernel 7.0.0-070000-generic,
# MES firmware 0x86 (linux-firmware 20260410), amdgpu.cwsr_enable=0.
# Container: docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-radv (Mesa RADV).
# Model: unsloth/Qwen3.6-35B-A3B-GGUF  UD-Q4_K_M.

llama-server \
  -m Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --jinja --chat-template-kwargs '{"enable_thinking":false}' \
  -c 262144 --parallel 1 -ngl 999 -fa 1 --no-mmap \
  -b 4096 -ub 4096 \
  --host 0.0.0.0 --port 8000

# Drive with agentic long-context prefill (opencode etc.). Reproduces in 10–15 min
# of sustained load on this hardware.
```


---

### 评论 #5 — Lafunamor (2026-04-21T19:47:47Z)

Follow-up on the two classes (silent-hang vs `-ub 4096` per-ring-reset) and a
cross-reference to what looks like the same bug being discussed elsewhere.

## `amdgpu.gpu_recovery=1` does not rescue the silent-hang class

Motivated by zw963's dmesg in ROCm/ROCm#5665 — theirs recovers via MODE2 reset
under `amdgpu.gpu_recovery=1`, ours doesn't. Added the parameter to our cmdline
(`iommu=pt amdgpu.gttsize=126976 ttm.pages_limit=32505856 amd_iommu=on
amdgpu.cwsr_enable=0 amdgpu.gpu_recovery=1`) and re-ran.

Two results, both expected in hindsight:

- **`-ub 4096` per-ring-reset class (n=1 this boot):** no change. Same
  `comp_1.1.0 timeout, signaled seq=11801, emitted seq=11803` → per-ring reset
  → `device wedged, but recovered through reset`. That class was already
  recoverable, so `gpu_recovery=1` has nothing new to do.
- **Silent-hang class (n=1 this boot, at `-ub 2048`):** no change. Full reboot
  required. Journal stopped writing mid-workload with no `ring timeout`, no
  reset attempt, no oops — same signature as the previous n=3 silent hangs.

Consistent with the parameter's scope: `gpu_recovery` acts when the hangcheck
fires. The silent-hang class never fires one, so there's nothing for it to
rescue. Ruling it out as a mitigation for this ticket, but leaving it set in
case it helps the `-ub 4096` class get a cleaner recovery on some future boot.

## Possible cross-reference — Framework community "SMU deadlock on Fedora 43"

https://community.frame.work/t/smu-deadlock-system-freeze-on-fedora-43/81795

Same hardware class (Strix Halo / gfx1151 / Ryzen AI MAX+ 395 / DCN 3.5),
different userspace triggers (Chromium on GPU-heavy pages rather than llama.cpp
inference), but the symptoms line up:

- Silent hard freeze requiring power-off on affected kernels/Mesa, OR
  2-minute GPU reset + black screen.
- Kernel range 6.17–6.19 reported; some users report 7.0 still affected.
- Root-cause hypothesis in that thread: `dcn35_smu_enable_pme_wa` deadlocks
  when the SMU already has a pending command. During display-pipe teardown the
  driver tries to disable gfxoff, cannot communicate with the busy SMU,
  cascading timeouts, requires MODE2 ASIC reset.

Two reasons this might be the same underlying bug that manifests as our silent
hang under sustained compute:

1. **The function name is `*_enable_pme_wa`** — a PME workaround in the DCN35
   path. Our silent-hang precursor pattern across repros has been
   `pcieport 0000:00:08.1: PME: Spurious native interrupt!` events on the
   PCIe port the GPU is attached to (0/1/3 events across n=3 Vulkan runs;
   2–3 events consistently on the vLLM runs). The forum thread is describing
   a deadlock in code that is named for the same PME-handling path that is
   firing spurious interrupts in our traces.
2. **`gpu_recovery=1` splits the outcomes cleanly in the forum thread** —
   with it, users auto-recover after 2–3 min; without it, hard power-off.
   On our workload it doesn't rescue us. That's a divergence worth flagging:
   either the trigger path is different enough that the hang sits below the
   recovery hook even with the parameter set, or we're hitting a distinct
   bug that happens to share the PME precursor signature.

## Mitigations reported on the forum we haven't tried

- Mesa downgrade to 25.0.7 (our current Mesa is 26.0.3 from Ubuntu 26.04).
- `amdgpu.runpm=0`, `amdgpu.dcdebugmask=0x10`, `amdgpu.gfxoff=0`,
  `amdgpu.mes=0` — all reported ineffective in the forum thread, not worth
  trying independently here.

The Mesa angle doesn't obviously fit a headless-compute workload with no
display-pipe teardown traffic, but it's the only untried lever from the forum
list that isn't already ruled out upstream.

## Related ROCm tickets that seem to describe the same class

- ROCm/ROCm#5665 — Strix Halo + ROCm 7.1 concurrent AI + video → MES
  REMOVE_QUEUE failures, MODE2 reset recovery. Same-host-class bug where the
  recovery path *does* fire.
- ROCm/ROCm#6012 — queue eviction cascade on gfx1151 after sustained
  multi-process GPU load; primary workaround is `amdgpu.cwsr_enable=0`
  (already applied here) and upgrade to ROCm 7.2+.
- ROCm/ROCm#5991 — gfx1151 page fault on basic tensor ops; amd-nicknick
  confirmed FW 0x83 is broken, `cwsr_enable=0` required until the upstream
  fix lands.
- ROCm/ROCm#5151 — gfx1151 + Ubuntu + Ollama/qwen3 + sustained inference →
  MES REMOVE_QUEUE hang → MODE2 reset. Closest reproducer; again the reset
  path fires there and doesn't on ours.

## Question for upstream

Is the `dcn35_smu_enable_pme_wa` deadlock reported on the Framework forum
understood to be distinct from, or the compute-side manifestation of, the
silent-hang class in this ticket? If the same, the PME-Spurious precursor on
our pcieport traces may be a useful early-warning signal for reproducers on
that bug. If distinct, we probably want to spin this into a separate ticket
rather than keep consolidating.

## Current state of the box

- Host: Framework Desktop, AMD Strix Halo gfx1151, kernel
  `7.0.0-070000-generic`, linux-firmware distro `20260319` (MES 0x86),
  `amdgpu.cwsr_enable=0 amdgpu.gpu_recovery=1`.
- Userspace rotated recently: Ubuntu 25.10 → 26.04 (Mesa 25.2.8 → 26.0.3);
  container updated to fresh `docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-radv`
  (Fedora 43, Mesa 25.3.6, llama.cpp 8874). BIOS is current; no updates
  available via fwupd. Both silent-hang and per-ring-reset classes reproduce
  on this configuration.
- Time-to-silent-hang at `-ub 2048` on this boot was ~12 min post-launch, much
  shorter than the historical hours-to-days. May be variance, may be the new
  userspace hitting the trigger harder; flagging but not yet load-bearing.


---

### 评论 #6 — Lafunamor (2026-04-26T21:53:01Z)

## Update — additional testing; three hypotheses ruled out, PMFW 100.6.0 confirmed

After additional testing on the same gfx1151 + MES `0x86` + PMFW `100.6.0` stack (BIOS `03.04`, latest available; Framework has not announced an update):

**Ruled out as triggers** (verified via SMU `dynamic_debug`, debugfs telemetry, fence ring sampling):
- PCIe ASPM transitions — ASPM was already disabled by default on this hardware. The "PME Spurious is a precursor" framing in earlier comments should be walked back to "PME Spurious is a co-symptom from an as-yet-unidentified link source".
- GFX-off cycling — verifiably suppressed under `amdgpu.gfxoff=0`; hang fires anyway.
- MES firmware activity during the hang — `amdgpu.mes_log_enable=1` shows the event ring populated only at probe init, static through workload. Confirms the earlier fence-info finding: MES barely participates; KFD doorbells bypass it.

**New**: forensics confirm `SMC fw version: 0x0a640600` = PMFW 100.6.0 — same as the [Framework forum SMU-deadlock thread](https://community.frame.work/t/smu-deadlock-system-freeze-on-fedora-43/81795). That thread's VPE-PG-cycling trigger does not apply on headless compute (verified via `pr_debug` on `smu_cmn.c`: VPE messages fire only at probe init, never during workload; `resp_reg` stays at `PPSMC_Result_OK` throughout). Same firmware base, different trigger paths — plausibly converging on the same internal state.

**Symptom unchanged**: silent hard hang under sustained compute, zero kernel-side observability — no reset attempt, no fence anomaly, no SMU error, no MES activity. Reproduces identically on ROCm/HSA and Vulkan/RADV. amdgpu can sometimes notice and recover via per-ring reset on the Vulkan-visible variant (4 of 5 captured crashes); the silent class never invokes any reset path.

Suggestions for additional in-driver tracing welcome.


---

### 评论 #7 — aclater (2026-04-28T22:12:08Z)

I'm experiencing the same, have documented [here](https://gitlab.freedesktop.org/drm/amd/-/work_items?sort=created_date&state=opened&search=395&first_page_size=20&show=eyJpaWQiOiI1MTcxIiwiZnVsbF9wYXRoIjoiZHJtL2FtZCIsImlkIjoxNDk1ODl9) and [here](https://bugzilla.redhat.com/show_bug.cgi?id=2457514)

---

### 评论 #8 — Lafunamor (2026-04-29T20:21:35Z)

## Update — likely same bug being worked on at AMD freedesktop tracker

A separate issue on the AMD freedesktop tracker is collecting reports of the same SMU mailbox / PMFW 100.6.0 bug class on this hardware, reachable from multiple triggers (Chromium WebGL, browser VAAPI, and vLLM compute on `kyuz0/vllm-therock-gfx1151` — the same container we use here): https://gitlab.freedesktop.org/drm/amd/-/work_items/5171

Holding active investigation here pending that fix. Will re-test the compute / silent-hang case once the fix lands and report back if our variant persists.


---

### 评论 #9 — Lafunamor (2026-05-12T14:57:57Z)

For visibility — a fresh freedesktop drm/amd issue is now open for this specific case (compute-path silent hang, distinct from the VPE one on freedesktop #5171): https://gitlab.freedesktop.org/drm/amd/-/work_items/5289. Will keep both tickets in sync.

---
