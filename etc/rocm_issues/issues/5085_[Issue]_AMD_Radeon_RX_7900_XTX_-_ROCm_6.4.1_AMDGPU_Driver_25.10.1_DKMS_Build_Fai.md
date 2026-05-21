# [Issue]: AMD Radeon RX 7900 XTX - ROCm 6.4.1 / AMDGPU Driver 25.10.1 DKMS Build Fails on Ubuntu 24.04.2 LTS (Kernel 6.14.0-24-generic) due to API Mismatches

> **Issue #5085**
> **状态**: closed
> **创建时间**: 2025-07-22T16:35:50Z
> **更新时间**: 2025-07-25T18:08:34Z
> **关闭时间**: 2025-07-25T18:08:34Z
> **作者**: cisnerosjo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5085

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am unable to successfully install the AMDGPU driver and ROCm 6.4.1 for my AMD Radeon RX 7900 XTX on Ubuntu 24.04.2 LTS. Despite following official AMD installation instructions and even attempting to use an officially supported kernel version for 24.04.2, the amdgpu-dkms module consistently fails to build, preventing the ROCm software stack from functioning.

Specific Errors Encountered (from sudo amdgpu-install -y --usecase=graphics,rocm):

The installation fails during the configuration of the amdgpu-dkms package. The system reports:

Errors were encountered while processing:
amd/amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)
The dkms build log, located at /var/lib/dkms/amdgpu/6.12.12-2164967.24.04/build/make.log, clearly indicates that the build is targeting the 6.14.0-24-generic kernel headers and encountering kernel API incompatibilities:

DKMS make.log for amdgpu-6.12.12-2164967.24.04 for kernel 6.14.0-24-generic (x86_64)
...
amd/amdgpu/amdgpu_drv.c:2416:25: error: implicit declaration of function ‘drm_fbdev_ttm_setup’ [-Werror=implicit-function-declaration]
  2416 |                                   drm_fbdev_ttm_setup(adev_to_drm(adev), 8);
       |                                   ^~~~~~~~~~~~~~~~~~~
...
amd/amdgpu/amdgpu_drv.c:3064:10: error: ‘struct drm_driver’ has no member named ‘date’
  3064 |           .date = DRIVER_DATE,
       |           ^~~~
...
amd/amdgpu/amdgpu_drv.h:43:33: error: initializer element is not computable at load time
   43 | #define DRIVER_DATE                     "20150101"
      |                                         ^~~~~~~~~~
amd/amdgpu/amdgpu_drv.c:3064:17: note: in expansion of macro ‘DRIVER_DATE’
  3064 |           .date = DRIVER_DATE,
       |                   ^~~~~~~~~~~
...
amd/amdgpu/amdgpu_drv.c:3098:10: error: ‘const struct drm_driver’ has no member named ‘date’
  3098 |           .date = DRIVER_DATE,
       |           ^~~~
These errors specifically point to changes in kernel API structures (like struct drm_driver no longer having a date member) and function availability (drm_fbdev_ttm_setup) in the 6.14 kernel compared to what the amdgpu driver expects.

ROCm Not Initialized / rocminfo Executable Missing:

Following the amdgpu-dkms failure, ROCm utilities are non-functional:

/opt/rocm/bin/rocminfo output: bash: /opt/rocm/bin/rocminfo: No such file or directory

/opt/rocm/bin/rocm-smi output: ROCk module is NOT loaded, possibly no GPU devices and ERROR:root:Driver not initialized (amdgpu not found in modules)

This indicates that critical ROCm components, including rocminfo, are not installed or are not initialized correctly due to the underlying driver failure.

Troubleshooting Steps Already Taken:

Followed AMD's official installation instructions for the specific driver and OS version.

Confirmed Secure Boot disabled in BIOS.

Ensured kernel headers (linux-headers-$(uname -r)) and build-essential dkms are installed and up-to-date.

Attempted to boot into the officially supported 6.11 HWE kernel (6.11.0-29-generic) for Ubuntu 24.04.2 LTS, as per ROCm 6.4.x documentation. (The amdgpu-dkms build, however, still targets the 6.14.0-24-generic kernel headers because they are present on the system, leading to the same compilation errors).

Performed full purges (sudo apt purge amdgpu* rocm* -y, sudo apt autoremove --purge -y, sudo apt clean) and reboots between attempts to ensure a clean state.

Reinstalled the amdgpu-install .deb package to ensure the command was available.

Attempted direct ROCm repository installation (rocm-libs) as a workaround, which installed user-space components but failed to make ROCm functional due to the missing rocminfo binary and underlying driver initialization issues.

Impact:

Due to these consistent driver compilation failures and ROCm initialization issues, my AMD Radeon RX 7900 XTX GPU cannot be utilized for local LLM acceleration and other compute tasks.

Request:

Could you please investigate this critical kernel module compatibility issue between the ROCm 6.4.1/AMDGPU 25.10.1 driver and the Ubuntu 24.04.2 LTS HWE kernels (specifically 6.14.0-24-generic, which is causing the DKMS build to fail)? An updated amdgpu-dkms package that correctly compiles against these newer kernel versions is urgently needed.

### Operating System

Ubuntu 24.04.2 LTS

### CPU

12th Gen Intel® Core™ i9-12900KF × 24

### GPU

AMD Radeon RX 7900 XTX (Navi 31)

### ROCm Version

ROCm 6.4.1 (from amdgpu-install_6.4.60401-1_all.deb)

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — dtl131 (2025-07-22T16:52:09Z)

You need ROCm 6.4.2 (just released) for 6.14 kernel support: https://github.com/ROCm/ROCm/issues/4619

---

### 评论 #2 — harkgill-amd (2025-07-25T18:08:34Z)

@cisnerosjo as @dtl131 mentioned ROCm 6.4.2 introduces 6.14 kernel support which should resolve the dkms build errors.

Will close this issue out as it was already tracked in the aforementioned ticket. If you are still encountering errors after upgrading to ROCm 6.4.2, please leave a comment and I'll reopen this issue for investigation. Thanks!

---
