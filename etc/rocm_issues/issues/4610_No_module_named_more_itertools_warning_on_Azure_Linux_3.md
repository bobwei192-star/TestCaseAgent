# No module named more_itertools warning on Azure Linux 3

> **Issue #4610**
> **状态**: open
> **创建时间**: 2025-04-11T23:16:02Z
> **更新时间**: 2025-04-11T23:16:02Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4610

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

During the driver installation process on Azure Linux 3, you might encounter the `ModuleNotFoundError: No module named 'more_itertools'` warning. This warning is a result of the reintroduction of `python3-wheel` and `python3-setuptools` dependencies in the CMake of `amdsmi`, which requires `more_itertools` to build these Python libraries . This issue will be fixed in a future ROCm release. As a workaround, use the following command before installation.

```
sudo python3 -m pip install more_itertools
```
