# When running the Windows 11 HIP Installer it tries to install 5.5.0 (Linux) not 5.5.1.

> **Issue #2377**
> **状态**: closed
> **创建时间**: 2023-08-12T13:15:22Z
> **更新时间**: 2024-07-12T18:44:40Z
> **关闭时间**: 2024-07-12T18:44:40Z
> **作者**: shott92
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2377

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- saadrahim

## 描述

When running the 
https://www.amd.com/en/developer/rocm-hub/eula/licenses.html?filename=AMD-Software-PRO-Edition-23.Q3-Win10-Win11-For-HIP.exe - AMD-Software-PRO-Edition-23.Q3-Win10-Win11-For-HIP installer - either normally or as adminstrator, it comes up with the offer to install 5.5.0 not the 5.5.1 as described on the page here:
https://www.amd.com/en/developer/rocm-hub/hip-sdk.html

![image](https://github.com/RadeonOpenCompute/ROCm/assets/37227619/18b52a30-15b4-423d-8ab2-928cccf6df3e)


seems to be a bug, could someone advise why this might be, and if there is a solution / work around please?

System version:
![image](https://github.com/RadeonOpenCompute/ROCm/assets/37227619/d1002689-ce13-42ff-9b1b-a56d841f6d9c)


Thanks

---

## 评论 (5 条)

### 评论 #1 — samathew121 (2023-08-16T04:56:05Z)

Hello saadrahim, Pls re-assign this ticked to Balla, Siva narayana in the UI team.

---

### 评论 #2 — kevinroosa (2023-09-13T12:12:00Z)

Adding to this ticket. Documentation for 5.6.1 points to 5.5 installer. Also, is there any clarification on if 5.6.1 is linux-only at the moment (prior to Win release)?

Attached is doc version and linked page.

![image](https://github.com/RadeonOpenCompute/ROCm/assets/46552859/83b315ed-9cc6-48aa-a774-8201da29c9dd)


---

### 评论 #3 — bdenhollander (2023-09-14T01:35:41Z)

5.6.1 was announced as [Linux only](https://github.com/RadeonOpenCompute/ROCm/releases/tag/rocm-5.6.1). This page gives a bit more information about future ROCm versioning:
https://rocm.docs.amd.com/en/latest/rocm.html#rocm-release-versioning

---

### 评论 #4 — ppanchad-amd (2024-05-14T15:29:03Z)

@shott92 Please try HIP SDK 5.7.1 (https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html). If resolved, please close ticket. Thanks!

---

### 评论 #5 — harkgill-amd (2024-07-12T18:44:40Z)

Hi @shott92, this is not a bug and the installation is working as intended. The version listed at [AMD HIP SDK for Windows](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html) is the ROCm version which correlates with that specific HIP SDK release. 

For example, the latest HIP SDK (6.1.0) will be installed when you select an installation for ROCm version 6.1.2. Not every Linux point release will have a corresponding SDK release for Windows.

---
