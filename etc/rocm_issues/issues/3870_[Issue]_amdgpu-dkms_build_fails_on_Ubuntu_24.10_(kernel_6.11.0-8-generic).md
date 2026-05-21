# [Issue]: amdgpu-dkms build fails on Ubuntu 24.10 (kernel 6.11.0-8-generic)

> **Issue #3870**
> **状态**: closed
> **创建时间**: 2024-10-06T22:54:36Z
> **更新时间**: 2025-02-13T09:43:10Z
> **关闭时间**: 2024-10-08T13:57:51Z
> **作者**: fornellas
> **标签**: AMD Radeon RX 7900 XT, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3870

## 标签

- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

amdgpu-dkms build fails:

```
Performing actions...
(Reading database ... 316051 files and directories currently installed.)
Removing qtchooser (66-2build2) ...
Setting up amdgpu-dkms (1:6.8.5.60202-2041575.24.04) ...
Removing old amdgpu-6.8.5-2041575.24.04 DKMS files...
Deleting module amdgpu-6.8.5-2041575.24.04 completely from the DKMS tree.
Loading new amdgpu-6.8.5-2041575.24.04 DKMS files...
Building for 6.11.0-8-generic
Building for architecture x86_64
Building initial module for 6.11.0-8-generic
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.crash'
Error! Bad return status for module build on kernel: 6.11.0-8-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.8.5-2041575.24.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status 10
Processing triggers for man-db (2.12.1-3) ...
Errors were encountered while processing:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)
Setting up amdgpu-dkms (1:6.8.5.60202-2041575.24.04) ...
Removing old amdgpu-6.8.5-2041575.24.04 DKMS files...
Deleting module amdgpu-6.8.5-2041575.24.04 completely from the DKMS tree.
Loading new amdgpu-6.8.5-2041575.24.04 DKMS files...
Building for 6.11.0-8-generic
Building for architecture x86_64
Building initial module for 6.11.0-8-generic
ERROR: Cannot create report: [Errno 17] File exists: '/var/crash/amdgpu-dkms.0.crash'
Error! Bad return status for module build on kernel: 6.11.0-8-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.8.5-2041575.24.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status 10
Errors were encountered while processing:
 amdgpu-dkms
```

From the `make.log` we can find various errors such as:

```
/tmp/amd.0wFA7BzU/scheduler/./gpu_scheduler_trace.h:60:1: error: macro "__assign_str" passed 2 arguments, but takes just 1
```

The root cause seems to be https://github.com/torvalds/linux/commit/2c92ca849fcc, which changed the arguments for the macro on kernel 6.10, so bulid fails (isn't `__` prefix for internal stuff that shouldn't be used anyway?).

### Operating System

Ubuntu 24.10 (Oracular Oriole)

### CPU

AMD Ryzen 7 3700X 8-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

Just try to install the package & bulid it on 6.11.0-8-generic.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Ubuntu 24.10 is still in development, but [is set to be released in 4 days](https://www.omgubuntu.co.uk/2024/05/ubuntu-24-10-release-date#:~:text=Canonical%20has%20published%20a%20draft,on%20Thursday%20October%2010%2C%202024.).

---

## 评论 (12 条)

### 评论 #1 — fornellas (2024-10-06T22:56:33Z)

PS: full build log [make.log](https://github.com/user-attachments/files/17271163/make.log)


---

### 评论 #2 — ghost (2024-10-07T05:31:43Z)

I have very similar failure on 22.04 as well. Not that I care much, I hope I'll get 3090 soon and forget AMD as a nightmare.

---

### 评论 #3 — matthiasfostel (2024-10-07T10:09:13Z)

Same issue on 24.04 with last two kernels downloaded from apt.

Edit: Make file:

[make.log](https://github.com/user-attachments/files/17276921/make.log)


---

### 评论 #4 — harkgill-amd (2024-10-08T13:57:51Z)

Hi @fornellas, the 6.11.0 kernel is not currently supported by ROCm 6.2 as highlighted in the [Compatibility Matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#operating-systems-and-kernel-versions). This issue will be addressed in a future release once support is announced.

---

### 评论 #5 — fornellas (2024-10-08T20:48:31Z)

@harkgill-amd this is a bit of a sorry state we're in:

- The [newest supported kernel is 6.8](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#operating-systems-and-kernel-versions).
- [6.8 was released on March 2024 and wend EOL on May 2024](https://en.wikipedia.org/wiki/Linux_kernel_version_history#Releases_6.x.y).
- Yes, distros do security patches after kernel EOL, but AMD being stuck to old kernels, forces users to be stuck with it.
- This means old software, lack of newer kernel features / driver support for other peripherals etc.
- Eg: in my case, I'm after KDE6 due to its Wayland fractional scaling, which is a _game changer_ for people with limited vision like me.

It'd be best that these drivers were distributed by Ubuntu & others to begin with, to avoid all this hassle... in the absence of that, do we have a concrete plan to support current kernels?

---

### 评论 #6 — derfasthirnlosenick (2024-11-03T06:30:23Z)

I suppose this will need to be fixed relatively soon, as RDNA4 is promoted for AI workloads and support was added in the 6.11 kernel.

And now with Ubuntu 24.10 out (which comes with 6.11), more users will run into this issue.

---

### 评论 #7 — bigcat88 (2024-11-03T21:00:45Z)

I have already encountered a problem where I can't update the Linux kernel with the driver for my Bluetooth card (it needs kernel 6.10) because I have a 7900XTX and I need ROCM to work.

I think other owners who buy new motherboards on X870(e) chipsets with new peripherals for which there are no drivers in kernel 6.10 and who have an AMD video card will be just as unpleasantly surprised.

---

### 评论 #8 — Snuupy (2024-11-07T10:00:52Z)

kubuntu 24.10 was released on Oct 10, 2024 with kernel 6.11. There is no ability to downgrade the kernel to 6.8 so users like me are stuck between choosing between KDE, or rocm on ubuntu 24.04. Please update compatibility for ubuntu 24.10 and/or kernel 6.11.

---

### 评论 #9 — panzi (2024-11-23T20:30:41Z)

Having the same issue using TuxedoOS, which is just Kubuntu plus some tools for their hardware. Would have liked to use my GPU in Blender Cycles and was negatively surprised when it said it didn't find any compatible devices (no HIP support). Trying to install the official driver gave the mentioned compiler error (and warnings about missing function declarations). This was a very expensive GPU for me to buy. First time I bought AMD.

[make.log](https://github.com/user-attachments/files/17882461/make.log)

**Edit:** Turns out TuxedoOS' out of the box drivers are basically all I need! I just had to also to install `libamdhip64-5` and more importantly my user wasn't in the `render` group, but `/dev/kfd` requires that group so you can access the render device. Added the group to my user, rebooted, everything works! (I vaguely remember to have installed other libraries and rocm stuff via apt-get, but don't remember the details. The group was probably all I needed anyway.)

---

### 评论 #10 — rajo (2024-11-29T11:24:51Z)

Similar here: just got me an Asus Vivobook with an Ryzen AI 365 + Radeon 880M; Ubuntu 24.04 is a tad too old for the new hardware, it just works better with 24.10 -- but then I can't use all the nice GPU acceleration... So with all the new hardware that is out there it would be nice, if the new kernels would be supported as well.

---

### 评论 #11 — ali-layken (2024-12-08T20:39:28Z)

I was able to install amdgpu-dkms on debian 6.11.10 using the fix in [#3036](https://github.com/ROCm/ROCm/issues/3036#issuecomment-2233511553). Run `uname -m` and make sure it says `x86_64`  or something appropriate and then use the x86 objtool: `apt install amdgpu-dkms`

---

### 评论 #12 — mbitsnbites (2025-02-13T09:23:10Z)

For the record, Ubuntu 24.04 LTS recently moved from kernel 6.8 to 6.11, and this build error in amdgpu-dkms (`macro "__assign_str" passed 2 arguments, but takes just 1`) prevented the kernel upgrade.

**Edit:** The solution was to uninstall amdgpu-dkms (was on 6.2.x), and install amdgpu-install 6.3.2 (instructions here: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html).

---
