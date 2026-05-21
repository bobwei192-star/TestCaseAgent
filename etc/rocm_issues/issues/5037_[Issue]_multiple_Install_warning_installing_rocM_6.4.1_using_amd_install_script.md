# [Issue]: multiple Install warning installing rocM 6.4.1 using amd install script

> **Issue #5037**
> **状态**: closed
> **创建时间**: 2025-07-12T23:29:14Z
> **更新时间**: 2025-11-10T14:54:06Z
> **关闭时间**: 2025-11-10T14:54:06Z
> **作者**: gomimeru
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5037

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I saw a similar issue report that was marked as closed that showed a very similar issue - issue #3035

The issue seems to be back in the radeon software install for linux with ROCm 6.4.1
after going into the page for  Driver install for linux on the AMD page and running the provided commands

i get multiple warnings of stuff not found:


> Setting` up rocm-hip-runtime-dev (6.4.1.60401-83~24.04) ...
 /bin/roc-obj not found, but that is OK
/bin/roc-obj-extract not found, but that is OK
/bin/roc-obj-ls not found, but that is OK
/bin/hipcc not found, but that is OK
/bin/hipcc.pl not found, but that is OK
/bin/hipcc.bin not found, but that is OK
/bin/hipcc_cmake_linker_helper not found, but that is OK
/bin/hipconfig not found, but that is OK
/bin/hipconfig.pl not found, but that is  #OK
/bin/hipconfig.bin not found, but that is OK
/bin/hipconvertinplace-perl.sh not found, but that is OK
/bin/hipconvertinplace.sh not found, but that is OK
/bin/hipdemangleatp not found, but that is OK
/bin/hipexamine-perl.sh not found, but that is OK
/bin/hipexamine.sh not found, but that is OK
/bin/hipify-perl not found, but that is OK
/bin/hipify-clang not found, but that is OK
/bin/amdclang not found, but that is OK
/bin/amdclang++ not found, but that is OK
/bin/amdflang not found, but that is OK
/bin/amdlld not found, but that is OK

> Setting up rocm-hip-sdk (6.4.1.60401-83~24.04) ...
/bin/hipfc not found, but that is OK

> Setting up rocm (6.4.1.60401-83~24.04) ...
/bin/runvx not found, but that is OK

I ran the script  on Linux Mint 22 instead of pure Ubuntu 24.04
whoever as linux mint 22 is based on 24.04 i wouldnt expect this to happen

### Operating System

Linux Mint 22.1

### CPU

AMD Ryzen 5 8500G w/ Radeon 740M Graphics

### GPU

Radeon 7600x

### ROCm Version

ROCm 6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

go to: https://www.amd.com/es/support/download/linux-drivers.html

run commands provided in Radeon™ Software for Linux® version 25.10.1 for Ubuntu 24.04.2 HWE with ROCm 6.4.1

> sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb
sudo apt install ./amdgpu-install_6.4.60401-1_all.deb
sudo amdgpu-install -y --usecase=graphics,rocm
sudo usermod -a -G render,video $LOGNAME`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — ppanchad-amd (2025-07-14T13:45:00Z)

Hi @gomimeru. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — harkgill-amd (2025-07-14T15:29:29Z)

Hi @gomimeru, could you please provide the output of 

- `cat /etc/os-release` - specifically looking for the `ID_LIKE` field
- `ls /opt/rocm-6.4.1/bin`

The `postinst` script that's throwing these warnings checks for `ID_LIKE = 'debian'` prior to setting the ROCm installation path. From a quick check online, it looks like Linux Mint 22 has this value set to `ubuntu` which likely results in the script failing to set the correct installation path.

---

### 评论 #3 — BeaverUI (2025-07-24T11:29:38Z)

I have the same issue, and indeed ID_LIKE="ubuntu debian". I manually set ID_LIKE="debian" while installing, then it passes cleanly.

---

### 评论 #4 — harkgill-amd (2025-07-24T15:04:30Z)

Thanks for confirming. We're working on a fix that'll make the check more lenient, allowing for Ubuntu based OSes to pass as well. 

---

### 评论 #5 — harkgill-amd (2025-07-31T18:00:39Z)

Quick update on this issue, the fix has made it's way into staging and will likely be released in ROCm 7.1.

---

### 评论 #6 — harkgill-amd (2025-10-30T19:31:50Z)

Hey @gomimeru and @BeaverUI, ROCm 7.1 has been released and I see the fix is present in the `postinst` scripts. 

Could you give the install a try on your end and close out the issue if it's resolved?

---

### 评论 #7 — harkgill-amd (2025-11-10T14:54:06Z)

Closing this out as fix has been released.

---
