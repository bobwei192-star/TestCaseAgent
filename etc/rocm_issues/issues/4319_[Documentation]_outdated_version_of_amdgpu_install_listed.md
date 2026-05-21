# [Documentation]: outdated version of amdgpu install listed

> **Issue #4319**
> **状态**: closed
> **创建时间**: 2025-01-30T15:06:03Z
> **更新时间**: 2025-01-31T06:31:19Z
> **关闭时间**: 2025-01-30T18:41:30Z
> **作者**: wsargent
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4319

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Description of errors

On the installation page https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html

the documentation says to install 6.2.3

```
wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/amdgpu-install_6.2.60203-1_all.deb
```

This will fail because of https://github.com/ROCm/ROCm/issues/2524

The newer version should be used from https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html

```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.2/ubuntu/noble/amdgpu-install_6.3.60302-1_all.deb
sudo apt install ./amdgpu-install_6.3.60302-1_all.deb
sudo apt update
```

### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (10 条)

### 评论 #1 — harkgill-amd (2025-01-30T15:15:20Z)

Hi @wsargent, both of these links point to the [Ubuntu AMDGPU installer installation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html) page which correctly highlights installation commands for ROCm 6.3.2.

```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.2/ubuntu/noble/amdgpu-install_6.3.60302-1_all.deb
sudo apt install ./amdgpu-install_6.3.60302-1_all.deb
sudo apt update
```
Are you still seeing instructions for ROCm 6.2.3 on your end for either of these links? 


---

### 评论 #2 — wsargent (2025-01-30T18:23:38Z)

Sorry, here is the correct link

https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#install-amd-unified-driver-package-repositories-and-installer-script



---

### 评论 #3 — wsargent (2025-01-30T18:26:37Z)

I think the WSL compatibility page as well points to ROCm 6.2.3

https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html

---

### 评论 #4 — wsargent (2025-01-30T18:32:47Z)

Okay, so I think maybe the disconnect is that WSL only supports ROCm 6.2.3, so even though it's running Ubuntu in the container, the instructions in https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html don't apply?

---

### 评论 #5 — wsargent (2025-01-30T18:35:59Z)

So I am using WSL, so that means I need 6.2.3 and therefore need a workaround for https://github.com/ROCm/ROCm/issues/2524.

---

### 评论 #6 — wsargent (2025-01-30T18:41:30Z)

And I am using Ubuntu 24.04 and not Ubuntu 22.04, so that explains that one.  Closing.

---

### 评论 #7 — harkgill-amd (2025-01-30T18:49:13Z)

Happy to hear you got it worked out. Just to clarify if someone runs across this thread, ROCm on Radeon, and by extension ROCm on WSL, currently support ROCm 6.2.3. You can find the instructions for installing ROCm for Radeon at [Install Radeon Software for Linux with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-radeon.html#install-radeon-software-for-linux-with-rocm) , and the WSL compatibility matrix [here](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html).

---

### 评论 #8 — briansp2020 (2025-01-30T18:57:38Z)

@harkgill-amd
ROCm 6.3 WSL support when?
Also, does AMD have plan to release WSL support simultaneously with regular ROCm release? 

---

### 评论 #9 — harkgill-amd (2025-01-30T19:33:52Z)

@briansp2020, I can't provide any timeline on when ROCm 6.3 support for WSL will be released but I can assure you our team is working hard to enable support. We understand the importance of syncing the WSL release with our standard Linux releases for the community. However, there are no plans to align the release schedules just yet.

---

### 评论 #10 — wsargent (2025-01-31T06:31:18Z)

Apparently Vulkan support is technically possible for cards that aren't supported by ROCm:

https://www.jeffgeerling.com/blog/2024/llms-accelerated-egpu-on-raspberry-pi-5

---
