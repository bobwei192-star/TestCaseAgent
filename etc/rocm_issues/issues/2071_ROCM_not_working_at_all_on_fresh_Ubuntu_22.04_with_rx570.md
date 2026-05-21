# ROCM not working at all on fresh Ubuntu 22.04 with rx570

> **Issue #2071**
> **状态**: closed
> **创建时间**: 2023-04-21T15:55:44Z
> **更新时间**: 2023-04-22T03:30:34Z
> **关闭时间**: 2023-04-22T02:01:10Z
> **作者**: ColdSpirit0
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2071

## 描述

Hi! I spent multiple days in trying to install ROCm on my Mint 21, based on Ubuntu 22, but got zero result.

I tried to install different versions with different ways; tried to install even ROCm 4.3.1, which should work on my GPU, but no; with dkms and without; downgraded kernels min to 5.14.0. It was no success for me to install ROCm 3.5.1, because it not building, and also old kernel not loading. I tried to install legacy opencl, but it not installing.

Today I installed fresh Ubuntu 22.04 to check it is just my OS or really ROCm not working. I installed ROCm 5.4.3 and it gave me same results - just no GPU agent in rocminfo and no devices in clinfo. 

GPU: XFX rx570 8gb
Ubuntu clinfo & rocminfo output: [info.log](https://github.com/RadeonOpenCompute/ROCm/files/11297349/info.log)


---

## 评论 (4 条)

### 评论 #1 — xuhuisheng (2023-04-21T22:22:57Z)

As we know, RX570 aka gfx803 was the only card which need PCIe atomic feature.
So you can check it with `dmesg | grep kfd`, if there is something like `[skip](kfd: skipped device 1002:7300, PCI rejects atomics)`, it said your cpu or motherboard cannot support PCIe atomic feature, so gfx803 cannot run properly.


---

### 评论 #2 — ColdSpirit0 (2023-04-22T02:01:10Z)

@xuhuisheng oh thank you! I had to read [manual](https://docs.amd.com/bundle/Hardware_and_Software_Reference_Guide/page/Hardware_and_Software_Support.html) much carefully... I spent so much time to get it to work, but now it clear for me. 

I have this line in dmesg:
`[    3.091074] kfd kfd: amdgpu: skipped device 1002:67df, PCI rejects atomics 730<0`

I can use this GPU on Windows with DirectML, maybe similar workaround existing on Linux? 

---

### 评论 #3 — xuhuisheng (2023-04-22T02:12:30Z)

@ColdSpirit0 
The AMD dont want to reply for gfx803 PCIe atomic question.

Even RDNA1 and RDNA2 can upgrade firmware to remove PCIe atomic requirement.

I am afraid gfx803 had been abandoned.

---

### 评论 #4 — ColdSpirit0 (2023-04-22T03:30:34Z)

Thank you again @xuhuisheng . Hope AMD will make the fix someday.

---
