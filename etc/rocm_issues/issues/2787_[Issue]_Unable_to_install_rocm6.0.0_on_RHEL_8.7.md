# [Issue]: Unable to install rocm/6.0.0 on RHEL 8.7

> **Issue #2787**
> **状态**: closed
> **创建时间**: 2024-01-09T15:28:36Z
> **更新时间**: 2024-01-30T14:53:19Z
> **关闭时间**: 2024-01-30T14:53:19Z
> **作者**: xinye83
> **标签**: Under Investigation, Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2787

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Documentation** (颜色: #5319e7)

## 描述

### Problem Description

I was following the install guide at `https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html` to try to install rocm/6.0.0 in a RHEL 8.7 container and it failed with the following error
```
[MIRROR] amdgpu-install-6.0.60000-1.el8.noarch.rpm: Status code: 404 for https://repo.radeon.com/amdgpu-install/6.0/rhel/8.7/amdgpu-install-6.0.60000-1.el8.noarch.rpm (IP: 10.78.90.46)
[MIRROR] amdgpu-install-6.0.60000-1.el8.noarch.rpm: Status code: 404 for https://repo.radeon.com/amdgpu-install/6.0/rhel/8.7/amdgpu-install-6.0.60000-1.el8.noarch.rpm (IP: 10.78.90.46)
[MIRROR] amdgpu-install-6.0.60000-1.el8.noarch.rpm: Status code: 404 for https://repo.radeon.com/amdgpu-install/6.0/rhel/8.7/amdgpu-install-6.0.60000-1.el8.noarch.rpm (IP: 10.78.90.46)
[MIRROR] amdgpu-install-6.0.60000-1.el8.noarch.rpm: Status code: 404 for https://repo.radeon.com/amdgpu-install/6.0/rhel/8.7/amdgpu-install-6.0.60000-1.el8.noarch.rpm (IP: 10.78.90.46)
[FAILED] amdgpu-install-6.0.60000-1.el8.noarch.rpm: Status code: 404 for https://repo.radeon.com/amdgpu-install/6.0/rhel/8.7/amdgpu-install-6.0.60000-1.el8.noarch.rpm (IP: 10.78.90.46)
Status code: 404 for https://repo.radeon.com/amdgpu-install/6.0/rhel/8.7/amdgpu-install-6.0.60000-1.el8.noarch.rpm (IP: 10.78.90.46)
```

### Operating System

RHEL 8.7

### CPU

null

### GPU

AMD Instinct MI250X

### Other

_No response_

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — yhuiYH (2024-01-09T18:57:45Z)

Seems like RHEL 8.7 and 9.1 are no longer supported in ROCm 6.0: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html.  The documentation did not update the RHEL instructions correctly.

Similar to #2737 , it seems other RHEL pages in the documentation need to be updated properly to 
1) Remove RHEL 8.7 and RHEL 9.1
2) Add RHEL 8.9 and RHEL 9.3

These are the pages that need to be fixed:
1) https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html
2) https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html

@xinye83 perhaps you can move your container to RHEL 8.8 until the documentation is fixed.

---

### 评论 #2 — yhuiYH (2024-01-30T14:53:19Z)

The documentation has been updated correctly now to remove RHEL 8.7 and 9.1, but add RHEL 8.9 and 9.3.  For example, in this page, the RHEL section shows correctly now:

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html

I believe we can close this.

---
