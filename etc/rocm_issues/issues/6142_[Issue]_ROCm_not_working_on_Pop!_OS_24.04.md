# [Issue]: ROCm not working on Pop!_OS 24.04

> **Issue #6142**
> **状态**: closed
> **创建时间**: 2026-04-11T21:55:24Z
> **更新时间**: 2026-04-14T17:59:51Z
> **关闭时间**: 2026-04-14T17:59:51Z
> **作者**: peastman
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6142

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

I just got a new computer (System76 Thelio Mira) with a Radeon RX 9070 XT and Pop!_OS 24.04.  It came with AMDGPU preinstalled, and I installed ROCm following the instructions at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html.  I can compile programs that use ROCm, but when I try to run anything that uses HIP or OpenCL, it fails to find any device. 

Here is the output of `rocminfo`, which is confusing.

```
ROCk module is loaded
Unable to open /dev/kfd read-write: Permission denied
peastman is member of render group
```

As it says, I'm in the `render` group, and `ls -l` confirms that's the group it belongs to:

```
crw-rw---- 1 root render 234, 0 Apr 11 12:15 /dev/kfd
```

So why is permission denied?  Here is the output of `clinfo`:

```
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3581.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 0
```

And here is `rocm-smi`:

```
========================================= ROCm System Management Interface =========================================
=================================================== Concise Info ===================================================
Device  Node  IDs              Temp    Power   Partitions          SCLK   MCLK     Fan  Perf  PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)   (Mem, Compute, ID)                                                  
====================================================================================================================
0       1     0x7550,   45211  31.0°C  15.0W   N/A, N/A, 0         36Mhz  96Mhz    0%   auto  330.0W  6%     3%    
1       2     0x13c0,   21194  35.0°C  0.009W  N/A, N/A, 0         N/A    2800Mhz  0%   auto  N/A     3%     0%    
====================================================================================================================
=============================================== End of ROCm SMI Log ================================================
```

I assume one of those is the CPU and the other is the GPU.  But `clinfo` doesn't find any devices.

### Operating System

Pop!_OS 24.04

### CPU

AMD Ryzen 9 9900X

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

7.2.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

See above.

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — darren-amd (2026-04-13T14:10:49Z)

Hi @peastman, 

Could you please try adding yourself to the video group as well? Please follow the instructions available [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#using-group-membership), and let me know if you run into any issues, thanks!

---

### 评论 #2 — peastman (2026-04-14T17:59:51Z)

I was already in the video group, so that wasn't the problem.  But it has started working on its own!  I spent a lot of time yesterday debugging a different problem where the computer couldn't recognize the keyboard, and at some point in the process ROCm started working.  I'm not sure what it was that did it.  Perhaps it just needed a reboot?

Thanks for your help!

---
