# [Documentation]: What is `rocm-utils`?

> **Issue #4530**
> **状态**: closed
> **创建时间**: 2025-03-26T01:27:18Z
> **更新时间**: 2025-05-26T15:07:57Z
> **关闭时间**: 2025-05-26T15:06:50Z
> **作者**: garrettbyrd
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4530

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

When using `dnf`/`apt` to install ROCm, `rocm-utils` is a package installed from `repo.radeon.com` ([e.g., `.deb` here](https://repo.radeon.com/rocm/apt/6.3.3/pool/main/r/rocm-utils/)) but is not mentioned anywhere in the ROCm documentation. The closest thing to documentation relating to this is [this GitHub Pages page of ROCm 4.1 documentation](https://cgmb-rocm-docs.readthedocs.io/en/latest/Installation_Guide/Software-Stack-for-AMD-GPU.html) that was cloned by Cory.

It seems that the only file it adds is a text file (`/opt/rocm/.info/version-utils` ) that contains a single line that specifies the ROCm version. (E.g., `6.3.3-74`.)

Is this an artifact from older versions of ROCm, or is this still used somewhere?

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-03-26T19:24:04Z)

Hey @garrettbyrd, rocm-utils is a legacy meta-package which contains 

- rocminfo
- rocm-cmake
- rocm-core

It's legacy status is why it didn't make it into [Packages in ROCm programming models](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/package-manager-integration.html#packages-in-rocm-programming-models). Currently in discussion with the docs team on the best approach to highlight this in our documentation. Will keep this thread updated.

---

### 评论 #2 — harkgill-amd (2025-05-26T15:06:50Z)

@garrettbyrd, the following excerpt will be added to the Packages in ROCm programming models page. 

```
rocm-utils is a legacy meta-package that includes rocminfo, rocm-cmake, and rocm-core. Other meta-packages manage the installation of these components.
```
The changes will be live in the next couple days. 

---
