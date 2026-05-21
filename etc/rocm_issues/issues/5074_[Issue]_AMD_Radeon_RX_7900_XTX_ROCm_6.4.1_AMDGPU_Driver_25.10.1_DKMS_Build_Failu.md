# [Issue]:  AMD Radeon RX 7900 XTX: ROCm 6.4.1 / AMDGPU Driver 25.10.1 DKMS Build Failure on Ubuntu 24.04.2 LTS (Kernel 6.14.0-24-generic)

> **Issue #5074**
> **状态**: closed
> **创建时间**: 2025-07-21T21:03:50Z
> **更新时间**: 2025-07-28T14:30:50Z
> **关闭时间**: 2025-07-25T18:04:48Z
> **作者**: cisnerosjo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5074

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Okay, I've filled out the GitHub Issue Report form for you based on all the details we've covered. You can copy and paste this directly into the form. Remember to fill in your CPU model.

Add a title*
[Issue]: AMD Radeon RX 7900 XTX: ROCm 6.4.1 / AMDGPU Driver 25.10.1 DKMS Build Failure on Ubuntu 24.04.2 LTS (Kernel 6.14.0-24-generic)

Problem Description*
I am attempting to install the AMDGPU driver and ROCm 6.4.1 for my AMD Radeon RX 7900 XTX on Ubuntu 24.04.2 LTS (Kernel 6.14.0-24-generic) for local LLM acceleration. Despite following the official AMD installation instructions, the amdgpu-dkms module fails to build for my kernel, preventing the full driver and ROCm stack from functioning correctly. This means my GPU cannot be used for compute tasks.

Specific Errors Encountered:

amdgpu-dkms Build Failure:
When installing "Radeon™ Software for Linux® version 25.10.1 for Ubuntu 24.04.2 HWE with ROCm 6.4.1" (from amdgpu-install_6.4.60401-1_all.deb), the amdgpu-dkms package fails to configure during the sudo amdgpu-install -y --usecase=graphics,rocm step.

The error messages from sudo apt install --reinstall amdgpu-dkms indicate the following:

Building for 6.14.0-24-generic
Building for architecture x86_64
Building initial module for 6.14.0-24-generic
Error! Bad return status for module build on kernel: 6.14.0-24-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.12.12-2164967.24.04/build/make.log for more information.
dpkg: error processing package amdgpu-dkms (--configure):
Key errors from /var/lib/dkms/amdgpu/6.12.12-2164967.24.04/build/make.log show kernel API incompatibilities:

error: 'struct drm_driver' has no member named 'date'

error: implicit declaration of function 'drm_fbdev_ttm_setup'

ROCm Not Initialized / rocminfo Executable Missing:
After the failed amdgpu-dkms installation, lsmod | grep amdgpu confirms the amdgpu kernel module is loaded (likely the Ubuntu-provided version). However, ROCm utilities fail to find the driver or run:

/opt/rocm/bin/rocminfo output: bash: /opt/rocm/bin/rocminfo: No such file or directory

/opt/rocm/bin/rocm-smi output: ROCk module is NOT loaded, possibly no GPU devices and ERROR:root:Driver not initialized (amdgpu not found in modules)

Even after attempting a "driverless" ROCm installation (adding https://repo.radeon.com/rocm/apt/6.4.1 noble main and installing rocm-libs), the rocminfo executable is still missing from /opt/rocm/bin (confirmed by ls /opt/rocm/bin and sudo find /opt/rocm* -name rocminfo which returned no output for rocminfo). This suggests an issue with the rocminfo package itself in this context.

### Operating System

Ubuntu 24.04.2 LTS

### CPU

12th Gen Intel® Core™ i9-12900KF × 24

### GPU

AMD Radeon RX 7900 XTX (Navi 31)

### ROCm Version

ROCm 6.4.1

### ROCm Component

rocminfo

### Steps to Reproduce

Ensure Ubuntu 24.04.2 LTS is fully updated (sudo apt update && sudo apt upgrade).

Verify kernel version is 6.14.0-24-generic (uname -r).

Confirm Secure Boot is disabled (mokutil --sb-state).

Download the driver installer: wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb

Install the driver: sudo apt install ./amdgpu-install_6.4.60401-1_all.deb

Run the installation command: sudo amdgpu-install -y --usecase=graphics,rocm

Observe the amdgpu-dkms package configuration failure during installation.

Attempt to verify ROCm: /opt/rocm/bin/rocminfo or /opt/rocm/bin/rocm-smi (these commands fail as described above).

(Optional, as a workaround attempt that also failed to fully resolve) Remove previous AMDGPU/ROCm installations: sudo apt purge rocm* amdgpu* -y && sudo apt autoremove --purge -y.

Add ROCm repository: wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | sudo apt-key add - and echo 'deb [arch=amd64] https://repo.radeon.com/rocm/apt/6.4.1 noble main' | sudo tee /etc/apt/sources.list.d/rocm.list.

Update apt and install core ROCm libs: sudo apt update && sudo apt install rocm-libs -y.

Set environment variables: echo 'export PATH=/opt/rocm/bin:$PATH' | sudo tee /etc/profile.d/rocm.sh && echo 'export LD_LIBRARY_PATH=/opt/rocm/lib:$LD_LIBRARY_PATH' | sudo tee -a /etc/profile.d/rocm.sh && source /etc/profile.d/rocm.sh.

Attempt to verify ROCm again: /opt/rocm/bin/rocminfo (still reports "No such file or directory").

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

The rocminfo executable is not found on my system after installation attempts. Therefore, I cannot provide output from /opt/rocm/bin/rocminfo --support. Its absence is part of the problem being reported.


ROCm Component
amdgpu-dkms, hip-runtime-amd, rocminfo (general installation failure affecting core components)

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — KiYugadgeter (2025-07-22T04:00:59Z)

I have same issue too.  
Probably HWE is enable on Your Environment.  
According to official ROCm documentation, 6.14 kernel is not supported yet, 
I suppose to Ubuntu has released 6.14 kernel bit earlier (6.14 is for 24.04.3?), but ROCm doesn't support it.  

Maybe we still keep 6.11 kernel.

https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#os-kernel-versions


---

### 评论 #2 — ppanchad-amd (2025-07-22T14:23:32Z)

Hi @cisnerosjo. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — cisnerosjo (2025-07-22T15:52:01Z)

> I have same issue too. Probably HWE is enable on Your Environment. According to official ROCm documentation, 6.14 kernel is not supported yet, I suppose to Ubuntu has released 6.14 kernel bit earlier (6.14 is for 24.04.3?), but ROCm doesn't support it.
> 
> Maybe we still keep 6.11 kernel.
> 
> https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#os-kernel-versions

Yes, I've read the issue, started to become a problem on anything >6.12. I'm actually going to try this, because I want to use the hardware, even if its limited. Because, it will still be less limited than it is now. Thanks for the tip!

---

### 评论 #4 — cisnerosjo (2025-07-22T16:32:28Z)

> I have same issue too. Probably HWE is enable on Your Environment. According to official ROCm documentation, 6.14 kernel is not supported yet, I suppose to Ubuntu has released 6.14 kernel bit earlier (6.14 is for 24.04.3?), but ROCm doesn't support it.
> 
> Maybe we still keep 6.11 kernel.
> 
> https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#os-kernel-versions

It didn't work, submitting another issue, to log

---

### 评论 #5 — harkgill-amd (2025-07-25T18:04:48Z)

Dup of https://github.com/ROCm/ROCm/issues/5074.

---

### 评论 #6 — maxbenin (2025-07-26T22:16:33Z)

I solved the problem forcing linux to use the latest Kernel that was compiled sucessfully by the amdgpu. In my case was 6.11.0-29-generic. 

Now i have this annoying issue every time i run apt-get upgrade or install that runs the compilation all over again for all kernels installed. Then it crashes on 6.14. I think i will uninstall this kernel temporarily, until AMD release something compatible.

---

### 评论 #7 — harkgill-amd (2025-07-28T13:47:19Z)

@maxbenin, the kernel driver packaged with ROCm 6.4.2 is compatible with both the 6.11 and 6.14 kernel. 

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html

---

### 评论 #8 — maxbenin (2025-07-28T14:20:14Z)

Hi, @harkgill-amd, is this driver release recent?
Because up until last Friday I was still facing compatibility issues with the latest kernel.
I'm just looking to get the video driver working properly — I don’t intend to use everything that ROCm provides.

---

### 评论 #9 — harkgill-amd (2025-07-28T14:29:08Z)

6.4.2 was released last week on Monday. Upgrading will resolve the build failures you're seeing with the 6.14 kernel. For reference, the specific failures were tracked in https://github.com/ROCm/ROCm/issues/4619.

---

### 评论 #10 — maxbenin (2025-07-28T14:30:50Z)

Thank you, my friend. I will try to update right now

---
