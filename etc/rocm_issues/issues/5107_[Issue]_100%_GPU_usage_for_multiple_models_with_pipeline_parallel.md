# [Issue]: 100% GPU usage for multiple models with pipeline parallel

> **Issue #5107**
> **状态**: open
> **创建时间**: 2025-07-27T20:36:05Z
> **更新时间**: 2025-12-16T15:38:20Z
> **作者**: DKingAlpha
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5107

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- zichguan-amd

## 描述

### Problem Description

`rocm-smi` reports 100% GPU Usage when **multiple** models load with device_map="auto" on a multi-gpu host, idle state.

The 100% GPU issue looks like not a third-party library implementation problem. It happens to:
1. llama.cpp with "-dev ROCm0,ROCm1,...".
2. transformers (sentence_transformers) with device_map="auto"

process CPU usage is around 0%.

I am using gfx906 so I can only test on ROCm 6.3.3.


### Operating System

Arch Linux

### CPU

2 x Intel(R) Xeon(R) E5-2680 v4 (56) @ 3.30 GHz

### GPU

4x MI50 32GB

### ROCm Version

ROCm 6.3.3

### ROCm Component

_No response_

### Steps to Reproduce

Code to Reproduce:
```py
import torch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "Qwen/Qwen3-Embedding-0.6B",
    model_kwargs={
        "device_map": "auto",
        "torch_dtype": torch.float16
    },
    tokenizer_kwargs={"padding_side": "left"},
)
```

Steps to Reproduce:
1. Install torch with ROCm acceleration.
2. pip install sentence_transformers
3. run code above, in two seperate python terminal.

After First model load
```sh
=========================================== ROCm System Management Interface ===========================================
===================================================== Concise Info =====================================================
Device  Node  IDs              Temp    Power     Partitions          SCLK    MCLK    Fan     Perf  PwrCap  VRAM%  GPU%
[3m              (DID,     GUID)  (Edge)  (Socket)  (Mem, Compute, ID)                                                     [0m
========================================================================================================================
0       2     0x66a1,   29631  45.0°C  24.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  4%     0%
1       3     0x66a1,   33535  47.0°C  19.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  1%     0%
2       4     0x66a1,   17183  43.0°C  18.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  1%     0%
3       5     0x66a1,   55003  43.0°C  18.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  2%     0%
========================================================================================================================
================================================= End of ROCm SMI Log ==================================================
```

After Second model load
```sh
============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp    Power     Partitions          SCLK     MCLK    Fan     Perf  PwrCap  VRAM%  GPU%
[3m              (DID,     GUID)  (Edge)  (Socket)  (Mem, Compute, ID)                                                      [0m
==========================================================================================================================
0       2     0x66a1,   29631  44.0°C  53.0W     N/A, N/A, 0         1725Mhz  350Mhz  15.69%  auto  225.0W  8%     100%
1       3     0x66a1,   33535  48.0°C  45.0W     N/A, N/A, 0         1725Mhz  350Mhz  16.08%  auto  225.0W  3%     100%
2       4     0x66a1,   17183  44.0°C  48.0W     N/A, N/A, 0         1725Mhz  350Mhz  14.51%  auto  225.0W  3%     100%
3       5     0x66a1,   55003  44.0°C  44.0W     N/A, N/A, 0         1725Mhz  350Mhz  14.51%  auto  225.0W  4%     100%
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
```

After Second model **unload**
```sh
=========================================== ROCm System Management Interface ===========================================
===================================================== Concise Info =====================================================
Device  Node  IDs              Temp    Power     Partitions          SCLK    MCLK    Fan     Perf  PwrCap  VRAM%  GPU%
[3m              (DID,     GUID)  (Edge)  (Socket)  (Mem, Compute, ID)                                                     [0m
========================================================================================================================
0       2     0x66a1,   29631  44.0°C  24.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  4%     0%
1       3     0x66a1,   33535  48.0°C  18.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  1%     0%
2       4     0x66a1,   17183  44.0°C  18.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  1%     0%
3       5     0x66a1,   55003  44.0°C  18.0W     N/A, N/A, 0         925Mhz  350Mhz  14.51%  auto  225.0W  2%     0%
========================================================================================================================
================================================= End of ROCm SMI Log ==================================================
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```sh
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

......

*******
Agent 3
*******
  Name:                    gfx906
  Uuid:                    GPU-12b008e17337ecd9
  Marketing Name:          AMD Radeon Graphics
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    2
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
    L2:                      8192(0x2000) KB
  Chip ID:                 26273(0x66a1)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   1725
  BDFID:                   1024
  Internal Node ID:        2
  Compute Unit:            60
  SIMDs per CU:            4
  Shader Engines:          4
  Shader Arrs. per Eng.:   1
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          64(0x40)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        40(0x28)
  Max Work-item Per CU:    2560(0xa00)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 472
  SDMA engine uCode::      145
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    33538048(0x1ffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
```

### Additional Information

Detailed test with llama.cpp:
1. If multiple MultiGPU models shares any same GPU, `shared GPU` usage goes to 100% instantly on load. `exclusive GPU` usage stays at 0%.
2. SingleGPU model + MultiGPU model works fine.

Test Table:

| First Model -dev | Second Model -dev | 100% GPU Usage (Idle) | 0% GPU Usage (Idle) |
| - | - | - | - |
| 0, 1 | 0, 1 | 0, 1| |
| 0, 1 | 1, 2 | 1|0, 2 |
| 0, 1 | 2, 3 | |0, 1, 2, 3 |
| 0, 1 | 1 | | 0, 1|
| 0, 1 | 2 | | 0, 1, 2|
| 0 | 1 | | 0, 1|

* number in cells: ROCm device index


---

## 评论 (14 条)

### 评论 #1 — ppanchad-amd (2025-07-28T13:30:55Z)

Hi @DKingAlpha. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — zichguan-amd (2025-08-14T15:34:40Z)

Hi @DKingAlpha, I'm able to repro the issue with your `sentence_transformers` setup, as well with 2x 7900XTX + ROCm 6.4.3 + torch==2.8.0+rocm6.4. I'm seeing two issues here:

1. GPU util stuck at 100% when loading a second model
2. wtv goes to GPU 1 also gets allocated to GPU 0

Both happens when setting `device_map` to anything except `"cuda:0"`. When allocating solely on GPU 0 I don't see this issue anymore.
However, trying with another method to load models
```
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-Embedding-0.6B",
    torch_dtype=torch.float16,
    device_map="auto"
)
```
Everything behaves as expected. If you can switch to AutoModel + AutoTokenizer it should solve your issue. I haven't tested llama.cpp yet, will have to look into how their model loading differ.

---

### 评论 #3 — DKingAlpha (2025-08-14T16:18:30Z)

@zichguan-amd Thanks for looking into this. I can confirm AutoModel + AutoTokenizer works as an alternative.

The demo code on the Qwen3-Embedding model page uses `sentence_transformers`, so I went with that. It might be coincidental that they share the same unexpected behavior. Since I dont know much about model loading and GPU tracing, I'll leave that for you to investigate.

---

### 评论 #4 — zichguan-amd (2025-08-15T18:05:36Z)

I'm not seeing any issues using llama.cpp either. With llama.cpp (5edf1592fdb9131d01321aeef4241c6a34969e27) + 2x 7900XTX+ ROCm 6.3.3, `./llama-cli -hf ggml-org/gemma-3-1b-it-GGUF -dev ROCm0,ROCm1` works as expected.

This seems to be a sentence-transformers issue when loading a model with `device_map`.
When initializing SentenceTransformers, the model gets loaded here https://github.com/UKPLab/sentence-transformers/blob/04ae2e064b0f92d6a80fe6d0cd58827b987e67ee/sentence_transformers/SentenceTransformer.py#L327. This will call into the same transformers backend as with AutoModel, which calls `PreTrainedModel.from_pretrained` This takes `device_map` into account, so it loads everything correctly. But later in the initialization, https://github.com/UKPLab/sentence-transformers/blob/04ae2e064b0f92d6a80fe6d0cd58827b987e67ee/sentence_transformers/SentenceTransformer.py#L367, it does a `self.to(device)` which moves everything to GPU 0. [get_device](https://github.com/UKPLab/sentence-transformers/blob/04ae2e064b0f92d6a80fe6d0cd58827b987e67ee/sentence_transformers/util/environment.py#L14) returns `cuda:0` in this case, you should see `Use pytorch device_name: cuda:0` if you enable logs.

That `self.to(device)` is where the issue is. It somehow keeps the GPU spinning, probably because parts of the model are already allocated on the GPU. If you comment it out, or pause the execution before that line, it behaves as expected. This also explains why stuff in GPU 1 always gets reallocated in GPU 0.

I'm not sure what should be the expected behaviour in this case, but for now let me know if you can get llama.cpp working as expected.

---

### 评论 #5 — DKingAlpha (2025-08-16T04:13:42Z)

> I'm not seeing any issues using llama.cpp either. With llama.cpp (5edf1592fdb9131d01321aeef4241c6a34969e27) + 2x 7900XTX+ ROCm 6.3.3, `./llama-cli -hf ggml-org/gemma-3-1b-it-GGUF -dev ROCm0,ROCm1` works as expected.
> 
> This seems to be a sentence-transformers issue when loading a model with `device_map`. When initializing SentenceTransformers, the model gets loaded here https://github.com/UKPLab/sentence-transformers/blob/04ae2e064b0f92d6a80fe6d0cd58827b987e67ee/sentence_transformers/SentenceTransformer.py#L327. This will call into the same transformers backend as with AutoModel, which calls `PreTrainedModel.from_pretrained` This takes `device_map` into account, so it loads everything correctly. But later in the initialization, https://github.com/UKPLab/sentence-transformers/blob/04ae2e064b0f92d6a80fe6d0cd58827b987e67ee/sentence_transformers/SentenceTransformer.py#L367, it does a `self.to(device)` which moves everything to GPU 0. [get_device](https://github.com/UKPLab/sentence-transformers/blob/04ae2e064b0f92d6a80fe6d0cd58827b987e67ee/sentence_transformers/util/environment.py#L14) returns `cuda:0` in this case, you should see `Use pytorch device_name: cuda:0` if you enable logs.
> 
> That `self.to(device)` is where the issue is. It somehow keeps the GPU spinning, probably because parts of the model are already allocated on the GPU. If you comment it out, or pause the execution before that line, it behaves as expected. This also explains why stuff in GPU 1 always gets reallocated in GPU 0.
> 
> I'm not sure what should be the expected behaviour in this case, but for now let me know if you can get llama.cpp working as expected.

You need `-ngl 999` or `export LLAMA_ARG_N_GPU_LAYERS=999` to get it loading in GPU.

With -ngl999 it's instantly 100%. Without -ngl999 it works as expected.

---

### 评论 #6 — knguyen298 (2025-11-17T05:08:39Z)

@zichguan-amd can we get an update here?

I am also experiencing this issue, 3x Mi50 with RocM 6.4.4 using llama.cpp. 

I load 2 models at start up:

- A small embedding model, using one GPU only
- A small task model, no GPU limitations i.e. using all three GPUs

I then load a large model (gpt-oss-120B), and initially everything seems nominal, GPUs are sitting idle at 15-20W. However the GPUs jump to 100% when inferencing and stay at 100% even after it’s done, drawing 50W each. Unloading the small task model immediately drops GPU power and usage back to normal. Constraining the task model to just one GPU fixes it, as well as using a smaller model that only needs one GPU. 

---

### 评论 #7 — zichguan-amd (2025-11-27T15:26:55Z)

Hi @knguyen298, sorry for the late reply. Things have changed between 6.3.3 and now. I have some different observations with ROCm 7.1 + llama.cpp @ 583cb83416467e8abf9b37349dcf1f6a0083745a. ~~I'm seeing 100% GPU utilization with just one model on a 2x gfx1100 system. With `-ngl 999` GPU utilization goes to 100% as soon as the first MemcpyAsync happens. With `-ngl 0` everything looks fine after model loads, but after an inference the GPU 0's utilization would get stuck at 100%. Nothing shows up when profiling the workload, there doesn't seem to be any GPU activity that's actually happening (no queues and dispatchs).~~

I've escalated the issue, and I'll make sure that it gets the attention from the right component team. Currently I can't narrow the issue down yet, `hipMemcpyAsync` alone doesn't trigger this behaviour. Please let me know if we are seeing the same issue and if you can find any smaller workloads/easier reproducer.

Edit: I was on an old firmware and observing a different issue. Latest firmware resolves it, and I see the same behaviour as OP and other people's comments.

---

### 评论 #8 — rsarwar87 (2025-12-03T20:10:35Z)

Hi. 

i am having similar issues on gfx1151. whenever i load more than 2 models, usage goes to 100 pc. these are the models i was loading. ressespective of which model, 3 models are loaded usage goes to 100pc. 

gpt-oss 20/120 are on 6.4.4.
glm on rocm 7.11
gemma on rocm 7.10

<img width="1184" height="265" alt="Image" src="https://github.com/user-attachments/assets/38c1cb8d-551d-450e-81d9-00e536b6c2da" />

 

---

### 评论 #9 — zichguan-amd (2025-12-04T18:36:33Z)

For now, you can work around it by build llama.cpp with `-DGGML_CUDA_NO_PEER_COPY=ON`. This disables peer to peer copy between GPUs and instead route them through CPU. It will be slower, but you can still offload the models across multiple GPUs.

---

### 评论 #10 — rsarwar87 (2025-12-05T09:40:07Z)

Hi. I am on single gpu. Strix halo.

> For now, you can work around it by build llama.cpp with `-DGGML_CUDA_NO_PEER_COPY=ON`. This disables peer to peer copy between GPUs and instead route them through CPU. It will be slower, but you can still offload the models across multiple GPUs.



---

### 评论 #11 — zichguan-amd (2025-12-05T15:37:34Z)

Hi @rsarwar87, that sounds like a different issue, might be related but I'm not seeing anything like this on gfx906 and gfx1100. Can you share your system config and provide repro steps?

---

### 评论 #12 — zichguan-amd (2025-12-10T15:43:48Z)

Hi @rsarwar87, I can confirm that this also happens on a single GPU system, with enough (3+) instances of llama.cpp running. It appears to be the same issue as https://github.com/ROCm/ROCm/issues/2625, using `GPU_MAX_HW_QUEUES=1` will allow you to launch more instances of llama.cpp without running into the problem. But eventually when you have enough processes running you will hit this issue. Kernel team is actively investigating this issue, I'll report back once we have more updates.

---

### 评论 #13 — rsarwar87 (2025-12-16T11:59:53Z)

Hi @zichguan-amd  thanks for confirming the issue. 
also noticed that the same issue occurs when I load models using ROCm and a third model using radv. does it still fall within expectation? Could it be an amdgpu firmware/kernel module, maybe? i only tested kernel 6.17, but considering it was first reported months ago (years if you consider #2625), i expect earlier kernels will have the same issue

I will try the GPU_MAX_HW_QUEUES flag and report back.

Regarding the build process, my Docker images are derived heavily from llama-lemonade, but I do apply rocWMMA patch. unclear if that could be related. 


---

### 评论 #14 — zichguan-amd (2025-12-16T15:38:20Z)

My assumption was that this might be a hardware scheduling issue, which would be related to firmware or kernel driver. So Vulkan could also be affected.

---
