# [Issue]: amdgpu-dkms fails with Ubuntu kernel 6.8.0-44

> **Issue #3701**
> **状态**: closed
> **创建时间**: 2024-09-11T08:12:13Z
> **更新时间**: 2025-11-06T09:36:56Z
> **关闭时间**: 2024-09-22T18:11:35Z
> **作者**: Wedge009
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, AMD Radeon VII, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3701

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

Looks like another problem with `amdgpu-dkms` and new kernels. I was running ROCm 6.2 just fine with kernel 6.8.0-41 - Ubuntu just pushed kernel 6.8.0-44, however, `amdgpu-dkms` fails with that kernel. Rolling back to kernel 6.8.0-41 restored ROCm for me.

### Operating System

Ubuntu 24.04.1

### CPU

Zen 2 and Zen 3

### GPU

AMD Radeon RX 7900 XTX, AMD Radeon VII

### ROCm Version

ROCm 6.2.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (86 条)

### 评论 #1 — harkgill-amd (2024-09-11T15:42:05Z)

Hi @Wedge009, thank you for reporting this issue. I was able to reproduce this when trying to build amdgpu-dkms on the 6.8.0-44 kernel and have created an internal ticket to fix this issue. 

Could you please share your `make.log` to confirm the errors are the same.

---

### 评论 #2 — chrisaga (2024-09-11T16:13:29Z)

> Hi @Wedge009, thank you for reporting this issue. I was able to reproduce this when trying to build amdgpu-dkms on the 6.8.0-44 kernel and have created an internal ticket to fix this issue.
> 
> Could you please share your `make.log` to confirm the errors are the same.

Hello @harkgill-amd
Just struggeling with the same issue here while upgrading to Ubuntu 24.04.1
Here is my `make.log` in case it could be usefull.
[make.log](https://github.com/user-attachments/files/16966486/make.log)

I confirm building for **6.8.0-40-generic** is **OK**
I confirm building for **6.8.0-44-generic** is **KO**


---

### 评论 #3 — SamuelMarks (2024-09-11T16:20:57Z)

Same on my end, upgrading from 6.8.0-41-generic to 6.8.0-44-generic:
[make.log](https://github.com/user-attachments/files/16966582/make.log)


---

### 评论 #4 — harkgill-amd (2024-09-11T17:32:18Z)

Thank you @chrisaga and @SamuelMarks, these are the errors I saw on my end as well. I will provide any relevant updates in this thread. In the meantime, please continue to use the 6.8.0-41 kernel. 

---

### 评论 #5 — MikeLP (2024-09-11T18:01:54Z)

I have the same issue

```

Building module:
Cleaning build area...(bad exit status: 2)
. /tmp/amd.iUoR6MTH/.env && make -j48 KERNELRELEASE=6.8.0-44-generic TTM_NAME=amdttm SCHED_NAME=amd-sched -C /lib/modules/6.8.0-44-generic/build M=/tmp/amd.iUoR6MTH.......(bad exit status: 2)
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.crash'
Error! Bad return status for module build on kernel: 6.8.0-44-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.8.5-2009582.24.04/build/make.log for more information.
dkms autoinstall on 6.8.0-44-generic/x86_64 succeeded for broadcom-sta
dkms autoinstall on 6.8.0-44-generic/x86_64 failed for amdgpu(10)
Error! One or more modules failed to install during autoinstall.
Refer to previous errors for more information.
 * dkms: autoinstall for kernel 6.8.0-44-generic
   ...fail!
run-parts: /etc/kernel/postinst.d/dkms exited with return code 11
dpkg: error processing package linux-image-6.8.0-44-generic (--configure):
 installed linux-image-6.8.0-44-generic package post-installation script subprocess returned error exit status 11
Errors were encountered while processing:
 linux-headers-6.8.0-44-generic
 linux-headers-generic-hwe-24.04
 linux-generic-hwe-24.04
 linux-image-6.8.0-44-generic

```

---

### 评论 #6 — ye-luo (2024-09-11T18:07:34Z)

I encountered the same issue. The failed installation left `/etc/modprobe.d/blacklist-amdgpu.conf` preventing auto loading amdgpu kernel module from `6.8.0-44`. After removing the blacklist file, I'm able to use ROCm 6.2 without installing amdgpu-dkms. amdgpu-dkms is versioned as `6.8.5`, so using upstream `amdgpu` kernel module from upstream linux 6.8 seems working fine on my machine. Hopefully this is useful for people like me who prefer updating kernels.

---

### 评论 #7 — rushilo (2024-09-11T20:54:51Z)

I believe I'm seeing the same issue

```

Building module:
Cleaning build area...(bad exit status: 2)
. /tmp/amd.bvrQUJ8r/.env && make -j16 KERNELRELEASE=6.8.0-44-generic TTM_NAME=amdttm SCHED_NAME=amd-sched -C /lib/modules/6.8.0-44-generic/build M=/tmp/amd.bvrQUJ8r.......
.................^[[B.(bad exit status: 2)
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.crash'
Error! Bad return status for module build on kernel: 6.8.0-44-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.7.0-1787201.22.04/build/make.log for more information.
dkms autoinstall on 6.8.0-44-generic/x86_64 failed for amdgpu(10)
Error! One or more modules failed to install during autoinstall.
Refer to previous errors for more information.
 * dkms: autoinstall for kernel 6.8.0-44-generic
   ...fail!
run-parts: /etc/kernel/postinst.d/dkms exited with return code 11
dpkg: error processing package linux-image-6.8.0-44-generic (--configure):
 installed linux-image-6.8.0-44-generic package post-installation script subprocess returned error exit status 11
No apport report written because MaxReports is reached already
                                                              Errors were encountered while processing:
 linux-headers-6.8.0-44-generic
 linux-headers-generic-hwe-24.04
 linux-generic-hwe-24.04
 linux-image-6.8.0-44-generic
E: Sub-process /usr/bin/dpkg returned an error code (1)
```


---

### 评论 #8 — Layoric (2024-09-12T00:27:36Z)

Hitting same issue and tried fresh install, below are details from crash file containing build error:

```
   CC [M]  /tmp/amd.H03KThtD/amd/amdgpu/../display/dc/basics/dc_common.o
   CC [M]  /tmp/amd.H03KThtD/amd/amdgpu/../display/dc/basics/dce_calcs.o
 /tmp/amd.H03KThtD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c: In function ‘dm_helpers_dp_mst_send_payload_allocation’:
 /tmp/amd.H03KThtD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
       |                                                 ~~~~~~~~~~~~~~~^~~~~~
       |                                                                |
       |                                                                struct drm_atomic_state *
 In file included from /tmp/amd.H03KThtD/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                  from /tmp/amd.H03KThtD/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25,
                  from /tmp/amd.H03KThtD/amd/backport/backport.h:57,
                  from <command-line>:
 ./include/drm/display/drm_dp_mst_helper.h:854:64: note: expected ‘struct drm_dp_mst_atomic_payload *’ but argument is of type ‘struct drm_atomic_state *’
   854 |                              struct drm_dp_mst_atomic_payload *payload);
       |                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~
 /tmp/amd.H03KThtD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:15: error: too many arguments to function ‘drm_dp_add_payload_part2’
   563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
       |               ^~~~~~~~~~~~~~~~~~~~~~~~
 ./include/drm/display/drm_dp_mst_helper.h:853:5: note: declared here
   853 | int drm_dp_add_payload_part2(struct drm_dp_mst_topology_mgr *mgr,
       |     ^~~~~~~~~~~~~~~~~~~~~~~~
 cc1: some warnings being treated as errors
 make[3]: *** [scripts/Makefile.build:243: /tmp/amd.H03KThtD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.o] Error 1
 make[3]: *** Waiting for unfinished jobs....
 make[2]: *** [scripts/Makefile.build:481: /tmp/amd.H03KThtD/amd/amdgpu] Error 2
 make[1]: *** [/usr/src/linux-headers-6.8.0-44-generic/Makefile:1925: /tmp/amd.H03KThtD] Error 2
 make: *** [Makefile:240: __sub-make] Error 2
 make: Leaving directory '/usr/src/linux-headers-6.8.0-44-generic'
DKMSKernelVersion: 6.8.0-44-generic
Date: Wed Sep 11 23:30:34 2024
DuplicateSignature: dkms:amdgpu-dkms:1:6.8.5.60200-2009582.24.04:/tmp/amd.H03KThtD/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
Package: amdgpu-dkms 1:6.8.5.60200-2009582.24.04
PackageVersion: 1:6.8.5.60200-2009582.24.04
SourcePackage: amdgpu-dkms
Title: amdgpu-dkms 1:6.8.5.60200-2009582.24.04: amdgpu kernel module failed to build
```

---

### 评论 #9 — nktice (2024-09-12T01:25:23Z)

Have same issue here ...  standard `apt update` lead to black screen at boot time... 
I can confirm that ROCm 6.1.3 has the same issue. 


---

### 评论 #10 — TiemenSch (2024-09-12T05:05:23Z)

Relevant ubuntu kernel changelog:

https://launchpad.net/ubuntu/+source/linux/6.8.0-44.44

---

### 评论 #11 — lowstz (2024-09-12T07:40:35Z)

I had the same issue yesterday， using `amdgpu-install` with `--no-dkms` fixed it for me.

**Update with @Layoric**
If you are using ROCM in your **container**, using `--no-dkms` will not mitigate your issue

---

### 评论 #12 — Layoric (2024-09-12T07:47:58Z)

@lowstz Are you using ROCM with containers? I believe dkms is required if you want to share host GPU with containers, at least that's [what the ROCM install instructions indicate](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html#install-amdgpu-dkms)

>## Install amdgpu-dkms
>In order to install only the DKMS, which is a minimal requirement for launching containers with GPU access, use the dkms use case:
> `amdgpu-install --usecase=dkms`

So is a show stopper at least for my setup.


---

### 评论 #13 — lowstz (2024-09-12T08:10:06Z)

@Layoric  I used it directly at the host level.
You are right, dkms is a [prerequisite](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html#prerequisites) for the container scenario. It would be better to temporarily roll back and hold the kernel version and wait for the real fix later. I updated my previous reply

---

### 评论 #14 — andyfutcher (2024-09-12T09:49:30Z)

I am experiencing the same issue Layoric described, from my kernel 6.8.0-44-generic build, amdgpu crash logs:
`error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]`

I too will have to keep booting up on the older kernel (load 6.8.0-41-generic) until the dkms build second argument is resolved. Hope the devs can help with this solution soon...

---

### 评论 #15 — NicholasDombi (2024-09-12T10:41:27Z)

Just my luck, I had begun a new journey and install of Ubuntu last night!  Of course the current Ubuntu 24.04.1 LTS (Noble Numbat) comes with the 6.8.0-44-generic kernel!  Every time I tried to build amdgpu-dkms, it had major errors and yep booted to black.  I wasted several hours because of this bug but now I know why thank goodness.  I even had a bug where if I removed the  6.8.0-44-generic kernel and just attempted to go with 6.8.0-41-generic, I lost all internet and network (icons and connection went missing from Ubuntu!).  Fair to say that the start of the journey has been rough...  Fingers double-crossed for a resolution.

---

### 评论 #16 — corinthian13 (2024-09-12T13:10:44Z)

Only started yesterday with me.

I already had kernel 6.8.0-40 in 22.04 before I made the upgrade on August 30.

But the first serious batch of system updates yesterday (including big kernel ones) showed up the issue.

My spool of rubbish:

`$ ./update

 apt updates ...

Hit:1 https://download.docker.com/linux/ubuntu jammy InRelease
Hit:2 http://security.ubuntu.com/ubuntu noble-security InRelease               
Hit:4 https://debian.neo4j.com stable InRelease                                
Hit:5 http://archive.ubuntu.com/ubuntu noble InRelease                         
Hit:6 http://archive.ubuntu.com/ubuntu noble-updates InRelease                 
Ign:7 https://releases.warp.dev/linux/deb stable InRelease                     
Hit:3 https://packages.microsoft.com/repos/edge stable InRelease               
Hit:8 https://releases.warp.dev/linux/deb stable Release            
Get:9 https://repo.charm.sh/apt * InRelease                         
Fetched 6,639 B in 2s (3,813 B/s)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
5 packages can be upgraded. Run 'apt list --upgradable' to see them.
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Calculating upgrade... Done
Get more security updates through Ubuntu Pro with 'esm-apps' enabled:
  libavcodec-extra libcjson1 libavdevice60 ffmpeg libpostproc57
  libavcodec-extra60 libavutil58 libswscale7 libswresample4 libavformat60
  libavfilter9
Learn more about Ubuntu Pro at https://ubuntu.com/pro
The following upgrades have been deferred due to phasing:
  fwupd libfwupd2 python3-distupgrade ubuntu-release-upgrader-core
  ubuntu-release-upgrader-gtk
0 upgraded, 0 newly installed, 0 to remove and 5 not upgraded.
4 not fully installed or removed.
After this operation, 0 B of additional disk space will be used.
Setting up linux-headers-6.8.0-44-generic (6.8.0-44.44) ...
/etc/kernel/header_postinst.d/dkms:
 * dkms: running auto installation service for kernel 6.8.0-44-generic
Sign command: /usr/bin/kmodsign
Signing key: /var/lib/shim-signed/mok/MOK.priv
Public certificate (MOK): /var/lib/shim-signed/mok/MOK.der

Running the pre_build script:
checking for a BSD-compatible install... /usr/bin/install -c
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether the compiler supports GNU C... yes
checking whether gcc accepts -g... yes
checking for gcc option to enable C11 features... none needed
checking how to run the C preprocessor... gcc -E
checking kernel source directory... /usr/src/linux-headers-6.8.0-44-generic
checking kernel build directory... /usr/src/linux-headers-6.8.0-44-generic
checking kernel source version... 6.8.0-44-generic
checking kernel file name for module symbols... Module.symvers
checking for linux/bits.h... yes
checking for linux/io-64-nonatomic-lo-hi.h... yes
checking for asm/set_memory.h... yes
checking for asm/fpu/api.h... yes
checking for linux/compiler_attributes.h... yes
checking for linux/fence-array.h... no
checking for linux/dma-resv.h... yes
checking for linux/mmap_lock.h... yes
checking for linux/pci-p2pdma.h... yes
checking for linux/dma-attrs.h... no
checking for linux/dma-buf-map.h... no
checking for linux/iosys-map.h... yes
checking for linux/stdarg.h... yes
checking for linux/dma-fence-chain.h... yes
checking for linux/xarray.h... yes
checking for linux/container_of.h... yes
checking for linux/cc_platform.h... yes
checking for linux/processor.h... yes
checking for linux/dma-map-ops.h... yes
checking for linux/apple-gmux.h... yes
checking for linux/device/class.h... yes
checking for linux/build_bug.h... yes
checking for linux/acpi_amd_wbrf.h... yes
checking for linux/units.h... yes
checking for drm/drm_backport.h... no
checking for drm/amdgpu_pciid.h... no
checking for drm/drm_probe_helper.h... yes
checking for drm/drmP.h... no
checking for drm/task_barrier.h... yes
checking for drm/drm_managed.h... yes
checking for drm/amd_asic_type.h... yes
checking for drm/drm_aperture.h... yes
checking for drm/dp/drm_dp_helper.h... no
checking for drm/dp/drm_dp_mst_helper.h... no
checking for drm/drm_gem_atomic_helper.h... yes
checking for drm/display/drm_dp_helper.h... yes
checking for drm/display/drm_dp_mst_helper.h... yes
checking for drm/display/drm_dsc.h... yes
checking for drm/display/drm_dsc_helper.h... yes
checking for drm/display/drm_hdmi_helper.h... yes
checking for drm/display/drm_hdcp_helper.h... yes
checking for drm/display/drm_hdcp.h... yes
checking for drm/display/drm_dp.h... yes
checking for linux/pgtable.h... yes
checking for drm/drm_fbdev_generic.h... yes
checking for drm/drm_suballoc.h... yes
checking for drm/drm_exec.h... yes
checking for drm/drm_eld.h... yes
checking for nproc... yes
checking for supported chips... done
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for module configuration... done
configure: creating ./config.status
config.status: creating config/config.h

Building module:
Cleaning build area...(bad exit status: 2)
. /tmp/amd.f1Tr7ZPd/.env && make -j4 KERNELRELEASE=6.8.0-44-generic TTM_NAME=amd
ttm SCHED_NAME=amd-sched -C /lib/modules/6.8.0-44-generic/build M=/tmp/amd.f1Tr7
ZPd.............................................................................
......................(bad exit status: 2)
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.c
rash'
Error! Bad return status for module build on kernel: 6.8.0-44-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.7.0-1787201.22.04/build/make.log for more informa
tion.
dkms autoinstall on 6.8.0-44-generic/x86_64 failed for amdgpu(10)
Error! One or more modules failed to install during autoinstall.
Refer to previous errors for more information.
 * dkms: autoinstall for kernel 6.8.0-44-generic
   ...fail!
run-parts: /etc/kernel/header_postinst.d/dkms exited with return code 11
dpkg: error processing package linux-headers-6.8.0-44-generic (--configure):
 installed linux-headers-6.8.0-44-generic package post-installation script subpr
ocess returned error exit status 11
Setting up linux-image-6.8.0-44-generic (6.8.0-44.44) ...
dpkg: dependency problems prevent configuration of linux-headers-generic:
 linux-headers-generic depends on linux-headers-6.8.0-44-generic; however:
  Package linux-headers-6.8.0-44-generic is not configured yet.

dpkg: error processing package linux-headers-generic (--configure):
 dependency problems - leaving unconfigured
dpkg: dependency problems prevent configuration of linux-generic:
 linux-generic depends on linux-headers-generic (= 6.8.0-44.44); however:
  Package linux-headers-generic is not configured yet.

dpkg: error processing package linux-generic (--configure):
 dependency problems - leaving unconfigured
No apport report written because the error message indicates its a followup erro
r from a previous failure.
                          No apport report written because the error message ind
icates its a followup error from a previous failure.
                                                    Processing triggers for linu
x-image-6.8.0-44-generic (6.8.0-44.44) ...
/etc/kernel/postinst.d/dkms:
 * dkms: running auto installation service for kernel 6.8.0-44-generic
Sign command: /usr/bin/kmodsign
Signing key: /var/lib/shim-signed/mok/MOK.priv
Public certificate (MOK): /var/lib/shim-signed/mok/MOK.der

Running the pre_build script:
checking for a BSD-compatible install... /usr/bin/install -c
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether the compiler supports GNU C... yes
checking whether gcc accepts -g... yes
checking for gcc option to enable C11 features... none needed
checking how to run the C preprocessor... gcc -E
checking kernel source directory... /usr/src/linux-headers-6.8.0-44-generic
checking kernel build directory... /usr/src/linux-headers-6.8.0-44-generic
checking kernel source version... 6.8.0-44-generic
checking kernel file name for module symbols... Module.symvers
checking for linux/bits.h... yes
checking for linux/io-64-nonatomic-lo-hi.h... yes
checking for asm/set_memory.h... yes
checking for asm/fpu/api.h... yes
checking for linux/compiler_attributes.h... yes
checking for linux/fence-array.h... no
checking for linux/dma-resv.h... yes
checking for linux/mmap_lock.h... yes
checking for linux/pci-p2pdma.h... yes
checking for linux/dma-attrs.h... no
checking for linux/dma-buf-map.h... no
checking for linux/iosys-map.h... yes
checking for linux/stdarg.h... yes
checking for linux/dma-fence-chain.h... yes
checking for linux/xarray.h... yes
checking for linux/container_of.h... yes
checking for linux/cc_platform.h... yes
checking for linux/processor.h... yes
checking for linux/dma-map-ops.h... yes
checking for linux/apple-gmux.h... yes
checking for linux/device/class.h... yes
checking for linux/build_bug.h... yes
checking for linux/acpi_amd_wbrf.h... yes
checking for linux/units.h... yes
checking for drm/drm_backport.h... no
checking for drm/amdgpu_pciid.h... no
checking for drm/drm_probe_helper.h... yes
checking for drm/drmP.h... no
checking for drm/task_barrier.h... yes
checking for drm/drm_managed.h... yes
checking for drm/amd_asic_type.h... yes
checking for drm/drm_aperture.h... yes
checking for drm/dp/drm_dp_helper.h... no
checking for drm/dp/drm_dp_mst_helper.h... no
checking for drm/drm_gem_atomic_helper.h... yes
checking for drm/display/drm_dp_helper.h... yes
checking for drm/display/drm_dp_mst_helper.h... yes
checking for drm/display/drm_dsc.h... yes
checking for drm/display/drm_dsc_helper.h... yes
checking for drm/display/drm_hdmi_helper.h... yes
checking for drm/display/drm_hdcp_helper.h... yes
checking for drm/display/drm_hdcp.h... yes
checking for drm/display/drm_dp.h... yes
checking for linux/pgtable.h... yes
checking for drm/drm_fbdev_generic.h... yes
checking for drm/drm_suballoc.h... yes
checking for drm/drm_exec.h... yes
checking for drm/drm_eld.h... yes
checking for nproc... yes
checking for supported chips... done
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for nproc... (cached) yes
checking for module configuration... done
configure: creating ./config.status
config.status: creating config/config.h

Building module:
Cleaning build area...(bad exit status: 2)
. /tmp/amd.FhxPpAsK/.env && make -j4 KERNELRELEASE=6.8.0-44-generic TTM_NAME=amd
ttm SCHED_NAME=amd-sched -C /lib/modules/6.8.0-44-generic/build M=/tmp/amd.FhxPp
AsK.............................................................................
..........................(bad exit status: 2)
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.c
rash'
Error! Bad return status for module build on kernel: 6.8.0-44-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.7.0-1787201.22.04/build/make.log for more informa
tion.
dkms autoinstall on 6.8.0-44-generic/x86_64 failed for amdgpu(10)
Error! One or more modules failed to install during autoinstall.
Refer to previous errors for more information.
 * dkms: autoinstall for kernel 6.8.0-44-generic
   ...fail!
run-parts: /etc/kernel/postinst.d/dkms exited with return code 11
dpkg: error processing package linux-image-6.8.0-44-generic (--configure):
 installed linux-image-6.8.0-44-generic package post-installation script subproc
ess returned error exit status 11
No apport report written because MaxReports is reached already
                                                              Errors were encoun
tered while processing:
 linux-headers-6.8.0-44-generic
 linux-headers-generic
 linux-generic
 linux-image-6.8.0-44-generic
E: Sub-process /usr/bin/dpkg returned an error code (1)`

---

### 评论 #17 — nktice (2024-09-12T13:29:30Z)

> I am experiencing the same issue Layoric described, from my kernel 6.8.0-44-generic build, amdgpu crash logs: `error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]`
> 
> I too will have to keep booting up on the older kernel (load 6.8.0-41-generic) until the dkms build second argument is resolved. Hope the devs can help with this solution soon...

It seems worth noting this particular function has been in the news : 
https://github.com/advisories/GHSA-52j9-mgvj-v9gh
It had been subject of vulnerability that's recently 'fixed'.

Perhaps someone can tell if the issue we have may be related.  
Does this 'fix' not work?  Or are AMD drivers perhaps exploited?
Given the issue one might not want to revert to older versions
if there is indeed a security issue being exploited. 

---

### 评论 #18 — Vidalvorada (2024-09-12T15:30:51Z)

Im on linux Mint. 
Ubuntu: 22.04 
kernel:  6.8.0-44-generic
GPU: AMD Radeon 7800XT

When i install amdgpu-dkms i get the following error:
`Building for 6.8.0-44-generic
Building for architecture amd64
Building initial module for 6.8.0-44-generic
Error! Bad return status for module build on kernel: 6.8.0-44-generic (amd64)
Consult /var/lib/dkms/amdgpu/6.8.5-2009582.24.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status
 10
Processing triggers for man-db (2.12.0-4build2) ...
Processing triggers for install-info (7.1-3build2) ...
Errors were encountered while processing:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)
`
my log is: 
[MYmake.log](https://github.com/user-attachments/files/16981983/MYmake.log)

After installation, when i select the kernel on GRUB the OS won't boot anymore. In compatibility mode (with deactivated video drivers, i think...) the OS boots normally. Hope this info helps, please solve this!

---

### 评论 #19 — alain-bkr (2024-09-12T16:19:48Z)

Same issue after upgrading from ubuntu 22.04 to 24.04
kernel : 6.8.0-44-generic
GPU: AMD Radeon RX6800XT

The /var/lib/dkms/amdgpu/6.8.5-2009582.24.04/build/make.log show errors in the last 10 lines

` amdgpu_dm_helpers.c:563:15: error: too many arguments to function ‘drm_dp_add_payload_part2’ ` 

the end of the make.log

``` 
  CC [M]  /tmp/amd.A28wySuZ/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_crc.o
/tmp/amd.A28wySuZ/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c: In function ‘dm_helpers_dp_mst_send_payload_allocation’:
/tmp/amd.A28wySuZ/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
  563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
      |                                                 ~~~~~~~~~~~~~~~^~~~~~
      |                                                                |
      |                                                                struct drm_atomic_state *
In file included from /tmp/amd.A28wySuZ/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                 from /tmp/amd.A28wySuZ/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25,
                 from /tmp/amd.A28wySuZ/amd/backport/backport.h:57,
                 from <command-line>:
./include/drm/display/drm_dp_mst_helper.h:854:64: note: expected ‘struct drm_dp_mst_atomic_payload *’ but argument is of type ‘struct drm_atomic_state *’
  854 |                              struct drm_dp_mst_atomic_payload *payload);
      |                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~
/tmp/amd.A28wySuZ/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:563:15: error: too many arguments to function ‘drm_dp_add_payload_part2’
  563 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
      |               ^~~~~~~~~~~~~~~~~~~~~~~~
./include/drm/display/drm_dp_mst_helper.h:853:5: note: declared here
  853 | int drm_dp_add_payload_part2(struct drm_dp_mst_topology_mgr *mgr,
      |     ^~~~~~~~~~~~~~~~~~~~~~~~
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243 : /tmp/amd.A28wySuZ/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.o] Erreur 1
make[3]: *** Attente des tâches non terminées....
make[2]: *** [scripts/Makefile.build:481 : /tmp/amd.A28wySuZ/amd/amdgpu] Erreur 2
make[1]: *** [/usr/src/linux-headers-6.8.0-44-generic/Makefile:1925 : /tmp/amd.A28wySuZ] Erreur 2
make: *** [Makefile:240 : __sub-make] Erreur 2
make : on quitte le répertoire « /usr/src/linux-headers-6.8.0-44-generic »
``` 




---

### 评论 #20 — alain-bkr (2024-09-12T16:21:07Z)

[make.log](https://github.com/user-attachments/files/16982636/make.log)


---

### 评论 #21 — nktice (2024-09-13T01:26:43Z)

Ubuntu replaced distro 24.04 with a new version ( 24.04.1 ) and have been encouraging all upgrade to it...  Alas it comes with no way to revert kernel to older versions...  ( <= 6.8.0-41 ).

Currently I've found one possible work around to get things going...
The new dev version Ubuntu 24.10 ( that's meant for next month ) 
comes with a kernel that does appear function with offered drivers - 6.8.0-31-generic. 
https://cdimage.ubuntu.com/daily-live/20240911/
If you go this route, you might want to stop upgrades to a new kernel - 
```bash
sudo apt-mark hold linux-image-6.8.0-31-generic
```
[ I am not sure if you'd need to get all the parts, or if that will do - but that's a key part, that might be enough to stop an automatic update from upgrading it. ] 

So far this appears to work with ROCm 6.2's amdgpu-dkms installs as normal.  [ Of course it does mean there's lots of other issues with the dev version... ] 


---

### 评论 #22 — NicholasDombi (2024-09-13T01:47:12Z)

@nktice Thanks...  Are you saying you ran the new install of 24.10 and it comes with 6.8.0-31-generic kernel?  Going to give this a shot. 

---

### 评论 #23 — nktice (2024-09-13T01:56:57Z)

> @nktice Thanks... Are you saying you ran the new install of 24.10 and it comes with 6.8.0-31-generic kernel? Going to give this a shot.

I maintain this guide on using some AI tools with AMD's cards...  https://github.com/nktice/AMD-AI -  Using Ubuntu 24.10 ( dev release ) in the last few hours, I have gone so far as to have  functioning ComfyUI and Stable Diffusion, but I am still working on textgen webui.   As such there's updates, that I have yet to post there, as I'm not finished.  But it seems to work for many of the functions like older versions.    I need a break now, as I've other things to do - here's my notes so far : https://github.com/nktice/AMD-AI/blob/main/Ubuntu24.10.md 

---

### 评论 #24 — Wedge009 (2024-09-13T02:21:43Z)

> Alas it comes with no way to revert kernel to older versions... ( <= 6.8.0-41 ).

Why do you say no way? Even with a clean, fresh installation of the OS, can't you manually install `linux-image-6.8.0-41-generic`, etc? That's basically what I did, though admittedly not with a clean installation.

---

### 评论 #25 — SamuelMarks (2024-09-13T03:48:42Z)

@nktice Try using https://github.com/bkw777/mainline - I used it many times to install various different kernel versions

---

### 评论 #26 — nktice (2024-09-13T04:42:19Z)

> @nktice Try using https://github.com/bkw777/mainline - I used it many times to install various different kernel versions

Tried that yesterday... I had the same issue with a newer kernel.  With older kernels, Ubuntu's variations don't appear offered - so the dash version, such as -41 isn't offered there.  I did attempt mainline's 6.8.0 but did not see how to get it to switch over to booting that one as the new system.  

It seemed easier to just install the packages with the apt system.  Alas it didn't seem to want to switch over to older kernels.  I wasn't sure if the issue was something else due to the changes in the new version of Ubuntu they released but had issues with.  Here's some news on that - which is somewhat related to what we're facing : 
https://discourse.ubuntu.com/t/upgrades-to-ubuntu-24-04-1-lts-are-enabled-again/47920
It notes that they're not catching error return codes and that makes messes.  The problem we have with amdgpu-dkms is compounded because its error isn't handled appropriately.  Gracious function there would have stopped at the error, and rolled-back upgrade. [ Instead I got a surprise black-screen after reboot, and no solution... 
  I suspect there's lots of folks being burned by this, as such it's tragic.   ]
Like I said above, some part may be Ubuntu's, not being gracious - but I understand such things get amazingly complicated there... 
It may be we need the ROCm maintainer folks to rebuild their stuff, and check it works with the now patched kernel versions that have been offered.  

---

### 评论 #27 — Wedge009 (2024-09-13T05:26:43Z)

Yes, of course, the onus is on a ROCm update to accommodate the new kernel if Ubuntu 24.04 is to be listed as supported. The kernel roll-back is only a work-around while we wait. The issue lies with ROCm, not the kernel.

I could be wrong, but it sounds like you're relying on the `linux-generic`/`linux-generic-hwe-24.04` meta-package which, of course, is only picking the latest kernel. You should be able to install kernel packages individually, for example:
* https://packages.ubuntu.com/noble/linux-headers-6.8.0-41-generic
* https://packages.ubuntu.com/noble/linux-image-6.8.0-41-generic
* https://packages.ubuntu.com/noble/linux-modules-6.8.0-41-generic
* etc

For as long as the meta-packages rely on kernels that ROCm doesn't agree with, they'll have to be removed, unfortunately. I mainly use `aptitude` to manage packages.

---

### 评论 #28 — nktice (2024-09-14T02:13:41Z)

Here are the commands to swap in the old kernel ( for those who need them... ) 
```bash
# check kernel version 
uname -r 
# example output : "6.8.0-44-generic" or after reboot "6.8.0-41-generic"

# list the apt packages that refer to that kernel version -
apt list --installed | grep 6.8.0-44 
# this shows the relevant files we need alternate versions for...

# install 6.8.0-41 files : 
sudo apt install linux-headers-6.8.0-41-generic linux-headers-6.8.0-41 linux-image-6.8.0-41-generic linux-modules-6.8.0-41-generic linux-modules-extra-6.8.0-41-generic linux-tools-6.8.0-41-generic linux-tools-6.8.0-41 -y

# remove current kernel - note that this will show a warning screen ( logic is reversed ) 
sudo apt remove linux-headers-6.8.0-44-generic linux-headers-6.8.0-44 linux-image-6.8.0-44-generic linux-modules-6.8.0-44-generic linux-modules-extra-6.8.0-44-generic linux-tools-6.8.0-44-generic linux-tools-6.8.0-44 -y

# Now refresh grub ( controls boot process ) 
sudo update-grub
# notice it's output should show only the preferred kernel. 

reboot 
# this will get you rebooted with the preferred kernel
````
 

---

### 评论 #29 — corinthian13 (2024-09-14T14:57:43Z)

@nktice 

The problem for me and others is that we already have 6.8.0-41 but cannot get 6.8.0-44 installed . . .

---

### 评论 #30 — ruvkr (2024-09-14T15:12:31Z)

@nktice Will I be able to update using apt update later?

---

### 评论 #31 — kswit (2024-09-14T17:32:58Z)

I found some minor changes in the Kernel driver:

[Recover the original NULL fix and remove the unnecessary input parameter 'state' for
drm_dp_add_payload_part2()](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=8e21de5f99b2368a5155037ce0aae8aaba3f5241)

they can be used for /var/lib/dkms/amdgpu/6.8.5-2009582.24.04/source/amd/display/amdgpu_dm/amdgpu_dm_helpers.c

After this correction, I managed to build the driver:
`amdgpu/6.8.5-2009582.24.04, 6.8.0-44-generic, x86_64: installed`

---

### 评论 #32 — nktice (2024-09-14T21:01:18Z)

> @corinthian13 
> 
> " The problem for me and others is that we already have 6.8.0-41 but cannot get 6.8.0-44 installed . . . "

Have you tried looking in grub's options while booting?  ( Advanced Options ).  
Here is some more info on relevant grub settings that I found useful : 
https://askubuntu.com/questions/82140/how-can-i-boot-with-an-older-kernel-version

The script I posted removes the newer kernel, so that the default is the older one, and then calls the 'update-grub' to prepare reboot - such that at reboot, it uses the old kernel [ it's the only choice. ]  


---

### 评论 #33 — corinthian13 (2024-09-14T21:15:07Z)

That Ask Ubuntu post is 2011, man.

In any case it seems to be the amdgpu version that needs to be adapted to suit the existing/new version of the Linux kernel.

I have no trouble booting (well, there is a long delay before the screen breaks open) from 6.8.0-41.
But I have concerns that this issue could be holding up future updates.

---

### 评论 #34 — nktice (2024-09-14T21:19:03Z)

> @ruvkr " Will I be able to update using apt update later? "

There's nothing in there that would stop you upgrading with the apt system. 
The issue we have is AMD's drivers don't support new kernels. 
Once there's new drivers, hopefully they will install in the normal way, 
and one can switch to using a newer kernel with apt ( or mainline ... ). 

---

### 评论 #35 — nktice (2024-09-14T21:22:20Z)

> That Ask Ubuntu post is 2011, man.
> 
> In any case it seems to be the amdgpu version that needs to be adapted to suit the existing/new version of the Linux kernel.
> 
> I have no trouble booting (well, there is a long delay before the screen breaks open) from 6.8.0-41. But I have concerns that this issue could be holding up future updates.

Given what I've seen with the AMD drivers and development... 
it is unlikely we'll see an update for this, and will have to wait...
so 6.2.1, or 6.3,  or whatever the next release is, 
that version might work... but they might just 'not support' new kernel versions. 



---

### 评论 #36 — aphor (2024-09-14T23:52:32Z)

Confirmed: 

1. amdgpu-uninstall
2. download and install latest amdgpu deb
3. amdgpu-dkms fails, with source to installed header compatibility errors during build

Same compiler errors as @alain-bkr and @Layoric from `amdgpu-dkms` build: 
```
...
  CC [M]  /tmp/amd.gUeRkJ9X/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_hdcp.o
/tmp/amd.gUeRkJ9X/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c: In function ‘dm_helpers_dp_mst_send_payload_allocation’:
/tmp/amd.gUeRkJ9X/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:560:64: error: passing argument 2 of ‘drm_dp_add_payload_part2’ from incompatible pointer type [-Werror=incompatible-pointer-types]
  560 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
      |                                                 ~~~~~~~~~~~~~~~^~~~~~
      |                                                                |
      |                                                                struct drm_atomic_state *
In file included from /tmp/amd.gUeRkJ9X/include/kcl/header/drm/display/drm_dp_mst_helper.h:6,
                 from /tmp/amd.gUeRkJ9X/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h:25,
                 from /tmp/amd.gUeRkJ9X/amd/backport/backport.h:57,
                 from <command-line>:
./include/drm/display/drm_dp_mst_helper.h:854:64: note: expected ‘struct drm_dp_mst_atomic_payload *’ but argument is of type ‘struct drm_atomic_state *’
  854 |                              struct drm_dp_mst_atomic_payload *payload);
      |                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~
/tmp/amd.gUeRkJ9X/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.c:560:15: error: too many arguments to function ‘drm_dp_add_payload_part2’
  560 |         ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
      |               ^~~~~~~~~~~~~~~~~~~~~~~~
./include/drm/display/drm_dp_mst_helper.h:853:5: note: declared here
  853 | int drm_dp_add_payload_part2(struct drm_dp_mst_topology_mgr *mgr,
      |     ^~~~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /tmp/amd.gUeRkJ9X/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_crc.o
  CC [M]  /tmp/amd.gUeRkJ9X/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_debugfs.o
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243: /tmp/amd.gUeRkJ9X/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm_helpers.o] Error 1
make[3]: *** Waiting for unfinished jobs....
make[2]: *** [scripts/Makefile.build:481: /tmp/amd.gUeRkJ9X/amd/amdgpu] Error 2
make[1]: *** [/usr/src/linux-headers-6.8.0-44-generic/Makefile:1925: /tmp/amd.gUeRkJ9X] Error 2
make: *** [Makefile:240: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.8.0-44-generic'
```


---

### 评论 #37 — SamuelMarks (2024-09-15T00:04:20Z)

When running the earlier kernel, e.g., 6.8.0-41, run these commands:
```sh
# Ensure you didn't accidentally `autoremove` any of the necessary packages; also run this if you're on the wrong kernel version
$ sudo apt install -y linux-headers-6.8.0-41-generic linux-headers-6.8.0-41 linux-image-6.8.0-41-generic linux-modules-6.8.0-41-generic linux-modules-extra-6.8.0-41-generic linux-tools-6.8.0-41-generic linux-tools-6.8.0-41
# Prevent this older kernel version from being automatically upgraded to 6.8.0-44
$ sudo apt-mark hold linux-*-6.8.0-41
# Remove the installed newer kernel + any configuration / build files
$ sudo apt purge -y linux-*-6.8.0-44
```

It should automatically update your bootloader (e.g., GRUB), and configure things properly. When AMD fixes this issue, you'll want to run: `sudo apt-mark unhold linux-*-6.8.0-41`

PS: Alternatively as I said earlier you can use https://github.com/bkw777/mainline to install non Canonical [pun intended?] versions of the Linux kernel. Not just the latest kernel version, but 100+ different versions. Technically it is Canonical, and you can see the versions here or with the `mainline` GUI or CLI https://kernel.ubuntu.com/mainline/?C=N;O=D


---

### 评论 #38 — alain-bkr (2024-09-15T00:29:44Z)

https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351075492

> I found some minor changes in the Kernel driver:
> 
> [Recover the original NULL fix and remove the unnecessary input parameter 'state' for drm_dp_add_payload_part2()](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id=8e21de5f99b2368a5155037ce0aae8aaba3f5241)
> 
> they can be used for /var/lib/dkms/amdgpu/6.8.5-2009582.24.04/source/amd/display/amdgpu_dm/amdgpu_dm_helpers.c
> 
> After this correction, I managed to build the driver: `amdgpu/6.8.5-2009582.24.04, 6.8.0-44-generic, x86_64: installed`

Nice investigation :+1: 

I guess you did just suppress the offending second argument  

``` 
--- amdgpu-6.8.5-2009582.24.04/amd/display/amdgpu_dm/amdgpu_dm_helpers.c.orig	2024-09-15 02:14:04.832572558 +0200
+++ amdgpu-6.8.5-2009582.24.04/amd/display/amdgpu_dm/amdgpu_dm_helpers.c	2024-09-15 02:15:20.000526238 +0200
@@ -560,7 +560,7 @@
 #endif
 
 #if defined(HAVE_DRM_DP_MST_TOPOLOGY_STATE_PAYLOADS)
-	ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
+	ret = drm_dp_add_payload_part2(mst_mgr, new_payload);
 #else
 	ret = drm_dp_update_payload_part2(mst_mgr);
 #endif
``` 

I did this, it compiles and upgrade, but i have no idea of the consequences (and how long it will last with future upgrades)



---

### 评论 #39 — nktice (2024-09-15T04:04:00Z)

> --- amdgpu-6.8.5-2009582.24.04/amd/display/amdgpu_dm/amdgpu_dm_helpers.c.orig	2024-09-15 02:14:04.832572558 +0200
> +++ amdgpu-6.8.5-2009582.24.04/amd/display/amdgpu_dm/amdgpu_dm_helpers.c	2024-09-15 02:15:20.000526238 +0200
> @@ -560,7 +560,7 @@
>  #endif
>  
>  #if defined(HAVE_DRM_DP_MST_TOPOLOGY_STATE_PAYLOADS)
> -	ret = drm_dp_add_payload_part2(mst_mgr, mst_state->base.state, new_payload);
> +	ret = drm_dp_add_payload_part2(mst_mgr, new_payload);
>  #else
>  	ret = drm_dp_update_payload_part2(mst_mgr);
>  #endif
> ```
> 
> I did this, it compiles and upgrade, but i have no idea of the consequences (and how long it will last with future upgrades)

Thanks for finding that...  for those who want to try it, here are shell commands...


This is assuming you have your apt system setup for ROCm - 
and are set to use ROCm version 6.2 ( under Ubuntu...  24.04.1 ) 

```bash 
# attempt (and fail) to install amdgpu-dkms - this get the source code, so we can change it...
sudo apt install  amdgpu-dkms 
# go to the directory...
cd /usr/src/amdgpu-6.8.5-2009582.24.04/amd/display/amdgpu_dm/
# backup file before editing...
sudo cp amdgpu_dm_helpers.c amdgpu_dm_helpers.c.orig
# edit the line...
sudo sed -i "s@mst_state->base.state,@\ @g" amdgpu_dm_helpers.c
# now we can finish the install with the amended code...
sudo apt install  amdgpu-dkms 
# in case that doesn't work... because it's installed, to 'reinstall' : 
# sudo apt reinstall  amdgpu-dkms 
```

Of course as always, it is use at your own risk, with no warranty... 
That said, it appears like it is working for me, with the 'new' kernel.  
This solution is likely better than using outdated kernels. 



---

### 评论 #40 — Wedge009 (2024-09-15T08:57:36Z)

> The problem for me and others is that we already have 6.8.0-41 but cannot get 6.8.0-44 installed . . .

I don't understand why this is a problem. The issue I reported here is with -44.

> I found some minor changes in the Kernel driver:
> 
> they can be used for /var/lib/dkms/amdgpu/6.8.5-2009582.24.04/source/amd/display/amdgpu_dm/amdgpu_dm_helpers.c
> 
> After this correction, I managed to build the driver: `amdgpu/6.8.5-2009582.24.04, 6.8.0-44-generic, x86_64: installed`

Could you submit a PR for that, please? It may be quicker for that to be merged than for the issue to be resolved internally.

---

### 评论 #41 — chrisaga (2024-09-15T15:09:18Z)

@nktice @alain-bkr , I used what you found to make a custom dkms.conf which allows to build ans install amdgpu-dkms without editing the source file.

It's a config file in `/etc/dkms` which contains the patch and the command to build the modules. See : https://github.com/chrisaga/amd-dkms-patch
Hopping this can be useful while we wait for a more permanent solution.

---

### 评论 #42 — alain-bkr (2024-09-16T07:48:23Z)

i believe this is a ubuntu specific problem, as they choose 6.8 kernel (sadly not a LTS one) , picked some patch in -44 and thus break their partner's code !

I create a bug report on Ubuntu side, as it is their patch that caused the bug 

 (`<rant>` Ubuntu picks random patch without testing partner's  software , not even basic compile test =  bad QA ! `</rant>`)

https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823

Just click to say "affects me too" :-) 
https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823/+affectsmetoo

---

### 评论 #43 — rushilo (2024-09-17T04:20:47Z)

> i believe this is a ubuntu specific problem, as they choose 6.8 kernel (sadly not a LTS one) , picked some patch in -44 and thus break their partner's code !
> 
> I create a bug report on Ubuntu side, as it is their patch that caused the bug
> 
> (`<rant>` Ubuntu picks random patch without testing partner's software , not even basic compile test = bad QA ! `</rant>`)
> 
> https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823
> 
> Just click to say "affects me too" :-) https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823/+affectsmetoo

Yeah I think you're right;  I have a second system (running essentially identical install of Ubuntu 24.04) with an Nvidia GPU and the 6.8.0-44 update broke my Nvidia graphics + CUDA driver packages as well. Must be something with how its handling dkms ?

---

### 评论 #44 — awz (2024-09-17T07:34:25Z)

https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351346975 

Worked for me.

---

### 评论 #45 — BrezzeLevsky (2024-09-17T10:11:03Z)

https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351631247
Work fo me.

Today 6.8.0-45-generic new Ubuntu 24 updates, kernel updates appeared again. Same problems.

---

### 评论 #46 — HardAndHeavy (2024-09-17T10:16:15Z)

https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351346975

I have a mistake. The file manager and messenger stopped working. Only the terminal and the browser worked.

---

### 评论 #47 — nktice (2024-09-17T18:38:28Z)

To test new kernel, I did an update today, with the change in place... 
( https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351346975 ) 
` sudo apt update -y && sudo apt upgrade -y ` 
ran without error, then rebooted my system, and it came back fine. 
`uname -r` before = 6.8.0-44-generic
`uname -r` after = 6.8.0-45-generic

---

### 评论 #48 — splineai-cloud (2024-09-17T23:00:33Z)

> To test new kernel, I did an update today, with the change in place... ( [#3701 (comment)](https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351346975) ) `sudo apt update -y && sudo apt upgrade -y` ran without error, then rebooted my system, and it came back fine. `uname -r` before = 6.8.0-44-generic `uname -r` after = 6.8.0-45-generic

------------------
Can we install amdgpu-dkms without any error?
That will be a great info!

~Syed


---

### 评论 #49 — splineai-cloud (2024-09-17T23:32:34Z)

> > To test new kernel, I did an update today, with the change in place... ( [#3701 (comment)](https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351346975) ) `sudo apt update -y && sudo apt upgrade -y` ran without error, then rebooted my system, and it came back fine. `uname -r` before = 6.8.0-44-generic `uname -r` after = 6.8.0-45-generic
> 
> Can we install amdgpu-dkms without any error? That will be a great info!
> 
> ~Syed

Good news the installation works!
$sudo apt install amdgpu-dkms

However, the command still returns error:
$ dkms status
Error! Could not locate dkms.conf file.
File: /var/lib/dkms/amdgpu/6.8.5-2009582.22.04/source/dkms.conf does not exist.


---

### 评论 #50 — e1248 (2024-09-18T11:27:30Z)

> i believe this is a ubuntu specific problem, as they choose 6.8 kernel (sadly not a LTS one) , picked some patch in -44 and thus break their partner's code !
> 
> I create a bug report on Ubuntu side, as it is their patch that caused the bug
> 
> (`<rant>` Ubuntu picks random patch without testing partner's software , not even basic compile test = bad QA ! `</rant>`)
> 
> https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823
> 
> Just click to say "affects me too" :-) https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823/+affectsmetoo

Unfortunately, that Ubuntu bug report has now been set to "Won't Fix" per this comment https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823/comments/5

FYI, that comment in the ubuntu bug report says the following:
> [Mario Limonciello (superm1)](https://launchpad.net/~superm1) wrote 17 hours ago:			[#5](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2080823/comments/5)
> I am tending to agree with Juerg, this is not Ubuntu's bug. They picked up a stable update that fixed a problem, but it just so happens this DKMS doesn't compile anymore.
>
> I think the DKMS package will need to be re-spun due to this change.
> I suggest reporting it here: https://gitlab.freedesktop.org/drm/amd/-/issues
>
> ---
>
> But that being said - why not use the amdgpu driver distributed in Ubuntu?
>
> **Changed in linux (Ubuntu):**
> **status:	Incomplete → Won't Fix**

Note at the bottom he has set the Ubuntu bug report to status: "Won't Fix".

---

### 评论 #51 — kentrussell (2024-09-18T15:45:31Z)

We're working on a KCL (Kernel Compatibility Layer) fix and will be deploying that once it's validated. No idea when it'll be released or which release it will be, though (IE if it'll be a respin of 6.2.1, come in 6.2.2, wait to 6.3, etc)

For reference, the KCL has a ton of "if this, then do that" checks based on what the base kernel supports. You can see them in "drivers/gpu/drm/amd/dkms/m4" . This will just be another one. We'll check for the number of params in drm_dp_add_payload_part2 and adjust accordingly. It happens a ton, and normally we have more time to detect and resolve these issues, before it ends up impacting the majority of users using the kernel provided by their OS. It's just some bad timing.

The current solution is possibly provided below. This is an internal patch, and the official AMD stance is to wait for the solution to be published in the next release. But if you want to do your own code editing, this is possibly the patch coming to resolve the issue:

```
commit 11d2faacb515afca6e2b0bc625d7c9889e3e9bb4
Author: Asher Song <Asher.Song@amd.com>
Date:   Tue Aug 27 09:35:42 2024 +0800

    drm/amdkcl: check drm_dp_add_payload_part2 whether requires three
    argunments

    It's caused by v6.9-rc6-1554-g8a0a7b98d4b6
    drm/mst: Fix NULL pointer dereference at drm_dp_add_payload_part2

    commit v5.19-rc6-1771-g4d07b0bc4034
    drm/display/dp_mst: Move all payload info into the atomic state

    Signed-off-by: Asher Song <Asher.Song@amd.com>

diff --git a/drivers/gpu/drm/amd/dkms/m4/drm-dp-mst-topology-state.m4 b/drivers/gpu/drm/amd/dkms/m4/drm-dp-mst-topology-state.m4
index 424778ea6606..d5928adc0984 100644
--- a/drivers/gpu/drm/amd/dkms/m4/drm-dp-mst-topology-state.m4
+++ b/drivers/gpu/drm/amd/dkms/m4/drm-dp-mst-topology-state.m4
@@ -67,3 +67,23 @@ AC_DEFUN([AC_AMDGPU_DRM_DP_MST_TOPOLOGY_STATE_PBN_DIV], [
         ])
 ])

+dnl #
+dnl # commit v6.9-rc6-1554-g8a0a7b98d4b6
+dnl # drm/mst: Fix NULL pointer dereference at drm_dp_add_payload_part2
+dnl #
+dnl # commit v5.19-rc6-1771-g4d07b0bc4034
+dnl # drm/display/dp_mst: Move all payload info into the atomic state
+dnl #
+AC_DEFUN([AC_AMDGPU_DRM_DP_ADD_PAYLOAD_PART2_THREE_ARGUMENTS], [
+       AC_KERNEL_DO_BACKGROUND([
+               AC_KERNEL_TRY_COMPILE([
+                       #include <drm/display/drm_dp_mst_helper.h>
+               ], [
+                   int a = 0;
+                       a = drm_dp_add_payload_part2(NULL, NULL, NULL);
+               ], [
+                       AC_DEFINE(HAVE_DRM_DP_ADD_PAYLOAD_PART2_THREE_ARGUMENTS, 1,
+                               [drm_dp_add_payload_part2 has three arguments])
+               ])
+       ])
+])
diff --git a/drivers/gpu/drm/amd/dkms/m4/kernel.m4 b/drivers/gpu/drm/amd/dkms/m4/kernel.m4
index 28f6cecf6472..81f4e9e2015a 100644
--- a/drivers/gpu/drm/amd/dkms/m4/kernel.m4
+++ b/drivers/gpu/drm/amd/dkms/m4/kernel.m4
@@ -239,6 +239,7 @@ AC_DEFUN([AC_CONFIG_KERNEL], [
        AC_AMDGPU_SMCA_UMC_V2
        AC_AMDGPU_TOPOLOGY_NUM_CORES_PER_PACKAGE
        AC_AMDGPU_DRM_CRTC_VBLANK_CRTC
+       AC_AMDGPU_DRM_DP_ADD_PAYLOAD_PART2_THREE_ARGUMENTS

        AC_KERNEL_WAIT
        AS_IF([test "$LINUX_OBJ" != "$LINUX"], [
diff --git a/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h b/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h
index 9791910ed58b..a84cd2ac22cc 100644
--- a/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h
+++ b/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h
@@ -104,4 +104,17 @@ _kcl_drm_dp_mst_topology_mgr_resume(struct drm_dp_mst_topology_mgr *mgr,
 #define drm_dp_mst_topology_mgr_resume _kcl_drm_dp_mst_topology_mgr_resume
 #endif

+#ifdef HAVE_DRM_DP_ADD_PAYLOAD_PART2_THREE_ARGUMENTS
+static inline int
+_kcl_drm_dp_add_payload_part2(struct drm_dp_mst_topology_mgr *mgr,
+                             struct drm_dp_mst_atomic_payload *payload)
+{
+       struct drm_dp_mst_topology_state *mst_state;
+
+       mst_state = to_drm_dp_mst_topology_state(mgr->base.state);
+       return drm_dp_add_payload_part2(mgr, mst_state->base.state, payload);
+}
+#define drm_dp_add_payload_part2 _kcl_drm_dp_add_payload_part2
+#endif
+
 #endif
(END)
        AS_IF([test "$LINUX_OBJ" != "$LINUX"], [
diff --git a/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h b/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h
index 9791910ed58b..a84cd2ac22cc 100644
--- a/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h
+++ b/include/kcl/backport/kcl_drm_dp_mst_helper_backport.h
@@ -104,4 +104,17 @@ _kcl_drm_dp_mst_topology_mgr_resume(struct drm_dp_mst_topology_mgr *mgr,
 #define drm_dp_mst_topology_mgr_resume _kcl_drm_dp_mst_topology_mgr_resume
 #endif

+#ifdef HAVE_DRM_DP_ADD_PAYLOAD_PART2_THREE_ARGUMENTS
+static inline int
+_kcl_drm_dp_add_payload_part2(struct drm_dp_mst_topology_mgr *mgr,
+                             struct drm_dp_mst_atomic_payload *payload)
+{
+       struct drm_dp_mst_topology_state *mst_state;
+
+       mst_state = to_drm_dp_mst_topology_state(mgr->base.state);
+       return drm_dp_add_payload_part2(mgr, mst_state->base.state, payload);
+}
+#define drm_dp_add_payload_part2 _kcl_drm_dp_add_payload_part2
+#endif
+
 #endif

```
Again, this isn't 100% confirmed, it's not been fully validated/tested, and it's not an "AMD-approved solution". It's just a kernel dev (me) who found what the potential solution might be using a patch that would be used for a release, in theory. 

But it's a method to get you all unblocked until the fix gets released. You can definitely wait for the next release to include the fix, but this would hopefully get sufficient numbers of you all unblocked. 

Repeating myself, this is not an "AMD recommended solution". This is just from a guy who understands the issue and knows that getting unblocked is paramount for some/most people. This patch comes with no official AMD testing or support as of today. But if you want to try it out, it could get you around the issue. 

---

### 评论 #52 — ruvkr (2024-09-18T17:09:19Z)

I used `amdgpu-install` to install ROCm, HIP, etc., aiming to get HIP working with Blender, and occasionally for Stable Diffusion via ComfyUI. The process installed `amdgpu-dkms` along with other packages.

Today, I decided to uninstall everything:

```
amdgpu-install --uninstall
sudo apt autoremove amdgpu-install
```

After a reboot, I updated to Linux 6.8.0-45, then reinstalled `amdgpu-install` but only installed HIP without DKMS:

```
amdgpu-install --usecase=hip --no-dkms
```

Surprisingly, both HIP in Blender and ComfyUI are working, and I managed to free up 20-30GB of disk space. No clue how. Not sure if its related but I thought it might be helpful to someone.

---

### 评论 #53 — andyfutcher (2024-09-18T19:36:50Z)

Seems we will have to depend on the AMDGPU dev team for the permanent solution for both PRO/ROCm and desktop graphics users using DKMS feature; I have updated my original ticket on AMDs git issue tracker. [amdgpu-dkms fails compile with kernel 6.8.0-44 and -45](https://gitlab.freedesktop.org/drm/amd/-/issues/3628) 

---

### 评论 #54 — 38 (2024-09-18T23:57:41Z)

> > ****
> 
> Note at the bottom he has set the Ubuntu bug report to status: "Won't Fix".

I am seeing the same error, and I believe this is something they should fix.
The problem is they pick a 6.9 patch and applied to 6.8 which changes the API that causes the downstream fails. 
So frustrated about the Ubuntu team. What they should do is either revert the patch that causing the issue or provide 6.9 kernels. Unfortunately they are doing none of these solutions. 

---

### 评论 #55 — robertegj (2024-09-19T01:01:32Z)

> I used `amdgpu-install` to install ROCm, HIP, etc., aiming to get HIP working with Blender, and occasionally for Stable Diffusion via ComfyUI. The process installed `amdgpu-dkms` along with other packages.
> 
> Today, I decided to uninstall everything:
> 
> ```
> amdgpu-install --uninstall
> sudo apt autoremove amdgpu-install
> ```
> 
> After a reboot, I updated to Linux 6.8.0-45, then reinstalled `amdgpu-install` but only installed HIP without DKMS:
> 
> ```
> amdgpu-install --usecase=hip --no-dkms
> ```
> 
> Surprisingly, both HIP in Blender and ComfyUI are working, and I managed to free up 20-30GB of disk space. No clue how. Not sure if its related but I thought it might be helpful to someone.

Please someone test this, because that's exactly how I ended up here. While it's nice to have graphics and games working I want blender support - but removing 35.7 GB of disk space (on my system) scares me. Those packages seem important.

`The following packages will be REMOVED:
  amd-smi-lib* amdgpu-core* amdgpu-dkms* amdgpu-dkms-firmware* amdgpu-lib* amdgpu-lib32* comgr* composablekernel-dev* gst-omx-amdgpu* half*
  hip-dev* hip-doc* hip-runtime-amd* hip-samples* hipblas* hipblas-dev* hipblaslt* hipblaslt-dev* hipcc* hipcub-dev* hipfft* hipfft-dev*
  hipfort-dev* hipify-clang* hiprand* hiprand-dev* hipsolver* hipsolver-dev* hipsparse* hipsparse-dev* hipsparselt* hipsparselt-dev* hiptensor*
  hiptensor-dev* hsa-amd-aqlprofile* hsa-rocr* hsa-rocr-dev* hsakmt-roct-dev* libdrm-amdgpu-amdgpu1* libdrm-amdgpu-amdgpu1:i386*
  libdrm-amdgpu-common* libdrm-amdgpu-dev* libdrm-amdgpu-radeon1* libdrm-amdgpu-radeon1:i386* libdrm2-amdgpu* libdrm2-amdgpu:i386*
  libegl1-amdgpu-mesa* libegl1-amdgpu-mesa:i386* libegl1-amdgpu-mesa-drivers* libegl1-amdgpu-mesa-drivers:i386* libgbm1-amdgpu*
  libgbm1-amdgpu:i386* libgl1-amdgpu-mesa-dri* libgl1-amdgpu-mesa-dri:i386* libgl1-amdgpu-mesa-glx* libgl1-amdgpu-mesa-glx:i386*
  libglapi-amdgpu-mesa* libglapi-amdgpu-mesa:i386* libllvm18.1-amdgpu* libllvm18.1-amdgpu:i386* libwayland-amdgpu-client0*
  libwayland-amdgpu-client0:i386* libwayland-amdgpu-server0* libwayland-amdgpu-server0:i386* libxatracker2-amdgpu* libxatracker2-amdgpu:i386*
  mesa-amdgpu-omx-drivers* mesa-amdgpu-va-drivers* mesa-amdgpu-va-drivers:i386* mesa-amdgpu-vdpau-drivers* mesa-amdgpu-vdpau-drivers:i386*
  migraphx* migraphx-dev* miopen-hip* miopen-hip-dev* mivisionx* mivisionx-dev* openmp-extras-dev* openmp-extras-runtime* rccl* rccl-dev*
  rocalution* rocalution-dev* rocblas* rocblas-dev* rocdecode* rocdecode-dev* rocfft* rocfft-dev* rocm* rocm-cmake* rocm-core* rocm-dbgapi*
  rocm-debug-agent* rocm-developer-tools* rocm-device-libs* rocm-gdb* rocm-hip-libraries* rocm-hip-runtime* rocm-hip-runtime-dev* rocm-hip-sdk*
  rocm-language-runtime* rocm-llvm* rocm-ml-libraries* rocm-ml-sdk* rocm-opencl* rocm-opencl-dev* rocm-opencl-icd-loader* rocm-opencl-runtime*
  rocm-opencl-sdk* rocm-openmp-sdk* rocm-smi-lib* rocm-utils* rocminfo* rocprim-dev* rocprofiler* rocprofiler-dev* rocprofiler-plugins*
  rocprofiler-register* rocprofiler-sdk* rocprofiler-sdk-roctx* rocrand* rocrand-dev* rocsolver* rocsolver-dev* rocsparse* rocsparse-dev*
  rocthrust-dev* roctracer* roctracer-dev* rocwmma-dev* rpp* rpp-dev* xserver-xorg-amdgpu-video-amdgpu*
`

This is of course _after_ using the solution from https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351346975 to get back up in the first place

---

### 评论 #56 — Wedge009 (2024-09-19T01:09:01Z)

Interesting... looking through the [list of supported operating systems](https://rocm.docs.amd.com/en/docs-6.2.0/compatibility/compatibility-matrix.html), I was surprised to learn that of all of them, Ubuntu's kernel is the most recent. I was under the impression other distributions are more aggressive in its adoption of kernel releases. (And they probably are... outside the context of ROCm support.)

But I suppose it would make sense that of the distributions the ROCm devs would aim to support, they would choose ones that tend to be more conservative (for example, I didn't realise until today that RHEL took such a conservative approach to kernel support).

---

### 评论 #57 — robertegj (2024-09-19T15:04:57Z)

For anyone still struggling to get HIP features even after following https://github.com/ROCm/ROCm/issues/3701#issuecomment-2351346975 and getting amdgpu installed properly, do

`sudo usermod -a -G render,video $LOGNAME`
`reboot`

This was all I needed for blender to recognize my GPU. Shows up in HIP devices now.
Guess I just got tangled in this kernel update mess because I didn't try that step first.



---

### 评论 #58 — kentrussell (2024-09-20T17:38:51Z)

6.2.1 has this resolved. I just pushed the code out now, specifically:
https://github.com/ROCm/ROCK-Kernel-Driver/commit/2f767b98d4539164c9f1fcb930e4c8f329d586e6
Will close this off next week unless someone finds it to not be working properly

---

### 评论 #59 — nktice (2024-09-20T21:17:38Z)

> @kentrussell  "6.2.1 has this resolved. I just pushed the code out now, specifically: [ROCm/ROCK-Kernel-Driver@2f767b9](https://github.com/ROCm/ROCK-Kernel-Driver/commit/2f767b98d4539164c9f1fcb930e4c8f329d586e6) Will close this off next week unless someone finds it to not be working properly"

Do you know when we may see the new release up on AMD's site?  
https://repo.radeon.com/amdgpu/ 


---

### 评论 #60 — kentrussell (2024-09-20T21:24:37Z)

Should be soon. Just getting the deployment out across all components and repos and mirrors and such. 

---

### 评论 #61 — aphor (2024-09-21T01:29:23Z)

I ditched grub for [ZFSBootMenu](https://docs.zfsbootmenu.org/). I am so happy when I need to revert things like broken kernel. It makes testing this stuff so much easier. The old-school install process is always a pain, but so worth it.

https://docs.zfsbootmenu.org/en/v2.3.x/

---

### 评论 #62 — nktice (2024-09-21T04:44:23Z)

@kentrussell - Thank you for your work... please pass our thanks to the team for resolving this.  
I have re-installed using ROCm 6.2.1 - works as expected.  


---

### 评论 #63 — HardAndHeavy (2024-09-21T21:10:18Z)

I installed ROCm 6.2.1 - it works fine. But a couple of programs broke (Obsidian, browser...) with the error: ["Cannot find target for triple amdgcn-- Unable to find target for this triple (no targets are registered)"](https://github.com/signalapp/Signal-Desktop/issues/6855).

I fixed the error based on the [comment from SamuelMarks](https://github.com/signalapp/Signal-Desktop/issues/6855#issuecomment-2118305464):
```
sudo apt remove mesa-va-drivers
# Removes `va-driver-all` also
```
I did it like this:
```
sudo apt remove mesa-va-drivers
sudo apt remove mesa-amdgpu-va-drivers:amd64
```

---

### 评论 #64 — andyfutcher (2024-09-21T22:04:26Z)

Can confirm amdgpu dkms drivers from repo.radeon.com/amdgpu/6.2.1 now install on kernel 6.8.0-45 without error, system boots and the GPU works.

Just a reminder to anyone not used to linux, you will need to tell your distro to use these repositories to get the latest drivers, in my case I added the following to my sources and let the system apt upgrade do the rest;

```
deb https://repo.radeon.com/amdgpu/6.2.1/ubuntu jammy main 
deb https://repo.radeon.com/rocm/apt/6.2.1 jammy main
```

Or you could wait for the maintainers to update: https://www.amd.com/en/support/download/linux-drivers.html for your distro.

Big thank you amdgpu devs and maintainers! 

---

### 评论 #65 — GazaShaggy (2024-09-22T08:25:29Z)

@AndyFutcher Thanks for that I'm relatively new to linux and had to do this to get mine to work only difference was I have separate sources in the folder "/etc/apt/sources.list.d/" once I updated the "amdgpu.list" and "rocm.list" it updated perfectly.
Thanks to all who made this work

---

### 评论 #66 — EmilPosmyk (2024-09-22T15:24:46Z)

Hi all, what about Ubuntu 24.04.1 Noble .... Is this also fixed or will be in the next release of the amdgpu version ? I get the titled error (I use UM890 Pro - Mini PC where is Ryzen 9 and Radeon 780M - kernel 6.8.0-45).

I see something that there is in distros of amdgpu: https://repo.radeon.com/amdgpu/6.2.1/ubuntu/dists/
And here is deb installer: https://repo.radeon.com/amdgpu-install/latest/ubuntu/ but when I use Ubuntu Noble version I still get the error:

> Building module:
> Cleaning build area...(bad exit status: 2)
> . /tmp/amd.XkSbMRp1/.env && make -j16 KERNELRELEASE=6.8.0-45-generic TTM_NAME=amdttm SCHED_NAME=amd-sched -C /lib/modules/6.8.0-45-generic/build M=/tmp/amd.XkSbMRp1.................(bad exit status: 2)
> ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.crash'
> Error! Bad return status for module build on kernel: 6.8.0-45-generic (x86_64)
> Consult /var/lib/dkms/amdgpu/6.8.5-2009582.24.04/build/make.log for more information.
> dkms autoinstall on 6.8.0-45-generic/x86_64 failed for amdgpu(10)
> Error! One or more modules failed to install during autoinstall.
> Refer to previous errors for more information.
>  * dkms: autoinstall for kernel 6.8.0-45-generic
>    ...fail!
> run-parts: /etc/kernel/postinst.d/dkms exited with return code 11
> dpkg: error processing package linux-image-6.8.0-45-generic (--configure):
>  installed linux-image-6.8.0-45-generic package post-installation script subprocess returned error exit status 11
> Errors were encountered while processing:
>  linux-image-6.8.0-45-generic
> E: Sub-process /usr/bin/dpkg returned an error code (1)


Can you please let me know what is the current status of it ?

---

### 评论 #67 — Wedge009 (2024-09-22T18:11:35Z)

I think this is a separate issue, I wasn't aware ROCm was supported on iGPUs anyway. I haven't yet attempted updating beyond -41 kernel, but I'm closing this based on others' reports that this issue is resolved. Other issues should be tracked separately.

---

### 评论 #68 — splineai-cloud (2024-09-22T22:02:11Z)

Hi,

I've seen the Ubuntu22.04.05 with 6.8 new kernel fails for dkms.
The 
-----------------------------------------------------------------------------------------------------------
$uname -a
Linux deepllm 6.8.0-45-generic #45~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Sep 11 15:25:05 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
$ dkms status
Error! Could not locate dkms.conf file.
File: /var/lib/dkms/amdgpu/6.7.0-1787201.22.04/source/dkms.conf does not exist.
----------------------------------------------------------------------------------------------------------

I wonder if the fix was tested for Ubuntu22.04.05.

Thanks,
Syed Hussain




---

### 评论 #69 — kentrussell (2024-09-23T13:52:26Z)

@splineai-cloud dkms is VERY simple in its implementation. In its implementation if /var/lib/dkms/$MODULE/$VERSION exists, then it is automatically assumed to be a valid source tree, even if it's empty. Which is what would throw the error there. The approved flow for installing ROCm's DKMS package is to remove the old one first, then install the new one. Most people don't do that though, because upgrades SHOULD work. But dkms doesn't support upgrades very well.

TL;DR: Remove the /var/lib/dkms/amdgpu/6.7.0-1787201.22.04 folder, and you'll be good.

---

### 评论 #70 — Arakade (2024-09-24T13:37:21Z)

Does anyone know whether the Ubuntu Noble situation has changed yet since [EmilPosmyk](https://github.com/EmilPosmyk)'s post?

---

### 评论 #71 — kentrussell (2024-09-24T13:50:38Z)

@EmilPosmyk @Arakade Without the make.log, it's impossible to say. ROCm 6.2.1 fixes the issue on the newer Ubuntu kernels where drm_dp_add_payload_part2 had the wrong number of parameters. But Emil's issue could be that he has no compiler installed, without the make.log output it's impossible to say. But the problems above have been addressed in 6.2.1

---

### 评论 #72 — chrisaga (2024-09-24T13:53:58Z)

> Does anyone know whether the Ubuntu Noble situation has changed yet since [EmilPosmyk](https://github.com/EmilPosmyk)'s post?

I confirm I was able to upgrade to ROCm 6.2.1 via apt (I was still with kernel 6.8.0-44-generic), then upgrade to kernel 6.8.0-45-generic.
Both times dkms modules installed OK.


---

### 评论 #73 — EmilPosmyk (2024-09-24T20:09:50Z)

I just checked fresh [installation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/amdgpu-install.html) for Ubuntu 24.04 and everything works. Many thanks !

Wonder only if I installed default cases like graphics, opencl, hip, should I see drivers in Additional drivers (previously I used NVIDIA drivers on this OS) ? :-)
Seems there was no issue during the installation, but after I see only default mode: 1024x768 (sudo lshw -C display):

> *-display                 
       description: VGA compatible controller
       product: Phoenix3
       vendor: Advanced Micro Devices, Inc. [AMD/ATI]
       physical id: 0
       bus info: pci@0000:c4:00.0
       logical name: /dev/fb0
       version: c4
       width: 64 bits
       clock: 33MHz
       capabilities: pm pciexpress msi msix vga_controller bus_master cap_list fb
       configuration: depth=32 latency=0 mode=1024x768 visual=truecolor xres=1024 yres=768
       resources: iomemory:7c0-7bf memory:7c00000000-7c0fffffff memory:dc000000-dc1fffff ioport:d000(size=256) memory:dc500000-dc57ffff
  *-graphics
       product: simpledrmdrmfb
       physical id: 1
       logical name: /dev/fb0
       capabilities: fb
       configuration: depth=32 resolution=1024,768

Any toughs on this ?

---

### 评论 #74 — EmilPosmyk (2024-09-25T06:56:53Z)

I'll install fresh Ubuntu 24.04.1 to see if it's ok ...

* update, I've checked both approaches:
1) cloned disk with Ubuntu 24.04.1 where were NVIDIA drivers and when I simply boot it in the MiniForum UM890 device the Radeon 780M is detected and all drivers are initialized it seems without the need of installing them (it is seen in the system details in the Settings section) surprisingly. I have to admit I didn't know it will work in this way earlier :-)
Steam works after initializing Vulkan shaders automatically as well.

2) fresh Ubuntu 24.04.1 same, all works by default like 1)

Sorry for the confusion, I got used to Nvidia for long time and didn't know it works nicely with AMD Radeon :-)

Confusion also was because I expected some drivers to be seen in the Additional Drivers app in Ubuntu like Nvidia, but that is I guess not how it works with Radeon. Now it's clear. 

Thanks

---

### 评论 #75 — aphor (2024-09-28T00:50:12Z)

I had problems reinstalling the amdgpu-installer package from prior to this fix. I thought it just added the rocm apt repos+key, but I retried manually adding the key and repos, after I'd upgraded the kernel to 6.8.0-45-generic, and just installing the amdgpu-dkms package. This worked, and rocm installed also.

Just beware the amdgpu-installer seems to peg package versions.

---

### 评论 #76 — sonic182 (2024-10-01T10:07:26Z)


Following [this comment](https://github.com/ROCm/ROCm/issues/3701#issuecomment-2365335731), for ubuntu 22.04 you can download amdgpu-install 6.2.1 (or even newer 6.2.2)  in here -> https://repo.radeon.com/amdgpu-install/6.2.1/ubuntu/jammy/ 

`wget https://repo.radeon.com/amdgpu-install/6.2.1/ubuntu/jammy/amdgpu-install_6.2.60201-1_all.deb`

install the .deb and run `amdgpu-install` 

---

### 评论 #77 — sonic182 (2024-10-01T10:24:03Z)

I have found this page more up to date -> https://rocm.docs.amd.com/en/latest/ very well documented

---

### 评论 #78 — pmmalinov01 (2024-10-02T20:21:17Z)

Installing 6.2.60201 solved the issue for me

---

### 评论 #79 — ugcoder (2024-10-08T10:16:41Z)

yeah, my ubuntu version is 22.04, and 6.8.0.45 is KO, im use 6.8.0.40 right now!

---

### 评论 #80 — ruizdiazever (2024-10-08T10:22:50Z)

  Same problem here, with a RX 7900 XTX

---

### 评论 #81 — dandingdjianjiao (2024-10-10T09:50:54Z)

> I installed ROCm 6.2.1 - it works fine. But a couple of programs broke (Obsidian, browser...) with the error: ["Cannot find target for triple amdgcn-- Unable to find target for this triple (no targets are registered)"](https://github.com/signalapp/Signal-Desktop/issues/6855).
> 
> I fixed the error based on the [comment from SamuelMarks](https://github.com/signalapp/Signal-Desktop/issues/6855#issuecomment-2118305464):
> 
> ```
> sudo apt remove mesa-va-drivers
> # Removes `va-driver-all` also
> ```
> 
> I did it like this:
> 
> ```
> sudo apt remove mesa-va-drivers
> sudo apt remove mesa-amdgpu-va-drivers:amd64
> ```
if I remove this package, ROCm will also be removed. How can I solve this issue without this package removed?


---

### 评论 #82 — harkgill-amd (2024-10-11T14:32:47Z)

Hi @dandingdjianjiao, installing with the graphics use case should resolve this issue.
```
sudo amdgpu-install --usecase=graphics,rocm
```

---

### 评论 #83 — Delitants (2024-11-12T03:17:07Z)

> Following [this comment](https://github.com/ROCm/ROCm/issues/3701#issuecomment-2365335731), for ubuntu 22.04 you can download amdgpu-install 6.2.1 (or even newer 6.2.2) in here -> https://repo.radeon.com/amdgpu-install/6.2.1/ubuntu/jammy/
> 
> `wget https://repo.radeon.com/amdgpu-install/6.2.1/ubuntu/jammy/amdgpu-install_6.2.60201-1_all.deb`
> 
> install the .deb and run `amdgpu-install`

amdgpu-install
Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
Hit:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease                                          
Hit:3 https://repo.radeon.com/amdgpu/6.0.2/ubuntu jammy InRelease                                          
Hit:4 http://us.archive.ubuntu.com/ubuntu jammy-security InRelease                                         
Get:5 https://repo.radeon.com/rocm/apt/6.2.1 jammy InRelease [2,620 B]                                     
Hit:6 https://www.synaptics.com/sites/default/files/Ubuntu stable InRelease                                
Hit:7 https://ppa.launchpadcontent.net/b-rad/kernel+mediatree+hauppauge/ubuntu jammy InRelease             
Hit:8 https://ppa.launchpadcontent.net/oibaf/graphics-drivers/ubuntu jammy InRelease
Get:9 https://repo.radeon.com/rocm/apt/6.2.1 jammy/main amd64 Packages [96.2 kB]
Fetched 98.8 kB in 8s (13.1 kB/s)                                                                          
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
linux-headers-6.8.0-48-generic is already the newest version (6.8.0-48.48~22.04.1).
linux-headers-6.8.0-48-generic set to manually installed.
amdgpu-dkms is already the newest version (1:6.3.6.60002-1718217.22.04).
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 amdgpu-lib32 : Depends: libdrm2-amdgpu:i386 but it is not installable
                Depends: libdrm-amdgpu-amdgpu1:i386 but it is not installable
                Depends: libllvm-amdgpu:i386 but it is not installable
                Depends: libxatracker2-amdgpu:i386 but it is not installable
                Depends: libgbm1-amdgpu:i386 but it is not installable
                Depends: libegl1-amdgpu-mesa:i386 but it is not installable
                Depends: libegl1-amdgpu-mesa-drivers:i386 but it is not installable
                Depends: libglapi-amdgpu-mesa:i386 but it is not installable
                Depends: libgl1-amdgpu-mesa-glx:i386 but it is not installable
                Depends: libgl1-amdgpu-mesa-dri:i386 but it is not installable
                Depends: mesa-amdgpu-va-drivers:i386 but it is not installable
                Depends: mesa-amdgpu-vdpau-drivers:i386 but it is not installable
E: Unable to correct problems, you have held broken packages.


---

### 评论 #84 — Wedge009 (2024-11-12T05:11:49Z)

I think this is a separate issue. You're pulling in 32-bit packages for Jammy, although they seem to be available at https://repo.radeon.com/amdgpu/6.2.1/ubuntu/pool/main/libd/libdrm-amdgpu/. This particular issue is resolved, I suggest you submit a new issue for your problem if you're still having trouble.

---

### 评论 #85 — Delitants (2024-11-12T05:27:35Z)

> I think this is a separate issue. You're pulling in 32-bit packages for Jammy, although they seem to be available at https://repo.radeon.com/amdgpu/6.2.1/ubuntu/pool/main/libd/libdrm-amdgpu/. This particular issue is resolved, I suggest you submit a new issue for your problem if you're still having trouble.

I'm not pulling anything, I have installed a package as suggested and executed "amdgpu-install". Why there is 32 bit request I have no idea, system is 64 bit. Faulty kernel is 6.8.0-48, reverted to 6.8.0-44 and GPU works again.

---

### 评论 #86 — alexander-musienko (2025-11-06T09:36:56Z)

> I used `amdgpu-install` to install ROCm, HIP, etc., aiming to get HIP working with Blender, and occasionally for Stable Diffusion via ComfyUI. The process installed `amdgpu-dkms` along with other packages.
> 
> Today, I decided to uninstall everything:
> 
> ```
> amdgpu-install --uninstall
> sudo apt autoremove amdgpu-install
> ```
> 
> After a reboot, I updated to Linux 6.8.0-45, then reinstalled `amdgpu-install` but only installed HIP without DKMS:
> 
> ```
> amdgpu-install --usecase=hip --no-dkms
> ```
> 
> Surprisingly, both HIP in Blender and ComfyUI are working, and I managed to free up 20-30GB of disk space. No clue how. Not sure if its related but I thought it might be helpful to someone.

Thank you very much, i used to have problem with booting of my ubuntu 25 after installation of amd gpu drivers, your hint solved my problem



---
