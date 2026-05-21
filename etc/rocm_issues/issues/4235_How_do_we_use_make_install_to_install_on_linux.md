# How  do we use make install to install on linux?

> **Issue #4235**
> **状态**: open
> **创建时间**: 2025-01-07T03:21:36Z
> **更新时间**: 2025-01-27T18:57:35Z
> **作者**: inevity
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4235

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

I have just build the ROCm on a x86 archlinux's ubuntu 24.04 docker container.

Now want to install on the arch linux, but How install?

Since the build process also create deb/rpm package, so i think the created files(binary/so etc) could be used on arch linux. 

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-01-07T14:51:15Z)

Hi @inevity. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — lucbruni-amd (2025-01-07T16:38:29Z)

Hi @inevity,

ROCm is not officially supported on Arch Linux (see [here](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#operating-systems-and-kernel-versions)). I apologize for the inconvenience.

However, for non deb/rpm-based distributions, there is work in-progress for an independent installer to distribute ROCm (see [this comment](https://github.com/ROCm/ROCm/issues/1630#issuecomment-2427582413) from our team recently).

What I can do is recommend you try the ArchLinux ROCm packages (https://archlinux.org/packages/extra/any/rocm-hip-sdk/). Though they are official on Arch, AMD does not maintain or have any control over them, so I cannot guarantee your experience may be as free of issues as it would on setups listed on the compatibility matrix.

Please let me know if you have any more questions. Thank you!

---

### 评论 #3 — inevity (2025-01-08T11:54:43Z)

> Hi @inevity,
> 
> ROCm is not officially supported on Arch Linux (see [here](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#operating-systems-and-kernel-versions)). I apologize for the inconvenience.
> 
> However, for non deb/rpm-based distributions, there is work in-progress for an independent installer to distribute ROCm (see [this comment](https://github.com/ROCm/ROCm/issues/1630#issuecomment-2427582413) from our team recently).
> 
> What I can do is recommend you try the ArchLinux ROCm packages (https://archlinux.org/packages/extra/any/rocm-hip-sdk/). Though they are official on Arch, AMD does not maintain or have any control over them, so I cannot guarantee your experience may be as free of issues as it would on setups listed on the compatibility matrix.
> 
> Please let me know if you have any more questions. Thank you!


I know ROCm is not officially supported on Arch linux. But as a linux developer, i think the open source ROCm should be working on any modern linux by using simple make install( or use some cross build tool)
I have no idea about how you do cross compile/build for the rocm. I see in the ubuntu 24.04 image in ROCm build, it also create some rpm packages, though not many as deb pkgs. 
The rocm-hip-sdk now is for 6.2, not 6.3.1. And to upgrade to 6.3.1, need too many tiny boring things to do such as get sha256sum etc.  Maybe i will do on some spare time. 
I will look into the independent installer to distribute ROCm. 
Thank you.


---

### 评论 #4 — lucbruni-amd (2025-01-08T15:05:20Z)

Thanks for your response, and I agree with you. There is no guarantee on the release date for the self-contained installer, but it is a work in progress. Until then, since some of the components of ROCm are proprietary and distributed by deb/rpm, we do not support other distributions. We would also need to regular testing among these distributions to ensure users on those environments do not encounter unexpected issues. While we watch for these endeavors, let's track their progress in the issue from my previous reply which is still open.

---

### 评论 #5 — saadrahim (2025-01-08T15:58:31Z)

The request here is to understand how to run make install. This is independent of the Linux distribution. This request was not completed and as such should not have been closed.

---

### 评论 #6 — erik-nilcoast (2025-01-27T18:57:34Z)

@saadrahim I'd love some similar instructions on how to run make install. I'm all compiled, which took a damn long time, but now I want to use it :)

---
