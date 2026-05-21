# [Issue]: Ollama compatibility issue with kernel/drivers causes ROCm container conflict

> **Issue #5679**
> **状态**: closed
> **创建时间**: 2025-11-20T02:15:30Z
> **更新时间**: 2025-12-09T19:02:17Z
> **关闭时间**: 2025-12-09T19:02:17Z
> **作者**: ChenxiWu-Lab
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5679

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

Description:
There is a compatibility issue when running Ollama with AMD GPU drivers on different Linux kernel versions, which conflicts with running ROCm-based containers like vLLM.

Environment:

Ollama version: [v0.12.11](https://github.com/ollama/ollama/releases/tag/v0.12.11)

Kernel versions tested:

6.8.x + AMD official driver → Ollama runs initially but triggers GPU driver crash under certain conditions

6.17.8 + open-source amdgpu driver → Ollama runs stably

Problem:

On 6.8 kernel + official AMD driver:

Ollama starts and can process initial prompts

When Ollama automatically unloads models after some time, subsequent prompts cause GPU driver crash

Likely cause: official driver has issues with VRAM handling or model unloading

On 6.17.8 kernel + open-source driver:

Ollama runs stably without driver crashes

However, ROCm containers (e.g., vLLM) cannot run because /dev/kfd does not exist in the open-source driver environment

Steps to Reproduce:

Install Ollama on 6.8 kernel with official AMD driver

Run Ollama and process several prompts

Wait for Ollama to automatically unload a model, then send additional prompts

Observe GPU driver crash

Upgrade to 6.17.8 kernel and switch to open-source amdgpu driver

Ollama runs stably

Attempt to run vLLM ROCm container

Container fails to start: OCI runtime create failed: failed to create shim task, because /dev/kfd is missing

Impact:

Cannot use Ollama and ROCm GPU containers on the same system

Official driver is unstable with Ollama

Open-source driver prevents running ROCm containers on GPU

Expected Behavior:

Ollama runs stably with open-source drivers

Or official driver does not crash when models are automatically unloaded

Ideally, allow running both Ollama and ROCm containers on the same system

Additional Information:

Attach dmesg or kernel logs showing GPU driver crash

Attach ROCm container error logs if available

### Operating System

ubuntu24.4.3

### CPU

AMD 3960X

### GPU

AI pro R9700

### ROCm Version

latest（2025/11/15）

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — tcgu-amd (2025-11-20T18:22:45Z)

@ChenxiWu-Lab, thanks for reaching out! I am sorry you are experiencing crashes with ROCm. To better understand the problem, can you provide:

1. The official amdgpu driver version, amdgpu-dkms version.
2. The open source driver / version.
3. The ROCm version
4. Output of rocminfo. 
5. Relevant dmsg logs after the crash. 

Thanks! 

---

### 评论 #2 — ChenxiWu-Lab (2025-11-22T01:44:28Z)

Thanks for your reply. At the time, I urgently needed to use Ollama, so I reinstalled the system multiple times, and the logs weren't properly preserved.

However, the issue I submitted on Ollama might be helpful:https://github.com/ollama/ollama/issues/13085

And I learned about switching kernels to use open-source drivers from this post:https://github.com/ollama/ollama/issues/12893#issuecomment-3534572020

I remember my ROCM and official driver versions were 7.1, while the current open-source driver uses the version that comes with the kernel.

$ modinfo amdgpu | grep version
srcversion:     921A6B7E58497CAAA0C1C6E
vermagic:       6.17.8-061708-generic SMP preempt mod_unload modversions
parm:           hws_gws_support:Assume MEC2 FW supports GWS barriers (false = rely on FW versio check (Default), true = force supported) (bool)

---

### 评论 #3 — tcgu-amd (2025-11-24T18:05:30Z)

Hi @ChenxiWu-Lab, sorry I am still confused about what you meant by open source driver.. Just to clarify, the official amdgpu driver *is open source* -- it is part of the the mainline linux kernel itself. I assumed you meant a third party driver but the links you provided does not seem to contain anything of the sort. If you are simply using the amdgpu driver built into kernel 6.17.8, you should have /dev/kfd available. How are you launching the ROCm containers? Did you map /dev/kfd to the containers? Thanks! 

Edit: Here's a guide for launching Docker on ROCm https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html, just in case. 

---

### 评论 #4 — tcgu-amd (2025-11-25T19:06:30Z)

Also @ChenxiWu-Lab, for running Ollama on 6.8.0, did you by chance install amdgpu-dkms with ROCm? Or did you directly run Ollama on bare metal? 

---

### 评论 #5 — ChenxiWu-Lab (2025-11-26T02:29:46Z)

> Also [@ChenxiWu-Lab](https://github.com/ChenxiWu-Lab), for running Ollama on 6.8.0, did you by chance install amdgpu-dkms with ROCm? Or did you directly run Ollama on bare metal?

Thank you very much for your reply. I apologize if I wasn't clear enough. The 6.17.8 kernel uses the kernel's built-in drivers. Ollama, however, uses an installation method (directly installed on the Ubuntu host as a system service) instead of Docker.

Initially, with the 6.8 kernel, I had a full installation of the 7.1.70100-1 driver and ROCM, and amdgpu-dkms was also installed. I encountered the previous problem: Ollama would freeze during model uninstallation, ROCM-SMI would continuously show that VRAM was occupied at 100%, but the temperature was at normal idle temperature.

Just a few days ago, I installed the 6.4.60403-1 driver and ROCM in the 6.8 kernel, and the problem disappeared. Then, to run a virtual machine, I installed another NVIDIA graphics card and performed hardware passthrough. Then the problem reappeared.

The current problem might be related to my BIOS settings (6.8 kernel, 6.4.6 driver, virtual machine): I forgot to enable Above 4G Decoding and Re-Size BAR.

However, this issue also occurred when using the 7.1.7 driver and ROCM with the 6.8 kernel, even without multiple GPUs or a virtual machine. Specifically, the Ollam model would freeze during unloading, ROCM-SMI would continuously show that VRAM was occupied at 100%, but the GPU temperature was at normal idle temperature.

After a long struggle with the AI, it concluded that this error usually indicates a Ring Hang in the GPU firmware or compute unit, and the driver failed to reset the GPU, which is related to AMD GPU power-saving strategies. I don't know if this information is helpful.

In short, my next step will be to try updating the motherboard BIOS and enabling the corresponding PCIe function, then try again to see if the error persists.

The query error is:
chenxi@chenxilab:~$ sudo dmesg -T | grep -i amdgpu

[Wed Nov 26 10:33:04 2025] [drm] amdgpu kernel modesetting enabled.

[Wed Nov 26 10:33:04 2025] [drm] amdgpu version: 6.12.12

[Wed Nov 26 10:33:04 2025] amdgpu: Virtual CRAT table created for CPU

[Wed Nov 26 10:33:04 2025] amdgpu: Topology: Add CPU node

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: enabling device (0006 -> 0007)

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 0 <soc24_common>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 1 <gmc_v12_0>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 2 <ih_v7_0>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 3 <psp>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 4 <smu>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 5 <dm>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 6 <gfx_v12_0>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 7 <sdma_v7_0>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 8 <vcn_v5_0_0>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 9 <jpeg_v5_0_0>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: detected ip block number 10 <mes_v12_0>

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from VFCT

[Wed Nov 26 10:33:04 2025] amdgpu: ATOM BIOS: 113-48WD6SHD1-P02

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: MEM ECC is active.

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: SRAM ECC is not presented.

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: RAS INFO: ras initialized successfully, hardware ability[101] ras_mask[101]

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: VRAM: 30576M 0x0000008000000000 - 0x0000008776FFFFFF (30576M used)

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: GART: 512M 0x0000000000000000 - 0x000000001FFFFFFF

[Wed Nov 26 10:33:04 2025] [drm] amdgpu: 30576M of VRAM memory ready

[Wed Nov 26 10:33:04 2025] [drm] amdgpu: 32068M of GTT memory ready.

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x0000008000000000).

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: GECC is currently enabled, which may affect performance

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: To disable GECC, please reboot the system and load the amdgpu driver with the parameter amdgpu_ras_enable=0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684a00 (104.74.0)

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: SMU is initialized successfully!

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0x4000000

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: program CP_MES_CNTL : 0xc000000

[Wed Nov 26 10:33:04 2025] amdgpu: HMM registered 30576MB device memory

[Wed Nov 26 10:33:04 2025] kfd kfd: amdgpu: Allocated 3969056 bytes on gart

[Wed Nov 26 10:33:04 2025] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1

[Wed Nov 26 10:33:04 2025] amdgpu: Virtual CRAT table created for GPU

[Wed Nov 26 10:33:04 2025] amdgpu: Topology: Add dGPU node [0x7551:0x1002]

[Wed Nov 26 10:33:04 2025] kfd kfd: amdgpu: added device 1002:7551

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: SE 4, SH per SE 2, CU per SH 8, active_cu_number 64

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 6 on hub 0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 7 on hub 0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 8 on hub 0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 9 on hub 0

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: amdgpu: Using BACO for runtime pm

[Wed Nov 26 10:33:04 2025] [drm] Initialized amdgpu 3.63.0 20150101 for 0000:03:00.0 on minor 1

[Wed Nov 26 10:33:04 2025] amdgpu 0000:03:00.0: [drm] Cannot find any crtc or sizes

[Wed Nov 26 10:33:07 2025] snd_hda_intel 0000:03:00.1: bound 0000:03:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])

[Wed Nov 26 10:34:45 2025] amdgpu: Freeing queue vital buffer 0x704611600000, queue evicted

[Wed Nov 26 10:37:05 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:05 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:05 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:05 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:05 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:05 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:05 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:05 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:05 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:05 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:06 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:06 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:06 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:06 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:06 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:06 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:06 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:06 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]

[Wed Nov 26 10:37:06 2025] Workqueue: events amdgpu_tlb_fence_work [amdgpu]

[Wed Nov 26 10:37:06 2025]  amdgpu_tlb_fence_work+0x29/0x140 [amdgpu]




---

### 评论 #6 — tcgu-amd (2025-11-26T18:08:28Z)

Hi @ChenxiWu-Lab Thank you for the clarifications! Can you explain a bit more about what's going on with the NVIDIA card? Installing both cards side-by-side is known to be prone to causing issues. 

Also, it would be helpful if you can show the amdgpu version in amd-smi as well (note amdgpu is versioned independently of ROCm). 

I will try to look into what's going on in the meantime. Thanks! 

---

### 评论 #7 — tcgu-amd (2025-11-27T19:13:49Z)

Hi @ChenxiWu-Lab, can you also run `journalctl -u ollama --no-pager --follow --pager-end | grep "loaded ROCm"` To verify that ollama is indeed using ROCm as the backend? Because ROCm backend does rely on /dev/kfd, and it is very weird that Ollama works but /dev/kfd is not found..


---

### 评论 #8 — tcgu-amd (2025-12-01T19:41:26Z)

It is probably worth mentioning as well that the latest Ollama ships with ROCm 6.3.3 built-in, which didn't support gfx1200. I recompiled Ollama with the latest ROCm 7.1 on 6.14 kernel and didn't observe the issue you described. 

---

### 评论 #9 — tcgu-amd (2025-12-09T19:02:17Z)

Hi @ChenxiWu-Lab, this issue will be closed for now due to no activity. Please feel free to continue to follow if further assistance is needed. Thanks! 

---
