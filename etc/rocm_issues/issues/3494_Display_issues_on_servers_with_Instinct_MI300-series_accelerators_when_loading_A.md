# Display issues on servers with Instinct MI300-series accelerators when loading AMDGPU driver

> **Issue #3494**
> **状态**: open
> **创建时间**: 2024-08-02T18:24:37Z
> **更新时间**: 2024-08-02T18:24:38Z
> **作者**: peterjunpark
> **标签**: Verified Issue, AMD Instinct MI300X, AMD Instinct MI300A, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3494

## 标签

- **Verified Issue** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **AMD Instinct MI300A** (颜色: #ededed)
- **6.2.0** (颜色: #31778C)

## 描述

AMD Instinct MI300-series accelerators and third-party GPUs such as the Matrox G200 have an issue impacting video output. The issue was reproduced on a Dell server model PowerEdge XE9680. Servers from other vendors utilizing Matrox G200 cards may be impacted as well. This issue was found with ROCm 6.2.0 but is present in older ROCm versions.

The AMDGPU driver shipped with ROCm interferes with the operation of the display card video output. On Dell systems, this includes both the local video output and remote access via iDRAC. The display appears blank (black) after loading the `amdgpu` driver modules. Video output impacts both terminal access when running in `runlevel 3` and GUI access when running in `runlevel 5`. Server functionality can still be accessed via SSH or other remote connection methods.
