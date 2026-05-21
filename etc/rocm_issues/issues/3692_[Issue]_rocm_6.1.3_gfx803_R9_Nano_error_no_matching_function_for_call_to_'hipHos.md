# [Issue]: rocm 6.1.3 gfx803 R9 Nano error: no matching function for call to 'hipHostAlloc'

> **Issue #3692**
> **状态**: closed
> **创建时间**: 2024-09-09T16:33:53Z
> **更新时间**: 2024-12-10T05:21:11Z
> **关闭时间**: 2024-12-10T05:21:10Z
> **作者**: djygithub
> **标签**: Under Investigation, AMD Radeon VII, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3692

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Error preparing Rocm 6.1.3 application with vintage hardware https://github.com/djygithub/craydgemm

### Operating System

NAME="Ubuntu" VERSION="22.04.4 LTS (Jammy Jellyfish)"

### CPU

 AMD Ryzen 7 1700 Eight-Core Processor

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIP

### Steps to Reproduce

Prepare application from https://github.com/djygithub/craydgemm

`/opt/rocm-6.1.3/bin/hipify-perl
 Matrix_Multiplication_GPU_DOUBLE_GIOPS_PINNED_TWO.cu > mmgpudoublegiops.cpp

/opt/rocm-6.1.3/bin/hipcc -O2 -o mmdblgpugiops  mmgpudoublegiops.cpp 

`mmgpudoublegiops.cpp:121:2: error: no matching function for call to 'hipHostAlloc'
  121 |         hipHostAlloc(&a,bytes_a,hipHostMallocDefault);
`

Worked around issue by changing the output file of hipify-perl (mmgpudoublegiops.cpp):

//allocate arrays
	//a = (int*) malloc( bytes_a );
	**hipHostMalloc**(&a,bytes_a,hipHostMallocDefault);
	CHECK(a == 0 ? hipErrorOutOfMemory : hipSuccess );
	//b = (int*) malloc( bytes_b );
	**hipHostMalloc**(&b,bytes_b,hipHostMallocDefault);
	CHECK(b == 0 ? hipErrorOutOfMemory : hipSuccess );
	//c = (int*) malloc( bytes_b );
	**hipHostMalloc**(&c,bytes_c,hipHostMallocDefault);
	CHECK(c == 0 ? hipErrorOutOfMemory : hipSuccess );

FWIW GFLOPS/second on the R9 using this application went up substantially from ROCM 4.1 to ROCM 6.1.3:
https://davidjyoung.com/cmg/sqldgemm24.pdf
![Slide36](https://github.com/user-attachments/assets/945125e8-a358-40c7-aea8-94de977fd53b)

Thanks.


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

david@r7pxeclient:~$ rocminfo --support
ROCk module version 6.7.0 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.13
Runtime Ext Version:     1.4
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 7 1700 Eight-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 1700 Eight-Core Processor
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
  Max Clock Freq. (MHz):   3000
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32797028(0x1f47164) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32797028(0x1f47164) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32797028(0x1f47164) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx803
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon (TM) R9 Fury Series
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
  Chip ID:                 29440(0x7300)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1000
  BDFID:                   2304
  Internal Node ID:        1
  Compute Unit:            64
  SIMDs per CU:            4
  Shader Engines:          4
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
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
  Packet Processor uCode:: 729
  SDMA engine uCode::      34
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    4194304(0x400000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    4194304(0x400000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx803
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
david@r7pxeclient:~$


### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-09-09T19:55:16Z)

Hi @djygithub, thank you for reporting this issue. I was able to reproduce the error after hipifying the sample you provided. Let me look into this further and get back to you.

---

### 评论 #2 — harkgill-amd (2024-09-10T17:32:05Z)

@djygithub, this error was caused due to a missing wrapper for the hipHostAlloc function. A fix for this issue will be available in an upcoming ROCm release along with some modifications to the functions behavior. Let's keep this ticket open for now and I will circle back to you once the fix is available to confirm and close out the issue.

For now, please continue to use the hipHostMalloc workaround that you have identified.

---

### 评论 #3 — harkgill-amd (2024-12-09T19:51:11Z)

Hi @djygithub, the changes to hipHostAlloc have been implemented in ROCm 6.3. I am no longer seeing any issues after hipifying and compiling the sample you provided. Could you please give it a try on your end?

---

### 评论 #4 — djygithub (2024-12-10T05:21:10Z)

Hello compiles and runs without issue on 6.3.0 nice work thanks!
Numbers are also slightly better:


  | GPU |   |  
-- | -- | -- | --
  | DGFLOPS/sec |   |  
  | rocm 4.1 | rocm 6.1 | rocm 6.3
1 | 75.36 | 143.47 | 143.5
2 | 112.96 | 181.92 | 182
3 | 112.91 | 177.74 | 185.92
4 | 115.65 | 179.94 | 188.09
5 | 116.12 | 181.49 | 189.19
6 | 117.03 | 182.48 | 190.75
7 | 119.67 | 182.96 | 191.32
8 | 120.63 | 184.54 | 192.85
9 | 117.78 | 184.45 | 192.32
10 | 118.26 | 184.81 | 192.98
11 |   | 184.08 | 192.25
12 |   | 183.93 | 193.27

**apt show rocm-libs -a**

`david@r7pxeclient:~/craydgemm/rocm63/craydgemm$ apt show rocm-libs -a
Package: rocm-libs
Version: 6.3.0.60300-39~22.04
Priority: optional
Section: devel
Maintainer: ROCm Dev Support <rocm-dev.support@amd.com>
Installed-Size: 13.3 kB
Depends: hipblas (= 2.3.0.60300-39~22.04), hipblaslt (= 0.10.0.60300-39~22.04), hipfft (= 1.0.17.60300-39~22.04), hipsolver (=                                      2.3.0.60300-39~22.04), hipsparse (= 3.1.2.60300-39~22.04), hiptensor (= 1.4.0.60300-39~22.04), miopen-hip (= 3.3.0.60300-39~22.                                     04), half (= 1.12.0.60300-39~22.04), rccl (= 2.21.5.60300-39~22.04), rocalution (= 3.2.1.60300-39~22.04), rocblas (= 4.3.0.6030                                     0-39~22.04), rocfft (= 1.0.31.60300-39~22.04), rocrand (= 3.2.0.60300-39~22.04), hiprand (= 2.11.0.60300-39~22.04), rocsolver (                                     = 3.27.0.60300-39~22.04), rocsparse (= 3.3.0.60300-39~22.04), rocm-core (= 6.3.0.60300-39~22.04), hipsparselt (= 0.2.2.60300-39                                     ~22.04), composablekernel-dev (= 1.1.0.60300-39~22.04), hipblas-dev (= 2.3.0.60300-39~22.04), hipblaslt-dev (= 0.10.0.60300-39~                                     22.04), hipcub-dev (= 3.3.0.60300-39~22.04), hipfft-dev (= 1.0.17.60300-39~22.04), hipsolver-dev (= 2.3.0.60300-39~22.04), hips                                     parse-dev (= 3.1.2.60300-39~22.04), hiptensor-dev (= 1.4.0.60300-39~22.04), miopen-hip-dev (= 3.3.0.60300-39~22.04), rccl-dev (                                     = 2.21.5.60300-39~22.04), rocalution-dev (= 3.2.1.60300-39~22.04), rocblas-dev (= 4.3.0.60300-39~22.04), rocfft-dev (= 1.0.31.6                                     0300-39~22.04), rocprim-dev (= 3.3.0.60300-39~22.04), rocrand-dev (= 3.2.0.60300-39~22.04), hiprand-dev (= 2.11.0.60300-39~22.0                                     4), rocsolver-dev (= 3.27.0.60300-39~22.04), rocsparse-dev (= 3.3.0.60300-39~22.04), rocthrust-dev (= 3.3.0.60300-39~22.04), ro                                     cwmma-dev (= 1.6.0.60300-39~22.04), hipsparselt-dev (= 0.2.2.60300-39~22.04)
Homepage: https://github.com/RadeonOpenCompute/ROCm
Download-Size: 1,054 B
APT-Sources: https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 Packages
Description: Radeon Open Compute (ROCm) Runtime software stack

david@r7pxeclient:~/craydgemm/rocm63/craydgemm$`

---
