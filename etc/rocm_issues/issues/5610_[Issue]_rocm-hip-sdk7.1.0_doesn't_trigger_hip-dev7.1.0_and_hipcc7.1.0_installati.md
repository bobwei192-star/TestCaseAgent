# [Issue]: rocm-hip-sdk7.1.0 doesn't trigger hip-dev7.1.0 and hipcc7.1.0 installation.

> **Issue #5610**
> **状态**: closed
> **创建时间**: 2025-10-31T21:07:49Z
> **更新时间**: 2026-01-22T15:18:46Z
> **关闭时间**: 2026-01-22T15:18:46Z
> **作者**: ye-luo
> **标签**: status: assessed, status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5610

## 标签

- **status: assessed** (颜色: #e6d813)
- **status: fix submitted** (颜色: #75d97e)

## 负责人

- zichguan-amd

## 描述

### Problem Description

Surprise that the actual hip compiler wrapper and header files not installed by default.
Broken package dependency?

### Operating System

Ubuntu 24.04

### CPU

...

### GPU

...

### ROCm Version

7.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — zichguan-amd (2025-11-04T19:16:33Z)

Hi @ye-luo, from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/package-manager-integration.html#id4, `rocm-hip-sdk` should depend on `rocm-hip-runtime-dev` which has `hip-dev` and `hipcc`.
6.4.4 package:
```
$ apt show rocm-hip-sdk
Package: rocm-hip-sdk
Version: 6.4.4.60404-129~24.04
Priority: optional
Section: devel
Maintainer: ROCm Dev Support <rocm-dev.support@amd.com>
Installed-Size: 13.3 kB
Depends: rocm-hip-libraries (= 6.4.4.60404-129~24.04), rocm-core (= 6.4.4.60404-129~24.04), rocm-hip-runtime-dev (= 6.4.4.60404-129~24.04), composablekernel-dev (= 1.1.0.60404-129~24.04), hipblas-common-dev (= 1.0.0.60404-129~24.04), hipblas-dev (= 2.4.0.60404-129~24.04), hipblaslt-dev (= 0.12.1.60404-129~24.04), hipcub-dev (= 3.4.0.60404-129~24.04), hipfft-dev (= 1.0.18.60404-129~24.04), hipsparse-dev (= 3.2.0.60404-129~24.04), hipsolver-dev (= 2.4.0.60404-129~24.04), hipfort-dev (= 0.6.0.60404-129~24.04), hiptensor-dev (= 1.5.0.60404-129~24.04), rccl-dev (= 2.22.3.60404-129~24.04), rocalution-dev (= 3.2.3.60404-129~24.04), rocblas-dev (= 4.4.1.60404-129~24.04), rocfft-dev (= 1.0.32.60404-129~24.04), rocprim-dev (= 3.4.1.60404-129~24.04), rocrand-dev (= 3.3.0.60404-129~24.04), hiprand-dev (= 2.12.0.60404-129~24.04), rocsolver-dev (= 3.28.2.60404-129~24.04), rocsparse-dev (= 3.4.0.60404-129~24.04), rocthrust-dev (= 3.3.0.60404-129~24.04), rocwmma-dev (= 1.7.0.60404-129~24.04), hipsparselt-dev (= 0.2.3.60404-129~24.04)
Homepage: https://github.com/RadeonOpenCompute/ROCm
Download-Size: 2,286 B
APT-Manual-Installed: no
APT-Sources: https://repo.radeon.com/rocm/apt/6.4.4 noble/main amd64 Packages
Description: Radeon Open Compute (ROCm) Runtime software stack
```
7.1.0 package:
```
$ apt show rocm-hip-sdk
Package: rocm-hip-sdk
Version: 7.1.0.70100-20~24.04
Priority: optional
Section: devel
Maintainer: ROCm Dev Support <rocm-dev.support@amd.com>
Installed-Size: 13.3 kB
Depends: rocm-hip-libraries (= 7.1.0.70100-20~24.04), rocm-core (= 7.1.0.70100-20~24.04), composablekernel-dev (= 1.1.0.70100-20~24.04), hipblas-common-dev (= 1.3.0.70100-20~24.04), hipblas-dev (= 3.1.0.70100-20~24.04), hipblaslt-dev (= 1.1.0.70100-20~24.04), hipcub-dev (= 4.1.0.70100-20~24.04), hipfft-dev (= 1.0.21.70100-20~24.04), hipsparse-dev (= 4.1.0.70100-20~24.04), hipsolver-dev (= 3.1.0.70100-20~24.04), hipfort-dev (= 0.7.1.70100-20~24.04), hiptensor-dev (= 2.0.0.70100-20~24.04), rccl-dev (= 2.27.7.70100-20~24.04), rocalution-dev (= 4.0.1.70100-20~24.04), rocblas-dev (= 5.1.0.70100-20~24.04), rocfft-dev (= 1.0.35.70100-20~24.04), rocprim-dev (= 4.1.0.70100-20~24.04), rocrand-dev (= 4.1.0.70100-20~24.04), hiprand-dev (= 3.1.0.70100-20~24.04), rocsolver-dev (= 3.31.0.70100-20~24.04), rocsparse-dev (= 4.1.0.70100-20~24.04), rocthrust-dev (= 4.1.0.70100-20~24.04), rocwmma-dev (= 2.0.0.70100-20~24.04), hipsparselt-dev (= 0.2.5.70100-20~24.04)
Homepage: https://github.com/RadeonOpenCompute/ROCm
Download-Size: 2,308 B
APT-Sources: https://repo.radeon.com/rocm/apt/7.1 noble/main amd64 Packages
Description: Radeon Open Compute (ROCm) Runtime software stack
```
7.1.0 is missing the `rocm-hip-runtime-dev` dependency. Seems like broken dependency indeed.

---

### 评论 #2 — hazecodeio (2025-11-04T20:16:41Z)

Something not right with installing 7.1 for me as well..
I used `amdgpu-install_7.1.70100-1_all` to upgrade from release 7.0.2
Tracing the dependencies I see broken dependency here:

https://repo.radeon.com/amdgpu/

<img width="700" height="58" alt="Image" src="https://github.com/user-attachments/assets/eb721e35-0c2a-4245-bfc9-72e4386edfa3" />

7.1 is missing..


---

### 评论 #3 — ianbmacdonald (2025-11-05T22:39:39Z)

> Something not right with installing 7.1 for me as well.. I used `amdgpu-install_7.1.70100-1_all` to upgrade from release 7.0.2 Tracing the dependencies I see broken dependency here:
> 
> https://repo.radeon.com/amdgpu/
> 
there is no 7.1 for amdgpu .. @hazecodeio  you are confused with https://repo.radeon.com/rocm/apt/ 

this has nothing to do with the missing dependency;  You can read more about the split between the two here: https://rocm.blogs.amd.com/ecosystems-and-partners/instinct-gpu-driver/README.html

---

### 评论 #4 — zichguan-amd (2025-11-06T21:39:07Z)

Hi @ye-luo, the dependency has been fixed and will be available in 7.2 release. Meanwhile please manually install the necessary packages for 7.1. Sorry for the inconvenience.

@hazecodeio are you have any other issue when installing 7.1? Thanks @ianbmacdonald for the explanation, the instinct driver paired with 7.1 is [30.20](https://repo.radeon.com/amdgpu/30.20/). 

---

### 评论 #5 — ye-luo (2025-11-06T23:50:12Z)

I was hoping for a fix in 7.1.x if possible.

---

### 评论 #6 — hazecodeio (2025-11-07T19:26:34Z)

@zichguan-amd  I'm all set, Thanks.  It turned out my issue is not related to what's being reported here.
It is being tracked here #5625

---

### 评论 #7 — zichguan-amd (2025-11-07T19:30:57Z)

Unfortunately, it's too late in the release cycle for 7.1.1. 7.2 will be the next release.

---

### 评论 #8 — zichguan-amd (2026-01-22T15:18:46Z)

Hi @ye-luo, 7.2 has been released and the dependency issue has been fixed. `rocm-hip-sdk` now properly depends on `rocm-hip-runtime-dev`.
```
$ apt-cache rdepends rocm-hip-runtime-dev
rocm-hip-runtime-dev
Reverse Depends:
  rocm-hip-sdk
```

---
