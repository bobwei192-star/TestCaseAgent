# [Issue]: amd-smi fails to set memory partition to NPS4 (ROCM6.3.2)

> **Issue #4439**
> **状态**: closed
> **创建时间**: 2025-03-03T19:36:35Z
> **更新时间**: 2025-03-11T19:24:38Z
> **关闭时间**: 2025-03-11T19:24:37Z
> **作者**: dezhiAmd
> **标签**: Under Investigation, AMD Instinct MI300X, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4439

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

sudo amd-smi set --memory-partition NPS4

          ****** WARNING ******

          Setting Dynamic Memory (NPS) partition modes require users to quit all GPU workloads.
          AMD SMI will then attempt to change memory (NPS) partition mode.
          Upon a successful set, AMD SMI will then initiate an action to restart AMD GPU driver.
          This action will change all GPU's in the hive to the requested memory (NPS) partition mode.

          Please use this utility with caution.

Do you accept these terms? [Y/N] Y

GPU: 0 again - Updating memory partition for gpu 0: [█████...................................] 20/140 secs remain
    MEMORY_PARTITION: [AMDSMI_STATUS_AMDGPU_RESTART_ERR] Could not successfully restart
        driver after applying NPS4 on GPU ID: 0 BDF:0000:05:00.0

GPU: 1
    MEMORY_PARTITION: [AMDSMI_STATUS_NOT_SUPPORTED] Device does not support setting
        memory partition to NPS4 on GPU ID: 1 BDF:0000:05:00.1

### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD EPYC 9554 64-Core Processor

### GPU

MI300X

### ROCm Version

ROCM6.3.2

### ROCm Component

_No response_

### Steps to Reproduce

1) Set compute partition to CPX by running:
amd-smi     set --compute-partition CPX
(Notice that now we have 64 GPU using ROCM-SMI)

2) Run 
amd-smi     set --memorypartition CPX

Now we see the issue

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — dezhiAmd (2025-03-03T19:45:22Z)

sudo amd-smi set --memory-partition NPS4 works on ROCM6.2.0. 
Please check:
SharkMi300x-4 use ROCM6.3.2 fail

smc300x-ccs-aus-GPUF280.cs-aus.dcgpu use ROCM6.2.0 works

---

### 评论 #2 — harkgill-amd (2025-03-06T19:52:24Z)

Synced with @dezhiAmd internally on this issue. Will keep GitHub issue thread updated with results of investigation for future reference.

---

### 评论 #3 — dezhiAmd (2025-03-11T19:24:37Z)

Thanks to the help from @harkgill-amd. Issue is fixed by following steps:
1) Do a clean uninstallation:
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```

2) Install ROCM6.3.3

---
