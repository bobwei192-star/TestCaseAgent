# [Documentation]: Broken links in ROCm 6.2.0 Release notes

> **Issue #3512**
> **状态**: closed
> **创建时间**: 2024-08-02T23:34:19Z
> **更新时间**: 2024-08-15T19:42:02Z
> **关闭时间**: 2024-08-15T19:42:02Z
> **作者**: xelibrion
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/3512

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

Section: PyTorch support for Autocast
Sentence: For more information, see
[Automatic mixed precision](https://rocm.docs.amd.com/en/docs-6.2.0/how-to/rocm-for-ai/train-a-model#automatic-mixed-precision-amp).

### Attach any links, screenshots, or additional evidence you think will be helpful.

![Uploading Screenshot 2024-08-03 at 9.33.59 AM.png…]()


---

## 评论 (3 条)

### 评论 #1 — Sabrewarrior (2024-08-03T14:42:22Z)

https://github.com/ROCm/ROCm/pull/3515 fixed the links on the website

There is a missing .html before #automatic-mixed-precision-amp in [6.2.0.md](https://github.com/ROCm/ROCm/blob/develop/tools/autotag/templates/highlights/6.2.0.md?plain=1) line 118 (and probably the other fixes), but not really sure if its used on the website. It is used on github release highlights though https://github.com/ROCm/ROCm/releases/tag/rocm-6.2.0

---

### 评论 #2 — harkgill-amd (2024-08-07T13:41:28Z)

Thank you @xelibrion and @Sabrewarrior! The links have been fixed in [RELEASE.md](https://github.com/ROCm/ROCm/blob/develop/RELEASE.md) and will be updated in [6.2.0.md](https://github.com/ROCm/ROCm/blob/develop/tools/autotag/templates/highlights/6.2.0.md?plain=1) shortly as well.

---

### 评论 #3 — harkgill-amd (2024-08-15T19:42:02Z)

Both instances of broken links have now been fixed, will close out the ticket. Thanks again for the help.

---
