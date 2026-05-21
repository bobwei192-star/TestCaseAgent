# [Documentation] Explicit tensorflow wheel naming convention for installation

> **Issue #2327**
> **状态**: closed
> **创建时间**: 2023-07-21T15:21:23Z
> **更新时间**: 2024-10-01T16:59:36Z
> **关闭时间**: 2024-10-01T16:59:35Z
> **作者**: pierreantoineH
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2327

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- sunway513

## 描述

The compatibility matrix between Tensorflow and ROCm is indicated in : 
https://rocm.docs.amd.com/en/latest/release/3rd_party_support_matrix.html

Nevertheless it might not be obvious that the wheel naming convention is TFversion.0.ROCmversion which might lead user to install Tensorflow wheel for not the right ROCm version.

On https://rocm.docs.amd.com/en/latest/how_to/tensorflow_install/tensorflow_install.html , it is indicated : 
For details on tensorflow-rocm wheels and ROCm version compatibility, see:
https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/blob/develop-upstream/rocm_docs/tensorflow-rocm-release.md
which is much more explicit but did not contain the latest compatibility matrix. (i.e ROCm 5.6 & Tensorflow 2.12)


---

## 评论 (3 条)

### 评论 #1 — saadrahim (2023-07-21T21:24:22Z)

@sunway513 can you help assign this issue?

---

### 评论 #2 — ppanchad-amd (2024-05-14T14:55:52Z)

@pierreantoineH @saadrahim Internal ticket has been created to fix documentation. Thanks!

---

### 评论 #3 — harkgill-amd (2024-10-01T16:59:36Z)

Hi @pierreantoineH, this issue is addressed in https://github.com/ROCm/rocm-install-on-linux/commit/ff56cdbc23f3e751e066587fd65e528763ee5465. Going forward, the naming convention for the wheels will follow the TF version (First wheel to follow this was `2.16.1`). A note has also been added in the documentation to highlight the `TFversion.ROCmversion` format for older wheels.

---
