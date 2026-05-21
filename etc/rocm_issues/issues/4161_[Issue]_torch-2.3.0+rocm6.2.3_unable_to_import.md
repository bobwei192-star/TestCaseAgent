# [Issue]: torch-2.3.0+rocm6.2.3 unable to import

> **Issue #4161**
> **状态**: closed
> **创建时间**: 2024-12-15T09:58:03Z
> **更新时间**: 2024-12-19T00:54:27Z
> **关闭时间**: 2024-12-19T00:54:26Z
> **作者**: thesapient1
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.2.3
> **URL**: https://github.com/ROCm/ROCm/issues/4161

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.2.3** (颜色: #ededed)

## 描述

### Problem Description

Unable to import torch after uninstalling WSL ROCm 6.1 and upgrading to 6.2.3 per [instructions](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html). Import fails with "ModuleNotFoundError" trying to find torch._utils

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

(with python 3.10.12 virtual environment active)
1. Uninstall previous versions of torch using `pip3 uninstall torch torchvision pytorch-triton-rocm`
2. Uninstall previous AMD drivers per [instructions](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html) `sudo amdgpu-uninstall`
3. Logout and restart WSL Ubuntu 22.04 distribution
4. Install per [instructions](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html) and verify install (verification successful)
5. Follow [instructions to install PyTorch ](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html)
6. Attempt to verify PyTorch installtion

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

WSL environment detected.
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
DMAbuf Support:          NO

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
  Compute Unit:            12
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24564908(0x176d4ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    24564908(0x176d4ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1100
  Marketing Name:          AMD Radeon RX 7900 XTX
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
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29772(0x744c)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2431
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  Coherent Host Access:    FALSE
  Memory Properties:
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
  Packet Processor uCode:: 2280
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25080676(0x17eb364) KB
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

### Additional Information

![image](https://github.com/user-attachments/assets/765456fe-5e38-48d8-8353-128d4da222ef)
Torch is clearly installed

`>>> import torch'
'Traceback (most recent call last):`
`  File "<stdin>", line 1, in <module>`
`  File "/home/beawbull/stable_diffusion/sdenv310/lib/python3.10/site-packages/torch/__init__.py", line 27, in <module>`
`    from ._utils import _import_dotted_name, classproperty`
`ModuleNotFoundError: No module named 'torch._utils'`

---

## 评论 (6 条)

### 评论 #1 — thesapient1 (2024-12-15T10:27:07Z)

Tried re-installing using ` pip3 install torch-2.3.0+rocm6.2.3-cp310-cp310-linux_x86_64.whl torchvision-0.18.0+rocm6.2.3-cp310-cp310-linux_x86_64.whl pytorch_triton_rocm-2.3.0+rocm6.2.3.5a02332983-cp310-cp310-linux_x86_64.whl --force-reinstall` . Uninstall/re-install succeeds but I get the same ModuleNotFoundError when attempting to import torch.

---

### 评论 #2 — xCentral (2024-12-15T13:51:36Z)

You may have forgotten to update the compatible runtime lib. 
Attempt to run:

location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so


Source of code from Article: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html

---

### 评论 #3 — thesapient1 (2024-12-15T23:53:16Z)

I'm pretty sure I did, but I retried that just in case. No change, still seeing the same issue.

I also tried uninstalling and re-installing Torch directly from PyTorch.org (the vanilla 2.5+ROCm 6.2 version) and got the same issue.

Oddly enough if I uninstall from the virtual environment and reinstall with sudo globally, it works fine in the global environment.

But I still can't import torch when running inside the python virtual environment (I still get an error that it can't find the _utility module).

---

### 评论 #4 — evshiron (2024-12-16T10:50:23Z)

@thesapient1 

Do you have NVIDIA stuff in `PATH`?

---

### 评论 #5 — harkgill-amd (2024-12-16T17:14:51Z)

Hi @thesapient1, I wasn't able to reproduce this within a python3.10 virtual environment w/ ROCm 6.2.3 (WSL). Based on your experiments, this seems to be a generic issue with your torch installations. 

Could you please verify if the `_utils.py` file exists in the following directory: `/home/beawbull/stable_diffusion/sdenv310/lib/python3.10/site-packages/torch/`? Additionally, could you try reinstalling and verifying PyTorch in a fresh virtual environment to ensure there are no conflicts or issues with the current setup?

---

### 评论 #6 — thesapient1 (2024-12-19T00:54:27Z)

Hello, after much trial and error I was able to figure out that something must have gone wrong with the previous pip uninstall. 

I don't know what, there weren't any errors or warnings, but it left folders behind. So, I was able to run pip uninstall of all of the torch-related packages _again_, both inside the virtual environment and outside of it, checking afterwards to make sure that it removed every folder (it did). After that I reinstalled torch inside the virtual environment and it works. I'm going to go ahead and close this as resolved with the resolution being "make sure pip uninstall did what it was supposed to".

---
