# [Issue]: Wrong memoryBusWidth is reported on Windows.

> **Issue #4514**
> **状态**: closed
> **创建时间**: 2025-03-19T13:16:02Z
> **更新时间**: 2025-05-02T18:51:14Z
> **关闭时间**: 2025-04-29T16:47:15Z
> **作者**: lshqqytiger
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4514

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I'm getting `memoryBusWidth=0` when I run `hipinfo.exe` in Windows.
I can get the same result from `hipGetDeviceProperties`.

```
device#                           0
Name:                             AMD Radeon RX 7900 XTX
pciBusID:                         3
pciDeviceID:                      0
pciDomainID:                      0
multiProcessorCount:              48
maxThreadsPerMultiProcessor:      2048
isMultiGpuBoard:                  0
clockRate:                        2526 Mhz
memoryClockRate:                  1250 Mhz
memoryBusWidth:                   0
totalGlobalMem:                   23.98 GB
totalConstMem:                    2147483647
sharedMemPerBlock:                64.00 KB
canMapHostMemory:                 1
regsPerBlock:                     0
warpSize:                         32
l2CacheSize:                      4194304
computeMode:                      0
maxThreadsPerBlock:               1024
maxThreadsDim.x:                  1024
maxThreadsDim.y:                  1024
maxThreadsDim.z:                  1024
maxGridSize.x:                    2147483647
maxGridSize.y:                    65536
maxGridSize.z:                    65536
major:                            11
minor:                            0
concurrentKernels:                1
cooperativeLaunch:                0
cooperativeMultiDeviceLaunch:     0
isIntegrated:                     0
maxTexture1D:                     16384
maxTexture2D.width:               16384
maxTexture2D.height:              16384
maxTexture3D.width:               2048
maxTexture3D.height:              2048
maxTexture3D.depth:               2048
hostNativeAtomicSupported:        1
isLargeBar:                       0
asicRevision:                     0
maxSharedMemoryPerMultiProcessor: 64.00 KB
clockInstructionRate:             1000.00 Mhz
arch.hasGlobalInt32Atomics:       1
arch.hasGlobalFloatAtomicExch:    1
arch.hasSharedInt32Atomics:       1
arch.hasSharedFloatAtomicExch:    1
arch.hasFloatAtomicAdd:           1
arch.hasGlobalInt64Atomics:       1
arch.hasSharedInt64Atomics:       1
arch.hasDoubles:                  1
arch.hasWarpVote:                 1
arch.hasWarpBallot:               1
arch.hasWarpShuffle:              1
arch.hasFunnelShift:              0
arch.hasThreadFenceSystem:        1
arch.hasSyncThreadsExt:           0
arch.hasSurfaceFuncs:             0
arch.has3dGrid:                   1
arch.hasDynamicParallelism:       0
gcnArchName:                      gfx1100
peers:
non-peers:                        device#0
```

It is reported as `384` which is expected in Ubuntu.

### Operating System

Windows 11 (10.0.26100)

### CPU

Intel(R) Core(TM) i9-14900K

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

HIP SDK 6.2.41512-db3292736

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-03-19T13:57:21Z)

Hi @lshqqytiger. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-04-29T16:47:15Z)

Hi @lshqqytiger, thanks for reporting this! We've addressed this internally and it should be fixed in an upcoming release. I'll update if I get more specific information on when this will land. Feel free to comment if you need further guidance on this and we can reopen if necessary. 

---

### 评论 #3 — lshqqytiger (2025-05-02T18:35:58Z)

Good to hear! Thanks.
I found that `hipDeviceAttributeMaxRegistersPerBlock` is also `0` in HIP SDK 6.2 on Windows while it is `65536` on Linux.
Will this issue be fixed in the upcoming release?

---

### 评论 #4 — schung-amd (2025-05-02T18:51:12Z)

Yes, the max registers per block output should also be corrected by the same fix.

---
