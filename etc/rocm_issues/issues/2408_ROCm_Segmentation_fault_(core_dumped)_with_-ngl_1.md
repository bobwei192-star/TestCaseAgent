# ROCm Segmentation fault (core dumped) with  -ngl 1

> **Issue #2408**
> **状态**: closed
> **创建时间**: 2023-08-25T19:49:28Z
> **更新时间**: 2023-08-25T19:52:40Z
> **关闭时间**: 2023-08-25T19:52:40Z
> **作者**: grigio
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2408

## 描述

ROCm works in the docker container but if I try to offload a layer I get a segfault

```
rocm-smi --showmeminfo vram



======================= ROCm System Management Interface =======================
============================= Memory Usage (Bytes) =============================
GPU[0]		: VRAM Total Memory (B): 536870912
GPU[0]		: VRAM Total Used Memory (B): 25616384
================================================================================
============================= End of ROCm SMI Log ==============================

```

```
./main  -ngl 1 -m /models/llama2_7b_chat_uncensored.gguf.q2_K.bin -p "write a poem"

root@11fe149603ba:/app# ./main  -ngl 1 -m /models/llama2_7b_chat_uncensored.gguf.q2_K.bin -p "write a poem"
main: build = 0 (unknown)
main: seed  = 1692992765
ggml_init_cublas: found 1 ROCm devices:
  Device 0: AMD Radeon Graphics, compute capability 10.3
llama_model_loader: loaded meta data with 18 key-value pairs and 291 tensors from /models/llama2_7b_chat_uncensored.gguf.q2_K.bin (version GGUF V1 (latest))
llama_model_loader: - tensor    0:                token_embd.weight q2_K     [  4096, 32000,     1,     1 ]
llama_model_loader: - tensor    1:               output_norm.weight f32      [  4096,     1,     1,     1 ]
llama_model_loader: - tensor    2:                    output.weight q6_K     [  4096, 32000,     1,     1 ]
llama_model_loader: - tensor    3:              blk.0.attn_q.weight q2_K     [  4096,  4096,     1,     1 ]
llama_model_loader: - tensor    4:              blk.0.attn_k.weight q2_K     [  4096,  4096,     1,     1 ]
llama_model_loader: - tensor    5:              blk.0.attn_v.weight q4_K     [  4096,  4096,     1,     1 ]
llama_model_loader: - tensor    6:         blk.0.attn_output.weight q4_K     [  4096,  4096,     1,     1 ]
llama_model_loader: - tensor    7:           blk.0.attn_norm.weight f32      [  4096,     1,     1,     1 ]
...
llm_load_tensors: ggml ctx size =    0.09 MB
llm_load_tensors: using ROCm for GPU acceleration
llm_load_tensors: mem required  = 2652.72 MB (+  256.00 MB per state)
llm_load_tensors: offloading 1 repeating layers to GPU
llm_load_tensors: offloaded 1/35 layers to GPU
llm_load_tensors: VRAM used: 81 MB
.................................................................................................
llama_new_context_with_model: kv self size  =  256.00 MB
llama_new_context_with_model: compute buffer total size =   71.91 MB
llama_new_context_with_model: VRAM scratch buffer: 70.50 MB

system_info: n_threads = 8 / 16 | AVX = 1 | AVX2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | FMA = 1 | NEON = 0 | ARM_FMA = 0 | F16C = 1 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 1 | SSE3 = 1 | VSX = 0 | 
sampling: repeat_last_n = 64, repeat_penalty = 1.100000, presence_penalty = 0.000000, frequency_penalty = 0.000000, top_k = 40, tfs_z = 1.000000, top_p = 0.950000, typical_p = 1.000000, temp = 0.800000, mirostat = 0, mirostat_lr = 0.100000, mirostat_ent = 5.000000
generate: n_ctx = 512, n_batch = 512, n_predict = 400, n_keep = 0


Segmentation fault (core dumped)
```
