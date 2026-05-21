# [Issue]: ROCm fails to report correct information after some time on dual W7800 configuration

> **Issue #4134**
> **状态**: closed
> **创建时间**: 2024-12-06T20:32:27Z
> **更新时间**: 2025-01-16T19:21:28Z
> **关闭时间**: 2025-01-16T19:21:27Z
> **作者**: garrettbyrd
> **标签**: Under Investigation, ROCm 6.1.0, 2x AMD Radeon Pro W7800
> **URL**: https://github.com/ROCm/ROCm/issues/4134

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.1.0** (颜色: #ededed)
- **2x AMD Radeon Pro W7800** (颜色: #ededed)

## 描述

### Problem Description

I am currently running a workstation with two AMD Radeon Pro W7800 cards. 

Link to motherboard: [Gigabyte TRX50-AERO-D](https://www.gigabyte.com/Motherboard/TRX50-AERO-D-rev-12)

As a reminder, the W7800 runs `gfx1100`. Upon system boot, both cards behave as expected. `rocm-smi` and `rocminfo` report the correct information, and the ROCm interface works correctly with PyTorch and other applications. 

After a seemingly arbitrary amount of time, ROCm seems to just "die" for each card. These events are independent per card, and the uptime after boot is <24hr before this occurs (I have not narrowed the time down exactly, and it does not even seem to be consistent). This occurs even if no ROCm-related program was run by the user.

I.e., I boot, wait, and then ROCm can no longer communicate with my cards. Here is what `rocm-smi` output after the "crash":

```
$ rocm-smi


Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
Expected integer value from monitor, but got ""
========================================== ROCm System Management Interface ==========================================
==================================================== Concise Info ====================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK  MCLK  Fan  Perf     PwrCap       VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                      
======================================================================================================================
0       2     0x745e,   49070  N/A     N/A    N/A, N/A, 0         None  None  0%   unknown  Unsupported  0%     0%    
1       1     0x745e,   8521   N/A     N/A    N/A, N/A, 0         None  None  0%   unknown  Unsupported  0%     0%    
======================================================================================================================
================================================ End of ROCm SMI Log =================================================

```

Is there any insight into what might be causing this? [This issue](https://github.com/ROCm/ROCm/issues/2681) seems related, but I am running ROCm 6.1.3.

### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen Threadripper 7960X 24-Cores

### GPU

2x AMD Radeon Pro W7800

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.7.0 is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1250
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — harkgill-amd (2024-12-09T18:48:43Z)

Hi @garrettbyrd, could you please provide the dmesg output after ROCm enters the erroneous state, as well as the Linux kernel version?

---

### 评论 #2 — garrettbyrd (2024-12-11T21:36:19Z)

kernel version is `5.15.0-122-generic`. attached is dmesg output.
[dmesg.txt](https://github.com/user-attachments/files/18102640/dmesg.txt)


---

### 评论 #3 — harkgill-amd (2024-12-12T21:42:02Z)

From the dmesg provided, it looks like your GPU is getting stuck in BACO, a low power state. 
```
amdgpu 0000:43:00.0: amdgpu: Failed to exit BACO state!
```
 We are currently working on reproducing this internally to further investigate. In the meantime, a couple questions for you
 
1. Do you see this issue when only using a single dGPU?
2. If you reload the amdgpu module with `sudo modprobe -r amdgpu` and `sudo modprobe amdgpu`, does rocm-smi function correctly?
3. When in the erroneous state, can you try to run a 3D workload such as `glxgears` to wake the GPU, then run rocm-smi?
4. Output of `cat /sys/class/drm/card0/device/power/runtime_status`

---

### 评论 #4 — harkgill-amd (2025-01-16T19:21:27Z)

Closing this issue due to lack of response. This looks to be the same issue as https://github.com/ROCm/ROCm/issues/4226 which we will use to further investigate.

---
