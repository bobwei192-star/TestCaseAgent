# [Issue]: ROCgdb: warning: amd-dbgapi: unable to enable GPU debugging due to a restriction error

> **Issue #5949**
> **状态**: closed
> **创建时间**: 2026-02-10T16:13:53Z
> **更新时间**: 2026-02-11T07:15:24Z
> **关闭时间**: 2026-02-11T07:15:24Z
> **作者**: TomClabault
> **标签**: AMD Radeon RX 7900 XTX, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5949

## 标签

- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

I downloaded & installed the ROCm 7.1.1 Windows SDK from here (https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html).

Trying to run rocgdb on my project (`rocgdb ./HIPRTPathTracer.exe`) yields this warning:

`amd-dbgapi: unable to enable GPU debugging due to a restriction error`

and so it seems that I cannot find memory access faults / other errors in my HIP kernels because of that. 

Is ROCgdb fully functional on Windows for HIP debugging? Is there something wrong with my setup?

### Operating System

Windows 10.0.26100

### CPU

i5 13600KF

### GPU

7900XTX

### ROCm Version

7.1.1

### ROCm Component

ROCgdb

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — schung-amd (2026-02-10T21:16:09Z)

Not sure if this is the expected error for this case, but unfortunately ROCgdb on Windows is only supported on single GPU `gfx120x` systems at the moment (see https://rocm.docs.amd.com/projects/install-on-windows/en/develop/how-to/debugger-windows.html#list-of-windows-rocgdb-limitations).

---

### 评论 #2 — TomClabault (2026-02-11T07:15:24Z)

Oh I see, I guess that explains it then, thanks!

---
