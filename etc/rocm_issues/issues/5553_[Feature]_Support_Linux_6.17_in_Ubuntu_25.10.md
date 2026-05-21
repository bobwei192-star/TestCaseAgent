# [Feature]: Support Linux 6.17 in Ubuntu 25.10

> **Issue #5553**
> **状态**: closed
> **创建时间**: 2025-10-21T18:09:43Z
> **更新时间**: 2025-10-22T15:31:44Z
> **关闭时间**: 2025-10-22T15:31:44Z
> **作者**: ianbmacdonald
> **标签**: Feature Request, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5553

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Suggestion Description

Currently the ROCm 7.02 drivers are ABI compatible with Ubuntu 25.04, so desktop users will prefer the newer distribution for Radeon / Strix Halo to take advantage of newer software, kernels, performance, hardware support, etc. 

Moving from 25.04 is a common upgrade pattern, so supporting 25.10  for users on Strix Halo and discrete Radeon GPUs make sense. 

Note: Related upstream patches for MES for Strix Halo are merged in to 6.18rc2, as well as current -proposed on 6.14, so we expect them in 6.17 as well. 

https://github.com/torvalds/linux/commit/1fb710793ce2619223adffaf981b1ff13cd48f17

https://bugs.launchpad.net/ubuntu/+source/linux-oem-6.14/+bug/2125201
* [noble] Fix system hang observed with comfy-ui (LP: [#2125201](https://bugs.launchpad.net/bugs/2125201))
    - drm/amd/include : Update MES v12 API for fence update
    - SAUCE: drm/amdgpu: Enable MES lr_compute_wa by default

### Operating System

Ubuntu 25.10

### GPU

gfx1151, gfx1100

### ROCm Component

amdgpu 6.14.14

---

## 评论 (3 条)

### 评论 #1 — ianbmacdonald (2025-10-21T18:13:05Z)

Here is the current dkms build log with a collection of errors, vibe summarized as:

dma-fence API: your tree defines __dma_fence_is_later(u64,u64) but 6.17 provides __dma_fence_is_later(struct dma_fence*, u64, u64) → hard type conflict.

mm/vm types: KCL re-typedefs vm_fault_t to int and wraps vmf_insert_*, but in 6.17 vm_fault_t is a bitwise unsigned int and the prototypes differ → multiple redefinition/implicit-decl errors.

TTM writeback path: references to mapping->a_ops->writepage and writeback_control.for_reclaim no longer match 6.17’s address_space_operations → compile errors.

[ubuntu2510_dkms_fail.txt](https://github.com/user-attachments/files/23028222/ubuntu2510_dkms_fail.txt)

---

### 评论 #2 — harkgill-amd (2025-10-21T19:16:10Z)

Hi @ianbmacdonald, `amdgpu-dkms` support for linux kernel 6.17 is planned for a future ROCm release. 

Just a quick reminder that users on Strix Halo shouldn't be installing the `amdgpu-dkms` package and should run with the in-kernel drivers already present. https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#prepare-the-system. While the 6.14 OEM kernel is recommended, I know user's have got this working on mainline 6.14 kernels as well - might be worth giving a try with 6.17.

---

### 评论 #3 — ianbmacdonald (2025-10-22T15:29:06Z)

DoH.  Not sure why I assumed newer was not already upstreamed.  Of course, there is no need for dkms with this open source stack, and it existing to simply backport ROCm to older Ubuntu versions like 22.x and 24.x.  

This is where CUDA habits of needing dkms to bind a closed source driver caused me to have momentary blinders.  The funny thing is, that when I vibe summarized the dkms failure log in GPT5, one of the outcomes suggested dropping dkms altogether, and I just dismissed it as hallucination, further cementing my bias away from the seemingly obvious right answer. 

Okay, so the real missing pieces are just the MES bits which do not actually appear in 6.17 OEM, and that is not a ROCm thing. 

```
amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.0.2+39589fda      amdgpu version: 6.17.0-5 ROCm version: 7.0.2    |
| Platform: Linux Baremetal                                                    |
|-------------------------------------+----------------------------------------|
| BDF                        GPU-Name | Mem-Uti   Temp   UEC       Power-Usage |
| GPU  HIP-ID  OAM-ID  Partition-Mode | GFX-Uti    Fan               Mem-Usage |
|=====================================+========================================|
| 0000:c5:00.0  Radeon 8060S Graphics | N/A        N/A   0             N/A/0 W |
|   0       0     N/A             N/A | N/A        N/A              161/512 MB |
+-------------------------------------+----------------------------------------+
+------------------------------------------------------------------------------+
| Processes:                                                                   |
|  GPU        PID  Process Name          GTT_MEM  VRAM_MEM  MEM_USAGE     CU % |
|==============================================================================|
|  No running processes found                                                  |
+------------------------------------------------------------------------------+
```

Thanks for the bump

---
