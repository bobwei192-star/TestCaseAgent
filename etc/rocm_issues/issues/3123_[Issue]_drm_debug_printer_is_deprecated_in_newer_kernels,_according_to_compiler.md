# [Issue]:  drm_debug_printer is deprecated in newer kernels, according to compiler it seems to be with drm_dbg_printer

> **Issue #3123**
> **状态**: closed
> **创建时间**: 2024-05-13T13:41:13Z
> **更新时间**: 2024-05-13T14:33:50Z
> **关闭时间**: 2024-05-13T14:27:08Z
> **作者**: waheedi
> **标签**: AMD Radeon VII, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3123

## 标签

- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Right now I'm using kernel master version, and I also have most of the 6.0+ kernels already I tried with 6.8 and 6.9 to install the 6.1.1 version (according to this issue #2939  , 6.1.1 seems to have some parts fixed for kernels 6.3+ but right now it fails with the below) :

```DKMS make.log for amdgpu-6.7.0-1769056.22.04 for kernel 6.8.0-rc6bargos+ (x86_64)
Mon May 13 02:49:27 PM CEST 2024
make: Entering directory '/home/bargo/projects/linux'
  CC [M]  /tmp/amd.EEGT9edr/scheduler/sched_main.o
  CC [M]  /tmp/amd.EEGT9edr/scheduler/sched_fence.o
  CC [M]  /tmp/amd.EEGT9edr/scheduler/sched_entity.o
  CC [M]  /tmp/amd.EEGT9edr/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /tmp/amd.EEGT9edr/amd/amdxcp/./backport/kcl_drm_drv.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_tt.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_bo.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_bo_util.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_bo_vm.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_module.o
  CC [M]  /tmp/amd.EEGT9edr/drm_gem_ttm_helper.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_execbuf_util.o
  CC [M]  /tmp/amd.EEGT9edr/amd/amdkcl/main.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_range_manager.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_resource.o
  CC [M]  /tmp/amd.EEGT9edr/amd/amdgpu/amdgpu_drv.o
/tmp/amd.EEGT9edr/amd/amdkcl/main.c:16:12: warning: no previous prototype for ‘amdkcl_init’ [-Wmissing-prototypes]
   16 | int __init amdkcl_init(void)
      |            ^~~~~~~~~~~
/tmp/amd.EEGT9edr/amd/amdkcl/main.c:33:13: warning: no previous prototype for ‘amdkcl_exit’ [-Wmissing-prototypes]
   33 | void __exit amdkcl_exit(void)
      |             ^~~~~~~~~~~
  CC [M]  /tmp/amd.EEGT9edr/amd/amdkcl/kcl_common.o
  LD [M]  /tmp/amd.EEGT9edr/amd/amdxcp/amdxcp.o
  CC [M]  /tmp/amd.EEGT9edr/ttm/ttm_pool.o
  CC [M]  /tmp/amd.EEGT9edr/amd/amdkcl/kcl_kernel_params.o
/tmp/amd.EEGT9edr/ttm/ttm_bo.c: In function ‘ttm_bo_mem_space_debug’:
/tmp/amd.EEGT9edr/ttm/ttm_bo.c:55:32: error: implicit declaration of function ‘drm_debug_printer’; did you mean ‘drm_dbg_printer’? [-Werror=implicit-function-declaration]
   55 |         struct drm_printer p = drm_debug_printer(TTM_PFX);
      |                                ^~~~~~~~~~~~~~~~~
      |                                drm_dbg_printer
/tmp/amd.EEGT9edr/ttm/ttm_bo.c:55:32: error: invalid initializer
cc1: some warnings being treated as errors
```

### Operating System

Ubuntu 22.04.03 (custom kernel config, but no code changes)
6.8.0-rc6bargos+
same as 6.9.0-rc

### CPU

Ryzen 7 2700X

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIP, ROCm

### Steps to Reproduce

`apt install ./amdgpu-install_6.1.60101-1_all.deb && amdgpu-install -y --usecase=rocm,hiplibsdk,mlsdk`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — kentrussell (2024-05-13T14:27:08Z)

This was resolved after 6.1 branched, by https://lists.freedesktop.org/archives/intel-xe/2024-January/023155.html . You can apply that yourself manually to the amdgpu-dkms code, or wait for ROCm 6.2 to roll out with that patch included.

---

### 评论 #2 — waheedi (2024-05-13T14:33:49Z)

@kentrussell that was quick Kent, thank you :)

---
