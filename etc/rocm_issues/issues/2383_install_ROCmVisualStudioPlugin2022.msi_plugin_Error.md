#  install ROCmVisualStudioPlugin2022.msi plugin Error

> **Issue #2383**
> **状态**: closed
> **创建时间**: 2023-08-16T13:17:44Z
> **更新时间**: 2024-06-24T20:43:06Z
> **关闭时间**: 2024-06-24T20:43:06Z
> **作者**: cheapw
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2383

## 描述

I came across an error while installing ROCmVisualStudioPlugin2022.msi plugin. The error content is 'There is a problem with this Windows install package. A program run as part of the setup did not finish as expected. Contact your support personnel or package vendor'.
My visual studio version is 17.7.0。
Windows version windows 11 professional workstation 23H2 22631.2191，
CPU AMD 6800H & Graphics card RX 6700M
<img width="481" alt="image" src="https://github.com/RadeonOpenCompute/ROCm/assets/30453216/f89bde90-bdf8-4ba6-bad3-219affe8d628">


---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-05-14T15:34:28Z)

@cheapw Please try with HIP SDK 5.7.1 (https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html). If resolved, please close the ticket. Thanks!

---

### 评论 #2 — harkgill-amd (2024-06-24T20:43:06Z)

Hi @cheapw, I could not reproduce this issue when installing the Visual Studio Plugin paired with the latest 5.7.1 HIP SDK. Please re-open this issue if the error persists. Thanks!

---
