# [Feature]: wider support for '--json' option

> **Issue #4374**
> **状态**: closed
> **创建时间**: 2025-02-14T08:25:36Z
> **更新时间**: 2025-03-11T19:45:45Z
> **关闭时间**: 2025-03-11T19:45:44Z
> **作者**: alexishuxley
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4374

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Our node monitoring scripts call `rocm-smi -a --json` and briefly cache its output in order to make a number of health checks on each compute node. We would like to add a new check for uncorrectable SDMA/GFX/MMHUB errors, but ...
```
[root@vipa1278 ~]# rocm-smi --json --showrasinfo 
WARNING: No JSON data to report
[root@vipa1278 ~]# rocm-smi --json --showrasinfo SDMA GFX MMHUB 
WARNING: No JSON data to report
[root@vipa1278 ~]# 
```
Please could you add support for the `--json` option to all `--show*` options. 

### Operating System

SUSE SLES 15SP*

### GPU

MI300A

### ROCm Component

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-02-28T16:35:38Z)

Hi @alexishuxley, `rocm-smi` has been deprecated in favour of it's successor, `amd-smi`. 

The relevant commands to check for RAS information would be a mix of `amd-smi static -r` and `amd-smi metric -e`. Both of these commands (and all of amd-smi) have json support with the `--json flag`. If these two commands don’t fully cover what you’re looking for, let me know, and I’ll double-check for any specific metrics.


---

### 评论 #2 — harkgill-amd (2025-03-11T19:45:44Z)

Closing this issue out for now. Please leave a comment if you encounter any issues with `--json` on `amd-smi`.

---
