# [Issue]: ROCm 6.4.1 support for Fedora 42 (dnf/yum) — repo availability?

> **Issue #4899**
> **状态**: closed
> **创建时间**: 2025-06-08T15:57:58Z
> **更新时间**: 2025-08-08T03:20:26Z
> **关闭时间**: 2025-06-09T20:37:27Z
> **作者**: bbbdan777
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4899

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

Hey ROCm team,

I’m running Fedora 42 with an AMD Radeon RX 7900 XTX, and I’ve noticed that ROCm 6.4.1 isn’t yet available via the usual YUM-compatible repos. So far, I’ve only been able to install 6.3.1 using:

sudo dnf install rocm-dev rocm-utils rocminfo rocm-smi 
It looks like RHEL 9.6 already has access to ROCm 6.4.1 via a separate .rpm and repo (amdgpu-install-6.4.60401-1.el9.noarch.rpm), but that’s not working out-of-the-box for Fedora users. I checked https://repo.radeon.com/rocm/yum and it still stops at 6.3.

A bit of context:

I’m part of a growing group of Fedora users (we’ve got a Discord server too) who are interested in ROCm. Some of us are using ROCm for development or GPU workloads, and we’re just hoping for a bit more clarity on Fedora support going forward.

Is there a plan to publish 6.4.1+ to it soon?

Really appreciate the work you all are doing on ROCm — just wanted to bring this up in case it slipped under the radar.

Thanks!
Daniel

### Operating System

Fedora 42

### CPU

Ryzen 9 5950x

### GPU

RX 7900 XTX

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

Check available ROCm versions in DNF

sudo dnf info rocm-dev
❌ ROCm 6.4.1 not found
✅ Only 6.3.1 is available

Try to explicitly install 6.4.1

sudo dnf install rocm-dev-6.4.1
❌ Output: No match for argument

Check the YUM repo directly
Visit: https://repo.radeon.com/rocm/yum/
❌ No 6.4.1/ directory listed — only 6.3/ exists

Compare to RHEL 9.6
ROCm 6.4.1 is available via:

sudo dnf install https://repo.radeon.com/amdgpu-install/6.4.1/rhel/9.6/amdgpu-install-6.4.60401-1.el9.noarch.rpm
sudo dnf install rocm
✅ Successfully installs 6.4.1 on RHEL 9.6

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — Matthew-Jenkins (2025-06-09T03:12:24Z)

It's not a huge deal. Unlike cuda, rocm is typically bundled with whatever software is using it. So if you want rocm 6.4.1 then use the radeon torch wheels. https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/ or the rocm dist for whatever.

Rocm 6.4.1 will be in f43. https://packages.fedoraproject.org/pkgs/rocm-core/rocm-core/ I'm not sure why, but on fedora repo rocm gets locked in on ga and doesn't get updated except in rawhide. 

---

### 评论 #2 — trixirt (2025-06-09T15:42:09Z)

I maintain the Fedora ROCm stack.
Rawhide is always updated with the latest ROCm as @Matthew-Jenkins says.  When Rawhide branches for F<num> by and large that version is locked in because other packages in Fedora build against it, like pytorch.  Updating ROCm in F42, would mean updating pytorch and similar which would be difficult without breaking functionality in the fedora release, so we do not do that.  So if you need/want to use the latest, embrace the rolling release :P . 

Fedora Rawhide was updated to 6.4.1 a couple of weeks ago.  Only the packages that actually changed.
OpenSUSE TumbleWeed (i also maintain) update happened last week, here https://download.opensuse.org/repositories/science:/GPU:/ROCm/openSUSE_Tumbleweed/x86_64/

You can find me on Fedora's matrix by following the link here
https://fedoraproject.org/wiki/SIGs/AI-ML#Communication_/_Contact

---

### 评论 #3 — bbbdan777 (2025-06-09T20:37:27Z)

Thank you both very much for the information. I'll wait for fedora 43 to release, which will ship with the 6.4.1 ROCm, and use the Pytorch wheels in the meantime!

---

### 评论 #4 — Djip007 (2025-07-21T23:37:15Z)

With fedora you can use toolbox to test f43/Rawhide that have the 6.4.1 ROCm.

It is simple and you have no impact on you stable installation.

---

### 评论 #5 — geerlingguy (2025-08-08T03:20:26Z)

FYI Rawhide is now on 6.4.2, I've been using that for some Ryzen AI Max+ 395 testing (see [this comment](https://github.com/geerlingguy/beowulf-ai-cluster/issues/7#issuecomment-3166435861)).

---
