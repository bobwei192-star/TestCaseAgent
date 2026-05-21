# [Issue]: Unable to install amdgpu on Ubuntu 22 LTS

> **Issue #4164**
> **状态**: closed
> **创建时间**: 2024-12-16T12:50:04Z
> **更新时间**: 2024-12-28T00:15:45Z
> **关闭时间**: 2024-12-20T16:04:10Z
> **作者**: facorazza
> **标签**: Under Investigation, ROCm 6.3.0, Radeon 760M Graphics
> **URL**: https://github.com/ROCm/ROCm/issues/4164

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)
- **Radeon 760M Graphics** (颜色: #ededed)

## 描述

### Problem Description

This is the kernel version I'm running

```
uname -srmv
Linux 6.8.0-49-generic #49~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Nov  6 17:42:15 UTC 2 x86_64
```

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 5 7640U w/ Radeon 760M Graphics

### GPU

Radeon 760M Graphics

### ROCm Version

ROCm 6.3.0

### ROCm Component

_No response_

### Steps to Reproduce

Run the commands described [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)
```
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.3/ubuntu/jammy/amdgpu-install_6.3.60300-1_all.deb
sudo apt install ./amdgpu-install_6.3.60300-1_all.deb
sudo apt update
sudo apt install amdgpu-dkms rocm
```

```
Building for 6.8.0-49-generic
Building for architecture x86_64
Building initial module for 6.8.0-49-generic
ERROR: Cannot create report: [Errno 17] File exists: &apos;/var/crash/amdgpu-dkms.0.crash&apos;
Error! Bad return status for module build on kernel: 6.8.0-49-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.10.5-2084815.22.04/build/make.log for more information.
<b>dpkg:</b> error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status 10
Errors were encountered while processing:
 amdgpu-dkms
<font color="#BF616A"><b>E: </b></font>Sub-process /usr/bin/dpkg returned an error code (1)
```

And this is the content of `/var/crash/amdgpu-dkms.0.crash`

```
ProblemType: Package
DKMSBuildLog:
 DKMS make.log for amdgpu-6.10.5-2084815.22.04 for kernel 6.8.0-49-generic (x86_64)
 lun 16 dic 2024, 00:00:06, CET
 make: Entering directory '/usr/src/linux-headers-6.8.0-49-generic'
 warning: the compiler differs from the one used to build the kernel
   The kernel was built by: x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
   You are using:           gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
   CC [M]  /var/tmp/amd.MPVyukgA/scheduler/sched_main.o
   CC [M]  /var/tmp/amd.MPVyukgA/scheduler/sched_fence.o
   CC [M]  /var/tmp/amd.MPVyukgA/scheduler/sched_entity.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdxcp/amdgpu_xcp_drv.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdxcp/./backport/kcl_drm_drv.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_tt.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_bo.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_bo_util.o
   CC [M]  /var/tmp/amd.MPVyukgA/drm_gem_ttm_helper.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_bo_vm.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/main.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdgpu/amdgpu_drv.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_module.o
 /var/tmp/amd.MPVyukgA/amd/amdkcl/main.c:14:12: warning: no previous prototype for ‘amdkcl_init’ [-Wmissing-prototypes]
    14 | int __init amdkcl_init(void)
       |            ^~~~~~~~~~~
 /var/tmp/amd.MPVyukgA/amd/amdkcl/main.c:29:13: warning: no previous prototype for ‘amdkcl_exit’ [-Wmissing-prototypes]
    29 | void __exit amdkcl_exit(void)
       |             ^~~~~~~~~~~
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_common.o
   LD [M]  /var/tmp/amd.MPVyukgA/amd/amdxcp/amdxcp.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_kernel_params.o
 In file included from /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_helper.h:34,
                  from /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_helper_backport.h:5,
                  from /var/tmp/amd.MPVyukgA/amd/backport/backport.h:56,
                  from <command-line>:
 /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_cec.h: In function ‘_kcl_drm_dp_cec_register_connector’:
 /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_cec.h:67:53: error: passing argument 2 of ‘drm_dp_cec_register_connector’ from incompatible pointer type [-Werror=incompatible-pointer-types]
    67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
       |                                            ~~~~~~~~~^~~~~~
       |                                                     |
       |                                                     char *
 In file included from /var/tmp/amd.MPVyukgA/include/kcl/header/drm/display/drm_dp_helper.h:6,
                  from /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_helper.h:33:
 ./include/drm/display/drm_dp_helper.h:727:58: note: expected ‘struct drm_connector *’ but argument is of type ‘char *’
   727 |                                    struct drm_connector *connector);
       |                                    ~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~
 /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_cec.h:67:9: error: too many arguments to function ‘drm_dp_cec_register_connector’
    67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
       |         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ./include/drm/display/drm_dp_helper.h:726:6: note: declared here
   726 | void drm_dp_cec_register_connector(struct drm_dp_aux *aux,
       |      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_helper_backport.h: At top level:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_helper_backport.h:24:19: error: static declaration of ‘drm_dp_read_dpcd_caps’ follows non-static declaration
    24 | static inline int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
       |                   ^~~~~~~~~~~~~~~~~~~~~
 ./include/drm/display/drm_dp_helper.h:510:5: note: previous declaration of ‘drm_dp_read_dpcd_caps’ with type ‘int(struct drm_dp_aux *, u8 *)’ {aka ‘int(struct drm_dp_aux *, unsigned char *)’}
   510 | int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
       |     ^~~~~~~~~~~~~~~~~~~~~
 In file included from /var/tmp/amd.MPVyukgA/amd/backport/backport.h:57:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_atomic_find_vcpi_slots’:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:59:33: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
    59 |                 pbn_backup = mgr->pbn_div;
       |                                 ^~
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:60:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
    60 |                 mgr->pbn_div = pbn_div;
       |                    ^~
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:63:21: error: implicit declaration of function ‘drm_dp_atomic_find_vcpi_slots’; did you mean ‘drm_dp_atomic_find_time_slots’? [-Werror=implicit-function-declaration]
    63 |         req_slots = drm_dp_atomic_find_vcpi_slots(state, mgr, port, pbn);
       |                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       |                     drm_dp_atomic_find_time_slots
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:66:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
    66 |                 mgr->pbn_div = pbn_backup;
       |                    ^~
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_mst_topology_mgr_resume’:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:102:16: error: too few arguments to function ‘drm_dp_mst_topology_mgr_resume’
   102 |         return drm_dp_mst_topology_mgr_resume(mgr);
       |                ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 In file included from /var/tmp/amd.MPVyukgA/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                  from /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25:
 ./include/drm/display/drm_dp_mst_helper.h:870:1: note: declared here
   870 | drm_dp_mst_topology_mgr_resume(struct drm_dp_mst_topology_mgr *mgr,
       | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_execbuf_util.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdgpu/amdgpu_device.o
   CC [M]  /var/tmp/amd.MPVyukgA/drm_buddy.o
 cc1: some warnings being treated as errors
 make[3]: *** [scripts/Makefile.build:243: /var/tmp/amd.MPVyukgA/amd/amdgpu/amdgpu_drv.o] Error 1
 make[3]: *** Waiting for unfinished jobs....
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/dma-buf/dma-resv.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_dma-resv.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_backlight.o
   LD [M]  /var/tmp/amd.MPVyukgA/amddrm_ttm_helper.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_ioctl.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_range_manager.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_resource.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_kthread.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_io.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_seq_file.o
   LD [M]  /var/tmp/amd.MPVyukgA/scheduler/amd-sched.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_pool.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_suspend.o
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_suspend.c:32:6: warning: no previous prototype for ‘amdkcl_suspend_init’ [-Wmissing-prototypes]
    32 | void amdkcl_suspend_init(void)
       |      ^~~~~~~~~~~~~~~~~~~
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_io.c:69:6: warning: no previous prototype for ‘amdkcl_io_init’ [-Wmissing-prototypes]
    69 | void amdkcl_io_init(void)
       |      ^~~~~~~~~~~~~~
 In file included from /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_helper.h:34,
                  from /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_helper_backport.h:5,
                  from /var/tmp/amd.MPVyukgA/amd/backport/backport.h:56,
                  from <command-line>:
 /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_cec.h: In function ‘_kcl_drm_dp_cec_register_connector’:
 /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_cec.h:67:53: error: passing argument 2 of ‘drm_dp_cec_register_connector’ from incompatible pointer type [-Werror=incompatible-pointer-types]
    67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
       |                                            ~~~~~~~~~^~~~~~
       |                                                     |
       |                                                     char *
 In file included from /var/tmp/amd.MPVyukgA/include/kcl/header/drm/display/drm_dp_helper.h:6,
                  from /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_helper.h:33:
 ./include/drm/display/drm_dp_helper.h:727:58: note: expected ‘struct drm_connector *’ but argument is of type ‘char *’
   727 |                                    struct drm_connector *connector);
       |                                    ~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~
 /var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_cec.h:67:9: error: too many arguments to function ‘drm_dp_cec_register_connector’
    67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
       |         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ./include/drm/display/drm_dp_helper.h:726:6: note: declared here
   726 | void drm_dp_cec_register_connector(struct drm_dp_aux *aux,
       |      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_helper_backport.h: At top level:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_helper_backport.h:24:19: error: static declaration of ‘drm_dp_read_dpcd_caps’ follows non-static declaration
    24 | static inline int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
       |                   ^~~~~~~~~~~~~~~~~~~~~
 ./include/drm/display/drm_dp_helper.h:510:5: note: previous declaration of ‘drm_dp_read_dpcd_caps’ with type ‘int(struct drm_dp_aux *, u8 *)’ {aka ‘int(struct drm_dp_aux *, unsigned char *)’}
   510 | int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
       |     ^~~~~~~~~~~~~~~~~~~~~
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_pci.o
 In file included from /var/tmp/amd.MPVyukgA/amd/backport/backport.h:57:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_atomic_find_vcpi_slots’:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:59:33: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
    59 |                 pbn_backup = mgr->pbn_div;
       |                                 ^~
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:60:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
    60 |                 mgr->pbn_div = pbn_div;
       |                    ^~
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_mm.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_memory.o
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:63:21: error: implicit declaration of function ‘drm_dp_atomic_find_vcpi_slots’; did you mean ‘drm_dp_atomic_find_time_slots’? [-Werror=implicit-function-declaration]
    63 |         req_slots = drm_dp_atomic_find_vcpi_slots(state, mgr, port, pbn);
       |                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       |                     drm_dp_atomic_find_time_slots
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:66:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
    66 |                 mgr->pbn_div = pbn_backup;
       |                    ^~
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_mst_topology_mgr_resume’:
 /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:102:16: error: too few arguments to function ‘drm_dp_mst_topology_mgr_resume’
   102 |         return drm_dp_mst_topology_mgr_resume(mgr);
       |                ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 In file included from /var/tmp/amd.MPVyukgA/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                  from /var/tmp/amd.MPVyukgA/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25:
 ./include/drm/display/drm_dp_mst_helper.h:870:1: note: declared here
   870 | drm_dp_mst_topology_mgr_resume(struct drm_dp_mst_topology_mgr *mgr,
       | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_fence.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_device.o
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_mm.c:58:6: warning: no previous prototype for ‘amdkcl_mm_init’ [-Wmissing-prototypes]
    58 | void amdkcl_mm_init(void)
       |      ^~~~~~~~~~~~~~
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_cache.o
 cc1: some warnings being treated as errors
 make[3]: *** [scripts/Makefile.build:243: /var/tmp/amd.MPVyukgA/amd/amdgpu/amdgpu_device.o] Error 1
 make[2]: *** [scripts/Makefile.build:481: /var/tmp/amd.MPVyukgA/amd/amdgpu] Error 2
 make[2]: *** Waiting for unfinished jobs....
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_fb.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_sys_manager.o
   CC [M]  /var/tmp/amd.MPVyukgA/ttm/ttm_agp_backend.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_print.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_edid.o
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_fence.c:239:6: warning: no previous prototype for ‘amdkcl_fence_init’ [-Wmissing-prototypes]
   239 | void amdkcl_fence_init(void)
       |      ^~~~~~~~~~~~~~~~~
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_crtc.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_connector.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_atomic_helper.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_device_cgroup.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_mn.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_modes.o
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_fb.c: In function ‘drm_fb_helper_fill_info’:
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_fb.c:45:9: error: implicit declaration of function ‘drm_fb_helper_fill_fix’; did you mean ‘drm_fb_helper_fill_info’? [-Werror=implicit-function-declaration]
    45 |         drm_fb_helper_fill_fix(info, fb->pitches[0], fb->format->depth);
       |         ^~~~~~~~~~~~~~~~~~~~~~
       |         drm_fb_helper_fill_info
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_fb.c:45:40: error: invalid use of undefined type ‘struct drm_framebuffer’
    45 |         drm_fb_helper_fill_fix(info, fb->pitches[0], fb->format->depth);
       |                                        ^~
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_fb.c:45:56: error: invalid use of undefined type ‘struct drm_framebuffer’
    45 |         drm_fb_helper_fill_fix(info, fb->pitches[0], fb->format->depth);
       |                                                        ^~
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_time.o
   CC [M]  /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_acpi_table.o
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_fb.c:46:9: error: implicit declaration of function ‘drm_fb_helper_fill_var’; did you mean ‘drm_fb_helper_fill_info’? [-Werror=implicit-function-declaration]
    46 |         drm_fb_helper_fill_var(info, fb_helper,
       |         ^~~~~~~~~~~~~~~~~~~~~~
       |         drm_fb_helper_fill_info
 cc1: some warnings being treated as errors
 make[3]: *** [scripts/Makefile.build:243: /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_drm_fb.o] Error 1
 make[3]: *** Waiting for unfinished jobs....
 /var/tmp/amd.MPVyukgA/amd/amdkcl/kcl_device_cgroup.c:29:6: warning: no previous prototype for ‘amdkcl_dev_cgroup_init’ [-Wmissing-prototypes]
    29 | void amdkcl_dev_cgroup_init(void)
       |      ^~~~~~~~~~~~~~~~~~~~~~
   LD [M]  /var/tmp/amd.MPVyukgA/ttm/amdttm.o
 make[2]: *** [scripts/Makefile.build:481: /var/tmp/amd.MPVyukgA/amd/amdkcl] Error 2
 make[1]: *** [/usr/src/linux-headers-6.8.0-49-generic/Makefile:1925: /var/tmp/amd.MPVyukgA] Error 2
 make: *** [Makefile:240: __sub-make] Error 2
 make: Leaving directory '/usr/src/linux-headers-6.8.0-49-generic'
DKMSKernelVersion: 6.8.0-49-generic
Date: Mon Dec 16 00:00:11 2024
DuplicateSignature: dkms:amdgpu-dkms:1:6.10.5.60300-2084815.22.04:/var/tmp/amd.MPVyukgA/include/kcl/kcl_drm_dp_cec.h:67:53: error: passing argument 2 of ‘drm_dp_cec_register_connector’ from incompatible pointer type [-Werror=incompatible-pointer-types]
Package: amdgpu-dkms 1:6.10.5.60300-2084815.22.04
PackageVersion: 1:6.10.5.60300-2084815.22.04
SourcePackage: amdgpu-dkms
Title: amdgpu-dkms 1:6.10.5.60300-2084815.22.04: amdgpu kernel module failed to build
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is NOT loaded, possibly no GPU devices

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — lucbruni-amd (2024-12-16T18:32:31Z)

Hi @facorazza, thank you for opening this issue. An internal ticket has been opened and this is now under investigation. Thanks!

---

### 评论 #2 — facorazza (2024-12-16T19:00:59Z)

> Hi @facorazza, thank you for opening this issue. An internal ticket has been opened and this is now under investigation. Thanks!

Thank you!

---

### 评论 #3 — lucbruni-amd (2024-12-16T21:41:38Z)

Hi @facorazza, thanks for your patience.

May I ask what Linux kernel headers you are using? I am not able to reproduce this with Ubuntu 22.04.5 LTS (Jammy Jellyfish) and 6.8.0-49-generic, however there may be a mismatch in headers between my system and yours. In my case, I purged other headers using `sudo apt purge linux-headers-<ver>*` before running **all** commands described [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) in order.

Additionally, I found a similar discussion post here https://github.com/ROCm/ROCm/discussions/2938, where a fresh re-installation was suggested. Would you mind trying that out as well and let me know? Thanks!

---

### 评论 #4 — facorazza (2024-12-17T17:00:09Z)

I had linux-headers-generic-hwe-22.04 installed.After removing it I rebooted and tried to install again but it failed. So I tried to purge amdgpu-dkms and rocm and re-ran the install script but I still get the same error

---

### 评论 #5 — lucbruni-amd (2024-12-18T16:50:21Z)

Hi @facorazza, thank you for trying, would you mind sharing your most recent `make.log` again? This will provide us with the best hints as to why the error is occurring. Thanks for your patience.

---

### 评论 #6 — facorazza (2024-12-18T17:07:31Z)

For completeness I tried to start clean:

```shell
➜  ~ sudo apt update                                             
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.3/ubuntu/jammy/amdgpu-install_6.3.60300-1_all.deb
sudo apt install ./amdgpu-install_6.3.60300-1_all.deb
sudo apt update
sudo apt install amdgpu-dkms rocm
Hit:1 http://it.archive.ubuntu.com/ubuntu jammy InRelease
Hit:2 http://security.ubuntu.com/ubuntu jammy-security InRelease                                                                                                                         
Hit:3 https://download.docker.com/linux/ubuntu jammy InRelease                                                                                                                           
Hit:4 http://it.archive.ubuntu.com/ubuntu jammy-updates InRelease                                                                                                                        
Hit:5 https://packages.wazuh.com/4.x/apt stable InRelease                                                                              
Hit:6 https://packages.microsoft.com/repos/code stable InRelease                                                 
Hit:7 http://it.archive.ubuntu.com/ubuntu jammy-backports InRelease                                              
Hit:8 https://baltocdn.com/helm/stable/debian all InRelease         
Hit:9 https://ppa.launchpadcontent.net/neovim-ppa/unstable/ubuntu jammy InRelease
Hit:10 https://ppa.launchpadcontent.net/superm1/ppd/ubuntu jammy InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
1 package can be upgraded. Run 'apt list --upgradable' to see it.
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
linux-headers-6.8.0-49-generic is already the newest version (6.8.0-49.49~22.04.1).
linux-modules-extra-6.8.0-49-generic is already the newest version (6.8.0-49.49~22.04.1).
0 upgraded, 0 newly installed, 0 to remove and 1 not upgraded.
--2024-12-18 18:09:05--  https://repo.radeon.com/amdgpu-install/6.3/ubuntu/jammy/amdgpu-install_6.3.60300-1_all.deb
Resolving repo.radeon.com (repo.radeon.com)... 173.222.107.209, 173.222.107.203, 2a02:26f0:8d00:34::217:54db, ...
Connecting to repo.radeon.com (repo.radeon.com)|173.222.107.209|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 17000 (17K) [application/octet-stream]
Saving to: ‘amdgpu-install_6.3.60300-1_all.deb.8’

amdgpu-install_6.3.60300-1_all.deb.8           100%[==================================================================================================>]  16,60K  --.-KB/s    in 0,001s  

2024-12-18 18:09:06 (16,0 MB/s) - ‘amdgpu-install_6.3.60300-1_all.deb.8’ saved [17000/17000]

Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'amdgpu-install' instead of './amdgpu-install_6.3.60300-1_all.deb'
The following NEW packages will be installed:
  amdgpu-install
0 upgraded, 1 newly installed, 0 to remove and 1 not upgraded.
Need to get 0 B/17,0 kB of archives.
After this operation, 74,8 kB of additional disk space will be used.
Get:1 /home/<user>/amdgpu-install_6.3.60300-1_all.deb amdgpu-install all 6.3.60300-2084815.22.04 [17,0 kB]
Selecting previously unselected package amdgpu-install.
(Reading database ... 470945 files and directories currently installed.)
Preparing to unpack .../amdgpu-install_6.3.60300-1_all.deb ...
Unpacking amdgpu-install (6.3.60300-2084815.22.04) ...
Setting up amdgpu-install (6.3.60300-2084815.22.04) ...
Scanning processes...                                                                                                                                                                     
Scanning candidates...                                                                                                                                                                    
Scanning processor microcode...                                                                                                                                                           
Scanning linux images...                                                                                                                                                                  

Running kernel seems to be up-to-date.

The processor microcode seems to be up-to-date.

Restarting services...
Service restarts being deferred:
 systemctl restart user@1000.service

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
N: Download is performed unsandboxed as root as file '/home/<user>/amdgpu-install_6.3.60300-1_all.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
Hit:1 http://it.archive.ubuntu.com/ubuntu jammy InRelease
Get:2 https://repo.radeon.com/amdgpu/6.3/ubuntu jammy InRelease [5.433 B]                                                                                                                
Hit:3 http://it.archive.ubuntu.com/ubuntu jammy-updates InRelease                                                                                                                        
Get:4 https://repo.radeon.com/rocm/apt/6.3 jammy InRelease [2.603 B]                                                                                                                     
Hit:5 http://it.archive.ubuntu.com/ubuntu jammy-backports InRelease                                                                                                                      
Hit:6 https://download.docker.com/linux/ubuntu jammy InRelease                                                                                                                           
Hit:7 https://packages.wazuh.com/4.x/apt stable InRelease                                                                                                                                
Hit:8 https://baltocdn.com/helm/stable/debian all InRelease                                                                                                                              
Hit:9 https://packages.microsoft.com/repos/code stable InRelease                                                                                            
Get:10 https://repo.radeon.com/amdgpu/6.3/ubuntu jammy/main amd64 Packages [14,1 kB]                                 
Get:11 https://repo.radeon.com/amdgpu/6.3/ubuntu jammy/main i386 Packages [12,2 kB]                     
Hit:12 https://ppa.launchpadcontent.net/neovim-ppa/unstable/ubuntu jammy InRelease
Hit:13 https://ppa.launchpadcontent.net/superm1/ppd/ubuntu jammy InRelease
Hit:14 http://security.ubuntu.com/ubuntu jammy-security InRelease
Get:15 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 Packages [75,2 kB]
Fetched 110 kB in 1s (94,7 kB/s)     
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
1 package can be upgraded. Run 'apt list --upgradable' to see it.
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  amd-smi-lib amdgpu-core amdgpu-dkms-firmware comgr composablekernel-dev dkms half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt
  hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev hiptensor
  hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev libamd2 libcamd2 libccolamd2 libcholmod3 libcolamd2 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev
  libdrm-amdgpu-radeon1 libdrm2-amdgpu libelf-dev libfile-copy-recursive-perl libmetis5 libsuitesparseconfig5 mesa-common-dev migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx
  mivisionx-dev openmp-extras-dev openmp-extras-runtime rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent
  rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip-libraries rocm-hip-runtime rocm-hip-runtime-dev rocm-hip-sdk rocm-language-runtime rocm-llvm rocm-ml-libraries rocm-ml-sdk
  rocm-opencl rocm-opencl-dev rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-smi-lib rocm-utils rocminfo rocprim-dev rocprofiler rocprofiler-dev rocprofiler-plugins
  rocprofiler-register rocprofiler-sdk rocprofiler-sdk-roctx rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp
  rpp-dev valgrind
Suggested packages:
  valgrind-dbg valgrind-mpi kcachegrind alleyoop valkyrie
The following NEW packages will be installed:
  amd-smi-lib amdgpu-core amdgpu-dkms amdgpu-dkms-firmware comgr composablekernel-dev dkms half hip-dev hip-doc hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev
  hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt hipsparselt-dev
  hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev libamd2 libcamd2 libccolamd2 libcholmod3 libcolamd2 libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev
  libdrm-amdgpu-radeon1 libdrm2-amdgpu libelf-dev libfile-copy-recursive-perl libmetis5 libsuitesparseconfig5 mesa-common-dev migraphx migraphx-dev miopen-hip miopen-hip-dev mivisionx
  mivisionx-dev openmp-extras-dev openmp-extras-runtime rccl rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm rocm-cmake rocm-core rocm-dbgapi
  rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip-libraries rocm-hip-runtime rocm-hip-runtime-dev rocm-hip-sdk rocm-language-runtime rocm-llvm
  rocm-ml-libraries rocm-ml-sdk rocm-opencl rocm-opencl-dev rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-smi-lib rocm-utils rocminfo rocprim-dev rocprofiler rocprofiler-dev
  rocprofiler-plugins rocprofiler-register rocprofiler-sdk rocprofiler-sdk-roctx rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev rocthrust-dev roctracer
  roctracer-dev rocwmma-dev rpp rpp-dev valgrind
0 upgraded, 111 newly installed, 0 to remove and 1 not upgraded.
Need to get 2.532 MB/2.817 MB of archives.
After this operation, 35,4 GB of additional disk space will be used.
Do you want to continue? [Y/n] 
Get:1 http://it.archive.ubuntu.com/ubuntu jammy-updates/main amd64 dkms all 2.8.7-2ubuntu2.2 [70,1 kB]
Get:2 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-core amd64 6.3.0.60300-39~22.04 [14,0 kB]
Get:3 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 amd-smi-lib amd64 24.7.1.60300-39~22.04 [1.369 kB]
Get:4 http://it.archive.ubuntu.com/ubuntu jammy/universe amd64 libfile-copy-recursive-perl all 0.45-1 [17,3 kB]
Get:5 http://it.archive.ubuntu.com/ubuntu jammy/main amd64 valgrind amd64 1:3.18.1-1ubuntu2 [14,1 MB]
Get:6 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 comgr amd64 2.8.0.60300-39~22.04 [54,4 MB]
Get:7 http://it.archive.ubuntu.com/ubuntu jammy/main amd64 libsuitesparseconfig5 amd64 1:5.10.1+dfsg-4build1 [10,4 kB]
Get:8 http://it.archive.ubuntu.com/ubuntu jammy/universe amd64 libamd2 amd64 1:5.10.1+dfsg-4build1 [21,6 kB]
Get:9 http://it.archive.ubuntu.com/ubuntu jammy/universe amd64 libcamd2 amd64 1:5.10.1+dfsg-4build1 [23,3 kB]
Get:10 http://it.archive.ubuntu.com/ubuntu jammy/universe amd64 libccolamd2 amd64 1:5.10.1+dfsg-4build1 [25,2 kB]
Get:11 http://it.archive.ubuntu.com/ubuntu jammy/main amd64 libcolamd2 amd64 1:5.10.1+dfsg-4build1 [18,0 kB]
Get:12 http://it.archive.ubuntu.com/ubuntu jammy/universe amd64 libmetis5 amd64 5.1.0.dfsg-7build2 [181 kB]
Get:13 http://it.archive.ubuntu.com/ubuntu jammy/universe amd64 libcholmod3 amd64 1:5.10.1+dfsg-4build1 [346 kB]
Get:14 http://it.archive.ubuntu.com/ubuntu jammy/main amd64 libelf-dev amd64 0.186-1build1 [64,4 kB]
Get:15 http://it.archive.ubuntu.com/ubuntu jammy-updates/main amd64 mesa-common-dev amd64 23.2.1-1ubuntu3.1~22.04.3 [2.208 kB]
Get:16 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 composablekernel-dev amd64 1.1.0.60300-39~22.04 [523 MB]
Get:17 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 half amd64 1.12.0.60300-39~22.04 [19,7 kB]                                                                                  
Get:18 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocprofiler-register amd64 0.4.0.60300-39~22.04 [223 kB]                                                                    
Get:19 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hsa-rocr amd64 1.14.0.60300-39~22.04 [1.336 kB]                                                                             
Get:20 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocminfo amd64 1.0.0.60300-39~22.04 [28,8 kB]                                                                               
Get:21 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hip-runtime-amd amd64 6.3.42131.60300-39~22.04 [13,6 MB]                                                                    
Get:22 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-llvm amd64 18.0.0.24455.60300-39~22.04 [326 MB]                                                                        
Get:23 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hsa-rocr-dev amd64 1.14.0.60300-39~22.04 [135 kB]                                                                           
Get:24 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hip-dev amd64 6.3.42131.60300-39~22.04 [316 kB]                                                                             
Get:25 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hip-doc amd64 6.3.42131.60300-39~22.04 [89,8 kB]                                                                            
Get:26 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipcc amd64 1.1.1.60300-39~22.04 [217 kB]                                                                                   
Get:27 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hip-samples amd64 6.3.42131.60300-39~22.04 [51,7 kB]                                                                        
Get:28 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipblaslt amd64 0.10.0.60300-39~22.04 [329 MB]                                                                              
Get:29 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocblas amd64 4.3.0.60300-39~22.04 [149 MB]                                                                                 
Get:30 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocsolver amd64 3.27.0.60300-39~22.04 [262 MB]                                                                              
Get:31 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipblas amd64 2.3.0.60300-39~22.04 [157 kB]                                                                                 
Get:32 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipblas-common-dev amd64 1.0.0.60300-39~22.04 [5.762 B]                                                                     
Get:33 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipblas-dev amd64 2.3.0.60300-39~22.04 [98,3 kB]                                                                            
Get:34 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipblaslt-dev amd64 0.10.0.60300-39~22.04 [27,0 kB]                                                                         
Get:35 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocprim-dev amd64 3.3.0.60300-39~22.04 [230 kB]                                                                             
Get:36 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipcub-dev amd64 3.3.0.60300-39~22.04 [74,5 kB]                                                                             
Get:37 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocfft amd64 1.0.31.60300-39~22.04 [120 MB]                                                                                 
Get:38 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipfft amd64 1.0.17.60300-39~22.04 [25,7 kB]                                                                                
Get:39 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipfft-dev amd64 1.0.17.60300-39~22.04 [11,2 kB]                                                                            
Get:40 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipfort-dev amd64 0.5.0.60300-39~22.04 [6.658 kB]                                                                           
Get:41 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipify-clang amd64 18.0.0.60300-39~22.04 [21,0 MB]                                                                          
Get:42 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hiprand amd64 2.11.0.60300-39~22.04 [5.002 B]                                                                               
Get:43 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hiprand-dev amd64 2.11.0.60300-39~22.04 [21,2 kB]                                                                           
Get:44 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipsolver amd64 2.3.0.60300-39~22.04 [54,5 kB]                                                                              
Get:45 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipsolver-dev amd64 2.3.0.60300-39~22.04 [18,9 kB]                                                                          
Get:46 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipsparse amd64 3.1.2.60300-39~22.04 [46,0 kB]                                                                              
Get:47 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipsparse-dev amd64 3.1.2.60300-39~22.04 [49,0 kB]                                                                          
Get:48 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipsparselt amd64 0.2.2.60300-39~22.04 [10,3 MB]                                                                            
Get:49 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hipsparselt-dev amd64 0.2.2.60300-39~22.04 [11,7 kB]                                                                        
Get:50 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hiptensor amd64 1.4.0.60300-39~22.04 [34,3 MB]                                                                              
Get:51 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hiptensor-dev amd64 1.4.0.60300-39~22.04 [13,2 kB]                                                                          
Get:52 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 hsa-amd-aqlprofile amd64 1.0.0.60300-39~22.04 [492 kB]                                                                      
Get:53 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocrand amd64 3.2.0.60300-39~22.04 [23,1 MB]                                                                                
Get:54 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 miopen-hip amd64 3.3.0.60300-39~22.04 [162 MB]                                                                              
Get:55 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 migraphx amd64 2.11.0.60300-39~22.04 [48,8 MB]                                                                              
Get:56 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 migraphx-dev amd64 2.11.0.60300-39~22.04 [172 kB]                                                                           
Get:57 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 miopen-hip-dev amd64 3.3.0.60300-39~22.04 [47,8 kB]                                                                         
Get:58 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 openmp-extras-runtime amd64 18.63.0.60300-39~22.04 [153 MB]                                                                 
Get:59 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-language-runtime amd64 6.3.0.60300-39~22.04 [836 B]                                                                    
Get:60 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-hip-runtime amd64 6.3.0.60300-39~22.04 [2.034 B]                                                                       
Get:61 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 mivisionx amd64 3.1.0.60300-39~22.04 [36,0 MB]                                                                              
Get:62 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-device-libs amd64 1.0.0.60300-39~22.04 [720 kB]                                                                        
Get:63 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-cmake amd64 0.14.0.60300-39~22.04 [24,7 kB]                                                                            
Get:64 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-hip-runtime-dev amd64 6.3.0.60300-39~22.04 [2.200 B]                                                                   
Get:65 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocblas-dev amd64 4.3.0.60300-39~22.04 [99,1 kB]                                                                            
Get:66 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 mivisionx-dev amd64 3.1.0.60300-39~22.04 [23,6 MB]                                                                          
Get:67 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 openmp-extras-dev amd64 18.63.0.60300-39~22.04 [51,0 MB]                                                                    
Get:68 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-smi-lib amd64 7.4.0.60300-39~22.04 [1.032 kB]                                                                          
Get:69 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rccl amd64 2.21.5.60300-39~22.04 [53,8 MB]                                                                                  
Get:70 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rccl-dev amd64 2.21.5.60300-39~22.04 [107 kB]                                                                               
Get:71 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocalution amd64 3.2.1.60300-39~22.04 [4.934 kB]                                                                            
Get:72 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocalution-dev amd64 3.2.1.60300-39~22.04 [43,0 kB]                                                                         
Get:73 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocfft-dev amd64 1.0.31.60300-39~22.04 [10,7 kB]                                                                            
Get:74 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-utils amd64 6.3.0.60300-39~22.04 [814 B]                                                                               
Get:75 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-dbgapi amd64 0.77.0.60300-39~22.04 [1.787 kB]                                                                          
Get:76 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-debug-agent amd64 2.0.3.60300-39~22.04 [56,6 kB]                                                                       
Get:77 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-gdb amd64 15.2.60300-39~22.04 [92,3 MB]                                                                                
Get:78 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocprofiler amd64 2.0.60300.60300-39~22.04 [929 kB]                                                                         
Get:79 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocprofiler-plugins amd64 2.0.60300.60300-39~22.04 [1.056 kB]                                                               
Get:80 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocprofiler-sdk-roctx amd64 0.5.0-39~22.04 [192 kB]                                                                         
Get:81 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocprofiler-sdk amd64 0.5.0-39~22.04 [3.646 kB]                                                                             
Get:82 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocprofiler-dev amd64 2.0.60300.60300-39~22.04 [23,9 kB]                                                                    
Get:83 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-developer-tools amd64 6.3.0.60300-39~22.04 [2.178 B]                                                                   
Get:84 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-openmp-sdk amd64 6.3.0.60300-39~22.04 [870 B]                                                                          
Get:85 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-opencl amd64 2.0.0.60300-39~22.04 [634 kB]                                                                             
Get:86 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-opencl-runtime amd64 6.3.0.60300-39~22.04 [2.004 B]                                                                    
Get:87 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-opencl-dev amd64 2.0.0.60300-39~22.04 [121 kB]                                                                         
Get:88 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-opencl-sdk amd64 6.3.0.60300-39~22.04 [824 B]                                                                          
Get:89 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-hip-libraries amd64 6.3.0.60300-39~22.04 [942 B]                                                                       
Get:90 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-ml-libraries amd64 6.3.0.60300-39~22.04 [846 B]                                                                        
Get:91 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocrand-dev amd64 3.2.0.60300-39~22.04 [543 kB]                                                                             
Get:92 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocsolver-dev amd64 3.27.0.60300-39~22.04 [52,0 kB]                                                                         
Get:93 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-hip-sdk amd64 6.3.0.60300-39~22.04 [2.194 B]                                                                           
Get:94 https://repo.radeon.com/rocm/apt/6.3 jammy/main amd64 rocm-ml-sdk amd64 6.3.0.60300-39~22.04 [826 B]                                                                              
Fetched 2.532 MB in 58s (43,7 MB/s)                                                                                                                                                      
Extracting templates from packages: 100%
Selecting previously unselected package dkms.
(Reading database ... 470963 files and directories currently installed.)
Preparing to unpack .../000-dkms_2.8.7-2ubuntu2.2_all.deb ...
Unpacking dkms (2.8.7-2ubuntu2.2) ...
Selecting previously unselected package rocm-core.
Preparing to unpack .../001-rocm-core_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-core (6.3.0.60300-39~22.04) ...
Selecting previously unselected package amd-smi-lib.
Preparing to unpack .../002-amd-smi-lib_24.7.1.60300-39~22.04_amd64.deb ...
Unpacking amd-smi-lib (24.7.1.60300-39~22.04) ...
Selecting previously unselected package amdgpu-core.
Preparing to unpack .../003-amdgpu-core_1%3a6.3.60300-2084815.22.04_all.deb ...
Unpacking amdgpu-core (1:6.3.60300-2084815.22.04) ...
Selecting previously unselected package amdgpu-dkms-firmware.
Preparing to unpack .../004-amdgpu-dkms-firmware_1%3a6.10.5.60300-2084815.22.04_all.deb ...
Unpacking amdgpu-dkms-firmware (1:6.10.5.60300-2084815.22.04) ...
Selecting previously unselected package amdgpu-dkms.
Preparing to unpack .../005-amdgpu-dkms_1%3a6.10.5.60300-2084815.22.04_all.deb ...
Unpacking amdgpu-dkms (1:6.10.5.60300-2084815.22.04) ...
Selecting previously unselected package comgr.
Preparing to unpack .../006-comgr_2.8.0.60300-39~22.04_amd64.deb ...
Unpacking comgr (2.8.0.60300-39~22.04) ...
Selecting previously unselected package composablekernel-dev.
Preparing to unpack .../007-composablekernel-dev_1.1.0.60300-39~22.04_amd64.deb ...
Unpacking composablekernel-dev (1.1.0.60300-39~22.04) ...
Selecting previously unselected package half.
Preparing to unpack .../008-half_1.12.0.60300-39~22.04_amd64.deb ...
Unpacking half (1.12.0.60300-39~22.04) ...
Selecting previously unselected package libfile-copy-recursive-perl.
Preparing to unpack .../009-libfile-copy-recursive-perl_0.45-1_all.deb ...
Unpacking libfile-copy-recursive-perl (0.45-1) ...
Selecting previously unselected package libdrm2-amdgpu:amd64.
Preparing to unpack .../010-libdrm2-amdgpu_1%3a2.4.123.60300-2084815.22.04_amd64.deb ...
Unpacking libdrm2-amdgpu:amd64 (1:2.4.123.60300-2084815.22.04) ...
Selecting previously unselected package libdrm-amdgpu-common.
Preparing to unpack .../011-libdrm-amdgpu-common_1.0.0.60300-2084815.22.04_all.deb ...
Unpacking libdrm-amdgpu-common (1.0.0.60300-2084815.22.04) ...
Selecting previously unselected package libdrm-amdgpu-amdgpu1:amd64.
Preparing to unpack .../012-libdrm-amdgpu-amdgpu1_1%3a2.4.123.60300-2084815.22.04_amd64.deb ...
Unpacking libdrm-amdgpu-amdgpu1:amd64 (1:2.4.123.60300-2084815.22.04) ...
Selecting previously unselected package rocprofiler-register.
Preparing to unpack .../013-rocprofiler-register_0.4.0.60300-39~22.04_amd64.deb ...
Unpacking rocprofiler-register (0.4.0.60300-39~22.04) ...
Selecting previously unselected package hsa-rocr.
Preparing to unpack .../014-hsa-rocr_1.14.0.60300-39~22.04_amd64.deb ...
Pre-install check for ROCr.
Unpacking hsa-rocr (1.14.0.60300-39~22.04) ...
Selecting previously unselected package rocminfo.
Preparing to unpack .../015-rocminfo_1.0.0.60300-39~22.04_amd64.deb ...
Unpacking rocminfo (1.0.0.60300-39~22.04) ...
Selecting previously unselected package hip-runtime-amd.
Preparing to unpack .../016-hip-runtime-amd_6.3.42131.60300-39~22.04_amd64.deb ...
Unpacking hip-runtime-amd (6.3.42131.60300-39~22.04) ...
Selecting previously unselected package rocm-llvm.
Preparing to unpack .../017-rocm-llvm_18.0.0.24455.60300-39~22.04_amd64.deb ...
Unpacking rocm-llvm (18.0.0.24455.60300-39~22.04) ...
Selecting previously unselected package libdrm-amdgpu-radeon1:amd64.
Preparing to unpack .../018-libdrm-amdgpu-radeon1_1%3a2.4.123.60300-2084815.22.04_amd64.deb ...
Unpacking libdrm-amdgpu-radeon1:amd64 (1:2.4.123.60300-2084815.22.04) ...
Selecting previously unselected package valgrind.
Preparing to unpack .../019-valgrind_1%3a3.18.1-1ubuntu2_amd64.deb ...
Unpacking valgrind (1:3.18.1-1ubuntu2) ...
Selecting previously unselected package libdrm-amdgpu-dev:amd64.
Preparing to unpack .../020-libdrm-amdgpu-dev_1%3a2.4.123.60300-2084815.22.04_amd64.deb ...
Unpacking libdrm-amdgpu-dev:amd64 (1:2.4.123.60300-2084815.22.04) ...
Selecting previously unselected package hsa-rocr-dev.
Preparing to unpack .../021-hsa-rocr-dev_1.14.0.60300-39~22.04_amd64.deb ...
Unpacking hsa-rocr-dev (1.14.0.60300-39~22.04) ...
Selecting previously unselected package hip-dev.
Preparing to unpack .../022-hip-dev_6.3.42131.60300-39~22.04_amd64.deb ...
Unpacking hip-dev (6.3.42131.60300-39~22.04) ...
Selecting previously unselected package hip-doc.
Preparing to unpack .../023-hip-doc_6.3.42131.60300-39~22.04_amd64.deb ...
Unpacking hip-doc (6.3.42131.60300-39~22.04) ...
Selecting previously unselected package hipcc.
Preparing to unpack .../024-hipcc_1.1.1.60300-39~22.04_amd64.deb ...
Unpacking hipcc (1.1.1.60300-39~22.04) ...
Selecting previously unselected package hip-samples.
Preparing to unpack .../025-hip-samples_6.3.42131.60300-39~22.04_amd64.deb ...
Unpacking hip-samples (6.3.42131.60300-39~22.04) ...
Selecting previously unselected package hipblaslt.
Preparing to unpack .../026-hipblaslt_0.10.0.60300-39~22.04_amd64.deb ...
Unpacking hipblaslt (0.10.0.60300-39~22.04) ...
Selecting previously unselected package rocblas.
Preparing to unpack .../027-rocblas_4.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocblas (4.3.0.60300-39~22.04) ...
Selecting previously unselected package rocsolver.
Preparing to unpack .../028-rocsolver_3.27.0.60300-39~22.04_amd64.deb ...
Unpacking rocsolver (3.27.0.60300-39~22.04) ...
Selecting previously unselected package hipblas.
Preparing to unpack .../029-hipblas_2.3.0.60300-39~22.04_amd64.deb ...
Unpacking hipblas (2.3.0.60300-39~22.04) ...
Selecting previously unselected package hipblas-common-dev.
Preparing to unpack .../030-hipblas-common-dev_1.0.0.60300-39~22.04_amd64.deb ...
Unpacking hipblas-common-dev (1.0.0.60300-39~22.04) ...
Selecting previously unselected package hipblas-dev.
Preparing to unpack .../031-hipblas-dev_2.3.0.60300-39~22.04_amd64.deb ...
Unpacking hipblas-dev (2.3.0.60300-39~22.04) ...
Selecting previously unselected package hipblaslt-dev.
Preparing to unpack .../032-hipblaslt-dev_0.10.0.60300-39~22.04_amd64.deb ...
Unpacking hipblaslt-dev (0.10.0.60300-39~22.04) ...
Selecting previously unselected package rocprim-dev.
Preparing to unpack .../033-rocprim-dev_3.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocprim-dev (3.3.0.60300-39~22.04) ...
Selecting previously unselected package hipcub-dev.
Preparing to unpack .../034-hipcub-dev_3.3.0.60300-39~22.04_amd64.deb ...
Unpacking hipcub-dev (3.3.0.60300-39~22.04) ...
Selecting previously unselected package rocfft.
Preparing to unpack .../035-rocfft_1.0.31.60300-39~22.04_amd64.deb ...
Unpacking rocfft (1.0.31.60300-39~22.04) ...
Selecting previously unselected package hipfft.
Preparing to unpack .../036-hipfft_1.0.17.60300-39~22.04_amd64.deb ...
Unpacking hipfft (1.0.17.60300-39~22.04) ...
Selecting previously unselected package hipfft-dev.
Preparing to unpack .../037-hipfft-dev_1.0.17.60300-39~22.04_amd64.deb ...
Unpacking hipfft-dev (1.0.17.60300-39~22.04) ...
Selecting previously unselected package hipfort-dev.
Preparing to unpack .../038-hipfort-dev_0.5.0.60300-39~22.04_amd64.deb ...
Unpacking hipfort-dev (0.5.0.60300-39~22.04) ...
Selecting previously unselected package hipify-clang.
Preparing to unpack .../039-hipify-clang_18.0.0.60300-39~22.04_amd64.deb ...
Unpacking hipify-clang (18.0.0.60300-39~22.04) ...
Selecting previously unselected package hiprand.
Preparing to unpack .../040-hiprand_2.11.0.60300-39~22.04_amd64.deb ...
Unpacking hiprand (2.11.0.60300-39~22.04) ...
Selecting previously unselected package hiprand-dev.
Preparing to unpack .../041-hiprand-dev_2.11.0.60300-39~22.04_amd64.deb ...
Unpacking hiprand-dev (2.11.0.60300-39~22.04) ...
Selecting previously unselected package hipsolver.
Preparing to unpack .../042-hipsolver_2.3.0.60300-39~22.04_amd64.deb ...
Unpacking hipsolver (2.3.0.60300-39~22.04) ...
Selecting previously unselected package hipsolver-dev.
Preparing to unpack .../043-hipsolver-dev_2.3.0.60300-39~22.04_amd64.deb ...
Unpacking hipsolver-dev (2.3.0.60300-39~22.04) ...
Selecting previously unselected package rocsparse.
Preparing to unpack .../044-rocsparse_3.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocsparse (3.3.0.60300-39~22.04) ...
Selecting previously unselected package hipsparse.
Preparing to unpack .../045-hipsparse_3.1.2.60300-39~22.04_amd64.deb ...
Unpacking hipsparse (3.1.2.60300-39~22.04) ...
Selecting previously unselected package hipsparse-dev.
Preparing to unpack .../046-hipsparse-dev_3.1.2.60300-39~22.04_amd64.deb ...
Unpacking hipsparse-dev (3.1.2.60300-39~22.04) ...
Selecting previously unselected package hipsparselt.
Preparing to unpack .../047-hipsparselt_0.2.2.60300-39~22.04_amd64.deb ...
Unpacking hipsparselt (0.2.2.60300-39~22.04) ...
Selecting previously unselected package hipsparselt-dev.
Preparing to unpack .../048-hipsparselt-dev_0.2.2.60300-39~22.04_amd64.deb ...
Unpacking hipsparselt-dev (0.2.2.60300-39~22.04) ...
Selecting previously unselected package hiptensor.
Preparing to unpack .../049-hiptensor_1.4.0.60300-39~22.04_amd64.deb ...
Unpacking hiptensor (1.4.0.60300-39~22.04) ...
Selecting previously unselected package hiptensor-dev.
Preparing to unpack .../050-hiptensor-dev_1.4.0.60300-39~22.04_amd64.deb ...
Unpacking hiptensor-dev (1.4.0.60300-39~22.04) ...
Selecting previously unselected package hsa-amd-aqlprofile.
Preparing to unpack .../051-hsa-amd-aqlprofile_1.0.0.60300-39~22.04_amd64.deb ...
Unpacking hsa-amd-aqlprofile (1.0.0.60300-39~22.04) ...
Selecting previously unselected package libsuitesparseconfig5:amd64.
Preparing to unpack .../052-libsuitesparseconfig5_1%3a5.10.1+dfsg-4build1_amd64.deb ...
Unpacking libsuitesparseconfig5:amd64 (1:5.10.1+dfsg-4build1) ...
Selecting previously unselected package libamd2:amd64.
Preparing to unpack .../053-libamd2_1%3a5.10.1+dfsg-4build1_amd64.deb ...
Unpacking libamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Selecting previously unselected package libcamd2:amd64.
Preparing to unpack .../054-libcamd2_1%3a5.10.1+dfsg-4build1_amd64.deb ...
Unpacking libcamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Selecting previously unselected package libccolamd2:amd64.
Preparing to unpack .../055-libccolamd2_1%3a5.10.1+dfsg-4build1_amd64.deb ...
Unpacking libccolamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Selecting previously unselected package libcolamd2:amd64.
Preparing to unpack .../056-libcolamd2_1%3a5.10.1+dfsg-4build1_amd64.deb ...
Unpacking libcolamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Selecting previously unselected package libmetis5:amd64.
Preparing to unpack .../057-libmetis5_5.1.0.dfsg-7build2_amd64.deb ...
Unpacking libmetis5:amd64 (5.1.0.dfsg-7build2) ...
Selecting previously unselected package libcholmod3:amd64.
Preparing to unpack .../058-libcholmod3_1%3a5.10.1+dfsg-4build1_amd64.deb ...
Unpacking libcholmod3:amd64 (1:5.10.1+dfsg-4build1) ...
Selecting previously unselected package libelf-dev:amd64.
Preparing to unpack .../059-libelf-dev_0.186-1build1_amd64.deb ...
Unpacking libelf-dev:amd64 (0.186-1build1) ...
Selecting previously unselected package mesa-common-dev:amd64.
Preparing to unpack .../060-mesa-common-dev_23.2.1-1ubuntu3.1~22.04.3_amd64.deb ...
Unpacking mesa-common-dev:amd64 (23.2.1-1ubuntu3.1~22.04.3) ...
Selecting previously unselected package roctracer.
Preparing to unpack .../061-roctracer_4.1.60300.60300-39~22.04_amd64.deb ...
Unpacking roctracer (4.1.60300.60300-39~22.04) ...
Selecting previously unselected package rocrand.
Preparing to unpack .../062-rocrand_3.2.0.60300-39~22.04_amd64.deb ...
Unpacking rocrand (3.2.0.60300-39~22.04) ...
Selecting previously unselected package miopen-hip.
Preparing to unpack .../063-miopen-hip_3.3.0.60300-39~22.04_amd64.deb ...
Unpacking miopen-hip (3.3.0.60300-39~22.04) ...
Selecting previously unselected package migraphx.
Preparing to unpack .../064-migraphx_2.11.0.60300-39~22.04_amd64.deb ...
Unpacking migraphx (2.11.0.60300-39~22.04) ...
Selecting previously unselected package migraphx-dev.
Preparing to unpack .../065-migraphx-dev_2.11.0.60300-39~22.04_amd64.deb ...
Unpacking migraphx-dev (2.11.0.60300-39~22.04) ...
Selecting previously unselected package miopen-hip-dev.
Preparing to unpack .../066-miopen-hip-dev_3.3.0.60300-39~22.04_amd64.deb ...
Unpacking miopen-hip-dev (3.3.0.60300-39~22.04) ...
Selecting previously unselected package openmp-extras-runtime.
Preparing to unpack .../067-openmp-extras-runtime_18.63.0.60300-39~22.04_amd64.deb ...
Unpacking openmp-extras-runtime (18.63.0.60300-39~22.04) ...
Selecting previously unselected package rocm-language-runtime.
Preparing to unpack .../068-rocm-language-runtime_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-language-runtime (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-hip-runtime.
Preparing to unpack .../069-rocm-hip-runtime_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-hip-runtime (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rpp.
Preparing to unpack .../070-rpp_1.9.1.60300-39~22.04_amd64.deb ...
Unpacking rpp (1.9.1.60300-39~22.04) ...
Selecting previously unselected package mivisionx.
Preparing to unpack .../071-mivisionx_3.1.0.60300-39~22.04_amd64.deb ...
Unpacking mivisionx (3.1.0.60300-39~22.04) ...
Selecting previously unselected package rocm-device-libs.
Preparing to unpack .../072-rocm-device-libs_1.0.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-device-libs (1.0.0.60300-39~22.04) ...
Selecting previously unselected package rocm-cmake.
Preparing to unpack .../073-rocm-cmake_0.14.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-cmake (0.14.0.60300-39~22.04) ...
Selecting previously unselected package rocm-hip-runtime-dev.
Preparing to unpack .../074-rocm-hip-runtime-dev_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-hip-runtime-dev (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rpp-dev.
Preparing to unpack .../075-rpp-dev_1.9.1.60300-39~22.04_amd64.deb ...
Unpacking rpp-dev (1.9.1.60300-39~22.04) ...
Selecting previously unselected package rocblas-dev.
Preparing to unpack .../076-rocblas-dev_4.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocblas-dev (4.3.0.60300-39~22.04) ...
Selecting previously unselected package mivisionx-dev.
Preparing to unpack .../077-mivisionx-dev_3.1.0.60300-39~22.04_amd64.deb ...
Unpacking mivisionx-dev (3.1.0.60300-39~22.04) ...
Selecting previously unselected package openmp-extras-dev.
Preparing to unpack .../078-openmp-extras-dev_18.63.0.60300-39~22.04_amd64.deb ...
Unpacking openmp-extras-dev (18.63.0.60300-39~22.04) ...
Selecting previously unselected package rocm-smi-lib.
Preparing to unpack .../079-rocm-smi-lib_7.4.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-smi-lib (7.4.0.60300-39~22.04) ...
Selecting previously unselected package rccl.
Preparing to unpack .../080-rccl_2.21.5.60300-39~22.04_amd64.deb ...
Unpacking rccl (2.21.5.60300-39~22.04) ...
Selecting previously unselected package rccl-dev.
Preparing to unpack .../081-rccl-dev_2.21.5.60300-39~22.04_amd64.deb ...
Unpacking rccl-dev (2.21.5.60300-39~22.04) ...
Selecting previously unselected package rocalution.
Preparing to unpack .../082-rocalution_3.2.1.60300-39~22.04_amd64.deb ...
Unpacking rocalution (3.2.1.60300-39~22.04) ...
Selecting previously unselected package rocalution-dev.
Preparing to unpack .../083-rocalution-dev_3.2.1.60300-39~22.04_amd64.deb ...
Unpacking rocalution-dev (3.2.1.60300-39~22.04) ...
Selecting previously unselected package rocfft-dev.
Preparing to unpack .../084-rocfft-dev_1.0.31.60300-39~22.04_amd64.deb ...
Unpacking rocfft-dev (1.0.31.60300-39~22.04) ...
Selecting previously unselected package rocm-utils.
Preparing to unpack .../085-rocm-utils_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-utils (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-dbgapi.
Preparing to unpack .../086-rocm-dbgapi_0.77.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-dbgapi (0.77.0.60300-39~22.04) ...
Selecting previously unselected package rocm-debug-agent.
Preparing to unpack .../087-rocm-debug-agent_2.0.3.60300-39~22.04_amd64.deb ...
Unpacking rocm-debug-agent (2.0.3.60300-39~22.04) ...
Selecting previously unselected package rocm-gdb.
Preparing to unpack .../088-rocm-gdb_15.2.60300-39~22.04_amd64.deb ...
Unpacking rocm-gdb (15.2.60300-39~22.04) ...
Selecting previously unselected package rocprofiler.
Preparing to unpack .../089-rocprofiler_2.0.60300.60300-39~22.04_amd64.deb ...
Unpacking rocprofiler (2.0.60300.60300-39~22.04) ...
Selecting previously unselected package rocprofiler-plugins.
Preparing to unpack .../090-rocprofiler-plugins_2.0.60300.60300-39~22.04_amd64.deb ...
Unpacking rocprofiler-plugins (2.0.60300.60300-39~22.04) ...
Selecting previously unselected package rocprofiler-sdk-roctx.
Preparing to unpack .../091-rocprofiler-sdk-roctx_0.5.0-39~22.04_amd64.deb ...
Unpacking rocprofiler-sdk-roctx (0.5.0-39~22.04) ...
Selecting previously unselected package rocprofiler-sdk.
Preparing to unpack .../092-rocprofiler-sdk_0.5.0-39~22.04_amd64.deb ...
Unpacking rocprofiler-sdk (0.5.0-39~22.04) ...
Selecting previously unselected package rocprofiler-dev.
Preparing to unpack .../093-rocprofiler-dev_2.0.60300.60300-39~22.04_amd64.deb ...
Unpacking rocprofiler-dev (2.0.60300.60300-39~22.04) ...
Selecting previously unselected package roctracer-dev.
Preparing to unpack .../094-roctracer-dev_4.1.60300.60300-39~22.04_amd64.deb ...
Unpacking roctracer-dev (4.1.60300.60300-39~22.04) ...
Selecting previously unselected package rocm-developer-tools.
Preparing to unpack .../095-rocm-developer-tools_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-developer-tools (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-openmp-sdk.
Preparing to unpack .../096-rocm-openmp-sdk_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-openmp-sdk (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-opencl.
Preparing to unpack .../097-rocm-opencl_2.0.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-opencl (2.0.0.60300-39~22.04) ...
Selecting previously unselected package rocm-opencl-runtime.
Preparing to unpack .../098-rocm-opencl-runtime_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-opencl-runtime (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-opencl-dev.
Preparing to unpack .../099-rocm-opencl-dev_2.0.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-opencl-dev (2.0.0.60300-39~22.04) ...
Selecting previously unselected package rocm-opencl-sdk.
Preparing to unpack .../100-rocm-opencl-sdk_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-opencl-sdk (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-hip-libraries.
Preparing to unpack .../101-rocm-hip-libraries_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-hip-libraries (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-ml-libraries.
Preparing to unpack .../102-rocm-ml-libraries_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-ml-libraries (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocrand-dev.
Preparing to unpack .../103-rocrand-dev_3.2.0.60300-39~22.04_amd64.deb ...
Unpacking rocrand-dev (3.2.0.60300-39~22.04) ...
Selecting previously unselected package rocsolver-dev.
Preparing to unpack .../104-rocsolver-dev_3.27.0.60300-39~22.04_amd64.deb ...
Unpacking rocsolver-dev (3.27.0.60300-39~22.04) ...
Selecting previously unselected package rocsparse-dev.
Preparing to unpack .../105-rocsparse-dev_3.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocsparse-dev (3.3.0.60300-39~22.04) ...
Selecting previously unselected package rocthrust-dev.
Preparing to unpack .../106-rocthrust-dev_3.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocthrust-dev (3.3.0.60300-39~22.04) ...
Selecting previously unselected package rocwmma-dev.
Preparing to unpack .../107-rocwmma-dev_1.6.0.60300-39~22.04_amd64.deb ...
Unpacking rocwmma-dev (1.6.0.60300-39~22.04) ...
Selecting previously unselected package rocm-hip-sdk.
Preparing to unpack .../108-rocm-hip-sdk_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-hip-sdk (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm-ml-sdk.
Preparing to unpack .../109-rocm-ml-sdk_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm-ml-sdk (6.3.0.60300-39~22.04) ...
Selecting previously unselected package rocm.
Preparing to unpack .../110-rocm_6.3.0.60300-39~22.04_amd64.deb ...
Unpacking rocm (6.3.0.60300-39~22.04) ...
Setting up libmetis5:amd64 (5.1.0.dfsg-7build2) ...
Setting up dkms (2.8.7-2ubuntu2.2) ...
Setting up rocm-core (6.3.0.60300-39~22.04) ...
update-alternatives: using /opt/rocm-6.3.0 to provide /opt/rocm (rocm) in auto mode
Setting up libfile-copy-recursive-perl (0.45-1) ...
Setting up rocm-device-libs (1.0.0.60300-39~22.04) ...
Setting up rocfft (1.0.31.60300-39~22.04) ...
Setting up libelf-dev:amd64 (0.186-1build1) ...
Setting up hipblas-common-dev (1.0.0.60300-39~22.04) ...
Setting up amdgpu-core (1:6.3.60300-2084815.22.04) ...
Setting up rocprofiler-register (0.4.0.60300-39~22.04) ...
Setting up amdgpu-dkms-firmware (1:6.10.5.60300-2084815.22.04) ...
Setting up rocwmma-dev (1.6.0.60300-39~22.04) ...
Setting up hipify-clang (18.0.0.60300-39~22.04) ...
Setting up libdrm-amdgpu-common (1.0.0.60300-2084815.22.04) ...
Setting up mesa-common-dev:amd64 (23.2.1-1ubuntu3.1~22.04.3) ...
Setting up rocm-smi-lib (7.4.0.60300-39~22.04) ...
Removed /etc/systemd/system/timers.target.wants/logrotate.timer.
Created symlink /etc/systemd/system/timers.target.wants/logrotate.timer → /lib/systemd/system/logrotate.timer.
Setting up valgrind (1:3.18.1-1ubuntu2) ...
Setting up libsuitesparseconfig5:amd64 (1:5.10.1+dfsg-4build1) ...
Setting up rocrand (3.2.0.60300-39~22.04) ...
Setting up rocm-llvm (18.0.0.24455.60300-39~22.04) ...
Setting up comgr (2.8.0.60300-39~22.04) ...
Setting up libamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Setting up hiprand (2.11.0.60300-39~22.04) ...
Setting up roctracer (4.1.60300.60300-39~22.04) ...
Setting up libcolamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Setting up rocrand-dev (3.2.0.60300-39~22.04) ...
Setting up composablekernel-dev (1.1.0.60300-39~22.04) ...
Setting up amd-smi-lib (24.7.1.60300-39~22.04) ...
Using pyproject.toml for installation due to setuptools version 59.6.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead
: https://pip.pypa.io/warnings/venv
Installing bash completion script /etc/bash_completion.d/python-argcomplete.sh
Removed /etc/systemd/system/timers.target.wants/logrotate.timer.
Created symlink /etc/systemd/system/timers.target.wants/logrotate.timer → /lib/systemd/system/logrotate.timer.
Setting up rocm-cmake (0.14.0.60300-39~22.04) ...
Setting up rocprofiler-sdk-roctx (0.5.0-39~22.04) ...
Setting up hsa-amd-aqlprofile (1.0.0.60300-39~22.04) ...
Setting up hipfft (1.0.17.60300-39~22.04) ...
Setting up hipfft-dev (1.0.17.60300-39~22.04) ...
Setting up hiptensor (1.4.0.60300-39~22.04) ...
Setting up half (1.12.0.60300-39~22.04) ...
Setting up hipblaslt (0.10.0.60300-39~22.04) ...
Setting up amdgpu-dkms (1:6.10.5.60300-2084815.22.04) ...
Loading new amdgpu-6.10.5-2084815.22.04 DKMS files...
Building for 6.8.0-49-generic
Building for architecture x86_64
Building initial module for 6.8.0-49-generic
Error! Bad return status for module build on kernel: 6.8.0-49-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.10.5-2084815.22.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status 10
Setting up hsa-rocr (1.14.0.60300-39~22.04) ...
Setting up libcamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Setting up hiptensor-dev (1.4.0.60300-39~22.04) ...
Setting up libdrm2-amdgpu:amd64 (1:2.4.123.60300-2084815.22.04) ...
Setting up rocm-dbgapi (0.77.0.60300-39~22.04) ...
Setting up rocfft-dev (1.0.31.60300-39~22.04) ...
Setting up hiprand-dev (2.11.0.60300-39~22.04) ...
Setting up rocm-opencl (2.0.0.60300-39~22.04) ...
Setting up rocprofiler-sdk (0.5.0-39~22.04) ...
Setting up libccolamd2:amd64 (1:5.10.1+dfsg-4build1) ...
Setting up hipblaslt-dev (0.10.0.60300-39~22.04) ...
Setting up libcholmod3:amd64 (1:5.10.1+dfsg-4build1) ...
Setting up libdrm-amdgpu-radeon1:amd64 (1:2.4.123.60300-2084815.22.04) ...
Setting up libdrm-amdgpu-amdgpu1:amd64 (1:2.4.123.60300-2084815.22.04) ...
Setting up rocminfo (1.0.0.60300-39~22.04) ...
Setting up hip-runtime-amd (6.3.42131.60300-39~22.04) ...
Setting up hsa-rocr-dev (1.14.0.60300-39~22.04) ...
Setting up openmp-extras-runtime (18.63.0.60300-39~22.04) ...
Setting up rocm-utils (6.3.0.60300-39~22.04) ...
Setting up rocprim-dev (3.3.0.60300-39~22.04) ...
Setting up rocm-gdb (15.2.60300-39~22.04) ...
Setting up rocm-debug-agent (2.0.3.60300-39~22.04) ...
Setting up libdrm-amdgpu-dev:amd64 (1:2.4.123.60300-2084815.22.04) ...
Setting up hipcub-dev (3.3.0.60300-39~22.04) ...
Setting up hipfort-dev (0.5.0.60300-39~22.04) ...
Setting up rocblas (4.3.0.60300-39~22.04) ...
Setting up rccl (2.21.5.60300-39~22.04) ...
Setting up hip-dev (6.3.42131.60300-39~22.04) ...
Setting up rocprofiler (2.0.60300.60300-39~22.04) ...
Setting up rocsparse (3.3.0.60300-39~22.04) ...
Setting up miopen-hip (3.3.0.60300-39~22.04) ...
Setting up rocm-opencl-dev (2.0.0.60300-39~22.04) ...
Setting up rocprofiler-dev (2.0.60300.60300-39~22.04) ...
Setting up rocthrust-dev (3.3.0.60300-39~22.04) ...
Setting up roctracer-dev (4.1.60300.60300-39~22.04) ...
Setting up openmp-extras-dev (18.63.0.60300-39~22.04) ...
Setting up rocm-language-runtime (6.3.0.60300-39~22.04) ...
Setting up migraphx (2.11.0.60300-39~22.04) ...
Setting up hipsparse (3.1.2.60300-39~22.04) ...
Setting up rocprofiler-plugins (2.0.60300.60300-39~22.04) ...
Setting up rocsolver (3.27.0.60300-39~22.04) ...
Setting up miopen-hip-dev (3.3.0.60300-39~22.04) ...
Setting up hipblas (2.3.0.60300-39~22.04) ...
Setting up rocm-hip-runtime (6.3.0.60300-39~22.04) ...
update-alternatives: using /opt/rocm-6.3.0/bin/rocm_agent_enumerator to provide /usr/bin/rocm_agent_enumerator (rocm_agent_enumerator) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/rocminfo to provide /usr/bin/rocminfo (rocminfo) in auto mode
Setting up rocm-developer-tools (6.3.0.60300-39~22.04) ...
update-alternatives: using /opt/rocm-6.3.0/bin/amd-smi to provide /usr/bin/amd-smi (amd-smi) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/rocgdb to provide /usr/bin/rocgdb (rocgdb) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/rocm-smi to provide /usr/bin/rocm-smi (rocm-smi) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/rocprof to provide /usr/bin/rocprof (rocprof) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/rocsys to provide /usr/bin/rocsys (rocsys) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/rocprofv2 to provide /usr/bin/rocprofv2 (rocprofv2) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/roccoremerge to provide /usr/bin/roccoremerge (roccoremerge) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/rocprofv3 to provide /usr/bin/rocprofv3 (rocprofv3) in auto mode
Setting up rocm-openmp-sdk (6.3.0.60300-39~22.04) ...
Setting up rccl-dev (2.21.5.60300-39~22.04) ...
Setting up rocblas-dev (4.3.0.60300-39~22.04) ...
Setting up hipcc (1.1.1.60300-39~22.04) ...
Setting up rocsparse-dev (3.3.0.60300-39~22.04) ...
Setting up hip-doc (6.3.42131.60300-39~22.04) ...
Setting up hipsparse-dev (3.1.2.60300-39~22.04) ...
Setting up hipblas-dev (2.3.0.60300-39~22.04) ...
Setting up rocsolver-dev (3.27.0.60300-39~22.04) ...
Setting up rocalution (3.2.1.60300-39~22.04) ...
Setting up migraphx-dev (2.11.0.60300-39~22.04) ...
Setting up hipsolver (2.3.0.60300-39~22.04) ...
Setting up rpp (1.9.1.60300-39~22.04) ...
Setting up hip-samples (6.3.42131.60300-39~22.04) ...
Setting up rocm-opencl-runtime (6.3.0.60300-39~22.04) ...
update-alternatives: using /opt/rocm-6.3.0/bin/clinfo to provide /usr/bin/clinfo (clinfo) in auto mode
Setting up hipsolver-dev (2.3.0.60300-39~22.04) ...
Setting up hipsparselt (0.2.2.60300-39~22.04) ...
Setting up rocm-hip-runtime-dev (6.3.0.60300-39~22.04) ...
update-alternatives: using /opt/rocm-6.3.0/bin/roc-obj to provide /usr/bin/roc-obj (roc-obj) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/roc-obj-extract to provide /usr/bin/roc-obj-extract (roc-obj-extract) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/roc-obj-ls to provide /usr/bin/roc-obj-ls (roc-obj-ls) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipcc to provide /usr/bin/hipcc (hipcc) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipcc.pl to provide /usr/bin/hipcc.pl (hipcc.pl) in auto mode
/opt/rocm-6.3.0/bin/hipcc.bin not found, but that is OK
update-alternatives: using /opt/rocm-6.3.0/bin/hipcc_cmake_linker_helper to provide /usr/bin/hipcc_cmake_linker_helper (hipcc_cmake_linker_helper) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipconfig to provide /usr/bin/hipconfig (hipconfig) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipconfig.pl to provide /usr/bin/hipconfig.pl (hipconfig.pl) in auto mode
/opt/rocm-6.3.0/bin/hipconfig.bin not found, but that is OK
update-alternatives: using /opt/rocm-6.3.0/bin/hipconvertinplace-perl.sh to provide /usr/bin/hipconvertinplace-perl.sh (hipconvertinplace-perl.sh) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipconvertinplace.sh to provide /usr/bin/hipconvertinplace.sh (hipconvertinplace.sh) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipdemangleatp to provide /usr/bin/hipdemangleatp (hipdemangleatp) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipexamine-perl.sh to provide /usr/bin/hipexamine-perl.sh (hipexamine-perl.sh) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipexamine.sh to provide /usr/bin/hipexamine.sh (hipexamine.sh) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipify-perl to provide /usr/bin/hipify-perl (hipify-perl) in auto mode
update-alternatives: using /opt/rocm-6.3.0/bin/hipify-clang to provide /usr/bin/hipify-clang (hipify-clang) in auto mode
Setting up rocm-hip-libraries (6.3.0.60300-39~22.04) ...
Setting up mivisionx (3.1.0.60300-39~22.04) ...
Setting up rocm-opencl-sdk (6.3.0.60300-39~22.04) ...
Setting up rocalution-dev (3.2.1.60300-39~22.04) ...
Setting up rpp-dev (1.9.1.60300-39~22.04) ...
Setting up hipsparselt-dev (0.2.2.60300-39~22.04) ...
Setting up rocm-ml-libraries (6.3.0.60300-39~22.04) ...
Setting up rocm-hip-sdk (6.3.0.60300-39~22.04) ...
update-alternatives: using /opt/rocm-6.3.0/bin/hipfc to provide /usr/bin/hipfc (hipfc) in auto mode
Setting up mivisionx-dev (3.1.0.60300-39~22.04) ...
Setting up rocm-ml-sdk (6.3.0.60300-39~22.04) ...
Setting up rocm (6.3.0.60300-39~22.04) ...
update-alternatives: using /opt/rocm-6.3.0/bin/runvx to provide /usr/bin/runvx (runvx) in auto mode
Processing triggers for man-db (2.10.2-1) ...
Processing triggers for libc-bin (2.35-0ubuntu3.8) ...
Errors were encountered while processing:
 amdgpu-dkms
needrestart is being skipped since dpkg has failed
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

`/var/lib/dkms/amdgpu/6.10.5-2084815.22.04/build/make.log`

```c
DKMS make.log for amdgpu-6.10.5-2084815.22.04 for kernel 6.8.0-49-generic (x86_64)
mer 18 dic 2024, 18:13:52, CET
make: Entering directory '/usr/src/linux-headers-6.8.0-49-generic'
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  You are using:           gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  CC [M]  /var/tmp/amd.Nu14KVgH/scheduler/sched_main.o
  CC [M]  /var/tmp/amd.Nu14KVgH/scheduler/sched_fence.o
  CC [M]  /var/tmp/amd.Nu14KVgH/scheduler/sched_entity.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdxcp/./backport/kcl_drm_drv.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_tt.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_bo.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/main.o
  CC [M]  /var/tmp/amd.Nu14KVgH/drm_gem_ttm_helper.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_bo_util.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_common.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdgpu/amdgpu_drv.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/main.c:14:12: warning: no previous prototype for ‘amdkcl_init’ [-Wmissing-prototypes]
   14 | int __init amdkcl_init(void)
      |            ^~~~~~~~~~~
/var/tmp/amd.Nu14KVgH/amd/amdkcl/main.c:29:13: warning: no previous prototype for ‘amdkcl_exit’ [-Wmissing-prototypes]
   29 | void __exit amdkcl_exit(void)
      |             ^~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_kernel_params.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_bo_vm.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdgpu/amdgpu_device.o
In file included from /var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_helper.h:34,
                 from /var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_helper_backport.h:5,
                 from /var/tmp/amd.Nu14KVgH/amd/backport/backport.h:56,
                 from <command-line>:
/var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_cec.h: In function ‘_kcl_drm_dp_cec_register_connector’:
/var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_cec.h:67:53: error: passing argument 2 of ‘drm_dp_cec_register_connector’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
      |                                            ~~~~~~~~~^~~~~~
      |                                                     |
      |                                                     char *
In file included from /var/tmp/amd.Nu14KVgH/include/kcl/header/drm/display/drm_dp_helper.h:6,
                 from /var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_helper.h:33:
./include/drm/display/drm_dp_helper.h:727:58: note: expected ‘struct drm_connector *’ but argument is of type ‘char *’
  727 |                                    struct drm_connector *connector);
      |                                    ~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~
/var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_cec.h:67:9: error: too many arguments to function ‘drm_dp_cec_register_connector’
   67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
      |         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./include/drm/display/drm_dp_helper.h:726:6: note: declared here
  726 | void drm_dp_cec_register_connector(struct drm_dp_aux *aux,
      |      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_helper_backport.h: At top level:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_helper_backport.h:24:19: error: static declaration of ‘drm_dp_read_dpcd_caps’ follows non-static declaration
   24 | static inline int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
      |                   ^~~~~~~~~~~~~~~~~~~~~
./include/drm/display/drm_dp_helper.h:510:5: note: previous declaration of ‘drm_dp_read_dpcd_caps’ with type ‘int(struct drm_dp_aux *, u8 *)’ {aka ‘int(struct drm_dp_aux *, unsigned char *)’}
  510 | int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
      |     ^~~~~~~~~~~~~~~~~~~~~
In file included from /var/tmp/amd.Nu14KVgH/amd/backport/backport.h:57:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_atomic_find_vcpi_slots’:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:59:33: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
   59 |                 pbn_backup = mgr->pbn_div;
      |                                 ^~
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:60:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
   60 |                 mgr->pbn_div = pbn_div;
      |                    ^~
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:63:21: error: implicit declaration of function ‘drm_dp_atomic_find_vcpi_slots’; did you mean ‘drm_dp_atomic_find_time_slots’? [-Werror=implicit-function-declaration]
   63 |         req_slots = drm_dp_atomic_find_vcpi_slots(state, mgr, port, pbn);
      |                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      |                     drm_dp_atomic_find_time_slots
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:66:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
   66 |                 mgr->pbn_div = pbn_backup;
      |                    ^~
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_mst_topology_mgr_resume’:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:102:16: error: too few arguments to function ‘drm_dp_mst_topology_mgr_resume’
  102 |         return drm_dp_mst_topology_mgr_resume(mgr);
      |                ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In file included from /var/tmp/amd.Nu14KVgH/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                 from /var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25:
./include/drm/display/drm_dp_mst_helper.h:870:1: note: declared here
  870 | drm_dp_mst_topology_mgr_resume(struct drm_dp_mst_topology_mgr *mgr,
      | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/dma-buf/dma-resv.o
  LD [M]  /var/tmp/amd.Nu14KVgH/amd/amdxcp/amdxcp.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_dma-resv.o
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243: /var/tmp/amd.Nu14KVgH/amd/amdgpu/amdgpu_drv.o] Error 1
make[3]: *** Waiting for unfinished jobs....
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_module.o
  CC [M]  /var/tmp/amd.Nu14KVgH/drm_buddy.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_backlight.o
In file included from /var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_helper.h:34,
                 from /var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_helper_backport.h:5,
                 from /var/tmp/amd.Nu14KVgH/amd/backport/backport.h:56,
                 from <command-line>:
/var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_cec.h: In function ‘_kcl_drm_dp_cec_register_connector’:
/var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_cec.h:67:53: error: passing argument 2 of ‘drm_dp_cec_register_connector’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
      |                                            ~~~~~~~~~^~~~~~
      |                                                     |
      |                                                     char *
In file included from /var/tmp/amd.Nu14KVgH/include/kcl/header/drm/display/drm_dp_helper.h:6,
                 from /var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_helper.h:33:
./include/drm/display/drm_dp_helper.h:727:58: note: expected ‘struct drm_connector *’ but argument is of type ‘char *’
  727 |                                    struct drm_connector *connector);
      |                                    ~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~
/var/tmp/amd.Nu14KVgH/include/kcl/kcl_drm_dp_cec.h:67:9: error: too many arguments to function ‘drm_dp_cec_register_connector’
   67 |         drm_dp_cec_register_connector(aux, connector->name, connector->dev->dev);
      |         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./include/drm/display/drm_dp_helper.h:726:6: note: declared here
  726 | void drm_dp_cec_register_connector(struct drm_dp_aux *aux,
      |      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_helper_backport.h: At top level:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_helper_backport.h:24:19: error: static declaration of ‘drm_dp_read_dpcd_caps’ follows non-static declaration
   24 | static inline int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
      |                   ^~~~~~~~~~~~~~~~~~~~~
./include/drm/display/drm_dp_helper.h:510:5: note: previous declaration of ‘drm_dp_read_dpcd_caps’ with type ‘int(struct drm_dp_aux *, u8 *)’ {aka ‘int(struct drm_dp_aux *, unsigned char *)’}
  510 | int drm_dp_read_dpcd_caps(struct drm_dp_aux *aux,
      |     ^~~~~~~~~~~~~~~~~~~~~
In file included from /var/tmp/amd.Nu14KVgH/amd/backport/backport.h:57:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_atomic_find_vcpi_slots’:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:59:33: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
   59 |                 pbn_backup = mgr->pbn_div;
      |                                 ^~
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:60:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
   60 |                 mgr->pbn_div = pbn_div;
      |                    ^~
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_execbuf_util.o
  LD [M]  /var/tmp/amd.Nu14KVgH/amddrm_ttm_helper.o
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:63:21: error: implicit declaration of function ‘drm_dp_atomic_find_vcpi_slots’; did you mean ‘drm_dp_atomic_find_time_slots’? [-Werror=implicit-function-declaration]
   63 |         req_slots = drm_dp_atomic_find_vcpi_slots(state, mgr, port, pbn);
      |                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      |                     drm_dp_atomic_find_time_slots
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:66:20: error: ‘struct drm_dp_mst_topology_mgr’ has no member named ‘pbn_div’
   66 |                 mgr->pbn_div = pbn_backup;
      |                    ^~
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h: In function ‘_kcl_drm_dp_mst_topology_mgr_resume’:
/var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:102:16: error: too few arguments to function ‘drm_dp_mst_topology_mgr_resume’
  102 |         return drm_dp_mst_topology_mgr_resume(mgr);
      |                ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In file included from /var/tmp/amd.Nu14KVgH/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                 from /var/tmp/amd.Nu14KVgH/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25:
./include/drm/display/drm_dp_mst_helper.h:870:1: note: declared here
  870 | drm_dp_mst_topology_mgr_resume(struct drm_dp_mst_topology_mgr *mgr,
      | ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_range_manager.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_ioctl.o
  LD [M]  /var/tmp/amd.Nu14KVgH/scheduler/amd-sched.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_resource.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_kthread.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_io.o
cc1: some warnings being treated as errors
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_pool.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_seq_file.o
make[3]: *** [scripts/Makefile.build:243: /var/tmp/amd.Nu14KVgH/amd/amdgpu/amdgpu_device.o] Error 1
make[2]: *** [scripts/Makefile.build:481: /var/tmp/amd.Nu14KVgH/amd/amdgpu] Error 2
make[2]: *** Waiting for unfinished jobs....
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_suspend.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_pci.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_suspend.c:32:6: warning: no previous prototype for ‘amdkcl_suspend_init’ [-Wmissing-prototypes]
   32 | void amdkcl_suspend_init(void)
      |      ^~~~~~~~~~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_mm.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_device.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_sys_manager.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_io.c:69:6: warning: no previous prototype for ‘amdkcl_io_init’ [-Wmissing-prototypes]
   69 | void amdkcl_io_init(void)
      |      ^~~~~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_memory.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_fence.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_mm.c:58:6: warning: no previous prototype for ‘amdkcl_mm_init’ [-Wmissing-prototypes]
   58 | void amdkcl_mm_init(void)
      |      ^~~~~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_cache.o
  CC [M]  /var/tmp/amd.Nu14KVgH/ttm/ttm_agp_backend.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_fb.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_print.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_edid.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_crtc.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_fence.c:239:6: warning: no previous prototype for ‘amdkcl_fence_init’ [-Wmissing-prototypes]
  239 | void amdkcl_fence_init(void)
      |      ^~~~~~~~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_connector.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_atomic_helper.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_device_cgroup.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_mn.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_modes.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_time.o
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_acpi_table.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_device_cgroup.c:29:6: warning: no previous prototype for ‘amdkcl_dev_cgroup_init’ [-Wmissing-prototypes]
   29 | void amdkcl_dev_cgroup_init(void)
      |      ^~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_page_alloc.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_fb.c: In function ‘drm_fb_helper_fill_info’:
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_fb.c:45:9: error: implicit declaration of function ‘drm_fb_helper_fill_fix’; did you mean ‘drm_fb_helper_fill_info’? [-Werror=implicit-function-declaration]
   45 |         drm_fb_helper_fill_fix(info, fb->pitches[0], fb->format->depth);
      |         ^~~~~~~~~~~~~~~~~~~~~~
      |         drm_fb_helper_fill_info
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_fb.c:45:40: error: invalid use of undefined type ‘struct drm_framebuffer’
   45 |         drm_fb_helper_fill_fix(info, fb->pitches[0], fb->format->depth);
      |                                        ^~
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_fb.c:45:56: error: invalid use of undefined type ‘struct drm_framebuffer’
   45 |         drm_fb_helper_fill_fix(info, fb->pitches[0], fb->format->depth);
      |                                                        ^~
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_fb.c:46:9: error: implicit declaration of function ‘drm_fb_helper_fill_var’; did you mean ‘drm_fb_helper_fill_info’? [-Werror=implicit-function-declaration]
   46 |         drm_fb_helper_fill_var(info, fb_helper,
      |         ^~~~~~~~~~~~~~~~~~~~~~
      |         drm_fb_helper_fill_info
cc1: some warnings being treated as errors
  CC [M]  /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_numa.o
make[3]: *** [scripts/Makefile.build:243: /var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_drm_fb.o] Error 1
make[3]: *** Waiting for unfinished jobs....
  LD [M]  /var/tmp/amd.Nu14KVgH/ttm/amdttm.o
/var/tmp/amd.Nu14KVgH/amd/amdkcl/kcl_numa.c:15:6: warning: no previous prototype for ‘amdkcl_numa_init’ [-Wmissing-prototypes]
   15 | void amdkcl_numa_init(void)
      |      ^~~~~~~~~~~~~~~~
make[2]: *** [scripts/Makefile.build:481: /var/tmp/amd.Nu14KVgH/amd/amdkcl] Error 2
make[1]: *** [/usr/src/linux-headers-6.8.0-49-generic/Makefile:1925: /var/tmp/amd.Nu14KVgH] Error 2
make: *** [Makefile:240: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.8.0-49-generic'
```

Edit: run apt autoremove

---

### 评论 #7 — lucbruni-amd (2024-12-19T14:48:27Z)

Hi @facorazza, thanks for providing `make.log` and for your continued patience in the matter.

Could you kindly provide the full output of `dpkg -l`?

---

### 评论 #8 — facorazza (2024-12-19T17:40:54Z)

Sure thing. I had to upload a file because the output is longer than the maximum comment length allowed.

[dpkg.txt](https://github.com/user-attachments/files/18201448/dpkg.txt)


---

### 评论 #9 — facorazza (2024-12-20T16:04:10Z)

Today, after installing the latest update for linux-image-generic-hwe-22.04, linux-libc-dev, linux-tools-common I was able to successfully install amdgpu and rocm

---

### 评论 #10 — mvastola (2024-12-28T00:15:44Z)

@facorazza, FYI, I can't be sure if you had the exact same issue as me given how you ultimately were able to solve yours, but I'd been experiencing the same compile errors on 24.04 and was able to trace it down to a conflict with the `libpam-tmpdir` package (which I see you have installed as well, according to your `dpkg.txt` file).

I'm kind of curious now how updating those packages fixed things for you, but in any case thought I'd point this out should you ever upgrade and the issue returns. (See #4204 for details)



---
