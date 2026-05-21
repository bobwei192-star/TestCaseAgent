# [Issue]: HSA_AMD_AGENT_INFO_SCRATCH_LIMIT_MAX cannot be queried! no ROCm-capable device is detected.

> **Issue #5924**
> **状态**: closed
> **创建时间**: 2026-02-02T19:08:35Z
> **更新时间**: 2026-02-03T20:22:10Z
> **关闭时间**: 2026-02-03T20:22:10Z
> **作者**: alexschroeter
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5924

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

GPUs are detected in rocm-smi and rocminfo but don't show up in the simplest of code examples.

```
rocm-smi


WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK     MCLK     Fan     Perf    PwrCap  VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)
==========================================================================================================================
0       2     0x740f,   1997   49.0°C  57.0W  N/A, N/A, 0         1700Mhz  1600Mhz  0%      high    300.0W  0%     0%
1       4     0x738c,   45163  39.0°C  54.0W  N/A, N/A, 0         1502Mhz  1200Mhz  0%      manual  290.0W  0%     0%
2       3     0x66a1,   51636  33.0°C  21.0W  N/A, N/A, 0         925Mhz   1000Mhz  14.51%  manual  225.0W  0%     0%
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================

```

### Operating System

Alma 9.7

### CPU

AMD EPYC 7452 32-Core Processor

### GPU

MI50,MI100,MI210

### ROCm Version

7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

```
#include <hip/hip_runtime.h>
#include <stdio.h>
int main() {
    int count = 0;
    hipError_t err = hipGetDeviceCount(&count);
    printf("hipGetDeviceCount returned: %d (error: %s)\n", count, hipGetErrorString(err));
    for (int i = 0; i < count; i++) {
        hipDeviceProp_t prop;
        hipGetDeviceProperties(&prop, i);
        printf("Device %d: %s\n", i, prop.name);
    }
    return 0;
}
```

`hipcc -O2 --offload-arch=gfx90a --offload-arch=gfx906 --offload-arch=gfx908 -o test_hip test_hip.cpp`

```
AMD_LOG_LEVEL=4 ./test_hip
:3:rocdevice.cpp            :415 : 11623516219 us: [pid:307076 tid: 0x7f195a24d400] Initalizing runtime stack, Enumerated GPU agents = 3
:3:rocdevice.cpp            :182 : 11623516276 us: [pid:307076 tid: 0x7f195a24d400] Numa selects cpu agent[0]=0x36bcd0(fine=0x36bec0,coarse=0x36c730) for gpu agent=0x3a91c0 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :269 : 11623516286 us: [pid:307076 tid: 0x7f195a24d400] Using dev kernel arg wa = 0
:3:comgrctx.cpp             :126 : 11623516320 us: [pid:307076 tid: 0x7f195a24d400] Loaded COMGR library version 3.0.
:2:rocdevice.cpp            :1076: 11623516337 us: [pid:307076 tid: 0x7f195a24d400] HSA_AMD_AGENT_INFO_SCRATCH_LIMIT_MAX cannot be queried!
:1:rocdevice.cpp            :655 : 11623516343 us: [pid:307076 tid: 0x7f195a24d400] populateOCLDeviceConstants failed for HSA device gfx90a (PCI ID 740f)
:1:rocdevice.cpp            :425 : 11623516348 us: [pid:307076 tid: 0x7f195a24d400] Error creating new instance of Device.
:3:rocdevice.cpp            :182 : 11623516368 us: [pid:307076 tid: 0x7f195a24d400] Numa selects cpu agent[1]=0x36a000(fine=0x36a1f0,coarse=0x36ad80) for gpu agent=0x3b26e0 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :269 : 11623516374 us: [pid:307076 tid: 0x7f195a24d400] Using dev kernel arg wa = 0
:2:rocdevice.cpp            :1076: 11623516381 us: [pid:307076 tid: 0x7f195a24d400] HSA_AMD_AGENT_INFO_SCRATCH_LIMIT_MAX cannot be queried!
:1:rocdevice.cpp            :655 : 11623516386 us: [pid:307076 tid: 0x7f195a24d400] populateOCLDeviceConstants failed for HSA device gfx906 (PCI ID 66a1)
:1:rocdevice.cpp            :425 : 11623516391 us: [pid:307076 tid: 0x7f195a24d400] Error creating new instance of Device.
:3:rocdevice.cpp            :182 : 11623516404 us: [pid:307076 tid: 0x7f195a24d400] Numa selects cpu agent[1]=0x36a000(fine=0x36a1f0,coarse=0x36ad80) for gpu agent=0x3b5bc0 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :269 : 11623516412 us: [pid:307076 tid: 0x7f195a24d400] Using dev kernel arg wa = 0
:2:rocdevice.cpp            :1076: 11623516421 us: [pid:307076 tid: 0x7f195a24d400] HSA_AMD_AGENT_INFO_SCRATCH_LIMIT_MAX cannot be queried!
:1:rocdevice.cpp            :655 : 11623516425 us: [pid:307076 tid: 0x7f195a24d400] populateOCLDeviceConstants failed for HSA device gfx908 (PCI ID 738c)
:1:rocdevice.cpp            :425 : 11623516433 us: [pid:307076 tid: 0x7f195a24d400] Error creating new instance of Device.
:3:hip_context.cpp          :60  : 11623516440 us: [pid:307076 tid: 0x7f195a24d400] HIP Version: 7.2.26015.fc0010cf6a, Direct Dispatch: 1
:3:os_posix.cpp             :934 : 11623516452 us: [pid:307076 tid: 0x7f195a24d400] HIP Library Path: /opt/rocm-7.2.0/lib/libamdhip64.so.7
:3:hip_device_runtime.cpp   :706 : 11623516477 us: [pid:307076 tid: 0x7f195a24d400]  hipGetDeviceCount ( 0x7fff77af23e4 )
:3:hip_device_runtime.cpp   :708 : 11623516487 us: [pid:307076 tid: 0x7f195a24d400] hipGetDeviceCount: Returned hipErrorNoDevice :
hipGetDeviceCount returned: 0 (error: no ROCm-capable device is detected)
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
/opt/rocm/bin/rocminfo --support
ROCk module version 6.16.13 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD EPYC 7452 32-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7452 32-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2350
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            64
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    263445064(0xfb3da48) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    263445064(0xfb3da48) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    263445064(0xfb3da48) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    263445064(0xfb3da48) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    AMD EPYC 7452 32-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7452 32-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2350
  BDFID:                   0
  Internal Node ID:        1
  Compute Unit:            64
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    264218192(0xfbfa650) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    264218192(0xfbfa650) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    264218192(0xfbfa650) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    264218192(0xfbfa650) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 3
*******
  Name:                    gfx90a
  Uuid:                    GPU-1bb9a9bbe9c86e9e
  Marketing Name:          AMD Instinct MI210
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    2
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 29711(0x740f)
  ASIC Revision:           1(0x1)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   1700
  BDFID:                   25344
  Internal Node ID:        2
  Compute Unit:            104
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    2048(0x800)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 100
  SDMA engine uCode::      9
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 4
*******
  Name:                    gfx906
  Uuid:                    GPU-3cc2512173497dfb
  Marketing Name:          AMD Instinct MI60 / MI50
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    3
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 26273(0x66a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1725
  BDFID:                   58112
  Internal Node ID:        3
  Compute Unit:            60
  SIMDs per CU:            4
  Shader Engines:          4
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        40(0x28)
  Max Work-item Per CU:    2560(0xa00)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 481
  SDMA engine uCode::      145
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 5
*******
  Name:                    gfx908
  Uuid:                    GPU-0eef0648d5e4e209
  Marketing Name:          AMD Instinct MI100
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    4
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 29580(0x738c)
  ASIC Revision:           2(0x2)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1502
  BDFID:                   33536
  Internal Node ID:        4
  Compute Unit:            120
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        40(0x28)
  Max Work-item Per CU:    2560(0xa00)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 71
  SDMA engine uCode::      18
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***
```

### Additional Information

```
NAME="AlmaLinux"
VERSION="9.7 (Moss Jungle Cat)"
CPU:
model name      : AMD EPYC 7452 32-Core Processor
GPU:
  Name:                    AMD EPYC 7452 32-Core Processor
  Marketing Name:          AMD EPYC 7452 32-Core Processor
  Name:                    AMD EPYC 7452 32-Core Processor
  Marketing Name:          AMD EPYC 7452 32-Core Processor
  Name:                    gfx90a
  Marketing Name:          AMD Instinct MI210
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx906
  Marketing Name:          AMD Instinct MI60 / MI50
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
  Name:                    gfx908
  Marketing Name:          AMD Instinct MI100
      Name:                    amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-
```

---

## 评论 (2 条)

### 评论 #1 — tcgu-amd (2026-02-03T19:45:48Z)

Hi @alexschroeter, thanks for reaching out! Just wanted to confirm, how did you install and set up ROCm on your system? 

---

### 评论 #2 — alexschroeter (2026-02-03T20:22:10Z)

It was a installation via the package manager with multiple versions of rocm. We reinstalled just a single rocm version 7.2.0 and now it works. Not sure if it was a bad install or the multiversion installation has issues.

---
