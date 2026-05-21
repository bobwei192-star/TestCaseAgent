# [Issue]: amd-smi  AttributeError: module 'amdsmi.amdsmi_interface' has no attribute 'amdsmi_get_node_handle' in multi rocm installation

> **Issue #5966**
> **状态**: closed
> **创建时间**: 2026-02-13T13:47:43Z
> **更新时间**: 2026-03-04T15:36:57Z
> **关闭时间**: 2026-03-04T15:36:57Z
> **作者**: alexschroeter
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5966

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- darren-amd

## 描述

### Problem Description

In multi ROCm installation with 7.2.0 and 6.2.4 amd-smi produces the following error

```
AttributeError: module 'amdsmi.amdsmi_interface' has no attribute 'amdsmi_get_node_handle'
```

Most likely related to https://github.com/ROCm/ROCm/issues/5875

### Operating System

Alma 9.7

### CPU

Irrelevant

### GPU

Irrelevant

### ROCm Version

6.2.4 + 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

Installed amdgpu-dkms from 30.10.3 and ROCm 6.2.4 and 7.2.0 from the repo and run amd-smi when 7.2.0 module is loaded get the error. When 6.2.4 is loaded output is correct.

---

## 评论 (5 条)

### 评论 #1 — alexschroeter (2026-02-13T14:11:50Z)

As a workaround I prepended the version specific path inside the module file.

add `prepend-path PYTHONPATH "/opt/rocm-7.2.0/share/amd_smi"` in `/usr/share/Modules/modulefiles/rocm/7.2.0` and do the same for the other version.

Note: I think the module load rocm should also have the `conflict rocm` line so you cannot load both.

---

### 评论 #2 — darren-amd (2026-02-18T19:00:01Z)

Hi @alexschroeter,

Thanks for reporting the issue! The issue is being caused by a function (in this case `amdsmi_get_node_handle`) that was introduced in 7.2 and not available in 6.2.4, and as the python library wasn't cleaned out you are referencing API's that don't exist. We have guidance in our documentation available [here](https://rocm.docs.amd.com/projects/amdsmi/en/latest/install/install.html#install-the-python-library-for-multiple-rocm-instances). We recommend that you uninstall the previous amd-smi python library before installing the newer version.

On another note, it seems that downgrading causes the issue (7.2 -> 6.2.4) but upgrading seems fine. I'd still recommend you uninstall previous library versions though as in our docs.

---

### 评论 #3 — alexschroeter (2026-02-19T09:01:25Z)

Hi @darren-amd, I see the entry in the documentation, thank you. I am however a bit confused. In a multi rocm installation if I `module load <the rocm version which doesn't have amd-smi installed>` I would expect amd-smi to fail again because it would be using the other pythonenv. It's also quite unintuitive to have multi version packages that don't work together. I feel that my solution is more consistent with what one would expect at the moment. Do I missunderstand?

---

### 评论 #4 — darren-amd (2026-02-20T19:49:22Z)

Hi @alexschroeter,

I think that it's a valid approach, let me follow up with the internal team and get back to you.

---

### 评论 #5 — darren-amd (2026-02-25T19:36:23Z)

Hi @alexschroeter,

We have a fix targeted for the next ROCm release: https://github.com/ROCm/rocm-systems/pull/3082, that adjusts the priority order for the amd-smi python library. I gave this a try by manually patching on a system with ROCm 6.3.1 and 7.2.0 installed and verified it fixes the issue. It will be included in the next release, but in the meantime you can either manually patch or continue using the method you described.

---
