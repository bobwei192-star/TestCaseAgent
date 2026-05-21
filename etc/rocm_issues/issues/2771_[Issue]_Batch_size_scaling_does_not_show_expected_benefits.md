# [Issue]: Batch size scaling does not show expected benefits

> **Issue #2771**
> **状态**: closed
> **创建时间**: 2023-12-28T00:29:35Z
> **更新时间**: 2024-03-02T04:47:29Z
> **关闭时间**: 2024-03-02T04:47:29Z
> **作者**: xelibrion
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2771

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I'm training a [FastSpeech2](https://github.com/ming024/FastSpeech2) model on my 7900 XTX, using the latest `rocm/pytorch:rocm6.0_ubuntu22.04_py3.9_pytorch_2.0.1` docker image.

What I've noticed is that increasing batch size does not necessarily translate to shorter epoch times. Adding simple instrumentation showed that increasing batch size has also increased time required to compute each of the steps in the pipeline. 

Times for all of `forward_pass`, `calc_loss` and `backward_pass` have lengthened. 
For `forward_pass` and `calc_loss` roughly inline with batch size increase (`4x`), and for `backward_pass` increase was `6x`! 

Is this expected behaviour?

Batch size = 16
![time_taken_batch_size_16](https://github.com/ROCm/ROCm/assets/175334/8240cf13-d914-48dd-aae2-6d9cb203edd6)

Batch size = 64
![time_taken_batch_size_64](https://github.com/ROCm/ROCm/assets/175334/6db23bac-e624-4c54-b719-086ad39b12b9)



### Operating System

Gentoo Linux (kernel 6.6.8)

### CPU

AMD Ryzen 9 3900X 12-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### Other

_No response_

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
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
  Name:                    AMD Ryzen 9 3900X 12-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 3900X 12-Core Processor
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
  Max Clock Freq. (MHz):   3800
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32790352(0x1f45750) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32790352(0x1f45750) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32790352(0x1f45750) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1100
  Uuid:                    GPU-f002f7e2741b7d34
  Marketing Name:          AMD Radeon RX 7900 XTX
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
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29772(0x744c)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2482
  BDFID:                   4096
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 528
  SDMA engine uCode::      19
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS:
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1100
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

_No response_

---

## 评论 (5 条)

### 评论 #1 — smalekta (2024-01-11T15:07:44Z)

@xelibrion  - Thanks for opening this github issue. I tried training [FastSpeech2](https://github.com/ming024/FastSpeech2) model on 7900XTX (also on W7900) + latest rocm/pytorch docker and I do not see any `performance inversion`.
(Increasing the batch size from 16 to 64 increases the throughput and reduces the epoch elapsed time, as expected)

Batch size = 16
![image](https://github.com/ROCm/ROCm/assets/144711992/b1338538-4ab4-4913-9da0-a8b92adf529d)

Batch size = 64
![image](https://github.com/ROCm/ROCm/assets/144711992/5a8225f2-4276-46b3-bb9c-41cad6632f3e)

Can you please provide the exact steps/instructions (and any modified/instrumented code you used) for us to repro your result? 

Thanks

---

### 评论 #2 — xelibrion (2024-01-12T12:20:02Z)

@smalekta thanks for looking into this. I published my changes at https://github.com/xelibrion/FastSpeech2

The issue I see is that you have quite a low baseline for epoch times in the screenshot for `batch_size = 16`. 
This is what I observe:
![Rocm_16](https://github.com/ROCm/ROCm/assets/175334/7963d1b1-0e7c-49f6-b81f-361a1447373c)

As you might notice, the run time for the first epoch is roughly inline with what you see, but then it quickly drops until it settles around 3 minute mark. 

Compare it with the screenshot for `batch_size = 64`, and you see the same (or in fact slightly longer) run times of around 3 minutes. Therefore we did not get any benefit at all from increasing batch size, epoch still takes the same amount of time to compute. 
![ROCM_64b](https://github.com/ROCm/ROCm/assets/175334/f90c5434-141a-4111-8f35-6570865f0f6f)



---

### 评论 #3 — vstempen (2024-02-22T23:17:39Z)

To take performance advantage of larger batches, hardware must have enough resources for command processor to dispatch all the queued kernels for parallel processing. In case of Navi31, larger number of dispatched kernels will just stay longer in HW queue. For experiment we tried to run FastSpeech2 training on 3 different platforms:
Navi31, 
  Number of GPUs:       1
Per GPU:
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
Observation:
Batch16 training is almost always overperforming Batch64, some epochs have similar durations.

MI300,
Number of GPUs:        1
Per GPU:
  Compute Unit:            240
  SIMDs per CU:            4
  Shader Engines:          24
Observation:
Batch64 only overperforming Batch16 when executing convolution kernels. Then epoch durations are almost the same. 

MI300,
Number of GPUs:    4
Per GPU:
  Compute Unit:            228
  SIMDs per CU:            4
  Shader Engines:          24
Observation:
Batch64 training is always overperforming Batch16.


As for much lower performance for first few epochs, during first time training some time-consuming convolution kernels are executed. During that MIOpen creates Find-Db database, where convolution data gets cached, which drastically increases performance for later epochs. 

https://rocm.docs.amd.com/projects/MIOpen/en/docs-5.0.2/finddb.html 
https://rocm.docs.amd.com/projects/MIOpen/en/docs-5.0.2/perfdatabase.html 

So, using batch16 for FastSpeech2 training on Navi31 is preferable, and you should not expect higher performance using batches with larger sizes.


































































































































































































































































































































































































































































































































































































































































































































































































---

### 评论 #4 — nartmada (2024-03-02T04:37:21Z)

Hi @xelibrion, it is an expected behavior.  You should not expect higher performance using batches with larger sizes. 

---

### 评论 #5 — xelibrion (2024-03-02T04:47:17Z)

@vstempen thank you for the detailed explanation, closing the issue now.

---
