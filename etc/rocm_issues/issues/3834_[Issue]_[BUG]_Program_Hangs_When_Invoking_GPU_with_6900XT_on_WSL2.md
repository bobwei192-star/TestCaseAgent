# [Issue]: [BUG] Program Hangs When Invoking GPU with 6900XT on WSL2

> **Issue #3834**
> **状态**: closed
> **创建时间**: 2024-09-29T05:37:03Z
> **更新时间**: 2024-09-29T06:03:25Z
> **关闭时间**: 2024-09-29T06:03:25Z
> **作者**: Titianzi
> **标签**: AMD Radeon Pro W6800, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3834

## 标签

- **AMD Radeon Pro W6800** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

WSL2 Linux Env：
-------------------------------

> OS: NAME="Ubuntu"
> VERSION="22.04.5 LTS (Jammy Jellyfish)"
> Kernel Version: 5.15.153.1-microsoft-standard-WSL2
> CPU: 
> model name      : AMD Ryzen 9 3900X 12-Core Processor
> GPU:
> Name:                    gfx1030
> Marketing Name:          AMD Radeon RX 6900 XT
> Name:                    amdgcn-amd-amdhsa--gfx1030

------------------------
Windows Host Env：
------------------------

> Windows 11 Version：10.0.22631
> CPU：AMD Ryzen 9 3900X 12-Core Processer
> GPUs：
> Parsec Virtual Display Adapter
> OrayIddDriver Device
> AMD Radeon RX 6900 XT
> NVIDIA GeForce RTX 3090

----------------------------

My environment is as follows:

AMD Radeon 6900XT
Driver Version: 24.6.1
Windows 11 Version: 10.0.22631
WSL2: Ubuntu 22.04
WSL Kernel Version: 5.15.153.1-microsoft-standard-WSL2
ROCm Version: rocm6.1.3
PyTorch: python3.10 + pytorch2.1.0 (from the Repo provided in the AMD official tutorial)

**The issue I'm encountering:**
In my case, rocminfo can detect the GPU normally.
torch.cuda.is_available() returns 'True'.
However, once I attempt to transfer data to the GPU memory using tensor.to(device), the entire program stops responding completely.

----------


### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 3900X 12-Core Processor

### GPU

AMD Radeon Pro W6800

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

for next pytorch code：
```
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
print(torch.cuda.current_device())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))

print(torch.cuda.is_available())

a=torch.rand(3,3,3,3).to(device)
print(a)
b=torch.rand(3,3,3,3).to(device)
print(b)
c=a+b
print(c)
print(c.device)
```
Console Lines Output:
> python rocm-torch-test.py 
> cuda:0
> 0
> /home/tz930/miniconda3/envs/rocm-pytorch-py310/lib/python3.10/site-packages/torch/cuda/__init__.py:611: UserWarning: Can't initialize NVML
>   warnings.warn("Can't initialize NVML")
> 1
> AMD Radeon RX 6900 XT
> True

and then the program hangs on code `a=torch.rand(3,3,3,3).to(device)`


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  ENABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    CPU
  Uuid:                    CPU-XX
  Marketing Name:          CPU
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
  Chip ID:                 0(0x0)
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65756660(0x3eb5df4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65756660(0x3eb5df4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1030
  Marketing Name:          AMD Radeon RX 6900 XT
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        16(0x10)
  Queue Min Size:          4096(0x1000)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L3:                      131072(0x20000) KB
  Chip ID:                 29631(0x73bf)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2015
  Internal Node ID:        1
  Compute Unit:            80
  SIMDs per CU:            2
  Shader Engines:          4
  Shader Arrs. per Eng.:   2
  Coherent Host Access:    FALSE
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
  Packet Processor uCode:: 118
  SDMA engine uCode::      0
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16729316(0xff44e4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1030
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

## 评论 (1 条)

### 评论 #1 — Titianzi (2024-09-29T06:03:25Z)

well, I just find 6900XT (GFX1030) havn't been in Compatibility list of rocm6.1.3 on WSL2 yet. So I'll close this issue. 

---
