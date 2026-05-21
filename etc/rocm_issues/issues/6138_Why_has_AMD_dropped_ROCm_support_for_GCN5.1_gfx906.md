# Why has AMD dropped ROCm support for GCN5.1 gfx906?

> **Issue #6138**
> **状态**: closed
> **创建时间**: 2026-04-09T20:04:21Z
> **更新时间**: 2026-05-04T02:05:38Z
> **关闭时间**: 2026-04-20T14:20:19Z
> **作者**: tjbbjt
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6138

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

Seems like AMD never realized the full potential of the GCN5.1 gfx906 architecture. Is the discontinuation of software for this "never fully supported hardware" simply a means of selling new hardware?  Is there something in the RDNA* architecture that is not available on the GCN* or is this just standard software depreciation?

I really don't want to support NVIDIA but it is these types of decisions that make it a consideration. Why not make the GCN5.1 gfx906 drivers open sourced instead?

Thanks.

---

## 评论 (2 条)

### 评论 #1 — darren-amd (2026-04-13T18:36:16Z)

Hi @tjbbjt,

Thanks for bringing this up! We're always looking to expand support for our community and we currently do have builds available for `gfx906` under [TheRock](https://github.com/ROCm/TheRock?tab=readme-ov-file#therock). You can find them [here](https://rocm.nightlies.amd.com/v2/gfx906/) and can install them by following the instructions [here](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-releases-using-pip):
```
python -m venv .venv
source .venv/bin/activate
pip install --index-url https://rocm.nightlies.amd.com/v2/gfx906/ "rocm[libraries,devel]"
```

Please give that a try and let me know if you run into any issues, thanks!

---

### 评论 #2 — tjbbjt (2026-05-03T22:45:50Z)


> ```
> python -m venv .venv
> source .venv/bin/activate
> pip install --index-url https://rocm.nightlies.amd.com/v2/gfx906/ "rocm[libraries,devel]"
> ```
> 
> Please give that a try and let me know if you run into any issues, thanks!

Thanks @darren-amd,

I am primarily trying to run DaVinci Resolve.

I was able to get DaVinci Resolve installed in a Fedora distrobox, then tried running/installing TheRock drivers as you listed above but upon launching Resolve in the python environment I'm getting the error: "Unsupported GPU Processing Mode". 

Tried:

`HSA_OVERRIDE_GFX_VERSION=9.0.6 /opt/resolve/bin/resolve`

Same outcome

rocminfo:

```
  Name:                    gfx906
  Uuid:                    GPU-d48a706172fd5d11
  Marketing Name:          AMD Radeon VII
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
  Chip ID:                 26287(0x66af)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1801
  BDFID:                   12032
  Internal Node ID:        1
  Compute Unit:            60
  SIMDs per CU:            4
  Shader Engines:          4
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
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
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 481
  SDMA engine uCode::      145
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
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx9-generic:xnack-
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
```


---
