# amd bugged in 7900xtx on linux damaging my display driver 

> **Issue #3400**
> **状态**: closed
> **创建时间**: 2024-07-06T06:46:25Z
> **更新时间**: 2024-07-14T08:32:17Z
> **关闭时间**: 2024-07-14T08:32:17Z
> **作者**: xalteropsx
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/3400

## 描述

```py
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups
wget https://repo.radeon.com/amdgpu-install/6.1.2/ubuntu/jammy/amdgpu-install_6.1.60102-1_all.deb
sudo apt install ./amdgpu-install_6.1.60102-1_all.deb
sudo apt update
sudo apt install amdgpu-dkms rocm
```
followed by this bug documents 


### Description of errors

```py
haideraf@haideraf:~/Downloads$ sudo apt install amdgpu-dkms
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
amdgpu-dkms is already the newest version (1:6.7.0.60103-1787201.22.04).
0 upgraded, 0 newly installed, 0 to remove and 3 not upgraded.
haideraf@haideraf:~/Downloads$ sudo apt install rocm-hip-libraries
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
rocm-hip-libraries is already the newest version (6.1.3.60103-122~22.04).
rocm-hip-libraries set to manually installed.
0 upgraded, 0 newly installed, 0 to remove and 3 not upgraded.
haideraf@haideraf:~/Downloads$ rocminfo
ROCk module is NOT loaded, possibly no GPU devices
haideraf@haideraf:~/Downloads$ dmesg | grep amd
[    0.000000] Linux version 6.5.0-41-generic (buildd@lcy02-amd64-120) (x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #41~22.04.2-Ubuntu SMP PREEMPT_DYNAMIC Mon Jun  3 11:32:55 UTC 2 (Ubuntu 6.5.0-41.41~22.04.2-generic 6.5.13)
[    0.652180] perf/amd_iommu: Detected AMD IOMMU #0 (2 banks, 4 counters/bank).
[    0.754335] amd_pstate: the _CPC object is not present in SBIOS or ACPI disabled
[    6.024209] kvm_amd: TSC scaling supported
[    6.024213] kvm_amd: Nested Virtualization enabled
[    6.024214] kvm_amd: Nested Paging enabled
[    6.024217] kvm_amd: SEV enabled (ASIDs 0 - 15)
[    6.024219] kvm_amd: SEV-ES enabled (ASIDs 0 - 4294967295)
[    6.024240] kvm_amd: Virtual VMLOAD VMSAVE supported
[    6.024241] kvm_amd: Virtual GIF supported
[    6.024242] kvm_amd: LBR virtualization supported
haideraf@haideraf:~/Downloads$ -^C

```

### Attach any links, screenshots, or additional evidence you think will be helpful.

```py
haideraf@haideraf:~/Downloads$ uname -m && cat /etc/*release
x86_64
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.4 LTS"
PRETTY_NAME="Ubuntu 22.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy


---

## 评论 (3 条)

### 评论 #1 — evshiron (2024-07-06T13:35:16Z)

Why don't we use `amdgpu-install` like this:

* https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html#installing-rocm-packages

---

### 评论 #2 — xalteropsx (2024-07-07T02:43:09Z)

not working at all  i tried these one as well after fresh reinstall linux same it keep break my display driver over and over

---

### 评论 #3 — harkgill-amd (2024-07-08T20:10:48Z)

Hi @xalteropsx, are you able to see your GPU listed in the output of `lspci | grep -i amd`? Could you also try manually loading the amdgpu kernel module through `modprobe amdgpu`.

---
