# [Documentation]: please keep a single source of truth for "Known Issues". Inconsistency found.

> **Issue #2920**
> **状态**: open
> **创建时间**: 2024-02-22T00:20:48Z
> **更新时间**: 2024-02-22T02:10:11Z
> **作者**: ye-luo
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2920

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

I hope there is only one team making the release of ROCm.
There is a section in https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-23-40-rocm-6-0-2
```
Known Issues

    Running PyTorch with iGPU enabled + Discrete GPU enabled may cause crashes. See the Limitations section within the How To Guide for details.
    GPU reset may occur when running multiple heavy Machine Learning workloads at same time over an extended period of time.
    Intermittent gpureset errors may be seen with Automatic 1111 webUI with IOMMU enabled. Please see https://community.amd.com/t5/knowledge-base/tkb-p/amd-rocm-tkb for suggested resolutions.
    RX 7900 GRE may exhibit a hang rather than Out Of Memory error on BERT FP32 training loads.
    Soft hang observed when running multi-queue workloads.
```

None of these were mentioned at https://github.com/ROCm/ROCm/blob/develop/CHANGELOG.md

Could you please improve the accuracy and consistency of info in release notes?


### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (1 条)

### 评论 #1 — nartmada (2024-02-22T02:09:57Z)

@ye-luo, thank you for catching this error.  I will forward your info to the internal team.

---
