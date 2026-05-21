# Support Ubuntu custom kernel

> **Issue #2458**
> **状态**: closed
> **创建时间**: 2023-09-15T02:35:18Z
> **更新时间**: 2024-01-21T23:09:46Z
> **关闭时间**: 2023-11-10T16:08:38Z
> **作者**: winstonma
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2458

## 描述

Currently AMD ROCm driver supports Ubuntu default kernel, but when I install DKMS module on kernel v6.5.3 I got the error from the log file.

```
In file included from /var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/ttm/backport/backport.h:15,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/include/kcl/backport/kcl_mm_backport.h: In function ‘kcl_get_user_pages_remote’:
/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/include/kcl/backport/kcl_mm_backport.h:36:38: error: passing argument 1 of ‘get_user_pages_remote’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   36 |         return get_user_pages_remote(tsk, mm, start, nr_pages, !!(gup_flags & FOLL_WRITE),
      |                                      ^~~
      |                                      |
      |                                      struct task_struct *
In file included from ./include/linux/scatterlist.h:8,
                 from ./include/linux/dma-mapping.h:11,
                 from /var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/include/kcl/kcl_dma_mapping.h:5,
                 from /var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/ttm/backport/backport.h:8:
./include/linux/mm.h:2397:46: note: expected ‘struct mm_struct *’ but argument is of type ‘struct task_struct *’
 2397 | long get_user_pages_remote(struct mm_struct *mm,
      |                            ~~~~~~~~~~~~~~~~~~^~
/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/include/kcl/backport/kcl_mm_backport.h:36:43: warning: passing argument 2 of ‘get_user_pages_remote’ makes integer from pointer without a cast [-Wint-conversion]
   36 |         return get_user_pages_remote(tsk, mm, start, nr_pages, !!(gup_flags & FOLL_WRITE),
      |                                           ^~
      |                                           |
      |                                           struct mm_struct *
./include/linux/mm.h:2398:42: note: expected ‘long unsigned int’ but argument is of type ‘struct mm_struct *’
 2398 |                            unsigned long start, unsigned long nr_pages,
      |                            ~~~~~~~~~~~~~~^~~~~
/var/lib/dkms/amdgpu/6.2.4-1646729.22.04/build/include/kcl/backport/kcl_mm_backport.h:36:64: warning: passing argument 5 of ‘get_user_pages_remote’ makes pointer from integer without a cast [-Wint-conversion]
   36 |         return get_user_pages_remote(tsk, mm, start, nr_pages, !!(gup_flags & FOLL_WRITE),
      |                                                                ^~~~~~~~~~~~~~~~~~~~~~~~~~
      |                                                                |
      |                                                                int
```

I am not sure but I guess it is caused by the flag settings problem at the very early stage. Would it be possible to get it supported? Thanks a lot

I attached the [make.log](https://github.com/RadeonOpenCompute/ROCm/files/12614979/make.log) for the reference.


---

## 评论 (14 条)

### 评论 #1 — nairboon (2023-11-09T12:59:18Z)

Probably #2451 needs to be fixed first.

---

### 评论 #2 — kentrussell (2023-11-10T16:08:38Z)

The 6.5.3 kernel isn't supported by ROCm currently (refer to https://rocm.docs.amd.com/en/docs-5.7.1/release/gpu_os_support.html for more info). The KCL (Kernel Compatibility Layer) team works on updating the kernel support, but 6.5.3 won't work out-of-the-box on ROCm 5.7.

That being said, when you install amdgpu-dkms, it installs the source code to /usr/src/amdgpu-$VERSION. It looks like the check fails here:
https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver/blob/master/include/kcl/backport/kcl_mm_backport.h#L29

If you want a quick-and-dirty workaround, just remove line 29, and 31-41. Or remove calls to kcl_get_user_pages_remote and replace them with the standard get_user_pages_remote() calls, with the right parameters:
long get_user_pages_remote(struct mm_struct *mm,
			   unsigned long start, unsigned long nr_pages,
			   unsigned int gup_flags, struct page **pages,
			   int *locked);

You can use dkms to rebuild the kernel at that point with the issues resolved, as a workaround for trying to use an unsupported kernel. Good luck!

---

### 评论 #3 — Herschdorfer (2023-11-10T19:39:29Z)

Im getting the same error but on 6.5.0

```
DKMS make.log for amdgpu-6.2.4-1664922.22.04 for kernel 6.5.0-10-generic (x86_64)
Fr 10 Nov 2023 20:34:10 CET
make: Entering directory '/usr/src/linux-headers-6.5.0-10-generic'
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
  You are using:           gcc-13 (Ubuntu 13.2.0-4ubuntu3) 13.2.0
  CC [M]  /var/lib/dkms/amdgpu/6.2.4-1664922.22.04/build/scheduler/sched_main.o
  CC [M]  /var/lib/dkms/amdgpu/6.2.4-1664922.22.04/build/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.2.4-1664922.22.04/build/ttm/ttm_tt.o
  CC [M]  /var/lib/dkms/amdgpu/6.2.4-1664922.22.04/build/amd/amdgpu/amdgpu_drv.o
In file included from /var/lib/dkms/amdgpu/6.2.4-1664922.22.04/build/ttm/backport/backport.h:15,
                 from <command-line>:
/var/lib/dkms/amdgpu/6.2.4-1664922.22.04/build/include/kcl/backport/kcl_mm_backport.h: In function ‘kcl_get_user_pages_remote’:
/var/lib/dkms/amdgpu/6.2.4-1664922.22.04/build/include/kcl/backport/kcl_mm_backport.h:36:38: error: passing argument 1 of ‘get_user_pages_remote’ from incompatible pointer type [-Werror=incompatible-pointer-types]
   36 |         return get_user_pages_remote(tsk, mm, start, nr_pages, !!(gup_flags & FOLL_WRITE),
      |                                      ^~~
      |                                      |
      |                                      struct task_struct *

```

---

### 评论 #4 — kentrussell (2023-11-10T20:54:39Z)

As I said above, the 6.5 kernel isn't supported by ROCm currently (refer to https://rocm.docs.amd.com/en/docs-5.7.1/release/gpu_os_support.html for more info). ROCm 5.7 works on 6.2, but we haven't tested it on newer kernels. But the steps above should help to work around it until 6.5 support lands in an official release.

---

### 评论 #5 — Herschdorfer (2023-11-11T07:38:54Z)

Ah sorry, for some reason I read 6.2 as 6.5.2. 

Thanks!

---

### 评论 #6 — winstonma (2023-11-13T04:38:06Z)

@Herschdorfer in my perspective I think AMD Driver dkms module works on 6.2 kernel that comes with Ubuntu 22.04.3 but it doesn't work on 6.2 kernel that built using pure source (e.g. [Mainline](https://kernel.ubuntu.com/mainline/)/[Zabbly](https://ubuntuhandbook.org/index.php/2023/08/install-latest-kernel-new-repository/)).

I am not sure what is the difference between the Ubuntu kernel and the vanilla Linux Kernel but I feel that they should be very similar. Also based on the error log and the driver source code that the [error function](https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver/blob/2a83b3a166ea27e10b5ecb9292965082f31c6b12/include/kcl/backport/kcl_mm_backport.h#L24C1-L24C1) have different definition based on build flags. So my gut feeling is if the right flag is being set, the driver compilation would go through.

---

### 评论 #7 — Herschdorfer (2023-11-13T08:31:32Z)

I'm actually on Ubuntu 23.10, which is not officially supported yet. I just thought I give it a try.

So I guess I have to wait for official support on this kernel version. 

---

### 评论 #8 — winstonma (2024-01-02T00:04:12Z)

> The 6.5.3 kernel isn't supported by ROCm currently (refer to https://rocm.docs.amd.com/en/docs-5.7.1/release/gpu_os_support.html for more info). The KCL (Kernel Compatibility Layer) team works on updating the kernel support, but 6.5.3 won't work out-of-the-box on ROCm 5.7.
> 
> That being said, when you install amdgpu-dkms, it installs the source code to /usr/src/amdgpu-$VERSION. It looks like the check fails here: https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver/blob/master/include/kcl/backport/kcl_mm_backport.h#L29
> 
> If you want a quick-and-dirty workaround, just remove line 29, and 31-41. Or remove calls to kcl_get_user_pages_remote and replace them with the standard get_user_pages_remote() calls, with the right parameters: long get_user_pages_remote(struct mm_struct *mm, unsigned long start, unsigned long nr_pages, unsigned int gup_flags, struct page **pages, int *locked);
> 
> You can use dkms to rebuild the kernel at that point with the issues resolved, as a workaround for trying to use an unsupported kernel. Good luck!

I agree making this compile would be a very simple thing (removing several lines of code, just make sure the function would not run into the code part that is not intended. That's why I think it is very doable on the driver side to make sure the driver code works with the default kernel flag.

---

### 评论 #9 — kentrussell (2024-01-02T15:03:00Z)

The issue is that they just hadn't finished the rebase required to support the 6.5 kernel at the time that ROCm 5.7 was branched (ROCm 5.7 kernel was based on 6.2). Similarly, 6.0 was branched off of a 6.3-based kernel. It looks like ROCm 6.1 should support the 6.5 kernel, based on my unofficial opinion. But at least in the interim we can get around the issue with the steps above. Support for 6.5 is coming, it just didn't align with the ROCm 6.0 branch date.

---

### 评论 #10 — winstonma (2024-01-11T09:44:39Z)

@kentrussell Thanks for the comment.

This morning [Ubuntu update it's  default kernel to 6.5](https://www.omgubuntu.co.uk/2024/01/ubuntu-2204-linux-6-5-kernel-update). I installed the kernel and the corresponding dkms module for ROCm 6.0 driver is built successfully. However the dkms module for custom module still can't be built.

ROCm 6.0 works on kernel 6.5 with the Ubuntu kernel. It doesn't work on kernel 6.5 (or even 6.4) with mainline kernel. So I guess kernel version is not the main issue here.

---

### 评论 #11 — kentrussell (2024-01-11T14:40:52Z)

The big thing is that "kernel version" is a bit of a nebulous concept, too. The stock Ubuntu 6.5 kernel will have different patches than some other kernel. Even some older 4.* based kernels have some patches from 6.2 or 6.3 backported in. So the official stance is "you need to use what we list as supported, since that's what the KCL guys test against and build patches for"

The unofficial stance is trying to figure out where installation fails. We have the KCL there to try to handle these things on a non-versioned basis (our old KCL was solely based on kernel version and was not nearly as reliable). If you are seeing specific compilation failures in the make.log file, then you can always manually edit it to reflect your kernel. If you're unsure of what you're seeing, you can attach your make.log here (the error will pop up during install to refer to /var/lib/dkms/some/path/here/build/make.log). 

Or if you're feeling even more adventurous, you can submit a patch to the ROCK-Kernel-Driver repo to fix the compilation if you want to get into the autoconf+m4 part of the KCL. There's no official upstream repo for the amdgpu-dkms code from their side, but if a PR gets put in the ROCK repo, I can make sure that it gets pulled internally by me or someone on the KCL team.

The KCL team will get to newer kernels and compatibility for it, as that's their job. Sometimes they just lag behind the most bleeding-edge kernels (or some of the less popular ones).

---

### 评论 #12 — winstonma (2024-01-11T23:28:06Z)

@kentrussell I totally agree that "kernel version" is a nebulous concept. As the title mentioned, I don't think kernel version is the reason I open this ticket. The reason I open this ticket is because initially my Ubuntu, running with factory 6.2 kernel, built the dkms driver without problem. But when I go to use mainline 6.2 kernel (or other version of the kernel), the dkms build fail. I am not complaining the driver is not working with the up-to-date kernel but I would rather urge the driver team to build the dkms module from the plain vanilla kernel and see if it works.

EDIT:
I would like to add a few lines
1. The mainline kernel I mentioned is from https://wiki.ubuntu.com/Kernel/MainlineBuilds
2. I am running ROCm 6.0 driver and it has problem building dkms module on mainline kernel 6.2

This is the command that I used to install the mainline kernel
```
# Install an app that help install mainline kernel
$ sudo add-apt-repository ppa:cappelikan/ppa
$ sudo apt update
$ sudo apt install mainline

# Install kernel 6.2, which should be supported by ROCm 5.7+
$ mainline install 6.2
# Here is the error message
ERROR (dkms apport): kernel package linux-headers-6.2.0-060200-generic is not supported
Error! Bad return status for module build on kernel: 6.2.0-060200-generic (x86_64)
$ dpkg -s amdgpu-install | grep '^Version:'
Version: 6.0.60000-1697589.22.04
```

The error message in the first post is the message I got since using the mainline kernel. The error message on the first post uses 6.5.X error message just because it was the log captured. I would like to say sorry if I confuses you.

Here is the conclusion of ROCm Driver 6.0 dkms building status:

| &nbsp; | &nbsp; |
|-- | ---- |
| Mainline 6.1   | ✅ |
| Mainline 6.2   | ❌, attached the [make.log](https://github.com/ROCm/ROCm/files/13910767/make.log) |
| Mainline 6.3   | ✅ |
| Mainline 6.4   | ✅ |
| Ubuntu HWE 6.5 | ✅ |
| Mainline 6.5 | ❌ |



---

### 评论 #13 — kentrussell (2024-01-17T14:11:08Z)

The 6.2 kernel issue should be resolved in the 6.1 release. It was a known quirk in that specific subtest that didn't make it into the branch build for ROCm 6.0. 

As for development in general, there is a kernel version listed in the dkms status of each build (or in the package name of amdgpu-dkms). This will indicate the base "vanilla" kernel version that was used for the DKMS branch. For example, ROCm 6.0 has "6.3.6" as the kernel portion. While backports will come to support other, newer kernel versions, that's usually the safest indicator to know what base kernel codebase was used for that release. Hopefully that helps a little bit.

---

### 评论 #14 — winstonma (2024-01-21T23:08:27Z)

Thanks @kentrussell. That would be helpful because which version of the kernel is needed to get the driver working by checking the version of the package `amdgpu-dkms`. Here is another command on Ubuntu that could check:

```bash
$ dpkg -s amdgpu-dkms | grep Version
Version: 1:6.3.6.60000-1697589.22.04
```

Which indicates that kernel version 6.3.6 is the base kernel.

---
