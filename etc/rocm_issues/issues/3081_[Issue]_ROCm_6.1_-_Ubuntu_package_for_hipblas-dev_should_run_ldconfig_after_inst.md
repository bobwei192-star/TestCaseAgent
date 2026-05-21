# [Issue] ROCm 6.1 - Ubuntu package for hipblas-dev should run ldconfig after install

> **Issue #3081**
> **状态**: closed
> **创建时间**: 2024-05-03T04:28:49Z
> **更新时间**: 2025-04-22T19:15:38Z
> **关闭时间**: 2025-04-22T19:15:37Z
> **作者**: linuxtek-canada
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3081

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

When installing hipblas-dev on Ubuntu using apt, the package installation should run ldconfig before completing.

We are testing building LocalAI using ROCm 6.1 based on an Ubuntu 22.04 image: rocm/dev-ubuntu-22.04:6.1.

Our build succeeds, but the execution fails with this error:

```
localai-1  | ./local-ai: error while loading shared libraries: libhipblas.so.2: cannot open shared object file: No such file or directory
```

We worked around the issue in our Dockerfile by manually calling ldconfig after the package installations, and were able to get everything running successfully.

This is due to the hipblas-dev package installation not running ldconfig, which is the [standard policy](https://www.debian.org/doc/debian-policy/ch-sharedlibs.html#ldconfig) when installing shared libraries.  Any AMD built deb package for Debian/Ubuntu should follow this policy:

```
Any such package must have the line activate-noawait ldconfig in its triggers control file (i.e. DEBIAN/triggers).
```
* /opt/rocm-6.1.0/lib isn't listed in /etc/ld.so.conf, it's in /etc/ld.so.conf.d.  However:
* If a file is added to  /etc/ld.so.conf.d/ and that location is included from /etc/ld.so.conf, it should follow this policy.
* /etc/ld.so.conf only has one line, and that is include /etc/ld.so.conf.d/*.conf, so anything in /etc/ld.so.conf.d/ is in /etc/ld.so.conf.
* If this is done as part of the package installation, it may not be needed as part of [post-installation instructions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/post-install.html).

### Operating System

Ubuntu 22.04 Jammy

### CPU

AMD Ryzen 7 7800X3D 8-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

hipBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — linuxtek-canada (2024-05-03T15:55:17Z)

Digging into this a bit more to confirm the package is missing the trigger, and so I can understand:

### Example - libc6 package

I downloaded the .deb for libc6 which also depends on a number of libraries, and adds new library files.  I extracted the control files, including the triggers:

```
apt-get download libc6
ar vx libc6_2.35-0ubuntu3.7_amd64.deb
mkdir control && tar -I zstd -xvf control.tar.zst -C control
ls -al  ./control
```

In the control directory, you can see the triggers file:

```
drwxr-xr-x. 1 root root    148 Apr 16 13:40 .
drwxr-xr-x. 1 root root    180 May  3 15:51 ..
-rw-r--r--. 1 root root     40 Apr 16 13:40 conffiles
-rw-r--r--. 1 root root   1353 Apr 16 13:40 control
-rw-r--r--. 1 root root  21606 Apr 16 13:40 md5sums
-rwxr-xr-x. 1 root root   7576 Apr 16 13:40 postinst
-rwxr-xr-x. 1 root root   1067 Apr 16 13:40 postrm
-rwxr-xr-x. 1 root root  17402 Apr 16 13:40 preinst
-rw-r--r--. 1 root root    930 Apr 16 13:40 shlibs
-rw-r--r--. 1 root root 151495 Apr 16 13:40 symbols
-rw-r--r--. 1 root root  85281 Apr 16 13:40 templates
-rw-r--r--. 1 root root     72 Apr 16 13:40 triggers
```
Which contains the expected command to run ldconfig:

```
# Triggers added by dh_makeshlibs/13.6ubuntu1
activate-noawait ldconfig
```

### Example - hipblas-dev

Comparing this to the hipblas-dev package, I ran these commands to download the .deb file, extract the control files and examine:

```
apt-get download hipblas-dev
ar vx hipblas-dev_2.1.0.60100-82~22.04_amd64.deb
mkdir control && tar -xvf control.tar.gz -C control
ls -al ./control
```

This is what I see:

```
drwxr-xr-x. 1 root root  54 May  3 15:53 .
drwxr-xr-x. 1 root root 202 May  3 15:53 ..
-rw-r--r--. 1 root root 279 Apr 12 04:46 control
-rw-r--r--. 1 root root 694 Apr 12 04:46 md5sums
-rw-r--r--. 1 root root   0 Apr 12 04:46 postinst
-rw-r--r--. 1 root root   0 Apr 12 04:46 prerm
```

So we are missing the expected triggers at the very least.




---

### 评论 #2 — ppanchad-amd (2024-05-07T15:16:58Z)

@linuxtek-canada Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — harkgill-amd (2025-02-18T20:09:01Z)

Hi @linuxtek-canada, ROCm supports multi-version installations and package management tools such as Spack which are difficult to manage alongside consistent use of `ldconfig` as a post install trigger. With respect to this, we opted towards allowing users to manage their own environments with either `LD_LIBRARY_PATH `or `ldconfig `as a post-install instruction. 

The ROCm libraries utilize `RUNPATH` to locate and link other dependent components. Similarly, there are two solutions when an external application needs to link a specific component library:

1. Compile the application using llvm from /opt/rocm-<ver>/bin/amdclang or /opt/rocm-<ver>/llvm/bin/clang. The compiler itself will add opt/rocm-<ver>/lib in RUNPATH
2. Manually add the /opt/rocm-<ver>/lib in LD_LIBRARY_PATH or ldconfig

---

### 评论 #4 — harkgill-amd (2025-04-22T19:15:37Z)

Closing this one out. Feel free to leave a comment if you have any additional questions.

---
