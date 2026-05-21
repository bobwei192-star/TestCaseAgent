# [Issue]: OpenCL Vendor detection in Multi ROCm broken

> **Issue #5977**
> **状态**: open
> **创建时间**: 2026-02-18T08:20:06Z
> **更新时间**: 2026-03-04T15:15:53Z
> **作者**: alexschroeter
> **标签**: ROCm 6.2.4, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5977

## 标签

- **ROCm 6.2.4** (颜色: #ededed)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Hi, it seems that something in the way OpenCL is handled changed at some point. We have a dual ROCm installation with 7.2.0 and 6.2.4 but detection of GPU devices is not consistent.

I would expect:
a) both versions to handle the same
b) Especially not showing up or showing up as two platforms seems broken

### Operating System

Alma 9.7

### CPU

Irelevant

### GPU

Irelevant

### ROCm Version

7.2.0, 6.2.4

### ROCm Component

_No response_

### Steps to Reproduce

Create a multi ROCm (6.2.4 and 7.2.0 in our case) installation.

Run
```
module purge
module load rocm/6.2.4
clinfo
```
All GPUs show up 8+2.
This behaviour, although correct, is very strange to me because the /etc/ld.so.conf.d that tells the system where to look for the libamdocl is not there. So it shouldn't know where to look at all, or is it looking according to some ROCM_PATH variable?

Run
```
module purge
module load rocm/7.2.0
clinfo
```

No GPU devices show up only CPUs 2.

I have a couple of thoughts on the reason for this.
- The order of installation might have an impact
- Package dependencies between the two versions might have changed so we are missing a "important package" in the 7.2.0 installation.
- **The `rocm-opencl-icd-loader`doesn't exist for 7.2.0 and sounds to me like it could do what is not happening for 7.2.0** 
- In the past there used to be a rocm file in /etc/ld.so.conf.d which defined the path to look for the libamdocl...so (It is not present in our installation)
- When exporting LD_LIBRARY_PATH to include /opt/rocm-<version>/lib in the modulefile for 7.2.0 the GPUs are detected twice. Which I believe might have to do with both rocm versions being in /etc/OpenCL/vendors

```
ls -l /etc/OpenCL/vendors/
total 12
-rw-r--r--. 1 root root 15 Feb 17 11:50 amdocl64_60204_139.icd
-rw-r--r--. 1 root root 15 Jan 10 01:36 amdocl64_70200_43.icd
-rw-r--r--  1 root root 18 Feb 17 18:11 pocl.icd


module load rocm/7.2.0
LD_LIBRARY_PATH=/opt/rocm-7.2.0 clinfo
Number of platforms:                             3
...
```
Which, by the way, doesn't happen in 6.2.4 (maybe due to some version check or because it simply works differently).

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — the16bitgamer (2026-02-18T17:56:35Z)

I am seeing a similar issue with 7.2 here is the clinfo output on my machine.

Number of platforms                               1
  Platform Name                                   AMD Accelerated Parallel Processing
  Platform Vendor                                 Advanced Micro Devices, Inc.
  Platform Version                                OpenCL 2.1 AMD-APP (3581.0)
  Platform Profile                                FULL_PROFILE
  Platform Extensions                             cl_khr_icd cl_amd_event_callback 
  Platform Extensions function suffix             AMD
  Platform Host timer resolution                  1ns

  Platform Name                                   AMD Accelerated Parallel Processing
Number of devices                                 1
  Device Name                                     gfx1103
  Device Vendor                                   Advanced Micro Devices, Inc.
  Device Vendor ID                                0x1002
  Device Version                                  OpenCL 2.0 
  Driver Version                                  3581.0 (HSA1.1,LC)
  Device OpenCL C Version                         OpenCL C 2.0 
  Device Type                                     GPU
  Device Board Name (AMD)                         AMD Radeon Graphics
  Device PCI-e ID (AMD)                           0x15bf
  Device Topology (AMD)                           PCI-E, 0000:ffffffc1:00.0
  Device Profile                                  FULL_PROFILE
  Device Available                                Yes
  Compiler Available                              Yes
  Linker Available                                Yes
  Max compute units                               4
  SIMD per compute unit (AMD)                     4
  SIMD width (AMD)                                32
  SIMD instruction width (AMD)                    1
  Max clock frequency                             2599MHz
  Graphics IP (AMD)                               11.0
  Device Partition                                (core)
    Max number of sub-devices                     4
    Supported partition types                     None
    Supported affinity domains                    (n/a)
  Max work item dimensions                        3
  Max work item sizes                             1024x1024x1024
  Max work group size                             256
  Preferred work group size (AMD)                 256
  Max work group size (AMD)                       1024
Memory access fault by GPU node-1 (Agent handle: 0x5a020e3bce10) on address 0x7f86a34eb000. Reason: Page not present or supervisor privilege.
Aborted (core dumped)


---

### 评论 #2 — alexschroeter (2026-02-19T09:19:57Z)

> I am seeing a similar issue with 7.2 here is the clinfo output on my machine.
> 
> Number of platforms 1 Platform Name AMD Accelerated Parallel Processing Platform Vendor Advanced Micro Devices, Inc. Platform Version OpenCL 2.1 AMD-APP (3581.0) Platform Profile FULL_PROFILE Platform Extensions cl_khr_icd cl_amd_event_callback Platform Extensions function suffix AMD Platform Host timer resolution 1ns
> 
> Platform Name AMD Accelerated Parallel Processing Number of devices 1 Device Name gfx1103 Device Vendor Advanced Micro Devices, Inc. Device Vendor ID 0x1002 Device Version OpenCL 2.0 Driver Version 3581.0 (HSA1.1,LC) Device OpenCL C Version OpenCL C 2.0 Device Type GPU Device Board Name (AMD) AMD Radeon Graphics Device PCI-e ID (AMD) 0x15bf Device Topology (AMD) PCI-E, 0000:ffffffc1:00.0 Device Profile FULL_PROFILE Device Available Yes Compiler Available Yes Linker Available Yes Max compute units 4 SIMD per compute unit (AMD) 4 SIMD width (AMD) 32 SIMD instruction width (AMD) 1 Max clock frequency 2599MHz Graphics IP (AMD) 11.0 Device Partition (core) Max number of sub-devices 4 Supported partition types None Supported affinity domains (n/a) Max work item dimensions 3 Max work item sizes 1024x1024x1024 Max work group size 256 Preferred work group size (AMD) 256 Max work group size (AMD) 1024 Memory access fault by GPU node-1 (Agent handle: 0x5a020e3bce10) on address 0x7f86a34eb000. Reason: Page not present or supervisor privilege. Aborted (core dumped)

Hi @the16bitgamer, I believe our two issues are unrelated. It sounds like you are trying to use an iGPU, which, if I understand correctly, is not officially supported. I read some reports that forcing the GPU to be recognized as a gfx1100 with `export HSA_OVERRIDE_GFX_VERSION=11.0.0` worked for some people, but you should probably open a separate issue.

---

### 评论 #3 — the16bitgamer (2026-02-19T13:27:25Z)

@alexschroeter will do

---

### 评论 #4 — harkgill-amd (2026-02-20T16:35:57Z)

Hey @alexschroeter, thanks for the report.

I've seen similar issues with `clinfo` in the past when the linker can't find ROCm libraries - the steps [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/post-install.html#configure-rocm-shared-objects) would usually help resolve this. In your Multi-ROCm installation, that step would look more like, 
```
sudo tee --append /etc/ld.so.conf.d/rocm.conf <<EOF
/opt/rocm-6.2.4/lib
/opt/rocm-6.2.4/lib64
/opt/rocm-7.2.0/lib
/opt/rocm-7.2.0/lib64
EOF
sudo ldconfig
```
This worked on my end with `clinfo` correctly displaying GPUs with both 6.2.4 and 7.2.0 modules. If this does resolve the issue on your end as well, we can update the [muti-version post-install steps](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/multi-version-install/multi-version-install-ubuntu.html#post-installation) to better document this.

---

### 评论 #5 — alexschroeter (2026-02-23T13:43:01Z)

Hi @harkgill-amd,

yes this works but it is not what one would expect. Let me clarify.

When I run module load rocm/<a version> I would expect the appropriate OpenCL library to be loaded. But your solution is loading all that can be found.

By setting the /etc/ld.so.conf.d/rocm.conf as you suggest the clinfo will list all the OpenCL vendor libraries it can find. Which in my case (multi-rocm install with 7.2.0 and 6.2.4) will be those for 7.2.0 and 6.2.4, this returns 2 (3 with pocl) vendors where it should only be 1 (or 2 if we include pocl). Making the selection mechanism of module load useless.

To make this work as expected, only the specific rocm version of the opencl library should be found. 

---

### 评论 #6 — harkgill-amd (2026-02-23T20:24:02Z)

Ah yes I missed that - thanks for the clarification.

For the first half of your issue (failure to find correct libs resulting in empty clinfo output), we should be able to bake in the following into the module files,
```
prepend-path LD_LIBRARY_PATH "${ROOT}/lib:${ROOT}/lib64
```
or in the case of older modules such as rocm/6.2.4 that don't use the ROOT variable
```
prepend-path LD_LIBRARY_PATH "/opt/rocm-6.2.4/lib:/opt/rocm-6.2.4/lib64"
```
This will keep the module specific behaviour while ensuring the appropriate libraries are found. Having done this, we still run into the duplicate GPU entries issue that you mentioned earlier where rocm/7.2.0 clinfo outputs 2x the # of expected entries. Pointing `OCL_ICD_VENDORS` to the correlated `.icd` in each module file does resolve the issue but I'm not sure if this is a valid approach as we'd be missing out on other vendor libraries. Will bring this up internally and get back to you but feel free to give this a try and share any feedback as we scope this out.

---

### 评论 #7 — alexschroeter (2026-02-24T09:05:34Z)

Our workaround at the moment is a version specific directory with the libs that get passed into the `OCL_ICD_VENDORS` environment variable but this is not a viable solution.

What would make most sense to me (and I don't know if this would work and/or doesn't create problems somewhere else) is if the icd files in `/etc/OpenCL/vendors`
would not link to the generic but the version specific libs (which are already there).

## So instead of this:
``` 
ls -l /etc/OpenCL/vendors/
total 8
-rw-r--r--. 1 root root 15 Feb 23 10:37 amdocl64_60204_139.icd
-rw-r--r--. 1 root root 15 Jan 10 01:36 amdocl64_70200_43.icd
```

```
cat /etc/OpenCL/vendors/*
libamdocl64.so
libamdocl64.so
```

```
ls /opt/rocm-7.2.0/lib/libamdocl64.so* -l
lrwxrwxrwx. 1 root root      16 Jan 10 01:36 /opt/rocm-7.2.0/lib/libamdocl64.so -> libamdocl64.so.2
lrwxrwxrwx. 1 root root      24 Jan 10 01:36 /opt/rocm-7.2.0/lib/libamdocl64.so.2 -> libamdocl64.so.2.1.70200
-rwxr-xr-x. 1 root root 1406256 Jan 10 01:36 /opt/rocm-7.2.0/lib/libamdocl64.so.2.1.70200
ls /opt/rocm-6.2.4/lib/libamdocl64.so* -l
lrwxrwxrwx. 1 root root      16 Oct 29  2024 /opt/rocm-6.2.4/lib/libamdocl64.so -> libamdocl64.so.2
lrwxrwxrwx. 1 root root      24 Oct 29  2024 /opt/rocm-6.2.4/lib/libamdocl64.so.2 -> libamdocl64.so.2.1.60204
-rwxr-xr-x. 1 root root 1643664 Oct 29  2024 /opt/rocm-6.2.4/lib/libamdocl64.so.2.1.60204
```

## It probably should be this:
``` 
ls -l /etc/OpenCL/vendors/
total 8
-rw-r--r--. 1 root root 15 Feb 23 10:37 amdocl64_60204_139.icd
-rw-r--r--. 1 root root 15 Jan 10 01:36 amdocl64_70200_43.icd
```

```
cat /etc/OpenCL/vendors/*
libamdocl64.so.2.1.60204
libamdocl64.so.2.1.70200
```

```
ls /opt/rocm-7.2.0/lib/libamdocl64.so* -l
lrwxrwxrwx. 1 root root      16 Jan 10 01:36 /opt/rocm-7.2.0/lib/libamdocl64.so -> libamdocl64.so.2
lrwxrwxrwx. 1 root root      24 Jan 10 01:36 /opt/rocm-7.2.0/lib/libamdocl64.so.2 -> libamdocl64.so.2.1.70200
-rwxr-xr-x. 1 root root 1406256 Jan 10 01:36 /opt/rocm-7.2.0/lib/libamdocl64.so.2.1.70200
ls /opt/rocm-6.2.4/lib/libamdocl64.so* -l
lrwxrwxrwx. 1 root root      16 Oct 29  2024 /opt/rocm-6.2.4/lib/libamdocl64.so -> libamdocl64.so.2
lrwxrwxrwx. 1 root root      24 Oct 29  2024 /opt/rocm-6.2.4/lib/libamdocl64.so.2 -> libamdocl64.so.2.1.60204
-rwxr-xr-x. 1 root root 1643664 Oct 29  2024 /opt/rocm-6.2.4/lib/libamdocl64.so.2.1.60204
```

This way, if there isn't something that I am missing, setting the ROCM-Version specific LD_LIBRARY_PATH (i.e. /opt/rocm-6.2.4/lib) would only find the library that is actually in the path. Of course this assumes that `/etc/ld.so.conf.d/rocm.conf` doesn't exist.

---
