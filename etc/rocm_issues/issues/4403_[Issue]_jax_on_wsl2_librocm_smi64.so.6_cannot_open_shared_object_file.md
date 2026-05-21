# [Issue]: jax on wsl2: librocm_smi64.so.6: cannot open shared object file

> **Issue #4403**
> **状态**: closed
> **创建时间**: 2025-02-20T15:49:23Z
> **更新时间**: 2025-02-20T16:58:07Z
> **关闭时间**: 2025-02-20T16:58:05Z
> **作者**: roblem
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4403

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

Hardware
GPU: 7900xtx
CPU: 7950x

Windows 11 running Ubuntu 22.04 on Wsl2.  

Install the rocm stack on wsl2 using [the instructions](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html):
```sh
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.2/ubuntu/jammy/amdgpu-install_6.3.60302-1_all.deb
sudo apt install ./amdgpu-install_6.3.60302-1_all.deb
amdgpu-install -y --usecase=wsl,rocm --no-dkms
```
Then Jax, Jaxlib, and the jax plugins were installed from the wheels at `https://github.com/ROCm/jax/releases` taking care to match python versions, as the advised installation method `pip install jax[rocm]` fails with rocm not a valid target/option error.

Running `python -c "import jax; print(jax.devices())"` throws this error:

```python
File ~/anaconda3/envs/jax/lib/python3.12/site-packages/jaxlib/xla_client.py:33
     30 import ml_dtypes
     31 import numpy as np
---> 33 from . import xla_extension as _xla
     35 # Note this module does *not* depend on any Python protocol buffers. The XLA
     36 # Python bindings are currently packaged both as part of jaxlib and as part
     37 # of TensorFlow. If we use protocol buffers here, then importing both jaxlib
   (...)
     44 # Pylint has false positives for type annotations.
     45 # pylint: disable=invalid-sequence-index
     47 ifrt_programs = _xla.ifrt_programs

ImportError: librocm_smi64.so.6: cannot open shared object file: No such file or directory
```

But elsewhere, it is stated that rocm-smi isn't supported on wsl2 because we install it using the rocm `--no-dkms` option.  Indeed running `rocm-smi`, reveals
```
$ rocm-smi
cat: /sys/module/amdgpu/initstate: No such file or directory
ERROR:root:Driver not initialized (amdgpu not found in modules)
```
which isn't a surprise as we don't have the amdgpu kernel module loaded.  I think the rocm check in jax needs to reference some other rocm tool like `rocminfo`.

### Operating System

Ubuntu 22.04

### CPU

7950x

### GPU

Radeon 7900xtx

### ROCm Version

6.3

### ROCm Component

_No response_

### Steps to Reproduce

See main comment

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
$ rocminfo --support
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
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 9 7950X 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 9 7950X 16-Core Processor
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
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            20
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    49332556(0x2f0c14c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49332556(0x2f0c14c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49332556(0x2f0c14c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    49332556(0x2f0c14c) KB
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
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2526
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
  Packet Processor uCode:: 232
  SDMA engine uCode::      21
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25079976(0x17eb0a8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25079976(0x17eb0a8) KB
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
```

### Additional Information

If I need to file this at jax I can do that.

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-02-20T16:20:01Z)

Hi @roblem. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-02-20T16:38:21Z)

Hi @roblem, the library should still be there on WSL, but the version number is probably wrong. Check `/opt/rocm/lib` to see what's there, I suspect you'll have to `ln -s  librocm_smi64.so.7  librocm_smi64.so.6`.

---

### 评论 #3 — roblem (2025-02-20T16:58:05Z)

Yes, that fixes things.  Also had to update the gcc in my conda environment but I can load jax and it sees the rocm device.

---
