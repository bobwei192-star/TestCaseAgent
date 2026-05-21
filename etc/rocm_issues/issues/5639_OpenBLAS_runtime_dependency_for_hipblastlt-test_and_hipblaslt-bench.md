# OpenBLAS runtime dependency for hipblastlt-test and hipblaslt-bench

> **Issue #5639**
> **状态**: open
> **创建时间**: 2025-11-07T23:39:12Z
> **更新时间**: 2025-11-08T00:10:51Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/5639

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.1.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Running `hipblaslt-test` or `hipblaslt-bench` without installing the OpenBLAS development package results in the following error:
```
libopenblas.so.0: cannot open shared object file: No such file or directory
```
As a workaround, first install `libopenblas-dev` or `libopenblas-deve`, depending on the package manager used. The issue will be fixed in a future ROCm release. 
