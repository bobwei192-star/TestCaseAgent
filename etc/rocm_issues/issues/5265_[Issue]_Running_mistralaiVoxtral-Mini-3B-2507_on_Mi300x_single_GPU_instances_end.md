# [Issue]: Running mistralai/Voxtral-Mini-3B-2507 on Mi300x single GPU instances ends up consuming 174GB of VRAM

> **Issue #5265**
> **状态**: closed
> **创建时间**: 2025-09-06T23:20:18Z
> **更新时间**: 2025-10-14T19:19:07Z
> **关闭时间**: 2025-10-14T19:19:07Z
> **作者**: hardiksd
> **标签**: Under Investigation, status: triage, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5265

## 标签

- **Under Investigation** (颜色: #0052cc)
- **status: triage** (颜色: #585dd7)
- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem Description

When using Voxtral using vllm serve 172GB of VRAM ends up getting consumed. The expectation should be around 30GB.



### Operating System

NAME="Ubuntu" VERSION="22.04.5 LTS (Jammy Jellyfish)"

### CPU

 INTEL(R) XEON(R) PLATINUM 8568Y+

### GPU

AMD Instinct MI300X VF

### ROCm Version

 rocm/vllm:rocm6.4.1_vllm_0.10.0_20250812

### ROCm Component

_No response_

### Steps to Reproduce

Step 1 - Install vllm enabled rocm docker container.
Step 2 - setup vllm and install vllm audio
Step 3 - serve voxtral using vllm. 

vllm serve mistralai/Voxtral-Mini-3B-2507 --tokenizer_mode mistral --config_format mistral --load_format mistral

Run transcription using the transcription end point on a 15 mins audio file.



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

root@snapshots-gpu-mi300x1-192gb-devcloud-atl1:~# /opt/rocm/bin/rocminfo --support
ROCk module version 6.12.12 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    INTEL(R) XEON(R) PLATINUM 8568Y+
  Uuid:                    CPU-XX
  Marketing Name:          INTEL(R) XEON(R) PLATINUM 8568Y+
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
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            20
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    247409340(0xebf2abc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    247409340(0xebf2abc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    247409340(0xebf2abc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    247409340(0xebf2abc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx942
  Uuid:                    GPU-56400332e6997d76
  Marketing Name:          AMD Instinct MI300X VF
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
    L1:                      32(0x20) KB
    L2:                      4096(0x1000) KB
    L3:                      262144(0x40000) KB
  Chip ID:                 29877(0x74b5)
  ASIC Revision:           1(0x1)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2100
  BDFID:                   33536
  Internal Node ID:        1
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
  Packet Processor uCode:: 177
  SDMA engine uCode::      24
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    200998912(0xbfb0000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    200998912(0xbfb0000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    200998912(0xbfb0000) KB
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
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx9-4-generic:sramecc+:xnack-
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

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-09-08T13:50:41Z)

Hi @hardiksd. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — zichguan-amd (2025-09-23T20:15:41Z)

> The expectation should be around 30GB.

Hi @hardiksd, can you provide more backgrounds on this number? The [model card](https://huggingface.co/mistralai/Voxtral-Mini-3B-2507) states

> Note: Running Voxtral-Mini-3B-2507 on GPU requires ~9.5 GB of GPU RAM in bf16 or fp16.

and I'm observing the right number `Model loading took 8.8672 GiB and 20.429927 seconds`.

Also note that vllm will try to utilize the full amount of memory given, see https://github.com/vllm-project/vllm/issues/8504 and https://docs.vllm.ai/en/latest/cli/serve.html#-gpu-memory-utilization. Default value being 0.9 so vllm will use ~192 GB * 0.9 = 172.8 GB, which is the number you are observing.

---

### 评论 #3 — zichguan-amd (2025-10-14T19:19:07Z)

Closing this out due to lack of activity, please let me know if you still have any questions or concerns and I can reopen the issue.

---
