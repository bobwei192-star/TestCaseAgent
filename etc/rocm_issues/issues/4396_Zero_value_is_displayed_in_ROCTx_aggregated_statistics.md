# Zero value is displayed in ROCTx aggregated statistics

> **Issue #4396**
> **状态**: closed
> **创建时间**: 2025-02-19T20:00:18Z
> **更新时间**: 2025-05-05T16:10:53Z
> **关闭时间**: 2025-05-05T16:10:53Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.3.3
> **URL**: https://github.com/ROCm/ROCm/issues/4396

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.3.3** (颜色: #aaaaaa)

## 描述

The ROCTx markers are standalone markers within the ROCProfiler-SDK library. Each marker reports only a single timestamp, which is recorded as the `start_timestamp` and `end_timestamp`. As a result, the value for aggregated statistics presented in `TotalDurationNs`, `maxNs`, and `minNs`, is zero. The zero value indicates that the actual execution time is not associated with the markers, which is an expected behavior.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2025-05-05T16:10:45Z)

Resolved in 6.4.0

---
