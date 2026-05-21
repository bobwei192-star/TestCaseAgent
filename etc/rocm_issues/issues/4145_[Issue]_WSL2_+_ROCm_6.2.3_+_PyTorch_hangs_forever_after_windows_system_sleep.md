# [Issue]: WSL2 + ROCm 6.2.3 + PyTorch hangs forever after windows system sleep

> **Issue #4145**
> **状态**: closed
> **创建时间**: 2024-12-09T16:47:35Z
> **更新时间**: 2024-12-23T14:31:17Z
> **关闭时间**: 2024-12-23T14:31:17Z
> **作者**: helloworld1
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.2.3
> **URL**: https://github.com/ROCm/ROCm/issues/4145

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.2.3** (颜色: #ededed)

## 描述

### Problem Description

All on recommended software on WSL2. Driver 24.12.1, Rocm 6.2.3 WSL2 ubuntu 22.04.5 LTS. PyTorch  2.3.0+rocm6.2.3.
The following code works after rebooting the computer
```
import torch

t = torch.Tensor([1,2,3,4])
t.to("cuda")
```

After system sleep, the program freezes at `t.to("cuda")` forever. Shutting down WSL2 and restarting does not work. After Rebooting Windows, the code works again.

### Operating System

Windows 11 (10.0.26100)

### CPU

AMD Ryzen 9 5950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

Reboot PC, and run to verify it works
```
import torch

t = torch.Tensor([1,2,3,4])
t.to("cuda")
```

Sleep PC and then run
```
import torch

t = torch.Tensor([1,2,3,4])
t.to("cuda")
```
It hangs on `t.to("cuda")`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
  Compute Unit:            32
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    57587508(0x36eb734) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    57587508(0x36eb734) KB
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
  Max Clock Freq. (MHz):   2304
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
      Size:                    25086124(0x17ec8ac) KB
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
*** Done ***
```

### Additional Information

_No response_

---

## 评论 (14 条)

### 评论 #1 — tcgu-amd (2024-12-09T19:57:11Z)

Hi @helloworld1 Thanks for reporting the error! I was able to reproduce your issue and we are currently investigating the root cause. Thanks! 

---

### 评论 #2 — tcgu-amd (2024-12-11T20:09:09Z)

Hi @helloworld1, a brief update: we are still in the progress of investigation -- currently it appears that the bug only occurs on one of our systems, which was really strange. Just wondering, have you experienced this problem with other ROCm versions? If not, would you mind trying ROCm 6.1.3 and let us know if the same issue occurs? Any additional data point would help us track it down. Thanks! 

---

### 评论 #3 — helloworld1 (2024-12-11T21:12:50Z)

Yes I also tried 6.1.3 and older version of AMD driver and the recommended torch 2.1. I still encountered the same problem. 

---

### 评论 #4 — tcgu-amd (2024-12-11T21:52:45Z)

I see. Can you try switching your GPU onto a different PCIe slot and see if anything changes? 

---

### 评论 #5 — helloworld1 (2024-12-12T14:35:40Z)

No changes after changing pcie slots. I don't have another GPU so I cannot test if the issue still repo on non display GPU .

---

### 评论 #6 — tcgu-amd (2024-12-12T14:45:57Z)

> No changes after changing pcie slots. I don't have another GPU so I cannot test if the issue still repo on non display GPU .

Got it! Thanks for confirming! 

---

### 评论 #7 — tcgu-amd (2024-12-13T19:08:50Z)

Hi @helloworld1, here is another quick update. We were able to reproduce the problem on another system now, but the only common factor these systems share seems to be they both use TUF gaming motherboards. Hence I am wondering if you could share some information about the motherboard you are using so we can more data points? Thanks!

---

### 评论 #8 — helloworld1 (2024-12-15T06:57:22Z)

The motherboard is Asus Strix X570 ITX.

---

### 评论 #9 — tcgu-amd (2024-12-16T15:32:03Z)

Thanks for the update! Seems like the issue might be related to motherboard then. Thanks! 

---

### 评论 #10 — tcgu-amd (2024-12-17T17:00:46Z)

@helloworld1! Hi, I was able to resolve the issue by enabling SR-IOV in the BIOS. Would you mind giving it a try and let us know if it works? The configuration path is Advanced -> PCI Subsystem Settings -> SR-IOV Support. 

Thanks!

---

### 评论 #11 — helloworld1 (2024-12-18T02:56:11Z)

Enabling SR-IOV indeed fix the issue! Thanks. Would you help to update the WSL documentations to hint user to enable SR-IOV?

---

### 评论 #12 — tcgu-amd (2024-12-18T16:23:58Z)

> Enabling SR-IOV indeed fix the issue! Thanks. Would you help to update the WSL documentations to hint user to enable SR-IO

We are still trying to understand the root cause right now. Once we get a better understanding, we will see what we can do to fix or help other users avoid this issue. Adding instructions in the docs would certainly be one of the options. Thanks for the suggestion! 

---

### 评论 #13 — tcgu-amd (2024-12-20T14:26:36Z)

By the way @helloworld1 would you mind if I mark this issue closed for now since the the particular issue itself is resolved?  If you like, we could open a separate issue to track the progress of potential docs update, or I can continue to provide update of the root cause investigation below. Thanks!

---

### 评论 #14 — helloworld1 (2024-12-21T21:41:26Z)

Yes, feel free to close the issue and track the root cause /doc update in a separate issue.

---
