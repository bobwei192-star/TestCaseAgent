# [Issue]: ROCm unable to load models and fails to fold 26.5.1

> **Issue #6227**
> **状态**: open
> **创建时间**: 2026-05-11T16:50:19Z
> **更新时间**: 2026-05-15T17:18:52Z
> **作者**: ratcampaign
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6227

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- mapatel-amd

## 描述

### Problem Description

After 26.5.1, ROCm has been unable to load any local models for both [b1264](https://github.com/lemonade-sdk/llamacpp-rocm/releases/tag/b1264) and [b9106](https://github.com/ggml-org/llama.cpp/releases/tag/b9106)
And
Running Folding@home with the forementioned driver version will not work and the work unit will be dumped.
I was able to fold again after reverting to 26.3.1.

After downgrading to 26.3.1, both versions of the llama.cpp backend started working again and so did Folding@home.

**NOTE:** Folding@home does not utilize HIP to fold proteins (yet). It runs with the OpenCL backend, but the drivers are still somehow broken.

**b1264** output; gets stuck:
```shell
C:\Users\hidden\Desktop\llamarocm>llama-server.exe -ngl 99 -c 16384 --temp 0.3 --top-k 64 --top-p 0.95 --no-mmap --no-context-shift --device ROCm1
ggml_cuda_init: found 2 ROCm devices (Total VRAM: 28781 MiB):
  Device 0: AMD Radeon(TM) Graphics, gfx1036 (0x1036), VMM: no, Wave Size: 32, VRAM: 12477 MiB
  Device 1: AMD Radeon RX 9070 XT, gfx1201 (0x1201), VMM: no, Wave Size: 32, VRAM: 16304 MiB
load_backend: loaded ROCm backend from C:\Users\hidden\Desktop\llamarocm\ggml-hip.dll
load_backend: loaded RPC backend from C:\Users\hidden\Desktop\llamarocm\ggml-rpc.dll
load_backend: loaded CPU backend from C:\Users\hidden\Desktop\llamarocm\ggml-cpu-zen4.dll
load_backend: loaded ROCm backend from C:\Users\hidden\Desktop\llamarocm\ggml-hip.dll
load_backend: loaded RPC backend from C:\Users\hidden\Desktop\llamarocm\ggml-rpc.dll
load_backend: loaded CPU backend from C:\Users\hidden\Desktop\llamarocm\ggml-cpu-zen4.dll
main: n_parallel is set to auto, using n_parallel = 4 and kv_unified = true
build_info: b9106-dd9280a66
system_info: n_threads = 8 (n_threads_batch = 8) / 16 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 |
Running without SSL
init: using 15 threads for HTTP server
srv   load_models: Loaded 0 cached model presets
srv    operator(): Available models (0) (*: custom preset)
main: starting router server, no model will be loaded in this process
start: binding port with default address family
main: router server is listening on http://127.0.0.1:8080
main: NOTE: router mode is experimental
main:       it is not recommended to use this mode in untrusted environments
``` 
**b9106** logs:
```shell
C:\Users\hidden\Desktop\llamahip>llama-server.exe -m C:\Users\hidden\Desktop\granite-4.1-8b-UD-Q8_K_XL.gguf -ngl 99 --no-mmap --no-context-shift -dev ROCm1
ggml_cuda_init: found 2 ROCm devices (Total VRAM: 28781 MiB):
  Device 0: AMD Radeon(TM) Graphics, gfx1036 (0x1036), VMM: no, Wave Size: 32, VRAM: 12477 MiB
  Device 1: AMD Radeon RX 9070 XT, gfx1201 (0x1201), VMM: no, Wave Size: 32, VRAM: 16304 MiB
load_backend: loaded ROCm backend from C:\Users\hidden\Desktop\llamahip\ggml-hip.dll
load_backend: loaded RPC backend from C:\Users\hidden\Desktop\llamahip\ggml-rpc.dll
load_backend: loaded CPU backend from C:\Users\hidden\Desktop\llamahip\ggml-cpu-zen4.dll
load_backend: loaded ROCm backend from C:\Users\hidden\Desktop\llamahip\ggml-hip.dll
load_backend: loaded RPC backend from C:\Users\hidden\Desktop\llamahip\ggml-rpc.dll
load_backend: loaded CPU backend from C:\Users\hidden\Desktop\llamahip\ggml-cpu-zen4.dll
main: n_parallel is set to auto, using n_parallel = 4 and kv_unified = true
build_info: b9106-dd9280a66
system_info: n_threads = 8 (n_threads_batch = 8) / 16 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 |
Running without SSL
init: using 15 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model 'C:\Users\hidden\Desktop\granite-4.1-8b-UD-Q8_K_XL.gguf'
common_init_result: fitting params to device memory, for bugs during this step try to reproduce them with -fit off, or provide --verbose logs if the bug only occurs with -fit on
common_params_fit_impl: getting device memory data for initial parameters:
common_memory_breakdown_print: | memory breakdown [MiB] | total    free     self   model   context   compute    unaccounted |
common_memory_breakdown_print: |   - ROCm1 (RX 9070 XT) | 16304 = 16140 + (30834 =  9938 +   20480 +     416) +      -30670 |
common_memory_breakdown_print: |   - Host               |                   1056 =   784 +       0 +     272                |
common_params_fit_impl: projected to use 30834 MiB of device memory vs. 16140 MiB of free device memory
common_params_fit_impl: cannot meet free memory target of 1024 MiB, need to reduce device memory by 15718 MiB
common_memory_breakdown_print: | memory breakdown [MiB] | total    free     self   model   context   compute    unaccounted |
common_memory_breakdown_print: |   - ROCm1 (RX 9070 XT) | 16304 = 16140 + (10782 =  9938 +     640 +     204) +      -10618 |
common_memory_breakdown_print: |   - Host               |                    808 =   784 +       0 +      24                |
common_params_fit_impl: context size reduced from 131072 to 31488 -> need 15726 MiB less memory in total
common_params_fit_impl: entire model can be fit by reducing context
common_fit_params: successfully fit params to free device memory
common_fit_params: fitting params to free memory took 0.11 seconds
llama_model_loader: loaded meta data with 45 key-value pairs and 363 tensors from C:\Users\hidden\Desktop\granite-4.1-8b-UD-Q8_K_XL.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = granite
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = Granite-4.1-8B
llama_model_loader: - kv   3:                           general.basename str              = Granite-4.1-8B
llama_model_loader: - kv   4:                       general.quantized_by str              = Unsloth
llama_model_loader: - kv   5:                         general.size_label str              = 8B
llama_model_loader: - kv   6:                            general.license str              = apache-2.0
llama_model_loader: - kv   7:                           general.repo_url str              = https://huggingface.co/unsloth
llama_model_loader: - kv   8:                   general.base_model.count u32              = 1
llama_model_loader: - kv   9:                  general.base_model.0.name str              = Granite 4.1 8b
llama_model_loader: - kv  10:          general.base_model.0.organization str              = Ibm Granite
llama_model_loader: - kv  11:              general.base_model.0.repo_url str              = https://huggingface.co/ibm-granite/gr...
llama_model_loader: - kv  12:                               general.tags arr[str,3]       = ["language", "unsloth", "granite-4.1"]
llama_model_loader: - kv  13:                        granite.block_count u32              = 40
llama_model_loader: - kv  14:                     granite.context_length u32              = 131072
llama_model_loader: - kv  15:                   granite.embedding_length u32              = 4096
llama_model_loader: - kv  16:                granite.feed_forward_length u32              = 12800
llama_model_loader: - kv  17:               granite.attention.head_count u32              = 32
llama_model_loader: - kv  18:            granite.attention.head_count_kv u32              = 8
llama_model_loader: - kv  19:                     granite.rope.freq_base f32              = 10000000.000000
llama_model_loader: - kv  20:   granite.attention.layer_norm_rms_epsilon f32              = 0.000010
llama_model_loader: - kv  21:                         granite.vocab_size u32              = 100352
llama_model_loader: - kv  22:               granite.rope.dimension_count u32              = 128
llama_model_loader: - kv  23:                    granite.attention.scale f32              = 0.007812
llama_model_loader: - kv  24:                    granite.embedding_scale f32              = 12.000000
llama_model_loader: - kv  25:                     granite.residual_scale f32              = 0.220000
llama_model_loader: - kv  26:                        granite.logit_scale f32              = 16.000000
llama_model_loader: - kv  27:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  28:                         tokenizer.ggml.pre str              = dbrx
llama_model_loader: - kv  29:                      tokenizer.ggml.tokens arr[str,100352]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  30:                  tokenizer.ggml.token_type arr[i32,100352]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  31:                      tokenizer.ggml.merges arr[str,100000]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  32:                tokenizer.ggml.bos_token_id u32              = 100257
llama_model_loader: - kv  33:                tokenizer.ggml.eos_token_id u32              = 100257
llama_model_loader: - kv  34:            tokenizer.ggml.unknown_token_id u32              = 100269
llama_model_loader: - kv  35:            tokenizer.ggml.padding_token_id u32              = 100256
llama_model_loader: - kv  36:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  37:                    tokenizer.chat_template str              = {%- set tools_system_message_prefix =...
llama_model_loader: - kv  38:            tokenizer.ggml.add_space_prefix bool             = false
llama_model_loader: - kv  39:               general.quantization_version u32              = 2
llama_model_loader: - kv  40:                          general.file_type u32              = 7
llama_model_loader: - kv  41:                      quantize.imatrix.file str              = granite-4.1-8b-GGUF/imatrix_unsloth.gguf
llama_model_loader: - kv  42:                   quantize.imatrix.dataset str              = unsloth_calibration_granite-4.1-8b.txt
llama_model_loader: - kv  43:             quantize.imatrix.entries_count u32              = 280
llama_model_loader: - kv  44:              quantize.imatrix.chunks_count u32              = 209
llama_model_loader: - type  f32:   81 tensors
llama_model_loader: - type  f16:  102 tensors
llama_model_loader: - type q8_0:  180 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q8_0
print_info: file size   = 10.47 GiB (10.23 BPW)
llama_prepare_model_devices: using device ROCm1 (AMD Radeon RX 9070 XT) (0000:03:00.0) - 16152 MiB free
load: 69 unused tokens
load: printing all EOG tokens:
load:   - 100257 ('<|end_of_text|>')
load:   - 100261 ('<|fim_pad|>')
load: special tokens cache size = 96
load: token to piece cache size = 0.6152 MB
print_info: arch                  = granite
print_info: vocab_only            = 0
print_info: no_alloc              = 0
print_info: n_ctx_train           = 131072
print_info: n_embd                = 4096
print_info: n_embd_inp            = 4096
print_info: n_layer               = 40
print_info: n_head                = 32
print_info: n_head_kv             = 8
print_info: n_rot                 = 128
print_info: n_swa                 = 0
print_info: is_swa_any            = 0
print_info: n_embd_head_k         = 128
print_info: n_embd_head_v         = 128
print_info: n_gqa                 = 4
print_info: n_embd_k_gqa          = 1024
print_info: n_embd_v_gqa          = 1024
print_info: f_norm_eps            = 0.0e+00
print_info: f_norm_rms_eps        = 1.0e-05
print_info: f_clamp_kqv           = 0.0e+00
print_info: f_max_alibi_bias      = 0.0e+00
print_info: f_logit_scale         = 1.6e+01
print_info: f_attn_scale          = 7.8e-03
print_info: f_attn_value_scale    = 0.0000
print_info: n_ff                  = 12800
print_info: n_expert              = 0
print_info: n_expert_used         = 0
print_info: n_expert_groups       = 0
print_info: n_group_used          = 0
print_info: causal attn           = 1
print_info: pooling type          = -1
print_info: rope type             = 0
print_info: rope scaling          = linear
print_info: freq_base_train       = 10000000.0
print_info: freq_scale_train      = 1
print_info: n_ctx_orig_yarn       = 131072
print_info: rope_yarn_log_mul     = 0.0000
print_info: rope_finetuned        = yes
print_info: model type            = 3B
print_info: model params          = 8.79 B
print_info: general.name          = Granite-4.1-8B
print_info: f_embedding_scale     = 12.000000
print_info: f_residual_scale      = 0.220000
print_info: f_attention_scale     = 0.007812
print_info: n_ff_shexp            = 0
print_info: vocab type            = BPE
print_info: n_vocab               = 100352
print_info: n_merges              = 100000
print_info: BOS token             = 100257 '<|end_of_text|>'
print_info: EOS token             = 100257 '<|end_of_text|>'
print_info: EOT token             = 100257 '<|end_of_text|>'
print_info: UNK token             = 100269 '<|unk|>'
print_info: PAD token             = 100256 '<|pad|>'
print_info: LF token              = 198 'Ċ'
print_info: FIM PRE token         = 100258 '<|fim_prefix|>'
print_info: FIM SUF token         = 100260 '<|fim_suffix|>'
print_info: FIM MID token         = 100259 '<|fim_middle|>'
print_info: FIM PAD token         = 100261 '<|fim_pad|>'
print_info: EOG token             = 100257 '<|end_of_text|>'
print_info: EOG token             = 100261 '<|fim_pad|>'
print_info: max token length      = 256
load_tensors: loading model tensors, this can take a while... (mmap = false, direct_io = false)
load_tensors: offloading output layer to GPU
load_tensors: offloading 39 repeating layers to GPU
load_tensors: offloaded 41/41 layers to GPU
load_tensors:        ROCm1 model buffer size =  9938.39 MiB
load_tensors:    ROCm_Host model buffer size =   784.00 MiB
.......................................................................................
common_init_result: added <|end_of_text|> logit bias = -inf
common_init_result: added <|fim_pad|> logit bias = -inf
llama_context: constructing llama_context
llama_context: n_seq_max     = 4
llama_context: n_ctx         = 31488
llama_context: n_ctx_seq     = 31488
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = auto
llama_context: kv_unified    = true
llama_context: freq_base     = 10000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_seq (31488) < n_ctx_train (131072) -- the full capacity of the model will not be utilized
llama_context:  ROCm_Host  output buffer size =     1.53 MiB
llama_kv_cache:      ROCm1 KV buffer size =  4920.00 MiB
llama_kv_cache: size = 4920.00 MiB ( 31488 cells,  40 layers,  4/1 seqs), K (f16): 2460.00 MiB, V (f16): 2460.00 MiB
llama_kv_cache: attn_rot_k = 0, n_embd_head_k_all = 128
llama_kv_cache: attn_rot_v = 0, n_embd_head_k_all = 128
sched_reserve: reserving ...
sched_reserve: Flash Attention was auto, set to enabled
sched_reserve: resolving fused Gated Delta Net support:
sched_reserve: fused Gated Delta Net (autoregressive) enabled
sched_reserve: fused Gated Delta Net (chunked) enabled
sched_reserve:      ROCm1 compute buffer size =   204.00 MiB
sched_reserve:  ROCm_Host compute buffer size =    77.51 MiB
sched_reserve: graph nodes  = 1329
sched_reserve: graph splits = 2
sched_reserve: reserve took 46.34 ms, sched copies = 1
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
ggml_cuda_compute_forward: SCALE failed
ROCm error: device kernel image is invalid
  current device: 1, in function ggml_cuda_compute_forward at D:/a/llama.cpp/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:3114
  err
D:/a/llama.cpp/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:102: ROCm error
```

**Folding@home** logs:
```shell
16:25:19:I1:WU39:************************************ System ************************************
16:25:19:I1:WU39: CPU: AMD Ryzen 7 9800X3D 8-Core Processor
16:25:19:I1:WU39: CPU ID: AuthenticAMD Family 26 Model 68 Stepping 0
16:25:19:I1:WU39: CPUs: 16
16:25:19:I1:WU39: Memory: 31.16GiB
16:25:19:I1:WU39:Free Memory: 18.45GiB
16:25:19:I1:WU39: OS Version: 10.0
16:25:19:I1:WU39:Has Battery: false
16:25:19:I1:WU39: On Battery: false
16:25:19:I1:WU39: Hostname: Main
16:25:19:I1:WU39: UTC Offset: 3
16:25:19:I1:WU39: PID: 14620
16:25:19:I1:WU39: CWD: C:\ProgramData\FAHClient\work
16:25:19:I1:WU39: Exec: C:\ProgramData\FAHClient\cores\openmm-core-24\windows-10-64bit\release\fahcore-24-windows-10-64bit-release-8.1.4\FahCore_24.exe
16:25:19:I1:WU39:************************************ OpenMM ************************************
16:25:19:I1:WU39: Version: 8.1.1
16:25:19:I1:WU39:********************************************************************************
16:25:19:I1:WU39:Project: 15413 (Run 0, Clone 678, Gen 12)
16:25:19:I1:WU39:Reading tar file core.xml
16:25:19:I1:WU39:Reading tar file integrator.xml
16:25:19:I1:WU39:Reading tar file state.xml
16:25:19:I1:WU39:Reading tar file system.xml
16:25:19:I1:WU39:Digital signatures verified
16:25:19:I1:WU39:Folding@home GPU Core24 Folding@home Core
16:25:19:I1:WU39:Version 8.1.4
16:25:19:I1:WU39: Checkpoint write interval: 100000 steps (5%) [20 total]
16:25:19:I1:WU39: JSON viewer frame write interval: 20000 steps (1%) [100 total]
16:25:19:I1:WU39: XTC frame write interval: 100000 steps (5%) [20 total]
16:25:19:I1:WU39: TRR frame write interval: disabled
16:25:19:I1:WU39: Global context and integrator variables write interval: disabled
16:25:19:I1:WU39:There are 3 platforms available.
16:25:19:I1:WU39:Platform 0: Reference
16:25:19:I1:WU39:Platform 1: CPU
16:25:19:I1:WU39:Platform 2: OpenCL
16:25:19:I1:WU39: opencl-device 1 specified
16:25:22:I1:WU39:Attempting to create OpenCL context:
16:25:22:I1:WU39: Configuring platform OpenCL
16:25:23:E :WU39:Core exited with Windows unhandled exception code 0xc0000005. See https://bit.ly/2CXgWkZ for more information.
16:25:23:E :WU39:Core returned FAILED_1 (0)
16:25:23:E :WU39:Run did not produce any results. Dumping WU
16:25:23:I1:Default:Added new work unit: cpus:0 gpus:gpu:03:00:00
16:25:23:I1:WU39:Sending dump report
16:25:23:I1:WU40:Requesting WU assignment for user ** team **
16:25:23:I2:OUT27:> POST /api/results HTTP/1.1
16:25:23:I2:OUT28:> POST /api/assign HTTP/1.1
16:25:24:I2:OUT27:< HTTP/1.1 200 HTTP_OK
16:25:24:I1:WU39:Dumped 
```

### Operating System

Windows 11 Pro 10.0.26200

### CPU

AMD Ryzen 7 9800X3D 8-Core Processor 

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

amdhip64_7.dll reports 10.0.3679.0

### ROCm Component

HIP, drivers

### Steps to Reproduce

**Local model/llama.cpp** issue:
Download the llama.cpp backends from the hyperlinks provided at the top
Download any model of choice from HuggingFace (as I think this is not model dependent)
Try to run your models with the args used above (or the ones that matter)

**Folding@home** issue:
Download the Windows (Windows 7+ 64-bit) binary from https://foldingathome.org/beta/
The program after installation starts to tray
Right-click the tray icon and press "Web Control", a webpage should open up in your browser
You should see your machine, press on the cogwheel next to it
Select your GPU from the list of GPUs and enable it (for my instance, gfx1201)
Put CPU core count to zero
Press the "Save" and then "Cancel" button on the top right
Press the play button on the right side of your machine, your computer should start folding now
App logs are found when pressing the list icon

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_
