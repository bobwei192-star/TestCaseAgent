# [Feature]: RX 7600 XT support

> **Issue #2901**
> **状态**: closed
> **创建时间**: 2024-02-16T23:56:36Z
> **更新时间**: 2025-06-01T18:01:35Z
> **关闭时间**: 2024-02-17T13:13:29Z
> **作者**: jonasgf
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2901

## 描述

### Suggestion Description

I recently bought an RX 7600 XT for primarily GPGPU purposes. I did unfortunately however not check the compatibility list before purchase and was sad to learn that my graphics card is currently not working with ROCm.

---

I have the latest ROCm packages installed (6.0.0).

`rocminfo` gives me the following:
```
$ /opt/rocm/bin/rocminfo --support
ROCk module is loaded
hsa api call failure at: /usr/src/debug/rocminfo/rocminfo-rocm-6.0.0/rocminfo.cc:1219
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```

`rocm-smi` lists the GPU as such:
```
0       [0x0518 : 0xc0]       N/A     N/A    N/A, N/A        None  None  0%   unknown  Unsupported    0%   0%    
        Navi 33 [Radeon RX 7                                                                                     
```

---

I first found the page listing [supported GPUs on Linux](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html). There is very few GPUs listed here.

The [supported GPUs on Windows](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html) page does list quite a few more GPUs, also the ones that AFAIK work well on Linux. I do not however see the RX 7600 XT listed here at all, so this gives me some hope that the GPU might be supported at some point.

I hope you can consider adding support for the RX 7600 XT, since it seems like a fantastic choice for ML and GPGPU in this budget range.

### Operating System

Arch Linux (Linux 6.7.4-arch1-1 x86_64)

### GPU

AMD Radeon RX 7600 XT

### ROCm Component

_No response_

---

## 评论 (11 条)

### 评论 #1 — jonasgf (2024-02-17T00:40:21Z)

Or am I mistaken, and this is supported as gfx1102? There might just be something wrong with my setup if others have gotten this to work. I am trying to get this to work on a headless server I just set up today.

---

### 评论 #2 — jonasgf (2024-02-17T03:22:13Z)

FWIW, I get the following in the kernel log when attempting to run `rocminfo`:
```
amdgpu 0000:09:00.0: amdgpu: Timeout waiting for VM flush ACK!
amdgpu 0000:09:00.0: amdgpu: Timeout waiting for VM flush ACK!
[drm] PCIE GART of 512M enabled (table at 0x0000008000000000).
[drm] PSP is resuming...
[drm:psp_hw_start [amdgpu]] *ERROR* PSP load kdb failed!
[drm:psp_resume [amdgpu]] *ERROR* PSP resume failed
[drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
amdgpu 0000:09:00.0: amdgpu: amdgpu_device_ip_resume failed (-62).
[drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
```

---

### 评论 #3 — jonasgf (2024-02-17T13:13:29Z)

So it seems like the problem was something with my setup. It works fine if I have a monitor attached to the graphics card.

I do however have to run my pytorch programs with `HSA_OVERRIDE_GFX_VERSION=11.0.0`.

And when it comes to the supported GPUs list, if the support is implied with the RX 7600 (non-XT), then my bad for misunderstanding. If there is a relevant difference then I think it should be added to the list if there is support for it.

---

### 评论 #4 — das-auge (2024-05-30T15:13:09Z)

I am not sure if I understood right:  Can you confirm that the RX 7600XT is provididing hardware acceleration for ROCm and Pytorch? 

---

### 评论 #5 — jonasgf (2024-05-30T19:38:54Z)

I was able to use it, yes. But I guess it is not officially supported.

---

### 评论 #6 — kozuch (2024-06-12T15:17:09Z)

AMD really sucks failing to provide proper support info. How they want to attack nVidia's market share like this? Is there maybe a community site where people would list supported cards themselves?

---

### 评论 #7 — kozuch (2024-06-12T17:45:47Z)

@jonasgf Do you have token generation speed from LLM (Llama 3 etc.) on this card?

---

### 评论 #8 — bdutta (2024-06-22T15:31:32Z)

@jonasgf would you mind sharing some information about the Linux OS/release you are running and what is the CPU/motherboard that you have ? I am looking at buying a RX 7600 XT for local LLM/inference (ollama/lmstudio), so would be needing ROCm support, but clearly AMD remains laggard with their documentation. They do mention need of PCI atomics in the processor, but reading some more posts, I gather that it might be a combination of processor and motherboard that ensure availability of PCI atomics for this GPU to work fine. I was hoping to reuse my existing i5-8400 it possible with this GPU.

---

### 评论 #9 — TeaCult (2024-10-07T09:31:44Z)

I made it work on archlinux with rocm 6.02 and torch 5.7 
gemma-2-27b-Q4  10.5 toks/sec 
SDXL %85 of RTX 3060 performance (I dont remember it/sec)   , force-fp16 fixes a lot in vae decoding 

Generally consumes too much ram in generations and training in pytorch compared to RTX although I preform frequent torch.cuda_empty_cache(). 

If bitsandbytes work (6.2 + torch nightly) , controlnets(comfy) does not , if controlnets work bitsandbytes does not. Is it a deal breaker ? Not sure. 

Bottom line: 
It works, You can generate images and use LLM inference on ggml gguf quantized files without any problem performantly. QLora tuning wont be working because of bitsandbytes and peft. 


---

### 评论 #10 — Deng-Xian-Sheng (2025-03-10T18:08:59Z)

run yolo12 by Ubuntu24 7600XT 8gb fail 

---

### 评论 #11 — henfri (2025-06-01T18:01:35Z)

Hello,

what about wsl? Is the 7600 XT supported?

The official Matrix does not show it as supported, but elsewhere I read that it works.

Greetings,
Hendrik

---
