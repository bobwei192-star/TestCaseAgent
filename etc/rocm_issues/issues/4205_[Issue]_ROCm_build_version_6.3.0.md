# [Issue]: ROCm build version 6.3.0 

> **Issue #4205**
> **状态**: closed
> **创建时间**: 2024-12-29T23:11:01Z
> **更新时间**: 2025-01-17T18:33:27Z
> **关闭时间**: 2025-01-17T18:33:25Z
> **作者**: rlee3030
> **标签**: Under Investigation, ROCm 6.3.0, GPU_ARCHS=gfx90a
> **URL**: https://github.com/ROCm/ROCm/issues/4205

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)
- **GPU_ARCHS=gfx90a** (颜色: #ededed)

## 描述

### Problem Description

Build issue found:   /src/out/ubuntu-22.04/22.04/logs/opencl_on_rocclr.errors on version 6.3.0

prerequisites script finished successfully but still having the error below.
Any ideas what this might be ???

```
-- Found AMD_OPENCL: /src/clr/opencl/khronos/headers/opencl2.2/CL
-- Found NUMA: /usr/lib/x86_64-linux-gnu/libnuma.so
-- Found OpenGL: /usr/lib/x86_64-linux-gnu/libOpenGL.so
--
ICD not found. Build may succeed if OpenCL ICD is installed in the system (missing: AMD_ICD_LIBRARY_DIR)
-- Found GLEW: /usr/include (found version "2.2.0")
--
ICD not found. Build may succeed if OpenCL ICD is installed in the system (missing: AMD_ICD_LIBRARY_DIR)
--
ICD not found. Build may succeed if OpenCL ICD is installed in the system (missing: AMD_ICD_LIBRARY_DIR)
--
ICD not found. Build may succeed if OpenCL ICD is installed in the system (missing: AMD_ICD_LIBRARY_DIR)
--
ICD not found. Build may succeed if OpenCL ICD is installed in the system (missing: AMD_ICD_LIBRARY_DIR)
^[[0mUsing CPACK_PACKAGE_VERSION 2.0.0.60300^[[0m
-- ROCM Installation path(ROCM_PATH): /opt/rocm-6.3.0
^[[0mUsing CPACK_DEBIAN_PACKAGE_RELEASE local.9999~22.04^[[0m
^[[0mUsing CPACK_RPM_PACKAGE_RELEASE local.9999^[[0m
^[[0mRESULT_VARIABLE 0 OUTPUT_VARIABLE: ^[[0m
-- Configuring done
^[[0mCMake Error: The following variables are used in this project, but they are set to NOTFOUND.
Please set them or make sure they are set and tested correctly in the CMake files:
```

### Operating System

Ubuntu 22.04.5 LTS 

### CPU

AMD EPYC 7742 64-Core Processor

### GPU

GPU_ARCHS=gfx90a  

### ROCm Version

ROCm 6.3.0

### ROCm Component

clr

### Steps to Reproduce

Installed on AMD Server, with Ubuntu 22.04.5 LTS
Linux msl-ssg-dgx2.msl.lab 5.15.0-127-generic #137-Ubuntu SMP Fri Nov 8 15:21:01 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
Followed the ROCm install instructions.
Using docker instructions to build the source code.

Note: I do not have a AMD GPU in this server right now.  This is a test environment to try to build the code.
The AMD GPU is in another server which is being brought up now and will be available shortly.
Not sure if AMD GPU presence is required for this software build ?

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is NOT loaded, possibly no GPU devices



### Additional Information

Let me know if more debug information is needed.

---

## 评论 (7 条)

### 评论 #1 — ppanchad-amd (2024-12-30T15:03:37Z)

Hi @rlee3030. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — darren-amd (2024-12-30T21:13:54Z)

Hi @rlee3030,

Thanks for reporting the issue. Currently the documentation for installation has a few errors, namely `ROCM_VERSION=6.3.1` does not have the corresponding build manifest and should instead point to `ROCM_VERSION=6.3.0` , as well as changing the docker image to pull the correct version: `docker pull rocm/rocm-build-ubuntu-22.04:6.2` should be `docker pull rocm/rocm-build-ubuntu-22.04:6.3`. There is currently a PR to fix the documentation here: https://github.com/ROCm/ROCm/pull/4207 that includes the updated instructions. The highlighted build issue was fixed with these changes.

However, I am currently encountering some other build issues, which I am investigating further.

Also, is there a particular reason you are building ROCm from source? It could be easier to follow the installation instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html).



---

### 评论 #3 — rlee3030 (2024-12-30T23:32:15Z)

Thanks for the quick response.  I will try your suggestion below. Best Regards RonSent from my iPhoneOn Dec 30, 2024, at 1:14 PM, darren-amd ***@***.***> wrote:﻿
Hi @rlee3030,
Thanks for reporting the issue. Currently the documentation for installation has a few errors, namely ROCM_VERSION=6.3.1 does not have the corresponding build manifest and should instead point to ROCM_VERSION=6.3.0 , as well as changing the docker image to pull the correct version: docker pull rocm/rocm-build-ubuntu-22.04:6.2 should be docker pull rocm/rocm-build-ubuntu-22.04:6.3. There is currently a PR to fix the documentation here: #4207 that includes the updated instructions.
I was able to build rocm-dev without any issues by following those instructions. Could you give that a try and let me know if you run into any issues building rocm-dev? Thanks!

—Reply to this email directly, view it on GitHub, or unsubscribe.You are receiving this because you were mentioned.Message ID: ***@***.***>

---

### 评论 #4 — darren-amd (2024-12-31T21:00:22Z)

Sounds good! 

The build issues I encountered were due to the processes being killed due to running out of RAM. Switching to a beefier system allowed the components to build successfully. It did however take a long time, so I still recommend not building from source and instead using the instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html). Please give it a try and let me know if you run into any issues.

---

### 评论 #5 — rlee3030 (2025-01-06T05:00:39Z)

Thanks for help. I was able to build it with your suggestions. I will try deploying it and see if everything is working. Does it help to set the GPU_ARCHS to reduce build time ?Mine is gfx90a Sent from my iPhoneOn Dec 31, 2024, at 1:00 PM, darren-amd ***@***.***> wrote:﻿
Sounds good!
The build issues I encountered were due to the processes being killed due to running out of RAM. Switching to a beefier system allowed the components to build successfully. It did however take a long time, so I still recommend not building from source and instead using the instructions here. Let me know if you run into any issues.

—Reply to this email directly, view it on GitHub, or unsubscribe.You are receiving this because you were mentioned.Message ID: ***@***.***>

---

### 评论 #6 — darren-amd (2025-01-06T14:31:22Z)

Awesome, yes building with GPU_ARCHS="gfx90a" should improve build time by limiting the architectures it builds for. 

---

### 评论 #7 — darren-amd (2025-01-17T18:33:25Z)

I'm going to close this ticket, but please feel free to create another if you running into any further build issues, thanks!

---
