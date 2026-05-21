# Error llvm build cmake in rhel and fedora  ERROR: ambiguous python shebang

> **Issue #3135**
> **状态**: closed
> **创建时间**: 2024-05-16T08:10:35Z
> **更新时间**: 2024-10-04T14:03:20Z
> **关闭时间**: 2024-10-04T14:03:20Z
> **作者**: perovskikh
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon VII
> **URL**: https://github.com/ROCm/ROCm/issues/3135

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon VII** (颜色: #ededed)

## 描述

### Problem Description

OS:
NAME="Red Hat Enterprise Linux"
VERSION="9.4 (Plow)"


```
[3922/3922] Generating ../../bin/llvm-readelf
[2/3] Run CPack packaging tool...
CPack: Create package using RPM
CPack: Install projects
CPack: - Install project: LLVM []
CPack: Create package
CPackRPM: Will use GENERATED spec file: /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/SPECS/llvm.spec
CPackRPM:Debug: You may consult rpmbuild logs in: 
CPackRPM:Debug:    - /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/rpmbuildllvm.err
CPackRPM:Debug: *** + umask 022
+ cd /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/BUILD
+ mv /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/tmpBBroot
+ RPM_EC=0
++ jobs -p
+ exit 0
+ umask 022
+ cd /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/BUILD
+ '[' /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux '!=' / ']'
+ rm -rf /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux
++ dirname /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux
+ mkdir -p /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM
+ mkdir /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux
+ '[' -e /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux ']'
+ rm -rf /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux
+ mv /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/tmpBBroot /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/LLVM-17.0.0git-Linux
+ /usr/lib/rpm/check-buildroot
+ /usr/lib/rpm/redhat/brp-ldconfig
+ /usr/lib/rpm/brp-compress
+ /usr/lib/rpm/brp-strip /usr/bin/strip
+ /usr/lib/rpm/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump
+ /usr/lib/rpm/redhat/brp-strip-lto /usr/bin/strip
+ /usr/lib/rpm/brp-strip-static-archive /usr/bin/strip
+ /usr/lib/rpm/redhat/brp-python-bytecompile '' 1 0
+ /usr/lib/rpm/brp-python-hardlink
+ /usr/lib/rpm/redhat/brp-mangle-shebangs
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/optrecord.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** WARNING: ./opt/rocm-6.0.2/llvm/share/opt-viewer/style.css is executable but has no shebang, removing executable bit
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/opt-diff.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/opt-stats.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/opt-viewer.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** WARNING: ./opt/rocm-6.0.2/llvm/share/opt-viewer/optpmap.py is executable but has no shebang, removing executable bit
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/bin/scan-view: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
error: Bad exit status from /var/tmp/rpm-tmp.H8Vx5N (%install)
    Bad exit status from /var/tmp/rpm-tmp.H8Vx5N (%install)
 ***
CPackRPM:Debug:    - /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/rpmbuildllvm.out
CPackRPM:Debug: *** Building target platforms: x86_64
Building for target x86_64
setting SOURCE_DATE_EPOCH=1278201600
Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.PJ22iy
Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.H8Vx5N
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/analyze-c++ from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/c++-analyzer from /usr/bin/env perl to #!/usr/bin/perl
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/intercept-c++ from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/ccc-analyzer from /usr/bin/env perl to #!/usr/bin/perl
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/analyze-cc from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/intercept-cc from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/share/clang/clang-format-diff.py from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/hmaptool from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/git-clang-format from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/scan-build-py from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/analyze-build from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/scan-build from /usr/bin/env perl to #!/usr/bin/perl
mangling shebang in /opt/rocm-6.0.2/llvm/bin/intercept-build from /usr/bin/env python3 to #!/usr/bin/python3


RPM build errors:
 ***
CMake Error at /root/workspace/ROCmLol/local/cmake-3.29.3-linux-x86_64/share/cmake-3.29/Modules/Internal/CPack/CPackRPM.cmake:1915 (message):
  RPM package was not generated!
  /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM
Call Stack (most recent call first):
  /root/workspace/ROCmLol/local/cmake-3.29.3-linux-x86_64/share/cmake-3.29/Modules/Internal/CPack/CPackRPM.cmake:1986 (cpack_rpm_generate_package)


CPack Error: Error while execution CPackRPM.cmake
CPack Error: Problem compressing the directory
CPack Error: Error when generating package: LLVM
FAILED: CMakeFiles/package.util 
cd /root/workspace/ROCmLol/build/llvm && /root/workspace/ROCmLol/local/cmake-3.29.3-linux-x86_64/bin/cpack --config ./CPackConfig.cmake
ninja: build stopped: subcommand failed.

```

### Operating System

Red Hat Enterprise Linux" VERSION="9.4 (Plow)"

### CPU

model name	: AMD Ryzen 5 5500

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (12 条)

### 评论 #1 — waheedi (2024-05-16T08:52:37Z)

You apparently have two pythons in your host, try to either remove one of the two pythons which is the python2, or cp /usr/bin/python3 /usr/local/bin/python or update the alternative name. That should fix the shebangbang problem :)

---

### 评论 #2 — perovskikh (2024-05-16T09:08:13Z)

Changes/Make ambiguous python shebangs error 
https://fedoraproject.org/wiki/Changes/Make_ambiguous_python_shebangs_error

---

### 评论 #3 — perovskikh (2024-05-17T04:39:52Z)

> You apparently have two pythons in your host, try to either remove one of the two pythons which is the python2, or cp /usr/bin/python3 /usr/local/bin/python or update the alternative name. That should fix the shebangbang problem :)

The fresh installation of fedora 40 did not work

---

### 评论 #4 — ppanchad-amd (2024-06-21T19:53:25Z)

@perovskikh Fedora 40 is not officially supported. Can you please confirm if issue occurs on RHEL? Thanks!

---

### 评论 #5 — schung-amd (2024-09-06T19:22:14Z)

Hi @perovskikh, does this issue still exist on RHEL with ROCm 6.2?

---

### 评论 #6 — perovskikh (2024-09-11T17:54:40Z)

> Hi @perovskikh, does this issue still exist on RHEL with ROCm 6.2?

There is no technical possibility to check now, in 3 weeks. As soon as I check, I will inform you.

---

### 评论 #7 — schung-amd (2024-09-11T18:52:40Z)

Thanks for the reply. Can you provide steps taken to reproduce this error? I can try to repro it on a clean install of RHEL 9.4.

---

### 评论 #8 — perovskikh (2024-09-11T19:17:23Z)

> Thanks for the reply. Can you provide steps taken to reproduce this error? I can try to repro it on a clean install of RHEL 9.4.

the problem was with shebang when building lvm #!/usr/bin/env python the patch replacing #!/usr/bin/env python with #!/usr/bin/env python3 solved the problem

---

### 评论 #9 — schung-amd (2024-09-11T19:25:16Z)

Are you building llvm by itself, or is this happening as part of building something else? Have you encountered this with any components other than llvm? I can see several files in our codebase with ambiguous Python shebangs, I'll see if RHEL complains about them like Fedora does and reach out to the internal team to find out if we need these to be ambiguous or not.

---

### 评论 #10 — perovskikh (2024-09-12T04:13:19Z)

This happens when manually assembling the llvm source code of ROCm 6.0.2 in :
+ /usr/lib/rpm/redhat/brp-mangle-shebangs
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/optrecord.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** WARNING: ./opt/rocm-6.0.2/llvm/share/opt-viewer/style.css is executable but has no shebang, removing executable bit
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/opt-diff.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/opt-stats.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/share/opt-viewer/opt-viewer.py: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
*** WARNING: ./opt/rocm-6.0.2/llvm/share/opt-viewer/optpmap.py is executable but has no shebang, removing executable bit
*** ERROR: ambiguous python shebang in /opt/rocm-6.0.2/llvm/bin/scan-view: #!/usr/bin/env python. Change it to python3 (or python2) explicitly.
error: Bad exit status from /var/tmp/rpm-tmp.H8Vx5N (%install)
    Bad exit status from /var/tmp/rpm-tmp.H8Vx5N (%install)
 ***
CPackRPM:Debug:    - /root/workspace/ROCmLol/build/llvm/_CPack_Packages/Linux/RPM/rpmbuildllvm.out
CPackRPM:Debug: *** Building target platforms: x86_64
Building for target x86_64
setting SOURCE_DATE_EPOCH=1278201600
Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.PJ22iy
Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.H8Vx5N
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/analyze-c++ from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/c++-analyzer from /usr/bin/env perl to #!/usr/bin/perl
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/intercept-c++ from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/ccc-analyzer from /usr/bin/env perl to #!/usr/bin/perl
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/analyze-cc from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/libexec/intercept-cc from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/share/clang/clang-format-diff.py from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/hmaptool from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/git-clang-format from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/scan-build-py from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/analyze-build from /usr/bin/env python3 to #!/usr/bin/python3
mangling shebang in /opt/rocm-6.0.2/llvm/bin/scan-build from /usr/bin/env perl to #!/usr/bin/perl
mangling shebang in /opt/rocm-6.0.2/llvm/bin/intercept-build from /usr/bin/env python3 to #!/usr/bin/python3

---

### 评论 #11 — schung-amd (2024-09-13T15:03:44Z)

Is this the llvm packaged with ROCm, or is this an external RPM package? Looking through our codebase, we do have some files with ambiguous Python shebangs, but none in llvm. Also, ROCm 6.0.2 doesn't support RHEL 9.4; I'll wait to see if you can repro this on your end with current ROCm.

---

### 评论 #12 — schung-amd (2024-10-04T14:03:20Z)

Closing this for now, as we don't support ROCm 6.0.2 on RHEL 9.4. Let me know if you see this issue in ROCm 6.2.1 or 6.2.2 and we can reopen this.

---
