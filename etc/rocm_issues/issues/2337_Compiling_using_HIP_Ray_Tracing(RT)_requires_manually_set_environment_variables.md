# Compiling using HIP Ray Tracing(RT) requires manually set environment variables

> **Issue #2337**
> **状态**: open
> **创建时间**: 2023-07-27T15:26:43Z
> **更新时间**: 2024-12-17T16:12:32Z
> **作者**: saadrahim
> **标签**: Verified Issue, Windows, 5.5.1
> **URL**: https://github.com/ROCm/ROCm/issues/2337

## 标签

- **Verified Issue** (颜色: #0052cc)
- **Windows** (颜色: #c2e0c6)
- **5.5.1** (颜色: #bfd4f2)

## 描述

A beta version of HIP RT is available with the AMD HIP SDK for Windows. To enable HIP RT compilation from command line, add following environment variables in addition to the steps described in #2336
- HIP_ROOT_DIR = C:\Program Files\AMD\ROCm\5.5\ (Compile the blender with HIPRT)
- HIPRT_ROOT_DIR = folder structure should be folder name../dist/bin/release (Point HIPRT bitcode file (.bc from HIP SDK /bin directory) files.


---

## 评论 (3 条)

### 评论 #1 — simszeto (2023-08-11T17:50:14Z)

This is for compiling Blender only and a [PR ](https://projects.blender.org/blender/blender/pulls/110519)is opened to fix this. 

---

### 评论 #2 — nartmada (2024-04-21T15:25:50Z)

@saadrahim, please confirm if the issue has been fixed.  Thanks.

---

### 评论 #3 — ghost (2024-04-27T14:09:12Z)

> @saadrahim, please confirm if the issue has been fixed. Thanks.

sorry for me replying instead but yes it is fixed for 5.5, but for 5.7 it still doesn't detect 5.7 automatically on Windows at least and needs HIPRT_BITCODE to be set to the path for the hiprt "bitcode" file (hiprt02001_5.7_amd_lib_win.bc)

---
