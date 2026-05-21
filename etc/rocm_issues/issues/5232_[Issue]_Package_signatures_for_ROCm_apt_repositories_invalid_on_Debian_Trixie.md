# [Issue]: Package signatures for ROCm apt repositories invalid on Debian Trixie

> **Issue #5232**
> **状态**: closed
> **创建时间**: 2025-08-27T18:22:34Z
> **更新时间**: 2025-10-17T16:56:18Z
> **关闭时间**: 2025-10-17T16:56:18Z
> **作者**: abrodersen
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5232

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- tcgu-amd

## 描述

### Problem Description

Because the signatures for the apt repo still use the SHA-1 hash, the signatures are no longer considered valid. The packages cannot be installed when using apt on Debian Trixie. This seems to be affecting numerous apt repositories, such as [VS Code](https://github.com/microsoft/vscode/issues/247505) and [Sublime Text](https://forum.sublimetext.com/t/debian-repo-getting-a-warning/76182).

The error message is as follows:
```
Reading package lists...
W: OpenPGP signature verification failed: https://repo.radeon.com/rocm/apt/6.4.3 noble InRelease: Sub-process /usr/bin/sqv returned an error code (1), error message is: Signing key on CA8BB4727A47B4D09B4EE8969386B48A1A693C5C is not bound:            No binding signature at time 2025-08-07T19:56:47Z   because: No binding signature at time 2025-08-07T19:56:47Z
E: The repository 'https://repo.radeon.com/rocm/apt/6.4.3 noble InRelease' is not signed.
```

### Operating System

Debian GNU/Linux 13 (trixie)

### CPU

AMD Ryzen 7 7800X3D 8-Core Processor

### GPU

AMD Radeon RX 5700 XT

### ROCm Version

6.4.3

### ROCm Component

_No response_

### Steps to Reproduce

Run the following on Debian Trixie:
```
curl -sSLf https://repo.radeon.com/rocm/rocm.gpg.key -o /etc/apt/keyrings/rocm.asc && \
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.asc] https://repo.radeon.com/rocm/apt/6.4.3 noble main" | \
    tee /etc/apt/sources.list.d/rocm.list && \
echo 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' | \
    tee /etc/apt/preferences.d/rocm-pin-600 && \
apt-get update && \
apt-get install -y --no-install-recommends \
    rocm
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-08-28T14:45:14Z)

Hi @abrodersen. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-09-02T18:15:51Z)

Hi @abrodersen, we are on our way to fully support Debian Trixie and this issue will be solved as a part of this effort in ROCm 7.x. Thanks! 

---

### 评论 #3 — tcgu-amd (2025-10-17T16:56:18Z)

Hi @abrodersen, now that 7.0.2 has been released, the issue should have been addressed. I will be closing this issue for now. Please let me know if you still find the issue persists and would like me to reopen. Thanks! 

---
