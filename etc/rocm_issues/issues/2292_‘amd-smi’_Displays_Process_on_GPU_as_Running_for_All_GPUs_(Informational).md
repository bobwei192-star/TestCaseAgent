# ‘amd-smi’ Displays Process on GPU as Running for All GPUs (Informational)

> **Issue #2292**
> **状态**: closed
> **创建时间**: 2023-06-28T22:06:31Z
> **更新时间**: 2024-03-24T04:43:52Z
> **关闭时间**: 2024-03-24T04:43:52Z
> **作者**: Rmalavally
> **标签**: 5.6.0, Informational
> **URL**: https://github.com/ROCm/ROCm/issues/2292

## 标签

- **5.6.0** (颜色: #b60205)
- **Informational** (颜色: #c5def5)

## 描述

```amd-smi``` displays processes as running for all GPUs when it may be running only on one GPU. 

```amd-smi``` currently uses the Linux kernel's definition of running processes. Future implementations may use the Kernel Fusion Driver's (KFD) definition of running processes. 

For more detailed information, refer to the memory usage for each GPU.
