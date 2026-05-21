# Can't use Rocm in wsl

> **Issue #4739**
> **状态**: closed
> **创建时间**: 2025-05-14T11:40:44Z
> **更新时间**: 2025-05-30T15:22:00Z
> **关闭时间**: 2025-05-30T15:21:59Z
> **作者**: hippy258
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4739

## 描述

### Problem Description

I followed the instructions in the documentation, but when using the rocminfo command, I can only see the CPU.https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html#post-install-verification-check

### Operating System

5.15.167.4-microsoft-standard-WSL2 Ubuntu 24.04.2 LTS

### CPU

AMD Ryzen 7 5700X 8-Core Processor

### GPU

AMD Redon 9700xt

### ROCm Version

amdgpu-install_6.3.60304-1_all.deb

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

### 评论 #1 — OrsoEric (2025-05-14T12:50:38Z)

[Your 7900XT should be compatible](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html), it's recomended that you use Ubuntu 22.



---

### 评论 #2 — hippy258 (2025-05-14T12:54:57Z)

> [Your GPU should be compatible](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html), it's recomended that you use Ubuntu 22.

I'm sorry, I misspoke, the GPU model is 9070xt, but I will try what you mentioned.

---

### 评论 #3 — OrsoEric (2025-05-14T13:01:19Z)

The 9070XT isn't listed in the compatibility matricies, I don't know if it the documentation is not updated, or the 9070XT is not supported by ROCm.

As an alternative, AMD put work in the DirectML ONNX runtime that should work with the 9070XT out of the box. On my system DirectML still has a 1/2 to 3/4 performance loss compared to ROCm (up from a 19/20 performance loss a few months ago), but it's very easy to setup, it should work out of the box directly under windows, at least it does on my 7900XTX. An application that uses it is Amuse.

For LLM inference, the Vulkan runtime works on my 7900XTX under windows out of the box, you could try if it works for the 9070XT as well.



---

### 评论 #4 — hippy258 (2025-05-14T13:07:53Z)

> The 9070XT isn't listed in the compatibility matricies, I don't know if it the documentation is not updated, or the 9070XT is not supported by ROCm.
> 
> As an alternative, AMD put work in the DirectML ONNX runtime that should work with the 9070XT out of the box. On my system DirectML still has a 1/2 to 3/4 performance loss compared to ROCm (up from a 19/20 performance loss a few months ago), but it's very easy to setup, it should work out of the box directly under windows, at least it does on my 7900XTX. An application that uses it is Amuse.
> 
> For LLM inference, the Vulkan runtime works on my 7900XTX under windows out of the box, you could try if it works for the 9070XT as well.

Thank u,my friend,I will try it later.

---

### 评论 #5 — Matthew-Jenkins (2025-05-14T13:25:39Z)

@hippy258 
The 9 series is not supported. If it isn't on the matrix, then it isn't supported. rocm support lags 6-12 months for consumer cards. Based on past performance support will probably make it in around fall. Then expect rocm to make it into whatever distro in 6-12 months from that. However since rocm is commonly bundled with pytorch you might not need to wait for your distro.

Until then, you can use vulkan. It misses out on some performance and when it crashes it can take a long time to recover. But it does work. I can report vulkan works great with llamacpp and lm studio. I THINK ollama uses vulkan too. I do not know if the ai cores will be used through vulkan, if I had to guess it wouldn't. But at least you get the raster performance.
https://github.com/ggml-org/llama.cpp/releases/download/b5379/llama-b5379-bin-ubuntu-vulkan-x64.zip

You can also try using rocm by forcing it to run as a previous generation. I'm not sure if that will work - but it might unlock 6 or 7 series performance if it does. If you do that, when using pytorch, there is a flag to use MIOPEN_FIND or something like that. You want mode 1 which runs a benchmark on startup to set the tuning params instead of using the built in pretuned numbers. It will make startup take a few minutes however. https://rocm.docs.amd.com/projects/MIOpen/en/latest/how-to/find-and-immediate.html#find-modes 

Try setting it to rx 6 series like so:
MIOPEN_FIND_MODE=1 HSA_OVERRIDE_GFX_VERSION=10.3.0 path/to/env/python main.py

---

### 评论 #6 — hippy258 (2025-05-14T13:34:47Z)

> [@hippy258](https://github.com/hippy258) The 9 series is not supported. If it isn't on the matrix, then it isn't supported. rocm support lags 6-12 months for consumer cards. Based on past performance support will probably make it in around fall. Then expect rocm to make it into whatever distro in 6-12 months from that. However since rocm is commonly bundled with pytorch you might not need to wait for your distro.
> 
> Until then, you can use vulkan. It misses out on some performance and when it crashes it can take a long time to recover. But it does work. I can report vulkan works great with llamacpp and lm studio. I THINK ollama uses vulkan too. I do not know if the ai cores will be used through vulkan, if I had to guess it wouldn't. But at least you get the raster performance. https://github.com/ggml-org/llama.cpp/releases/download/b5379/llama-b5379-bin-ubuntu-vulkan-x64.zip
> 
> You can also try using rocm by forcing it to run as a previous generation. I'm not sure if that will work - but it might unlock 6 or 7 series performance if it does. If you do that, when using pytorch, there is a flag to use MIOPEN_FIND or something like that. You want mode 1 which runs a benchmark on startup to set the tuning params instead of using the built in pretuned numbers. It will make startup take a few minutes however. https://rocm.docs.amd.com/projects/MIOpen/en/latest/how-to/find-and-immediate.html#find-modes
> 
> Try setting it to rx 6 series like so: MIOPEN_FIND_MODE=1 HSA_OVERRIDE_GFX_VERSION=10.3.0 path/to/env/python main.py

Thank you,I got it! I'm still a newbie in AI and just starting to figure things out. Really appreciate your detailed response – it's super helpful!

---

### 评论 #7 — Matthew-Jenkins (2025-05-14T14:19:20Z)

@hippy258 let me know if vulkan works for you on wsl or if doing the find mode and hsa override enables rocm for you.

---

### 评论 #8 — ppanchad-amd (2025-05-15T20:28:41Z)

Hi @hippy258 Please confirm if issue is resolved for you. If so, please close the ticket. Thanks!

---

### 评论 #9 — ppanchad-amd (2025-05-30T15:21:59Z)

Closing ticket due to lack of response.  Please feel to comment or re-open another ticket if you still have issue. Thanks!

---
