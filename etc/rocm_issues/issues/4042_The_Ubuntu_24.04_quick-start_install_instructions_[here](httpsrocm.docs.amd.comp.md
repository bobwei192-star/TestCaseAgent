# The Ubuntu 24.04 quick-start install instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) simply don't work, yielding:

> **Issue #4042**
> **状态**: closed
> **创建时间**: 2024-11-20T00:18:10Z
> **更新时间**: 2024-11-25T15:02:36Z
> **关闭时间**: 2024-11-25T15:02:36Z
> **作者**: saadrahim
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4042

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

              The Ubuntu 24.04 quick-start install instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) simply don't work, yielding:
```
The following packages have unmet dependencies:
 hipsolver : Depends: libcholmod3 but it is not installable
             Depends: libsuitesparseconfig5 but it is not installable
 rocm-gdb : Depends: libpython3.10 (>= 3.10.0) but it is not installable
 ```
I guess documentation was copied and pasted with only version number updates, assuming the steps would work about being tested.  No doubt testing these steps takes significant effort - but it's either once at source, or every poor user :-(

The detailed instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/native-install/ubuntu.html) **do work**, I guess because it's vital to register the AMD repo's.

_Originally posted by @chris-hatton in https://github.com/ROCm/ROCm/issues/2993#issuecomment-2480859340_
            

---

## 评论 (3 条)

### 评论 #1 — saadrahim (2024-11-20T00:18:40Z)

Please correct the documentation

---

### 评论 #2 — harkgill-amd (2024-11-20T15:26:04Z)

Hi @saadrahim, left a comment on the previous thread. I wasn't able to reproduce the dependency errors reported and it's likely the issue has to do with the user's environment. I've provided steps for a clean reinstallation 

We can continue to use this thread for updates. 

---

### 评论 #3 — harkgill-amd (2024-11-25T15:02:36Z)

Was able to reproduce the exact dependency errors reported by the user. There was a mismatch in the amdgpu-install version on the system versus the OS installed (jammy amdgpu-install, noble OS installed). Will close out this issue as I've provided the exact steps to resolve this issue over at https://github.com/ROCm/ROCm/issues/2993#issuecomment-2498245912. Thanks!

---
