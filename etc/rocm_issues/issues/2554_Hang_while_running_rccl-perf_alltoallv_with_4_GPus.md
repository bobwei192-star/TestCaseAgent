# Hang while running rccl-perf alltoallv with 4 GPus

> **Issue #2554**
> **状态**: closed
> **创建时间**: 2023-10-13T21:46:21Z
> **更新时间**: 2024-02-02T21:59:51Z
> **关闭时间**: 2024-02-02T21:59:51Z
> **作者**: Rmalavally
> **标签**: Under Investigation, 5.7.1, Workaround
> **URL**: https://github.com/ROCm/ROCm/issues/2554

## 标签

- **Under Investigation** (颜色: #0052cc)
- **5.7.1** (颜色: #b60205)
- **Workaround** (颜色: #A1F1A2)

## 描述

When RCCL is tested on a machine with no XGMI, a hang is observed while running rccl-perf alltoallv with 4 GPus.
As a workaround, set the value of the variable to 2 while running the tests,

NCCL_MAX_P2P_NCHANNELS=2

This issue is under investigation and will be fixed in a future release.


---

## 评论 (1 条)

### 评论 #1 — Rmalavally (2024-02-02T21:59:51Z)

This known issue was fixed in the ROCm 6.0 release. 

---
