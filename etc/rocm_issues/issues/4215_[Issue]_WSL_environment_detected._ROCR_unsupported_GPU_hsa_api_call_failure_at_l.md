# [Issue]: WSL environment detected. ROCR: unsupported GPU hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1306 Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

> **Issue #4215**
> **状态**: closed
> **创建时间**: 2025-01-02T02:33:10Z
> **更新时间**: 2025-08-09T16:31:17Z
> **关闭时间**: 2025-01-17T15:15:49Z
> **作者**: Akash-1711
> **标签**: Under Investigation, ROCm 6.2.3, AMD Radeon RX 7700XT
> **URL**: https://github.com/ROCm/ROCm/issues/4215

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **AMD Radeon RX 7700XT** (颜色: #ededed)

## 描述

### Problem Description

Im trying to install ComfyUI in WSL2 im following this [Tutorial](https://www.youtube.com/watch?v=p1jKqV9IV8I) and https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html 
when i try to do post-install verification by "rocminfo" im getting this error. 
GPU drivers are 24.12.1 and windows 11OS
im not sure what else to add in here. if this info is not enough please let me know, i will try to provide it. 

### Operating System

Ubuntu 22.04.5

### CPU

AMD Ryzen 5 7600X

### GPU

AMD Radeon RX 7700XT

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (16 条)

### 评论 #1 — ppanchad-amd (2025-01-02T14:11:27Z)

Hi @Akash-1711. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — Vineeth-Narayan (2025-01-08T08:49:43Z)

Hi, 
I am having the same issue with CPU Ryzen 7 6800H and GPU RX 6800S with Ubuntu 22.04.5 LTS.

WSL environment detected.
ROCR: unsupported GPU
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1306
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

---

### 评论 #3 — sohaibnd (2025-01-09T15:58:35Z)

Hi @Akash-1711 @Vineeth-Narayan, can you check your device status in device manager?

---

### 评论 #4 — ricecrackerfiend (2025-01-09T20:19:26Z)

I'm running into this exact same error, however I'm on Ubuntu 24.04.1 LTS.

My GPU is an RX 7800 XT.

In device manager, my GPU's status is: "This device is working properly."

---

### 评论 #5 — sohaibnd (2025-01-10T16:52:10Z)

@Akash-1711 @Vineeth-Narayan @petersonmichaelj These GPUs are not supported on WSL so the unsupported GPU error is expected ([see the compatibility matrix for WSL](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html)). If you see this issue on a supported config, please let me know and I can look into it further.

---

### 评论 #6 — DonCaton (2025-01-11T20:53:39Z)

Will be support for AMD GPU RX580 ? I have two of them, they run smoothly any games and I also used them for Ethereum mining at some point. They should be supported to run LLM Inference Engines in WSL2 Docker

---

### 评论 #7 — sohaibnd (2025-01-13T15:44:01Z)

@DonCaton There aren't any plans to support the RX 580 unfortunately.

---

### 评论 #8 — sohaibnd (2025-01-17T15:15:49Z)

Closing this issue as there is no further action.

---

### 评论 #9 — connorblack (2025-02-16T02:55:12Z)

@sohaibnd I'm getting this error on a fresh (bare metal, non-WSL) Ubuntu 22 install, gfx1100 GPUs. This should probably be reopened:
```
amdgpu-install --usecase=dkms,rocm,rocmdev,rocmdevtools,lrt,openclsdk,hip,hiplibsdk,openmpsdk,mllib,mlsdk,asan --install-recommends --install-suggests
Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
Hit:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease
Hit:3 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease
Hit:4 https://download.docker.com/linux/ubuntu jammy InRelease                                                                                  
Hit:5 https://repo.radeon.com/amdgpu/6.3.2/ubuntu jammy InRelease                                                                               
Hit:6 https://repo.radeon.com/rocm/apt/6.3.2 jammy InRelease                                                              
Hit:7 http://security.ubuntu.com/ubuntu jammy-security InRelease                                                          
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
linux-headers-5.15.0-131-generic is already the newest version (5.15.0-131.141).
amdgpu-dkms is already the newest version (1:6.10.5.60302-2109964.22.04).
rocm is already the newest version (6.3.2.60302-66~22.04).
rocm-asan is already the newest version (6.3.2.60302-66~22.04).
rocm-dev is already the newest version (6.3.2.60302-66~22.04).
rocm-developer-tools is already the newest version (6.3.2.60302-66~22.04).
rocm-hip-runtime is already the newest version (6.3.2.60302-66~22.04).
rocm-hip-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-language-runtime is already the newest version (6.3.2.60302-66~22.04).
rocm-ml-libraries is already the newest version (6.3.2.60302-66~22.04).
rocm-ml-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-opencl-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-openmp-sdk is already the newest version (6.3.2.60302-66~22.04).
rocm-utils is already the newest version (6.3.2.60302-66~22.04).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
rocminfo
clinfo
ROCk module version 6.10.5 is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1282
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 0
```

---

### 评论 #10 — sohaibnd (2025-02-18T15:36:45Z)

@connorblack While the error message is similar, the issue reported by the users above is specific to unsupported GPUs on WSL (note the "ROCR: unsupported GPU" in the error message). Please create a separate issue for this.


---

### 评论 #11 — Apriqi (2025-04-17T07:07:57Z)

请问有结果吗？WSL ROCM未来安排什么版本支持一下旧版显卡，本人使用7800XT，如果不打算支持，能否告知？是否意味着以往的显卡AI都是噱头？

---

### 评论 #12 — sohaibnd (2025-04-21T19:28:54Z)

@Apriqi The [docs](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html) mention that the 7800XT is not currently supported on WSL. In terms of future support, we are working on supporting some older GPUs but nothing has been announced yet so please wait till the next WSL ROCM release for an update.






---

### 评论 #13 — Apriqi (2025-04-23T09:31:24Z)

> 努力支持一些较旧的 GPU，但尚未宣布任何内容，因此请等待下一个 WSL ROCM 版本进行更新。

随着新显卡的发布，较旧的GPU支持希望渺茫，早知道就不买AMD了

---

### 评论 #14 — SENPAI-code66 (2025-05-05T15:16:28Z)

After wasting a whole day I find out that my rx 6700 xt is not supported. What a waste of money. I am never buying AMD ever in my life

---

### 评论 #15 — indai123 (2025-07-27T17:48:29Z)

I legit have rx 7800 xt which is supported ,yet when I put rocminfo, WSL2 freaks out with the data running out

---

### 评论 #16 — RedGreenBlue999 (2025-08-09T16:31:17Z)

> I legit have rx 7800 xt which is supported ,yet when I put rocminfo, WSL2 freaks out with the data running out

Did you get it work? I have 7800 xt as well.

---
