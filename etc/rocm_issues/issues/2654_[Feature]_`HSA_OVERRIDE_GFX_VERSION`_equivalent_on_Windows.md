# [Feature]: `HSA_OVERRIDE_GFX_VERSION` equivalent on Windows

> **Issue #2654**
> **状态**: closed
> **创建时间**: 2023-11-17T14:20:31Z
> **更新时间**: 2024-05-17T17:22:37Z
> **关闭时间**: 2024-05-17T17:22:37Z
> **作者**: pxl-th
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2654

## 描述

Is there an equivalent to `HSA_OVERRIDE_GFX_VERSION` on Windows?
On Linux this can be used to enable ROCm support for `gfx103x` other than `gfx1030`.

---

## 评论 (3 条)

### 评论 #1 — riverzhou (2023-12-02T15:02:41Z)

Same question.

---

### 评论 #2 — DGdev91 (2024-01-05T01:33:41Z)

I tried to run [Koboldcpp-rocm](https://github.com/YellowRoseCx/koboldcpp-rocm) on my RX 5700xt, on windows.
The "koboldcpp_rocm_files.zip" version comes with rocblas files packaged inside the zip, so i copied all the files related to gfx1030 changing the "1030" to "1010" using this script (seems like just renaming breaks something):
```
@echo off
setlocal enabledelayedexpansion

for %%F in (*1030*) do (
    set "newName=%%F"
    set "newName=!newName:1030=1010!"
    copy "%%F" "!newName!"
)

echo Copying completed.
pause
```

It outputs random gibberish, but i had a very similar issue as well on Linux when i tried to run autogptq-rocm, and it could be an issue related to just the 5700xt and rocblas.

If you have a different card, can you try that?


---

### 评论 #3 — ppanchad-amd (2024-05-17T17:22:37Z)

@pxl-th No, there’s no available option like that on Windows. Thanks!

---
