# [Issue]: Intermittent GPU Hang HW Exception by GPU on MI300X when training with axolotl

> **Issue #4021**
> **状态**: closed
> **创建时间**: 2024-11-09T16:36:14Z
> **更新时间**: 2026-02-05T15:03:12Z
> **关闭时间**: 2025-01-08T21:49:01Z
> **作者**: lhl
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.2.3
> **URL**: https://github.com/ROCm/ROCm/issues/4021

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.2.3** (颜色: #ededed)

## 描述

### Problem Description

When running [axolotl](https://github.com/axolotl-ai-cloud/axolotl/) runs, I get intermittent GPU hangs:

```
{'loss': 0.4589, 'grad_norm': 1.0493940198290594, 'learning_rate': 5.284132841328413e-06, 'epoch': 1.22}
 41%|██████████████████████████████████████████▌                                                              | 366/903 [5:15:39<6:53:09, 46.16s/it]HW Exception by GPU node-9 (Agent handle: 0x631351bb5a20) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x64ff272d8ab0) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x565d634d8610) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x5ea50312c910) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x619acaf10aa0) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x5ab551f9f310) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x5e2772f37790) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x5a6c6e4a4680) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x582b7268cac0) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x5b5e27441f40) reason :GPU Hang
HW Exception by GPU node-9 (Agent handle: 0x5c6c69e57ff0) reason :GPU Hang
Aborted (core dumped)
(axolotl) 134 hotaisle@ENC1-CLS01-SVR14:~/shisa-v2/train/ablations$ [rank2]:[E1109 16:13:20.222288244 ProcessGroupNCCL.cpp:616] [Rank 2] Watchdog caught collective operation timeout: WorkNCCL(SeqNum=500045, OpType=_REDUCE_SCATTER_BASE, NumelIn=67108864, NumelOut=8388608, Timeout(ms)=600000) ran for 600038 milliseconds before timing out.
[rank2]:[E1109 16:13:20.222705810 ProcessGroupNCCL.cpp:1785] [PG ID 1 PG GUID 1 Rank 2] Exception (either an error or timeout) detected by watchdog at work: 500045, last enqueued NCCL work: 500047, last completed NCCL work: 500044.
[rank7]:[E1109 16:13:20.230357202 ProcessGroupNCCL.cpp:616] [Rank 7] Watchdog caught collective operation timeout: WorkNCCL(SeqNum=500045, OpType=_REDUCE_SCATTER_BASE, NumelIn=67108864, NumelOut=8388608, Timeout(ms)=600000) ran for 600046 milliseconds before timing out.
[rank7]:[E1109 16:13:20.230674458 ProcessGroupNCCL.cpp:1785] [PG ID 1 PG GUID 1 Rank 7] Exception (either an error or timeout) detected by watchdog at work: 500045, last enqueued NCCL work: 500047, last completed NCCL work: 500044.
[rank3]:[E1109 16:13:20.249114105 ProcessGroupNCCL.cpp:616] [Rank 3] Watchdog caught collective operation timeout: WorkNCCL(SeqNum=500045, OpType=_REDUCE_SCATTER_BASE, NumelIn=67108864, NumelOut=8388608, Timeout(ms)=600000) ran for 600065 milliseconds before timing out.
[rank3]:[E1109 16:13:20.249396998 ProcessGroupNCCL.cpp:1785] [PG ID 1 PG GUID 1 Rank 3] Exception (either an error or timeout) detected by watchdog at work: 500045, last enqueued NCCL work: 500045, last completed NCCL work: 500044.
[rank4]:[E1109 16:13:20.252514562 ProcessGroupNCCL.cpp:616] [Rank 4] Watchdog caught collective operation timeout: WorkNCCL(SeqNum=500045, OpType=_REDUCE_SCATTER_BASE, NumelIn=67108864, NumelOut=8388608, Timeout(ms)=600000) ran for 600068 milliseconds before timing out.
[rank4]:[E1109 16:13:20.252770852 ProcessGroupNCCL.cpp:1785] [PG ID 1 PG GUID 1 Rank 4] Exception (either an error or timeout) detected by watchdog at work: 500045, last enqueued NCCL work: 500045, last completed NCCL work: 500044.
[rank6]:[E1109 16:13:20.262103416 ProcessGroupNCCL.cpp:616] [Rank 6] Watchdog caught collective operation timeout: WorkNCCL(SeqNum=500045, OpType=_REDUCE_SCATTER_BASE, NumelIn=67108864, NumelOut=8388608, Timeout(ms)=600000) ran for 600078 milliseconds before timing out.
[rank6]:[E1109 16:13:20.262386071 ProcessGroupNCCL.cpp:1785] [PG ID 1 PG GUID 1 Rank 6] Exception (either an error or timeout) detected by watchdog at work: 500045, last enqueued NCCL work: 500045, last completed NCCL work: 500044.
[rank1]:[E1109 16:13:20.273208899 ProcessGroupNCCL.cpp:616] [Rank 1] Watchdog caught collective operation timeout: WorkNCCL(SeqNum=500045, OpType=_REDUCE_SCATTER_BASE, NumelIn=67108864, NumelOut=8388608, Timeout(ms)=600000) ran for 600089 milliseconds before timing out.
[rank1]:[E1109 16:13:20.273362088 ProcessGroupNCCL.cpp:1785] [PG ID 1 PG GUID 1 Rank 1] Exception (either an error or timeout) detected by watchdog at work: 500045, last enqueued NCCL work: 500047, last completed NCCL work: 500044.
```

Note, the GPUs are left in a bad state (despite a reset being reported in dmesg, logs included below):
```
============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp        Power     Partitions          SCLK    MCLK    Fan  Perf  PwrCap  VRAM%  GPU%
^[3m              (DID,     GUID)  (Junction)  (Socket)  (Mem, Compute, ID)                                                  ^[0m
==========================================================================================================================
0       2     0x74a1,   55354  48.0°C      145.0W    NPS1, SPX, 0        132Mhz  900Mhz  0%   auto  750.0W  1%     0%
1       3     0x74a1,   41632  40.0°C      138.0W    NPS1, SPX, 0        131Mhz  900Mhz  0%   auto  750.0W  75%    0%
2       4     0x74a1,   47045  42.0°C      135.0W    NPS1, SPX, 0        132Mhz  900Mhz  0%   auto  750.0W  74%    0%
3       5     0x74a1,   60169  49.0°C      150.0W    NPS1, SPX, 0        132Mhz  900Mhz  0%   auto  750.0W  74%    0%
4       6     0x74a1,   56024  47.0°C      146.0W    NPS1, SPX, 0        132Mhz  900Mhz  0%   auto  750.0W  75%    0%
5       7     0x74a1,   705    42.0°C      139.0W    NPS1, SPX, 0        132Mhz  900Mhz  0%   auto  750.0W  1%     0%
6       8     0x74a1,   59108  48.0°C      147.0W    NPS1, SPX, 0        132Mhz  900Mhz  0%   auto  750.0W  75%    0%
7       9     0x74a1,   10985  40.0°C      138.0W    NPS1, SPX, 0        132Mhz  900Mhz  0%   auto  750.0W  74%    0%
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
```

VRAM remains in use. Running an additional GPU reset does not work: `sudo amd-smi reset -g 0 -G`, a full system reboot is required to clear this up.

This seems to happen on about half of my runs (that are greater than a few hours).

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

Intel(R) Xeon(R) Platinum 8470

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

Install and run axolotl, eg:
```
accelerate launch -m axolotl.cli.train mi300x-llama3.1-70b-fft.dsz3.yaml
```
You can see https://github.com/AUGMXNT/MI300-testing/ or https://github.com/shisa-ai/shisa-v2/tree/main/train/ablations for some sample yaml files (I am running llama3-70b ffts that take about 12-20h to do)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
```
ROCk module version 6.8.5 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.14
Runtime Ext Version:     1.6
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
  Name:                    Intel(R) Xeon(R) Platinum 8470
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Xeon(R) Platinum 8470
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
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3800
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            104
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    1056364836(0x3ef6d924) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1056364836(0x3ef6d924) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    1056364836(0x3ef6d924) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    Intel(R) Xeon(R) Platinum 8470
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Xeon(R) Platinum 8470
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
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3800
  BDFID:                   0
  Internal Node ID:        1
  Compute Unit:            104
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    1056871544(0x3efe9478) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1056871544(0x3efe9478) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    1056871544(0x3efe9478) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 3
*******
  Name:                    gfx942
  Uuid:                    GPU-07386a321fa45d1e
  Marketing Name:          AMD Instinct MI300X
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
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   6912
  Internal Node ID:        2
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
  Name:                    gfx942
  Uuid:                    GPU-c14abb436c69353f
  Marketing Name:          AMD Instinct MI300X
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
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   15616
  Internal Node ID:        3
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
  Name:                    gfx942
  Uuid:                    GPU-4be0e20b12ab7fa1
  Marketing Name:          AMD Instinct MI300X
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
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   19968
  Internal Node ID:        4
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
Agent 6
*******
  Name:                    gfx942
  Uuid:                    GPU-18c80aec63536c85
  Marketing Name:          AMD Instinct MI300X
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    5
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   24320
  Internal Node ID:        5
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
Agent 7
*******
  Name:                    gfx942
  Uuid:                    GPU-98c78750297b3198
  Marketing Name:          AMD Instinct MI300X
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    6
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   40192
  Internal Node ID:        6
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
Agent 8
*******
  Name:                    gfx942
  Uuid:                    GPU-c8d0ce1363e0130e
  Marketing Name:          AMD Instinct MI300X
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    7
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   48384
  Internal Node ID:        7
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
Agent 9
*******
  Name:                    gfx942
  Uuid:                    GPU-fdee8fae2de9f2b6
  Marketing Name:          AMD Instinct MI300X
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    8
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   52480
  Internal Node ID:        8
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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
Agent 10
*******
  Name:                    gfx942
  Uuid:                    GPU-6f890acb8eb0492b
  Marketing Name:          AMD Instinct MI300X
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    9
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29857(0x74a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2100
  BDFID:                   56576
  Internal Node ID:        9
  Compute Unit:            304
  SIMDs per CU:            4
  Shader Engines:          32
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
  Packet Processor uCode:: 150
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    201310208(0xbffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 4
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx942:sramecc+:xnack-
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

Here's what the `dmesg` looks like:
```
[76914.152141] amdgpu 0000:dd:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[76914.152174] amdgpu 0000:3d:00.0: amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[76914.152926] amdgpu 0000:1b:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.152940] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xbaa000000000080b
[76914.152948] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[76914.152953] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[76914.152957] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001d02e1f007900
[76914.152961] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000000005d003e1b
[76914.156884] amdgpu: Failed to restore process queues
[76914.156901] amdgpu: Failed to restore process queues
[76914.156914] amdgpu: Failed to restore process queues
[76914.156925] amdgpu: Failed to restore process queues
[76914.156935] amdgpu: Failed to restore process queues
[76914.156945] amdgpu: Failed to restore process queues
[76914.156956] amdgpu: Failed to restore process queues
[76914.156965] amdgpu: Failed to restore process queues
[76914.184889] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.184894] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xd820000000060150
[76914.184898] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[76914.184902] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008005100000000
[76914.184906] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0000605011a09201
[76914.184910] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x009c732d4a000000
[76914.185363] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.185366] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xd820000000060150
[76914.185370] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[76914.185373] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008003100000000
[76914.185377] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0000605011a09201
[76914.185381] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x009c752d4a000000
[76914.185838] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.185842] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].STATUS=0xd820000000060400
[76914.185846] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].ADDR=0x0000000000000000
[76914.185850] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].MISC0=0xd008008100000000
[76914.185853] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].IPID=0x0000605011a09201
[76914.185857] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].SYND=0x00000000809c812d
[76914.186309] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.186313] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[03].STATUS=0xd820000000060150
[76914.186316] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[03].ADDR=0x0000000000000000
[76914.186320] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[03].MISC0=0xd008000400000000
[76914.186324] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[03].IPID=0x0000605011a09201
[76914.186327] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[03].SYND=0x009c812d4a000000
[76914.186783] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.186786] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[04].STATUS=0xd820000000060150
[76914.186790] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[04].ADDR=0x0000000000000000
[76914.186794] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[04].MISC0=0xd00800f800000000
[76914.186797] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[04].IPID=0x0000605011a09201
[76914.186801] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[04].SYND=0x009c812d4a000000
[76914.187259] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.187262] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[05].STATUS=0xd820000000060150
[76914.187266] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[05].ADDR=0x0000000000000000
[76914.187269] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[05].MISC0=0xd008005100000000
[76914.187273] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[05].IPID=0x0000605011a09201
[76914.187277] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[05].SYND=0x009c752d4a000000
[76914.187740] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.187744] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[06].STATUS=0xd820000000060150
[76914.187748] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[06].ADDR=0x0000000000000000
[76914.187751] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[06].MISC0=0xd008004000000000
[76914.187755] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[06].IPID=0x0000605011a09201
[76914.187759] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[06].SYND=0x009c752d4a000000
[76914.188214] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.188217] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[07].STATUS=0xd820000000060150
[76914.188221] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[07].ADDR=0x0000000000000000
[76914.188225] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[07].MISC0=0xd008002000000000
[76914.188228] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[07].IPID=0x0000605011a09201
[76914.188232] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[07].SYND=0x009c752d4a000000
[76914.188696] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.188700] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[08].STATUS=0xd820000000060150
[76914.188704] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[08].ADDR=0x0000000000000000
[76914.188708] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[08].MISC0=0xd00800a400000000
[76914.188711] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[08].IPID=0x0000605011a09201
[76914.188715] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[08].SYND=0x009c752d4a000000
[76914.189163] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.189166] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[09].STATUS=0xd820000000060150
[76914.189169] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[09].ADDR=0x0000000000000000
[76914.189172] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[09].MISC0=0xd008005000000000
[76914.189175] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[09].IPID=0x0000605011a09201
[76914.189178] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[09].SYND=0x009c752d4a000000
[76914.189644] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.189647] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[10].STATUS=0xd820000000060150
[76914.189651] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[10].ADDR=0x0000000000000000
[76914.189655] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[10].MISC0=0xd008012400000000
[76914.189658] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[10].IPID=0x0000605011a09201
[76914.189662] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[10].SYND=0x009c812d4a000000
[76914.190110] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[76914.190112] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[11].STATUS=0xd820000000060150
[76914.190116] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[11].ADDR=0x0000000000000000
[76914.190119] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[11].MISC0=0xd008013500000000
[76914.190122] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[11].IPID=0x0000605011a09201
[76914.190126] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[11].SYND=0x009c812d4a000000
[76914.190522] amdgpu 0000:9d:00.0: {1}socket: 6, die: 1, 1533 new correctable hardware errors detected in xgmi_wafl block
[76914.190529] amdgpu 0000:9d:00.0: {1}socket: 6, die: 1, 1533 correctable hardware errors detected in total in xgmi_wafl block
[76914.214195] amdgpu 0000:dd:00.0: amdgpu: GPU reset begin!
[76914.216568] Pid 1230312(python3.12) over core_pipe_limit
[76914.216571] Skipping core dump
[76914.237823] amdgpu 0000:dd:00.0: amdgpu: Dumping IP State
[76914.237826] amdgpu 0000:dd:00.0: amdgpu: Dumping IP State Completed
[76914.238315] amdgpu 0000:1b:00.0: amdgpu: MODE1 reset
[76914.238316] amdgpu 0000:dd:00.0: amdgpu: MODE1 reset
[76914.238321] amdgpu 0000:dd:00.0: amdgpu: GPU mode1 reset
[76914.238320] amdgpu 0000:3d:00.0: amdgpu: MODE1 reset
[76914.238322] amdgpu 0000:1b:00.0: amdgpu: GPU mode1 reset
[76914.238321] amdgpu 0000:4e:00.0: amdgpu: MODE1 reset
[76914.238322] amdgpu 0000:bd:00.0: amdgpu: MODE1 reset
[76914.238323] amdgpu 0000:9d:00.0: amdgpu: MODE1 reset
[76914.238323] amdgpu 0000:5f:00.0: amdgpu: MODE1 reset
[76914.238324] amdgpu 0000:cd:00.0: amdgpu: MODE1 reset
[76914.238329] amdgpu 0000:9d:00.0: amdgpu: GPU mode1 reset
[76914.238330] amdgpu 0000:5f:00.0: amdgpu: GPU mode1 reset
[76914.238332] amdgpu 0000:bd:00.0: amdgpu: GPU mode1 reset
[76914.238334] amdgpu 0000:4e:00.0: amdgpu: GPU mode1 reset
[76914.238336] amdgpu 0000:cd:00.0: amdgpu: GPU mode1 reset
[76914.238337] amdgpu 0000:3d:00.0: amdgpu: GPU mode1 reset
[76914.240668] amdgpu 0000:dd:00.0: amdgpu: GPU smu mode1 reset
[76914.241079] amdgpu 0000:cd:00.0: amdgpu: GPU smu mode1 reset
[76914.241104] amdgpu 0000:1b:00.0: amdgpu: GPU smu mode1 reset
[76914.241152] amdgpu 0000:5f:00.0: amdgpu: GPU smu mode1 reset
[76914.241257] amdgpu 0000:3d:00.0: amdgpu: GPU smu mode1 reset
[76914.241282] amdgpu 0000:4e:00.0: amdgpu: GPU smu mode1 reset
[76914.243199] amdgpu 0000:9d:00.0: amdgpu: GPU smu mode1 reset
[76914.243283] amdgpu 0000:bd:00.0: amdgpu: GPU smu mode1 reset
[76919.010450] amdgpu 0000:dd:00.0: amdgpu: GPU reset succeeded, trying to resume
[76919.011774] [drm] PCIE GART of 512M enabled.
[76919.011779] [drm] PTB located at 0x000002EFED700000
[76919.011910] [drm] VRAM is lost due to GPU reset!
```

---

## 评论 (43 条)

### 评论 #1 — ppanchad-amd (2024-11-11T18:12:11Z)

Hi @lhl. Internal ticket is created to investigate your issue. Thanks!

---

### 评论 #2 — miron-boiangiu (2024-11-16T21:05:42Z)

I have the same exact problem when trying to train a model with PyTorch.

---

### 评论 #3 — lhl (2024-11-17T12:42:52Z)

@ppanchad-amd so a couple updates. This happens:
- 100% of the time 6-9h using axolotl and liger kernels: https://embeddedllm.com/blog/cuda-to-rocm-portability-case-study-liger-kernel
- maybe 50% of the time in a 15h training run using axolotl and regular kernel (trl-based trainer)
- I've seen similar hangs on vLLM occasionally. I have seen this reproduced reliably trying to load deepseek-ai/DeepSeek-V2.5 w/ ROCm/vLLM - eg run `VLLM_USE_TRITON_FLASH_ATTN=0 vllm serve -tp 8 deepseek-ai/DeepSeek-V2.5 --trust-remote-code` although that might be a different bug since it doesn't have stuff hanging around in memroy This was replicated by @tjtanaa on a separate machine.
- Continues to be an issue w/ 6.2.4

I have dmesg logs for many of these crashes if necessary.

---

### 评论 #4 — jamesxu2 (2024-11-18T19:31:33Z)

Hi @lhl, thanks for the update. I have tried to run axolotl on some small (~2.5h) workloads with an MI300X server but wasn't able to reproduce this locally. That seems to add up given your observed long runtime requirement to trigger this bug. 

> 100% of the time 6-9h using axolotl and liger kernels: 

What specific Liger kernel are you running? Are you referring to the two Liger kernels in the [second repository](https://github.com/shisa-ai/shisa-v2/tree/main/train/ablations) you linked in the original issue or something else?

I'd like to get this down to a minimal reproducer so the cost to repro is less staggering - I can try assessing this bug via the most reliable/quickest path which seems to be the liger kernels. 

> I have dmesg logs for many of these crashes if necessary.

The error signature in your dmesg is somewhat ambiguous, but if you're able to please share your other dmesg logs with me. You can attach them to the ticket or email me (see my profile) if you're uncomfortable sharing this publicly. 

@miron-boiangiu, if you have a faster way to reproduce this issue, please provide some more information and that can help us find a solution faster. What model are you training with Pytorch, and are you using the same hardware as @lhl (mi300x)? If it really is the same issue, we can consolidate the discussion here in the same Github issue.



---

### 评论 #5 — lhl (2024-11-19T04:29:43Z)

Here is the most recent failure just checking on my latest traiing run, it was only a single node hang and didn't leave memory resident. This was `4:51:05<8:54:01` (5h into a ~14h run). Error:

```
 33%|███████████████████Memory access fault by GPU node-3 (Agent handle: 0x5a5c587a51c0) on address 0x709843600000. Reason: Write access to a read-only page.:54:01, 26.24s/it]
```

from `dmesg` (if there's a better place to look at more useful errors let me know:
```
[19277.975559] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32790)
[19277.975569] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] no-retry page fault (src_id:0 ring:160 vmid:3 pasid:32790)
[19277.975611] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.975625] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843600000 from IH client 0x12 (VMC)
[19277.975640] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.975655] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00360251
[19277.975667] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0x101)
[19277.975679] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x1
[19277.975694] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.975702] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x5
[19277.975711] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.975722] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x1
[19277.975743] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] no-retry page fault (src_id:0 ring:160 vmid:3 pasid:32790)
[19277.975762] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.975782] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843600000 from IH client 0x12 (VMC)
[19277.975802] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.975819] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00360341
[19277.975834] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0x101)
[19277.975848] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x1
[19277.975859] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.975871] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x4
[19277.975882] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x1
[19277.975893] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x1
[19277.975903] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] no-retry page fault (src_id:0 ring:160 vmid:3 pasid:32790)
[19277.975920] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.975933] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843600000 from IH client 0x12 (VMC)
[19277.975948] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.975964] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19277.975975] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19277.975987] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19277.975996] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.976005] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19277.976015] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.976025] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
[19277.976034] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] no-retry page fault (src_id:0 ring:160 vmid:3 pasid:32790)
[19277.976051] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.976064] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843600000 from IH client 0x12 (VMC)
[19277.976079] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.976095] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19277.976106] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19277.976118] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19277.976128] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.976137] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19277.976147] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.976425] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
[19277.976679] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] no-retry page fault (src_id:0 ring:160 vmid:3 pasid:32790)
[19277.976942] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.977192] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843600000 from IH client 0x12 (VMC)
[19277.977437] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.977680] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19277.977919] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19277.978154] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19277.978383] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.978610] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19277.978837] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.979061] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
[19277.979305] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.979477] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843600000 from IH client 0x12 (VMC)
[19277.979646] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.979890] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19277.980057] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19277.980222] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19277.980384] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.980541] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19277.980700] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.980922] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
[19277.981083] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32790)
[19277.981250] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.981413] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843601000 from IH client 0x12 (VMC)
[19277.981581] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.981774] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19277.981942] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19277.982108] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19277.982269] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.982428] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19277.982585] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.982785] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
[19277.982945] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32790)
[19277.983119] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.983282] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843602000 from IH client 0x12 (VMC)
[19277.983449] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.983621] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19277.983823] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19277.983989] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19277.984151] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.984309] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19277.984466] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.984621] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
[19277.984810] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32790)
[19277.984984] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19277.985148] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843603000 from IH client 0x12 (VMC)
[19277.985316] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19277.985487] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19277.985652] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19277.985866] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19277.986029] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19277.986187] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19277.986343] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19277.986499] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
[19278.003288] amdgpu 0000:3d:00.0: amdgpu: [mmhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32790)
[19278.003623] amdgpu 0000:3d:00.0: amdgpu:  for process python3.12 pid 6071 thread python3.12 pid 6071)
[19278.003924] amdgpu 0000:3d:00.0: amdgpu:   in page starting at address 0x0000709843604000 from IH client 0x12 (VMC)
[19278.004213] amdgpu 0000:3d:00.0: amdgpu:   cookie node_id 0 fault from die AID0
[19278.004501] amdgpu 0000:3d:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00000000
[19278.004919] amdgpu 0000:3d:00.0: amdgpu:      Faulty UTCL2 client ID: unknown (0x0)
[19278.005274] amdgpu 0000:3d:00.0: amdgpu:      MORE_FAULTS: 0x0
[19278.005533] amdgpu 0000:3d:00.0: amdgpu:      WALKER_ERROR: 0x0
[19278.005955] amdgpu 0000:3d:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[19278.006294] amdgpu 0000:3d:00.0: amdgpu:      MAPPING_ERROR: 0x0
[19278.006555] amdgpu 0000:3d:00.0: amdgpu:      RW: 0x0
```

This is the more standard mult-GPU hang:
```
[500967.571516] amdgpu 0000:dd:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[500967.587601] amdgpu 0000:4e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[500967.587615] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xfaa00000000d080b
[500967.587623] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[500967.587628] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000600000000
[500967.587633] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0002702e1f000300
[500967.587637] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000000005d000000
[500967.587920] amdgpu 0000:4e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[500967.587924] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xbaa000000000080b
[500967.587928] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[500967.587932] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[500967.587936] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001b02e1f007900
[500967.587940] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x000000005d00241b
[500967.607060] amdgpu 0000:1b:00.0: amdgpu: Couldn't get PPT limit
[500967.610557] amdgpu 0000:3d:00.0: amdgpu: Couldn't get PPT limit
[500967.613844] amdgpu 0000:4e:00.0: amdgpu: Couldn't get PPT limit
[500967.617094] amdgpu 0000:5f:00.0: amdgpu: Couldn't get PPT limit
[500967.620317] amdgpu 0000:9d:00.0: amdgpu: Couldn't get PPT limit
[500967.623543] amdgpu 0000:bd:00.0: amdgpu: Couldn't get PPT limit
[500967.626774] amdgpu 0000:cd:00.0: amdgpu: Couldn't get PPT limit
[500967.627733] amdgpu 0000:dd:00.0: amdgpu: GPU reset begin!
[500967.628695] Pid 4141112(accelerate) over core_pipe_limit
[500967.628699] Skipping core dump
[500967.651415] amdgpu 0000:dd:00.0: amdgpu: Dumping IP State
[500967.651419] amdgpu 0000:dd:00.0: amdgpu: Dumping IP State Completed
[500967.651971] amdgpu 0000:bd:00.0: amdgpu: MODE1 reset
[500967.651972] amdgpu 0000:3d:00.0: amdgpu: MODE1 reset
[500967.651971] amdgpu 0000:dd:00.0: amdgpu: MODE1 reset
[500967.651973] amdgpu 0000:5f:00.0: amdgpu: MODE1 reset
[500967.651976] amdgpu 0000:9d:00.0: amdgpu: MODE1 reset
[500967.651977] amdgpu 0000:3d:00.0: amdgpu: GPU mode1 reset
[500967.651977] amdgpu 0000:4e:00.0: amdgpu: MODE1 reset
[500967.651979] amdgpu 0000:5f:00.0: amdgpu: GPU mode1 reset
[500967.651979] amdgpu 0000:bd:00.0: amdgpu: GPU mode1 reset
[500967.651977] amdgpu 0000:1b:00.0: amdgpu: MODE1 reset
[500967.651979] amdgpu 0000:cd:00.0: amdgpu: MODE1 reset
[500967.651983] amdgpu 0000:9d:00.0: amdgpu: GPU mode1 reset
[500967.651986] amdgpu 0000:dd:00.0: amdgpu: GPU mode1 reset
[500967.651990] amdgpu 0000:cd:00.0: amdgpu: GPU mode1 reset
[500967.651990] amdgpu 0000:1b:00.0: amdgpu: GPU mode1 reset
[500967.651993] amdgpu 0000:4e:00.0: amdgpu: GPU mode1 reset
[500967.654206] amdgpu 0000:3d:00.0: amdgpu: GPU smu mode1 reset
[500967.654593] amdgpu 0000:1b:00.0: amdgpu: GPU smu mode1 reset
[500967.654774] amdgpu 0000:bd:00.0: amdgpu: GPU smu mode1 reset
[500967.654797] amdgpu 0000:9d:00.0: amdgpu: GPU smu mode1 reset
[500967.654840] amdgpu 0000:dd:00.0: amdgpu: GPU smu mode1 reset
[500967.654862] amdgpu 0000:cd:00.0: amdgpu: GPU smu mode1 reset
[500967.656096] amdgpu 0000:5f:00.0: amdgpu: GPU smu mode1 reset
[500967.656170] amdgpu 0000:4e:00.0: amdgpu: GPU smu mode1 reset
[500972.423331] amdgpu 0000:dd:00.0: amdgpu: GPU reset succeeded, trying to resume
[500972.424642] [drm] PCIE GART of 512M enabled.
[500972.424647] [drm] PTB located at 0x000002EFED700000
[500972.424765] [drm] VRAM is lost due to GPU reset!
[500972.424767] amdgpu 0000:dd:00.0: amdgpu: PSP is resuming...
[500973.142440] amdgpu 0000:dd:00.0: amdgpu: RAP: optional rap ta ucode is not available
[500973.142448] amdgpu 0000:dd:00.0: amdgpu: Requesting 1 partitions through PSP
[500973.150787] amdgpu 0000:dd:00.0: amdgpu: SMU is resuming...
[500973.150793] amdgpu 0000:dd:00.0: amdgpu: smu driver if version = 0x08042024, smu fw if version = 0x08042027, smu fw program = 0, smu fw version = 0x00556b01 (85.107.1)
[500973.150796] amdgpu 0000:dd:00.0: amdgpu: SMU driver if version not matched
[500973.160234] amdgpu 0000:dd:00.0: amdgpu: SMU is resumed successfully!
```
Note that in this case, the GPU reports resetting correctly but leaves memory resident on some of the GPUs (usually 1-3, but I've seen as many as 6):

![Screenshot from 2024-11-17 12-28-55](https://github.com/user-attachments/assets/3bb87353-f44e-4d00-a335-a9a63c03e6a0)

Running `sudo amd-smi reset -g 0 -G` doesn't help, only a complete system reboot will recover the occupied memory.

I actually recently cleared a bunch of logs it looks like, but I noticed that while I get a variety of GPU hang reasons, the  [gfxhub0] retry page fault / cookie node_id 1 fault from die / VM_L2_PROTECTION_FAULT_STATUS errors were pretty common.

The Liger kernels which might make it easier to reproduce were the same ones here: https://embeddedllm.com/blog/cuda-to-rocm-portability-case-study-liger-kernel and installed the same way:

```
python -m pip install "git+https://github.com/linkedin/Liger-Kernel.git#egg=liger-kernel[transformers]"
```

Note, they did a fair amount of benchmarking/tests presumably without problems on an 8xMI300X node, however only with 7B class models using the Alpaca dataset (so short runs). The earliest I've seen a GPU hang is ~3h in. I'm testing exclusively w/ the standard trl/axolotl kernels, not liger since I'm actually trying to finish runs... I'll keep posting additional crash/logs here if they are different.

---

### 评论 #6 — jamesxu2 (2024-11-20T22:12:13Z)

@lhl Have you been able to reproduce this issue using some workload less complex than through Axolotl fine tuning? 

Axolotl seems to depend on and require a source build of flashAttention, xformers, bitsandbytes and deepspeed to work on ROCm, which are relatively new and all of which have numerous problems building. While it seems theoretically possible to get this working for ROCm without a dependency-hell-type situation, most of these repositories are still being actively worked on and aren't in a fully stable state for ROCm. 

While it should be possible for us to match your stack eventually, a more minimal and less fragile reproducer would be a great help as this issue is complex enough. If there really isn't another option, that's fine too. 


---

### 评论 #7 — lhl (2024-11-21T06:46:16Z)

Yeah, axolotl is a bit of a bear, although the only real conflict is axolotl installing the wrong version of bitsandbytes. I then manually reinstall the multi-backend version:

```
pip install --force-reinstall 'https://github.com/bitsandbytes-foundation/bitsandbytes/releases/download/continuous-release_multi-backend-refactor/bitsandbytes-0.44.1.dev0-py3-none-manylinux_2_24_x86_64.whl'
```

I have vLLM method that much more reliably causes GPU hangs that I'll post when the node frees up but I'm not sure if it's actually the same bug.  I can try to queue up a throwaway overnight `torchtune` run just to see if I can get that to replicate in a couple days.

---

### 评论 #8 — anthonix (2024-11-21T20:57:19Z)

I've seen "{1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!" issues on multiple different MI300x machines after a few hours of training (sometimes occurs after just an hour or two, sometimes takes a day or two). 

I'm running low level code with no deps outside of ROCm, so this doesn't seem to be related to axolotl / bitsandbytes / xformers / flashattention / deepspeed.. seems like an actual HW issue or ROCm issue. 

---

### 评论 #9 — jamesxu2 (2024-11-21T21:36:18Z)

@anthonix, I was commenting on the build issues for @lhl's reproducer when I mentioned those deps, I wasn't able to run an extended training attempt as there were several conflicting dependencies to sort out. I also think the root cause is something deeper than application-software level, but I would prefer a less complex reproducer to assess that. 

> I'm running low level code with no deps outside of ROCm

Can you provide more detailed reproduction steps? Please include the workload you're running / OS / ROCm version. I don't mean to hijack this issue, and we can always open a new one if this turns out to be distinct, but for now I think it won't hurt to consolidate these similar looking issues in one discussion. 

---

### 评论 #10 — anthonix (2024-11-21T22:05:00Z)

The workload is training, OS is ubuntu 22.04, kernel is 6.8.0-48-generic, ROCm is 6.2.2

Given that I see this same issue on standalone/no-deps code with annoying regularity (but unfortunately I can't share that code), I would suggest running NanoGPT [1] across a few hundred B tokens to repro it on your side.

[1] https://github.com/karpathy/nanoGPT

---

### 评论 #11 — jon-hotaisle (2024-11-21T23:04:02Z)

Filed in ontrack as `HTAA-2`

---

### 评论 #12 — lhl (2024-11-22T04:02:12Z)

FYI, I was seeing if I can switch to torchtune/fsdp as an easier replication after my last axolotl/deepspeed zero3 tune, but it hung so hard that a system reboot actually failed to reinitialize the GPUs, which was a first:

```
[    0.000000]   AMD AuthenticAMD
[    0.008575] RAMDISK: [mem 0x41dee000-0x4be92fff]
[   15.125331] [drm] amdgpu kernel modesetting enabled.
[   15.126639] amdgpu: Virtual CRAT table created for CPU
[   15.127183] amdgpu: Topology: Add CPU node
[   15.142700] amdgpu 0000:1b:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.143045] amdgpu 0000:1b:00.0: amdgpu: Fetched VBIOS from platform
[   15.143235] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.144163] amdgpu 0000:1b:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.144375] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.145654] amdgpu 0000:1b:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.146700] amdgpu 0000:1b:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.147280] amdgpu 0000:1b:00.0: amdgpu: Fatal error during GPU init
[   15.147531] amdgpu 0000:1b:00.0: amdgpu: amdgpu: finishing device.
[   15.161634] amdgpu 0000:3d:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.161972] amdgpu 0000:3d:00.0: amdgpu: Fetched VBIOS from platform
[   15.162159] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.163042] amdgpu 0000:3d:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.163388] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.164194] amdgpu 0000:3d:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.165000] amdgpu 0000:3d:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.165564] amdgpu 0000:3d:00.0: amdgpu: Fatal error during GPU init
[   15.165765] amdgpu 0000:3d:00.0: amdgpu: amdgpu: finishing device.
[   15.182959] amdgpu 0000:4e:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.183329] amdgpu 0000:4e:00.0: amdgpu: Fetched VBIOS from platform
[   15.183569] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.184432] amdgpu 0000:4e:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.184624] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.185308] amdgpu 0000:4e:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.186114] amdgpu 0000:4e:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.186624] amdgpu 0000:4e:00.0: amdgpu: Fatal error during GPU init
[   15.186801] amdgpu 0000:4e:00.0: amdgpu: amdgpu: finishing device.
[   15.201409] amdgpu 0000:5f:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.201861] amdgpu 0000:5f:00.0: amdgpu: Fetched VBIOS from platform
[   15.202073] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.202931] amdgpu 0000:5f:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.203138] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.203933] amdgpu 0000:5f:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.204745] amdgpu 0000:5f:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.205252] amdgpu 0000:5f:00.0: amdgpu: Fatal error during GPU init
[   15.205458] amdgpu 0000:5f:00.0: amdgpu: amdgpu: finishing device.
[   15.231067] amdgpu 0000:9d:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.242434] amdgpu 0000:9d:00.0: amdgpu: Fetched VBIOS from platform
[   15.242653] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.243605] amdgpu 0000:9d:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.243825] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.244678] amdgpu 0000:9d:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.245519] amdgpu 0000:9d:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.246040] amdgpu 0000:9d:00.0: amdgpu: Fatal error during GPU init
[   15.246236] amdgpu 0000:9d:00.0: amdgpu: amdgpu: finishing device.
[   15.269887] amdgpu 0000:bd:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.270326] amdgpu 0000:bd:00.0: amdgpu: Fetched VBIOS from platform
[   15.270555] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.271433] amdgpu 0000:bd:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.271631] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.272376] amdgpu 0000:bd:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.273239] amdgpu 0000:bd:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.273757] amdgpu 0000:bd:00.0: amdgpu: Fatal error during GPU init
[   15.273942] amdgpu 0000:bd:00.0: amdgpu: amdgpu: finishing device.
[   15.287695] amdgpu 0000:cd:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.288099] amdgpu 0000:cd:00.0: amdgpu: Fetched VBIOS from platform
[   15.288293] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.289168] amdgpu 0000:cd:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.289372] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.290108] amdgpu 0000:cd:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.290900] amdgpu 0000:cd:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.291393] amdgpu 0000:cd:00.0: amdgpu: Fatal error during GPU init
[   15.291658] amdgpu 0000:cd:00.0: amdgpu: amdgpu: finishing device.
[   15.304957] amdgpu 0000:dd:00.0: ROM [??? 0x00000000 flags 0x20000000]: can't assign; bogus alignment
[   15.305326] amdgpu 0000:dd:00.0: amdgpu: Fetched VBIOS from platform
[   15.305534] amdgpu: ATOM BIOS: 113-MI3SRIOV-001
[   15.306356] amdgpu 0000:dd:00.0: amdgpu: packed SOS count exceeds maximum limit
[   15.306584] [drm:amdgpu_device_ip_early_init [amdgpu]] *ERROR* early_init of IP block <psp> failed -22
[   15.307275] amdgpu 0000:dd:00.0: [drm:vcn_v4_0_3_early_init [amdgpu]] VCN decode is enabled in VM mode
[   15.308074] amdgpu 0000:dd:00.0: [drm:jpeg_v4_0_3_early_init [amdgpu]] JPEG decode is enabled in VM mode
[   15.308633] amdgpu 0000:dd:00.0: amdgpu: Fatal error during GPU init
[   15.308806] amdgpu 0000:dd:00.0: amdgpu: amdgpu: finishing device.
```

On a full power cycle, they did reinitialize, so this points to some pretty low level hangups. Thanks @anthonix for confirming you're able to replicate on an entirely different stack, makes me more confident to try an extended run and see if I can replicate w/ torchtune/fsdp - this has a lot less moving parts (just pip install of torch, torchao, torchtune). Will report back when (pretty sure not if) it fails.

---

### 评论 #13 — anthonix (2024-11-23T03:38:31Z)

I just had another instance occur about an hour into a training run. 

@jamesxu2 @ppanchad-amd are you able to decode these ACA entries? Or point me to some docs on what these status bits etc mean?

```
[104166.123080] amdgpu 0000:bd:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[104166.131389] amdgpu 0000:1b:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.131405] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[104166.131414] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[104166.131419] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[104166.131424] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001900138430400
[104166.131428] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[104166.131716] amdgpu 0000:1b:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.131719] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x98000800003e0000
[104166.131723] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[104166.131727] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000000000000
[104166.131731] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001d00136430400
[104166.131735] amdgpu 0000:1b:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000000
[104166.139749] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.139753] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[104166.139757] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[104166.139761] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[104166.139764] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001800136430400
[104166.139768] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[104166.140309] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.140313] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x8c204000003a0000
[104166.140317] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000010300000194
[104166.140321] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[104166.140325] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001c00136430400
[104166.140329] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000c06
[104166.140823] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.140826] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x8c204000003a0000
[104166.140830] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000010300000194
[104166.140834] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[104166.140838] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001c00136430400
[104166.140841] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000c06
[104166.141352] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.141356] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].STATUS=0x8c204000003a0000
[104166.141360] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].ADDR=0x0000010300000194
[104166.141364] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].MISC0=0xd008000100000000
[104166.141367] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].IPID=0x0001c00136430400
[104166.141371] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].SYND=0x0000000000000c06
[104166.141861] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.141864] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[03].STATUS=0x8c204000003a0000
[104166.141868] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[03].ADDR=0x0000010300000194
[104166.141872] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[03].MISC0=0xd008000100000000
[104166.141875] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[03].IPID=0x0001c00136430400
[104166.141879] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[03].SYND=0x0000000000000c06
[104166.142385] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.142389] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[04].STATUS=0x8c204000003a0000
[104166.142393] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[04].ADDR=0x0000010300000194
[104166.142396] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[04].MISC0=0xd008000100000000
[104166.142400] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[04].IPID=0x0001c00136430400
[104166.142404] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[04].SYND=0x0000000000000c06
[104166.142891] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.142896] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[05].STATUS=0x8c204000003a0000
[104166.142899] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[05].ADDR=0x0000010300000194
[104166.142903] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[05].MISC0=0xd008000100000000
[104166.142907] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[05].IPID=0x0001c00136430400
[104166.142910] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[05].SYND=0x0000000000000c06
[104166.143418] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.143422] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[06].STATUS=0x8c204000003a0000
[104166.143426] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[06].ADDR=0x0000010300000194
[104166.143429] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[06].MISC0=0xd008000100000000
[104166.143433] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[06].IPID=0x0001c00136430400
[104166.143437] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[06].SYND=0x0000000000000c06
[104166.143930] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.143933] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[07].STATUS=0x8c204000003a0000
[104166.143937] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[07].ADDR=0x0000010300000194
[104166.143941] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[07].MISC0=0xd008000100000000
[104166.143944] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[07].IPID=0x0001c00136430400
[104166.143948] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[07].SYND=0x0000000000000c06
[104166.144464] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.144467] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[08].STATUS=0x8c204000003a0000
[104166.144471] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[08].ADDR=0x0000010300000194
[104166.144475] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[08].MISC0=0xd008000100000000
[104166.144479] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[08].IPID=0x0001c00136430400
[104166.144482] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[08].SYND=0x0000000000000c06
[104166.144973] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.144976] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[09].STATUS=0x8c204000003a0000
[104166.144980] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[09].ADDR=0x0000010300000194
[104166.144984] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[09].MISC0=0xd008000100000000
[104166.144988] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[09].IPID=0x0001c00136430400
[104166.144991] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[09].SYND=0x0000000000000c06
[104166.145345] amdgpu 0000:3d:00.0: {1}socket: 0, die: 3, 10 new correctable hardware errors detected in gfx block
[104166.145353] amdgpu 0000:3d:00.0: {1}socket: 0, die: 3, 10 correctable hardware errors detected in total in gfx block
[104166.160662] amdgpu 0000:5f:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.160666] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[104166.160670] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[104166.160674] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[104166.160678] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001600136430400
[104166.160682] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[104166.168692] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.168696] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[104166.168699] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[104166.168702] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[104166.168705] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001e00138430401
[104166.168708] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[104166.177251] amdgpu 0000:cd:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.177254] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xbaa000000008080b
[104166.177257] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[104166.177259] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[104166.177262] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0002502e1f001001
[104166.177264] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000000005d00000d
[104166.177557] amdgpu 0000:cd:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[104166.177559] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xfaa000000000080b
[104166.177561] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[104166.177564] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000200000000
[104166.177566] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001902e1f007901
[104166.177569] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x000000005d00b21a
```

---

### 评论 #14 — anthonix (2024-11-23T06:12:43Z)

And it just happened again on a different machine. 

Some of the STATUS bits are different:

`
[13850.912648] amdgpu 0000:1c:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[13850.927924] amdgpu 0000:42:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.927941] amdgpu 0000:42:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[13850.927950] amdgpu 0000:42:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[13850.927955] amdgpu 0000:42:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[13850.927960] amdgpu 0000:42:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001000138430400
[13850.927964] amdgpu 0000:42:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[13850.935971] amdgpu 0000:55:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.935975] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[13850.935980] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[13850.935983] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[13850.935987] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001300136430400
[13850.935991] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[13850.936280] amdgpu 0000:55:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.936283] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x98000800003e0000
[13850.936287] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[13850.936291] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000000000000
[13850.936294] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001300138430400
[13850.936298] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000000
[13850.936586] amdgpu 0000:55:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.936589] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[02].STATUS=0x98000800003e0000
[13850.936593] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[02].ADDR=0x0000000000000000
[13850.936596] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[02].MISC0=0xd008000000000000
[13850.936600] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[02].IPID=0x0001700136430400
[13850.936604] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[02].SYND=0x0000000000000000
[13850.936899] amdgpu 0000:55:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.936903] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[03].STATUS=0x98000800003e0000
[13850.936907] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[03].ADDR=0x0000000000000000
[13850.936910] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[03].MISC0=0xd008000000000000
[13850.936914] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[03].IPID=0x0001700138430400
[13850.936918] amdgpu 0000:55:00.0: {1}[Hardware Error]: aca entry[03].SYND=0x0000000000000000
[13850.952759] amdgpu 0000:9e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.952763] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xfaa0000000060808
[13850.952767] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[13850.952770] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[13850.952774] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x000061701b310101
[13850.952778] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000060715d000000
[13850.953027] amdgpu 0000:9e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.953031] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xfaa0000000060808
[13850.953034] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[13850.953038] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[13850.953042] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x000061701b510101
[13850.953045] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x000060715d000000
[13850.953294] amdgpu 0000:9e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.953297] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[02].STATUS=0xfaa0000000060808
[13850.953301] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[02].ADDR=0x0000000000000000
[13850.953305] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[02].MISC0=0xd008000100000000
[13850.953308] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[02].IPID=0x0000e1701b410101
[13850.953312] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[02].SYND=0x000060715d000000
[13850.953560] amdgpu 0000:9e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.953564] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[03].STATUS=0xfaa0000000060808
[13850.953567] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[03].ADDR=0x0000000000000000
[13850.953571] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[03].MISC0=0xd008000100000000
[13850.953575] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[03].IPID=0x0000e1701b610101
[13850.953578] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[03].SYND=0x000060715d000000
[13850.961545] amdgpu 0000:c2:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.961549] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[13850.961552] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[13850.961556] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[13850.961559] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001300138430401
[13850.961562] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[13850.961881] amdgpu 0000:c2:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.961885] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x98000800003e0000
[13850.961888] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[13850.961891] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000000000000
[13850.961895] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001700138430401
[13850.961898] amdgpu 0000:c2:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000000
[13850.962702] amdgpu 0000:d4:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.962705] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xbaa000000000080b
[13850.962708] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[13850.962711] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[13850.962714] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001102e1f007901
[13850.962717] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000000005d003f1b
[13850.963042] amdgpu 0000:d4:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.963045] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xbaa000000000080b
[13850.963048] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[13850.963051] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[13850.963054] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001902e1f007901
[13850.963057] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x000000005d00331b
[13850.963396] amdgpu 0000:d4:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.963399] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[02].STATUS=0xbaa000000008080b
[13850.963402] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[02].ADDR=0x0000000000000000
[13850.963405] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[02].MISC0=0xd008000100000000
[13850.963408] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[02].IPID=0x0002902e1f001201
[13850.963411] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[02].SYND=0x000000005d000017
[13850.971333] amdgpu 0000:e6:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.971336] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[13850.971339] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[13850.971341] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[13850.971344] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001000136430401
[13850.971346] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[13850.971583] amdgpu 0000:e6:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[13850.971585] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x98000800003e0000
[13850.971588] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[13850.971590] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000000000000
[13850.971592] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001400136430401
[13850.971595] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000000
[13850.972043] amdgpu 0000:1c:00.0: amdgpu: GPU reset begin!
`

---

### 评论 #15 — anthonix (2024-11-23T07:19:13Z)

And again, with slightly different ACA events logged:

`
[12841.580633] amdgpu 0000:bd:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[12841.596872] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.596888] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x8c204000003a0000
[12841.596896] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000010300000194
[12841.596901] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[12841.596906] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001c00136430400
[12841.596910] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000c06
[12841.597431] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.597435] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x8c204000003a0000
[12841.597440] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000010300000194
[12841.597444] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[12841.597448] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001c00136430400
[12841.597451] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000c06
[12841.597952] amdgpu 0000:3d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.597956] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].STATUS=0x8c204000003a0000
[12841.597959] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].ADDR=0x0000010300000194
[12841.597963] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].MISC0=0xd008000100000000
[12841.597967] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].IPID=0x0001c00136430400
[12841.597970] amdgpu 0000:3d:00.0: {1}[Hardware Error]: aca entry[02].SYND=0x0000000000000c06
[12841.598318] amdgpu 0000:3d:00.0: {1}socket: 0, die: 3, 3 new correctable hardware errors detected in gfx block
[12841.598325] amdgpu 0000:3d:00.0: {1}socket: 0, die: 3, 3 correctable hardware errors detected in total in gfx block
[12841.613652] amdgpu 0000:5f:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.613656] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[12841.613660] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[12841.613664] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[12841.613668] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001a00138430400
[12841.613672] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[12841.614476] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.614480] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xbaa000000000080b
[12841.614484] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[12841.614487] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[12841.614491] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001602e1f007901
[12841.614495] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000000005d00331b
[12841.614793] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.614797] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xbaa000000000080b
[12841.614801] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[12841.614804] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[12841.614808] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001a02e1f007901
[12841.614812] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x000000005d00331b
[12841.615110] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.615114] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].STATUS=0xbaa000000008080b
[12841.615118] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].ADDR=0x0000000000000000
[12841.615121] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].MISC0=0xd008000100000000
[12841.615125] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].IPID=0x0002a02e1f001201
[12841.615129] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[02].SYND=0x000000005d00004a
[12841.623153] amdgpu 0000:bd:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.623157] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[12841.623160] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[12841.623163] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[12841.623167] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001700136430401
[12841.623170] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[12841.631161] amdgpu 0000:cd:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[12841.631164] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[12841.631167] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[12841.631170] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[12841.631172] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001900136430401
[12841.631175] amdgpu 0000:cd:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[12841.639367] amdgpu 0000:bd:00.0: amdgpu: GPU reset begin!
`

---

### 评论 #16 — anthonix (2024-11-23T19:42:34Z)

And a couple more examples : 

`
[ 8390.785329] amdgpu 0000:68:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[ 8390.823777] amdgpu 0000:9e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 8390.823790] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[ 8390.823799] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 8390.823805] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[ 8390.823809] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001200136430401
[ 8390.823813] amdgpu 0000:9e:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[ 8390.839486] amdgpu 0000:d4:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 8390.839489] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[ 8390.839493] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 8390.839496] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[ 8390.839499] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001100136430401
[ 8390.839502] amdgpu 0000:d4:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[ 8390.840313] amdgpu 0000:e6:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 8390.840316] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xbaa000000008080b
[ 8390.840319] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 8390.840321] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[ 8390.840324] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0002802e1f001101
[ 8390.840327] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000000005d000041
[ 8390.840667] amdgpu 0000:e6:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 8390.840669] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xbaa000000000080b
[ 8390.840672] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[ 8390.840674] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[ 8390.840677] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001c02e1f007901
[ 8390.840680] amdgpu 0000:e6:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x000000005d002e1b
[ 8390.841160] amdgpu 0000:68:00.0: amdgpu: GPU reset begin!
`

and 


`
[ 6854.851268] amdgpu 0000:1b:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[ 6854.874278] amdgpu 0000:4e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.874295] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[ 6854.874303] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 6854.874308] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[ 6854.874313] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001300136430400
[ 6854.874318] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[ 6854.874613] amdgpu 0000:4e:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.874616] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x98000800003e0000
[ 6854.874620] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[ 6854.874623] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000000000000
[ 6854.874627] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001700136430400
[ 6854.874631] amdgpu 0000:4e:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000000
[ 6854.882672] amdgpu 0000:5f:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.882676] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[ 6854.882680] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 6854.882684] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[ 6854.882688] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001e00136430400
[ 6854.882692] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[ 6854.883003] amdgpu 0000:5f:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.883008] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0x98000800003e0000
[ 6854.883012] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[ 6854.883015] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000000000000
[ 6854.883019] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001e00138430400
[ 6854.883022] amdgpu 0000:5f:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x0000000000000000
[ 6854.883843] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.883846] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0xbaa000000000080b
[ 6854.883850] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 6854.883854] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000100000000
[ 6854.883858] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001602e1f007901
[ 6854.883861] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x000000005d00361b
[ 6854.884158] amdgpu 0000:9d:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.884163] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].STATUS=0xbaa000000000080b
[ 6854.884167] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].ADDR=0x0000000000000000
[ 6854.884170] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].MISC0=0xd008000100000000
[ 6854.884174] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].IPID=0x0001e02e1f007901
[ 6854.884178] amdgpu 0000:9d:00.0: {1}[Hardware Error]: aca entry[01].SYND=0x000000005d003a1b
[ 6854.892169] amdgpu 0000:bd:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.892173] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[ 6854.892177] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 6854.892180] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[ 6854.892184] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001700136430401
[ 6854.892187] amdgpu 0000:bd:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[ 6854.907881] amdgpu 0000:dd:00.0: {1}[Hardware Error]: Accelerator Check Architecture events logged
[ 6854.907884] amdgpu 0000:dd:00.0: {1}[Hardware Error]: aca entry[00].STATUS=0x98000800003e0000
[ 6854.907887] amdgpu 0000:dd:00.0: {1}[Hardware Error]: aca entry[00].ADDR=0x0000000000000000
[ 6854.907889] amdgpu 0000:dd:00.0: {1}[Hardware Error]: aca entry[00].MISC0=0xd008000000000000
[ 6854.907891] amdgpu 0000:dd:00.0: {1}[Hardware Error]: aca entry[00].IPID=0x0001400138430401
[ 6854.907894] amdgpu 0000:dd:00.0: {1}[Hardware Error]: aca entry[00].SYND=0x0000000000000000
[ 6854.908379] amdgpu 0000:1b:00.0: amdgpu: GPU reset begin!
`

---

### 评论 #17 — lhl (2024-11-24T07:23:03Z)

The past couple days I've been running some extended (14h+) `torchtune` runs that don't seem to have hangs. I wrote a simple [env output tool](https://github.com/shisa-ai/shisa-v2/blob/main/env-info.py) (inspired, but simplified vs vLLMs). Here's the torchtune environment:

```
++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

=== System Information ===
Os Info: Ubuntu 22.04.5 LTS
Kernel: Linux ENC1-CLS01-SVR14 6.8.0-49-generic #49~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Nov  6 17:42:15 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
Cpu Info: CPU: Intel(R) Xeon(R) Platinum 8470 (x208)
Memory Info: Total Memory: 2063707 MB

=== GPU Information ===
CUDA: Not found
ROCm: ROCM-SMI version: 2.3.1+e370dfa
ROCM-SMI-LIB version: 7.3.0
PyTorch CUDA Available: True
PyTorch CUDA Version: N/A
PyTorch HIP Version: 6.2.41133-dd7f95766

GPU Count: 8
GPU 0: AMD Instinct MI300X
GPU 1: AMD Instinct MI300X
GPU 2: AMD Instinct MI300X
GPU 3: AMD Instinct MI300X
GPU 4: AMD Instinct MI300X
GPU 5: AMD Instinct MI300X
GPU 6: AMD Instinct MI300X
GPU 7: AMD Instinct MI300X

=== Package Versions ===
triton: 3.1.0
torch: 2.5.1+rocm6.2
torchao: 0.6.1
transformers: 4.46.3
flash_attn: 2.7.0.post2
xformers: Not installed
deepspeed: Not installed
accelerate: 1.0.1
bitsandbytes: 0.44.1.dev+cd3cb68
axolotl: Not installed
torchtune: 0.4.0+cpu
```

I'm running the stable version of torch here, the only thing compiled from source is ROCm/flash_attn.

Note, I get an error if I try to run `compile: True` but it runs without. I also get an error if I try to use the `bitsandbytes.optim.PagedAdamW8bit` optimizer (not happy w/ FSDP it seems), so I just use `torch.optim.AdamW` which leads to an eventual OOM at bsz=8, but is fine for just trying to see if I can replicate a hang.

Note, torchtune was about 2X slower than axolotl for training, so I don't think it's really an option for actual use. Also, FSDP has had [historical training accuracy issues](https://github.com/huggingface/accelerate/issues/2624) - this was [finally identified as a difference in mixed precision behavior](https://huggingface.co/blog/deepspeed-to-fsdp-and-back) and the [behavior is fairly well documented now](https://huggingface.co/docs/accelerate/concept_guides/fsdp_and_deepspeed) but torchtune doesn't support this: https://pytorch.org/torchtune/stable/tutorials/memory_optimizations.html#model-precision

Anyway, it did make me wonder if this was a DeepSpeed specific issue, so I revisited axolotl to see if I could hang it by switching to FSDP. Despite carefully trying to port over the dsz3 config to fsdp, I ran into OOMs, so I'll include this just as a reference in case anyone is trying to go down this path:
```
# FSDP settings
deepspeed:
fsdp:
  - full_shard
  - auto_wrap

fsdp_config:
  fsdp_limit_all_gathers: true                    # Limit all-gather operations
  fsdp_sync_module_states: true                   # Synchronize module states across GPUs
  fsdp_offload_params: true                       # DSz3 doesn't doe this, but we OOM
  fsdp_use_orig_params: false                     # Not using torch.compile
  fsdp_cpu_ram_efficient_loading: true            # Efficient model loading
  fsdp_auto_wrap_policy: TRANSFORMER_BASED_WRAP   # Auto-wrap policy for transformer layers
  fsdp_transformer_layer_cls_to_wrap: LlamaDecoderLayer  # Replace with your model's layer class
  fsdp_state_dict_type: FULL_STATE_DICT           # Save full state dict for checkpoints
  fsdp_activation_checkpointing: true             # When using FSDP full shard, instead of using `gradient_checkpointing` in TrainingArguments, please use `activation_checkpointing` in `fsdp_config`. The forme
r introduces a redundant AllGather operation in backward pass. Reference: https://github.com/huggingface/transformers/issues/30404
  fsdp_sharding_strategy: FULL_SHARD              # Equivalent to DeepSpeed Zero Stage 3
  fsdp_backward_prefetch: BACKWARD_PRE            # Prefetching strategy
```
Anyway, one thing I did notice while reviewing the startup logs trying to get things working, I did see some things that might be related (or might not). In FSDP:

```
[rank0]:[W1124 07:06:04.499757541 ProcessGroupNCCL.cpp:1250] Warning: WARNING: process group has NOT been destroyed before we destruct ProcessGroupNCCL. On normal program exit, the application should call destroy_process_group to ensure that any pending NCCL operations have finished in this process. In rare cases this process can exit before this point and block the progress of another member of the process group. This constraint has always been present,  but this warning has only been added since PyTorch 2.4 (function operator())
```

And it turns out this is something that shows up when running axolotl for both FSDP and DeepSpeed configs, I get stuff like this for every GPU on startup:

```
[rank3]:[W1121 08:40:24.932363885 ProcessGroupNCCL.cpp:4393] [PG ID 0 PG GUID 0 Rank 3]  using GPU 3 to perform barrier as devices used by this process are currently unknown.
 This can potentially cause a hang if this rank to GPU mapping is incorrect. Specify device_ids in barrier() to force use of a particular device, or call init_process_group()
 with a device_id.
```

axolotl has barrier calls here (not many): https://github.com/search?q=repo%3Aaxolotl-ai-cloud%2Faxolotl%20barrier()&type=code and here is their main distributed helper code: https://github.com/axolotl-ai-cloud/axolotl/blob/main/src/axolotl/utils/distributed.py

If this is the issue this must be a difference in how NCCL vs RCCL handle things and how things are hipified? I have some upcoming deadlines and while I want to try some raw trl, or maybe lightning and see if there are mature, easier to replicate trainers can replicate the errors, maybe antonix's suggestion on nanogpt makes sense (will leave that to anyone trying to replicate, I'll probably just retreat to H100s to get my training work done since even in the best case, that seems to be better raw perf and price/perf) for my workflow.

---

### 评论 #18 — anthonix (2024-11-25T00:54:34Z)

I've seen the problem when using FSDP style (though not torchtune) and ZeRO stage 1 style (but not actually using deepspeed) parallelism on multi-node configurations.

@lhl have you seen this issue on single node training? I don't *think* I've seen it on a single node run..  

Also I'm wondering if you might need to wait much longer (in terms of wall clock time) to see the issue with FSDP torchtune, because the step time is much slower.

---

### 评论 #19 — lhl (2024-11-25T07:37:20Z)

@anthonix since I've only been testing on a single 8xMI300X node, actually *all* the errors I've posted/encountered so far are on a single node. It is also why I'm keen to see it replicated on different hw, but yeah, it being a long-running bug makes it hard/inefficient to poke at. I would be interested to hear if anyone w/ more MI300X hardware (say Meta, presumably using FSDP, or MS presumably using DeepSpeed have tried using training and run across similar errors).

---

### 评论 #20 — anthonix (2024-11-25T19:12:09Z)

Ahh ok. It seems with multi node the error is likely to happen sooner (in one case I've seen it after only ~1 hour on 4x nodes).

I'm very interested to find out what those Accelerator Check Architecture events decode as.. hopefully that helps get to the bottom of this. Any updates from someone at AMD on that? 

---

### 评论 #21 — jamesxu2 (2024-11-25T19:21:45Z)

@lhl @anthonix We have an internal decoder for those ACA events but it's unfortunately not something I can provide information on. It is definitely helpful that you've provided them however, so we can make comparisons to other error reports. The failure logs being shared in this thread point to a pretty diverse set of failures (e.g. The initial hang + GPU reset failure are distinct issues, but correlated), so this is quite challenging to debug, but I am trying a few things that you all have suggested in this thread.

Also if you don't mind, I may make some edits to the formatting of your comments so they don't appear in a single line. 



---

### 评论 #22 — anthonix (2024-11-25T19:27:55Z)

@jamesxu2 thanks.. can I ask why you are not able to share the documentation for the ACA events? It seems like it could be very helpful in solving this issue, or at least helping us work around it

---

### 评论 #23 — jamesxu2 (2024-11-25T19:58:17Z)

@anthonix The documentation itself is confidential and interpreting it would require a swath of confidential background information. However, I do appreciate your interest in helping to investigate, and the discussion here has been valuable to the investigation. 

---

### 评论 #24 — anthonix (2024-11-25T21:21:01Z)

Oh :( Well if then ACA STATUS bits are confidential, how about I make some guesses at diagnostic tests that might be useful to run on my side, and you can look at the documentation for me, and give a thumbs up or thumbs down (sort of like charades). Quite keen to get to the bottom of this, given that we have a bunch of MI300x machines sitting idle.

1. Would it be worthwhile to do a training run with any of the CG and/or PG chicken bits enabled? (i.e., deassert various bits in cg_mask and/or pg_mask)? 

---

### 评论 #25 — anthonix (2024-11-26T20:44:03Z)

@lhl I've been running some single node runs in parallel to test some theories.. so far I can confirm I also see the faults on a single node

---

### 评论 #26 — Snektron (2024-11-27T21:27:26Z)

I've encountered this on a MI300X node while running rocPRIM benchmarks in the past weeks. Unfortunately I don't have any logs, this instance didn't allow me to access dmesg.

---

### 评论 #27 — jon-hotaisle (2024-11-28T01:15:00Z)

Update: AMD is looking into this internally. Hopefully we know more soon.

---

### 评论 #28 — anthonix (2024-11-29T22:45:16Z)

Another ATHUB uncorrectable hardware error, but this one is a little different to the others I've seen so far, and went on to cause kernel panic in the amdgpu driver when tried to reboot: 

EDIT: attached a txt of the dmesg because newlines getting screwed up
[crash.txt](https://github.com/user-attachments/files/17963389/crash.txt)


```
[126737.160982] amdgpu 0000:9e:00.0: amdgpu: qcm fence wait loop timeout expired. 
[126737.161007] amdgpu 0000:9e:00.0: amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption. 
[126737.161022] amdgpu: Failed to evict process queues
[126737.162652] amdgpu 0000:9e:00.0: amdgpu: GPU reset begin!
[126746.021168] amdgpu 0000:1c:00.0: amdgpu: qcm fence wait loop timeout expired
[126746.021188] amdgpu 0000:1c:00.0: amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[126746.021201] amdgpu: Failed to evict process queues
[126746.165170] amdgpu 0000:c2:00.0: amdgpu: qcm fence wait loop timeout expired
[126746.165192] amdgpu 0000:c2:00.0: amdgpu: The cp might be in an unrecoverable state due to an unsuccessful queues preemption
[126746.165208] amdgpu: Failed to evict process queues
[126748.505383] amdgpu 0000:e6:00.0: {1}uncorrectable hardware error(ERREVENT_ATHUB_INTERRUPT) detected!
[126748.505401] {1}[Hardware Error]: Hardware error from APEI Generic Hardware Error Source: 5
[126748.505423] {1}[Hardware Error]: event severity: recoverable
[126748.505435] {1}[Hardware Error]:  Error 0, type: fatal
[126748.505446] {1}[Hardware Error]:   section_type: PCIe error
[126748.505455] {1}[Hardware Error]:   port_type: 5, upstream switch port
[126748.505466] {1}[Hardware Error]:   version: 3.0
[126748.505476] {1}[Hardware Error]:   command: 0x0007, status: 0x0010
[126748.505486] {1}[Hardware Error]:   device_id: 0000:99:00.0
[126748.505495] {1}[Hardware Error]:   slot: 0
[126748.505502] {1}[Hardware Error]:   secondary_bus: 0x9a
[126748.505511] {1}[Hardware Error]:   vendor_id: 0x1000, device_id: 0xc030
[126748.505522] {1}[Hardware Error]:   class_code: 060400
[126748.505531] {1}[Hardware Error]:   bridge: secondary_status: 0x4000, control: 0x0003
[126748.505540] {1}[Hardware Error]:   aer_uncor_status: 0x00004000, aer_uncor_mask: 0x03810000
[126748.505551] {1}[Hardware Error]:   aer_uncor_severity: 0x004ef030
[126748.505558] {1}[Hardware Error]:   TLP Header: 00000000 00000000 00000000 00000000
[126748.505568] {1}[Hardware Error]:  Error 1, type: fatal
[126748.505575] {1}[Hardware Error]:   section_type: PCIe error
[126748.505583] {1}[Hardware Error]:   port_type: 6, downstream switch port
[126748.505591] {1}[Hardware Error]:   version: 3.0
[126748.505598] {1}[Hardware Error]:   command: 0x0007, status: 0x0010
[126748.505607] {1}[Hardware Error]:   device_id: 0000:9a:01.0
[126748.505614] {1}[Hardware Error]:   slot: 25
[126748.505620] {1}[Hardware Error]:   secondary_bus: 0x9c
[126748.505627] {1}[Hardware Error]:   vendor_id: 0x1000, device_id: 0xc030
[126748.505635] {1}[Hardware Error]:   class_code: 060400
[126748.505642] {1}[Hardware Error]:   bridge: secondary_status: 0x0000, control: 0x0003
[126748.505651] {1}[Hardware Error]:   aer_uncor_status: 0x00004000, aer_uncor_mask: 0x03a10000
[126748.505662] {1}[Hardware Error]:   aer_uncor_severity: 0x044ef030
[126748.505670] {1}[Hardware Error]:   TLP Header: 00000000 00000000 00000000 00000000
[126748.505776] pcieport 0000:99:00.0: AER: aer_status: 0x00004000, aer_mask: 0x03810000
[126748.505789] pcieport 0000:99:00.0:    [14] CmpltTO                (First)
[126748.505798] pcieport 0000:99:00.0: AER: aer_layer=Transaction Layer, aer_agent=Requester ID
[126748.505809] pcieport 0000:99:00.0: AER: aer_uncor_severity: 0x004ef030
```

---

### 评论 #29 — jamesxu2 (2024-12-11T21:20:38Z)

Hi @anthonix and @lhl, I just wanted to provide an update from our side and some more questions. 

We've been chasing the reproduction of this issue for the past few weeks but have been unable to induce the ERREVENT_ATHUB_INTERRUPT that you are reporting. We've tried with your suggested workloads - Axolotl finetuning of llama models and nanogpt, over several multi-hour and multi-day runs, and have not been successful in observing the failure. Thank you for your error logs and setup descriptions so far.

That said, a few questions:

1. What version of axolotl are you using? 
2. Did you make any modifications to its dependencies as listed in its requirements.txt?
3. Can you provide the output of pip freeze so we can see your installed python package versions?
4. Do you run into this issue with finetuning of all llama models you've tried (ie. with 8B models) or is it only with the 70B+ models? As you have also experienced, there are many conditions in which we run into device OOM. 
5. Are both of you experiencing this on HotAisle's MI300X servers?
6. If yes to (5), which HTA server did you experience the crash on? 

Thanks!

---

### 评论 #30 — YangWang92 (2024-12-12T09:29:00Z)

I encountered a similar issue with the Mi300x, where flash_attention + vLLM triggers a problem.
```
[5615152.198602] gmc_v9_0_process_interrupt: 6 callbacks suppressed
[5615152.198606] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.204726] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.210841] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344600000 from IH client 0x1b (UTCL2)
[5615152.216978] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 2 fault from die AID0.XCD1
[5615152.221281] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.227441] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.233333] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344601000 from IH client 0x1b (UTCL2)
[5615152.239272] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 2 fault from die AID0.XCD1
[5615152.243534] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.248754] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.254814] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344600000 from IH client 0x1b (UTCL2)
[5615152.261053] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 6 fault from die AID1.XCD1
[5615152.265526] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.271064] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.277062] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344600000 from IH client 0x1b (UTCL2)
[5615152.283128] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 5 fault from die AID1.XCD0
[5615152.287808] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.293190] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.299148] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344600000 from IH client 0x1b (UTCL2)
[5615152.305222] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 14 fault from die AID3.XCD1
[5615152.309822] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.315173] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.321374] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344600000 from IH client 0x1b (UTCL2)
[5615152.327733] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 13 fault from die AID3.XCD0
[5615152.332752] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.338147] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.344255] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344601000 from IH client 0x1b (UTCL2)
[5615152.350799] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 6 fault from die AID1.XCD1
[5615152.355293] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.360854] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.367219] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344601000 from IH client 0x1b (UTCL2)
[5615152.373287] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 5 fault from die AID1.XCD0
[5615152.377998] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.383891] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.389881] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344601000 from IH client 0x1b (UTCL2)
[5615152.396344] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 14 fault from die AID3.XCD1
[5615152.400839] amdgpu 0008:00:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32850)
[5615152.406820] amdgpu 0008:00:00.0: amdgpu:  for process pt_main_thread pid 1200233 thread pt_main_thread pid 1200233)
[5615152.413606] amdgpu 0008:00:00.0: amdgpu:   in page starting at address 0x00007ed344601000 from IH client 0x1b (UTCL2)
[5615152.419710] amdgpu 0008:00:00.0: amdgpu:   cookie node_id 13 fault from die AID3.XCD0
```

---

### 评论 #31 — anthonix (2024-12-12T13:31:33Z)

For my case, after not seeing any faults for a week or so..  I got the fault again today. After several reboots I realized it was now easily repeatable and occurred within a few mins every time. I then looked at the code I had changed earlier, found a bug, fixed it, and now I haven't seen the fault for hours.

As for @lhl's case, @jamesxu2 I noticed you were using different versions of PyTorch compared to what @lhl mentioned above -- I think that may be a crucial detail in replicating his case, but in general to most quickly replicate you will probably need to ensure every SW component is either the same version if @lhl had downloaded it, or built in the same way if he built it from source.

And AMD, can you *please* do something about the withheld documentation for these ACA codes so that folks might not have to go through this in future?

Thanks, and good luck everyone. 

---

### 评论 #32 — jamesxu2 (2024-12-12T15:13:15Z)

Hi @anthonix, thanks for the update. 

I would still appreciate answers to the questions I asked, especially which hotaisle server (ENC**X**-CLS**Y**-SVR**Z**) you've encountered those faults on. 

>  in general to most quickly replicate you will probably need to ensure every SW component is either the same version [...]

Thanks for the advice, we've tried several different setups and we can try fixing the Python version to 3.12 if you think that's a critical detail. It would help us if you and @lhl provided the output of **pip freeze** from a faulting configuration to help us identify all the python dependencies. 

> And AMD, can you please do something about the withheld documentation for these ACA codes so that folks might not have to go through this in future?

I'm sorry but those ACA codes are designed for internal debug use only. They're not releasable at the moment, and they would not be interpretable anyways without extensive training and access to confidential information. We appreciate that you've shared them and they have been looked at internally to improve our understanding of the failure.  

@lhl, I notice inside the https://github.com/AUGMXNT/MI300-testing repo, you've listed a few system setup files and notebooks with the error log. From those, I see possible use of **ENC1-CLS01-SVR09** and **ENC1-CLS01-SVR14**, but I'm unable to correlate that to the [crash log](https://github.com/AUGMXNT/MI300-testing/blob/main/train-axolotl-llama3-8b.ipynb) you provided with the llama3.1-8b fine tuning result. Can you clarify on which server(s) you've encountered the ERREVENT_ATHUB_INTERRUPT faults?

I am particularly interested in the identity of the server(s?) encountering the fault from these comments.

1. https://github.com/ROCm/ROCm/issues/4021#issuecomment-2495633620
2. https://github.com/ROCm/ROCm/issues/4021#issuecomment-2492831692
3. https://github.com/ROCm/ROCm/issues/4021#issuecomment-2484684263
4. The original issue report 




---

### 评论 #33 — lhl (2024-12-12T16:57:45Z)

Hey @jamesxu2 , maybe @jon-hotaisle can help confirm/coordinate, but my understanding was that the keys were handed over so to speak for ENC1-CLS01-SVR14 a week or so ago so that the right people could take a look directly on the system? If you're that person and don't have access to it, maybe you can chat w/ Jon/Clint directly? I left a `README-replicate-crashes.txt` to make it easier, but basically since everything is exactly installed as is, you can just activate the mamba env, and run the training in place and see what pops out directly. (SRV9 had different errors that were diagnosed as faulty hardware and replaced, I moved over to SRV14 to continue testing, which was fine for inference, but well, this issue). I have a `20241103-memory-errors` folder w/ some dumps and you can page through `journalctl` - there are a lot of boots because I the GPUs constantly would get in a state.

This potentially being exacerbated by Python 3.12 is intriguing (the axolotl venv is using 3.12.7). Obviously lots of moving parts everywhere. 

(I'm running uh, actual training runs on H100s atm so my time to assist w/ debugging will be a bit limited, but it would be nice revisit if this can get nailed down since the original goal was to [do a writeup like my inferencing one](https://shisa.ai/blog/posts/tuning-vllm-mi300x/), and it'd be nice to be able to have a some more interesting things to say).

---

### 评论 #34 — anthonix (2024-12-12T20:54:54Z)

@jamesxu2 I've seen the fault on all 4 machines I've used -- which includes the two I handed over to you (SRV12 and SRV13). I saw SRV12 and SRV13 experience the fault (with my buggy code) mere hours before I handed them over to you, and thats why I chose those two for you to investigate.

Same four machines have been running all night (with my debugged code) and still no faults. 

EDIT: sorry in my last post I meant say *PyTorch* version.. not Python version

Good luck.

---

### 评论 #35 — jamesxu2 (2024-12-12T21:23:13Z)

@anthonix @lhl, thanks for the update and information. I'll let you know when we know more. 

---

### 评论 #36 — jamesxu2 (2025-01-08T21:49:01Z)

This issue has been assessed with the help of HotAisle, @lhl and @anthonix, and we have resolved it internally. 

---

### 评论 #37 — lhl (2025-01-09T04:38:14Z)

Great news! Can you give an ETA/target for when the issue will be resolved/available for production use?

---

### 评论 #38 — philip-essential (2025-02-12T19:26:40Z)

Hi @jamesxu2, I've seen a `GPU Hang` error a couple times on a different training stack on ROCm 6.3.1.  I don't know if it's the same issue, but is the fix for this out yet?  Should I expect the issue to be resolved by upgrading to 6.3.2?

---

### 评论 #39 — rootfs (2026-02-04T14:36:16Z)

@jamesxu2 I am using  `rocm/pytorch:latest` container image, but hit error below, is there a solution to this? thanks.

# Env
8 x AMD Instinct MI300X

# Dump
```
GPU coredump: execvp failed: No such file or directory
Failed to write segment data to pipe: Success
GPU coredump: handler exited with error (status: 1)
GPU core dump failed
Kernel Name: _ZN2at6native24vectorized_gather_kernelILi16ElEEvPcS2_PT0_illllb
VGPU=0x770de882f5b0 SWq=0x774e03e1e000, HWq=0x770df0200000, id=4
        Dispatch Header =0xb02 (type=2, barrier=1, acquire=1, release=1), setup=0
        grid=[196608, 1, 1], workgroup=[192, 1, 1]
        private_seg_size=0, group_seg_size=0
        kernel_obj=0x774dfb6d9100, kernarg_address=0x0x770ccc70ed00
        completion_signal=0x0, correlation_id=0
        rptr=65751, wptr=65956
 Kernel Name: _ZN2at6native24vectorized_gather_kernelILi16ElEEvPcS2_PT0_illllb
VGPU=0x1e5146a0 SWq=0x774e03e1e000, HWq=0x770df0200000, id=4
        Dispatch Header =0xb02 (type=2, barrier=1, acquire=1, release=1), setup=0
        grid=[196608, 1, 1], workgroup=[192, 1, 1]
        private_seg_size=0, group_seg_size=0
        kernel_obj=0x774dfb6d9100, kernarg_address=0x0x770ccc70ed00
        completion_signal=0x0, correlation_id=0
        rptr=65751, wptr=65956
 :0:rocdevice.cpp            :3586: 2616203620 us:  Callback: Queue 0x770df0200000 aborting with error : HSA_STATUS_ERROR_EXCEPTION: An HSAIL operation resulted in a hardware exception. code: 0x1016
W0204 18:37:05.094000 1 torch/distributed/elastic/multiprocessing/api.py:908] Sending process 114 closing signal SIGTERM
```

---

### 评论 #40 — schung-amd (2026-02-04T19:28:54Z)

Hi @rootfs, can you submit a new issue for that? This one is over a year old and may not be relevant. Ping me once you've done that and we'll take a look.

---

### 评论 #41 — rootfs (2026-02-04T21:00:27Z)

@schung-amd sure, will do. Per my limited debug, it looks GPU-to-GPU communication caused the transient error.

---

### 评论 #42 — rootfs (2026-02-05T14:32:05Z)

@schung-amd actually the problem went away after i used f32 and bp16 mixed precision and fix a data shard corruption issue on my end. The [model](https://huggingface.co/llm-semantic-router/multi-modal-embed-small) finished successfully

---

### 评论 #43 — schung-amd (2026-02-05T15:03:12Z)

Great, glad to hear. Feel free to submit a new issue if you encounter any further problems.

---
