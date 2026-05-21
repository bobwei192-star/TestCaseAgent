# amdgpu-dkms: make[2]: /bin/sh: Argument list too long

> **Issue #2317**
> **状态**: closed
> **创建时间**: 2023-07-07T08:50:52Z
> **更新时间**: 2023-07-07T09:14:28Z
> **关闭时间**: 2023-07-07T09:14:28Z
> **作者**: resendarx
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2317

## 描述

I've been following this guide https://docs.amd.com/en/docs-5.3.0/deploy/linux/os-native/install.html to get ROCm on Linux Mint 21.1 (based on Ubuntu 22 jammy) but amgdpu-dkms fails to build with the following log:

```
DKMS make.log for amdgpu-5.18.2.22.40-1483871.22.04 for kernel 5.15.0-76-generic (amd64)
make: Entering directory '/usr/src/linux-headers-5.15.0-76-generic'
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/Makefile:26: "Local GCC version 110303 does not match kernel compiler GCC version 110300"
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/Makefile:27: "This may cause unexpected and hard-to-isolate compiler-related issues"
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/drm_gem_ttm_helper.o
(snip)
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/amdgpu_amdkfd_gfx_v11.o
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../amdkfd/kfd_debug.c: In function ‘kfd_dbg_trap_device_snapshot’:
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../amdkfd/kfd_debug.c:963:1: warning: the frame size of 1080 bytes is larger than 1024 bytes [-Wframe-larger-than=]
  963 | }
      | ^
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/amdgpu_amdkfd_rlc_spm.o
(snip)
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/clk_mgr/dce110/dce110_clk_mgr.o
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/dml/dcn32/display_mode_vba_util_32.c: In function ‘dml32_CalculateVMRowAndSwath’:
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/dml/dcn32/display_mode_vba_util_32.c:2226:1: warning: the frame size of 1152 bytes is larger than 1024 bytes [-Wframe-larger-than=]
 2226 | } // CalculateVMRowAndSwath
      | ^
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/clk_mgr/dce112/dce112_clk_mgr.o
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/clk_mgr/dce120/dce120_clk_mgr.o
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/clk_mgr/dcn10/rv1_clk_mgr.o
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/dml/dcn32/display_mode_vba_util_32.c: In function ‘dml32_UseMinimumDCFCLK’:
/var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/dml/dcn32/display_mode_vba_util_32.c:3116:1: warning: the frame size of 1376 bytes is larger than 1024 bytes [-Wframe-larger-than=]
 3116 | }
      | ^
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../display/dc/clk_mgr/dcn10/rv1_clk_mgr_vbios_smu.o
(snip)
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../backport/kcl_drm_drv.o
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../backport/kcl_drm_gem_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../backport/kcl_drm_gem_framebuffer_helper.o
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../backport/kcl_drm_gem.o
  CC [M]  /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/../backport/kcl_drm_modeset_helper.o
make[2]: /bin/sh: Argument list too long
make[2]: *** [scripts/Makefile.build:494: /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu/amdgpu.o] Error 127
make[1]: *** [scripts/Makefile.build:560: /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build/amd/amdgpu] Error 2
make: *** [Makefile:1914: /var/lib/dkms/amdgpu/5.18.2.22.40-1483871.22.04/build] Error 2
make: Leaving directory '/usr/src/linux-headers-5.15.0-76-generic'
```

Steps to reproduce (tested on fresh installation of Linux Mint with `apt update ; apt upgrade -y` afterwards):
1. Follow this guide https://docs.amd.com/en/docs-5.3.0/deploy/linux/os-native/install.html for Ubuntu 22.04 right as it says in steps "1. Download and convert the package signing key" and "2. Add the AMDGPU Repository and Install the Kernel-mode Driver"
2. On step "3. Add the ROCm Repository" replace `for ver in 5.2.1 5.3; do` with `for ver in 5.3; do` otherwise `apt` will complain about HTTP 404 error code.
3. Proceed to step "4. Install packages". To produce the log above I ran this command: `LANGUAGE=en-US.UTF-8 sudo apt install rocm-hip-runtime`
4. Get the "Argument list too long" error

---

## 评论 (1 条)

### 评论 #1 — resendarx (2023-07-07T09:14:28Z)

My bad, haven't noticed it's an outdated version. Installing the latest version of HIP (v5.6.0 at the time of writing) went just fine.

---
