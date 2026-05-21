# Fix EULA link

> **Issue #2072**
> **状态**: closed
> **创建时间**: 2023-04-21T17:39:23Z
> **更新时间**: 2023-06-02T21:56:32Z
> **关闭时间**: 2023-06-02T21:56:32Z
> **作者**: samjwu
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2072

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- Rmalavally

## 描述

Broken link: https://www.amd.com/en/support/gpu-pro-eula

Affected Files:
`release/licensing.md`
`deploy/linux/install_overview.md`


---

## 评论 (5 条)

### 评论 #1 — Rmalavally (2023-05-03T18:33:52Z)

@samjwu I don't see installing_linux in 'understand'. Have you renamed it and moved it to https://github.com/RadeonOpenCompute/ROCm/tree/develop/docs/deploy/linux? 

Please confirm.

---

### 评论 #2 — samjwu (2023-05-03T19:03:28Z)

Yes, it was moved to https://github.com/RadeonOpenCompute/ROCm/blob/develop/docs/deploy/linux/install_overview.md. I have updated the issue description.

This commit https://github.com/RadeonOpenCompute/ROCm/commit/4a1c9ffcd2ab9e6d08fc98e07403e241740ac804 has the diff where I removed references to the EULA link. (`docs/understand/installing_linux.md` has moved to `docs/deploy/linux/install_overview.md`)

---

### 评论 #3 — Rmalavally (2023-05-03T19:17:18Z)

Perfect. Thanks so much!

---

### 评论 #4 — Rmalavally (2023-05-03T20:22:02Z)

I fixed both md files. Could you please review and merge the PR? Thanks so much.


---

### 评论 #5 — samjwu (2023-06-02T21:53:45Z)

https://github.com/RadeonOpenCompute/ROCm/pull/2105

---
