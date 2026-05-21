# ROCm debugging tools might become unresponsive in SELinux-enabled distributions

> **Issue #5498**
> **状态**: open
> **创建时间**: 2025-10-10T22:37:30Z
> **更新时间**: 2025-10-10T22:39:18Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.2
> **URL**: https://github.com/ROCm/ROCm/issues/5498

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.2** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Red Hat Enterprise Linux (RHEL) and related distributions automatically enable a security feature named Security-Enhanced Linux (SELinux), which may prevent ROCm debugging tools, such as ROCgdb, ROCdbgapi, and ROCR Debug Agent, from working correctly.
 
The problem occurs when attempting to debug a program that contains code that runs on the GPU. The debugging session might become unresponsive while attempting to reach a breakpoint or executing instruction-stepping in device code. ROCgdb will still be responsive and accept interruptions by pressing `Control+C`, but the breakpoint in device code won't be hit, and the instruction-stepping operation will not be completed.
 
The ROCR Debug Agent might also become unresponsive when attempting to capture data from a program that is experiencing queue errors, memory faults, or other triggering events.
 
For a detailed workaround, see the [Installation troubleshooting](https://rocm.docs.amd.com/projects/install-on-linux-internal/en/latest/reference/install-faq.html#issue-10-rocm-debugging-tools-might-become-unresponsive-in-selinux-enabled-distributions) documentation. This issue will be fixed in a future ROCm release.
