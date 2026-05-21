# [Issue]: ROCm fails with "GPU node has unrecognized id" error when AOCC compiler environment is sourced

> **Issue #6233**
> **状态**: open
> **创建时间**: 2026-05-12T08:54:00Z
> **更新时间**: 2026-05-13T15:03:44Z
> **作者**: Mamoru-Yuasa
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6233

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description


## Problem Description
When sourcing `/opt/AMD/aocc-compiler-5.1.0/setenv_AOCC.sh`, the `rocminfo` command fails with the following errors:

```
$rocminfo
ROCk module version 6.16.13 is loaded
Warning: Agent creation failed.
The GPU node has an unrecognized id.

hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:299
Call returned HSA_STATUS_ERROR_INVALID_ARGUMENT: One of the actual arguments does not meet a precondition stated in the documentation of the corresponding formal argument.
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:1337
Call returned HSA_STATUS_ERROR_INVALID_ARGUMENT: One of the actual arguments does not meet a precondition stated in the documentation of the corresponding formal argument.
```




### Operating System

Ubuntu 24.04.4 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 9950X3D 16-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 7.2.1

### ROCm Component

_No response_

### Steps to Reproduce

## Steps to Reproduce

1. Download and install AOCC 5.1.0 (`aocc-compiler-5.1.0_1_amd64.deb`) from:

https://www.amd.com/en/developer/aocc.html

2. Install Radeon Software for Linux / ROCm by following:

https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html

3. Source the AOCC environment:

```bash
source <compdir>/setenv_AOCC.sh
```

4. Run:

```bash
rocminfo
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.16.13 is loaded
Warning: Agent creation failed.
The GPU node has an unrecognized id.

hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:299
Call returned HSA_STATUS_ERROR_INVALID_ARGUMENT: One of the actual arguments does not meet a precondition stated in the documentation of the corresponding formal argument.
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:1337
Call returned HSA_STATUS_ERROR_INVALID_ARGUMENT: One of the actual arguments does not meet a precondition stated in the documentation of the corresponding formal argument.

### Additional Information

### Workaround
Remove `source /opt/AMD/aocc-compiler-5.1.0/setenv_AOCC.sh` from `.bashrc`. 

Instead, manage the AOCC compiler environment through a module system (e.g., `module` or `spack`) when it is actually needed for compilation. This prevents environment variable conflicts between ROCm and AOCC during normal runtime operations.

### Root Cause Analysis
There appears to be an environment variable conflict or incompatibility when AOCC's setup script is sourced globally via `.bashrc`. It is recommended to use separate environment management systems for ROCm binaries and AOCC compiler to avoid variable collisions.normal runtime operations.

