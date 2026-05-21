# [Issue]: Ubuntu 24.04 install of Rocm 6.2.xxx fails

> **Issue #3762**
> **状态**: closed
> **创建时间**: 2024-09-19T23:13:39Z
> **更新时间**: 2024-09-20T17:39:39Z
> **关闭时间**: 2024-09-20T13:25:03Z
> **作者**: sarahkaylor
> **标签**: AMD Radeon Pro W7900, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3762

## 标签

- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

I followed the quick-install steps on a fresh install of Ubuntu 24.04 desktop. I have a Ryzen 3700x CPU and a Radeon Pro W7900. I followed these instructions: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html

It seems that the installation is failing when trying to compile the kernel module(s):

ProblemType: Package
DKMSBuildLog:
 DKMS make.log for amdgpu-6.8.5-2009582.24.04 for kernel 6.8.0-45-generic (x86_64)
 Thu Sep 19 05:54:57 PM CDT 2024
 make: Entering directory '/usr/src/linux-headers-6.8.0-45-generic'
 warning: the compiler differs from the one used to build the kernel
   The kernel was built by: x86_64-linux-gnu-gcc-13 (Ubuntu 13.2.0-23ubuntu4) 13.2.0
   You are using:           gcc-13 (Ubuntu 13.2.0-23ubuntu4) 13.2.0
   CC [M]  /tmp/amd.chrxdkMD/scheduler/sched_main.o
   CC [M]  /tmp/amd.chrxdkMD/scheduler/sched_fence.o
   CC [M]  /tmp/amd.chrxdkMD/scheduler/sched_entity.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdxcp/amdgpu_xcp_drv.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdxcp/./backport/kcl_drm_drv.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_tt.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_bo.o
   CC [M]  /tmp/amd.chrxdkMD/drm_gem_ttm_helper.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_bo_util.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_bo_vm.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_module.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/main.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_execbuf_util.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_range_manager.o
   CC [M]  /tmp/amd.chrxdkMD/drm_buddy.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_drv.o
 /tmp/amd.chrxdkMD/amd/amdkcl/main.c:17:12: warning: no previous prototype for ‘amdkcl_init’ [-Wmissing-prototypes]
    17 | int __init amdkcl_init(void)
       |            ^~~~~~~~~~~
 /tmp/amd.chrxdkMD/amd/amdkcl/main.c:35:13: warning: no previous prototype for ‘amdkcl_exit’ [-Wmissing-prototypes]
    35 | void __exit amdkcl_exit(void)
       |             ^~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_common.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_kernel_params.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_resource.o
   LD [M]  /tmp/amd.chrxdkMD/amd/amdxcp/amdxcp.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/dma-buf/dma-resv.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_device.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_common.c:30:6: warning: no previous prototype for ‘amdkcl_symbol_init’ [-Wmissing-prototypes]
    30 | void amdkcl_symbol_init(void)
       |      ^~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_pool.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_backlight.o
   LD [M]  /tmp/amd.chrxdkMD/amddrm_buddy.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_ioctl.o
   LD [M]  /tmp/amd.chrxdkMD/amddrm_ttm_helper.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_doorbell_mgr.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_device.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_kthread.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_sys_manager.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_kms.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_io.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_agp_backend.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_seq_file.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_atombios.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_suspend.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_suspend.c:32:6: warning: no previous prototype for ‘amdkcl_suspend_init’ [-Wmissing-prototypes]
    32 | void amdkcl_suspend_init(void)
       |      ^~~~~~~~~~~~~~~~~~~
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_io.c:69:6: warning: no previous prototype for ‘amdkcl_io_init’ [-Wmissing-prototypes]


### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

AMD Ryzen 7 3700x 8-Core Processor

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.2.0

### ROCm Component

ROCm

### Steps to Reproduce

1. Install Ubuntu 24.04 desktop onto a computer as the only operating system.
2. Follow the steps detailed on https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html
3. Observe error installing amdgpu-dkms.
4. Look at the file /var/crash/amdgpu-dkms.0.crash for details

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

This program cannot be run because the install failed:

### Additional Information

$uname -a
Linux radeonpro 6.8.0-45-generic #45-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 30 12:02:04 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

$cat /etc/lsb-release 
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04.1 LTS"

$ cat /proc/cpuinfo

vendor_id	: AuthenticAMD
cpu family	: 23
model		: 113
model name	: AMD Ryzen 7 3700X 8-Core Processor
stepping	: 0
microcode	: 0x8701021
cpu MHz		: 2124.398
cache size	: 512 KB
physical id	: 0
siblings	: 16
core id		: 7
cpu cores	: 8
apicid		: 15
initial apicid	: 15
fpu		: yes
fpu_exception	: yes
cpuid level	: 16
wp		: yes

---

## 评论 (5 条)

### 评论 #1 — sarahkaylor (2024-09-19T23:15:54Z)

Full contents of the crash log in /var:

ProblemType: Package
DKMSBuildLog:
 DKMS make.log for amdgpu-6.8.5-2009582.24.04 for kernel 6.8.0-45-generic (x86_64)
 Thu Sep 19 05:54:57 PM CDT 2024
 make: Entering directory '/usr/src/linux-headers-6.8.0-45-generic'
 warning: the compiler differs from the one used to build the kernel
   The kernel was built by: x86_64-linux-gnu-gcc-13 (Ubuntu 13.2.0-23ubuntu4) 13.2.0
   You are using:           gcc-13 (Ubuntu 13.2.0-23ubuntu4) 13.2.0
   CC [M]  /tmp/amd.chrxdkMD/scheduler/sched_main.o
   CC [M]  /tmp/amd.chrxdkMD/scheduler/sched_fence.o
   CC [M]  /tmp/amd.chrxdkMD/scheduler/sched_entity.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdxcp/amdgpu_xcp_drv.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdxcp/./backport/kcl_drm_drv.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_tt.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_bo.o
   CC [M]  /tmp/amd.chrxdkMD/drm_gem_ttm_helper.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_bo_util.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_bo_vm.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_module.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/main.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_execbuf_util.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_range_manager.o
   CC [M]  /tmp/amd.chrxdkMD/drm_buddy.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_drv.o
 /tmp/amd.chrxdkMD/amd/amdkcl/main.c:17:12: warning: no previous prototype for ‘amdkcl_init’ [-Wmissing-prototypes]
    17 | int __init amdkcl_init(void)
       |            ^~~~~~~~~~~
 /tmp/amd.chrxdkMD/amd/amdkcl/main.c:35:13: warning: no previous prototype for ‘amdkcl_exit’ [-Wmissing-prototypes]
    35 | void __exit amdkcl_exit(void)
       |             ^~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_common.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_kernel_params.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_resource.o
   LD [M]  /tmp/amd.chrxdkMD/amd/amdxcp/amdxcp.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/dma-buf/dma-resv.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_device.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_common.c:30:6: warning: no previous prototype for ‘amdkcl_symbol_init’ [-Wmissing-prototypes]
    30 | void amdkcl_symbol_init(void)
       |      ^~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_pool.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_backlight.o
   LD [M]  /tmp/amd.chrxdkMD/amddrm_buddy.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_ioctl.o
   LD [M]  /tmp/amd.chrxdkMD/amddrm_ttm_helper.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_doorbell_mgr.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_device.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_kthread.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_sys_manager.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_kms.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_io.o
   CC [M]  /tmp/amd.chrxdkMD/ttm/ttm_agp_backend.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_seq_file.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_atombios.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_suspend.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_suspend.c:32:6: warning: no previous prototype for ‘amdkcl_suspend_init’ [-Wmissing-prototypes]
    32 | void amdkcl_suspend_init(void)
       |      ^~~~~~~~~~~~~~~~~~~
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_io.c:69:6: warning: no previous prototype for ‘amdkcl_io_init’ [-Wmissing-prototypes]
    69 | void amdkcl_io_init(void)
       |      ^~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/atombios_crtc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_pci.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_mm.o
   LD [M]  /tmp/amd.chrxdkMD/scheduler/amd-sched.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_memory.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_connectors.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_sched.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_fence.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_sched.c:24:6: warning: no previous prototype for ‘amdkcl_sched_init’ [-Wmissing-prototypes]
    24 | void amdkcl_sched_init(void)
       |      ^~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/atom.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_reservation.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_cache.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_mm.c:58:6: warning: no previous prototype for ‘amdkcl_mm_init’ [-Wmissing-prototypes]
    58 | void amdkcl_mm_init(void)
       |      ^~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_fence.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ttm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_fb.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_reservation.c:37:6: warning: no previous prototype for ‘amdkcl_reservation_init’ [-Wmissing-prototypes]
    37 | void amdkcl_reservation_init(void)
       |      ^~~~~~~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_object.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_print.o
   LD [M]  /tmp/amd.chrxdkMD/ttm/amdttm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_gart.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_fence.c:239:6: warning: no previous prototype for ‘amdkcl_fence_init’ [-Wmissing-prototypes]
   239 | void amdkcl_fence_init(void)
       |      ^~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_crtc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_encoders.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_connector.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_atomic_helper.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_display.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_device_cgroup.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_mn.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_i2c.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_gem.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_modes.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_time.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_device_cgroup.c:29:6: warning: no previous prototype for ‘amdkcl_dev_cgroup_init’ [-Wmissing-prototypes]
    29 | void amdkcl_dev_cgroup_init(void)
       |      ^~~~~~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_acpi_table.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ring.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_cs.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_page_alloc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_numa.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_bios.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_fs_read_write.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_benchmark.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_aperture.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_simple_kms_helper.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_bitmap.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/atombios_dp.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_numa.c:15:6: warning: no previous prototype for ‘amdkcl_numa_init’ [-Wmissing-prototypes]
    15 | void amdkcl_numa_init(void)
       |      ^~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_afmt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_vmscan.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_dma_fence_chain.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_mce_amd.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_trace_points.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/atombios_encoders.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_vmscan.c:25:6: warning: no previous prototype for ‘synchronize_shrinkers’ [-Wmissing-prototypes]
    25 | void synchronize_shrinkers(void)
       |      ^~~~~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_workqueue.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_sa.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_cpumask.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_dsc_helper.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_mm_slab.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_workqueue.c:40:6: warning: no previous prototype for ‘amdkcl_workqueue_init’ [-Wmissing-prototypes]
    40 | void amdkcl_workqueue_init(void)
       |      ^~~~~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/atombios_i2c.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_irqdesc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_dma_buf.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_suballoc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_exec.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_dp_helper.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vm_pt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_prime.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vm_tlb_fence.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_hdcp.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ib.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_debugfs_inode.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_pll.o
 /tmp/amd.chrxdkMD/amd/amdkcl/kcl_drm_prime.c:22:6: warning: no previous prototype for ‘amdkcl_prime_init’ [-Wmissing-prototypes]
    22 | void amdkcl_prime_init(void)
       |      ^~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_debugfs_file.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ucode.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_sysfs_emit.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_bo_list.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdkcl/kcl_wbrf.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ctx.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_sync.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_gtt_mgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_preempt_mgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vram_mgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_virt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_atomfirmware.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vf_error.o
   LD [M]  /tmp/amd.chrxdkMD/amd/amdkcl/amdkcl.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_sched.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_debugfs.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ids.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_gmc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_mmhub.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_hdp.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_xgmi.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_csa.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ras.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vm_cpu.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_sem.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vm_sdma.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_discovery.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ras_eeprom.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_nbio.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_umc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smu_v11_0_i2c.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_fru_eeprom.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_rap.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_fw_attestation.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_securedisplay.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_eeprom.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_mca.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_psp_ta.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_lsdma.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ring_mux.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_xcp.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_seq64.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_aca.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_dev_coredump.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_fdinfo.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_pmu.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/cik.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/cik_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/dce_v8_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/cik_sdma.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/uvd_v4_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vce_v2_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/si.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gmc_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/si_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/si_dma.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/dce_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/uvd_v3_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vi.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mxgpu_vi.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v6_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/soc15.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/emu_soc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mxgpu_ai.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vega10_reg_init.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vega20_reg_init.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v7_4.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v2_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nv.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/arct_reg_init.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mxgpu_nv.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v7_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/hdp_v4_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/hdp_v5_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/aldebaran_reg_init.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/aldebaran.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/soc21.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/soc24.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sienna_cichlid.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smu_v13_0_10.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v4_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/hdp_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v7_7.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/hdp_v5_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/lsdma_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v7_9.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/aqua_vanjaram.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbio_v7_11.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/lsdma_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/hdp_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/nbif_v6_3_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/df_v1_7.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/df_v3_6.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/df_v4_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/df_v4_6_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gmc_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gmc_v8_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gmc_v9_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v1_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v9_4.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v2_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v2_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gmc_v10_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v2_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v2_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v1_7.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v3_0_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gmc_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v3_0_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v3_0_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v1_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v1_8.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v3_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v11_5_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mmhub_v4_1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfxhub_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gmc_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/umc_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/umc_v6_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/umc_v6_7.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/umc_v8_7.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/umc_v8_10.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/umc_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_irq.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/iceland_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/tonga_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/cz_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vega10_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vega20_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/navi10_ih.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/ih_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/ih_v6_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/ih_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_psp.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v3_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v10_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v11_0_8.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v13_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v13_0_4.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/psp_v14_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/dce_v10_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/dce_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vkms.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_gfx.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_rlc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v8_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v9_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v9_4.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v9_4_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v9_4_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v10_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/imu_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v11_0_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/imu_v11_0_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/gfx_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/imu_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_sdma.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v2_4.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v4_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v4_4.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v4_4_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v5_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v5_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/sdma_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_mes.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mes_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mes_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_uvd.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/uvd_v5_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/uvd_v6_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/uvd_v7_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vce.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vce_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vce_v4_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vcn.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_sw_ring.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v2_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v2_5.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v4_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v4_0_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v4_0_5.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vcn_v5_0_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_jpeg.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v2_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v2_5.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v4_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v4_0_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v4_0_5.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/jpeg_v5_0_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_vpe.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/vpe_v6_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_umsch_mm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/umsch_mm_v4_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/athub_v1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/athub_v2_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/athub_v2_1.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/athub_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/athub_v4_1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smuio_v9_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smuio_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smuio_v11_0_6.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smuio_v13_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smuio_v13_0_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smuio_v13_0_6.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/smuio_v14_0_2.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_reset.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/mca_v3_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_module.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_chardev.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_topology.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_pasid.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_doorbell.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_flat_memory.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_process.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_queue.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_mqd_manager.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_mqd_manager_cik.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_mqd_manager_vi.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_mqd_manager_v9.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_mqd_manager_v10.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_mqd_manager_v11.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_mqd_manager_v12.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_kernel_queue.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_packet_manager.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_packet_manager_vi.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_packet_manager_v9.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_process_queue_manager.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device_queue_manager.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device_queue_manager_cik.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device_queue_manager_vi.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device_queue_manager_v9.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device_queue_manager_v10.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device_queue_manager_v11.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_device_queue_manager_v12.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_interrupt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_events.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/cik_event_interrupt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_int_process_v9.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_int_process_v10.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_int_process_v11.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_smi_events.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_crat.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_peerdirect.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_ipc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_trace.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_spm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_debug.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_pc_sampling.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_debugfs.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_svm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../amdkfd/kfd_migrate.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_fence.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gpuvm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gfx_v8.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gfx_v9.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_arcturus.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_aldebaran.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gc_9_4_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gfx_v10.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gfx_v10_3.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gfx_v11.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gfx_v12.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_rlc_spm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_amdkfd_gfx_v7.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_cgs.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_job.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_ioc32.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_atpx_handler.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_acpi.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/amdgpu_hmm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu11/arcturus_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu11/navi10_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu11/sienna_cichlid_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu11/vangogh_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu11/cyan_skillfish_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu11/smu_v11_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu12/renoir_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu12/smu_v12_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/smu_v13_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/aldebaran_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/yellow_carp_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/smu_v13_0_0_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/smu_v13_0_4_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/smu_v13_0_5_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/smu_v13_0_7_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu13/smu_v13_0_6_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu14/smu_v14_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu14/smu_v14_0_0_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu14/smu_v14_0_2_ppt.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/amdgpu_smu.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/swsmu/smu_cmn.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/smu8_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/tonga_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/fiji_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/polaris10_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/iceland_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/smu7_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/vega10_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/smu10_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/ci_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/vega12_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/vegam_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/smu9_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/smumgr/vega20_smumgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/hwmgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/processpptables.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/hardwaremanager.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu8_hwmgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/pppcielanes.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/process_pptables_v1_0.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/ppatomctrl.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/ppatomfwctrl.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu7_hwmgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu7_powertune.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu7_thermal.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu7_clockpowergating.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega10_processpptables.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega10_hwmgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega10_powertune.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega10_thermal.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu10_hwmgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/pp_psm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega12_processpptables.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega12_hwmgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega12_thermal.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/pp_overdriver.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu_helper.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega20_processpptables.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega20_hwmgr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega20_powertune.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega20_thermal.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/common_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega10_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega20_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/vega12_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu9_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/tonga_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/polaris_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/fiji_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/ci_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/hwmgr/smu7_baco.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/powerplay/amd_powerplay.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/legacy-dpm/legacy_dpm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/legacy-dpm/kv_dpm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/legacy-dpm/kv_smc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/legacy-dpm/si_dpm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/legacy-dpm/si_smc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/amdgpu_dpm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/amdgpu_pm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../pm/amdgpu_dpm_internal.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_plane.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_crtc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_irq.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_mst_types.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_color.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_services.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_pp_smu.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_psr.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_replay.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_wb.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/dc_fpu.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_hdcp.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_crc.o
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_debugfs.o
 /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c: In function ‘dm_helpers_dp_mst_send_payload_allocation’:
 /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
       |                                                 ~~~~~~~~~~~~~~~^~~~~~
       |                                                                |
       |                                                                struct drm_atomic_state *
 In file included from /tmp/amd.chrxdkMD/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                  from /tmp/amd.chrxdkMD/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25,
                  from /tmp/amd.chrxdkMD/amd/backport/backport.h:57,
                  from <command-line>:
 ./include/drm/display/drm_dp_mst_helper.h:854:64: note: expected ‘struct drm_dp_mst_atomic_payload *’ but argument is of type ‘struct drm_atomic_state *’
   854 |                              struct drm_dp_mst_atomic_payload *payload);
       |                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~
 /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:15: error: too many arguments to function ‘drm_dp_add_payload_part2’
   563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
       |               ^~~~~~~~~~~~~~~~~~~~~~~~
 ./include/drm/display/drm_dp_mst_helper.h:853:5: note: declared here
   853 | int drm_dp_add_payload_part2(struct drm_dp_mst_topology_mgr *mgr,
       |     ^~~~~~~~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.chrxdkMD/amd/amdgpu/../display/dc/basics/conversion.o
 cc1: some warnings being treated as errors
 make[3]: *** [scripts/Makefile.build:243: /tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.o] Error 1
 make[3]: *** Waiting for unfinished jobs....
 make[2]: *** [scripts/Makefile.build:481: /tmp/amd.chrxdkMD/amd/amdgpu] Error 2
 make[1]: *** [/usr/src/linux-headers-6.8.0-45-generic/Makefile:1925: /tmp/amd.chrxdkMD] Error 2
 make: *** [Makefile:240: __sub-make] Error 2
 make: Leaving directory '/usr/src/linux-headers-6.8.0-45-generic'
DKMSKernelVersion: 6.8.0-45-generic
Date: Thu Sep 19 17:55:48 2024
DuplicateSignature: dkms:amdgpu-dkms:1:6.8.5.60200-2009582.24.04:/tmp/amd.chrxdkMD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
Package: amdgpu-dkms 1:6.8.5.60200-2009582.24.04
PackageVersion: 1:6.8.5.60200-2009582.24.04
SourcePackage: amdgpu-dkms
Title: amdgpu-dkms 1:6.8.5.60200-2009582.24.04: amdgpu kernel module failed to build


---

### 评论 #2 — sarahkaylor (2024-09-19T23:20:33Z)

This issue was previously reported 6 months ago. It may have been broken for Ubuntu 24.04 for half a year perhaps.

https://github.com/ROCm/ROCm/discussions/2938

---

### 评论 #3 — sarahkaylor (2024-09-20T00:24:24Z)

Performed a fresh install of 22.04 (the above error is for 24.04).

$ cat /etc/lsb-release

DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.5 LTS"

Followed these steps:

sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.2/ubuntu/jammy/amdgpu-install_6.2.60200-1_all.deb
sudo apt install ./amdgpu-install_6.2.60200-1_all.deb
sudo apt update
sudo apt install amdgpu-dkms rocm

Same fundamental kernel module compilation error here too -->

  CC [M]  /tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_hdcp.o
 /tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c: In function ‘dm_helpers_dp_mst_send_payload_allocation’:
 /tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
       |                                                 ~~~~~~~~~~~~~~~^~~~~~
       |                                                                |
       |                                                                struct drm_atomic_state *
 In file included from /tmp/amd.TeqEPO3b/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                  from /tmp/amd.TeqEPO3b/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25,
                  from /tmp/amd.TeqEPO3b/amd/backport/backport.h:57,
                  from <command-line>:
 ./include/drm/display/drm_dp_mst_helper.h:854:64: note: expected ‘struct drm_dp_mst_atomic_payload *’ but argument is of type ‘struct drm_atomic_state *’
   854 |                              struct drm_dp_mst_atomic_payload *payload);
       |                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~
 /tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:15: error: too many arguments to function ‘drm_dp_add_payload_part2’
   563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
       |               ^~~~~~~~~~~~~~~~~~~~~~~~
 ./include/drm/display/drm_dp_mst_helper.h:853:5: note: declared here
   853 | int drm_dp_add_payload_part2(struct drm_dp_mst_topology_mgr *mgr,
       |     ^~~~~~~~~~~~~~~~~~~~~~~~
   CC [M]  /tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_crc.o
   CC [M]  /tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_debugfs.o
 cc1: some warnings being treated as errors
   CC [M]  /tmp/amd.TeqEPO3b/amd/amdgpu/../display/dc/basics/conversion.o
 make[3]: *** [scripts/Makefile.build:243: /tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.o] Error 1
 make[3]: *** Waiting for unfinished jobs....
 make[2]: *** [scripts/Makefile.build:481: /tmp/amd.TeqEPO3b/amd/amdgpu] Error 2
 make[1]: *** [/usr/src/linux-headers-6.8.0-45-generic/Makefile:1925: /tmp/amd.TeqEPO3b] Error 2
 make: *** [Makefile:240: __sub-make] Error 2
 make: Leaving directory '/usr/src/linux-headers-6.8.0-45-generic'
DKMSKernelVersion: 6.8.0-45-generic
Date: Thu Sep 19 19:15:30 2024
DuplicateSignature: dkms:amdgpu-dkms:1:6.8.5.60200-2009582.22.04:/tmp/amd.TeqEPO3b/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
Package: amdgpu-dkms 1:6.8.5.60200-2009582.22.04
PackageVersion: 1:6.8.5.60200-2009582.22.04
SourcePackage: amdgpu-dkms



---

### 评论 #4 — kentrussell (2024-09-20T13:25:03Z)

> This issue was previously reported 6 months ago. It may have been broken for Ubuntu 24.04 for half a year perhaps.
> 
> #2938

2938 was a dIfferent error. That one also failed to install, but for different functions being undefined. This issue is specific to the 6.8.0-44+ kernels. Please refer to https://github.com/ROCm/ROCm/issues/3701 . I'll close this off so that we can track everything in 3701, instead of having multiple bug reports open for the same failure.


---

### 评论 #5 — kentrussell (2024-09-20T17:39:37Z)

6.2.1 has this resolved. I just pushed the code out now, specifically:
https://github.com/ROCm/ROCK-Kernel-Driver/commit/2f767b98d4539164c9f1fcb930e4c8f329d586e6

---
