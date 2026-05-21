# [Issue]: error output from rocminfo with AMD Radeon Pro W7900

> **Issue #2682**
> **状态**: closed
> **创建时间**: 2023-11-29T15:01:16Z
> **更新时间**: 2024-01-30T16:22:32Z
> **关闭时间**: 2024-01-30T16:22:31Z
> **作者**: alexhegit
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2682

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Run rocminfo

### Operating System

Ubun

### CPU

AMD Ryzen 7900

### GPU

AMD Radeon Pro W7900

### ROCm Version

5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

1. run rocminfo

### Output of /opt/rocm/bin/rocminfo --support

amd@AIG-PM:~$ rocminfo
ROCk module is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1204
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.


---

## 评论 (4 条)

### 评论 #1 — nartmada (2024-01-17T04:28:48Z)

An internal ticket has been created to investigate this issue.

---

### 评论 #2 — nartmada (2024-01-17T23:02:49Z)

Hi @alexhegit, we are not able to repro your issue here at AMD.  Can you please share your ROCm installation steps?  Thanks.

---

### 评论 #3 — nartmada (2024-01-23T03:41:59Z)

Hi @alexhegit, can you please share your ROCm installation steps?  We are not able to repro your issue here at AMD.  Thanks.

---

### 评论 #4 — nartmada (2024-01-30T16:22:31Z)

Closing the ticket as there is no response @alexhegit.  Please re-open if you still cannot get rocminfo to work.  Thanks.

---
