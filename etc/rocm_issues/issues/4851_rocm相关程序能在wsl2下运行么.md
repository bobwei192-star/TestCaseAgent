# rocm相关程序能在wsl2下运行么

> **Issue #4851**
> **状态**: closed
> **创建时间**: 2025-05-30T16:47:54Z
> **更新时间**: 2025-06-02T14:49:45Z
> **关闭时间**: 2025-05-31T11:37:17Z
> **作者**: zheliangzhi
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4851

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

没有查看清楚一股脑搭建好了才发现用不了。

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-05-30T19:06:48Z)

Hi @zheliangzhi, ROCm is supported on WSL. You can find more information, including the install instructions, over at [Install Radeon software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html). 

Could you please provide more information regarding the issue you're running into? The workload, steps to reproduce and error logs would be a good start.

---

### 评论 #2 — zheliangzhi (2025-05-31T02:15:28Z)

我7900xt使用wsl2 Ubuntu-24.04的时候，按照rocm文档搭建使用ComfyUI的步骤试过几次了，groups，rocminfo验证没问题，pytorch验证也没问题，但就是读不到gpu。是因为按照说明说的方法安装sudo  amdgpu-install --usecase=rocm --no-dkms这一步里缺失了gpu内核么？

---

### 评论 #3 — jjasoncool (2025-05-31T10:59:28Z)

I think it is basic etiquette to even use a translator to ask questions

---

### 评论 #4 — harkgill-amd (2025-06-02T13:29:08Z)

`-no-dkms` is used within a WSL environment as the Linux kernel driver is not needed. Instead, the WSL compatible Windows driver must be installed on the host [AMD Software: Adrenalin Edition™ 25.3.1 for WSL2](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-25-3-1.html). This driver is mandatory and without it, the GPU will not be detected within WSL. 

For more information, head over to the WSL prerequisites page https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#prerequisites

---

### 评论 #5 — zheliangzhi (2025-06-02T14:49:44Z)

Okay, I'll try again. Thank you.

---
