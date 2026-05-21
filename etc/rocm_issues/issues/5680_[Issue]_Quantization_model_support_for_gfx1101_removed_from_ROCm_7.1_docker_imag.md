# [Issue]: Quantization model support for gfx1101 removed from ROCm 7.1 docker image

> **Issue #5680**
> **状态**: closed
> **创建时间**: 2025-11-20T03:30:48Z
> **更新时间**: 2025-12-04T15:55:12Z
> **关闭时间**: 2025-12-04T15:55:12Z
> **作者**: tobing
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5680

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

I ran **AIDC-AI/Ovis2-8B-GPTQ-Int4** model with **rocm/vllm-dev:nightly_main_20251112** and no issue at all. 
Later I tried with **rocm/vllm-dev:nightly_main_20251117** and I got this error

**RuntimeError: Get GPU arch from rocminfo failed "Unknown GPU architecture: gfx1101. Supported architectures: ['native', 'gfx90a', 'gfx908', 'gfx940', 'gfx941', 'gfx942', 'gfx945', 'gfx1100', 'gfx950']"**

After I checked, seems the base image changed from ROCm 7.0 to ROCm 7.1. 
I built latest vLLM with different base images. After tested I can confirm this is related to ROCm not vLLM.
No issue with unquantized model **Qwen/Qwen3-VL-2B-Instruct**

Full logs
**rocm/vllm-dev:base**

```
vllm-ovis  | INFO 11-20 09:59:38 [scheduler.py:216] Chunked prefill is enabled with max_num_batched_tokens=2048.
vllm-ovis  | (APIServer pid=1) INFO 11-20 09:59:38 [api_server.py:1978] vLLM API server version 0.11.2.dev69+g3fb0d9099
vllm-ovis  | (APIServer pid=1) INFO 11-20 09:59:38 [utils.py:253] non-default args: {'host': '0.0.0.0', 'model': 'AIDC-AI/Ovis2-8B-GPTQ-Int4', 'trust_remote_code': True, 'dtype': 'float16', 'max_model_len': 8192, 'disable_cascade_attn': True, 'gpu_memory_utilization': 0.85, 'limit_mm_per_prompt': {'image': 1, 'video': 1, 'audio': 1}, 'max_num_batched_tokens': 8192, 'max_num_seqs': 5, 'enable_chunked_prefill': True, 'disable_log_stats': True}
vllm-ovis  | (APIServer pid=1) The argument `trust_remote_code` is to be used with Auto classes. It has no effect here and is ignored.
vllm-ovis  | (APIServer pid=1) INFO 11-20 09:59:47 [model.py:644] Resolved architecture: Ovis
vllm-ovis  | (APIServer pid=1) WARNING 11-20 09:59:47 [model.py:1995] Casting torch.bfloat16 to torch.float16.
vllm-ovis  | (APIServer pid=1) INFO 11-20 09:59:47 [model.py:1769] Using max model len 8192
vllm-ovis  | (APIServer pid=1) Traceback (most recent call last):
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/chip_info.py", line 63, in get_gfx_custom_op_core
vllm-ovis  | (APIServer pid=1)     return gfx_mapping[line.split(":")[-1].strip()]
vllm-ovis  | (APIServer pid=1)            ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1) KeyError: 'gfx1101'
vllm-ovis  | (APIServer pid=1) 
vllm-ovis  | (APIServer pid=1) During handling of the above exception, another exception occurred:
vllm-ovis  | (APIServer pid=1) 
vllm-ovis  | (APIServer pid=1) Traceback (most recent call last):
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/chip_info.py", line 65, in get_gfx_custom_op_core
vllm-ovis  | (APIServer pid=1)     raise KeyError(
vllm-ovis  | (APIServer pid=1) KeyError: "Unknown GPU architecture: gfx1101. Supported architectures: ['native', 'gfx90a', 'gfx908', 'gfx940', 'gfx941', 'gfx942', 'gfx945', 'gfx1100', 'gfx950']"
vllm-ovis  | (APIServer pid=1) 
vllm-ovis  | (APIServer pid=1) During handling of the above exception, another exception occurred:
vllm-ovis  | (APIServer pid=1) 
vllm-ovis  | (APIServer pid=1) Traceback (most recent call last):
vllm-ovis  | (APIServer pid=1)   File "<frozen runpy>", line 198, in _run_module_as_main
vllm-ovis  | (APIServer pid=1)   File "<frozen runpy>", line 88, in _run_code
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 2100, in <module>
vllm-ovis  | (APIServer pid=1)     uvloop.run(run_server(args))
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 96, in run
vllm-ovis  | (APIServer pid=1)     return __asyncio.run(
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 195, in run
vllm-ovis  | (APIServer pid=1)     return runner.run(main)
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
vllm-ovis  | (APIServer pid=1)     return self._loop.run_until_complete(task)
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 48, in wrapper
vllm-ovis  | (APIServer pid=1)     return await main
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 2028, in run_server
vllm-ovis  | (APIServer pid=1)     await run_server_worker(listen_address, sock, args, **uvicorn_kwargs)
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 2047, in run_server_worker
vllm-ovis  | (APIServer pid=1)     async with build_async_engine_client(
vllm-ovis  | (APIServer pid=1)                ^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
vllm-ovis  | (APIServer pid=1)     return await anext(self.gen)
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 196, in build_async_engine_client
vllm-ovis  | (APIServer pid=1)     async with build_async_engine_client_from_engine_args(
vllm-ovis  | (APIServer pid=1)                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
vllm-ovis  | (APIServer pid=1)     return await anext(self.gen)
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 222, in build_async_engine_client_from_engine_args
vllm-ovis  | (APIServer pid=1)     vllm_config = engine_args.create_engine_config(usage_context=usage_context)
vllm-ovis  | (APIServer pid=1)                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/arg_utils.py", line 1371, in create_engine_config
vllm-ovis  | (APIServer pid=1)     model_config = self.create_model_config()
vllm-ovis  | (APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/arg_utils.py", line 1226, in create_model_config
vllm-ovis  | (APIServer pid=1)     return ModelConfig(
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/pydantic/_internal/_dataclasses.py", line 121, in __init__
vllm-ovis  | (APIServer pid=1)     s.__pydantic_validator__.validate_python(ArgsKwargs(args, kwargs), self_instance=s)
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/config/model.py", line 728, in __post_init__
vllm-ovis  | (APIServer pid=1)     self._verify_quantization()
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/config/model.py", line 1035, in _verify_quantization
vllm-ovis  | (APIServer pid=1)     method = me_quant.get_quantization_config(name)
vllm-ovis  | (APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/quantization/__init__.py", line 102, in get_quantization_config
vllm-ovis  | (APIServer pid=1)     from vllm.model_executor.layers.quantization.quark.quark import QuarkConfig
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/quantization/quark/quark.py", line 25, in <module>
vllm-ovis  | (APIServer pid=1)     from vllm.model_executor.layers.quantization.quark.schemes import (
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/quantization/quark/schemes/__init__.py", line 4, in <module>
vllm-ovis  | (APIServer pid=1)     from .quark_ocp_mx import QuarkOCP_MX
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py", line 51, in <module>
vllm-ovis  | (APIServer pid=1)     from aiter.ops.shuffle import shuffle_weight
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/__init__.py", line 50, in <module>
vllm-ovis  | (APIServer pid=1)     from .jit import core as core
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/core.py", line 198, in <module>
vllm-ovis  | (APIServer pid=1)     gfx = get_gfx()
vllm-ovis  | (APIServer pid=1)           ^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/chip_info.py", line 85, in get_gfx
vllm-ovis  | (APIServer pid=1)     gfx_num = get_gfx_custom_op()
vllm-ovis  | (APIServer pid=1)               ^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/torch_guard.py", line 332, in wrapper_custom
vllm-ovis  | (APIServer pid=1)     else getattr(torch.ops.aiter, f"{loadName}")(
vllm-ovis  | (APIServer pid=1)          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/torch/_ops.py", line 1254, in __call__
vllm-ovis  | (APIServer pid=1)     return self._op(*args, **kwargs)
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/torch_guard.py", line 308, in outer_wrapper_dummy
vllm-ovis  | (APIServer pid=1)     else (torch.empty(1, device=device), wrapper(*args, **kwargs))
vllm-ovis  | (APIServer pid=1)                                          ^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/torch_guard.py", line 201, in wrapper
vllm-ovis  | (APIServer pid=1)     return func(*args, **kwargs)
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/chip_info.py", line 45, in get_gfx_custom_op
vllm-ovis  | (APIServer pid=1)     return get_gfx_custom_op_core()
vllm-ovis  | (APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^
vllm-ovis  | (APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/chip_info.py", line 71, in get_gfx_custom_op_core
vllm-ovis  | (APIServer pid=1)     raise RuntimeError(f"Get GPU arch from rocminfo failed {str(e)}")
vllm-ovis  | (APIServer pid=1) RuntimeError: Get GPU arch from rocminfo failed "Unknown GPU architecture: gfx1101. Supported architectures: ['native', 'gfx90a', 'gfx908', 'gfx940', 'gfx941', 'gfx942', 'gfx945', 'gfx1100', 'gfx950']"
vllm-ovis exited with code 1

``` 

**rocm/vllm-dev:base_custom_main_20251023**
```
vllm-ovis  | INFO 11-20 10:09:41 [scheduler.py:216] Chunked prefill is enabled with max_num_batched_tokens=2048.
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:09:41 [api_server.py:1978] vLLM API server version 0.11.2.dev69+g3fb0d9099
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:09:41 [utils.py:253] non-default args: {'host': '0.0.0.0', 'model': 'AIDC-AI/Ovis2-8B-GPTQ-Int4', 'trust_remote_code': True, 'dtype': 'float16', 'max_model_len': 8192, 'disable_cascade_attn': True, 'gpu_memory_utilization': 0.85, 'limit_mm_per_prompt': {'image': 1, 'video': 1, 'audio': 1}, 'max_num_batched_tokens': 8192, 'max_num_seqs': 5, 'enable_chunked_prefill': True, 'disable_log_stats': True}
vllm-ovis  | (APIServer pid=1) The argument `trust_remote_code` is to be used with Auto classes. It has no effect here and is ignored.
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:09:49 [model.py:644] Resolved architecture: Ovis
vllm-ovis  | (APIServer pid=1) WARNING 11-20 10:09:49 [model.py:1995] Casting torch.bfloat16 to torch.float16.
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:09:49 [model.py:1769] Using max model len 8192
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:09:51 [scheduler.py:216] Chunked prefill is enabled with max_num_batched_tokens=8192.
vllm-ovis  | (APIServer pid=1) WARNING 11-20 10:09:51 [gptq.py:99] Currently, the 4-bit gptq_gemm kernel for GPTQ is buggy. Please switch to gptq_marlin or gptq_bitblas.
Parse safetensors files: 100% 2/2 [00:01<00:00,  1.99it/s]
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:00 [core.py:93] Initializing a V1 LLM engine (v0.11.2.dev69+g3fb0d9099) with config: model='AIDC-AI/Ovis2-8B-GPTQ-Int4', speculative_config=None, tokenizer='AIDC-AI/Ovis2-8B-GPTQ-Int4', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.float16, max_seq_len=8192, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=gptq, enforce_eager=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=0, served_model_name=AIDC-AI/Ovis2-8B-GPTQ-Int4, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::kda_attention', 'vllm::sparse_attn_indexer'], 'compile_mm_encoder': False, 'use_inductor': None, 'compile_sizes': [], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {}, 'max_cudagraph_capture_size': 8, 'local_cache_dir': None}
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:03 [parallel_state.py:1217] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.19.0.2:35895 backend=nccl
vllm-ovis  | [Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
vllm-ovis  | [Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
vllm-ovis  | [Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
vllm-ovis  | [Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
vllm-ovis  | [Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
vllm-ovis  | [Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
vllm-ovis  | [Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:03 [parallel_state.py:1425] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank 0
vllm-ovis  | (EngineCore_DP0 pid=100) Using a slow image processor as `use_fast` is unset and a slow processor was saved with this model. `use_fast=True` will be the default behavior in v4.52, even if the model was saved with a slow processor. This will result in minor differences in outputs. You'll still be able to use a slow processor with `use_fast=False`.
vllm-ovis  | (EngineCore_DP0 pid=100) /usr/local/lib/python3.12/dist-packages/vllm/transformers_utils/processors/ovis.py:411: UserWarning: To copy construct from a tensor, it is recommended to use sourceTensor.detach().clone() or sourceTensor.detach().clone().requires_grad_(True), rather than torch.tensor(sourceTensor).
vllm-ovis  | (EngineCore_DP0 pid=100)   return torch.tensor(pixel_values), image_placeholders, torch.tensor(grid)
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:13 [gpu_model_runner.py:3279] Starting to load model AIDC-AI/Ovis2-8B-GPTQ-Int4...
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:14 [rocm.py:279] Using Triton Attention backend.
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:14 [layer.py:571] MultiHeadAttention attn_backend: AttentionBackendEnum.TORCH_SDPA, use_upstream_fa: False
Loading safetensors checkpoint shards: 100% 2/2 [00:05<00:00,  2.65s/it]
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:21 [default_loader.py:290] Loading weights took 5.48 seconds
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:21 [gpu_model_runner.py:3358] Model loading took 7.8926 GiB memory and 7.669449 seconds
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:21 [gpu_model_runner.py:4108] Encoder cache will be initialized with a budget of 8192 tokens, and profiled with 3 image items of the maximum feature size.
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:27 [backends.py:648] Using cache directory: /root/.cache/vllm/torch_compile_cache/fdb641a9aa/rank_0_0/backbone for vLLM's torch.compile
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:27 [backends.py:708] Dynamo bytecode transform time: 4.81 s
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:31 [backends.py:255] Cache the graph for dynamic shape for later use
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:40 [backends.py:286] Compiling a graph for dynamic shape takes 12.93 s
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:42 [monitor.py:34] torch.compile takes 17.74 s in total
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:45 [gpu_worker.py:360] Available KV cache memory: 0.79 GiB
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:45 [kv_cache_utils.py:1234] GPU KV cache size: 14,800 tokens
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:45 [kv_cache_utils.py:1239] Maximum concurrency for 8,192 tokens per request: 1.81x
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100% 4/4 [00:00<00:00, 30.34it/s]
Capturing CUDA graphs (decode, FULL): 100% 3/3 [00:01<00:00,  1.86it/s]
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:48 [gpu_model_runner.py:4264] Graph capturing finished in 2 secs, took 0.38 GiB
vllm-ovis  | (EngineCore_DP0 pid=100) INFO 11-20 10:10:48 [core.py:253] init engine (profile, create kv cache, warmup model) took 26.34 seconds
vllm-ovis  | (EngineCore_DP0 pid=100) /usr/local/lib/python3.12/dist-packages/vllm/transformers_utils/processors/ovis.py:411: UserWarning: To copy construct from a tensor, it is recommended to use sourceTensor.detach().clone() or sourceTensor.detach().clone().requires_grad_(True), rather than torch.tensor(sourceTensor).
vllm-ovis  | (EngineCore_DP0 pid=100)   return torch.tensor(pixel_values), image_placeholders, torch.tensor(grid)
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:50 [api_server.py:1726] Supported tasks: ['generate']
vllm-ovis  | (APIServer pid=1) WARNING 11-20 10:10:51 [model.py:1588] Default sampling parameters have been overridden by the model's Hugging Face generation config recommended from the model creator. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [serving_responses.py:154] Using default chat sampling params from model: {'repetition_penalty': 1.05, 'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [serving_chat.py:131] Using default chat sampling params from model: {'repetition_penalty': 1.05, 'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [serving_completion.py:73] Using default completion sampling params from model: {'repetition_penalty': 1.05, 'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [serving_chat.py:131] Using default chat sampling params from model: {'repetition_penalty': 1.05, 'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [api_server.py:2056] Starting vLLM API server 0 on http://0.0.0.0:8000
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:38] Available routes are:
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /openapi.json, Methods: GET, HEAD
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /docs, Methods: GET, HEAD
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /docs/oauth2-redirect, Methods: GET, HEAD
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /redoc, Methods: GET, HEAD
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /health, Methods: GET
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /load, Methods: GET
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /tokenize, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /detokenize, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/models, Methods: GET
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /version, Methods: GET
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/responses, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/responses/{response_id}, Methods: GET
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/responses/{response_id}/cancel, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/messages, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/chat/completions, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/completions, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/embeddings, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /pooling, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /classify, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /score, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/score, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/audio/transcriptions, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/audio/translations, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /rerank, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v1/rerank, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /v2/rerank, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /scale_elastic_ep, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /is_scaling_elastic_ep, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /ping, Methods: GET
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /ping, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /invocations, Methods: POST
vllm-ovis  | (APIServer pid=1) INFO 11-20 10:10:51 [launcher.py:46] Route: /metrics, Methods: GET
vllm-ovis  | (APIServer pid=1) INFO:     Started server process [1]
vllm-ovis  | (APIServer pid=1) INFO:     Waiting for application startup.
vllm-ovis  | (APIServer pid=1) INFO:     Application startup complete.

```



### Operating System

CachyOS Linux

### CPU

AMD Ryzen 7 5700X3D 8-Core Processor

### GPU

AMD Radeon RX 7800 XT

### ROCm Version

ROCm 7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — harkgill-amd (2025-11-20T20:52:36Z)

Hi @tobing, the error has to do with a lack of gfx1101 support with aiter. There wasn't support in the previous nightlies, the aiter code path just wasn't being exposed as it is in the new images. It now get's called into by `self._verify_quantization()`, which is why you only  see it with quantized models, and then specifically by `from aiter.ops.shuffle import shuffle_weight`. In theory, the environment variable `VLLM_ROCM_USE_AITER=0` should disable aiter completely but it practice, it still hits the `KeyError` - will look into this further.

For the time being, the simplest solution would be for you to use the Navi/gfx1101 specific vLLM docker image https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedrad/linux/vllm/build-docker-image.html#download-docker-image. This image omits the aiter installation completely. The second option would be to continue using the rocm/vllm-dev nightlies and manually uninstall aiter as it's not being used (essentially what the Navi image is doing amongst other changes).


---

### 评论 #2 — tobing (2025-11-20T23:59:14Z)

Hi @harkgill-amd 

As you mentioned the environment variable `VLLM_ROCM_USE_AITER=0` still hits the `KeyError`. Yes, I have tried it.
For now, I will use another option until the base image fixed. Thanks

---

### 评论 #3 — sstamenk (2025-11-27T10:59:22Z)

@tobing as a temporary workaround you can uninstall aiter with `pip uninstall aiter`

---

### 评论 #4 — tobing (2025-11-27T11:06:49Z)

@sstamenk yes. For temporary workaround I did that 

---

### 评论 #5 — harkgill-amd (2025-12-04T15:55:12Z)

Hey @tobing, https://github.com/ROCm/aiter/pull/1498 just got merged which will solve the `KeyError` failures on `gfx1101`. It might take a couple days for the changes to get picked up by the rocm/vllm-dev images. Will close this out for now but feel free to leave a comment if you see the issue going forward.

---
