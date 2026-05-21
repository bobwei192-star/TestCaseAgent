# Will future versions add support for the 7000 series?

> **Issue #2130**
> **状态**: closed
> **创建时间**: 2023-05-11T17:45:05Z
> **更新时间**: 2024-04-07T17:57:24Z
> **关闭时间**: 2024-04-07T17:57:24Z
> **作者**: MomijiHanako
> **标签**: hardware:Radeon
> **URL**: https://github.com/ROCm/ROCm/issues/2130

## 标签

- **hardware:Radeon** (颜色: #2B113F)

## 描述

I would like to know,

---

## 评论 (3 条)

### 评论 #1 — Mushoz (2023-05-15T13:32:08Z)

It already supports the 7900 XTX and 7900 XT. You do need to compile Pytorch and Tensorflow manually right now to get it to work though. Examples can be found in this issue on how to do so: https://github.com/RadeonOpenCompute/ROCm/issues/1880

---

### 评论 #2 — briansp2020 (2023-09-04T15:33:16Z)

Are there still people who are waiting for 7900XTX support? Though the performance is still a bit poor, TensorFlow-upstream now runs when built on the latest ROCm release. I was looking into the status of ROCm support for 7900XTX and found a few issues opened by different people and wanted to link all to the issue I opened in MIOpen repo. Though there has not been any confirmation from the developer, I think the performance issues are due to insufficient optimization of MIOpen. 
https://github.com/ROCmSoftwarePlatform/MIOpen/issues/2342

---

### 评论 #3 — nartmada (2024-04-07T17:57:24Z)

@MomijiHanako, @Mushoz, @briansp2020, my apologies for not following up.

Since ROCm 5.7.1, there is support for the 7000 series GPUs.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

![image](https://github.com/ROCm/ROCm/assets/144284448/4e98e500-b7a4-4693-a6ad-d0049db2a5bb)


---
