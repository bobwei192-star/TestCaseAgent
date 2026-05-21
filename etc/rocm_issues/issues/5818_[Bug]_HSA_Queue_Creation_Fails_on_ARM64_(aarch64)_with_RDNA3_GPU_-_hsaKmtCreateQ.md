# [Bug]: HSA Queue Creation Fails on ARM64 (aarch64) with RDNA3 GPU - hsaKmtCreateQueue

> **Issue #5818**
> **状态**: closed
> **创建时间**: 2025-12-29T05:00:08Z
> **更新时间**: 2026-02-19T18:12:27Z
> **关闭时间**: 2026-02-19T18:12:27Z
> **作者**: atayozcan
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5818

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

# [Bug]: HSA Queue Creation Fails on ARM64 (aarch64) with RDNA3 GPU - "Queue create failed at hsaKmtCreateQueue"

## Environment

- **OS:** Ubuntu 25.10 (Questing Quokka)
- **Kernel:** 6.17.0-8-generic aarch64
- **CPU:** ARM Cortex-X4/A720 (Radxa Orion O6 - Rockchip RK3588)
- **GPU:** AMD Radeon RX 7600M XT (gfx1102 / Navi 33)
- **ROCm/HIP:** Built from source (HIP 6.1.2, CLR 6.1.2)
- **PCIe:** x16 slot via PCIe switch

## Problem Description

HIP kernel execution fails with "HSA exception: Queue create failed at hsaKmtCreateQueue" on ARM64 (aarch64) platform with AMD RDNA3 GPU.

The KFD driver loads successfully, GPU is detected, memory allocation works, but compute queue creation fails at kernel launch time.

## Steps to Reproduce

1. Build HIP 6.1.2 from source on aarch64 (requires patching `hip_embed_pch.sh` to use aarch64 aux-triple)
2. Compile simple HIP test program targeting gfx1100:
```cpp
#include <hip/hip_runtime.h>
#include <stdio.h>

__global__ void simpleKernel(int *data) {
    data[threadIdx.x] = threadIdx.x;
}

int main() {
    int *d_data;
    hipMalloc(&d_data, 64);
    simpleKernel<<<1, 16>>>(d_data);  // Fails here
    hipDeviceSynchronize();
    hipFree(d_data);
    return 0;
}
```
3. Run with: `HSA_OVERRIDE_GFX_VERSION=11.0.0 ./hip_test`

## Expected Behavior

Kernel should execute on GPU.

## Actual Behavior

```
Step 1: Getting device count...
Found 1 devices
Step 2: Setting device 0...
Device 0 set
Step 3: Allocating device memory (64 bytes)...
Memory allocated at 0x4100c00000
Step 4: Launching kernel...
HSA exception: Queue create failed at hsaKmtCreateQueue
Step 5: Synchronizing...
Kernel completed!
```

The error `hipErrorSharedObjectInitFailed` is returned from `hipLaunchKernel`.

## What Works

- `rocminfo` correctly detects GPU (gfx1102, AMD Radeon RX 7600M XT)
- `hipGetDeviceCount()` returns 1
- `hipSetDevice(0)` succeeds
- `hipMalloc()` succeeds - GPU memory allocation works
- KFD driver loads: `kfd kfd: amdgpu: added device 1002:7480`

## What Fails

- `hsaKmtCreateQueue` - compute queue creation in KFD
- Any actual GPU kernel execution

## Additional Context

### Without HSA_OVERRIDE_GFX_VERSION
Without the gfx version override, the system hard-crashes (complete lockup requiring power cycle). With `HSA_OVERRIDE_GFX_VERSION=11.0.0`, it fails gracefully with the queue error.

### Kernel IOMMU Configuration
Initially saw ARM SMMU faults:
```
arm-smmu-v3: unpriv data write s1 "Input address caused fault"
```
Fixed by adding `iommu.passthrough=1` kernel parameter. Queue creation still fails after this fix.

### Debug Output (AMD_LOG_LEVEL=4)
```
:3:rocdevice.cpp :1680: Gfx Major/Minor/Stepping: 11/0/0
:3:rocdevice.cpp :1682: HMM support: 1, XNACK: 0, Direct host access: 0
:4:rocdevice.cpp :2191: Allocate hsa device memory 0x4100c00000, size 0x40
:3:devprogram.cpp :2681: Using Code Object V4.
HSA exception: Queue create failed at hsaKmtCreateQueue
:3:hip_module.cpp :679: hipLaunchKernel: Returned hipErrorSharedObjectInitFailed
```

## Analysis

The failure occurs in `hsaKmtCreateQueue` which is in the ROCT-Thunk-Interface layer, calling into the KFD kernel driver. The KFD driver was patched to compile on ARM64 but queue creation logic may have x86-specific assumptions or missing ARM64 implementation.

## Related Issues

- #3960 - ROCm support on arm64 (closed, acknowledged but not planned short-term)
- #4405 - How to compile the rocm version of aarch64 (closed, AMD confirmed no current support)

## Request

Even if full ARM64 support isn't planned until the Fujitsu partnership (~2027), this specific technical finding about queue creation failure could help:
1. Document the current limitation precisely
2. Guide future ARM64 porting efforts
3. Help community members attempting similar setups

The infrastructure (KFD loading, device detection, memory allocation) works - the specific blocker is queue creation in ROCT/KFD.


---

## 评论 (1 条)

### 评论 #1 — darren-amd (2026-02-19T18:12:15Z)

Hi @atayozcan,

Thanks for the request. I don't currently have any additional information on timelines, but I will convert this to a discussion where community members are welcome to collaborate.

---
