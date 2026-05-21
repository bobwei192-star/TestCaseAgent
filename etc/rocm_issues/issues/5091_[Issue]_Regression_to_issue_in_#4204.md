# [Issue]: Regression to issue in #4204

> **Issue #5091**
> **状态**: closed
> **创建时间**: 2025-07-23T03:01:57Z
> **更新时间**: 2025-09-16T17:51:27Z
> **关闭时间**: 2025-09-16T17:51:27Z
> **作者**: mvastola
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5091

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

cc: @ppanchad-amd,  @lucbruni-amd

Hi guys,
So it seems the issue I identified in https://github.com/ROCm/ROCm/issues/4204 has resurfaced. 

Unfortunately I can't immediately point to where/when the regression occurred, as last time the issue was ["fixed internally"](https://github.com/ROCm/ROCm/issues/4204#issuecomment-2701294095) and I admittedly haven't been keeping an eye on my amdgpu kernel module updates to be able to pinpoint which public commit (if any) the regression might be visible in.

What I can say is `apt dist-upgrade` has been failing for me for maybe a month now due to errors compiling the `amdgpu` DKMS module. I finally took 5 minutes to look at why it wasn't compiling tonight and the first thing I did -- hoping whatever the issue was had been fixed -- was to bump the apt repo I was using from https://repo.radeon.com/amdgpu/5.4.1/ to https://repo.radeon.com/amdgpu/6.4.2/. This didn't fix the problem. Next I googled the compile error and wound back at https://github.com/ROCm/ROCm/issues/4204 😄 .

Anyway, adding `unset TMPDIR` to the top of the pre-build script immediately fixed the problem. I'm happy to help troubleshoot if needed (and assuming the issue is even located in a public repo), but I'm hoping it'll be trivial on your end to see where the issue was re-introduced internally.

Please let me know if you need anything from me.

### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

AMD Ryzen Threadripper 2950X 16-Core Processor

### GPU

AMD Radeon RX 6600

### ROCm Version

AMD GPU DKMS Kernel Module from https://repo.radeon.com/amdgpu/ version 5.4.1 and 6.4.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-07-23T13:54:32Z)

@mvastola Thanks for reporting! We will continue with the investigation. Thanks!

---

### 评论 #2 — lucbruni-amd (2025-07-23T19:19:42Z)

Hi @mvastola, sorry to hear that the issue you (and I) had thought was resolved months ago has come back to haunt your system. 

I'm glad it didn't take much time for you to arrive at the same point as before and put in a local patch to fix it. Also, I appreciate your offer to help troubleshoot - unfortunately the repository these module releases are being built from is still internal, but I'll make sure this gets taken care of. I've also located a precise set of branches in this repository where the patch seems to have gotten lost in transit, affirming this as an actual regression.

I will contact our DKMS and CI teams to understand the branch creation and build processes a little better, although I assume this was a result of erroneously branching off a staging or release branch with an earlier minor version number that didn't include the patch.

Thanks for the report, and I'll let you know when there's an update.

---

### 评论 #3 — mvastola (2025-07-23T19:21:11Z)

Sounds good. Thanks!

---

### 评论 #4 — lucbruni-amd (2025-09-16T17:51:27Z)

Hi @mvastola,

Thanks for your patience. ROCm 7.0.0 is officially out - and with it, the fix for this regression.

I've verified the change is in the `pre-build.sh` script and I did not encounter conflicts with `libpam-tmpdir`.

Closing this issue (hopefully for good this time) as resolved. If you encounter any troubles with ROCm 7 feel free to open further Github issues.

Thanks!

---
