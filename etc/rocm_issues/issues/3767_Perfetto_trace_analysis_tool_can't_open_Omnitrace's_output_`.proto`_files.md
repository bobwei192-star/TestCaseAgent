# Perfetto trace analysis tool can't open Omnitrace's output `.proto` files

> **Issue #3767**
> **状态**: closed
> **创建时间**: 2024-09-20T21:25:02Z
> **更新时间**: 2025-01-10T14:57:57Z
> **关闭时间**: 2025-01-10T14:57:56Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/3767

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.2.1** (颜色: #BDBEE3)

## 描述

Perfetto can no longer open [Omnitrace](https://rocm.docs.amd.com/projects/omnitrace/en/docs-6.2.1) proto files. Loading Perfetto trace output `.proto` files in the latest version of [ui.perfetto.dev](ui.perfetto.dev) can result in a dialog with the message, "Oops, something went wrong! Please file a bug." The information in the dialog will refer to an "Unknown field type."

The workaround is to open the files with a previous version of the Perfetto UI found at [https://ui.perfetto.dev/v46.0-35b3d9845/#!/](https://ui.perfetto.dev/v46.0-35b3d9845/#!/).

---

## 评论 (2 条)

### 评论 #1 — sohaibnd (2024-12-02T16:07:34Z)

This is a known issue with Perfetto v47, also mentioned in the [Omnitrace docs](https://rocm.docs.amd.com/projects/omnitrace/en/latest/what-is-omnitrace.html):

![image](https://github.com/user-attachments/assets/04af2ccb-4b2f-4a8b-9673-b68cc2780430)


---

### 评论 #2 — peterjunpark (2025-01-10T14:57:56Z)

Fixed in ROCm 6.3.1.

---
