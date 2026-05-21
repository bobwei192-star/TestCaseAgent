# Uncorrectable errors are undetected after poison consumption testing

> **Issue #3192**
> **状态**: closed
> **创建时间**: 2024-05-30T18:06:25Z
> **更新时间**: 2024-05-31T15:24:06Z
> **关闭时间**: 2024-05-31T15:23:41Z
> **作者**: peterjunpark
> **标签**: Verified Issue, AMD Instinct MI300X, 6.1.2
> **URL**: https://github.com/ROCm/ROCm/issues/3192

## 标签

- **Verified Issue** (颜色: #0052cc)
- **AMD Instinct MI300X** (颜色: #ededed)
- **6.1.2** (颜色: #805A56)

## 描述

During poison consumption testing, the injection of uncorrectable errors can fail to generate an interrupt to the driver, resulting in undetected errors. This can result in reliability and recovery issues on MI300X accelerator-based setups.

This issue has been investigated and will be fixed in a future release.
