# [Issue]: [Windows] Inconsistent memory usage when generating images with SD3.5

> **Issue #6257**
> **状态**: open
> **创建时间**: 2026-05-14T03:19:55Z
> **更新时间**: 2026-05-19T05:22:39Z
> **作者**: amd-fangchou
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6257

## 负责人

- amd-nicknick

## 描述

### Problem Description

1st run : generate 999 images with SD3.5 → Check Python process is around 9GB → When 1st run finish, run 2nd run immediately → Python process become 11GB

### Operating System

10.0.26200

### CPU

AMD Ryzen ai Max+ 392 w/ Radeon 8060s

### GPU

amd radeon 8060s graphics

### ROCm Version

7.13.0

### ROCm Component

_No response_

### Steps to Reproduce

Set up an environment and run text-to-image generation by using the following command to generate 512x512 image.

> python inf_t2i_torch.py --num_images 5 -n 4 --transformer_folder transformer-flash --text_encoder_folder text_encoder_4bit --text_encoder_2_folder text_encoder_2_4bit --t5 --t5_folder text_encoder_3_gptq_2bit -W 512 -H 512

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Below modification can not fix this issue.

> - low_cpu_mem_usage=True: Makes from_pretrained() load weights layer by layer, reducing the CPU memory peak.
> - gc.collect(): Forces immediate garbage collection of old CPU-side tensors right after .to("cuda").
> - torch.cuda.empty_cache(): Clears unused blocks from the CUDA allocator cache.

set API Monitor to record every individual VirtualAlloc and VirtualFree call for 9G case and 11G case

- All three DLLs (amdhip64_7.dll, c10.dll, python313.dll) commit exactly the same total bytes in both runs. The allocation sizes, patterns, and sequences are identical. No extra memory is being allocated in the 11 GB run.
- The entire difference comes from c10.dll's VirtualFree(MEM_DECOMMIT) behavior. PyTorch's CPU memory allocator (c10) fails to release ~3.7 GB of staging buffers in the 11 GB run that it successfully releases in the 9.2 GB run.

Build C10.dll private symbol to parsing the call stack
The missing calls may come from below call stack(mi_segment_try_purge)
<img width="1342" height="638" alt="Image" src="https://github.com/user-attachments/assets/e1498b30-21a0-4d4e-8bdb-696ad361dfa6" />
