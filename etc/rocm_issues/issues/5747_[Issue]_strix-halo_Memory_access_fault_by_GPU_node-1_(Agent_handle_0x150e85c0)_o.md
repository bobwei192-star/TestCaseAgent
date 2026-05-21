# [Issue]: strix-halo : Memory access fault by GPU node-1 (Agent handle: 0x150e85c0) on address 0x7fdb980a6000. Reason: Page not present or supervisor privilege. Aborted (core dumped)

> **Issue #5747**
> **状态**: closed
> **创建时间**: 2025-12-08T14:47:23Z
> **更新时间**: 2026-01-08T10:34:34Z
> **关闭时间**: 2026-01-08T10:34:34Z
> **作者**: jmb-streamsets
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5747

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

Was working with:
     - kernel.x86_64 6.17.7-300.fc43, 
     - kernel.x86_64 6.17.8-300.fc43
 but not with:
     - kernel.x86_64 6.17.9-300.fc43

It is possible that would be linked to a firmware regression.


### Operating System

LSB Version:    n/a Distributor ID: Fedora Description:    Fedora Linux 43 (KDE Plasma Desktop Edition) Release:        43 Codename:       n/a

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

Strix Halo [Radeon Graphics / Radeon 8050S Graphics / Radeon 8060S Graphics]

### ROCm Version

VBIOS version: 113-STRXLGEN-001

### ROCm Component

_No response_

### Steps to Reproduce

Was working with:
     - kernel.x86_64 6.17.7-300.fc43, 
     - kernel.x86_64 6.17.8-300.fc43
 but not with:
     - kernel.x86_64 6.17.9-300.fc43

It is possible that would be linked to a firmware regression.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ianbmacdonald (2025-12-09T00:13:58Z)

You would need to show your firmware version to determine if you are just running the 0x83 that was rolled back a week ago.  Check out #5724 to see if this is a duplicate of that issue.



---

### 评论 #2 — amd-nicknick (2025-12-11T15:56:28Z)

Hi @jmb-streamsets, as pointed out by @ianbmacdonald, below is my suggested course of action to isolate the issue.
We've seen uptrend in this duplicate report because Fedora seems to have picked up the broken firmware.

* If you're on MES 0x83 (Check with `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info`):
  * Rollback to MES 0x80, check the `linux-firmware` package from your distro.
  * Upstream kernel firmware **after** https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/commit/?id=3d5c8135206cef364e7d353711b3e7358a90d152
* If you're on MES 0x80
  * Try disabling CWSR: Kernel parameter `amdgpu.cwsr_enable=0`
* If you're on MES <0x80
  * Update your kernel and firmware. For Ubuntu ensure you're on the OEM kernel **without** amdgpu DKMS.

---

### 评论 #3 — amd-nicknick (2025-12-26T08:00:36Z)

Hi @jmb-streamsets, are you still encountering the faults after reverting the firmware?

---

### 评论 #4 — amd-nicknick (2026-01-08T10:34:34Z)

Closing this issue due to inactivity for now, @jmb-streamsets, if you still encounter any problem with the above steps, feel free to reopen. Thanks!

---
