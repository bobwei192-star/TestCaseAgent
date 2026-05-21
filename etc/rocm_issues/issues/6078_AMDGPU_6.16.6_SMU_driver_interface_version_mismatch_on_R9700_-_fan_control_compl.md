# AMDGPU 6.16.6 SMU driver interface version mismatch on R9700 - fan control completely broken on Linux

> **Issue #6078**
> **状态**: closed
> **创建时间**: 2026-03-29T15:41:14Z
> **更新时间**: 2026-04-02T06:43:26Z
> **关闭时间**: 2026-04-02T06:43:25Z
> **作者**: lobsteroh
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6078

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

**Hardware:** ASUS Turbo Radeon AI Pro R9700 32GB (brand new)
**vBIOS:** 115-G287BP00-100
**OS:** Ubuntu 24.04
**Kernel:** 6.17.0-19
**ROCm:** 6.4
**AMDGPU driver:** 6.16.6

## Issue

The GPU fan does not spin under any load on Linux. During AI training the GPU reached 109°C and thermally throttled with the fan physically stationary throughout.

## SMU Firmware Mismatch (root cause)

From dmesg:
```
amdgpu 0000:2d:00.0: amdgpu: smu driver if version = 0x0000002e (46)
amdgpu 0000:2d:00.0: amdgpu: smu fw if version  = 0x00000032 (50)
amdgpu 0000:2d:00.0: amdgpu: smu fw version = 0x00684b00 (104.75.0)
amdgpu 0000:2d:00.0: amdgpu: SMU driver if version not matched
```

The card firmware is 4 interface versions ahead of what AMDGPU driver 6.16.6 supports. Driver expects SMU interface version 46, card reports version 50. This mismatch results in fan control registers being inaccessible.

## Technical Findings

- `rocm-smi --setfan` returns 'Not supported on this system'
- sysfs `pwm1` node is READ-ONLY (-r--r--r--) — fan speed cannot be written
- `fan1_enable` returns 'Invalid argument' when read
- GPU enters runtime power suspend during load, suppressing fan control
- Waking GPU with `echo on > power/control` allows fan1_input to be read (returns 12 RPM) but fan is physically stationary
- GPU reached 109°C and thermally throttled during AI training with fan stationary throughout

## Request

The AMDGPU driver needs to be updated to support SMU interface version 50 (0x00000032) as shipped on the R9700. Until this is resolved, fan control is completely non-functional on Linux and the card is unsafe for sustained AI/ML workloads — which is the primary use case for this card.

---

## 评论 (4 条)

### 评论 #1 — lobsteroh (2026-03-29T15:55:36Z)

UPDATE: Tested on ROCm 7.2.1 / AMDGPU 6.16.13 (released 2026-03-25).
SMU mismatch persists unchanged:

smu driver if version = 0x0000002e (46)
smu fw if version  = 0x00000032 (50)
amdgpu: SMU driver if version not matched

fan1_input still returns 'Device or resource busy' until GPU 
is manually woken from runtime suspend. pwm1 remains read-only.
Fan control is broken across both AMDGPU 6.16.6 and 6.16.13.
Driver update to support SMU interface version 50 is required.

Fan does not spin up automatically under load. GPU reached 109°C 
and thermally throttled during AI training with fan physically 
stationary throughout. Issue confirmed across both AMDGPU 6.16.6 
and 6.16.13. The SMU interface mismatch is preventing the driver 
from issuing fan control commands in response to thermal demand.
Driver update to support SMU interface version 50 is required.

---

### 评论 #2 — Mikeysax (2026-04-01T02:51:42Z)

My R9700 stays at 30% fan speed:


<img width="1008" height="644" alt="Image" src="https://github.com/user-attachments/assets/a147838c-1f58-4817-af07-526a0d629aaf" />


<img width="809" height="166" alt="Image" src="https://github.com/user-attachments/assets/914893c0-ff5e-44b7-a326-cde953583d53" />


```
========================================== ROCm System Management Interface ==========================================
==================================================== Concise Info ====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK     MCLK     Fan    Perf  PwrCap  VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)
======================================================================================================================
0       1     0x7551,   35461  41.0°C  44.0W  N/A, N/A, 0         1153Mhz  1258Mhz  29.8%  auto  210.0W  8%     9%
======================================================================================================================
================================================ End of ROCm SMI Log =================================================
```

```
+------------------------------------------------------------------------------+
| AMD-SMI 26.2.2+e1a6bc5663    amdgpu version: 6.18.7-76061807 ROCm version: 7.2.1    |
| VBIOS version: 00158744                                                      |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:0c:00.0    AMD Radeon Graphics | 0 %      42 °C   0            45/210 W |
|   0       0     N/A             N/A | 6 %     29.8 %           2732/32624 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```

---

### 评论 #3 — amd-nicknick (2026-04-02T04:21:24Z)

Hi @lobsteroh, the SMU if version does not need to exactly match between driver and the firmware for the card to function, this message is usually harmless. 
Could you please try purging out the amdgpu driver package (including the amdgpu-firmware) package, then perform a reinstall? I think there is residue firmware files being used here. The card contains a default fan curve and that will be used.

---

### 评论 #4 — amd-nicknick (2026-04-02T06:43:26Z)

Hi @lobsteroh, let' track this on the other issue you've opened #6101.
If I misunderstood and this is separate issue, please let me know & reopen this one. Thanks!

---
