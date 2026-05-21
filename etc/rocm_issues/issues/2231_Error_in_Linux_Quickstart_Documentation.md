# Error in Linux Quickstart Documentation

> **Issue #2231**
> **状态**: closed
> **创建时间**: 2023-06-09T12:32:20Z
> **更新时间**: 2023-06-09T19:56:24Z
> **关闭时间**: 2023-06-09T19:56:24Z
> **作者**: Malexandra-de
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2231

## 描述

On the page [https://rocm.docs.amd.com/en/latest/deploy/linux/quick_start.html](https://rocm.docs.amd.com/en/latest/deploy/linux/quick_start.html) there is an error in the `Add the repositories` Ubuntu 22.04 section. The line `echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' | sudo tee /etc/apt/preferences.d/rocm-pin-600` is misplaced and causes issues with apt.
