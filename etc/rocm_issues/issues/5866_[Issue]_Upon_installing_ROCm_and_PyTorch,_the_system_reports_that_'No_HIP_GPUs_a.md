# [Issue]: Upon installing ROCm and PyTorch, the system reports that 'No HIP GPUs are available'.

> **Issue #5866**
> **状态**: closed
> **创建时间**: 2026-01-18T03:39:29Z
> **更新时间**: 2026-01-22T15:00:01Z
> **关闭时间**: 2026-01-22T15:00:01Z
> **作者**: soapold
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5866

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

I attempted to install ROCm on Ubuntu 22.04 (WSL2). However, PyTorch fails to detect any available GPU after the installation. My GPU is a Radeon RX 7900 XTX, so theoretically, this shouldn't be an issue.

<img width="1115" height="628" alt="Image" src="https://github.com/user-attachments/assets/89b0c63b-e2e5-4d14-8f08-37953cc4b57a" />[](url)

### Operating System

Ubuntu 22.04 (WSL2)

### CPU

AMD Ryzen 7 7700 8-Core Processor

### GPU

AMD Radeon RX 7900 XTX 

### ROCm Version

6.4.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — Papina (2026-01-19T02:31:34Z)

same for AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

fresh WSL2 Ubuntu build
followed all steps at: 
`https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html`
`https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-pytorch.html` (upto and including step 4
`https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-pytorch.html#verify-pytorch-installation`

```bash
(venv) luton@MS-S1MAX:~$ rocminfo --support
WSL environment detected.
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            32
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32678008(0x1f2a078) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32678008(0x1f2a078) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32678008(0x1f2a078) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32678008(0x1f2a078) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
```

```bash
python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
Success
```

```bash
(venv) luton@MS-S1MAX:~$ python3 -c 'import torch; print(torch.cuda.is_available())'
False
```

```bash
(venv) luton@MS-S1MAX:~$ python3 -c "import torch; print(f'device name [0]: ' ,torch.cuda.get_device_name(0))"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/home/luton/venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 506, in get_device_name
    return get_device_properties(device).name
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/luton/venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 538, in get_device_properties
    _lazy_init()  # will define _get_device_properties
    ^^^^^^^^^^^^
  File "/home/luton/venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 334, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No HIP GPUs are available
```

---

### 评论 #2 — soapold (2026-01-19T02:37:16Z)

I did exactly what you did, I followed the instructions, but I failed.

---

### 评论 #3 — schung-amd (2026-01-19T20:02:54Z)

@soapold What does `rocminfo` show? If the integrated graphics are shown please try disabling them, as that's known to cause issues in WSL.

@Papina Unfortunately we don't have ROCm + WSL support for that hardware at this time; see https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html.

---

### 评论 #4 — soapold (2026-01-20T01:05:18Z)

Integrated graphics are shown as you mentioned， but I already disabled them long time ago， I have no idea why WSL still can detect them.

WSL environment detected.
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
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
  Name:                    AMD Ryzen 7 7700 8-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 7700 8-Core Processor
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
  Compute Unit:            6
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    24611556(0x1778ae4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24611556(0x1778ae4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24611556(0x1778ae4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    24611556(0x1778ae4) KB
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
  Packet Processor uCode:: 542
  SDMA engine uCode::      24
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
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
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

### 评论 #5 — schung-amd (2026-01-20T15:02:39Z)

Thanks for the response. I think your integrated graphics are disabled as you said and that's just the CPU in `rocminfo`. I'll try to repro this and get back to you.

---

### 评论 #6 — schung-amd (2026-01-20T21:21:51Z)

I couldn't reproduce this on a 9070, will set up a WSL test system with a 7900 as a sanity check although I don't think there should be a difference there. What Adrenalin driver version are you on? A common pitfall is that ROCm + WSL requires a specific Adrenalin driver version (25.8.1 at the time of writing according to https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html).

---

### 评论 #7 — soapold (2026-01-21T00:52:29Z)

I am currently on version 25.10.30.02 . I noticed you mentioned version 25.8.1.Is my newer version (25.10) is compatible, or is strictly 25.8.1 required?
<img width="1588" height="963" alt="Image" src="https://github.com/user-attachments/assets/edf07b14-52c7-411e-b925-b0fa08a1f1da" />

---

### 评论 #8 — schung-amd (2026-01-21T15:51:32Z)

Only specific versions are compatible, I don't recognize that driver version off the top of my head but you'll most likely need to downgrade. If that's a dealbreaker and you need a newer driver for gaming or other reasons, we have some native Windows support via TheRock and HIP SDK that might suffice if WSL itself isn't a requirement.

---

### 评论 #9 — soapold (2026-01-22T02:35:11Z)

Thanks a lot, I finally made it work on the GPU now

---

### 评论 #10 — schung-amd (2026-01-22T15:00:01Z)

Great, glad to hear it! Closing for now, feel free to comment if this issue pops up again in the future and we can reopen if necessary.

---
