# Rocm6 not working with PCIE x1 gen1

> **Issue #2926**
> **状态**: closed
> **创建时间**: 2024-02-23T23:52:25Z
> **更新时间**: 2024-10-09T14:22:01Z
> **关闭时间**: 2024-10-09T14:22:01Z
> **作者**: userbox020
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2926

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

Hello, 
Im trying to use llamacpp with rocm6 and hipBlas under pcie x1 gen1 without success. 
So im using at the moment Vulkan

### Operating System

"22.04.4 LTS (Jammy Jellyfish)

### CPU

Intel(R) Core(TM) i7-7700T CPU @ 2.90GHz

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

hipBLAS

### Steps to Reproduce

git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp/
make LLAMA_HIPBLAS=1
./main -m /openhermes-2.5-neural-chat-v3-3-slerp.Q8_0.gguf -p "Hi you how are you" -ngl 90 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — nartmada (2024-02-24T02:24:44Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — jamesxu2 (2024-07-15T14:48:48Z)

Hi @userbox020 , can you provide more specific information about the failure you're experiencing - what kind of errors are printed? 

Some things that can help our investigation are:
- A full console log when you run llama_cpp
- The output of dmesg
- The output of ```/opt/rocm/bin/rocminfo --support```

Thanks!

---

### 评论 #3 — jamesxu2 (2024-07-15T16:01:52Z)

I will add that [ROCm uses PCIe atomics](https://rocm.docs.amd.com/en/latest/conceptual/More-about-how-ROCm-uses-PCIe-Atomics.html) which are a feature of PCIe gen 3.0+. The [documentation on system requirements](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#cpu-support) also states that you require a CPU that supports PCIe atomics (I believe your CPU does, but your motherboard's PCIe hardware doesn't), so using a PCIe gen 1 system probably will not work. However, we might be able to investigate further with logs.

You can check if your system supports PCIe atomics with the following command:
```grep flags /sys/class/kfd/kfd/topology/nodes/*/io_links/0/properties```

---

### 评论 #4 — userbox020 (2024-07-17T20:06:46Z)

@jamesxu2  sorry for the delay, i just saw the response. I have turn off my hobby computer that i use for testing AI stuff, going to turn it on this weekend and send you the errors. But llamacpp its the only one that works with PCIe x1 gen1 but only with a very old llamacpp version and rocm5.6. But also i was able to run llamacpp on pcie x1 gen1 it with vulkan and rocm6 

This weekend going to turn on my hobby computer that i use for AI stuff, i have there my AMD cards connected on a pcie x1 gen1 slots and going to run again llamacpp, also im interested in the cuda adaptor for rocm https://docs.scale-lang.com/ it will solve lots off error and will be able to run all the other LLM infering engines other than llamacpp there are few that are way more faster and better than llamacpp but only works with cuda


---

### 评论 #5 — jamesxu2 (2024-08-15T20:35:41Z)

Hi @userbox020 , do you have an update with more details on the errors you're seeing? 

Also, ROCm 6.2 [was released recently](https://rocm.docs.amd.com/en/latest/about/release-notes.html) you may be able to upgrade to see if there is a difference. 
 

---

### 评论 #6 — jamesxu2 (2024-10-09T14:22:01Z)

Closing this ticket due to lack of response. Feel free to reopen it @userbox020 if you get around to testing this issue. 

---
