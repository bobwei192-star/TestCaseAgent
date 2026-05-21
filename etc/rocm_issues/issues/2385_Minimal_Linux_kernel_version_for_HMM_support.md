# Minimal Linux kernel version for HMM support 

> **Issue #2385**
> **状态**: closed
> **创建时间**: 2023-08-17T01:01:32Z
> **更新时间**: 2024-05-16T00:33:15Z
> **关闭时间**: 2024-05-16T00:33:15Z
> **作者**: vitduck
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2385

## 描述

Hi, 

What is the minimal version of Linux kernel that can support Heterogeneous Memory Management (HMM) ? 

I could not find the exact information from internet.
For instance, NVIDIA requires CUDA 12.2 and a recent version of the kernel, e.g. 6.1.24+ or 6.2.11+ 

I am using Rocky Linux 8.8 shipped with 4.18 version of the kernel. 
Before installing ROCM, I would like to check if kernel upgrade is required. 

Thanks. 


---

## 评论 (9 条)

### 评论 #1 — kentrussell (2024-01-02T18:09:57Z)

It's difficult to say, because a 4.18 kernel could have HMM backported completely into it. While that's unlikely, it's the reason that we can't nail down a specific kernel version. Some distros use an older kernel and backport everything into it, other ones are pretty bleeding-edge.
The definitive way to check, since KFD should be working on that GPU already with upstream support, is to check /sys/class/kfd/kfd/topology/nodes/*/properties

We define the support as #define HSA_CAP_SVMAPI_SUPPORTED        0x08000000

So you can use that to check if it's supported. 
For a standard base kernel, 4.18 wouldn't have HMM support by default. But for example, SUSE backported HMM support into their 5.3 kernel in SLE15 SP3. So it will vary depending on the kernel maintainer for that distro. Not a definitive answer, but that's due it being difficult to 100% definitively answer across all distros+kernels. Hopefully the above info will help

---

### 评论 #2 — vitduck (2024-01-04T07:09:24Z)

Hi @kentrussell 

Thanks for answering the question. 
Unfortunately, I no longer have access to the test server to check `/sys/class/kfd/kfd/topology/nodes/*/properties` as suggested. 

I agree on the issue of kernel back porting. 
But I appreciate if AMD documentation is more explicit, especially when official hardware support is severe lacking. 
As mentioned in my opening post, NVIDIA is very explicit about the conditions of HMM, which saves us from trial and error. 
AMD ecosystem is very  esoteric and only handful of individuals, such as yourself knows what is going on.  

I much appreciate if you can clarify some follow up question. 
- Is HMM also tied to a specific version of ROCm ? 
- Does `XNACK`, i.e. automatic page migration, depends on HMM ? 
   My impression from reading Frontier user guide is that XNACK does not work correctly without HMM. 
   In case of NVIDIA, they are separated. So `cudaMallocManaged` does not require HMM, while `hipMallocManaged` does. 
- HSA did not catch on after Kaeveri and has since re-purposed as a thin layer between ROCm runtime and hardware.  
  However, I could not find further information on the role of HSA within ROCm. 
  HSA was orginally designed for APU, so how was it adopted to dGPU ? 

Thanks 

---

### 评论 #3 — kentrussell (2024-01-04T14:13:11Z)

HMM support: The official declaration of ROCm HMM support came in ROCm 4.5 (https://cgmb-rocm-docs.readthedocs.io/en/latest/Current_Release_Notes/Current-Release-Notes.html) . The official line at the time was:
_This feature is only supported on recent Linux kernels. Currently, it works on Ubuntu versions with 5.6 or newer kernels and the DKMS driver from ROCm. Current releases of RHEL and SLES do not support this feature yet. Future releases of those distributions will add support for this. The unified memory feature is also supported in the KFD driver included with upstream kernels starting from Linux 5.14._
So officially we say 5.6 kernel with the ROCm DKMS kernel package, or upstream kernel from 5.14 onward. But again, backports are a thing, so it's not a rigid requirement where a kernel HAS to be 5.6-based. But it's a reasonable baseline for HMM support, since that's when it went into Linus' master branch. But I agree, it's annoying that the support message got lost in subsequent releases. If nothing else, 5.6-based kernels and newer will have it for sure. Older ones you'd have to manually look. Per the KFD Kconfig, CONFIG_HSA_SVM requires HSA_AMD and DEVICE_PRIVATE, as well as HMM_MIRROR and MMU_NOTIFIER . If you've got those enabled, then SVM will work when you install the kernel DKMS package.
.
XNACK: Yes, HMM is required for XNACK. I don't think we explicitly state it anywhere in our docs, In the kernel we have it ifdef'd with https://github.com/ROCm/ROCK-Kernel-Driver/blob/master/drivers/gpu/drm/amd/amdkfd/kfd_chardev.c#L1077 .So if HMM (CONFIG_AMD_SVM) isn't enabled, trying to set/get xnack mode returns -EPERM. So one can infer it, but only after trying to do it on a system without HMM enabled.
.
HSA: HSA wasn't suitable for dGPU, so it morphed into ROCr to do what we were trying to achieve with HSA. Then ROCr continued to change and improve as it went along, so we're not able to fit inside the HSA specifications anymore. But what HSA was trying to achieve has been supported in ROCr, namely APUs, dGPUs and APUs+dGPUs working together on the same task with shared memory and all that good stuff that HSA was designed for.

---

### 评论 #4 — vitduck (2024-01-10T06:46:36Z)

> But I agree, it's annoying that the support message got lost in subsequent releases. If nothing else, 5.6-based kernels and newer will have it for sure. Older ones you'd have to manually look. Per the KFD Kconfig, CONFIG_HSA_SVM requires HSA_AMD and DEVICE_PRIVATE, as well as HMM_MIRROR and MMU_NOTIFIER . If you've got those enabled, then SVM will work when you install the kernel DKMS package.

At the time of testing, we couldn't find this information on the 5.x release notes. 
But I will include the kernel requirements to our internal documentations. Thanks for the clarification. 

> Yes, HMM is required for XNACK

Forcing automatic page migration via  `export HSA_XNACK=1` and `amdgpu.noretry=0` resulted in a segmentation fault that we did not manage to resolve, even  on 6.2 kernel branch. 

But I can understand the difference between CUDA and HIP a little better: 
1. CUDA's UVM:  
- Page migration is handled by GPU driver in tandem with far-fault registers, i.e hardware-oriented. 
- HMM is only recently introduced to allow direct passing of `malloc()` pointers to devices

2. HIP's XNACK: 
- Page migration is handled by Linux kernel via HMM since AMD does not  have specific registers to handle page fault events. 
- HMM works ubiquitously with both `malloc()` and `hipMallocManaged()` 

Thus, the most important difference in term of performance will be the degree of overheading of driver and kernel for CUDA and HIP, respectively.  This was what we trying to measure since UVM typical degrade performance with frequent data migrations. 
Is my understanding correct ? 

> But what HSA was trying to achieve has been supported in ROCr, namely APUs, dGPUs and APUs+dGPUs working together on the same task with shared memory and all that good stuff that HSA was designed for.

The following picture is taken from CDNA 3 white paper: 
![image](https://github.com/ROCm/ROCm/assets/575950/f0cd8b16-96ac-4e09-9846-49c3865f4faa)

This schematic representation is very close to what HSA initial proposed. But as I understand: 
- HSA proposed a unified page table for CPU and GPU, eliminating the need of  address translation service
- MI300A has unified memory.  Does this also imply or guarantee the existence of unified page table as well ?

Please pardon me if some of the questions come off as basic. 
Our users would probably have no issue transition to AMD. 
But as infrastructure management, we need to prepare technical documentations and right now information is quite sparse. 

---

### 评论 #5 — kentrussell (2024-01-18T14:47:55Z)

It's quite alright. While the grand vision of 1 unified page table using IOMMU v2 couldn't provide best results, we've got a single unified address space in userspace. The kernel has separate page tables for CPU and GPU however. On the MI300As, we're using HMM to handle this. But the final answer is that there's no single unified page table. There's a single unified address space for userspace, but the kernel still separates the CPU and GPU tables. Hopefully that helps!

---

### 评论 #6 — kentrussell (2024-01-18T14:48:00Z)

It's quite alright. While the grand vision of 1 unified page table using IOMMU v2 couldn't provide best results, we've got a single unified address space in userspace. The kernel has separate page tables for CPU and GPU however. On the MI300As, we're using HMM to handle this. But the final answer is that there's no single unified page table. There's a single unified address space for userspace, but the kernel still separates the CPU and GPU tables. Hopefully that helps!

---

### 评论 #7 — vitduck (2024-01-23T08:47:32Z)

Thanks for clarification. 

I would like to confirm one more thing regarding `XNACK` before closing this issue. 
If we look at the isa table https://github.com/ROCm/ROCR-Runtime/blob/master/src/core/runtime/isa.cpp 

```
  ISAREG_ENTRY_GEN("gfx906",                 9, 0, 6,  any,         any,         64)
  ISAREG_ENTRY_GEN("gfx906:xnack-",          9, 0, 6,  any,         disabled,    64)
  ISAREG_ENTRY_GEN("gfx906:xnack+",          9, 0, 6,  any,         enabled,     64)
  ISAREG_ENTRY_GEN("gfx906:sramecc-",        9, 0, 6,  disabled,    any,         64)
  ISAREG_ENTRY_GEN("gfx906:sramecc+",        9, 0, 6,  enabled,     any,         64)
  ISAREG_ENTRY_GEN("gfx906:sramecc-:xnack-", 9, 0, 6,  disabled,    disabled,    64)
  ISAREG_ENTRY_GEN("gfx906:sramecc-:xnack+", 9, 0, 6,  disabled,    enabled,     64)
  ISAREG_ENTRY_GEN("gfx906:sramecc+:xnack-", 9, 0, 6,  enabled,     disabled,    64)
  ISAREG_ENTRY_GEN("gfx906:sramecc+:xnack+", 9, 0, 6,  enabled,     enabled,     64)
  ISAREG_ENTRY_GEN("gfx1100",                11, 0, 0, unsupported, unsupported, 32)
```
The existence of `xnack-` and `xnack+` implies that `gfx906` supports `XNACK` whereas the enthusiast-class `gfx1100` cannot.  
Unless this is sensitive information, and you don't want to disclose it (which is totally fine): 

- Is this due to a specific hardware limitation in `gfx1100` albeit being a new architecture ? 
- From our discussion so far, it is understood that the `XNACK` feature relied on HMM, a generic features of Linux kernel. 
   Thus, will `XNACK` be eventually extended to to gfx11-class GPUs in the future ? 

---

### 评论 #8 — kentrussell (2024-05-14T16:30:23Z)

The list there comprises the current support for the various ASICs. These are determined by a number of different criteria, including HW capabilities. We don’t often declare XNACK support after-the-fact, as this will usually be formally established when the code is merged during ASIC bringup. IE If it’s not supported now, it’s very unlikely to be supported later.

Not to say that it cannot happen, but there are a number of reasons why XNACK may be supported or not supported, and those are usually established during bringup before the ASIC-specific code is merged into the various projects and the product is released. I know that this isn’t a direct answer, but unfortunately that’s all of the information that is available on gfx10/gfx11 XNACK support at this time. As of right now, MI products are the only products with XNACK support in ROCm.


---

### 评论 #9 — vitduck (2024-05-16T00:33:12Z)

Thanks for clarifying many of our confusions. 
 
I would like to close the issue. 

---
