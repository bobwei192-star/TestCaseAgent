# [Issue]:  DKMS compile error debian testing Kernel 6.5

> **Issue #2694**
> **状态**: closed
> **创建时间**: 2023-12-06T21:42:24Z
> **更新时间**: 2024-06-19T17:17:54Z
> **关闭时间**: 2024-06-19T17:17:54Z
> **作者**: ithuis
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2694

## 描述

### Problem Description

i am trying to install drivers via

amdgpu-install --no-32 


then i get the compile error 

DKMS make.log for amdgpu-6.2.4-1646729.22.04 for kernel 6.5.0-5-amd64 (amd64)
wo  6 dec 2023 22:36:56 CET
make: Map '/usr/src/linux-headers-6.5.0-5-amd64' wordt binnengegaan
/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/Makefile:52: *** dma_resv->seq is missing. exit....  Gestopt.
make[1]: *** [/usr/src/linux-headers-6.5.0-5-common/Makefile:2059: /var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build] Fout 2
make: *** [/usr/src/linux-headers-6.5.0-5-common/Makefile:246: __sub-make] Fout 2
make: Map '/usr/src/linux-headers-6.5.0-5-amd64' wordt verlaten


### Operating System

Debian testing

### CPU

AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics

### GPU

AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics

### ROCm Version

5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

amdgp-install --no-32

### Output of /opt/rocm/bin/rocminfo --support

ROCk module is NOT loaded, possibly no GPU devices

---

## 评论 (6 条)

### 评论 #1 — nairboon (2023-12-28T10:42:03Z)

The kernel is probably too new and not yet supported. See also #2451 and #2458 

---

### 评论 #2 — nairboon (2024-01-02T07:58:26Z)

Just for info:
The modifications from https://github.com/ROCm/ROCm/issues/2458#issuecomment-1806014506 alone are not sufficient and further modifications in the KCL are needed to compile with 6.5.15.
> If you want a quick-and-dirty workaround, just remove line 29, and 31-41. Or remove calls to kcl_get_user_pages_remote and replace them with the standard get_user_pages_remote() calls, with the right parameters:
> long get_user_pages_remote(struct mm_struct *mm,
> unsigned long start, unsigned long nr_pages,
> unsigned int gup_flags, struct page **pages,
> int *locked);

`CC [M]  /var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_ioctl.o /var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/ttm/ttm_bo_vm.c: In function ‘amdttm_bo_mmap_obj’:
  CC [M]  /var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_kthread.o
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/ttm/ttm_bo_vm.c:602:23: error: assignment of read-only member ‘vm_flags’
602 |         vma->vm_flags |= VM_PFNMAP;
       |                       ^~
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/ttm/ttm_bo_vm.c:603:23: error: assignment of read-only member ‘vm_flags’
  603 |         vma->vm_flags |= VM_IO | VM_DONTEXPAND | VM_DONTDUMP;
      |                       ^~
  CC [M]  /var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_memory.o
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdgpu/amdgpu_ttm.c: In function ‘amdgpu_ttm_tt_get_user_pages’:
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdgpu/amdgpu_ttm.c:830:24: error: ‘struct mm_struct’ has no member named ‘mmap_sem’; did you mean ‘mmap_base’?
  830 |         down_read(&mm->mmap_sem);
      |                        ^~~~~~~~
      |                        mmap_base
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdgpu/amdgpu_ttm.c:842:38: error: ‘struct mm_struct’ has no member named ‘mmap_sem’; did you mean ‘mmap_base’?
  842 |                         up_read(&mm->mmap_sem);
      |                                      ^~~~~~~~
      |                                      mmap_base
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdgpu/amdgpu_ttm.c:877:22: error: ‘struct mm_struct’ has no member named ‘mmap_sem’; did you mean ‘mmap_base’?
  877 |         up_read(&mm->mmap_sem);
      |                      ^~~~~~~~
      |                      mmap_base
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdgpu/amdgpu_ttm.c:882:22: error: ‘struct mm_struct’ has no member named ‘mmap_sem’; did you mean ‘mmap_base’?
  882 |         up_read(&mm->mmap_sem);
      |                      ^~~~~~~~
      |                      mmap_base
  CC [M]  /var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_drm_fb.o
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_memory.c: In function ‘vmf_insert_pfn_pmd_prot’:
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_memory.c:86:18: error: assignment of member ‘vma’ in read-only object
   86 |         cvmf.vma = &cvma;
      |                  ^
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_memory.c: In function ‘vmf_insert_pfn_pud_prot’:
/var/lib/dkms/amdgpu/6.2.4-1666569.22.04/build/amd/amdkcl/kcl_memory.c:105:18: error: assignment of member ‘vma’ in read-only object
  105 |         cvmf.vma = &cvma; `
 




---

### 评论 #3 — kentrussell (2024-01-02T17:45:19Z)

This should be addressed in ROCm 6.1 once we move to a 6.5-based kernel. 

---

### 评论 #4 — ppanchad-amd (2024-05-17T17:14:29Z)

@ithuis Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

---

### 评论 #5 — MirtoBusico (2024-05-17T17:19:51Z)

> @ithuis Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

I'll try ASAP
But in Debian testing the kernel version is
`Linux bianco500 6.7.12-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.7.12-1 (2024-04-24) x86_64 GNU/Linux`

---

### 评论 #6 — nairboon (2024-05-18T13:12:57Z)

> @ithuis Can you please test with latest ROCm 6.1.1? If resolved, please close ticket. Thanks!

I compiled it on 6.5 (`amdgpu/6.7.0-1769056.22.04, 6.5.11-4-liquorix-amd64, x86_64: installed`)
and it runs on 6.8.10 :+1:

---
