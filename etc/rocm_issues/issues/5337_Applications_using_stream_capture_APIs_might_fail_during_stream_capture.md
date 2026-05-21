# Applications using stream capture APIs might fail during stream capture

> **Issue #5337**
> **状态**: open
> **创建时间**: 2025-09-16T15:26:53Z
> **更新时间**: 2026-03-06T15:44:58Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/5337

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Applications using ``hipLaunchHostFunc`` with stream capture APIs might fail to capture graphs during stream capture, and return `hipErrorStreamCaptureUnsupported`. This issue resulted from an update in ``hipStreamAddCallback``. This issue will be fixed in a future ROCm release.
