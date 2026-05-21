# Unable to open /dev/kfd read-write: Cannot allocate memory

> **Issue #2232**
> **状态**: closed
> **创建时间**: 2023-06-09T12:50:04Z
> **更新时间**: 2023-11-10T16:24:26Z
> **关闭时间**: 2023-11-10T16:24:25Z
> **作者**: R0rschach02
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2232

## 描述

As I try: 

`rocminfo

ROCk module is loaded

Unable to open /dev/kfd read-write: Cannot allocate memory

igor is member of render group

hsa api call failure at: /src/rocminfo/rocminfo.cc:1142

Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
`

look into dmesg: 

`sudo dmesg | grep kfd

[    3.548555] kfd kfd: amdgpu: PITCAIRN  not supported in kfd
`
Info: 

`uname -r

5.4.0-54-generic
`
`lspci | grep VGA

01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Curacao PRO [Radeon R7 370 / R9 270/370 OEM]
`

I've been using this guidance here: https://github.com/Grench6/RX580-rocM-tensorflow-ubuntu20.4-guide

Thanks in advance for help! 

---

## 评论 (4 条)

### 评论 #1 — Ameobea (2023-06-09T19:02:53Z)

My user needed to be added to both the `video` and `render` groups on my machine.  Also need to reboot after setting those permissions.

I was able to test if it worked by running `cat /dev/kfd`.  Before my permissions were correct, it gave "permission denied" or something like that.  After permissions were fixed, I see "cat: /dev/kfd: Invalid argument" and my ROCm install works.

---

### 评论 #2 — R0rschach02 (2023-06-10T12:25:23Z)

As I try running cat /dev/kfd I get following message: cat: /dev/kfd: Cannot allocate memory 

And if I try to add my user to the video permission group and reboot my PC I still get the same error message as above


---

### 评论 #3 — Ameobea (2023-06-10T20:36:58Z)

I see.  I'm afraid I don't know what's going on for you in this case then; that is different than what I was getting.

---

### 评论 #4 — kentrussell (2023-11-10T16:24:26Z)

Your GPU is not supported by KFD:
[ 3.548555] kfd kfd: amdgpu: PITCAIRN not supported in kfd
You're using a gfx6 device. ROCm requires at least gfx8 (Hawaii is the only gfx7 GPU supported, gfx6-and-older aren't supported due to missing HW capabilities) . You can refer to https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html for official ROCm GPU support, but you won't be able to use a Pitcairn card for KFD,

---
