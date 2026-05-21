# [Issue]: Ubuntu 64-bit 24.04 daily installation - fails to install

> **Issue #2939**
> **状态**: closed
> **创建时间**: 2024-03-03T16:36:41Z
> **更新时间**: 2024-08-28T18:27:29Z
> **关闭时间**: 2024-08-28T18:27:29Z
> **作者**: cscd98
> **标签**: Feature Request, Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2939

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

sudo apt install amdgpu-dkms
```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
amdgpu-dkms is already the newest version (1:6.3.6.60002-1718217.22.04).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
1 not fully installed or removed.
After this operation, 0 B of additional disk space will be used.
Do you want to continue? [Y/n] y
Setting up amdgpu-dkms (1:6.3.6.60002-1718217.22.04) ...
Removing old amdgpu-6.3.6-1718217.22.04 DKMS files...
Deleting module amdgpu-6.3.6-1718217.22.04 completely from the DKMS tree.
Loading new amdgpu-6.3.6-1718217.22.04 DKMS files...
Building for 6.8.0-11-generic
Building for architecture x86_64
Building initial module for 6.8.0-11-generic
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.crash'
Error! Bad return status for module build on kernel: 6.8.0-11-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status 10
Errors were encountered while processing:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

cat /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/make.log
```
DKMS make.log for amdgpu-6.3.6-1718217.22.04 for kernel 6.8.0-11-generic (x86_64)
Sun Mar  3 04:17:26 PM GMT 2024
make: Entering directory '/usr/src/linux-headers-6.8.0-11-generic'
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-13 (Ubuntu 13.2.0-13ubuntu1) 13.2.0
  You are using:           gcc-13 (Ubuntu 13.2.0-16ubuntu1) 13.2.0
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/sched_main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/sched_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/sched_entity.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdxcp/./backport/kcl_drm_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_tt.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/drm_gem_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_vm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_module.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_common.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_execbuf_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/drm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/main.c:16:12: warning: no previous prototype for ‘amdkcl_init’ [-Wmissing-prototypes]
   16 | int __init amdkcl_init(void)
      |            ^~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/main.c:33:13: warning: no previous prototype for ‘amdkcl_exit’ [-Wmissing-prototypes]
   33 | void __exit amdkcl_exit(void)
      |             ^~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_kernel_params.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_range_manager.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_common.c:30:6: warning: no previous prototype for ‘amdkcl_symbol_init’ [-Wmissing-prototypes]
   30 | void amdkcl_symbol_init(void)
      |      ^~~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/dma-buf/dma-resv.o
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo.c:37:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h: At top level:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_vm.c:37:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h: At top level:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_execbuf_util.c:30:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h: At top level:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
cc1: some warnings being treated as errors
cc1: some warnings being treated as errors
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/drm_gem_ttm_helper.h:10,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/drm_gem_ttm_helper.c:5:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h: At top level:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_util.c:34:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h: At top level:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_tt.c:45:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h: At top level:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_vm.o] Error 1
make[3]: *** Waiting for unfinished jobs....
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo.o] Error 1
cc1: some warnings being treated as errors
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_backlight.o
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_module.o] Error 1
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_execbuf_util.o] Error 1
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_doorbell_mgr.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_ioctl.o
make[2]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/drm_gem_ttm_helper.o] Error 1
make[2]: *** Waiting for unfinished jobs....
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_kthread.o
cc1: some warnings being treated as errors
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_tt.o] Error 1
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_util.o] Error 1
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_kms.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_io.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdxcp/amdxcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_atombios.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_seq_file.o
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:54,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/include/kcl/kcl_amdgpu_drm_fb_helper.h:37,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/backport.h:69,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/atombios_crtc.o
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/backport/backport.h:20,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h: In function ‘kcl_register_shrinker’:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/kcl/kcl_shrinker.h:16:16: error: implicit declaration of function ‘register_shrinker’; did you mean ‘kcl_register_shrinker’? [-Werror=implicit-function-declaration]
   16 |         return register_shrinker(shrinker);
      |                ^~~~~~~~~~~~~~~~~
      |                kcl_register_shrinker
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_suspend.o
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_range_manager.c:32:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h: At top level:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_io.c:69:6: warning: no previous prototype for ‘amdkcl_io_init’ [-Wmissing-prototypes]
   69 | void amdkcl_io_init(void)
      |      ^~~~~~~~~~~~~~
cc1: some warnings being treated as errors
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:60:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2903:66: error: ‘DRM_UNLOCKED’ undeclared here (not in a function); did you mean ‘VM_LOCKED’?
 2903 |         DRM_IOCTL_DEF_DRV(AMDGPU_SEM, amdgpu_sem_ioctl, DRM_AUTH|DRM_UNLOCKED|DRM_RENDER_ALLOW)
      |                                                                  ^~~~~~~~~~~~
./include/drm/drm_ioctl.h:155:26: note: in definition of macro ‘DRM_IOCTL_DEF_DRV’
  155 |                 .flags = _flags,                                        \
      |                          ^~~~~~
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_range_manager.o] Error 1
make[2]: *** [scripts/Makefile.build:481: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm] Error 2
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:10: error: ‘struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: note: (near initialization for ‘amdgpu_kms_driver.gem_prime_import_sg_table’)
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:10: error: ‘const struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: note: (near initialization for ‘amdgpu_partition_driver.gem_prime_import_sg_table’)
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_connectors.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_suspend.c:32:6: warning: no previous prototype for ‘amdkcl_suspend_init’ [-Wmissing-prototypes]
   32 | void amdkcl_suspend_init(void)
      |      ^~~~~~~~~~~~~~~~~~~
cc1: some warnings being treated as errors
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_pci.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mm.o
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.o] Error 1
make[3]: *** Waiting for unfinished jobs....
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_memory.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_sched.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_reservation.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_cache.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_sched.c:24:6: warning: no previous prototype for ‘amdkcl_sched_init’ [-Wmissing-prototypes]
   24 | void amdkcl_sched_init(void)
      |      ^~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_fb.o
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:54,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/include/kcl/kcl_amdgpu_drm_fb_helper.h:37,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/backport.h:69,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:54,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/include/kcl/kcl_amdgpu_drm_fb_helper.h:37,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/backport.h:69,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:54,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/include/kcl/kcl_amdgpu_drm_fb_helper.h:37,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/backport.h:69,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_doorbell_mgr.o] Error 1
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_print.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_crtc.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mm.c:39:6: warning: no previous prototype for ‘amdkcl_mm_init’ [-Wmissing-prototypes]
   39 | void amdkcl_mm_init(void)
      |      ^~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_reservation.c:37:6: warning: no previous prototype for ‘amdkcl_reservation_init’ [-Wmissing-prototypes]
   37 | void amdkcl_reservation_init(void)
      |      ^~~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_connector.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_atomic_helper.o
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_kms.o] Error 1
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:54,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/include/kcl/kcl_amdgpu_drm_fb_helper.h:37,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/backport.h:69,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_device_cgroup.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mn.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/amd-sched.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_modes.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_fence.c:239:6: warning: no previous prototype for ‘amdkcl_fence_init’ [-Wmissing-prototypes]
  239 | void amdkcl_fence_init(void)
      |      ^~~~~~~~~~~~~~~~~
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_device.o] Error 1
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_time.o
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_atombios.o] Error 1
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_acpi_table.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_page_alloc.o
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:54,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/include/kcl/kcl_amdgpu_drm_fb_helper.h:37,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/backport.h:69,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_numa.o
In file included from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_device.h:31,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_bo.h:40,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu.h:54,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/include/kcl/kcl_amdgpu_drm_fb_helper.h:37,
                 from /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/backport/backport.h:69,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/include/drm/ttm/ttm_pool.h:77:45: error: ‘MAX_ORDER’ undeclared here (not in a function); did you mean ‘PMD_ORDER’?
   77 |                 struct ttm_pool_type orders[MAX_ORDER];
      |                                             ^~~~~~~~~
      |                                             PMD_ORDER
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_fs_read_write.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_aperture.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_simple_kms_helper.o
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/atombios_crtc.o] Error 1
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_bitmap.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_vmscan.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_dma_fence_chain.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_device_cgroup.c:29:6: warning: no previous prototype for ‘amdkcl_dev_cgroup_init’ [-Wmissing-prototypes]
   29 | void amdkcl_dev_cgroup_init(void)
      |      ^~~~~~~~~~~~~~~~~~~~~~
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_connectors.o] Error 1
make[2]: *** [scripts/Makefile.build:481: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu] Error 2
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mce_amd.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_workqueue.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_cpumask.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_dsc_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mm_slab.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_irqdesc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_suballoc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_dp_helper.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_vmscan.c:25:6: warning: no previous prototype for ‘synchronize_shrinkers’ [-Wmissing-prototypes]
   25 | void synchronize_shrinkers(void)
      |      ^~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mce_amd.c:16:22: warning: no previous prototype for ‘kcl_smca_get_bank_type’ [-Wmissing-prototypes]
   16 | enum smca_bank_types kcl_smca_get_bank_type(unsigned int cpu, unsigned int bank)
      |                      ^~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_hdcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_debugfs_inode.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_workqueue.c:40:6: warning: no previous prototype for ‘amdkcl_workqueue_init’ [-Wmissing-prototypes]
   40 | void amdkcl_workqueue_init(void)
      |      ^~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_debugfs_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_sysfs_emit.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_numa.c:15:6: warning: no previous prototype for ‘amdkcl_numa_init’ [-Wmissing-prototypes]
   15 | void amdkcl_numa_init(void)
      |      ^~~~~~~~~~~~~~~~
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/amdkcl.o
make[1]: *** [/usr/src/linux-headers-6.8.0-11-generic/Makefile:1926: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build] Error 2
make: *** [Makefile:240: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.8.0-11-generic'

### Operating System

24.04 (Noble Numbat)

### CPU

AMD Ryzen 7 6800HS with Radeon Graphics

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

GPU is AMD Radeon™ RX 6800S, unable to select that in the GPU list..

---

## 评论 (49 条)

### 评论 #1 — smehrbrodt (2024-03-07T11:05:16Z)

Confirm, same issue here with Ubuntu 24.04 daily.

---

### 评论 #2 — nartmada (2024-03-11T17:20:52Z)

Hi @csdougliss and @smehrbrodt, 

Ubuntu 24.04 is not a supported OS.  

Please refer to this link.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

---

### 评论 #3 — cscd98 (2024-03-11T20:00:49Z)

@nartmada 24.04 is out next month. You'd think you would be working on supporting it :+1: 

---

### 评论 #4 — nartmada (2024-03-11T20:59:34Z)

I have asked the internal team to take a look.

---

### 评论 #5 — nartmada (2024-03-11T22:16:02Z)

Hi @csdougliss, Ubuntu 24.04 will be supported in an upcoming ROCm release.  

---

### 评论 #6 — nartmada (2024-03-22T14:10:54Z)

Closing this ticket for now.  When ROCm has support for Ubuntu 24.04, please re-open if you still have installation issue.  Thank you.

---

### 评论 #7 — keryell (2024-03-27T16:56:21Z)

> Hi @csdougliss, Ubuntu 24.04 will be supported in an upcoming ROCm release.

The problem is not to *be supported in an upcoming ROCm release* but from the first day Ubuntu 24.04 is out. And for that it has to be tested with pre-release versions.
This is a fair issue that should not have been closed.

---

### 评论 #8 — keryell (2024-03-27T17:02:08Z)

There were some related comments in https://github.com/ROCm/ROCm/issues/1590#issuecomment-1922965412

---

### 评论 #9 — insanie (2024-04-08T18:29:31Z)

I can confirm that the issue has nothing to do with Ubuntu version but rather kernel version. I tried this with kernels 6.5, 6.7 and 6.8 and all of them failed. It seems like module compiling is hardcoded for 6.3, or at least it needs specific headers and/or extra modules for it that are not present for anything above 6.3.
While Ubuntu 24.04 will be shipped with 6.5 and will supposedly have ROCm from its distro repo available, that's not a solution at all. I would like to have this liberty to install custom kernels and install ROCm at the same time.
I'm gonna dig into the source of amdgpu-dkms at least to understand what are the real prerequisites for its successful compilation.

---

### 评论 #10 — Wedge009 (2024-04-12T00:09:16Z)

I'm also interested in this.

> ...Ubuntu 24.04 will be supported in an upcoming ROCm release.

Understanding that there are time and resource limitations, is there an estimated time when that 'upcoming release' will be made available? I think from past experience it's often quite some time before drivers supporting a new Ubuntu version is released.

> I can confirm that the issue has nothing to do with Ubuntu version but rather kernel version.

I agree that it's often different kernels that cause difficulties. eg I still have a few pre-Vega GPUs that I use legacy OpenCL with and packages for that are only available until ROCm 5.7.1. I've found that legacy OpenCL will still install and function with kernel 6.2 (as per [support documentation](https://rocm.docs.amd.com/en/docs-5.7.1/release/gpu_os_support.html)), but not the current HWE kernel for Ubuntu 22.04, which is [kernel 6.5](https://packages.ubuntu.com/jammy-updates/linux-generic-hwe-22.04). (If I recall correctly it was indeed amdgpu-dkms that failed to configure properly.) I accept that legacy is legacy and there won't be future support for it, but [Ubuntu 22.04 is supported until April 2027](https://ubuntu.com/about/release-cycle) so at least I can stay on the older kernel for a few more years.

For my Vega GPUs, I have similar concerns about whether or not the current ROCr-based OpenCL in ROCm 6.0.x will still work with the standard kernel 6.8 that [Ubuntu 24.04 will release with](https://packages.ubuntu.com/noble/linux-generic). Even if Ubuntu 24.04 is still yet to be released I don't think it's unreasonable to leave open issues like this so they can be used as reference for future work.

(I just remembered that even support for Vega20 is deprecated in ROCm 6.0.x... and for Vega10 I have to make do with ROCm 5.7.3 with kernel 6.2 as well because otherwise my OpenCL applications break.)

---

### 评论 #11 — erkinalp (2024-04-25T19:30:38Z)

> even support for Vega20 is deprecated in ROCm 6.0.x...

For no reason, given a CDNA core is architecturally a larger Vega core.

---

### 评论 #12 — Wedge009 (2024-04-25T22:36:19Z)

To be fair, I'm sure there are still some differences between CDNA and GCN.

---

### 评论 #13 — Wedge009 (2024-04-25T23:48:56Z)

BTW, 24.04 is released now. Can this be re-opened?

---

### 评论 #14 — keryell (2024-04-26T10:20:29Z)

Reopening to celebrate the official Ubuntu 24.04 publication.

---

### 评论 #15 — erkinalp (2024-04-26T10:30:17Z)

@keryell should have been opened well well before.

---

### 评论 #16 — keryell (2024-04-26T14:56:38Z)

> @keryell should have been opened well well before.

This is just for tracking the request and avoiding someone to open again and again this request.
It is already on the roadmap and this will probably not make the roadmap faster, unfortunately.

---

### 评论 #17 — erkinalp (2024-04-26T18:18:25Z)

> It is already on the roadmap and this will probably not make the roadmap faster, unfortunately.

publish the WIP so more manpower

---

### 评论 #18 — DhruvDh (2024-05-11T01:39:30Z)

> I can confirm that the issue has nothing to do with Ubuntu version but rather kernel version. I tried this with kernels 6.5, 6.7 and 6.8 and all of them failed. It seems like module compiling is hardcoded for 6.3, or at least it needs specific headers and/or extra modules for it that are not present for anything above 6.3. While Ubuntu 24.04 will be shipped with 6.5 and will supposedly have ROCm from its distro repo available, that's not a solution at all. I would like to have this liberty to install custom kernels and install ROCm at the same time. I'm gonna dig into the source of amdgpu-dkms at least to understand what are the real prerequisites for its successful compilation.

https://github.com/ROCm/ROCm/pull/3116 mentions that ROCm 6.1.1 was tested against kernel 6.8

---

### 评论 #19 — Wedge009 (2024-05-11T02:25:57Z)

Thanks for that. I hadn't seen anything change in the documentation for 6.1.1 so I thought Ubuntu 24.04 / kernel 6.8 still wasn't supported yet.

---

### 评论 #20 — All3xJ (2024-05-13T14:39:44Z)

I have Ubuntu 24.04 and I have [this issue](https://gitlab.freedesktop.org/drm/amd/-/issues/3372)

---

### 评论 #21 — supernovae (2024-05-13T16:42:43Z)

Can anyone confirm ROCm 6.1.1 works with ubuntu 24.0.4?  I need a new kernel to fix a known crash with:

https://gitlab.freedesktop.org/drm/amd/-/issues/2282#note_1901512

Causing apps to fail/terminate on ttm_bo_delayed_delete [amdttm]

If 6.1.1 works, i'll do the uprgade to 23.0.4 -> 24.0.4

---

### 评论 #22 — supernovae (2024-05-13T18:04:45Z)

Can confirm, package dependencies don't work on 24.0.4

```he following information may help to resolve the situation:

The following packages have unmet dependencies:
 hipsolver : Depends: libcholmod3 but it is not installable
             Depends: libsuitesparseconfig5 but it is not installable
 rocm-gdb : Depends: libtinfo5 but it is not installable
            Depends: libncurses5 but it is not installable
            Depends: libpython3.10 but it is not installable or
                     libpython3.8 but it is not installable
E: Unable to correct problems, you have held broken packages.
```

---

### 评论 #23 — insanie (2024-05-13T20:12:16Z)

> The following packages have unmet dependencies:
>  hipsolver : Depends: libcholmod3 but it is not installable
>              Depends: libsuitesparseconfig5 but it is not installable
>  rocm-gdb : Depends: libtinfo5 but it is not installable
>             Depends: libncurses5 but it is not installable
>             Depends: libpython3.10 but it is not installable or
>                      libpython3.8 but it is not installable

Got the same issues on kernel 6.8.2 (Ubuntu 23.10 but it's the kernel that matters).
libcholmod3 is not even available for Ubuntu in proper way.
Python 3.10 or 3.8 doesn't even make sense - I get it 3.8 has python2 backwards compatible but 3.10 is the one that dropped this compatibility! What's the point of asking these two versions over 3.11 or 3.12 then?
So many questions...


---

### 评论 #24 — supernovae (2024-05-14T13:18:26Z)

I was able to run `apt download` to download things and `dpkg -i` with force install to get things working for C compiled tensorflow apps on 24.0.4 but it means i'll have to repair each time i run apt-update... but... it works lol.

I downloaded rocm and looking into building it to see if i could package new versions. I may work on that more later this afternoon.

---

### 评论 #25 — nairboon (2024-05-18T13:31:17Z)

> @supernovae  Can anyone confirm ROCm 6.1.1 works with ubuntu 24.0.4? I need a new kernel to fix a known crash with:

The latest release 6.1.1 compiles on kernel 6.8


> ```
> 
> The following packages have unmet dependencies:
>  hipsolver : Depends: libcholmod3 but it is not installable
>              Depends: libsuitesparseconfig5 but it is not installable
>  rocm-gdb : Depends: libtinfo5 but it is not installable
>             Depends: libncurses5 but it is not installable
>             Depends: libpython3.10 but it is not installable or
>                      libpython3.8 but it is not installable
> E: Unable to correct problems, you have held broken packages.
> ```

This is a different (packaging) problem and has nothing to do with the kernel. There is even an issue for that: #2524 


---

### 评论 #26 — supernovae (2024-05-20T14:07:52Z)

How does one get kernel 6.8 to work? I tried downloading a newer kernel, but it seems at 6.7 and higher they use a newer GLIBC than what 22.0.4 has so the headers complain when installing.

I wish 24.04. support could just come in a quick 6.1.2 release.

---

### 评论 #27 — pappacena (2024-05-20T14:28:37Z)

> I wish 24.04. support could just come in a quick 6.1.2 release.

+1 on giving higher priority to this. Ubuntu 24.04 was officially released like a month ago, and it is probably gaining a lot of popularity already.

---

### 评论 #28 — Novantric (2024-05-20T16:41:26Z)

Another +1, I downloaded 24.04 and tried to install the 23 version of the driver but it failed, so I purged it incorrectly and had to reinstall the whole OS LOL.
I hope it works with the latest stable kernel cause I'm on 6.9.1 rn for the AMD CPU enhancements.

---

### 评论 #29 — Mystro256 (2024-05-21T19:43:52Z)

> How does one get kernel 6.8 to work? I tried downloading a newer kernel, but it seems at 6.7 and higher they use a newer GLIBC than what 22.0.4 has so the headers complain when installing.
> 
> I wish 24.04. support could just come in a quick 6.1.2 release.

Ubuntu 24.04 support will be available in a future release, i.e. 6.2 or later (I'm not sure of the exact release personally), but it will not be back ported to 6.1.x.

---

### 评论 #30 — Wedge009 (2024-05-21T22:36:04Z)

> ...but it will not be back ported to 6.1.x.

So deprecated hardware support will likely be dropped, then? Looks like I'll be forced to stay on 22.04 then.

---

### 评论 #31 — foxsae (2024-05-22T02:59:26Z)

I can report that I just installed a fresh version of 24.04 which came out almost 2 months ago and this is still broken.
This is really frustraiting.


---

### 评论 #32 — Wedge009 (2024-05-22T03:16:48Z)

When Ubuntu 22.04 was released, OpenCL support was still being distributed via amdgpu-pro instead of through ROCm. I remember having to wait some time for official support of the then-new Ubuntu, but I can't recall how long that was.

It's really hard to find archived information (since things seem to get moved/deleted frequently), but according to AMD's [Previous Drivers](https://www.amd.com/en/support/downloads/previous-drivers.html/graphics/radeon-rx/radeon-rx-vega-series/amd-radeon-vii.html) page the oldest driver support for Ubuntu 22.04 was released on 2022-07-14 (the release notes link is broken, by the looks of it). That's quite some time - several months - after Ubuntu 22.04's release on [2022-04-21](https://lists.ubuntu.com/archives/ubuntu-announce/2022-April/000279.html).

---

### 评论 #33 — foxsae (2024-05-22T06:39:06Z)

I've moved back to 22.04 unfortunately trying to get this to work for 24.04 "LTS" ended up putting my system into an unrecoverable state and data and time was lost so I reinstalled 22.04 ...maybe LTS shouldn't be released when things aren't ready, for you know, every user who has a Radeon and needs acceleration, seems like that would be something important to include in a new LTS release.

---

### 评论 #34 — Wedge009 (2024-05-22T06:57:11Z)

AFAIK, the issue is with AMD support for Ubuntu 24.04 / kernel 6.8+, not the other way around.

---

### 评论 #35 — nairboon (2024-05-22T08:55:14Z)

> I can report that I just installed a fresh version of 24.04 which came out almost 2 months ago and this is still broken. This is really frustraiting.

It's not really broken, because it never worked in the first place and no one said that it even should work.
Ubuntu 24.04 is simply not yet supported, as is clearly stated in [the documentation](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html)

---

### 评论 #36 — samstride (2024-05-23T22:55:05Z)

Any chance we can get support for 7800xt added to rocm please?

---

### 评论 #37 — Le-onardo (2024-05-28T12:15:23Z)

Hi,

24.04 is not officially supported, but you should be able to install the packages (libcholmod3, libsuitesparseconfig5 [...]) from Ubuntu Jammy (22.04). If you have a clean system, this will not break anything as the packages are not referred in Ubuntu Noble (24.04) and were replaced by new versions with new names. This can be done by changing the /etc/apt/sources.list.d accordingly or by installing the .deb packages directly. I ran into the same issue and "fixed" it this way.

---

### 评论 #38 — rudiservo (2024-06-06T12:02:08Z)

Just installed ROCm v6.1.2 and amdgpu-dkms in Pop_OS 22.04 but with kernel 6.8, with no issues besides secureboot fail that is quite normal for pop_os.

Can anyone try on ubuntu 24.04?

---

### 评论 #39 — Wedge009 (2024-07-18T09:42:19Z)

I tried a fresh installation of Ubuntu 24.04 and ROCm 6.1.3 (using Jammy repository) seems to install okay, at least just for the OpenCL support that I use. I'm still inclined to wait until official support for Noble/24.04 before I upgrade my existing Ubuntu machines (only for those that still use supported GPUs, that is).

---

### 评论 #40 — Wedge009 (2024-07-18T09:49:36Z)

> Any chance we can get support for 7800xt added to rocm please?

I think such questions are better suited for other issues such as #2627.

---

### 评论 #41 — Wedge009 (2024-08-03T00:26:37Z)

[Documentation for just-released ROCm 6.2.0 lists official support for Ubuntu 24.04](https://rocm.docs.amd.com/en/docs-6.2.0/compatibility/compatibility-matrix.html#past-rocm-compatibility-matrix). I've yet to confirm this, though, especially since support for gfx906 is officially dropped.

---

### 评论 #42 — ckuethe (2024-08-03T01:30:38Z)

Following https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.2.0/install/quick-start.html

```
...
Need to get 2,319 MB of archives.
After this operation, 34.7 GB of additional disk space will be used.
```

Ok then.

After rebooting to pick up a new kernel, `rocm-smi` correctly reports my device and `JtR` happily runs OpenCL benchmarks.

Ubuntu 24.04 LTS (GNU/Linux 6.8.0-39-generic x86_64), "AMD Ryzen 7 2700X Eight-Core Processor"

---

### 评论 #43 — air-fuel-ratio (2024-08-03T03:33:06Z)

Is anybody using rocm 6.2 on KDE without issue? I just tried on Kubuntu and i get a black screen with a frozen mouse on Wayland and on X11 plasma is buggy with artefacts and menus opening and closing instantly.

Removing the DKMS module did not fix the issue, i had to remove all packages installed by rocm.

---

### 评论 #44 — Wedge009 (2024-08-03T04:51:55Z)

I'm still using ROCm 6.1.3 for the time being, with Kubuntu 24.04 - RX 7900 XTX and Radeon VII (separate machines).

Are you using the default Mesa packages? What video hardware?

---

### 评论 #45 — air-fuel-ratio (2024-08-03T04:54:43Z)

> I'm still using ROCm 6.1.3 for the time being, with Kubuntu 24.04 - RX 7900 XTX and Radeon VII (separate machines).
> 
> Are you using the default Mesa packages? What video hardware?

7900 XTX, everything is stock no PPA. 6.2 installed without issues.

---

### 评论 #46 — Wedge009 (2024-08-03T05:15:27Z)

I'll advise if I have anything similar, but I suggest a new issue to report this.

---

### 评论 #47 — air-fuel-ratio (2024-08-03T06:58:35Z)

Running amdgpu-install to reinstall fixed my issue, not sure what happened there. 

Can confirm Kubuntu 24.04 plasma on wayland working without issue.

---

### 评论 #48 — harkgill-amd (2024-08-07T13:51:54Z)

Hi @csdougliss, Ubuntu 24.04 support is now official with the release of ROCm 6.2.0. Could you please try installing with the steps in the [Quick start installation guide ](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) to see if you're issue is now resolved.

---

### 评论 #49 — harkgill-amd (2024-08-28T18:27:29Z)

Closing this ticket. If you do encounter any issues installing ROCm on Ubuntu 24.04, please open a new ticket, thanks!

---
