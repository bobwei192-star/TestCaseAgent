# AddressSanitizer fails in applications using texture references

> **Issue #2552**
> **状态**: closed
> **创建时间**: 2023-10-13T21:40:21Z
> **更新时间**: 2024-05-15T18:42:07Z
> **关闭时间**: 2024-05-15T18:42:07Z
> **作者**: Rmalavally
> **标签**: Resolved, 5.7.1
> **URL**: https://github.com/ROCm/ROCm/issues/2552

## 标签

- **Resolved** (颜色: #6DAE35)
- **5.7.1** (颜色: #b60205)

## 描述

The AddressSanitizer (ASan) feature may be unusable for HIP applications using texture references due to a runtime check failing on ASan instrumented texture references.

This known issue is under investigation and is expected to be fixed in a future release.

This issue is now resolved.


---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-05-15T14:52:44Z)

@Rmalavally Is this fixed in latest ROCm 6.1.1? Thanks!

---

### 评论 #2 — Rmalavally (2024-05-15T16:26:01Z)

> @Rmalavally Is this fixed in latest ROCm 6.1.1? Thanks!

Thanks for the follow up. 

Yes. This issue was fixed in the ROCm 6.1 release. I have updated the issue here to reflect this detail. 

---
