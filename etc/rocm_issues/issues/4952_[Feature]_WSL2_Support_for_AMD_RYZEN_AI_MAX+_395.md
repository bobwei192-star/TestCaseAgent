# [Feature]: WSL2 Support for AMD RYZEN AI MAX+ 395

> **Issue #4952**
> **状态**: closed
> **创建时间**: 2025-06-22T18:26:31Z
> **更新时间**: 2026-02-06T13:30:36Z
> **关闭时间**: 2026-01-29T18:36:02Z
> **作者**: yaoman3
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/4952

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Suggestion Description

Description:
After installing the AMD GPU driver for WSL2, the system fails to recognize the Radeon 8060S graphics card (gfx1151). The only hardware detected is the CPU, and there are no signs of the GPU functioning within the Windows Subsystem for Linux environment. Could add the support for AMD RYZEN AI MAX+ 395 w/ Radeon 8060S?

Steps to Reproduce:

Install WSL2 on Windows 11.
Update to the latest kernel and install the necessary dependencies for AMD GPU support.
Install the AMDGPU drivers following the official installation guide.
Launch the WSL2 terminal and run a command to list hardware details (e.g., lspci or glxinfo).
Expected Behavior:
The system should detect the Radeon 8060S and display relevant GPU information alongside the CPU.

Actual Behavior:
Only the CPU is detected, and there is no acknowledgment of the Radeon 8060S in the hardware listings.

Environment:

WSL2 version: 2.4.13.0
Windows version: Windows 11
AMDGPU driver version: 25.6.1
Radeon model: 8060S

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (12 条)

### 评论 #1 — zl6977 (2025-09-02T14:00:09Z)

I am also looking forward to this.

BTW, I see there is already [preview ROCm for AI MAX+ 395](https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-from-tarballs). Is there any "preview WSL-support windows driver"?

---

### 评论 #2 — zl6977 (2025-09-25T10:31:39Z)

It is happy to see the newly released ROCm provide support on AI Max 300 Series, and also the new drivers.
May I ask if the WSL support for AI Max 300 Series is also coming on the way?

---

### 评论 #3 — xhefritoro (2025-10-01T14:04:44Z)

Any updates on ETA when this feature will be developed? 

---

### 评论 #4 — sebastienbo (2025-11-01T12:09:27Z)

I'm also blocked because of this. WSL2 is so important for coding agents. Please fix this.

---

### 评论 #5 — angieduan (2025-11-06T08:54:20Z)

It would be very exciting to get gfx1151 running in WSL2.

---

### 评论 #6 — liamhelmer (2025-11-09T17:45:26Z)

I'm also definitely interested. This seems like a big gap honestly: having AI Max+ 395 support for wsl2 seems like a core functionality that is missing from the product!

---

### 评论 #7 — ikx94 (2026-01-15T12:08:11Z)

also definitely interested and in need of this

---

### 评论 #8 — schung-amd (2026-01-27T16:26:25Z)

Hi all, sorry for the lack of response on this. We are aware that WSL support parity with Linux, both in terms of ROCm version and hardware support, is highly desired by the community, and are starting to look into a way to provide this.

When more details are available to share, I'll update here. Thanks for your interest, this is a good signal boost!

---

### 评论 #9 — zl6977 (2026-01-27T16:39:50Z)

Happy to hear the update from AMD developer, looking forward to at least **an estimated/non-strict timeline**, e.g., preview version in 6 months?
If the waiting time is too long, maybe the best for us is to ask IT to switch our OS to Linux...


> Hi all, sorry for the lack of response on this. We are aware that WSL support parity with Linux, both in terms of ROCm version and hardware support, is highly desired by the community, and are starting to look into a way to provide this.
> 
> When more details are available to share, I'll update here. Thanks for your interest, this is a good signal boost!



---

### 评论 #10 — schung-amd (2026-01-29T18:36:02Z)

Good news, this is happening faster than I thought, and I've been informed we actually have a preview available right now: https://github.com/ROCm/librocdxg/!

We're not quite ready for the official release so our docs haven't been updated, but this will be our WSL + ROCm solution moving forward. Please give this a go and report any issues you see.

I'm going to close this for our internal tracking purposes as this feature is on track to be delivered, but feel free to continue discussion here. If ROCDXG does not fully address this feature request we can reopen if necessary.

---

### 评论 #11 — rubentorresbonet (2026-02-06T13:28:18Z)

is the preview already available even if undocumented? I am in rocdxg-roct 1.1.0 but still finding issues @schung-amd 

---

### 评论 #12 — PeronGH (2026-02-06T13:30:36Z)

> is the preview already available even if undocumented? I am in rocdxg-roct 1.1.0 but still finding issues [@schung-amd](https://github.com/schung-amd)

Yes, it is already available. I documented my process [here](https://gist.github.com/PeronGH/506d063311fa746dd76b6c86a8bdfbdb).

---
