# [Issue]: ROCm 7.0.3/7.2.1 have fewer ASAN RPMs than 7.0.2/7.2.0; naming and rpath variants differ

> **Issue #6145**
> **状态**: closed
> **创建时间**: 2026-04-13T14:14:38Z
> **更新时间**: 2026-04-27T18:37:06Z
> **关闭时间**: 2026-04-27T18:36:58Z
> **作者**: ragges
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6145

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Problem Description


rocm 7.0.3 and 7.2.1 has fewer packages than e.g. 7.0.2 and 7.2.0.
It seems mainly to be asan packages that are missing.

For example, in 7.2.0, there are:
  roctracer-asan-4.1.70200.70200-sles156.43.x86_64.rpm
  roctracer-asan7.2.0-4.1.70200.70200-sles156.43.x86_64.rpm
  roctracer-asan-rpath7.2.0-4.1.70200.70200-sles156.43.x86_64.rpm

where
  roctracer-asan-rpath7.2.0-4.1.70200.70200-sles156.43.x86_64.rpm 
and
  roctracer-asan7.2.0-4.1.70200.70200-sles156.43.x86_64.rpm
seem to contain the same things, which is maybe not intentional.

In 7.2.1, there is only
  roctracer-asan-4.1.70201.70201-sles156.81.x86_64.rpm

So no rpath version, which may or may not be intentional, and you went with the
  roctracer-asan-4.1.70201.70201-sles156.81.x86_64.rpm
instead of the
  roctracer-asan7.2.1-4.1.70201.70201-sles156.81.x86_64.rpm
which I don't know if it is intentional, since now it is much tricker to point out a specific version of things in the same way as you could before.

Is this a mistake, or should we adapt to this?

Best regards,
Ragnar

### Operating System

sles15sp7

### CPU

AMD EPYC 7A53 64-Core Processor

### GPU

AMD Instinct MI250X

### ROCm Version

ROCm 7.2.1 (and 7.0.3)

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — nunnikri (2026-04-16T15:49:08Z)

Following is the difference bw these packages.
roctracer-asan-4.1.70200.70200-sles156.43.x86_64.rpm -> Non version asan packge
roctracer-asan7.2.0-4.1.70200.70200-sles156.43.x86_64.rpm -> Versioned asan package. Contents same as non-version, used it for multi version install.
roctracer-asan-rpath7.2.0-4.1.70200.70200-sles156.43.x86_64.rpm -> versioned rpath asan package. Contents name will be same but RUN_PATH has been changed to RPATH in the asan libraries. 

In latest release, some of these packages are not released @JeniferC99 is this intended. 

---

### 评论 #2 — lucbruni-amd (2026-04-27T18:36:58Z)

This will not be addressed for previous versions of ROCm, but will be for the next upcoming release. Please feel free to reopen this issue or open a new one if this persists in the next release.

---
