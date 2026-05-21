# [Issue]: [WSL2] PyTorch nn.Module.to("cuda") hangs with models >262,656 parameters; process hangs on exit

> **Issue #5888**
> **状态**: closed
> **创建时间**: 2026-01-23T00:40:27Z
> **更新时间**: 2026-02-20T20:34:22Z
> **关闭时间**: 2026-02-20T20:34:21Z
> **作者**: Caphalem
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5888

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

Using ROCm 6.4.2 on WSL2 with an AMD Radeon RX 7900 XTX, PyTorch exhibits two related issues:

1. **Model transfer hang:** `nn.Module.to("cuda")` hangs indefinitely when the model exceeds ~262,656 parameters. The threshold appears to be exactly at the 512×512 boundary—`nn.Linear(512, 512)` succeeds (262,656 params), but `nn.Linear(513, 513)` hangs.

2. **Process exit hang:** After any Python script that imports PyTorch completes, the Python process enters uninterruptible sleep (`D` state in `ps aux`) and never exits. The terminal becomes corrupted (echoes all keyboard input, Ctrl+C doesn't work). This happens even with simple scripts that only move small tensors to GPU.

Notably, simple tensor operations work fine but hangs after completion:
```python
x = torch.tensor([1.0, 2.0, 3.0]).to("cuda")  # Works
y = x + x  # Works
# Hangs indefinitely
```

But moving any `nn.Module` larger than the threshold fails:
```python
model = nn.Linear(513, 513)
model.to("cuda")  # Hangs indefinitely
```

## **Environment**

| Component | Version |
|-----------|---------|
| **OS (Host)** | Windows 10 Pro Build 19045 |
| **WSL Version** | 2.6.3.0 |
| **WSL Kernel** | 6.6.87.2-1 |
| **WSL Distro** | Ubuntu 24.04.3 LTS |
| **Python** | 3.12.3 |
| **CPU** | Intel Core i9-9900K |
| **Motherboard** | Gigabyte Z390 AORUS Master |
| **RAM** | 32GB |
| **GPU** | AMD Radeon RX 7900 XTX (gfx1100) |
| **AMD Driver** | Adrenalin 25.8.1 |
| **ROCm** | 6.4.2 |
| **PyTorch** | 2.6.0+rocm6.4.2 (from repo.radeon.com) |

### Operating System

Windows 10 Pro Build 19045

### CPU

Intel Core i9-9900K

### GPU

NITRO+ AMD Radeon™ RX 7900 XTX Vapor-X 24GB

### ROCm Version

ROCm 6.4.2

### ROCm Component

_No response_

### Steps to Reproduce

1. Set up WSL2 Ubuntu 24.04 with ROCm 6.4.2 following official documentation
2. Install PyTorch wheels from repo.radeon.com for ROCm 6.4.2
3. Run the following script:

```python
import torch
import torch.nn as nn

for size in [512, 513]:
    print(f"Trying nn.Linear({size}, {size})...", end=" ", flush=True)
    model = nn.Linear(size, size)
    param_count = sum(p.numel() for p in model.parameters())
    model.to("cuda")
    print(f"OK ({param_count:,} params)")
```

**Expected:** Both sizes complete successfully
**Actual:** 512 completes, 513 hangs indefinitely

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz
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
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    16341164(0xf958ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16341164(0xf958ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16341164(0xf958ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16341164(0xf958ac) KB
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

### Additional Information

- `rocminfo` correctly detects the GPU
- `torch.cuda.is_available()` returns `True`
- `torch.cuda.get_device_name(0)` returns correct GPU name
- The 512 parameter boundary suggests a possible buffer size or memory alignment issue in the HSA runtime
- Environment variables `HSA_ENABLE_SDMA=0` and `LD_PRELOAD=/opt/rocm/lib/libamdhip64.so` do not resolve the issue
- The process exit hang occurs regardless of model size (even scripts with only small tensor operations hang on exit)

---

## 评论 (4 条)

### 评论 #1 — schung-amd (2026-01-29T15:13:12Z)

Hi @Caphalem, we have a new WSL + ROCm release (see updated steps in https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html); do you still see this issue with ROCm 7.2 and Adrenalin 26.1.1?

---

### 评论 #2 — Caphalem (2026-01-29T19:49:56Z)

Hi @schung-amd, I updated to Adrenalin 26.1.1 and set up a new WSL environment with ROCm 7.2.
The results seem to be the same with the added bonus of `rocminfo` now entering the endless `D+` process state, after printing the results, as well.
However, with Adrenalin 26.1.1, it seems that I can use ROCm PyTorch on Windows now without issue.

---

### 评论 #3 — schung-amd (2026-01-29T20:10:11Z)

Glad to hear that it has improved the native Windows experience for you. I'll try to repro the WSL issue.

---

### 评论 #4 — schung-amd (2026-02-20T20:34:21Z)

Sorry for the delay on this, I haven't been able to repro the hang or the `rocminfo` non-termination you saw. I'm going to close this for now on the assumption that there's an issue with your WSL install, please try reinstalling everything and if you're still seeing this issue we can reopen.

---
