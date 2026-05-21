# [Issue]: amdgpu: Fatal error during GPU init

> **Issue #2747**
> **状态**: closed
> **创建时间**: 2023-12-18T09:07:36Z
> **更新时间**: 2024-01-12T06:12:03Z
> **关闭时间**: 2024-01-12T06:12:03Z
> **作者**: simonschuang
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2747

## 描述

### Suggestion Description

I have a server installed 4x MI210 GPUs with a Infinity Fabric bridge, running on Ubuntu 20.04 kernel 5.15.0-88-generic.
I follow the [installation document](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/ubuntu.html) to install the amdgpu-dkms 6.0

We encounter errors when loading amdgpu kernel module.
`modprobe amdgpu`
```
[Mon Dec 18 08:34:36 2023] amdgpu 0000:c7:00.0: amdgpu: Will use PSP to load VCN firmware
[Mon Dec 18 08:34:36 2023] [drm:psp_hw_start [amdgpu]] *ERROR* PSP create ring failed!
[Mon Dec 18 08:34:37 2023] [drm:psp_v13_0_ring_destroy [amdgpu]] *ERROR* Fail to stop psp ring
[Mon Dec 18 08:34:37 2023] [drm:amdgpu_fill_buffer [amdgpu]] *ERROR* Trying to clear memory with ring turned off.
```



The full dmesg log is here
[modprobe_amdgpu.log](https://github.com/ROCm/ROCm/files/13701635/modprobe_amdgpu.log)



### Operating System

Ubuntu 20.04 (AGESA 1.0.0.7)

### GPU

MI210x4 with infinity fabric


### ROCm Component

_No response_

---

## 评论 (1 条)

### 评论 #1 — simonschuang (2024-01-12T06:12:03Z)

Hi there, the rocm-smi can successfully show all four MI210 GPUs after I unplugged the infinity fabric link. Probabily I got a defective one. I'm closing this issue since it doesn't seem like a software issue. 

---
