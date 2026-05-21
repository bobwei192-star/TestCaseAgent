# [Issue]: Unable to offload LLM model on gfx1100 using rocm and llama.cpp, however model executes on cpu

> **Issue #5104**
> **状态**: closed
> **创建时间**: 2025-07-26T03:45:52Z
> **更新时间**: 2025-07-29T20:24:11Z
> **关闭时间**: 2025-07-29T16:41:53Z
> **作者**: chowdri
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5104

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

```
$ echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";

OS:
NAME="elementary OS"
VERSION="8"

$ echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;

CPU: 
model name	: AMD Ryzen 9 7950X3D 16-Core Processor

$ echo "GPU:" && /opt/rocm-6.4.2/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";

GPU:
  Name:                    AMD Ryzen 9 7950X3D 16-Core Processor
  Marketing Name:          AMD Ryzen 9 7950X3D 16-Core Processor
  Name:                    gfx1100                            
  Marketing Name:          Radeon RX 7900 GRE                 
      Name:                    amdgcn-amd-amdhsa--gfx1100         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    gfx900                             
  Marketing Name:          Radeon RX Vega                     
      Name:                    amdgcn-amd-amdhsa--gfx900:xnack-   
      Name:                    amdgcn-amd-amdhsa--gfx9-generic:xnack-

```

I'm trying to run llm models using llama.cpp and HIP options on the program. I have tried to run the program with multiple environment variable options (ROCR_VISIBLE_DEVICES and HIP_VISIBLE_DEVICES). However when I isolate the gfx1100 device, then in some cases the llm loads and executes from cpu and system memory (gpu in case of llama-bench and cpu in the case of llama-cli). 

I have opened this issue on llama.cpp as well because I'm not sure where exactly is the problem: https://github.com/ggml-org/llama.cpp/issues/14696

Much thanks for any guidance and insights in the matter.

### Operating System

elementary OS 8 (ubuntu 24.04)

### CPU

AMD Ryzen 9 7950X3D

### GPU

7900 GRE & Vega 64

### ROCm Version

6.4.2

### ROCm Component

HIP

### Steps to Reproduce

```
$ llama-cli --version

ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 2 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
  Device 1: Radeon RX Vega, gfx900:xnack- (0x900), VMM: no, Wave Size: 64
version: 5898 (cbc68be5)
built with cc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0 for x86_64-linux-gnu

$ llama-cli -m Qwen3-14B-Q8_0.gguf 
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 2 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
  Device 1: Radeon RX Vega, gfx900:xnack- (0x900), VMM: no, Wave Size: 64
build: 5898 (cbc68be5) with cc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0 for x86_64-linux-gnu
main: llama backend init
main: load the model and apply lora adapter, if any
llama_model_load_from_file_impl: using device ROCm0 (Radeon RX 7900 GRE) - 16312 MiB free
llama_model_load_from_file_impl: using device ROCm1 (Radeon RX Vega) - 8160 MiB free
llama_model_loader: loaded meta data with 27 key-value pairs and 443 tensors from Qwen3-14B-Q8_0.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen3
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Qwen3 14B
llama_model_loader: - kv   3:                           general.basename str              = Qwen3
llama_model_loader: - kv   4:                         general.size_label str              = 14B
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
llama_model_loader: - kv  17:                      tokenizer.ggml.tokens arr[str,151936]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  18:                  tokenizer.ggml.token_type arr[i32,151936]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  19:                      tokenizer.ggml.merges arr[str,151387]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  20:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  21:            tokenizer.ggml.padding_token_id u32              = 151643
llama_model_loader: - kv  22:                tokenizer.ggml.bos_token_id u32              = 151643
llama_model_loader: - kv  23:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  24:                    tokenizer.chat_template str              = {%- if tools %}\n    {{- '<|im_start|>...
llama_model_loader: - kv  25:               general.quantization_version u32              = 2
llama_model_loader: - kv  26:                          general.file_type u32              = 7
llama_model_loader: - type  f32:  161 tensors
llama_model_loader: - type q8_0:  282 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q8_0
print_info: file size   = 14.61 GiB (8.50 BPW) 
load: special tokens cache size = 26
load: token to piece cache size = 0.9311 MB
print_info: arch             = qwen3
print_info: vocab_only       = 0
print_info: n_ctx_train      = 32768
print_info: n_embd           = 5120
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
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 1000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 32768
print_info: rope_finetuned   = unknown
print_info: model type       = 14B
print_info: model params     = 14.77 B
print_info: general.name     = Qwen3 14B
print_info: vocab type       = BPE
print_info: n_vocab          = 151936
print_info: n_merges         = 151387
print_info: BOS token        = 151643 '<|endoftext|>'
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151645 '<|im_end|>'
print_info: PAD token        = 151643 '<|endoftext|>'
print_info: LF token         = 198 'Ċ'
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
load_tensors: offloading 0 repeating layers to GPU
load_tensors: offloaded 0/41 layers to GPU
load_tensors:   CPU_Mapped model buffer size = 14965.61 MiB
............................................................................................
llama_context: constructing llama_context
llama_context: n_seq_max     = 1
llama_context: n_ctx         = 4096
llama_context: n_ctx_per_seq = 4096
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = 0
llama_context: freq_base     = 1000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_per_seq (4096) < n_ctx_train (32768) -- the full capacity of the model will not be utilized
llama_context:        CPU  output buffer size =     0.58 MiB
llama_kv_cache_unified:        CPU KV buffer size =   640.00 MiB
llama_kv_cache_unified: size =  640.00 MiB (  4096 cells,  40 layers,  1 seqs), K (f16):  320.00 MiB, V (f16):  320.00 MiB
llama_kv_cache_unified: LLAMA_SET_ROWS=0, using old ggml_cpy() method for backwards compatibility
llama_context:      ROCm0 compute buffer size =  1094.99 MiB
llama_context:  ROCm_Host compute buffer size =    18.01 MiB
llama_context: graph nodes  = 1606
llama_context: graph splits = 524 (with bs=512), 121 (with bs=1)
common_init_from_params: setting dry_penalty_last_n to ctx_size = 4096
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
ggml_cuda_compute_forward: MUL failed
ROCm error: invalid device function
  current device: 0, in function ggml_cuda_compute_forward at /home/praful/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:2482
  err
/home/praful/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:79: ROCm error
[New LWP 626504]
[New LWP 626503]
[New LWP 626502]
[New LWP 626501]
[New LWP 626500]
[New LWP 626499]
[New LWP 626498]
[New LWP 626497]
[New LWP 626496]
[New LWP 626495]
[New LWP 626494]
[New LWP 626493]
[New LWP 626492]
[New LWP 626491]
[New LWP 626490]
[New LWP 626424]
[New LWP 626293]
[New LWP 626031]
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/liblber.so.2
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/libbrotlidec.so.1
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/libbrotlicommon.so.1
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
0x00007009c1b107e3 in __GI___wait4 (pid=626505, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
warning: 30	../sysdeps/unix/sysv/linux/wait4.c: No such file or directory
#0  0x00007009c1b107e3 in __GI___wait4 (pid=626505, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
30	in ../sysdeps/unix/sysv/linux/wait4.c
#1  0x00007009c218fde3 in ggml_print_backtrace () from /home/praful/llama.cpp/build/bin/libggml-base.so
#2  0x00007009c218ff8b in ggml_abort () from /home/praful/llama.cpp/build/bin/libggml-base.so
#3  0x00007009be2e7f22 in ggml_cuda_error(char const*, char const*, char const*, int, char const*) () from /home/praful/llama.cpp/build/bin/libggml-hip.so
#4  0x00007009be2eed2a in ggml_backend_cuda_graph_compute(ggml_backend*, ggml_cgraph*) () from /home/praful/llama.cpp/build/bin/libggml-hip.so
#5  0x00007009c21a7b33 in ggml_backend_sched_graph_compute_async () from /home/praful/llama.cpp/build/bin/libggml-base.so
#6  0x00007009c22b75d1 in llama_context::graph_compute(ggml_cgraph*, bool) () from /home/praful/llama.cpp/build/bin/libllama.so
#7  0x00007009c22b7c03 in llama_context::process_ubatch(llama_ubatch const&, llm_graph_type, llama_memory_context_i*, ggml_status&) () from /home/praful/llama.cpp/build/bin/libllama.so
#8  0x00007009c22bb584 in llama_context::decode(llama_batch const&) () from /home/praful/llama.cpp/build/bin/libllama.so
#9  0x00007009c22bc7df in llama_decode () from /home/praful/llama.cpp/build/bin/libllama.so
#10 0x00005ee35b50d42a in common_init_from_params(common_params&) ()
#11 0x00005ee35b4183da in main ()
[Inferior 1 (process 626028) detached]
Aborted (core dumped)


$ llama-bench -m .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf 

ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 2 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
  Device 1: Radeon RX Vega, gfx900:xnack- (0x900), VMM: no, Wave Size: 64
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
/home/praful/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:79: ROCm error
[New LWP 20492]
[New LWP 19320]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
0x00007d701c9107e3 in __GI___wait4 (pid=20819, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
warning: 30	../sysdeps/unix/sysv/linux/wait4.c: No such file or directory
#0  0x00007d701c9107e3 in __GI___wait4 (pid=20819, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
30	in ../sysdeps/unix/sysv/linux/wait4.c
#1  0x00007d701cfeade3 in ggml_print_backtrace () from /home/praful/llama.cpp/build/bin/libggml-base.so
#2  0x00007d701cfeaf8b in ggml_abort () from /home/praful/llama.cpp/build/bin/libggml-base.so
#3  0x00007d701a0e7f22 in ggml_cuda_error(char const*, char const*, char const*, int, char const*) () from /home/praful/llama.cpp/build/bin/libggml-hip.so
#4  0x00007d701a0eed2a in ggml_backend_cuda_graph_compute(ggml_backend*, ggml_cgraph*) () from /home/praful/llama.cpp/build/bin/libggml-hip.so
#5  0x00007d701d002b33 in ggml_backend_sched_graph_compute_async () from /home/praful/llama.cpp/build/bin/libggml-base.so
#6  0x00007d701d1125d1 in llama_context::graph_compute(ggml_cgraph*, bool) () from /home/praful/llama.cpp/build/bin/libllama.so
#7  0x00007d701d112c03 in llama_context::process_ubatch(llama_ubatch const&, llm_graph_type, llama_memory_context_i*, ggml_status&) () from /home/praful/llama.cpp/build/bin/libllama.so
#8  0x00007d701d116584 in llama_context::decode(llama_batch const&) () from /home/praful/llama.cpp/build/bin/libllama.so
#9  0x00007d701d1177df in llama_decode () from /home/praful/llama.cpp/build/bin/libllama.so
#10 0x00005f577da92a11 in test_prompt(llama_context*, int, int, int) ()
#11 0x00005f577da8e994 in main ()
[Inferior 1 (process 19317) detached]
Aborted (core dumped)

$ export ROCR_VISIBLE_DEVICES=0

$ llama-bench -m .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf 
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen3 14B Q8_0                 |  14.61 GiB |    14.77 B | ROCm       |  99 |           pp512 |       1143.73 ± 3.81 |
| qwen3 14B Q8_0                 |  14.61 GiB |    14.77 B | ROCm       |  99 |           tg128 |         32.53 ± 0.12 |

build: cbc68be5 (5898)

$ export ROCR_VISIBLE_DEVICES=1

$ llama-bench -m .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf 
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX Vega, gfx900:xnack- (0x900), VMM: no, Wave Size: 64
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
main: error: failed to load model '.lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf'

export ROCR_VISIBLE_DEVICES=0

$llama-cli -m .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf 

ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
build: 5898 (cbc68be5) with cc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0 for x86_64-linux-gnu
main: llama backend init
main: load the model and apply lora adapter, if any
llama_model_load_from_file_impl: using device ROCm0 (Radeon RX 7900 GRE) - 16312 MiB free
llama_model_loader: loaded meta data with 27 key-value pairs and 443 tensors from .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen3
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Qwen3 14B
llama_model_loader: - kv   3:                           general.basename str              = Qwen3
llama_model_loader: - kv   4:                         general.size_label str              = 14B
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
llama_model_loader: - kv  17:                      tokenizer.ggml.tokens arr[str,151936]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  18:                  tokenizer.ggml.token_type arr[i32,151936]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  19:                      tokenizer.ggml.merges arr[str,151387]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  20:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  21:            tokenizer.ggml.padding_token_id u32              = 151643
llama_model_loader: - kv  22:                tokenizer.ggml.bos_token_id u32              = 151643
llama_model_loader: - kv  23:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  24:                    tokenizer.chat_template str              = {%- if tools %}\n    {{- '<|im_start|>...
llama_model_loader: - kv  25:               general.quantization_version u32              = 2
llama_model_loader: - kv  26:                          general.file_type u32              = 7
llama_model_loader: - type  f32:  161 tensors
llama_model_loader: - type q8_0:  282 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q8_0
print_info: file size   = 14.61 GiB (8.50 BPW) 
load: special tokens cache size = 26
load: token to piece cache size = 0.9311 MB
print_info: arch             = qwen3
print_info: vocab_only       = 0
print_info: n_ctx_train      = 32768
print_info: n_embd           = 5120
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
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 1000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 32768
print_info: rope_finetuned   = unknown
print_info: model type       = 14B
print_info: model params     = 14.77 B
print_info: general.name     = Qwen3 14B
print_info: vocab type       = BPE
print_info: n_vocab          = 151936
print_info: n_merges         = 151387
print_info: BOS token        = 151643 '<|endoftext|>'
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151645 '<|im_end|>'
print_info: PAD token        = 151643 '<|endoftext|>'
print_info: LF token         = 198 'Ċ'
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
load_tensors: offloading 0 repeating layers to GPU
load_tensors: offloaded 0/41 layers to GPU
load_tensors:   CPU_Mapped model buffer size = 14965.61 MiB
............................................................................................
llama_context: constructing llama_context
llama_context: n_seq_max     = 1
llama_context: n_ctx         = 4096
llama_context: n_ctx_per_seq = 4096
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = 0
llama_context: freq_base     = 1000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_per_seq (4096) < n_ctx_train (32768) -- the full capacity of the model will not be utilized
llama_context:        CPU  output buffer size =     0.58 MiB
llama_kv_cache_unified:        CPU KV buffer size =   640.00 MiB
llama_kv_cache_unified: size =  640.00 MiB (  4096 cells,  40 layers,  1 seqs), K (f16):  320.00 MiB, V (f16):  320.00 MiB
llama_kv_cache_unified: LLAMA_SET_ROWS=0, using old ggml_cpy() method for backwards compatibility
llama_context:      ROCm0 compute buffer size =  1094.99 MiB
llama_context:  ROCm_Host compute buffer size =    18.01 MiB
llama_context: graph nodes  = 1606
llama_context: graph splits = 524 (with bs=512), 121 (with bs=1)
common_init_from_params: setting dry_penalty_last_n to ctx_size = 4096
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
main: llama threadpool init, n_threads = 16
main: chat template is available, enabling conversation mode (disable it with -no-cnv)
main: chat template example:
<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there<|im_end|>
<|im_start|>user
How are you?<|im_end|>
<|im_start|>assistant


system_info: n_threads = 16 (n_threads_batch = 16) / 32 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | 

main: interactive mode on.
sampler seed: 813641237
sampler params: 
	repeat_last_n = 64, repeat_penalty = 1.000, frequency_penalty = 0.000, presence_penalty = 0.000
	dry_multiplier = 0.000, dry_base = 1.750, dry_allowed_length = 2, dry_penalty_last_n = 4096
	top_k = 40, top_p = 0.950, min_p = 0.050, xtc_probability = 0.000, xtc_threshold = 0.100, typical_p = 1.000, top_n_sigma = -1.000, temp = 0.800
	mirostat = 0, mirostat_lr = 0.100, mirostat_ent = 5.000
sampler chain: logits -> logit-bias -> penalties -> dry -> top-n-sigma -> top-k -> typical -> top-p -> min-p -> xtc -> temp-ext -> dist 
generate: n_ctx = 4096, n_batch = 2048, n_predict = -1, n_keep = 0

== Running in interactive mode. ==
 - Press Ctrl+C to interject at any time.
 - Press Return to return control to the AI.
 - To return control without starting a new line, end your input with '/'.
 - If you want to submit another line, end your input with '\'.
 - Not using system message. To change it, set a different value via -sys PROMPT


> 

$ export HIP_VISIBLE_DEVICES=0

$ llama-bench -m .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf 
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen3 14B Q8_0                 |  14.61 GiB |    14.77 B | ROCm       |  99 |           pp512 |       1051.76 ± 3.47 |
| qwen3 14B Q8_0                 |  14.61 GiB |    14.77 B | ROCm       |  99 |           tg128 |         29.21 ± 0.01 |

build: cbc68be5 (5898)

llama-cli -m .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf 
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
build: 5898 (cbc68be5) with cc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0 for x86_64-linux-gnu
main: llama backend init
main: load the model and apply lora adapter, if any
llama_model_load_from_file_impl: using device ROCm0 (Radeon RX 7900 GRE) - 16312 MiB free
llama_model_loader: loaded meta data with 27 key-value pairs and 443 tensors from .lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen3
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Qwen3 14B
llama_model_loader: - kv   3:                           general.basename str              = Qwen3
llama_model_loader: - kv   4:                         general.size_label str              = 14B
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
llama_model_loader: - kv  17:                      tokenizer.ggml.tokens arr[str,151936]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  18:                  tokenizer.ggml.token_type arr[i32,151936]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  19:                      tokenizer.ggml.merges arr[str,151387]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  20:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  21:            tokenizer.ggml.padding_token_id u32              = 151643
llama_model_loader: - kv  22:                tokenizer.ggml.bos_token_id u32              = 151643
llama_model_loader: - kv  23:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  24:                    tokenizer.chat_template str              = {%- if tools %}\n    {{- '<|im_start|>...
llama_model_loader: - kv  25:               general.quantization_version u32              = 2
llama_model_loader: - kv  26:                          general.file_type u32              = 7
llama_model_loader: - type  f32:  161 tensors
llama_model_loader: - type q8_0:  282 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q8_0
print_info: file size   = 14.61 GiB (8.50 BPW) 
load: special tokens cache size = 26
load: token to piece cache size = 0.9311 MB
print_info: arch             = qwen3
print_info: vocab_only       = 0
print_info: n_ctx_train      = 32768
print_info: n_embd           = 5120
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
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 1000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 32768
print_info: rope_finetuned   = unknown
print_info: model type       = 14B
print_info: model params     = 14.77 B
print_info: general.name     = Qwen3 14B
print_info: vocab type       = BPE
print_info: n_vocab          = 151936
print_info: n_merges         = 151387
print_info: BOS token        = 151643 '<|endoftext|>'
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151645 '<|im_end|>'
print_info: PAD token        = 151643 '<|endoftext|>'
print_info: LF token         = 198 'Ċ'
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
load_tensors: offloading 0 repeating layers to GPU
load_tensors: offloaded 0/41 layers to GPU
load_tensors:   CPU_Mapped model buffer size = 14965.61 MiB
............................................................................................
llama_context: constructing llama_context
llama_context: n_seq_max     = 1
llama_context: n_ctx         = 4096
llama_context: n_ctx_per_seq = 4096
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = 0
llama_context: freq_base     = 1000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_per_seq (4096) < n_ctx_train (32768) -- the full capacity of the model will not be utilized
llama_context:        CPU  output buffer size =     0.58 MiB
llama_kv_cache_unified:        CPU KV buffer size =   640.00 MiB
llama_kv_cache_unified: size =  640.00 MiB (  4096 cells,  40 layers,  1 seqs), K (f16):  320.00 MiB, V (f16):  320.00 MiB
llama_kv_cache_unified: LLAMA_SET_ROWS=0, using old ggml_cpy() method for backwards compatibility
llama_context:      ROCm0 compute buffer size =  1094.99 MiB
llama_context:  ROCm_Host compute buffer size =    18.01 MiB
llama_context: graph nodes  = 1606
llama_context: graph splits = 524 (with bs=512), 121 (with bs=1)
common_init_from_params: setting dry_penalty_last_n to ctx_size = 4096
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
main: llama threadpool init, n_threads = 16
main: chat template is available, enabling conversation mode (disable it with -no-cnv)
main: chat template example:
<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there<|im_end|>
<|im_start|>user
How are you?<|im_end|>
<|im_start|>assistant


system_info: n_threads = 16 (n_threads_batch = 16) / 32 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | 

main: interactive mode on.
sampler seed: 2541227824
sampler params: 
	repeat_last_n = 64, repeat_penalty = 1.000, frequency_penalty = 0.000, presence_penalty = 0.000
	dry_multiplier = 0.000, dry_base = 1.750, dry_allowed_length = 2, dry_penalty_last_n = 4096
	top_k = 40, top_p = 0.950, min_p = 0.050, xtc_probability = 0.000, xtc_threshold = 0.100, typical_p = 1.000, top_n_sigma = -1.000, temp = 0.800
	mirostat = 0, mirostat_lr = 0.100, mirostat_ent = 5.000
sampler chain: logits -> logit-bias -> penalties -> dry -> top-n-sigma -> top-k -> typical -> top-p -> min-p -> xtc -> temp-ext -> dist 
generate: n_ctx = 4096, n_batch = 2048, n_predict = -1, n_keep = 0

== Running in interactive mode. ==
 - Press Ctrl+C to interject at any time.
 - Press Return to return control to the AI.
 - To return control without starting a new line, end your input with '/'.
 - If you want to submit another line, end your input with '\'.
 - Not using system message. To change it, set a different value via -sys PROMPT


> 

```




### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
$ rocminfo 

ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 9 7950X3D 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X3D 16-Core Processor
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    0                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5763                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65427024(0x3e65650) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65427024(0x3e65650) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65427024(0x3e65650) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65427024(0x3e65650) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-fd9ca3bcfec72db2               
  Marketing Name:          Radeon RX 7900 GRE                 
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      6144(0x1800) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   1927                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          32(0x20)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    1024(0x400)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 542                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1100         
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx900                             
  Uuid:                    GPU-0215085621863084               
  Marketing Name:          Radeon RX Vega                     
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
    L2:                      4096(0x1000) KB                    
  Chip ID:                 26751(0x687f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1630                               
  BDFID:                   6656                               
  Internal Node ID:        2                                  
  Compute Unit:            64                                 
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
  SDMA engine uCode::      434                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    8372224(0x7fc000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx900:xnack-   
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx9-generic:xnack-
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
*** Done ***             

```

### Additional Information

In the last two instances, while the model loads, it does so on cpu and not the gpu. I don't understand why this is the case. 

---

## 评论 (25 条)

### 评论 #1 — ppanchad-amd (2025-07-28T13:18:00Z)

Hi @chowdri. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-07-28T16:35:09Z)

Hi @chowdri thanks for reaching out! Vega (gfx900) is not well supported by ROCm. AFAIK, llama.cpp will try to use all devices available, that's likely why you see it failing when Vega is visible in your log. 

> then in some cases the llm loads and executes from cpu and system memory (gpu in case of llama-bench and cpu in the case of llama-cli).

In your log, it looks like GPU is being used for both llama-bench and llama-cli. Can you check with amd-smi/rocm-smi and check the GPU usage when running with llama-cli? 

Thanks! 

---

### 评论 #3 — chowdri (2025-07-28T16:36:52Z)

I have checked. llama-bench runs on GPU and llama-cli runs on cpu. Even the logs say so:
```
load_tensors: loading model tensors, this can take a while... (mmap = true)
load_tensors: offloading 0 repeating layers to GPU
load_tensors: offloaded 0/41 layers to GPU
load_tensors:   CPU_Mapped model buffer size = 14965.61 MiB

```

---

### 评论 #4 — tcgu-amd (2025-07-28T16:39:21Z)

> I have checked. llama-bench runs on GPU and llama-cli runs on cpu. Even the logs say so:
> 
> ```
> load_tensors: loading model tensors, this can take a while... (mmap = true)
> load_tensors: offloading 0 repeating layers to GPU
> load_tensors: offloaded 0/41 layers to GPU
> load_tensors:   CPU_Mapped model buffer size = 14965.61 MiB
> ```

Interesting...thanks for confirming! 

---

### 评论 #5 — tcgu-amd (2025-07-28T17:52:16Z)


Hi @chowdri, just reproduced the issue locally. I think you simply need to manually specify the number of layers to offload (i.e. append a -ngl 41 to your llama-cli command). Let me know if this works! 

Thanks!

---

### 评论 #6 — chowdri (2025-07-28T18:22:20Z)

I tried to reinstall llama.cpp (assuming an improper build). However, now, I'm unable to build the following: 

```
~/llama.cpp$ HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" cmake -S . -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1100 -DGGML_HIP_ROCWMMA_FATTN=ON -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release -- -j 32

-- Warning: ccache not found - consider installing it for faster compilation or disable this warning with GGML_CCACHE=OFF
-- CMAKE_SYSTEM_PROCESSOR: x86_64
-- GGML_SYSTEM_ARCH: x86
-- Including CPU backend
-- x86 detected
-- Adding CPU backend variant ggml-cpu: -march=native 
-- The HIP compiler identification is unknown
-- Detecting HIP compiler ABI info
-- Detecting HIP compiler ABI info - failed
-- Check for working HIP compiler: /opt/rocm-6.4.2/lib/llvm/bin/clang
-- Check for working HIP compiler: /opt/rocm-6.4.2/lib/llvm/bin/clang - broken
CMake Error at /usr/share/cmake-3.28/Modules/CMakeTestHIPCompiler.cmake:73 (message):
  The HIP compiler

    "/opt/rocm-6.4.2/lib/llvm/bin/clang"

  is not able to compile a simple test program.

  It fails with the following output:

    Change Dir: '/home/praful/llama.cpp/build/CMakeFiles/CMakeScratch/TryCompile-akcJjI'
    
    Run Build Command(s): /usr/bin/cmake -E env VERBOSE=1 /usr/bin/gmake -f Makefile cmTC_288b0/fast
    /usr/bin/gmake  -f CMakeFiles/cmTC_288b0.dir/build.make CMakeFiles/cmTC_288b0.dir/build
    gmake[1]: Entering directory '/home/praful/llama.cpp/build/CMakeFiles/CMakeScratch/TryCompile-akcJjI'
    Building HIP object CMakeFiles/cmTC_288b0.dir/testHIPCompiler.hip.o
    /opt/rocm-6.4.2/lib/llvm/bin/clang    --offload-arch=gfx1100 -o CMakeFiles/cmTC_288b0.dir/testHIPCompiler.hip.o  -c /home/praful/llama.cpp/build/CMakeFiles/CMakeScratch/TryCompile-akcJjI/testHIPCompiler.hip
    In file included from <built-in>:1:
    In file included from /opt/rocm-6.4.2/lib/llvm/lib/clang/19/include/__clang_hip_runtime_wrapper.h:111:
    /opt/rocm-6.4.2/lib/llvm/lib/clang/19/include/cuda_wrappers/cmath:27:15: fatal error: 'cmath' file not found
       27 | #include_next <cmath>
          |               ^~~~~~~
    1 error generated when compiling for gfx1100.
    gmake[1]: *** [CMakeFiles/cmTC_288b0.dir/build.make:78: CMakeFiles/cmTC_288b0.dir/testHIPCompiler.hip.o] Error 1
    gmake[1]: Leaving directory '/home/praful/llama.cpp/build/CMakeFiles/CMakeScratch/TryCompile-akcJjI'
    gmake: *** [Makefile:127: cmTC_288b0/fast] Error 2
    
    

  

  CMake will not be able to correctly generate this project.
Call Stack (most recent call first):
  ggml/src/ggml-hip/CMakeLists.txt:36 (enable_language)


-- Configuring incomplete, errors occurred!

$ clang -v

Ubuntu clang version 18.1.3 (1ubuntu1)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/13
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/14
Selected GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/14
Candidate multilib: .;@m64
Selected multilib: .;@m64
Found HIP installation: /opt/rocm-6.4.2/, version 6.4.43484
```

How is this possible?

---

### 评论 #7 — tcgu-amd (2025-07-28T18:39:15Z)

Huh, that's odd. It appears to be a misconfiguration with libstdc++. Can you show the output of `/opt/rocm-6.4.2/lib/llvm/bin/clang-v`? You probably have already, but clearing the build folder before building again might help as well. 

---

### 评论 #8 — chowdri (2025-07-28T18:41:28Z)

yeah, I have 2 versions of clang it seems. Also clang-19 seems broken

```
$ /opt/rocm-6.4.2/lib/llvm/bin/clang -v
AMD clang version 19.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-6.4.2 25224 d366fa84f3fdcbd4b10847ebd5db572ae12a34fb)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.4.2/lib/llvm/bin
Configuration file: /opt/rocm-6.4.2/lib/llvm/bin/clang.cfg
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/13
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
Candidate multilib: .;@m64
Selected multilib: .;@m64
Found HIP installation: /opt/rocm-6.4.2/lib/llvm/bin/../../.., version 6.4.43484
 "/opt/rocm-6.4.2/lib/llvm/bin/ld.lld" --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o a.out /lib/x86_64-linux-gnu/crt1.o /lib/x86_64-linux-gnu/crti.o /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtbegin-x86_64.o -L/usr/lib/gcc/x86_64-linux-gnu/14 -L/usr/lib/gcc/x86_64-linux-gnu/14/../../../../lib64 -L/lib/x86_64-linux-gnu -L/lib/../lib64 -L/usr/lib/x86_64-linux-gnu -L/usr/lib/../lib64 -L/lib -L/usr/lib --enable-new-dtags /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed -lc /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtend-x86_64.o /lib/x86_64-linux-gnu/crtn.o
ld.lld: error: undefined symbol: main
>>> referenced by /lib/x86_64-linux-gnu/crt1.o:(_start)
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

I'm trying to reinstall rocm again with clang-18. Let's see how it goes. 


---

### 评论 #9 — tcgu-amd (2025-07-28T18:46:03Z)

> yeah, I have 2 versions of clang it seems. Also clang-19 seems broken
> 
> ```
> $ /opt/rocm-6.4.2/lib/llvm/bin/clang -v
> AMD clang version 19.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-6.4.2 25224 d366fa84f3fdcbd4b10847ebd5db572ae12a34fb)
> Target: x86_64-unknown-linux-gnu
> Thread model: posix
> InstalledDir: /opt/rocm-6.4.2/lib/llvm/bin
> Configuration file: /opt/rocm-6.4.2/lib/llvm/bin/clang.cfg
> Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
> Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/13
> Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
> Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
> Candidate multilib: .;@m64
> Selected multilib: .;@m64
> Found HIP installation: /opt/rocm-6.4.2/lib/llvm/bin/../../.., version 6.4.43484
>  "/opt/rocm-6.4.2/lib/llvm/bin/ld.lld" --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o a.out /lib/x86_64-linux-gnu/crt1.o /lib/x86_64-linux-gnu/crti.o /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtbegin-x86_64.o -L/usr/lib/gcc/x86_64-linux-gnu/14 -L/usr/lib/gcc/x86_64-linux-gnu/14/../../../../lib64 -L/lib/x86_64-linux-gnu -L/lib/../lib64 -L/usr/lib/x86_64-linux-gnu -L/usr/lib/../lib64 -L/lib -L/usr/lib --enable-new-dtags /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed -lc /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtend-x86_64.o /lib/x86_64-linux-gnu/crtn.o
> ld.lld: error: undefined symbol: main
> >>> referenced by /lib/x86_64-linux-gnu/crt1.o:(_start)
> clang: error: linker command failed with exit code 1 (use -v to see invocation)
> ```
> 
> I'm trying to reinstall rocm again with clang-18. Let's see how it goes.

I am not sure if clang-19 is the problem. ROCm ships with its own clang, that's what you see under /opt/rocm/lib/llvm/bin/clang. It has been upgraded to 19 since 6.4.0, and if you were building fine before, it should be okay. I would try reinstalling libstdc++-14-dev to see if that solves the issue. 

---

### 评论 #10 — chowdri (2025-07-28T18:54:17Z)

It seems that libstdc++-14-dev wasn't installed. so I did it all again

```
$ sudo apt-get install libstdc++-14-dev

[sudo] password for praful:            
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libclang-common-19-dev libclang-cpp19 libclang-rt-19-dev libclang1-19 llvm-19 llvm-19-dev llvm-19-linker-tools
  llvm-19-runtime llvm-19-tools
Use 'sudo apt autoremove' to remove them.
Suggested packages:
  libstdc++-14-doc
The following NEW packages will be installed:
  libstdc++-14-dev
0 upgraded, 1 newly installed, 0 to remove and 5 not upgraded.
Need to get 2,507 kB of archives.
After this operation, 22.8 MB of additional disk space will be used.
Get:1 http://security.ubuntu.com/ubuntu noble-security/universe amd64 libstdc++-14-dev amd64 14.2.0-4ubuntu2~24.04 [2,507 kB]
Fetched 2,507 kB in 2s (1,011 kB/s)           
Selecting previously unselected package libstdc++-14-dev:amd64.
(Reading database ... 294396 files and directories currently installed.)
Preparing to unpack .../libstdc++-14-dev_14.2.0-4ubuntu2~24.04_amd64.deb ...
Unpacking libstdc++-14-dev:amd64 (14.2.0-4ubuntu2~24.04) ...
Setting up libstdc++-14-dev:amd64 (14.2.0-4ubuntu2~24.04) 
...

$ /opt/rocm-6.4.2/lib/llvm/bin/clang -v

AMD clang version 19.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-6.4.2 25224 d366fa84f3fdcbd4b10847ebd5db572ae12a34fb)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.4.2/lib/llvm/bin
Configuration file: /opt/rocm-6.4.2/lib/llvm/bin/clang.cfg
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/13
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
Candidate multilib: .;@m64
Selected multilib: .;@m64
Found HIP installation: /opt/rocm-6.4.2/lib/llvm/bin/../../.., version 6.4.43484
 "/opt/rocm-6.4.2/lib/llvm/bin/ld.lld" --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o a.out /lib/x86_64-linux-gnu/crt1.o /lib/x86_64-linux-gnu/crti.o /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtbegin-x86_64.o -L/usr/lib/gcc/x86_64-linux-gnu/14 -L/usr/lib/gcc/x86_64-linux-gnu/14/../../../../lib64 -L/lib/x86_64-linux-gnu -L/lib/../lib64 -L/usr/lib/x86_64-linux-gnu -L/usr/lib/../lib64 -L/lib -L/usr/lib --enable-new-dtags /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed -lc /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtend-x86_64.o /lib/x86_64-linux-gnu/crtn.o
ld.lld: error: undefined symbol: main
>>> referenced by /lib/x86_64-linux-gnu/crt1.o:(_start)
clang: error: linker command failed with exit code 1 (use -v to see invocation)

$ amdgpu-uninstall 

Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  dwarves gcc-11-base gdal-data gdal-plugins libamd-comgr2 libamdhip64-5 libarmadillo12 libarpack2t64 libasan6
  libavcodec-dev libavformat-dev libavutil-dev libcfitsio10t64 libcharls2 libclang-common-19-dev libclang-cpp19
  libclang-rt-19-dev libclang1-19 libdc1394-dev libdeflate-dev libdrm-dev libelf-dev libevent-core-2.1-7t64
  libevent-pthreads-2.1-7t64 libexif-dev libexif-doc libfabric1 libfile-copy-recursive-perl libfile-which-perl
  libfreexl1 libfyba0t64 libgcc-11-dev libgdal34t64 libgdcm-dev libgdcm3.0t64 libgeos-c1t64 libgeos3.12.1t64
  libgeotiff5 libgl2ps1.4 libglew2.2 libgphoto2-dev libhdf4-0-alt libhdf5-hl-100t64 libhsa-runtime64-1 libhsakmt1
  libhwloc-plugins libhwloc15 libimath-dev libjbig-dev libjpeg-dev libjpeg-turbo8-dev libjpeg8-dev libkmlbase1t64
  libkmldom1t64 libkmlengine1t64 liblept5 liblerc-dev libllvm17t64 liblzma-dev libmunge2 libnetcdf19t64 libnuma-dev
  libodbc2 libodbcinst2 libogdi4.1 libopencv-calib3d-dev libopencv-calib3d406t64 libopencv-contrib-dev
  libopencv-contrib406t64 libopencv-core-dev libopencv-core406t64 libopencv-dev libopencv-dnn-dev
  libopencv-dnn406t64 libopencv-features2d-dev libopencv-features2d406t64 libopencv-flann-dev libopencv-flann406t64
  libopencv-highgui-dev libopencv-highgui406t64 libopencv-imgcodecs-dev libopencv-imgcodecs406t64
  libopencv-imgproc-dev libopencv-imgproc406t64 libopencv-java libopencv-ml-dev libopencv-ml406t64
  libopencv-objdetect-dev libopencv-objdetect406t64 libopencv-photo-dev libopencv-photo406t64 libopencv-shape-dev
  libopencv-shape406t64 libopencv-stitching-dev libopencv-stitching406t64 libopencv-superres-dev
  libopencv-superres406t64 libopencv-video-dev libopencv-video406t64 libopencv-videoio-dev libopencv-videoio406t64
  libopencv-videostab-dev libopencv-videostab406t64 libopencv-viz-dev libopencv-viz406t64 libopencv406-jni
  libopenexr-dev libopenmpi3t64 libpciaccess-dev libpmix2t64 libproj25 libpsm-infinipath1 libpsm2-2 libraw1394-dev
  libraw1394-tools librdmacm1t64 librttopo1 libsharpyuv-dev libsocket++1 libspatialite8t64 libstdc++-11-dev
  libsuperlu6 libswresample-dev libswscale-dev libtbb-dev libtbb12 libtbbbind-2-5 libtbbmalloc2 libtesseract5
  libtiff-dev libtiffxx6 libtsan0 libucx0 liburiparser1 libvtk9.1t64 libwebp-dev libxerces-c3.2t64 libxnvctrl0
  llvm-19 llvm-19-dev llvm-19-linker-tools llvm-19-runtime llvm-19-tools mesa-common-dev opencv-data pahole
  proj-bin proj-data python3-argcomplete unixodbc-common valgrind
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  amd-smi-lib* amdgpu-core* amdgpu-dkms* amdgpu-dkms-firmware* comgr* composablekernel-dev* half* hip-dev* hip-doc*
  hip-runtime-amd* hip-samples* hipblas* hipblas-common-dev* hipblas-dev* hipblaslt* hipblaslt-dev* hipcc*
  hipcub-dev* hipfft* hipfft-dev* hipfort-dev* hipify-clang* hiprand* hiprand-dev* hipsolver* hipsolver-dev*
  hipsparse* hipsparse-dev* hipsparselt* hipsparselt-dev* hiptensor* hiptensor-dev* hsa-amd-aqlprofile* hsa-rocr*
  hsa-rocr-dev* libdrm-amdgpu-amdgpu1* libdrm-amdgpu-common* libdrm-amdgpu-dev* libdrm-amdgpu-radeon1*
  libdrm2-amdgpu* migraphx* migraphx-dev* miopen-hip* miopen-hip-dev* mivisionx* mivisionx-dev* openmp-extras-dev*
  openmp-extras-runtime* rccl* rccl-dev* rocalution* rocalution-dev* rocblas* rocblas-dev* rocfft* rocfft-dev*
  rocm* rocm-cmake* rocm-core* rocm-dbgapi* rocm-debug-agent* rocm-developer-tools* rocm-device-libs* rocm-gdb*
  rocm-hip-libraries* rocm-hip-runtime* rocm-hip-runtime-dev* rocm-hip-sdk* rocm-language-runtime* rocm-llvm*
  rocm-ml-libraries* rocm-ml-sdk* rocm-opencl* rocm-opencl-dev* rocm-opencl-runtime* rocm-opencl-sdk*
  rocm-openmp-sdk* rocm-smi-lib* rocm-utils* rocminfo* rocprim-dev* rocprofiler* rocprofiler-compute*
  rocprofiler-dev* rocprofiler-plugins* rocprofiler-register* rocprofiler-sdk* rocprofiler-sdk-roctx*
  rocprofiler-systems* rocrand* rocrand-dev* rocsolver* rocsolver-dev* rocsparse* rocsparse-dev* rocthrust-dev*
  roctracer* roctracer-dev* rocwmma-dev* rpp* rpp-dev*
0 upgraded, 0 newly installed, 101 to remove and 5 not upgraded.
After this operation, 24.2 GB disk space will be freed.
Do you want to continue? [Y/n] y
(Reading database ... 295270 files and directories currently installed.)
Removing rocm (6.4.2.60402-120~24.04) ...
Removing rocm-developer-tools (6.4.2.60402-120~24.04) ...
Removing amd-smi-lib (25.5.1.60402-120~24.04) ...
Removing AMDSMI LIB Packages...
Removing AMDSMI Lib Packages...
Removed AMD-SMI python library (amdsmi)...
python library removed
ldconfig removed
leftovers removed
log folder removed
rocm tests directory removed
Removed "/etc/systemd/system/timers.target.wants/logrotate.timer".
Created symlink /etc/systemd/system/timers.target.wants/logrotate.timer → /usr/lib/systemd/system/logrotate.timer.
logrotate configuration restored
Removing roctracer-dev (4.1.60402.60402-120~24.04) ...
Removing rocprofiler-plugins (2.0.60402.60402-120~24.04) ...
Removing libdrm-amdgpu-dev:amd64 (1:2.4.124.60402-2187269.24.04) ...
Removing rocprofiler-dev (2.0.60402.60402-120~24.04) ...
Removing libdrm-amdgpu-amdgpu1:amd64 (1:2.4.124.60402-2187269.24.04) ...
Removing libdrm-amdgpu-radeon1:amd64 (1:2.4.124.60402-2187269.24.04) ...
Removing libdrm2-amdgpu:amd64 (1:2.4.124.60402-2187269.24.04) ...
Removing libdrm-amdgpu-common (1.0.0.60402-2187269.24.04) ...
Removing amdgpu-core (1:6.4.60402-2187269.24.04) ...
Removing amdgpu-dkms (1:6.12.12.60402-2187269.24.04) ...
Module amdgpu-6.12.12-2187269.24.04 for kernel 6.14.0-24-generic (x86_64).
Before uninstall, this module version was ACTIVE on this kernel.

amdgpu.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.14.0-24-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amdttm.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.14.0-24-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amdkcl.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.14.0-24-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amd-sched.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.14.0-24-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amddrm_ttm_helper.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.14.0-24-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amddrm_buddy.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.14.0-24-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.

amdxcp.ko.zst:
 - Uninstallation
   - Deleting from: /lib/modules/6.14.0-24-generic/updates/dkms/
 - Original module
   - No original module was found for this module on this kernel.
   - Use the dkms install command to reinstall any previous module version.
depmod...
Deleting module amdgpu-6.12.12-2187269.24.04 completely from the DKMS tree.
update-initramfs: Generating /boot/initrd.img-6.14.0-24-generic
I: The initramfs will attempt to resume from /dev/dm-2
I: (/dev/mapper/data_fMRNn-swap)
I: Set the RESUME variable to override this.
Removing amdgpu-dkms-firmware (1:6.12.12.60402-2187269.24.04) ...
Removing rocm-opencl-sdk (6.4.2.60402-120~24.04) ...
Removing rocm-opencl-runtime (6.4.2.60402-120~24.04) ...
Removing rocm-opencl-dev (2.0.0.60402-120~24.04) ...
Removing rocm-opencl (2.0.0.60402-120~24.04) ...
Removing rocm-openmp-sdk (6.4.2.60402-120~24.04) ...
Removing rocm-ml-sdk (6.4.2.60402-120~24.04) ...
Removing rocm-hip-sdk (6.4.2.60402-120~24.04) ...
Removing composablekernel-dev (1.1.0.60402-120~24.04) ...
Removing mivisionx-dev (3.2.0.60402-120~24.04) ...
Removing rpp-dev (1.9.10.60402-120~24.04) ...
Removing rocm-ml-libraries (6.4.2.60402-120~24.04) ...
Removing rocm-hip-runtime-dev (6.4.2.60402-120~24.04) ...
Removing hip-doc (6.4.43484.60402-120~24.04) ...
Removing migraphx-dev (2.12.0.60402-120~24.04) ...
Removing rocsparse-dev (3.4.0.60402-120~24.04) ...
Removing rocm-hip-libraries (6.4.2.60402-120~24.04) ...
Removing rocthrust-dev (3.3.0.60402-120~24.04) ...
Removing hip-samples (6.4.43484.60402-120~24.04) ...
Removing hipblas-dev (2.4.0.60402-120~24.04) ...
Removing hipblas (2.4.0.60402-120~24.04) ...
Removing hipblaslt-dev (0.12.1.60402-120~24.04) ...
Removing hipblas-common-dev (1.0.0.60402-120~24.04) ...
Removing rocblas-dev (4.4.1.60402-120~24.04) ...
Removing hipcub-dev (3.4.0.60402-120~24.04) ...
Removing hipfft-dev (1.0.18.60402-120~24.04) ...
Removing hipfft (1.0.18.60402-120~24.04) ...
Removing hipfort-dev (0.6.0.60402-120~24.04) ...
Removing hipify-clang (19.0.0.60402-120~24.04) ...
Removing hiprand-dev (2.12.0.60402-120~24.04) ...
Removing hiprand (2.12.0.60402-120~24.04) ...
Removing hipsolver-dev (2.4.0.60402-120~24.04) ...
Removing hipsolver (2.4.0.60402-120~24.04) ...
Removing hipsparse-dev (3.2.0.60402-120~24.04) ...
Removing hipsparselt-dev (0.2.3.60402-120~24.04) ...
Removing hipsparselt (0.2.3.60402-120~24.04) ...
Removing hipsparse (3.2.0.60402-120~24.04) ...
Removing hiptensor-dev (1.5.0.60402-120~24.04) ...
Removing hiptensor (1.5.0.60402-120~24.04) ...
Removing hsa-amd-aqlprofile (1.0.0.60402-120~24.04) ...
Removing miopen-hip-dev (3.4.0.60402-120~24.04) ...
Removing mivisionx (3.2.0.60402-120~24.04) ...
Removing openmp-extras-dev (18.63.0.60402-120~24.04) ...
Removing rpp (1.9.10.60402-120~24.04) ...
Removing rccl-dev (2.22.3.60402-120~24.04) ...
Removing rccl (2.22.3.60402-120~24.04) ...
Removing rocalution-dev (3.2.3.60402-120~24.04) ...
Removing rocalution (3.2.3.60402-120~24.04) ...
Removing rocfft-dev (1.0.32.60402-120~24.04) ...
Removing rocfft (1.0.32.60402-120~24.04) ...
Removing rocm-utils (6.4.2.60402-120~24.04) ...
Removing rocm-cmake (0.14.0.60402-120~24.04) ...
Removing rocwmma-dev (1.7.0.60402-120~24.04) ...
Removing rocm-gdb (15.2.60402-120~24.04) ...
Running pre-uninstallation script...
 all requisite libs removed successfully 
pre-uninstallation done.
Removing rocm-debug-agent (2.0.4.60402-120~24.04) ...
Removing rocm-dbgapi (0.77.2.60402-120~24.04) ...
Removing rocm-device-libs (1.0.0.60402-120~24.04) ...
Removing rocm-hip-runtime (6.4.2.60402-120~24.04) ...
Removing rocprofiler-systems (1.0.2.60402-120~24.04) ...
Removing rocm-smi-lib (7.5.0.60402-120~24.04) ...
Removing rocprofiler-compute (3.1.1.60402-120~24.04) ...
Removing rocprofiler-sdk (0.6.0-120~24.04) ...
Removing rocprofiler-sdk-roctx (0.6.0-120~24.04) ...
Removing rocrand-dev (3.3.0.60402-120~24.04) ...
Removing rocsolver-dev (3.28.2.60402-120~24.04) ...
Removing rocsolver (3.28.2.60402-120~24.04) ...
Removing rocprofiler (2.0.60402.60402-120~24.04) ...
Removing rocm-language-runtime (6.4.2.60402-120~24.04) ...
Removing migraphx (2.12.0.60402-120~24.04) ...
Removing hip-dev (6.4.43484.60402-120~24.04) ...
Removing rocsparse (3.4.0.60402-120~24.04) ...
Removing rocprim-dev (3.4.1.60402-120~24.04) ...
Removing hipcc (1.1.1.60402-120~24.04) ...
Removing miopen-hip (3.4.0.60402-120~24.04) ...
Removing openmp-extras-runtime (18.63.0.60402-120~24.04) ...
Removing rocm-llvm (19.0.0.25224.60402-120~24.04) ...
Removing rocrand (3.3.0.60402-120~24.04) ...
Removing hsa-rocr-dev (1.15.0.60402-120~24.04) ...
Removing half (1.12.0.60402-120~24.04) ...
Removing rocblas (4.4.1.60402-120~24.04) ...
Removing hipblaslt (0.12.1.60402-120~24.04) ...
Removing roctracer (4.1.60402.60402-120~24.04) ...
Removing hip-runtime-amd (6.4.43484.60402-120~24.04) ...
Removing rocminfo (1.0.0.60402-120~24.04) ...
Removing hsa-rocr (1.15.0.60402-120~24.04) ...
Removing comgr (3.0.0.60402-120~24.04) ...
Removing rocprofiler-register (0.4.0.60402-120~24.04) ...
Removing rocm-core (6.4.2.60402-120~24.04) ...
Processing triggers for libc-bin (2.39-0ubuntu8.5) ...
(Reading database ... 278505 files and directories currently installed.)
Purging configuration files for amdgpu-dkms (1:6.12.12.60402-2187269.24.04) ...
Purging configuration files for rocm-opencl (2.0.0.60402-120~24.04) ...
Hit:1 https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease
Hit:2 https://repo.radeon.com/rocm/apt/6.4.2 noble InRelease                                                        
Hit:3 http://security.ubuntu.com/ubuntu noble-security InRelease                                                    
Hit:4 http://archive.ubuntu.com/ubuntu noble InRelease                                                              
Get:5 https://dl.cloudsmith.io/public/coolercontrol/coolercontrol/deb/ubuntu noble InRelease [3,130 B]
Hit:6 https://ppa.launchpadcontent.net/elementary-os/stable/ubuntu noble InRelease
Hit:7 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:8 https://ppa.launchpadcontent.net/openrazer/stable/ubuntu noble InRelease
Hit:9 https://ppa.launchpadcontent.net/elementary-os/os-patches/ubuntu noble InRelease
Hit:10 https://ppa.launchpadcontent.net/polychromatic/stable/ubuntu noble InRelease
Fetched 3,130 B in 1s (2,828 B/s)
Reading package lists... Done

$ amdgpu-install -y --usecase=rocm

Get:1 https://dl.cloudsmith.io/public/coolercontrol/coolercontrol/deb/ubuntu noble InRelease [3,130 B]
Hit:2 https://repo.radeon.com/amdgpu/6.4.2/ubuntu noble InRelease                                                   
Hit:3 https://repo.radeon.com/rocm/apt/6.4.2 noble InRelease                                                        
Hit:4 http://archive.ubuntu.com/ubuntu noble InRelease                                                              
Hit:5 http://archive.ubuntu.com/ubuntu noble-updates InRelease                                                      
Hit:6 http://security.ubuntu.com/ubuntu noble-security InRelease    
Hit:7 https://ppa.launchpadcontent.net/elementary-os/stable/ubuntu noble InRelease
Hit:8 https://ppa.launchpadcontent.net/openrazer/stable/ubuntu noble InRelease
Hit:9 https://ppa.launchpadcontent.net/elementary-os/os-patches/ubuntu noble InRelease
Hit:10 https://ppa.launchpadcontent.net/polychromatic/stable/ubuntu noble InRelease
Fetched 3,130 B in 1s (2,606 B/s)
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
linux-headers-6.11.0-19-generic is already the newest version (6.11.0-19.19~24.04.1).
linux-headers-6.14.0-24-generic is already the newest version (6.14.0-24.24~24.04.3).
The following packages were automatically installed and are no longer required:
  libclang-common-19-dev libclang-cpp19 libclang-rt-19-dev libclang1-19 llvm-19 llvm-19-dev llvm-19-linker-tools
  llvm-19-runtime llvm-19-tools
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  amd-smi-lib amdgpu-core amdgpu-dkms-firmware comgr composablekernel-dev half hip-dev hip-doc hip-runtime-amd
  hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev hipfft hipfft-dev
  hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev hipsparselt
  hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev libdrm-amdgpu-amdgpu1
  libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm2-amdgpu migraphx migraphx-dev miopen-hip
  miopen-hip-dev mivisionx mivisionx-dev openmp-extras-dev openmp-extras-runtime rccl rccl-dev rocalution
  rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm-cmake rocm-core rocm-dbgapi rocm-debug-agent
  rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip-libraries rocm-hip-runtime rocm-hip-runtime-dev
  rocm-hip-sdk rocm-language-runtime rocm-llvm rocm-ml-libraries rocm-ml-sdk rocm-opencl rocm-opencl-dev
  rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-smi-lib rocm-utils rocminfo rocprim-dev rocprofiler
  rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk
  rocprofiler-sdk-roctx rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev
  rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev
The following NEW packages will be installed:
  amd-smi-lib amdgpu-core amdgpu-dkms amdgpu-dkms-firmware comgr composablekernel-dev half hip-dev hip-doc
  hip-runtime-amd hip-samples hipblas hipblas-common-dev hipblas-dev hipblaslt hipblaslt-dev hipcc hipcub-dev
  hipfft hipfft-dev hipfort-dev hipify-clang hiprand hiprand-dev hipsolver hipsolver-dev hipsparse hipsparse-dev
  hipsparselt hipsparselt-dev hiptensor hiptensor-dev hsa-amd-aqlprofile hsa-rocr hsa-rocr-dev
  libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm-amdgpu-dev libdrm-amdgpu-radeon1 libdrm2-amdgpu migraphx
  migraphx-dev miopen-hip miopen-hip-dev mivisionx mivisionx-dev openmp-extras-dev openmp-extras-runtime rccl
  rccl-dev rocalution rocalution-dev rocblas rocblas-dev rocfft rocfft-dev rocm rocm-cmake rocm-core rocm-dbgapi
  rocm-debug-agent rocm-developer-tools rocm-device-libs rocm-gdb rocm-hip-libraries rocm-hip-runtime
  rocm-hip-runtime-dev rocm-hip-sdk rocm-language-runtime rocm-llvm rocm-ml-libraries rocm-ml-sdk rocm-opencl
  rocm-opencl-dev rocm-opencl-runtime rocm-opencl-sdk rocm-openmp-sdk rocm-smi-lib rocm-utils rocminfo rocprim-dev
  rocprofiler rocprofiler-compute rocprofiler-dev rocprofiler-plugins rocprofiler-register rocprofiler-sdk
  rocprofiler-sdk-roctx rocprofiler-systems rocrand rocrand-dev rocsolver rocsolver-dev rocsparse rocsparse-dev
  rocthrust-dev roctracer roctracer-dev rocwmma-dev rpp rpp-dev
0 upgraded, 101 newly installed, 0 to remove and 5 not upgraded.
Need to get 0 B/3,951 MB of archives.
After this operation, 24.2 GB of additional disk space will be used.
Extracting templates from packages: 100%
Selecting previously unselected package rocm-core.
(Reading database ... 278505 files and directories currently installed.)
Preparing to unpack .../000-rocm-core_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-core (6.4.2.60402-120~24.04) ...
Selecting previously unselected package amd-smi-lib.
Preparing to unpack .../001-amd-smi-lib_25.5.1.60402-120~24.04_amd64.deb ...
Unpacking amd-smi-lib (25.5.1.60402-120~24.04) ...
Selecting previously unselected package amdgpu-core.
Preparing to unpack .../002-amdgpu-core_1%3a6.4.60402-2187269.24.04_all.deb ...
Unpacking amdgpu-core (1:6.4.60402-2187269.24.04) ...
Selecting previously unselected package amdgpu-dkms-firmware.
Preparing to unpack .../003-amdgpu-dkms-firmware_1%3a6.12.12.60402-2187269.24.04_all.deb ...
Unpacking amdgpu-dkms-firmware (1:6.12.12.60402-2187269.24.04) ...
Selecting previously unselected package amdgpu-dkms.
Preparing to unpack .../004-amdgpu-dkms_1%3a6.12.12.60402-2187269.24.04_all.deb ...
Unpacking amdgpu-dkms (1:6.12.12.60402-2187269.24.04) ...
Selecting previously unselected package comgr.
Preparing to unpack .../005-comgr_3.0.0.60402-120~24.04_amd64.deb ...
Unpacking comgr (3.0.0.60402-120~24.04) ...
Selecting previously unselected package composablekernel-dev.
Preparing to unpack .../006-composablekernel-dev_1.1.0.60402-120~24.04_amd64.deb ...
Unpacking composablekernel-dev (1.1.0.60402-120~24.04) ...
Selecting previously unselected package half.
Preparing to unpack .../007-half_1.12.0.60402-120~24.04_amd64.deb ...
Unpacking half (1.12.0.60402-120~24.04) ...
Selecting previously unselected package libdrm2-amdgpu:amd64.
Preparing to unpack .../008-libdrm2-amdgpu_1%3a2.4.124.60402-2187269.24.04_amd64.deb ...
Unpacking libdrm2-amdgpu:amd64 (1:2.4.124.60402-2187269.24.04) ...
Selecting previously unselected package libdrm-amdgpu-common.
Preparing to unpack .../009-libdrm-amdgpu-common_1.0.0.60402-2187269.24.04_all.deb ...
Unpacking libdrm-amdgpu-common (1.0.0.60402-2187269.24.04) ...
Selecting previously unselected package libdrm-amdgpu-amdgpu1:amd64.
Preparing to unpack .../010-libdrm-amdgpu-amdgpu1_1%3a2.4.124.60402-2187269.24.04_amd64.deb ...
Unpacking libdrm-amdgpu-amdgpu1:amd64 (1:2.4.124.60402-2187269.24.04) ...
Selecting previously unselected package rocprofiler-register.
Preparing to unpack .../011-rocprofiler-register_0.4.0.60402-120~24.04_amd64.deb ...
Unpacking rocprofiler-register (0.4.0.60402-120~24.04) ...
Selecting previously unselected package hsa-rocr.
Preparing to unpack .../012-hsa-rocr_1.15.0.60402-120~24.04_amd64.deb ...
Pre-install check for ROCr.
Unpacking hsa-rocr (1.15.0.60402-120~24.04) ...
Selecting previously unselected package rocminfo.
Preparing to unpack .../013-rocminfo_1.0.0.60402-120~24.04_amd64.deb ...
Unpacking rocminfo (1.0.0.60402-120~24.04) ...
Selecting previously unselected package hip-runtime-amd.
Preparing to unpack .../014-hip-runtime-amd_6.4.43484.60402-120~24.04_amd64.deb ...
Unpacking hip-runtime-amd (6.4.43484.60402-120~24.04) ...
Selecting previously unselected package rocm-llvm.
Preparing to unpack .../015-rocm-llvm_19.0.0.25224.60402-120~24.04_amd64.deb ...
Unpacking rocm-llvm (19.0.0.25224.60402-120~24.04) ...
Selecting previously unselected package libdrm-amdgpu-radeon1:amd64.
Preparing to unpack .../016-libdrm-amdgpu-radeon1_1%3a2.4.124.60402-2187269.24.04_amd64.deb ...
Unpacking libdrm-amdgpu-radeon1:amd64 (1:2.4.124.60402-2187269.24.04) ...It seems that libstdc++-14-dev wasn't installed. so I did it all again


Selecting previously unselected package libdrm-amdgpu-dev:amd64.
Preparing to unpack .../017-libdrm-amdgpu-dev_1%3a2.4.124.60402-2187269.24.04_amd64.deb ...
Unpacking libdrm-amdgpu-dev:amd64 (1:2.4.124.60402-2187269.24.04) ...
Selecting previously unselected package hsa-rocr-dev.
Preparing to unpack .../018-hsa-rocr-dev_1.15.0.60402-120~24.04_amd64.deb ...
Unpacking hsa-rocr-dev (1.15.0.60402-120~24.04) ...
Selecting previously unselected package hipcc.
Preparing to unpack .../019-hipcc_1.1.1.60402-120~24.04_amd64.deb ...
Unpacking hipcc (1.1.1.60402-120~24.04) ...
Selecting previously unselected package hip-dev.
Preparing to unpack .../020-hip-dev_6.4.43484.60402-120~24.04_amd64.deb ...
Unpacking hip-dev (6.4.43484.60402-120~24.04) ...
Selecting previously unselected package hip-doc.
Preparing to unpack .../021-hip-doc_6.4.43484.60402-120~24.04_amd64.deb ...
Unpacking hip-doc (6.4.43484.60402-120~24.04) ...
Selecting previously unselected package hip-samples.
Preparing to unpack .../022-hip-samples_6.4.43484.60402-120~24.04_amd64.deb ...
Unpacking hip-samples (6.4.43484.60402-120~24.04) ...
Selecting previously unselected package roctracer.
Preparing to unpack .../023-roctracer_4.1.60402.60402-120~24.04_amd64.deb ...
Unpacking roctracer (4.1.60402.60402-120~24.04) ...
Selecting previously unselected package hipblaslt.
Preparing to unpack .../024-hipblaslt_0.12.1.60402-120~24.04_amd64.deb ...
Unpacking hipblaslt (0.12.1.60402-120~24.04) ...
Selecting previously unselected package rocblas.
Preparing to unpack .../025-rocblas_4.4.1.60402-120~24.04_amd64.deb ...
Unpacking rocblas (4.4.1.60402-120~24.04) ...
Selecting previously unselected package rocsolver.
Preparing to unpack .../026-rocsolver_3.28.2.60402-120~24.04_amd64.deb ...
Unpacking rocsolver (3.28.2.60402-120~24.04) ...
Selecting previously unselected package hipblas.
Preparing to unpack .../027-hipblas_2.4.0.60402-120~24.04_amd64.deb ...
Unpacking hipblas (2.4.0.60402-120~24.04) ...
Selecting previously unselected package hipblas-common-dev.
Preparing to unpack .../028-hipblas-common-dev_1.0.0.60402-120~24.04_amd64.deb ...
Unpacking hipblas-common-dev (1.0.0.60402-120~24.04) ...
Selecting previously unselected package hipblas-dev.
Preparing to unpack .../029-hipblas-dev_2.4.0.60402-120~24.04_amd64.deb ...
Unpacking hipblas-dev (2.4.0.60402-120~24.04) ...
Selecting previously unselected package hipblaslt-dev.
Preparing to unpack .../030-hipblaslt-dev_0.12.1.60402-120~24.04_amd64.deb ...
Unpacking hipblaslt-dev (0.12.1.60402-120~24.04) ...
Selecting previously unselected package rocprim-dev.
Preparing to unpack .../031-rocprim-dev_3.4.1.60402-120~24.04_amd64.deb ...
Unpacking rocprim-dev (3.4.1.60402-120~24.04) ...
Selecting previously unselected package hipcub-dev.
Preparing to unpack .../032-hipcub-dev_3.4.0.60402-120~24.04_amd64.deb ...
Unpacking hipcub-dev (3.4.0.60402-120~24.04) ...
Selecting previously unselected package rocfft.
Preparing to unpack .../033-rocfft_1.0.32.60402-120~24.04_amd64.deb ...
Unpacking rocfft (1.0.32.60402-120~24.04) ...
Selecting previously unselected package hipfft.
Preparing to unpack .../034-hipfft_1.0.18.60402-120~24.04_amd64.deb ...
Unpacking hipfft (1.0.18.60402-120~24.04) ...
Selecting previously unselected package hipfft-dev.
Preparing to unpack .../035-hipfft-dev_1.0.18.60402-120~24.04_amd64.deb ...
Unpacking hipfft-dev (1.0.18.60402-120~24.04) ...
Selecting previously unselected package hipfort-dev.
Preparing to unpack .../036-hipfort-dev_0.6.0.60402-120~24.04_amd64.deb ...
Unpacking hipfort-dev (0.6.0.60402-120~24.04) ...
Selecting previously unselected package hipify-clang.
Preparing to unpack .../037-hipify-clang_19.0.0.60402-120~24.04_amd64.deb ...
Unpacking hipify-clang (19.0.0.60402-120~24.04) ...
Selecting previously unselected package hiprand.
Preparing to unpack .../038-hiprand_2.12.0.60402-120~24.04_amd64.deb ...
Unpacking hiprand (2.12.0.60402-120~24.04) ...
Selecting previously unselected package hiprand-dev.
Preparing to unpack .../039-hiprand-dev_2.12.0.60402-120~24.04_amd64.deb ...
Unpacking hiprand-dev (2.12.0.60402-120~24.04) ...
Selecting previously unselected package hipsolver.
Preparing to unpack .../040-hipsolver_2.4.0.60402-120~24.04_amd64.deb ...
Unpacking hipsolver (2.4.0.60402-120~24.04) ...
Selecting previously unselected package hipsolver-dev.
Preparing to unpack .../041-hipsolver-dev_2.4.0.60402-120~24.04_amd64.deb ...
Unpacking hipsolver-dev (2.4.0.60402-120~24.04) ...
Selecting previously unselected package rocsparse.
Preparing to unpack .../042-rocsparse_3.4.0.60402-120~24.04_amd64.deb ...
Unpacking rocsparse (3.4.0.60402-120~24.04) ...
Selecting previously unselected package hipsparse.
Preparing to unpack .../043-hipsparse_3.2.0.60402-120~24.04_amd64.deb ...
Unpacking hipsparse (3.2.0.60402-120~24.04) ...
Selecting previously unselected package hipsparse-dev.
Preparing to unpack .../044-hipsparse-dev_3.2.0.60402-120~24.04_amd64.deb ...
Unpacking hipsparse-dev (3.2.0.60402-120~24.04) ...
Selecting previously unselected package hipsparselt.
Preparing to unpack .../045-hipsparselt_0.2.3.60402-120~24.04_amd64.deb ...
Unpacking hipsparselt (0.2.3.60402-120~24.04) ...
Selecting previously unselected package hipsparselt-dev.
Preparing to unpack .../046-hipsparselt-dev_0.2.3.60402-120~24.04_amd64.deb ...
Unpacking hipsparselt-dev (0.2.3.60402-120~24.04) ...
Selecting previously unselected package hiptensor.
Preparing to unpack .../047-hiptensor_1.5.0.60402-120~24.04_amd64.deb ...
Unpacking hiptensor (1.5.0.60402-120~24.04) ...
Selecting previously unselected package hiptensor-dev.
Preparing to unpack .../048-hiptensor-dev_1.5.0.60402-120~24.04_amd64.deb ...
Unpacking hiptensor-dev (1.5.0.60402-120~24.04) ...
Selecting previously unselected package hsa-amd-aqlprofile.
Preparing to unpack .../049-hsa-amd-aqlprofile_1.0.0.60402-120~24.04_amd64.deb ...
Unpacking hsa-amd-aqlprofile (1.0.0.60402-120~24.04) ...
Selecting previously unselected package rocrand.
Preparing to unpack .../050-rocrand_3.3.0.60402-120~24.04_amd64.deb ...
Unpacking rocrand (3.3.0.60402-120~24.04) ...
Selecting previously unselected package miopen-hip.
Preparing to unpack .../051-miopen-hip_3.4.0.60402-120~24.04_amd64.deb ...
Unpacking miopen-hip (3.4.0.60402-120~24.04) ...
Selecting previously unselected package migraphx.
Preparing to unpack .../052-migraphx_2.12.0.60402-120~24.04_amd64.deb ...
Unpacking migraphx (2.12.0.60402-120~24.04) ...
Selecting previously unselected package migraphx-dev.
Preparing to unpack .../053-migraphx-dev_2.12.0.60402-120~24.04_amd64.deb ...
Unpacking migraphx-dev (2.12.0.60402-120~24.04) ...
Selecting previously unselected package miopen-hip-dev.
Preparing to unpack .../054-miopen-hip-dev_3.4.0.60402-120~24.04_amd64.deb ...
Unpacking miopen-hip-dev (3.4.0.60402-120~24.04) ...
Selecting previously unselected package openmp-extras-runtime.
Preparing to unpack .../055-openmp-extras-runtime_18.63.0.60402-120~24.04_amd64.deb ...
Unpacking openmp-extras-runtime (18.63.0.60402-120~24.04) ...
Selecting previously unselected package rocm-language-runtime.
Preparing to unpack .../056-rocm-language-runtime_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-language-runtime (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-hip-runtime.
Preparing to unpack .../057-rocm-hip-runtime_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-hip-runtime (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rpp.
Preparing to unpack .../058-rpp_1.9.10.60402-120~24.04_amd64.deb ...
Unpacking rpp (1.9.10.60402-120~24.04) ...
Selecting previously unselected package mivisionx.
Preparing to unpack .../059-mivisionx_3.2.0.60402-120~24.04_amd64.deb ...
Unpacking mivisionx (3.2.0.60402-120~24.04) ...
Selecting previously unselected package rocm-device-libs.
Preparing to unpack .../060-rocm-device-libs_1.0.0.60402-120~24.04_amd64.deb ...
Unpacking rocm-device-libs (1.0.0.60402-120~24.04) ...
Selecting previously unselected package rocm-cmake.
Preparing to unpack .../061-rocm-cmake_0.14.0.60402-120~24.04_amd64.deb ...
Unpacking rocm-cmake (0.14.0.60402-120~24.04) ...
Selecting previously unselected package rocm-hip-runtime-dev.
Preparing to unpack .../062-rocm-hip-runtime-dev_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-hip-runtime-dev (6.4.2.60402-120~24.04) ...
Selecting previously unselected package openmp-extras-dev.
Preparing to unpack .../063-openmp-extras-dev_18.63.0.60402-120~24.04_amd64.deb ...
Unpacking openmp-extras-dev (18.63.0.60402-120~24.04) ...
Selecting previously unselected package rpp-dev.
Preparing to unpack .../064-rpp-dev_1.9.10.60402-120~24.04_amd64.deb ...
Unpacking rpp-dev (1.9.10.60402-120~24.04) ...
Selecting previously unselected package rocblas-dev.
Preparing to unpack .../065-rocblas-dev_4.4.1.60402-120~24.04_amd64.deb ...
Unpacking rocblas-dev (4.4.1.60402-120~24.04) ...
Selecting previously unselected package mivisionx-dev.
Preparing to unpack .../066-mivisionx-dev_3.2.0.60402-120~24.04_amd64.deb ...
Unpacking mivisionx-dev (3.2.0.60402-120~24.04) ...
Selecting previously unselected package rocm-smi-lib.
Preparing to unpack .../067-rocm-smi-lib_7.5.0.60402-120~24.04_amd64.deb ...
Unpacking rocm-smi-lib (7.5.0.60402-120~24.04) ...
Selecting previously unselected package rccl.
Preparing to unpack .../068-rccl_2.22.3.60402-120~24.04_amd64.deb ...
Unpacking rccl (2.22.3.60402-120~24.04) ...
Selecting previously unselected package rccl-dev.
Preparing to unpack .../069-rccl-dev_2.22.3.60402-120~24.04_amd64.deb ...
Unpacking rccl-dev (2.22.3.60402-120~24.04) ...
Selecting previously unselected package rocalution.
Preparing to unpack .../070-rocalution_3.2.3.60402-120~24.04_amd64.deb ...
Unpacking rocalution (3.2.3.60402-120~24.04) ...
Selecting previously unselected package rocalution-dev.
Preparing to unpack .../071-rocalution-dev_3.2.3.60402-120~24.04_amd64.deb ...
Unpacking rocalution-dev (3.2.3.60402-120~24.04) ...
Selecting previously unselected package rocfft-dev.
Preparing to unpack .../072-rocfft-dev_1.0.32.60402-120~24.04_amd64.deb ...
Unpacking rocfft-dev (1.0.32.60402-120~24.04) ...
Selecting previously unselected package rocm-utils.
Preparing to unpack .../073-rocm-utils_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-utils (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-dbgapi.
Preparing to unpack .../074-rocm-dbgapi_0.77.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-dbgapi (0.77.2.60402-120~24.04) ...
Selecting previously unselected package rocm-debug-agent.
Preparing to unpack .../075-rocm-debug-agent_2.0.4.60402-120~24.04_amd64.deb ...
Unpacking rocm-debug-agent (2.0.4.60402-120~24.04) ...
Selecting previously unselected package rocm-gdb.
Preparing to unpack .../076-rocm-gdb_15.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-gdb (15.2.60402-120~24.04) ...
Selecting previously unselected package rocprofiler.
Preparing to unpack .../077-rocprofiler_2.0.60402.60402-120~24.04_amd64.deb ...
Unpacking rocprofiler (2.0.60402.60402-120~24.04) ...
Selecting previously unselected package rocprofiler-plugins.
Preparing to unpack .../078-rocprofiler-plugins_2.0.60402.60402-120~24.04_amd64.deb ...
Unpacking rocprofiler-plugins (2.0.60402.60402-120~24.04) ...
Selecting previously unselected package rocprofiler-sdk-roctx.
Preparing to unpack .../079-rocprofiler-sdk-roctx_0.6.0-120~24.04_amd64.deb ...
Unpacking rocprofiler-sdk-roctx (0.6.0-120~24.04) ...
Selecting previously unselected package rocprofiler-sdk.
Preparing to unpack .../080-rocprofiler-sdk_0.6.0-120~24.04_amd64.deb ...
Unpacking rocprofiler-sdk (0.6.0-120~24.04) ...
Selecting previously unselected package rocprofiler-compute.
Preparing to unpack .../081-rocprofiler-compute_3.1.1.60402-120~24.04_amd64.deb ...
Unpacking rocprofiler-compute (3.1.1.60402-120~24.04) ...
Selecting previously unselected package rocprofiler-systems.
Preparing to unpack .../082-rocprofiler-systems_1.0.2.60402-120~24.04_amd64.deb ...
Unpacking rocprofiler-systems (1.0.2.60402-120~24.04) ...
Selecting previously unselected package rocprofiler-dev.
Preparing to unpack .../083-rocprofiler-dev_2.0.60402.60402-120~24.04_amd64.deb ...
Unpacking rocprofiler-dev (2.0.60402.60402-120~24.04) ...
Selecting previously unselected package roctracer-dev.
Preparing to unpack .../084-roctracer-dev_4.1.60402.60402-120~24.04_amd64.deb ...
Unpacking roctracer-dev (4.1.60402.60402-120~24.04) ...
Selecting previously unselected package rocm-developer-tools.
Preparing to unpack .../085-rocm-developer-tools_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-developer-tools (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-openmp-sdk.
Preparing to unpack .../086-rocm-openmp-sdk_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-openmp-sdk (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-opencl.
Preparing to unpack .../087-rocm-opencl_2.0.0.60402-120~24.04_amd64.deb ...
Unpacking rocm-opencl (2.0.0.60402-120~24.04) ...
Selecting previously unselected package rocm-opencl-runtime.
Preparing to unpack .../088-rocm-opencl-runtime_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-opencl-runtime (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-opencl-dev.
Preparing to unpack .../089-rocm-opencl-dev_2.0.0.60402-120~24.04_amd64.deb ...
Unpacking rocm-opencl-dev (2.0.0.60402-120~24.04) ...
Selecting previously unselected package rocm-opencl-sdk.
Preparing to unpack .../090-rocm-opencl-sdk_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-opencl-sdk (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-hip-libraries.
Preparing to unpack .../091-rocm-hip-libraries_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-hip-libraries (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-ml-libraries.
Preparing to unpack .../092-rocm-ml-libraries_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-ml-libraries (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocrand-dev.
Preparing to unpack .../093-rocrand-dev_3.3.0.60402-120~24.04_amd64.deb ...
Unpacking rocrand-dev (3.3.0.60402-120~24.04) ...
Selecting previously unselected package rocsolver-dev.
Preparing to unpack .../094-rocsolver-dev_3.28.2.60402-120~24.04_amd64.deb ...
Unpacking rocsolver-dev (3.28.2.60402-120~24.04) ...
Selecting previously unselected package rocsparse-dev.
Preparing to unpack .../095-rocsparse-dev_3.4.0.60402-120~24.04_amd64.deb ...
Unpacking rocsparse-dev (3.4.0.60402-120~24.04) ...
Selecting previously unselected package rocthrust-dev.
Preparing to unpack .../096-rocthrust-dev_3.3.0.60402-120~24.04_amd64.deb ...
Unpacking rocthrust-dev (3.3.0.60402-120~24.04) ...
Selecting previously unselected package rocwmma-dev.
Preparing to unpack .../097-rocwmma-dev_1.7.0.60402-120~24.04_amd64.deb ...
Unpacking rocwmma-dev (1.7.0.60402-120~24.04) ...
Selecting previously unselected package rocm-hip-sdk.
Preparing to unpack .../098-rocm-hip-sdk_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-hip-sdk (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm-ml-sdk.
Preparing to unpack .../099-rocm-ml-sdk_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm-ml-sdk (6.4.2.60402-120~24.04) ...
Selecting previously unselected package rocm.
Preparing to unpack .../100-rocm_6.4.2.60402-120~24.04_amd64.deb ...
Unpacking rocm (6.4.2.60402-120~24.04) ...
Setting up rocm-core (6.4.2.60402-120~24.04) ...
Setting up rocm-device-libs (1.0.0.60402-120~24.04) ...
Setting up rocfft (1.0.32.60402-120~24.04) ...
Setting up hipblas-common-dev (1.0.0.60402-120~24.04) ...
Setting up amdgpu-core (1:6.4.60402-2187269.24.04) ...
Setting up rocprofiler-register (0.4.0.60402-120~24.04) ...
Setting up amdgpu-dkms-firmware (1:6.12.12.60402-2187269.24.04) ...
Setting up rocwmma-dev (1.7.0.60402-120~24.04) ...
Setting up hipify-clang (19.0.0.60402-120~24.04) ...
Setting up libdrm-amdgpu-common (1.0.0.60402-2187269.24.04) ...
Setting up rocm-smi-lib (7.5.0.60402-120~24.04) ...
Removed "/etc/systemd/system/timers.target.wants/logrotate.timer".
Created symlink /etc/systemd/system/timers.target.wants/logrotate.timer → /usr/lib/systemd/system/logrotate.timer.
Setting up rocrand (3.3.0.60402-120~24.04) ...
Setting up rocm-llvm (19.0.0.25224.60402-120~24.04) ...
Setting up comgr (3.0.0.60402-120~24.04) ...
Setting up hiprand (2.12.0.60402-120~24.04) ...
Setting up roctracer (4.1.60402.60402-120~24.04) ...
Setting up rocrand-dev (3.3.0.60402-120~24.04) ...
Setting up composablekernel-dev (1.1.0.60402-120~24.04) ...
Setting up amd-smi-lib (25.5.1.60402-120~24.04) ...
Using pyproject.toml for installation due to setuptools version 68.1.2
Defaulting to system-wide installation.
Installing /usr/lib/python3/dist-packages/argcomplete/bash_completion.d/_python-argcomplete to /usr/local/share/zsh/site-functions/_python-argcomplete...
Installed.
Installing /usr/lib/python3/dist-packages/argcomplete/bash_completion.d/_python-argcomplete to /etc/bash_completion.d/python-argcomplete...
Installed.
Please restart your shell or source the installed file to activate it.
Removed "/etc/systemd/system/timers.target.wants/logrotate.timer".
Created symlink /etc/systemd/system/timers.target.wants/logrotate.timer → /usr/lib/systemd/system/logrotate.timer.
Setting up rocm-cmake (0.14.0.60402-120~24.04) ...
Setting up rocprofiler-sdk-roctx (0.6.0-120~24.04) ...
Setting up hsa-amd-aqlprofile (1.0.0.60402-120~24.04) ...
Setting up hipfft (1.0.18.60402-120~24.04) ...
Setting up hipfft-dev (1.0.18.60402-120~24.04) ...
Setting up hiptensor (1.5.0.60402-120~24.04) ...
Setting up half (1.12.0.60402-120~24.04) ...
Setting up hipblaslt (0.12.1.60402-120~24.04) ...
Setting up amdgpu-dkms (1:6.12.12.60402-2187269.24.04) ...
Loading new amdgpu-6.12.12-2187269.24.04 DKMS files...
Building for 6.14.0-24-generic
Building for architecture x86_64
Building initial module for 6.14.0-24-generic
At main.c:251:
- SSL error:1E08010C:DECODER routines::unsupported: ../crypto/encode_decode/decoder_lib.c:101
kmodsign: /var/lib/shim-signed/mok/MOK.priv: No such file or directory
At main.c:251:
- SSL error:1E08010C:DECODER routines::unsupported: ../crypto/encode_decode/decoder_lib.c:101
kmodsign: /var/lib/shim-signed/mok/MOK.priv: No such file or directory
At main.c:251:
- SSL error:1E08010C:DECODER routines::unsupported: ../crypto/encode_decode/decoder_lib.c:101
kmodsign: /var/lib/shim-signed/mok/MOK.priv: No such file or directory
At main.c:251:
- SSL error:1E08010C:DECODER routines::unsupported: ../crypto/encode_decode/decoder_lib.c:101
kmodsign: /var/lib/shim-signed/mok/MOK.priv: No such file or directory
At main.c:251:
- SSL error:1E08010C:DECODER routines::unsupported: ../crypto/encode_decode/decoder_lib.c:101
kmodsign: /var/lib/shim-signed/mok/MOK.priv: No such file or directory
At main.c:251:
- SSL error:1E08010C:DECODER routines::unsupported: ../crypto/encode_decode/decoder_lib.c:101
kmodsign: /var/lib/shim-signed/mok/MOK.priv: No such file or directory
At main.c:251:
- SSL error:1E08010C:DECODER routines::unsupported: ../crypto/encode_decode/decoder_lib.c:101
kmodsign: /var/lib/shim-signed/mok/MOK.priv: No such file or directory
Done.
Forcing installation of amdgpu

amdgpu.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.14.0-24-generic/updates/dkms/

amdttm.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.14.0-24-generic/updates/dkms/

amdkcl.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.14.0-24-generic/updates/dkms/

amd-sched.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.14.0-24-generic/updates/dkms/

amddrm_ttm_helper.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.14.0-24-generic/updates/dkms/

amddrm_buddy.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.14.0-24-generic/updates/dkms/

amdxcp.ko.zst:
Running module version sanity check.
 - Original module
 - Installation
   - Installing to /lib/modules/6.14.0-24-generic/updates/dkms/
depmod...
update-initramfs: Generating /boot/initrd.img-6.14.0-24-generic
I: The initramfs will attempt to resume from /dev/dm-2
I: (/dev/mapper/data_fMRNn-swap)
I: Set the RESUME variable to override this.
Setting up hsa-rocr (1.15.0.60402-120~24.04) ...
Setting up hiptensor-dev (1.5.0.60402-120~24.04) ...
Setting up libdrm2-amdgpu:amd64 (1:2.4.124.60402-2187269.24.04) ...
Setting up rocm-dbgapi (0.77.2.60402-120~24.04) ...
Setting up rocfft-dev (1.0.32.60402-120~24.04) ...
Setting up hiprand-dev (2.12.0.60402-120~24.04) ...
Setting up rocm-opencl (2.0.0.60402-120~24.04) ...
Setting up rocprofiler-sdk (0.6.0-120~24.04) ...
Setting up hipblaslt-dev (0.12.1.60402-120~24.04) ...
Setting up hipcc (1.1.1.60402-120~24.04) ...
Setting up libdrm-amdgpu-radeon1:amd64 (1:2.4.124.60402-2187269.24.04) ...
Setting up rocprofiler-systems (1.0.2.60402-120~24.04) ...
Setting up libdrm-amdgpu-amdgpu1:amd64 (1:2.4.124.60402-2187269.24.04) ...
Setting up rocminfo (1.0.0.60402-120~24.04) ...
Setting up hip-runtime-amd (6.4.43484.60402-120~24.04) ...
Setting up hsa-rocr-dev (1.15.0.60402-120~24.04) ...
Setting up openmp-extras-runtime (18.63.0.60402-120~24.04) ...
Setting up rocm-utils (6.4.2.60402-120~24.04) ...
Setting up rocprim-dev (3.4.1.60402-120~24.04) ...
Setting up rocm-gdb (15.2.60402-120~24.04) ...
Running post-installation script...
Installing rocm-gdb with [/lib/python3.12/config-3.12-x86_64-linux-gnu/libpython3.12.so].
post-installation done.
Setting up rocm-debug-agent (2.0.4.60402-120~24.04) ...
Setting up libdrm-amdgpu-dev:amd64 (1:2.4.124.60402-2187269.24.04) ...
Setting up hipcub-dev (3.4.0.60402-120~24.04) ...
Setting up hipfort-dev (0.6.0.60402-120~24.04) ...
Setting up rocblas (4.4.1.60402-120~24.04) ...
Setting up rccl (2.22.3.60402-120~24.04) ...
Setting up hip-dev (6.4.43484.60402-120~24.04) ...
Setting up rocprofiler (2.0.60402.60402-120~24.04) ...
Setting up hip-samples (6.4.43484.60402-120~24.04) ...
Setting up rocsparse (3.4.0.60402-120~24.04) ...
Setting up miopen-hip (3.4.0.60402-120~24.04) ...
Setting up rocm-opencl-dev (2.0.0.60402-120~24.04) ...
Setting up rocprofiler-dev (2.0.60402.60402-120~24.04) ...
Setting up rocthrust-dev (3.3.0.60402-120~24.04) ...
Setting up roctracer-dev (4.1.60402.60402-120~24.04) ...
Setting up rocprofiler-compute (3.1.1.60402-120~24.04) ...
Setting up openmp-extras-dev (18.63.0.60402-120~24.04) ...
Setting up rocm-language-runtime (6.4.2.60402-120~24.04) ...
Setting up migraphx (2.12.0.60402-120~24.04) ...
Setting up hipsparse (3.2.0.60402-120~24.04) ...
Setting up rocprofiler-plugins (2.0.60402.60402-120~24.04) ...
Setting up rocsolver (3.28.2.60402-120~24.04) ...
Setting up miopen-hip-dev (3.4.0.60402-120~24.04) ...
Setting up hipblas (2.4.0.60402-120~24.04) ...
Setting up rocm-hip-runtime (6.4.2.60402-120~24.04) ...
/bin/rocm_agent_enumerator not found, but that is OK
/bin/rocminfo not found, but that is OK
Setting up rocm-developer-tools (6.4.2.60402-120~24.04) ...
/bin/amd-smi not found, but that is OK
/bin/rocgdb not found, but that is OK
/bin/rocm-smi not found, but that is OK
/bin/rocprof not found, but that is OK
/bin/rocsys not found, but that is OK
/bin/rocprofv2 not found, but that is OK
/bin/roccoremerge not found, but that is OK
/bin/rocprofv3 not found, but that is OK
/bin/rocprof-compute not found, but that is OK
/bin/rocprof-sys-avail not found, but that is OK
/bin/rocprof-sys-instrument not found, but that is OK
/bin/rocprof-sys-run not found, but that is OK
/bin/rocprof-sys-sample not found, but that is OK
/bin/rocprof-sys-causal not found, but that is OK
Setting up rocm-openmp-sdk (6.4.2.60402-120~24.04) ...
Setting up rccl-dev (2.22.3.60402-120~24.04) ...
Setting up rocblas-dev (4.4.1.60402-120~24.04) ...
Setting up rocsparse-dev (3.4.0.60402-120~24.04) ...
Setting up hip-doc (6.4.43484.60402-120~24.04) ...
Setting up hipsparse-dev (3.2.0.60402-120~24.04) ...
Setting up hipblas-dev (2.4.0.60402-120~24.04) ...
Setting up rocsolver-dev (3.28.2.60402-120~24.04) ...
Setting up rocalution (3.2.3.60402-120~24.04) ...
Setting up migraphx-dev (2.12.0.60402-120~24.04) ...
Setting up hipsolver (2.4.0.60402-120~24.04) ...
Setting up rpp (1.9.10.60402-120~24.04) ...
Setting up rocm-opencl-runtime (6.4.2.60402-120~24.04) ...
/bin/clinfo not found, but that is OK
Setting up hipsolver-dev (2.4.0.60402-120~24.04) ...
Setting up hipsparselt (0.2.3.60402-120~24.04) ...
Setting up rocm-hip-runtime-dev (6.4.2.60402-120~24.04) ...
/bin/roc-obj not found, but that is OK
/bin/roc-obj-extract not found, but that is OK
/bin/roc-obj-ls not found, but that is OK
/bin/hipcc not found, but that is OK
/bin/hipcc.pl not found, but that is OK
/bin/hipcc.bin not found, but that is OK
/bin/hipcc_cmake_linker_helper not found, but that is OK
/bin/hipconfig not found, but that is OK
/bin/hipconfig.pl not found, but that is OK
/bin/hipconfig.bin not found, but that is OK
/bin/hipconvertinplace-perl.sh not found, but that is OK
/bin/hipconvertinplace.sh not found, but that is OK
/bin/hipdemangleatp not found, but that is OK
/bin/hipexamine-perl.sh not found, but that is OK
/bin/hipexamine.sh not found, but that is OK
/bin/hipify-perl not found, but that is OK
/bin/hipify-clang not found, but that is OK
/bin/amdclang not found, but that is OK
/bin/amdclang++ not found, but that is OK
/bin/amdflang not found, but that is OK
/bin/amdlld not found, but that is OK
Setting up rocm-hip-libraries (6.4.2.60402-120~24.04) ...
Setting up mivisionx (3.2.0.60402-120~24.04) ...
Setting up rocm-opencl-sdk (6.4.2.60402-120~24.04) ...
Setting up rocalution-dev (3.2.3.60402-120~24.04) ...
Setting up rpp-dev (1.9.10.60402-120~24.04) ...
Setting up hipsparselt-dev (0.2.3.60402-120~24.04) ...
Setting up rocm-ml-libraries (6.4.2.60402-120~24.04) ...
Setting up rocm-hip-sdk (6.4.2.60402-120~24.04) ...
/bin/hipfc not found, but that is OK
Setting up mivisionx-dev (3.2.0.60402-120~24.04) ...
Setting up rocm-ml-sdk (6.4.2.60402-120~24.04) ...
Setting up rocm (6.4.2.60402-120~24.04) ...
/bin/runvx not found, but that is OK
Processing triggers for libc-bin (2.39-0ubuntu8.5) ...

$ /opt/rocm-6.4.2/lib/llvm/bin/clang -v

AMD clang version 19.0.0git (https://github.com/RadeonOpenCompute/llvm-project roc-6.4.2 25224 d366fa84f3fdcbd4b10847ebd5db572ae12a34fb)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm-6.4.2/lib/llvm/bin
Configuration file: /opt/rocm-6.4.2/lib/llvm/bin/clang.cfg
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/13
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/14
Candidate multilib: .;@m64
Selected multilib: .;@m64
Found HIP installation: /opt/rocm-6.4.2/lib/llvm/bin/../../.., version 6.4.43484
 "/opt/rocm-6.4.2/lib/llvm/bin/ld.lld" --hash-style=gnu --eh-frame-hdr -m elf_x86_64 -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o a.out /lib/x86_64-linux-gnu/crt1.o /lib/x86_64-linux-gnu/crti.o /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtbegin-x86_64.o -L/usr/lib/gcc/x86_64-linux-gnu/14 -L/usr/lib/gcc/x86_64-linux-gnu/14/../../../../lib64 -L/lib/x86_64-linux-gnu -L/lib/../lib64 -L/usr/lib/x86_64-linux-gnu -L/usr/lib/../lib64 -L/lib -L/usr/lib --enable-new-dtags /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed -lc /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/libclang_rt.builtins-x86_64.a --as-needed -lgcc_s --no-as-needed /opt/rocm-6.4.2/lib/llvm/lib/clang/19/lib/linux/clang_rt.crtend-x86_64.o /lib/x86_64-linux-gnu/crtn.o
ld.lld: error: undefined symbol: main
>>> referenced by /lib/x86_64-linux-gnu/crt1.o:(_start)
clang: error: linker command failed with exit code 1 (use -v to see invocation)

```

Going to restart, to see if it makes any difference. 


---

### 评论 #11 — chowdri (2025-07-28T18:56:55Z)

Update: restart makes no difference. 


---

### 评论 #12 — tcgu-amd (2025-07-28T19:08:11Z)

Try building again?

---

### 评论 #13 — Nindaleth (2025-07-28T19:14:59Z)

If it helps in any way, `/opt/rocm-6.4.2/lib/llvm/bin/clang -v` also fails for me, but I can build llama.cpp with HIP support no problem.

I think that that command forces it to compile something verbosely out of nothing, was the intention maybe `/opt/rocm-6.4.2/lib/llvm/bin/clang --version` to display version info?

---

### 评论 #14 — tcgu-amd (2025-07-28T19:16:25Z)

> If it helps in any way, `/opt/rocm-6.4.2/lib/llvm/bin/clang -v` also fails for me, but I can build llama.cpp with HIP support no problem.
> 
> I think that that command forces it to compile something verbosely out of nothing, was the intention maybe `/opt/rocm-6.4.2/lib/llvm/bin/clang --version` to display version info?

Yes I think you are correct, I also get an error with -v

---

### 评论 #15 — chowdri (2025-07-28T19:17:02Z)

yes, now the model loads. Doesnt run, but I dont know that's a rocm issue or llama issue. 

```
$ export HIP_VISIBLE_DEVICES=0

$ llama-cli -m ../.lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf -ngl 41

ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 GRE, gfx1100 (0x1100), VMM: no, Wave Size: 32
build: 6019 (8ad7b3e6) with cc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0 for x86_64-linux-gnu
main: llama backend init
main: load the model and apply lora adapter, if any
llama_model_load_from_file_impl: using device ROCm0 (Radeon RX 7900 GRE) - 16322 MiB free
llama_model_loader: loaded meta data with 27 key-value pairs and 443 tensors from ../.lmstudio/models/lmstudio-community/Qwen3-14B-GGUF/Qwen3-14B-Q8_0.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen3
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Qwen3 14B
llama_model_loader: - kv   3:                           general.basename str              = Qwen3
llama_model_loader: - kv   4:                         general.size_label str              = 14B
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
llama_model_loader: - kv  17:                      tokenizer.ggml.tokens arr[str,151936]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  18:                  tokenizer.ggml.token_type arr[i32,151936]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  19:                      tokenizer.ggml.merges arr[str,151387]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  20:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  21:            tokenizer.ggml.padding_token_id u32              = 151643
llama_model_loader: - kv  22:                tokenizer.ggml.bos_token_id u32              = 151643
llama_model_loader: - kv  23:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  24:                    tokenizer.chat_template str              = {%- if tools %}\n    {{- '<|im_start|>...
llama_model_loader: - kv  25:               general.quantization_version u32              = 2
llama_model_loader: - kv  26:                          general.file_type u32              = 7
llama_model_loader: - type  f32:  161 tensors
llama_model_loader: - type q8_0:  282 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q8_0
print_info: file size   = 14.61 GiB (8.50 BPW) 
load: special tokens cache size = 26
load: token to piece cache size = 0.9311 MB
print_info: arch             = qwen3
print_info: vocab_only       = 0
print_info: n_ctx_train      = 32768
print_info: n_embd           = 5120
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
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 1000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 32768
print_info: rope_finetuned   = unknown
print_info: model type       = 14B
print_info: model params     = 14.77 B
print_info: general.name     = Qwen3 14B
print_info: vocab type       = BPE
print_info: n_vocab          = 151936
print_info: n_merges         = 151387
print_info: BOS token        = 151643 '<|endoftext|>'
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151645 '<|im_end|>'
print_info: PAD token        = 151643 '<|endoftext|>'
print_info: LF token         = 198 'Ċ'
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
load_tensors:        ROCm0 model buffer size = 14177.36 MiB
load_tensors:   CPU_Mapped model buffer size =   788.24 MiB
...........................................................................................
llama_context: constructing llama_context
llama_context: non-unified KV cache requires ggml_set_rows() - forcing unified KV cache
llama_context: n_seq_max     = 1
llama_context: n_ctx         = 4096
llama_context: n_ctx_per_seq = 4096
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = 0
llama_context: kv_unified    = true
llama_context: freq_base     = 1000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_per_seq (4096) < n_ctx_train (32768) -- the full capacity of the model will not be utilized
llama_context:  ROCm_Host  output buffer size =     0.58 MiB
llama_kv_cache_unified:      ROCm0 KV buffer size =   640.00 MiB
llama_kv_cache_unified: size =  640.00 MiB (  4096 cells,  40 layers,  1/ 1 seqs), K (f16):  320.00 MiB, V (f16):  320.00 MiB
llama_kv_cache_unified: LLAMA_SET_ROWS=0, using old ggml_cpy() method for backwards compatibility
llama_context:      ROCm0 compute buffer size =   368.00 MiB
llama_context:  ROCm_Host compute buffer size =    18.01 MiB
llama_context: graph nodes  = 1646
llama_context: graph splits = 2
common_init_from_params: added <|endoftext|> logit bias = -inf
common_init_from_params: added <|im_end|> logit bias = -inf
common_init_from_params: added <|fim_pad|> logit bias = -inf
common_init_from_params: added <|repo_name|> logit bias = -inf
common_init_from_params: added <|file_sep|> logit bias = -inf
common_init_from_params: setting dry_penalty_last_n to ctx_size = 4096
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
main: llama threadpool init, n_threads = 16
main: chat template is available, enabling conversation mode (disable it with -no-cnv)
main: chat template example:
<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there<|im_end|>
<|im_start|>user
How are you?<|im_end|>
<|im_start|>assistant


system_info: n_threads = 16 (n_threads_batch = 16) / 32 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | 

main: interactive mode on.
sampler seed: 3155407193
sampler params: 
	repeat_last_n = 64, repeat_penalty = 1.000, frequency_penalty = 0.000, presence_penalty = 0.000
	dry_multiplier = 0.000, dry_base = 1.750, dry_allowed_length = 2, dry_penalty_last_n = 4096
	top_k = 40, top_p = 0.950, min_p = 0.050, xtc_probability = 0.000, xtc_threshold = 0.100, typical_p = 1.000, top_n_sigma = -1.000, temp = 0.800
	mirostat = 0, mirostat_lr = 0.100, mirostat_ent = 5.000
sampler chain: logits -> logit-bias -> penalties -> dry -> top-n-sigma -> top-k -> typical -> top-p -> min-p -> xtc -> temp-ext -> dist 
generate: n_ctx = 4096, n_batch = 2048, n_predict = -1, n_keep = 0

== Running in interactive mode. ==
 - Press Ctrl+C to interject at any time.
 - Press Return to return control to the AI.
 - To return control without starting a new line, end your input with '/'.
 - If you want to submit another line, end your input with '\'.
 - Not using system message. To change it, set a different value via -sys PROMPT
```



---

### 评论 #16 — Nindaleth (2025-07-28T19:19:19Z)

Cool! Now llama.cpp runs as designed. It compiled successfully, offloaded all layers as expected and now awaits your turn in conversation, you have to type something to keep the conversation going. I think the original issue (and all ROCm-related issues) is solved here.

---

### 评论 #17 — chowdri (2025-07-28T19:20:38Z)

I did, 

```
> what can this tool do for me

llama_perf_sampler_print:    sampling time =       0.00 ms /    15 runs   (    0.00 ms per token, 5000000.00 tokens per second)
llama_perf_context_print:        load time =    7274.11 ms
llama_perf_context_print: prompt eval time =       0.00 ms /     1 tokens (    0.00 ms per token,      inf tokens per second)
llama_perf_context_print:        eval time =       0.00 ms /     1 runs   (    0.00 ms per token,      inf tokens per second)
llama_perf_context_print:       total time =  119086.67 ms /     2 tokens
llama_perf_context_print:    graphs reused =          0
Interrupted by user

```

---

### 评论 #18 — tcgu-amd (2025-07-28T19:44:43Z)

Interesting, so it just silently exited, but didn't crash either. Can you try with -v to see what the log says?


---

### 评论 #19 — chowdri (2025-07-28T20:28:20Z)

no, no, I had to exit because it was taking too long. It was running on the gpu though


---

### 评论 #20 — tcgu-amd (2025-07-29T16:41:53Z)

Hi @chowdri, I was looking at your other ticket -- seems you are able to get it to run on GPU but right now the performance is extremely slow. I am going to close this ticket for now since the original issue is now resolved. I think it would be the best to open a new ticket for performance (easier for other users to search it up). 

By the way, for performance, if you can run your workload with AMD_LOG_LEVEL=5 and share the outputs that would be great. 

Thanks! 

P.S. After opening a new ticket, please mention me there so I can continue to help you. :)

---

### 评论 #21 — chowdri (2025-07-29T19:46:35Z)

where to set this parameter: AMD_LOG_LEVEL=5?

---

### 评论 #22 — tcgu-amd (2025-07-29T19:49:17Z)

> where to set this parameter: AMD_LOG_LEVEL=5 

It is an env variable so you can just export it.

---

### 评论 #23 — chowdri (2025-07-29T19:50:33Z)

how to access the logs?

---

### 评论 #24 — tcgu-amd (2025-07-29T20:00:14Z)

> how to access the logs?

You should be able to see it on command line

---

### 评论 #25 — chowdri (2025-07-29T20:22:09Z)

<!-- Failed to upload "rocm_llama.log" -->
The logs are really elaborate. I dont think github would let me post comments this long. My browser itself is struggling to incorporate the paste.
I cant attach the log in a file either, it's 41+ MB.

---
