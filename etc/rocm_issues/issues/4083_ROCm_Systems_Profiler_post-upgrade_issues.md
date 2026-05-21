# ROCm Systems Profiler post-upgrade issues

> **Issue #4083**
> **状态**: closed
> **创建时间**: 2024-12-03T22:19:33Z
> **更新时间**: 2024-12-20T23:09:18Z
> **关闭时间**: 2024-12-20T23:09:18Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4083

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.3.0** (颜色: #303737)

## 描述

In ROCm 6.3.0, the `omnitrace` package is now named `rocprofiler-systems`. As a result, running `apt install omnitrace` will fail to locate the package. Instead, use `apt install rocprofiler-systems`. See [ROCm Systems Profiler 0.1.0](https://rocm-stg.amd.com/en/latest/about/release-notes.html#rocm-systems-profiler-0-1-0).

When upgrading from ROCm 6.2 to 6.3, any existing `/opt/rocm-6.2/../omnitrace` folders are not automatically removed. To clean up these folders, manually uninstall Omnitrace using `apt remove omnitrace`.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2024-12-20T23:09:18Z)

Fixed in ROCm 6.3.1.

---
