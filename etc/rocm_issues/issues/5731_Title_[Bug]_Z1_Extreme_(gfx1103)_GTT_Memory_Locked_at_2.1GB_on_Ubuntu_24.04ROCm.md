# Title: [Bug] Z1 Extreme (gfx1103) GTT Memory Locked at 2.1GB on Ubuntu 24.04/ROCm 6.x/7.x

> **Issue #5731**
> **状态**: closed
> **创建时间**: 2025-12-02T16:34:18Z
> **更新时间**: 2025-12-29T15:38:15Z
> **关闭时间**: 2025-12-29T15:38:15Z
> **作者**: busybatteries-prog
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5731

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

[please retype all that in a plaint ext format to....pdf](https://github.com/user-attachments/files/23886190/please.retype.all.that.in.a.plaint.ext.format.to.pdf)

---

## 评论 (3 条)

### 评论 #1 — darren-amd (2025-12-03T15:29:14Z)

Hi @busybatteries-prog,

Thanks for reporting this issue. 

Regarding ollama not using GTT memory properly, I found a couple reports on this issue such as https://github.com/ollama/ollama/issues/5471, along with a linked PR: https://github.com/ollama/ollama/pull/13196. This appears to be an issue that they are actively addressing.

It also looks like you're trying to install the Ubuntu 22.04 packages and are unable to find packages for 24.04. We have packages that are available with instructions [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html) for Ubuntu 24.04. Please follow the instructions under Ubuntu -> 24.04 for both `ROCm installation` and `AMDGPU driver installation` and let me know if the issue persists, thanks!


---

### 评论 #2 — ianbmacdonald (2025-12-04T17:08:12Z)

Looks like a couple of issues (beyond the vibe created issue pdf) 🥇 

For your packaging dependency issue, it can be sorted out with a bit of apt foo, if the instructions in the comment above do not fix them.  If following the instructions fails, paste the output of `sudo apt update && apt upgrade -s` and it should be clear what is going on (Partial upgrade, apt pinning, etc.) 

For your GTT issue specifically, you need to confirm what you are actually telling amdgpu to do and what you have your BIOS configured for.  The output of these will help:

`$sudo dmesg | grep amdgpu | grep memory `

`$sudo dmesg | head -n 2`

---

### 评论 #3 — darren-amd (2025-12-29T15:38:15Z)

Thanks for the additional debug steps! I'm going to close this ticket out due to inactivity, but please feel free to reopen if the issue persists after the steps suggested above, thanks!

---
