# hipBLASLt performance regression for specific GEMM configurations

> **Issue #6065**
> **状态**: open
> **创建时间**: 2026-03-25T23:24:56Z
> **更新时间**: 2026-03-25T23:25:54Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/6065

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.2.1** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

You might observe a noticeable performance regression if you’re using hipBLASLt with the following GPUs for LLMs with specific GEMM configurations:

#### AMD Instinct MI300X and MI325X GPUs

Affected GEMM configurations:

* 16384 × 16384 × 6656 (BBS, TN)

* 32768 × 8192 × 3072 (BBS, TN)

* 9728 × 8192 × 65536 (F8F8S, TN)

#### AMD Instinct MI350 Series GPUs

Affected GEMM configurations:

* 4096 × 4096 × 1 × 8192

* 4096 × 4096 × 1 × 16384

* 8192 × 8192 × 1 × 8192

* 8192 × 8192 × 1 × 16384

Due to this issue, you might also observe a slight increase in the test or inference time. This issue is resolved in the {fab}`github`[hipBLASLt develop branch](https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipblaslt) and will be part of a future ROCm release.
