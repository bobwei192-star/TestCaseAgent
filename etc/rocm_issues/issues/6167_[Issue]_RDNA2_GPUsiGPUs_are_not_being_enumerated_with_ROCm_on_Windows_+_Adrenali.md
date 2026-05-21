# [Issue]: RDNA2 GPUs/iGPUs are not being enumerated with ROCm on Windows + Adrenalin 26.3.1

> **Issue #6167**
> **状态**: open
> **创建时间**: 2026-04-21T05:56:11Z
> **更新时间**: 2026-04-23T18:54:05Z
> **作者**: enpinion
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6167

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

If system has only iGPU (gfx1036 - Raphael), clr/pal fails to enumerate iGPU. (Such as system with Non-AMD card installed or just with iGPU)

However, if any AMD dGPU installed (Tested with RX5500 - gfx1012 and R9700 - gfx1201) gfx1036 listed as an available device.

<details>
<summary>rocminfo without any dGPU</summary>

> pid:25152 tid:0x26356 [topology_sysfs_get_system_props] No WDDM adapters found.
> 
> pid:25152 tid:0x26356 [topology_sysfs_get_system_props] No WDDM adapters found.
> 
> checkHipErrors() HIP API error = 0100 "no ROCm-capable device is detected" from file <S:\gitroot\rocm\TheRock\rocm-systems\projects\hip-tests\samples\1_Utils\hipInfo\hipInfo.cpp>, line 181.

</details>

<details>
<summary>rocminfo with dGPU</summary>

> --------------------------------------------------------------------------------
> 
> device#                           0
> Name:                             AMD Radeon AI PRO R9700
> pciBusID:                         3
> pciDeviceID:                      0
> pciDomainID:                      0
> multiProcessorCount:              32
> maxThreadsPerMultiProcessor:      2048
> isMultiGpuBoard:                  0
> clockRate:                        2350 Mhz
> memoryClockRate:                  1259 Mhz
> memoryBusWidth:                   256
> totalGlobalMem:                   31.86 GB
> totalConstMem:                    2147483647
> sharedMemPerBlock:                64.00 KB
> canMapHostMemory:                 1
> regsPerBlock:                     196608
> warpSize:                         32
> l2CacheSize:                      8388608
> computeMode:                      0
> maxThreadsPerBlock:               1024
> maxThreadsDim.x:                  1024
> maxThreadsDim.y:                  1024
> maxThreadsDim.z:                  1024
> maxGridSize.x:                    2147483647
> maxGridSize.y:                    65536
> maxGridSize.z:                    65536
> major:                            12
> minor:                            0
> concurrentKernels:                1
> cooperativeLaunch:                0
> cooperativeMultiDeviceLaunch:     0
> isIntegrated:                     0
> maxTexture1D:                     16384
> maxTexture2D.width:               16384
> maxTexture2D.height:              16384
> maxTexture3D.width:               2048
> maxTexture3D.height:              2048
> maxTexture3D.depth:               2048
> hostNativeAtomicSupported:        1
> isLargeBar:                       0
> asicRevision:                     0
> maxSharedMemoryPerMultiProcessor: 64.00 KB
> clockInstructionRate:             1000.00 Mhz
> arch.hasGlobalInt32Atomics:       1
> arch.hasGlobalFloatAtomicExch:    1
> arch.hasSharedInt32Atomics:       1
> arch.hasSharedFloatAtomicExch:    1
> arch.hasFloatAtomicAdd:           1
> arch.hasGlobalInt64Atomics:       1
> arch.hasSharedInt64Atomics:       1
> arch.hasDoubles:                  1
> arch.hasWarpVote:                 1
> arch.hasWarpBallot:               1
> arch.hasWarpShuffle:              1
> arch.hasFunnelShift:              0
> arch.hasThreadFenceSystem:        1
> arch.hasSyncThreadsExt:           0
> arch.hasSurfaceFuncs:             0
> arch.has3dGrid:                   1
> arch.hasDynamicParallelism:       0
> gcnArchName:                      gfx1201
> maxAvailableVgprsPerThread:       256 DWORDs
> peers:
> non-peers:                        device#0 device#1
> 
> memInfo.total:                    31.86 GB
> memInfo.free:                     31.71 GB (100%)
> --------------------------------------------------------------------------------
> device#                           1
> Name:                             AMD Radeon(TM) Graphics
> pciBusID:                         121
> pciDeviceID:                      0
> pciDomainID:                      0
> multiProcessorCount:              1
> maxThreadsPerMultiProcessor:      2048
> isMultiGpuBoard:                  0
> clockRate:                        2200 Mhz
> memoryClockRate:                  1750 Mhz
> memoryBusWidth:                   128
> totalGlobalMem:                   49.09 GB
> totalConstMem:                    2147483647
> sharedMemPerBlock:                64.00 KB
> canMapHostMemory:                 1
> regsPerBlock:                     131072
> warpSize:                         32
> l2CacheSize:                      4194304
> computeMode:                      0
> maxThreadsPerBlock:               1024
> maxThreadsDim.x:                  1024
> maxThreadsDim.y:                  1024
> maxThreadsDim.z:                  1024
> maxGridSize.x:                    2147483647
> maxGridSize.y:                    65536
> maxGridSize.z:                    65536
> major:                            10
> minor:                            3
> concurrentKernels:                1
> cooperativeLaunch:                0
> cooperativeMultiDeviceLaunch:     0
> isIntegrated:                     1
> maxTexture1D:                     16384
> maxTexture2D.width:               16384
> maxTexture2D.height:              16384
> maxTexture3D.width:               2048
> maxTexture3D.height:              2048
> maxTexture3D.depth:               2048
> hostNativeAtomicSupported:        0
> isLargeBar:                       0
> asicRevision:                     0
> maxSharedMemoryPerMultiProcessor: 64.00 KB
> clockInstructionRate:             1000.00 Mhz
> arch.hasGlobalInt32Atomics:       1
> arch.hasGlobalFloatAtomicExch:    1
> arch.hasSharedInt32Atomics:       1
> arch.hasSharedFloatAtomicExch:    1
> arch.hasFloatAtomicAdd:           1
> arch.hasGlobalInt64Atomics:       1
> arch.hasSharedInt64Atomics:       1
> arch.hasDoubles:                  1
> arch.hasWarpVote:                 1
> arch.hasWarpBallot:               1
> arch.hasWarpShuffle:              1
> arch.hasFunnelShift:              0
> arch.hasThreadFenceSystem:        1
> arch.hasSyncThreadsExt:           0
> arch.hasSurfaceFuncs:             0
> arch.has3dGrid:                   1
> arch.hasDynamicParallelism:       0
> gcnArchName:                      gfx1036
> maxAvailableVgprsPerThread:       256 DWORDs
> peers:
> non-peers:                        device#0 device#1
> 
> memInfo.total:                    49.09 GB
> memInfo.free:                     48.95 GB (100%)

</details>
 #5871 


### Operating System

Windows 11 25H2 (26200.8246)

### CPU

AMD Ryzen 9 9950X3D 16-Core Processor

### GPU

AMD Radeon(TM) Graphics (gfx1036)

### ROCm Version

7.12

### ROCm Component

clr

### Steps to Reproduce

1. Remove any AMD dGPUs.
2. Boot with iGPU (or with Non-AMD GPU)
3. Run hipinfo.exe
4. "checkHipErrors() HIP API error = 0100 "no ROCm-capable device is detected"

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Tested with both the official HIP SDK, theRock latest build from source, remove any related environment variables etc.

---

## 评论 (2 条)

### 评论 #1 — CarlGao4 (2026-04-22T09:00:14Z)

Are you using TheRock builds? 103X-iGPU is not supported yet. You should wait for TheRock 7.13 release

---

### 评论 #2 — schung-amd (2026-04-23T18:52:31Z)

Thanks for the report. As mentioned we don't have ROCm support yet for that device, but it might still be useful to show info about it  as even without a dGPU installed as it can be used in other contexts. 

I suspect this is fixed by https://github.com/ROCm/rocm-systems/pull/5119, which just landed in TheRock mainline and should be available in today's nightlies; it's a fix for a similar issue on Strix Halo but I think it extends to this scenario. You can test this yourself, or I'll see if I can get a Windows + iGPU + dGPU system to verify.

---
