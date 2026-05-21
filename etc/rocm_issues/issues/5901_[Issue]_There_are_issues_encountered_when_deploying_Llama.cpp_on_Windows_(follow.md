# [Issue]: There are issues encountered when deploying Llama.cpp on Windows (followed The documentation at "rocm.docs.amd.com" for the AMD-validated llama.cpp prebuilt binaries)

> **Issue #5901**
> **状态**: closed
> **创建时间**: 2026-01-25T17:45:21Z
> **更新时间**: 2026-02-20T15:21:45Z
> **关闭时间**: 2026-02-20T15:21:45Z
> **作者**: Kagamine-Rinrin
> **标签**: Documentation, AMD Radeon RX 7900 XTX, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5901

## 标签

- **Documentation** (颜色: #5319e7)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I followed The documentation at "rocm.docs.amd.com" for the AMD-validated llama.cpp prebuilt binaries
https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.1.1/docs/advanced/advancedrad/windows/llm/llamacpp.html
However, when I executed according to the documentation, an error occurred: 

> ROCm error: invalid device function ... at C:/develop/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:2727

This error is indeed confusing, as it points to a non-existent folder "C:/develop/llama.cpp", as well as the CUDA file "ggml-cuda/ggml-cuda.cu"and the function ggml_cuda_compute_forward.
Given that the document does not require the deployment of Docker, I believe this is an error, so I am report it


The following is the complete log:


> PS G:\SSD-Games2\AI\Text-processing\llama\llama-b7146-windows-rocm-7.1.1-gfx1150-gfx1151-x64> .\llama-server.exe -m "G:\SSD-Games2\AI\Text-processing\Tifa-DeepsexV3-14b-Chat-NoCot-0626-Q6.gguf" -c 2048 -ngl 99 -fa on --port 8080
HIP Library Path: G:\SSD-Games2\AI\Text-processing\llama\llama-b7146-windows-rocm-7.1.1-gfx1150-gfx1151-x64\amdhip64_7.dll
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: AMD Radeon RX 7900 XTX, gfx1100 (0x1100), VMM: no, Wave Size: 32
main: setting n_parallel = 4 and kv_unified = true (add -kvu to disable this)
build: 1239 (b8372ee) with clang version 21.0.0git (git@github.com:Compute-Mirrors/llvm-project 5dcc622b51ecd499912c1062ce2b0ecda60d8e93) for x86_64-pc-windows-msvc
system info: n_threads = 8, n_threads_batch = 8, total_threads = 16
system_info: n_threads = 8 (n_threads_batch = 8) / 16 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : LLAMAFILE = 1 | REPACK = 1 |
init: using 15 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model 'G:\SSD-Games2\AI\Text-processing\Tifa-DeepsexV3-14b-Chat-NoCot-0626-Q6.gguf'
llama_model_load_from_file_impl: using device ROCm0 (AMD Radeon RX 7900 XTX) (0000:0d:00.0) - 24411 MiB free
llama_model_loader: loaded meta data with 27 key-value pairs and 443 tensors from G:\SSD-Games2\AI\Text-processing\Tifa-DeepsexV3-14b-Chat-NoCot-0626-Q6.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen3
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Dir
llama_model_loader: - kv   3:                         general.size_label str              = 15B
llama_model_loader: - kv   4:                            general.license str              = Apache License 2.0
llama_model_loader: - kv   5:                          qwen3.block_count u32              = 40
llama_model_loader: - kv   6:                       qwen3.context_length u32              = 32768
llama_model_loader: - kv   7:                     qwen3.embedding_length u32              = 5120
llama_model_loader: - kv   8:                  qwen3.feed_forward_length u32              = 17408
llama_model_loader: - kv   9:                 qwen3.attention.head_count u32              = 40
llama_model_loader: - kv  10:              qwen3.attention.head_count_kv u32              = 8
llama_model_loader: - kv  11:                       qwen3.rope.freq_base f32              = 1000000.000000
llama_model_loader: - kv  12:     qwen3.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  13:                 qwen3.attention.key_length u32              = 128
llama_model_loader: - kv  14:               qwen3.attention.value_length u32              = 128
llama_model_loader: - kv  15:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  16:                         tokenizer.ggml.pre str              = qwen2
llama_model_loader: - kv  17:                      tokenizer.ggml.tokens arr[str,151669]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  18:                  tokenizer.ggml.token_type arr[i32,151669]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  19:                      tokenizer.ggml.merges arr[str,151387]  = ["臓 臓", "臓臓 臓臓", "i n", "臓 t",...
llama_model_loader: - kv  20:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  21:            tokenizer.ggml.padding_token_id u32              = 128247
llama_model_loader: - kv  22:                tokenizer.ggml.bos_token_id u32              = 151643
llama_model_loader: - kv  23:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  24:                    tokenizer.chat_template str              = {%- if tools %}\n    {{- '<|im_start|>...
llama_model_loader: - kv  25:               general.quantization_version u32              = 2
llama_model_loader: - kv  26:                          general.file_type u32              = 18
llama_model_loader: - type  f32:  161 tensors
llama_model_loader: - type q6_K:  282 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q6_K
print_info: file size   = 11.28 GiB (6.56 BPW)
load: printing all EOG tokens:
load:   - 151643 ('<|endoftext|>')
load:   - 151645 ('<|im_end|>')
load:   - 151662 ('<|fim_pad|>')
load:   - 151663 ('<|repo_name|>')
load:   - 151664 ('<|file_sep|>')
load: special tokens cache size = 27
load: token to piece cache size = 0.9311 MB
print_info: arch             = qwen3
print_info: vocab_only       = 0
print_info: n_ctx_train      = 32768
print_info: n_embd           = 5120
print_info: n_embd_inp       = 5120
print_info: n_layer          = 40
print_info: n_head           = 40
print_info: n_head_kv        = 8
print_info: n_rot            = 128
print_info: n_swa            = 0
print_info: is_swa_any       = 0
print_info: n_embd_head_k    = 128
print_info: n_embd_head_v    = 128
print_info: n_gqa            = 5
print_info: n_embd_k_gqa     = 1024
print_info: n_embd_v_gqa     = 1024
print_info: f_norm_eps       = 0.0e+00
print_info: f_norm_rms_eps   = 1.0e-06
print_info: f_clamp_kqv      = 0.0e+00
print_info: f_max_alibi_bias = 0.0e+00
print_info: f_logit_scale    = 0.0e+00
print_info: f_attn_scale     = 0.0e+00
print_info: n_ff             = 17408
print_info: n_expert         = 0
print_info: n_expert_used    = 0
print_info: n_expert_groups  = 0
print_info: n_group_used     = 0
print_info: causal attn      = 1
print_info: pooling type     = -1
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 1000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 32768
print_info: rope_finetuned   = unknown
print_info: model type       = 14B
print_info: model params     = 14.77 B
print_info: general.name     = Dir
print_info: vocab type       = BPE
print_info: n_vocab          = 151669
print_info: n_merges         = 151387
print_info: BOS token        = 151643 '<|endoftext|>'
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151645 '<|im_end|>'
print_info: PAD token        = 128247 '</s>'
print_info: LF token         = 198 '膴'
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
load_tensors: loading model tensors, this can take a while... (mmap = true)
load_tensors: offloading 40 repeating layers to GPU
load_tensors: offloading output layer to GPU
load_tensors: offloaded 41/41 layers to GPU
load_tensors:   CPU_Mapped model buffer size =   607.50 MiB
load_tensors:        ROCm0 model buffer size = 10945.06 MiB
............................................................................................
llama_context: constructing llama_context
llama_context: n_seq_max     = 4
llama_context: n_ctx         = 2048
llama_context: n_batch       = 2048
llama_context: causal_attn   = 1
llama_context: flash_attn    = enabled
llama_context: kv_unified    = true
llama_context: freq_base     = 1000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_seq (2048) < n_ctx_train (32768) -- the full capacity of the model will not be utilized
llama_context:  ROCm_Host  output buffer size =     2.31 MiB
llama_kv_cache:      ROCm0 KV buffer size =   320.00 MiB
llama_kv_cache: size =  320.00 MiB (  2048 cells,  40 layers,  4/1 seqs), K (f16):  160.00 MiB, V (f16):  160.00 MiB
llama_context:      ROCm0 compute buffer size =   306.23 MiB
llama_context:  ROCm_Host compute buffer size =    14.01 MiB
llama_context: graph nodes  = 1407
llama_context: graph splits = 2
common_init_from_params: added <|endoftext|> logit bias = -inf
common_init_from_params: added <|im_end|> logit bias = -inf
common_init_from_params: added <|fim_pad|> logit bias = -inf
common_init_from_params: added <|repo_name|> logit bias = -inf
common_init_from_params: added <|file_sep|> logit bias = -inf
common_init_from_params: setting dry_penalty_last_n to ctx_size = 2048
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
ggml_cuda_compute_forward: MUL_MAT failed
ROCm error: invalid device function
  current device: 0, in function ggml_cuda_compute_forward at C:/develop/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:2727
  err
C:/develop/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:89: ROCm error

### Operating System

Windows 10 

### CPU

AMD 5800X3D

### GPU

AMD 7900XTX

### ROCm Version

ROCM 7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — harkgill-amd (2026-01-26T15:44:00Z)

Hey @Kagamine-Rinrin, noticed the llama-cpp binaries that you're using are for `gfx1151`/`gfx1150`,

> Text-processing\llama\llama-b7146-windows-rocm-7.1.1-gfx1150-gfx1151-x64

though you're GPU is actually `gfx1100`,

> Device 0: AMD Radeon RX 7900 XTX, gfx1100

This is likely the cause of the `invalid device function` errors that you're encountering. Could you try running the "Windows Navi" command in the docs and use those binaries instead? 

<img width="766" height="183" alt="Image" src="https://github.com/user-attachments/assets/05ffb54f-bfb2-4d61-b156-cf06b325e86f" />

Note: With the ROCm 7.2 release, the llama-cpp binaries are merged into a single binary for gfx11, gfx12 and gfx115X https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/advanced/advancedrad/windows/llm/llamacpp.html

---

### 评论 #2 — Kagamine-Rinrin (2026-01-27T11:30:14Z)

Thank you for your reply.
After changed to the gfx110X version, llama.cpp runs normally.
However, I also found an issue in the ROCM 7.2 documentation. In the "Llama.cpp pre-built binaries (on Windows)" section, the operating system is incorrectly written as "Ubuntu 24.04" in steps 4, 5, and 6
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedryz/windows/llm/llamacpp.html
<img width="534" height="1037" alt="Image" src="https://github.com/user-attachments/assets/79ab50d9-e4d9-4175-8815-757141bcff28" />

---

### 评论 #3 — harkgill-amd (2026-01-27T16:23:54Z)

Thanks for the heads up, this should be fixed shortly.

---

### 评论 #4 — Kagamine-Rinrin (2026-02-10T04:36:43Z)

I reopened this issue because I noticed that the text had once again changed back to "Ubuntu".
It was once repaired,but now :<

<img width="171" height="559" alt="Image" src="https://github.com/user-attachments/assets/bb08a894-4336-46f3-8db3-4862c38af83e" />


---

### 评论 #5 — harkgill-amd (2026-02-10T15:13:40Z)

Hey @Kagamine-Rinrin, I'm seeing Windows tabs in the Windows page, see below.

<img width="1648" height="899" alt="Image" src="https://github.com/user-attachments/assets/9dd3811a-d519-4182-a478-ce86201b17d6" />

Are you on the latest version of the docs?

---

### 评论 #6 — Kagamine-Rinrin (2026-02-13T04:37:52Z)

I apologize for not describing it clearly. Actually, it comes from here
https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedrad/windows/llm/llamacpp.html

<img width="1135" height="859" alt="Image" src="https://github.com/user-attachments/assets/4c44c559-bea3-4169-a221-0b773162cd4f" />

---
