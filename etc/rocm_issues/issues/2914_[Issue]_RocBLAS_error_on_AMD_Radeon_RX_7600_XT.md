# [Issue]: RocBLAS error on AMD Radeon RX 7600 XT

> **Issue #2914**
> **状态**: closed
> **创建时间**: 2024-02-21T03:49:36Z
> **更新时间**: 2024-02-24T02:28:05Z
> **关闭时间**: 2024-02-24T02:28:05Z
> **作者**: SusieDreemurr
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2914

## 描述

Rocm is showing my GPU but I get this error when trying to load an AI model: 

rocBLAS error: Cannot read /home/krusie/text-generation-webui/installer_files/env/lib/python3.11/site-packages/torch/lib/rocblas/library/TensileLibrary.dat: No such file or directory
Aborted (core dumped)

---

## 评论 (3 条)

### 评论 #1 — nartmada (2024-02-21T20:24:57Z)

Hi @SusieDreemurr, 

RX 7600 XT is not officially supported by AMD.  Please refer to the System Requirement link https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

Unofficially some people have a workaround by setting environment variable HSA_OVERRIDE_GFX_VERSION=11.0.0.  This is not supported by AMD but some have had success with it.

Thanks. 

---

### 评论 #2 — SusieDreemurr (2024-02-22T03:53:32Z)

Ah, bummer. :/  Well, hopefully there will be official support but in the meantime, thanks for the workaround! 



---

### 评论 #3 — nartmada (2024-02-24T02:28:05Z)

Closing this ticket as a workaround has been provided for this issue.  Thanks.

---
