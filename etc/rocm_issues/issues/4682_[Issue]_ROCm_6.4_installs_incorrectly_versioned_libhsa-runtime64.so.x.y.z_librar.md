# [Issue]: ROCm 6.4 installs incorrectly versioned libhsa-runtime64.so.x.y.z library on WSL2-based Ubuntu 24.04 systems

> **Issue #4682**
> **状态**: closed
> **创建时间**: 2025-04-24T18:26:54Z
> **更新时间**: 2025-06-05T18:04:47Z
> **关闭时间**: 2025-06-05T18:04:46Z
> **作者**: sbates130272
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4682

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

The version number on the libhsa-runtime63.so.x.y.z is incorrect on WSL2-based installs of ROCm 6.4.0 on Ubuntu 24.04.

### Operating System

Windows 11 with WSL2-based Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics

### GPU

N/A

### ROCm Version

ROCm 6.4.0

### ROCm Component

ROCR-Runtime

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
$ sudo amdgpu-install --no-dkms --no-32 --usecase=rocm
...
$ dpkg -L hsa-runtime-rocr4wsl-amdgpu
/.
/opt
/opt/rocm-6.4.0
/opt/rocm-6.4.0/lib
/opt/rocm-6.4.0/lib/libhsa-runtime64.so.1.14.0
/usr
/usr/share
/usr/share/doc
/usr/share/doc/hsa-runtime-rocr4wsl-amdgpu
/usr/share/doc/hsa-runtime-rocr4wsl-amdgpu/changelog.Debian.gz
/usr/share/doc/hsa-runtime-rocr4wsl-amdgpu/copyright
/opt/rocm-6.4.0/lib/libhsa-runtime64.so
/opt/rocm-6.4.0/lib/libhsa-runtime64.so.1
```
Note that the versioning on ```/opt/rocm-6.4.0/lib/libhsa-runtime64.so.1.14.0``` is incorrest. It should be ```/opt/rocm-6.4.0/lib/libhsa-runtime64.so.1.15.60400```.


### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — sbates130272 (2025-04-24T19:12:26Z)

```
$ cmake ..
-- The CXX compiler identification is GNU 13.3.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
CMake Error at /opt/rocm/lib/cmake/hsa-runtime64/hsa-runtime64Targets.cmake:80 (message):
  The imported target "hsa-runtime64::hsa-runtime64" references the file

     "/opt/rocm/lib/libhsa-runtime64.so.1.15.60400"

  but this file does not exist.  Possible reasons include:

  * The file was deleted, renamed, or moved to another location.

  * An install or uninstall procedure did not complete successfully.

  * The installation package was faulty and contained

     "/opt/rocm/lib/cmake/hsa-runtime64/hsa-runtime64Targets.cmake"

  but not all the files it references.

Call Stack (most recent call first):
  /opt/rocm/lib/cmake/hsa-runtime64/hsa-runtime64-config.cmake:82 (include)
  /usr/share/cmake-3.28/Modules/CMakeFindDependencyMacro.cmake:76 (find_package)
  /opt/rocm/lib/cmake/hip/hip-config-amd.cmake:133 (find_dependency)
  /opt/rocm/lib/cmake/hip/hip-config.cmake:149 (include)
  CMakeLists.txt:40 (find_package)


-- Configuring incomplete, errors occurred!
```

---

### 评论 #2 — harkgill-amd (2025-04-24T19:50:37Z)

Hi @sbates130272, WSL based ROCm installations use a different versioning/filename for libhsa-runtime64.so when compared to Native Linux. The CMake error is caused by exactly that, CMake is expecting the Linux `.1.15.60400` version but only the WSL `.1.14.0` exists.

The current recommendation is to alter the expected filename in `/opt/rocm/lib/cmake/hsa-runtime64/hsa-runtime64Targets-relwithdebinfo.cmake` to the WSL specific version as highlighted in [WSL Specific Issues](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/limitations.html#wsl-specific-issues). An alternative method is to create a symbolic link between both versions, for example
```
cd /opt/rocm/lib/
ln -s libhsa-runtime64.so.1.14.0 libhsa-runtime64.so.1.15.60400
```
Please give either method a try and let me know if you have any questions.

---

### 评论 #3 — sbates130272 (2025-04-24T23:51:12Z)

_The current recommendation is to alter the expected filename in /opt/rocm/lib/cmake/hsa-runtime64/hsa-runtime64Targets-relwithdebinfo.cmake to the WSL specific version as highlighted in WSL Specific Issues._

Thanks @harkgill-amd. I can confirm that this fixed the issue. I assume this will be fixed in due course.

---

### 评论 #4 — harkgill-amd (2025-04-29T19:47:08Z)

Glad to hear it's working on your end. A fix is planned for an upcoming release that will eliminate the need for the workaround.



---

### 评论 #5 — harkgill-amd (2025-06-05T18:04:46Z)

This issue is addressed in the new ROCm 6.4.1 WSL release as `libhsa-runtime64.so` now follows the Linux versioning.
```
ls /opt/rocm/lib | grep libhsa-runtime
libhsa-runtime64.so
libhsa-runtime64.so.1
libhsa-runtime64.so.1.15.60401
```

---
