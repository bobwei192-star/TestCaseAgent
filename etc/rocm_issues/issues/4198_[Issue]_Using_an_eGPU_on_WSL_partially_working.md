# [Issue]: Using an eGPU on WSL partially working

> **Issue #4198**
> **状态**: closed
> **创建时间**: 2024-12-24T18:02:44Z
> **更新时间**: 2025-01-06T14:56:05Z
> **关闭时间**: 2025-01-06T14:56:05Z
> **作者**: adelj88
> **标签**: Under Investigation, AMD Radeon RX 7900 GRE, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4198

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 GRE** (颜色: #ededed)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

I'm using an Asus Zenbook S16 that's equipped with a Ryzen AI 9 365, where I've connected a 7900 GRE through an eGPU setup (via USB4). 

I've confirmed that I can run HIP applications via Windows normally (using the ROCM examples, and by disabling the iGPU), but when trying to run this via WSL2, I run into an odd issue. 

Using `rocm-examples` as the testbed, if I try running any of the examples (e.g. `hip_saxpy`), I get the following error and message from the logs

```
:3:rocvirtual.cpp           :3056: 0368660738d us:  ShaderName : _Z12saxpy_kernelfPKfPfj
:1:rocvirtual.cpp           :3103: 0368660788d us:  Pcie atomics not enabled, hostcall not supported
:1:rocvirtual.cpp           :3465: 0368660830d us:  AQL dispatch failed!
:4:command.cpp              :169 : 0368660838d us:  Command 0x324b51d8 complete
:3:hip_module.cpp           :687 : 0368660842d us:  hipLaunchKernel: Returned hipErrorIllegalState :
``` 

Do note that memory transfers work normally, but kernel execution is where the error occurs. What's funny is that if I run a kernel that's been loaded in via RTC (using `hip_runtime_compilation` from `rocm-examples`), it works!

```
:3:rocvirtual.cpp           :3056: 0476093984d us:  ShaderName : saxpy_kernel
:4:rocvirtual.cpp           :905 : 0476093991d us:  SWq=0x7f20902c0000, HWq=0x7f20902d0000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[4096, 1, 1], workgroup=[128, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x7f288fc08880, kernarg_address=0x7f2090580000, completion_signal=0x0, correlation_id=0, rptr=2, wptr=2
:3:hip_module.cpp           :463 : 0476094066d us:  hipModuleLaunchKernel: Returned hipSuccess :
```

Any ideas on how to fix the above via WSL? I've listed my specs, and rocm version below.

### Operating System

Windows 11 (WSL2: Ubuntu 24.04.1 LTS)

### CPU

AMD Ryzen AI 9 365 w/ Radeon 880M

### GPU

AMD Radeon RX 7900 GRE

### ROCm Version

ROCm 6.3.0

### ROCm Component

HIP, ROCm

### Steps to Reproduce

Not sure if you would have the right setup to reproduce this, given the setup I'm using. For the USB4 egpu setup, I'm using an ADT-Link UT4G board which is based off the ASMedia ASM2464PDX chipset.

As for the code reproduction, I'm using `rocm-examples`, specifically any binary compiled under `HIP-Basic`.

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
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen AI 9 365 w/ Radeon 880M
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen AI 9 365 w/ Radeon 880M
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
  Compute Unit:            20
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    16378220(0xf9e96c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16378220(0xf9e96c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16378220(0xf9e96c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16378220(0xf9e96c) KB
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
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1927
  Internal Node ID:        1
  Compute Unit:            80
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
      Size:                    16691368(0xfeb0a8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16691368(0xfeb0a8) KB
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

_No response_

---

## 评论 (15 条)

### 评论 #1 — ppanchad-amd (2024-12-24T19:43:51Z)

Hi @AJcodes. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — zichguan-amd (2024-12-24T21:53:57Z)

Hi @AJcodes, can you try the supported configuration [here](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix)? ROCm 6.2.3 + Adrenalin 24.12.1 + Ubuntu 22.04. Your eGPU seems to work correctly and is being picked up by hip and the driver so I suspect it is a setup issue with WSL. I tested with a standard dGPU setup and it works, unfortunately I don't have an eGPU setup to verify.

---

### 评论 #3 — adelj88 (2024-12-24T22:57:47Z)

@zichguan-amd I've already tried it the supported configuration, and ran into the same issue unfortunately. I also decided to try an Ubuntu install and I ran into the same issue. I do wonder if it has to do with the iGPU, as I noticed that I ran into a different error if I ran the examples on Windows until I disabled it in the device manager

---

### 评论 #4 — zichguan-amd (2024-12-30T16:47:19Z)

It may be a PCIE atomic problem. If you only intend to do ML workloads using PyTorch, try this instead: [ROCm/pytorch-micro-benchmarking](https://github.com/ROCm/pytorch-micro-benchmarking). PyTorch should not use PCIE atomics, but some HIP functions do need it.

Since you have native Linux, can you locate your GPU's pcie slot using `lspci | grep VGA`, example output:
<pre><b>2e:00.0</b> VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 31 [Radeon RX 7900 XT/7900 XTX/7900 GRE/7900M] (rev c8)</pre>
and check the output of <pre>sudo lspci -kkvvv -s <b>2e:00.0</b> | grep -i atomic </pre>
You should have a similar output to the following, indicating that PCIE atomic is enabled, 
```
AtomicOpsCap: 32bit+ 64bit+ 128bitCAS-
AtomicOpsCtl: ReqEn+
```

> I do wonder if it has to do with the iGPU

You do need to disable the iGPU as ROCm does not support it, see https://rocm.docs.amd.com/projects/radeon/en/latest/docs/prerequisites.html#disable-igpu. 

---

### 评论 #5 — adelj88 (2024-12-30T21:09:46Z)

@zichguan-amd Apologies for accidentally closing the issue.

I decided to make a fresh install of Ubuntu 22.04.5 LTS with ROCm 6.3.1, and I just confirmed that I'm running into the same error as I am in WSL2 (where saxpy throws the PCIe atomic error, but HIPRTC runs fine). I ran the command like you asked and got the following

```
AtomicOpsCap: 32bit+ 64bit+ 128bitCAS-
AtomicOpsCtl: ReqEn-
```

Unfortunately I have no way of disabling the iGPU via the BIOs, and not through Ubuntu either. I'm only able to disable it manually in Windows.

For context, I'm just preparing my environment for some HIP kernels that I need to write and optimise, and it seems like my only option is to work only in Windows; since both WSL2 and Ubuntu have the exact same error.

---

### 评论 #6 — adelj88 (2024-12-30T21:49:30Z)

It's likely that PCIe atomics isn't supported over PCIe tunnelling (something I just heard from someone else who is running into similar issues), though I can't confirm this yet. 

I do find it odd that I can run HIP kernels via Windows though (made sure of this by disabling the iGPU in device manager; even if it is enabled the 880M can't run HIP kernels due to bitcode issues), so I'll continue to investigate further

---

### 评论 #7 — zichguan-amd (2024-12-30T22:27:38Z)

@AJcodes I'm not familiar with how HIP SDK handles atomics so I cannot tell why it works on HIP SDK but not WSL/Ubuntu. Based on your output your system is PCIe atomic capable (32bit+ 64bit+), but the request bit is disabled (ReqEn-). On native Ubuntu, can you check your PCIe capability configuration registers with `sudo setpci -s <your-gpu-pcie-slot> 8c.b`?

---

### 评论 #8 — adelj88 (2024-12-30T22:58:21Z)

@zichguan-amd Just ran that line you provided, I get `00`

---

### 评论 #9 — zichguan-amd (2024-12-30T23:02:02Z)

Ok then can you try `sudo setpci -s <your-gpu-pcie-slot> 8c.b=40` and recheck `sudo lspci -kkvvv -s <your-gpu-pcie-slot> | grep -i atomic`? If all's good, try rerun the rocm examples too.

---

### 评论 #10 — adelj88 (2024-12-30T23:05:15Z)

@zichguan-amd Just did that, I now see 

```
AtomicOpsCtl: ReqEn+
```

But when running the rocm examples, I'm still met with
```
:1:rocvirtual.cpp           :3103: 0524793290d us:  Pcie atomics not enabled, hostcall not supported
:1:rocvirtual.cpp           :3465: 0524793291d us:  AQL dispatch failed!
```

---

### 评论 #11 — zichguan-amd (2024-12-31T20:55:26Z)

It might indeed be PCIe tunnelling over USB4 not supporting atomics, I'm not sure if there's any workaround for it so, please use HIP SDK for now.

---

### 评论 #12 — adelj88 (2025-01-02T11:21:33Z)

I dug a little deeper and found the PCI bridge (in this case the ASM2464PDX controller) has its Routing bit disabled

```
sudo lspci -kkvvv -s 61:00.0 | grep -i atomic
AtomicOpsCap: Routing-
AtomicOpsCtl: EgressBlck-
```

Based on my understanding of the ROCm docs, that bit needs to be enabled alongside `ReqEn` correct? Would you happen to know what the register bit for the routing bit is? Or alternatively, how to set `DEVCTL2.ATOMICOP_REQUESTER_ENABLE ` 

---

### 评论 #13 — zichguan-amd (2025-01-02T20:02:41Z)

Unfortunately, the Routing bit is read only, in fact the whole DEVCAP2 register cannot be modified.

> Based on my understanding of the ROCm docs, that bit needs to be enabled alongside ReqEn correct?

You are correct, all components involved need to be PCIe atomic(routing) capable. So your current setup does not physically support PCIe atomics.

---

### 评论 #14 — adelj88 (2025-01-05T22:31:30Z)

Yea, just verified it, guess I'll stick to Windows for development for now - by the way, in relations to this [comment](https://github.com/ROCm/ROCm/issues/3470?fbclid=IwZXh0bgNhZW0CMTEAAR2HYoZpv7KqbzFQsD6xxHx1hLYaKicNw1L13iatznKNLtK21QzCsuXFn20_aem_xx3e0SXMyD4BHKc7oyiTsA#issuecomment-2326562145) made a few months back, is that still being considered?

---

### 评论 #15 — zichguan-amd (2025-01-06T14:43:58Z)

Yes, it's still under development.

---
