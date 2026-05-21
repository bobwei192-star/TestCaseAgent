# ROCm performance anomaly

> **Issue #4722**
> **状态**: closed
> **创建时间**: 2025-05-08T10:51:09Z
> **更新时间**: 2025-05-13T17:57:43Z
> **关闭时间**: 2025-05-13T17:57:18Z
> **作者**: chowdri
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4722

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I have elementaryOS/ubuntu 24.04 and  rocm 6.4 setup with gfx1100 on my system following this guide (--usecase=rocm): https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/amdgpu-installer/amdgpu-installer-ubuntu.html

Further, I built llama.cpp on my system using this guide (for HIP build I used `-DGGML_HIP_ROCWMMA_FATTN=ON` option) : https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md 

When I use LM Studio (0.3.15 Build 11), it offers vulkan and rocm runtime options: ROCm llama.cpp (Linux) v1.29.0 and Vulkan llama.cpp (Linux) v1.29.0. I don't know if it employs the rocm installation of the system. 

I loaded a gemma 3 12b (q8) model on the gpu using both runtime options sequentially (ROCm then Vulkan). For a given question asked on both runtime cases I get the following outcome: 

![Image](https://github.com/user-attachments/assets/fb4c06a7-7986-479f-a870-3146cc25d829)

![Image](https://github.com/user-attachments/assets/39cf64b9-f4f1-4cc5-a3e8-e193dbaa1353)

![Image](https://github.com/user-attachments/assets/6d051c5c-19de-431d-b1db-4c2a483a87d3)

ROCm : 16.91 tok/sec, 1514 tokens, 3.49s to first token, Stop reason: EOS Token Found
Vulkan: 24.43 tok/sec, 1514 tokens, 4.93s to first token, Stop reason: EOS Token Found

This outcome is consistently repeatable (within reasonable margins).

I thought that ROCm was supposed to be the faster scheme. Is this an issue with LM Studio or the ROCm installation? 

Much thanks for any time and effort expended shedding light on the issue or any help resolving it. 

---

## 评论 (12 条)

### 评论 #1 — IMbackK (2025-05-08T11:47:32Z)

This has nothing to do with rocm, ggml/llamacpp's cuda/hip kernels are just worse on gfx11 than the vulkan ones. The vulkan ones where developed on rdna with its characteristics in mind while the cuda/hip kernels where developed with nvidia devices in mind and not optimized for rdna. I have spent some time optimizeing the cuda/hip kernels for gcn/cdna but that dosent help rdna/gfx11 any.

In gpu programing there is unfortionatly no performance protablility, for good performance every application needs to be optimized for eatch architecture, there is not that mutch amd/rocm can do about that.

---

### 评论 #2 — chowdri (2025-05-08T11:53:22Z)

This is way beyond my skill set. However, what can I learn and do to optimize said kernels for my hardware and application? I have the llama.cpp repo on my system. 
Also, I have a Vega 64, which runs fine on vulkan. Anyway to get it working on rocm?

---

### 评论 #3 — IMbackK (2025-05-08T12:43:35Z)

For optimization you need to learn gpu programing: cuda and hip, lots of good places/guides to start llerning cuda so i would start there.  On linux gfx900 (Vega10) still works completely fine with rocm. I would recommend a distrobution with rocm in its official repos like arch linux, nixos, fedora or debian then just compile the hip version of llamacpp. On windows i belive you are out of luck.

Vega10 is pretty bad at quantized llms btw as it lacks 8bit dot product instructions, which where introduced with vega20/Radeon VII.

---

### 评论 #4 — chowdri (2025-05-09T16:07:15Z)

Yeah, Vega 64 with 8 GB VRAM has limits on what models it can run fast. However, HBCC allows it to run much bigger models (at a glacial pace). The VRAM is HBM, so that's a plus (kinda sorta).

On rocm 6.4, support for Vega 64 was dropped by rocm. On vulkan, the Vega is giving me 36 tok/sec on 3B q4 models vs 55 tok/sec with 7900 GRE (gfx1100). Not bad for a 2017 card. 

---

### 评论 #5 — IMbackK (2025-05-09T16:23:21Z)

no, gfx900 still works fine on rocm.

---

### 评论 #6 — chowdri (2025-05-09T17:00:30Z)

I had to buy gfx1100 because gfx900 was not supported this year. 
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html

Perhaps it works on older rocm versions. However, I have checked, gfx900 can do simple compute operations with rocm & pytorch (basic matrix multiplications).

But when I run tensorflow, it says no binaries for gfx900. 


---

### 评论 #7 — IMbackK (2025-05-09T17:31:05Z)

No it still works, even in git rocm (ie what will be rocm 7.0)

official support has been dropped for a really long time (rocm 4.5 or so) but it still works, some stuff you may have to compile with the arch enabled.

You may want to check out the packages not built by amd like those in distro pacakges, they still build for gfx900 across the board, even amd still builds for gfx900 in most places.

---

### 评论 #8 — chowdri (2025-05-09T17:34:27Z)

how to compile llama.cpp for HIP? `-DAMDGPU_TARGETS=gfx900` will work?

---

### 评论 #9 — IMbackK (2025-05-09T20:54:11Z)

sure, also just compileing on a device with a gfx900 gpu installed will make it build for gfx900 by default, you also need to have rocblas compiled for gfx900, however this is still done by default for every rocm version see https://github.com/ROCm/rocBLAS/blob/9391ecc1325c55db2c79e0cb7f61c781bfaa6fd2/CMakeLists.txt#L88

---

### 评论 #10 — chowdri (2025-05-10T09:30:29Z)

I can't see rocm 6.4 on it. But let's assume it does. I tried compiling llama.cpp HIP for gfx900 and it completes. However, when I run LM Studio. The rocm llama.cpp runtime does not provide an option for gfx900. 


---

### 评论 #11 — ppanchad-amd (2025-05-13T15:26:44Z)

Hi @chowdri. Internal ticket has been created to further assist you with your issue. Thanks!

---

### 评论 #12 — tcgu-amd (2025-05-13T17:57:18Z)

@chowdri. Thank you for reaching out! I am sorry you are experiencing performance issues with ROCm. As has been summed up in the previous replies, there's not a lot we can do regarding the issue right now. I would just like to add that we have been [listening for feedbacks regarding supporting older ROCm architectures](https://github.com/ROCm/ROCm/discussions/4276), and will hopefully expand our support soon. For now, customized build seems like the best option (some modifications might be needed allow unsupported runtime to be used by thrid-party applications such as llama.cpp).

I will be closing this issue for now, but please feel free to continue the discussion below. If you have further questions, I will be happy to help the best I can. Thanks! :)

---
