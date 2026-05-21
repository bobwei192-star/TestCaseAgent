# [Issue]: Cannot install ROCm on ubi-based container (RHEL)

> **Issue #3957**
> **状态**: closed
> **创建时间**: 2024-10-30T09:24:58Z
> **更新时间**: 2024-11-05T18:18:43Z
> **关闭时间**: 2024-11-05T18:18:43Z
> **作者**: dtrifiro
> **标签**: Under Investigation, ROCm 6.2.0, ROCm 6.2.3, ROCm 6.2.2, ROCm 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/3957

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.0** (颜色: #ededed)
- **ROCm 6.2.3** (颜色: #ededed)
- **ROCm 6.2.2** (颜色: #ededed)
- **ROCm 6.2.1** (颜色: #ededed)

## 描述

### Problem Description

I'm trying to build a simple ubi-based dockerfile in which I install the ROCm package following the [official instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/rhel.html)

```dockerfile
FROM registry.access.redhat.com/ubi9/ubi

ARG ROCM_VERSION=6.2.3
RUN printf "[amdgpu]\n\
name=amdgpu\n\
baseurl=https://repo.radeon.com/amdgpu/${ROCM_VERSION}/rhel/9.4/main/x86_64/\n\
enabled=1\n\
priority=50\n\
gpgcheck=1\n\
gpgkey=https://repo.radeon.com/rocm/rocm.gpg.key\n\
[ROCm-${ROCM_VERSION}]\n\
name=ROCm${ROCM_VERSION}\n\
baseurl=https://repo.radeon.com/rocm/rhel9/${ROCM_VERSION}/main\n\
enabled=1\n\
priority=50\n\
gpgcheck=1\n\
gpgkey=https://repo.radeon.com/rocm/rocm.gpg.key" > /etc/yum.repos.d/amdgpu.repo


RUN dnf -y install \
        rocm
```

However, building this results in a dependency error:

```
#0 building with "default" instance using docker driver

#1 [internal] connecting to local controller
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile.ubi.test
#2 transferring dockerfile: 606B done
#2 DONE 0.0s

#3 [internal] load metadata for registry.access.redhat.com/ubi9/ubi:latest
#3 DONE 0.0s

#4 [internal] load .dockerignore
#4 transferring context: 397B done
#4 DONE 0.0s

#5 [1/3] FROM registry.access.redhat.com/ubi9/ubi:latest
#5 DONE 0.0s

#6 [2/3] RUN printf "[amdgpu]\nname=amdgpu\nbaseurl=https://repo.radeon.com/amdgpu/6.2.3/rhel/9.4/main/x86_64/\nenabled=1\npriority=50\ngpgcheck=1\ngpgkey=https://repo.radeon.com/rocm/rocm.gpg.key\n[ROCm-6.2.3]\nname=ROCm6.2.3\nbaseurl=https://repo.radeon.com/rocm/rhel9/6.2.3/main\nenabled=1\npriority=50\ngpgcheck=1\ngpgkey=https://repo.radeon.com/rocm/rocm.gpg.key" > /etc/yum.repos.d/amdgpu.repo

#7 [3/3] RUN dnf -y install         rocm
#7 0.379 Updating Subscription Management repositories.
#7 0.379 Unable to read consumer identity
#7 0.380
#7 0.380 This system is not registered with an entitlement server. You can use subscription-manager to register.
#7 0.380
#7 1.144 amdgpu                                          102 kB/s |  76 kB     00:00
#7 1.955 ROCm6.2.3                                       807 kB/s | 645 kB     00:00
#7 2.722 Red Hat Universal Base Image 9 (RPMs) - BaseOS  751 kB/s | 524 kB     00:00
#7 3.490 Red Hat Universal Base Image 9 (RPMs) - AppStre 2.9 MB/s | 2.1 MB     00:00
#7 4.055 Red Hat Universal Base Image 9 (RPMs) - CodeRea 809 kB/s | 278 kB     00:00
#7 4.199 (try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
#7 4.199 Error:
#7 4.199  Problem: package rocm-6.2.3.60203-124.el9.x86_64 from ROCm-6.2.3 requires mivisionx = 3.0.0.60203-124, but none of the providers can be installed
#7 4.199   - package mivisionx-3.0.0.60203-124.x86_64 from ROCm-6.2.3 requires rocdecode, but none of the providers can be installed
#7 4.199   - conflicting requests
#7 4.199   - nothing provides libva needed by rocdecode-0.6.0.60203-124.x86_64 from ROCm-6.2.3
#7 ERROR: process "/bin/sh -c dnf -y install         rocm" did not complete successfully: exit code: 1
------
 > [3/3] RUN dnf -y install         rocm:
1.955 ROCm6.2.3                                       807 kB/s | 645 kB     00:00
2.722 Red Hat Universal Base Image 9 (RPMs) - BaseOS  751 kB/s | 524 kB     00:00
3.490 Red Hat Universal Base Image 9 (RPMs) - AppStre 2.9 MB/s | 2.1 MB     00:00
4.055 Red Hat Universal Base Image 9 (RPMs) - CodeRea 809 kB/s | 278 kB     00:00
4.199 (try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
4.199 Error:
4.199  Problem: package rocm-6.2.3.60203-124.el9.x86_64 from ROCm-6.2.3 requires mivisionx = 3.0.0.60203-124, but none of the providers can be installed
4.199   - package mivisionx-3.0.0.60203-124.x86_64 from ROCm-6.2.3 requires rocdecode, but none of the providers can be installed
4.199   - conflicting requests
4.199   - nothing provides libva needed by rocdecode-0.6.0.60203-124.x86_64 from ROCm-6.2.3
------
Dockerfile:20
--------------------
  19 |
  20 | >>> RUN dnf -y install \
  21 | >>>         rocm
  22 |
--------------------
ERROR: process "/bin/sh -c dnf -y install         rocm" did not complete successfully: exit code: 1
```

This was working fine with 6.1.3: 
```bash
docker build --build-arg=ROCM_VERSION=6.1.3 .
```
works fine.


I can trace down the cause of this to the update of `mivisionx` from 2.5 to 3.0, which now pulls in `rocdecode` which requires `libva`


Dependencies for `mivisionx` for 6.1.3:
```
package: mivisionx-2.5.0.60103-122.x86_64
  dependency: half
   provider: half-1.12.0.60103-122.el9.x86_64
  dependency: migraphx
   provider: migraphx-2.9.0.60103-122.el9.x86_64
  dependency: miopen-hip
   provider: miopen-hip-3.1.0.60103-122.el9.x86_64
  dependency: rocblas
   provider: rocblas-4.1.2.60103-122.el9.x86_64
  dependency: rocm-core
   provider: rocm-core-6.1.3.60103-122.el9.x86_64
  dependency: rocm-hip-runtime
   provider: rocm-hip-runtime-6.1.3.60103-122.el9.x86_64
  dependency: rpp
   provider: rpp-1.5.0.60103-122.el9.x86_64
```

Dependencies for `mivisionx` for 6.2.3:

```
package: mivisionx-2.5.0.60103-122.x86_64
  dependency: half
   provider: half-1.12.0.60103-122.el9.x86_64
  dependency: migraphx
   provider: migraphx-2.9.0.60103-122.el9.x86_64
  dependency: miopen-hip
   provider: miopen-hip-3.1.0.60103-122.el9.x86_64
  dependency: rocblas
   provider: rocblas-4.1.2.60103-122.el9.x86_64
  dependency: rocm-core
   provider: rocm-core-6.1.3.60103-122.el9.x86_64
  dependency: rocm-hip-runtime
   provider: rocm-hip-runtime-6.1.3.60103-122.el9.x86_64
  dependency: rpp
   provider: rpp-1.5.0.60103-122.el9.x86_64
```






### Operating System

Red Hat Enterprise Linux 9.4

### CPU

.

### GPU

.

### ROCm Version

ROCm 6.2.3, ROCm 6.2.2, ROCm 6.2.1, ROCm 6.2.0

### ROCm Component

MIVisionX

### Steps to Reproduce

`docker build --build-arg=ROCM_VERSION=6.2.3 .`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — RH-steve-grubb (2024-10-30T13:26:15Z)

I have a feeling this is being pulled in to support multi-modal models. But can we make this a soft dependency so that text only models can work without pulling in a whole desktop? (libva depends on libX11.)

---

### 评论 #2 — Mystro256 (2024-10-30T14:36:15Z)

> However, building this results in a dependency error:

libva is in the Appstream repo provided for RHEL 9; I suspect this image only has BaseOS enabled. If you want to pull in all of ROCm, including mivisionx, you need to enable Appstream.

> I have a feeling this is being pulled in to support multi-modal models. But can we make this a soft dependency so that text only models can work without pulling in a whole desktop? (libva depends on libX11.)

So this is a hard dependency for mivisionx unfortunately since it depends on rocdecode and that links to libva.
With that said, the "rocm" package is just a metapackage, a user can just install all of rocm excluding rocdecode like so:

sudo dnf install rocm-developer-tools rocm-ml-sdk rocm-opencl-sdk rocm-openmp-sdk rocm-utils

---
