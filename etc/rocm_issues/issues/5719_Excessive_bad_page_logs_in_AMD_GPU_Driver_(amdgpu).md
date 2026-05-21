# Excessive bad page logs in AMD GPU Driver (amdgpu)

> **Issue #5719**
> **状态**: open
> **创建时间**: 2025-11-28T15:20:56Z
> **更新时间**: 2025-11-28T15:20:56Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.1
> **URL**: https://github.com/ROCm/ROCm/issues/5719

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Due to partial data corruption of Electrically Erasable Programmable Read-Only Memory (EEPROM) and limited error handling in the AMD GPU Driver(amdgpu), excessive log output might result when querying the reliability, availability, and serviceability (RAS) bad pages. This issue will be fixed in a future AMD GPU Driver(amdgpu) and ROCm release.
