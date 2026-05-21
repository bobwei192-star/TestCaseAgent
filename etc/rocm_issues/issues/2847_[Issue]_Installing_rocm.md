# [Issue]: Installing rocm

> **Issue #2847**
> **状态**: closed
> **创建时间**: 2024-01-27T06:20:05Z
> **更新时间**: 2024-01-29T08:06:24Z
> **关闭时间**: 2024-01-29T03:19:37Z
> **作者**: BujSet
> **标签**: AMD Instinct MI300X, ROCm 6.0.0
> **URL**: https://github.com/ROCm/ROCm/issues/2847

## 标签

- **AMD Instinct MI300X** (颜色: #ededed)
- **ROCm 6.0.0** (颜色: #ededed)

## 描述

### Problem Description

I have been trying to install rocm on my machine without success for quite some time, and haven't been having much success. 

In reporting this issue, I was ran 
```
 echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
```

and had the following output:

```
GPU:
```

Which is was concerning, however, I do see that the GPU is discoverable via:

```
sudo lshw -numeric -C display
  *-display UNCLAIMED
       description: VGA compatible controller
       product: Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] [1002:67DF]
       vendor: Advanced Micro Devices, Inc. [AMD/ATI] [1002]
       physical id: 0
       bus info: pci@0000:09:00.0
       version: c7
       width: 64 bits
       clock: 33MHz
       capabilities: pm pciexpress msi vga_controller bus_master cap_list
       configuration: latency=0
       resources: memory:e0000000-efffffff memory:f0000000-f01fffff ioport:2000(size=256) memory:f0a00000-f0a3ffff memory:f0a60000-f0a7ffff
```

My kernel verison is:

```
uname -srmv
Linux 5.15.0-91-generic #101~20.04.1-Ubuntu SMP Thu Nov 16 14:22:28 UTC 2023 x86_64
```
Which seems to satisfy the supported OS requirements listed [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-distributions).



### Operating System

Ubuntu 20.04.6 LTS (Focal Fossa)"

### CPU

AMD Ryzen 7 2700X Eight-Core Processor

### GPU

AMD Instinct MI300X

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is NOT loaded, possibly no GPU devices

### Additional Information

Looking into it, it looks like rocm6.0 may not be supported for my device, however, I'm unable to determine what version of rocm I need. A pointer to the right version installation docs would be helpful here, thanks!

Also, the issue dialogue made me select a GPU, but didn't list my GPU, so I chose MI300X.

---

## 评论 (5 条)

### 评论 #1 — c0dn (2024-01-29T02:44:06Z)

On ROCm 6.0 release notes, there's a tick for MI300X for Ubuntu 22.04.5 only, I would try that first.
If your company does not mind a arch distribution, you can try it too. The community maintained packages work well, even on newer kernels. 
Just remember, you need ROCm 6.0 so enable extra-testing repo to get the rocm6.0 package on arch

---

### 评论 #2 — BujSet (2024-01-29T03:10:59Z)

Sorry, maybe I wasn't clear in my original post. I do **_not_** have a MI300 GPU, I believe I have a Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] device. I tried installing rocm6.0, but it seems that my device is not compatible so I'm trying to ascertain what version of rocm I **_can_** install that is compatible with my product. I only selected MI300 since the dropdown option **_did not list_** my GPU as a valid option. 

---

### 评论 #3 — c0dn (2024-01-29T03:13:55Z)

If that's the case, you will need to search around the internet for help.
The latest version of ROCm will not support such old cards, maybe try an older version with a few hacks to get it working

---

### 评论 #4 — BujSet (2024-01-29T03:19:37Z)

Ah I see, I was looking through the docs, hoping to find a table of some sort that could help identify what versions of rocm are support on what devices, but with no such luck. Will keep searching, thanks anyway though!

---

### 评论 #5 — cgmb (2024-01-29T08:05:00Z)

@BujSet, Ellesmere was once officially supported, but the last version of ROCm that was tested on Ellesmere was ROCm 3.5. You can probably still use the modern amdgpu-dkms, but you'll need to use the old rocm repo for HIP and the math libraries. Support for Ellesmere was still enabled in a number of later releases, but I'm not sure how well it worked since it was not tested. On some later releases, you need to set the environment variable `ROC_ENABLE_PRE_VEGA=1` for your GPU to be recognized.

IIRC, these ROCm 3.5 packages were built for Ubuntu 18.04:
https://repo.radeon.com/rocm/apt/3.5.1/


---
