# [Issue]: failed call to hipInit: HIP_ERROR_InvalidDevice

> **Issue #3071**
> **状态**: closed
> **创建时间**: 2024-04-29T22:04:53Z
> **更新时间**: 2024-06-21T15:41:21Z
> **关闭时间**: 2024-06-14T15:15:17Z
> **作者**: Looong01
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3071

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

TensorFlow cannot detect GPU

$ python -c "import tensorflow as tf;print(tf.config.list_physical_devices('GPU'))"
2024-04-29 21:45:03.118699: E external/local_xla/xla/stream_executor/plugin_registry.cc:93] Invalid plugin kind specified: DNN
2024-04-29 21:45:03.156327: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2024-04-29 21:45:04.020735: E external/local_xla/xla/stream_executor/rocm/rocm_driver.cc:261] failed call to hipInit: HIP_ERROR_InvalidDevice
2024-04-29 21:45:04.020751: I external/local_xla/xla/stream_executor/rocm/rocm_diagnostics.cc:111] retrieving ROCM diagnostic information for host: home
2024-04-29 21:45:04.020755: I external/local_xla/xla/stream_executor/rocm/rocm_diagnostics.cc:118] hostname: home
2024-04-29 21:45:04.020782: I external/local_xla/xla/stream_executor/rocm/rocm_diagnostics.cc:141] librocm reported version is: NOT_FOUND: was unable to find librocm.so DSO loaded into this program
2024-04-29 21:45:04.020787: I external/local_xla/xla/stream_executor/rocm/rocm_diagnostics.cc:145] kernel reported version is: UNIMPLEMENTED: kernel reported driver version not implemented
[]

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Follow the steps [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/ubuntu.html#uninstalling) o install amdgpu driver and rocm-6.1.0 and hip sdk.
2. conda create -n TensorFlow python=3.10 -y
3. conda activate TensorFlow
4. wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1/tensorflow_rocm-2.15.0-cp310-cp310-manylinux2014_x86_64.whl
5. pip install ./tensorflow_rocm-2.15.0-cp310-cp310-manylinux2014_x86_64.whl
6. python -c "import tensorflow as tf;print(tf.config.list_physical_devices('GPU'))"

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
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
  Max Clock Freq. (MHz):   4700
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            8
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65781560(0x3ebbf38) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65781560(0x3ebbf38) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65781560(0x3ebbf38) KB
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
  Uuid:                    GPU-85631fd855c9cea1
  Marketing Name:          Radeon RX 7900 XTX
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
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
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
  Packet Processor uCode:: 92
  SDMA engine uCode::      20
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB
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

### Additional Information

OS:
NAME="Ubuntu"
VERSION="22.04.4 LTS (Jammy Jellyfish)"

CPU:
model name      : Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz

GPU:
  Name:                    Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Marketing Name:          Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Name:                    gfx1100
  Marketing Name:          Radeon RX 7900 XTX
      Name:                    amdgcn-amd-amdhsa--gfx1100

---

## 评论 (6 条)

### 评论 #1 — briansp2020 (2024-04-30T03:18:35Z)

If you are willing to try docker, you might want to try latest ROCm tensorflow build from 
https://hub.docker.com/r/rocm/tensorflow/tags

>docker pull rocm/tensorflow:rocm6.1-py3.9-tf2.15-dev

---

### 评论 #2 — Looong01 (2024-04-30T03:20:51Z)

> If you are willing to try docker, you might want to try latest ROCm tensorflow build from 
> https://hub.docker.com/r/rocm/tensorflow/tags
> 
> >docker pull rocm/tensorflow:rocm6.1-py3.9-tf2.15-dev

I tried and no help. It shows the same errors. 

---

### 评论 #3 — ppanchad-amd (2024-05-07T17:54:45Z)

@Looong01 Internal ticket has been created to fix this issue. Thanks!

---

### 评论 #4 — jamesxu2 (2024-06-13T19:33:53Z)

Hello @Looong01, please try adding yourself to the **render** and **video** groups so that your current user can access your GPU resources: 
`sudo usermod -a -G render,video $LOGNAME`

Then reboot your machine to try again. 

Please let me know if this issue still appears afterwards.

---

### 评论 #5 — Looong01 (2024-06-14T15:15:17Z)

> Hello @Looong01, please try adding yourself to the **render** and **video** groups so that your current user can access your GPU resources: `sudo usermod -a -G render,video $LOGNAME`
> 
> Then reboot your machine to try again.
> 
> Please let me know if this issue still appears afterwards.

Thank u very much! It works.
Btw, Could u AMD engineer add this command```sudo usermod -a -G render,video $LOGNAME``` and instructions in the docs of ROCm installation, like "https://rocm.docs.amd.com/"? Bc it is really confused for us to find the problems by ourselves. It has been there for half year!

---

### 评论 #6 — ppanchad-amd (2024-06-21T15:41:19Z)

@Looong01 This command is already in the installation guide: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html

---
