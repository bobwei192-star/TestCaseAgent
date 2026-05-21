# [Issue]: Poor performance with OpenCL host-side command queues with more then one GPU when profiling is enabled . 

> **Issue #3357**
> **状态**: closed
> **创建时间**: 2024-06-25T20:07:27Z
> **更新时间**: 2025-07-08T19:57:38Z
> **关闭时间**: 2025-07-08T19:57:38Z
> **作者**: andrerenard
> **标签**: Under Investigation, ROCm 6.0.0, AMD Instinct MI100
> **URL**: https://github.com/ROCm/ROCm/issues/3357

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Instinct MI100** (颜色: #ededed)

## 描述

### Problem Description

I've run into an interesting problem with OpenCL host-side command queues when profiling is enabled _and_ more then one GPU is used. 

Some background: 
* My application uses 3 command queues for each GPU, one for host->device, one for kernels, one for device->host.  
* I have two CPUs and two GPUs in the system.  Each GPU is on it's own NUMA domain (CPU). 

If I run with just one of the two GPUs (doesn't matter which one), then everything works as expected with profiling enabled or disabled.   However, when using both GPUs simultaneously, enabling profiling causes a performance regression.    Specifically there appear to be large delays when queueing operations on the GPU, resulting in lots of dead time on the GPU. 

The summary of configurations is:
```
GPU 1 only with profiling enabled: works as expected. 
GPU 2 only with profiling enabled: works as expected.
GPU 1 and 2 with profiling enabled: queuing is delayed.
GPU 1 and 2 with profiling disabled: works as expected.
```

I'm creating the profiling enabled command queues using: 
```
cl_queue_properties properties[] = { CL_QUEUE_PROPERTIES, CL_QUEUE_PROFILING_ENABLE, 0};
queue[i] = clCreateCommandQueueWithProperties(context, device_id, properties, &err);
``` 
And without profiling using:
```
cl_queue_properties properties[] = { CL_QUEUE_PROPERTIES, 0, 0};
queue[i] = clCreateCommandQueueWithProperties(context, device_id, properties, &err);
```
Each GPU is managed by it's own set of threads, so the above code is used to generate 3 queues for each GPU. 


I haven't been able to upload the rocprof traces since they are too big, but here is a screen shot of what I'm seeing with profiling disabled and two GPUs (expected result):
<img width="1677" alt="image" src="https://github.com/ROCm/ROCm/assets/597324/b510bdfc-63ef-44d8-9318-3158575f7d65">
And with two GPUs and profiling enabled (unexpected result):
<img width="1678" alt="image" src="https://github.com/ROCm/ROCm/assets/597324/ec0c9ef0-eefe-4112-83ba-01312684b071">
With only one GPU and profiling enabled everything work fine: 
<img width="1678" alt="image" src="https://github.com/ROCm/ROCm/assets/597324/2c8a1b1f-ba01-4a26-9bbe-f9bdc65cc551">

It's feels like there is some resource shared between the GPUs at the driver level that results in stalls in the host-side queues.  Although I haven't been able to confirm this.   

I'm able to work around this by simply disabling profiling, but that's slightly inconvenient, since I like to track copy/kernel average completion times to tune the power profiles. 

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

AMD EPYC 7402 24-Core Processor (2P configuration)

### GPU

AMD Instinct MI100

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD EPYC 7402 24-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7402 24-Core Processor
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
  Max Clock Freq. (MHz):   2800
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
      Size:                    528220356(0x1f7c00c4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    528220356(0x1f7c00c4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    528220356(0x1f7c00c4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    AMD EPYC 7402 24-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 7402 24-Core Processor
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
  Max Clock Freq. (MHz):   2800
  BDFID:                   0
  Internal Node ID:        1
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    1056952328(0x3effd008) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    1056952328(0x3effd008) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    1056952328(0x3effd008) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 3
*******
  Name:                    gfx908
  Uuid:                    GPU-84ba779eceead603
  Marketing Name:          AMD Instinct MI100
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
  Chip ID:                 29580(0x738c)
  ASIC Revision:           2(0x2)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1502
  BDFID:                   17152
  Internal Node ID:        2
  Compute Unit:            120
  SIMDs per CU:            4
  Shader Engines:          8
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
  Packet Processor uCode:: 65
  SDMA engine uCode::      18
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    33538048(0x1ffc000) KB
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
*******
Agent 4
*******
  Name:                    gfx908
  Uuid:                    GPU-866e2aee769e1c8b
  Marketing Name:          AMD Instinct MI100
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
  Chip ID:                 29580(0x738c)
  ASIC Revision:           2(0x2)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1502
  BDFID:                   41728
  Internal Node ID:        3
  Compute Unit:            120
  SIMDs per CU:            4
  Shader Engines:          8
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
  Packet Processor uCode:: 65
  SDMA engine uCode::      18
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    33538048(0x1ffc000) KB
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

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — andrerenard (2024-06-25T21:22:33Z)

I can confirm this issue exists with ROCm version 6.1.2-119 as well. 

---

### 评论 #2 — ppanchad-amd (2024-07-17T15:25:47Z)

@andrerenard Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — jamesxu2 (2024-07-18T19:38:09Z)

Hi @andrerenard , can you ideally provide some code to reproduce the issue or capture a smaller profile JSON/pftrace and upload it? There isn't an obvious answer to why this slowdown occurs, and while some performance hit is expected with profiling, it is interesting that it manifests in this strange scheduling behaviour.

> It's feels like there is some resource shared between the GPUs at the driver level that results in stalls in the host-side queues. Although I haven't been able to confirm this.

I think this is a good guess, though it's hard to confirm with the information I have so far.  For the "not working" screenshot, it looks almost like the _corr.kd_ blocks are scheduled serially instead of in parallel indicating potentially some cross-GPU dependency/locking, though this may be a byproduct of something scheduling them as such when profiling is on.

Additionally, how are you collecting rocprof traces? I don't believe [rocprof can profile OpenCL kernels](https://github.com/ROCm/ROCm/issues/1100) but you clearly have captured them in your screenshots.





---

### 评论 #4 — andrerenard (2024-07-18T20:20:20Z)

I'm running rocprof with the following command: 
```
rocprof --tool-version 1  --hsa-trace <command>
``` 
It's not ideal for OpenCL, but it does get at the underlying HSA layer which is better than nothing. 

It'll be hard to get a small enough trace file, since the application has a long startup sequence.  So instead I've uploaded the json files here: 
- Unexpected result (profile enabled): https://drive.google.com/file/d/16shbxmZCDvuXnDRVzmBf7e8DAES3avbX/view?usp=sharing
- Expected result (profile disabled): https://drive.google.com/file/d/16sU0x5MHzyUUHJBewl69DGW4u-wzf6mK/view?usp=sharing

I should note I've also tried disabling all calls related to collecting profiling data, but it still has issues.  Only the initial `CL_QUEUE_PROFILING_ENABLE` flag makes a difference. 

I'll have to work on producing a code which can reproduce this issue in a way you can run it, it's all open source, but at the moment the code requires being connected to a bunch of custom FPGAs over the network.  I'll have to adjust things to use locally generated simulated input data.

---

### 评论 #5 — ppanchad-amd (2025-05-29T15:38:51Z)

Hi @andrerenard. Can you please check if you are still running into this issue with the latest ROCm stack? If you are, please provide us a code that can reproduce this issue. Thanks!

---

### 评论 #6 — schung-amd (2025-07-08T19:57:38Z)

Closing for now due to lack of response. If you're still seeing this with current ROCm versions feel free to comment with code to reproduce this and we can reopen if necessary.

---
