# AMD SMI CLI triggers repeated kernel errors on GPUs with partitioning support

> **Issue #5720**
> **状态**: closed
> **创建时间**: 2025-11-28T17:28:49Z
> **更新时间**: 2026-01-28T16:18:33Z
> **关闭时间**: 2026-01-28T16:18:33Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.1
> **URL**: https://github.com/ROCm/ROCm/issues/5720

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Running the `amd-smi` CLI on GPUs with partitioning support, such as the AMD
Instinct MI300 series, might produce repeated kernel error messages in the
system logs. This occurs when `amd-smi` attempts to open the GPU
partition device nodes `/dev/dri/renderD*` during the permission checks. On
GPUs with partitioning support, unconfigured partition devices are
intentionally invalid until configured. As a result, the AMD GPU Driver (amdgpu)
logs errors in `dmesg`, such as: 

```
amdgpu 0000:15:00.0: amdgpu: renderD153 partition 1 not valid!
```

These repeated kernel logs can clutter the system logs and may cause
unnecessary concern about GPU health. However, this is a non-functional issue
and does not affect AMD SMI functionality or GPU performance. This issue will
be fixed in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — prbasyal-amd (2026-01-28T16:18:33Z)

Resolved in ROCm 7.2.0.

---
