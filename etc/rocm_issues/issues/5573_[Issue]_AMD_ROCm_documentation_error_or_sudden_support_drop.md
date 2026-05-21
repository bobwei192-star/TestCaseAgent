# [Issue]: AMD ROCm documentation error or sudden support drop?

> **Issue #5573**
> **状态**: closed
> **创建时间**: 2025-10-25T22:20:34Z
> **更新时间**: 2025-10-30T20:16:10Z
> **关闭时间**: 2025-10-30T20:16:10Z
> **作者**: ghost
> **标签**: Documentation, status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5573

## 标签

- **Documentation** (颜色: #5319e7)
- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Hey, today I read the ROCm documentation again and I was shocked, my 6950xt is not listed in the Linux installation guide anymore. It was always listed with AMD Radeon RX 6950 XT	RDNA2	gfx1030 and working runtime + HIP SDK.

Earlier this year I heard that you guys worked on WSL2 support and even created a ROCm wishlist for WSL. I was so, so happy to read this, sadly RDNA2 is still not supported, but whatever, I'm glad that it works on Linux. But I'm afraid now, because my GPU isn't even listed for the Linux installation guide anymore... is this because of ROCm 7?

I'm running Fedora 42 now and ROCm is packaged in the official repo, it's ROCm 6.3.x, it works! Even with a 6.16 or 6.17 kernel.

Dear AMD ROCm team, I can live without WSL support, but will you at least support us RDNA2 users on Linux? I have not tried ROCm 7 on Linux yet and I'm afraid to, please don't drop the support, when it worked on previous versions.

### Operating System

Linux & Windows

### CPU

5800x3d

### GPU

RDNA2 6950xt

### ROCm Version

6.3.x & 7.x?

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — ianbmacdonald (2025-10-27T17:30:26Z)

Not speaking on behalf of AMD, but recent research into where the best bang for the buck is in local inference lead me to the Strix Halo (RDNA 3.5) and RX 7000 XTX (RDNA3), as there is a gap in the instruction set between RDNA2 and RDNA3, specifically with matrix math capabilities.   I think this might unfortunately leave RDNA2 behind for AI related application library support. This is where some of the biggest jumps in speed have come from in RDNA3+  https://gpuopen.com/learn/wmma_on_rdna3/  

---

### 评论 #2 — harkgill-amd (2025-10-27T18:02:21Z)

Hi @VibeCoding1337, we haven't dropped any support with ROCm 7, only expanded. The 6950 XT and other 6000 series gaming cards were never listed in our support matrices as far as I'm aware - could you point me to which matrix you're referring to? They do still fall under `gfx1030`, the same architecture AMD Radeon PRO W6800 which means you should get a similar level of usability, we just haven't validated the release for your card specifically.

For gfx1030, you can also use [TheRock](https://github.com/ROCm/TheRock/blob/main/RELEASES.md) which recently added ROCm wheels (https://github.com/ROCm/TheRock/commit/919078957d953e6464a165631e3404d7c301ceed)  and is in the process of enabling torch wheels.

If you do run into any issues with the Fedora ROCm 7 packages w/ your 6950 XT, feel free to share it in this thread or create a new issue and we can take a deeper look to see if there are any regressions.



---

### 评论 #3 — GreenShadows (2025-10-27T18:58:33Z)

> Hi [@VibeCoding1337](https://github.com/VibeCoding1337), we haven't dropped any support with ROCm 7, only expanded. The 6950 XT and other 6000 series gaming cards were never listed in our support matrices as far as I'm aware - could you point me to which matrix you're referring to? They do still fall under `gfx1030`, the same architecture AMD Radeon PRO W6800 which means you should get a similar level of usability, we just haven't validated the release for your card specifically.
> 
> For gfx1030, you can also use [TheRock](https://github.com/ROCm/TheRock/blob/main/RELEASES.md) which recently added ROCm wheels ([ROCm/TheRock@9190789](https://github.com/ROCm/TheRock/commit/919078957d953e6464a165631e3404d7c301ceed)) and is in the process of enabling torch wheels.
> 
> If you do run into any issues with the Fedora ROCm 7 packages w/ your 6950 XT, feel free to share it in this thread or create a new issue and we can take a deeper look to see if there are any regressions.

Probably here, where they promised broad support.

https://github.com/ROCm/ROCm/discussions/4276

<img width="1080" height="2303" alt="Image" src="https://github.com/user-attachments/assets/0b37a472-7a43-4e3e-8d24-adf147688c7d" />

---

### 评论 #4 — harkgill-amd (2025-10-27T19:06:12Z)

That matrix is for the HIP SDK on Windows where the 6950XT is still supported in the latest release https://rocm.docs.amd.com/projects/install-on-windows/en/develop/reference/system-requirements.html#windows-supported-gpus-and-apus. 

The confusion between matrices and documentation spaces is something we're well aware of and are in the process of resolving. The ROCm 7.9 preview compatibility matrix provides a glimpse into what a future matrix could look like https://rocm.docs.amd.com/en/7.9.0-preview/compatibility/compatibility-matrix.html#rocm-compatibility-matrix.

---

### 评论 #5 — ghost (2025-10-28T00:04:11Z)

Thank you all for the clarifications! And yes, I meant the ROCm device support wishlist that @GreenShadows linked. Also thanks @harkgill-amd. I’m happy to hear support wasn’t dropped, just expanded.

I was a bit confused because the ROCm Linux install page looks different now:
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/

I thought I had previously seen the RX 6950 XT listed as supported, but maybe I mixed it up with gfx1030 compatibility.


I do have one more question: ROCm officially supports specific kernels and distributions, and I’ve experienced breakage after kernel updates on some rolling-release distros. For example, ROCm officially supported kernel 6.8 but it still worked through 6.13, but stopped with 6.14.

However, Fedora Workstation seems to keep ROCm working even with very new kernels (up to 6.17 in my tests). Is that because Fedora maintains its own ROCm packages to match each kernel update? And what exactly prevents upstream ROCm from supporting newer kernels more quickly? I understand this isn’t usually a problem on LTS distros, because the kernel version stays pretty much the same, but how does Fedora manage to stay compatible even though it isn’t officially supported?

<img width="837" height="979" alt="Image" src="https://github.com/user-attachments/assets/8881a41b-337f-4b5c-9345-799f564cde81" />

---

### 评论 #6 — harkgill-amd (2025-10-30T18:31:26Z)

> ROCm officially supports specific kernels and distributions, and I’ve experienced breakage after kernel updates on some rolling-release distros. For example, ROCm officially supported kernel 6.8 but it still worked through 6.13, but stopped with 6.14.

What you're seeing in these breakages is that the amdgpu-dkms driver packaged with your ROCm release fails to build for a specific kernel version (in your case it was 6.14). Historically, the amdgpu-dkms driver and ROCm were tightly coupled which is why when dkms fails to build, it's deemed that ROCm as a whole doesn't work for that kernel version. We've since been working on decoupling the two pieces of software ([ref](https://rocm.blogs.amd.com/ecosystems-and-partners/instinct-gpu-driver/README.html)) so that we can get to the point where unless the "Instinct driver" is required, users can go ahead and use ROCm with the in-kernel amdgpu drivers. 

This is exactly the case on Fedora. The distro hosts it's own ROCm packages and recommends using the in-kernel drivers.  amdgpu-dkms is never installed so there's no need to wait for there to be support for your kernel. https://fedoraproject.org/wiki/SIGs/HC#Quick_Start.

---

### 评论 #7 — ghost (2025-10-30T20:16:10Z)

Thank you very much for you help and info, I don't have any further questions. Have a nice day :) @harkgill-amd 

---
