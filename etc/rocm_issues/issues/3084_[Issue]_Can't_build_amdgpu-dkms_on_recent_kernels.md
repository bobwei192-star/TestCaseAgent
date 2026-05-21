# [Issue]: Can't build amdgpu-dkms on recent kernels

> **Issue #3084**
> **状态**: closed
> **创建时间**: 2024-05-04T12:07:53Z
> **更新时间**: 2024-05-21T15:43:19Z
> **关闭时间**: 2024-05-21T15:43:18Z
> **作者**: G-Guillard
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3084

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

As mentioned in [this comment](https://github.com/ROCm/ROCm/issues/2939#issuecomment-2043411225), issue reported in #2939 isn't Ubuntu specific but kernel-related.

The main error, `‘MAX_ORDER’ undeclared here`, is due to [this change](https://github.com/torvalds/linux/commit/5e0a760b44417f7cadd79de2204d6247109558a0) in the kernel source.  It is easy to fix, just replace the few occurrences of `MAX_ORDER + 1` into `NR_PAGE_ORDERS` and of `MAX_ORDER` into `NR_PAGE_ORDERS - 1` in the following files :

/usr/src/amdgpu-6.7.0-1756574.22.04/ttm/ttm_pool.c
/usr/src/amdgpu-6.7.0-1756574.22.04/ttm/tests/ttm_pool_test.c
/usr/src/amdgpu-6.7.0-1756574.22.04/ttm/tests/ttm_device_test.c
/usr/src/amdgpu-6.7.0-1756574.22.04/include/drm/ttm/ttm_pool.h

However the build also fails on two other issues.

The first one, `error: ‘I2C_CLASS_DDC’ undeclared (first use in this function); did you mean ‘I2C_CLASS_SPD’?` is related to [this change](https://github.com/torvalds/linux/commit/b60db383e2ba64a18e49b6bef3be1ab18aa159f1) in the kernel source and can be fixed by adding `#define I2C_CLASS_DDC		(1<<3)	/* DDC bus on graphics adapters */` to `amd/display/amdgpu_dm/amdgpu_dm.h` and `amd/amdgpu/amdgpu_i2c.h`.

The last one, `too few arguments to function ‘drm_exec_init’`, can simply be fixed by adding a 0 argument to calls to this function (e.g. `drm_exec_init(&exec, DRM_EXEC_IGNORE_DUPLICATES);` -> `drm_exec_init(&exec, DRM_EXEC_IGNORE_DUPLICATES, 0);`).

I don't know how to check if the module works as expected after that, but at least it builds.

As I'm a complete kernel noob, I'm not sure whether there may be side effects by this modifications.  The first one should be pretty safe as I understand it.  The commit comment of the I2C one is not very reassuring.  I think the last one should also be safe.

### Operating System

GNU/Linux

NB : GPU randomly selected as mine is not in the list (Lucienne). Same for ROCm, 6.7 is not in the list.

---

## 评论 (4 条)

### 评论 #1 — countradooku (2024-05-04T15:38:24Z)

dkms is only avilable on kernel 6.5 maximum

---

### 评论 #2 — ppanchad-amd (2024-05-07T15:52:20Z)

@G-Guillard Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — nairboon (2024-05-18T13:25:44Z)

> dkms is only avilable on kernel 6.5 maximum


The latest release 6.1.1 seems to compile on kernel 6.8

---

### 评论 #4 — ppanchad-amd (2024-05-21T15:43:18Z)

@nairboon Thank you for verifying with the latest build

---
