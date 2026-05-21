# [Bug]: RX 9070 XT (gfx1200) - rocminfo/ollama hang or killed during HSA discovery on ROCm 7.1.1

> **Issue #5812**
> **状态**: closed
> **创建时间**: 2025-12-24T19:23:41Z
> **更新时间**: 2026-01-13T15:45:39Z
> **关闭时间**: 2026-01-13T15:45:39Z
> **作者**: TigerAI-TW
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5812

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

md-smi
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.0+021c61fc      amdgpu version: 6.16.6   ROCm version: 7.1.1    |
| VBIOS version: 00131162                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:04:00.0  AMD Radeon RX 9070 XT | 0 %      41 °C   0            16/304 W |
|   0       0     N/A             N/A | 0 %      0.0 %             84/16304 MB |
|-------------------------------------+----------------------------------------|
| 0000:07:00.0  AMD Radeon RX 9070 XT | 0 %      40 °C   0            17/304 W |
|   1       1     N/A             N/A | 3 %      0.0 %            347/16304 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|    0       5300  N/A                     0.0 B     0.0 B      0.0 B  N/A     |
|    1       5300  N/A                     0.0 B     0.0 B      0.0 B  N/A     |
+------------------------------------------------------------------------------+

Bash HSA_ENABLE_SDMA=0 rocminfo
killed

## AI Tell
Issue Description:
System Environment:

GPU: Dual AMD Radeon RX 9070 XT (RDNA 4 / gfx1200)

OS: Ubuntu 24.04 (or your specific version)

Kernel: 6.16.6-amdgpu

ROCm Version: 7.1.1

Driver Version: 26.2.0 (amdgpu 6.16.6)

Ollama Version: 0.13.5 (ROCm variant)

Steps to Reproduce:

Install ROCm 7.1.1 and latest amdgpu drivers for RDNA 4 support.

Verify hardware visibility via amd-smi (Success: both GPUs detected).

Attempt to run rocminfo or start ollama serve.

Observe the process behavior.

Actual Behavior:

Standard execution: rocminfo and ollama hang indefinitely during GPU discovery (likely a deadlock in HSA queue initialization).

With HSA_ENABLE_SDMA=0: rocminfo is immediately Killed by the OS after loading the ROCk module.

Log snippet from Ollama: failure during GPU discovery error="failed to finish discovery before timeout".

Expected Behavior: ROCm runtime should correctly initialize HSA agents and queues for gfx1200/gfx1201 architecture without deadlocking or triggering kernel kills.

Additional Context: amd-smi output shows the cards are functional and recognized as "AMD Radeon RX 9070 XT". The issue seems isolated to the HSA/HIP runtime layer when interacting with RDNA 4 hardware.



### Operating System

Ubuntu 24.04.3

### CPU

Xeon 2680v4

### GPU

Daul RX 9070 XT (RDNA 4 / gfx1200)

### ROCm Version

ROCm Version: 7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — schung-amd (2025-12-29T21:39:16Z)

Hi @TigerAI-TW, I'll try to repro this, but...

> Kernel: 6.16.6-amdgpu

We don't have support for this kernel yet (see https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-distributions), which might be related to the issue you're seeing.

---

### 评论 #2 — schung-amd (2025-12-30T20:00:40Z)

Not seeing a rocminfo hang locally. My test system only has a single 9070XT at the moment; I don't think dual GPU would affect anything here as we haven't seen rocminfo hangs in other dual GPU systems, but I'll try it anyway once I have access to another card. My `amd-smi` output is
```
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.0+021c61fc      amdgpu version: 6.16.6-061606 ROCm version: 7.1.1    |
| VBIOS version: 023.008.000.068.000001                                        |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:03:00.0  AMD Radeon RX 9070 XT | 0 %      36 °C   0            19/330 W |
|   0       0     N/A             N/A | 94 %     0.0 %            789/16304 MB |
+-------------------------------------+----------------------------------------+
```

---

### 评论 #3 — schung-amd (2026-01-13T15:45:39Z)

Closing for now as I have not been able to reproduce this. Please try a supported kernel version and see if that helps with this issue. Feel free to continue commenting here and we can reopen this if necessary.

---
