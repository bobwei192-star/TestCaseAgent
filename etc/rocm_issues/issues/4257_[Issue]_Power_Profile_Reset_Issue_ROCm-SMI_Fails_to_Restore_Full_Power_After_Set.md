# [Issue]: Power Profile Reset Issue: ROCm-SMI Fails to Restore Full Power After Setting Low Profile

> **Issue #4257**
> **状态**: closed
> **创建时间**: 2025-01-14T13:31:35Z
> **更新时间**: 2025-01-27T14:32:32Z
> **关闭时间**: 2025-01-24T14:35:15Z
> **作者**: snehargho
> **标签**: Under Investigation, AMD Radeon RX 7900 GRE, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4257

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 GRE** (颜色: #ededed)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

Initially System reaches peak power (220W) when running a load (ollama model in this case)

Executed: rocm-smi --setperflevel low

System does not go beyond 27W and the token speed on ollama is totally acceptable for me.

Problem begins when I revert the performance level using: rocm-smi --setperflevel auto

The power does not reach the peak as it used to..it reaches 143W max...If I set the performance to high, then 153W max. 

However, the system again recovers ability to reach 220W upon rebooting.

### Operating System

Arch Linux

### CPU

AMD Ryzen 5 7600 6-Core Processor

### GPU

AMD Radeon RX 7900 GRE

### ROCm Version

ROCm 6.3.0

### ROCm Component

rocm_smi_lib

### Steps to Reproduce

1. Check max power system reaches
2. run rocm-smi --setperflevel low
3. Check max power (should be fairly lower now as desired)
4. Work done
5. Revert to auto using rocm-smi --setperflevel auto
6. Run a load to check max power again...This time you will not get what you used to get at step 1

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
  Name:                    AMD Ryzen 5 7600 6-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 5 7600 6-Core Processor
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
  Max Clock Freq. (MHz):   5170
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            12
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    15535996(0xed0f7c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    15535996(0xed0f7c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    15535996(0xed0f7c) KB
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
  Uuid:                    GPU-42147bdb07129c03
  Marketing Name:          AMD Radeon RX 7900 GRE
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
    L3:                      65536(0x10000) KB
  Chip ID:                 29772(0x744c)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   1927
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            80
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
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
  Packet Processor uCode:: 462
  SDMA engine uCode::      24
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB
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
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2200
  BDFID:                   5120
  Internal Node ID:        2
  Compute Unit:            2
  SIMDs per CU:            2
  Shader Engines:          1
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
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
  Packet Processor uCode:: 21
  SDMA engine uCode::      9
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    7767996(0x7687bc) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    7767996(0x7687bc) KB
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

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-01-14T14:42:27Z)

Hi @Snehargho123. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-01-14T19:34:06Z)

Hi @Snehargho123, thanks for reporting this. I've been able to reproduce it on a 7900XTX, and it extends to `amd-smi` and the amdgpu sysfs API as well. Reaching out to internal team to figure out what's happening here.

---

### 评论 #3 — schung-amd (2025-01-24T14:35:15Z)

This was actually resolved already but the change didn't make it into the ROCm release (you can see it [here](https://gitlab.freedesktop.org/agd5f/linux/-/commit/3d73327b748baaddf82cfad791fc25f8f1822ffe)). Checking with internal teams to figure out when this will land in ROCm. For now, although it may be inconvenient, you can reboot to restore the power settings as you've noted. You can also try to apply the patch yourself if you wish.

Closing this for now as we're just waiting on the fix to land, feel free to continue discussion here if you need additional guidance. I'll update once I know more about the timeline for this.

---

### 评论 #4 — schung-amd (2025-01-27T14:32:31Z)

This will be fixed in the next minor release (i.e. 6.4 at the moment) and probably not before then.

---
