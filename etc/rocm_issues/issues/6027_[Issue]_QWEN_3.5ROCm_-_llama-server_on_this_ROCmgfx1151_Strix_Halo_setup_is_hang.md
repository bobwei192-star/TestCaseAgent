# [Issue]: QWEN 3.5|ROCm - llama-server on this ROCm/gfx1151 Strix Halo setup is hanging during tensor finalization / backend graph init after offload placement.

> **Issue #6027**
> **状态**: closed
> **创建时间**: 2026-03-10T00:04:16Z
> **更新时间**: 2026-04-01T15:05:29Z
> **关闭时间**: 2026-04-01T15:05:29Z
> **作者**: dustinwish
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6027

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem Description

Copied from AMD Discord: Anyone running QWEN 3.5 yet? Seems there are llama issues with it?

OK... After updating llama to b8245 release ....no dice. It is getting stuck at warm-up so I killed the warm up, same issue, I tried --n-gpu-layers 0  up to 99 to get it to run on the CPU.....still stuck. I tried down shifting the model Same pattern — 99.9% CPU, VmRSS frozen at 310MB, VmSize stopped growing. It's hung again at sched_reserve even on Qwen3.5-27B.
rocminfo | grep -i version
ROCk module version 6.16.13 is loaded
Runtime Version:         1.18
Runtime Ext Version:     1.15
The 27B also has SSM/DeltaNet layers so it hits the same sched_reserve deadlock.
t is not just the 35B A3B model. Your 27B Qwen 3.5 also reaches the same stage:

metadata loads

tensors are assigned

layers are offloaded to ROCm

then it stalls at load_tensors

That points much more strongly to a ROCm + Strix Halo + full-offload loading problem than to a bad GGUF or missing Qwen support. There is an upstream llama.cpp issue specifically reporting Strix Halo / gfx1151 systems hanging at load_tensors, and another Strix Halo issue about ROCm memory behavior on this platform.

OK... After updating llama to b8245 release ....no dice. It is getting stuck at warm-up so I killed the warm up, same issue, I tried --n-gpu-layers 0  up to 99 to get it to run on the CPU.....still stuck. I tried down shifting the model Same pattern — 99.9% CPU, VmRSS frozen at 310MB, VmSize stopped growing. It's hung again at sched_reserve even on Qwen3.5-27B.
rocminfo | grep -i version
ROCk module version 6.16.13 is loaded
Runtime Version:         1.18
Runtime Ext Version:     1.15
The 27B also has SSM/DeltaNet layers so it hits the same sched_reserve deadlock.
t is not just the 35B A3B model. Your 27B Qwen 3.5 also reaches the same stage:

metadata loads

tensors are assigned

layers are offloaded to ROCm

then it stalls at load_tensors

That points much more strongly to a ROCm + Strix Halo + full-offload loading problem than to a bad GGUF or missing Qwen support. There is an upstream llama.cpp issue specifically reporting Strix Halo / gfx1151 systems hanging at load_tensors, and another Strix Halo issue about ROCm memory behavior on this platform.

llama-server on this ROCm/gfx1151 Strix Halo setup is hanging during tensor finalization / backend graph init after offload placement.
What it still points to

It is more likely:

ROCm backend bug on Strix Halo / gfx1151

full or partial GPU offload path issue

specific interaction with this llama.cpp build on your platform
ggml_cuda_init: failed to initialize ROCm: no ROCm-capable device is detected

PID %CPU %MEM     ELAPSED CMD
  70547  100 11.9       01:02 ./llama-server -m /home/dustinwish/.cache/huggingface/hub/models--unsloth--Qwen3.5-27B-GGUF/snapshots/d0cb6e
VmSize: 22655272 kB
VmRSS:  15637476 kB

read_bytes: 0
write_bytes: 294912
cancelled_write_bytes: 258048
dustinwish@bigdai:~/downloads/llama.cpp/build/bin$ unset HIP_VISIBLE_DEVICES
export GGML_HIP_FORCE_MMQ=1

./llama-server \
  -m ~/.cache/huggingface/hub/models--unsloth--Qwen3.5-27B-GGUF/snapshots/d0cb6e84962d23e5b86e65f7c21e003faf0f0d68/Qwen3.5-27B-Q4_K_M.gguf \
  --ctx-size 2048 \

dustinwish@bigdai:~/downloads/llama.cpp/build/bin$ unset HIP_VISIBLE_DEVICES
export GGML_HIP_FORCE_MMQ=1

./llama-server \
  -m ~/.cache/huggingface/hub/models--unsloth--Qwen3.5-27B-GGUF/snapshots/d0cb6e84962d23e5b86e65f7c21e003faf0f0d68/Qwen3.5-27B-Q4_K_M.gguf \
  --ctx-size 2048 \
  --batch-size 128 \
  --ubatch-size 32 \
  --fit off \
  --no-warmup \
  --no-mmap \
  --flash-attn off \
  --n-gpu-layers 1 \
  --host 127.0.0.1 \
  --port 8001
ggml_cuda_init: found 1 ROCm devices (Total VRAM: 63720 MiB):
  Device 0: AMD Radeon Graphics, gfx1151 (0x1151), VMM: no, Wave Size: 32, VRAM: 63720 MiB (63716 MiB free)
main: n_parallel is set to auto, using n_parallel = 4 and kv_unified = true
build: 8248 (5f4cdac38) with GNU 13.3.0 for Linux x86_64
system info: n_threads = 16, n_threads_batch = 16, total_threads = 32

system_info: n_threads = 16 (n_threads_batch = 16) / 32 | ROCm : NO_VMM = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX_VNNI = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 |

Running without SSL
init: using 31 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model '/home/dustinwish/.cache/huggingface/hub/models--unsloth--Qwen3.5-27B-GGUF/snapshots/d0cb6e84962d23e5b86e65f7c21e003faf0f0d68/Qwen3.5-27B-Q4_K_M.gguf'
llama_model_load_from_file_impl: using device ROCm0 (AMD Radeon Graphics) (0000:c6:00.0) - 125192 MiB free
llama_model_loader: loaded meta data with 49 key-value pairs and 851 tensors from /home/dustinwish/.cache/huggingface/hub/models--unsloth--Qwen3.5-27B-GGUF/snapshots/d0cb6e84962d23e5b86e65f7c21e003faf0f0d68/Qwen3.5-27B-Q4_K_M.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen35
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                     general.sampling.top_k i32              = 20
llama_model_loader: - kv   3:                     general.sampling.top_p f32              = 0.950000
llama_model_loader: - kv   4:                      general.sampling.temp f32              = 0.600000
llama_model_loader: - kv   5:                               general.name str              = Qwen3.5-27B
llama_model_loader: - kv   6:                           general.basename str              = Qwen3.5-27B
llama_model_loader: - kv   7:                       general.quantized_by str              = Unsloth
llama_model_loader: - kv   8:                         general.size_label str              = 27B
llama_model_loader: - kv   9:                            general.license str              = apache-2.0
llama_model_loader: - kv  10:                       general.license.link str              = https://huggingface.co/Qwen/Qwen3.5-2...
llama_model_loader: - kv  11:                           general.repo_url str              = https://huggingface.co/unsloth
llama_model_loader: - kv  12:                   general.base_model.count u32              = 1
llama_model_loader: - kv  13:                  general.base_model.0.name str              = Qwen3.5 27B
llama_model_loader: - kv  14:          general.base_model.0.organization str              = Qwen
llama_model_loader: - kv  15:              general.base_model.0.repo_url str              = https://huggingface.co/Qwen/Qwen3.5-27B
llama_model_loader: - kv  16:                               general.tags arr[str,3]       = ["qwen3_5_moe", "unsloth", "image-tex...
llama_model_loader: - kv  17:                         qwen35.block_count u32              = 64
llama_model_loader: - kv  18:                      qwen35.context_length u32              = 262144
llama_model_loader: - kv  19:                    qwen35.embedding_length u32              = 5120
llama_model_loader: - kv  20:                 qwen35.feed_forward_length u32              = 17408
llama_model_loader: - kv  21:                qwen35.attention.head_count u32              = 24
llama_model_loader: - kv  22:             qwen35.attention.head_count_kv u32              = 4
llama_model_loader: - kv  23:             qwen35.rope.dimension_sections arr[i32,4]       = [11, 11, 10, 0]
llama_model_loader: - kv  24:                      qwen35.rope.freq_base f32              = 10000000.000000
llama_model_loader: - kv  25:    qwen35.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  26:                qwen35.attention.key_length u32              = 256
llama_model_loader: - kv  27:              qwen35.attention.value_length u32              = 256
llama_model_loader: - kv  28:                     qwen35.ssm.conv_kernel u32              = 4
llama_model_loader: - kv  29:                      qwen35.ssm.state_size u32              = 128
llama_model_loader: - kv  30:                     qwen35.ssm.group_count u32              = 16
llama_model_loader: - kv  31:                  qwen35.ssm.time_step_rank u32              = 48
llama_model_loader: - kv  32:                      qwen35.ssm.inner_size u32              = 6144
llama_model_loader: - kv  33:             qwen35.full_attention_interval u32              = 4
llama_model_loader: - kv  34:                qwen35.rope.dimension_count u32              = 64
llama_model_loader: - kv  35:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  36:                         tokenizer.ggml.pre str              = qwen35
llama_model_loader: - kv  37:                      tokenizer.ggml.tokens arr[str,248320]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  38:                  tokenizer.ggml.token_type arr[i32,248320]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  39:                      tokenizer.ggml.merges arr[str,247587]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  40:                tokenizer.ggml.eos_token_id u32              = 248046
llama_model_loader: - kv  41:            tokenizer.ggml.padding_token_id u32              = 248055
llama_model_loader: - kv  42:                    tokenizer.chat_template str              = {%- set image_count = namespace(value...
llama_model_loader: - kv  43:               general.quantization_version u32              = 2
llama_model_loader: - kv  44:                          general.file_type u32              = 15
llama_model_loader: - kv  45:                      quantize.imatrix.file str              = Qwen3.5-27B-GGUF/imatrix_unsloth.gguf
llama_model_loader: - kv  46:                   quantize.imatrix.dataset str              = unsloth_calibration_Qwen3.5-27B.txt
llama_model_loader: - kv  47:             quantize.imatrix.entries_count u32              = 496
llama_model_loader: - kv  48:              quantize.imatrix.chunks_count u32              = 80
llama_model_loader: - type  f32:  353 tensors
llama_model_loader: - type q8_0:   96 tensors
llama_model_loader: - type q4_K:  263 tensors
llama_model_loader: - type q5_K:   96 tensors
llama_model_loader: - type q6_K:   43 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q4_K - Medium
print_info: file size   = 15.58 GiB (4.98 BPW)
load: 0 unused tokens
load: printing all EOG tokens:
load:   - 248044 ('<|endoftext|>')
load:   - 248046 ('<|im_end|>')
load:   - 248063 ('<|fim_pad|>')
load:   - 248064 ('<|repo_name|>')
load:   - 248065 ('<|file_sep|>')
load: special tokens cache size = 33
load: token to piece cache size = 1.7581 MB
print_info: arch                  = qwen35
print_info: vocab_only            = 0
print_info: no_alloc              = 0
... (72 lines left)

dustinwish@bigdai:~/downloads/llama-b8245$ # Check ROCm version while we wait
cat /opt/rocm/.info/version 2>/dev/null || \
rocminfo 2>/dev/null | grep "Runtime Version" | head -3
7.2.0
dustinwish@bigdai:~/downloads/llama-b8245$
So it.....it iseems like a ROCm issue at this point?
I'm going to switch over to Vulkan to see how it runs with it instead and follow for fixes
QWEN 3.5 seems buggy for sure
hat confirms it: even --n-gpu-layers 1 hangs on your Strix Halo ROCm path.

The key lines are:

load_tensors: offloaded 1/65 layers to GPU
load_tensors:          CPU model buffer size =   682.03 MiB
load_tensors:        ROCm0 model buffer size =   994.65 MiB
load_tensors:    ROCm_Host model buffer size = 14278.12 MiB

So the failure is not “too many GPU layers.”
It happens as soon as the HIP backend tries to use any GPU-resident model buffer and a very large ROCm_Host staging/allocation buffer.

That means your practical conclusion is:

On this current llama.cpp + ROCm + gfx1151 setup, GPU offload is unusable. CPU-only works.

Well... It runs super fast on Vulkan...
dustinwish@bigdai:~/downloads/llama-vulkan/llama-b8245$ ./llama-server \
  -m ~/lemonade-models/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf \
  --fit off \
  --n-gpu-layers 99 \
  --ctx-size 4096 \
  --batch-size 256 \

dustinwish@bigdai:~/downloads/llama-vulkan/llama-b8245$ ./llama-server \
  -m ~/lemonade-models/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf \
  --fit off \
  --n-gpu-layers 99 \
  --ctx-size 4096 \
  --batch-size 256 \
  --host 0.0.0.0 \
  --port 8001
load_backend: loaded RPC backend from /home/dustinwish/downloads/llama-vulkan/llama-b8245/libggml-rpc.so
ggml_vulkan: Found 1 Vulkan devices:
ggml_vulkan: 0 = AMD Radeon Graphics (RADV GFX1151) (radv) | uma: 1 | fp16: 1 | bf16: 0 | warp size: 64 | shared memory: 65536 | int dot: 1 | matrix cores: KHR_coopmat
load_backend: loaded Vulkan backend from /home/dustinwish/downloads/llama-vulkan/llama-b8245/libggml-vulkan.so
load_backend: loaded CPU backend from /home/dustinwish/downloads/llama-vulkan/llama-b8245/libggml-cpu-zen4.so
main: n_parallel is set to auto, using n_parallel = 4 and kv_unified = true
build: 8245 (d417bc43d) with GNU 11.4.0 for Linux x86_64
system info: n_threads = 16, n_threads_batch = 16, total_threads = 32

system_info: n_threads = 16 (n_threads_batch = 16) / 32 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | AVX512_BF16 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 |

Running without SSL
init: using 31 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model '/home/dustinwish/lemonade-models/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf'
llama_model_load_from_file_impl: using device Vulkan0 (AMD Radeon Graphics (RADV GFX1151)) (0000:c6:00.0) - 63425 MiB free
llama_model_loader: loaded meta data with 52 key-value pairs and 733 tensors from /home/dustinwish/lemonade-models/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen35moe
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                     general.sampling.top_k i32              = 20
llama_model_loader: - kv   3:                     general.sampling.top_p f32              = 0.950000
llama_model_loader: - kv   4:                      general.sampling.temp f32              = 1.000000
llama_model_loader: - kv   5:                               general.name str              = Qwen3.5-35B-A3B
llama_model_loader: - kv   6:                           general.basename str              = Qwen3.5-35B-A3B
llama_model_loader: - kv   7:                       general.quantized_by str              = Unsloth
llama_model_loader: - kv   8:                         general.size_label str              = 35B-A3B
llama_model_loader: - kv   9:                            general.license str              = apache-2.0
llama_model_loader: - kv  10:                       general.license.link str              = https://huggingface.co/Qwen/Qwen3.5-3...
llama_model_loader: - kv  11:                           general.repo_url str              = https://huggingface.co/unsloth
llama_model_loader: - kv  12:                   general.base_model.count u32              = 1
llama_model_loader: - kv  13:                  general.base_model.0.name str              = Qwen3.5 35B A3B
llama_model_loader: - kv  14:          general.base_model.0.organization str              = Qwen
llama_model_loader: - kv  15:              general.base_model.0.repo_url str              = https://huggingface.co/Qwen/Qwen3.5-3...
llama_model_loader: - kv  16:                               general.tags arr[str,2]       = ["unsloth", "image-text-to-text"]
llama_model_loader: - kv  17:                      qwen35moe.block_count u32              = 40
llama_model_loader: - kv  18:                   qwen35moe.context_length u32              = 262144
llama_model_loader: - kv  19:                 qwen35moe.embedding_length u32              = 2048
llama_model_loader: - kv  20:             qwen35moe.attention.head_count u32              = 16
llama_model_loader: - kv  21:          qwen35moe.attention.head_count_kv u32              = 2
llama_model_loader: - kv  22:          qwen35moe.rope.dimension_sections arr[i32,4]       = [11, 11, 10, 0]
llama_model_loader: - kv  23:                   qwen35moe.rope.freq_base f32              = 10000000.000000
llama_model_loader: - kv  24: qwen35moe.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  25:                     qwen35moe.expert_count u32              = 256
llama_model_loader: - kv  26:                qwen35moe.expert_used_count u32              = 8
llama_model_loader: - kv  27:             qwen35moe.attention.key_length u32              = 256
llama_model_loader: - kv  28:           qwen35moe.attention.value_length u32              = 256
llama_model_loader: - kv  29:       qwen35moe.expert_feed_forward_length u32              = 512
llama_model_loader: - kv  30: qwen35moe.expert_shared_feed_forward_length u32              = 512
llama_model_loader: - kv  31:                  qwen35moe.ssm.conv_kernel u32              = 4
llama_model_loader: - kv  32:                   qwen35moe.ssm.state_size u32              = 128
llama_model_loader: - kv  33:                  qwen35moe.ssm.group_count u32              = 16
llama_model_loader: - kv  34:               qwen35moe.ssm.time_step_rank u32              = 32
llama_model_loader: - kv  35:                   qwen35moe.ssm.inner_size u32              = 4096
llama_model_loader: - kv  36:          qwen35moe.full_attention_interval u32              = 4
llama_model_loader: - kv  37:             qwen35moe.rope.dimension_count u32              = 64
llama_model_loader: - kv  38:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  39:                         tokenizer.ggml.pre str              = qwen35
llama_model_loader: - kv  40:                      tokenizer.ggml.tokens arr[str,248320]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  41:                  tokenizer.ggml.token_type arr[i32,248320]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  42:                      tokenizer.ggml.merges arr[str,247587]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  43:                tokenizer.ggml.eos_token_id u32              = 248046
llama_model_loader: - kv  44:            tokenizer.ggml.padding_token_id u32              = 248055
llama_model_loader: - kv  45:                    tokenizer.chat_template str              = {%- set image_count = namespace(value...
llama_model_loader: - kv  46:               general.quantization_version u32              = 2
llama_model_loader: - kv  47:                          general.file_type u32              = 15
llama_model_loader: - kv  48:                      quantize.imatrix.file str              = Qwen3.5-35B-A3B-GGUF/imatrix_unsloth....
llama_model_loader: - kv  49:                   quantize.imatrix.dataset str              = unsloth_calibration_Qwen3.5-35B-A3B.txt
llama_model_loader: - kv  50:             quantize.imatrix.entries_count u32              = 510
llama_model_loader: - kv  51:              quantize.imatrix.chunks_count u32              = 76
llama_model_loader: - type  f32:  301 tensors
llama_model_loader: - type q8_0:  312 tensors
llama_model_loader: - type q4_K:   78 tensors
llama_model_loader: - type q5_K:   41 tensors
llama_model_loader: - type q6_K:    1 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q4_K - Medium
print_info: file size   = 20.70 GiB (5.13 BPW)
load: 0 unused tokens
load: printing all EOG tokens:
load:   - 248044 ('<|endoftext|>')
load:   - 248046 ('<|im_end|>')
load:   - 248063 ('<|fim_pad|>')
load:   - 248064 ('<|repo_name|>')
load:   - 248065 ('<|file_sep|>')
load: special tokens cache size = 33
load: token to piece cache size = 1.7581 MB
print_info: arch                  = qwen35moe
print_info: vocab_only            = 0
print_info: no_alloc              = 0
print_info: n_ctx_train           = 262144
... (129 lines left)

So it seems like a ROCm issue for sure....

dustinwish@bigdai:~$   echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
  echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
  echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
OS:
NAME="Ubuntu"
VERSION="24.04.4 LTS (Noble Numbat)"
CPU:
model name	: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151
  Marketing Name:          AMD Radeon Graphics
      Name:                    amdgcn-amd-amdhsa--gfx1151
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
  Name:                    aie2p
  Marketing Name:          RyzenAI-npu5
dustinwish@bigdai:~$

### Operating System

Ubuntu 24.04.4 LTS (Noble Numbat)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

dustinwish@bigdai:~$ /opt/rocm/bin/rocminfo --support
ROCk module version 6.16.13 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.15
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5187
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
      Size:                    130499400(0x7c74348) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130499400(0x7c74348) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    130499400(0x7c74348) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    130499400(0x7c74348) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1151
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon Graphics
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
    L2:                      2048(0x800) KB
    L3:                      32768(0x8000) KB
  Chip ID:                 5510(0x1586)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   2900
  BDFID:                   50688
  Internal Node ID:        1
  Compute Unit:            40
  SIMDs per CU:            2
  Shader Engines:          2
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
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

    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 32
  SDMA engine uCode::      17
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65249700(0x3e3a1a4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65249700(0x3e3a1a4) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1151
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
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
        x                        2147483647(0x7fffffff)
        y                        65535(0xffff)
        z                        65535(0xffff)
      FBarrier Max Size:       32
*******
Agent 3
*******
  Name:                    aie2p
  Uuid:                    AIE-XX
  Marketing Name:          RyzenAI-npu5
  Vendor Name:             AMD
  Feature:                 AGENT_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        1(0x1)
  Queue Min Size:          64(0x40)
  Queue Max Size:          64(0x40)
  Queue Type:              SINGLE
  Node:                    0
  Device Type:             DSP
  Cache Info:
    L2:                      2048(0x800) KB
    L3:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          0(0x0)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            0
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:0
  Memory Properties:
  Features:                AGENT_DISPATCH
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    130499400(0x7c74348) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65536(0x10000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    130499400(0x7c74348) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — zichguan-amd (2026-03-17T19:37:29Z)

Hi @dustinwish, I just tested gfx1151 on llama.cpp@ee4801e5a6ee7ee4063144ab44ab4e127f76fba8 + therock-dist-linux-gfx110X-all-7.13.0a20260316.tar.gz, and was able to run with `./llama-server   -hf unsloth/Qwen3.5-27B-GGUF   --ctx-size 2048   --batch-size 128   --ubatch-size 32   --fit off   --no-warmup   --no-mmap   --flash-attn off   --n-gpu-layers 1   --host 127.0.0.1   --port 8001 --verbose` without any issue. Can you provide the kernel version, do you have dkms installed, and dmesg logs?

---

### 评论 #2 — odellus (2026-03-18T06:04:45Z)

I am seeing the same error

---

### 评论 #3 — odellus (2026-03-18T06:07:03Z)

For me it is because the GPU is in a low power state. If I use anything less than the 7.11 preview ROCm llama-server hangs because the GPU is asleep/low power state. If I use 7.11 preview the compiler instructions don't actually apply to my chipset and if I try to fake it I get errors about .dat files not being found because I don't have the Tensor profile or whatever for the chipset I'm pretending to be so I can actually use my computer.

---

### 评论 #4 — npodbielski (2026-03-25T19:52:51Z)

> Hi [@dustinwish](https://github.com/dustinwish), I just tested gfx1151 on llama.cpp@ee4801e5a6ee7ee4063144ab44ab4e127f76fba8


I tested it now on the latest release. Works. 

---

### 评论 #5 — zichguan-amd (2026-03-25T20:08:28Z)

Side note, ROCm 7.2.1 is out and it should fix the low power state issue

---

### 评论 #6 — zichguan-amd (2026-04-01T15:05:29Z)

Closing this since OP is not responding and there's confirmation that OP's configuration works on latest release.

---
