# [Issue]: Tensorflow documentation needs improvments

> **Issue #2594**
> **状态**: closed
> **创建时间**: 2023-10-22T21:41:51Z
> **更新时间**: 2024-10-01T17:04:02Z
> **关闭时间**: 2024-10-01T17:04:02Z
> **作者**: briansp2020
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2594

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Problem Description

After working with 7900XTX for a while and seeing it getting official support, I wanted to try out another hardware that has been out for a while. Even though 7900XTX started working, it still is not production-ready as I have encountered many stability issues, requiring me to reboot (ex. https://github.com/ROCmSoftwarePlatform/pytorch/issues/1284). 

I was hoping that MI100 would be better supported since the hardware has been out for a long time and it, unlike 7900XTX, was a product made for data center/enterprise. However, I noticed some issues with TensorFlow instructions (https://rocm.docs.amd.com/en/latest/how_to/tensorflow_install/tensorflow_install.html)

After pulling the latest tensorflow docker and running it.
>docker pull rocm/tensorflow:latest
>'docker run -it --network=host --device=/dev/kfd --device=/dev/dri --ipc=host --shm-size 16G --group-add=video --cap-add=SYS_PTRACE --security-opt seccomp=unconfined rocm/tensorflow:latest

1. I tried to run the benchmark using the files that are already in the docker and got bunch of errors. It turned out that the benchmark repo was updated to to resolve the issue but the official docker was not updated to include it.
2. The [Run a Basic TensorFlow Example](https://rocm.docs.amd.com/en/latest/how_to/tensorflow_install/tensorflow_install.html#run-a-basic-tensorflow-example) section in the instruction does not work. mnist_tf.py does not seem to be part of the model repo and I don't see a requirement.txt in the root directory of the repo either.


### Operating System

Ubuntu 22.04.3 LTS

### CPU

AMD Ryzen 9 7900X

### GPU

MI100

### ROCm Version

5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

Pull the latest tensorflow and try to [Run a Basic TensorFlow Example](https://rocm.docs.amd.com/en/latest/how_to/tensorflow_install/tensorflow_install.html#run-a-basic-tensorflow-example) 

### Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen 9 7900X 12-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 7900X 12-Core Processor
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
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    64953076(0x3df1af4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    64953076(0x3df1af4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    64953076(0x3df1af4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx908
  Uuid:                    GPU-cafb6d633e33407e
  Marketing Name:          AMD Instinct MI100
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
    L2:                      8192(0x2000) KB
  Chip ID:                 29580(0x738c)
  ASIC Revision:           2(0x2)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1502
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            120
  SIMDs per CU:            4
  Shader Engines:          8
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
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
      Segment:                 GLOBAL; FLAGS:
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
Agent 3
*******
  Name:                    gfx1036
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon Graphics
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
    L2:                      256(0x100) KB
  Chip ID:                 5710(0x164e)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2200
  BDFID:                   3584
  Internal Node ID:        2
  Compute Unit:            2
  SIMDs per CU:            2
  Shader Engines:          1
  Shader Arrs. per Eng.:   1
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
  Packet Processor uCode:: 20
  SDMA engine uCode::      8
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    524288(0x80000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS:
      Size:                    524288(0x80000) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1036
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

---

## 评论 (6 条)

### 评论 #1 — briansp2020 (2023-10-22T21:57:14Z)

Also, it would be good to add that if using the latest Ryzen 7000 series with iGPU, one has to add 
>export HIP_VISIBLE_DEVICES=0

after starting the docker image.

---

### 评论 #2 — i-chaochen (2023-11-07T11:01:06Z)

Thanks for suggestion! Yes, there are some issues on upstream Tensorflow and we recommend you to use our ROCm develop-upstream Tensorflow.

https://github.com/ROCmSoftwarePlatform/tensorflow-upstream

---

### 评论 #3 — briansp2020 (2023-11-07T14:07:46Z)

This is I reported is for NOT for the upstream Tensorflow. I've been working exclusively with ROCm tensorflow-upstream that I built myself and the docker images from ROCm hub. AFAIK, upstream Tensorflow does not support 7900XTX nor any binary release of tensorflow-rocm. Probably because 7900XTX support is still broken in ROCm tensorflow release despite its [official support](https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html#linux-supported-gpus).  

Building from the source still has issues. Two notable issues I personally encountered are [#2292](https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/issues/2292 ) and [#2191](https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/pull/2191)

[#2191](https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/pull/2191) is especially frustrating for me because it keeps re-appearing. Right now, r2.14-rocm-enhanced does not work with 7900XTX because the #2191 bug is still present in that branch even though the branch was created after the fix was merged.

---

### 评论 #4 — ppanchad-amd (2024-05-15T15:28:59Z)

@briansp2020 Internal ticket has been created to fix the documentation. Thanks!

---

### 评论 #5 — harkgill-amd (2024-07-24T19:01:56Z)

Hi @briansp2020, using the latest TensorFlow Docker image and following [Installing TensorFlow for ROCm](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/3rd-party/tensorflow-install.html#running-a-basic-tensorflow-example), I was able to run the basic MNIST example, outputting:

`313/313 - 1s - loss: 0.0792 - accuracy: 0.9767 - 849ms/epoch - 3ms/step`

Are you still experiencing issues with benchmarks on the latest image? 


---

### 评论 #6 — harkgill-amd (2024-10-01T17:04:02Z)

Closing this issue out. @briansp2020, if you are still encountering issues with TensorFlow on the supported docker image, please leave a comment and I will re-open this ticket. Thanks!

---
