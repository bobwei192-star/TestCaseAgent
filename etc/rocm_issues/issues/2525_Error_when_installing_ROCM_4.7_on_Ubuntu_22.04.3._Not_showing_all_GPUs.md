# Error when installing ROCM 4.7 on Ubuntu 22.04.3. Not showing all GPUs. 

> **Issue #2525**
> **状态**: closed
> **创建时间**: 2023-10-04T19:40:51Z
> **更新时间**: 2024-02-01T03:19:22Z
> **关闭时间**: 2024-02-01T03:19:22Z
> **作者**: TheNoise2Signal
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2525

## 描述

This is a fresh Ubuntu install. I've upgraded my kernel to 6.2 in accordance to the Prerequisites on the website (https://rocm.docs.amd.com/en/latest/deploy/linux/prerequisites.html)
Showing `uname -m && cat /etc/*release`:
```x86_64
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.3 LTS"
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

My Kernel version is: `Linux 6.2.0-060200-generic #202302191831 SMP PREEMPT_DYNAMIC Sun Feb 19 23:37:22 UTC 2023 x86_64`

I'm trying to install according to https://rocm.docs.amd.com/en/latest/deploy/linux/installer/install.html

When I run `sudo amdgpu-install --usecase=rocm`, it fails stating
```ERROR (dkms apport): kernel package linux-headers-6.2.0-060200-generic is not supported
Error! Bad return status for module build on kernel: 6.2.0-060200-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.2.4-1652687.22.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
 installed amdgpu-dkms package post-installation script subprocess returned error exit status 10
Errors were encountered while processing:
 amdgpu-dkms
needrestart is being skipped since dpkg has failed
E: Sub-process /usr/bin/dpkg returned an error code (1)```

But when I run ```
apt-cache policy amdgpu amdgpu-dkms
amdgpu:
  Installed: (none)
  Candidate: 1:5.7.50700-1652687.22.04
  Version table:
     1:5.7.50700-1652687.22.04 600
        600 https://repo.radeon.com/amdgpu/5.7/ubuntu jammy/main amd64 Packages
amdgpu-dkms:
  Installed: 1:6.2.4.50700-1652687.22.04
  Candidate: 1:6.2.4.50700-1652687.22.04
  Version table:
 *** 1:6.2.4.50700-1652687.22.04 600
        600 https://repo.radeon.com/amdgpu/5.7/ubuntu jammy/main amd64 Packages
        100 /var/lib/dpkg/status
  ```

Running rocm-smi shows only 1 GPU while it should be showing 8. `sudo lspci | grep -i "display"` shows me all my GPUs.








---

## 评论 (3 条)

### 评论 #1 — pramenku (2023-10-23T17:42:26Z)

@saksham36  is rocm4.7 typo?

You meant 5.7?

Attach the make.log. path of the log, you can see in  console output

Also, please give a try with 5.7.1 latest https://rocm.docs.amd.com/en/docs-5.7.1/release/gpu_os_support.html

---

### 评论 #2 — nartmada (2024-01-17T04:54:22Z)

Hi @saksham36, please check latest ROCm6.0.0 to see if your issue has been fixed.  Please close the ticket if issue is fixed.  Thanks.

---

### 评论 #3 — nartmada (2024-02-01T03:19:22Z)

Closing the ticket as no response from @saksham36.  Please re-open the ticket if the issue still exists with latest ROCm6.0.0.  Thanks.

---
