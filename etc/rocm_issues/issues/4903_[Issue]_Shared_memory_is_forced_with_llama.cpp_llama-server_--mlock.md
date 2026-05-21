# [Issue]: Shared memory is forced with llama.cpp llama-server --mlock

> **Issue #4903**
> **状态**: closed
> **创建时间**: 2025-06-08T22:27:48Z
> **更新时间**: 2026-03-08T08:37:02Z
> **关闭时间**: 2025-06-24T20:55:37Z
> **作者**: unclemusclez
> **标签**: Under Investigation, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/4903

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

```
llama-server.exe  -m "C:\Users\musclez\Downloads\llama-b5603-bin-win-hip-radeon-x64\Qwen3-Embedding-8B-Q8_0.gguf"  -a qwen3 -b 1024 -ub 1024 -c 1024 -fa --no-mmap -ngl 999 --embeddings --pooling mean --no-webui -sm none --mlock -mg 0
```

--mlock is supposed to lock it to VRAM on windows, but even with it active and low VRAM usage, it offloads to the shared/system memory.

![Image](https://github.com/user-attachments/assets/2d75b9ca-0f01-4887-a8ca-6e89ef19708e)

![Image](https://github.com/user-attachments/assets/09ee4b3d-3f22-4eca-b958-85c18a73918f)

![Image](https://github.com/user-attachments/assets/4c1073e8-bd42-4173-8cd1-6dcf7294befd)

https://github.com/ggml-org/llama.cpp/issues/9964

### Operating System

Windows 11

### CPU

7800x3D

### GPU

7900XT

### ROCm Version

ROCm 6.2

### ROCm Component

hipBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (22 条)

### 评论 #1 — Matthew-Jenkins (2025-06-09T03:05:09Z)

1. Not what mlock does
2. This should probably go in llamacpp not rocm. 

https://github.com/ggml-org/llama.cpp/blob/247e5c6e447707bb4539bdf1913d206088a8fc69/tools/main/README.md?plain=1#L336

---

### 评论 #2 — unclemusclez (2025-06-09T03:14:13Z)

@Matthew-Jenkins  yeah sorry i got confused with the exact flag.

`-ngl 999 -mg 0 --no-mmap` should lock it to a single device.

This was an issue that occurred with a previous ROCm Driver for windows but was fixed in: https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-12-1.html

I believe there was a regression. I haven't been running inference on windows lately, but this causes inference to slow down significantly. It will utilize system memory, even when disabled.

---

### 评论 #3 — Matthew-Jenkins (2025-06-09T03:42:41Z)

What you're showing me seems to be expected. Any part which isn't supported by the drivers will drop back to cpu. I'm not a windows guy, but my understanding is that windows support isn't as good as linux. Try removing -fa. It looks like that might be the kv cache. 

---

### 评论 #4 — unclemusclez (2025-06-09T04:11:14Z)

the expected result would be if there is not enough RAM, it should crash.

In theory, and i have confirmed this, i can utilize way more ram available, via the system memory.

i run this on linux as well. this is specific to windows

---

### 评论 #5 — Matthew-Jenkins (2025-06-09T13:22:53Z)

It's not a matter of enough ram. I'm not sure where you got that from. Did you try it without -fa?

---

### 评论 #6 — harkgill-amd (2025-06-09T17:42:03Z)

Hi @unclemusclez, could you please share the commands you used to build llama.cpp with the HIP backend?

To add some context, the original issue on Windows + ROCm that resulted in shared memory being used rather than GPU memory was seen with a simple `hipMalloc()`. I'm not seeing that issue with the 25.6.1 Adrenalin driver, can you try running the script from https://github.com/ROCm/HIP/issues/3644 on your end to confirm as well?

---

### 评论 #7 — unclemusclez (2025-06-09T20:39:30Z)

i see now. I have 
```
 cmake -S . -B build -G Ninja -DAMDGPU_TARGETS=gfx1100 -DGGML_HIP=ON -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA_ENABLE_UNIFIED_MEMORY=1 -DBUILD_SHARED_LIBS=ON -DLLAMA_CURL=ON
```
but `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` is not toggle-able, I guess?

This is good to know. i assume this is exactly what I would need active with a new AI MAX+ chip?

Or, if i wanted to build an epyc sever with pcie compute units and system memory?

**Update:**
-------

I think it's ROCm.
@harkgill-amd 

![Image](https://github.com/user-attachments/assets/231dc591-31be-49f3-9539-0addbb8b7da0)
rebuilt with this:
```shell
set PATH=%PATH%;C:\Program Files\AMD\ROCm\6.2\bin
cmake -S . -B build -G Ninja -DAMDGPU_TARGETS=gfx1100 -DGGML_HIP=ON -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA_ENABLE_UNIFIED_MEMORY=0 -DBUILD_SHARED_LIBS=ON -DLLAMA_CURL=OFF
cmake --build build
```
executed with:
```shell
set HIP_VISIBLE_DEVICES=1

llama-server.exe  -m "C:\Users\musclez\Downloads\llama-b5603-bin-win-hip-radeon-x64\Qwen3-Embedding-8B-Q8_0.gguf"  -a qwen3 -b 2048 -ub 2048 -c 0 -fa --no-mmap -ngl 999 --embeddings --pooling mean --no-webui  -mg 0 -sm none -dev ROCm0

```
```shell
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon RX 7900 XT, gfx1100 (0x1100), VMM: no, Wave Size: 32
build: 5618 (1f63e75f) with clang version 19.0.0git (git@github.amd.com:Compute-Mirrors/llvm-project 5353ca3e0e5ae54a31eeebe223da212fa405567a) for x86_64-pc-windows-msvc
system info: n_threads = 8, n_threads_batch = 8, total_threads = 16

system_info: n_threads = 8 (n_threads_batch = 8) / 16 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | REPACK = 1 |

Web UI is disabled
main: binding port with default address family
main: HTTP server is listening, hostname: 127.0.0.1, port: 8080, http threads: 15
main: loading model
srv    load_model: loading model 'C:\Users\musclez\Downloads\llama-b5603-bin-win-hip-radeon-x64\Qwen3-Embedding-8B-Q8_0.gguf'
llama_model_load_from_file_impl: using device ROCm0 (AMD Radeon RX 7900 XT) - 20314 MiB free
llama_model_loader: loaded meta data with 27 key-value pairs and 398 tensors from C:\Users\musclez\Downloads\llama-b5603-bin-win-hip-radeon-x64\Qwen3-Embedding-8B-Q8_0.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen3
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Qwen3 Embedding 8B Bf16
llama_model_loader: - kv   3:                           general.basename str              = Qwen3-Embedding
llama_model_loader: - kv   4:                         general.size_label str              = 8B
llama_model_loader: - kv   5:                          qwen3.block_count u32              = 36
llama_model_loader: - kv   6:                       qwen3.context_length u32              = 40960
llama_model_loader: - kv   7:                     qwen3.embedding_length u32              = 4096
llama_model_loader: - kv   8:                  qwen3.feed_forward_length u32              = 12288
llama_model_loader: - kv   9:                 qwen3.attention.head_count u32              = 32
llama_model_loader: - kv  10:              qwen3.attention.head_count_kv u32              = 8
llama_model_loader: - kv  11:                       qwen3.rope.freq_base f32              = 1000000.000000
llama_model_loader: - kv  12:     qwen3.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  13:                 qwen3.attention.key_length u32              = 128
llama_model_loader: - kv  14:               qwen3.attention.value_length u32              = 128
llama_model_loader: - kv  15:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  16:                         tokenizer.ggml.pre str              = qwen2
llama_model_loader: - kv  17:                      tokenizer.ggml.tokens arr[str,151665]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  18:                  tokenizer.ggml.token_type arr[i32,151665]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  19:                      tokenizer.ggml.merges arr[str,151387]  = ["─á ─á", "─á─á ─á─á", "i n", "─á t",...
llama_model_loader: - kv  20:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  21:            tokenizer.ggml.padding_token_id u32              = 151643
llama_model_loader: - kv  22:                tokenizer.ggml.bos_token_id u32              = 151643
llama_model_loader: - kv  23:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  24:                    tokenizer.chat_template str              = {%- if tools %}\n    {{- '<|im_start|>...
llama_model_loader: - kv  25:               general.quantization_version u32              = 2
llama_model_loader: - kv  26:                          general.file_type u32              = 7
llama_model_loader: - type  f32:  145 tensors
llama_model_loader: - type q8_0:  253 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q8_0
print_info: file size   = 7.49 GiB (8.50 BPW)
load: special tokens cache size = 22
load: token to piece cache size = 0.9310 MB
print_info: arch             = qwen3
print_info: vocab_only       = 0
print_info: n_ctx_train      = 40960
print_info: n_embd           = 4096
print_info: n_layer          = 36
print_info: n_head           = 32
print_info: n_head_kv        = 8
print_info: n_rot            = 128
print_info: n_swa            = 0
print_info: is_swa_any       = 0
print_info: n_embd_head_k    = 128
print_info: n_embd_head_v    = 128
print_info: n_gqa            = 4
print_info: n_embd_k_gqa     = 1024
print_info: n_embd_v_gqa     = 1024
print_info: f_norm_eps       = 0.0e+00
print_info: f_norm_rms_eps   = 1.0e-06
print_info: f_clamp_kqv      = 0.0e+00
print_info: f_max_alibi_bias = 0.0e+00
print_info: f_logit_scale    = 0.0e+00
print_info: f_attn_scale     = 0.0e+00
print_info: n_ff             = 12288
print_info: n_expert         = 0
print_info: n_expert_used    = 0
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 1000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 40960
print_info: rope_finetuned   = unknown
print_info: ssm_d_conv       = 0
print_info: ssm_d_inner      = 0
print_info: ssm_d_state      = 0
print_info: ssm_dt_rank      = 0
print_info: ssm_dt_b_c_rms   = 0
print_info: model type       = 8B
print_info: model params     = 7.57 B
print_info: general.name     = Qwen3 Embedding 8B Bf16
print_info: vocab type       = BPE
print_info: n_vocab          = 151665
print_info: n_merges         = 151387
print_info: BOS token        = 151643 '<|endoftext|>'
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151645 '<|im_end|>'
print_info: PAD token        = 151643 '<|endoftext|>'
print_info: LF token         = 198 '─è'
print_info: FIM PRE token    = 151659 '<|fim_prefix|>'
print_info: FIM SUF token    = 151661 '<|fim_suffix|>'
print_info: FIM MID token    = 151660 '<|fim_middle|>'
print_info: FIM PAD token    = 151662 '<|fim_pad|>'
print_info: FIM REP token    = 151663 '<|repo_name|>'
print_info: FIM SEP token    = 151664 '<|file_sep|>'
print_info: EOG token        = 151643 '<|endoftext|>'
print_info: EOG token        = 151645 '<|im_end|>'
print_info: EOG token        = 151662 '<|fim_pad|>'
print_info: EOG token        = 151663 '<|repo_name|>'
print_info: EOG token        = 151664 '<|file_sep|>'
print_info: max token length = 256
load_tensors: loading model tensors, this can take a while... (mmap = false)
load_tensors: offloading 36 repeating layers to GPU
load_tensors: offloading output layer to GPU
load_tensors: offloaded 37/37 layers to GPU
load_tensors:        ROCm0 model buffer size =  7668.64 MiB
load_tensors:    ROCm_Host model buffer size =   629.47 MiB
.......................................................................................
llama_context: constructing llama_context
llama_context: n_seq_max     = 1
llama_context: n_ctx         = 40960
llama_context: n_ctx_per_seq = 40960
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 2048
llama_context: causal_attn   = 1
llama_context: flash_attn    = 1
llama_context: freq_base     = 1000000.0
llama_context: freq_scale    = 1
llama_context:  ROCm_Host  output buffer size =     0.00 MiB
llama_kv_cache_unified:      ROCm0 KV buffer size =  5760.00 MiB
llama_kv_cache_unified: size = 5760.00 MiB ( 40960 cells,  36 layers,  1 seqs), K (f16): 2880.00 MiB, V (f16): 2880.00 MiB
llama_context:      ROCm0 compute buffer size =  1552.90 MiB
llama_context:  ROCm_Host compute buffer size =   368.02 MiB
llama_context: graph nodes  = 1306
llama_context: graph splits = 2
common_init_from_params: setting dry_penalty_last_n to ctx_size = 40960
```
i havent been able to get TheRock to run on my env yet, but i will attemp that in the near future. 
this is just on the most recent vanilla rocm windows 11 driver for 7900xt




---

### 评论 #8 — harkgill-amd (2025-06-10T15:59:37Z)

Thanks for the logs @unclemusclez. I gave your steps a try with both the latest 25.6.1 and 24.12.1 drivers, the latter being the first driver with the shared GPU memory oversubscription fix. In both cases, there's a small increase (~0.5 GB ) in shared GPU memory usage despite all model layers being loaded directly into GPU VRAM. There is also no sign of a performance regression with `llama-bench` reporting ~70 t/s with both adrenalin releases. 

Taking this into account, I don't believe there's any issue with ROCm here. There are flags such as `--no-mmap` that you can remove on your end to minimize shared GPU memory usage, but so long as there's no inherent performance loss, slight shared memory usage shouldn't be a concern. For reference, I was able to get the following with the 25.6.1 driver,

![Image](https://github.com/user-attachments/assets/605f5300-019d-48ca-90cf-c1d210490fc2)

> This is good to know. i assume this is exactly what I would need active with a new AI MAX+ chip?

For llama.cpp + the new AI MAX APUs, you'd need to set the following flags during your build, ` -DGGML_HIP_UMA=ON -DGGML_HIP=ON -DGGML_HIP_ROCWMMA_FATTN=ON  --DAMDGPU_TARGETS=gfx1151`

---

### 评论 #9 — unclemusclez (2025-06-10T19:11:53Z)

I would argue that you are experiencing my same issue.

Albeit, i am a little confused at the point, I dont think i should be able to utilize reserved system memory for my VRAM if all layers are offloaded on the the GPU. `-ngl 999` should accomplish this.

![Image](https://github.com/user-attachments/assets/d5c6317b-3a00-4fa6-a808-48323d0ae051)

I hate to ask, but can you verify these same numbers on the same machine with Ubuntu?

It should not be the same tokens/s If VRAM is over.
It should not even be able to go over the limit, I thought.

I have most likely been utlizing `mmap` incorrectly
https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createfilemappinga



---

### 评论 #10 — unclemusclez (2025-06-10T19:21:31Z)

I think i am actually using `--no-mmap` correct, as otherwise the load is much slower due to layers being offloaded on to the system memory.

are you sure in your case, your layers that do not get sent to the shared memory for `--no-mmap` and non-shared, dedicated CPU System memory for `mmap=1`.

I suspect the memory Extra bit you noticed that was not put on your GPU from --no-map=0 was actually just in your System memory, hence, no real change in performance.

---

### 评论 #11 — harkgill-amd (2025-06-11T15:40:27Z)

Specifically for ROCm, offloading to shared memory by `hipMalloc()` is supported when model size > GPU VRAM size (on Windows). `ngl 999` will try forcing all layers onto the GPU but again, if model size > GPU VRAM size, some layers will be pushed to shared memory instead. You can see this in the llama.cpp output with --verbose,
```
...
load_tensors: offloaded 20/81 layers to GPU
...
llama_kv_cache_unified: layer  57: dev = CPU
llama_kv_cache_unified: layer  58: dev = CPU
llama_kv_cache_unified: layer  59: dev = CPU
llama_kv_cache_unified: layer  60: dev = ROCm0
llama_kv_cache_unified: layer  61: dev = ROCm0
llama_kv_cache_unified: layer  62: dev = ROCm0
...
```
Currently, Linux does not have the option to offload to shared memory, which is probably why you're expecting a crash. The same case on Linux will result in the error,
```
alloc_tensor_range: failed to allocate ROCm0 buffer of size 139008704512
llama_model_load: error loading model: unable to allocate ROCm0 buffer
llama_model_load_from_file_impl: failed to load model
main: exiting due to model loading error
...
```
As for what flags such as `--no-mmap` do and when to best use them, I'd recommend opening up a discussion post over at https://github.com/ggml-org/llama.cpp/discussions.


---

### 评论 #12 — unclemusclez (2025-06-11T20:50:39Z)

> Specifically for ROCm, offloading to shared memory by `hipMalloc()` is supported when model size > GPU VRAM size (on Windows). `ngl 999` will try forcing all layers onto the GPU but again, if model size > GPU VRAM size, some layers will be pushed to shared memory instead. You can see this in the llama.cpp output with --verbose,
> 
> ```
> ...
> load_tensors: offloaded 20/81 layers to GPU
> ...
> llama_kv_cache_unified: layer  57: dev = CPU
> llama_kv_cache_unified: layer  58: dev = CPU
> llama_kv_cache_unified: layer  59: dev = CPU
> llama_kv_cache_unified: layer  60: dev = ROCm0
> llama_kv_cache_unified: layer  61: dev = ROCm0
> llama_kv_cache_unified: layer  62: dev = ROCm0
> ...
> ```
> 
> Currently, Linux does not have the option to offload to shared memory, which is probably why you're expecting a crash. The same case on Linux will result in the error,
> 
> ```
> alloc_tensor_range: failed to allocate ROCm0 buffer of size 139008704512
> llama_model_load: error loading model: unable to allocate ROCm0 buffer
> llama_model_load_from_file_impl: failed to load model
> main: exiting due to model loading error
> ...
> ```
> 
> As for what flags such as `--no-mmap` do and when to best use them, I'd recommend opening up a discussion post over at https://github.com/ggml-org/llama.cpp/discussions.

Typically on a Linux system and under normal conditions, if system memory is disabled, it should OOM when the model is too large for the VRAM.

it should never go into system memory.

---

### 评论 #13 — Matthew-Jenkins (2025-06-12T13:51:05Z)

I can vouch that on linux if everything is offloaded to gpu and it runs out of vram - it get oom reaped.

---

### 评论 #14 — harkgill-amd (2025-06-12T16:44:38Z)

Yup, the OOM is the expected behaviour which coincides with what we're all seeing in our testing. To summarize the expected results so we're all on the same page, assuming `ngl 999` is set, ROCm + llama.cpp should behave in the following manner

- `Windows` - model size < GPU VRAM size: All model layers are stored in VRAM
- `Windows` - model size > GPU VRAM size: VRAM houses as many layers as possible, remaining layers are offloaded to shared memory
- `Linux` - model size < GPU VRAM size: All model layers are stored in VRAM
- `Linux`- model size > GPU VRAM size: Out of memory as shared memory offloading not supported

Hope that clears up any confusion. Please let me know if you notice any discrepancies during your testing compared to the expected results. If everything looks good, we can go ahead and close this issue.

---

### 评论 #15 — unclemusclez (2025-06-12T17:48:54Z)

@harkgill-amd No. The OOM is the correct behavior. You should also be getting higher tokens/s.

Windows splitting the memory, at all, when it's set to GPU only is un-expected behavior, no matter the platform. 

It has been a bug for a few generations of widnows drivers it would seem.

It was not always like this. It also makes it somewhat unusable. I haven't run local AI on my windows machine for months, due to this driver issue. There is an older driver that will work.

i want to say this is the last stable AMD driver i am aware of for ROCm Pytorch and llama.cpp https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-7-1.html

---

### 评论 #16 — harkgill-amd (2025-06-19T14:03:23Z)

Offloading to shared memory on Windows was purposefully added as a feature. Please see the following notes in the [hip/clr 6.4 changelog](https://github.com/ROCm/clr/blob/amd-staging/CHANGELOG.md#resolved-issues-3),

> Out of memory error on Windows. When the user calls hipMalloc for device memory allocation while specifying a size larger than the available device memory, the HIP runtime fixes the error in the API implementation, allocating the available device memory plus system memory (shared virtual memory).

For reference, you can also find the commit that introduced this over at https://github.com/ROCm/clr/commit/b07178618c2e1a82cf016c23170b0228f5d53d87. 


> i want to say this is the last stable AMD driver i am aware of for ROCm Pytorch and llama.cpp https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-7-1.html

Each adrenalin release has a corresponding HIP runtime that ships alongside it. You're correct in that the 24.7.1 driver does not have the changes from https://github.com/ROCm/clr/commit/b07178618c2e1a82cf016c23170b0228f5d53d87 in the HIP runtime that ships with it. Newer drivers include these changes, hence the shared memory offloading - this is not a bug.

If you want to revert back to the behaviour from previous drivers, you can copy the following DLL binaries from `C:\Program Files\AMD\ROCm\6.2\bin` over to your llama.cpp application executable directory,

- `amdhip64_6.dll`
- `amd_comgr_2.dll`

This will effectively downgrade the HIP runtime llama.cpp uses from 6.4 (based on adrenalin release 25.6.1) to 6.2 from the HIP SDK. As for performance, I'm seeing the same tokens/s with all three configurations (25.6.1, 24.7.1, 25.6.1 with 6.2 HIP Runtime). If you suspect there is a performance regression, please provide more details including the current vs previous token/s and the exact `llama-bench` command you're using.


---

### 评论 #17 — unclemusclez (2025-06-19T14:12:37Z)

> Offloading to shared memory on Windows was purposefully added as a feature. Please see the following notes in the [hip/clr 6.4 changelog](https://github.com/ROCm/clr/blob/amd-staging/CHANGELOG.md#resolved-issues-3),
> 
> > Out of memory error on Windows. When the user calls hipMalloc for device memory allocation while specifying a size larger than the available device memory, the HIP runtime fixes the error in the API implementation, allocating the available device memory plus system memory (shared virtual memory).
> 
> For reference, you can also find the commit that introduced this over at [ROCm/clr@b071786](https://github.com/ROCm/clr/commit/b07178618c2e1a82cf016c23170b0228f5d53d87).
> 
> > i want to say this is the last stable AMD driver i am aware of for ROCm Pytorch and llama.cpp https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-7-1.html
> 
> Each adrenalin release has a corresponding HIP runtime that ships alongside it. You're correct in that the 24.7.1 driver does not have the changes from [ROCm/clr@b071786](https://github.com/ROCm/clr/commit/b07178618c2e1a82cf016c23170b0228f5d53d87) in the HIP runtime that ships with it. Newer drivers include these changes, hence the shared memory offloading - this is not a bug.
> 
> If you want to revert back to the behaviour from previous drivers, you can copy the following DLL binaries from `C:\Program Files\AMD\ROCm\6.2\bin` over to your llama.cpp application executable directory,
> 
>     * `amdhip64_6.dll`
> 
>     * `amd_comgr_2.dll`
> 
> 
> This will effectively downgrade the HIP runtime llama.cpp uses from 6.4 (based on adrenalin release 25.6.1) to 6.2 from the HIP SDK. As for performance, I'm seeing the same tokens/s with all three configurations (25.6.1, 24.7.1, 25.6.1 with 6.2 HIP Runtime). If you suspect there is a performance regression, please provide more details including the current vs previous token/s and the exact `llama-bench` command you're using.

I dont have time for this at the moment, hence why I haven't used the windows env for almost a year.

I found this issue from trying to compare my mi60 to my 7900xt. on my linux machine (mi60), i can embed documents into vecordb without stutter and much more quickly than with my 7900xt. It's not a VRAM bottleneck. And in general, the RDNA3 should be significantly faster than Vega.

I believe this should be reviewed. just simple processing of batches is much slower on windows. This behavior is consistent with memory offloading.

If this is intended, I would really reconsider the intention. This logically doesn't make any sense to me. How are you able to offload to system memory without degradation? No one wants this.


---

### 评论 #18 — harkgill-amd (2025-06-24T20:55:37Z)

There are two distinct cases you're referring to. 

When there is no VRAM bottleneck (model size < GPU VRAM size), there is no inherent performance degradation as all layers are stored on GPU VRAM. I ran a couple different experiments to confirm this across both Linux and Windows on a 7900XT and only saw a discrepancy of ~5% in the reported tokens/s between OSes.

When there is a VRAM bottleneck (model size > GPU VRAM size), the options are limited to either throwing an OOM error or offloading model layers to shared memory. Comparing performance in this case vs a non bottleneck case doesn't make sense - some performance degradation is expected. It might be worth noting that in this case, other backends such as CUDA opt to offload to shared memory as well.

We are currently investigating other reports of poor llama.cpp performance while using a ROCm backend, https://github.com/ROCm/ROCm/issues/4883#issuecomment-2970735490, though this is not related to the usage of shared memory as they're seen on Linux and in the "no VRAM bottleneck" case.

> I found this issue from trying to compare my mi60 to my 7900xt. on my linux machine (mi60), i can embed documents into vecordb without stutter and much more quickly than with my 7900xt. It's not a VRAM bottleneck. And in general, the RDNA3 should be significantly faster than Vega.

There may be a real issue here but without more information, we can't really know what's going on. I'd suggest creating a new issue once you get the chance with your findings and steps to reproduce. I'll be closing this issue out as we've ran multiple experiments but don't see any deviations from the expected - feel free to leave a comment if you have any more questions.

---

### 评论 #19 — unclemusclez (2025-06-26T12:10:43Z)

I'll try to follow up on this.

For me, normally, utilization of shared GPU memory would be an indicator of something not working correctly. 

I am getting inconsistent results with what you state. Either stagnated batching, or low GPU usage. Granted this could be an environment issue, but I do believe I am using `--no-mmap` correctly, and if it were functioning properly on Windows, it would not be putting information into system memory.

It seems to be the case with `--no-mmap` active, the SYS memory being utilized perhaps might be Shared VRAM, but I still do not see how this would be beneficial for performance.

I maintain, this is something that did not occur with the older driver.

My inability to properly utilize the current driver might be mixed up with not understanding how the current driver performs, but certainly things are not clicking the way they used to for me.

At the moment I have too much stuff going on to downgrade and check drivers. I've been trying to keep up with development, and I recently tried to migrate from WSL to straight Windows with TheRock, but it hasn't been very simple. 

There are a few tickets I wish I could be more attentive to, but I have been lucky enough to gain access to more powerful cloud environments, so my time has been split up between whatever works consistently locally (my MI60 on Linux) and whoever is willing to give me credits (😅), rather than tinkering with the 7900XT on my windows machine.

In a perfect world, I would have better a working environment that I could check everything a little more attentively, but I don't really have the resources, and the race is on, so time is of the essence.

I appreciate you looking into it. 


---

### 评论 #20 — dinana (2025-09-28T15:06:34Z)

@harkgill-amd I am seeing the same pattern with shared GPU memory being used on an AI MAx 8060s (Strix Halo) with 96GB VRAM allocated and only a ~34GB model loaded and ~16GB for KV cache, the ~16GB gets loaded into shared GPU memory.

---

### 评论 #21 — Geramy (2025-12-23T05:53:18Z)

I am having the same issue on a Strix Halo 395+ Max 128GB Ram, I am able to load a 60GB model with ROCm and obtain 40TPS roughly but I cant get my full context amount without it saying it cant allocate more memory and so I have to run cache in degraded mode which I dont like, with is on 7.1.1 and custom compiled llamacpp, maybe there is another rocm i shoudl try?

---

### 评论 #22 — kripper (2026-03-08T08:36:11Z)

> [@harkgill-amd](https://github.com/harkgill-amd) I am seeing the same pattern with shared GPU memory being used on an AI MAx 8060s (Strix Halo) with 96GB VRAM allocated and only a ~34GB model loaded and ~16GB for KV cache, the ~16GB gets loaded into shared GPU memory.

Same case here, but I believe it may be correct/desirable that llama-server swaps the *unused* kv-cache when setting it fixed to 16 GB, as long as reading it from the storage is faster than its recompute.

I'm not sure if we really want to use --mlock.

---
