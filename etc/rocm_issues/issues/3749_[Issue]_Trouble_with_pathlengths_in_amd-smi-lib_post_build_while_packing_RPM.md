# [Issue]: Trouble with pathlengths in amd-smi-lib post build while packing RPM

> **Issue #3749**
> **状态**: closed
> **创建时间**: 2024-09-18T16:52:08Z
> **更新时间**: 2024-09-19T18:55:35Z
> **关闭时间**: 2024-09-19T18:55:35Z
> **作者**: jdumke
> **标签**: AMD Radeon Pro W6800, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3749

## 标签

- **AMD Radeon Pro W6800** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

While packing the RPM  for amd_smi_lib rpmbuild encounters trouble with unfitting pathlengts (see below).

My GPU, I want to build for is a:  AMD Radeon Pro WX 5100 Graphics

### Operating System

Debian 12 Bookworm with Backports

### CPU

AMD Ryzen 5 5600G with Radeon Graphics

### GPU

AMD Radeon Pro W6800

### ROCm Version

ROCm 6.2.0

### ROCm Component

amdsmi

### Steps to Reproduce

vanilla build of ROCm 6.2.0 like described in README.md for ROCm.git
local settings: export GPU_ARCHS="gfx803;gfx90c"

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

[all fine, until …]
CPack: Create package using RPM
CPack: Install projects
CPack: - Run preinstall target for: amd_smi_libraries
CPack: - Install project: amd_smi_libraries []
CPack: -   Install component: dev
CPack: -   Install component: tests
CPack: Create package
CMake Warning (dev) at /usr/share/cmake-3.30/Modules/Internal/CPack/CPackRPM.cmake:1130 (message):
  CPackRPM:Warning: SUGGESTS not supported in provided rpmbuild.  Tag will
  not be used.
Call Stack (most recent call first):
  /usr/share/cmake-3.30/Modules/Internal/CPack/CPackRPM.cmake:1986 (cpack_rpm_generate_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Error at /usr/share/cmake-3.30/Modules/Internal/CPack/CPackRPM.cmake:676 (message):
  CPackRPM: source dir path '/home/builder/devel/amd/rocm-6.2/amdsmi' is
  shorter than debuginfo sources dir path
  '/usr/src/debug/amd-smi-lib-24.6.0.60200-Linux/runtime/src_0'! Source dir
  path must be longer than debuginfo sources dir path.  Set
  CPACK_RPM_BUILD_SOURCE_DIRS_PREFIX variable to a shorter value or make
  source dir path longer.  Required for debuginfo packaging.  See
  documentation of CPACK_RPM_DEBUGINFO_PACKAGE variable for details.
Call Stack (most recent call first):
  /usr/share/cmake-3.30/Modules/Internal/CPack/CPackRPM.cmake:1484 (cpack_rpm_debugsymbol_check)
  /usr/share/cmake-3.30/Modules/Internal/CPack/CPackRPM.cmake:1986 (cpack_rpm_generate_package)


CPack Error: Error while execution CPackRPM.cmake
CPack Error: Error while execution CPackRPM.cmake
CPack Error: Problem compressing the directory
CPack Error: Error when generating package: amd-smi-lib
gmake[1]: *** [Makefile:74: package] Error 1
gmake[1]: Leaving directory '/home/builder/devel/amd/rocm-6.2/out/debian-12/12/build/amdsmi'


real	1m2.994s
user	3m10.793s
sys	0m17.615s
+ mv /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/amd_smi_lib.inprogress /home/builder/devel/amd/rocm-6.2/out/debian-12/12/logs/amd_smi_lib.errors
+ echo Error in amd_smi_lib
Error in amd_smi_lib
+ exit 1

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-09-19T18:55:35Z)

Hi @jdumke, this likely has the same root cause as what's being investigated in https://github.com/ROCm/ROCm/issues/3743 
and https://github.com/ROCm/ROCm/issues/3743#issuecomment-2361114653. 

Could you please try to build ROCm 6.2.0 in an Ubuntu docker container and let us know if the path errors are resolved. Let's continue to use the other ticket for correspondence.

---
