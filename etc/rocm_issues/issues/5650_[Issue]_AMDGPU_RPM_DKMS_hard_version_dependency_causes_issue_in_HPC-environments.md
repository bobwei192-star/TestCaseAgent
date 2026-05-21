# [Issue]: AMDGPU RPM DKMS hard version dependency causes issue in HPC-environments

> **Issue #5650**
> **状态**: closed
> **创建时间**: 2025-11-11T10:44:54Z
> **更新时间**: 2026-01-21T20:58:41Z
> **关闭时间**: 2026-01-21T20:58:41Z
> **作者**: tuxwielder
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5650

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

We are running a HPC-cluster (on Alma 8) with mixed AMD and Nvidia systems. We typically build compute node images on our headnode which are then deployed to our compute nodes.

The AMDGPU requires dkms = 3.1.1 whereas Nvidia nowadays installs dkms-3.2.2.

Can we lose the dependency on a specific DKMS version? 

### Operating System

Alma Linux 8

### CPU

AMD EPYC 9554 64-Core Processor

### GPU

AMD MI300A (target system)

### ROCm Version

7.1

### ROCm Component

_No response_

### Steps to Reproduce

Have dkms 3.2.2 installed and then try to 'dnf install amdgpu-dkms'.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (12 条)

### 评论 #1 — tcgu-amd (2025-11-11T18:06:25Z)

@tuxwielder, thanks for reaching out! To avoid bugs and to ensure stability, I don't think it is possible to drop dkms version dependency unfortunately. I am not sure about how your workflow functions, but I would avoid mixing nvidia/amdgpu builds/environment since the two ecosystems were never designed to work side-by-side. 

---

### 评论 #2 — saadrahim (2025-11-11T18:17:22Z)

Hi @tuxwielder ,
Is your request to chang the dkms dependency of AMD GPU to dkms >= 3.1.1 instead of dkms ==3.1.1?

---

### 评论 #3 — tuxwielder (2025-11-11T18:38:05Z)

> Hi [@tuxwielder](https://github.com/tuxwielder) , Is your request to chang the dkms dependency of AMD GPU to dkms >= 3.1.1 instead of dkms ==3.1.1?

Hi @saadrahim,

Yes, that is my request (>=3.1.1). We depend on a number of applications that require DKMS; amdgpu, nvidia, and ZFS modules. All require "current" DKMS versions, only AMD (thus far) requires a specific version.

---

### 评论 #4 — tuxwielder (2025-11-11T18:43:47Z)

> [@tuxwielder](https://github.com/tuxwielder), thanks for reaching out! To avoid bugs and to ensure stability, I don't think it is possible to drop dkms version dependency unfortunately. I am not sure about how your workflow functions, but I would avoid mixing nvidia/amdgpu builds/environment since the two ecosystems were never designed to work side-by-side.

Understandable, but not very practical in some HPC-environments. We PXE/Grub-boot our compute nodes using hybridised images. Although the images can be node-specific, large parts of the libraries are offered through the network (from a head/storage node). The headnode is not equiped with a GPU (of any vendor, well I suppose it has an elementary "VGA"-like GPU but I digress), but needs to offer the libraries and to be able to build the kernel modules (for the images).

I think this is not an uncommon pattern for HPC sites. 

---

### 评论 #5 — tuxwielder (2025-11-11T23:08:20Z)

As an extra note, the conflict is actually against dkms as provided by epel:

```
...
  - cannot install both dkms-3.1.1-1.el8.noarch from amdgpu and dkms-3.2.2-1.el8.noarch from @System
  - cannot install both dkms-3.2.2-1.el8.noarch from epel and dkms-3.1.1-1.el8.noarch from amdgpu
  - package amdgpu-dkms-1:6.16.6-2238411.el8.noarch from @commandline requires dkms = 3.1.1, but none of the providers can be installed
  - conflicting requests
...
```

Epel being enabled is pretty standard I think?

---

### 评论 #6 — Mystro256 (2025-11-12T19:31:57Z)

> The AMDGPU requires dkms = 3.1.1 whereas Nvidia nowadays installs dkms-3.2.2.

Are you sure this is correct? amdgpu should require (dkms <= 3.1.2 or dkms >= 3.1.4), as it is broken with 3.1.3. Any version excluding 3.1.3 should be able to be used.

A potential problem is that we supply a tested version of dkms in the amdgpu repository and the official rocm docs recommends prioritising the amdgpu repo over EPEL.
See:
https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.3.3/install/install-methods/package-manager/package-manager-rhel.html
it mentions "priority=50". Default priority should be 99, and lower number means high priority. This means when you add the amdgpu repo, it will consider the amdgpu dkms package a higher priority. This has nothing to do with the amdgpu-dkms package itself.

So if you want to use the EPEL version of dkms, please make sure you configure your amdgpu repository to not specify priority, or set it to something higher than EPEL (likely 99 by default).

It should be noted that EPEL is not a fully tested product, and is community supported. Using latest dkms from EPEL is not verified by Redhat nor AMD. Please use at your own risk.

If this resolves your issue, I'm happy to ask the documentation team to clarify this on the rocm docs page.

Thanks

---

### 评论 #7 — Mystro256 (2025-11-12T19:50:23Z)

> Epel being enabled is pretty standard I think?

Yes, but as I mentioned before, it's not a verified product. Using RHEL's default repositories are supported by RH, using AMD's repositories are supported by AMD, and using EPEL is community supported (Fedora community). If you run into issues using dkms from EPEL, this is not something we can fix since it is managed by the Fedora community, and you will have to file bugs with them.

An example is when 3.1.3 dropped, it broke the amdgpu-dkms package, but they did update to 3.1.4, which resolved the issue. We did our diligence to make sure the package avoids any version newer or older, but we also supply a copy of dkms that we test against, for users who want more reassurance of stability.

---

### 评论 #8 — Mystro256 (2025-11-12T21:50:44Z)

Ah I think I see the issue here, it seems like someone added the dependency specifically for the rhel 8 package.

Let me investigate and get back to you.

---

### 评论 #9 — sarianpo-amd (2025-11-14T18:23:00Z)

DKMS dependency for RHEL8 will be reverted on Monday.

---

### 评论 #10 — sarianpo-amd (2025-11-19T21:09:21Z)

The changes can be merged on Dec 2nd.

As a short-term solution, you can use the 7.0 release.

---

### 评论 #11 — tcgu-amd (2025-12-09T18:59:48Z)

@tuxwielder can you verify if the issue has been resolved for you? Thanks! 

---

### 评论 #12 — tcgu-amd (2026-01-21T20:58:41Z)

Closing this issue since it has been resolved. 

---
