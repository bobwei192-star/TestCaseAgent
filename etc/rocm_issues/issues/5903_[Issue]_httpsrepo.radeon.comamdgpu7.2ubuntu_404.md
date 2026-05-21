# [Issue]: https://repo.radeon.com/amdgpu/7.2/ubuntu 404

> **Issue #5903**
> **状态**: closed
> **创建时间**: 2026-01-26T13:21:35Z
> **更新时间**: 2026-01-31T13:40:06Z
> **关闭时间**: 2026-01-31T13:40:06Z
> **作者**: yanite
> **标签**: AMD Radeon RX 7900 XTX, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5903

## 标签

- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

command not work at wsl2
`amdgpu-install -y --usecase=wsl,rocm --no-dkms` 

错误:9 https://repo.radeon.com/amdgpu/7.2/ubuntu noble Release
  404  Not Found [IP: 23.219.89.145 443]

install from https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html

### Operating System

Windows WSL2

### CPU

AMD 7950x

### GPU

RX 7900xtx

### ROCm Version

ROCM 7.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — peter247 (2026-01-27T12:14:47Z)

I had the same problem do a :-

amdgpu-install --uninstall --rocmrelease=all
apt purge amdgpu-install
apt autoremove

and start again , You will find the /etc/apt/sources.list.d/??? is a mix of the old and new repos .
https://github.com/ROCm/ROCm/issues/5881

---

### 评论 #2 — harkgill-amd (2026-01-27T21:22:20Z)

As @peter247 mentioned, give the steps from https://github.com/ROCm/ROCm/issues/5881#issuecomment-3786689561 a try to see if they resolve your issue.

---
