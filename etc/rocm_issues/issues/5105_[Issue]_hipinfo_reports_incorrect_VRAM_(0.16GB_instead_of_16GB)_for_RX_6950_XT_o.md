# [Issue]: hipinfo reports incorrect VRAM (0.16GB instead of 16GB) for RX 6950 XT on Windows 11 with HIP SDK 6.2

> **Issue #5105**
> **状态**: closed
> **创建时间**: 2025-07-26T16:47:58Z
> **更新时间**: 2025-12-09T21:26:17Z
> **关闭时间**: 2025-12-09T21:08:24Z
> **作者**: iso3789
> **标签**: Windows, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5105

## 标签

- **Windows** (颜色: #c2e0c6)
- **status: triage** (颜色: #585dd7)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

When running hipinfo.exe on my Windows 11 system with an AMD Radeon RX 6950 XT GPU, the reported totalGlobalMem (VRAM) is incorrect. Instead of displaying the actual 16 GB of VRAM, it consistently shows 0.16 GB.

Other crucial hardware details are also misreported, such as memoryBusWidth being shown as 0.

Steps to Reproduce

    Hardware: AMD Radeon RX 6950 XT (RDNA2 / gfx1030 architecture).

    Operating System: Windows 11.

    Graphics Driver: Latest official AMD Adrenalin drivers installed and up-to-date.

    HIP SDK: AMD Software: PRO Edition 24.Q4 for HIP (tested with both versions 6.1 and 6.2, installed natively on Windows).

After installing the HIP SDK, navigate to the bin directory (e.g., C:\AMD\ROCm\6.2\bin) and execute hipinfo.exe.

Expected Behavior

hipinfo.exe should accurately report the totalGlobalMem as 16 GB (or approximately 16384 MB) for the AMD Radeon RX 6950 XT. The memoryBusWidth should also reflect the correct value (e.g., 256).

Actual Behavior (Console Output from hipinfo.exe)

PS C:\AMD\ROCm\6.2\bin> hipinfo.exe

--------------------------------------------------------------------------------
device#                               0
Name:                                 AMD Radeon RX 6950 XT
pciBusID:                             16
pciDeviceID:                          0
pciDomainID:                          0
multiProcessorCount:                  40
maxThreadsPerMultiProcessor:          2048
isMultiGpuBoard:                      0
clockRate:                            2162 Mhz
memoryClockRate:                      1125 Mhz
memoryBusWidth:                       0
totalGlobalMem:                       0.16 GB
totalConstMem:                        171630919
sharedMemPerBlock:                    64.00 KB
canMapHostMemory:                     1
regsPerBlock:                         0
warpSize:                             32
l2CacheSize:                          4194304
computeMode:                          0
maxThreadsPerBlock:                   1024
maxThreadsDim.x:                      1024
maxThreadsDim.y:                      1024
maxThreadsDim.z:                      1024
maxGridSize.x:                        2147483647
maxGridSize.y:                        65536
maxGridSize.z:                        65536
major:                                10
minor:                                3
concurrentKernels:                    1
cooperativeLaunch:                    0
cooperativeMultiDeviceLaunch:         0
isIntegrated:                         0
maxTexture1D:                         16384
maxTexture2D.width:                   16384
maxTexture2D.height:                  16384
maxTexture3D.width:                   2048
maxTexture3D.height:                  2048
maxTexture3D.depth:                   2048
hostNativeAtomicSupported:            1
isLargeBar:                           0
asicRevision:                         0
maxSharedMemoryPerMultiProcessor:     64.00 KB
clockInstructionRate:                 1000.00 Mhz
arch.hasGlobalInt32Atomics:           1
arch.hasGlobalFloatAtomicExch:        1
arch.hasSharedInt32Atomics:           1
arch.hasSharedFloatAtomicExch:        1
arch.hasFloatAtomicAdd:               1
arch.hasGlobalInt64Atomics:           1
arch.hasSharedInt64Atomics:           1
arch.hasDoubles:                      1
arch.hasWarpVote:                     1
arch.hasWarpBallot:                   1
arch.hasWarpShuffle:                  1
arch.hasFunnelShift:                  0
arch.hasThreadFenceSystem:            1
arch.hasSyncThreadsExt:               0
arch.hasSurfaceFuncs:                 0
arch.has3dGrid:                       1
arch.hasDynamicParallelism:           0
gcnArchName:                          gfx1030
peers:
non-peers:                            device#0

memInfo.total:                        0.16 GB
memInfo.free:                         0.02 GB (14%)

Additional Information

    Other system tools, such as AMD Software: Adrenalin Edition and DirectX Diagnostic Tool (dxdiag), correctly report the VRAM for the Radeon RX 6950 XT as 16368 MB GDDR6. This indicates that the operating system and underlying graphics drivers recognize the hardware correctly, and the issue appears to be specific to how the HIP SDK queries or interprets this information.

    I have performed clean installations of both HIP SDK versions (6.1 and 6.2), ensuring all previous components were removed, but the error persists.

    No relevant environment variables (e.g., HIP_VISIBLE_DEVICES, HSA_OVERRIDE_GFX_VERSION) are set that would interfere with device detection.

### Operating System

Win 11 Pro 24H2

### CPU

AMD Ryzen 9 3900X 12-Core Processor (3.80 GHz)

### GPU

AMD Radeon RX 6950 XT

### ROCm Version

6.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-07-28T13:21:29Z)

Hi @iso3789. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — lucbruni-amd (2025-11-27T18:47:09Z)

Hi @iso3789, is this still an issue with the latest ROCm stack?

---

### 评论 #3 — lucbruni-amd (2025-12-09T21:08:17Z)

Closing this issue due to inactivity as this is on an older ROCm stack. Feel free to reopen this issue or open a new one if this persists. Thanks!

---

### 评论 #4 — iso3789 (2025-12-09T21:24:29Z)

Hi Luca,

I was checking it last time again and it was working, thanks!

Best regards,
Ivan

Sent from [Proton Mail](https://proton.me/mail/home) for Android.

-------- Original Message --------
On Tuesday, 12/09/25 at 22:08 Luca Bruni ***@***.***> wrote:

> Closed [#5105](https://github.com/ROCm/ROCm/issues/5105) as completed.
>
> —
> Reply to this email directly, [view it on GitHub](https://github.com/ROCm/ROCm/issues/5105#event-21464005365), or [unsubscribe](https://github.com/notifications/unsubscribe-auth/AVUMOSCT7QH3QYJZKDWUIS34A4253AVCNFSM6AAAAACCNYLVOKVHI2DSMVQWIX3LMV45UABCJFZXG5LFIV3GK3TUJZXXI2LGNFRWC5DJN5XDWMRRGQ3DIMBQGUZTMNI).
> You are receiving this because you were mentioned.Message ID: ***@***.***>

---

### 评论 #5 — lucbruni-amd (2025-12-09T21:26:17Z)

That's great news. Thanks for opening issues with us - we appreciate your effort to help us find and solve them. Please don't hesitate to open further issues around the ROCm repositories if you find any!

---
