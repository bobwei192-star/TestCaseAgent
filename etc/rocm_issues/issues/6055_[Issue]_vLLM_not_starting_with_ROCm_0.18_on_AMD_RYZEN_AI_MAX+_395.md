# [Issue]: vLLM not starting with ROCm  0.18 on AMD RYZEN AI MAX+ 395

> **Issue #6055**
> **状态**: closed
> **创建时间**: 2026-03-23T23:05:32Z
> **更新时间**: 2026-04-06T16:53:29Z
> **关闭时间**: 2026-04-06T16:53:29Z
> **作者**: JosefBraeuer
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6055

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

I am unable to start the docker container, the Engine core initialization fails. 

i tried qwen 3.5 35b and qwen 2.5 coder 7b, both as AWQ or GGUF
tried rcom/vllm-dev and vllm/vllm-openai-rocm containers. 
i only managed to get the 2.5 7b model running with a custom container i found in another issue here:
rocm/vllm-dev:rocm7.2_navi_ubuntu24.04_py3.12_pytorch_2.9_vllm_0.14.0rc0
without changing any other parameter
due to the old vllm version i cannot run the 35b moe model. 
the 7b model works with the older container on V1 and V0 (VLLM_USE_V1 = 0)



### Operating System

NAME="Ubuntu" VERSION="24.04.4 LTS (Noble Numbat)"

### CPU

model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S   Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S   Name:                    gfx1151   Marketing Name:          AMD Radeon Graphics       Name:                    amdgcn-amd-amdhsa--gfx1151       Name:                    amdgcn-amd-amdhsa--gfx11-generic

### ROCm Version

0.18.1rc1.dev27

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

(APIServer pid=1) INFO 03-23 22:45:59 [utils.py:297]
(APIServer pid=1) INFO 03-23 22:45:59 [utils.py:297]        █     █     █▄   ▄█
(APIServer pid=1) INFO 03-23 22:45:59 [utils.py:297]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.18.1rc1.dev27+g63f49b8bd
(APIServer pid=1) INFO 03-23 22:45:59 [utils.py:297]   █▄█▀ █     █     █     █  model   /models/AWQ/Qwen3.5-35B-A3B-AWQ
(APIServer pid=1) INFO 03-23 22:45:59 [utils.py:297]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=1) INFO 03-23 22:45:59 [utils.py:297]
(APIServer pid=1) INFO 03-23 22:45:59 [utils.py:233] non-default args: {'model': '/models/AWQ/Qwen3.5-35B-A3B-AWQ', 'trust_remote_code': True, 'dtype': 'half', 'max_model_len': 8192, 'quantization': 'awq', 'enforce_eager': True, 'distributed_executor_backend': 'mp', 'gpu_memory_utilization': 0.25}
(APIServer pid=1) The argument `trust_remote_code` is to be used with Auto classes. It has no effect here and is ignored.
(APIServer pid=1) WARNING 03-23 22:46:06 [gpt_oss_triton_kernels_moe.py:59] Using legacy triton_kernels on ROCm
(APIServer pid=1) INFO 03-23 22:46:06 [model.py:540] Resolved architecture: Qwen3_5MoeForConditionalGeneration
(APIServer pid=1) INFO 03-23 22:46:06 [model.py:1606] Using max model len 8192
(APIServer pid=1) [aiter] start build [module_aiter_enum] under /usr/local/lib/python3.12/dist-packages/aiter/jit/build/module_aiter_enum
(APIServer pid=1) [aiter] finish build [module_aiter_enum], cost 8.1s
(APIServer pid=1) [aiter] import [module_aiter_enum] under /usr/local/lib/python3.12/dist-packages/aiter/jit/module_aiter_enum.so
(APIServer pid=1) INFO 03-23 22:46:16 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=1) INFO 03-23 22:46:16 [config.py:228] Setting attention block size to 1056 tokens to ensure that attention page size is >= mamba page size.
(APIServer pid=1) INFO 03-23 22:46:16 [config.py:259] Padding mamba page size by 0.76% to ensure that mamba page size and attention page size are exactly equal.
(APIServer pid=1) INFO 03-23 22:46:16 [vllm.py:750] Asynchronous scheduling is enabled.
(APIServer pid=1) WARNING 03-23 22:46:16 [vllm.py:795] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
(APIServer pid=1) WARNING 03-23 22:46:16 [vllm.py:806] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
(APIServer pid=1) INFO 03-23 22:46:16 [vllm.py:971] Cudagraph is disabled under eager mode
(APIServer pid=1) INFO 03-23 22:46:16 [compilation.py:289] Enabled custom fusions: norm_quant, act_quant
(EngineCore pid=500) INFO 03-23 22:46:24 [core.py:105] Initializing a V1 LLM engine (v0.18.1rc1.dev27+g63f49b8bd) with config: model='/models/AWQ/Qwen3.5-35B-A3B-AWQ', speculative_config=None, tokenizer='/models/AWQ/Qwen3.5-35B-A3B-AWQ', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.float16, max_seq_len=8192, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=True, quantization=awq, enforce_eager=True, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=/models/AWQ/Qwen3.5-35B-A3B-AWQ, enable_prefix_caching=False, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.NONE: 0>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['+sparse_attn_indexer', 'all'], 'splitting_ops': [], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_endpoints': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.NONE: 0>, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': [], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 0, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
(EngineCore pid=500) WARNING 03-23 22:46:24 [multiproc_executor.py:1014] Reducing Torch parallelism from 32 threads to 1 to avoid unnecessary CPU contention. Set OMP_NUM_THREADS in the external environment to tune this value as needed.
(EngineCore pid=500) INFO 03-23 22:46:24 [multiproc_executor.py:134] DP group leader: node_rank=0, node_rank_within_dp=0, master_addr=127.0.0.1, mq_connect_ip=172.18.0.5 (local), world_size=1, local_world_size=1
WARNING 03-23 22:46:29 [gpt_oss_triton_kernels_moe.py:59] Using legacy triton_kernels on ROCm
(Worker pid=601) INFO 03-23 22:46:29 [parallel_state.py:1400] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://127.0.0.1:36821 backend=nccl
(Worker pid=601) INFO 03-23 22:46:29 [parallel_state.py:1716] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank 0, EPLB rank N/A
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108] EngineCore failed to start.
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108] Traceback (most recent call last):
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1082, in run_engine_core
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     engine_core = EngineCoreProc(*args, engine_index=dp_rank, **kwargs)
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     return func(*args, **kwargs)
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 848, in __init__
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     super().__init__(
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 114, in __init__
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     self.model_executor = executor_class(vllm_config)
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/multiproc_executor.py", line 101, in __init__
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     super().__init__(vllm_config)
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     return func(*args, **kwargs)
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/abstract.py", line 103, in __init__
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     self._init_executor()
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/multiproc_executor.py", line 190, in _init_executor
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     self.workers = WorkerProc.wait_for_ready(unready_workers)
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/multiproc_executor.py", line 736, in wait_for_ready
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108]     raise e from None
(EngineCore pid=500) ERROR 03-23 22:46:30 [core.py:1108] Exception: WorkerProc initialization failed due to an exception in a background process. See stack trace for root cause.
(EngineCore pid=500) Process EngineCore:
(EngineCore pid=500) Traceback (most recent call last):
(EngineCore pid=500)   File "/usr/lib/python3.12/multiprocessing/process.py", line 314, in _bootstrap
(EngineCore pid=500)     self.run()
(EngineCore pid=500)   File "/usr/lib/python3.12/multiprocessing/process.py", line 108, in run
(EngineCore pid=500)     self._target(*self._args, **self._kwargs)
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1112, in run_engine_core
(EngineCore pid=500)     raise e
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 1082, in run_engine_core
(EngineCore pid=500)     engine_core = EngineCoreProc(*args, engine_index=dp_rank, **kwargs)
(EngineCore pid=500)                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
(EngineCore pid=500)     return func(*args, **kwargs)
(EngineCore pid=500)            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 848, in __init__
(EngineCore pid=500)     super().__init__(
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core.py", line 114, in __init__
(EngineCore pid=500)     self.model_executor = executor_class(vllm_config)
(EngineCore pid=500)                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/multiproc_executor.py", line 101, in __init__
(EngineCore pid=500)     super().__init__(vllm_config)
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
(EngineCore pid=500)     return func(*args, **kwargs)
(EngineCore pid=500)            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/abstract.py", line 103, in __init__
(EngineCore pid=500)     self._init_executor()
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/multiproc_executor.py", line 190, in _init_executor
(EngineCore pid=500)     self.workers = WorkerProc.wait_for_ready(unready_workers)
(EngineCore pid=500)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=500)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/executor/multiproc_executor.py", line 736, in wait_for_ready
(EngineCore pid=500)     raise e from None
(EngineCore pid=500) Exception: WorkerProc initialization failed due to an exception in a background process. See stack trace for root cause.
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "<frozen runpy>", line 198, in _run_module_as_main
(APIServer pid=1)   File "<frozen runpy>", line 88, in _run_code
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 710, in <module>
(APIServer pid=1)     uvloop.run(run_server(args))
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 96, in run
(APIServer pid=1)     return __asyncio.run(
(APIServer pid=1)            ^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 195, in run
(APIServer pid=1)     return runner.run(main)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
(APIServer pid=1)     return self._loop.run_until_complete(task)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 48, in wrapper
(APIServer pid=1)     return await main
(APIServer pid=1)            ^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 670, in run_server
(APIServer pid=1)     await run_server_worker(listen_address, sock, args, **uvicorn_kwargs)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 684, in run_server_worker
(APIServer pid=1)     async with build_async_engine_client(
(APIServer pid=1)                ^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
(APIServer pid=1)     return await anext(self.gen)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 100, in build_async_engine_client
(APIServer pid=1)     async with build_async_engine_client_from_engine_args(
(APIServer pid=1)                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
(APIServer pid=1)     return await anext(self.gen)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/api_server.py", line 136, in build_async_engine_client_from_engine_args
(APIServer pid=1)     async_llm = AsyncLLM.from_vllm_config(
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 225, in from_vllm_config
(APIServer pid=1)     return cls(
(APIServer pid=1)            ^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/async_llm.py", line 154, in __init__
(APIServer pid=1)     self.engine_core = EngineCoreClient.make_async_mp_client(
(APIServer pid=1)                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
(APIServer pid=1)     return func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 130, in make_async_mp_client
(APIServer pid=1)     return AsyncMPClient(*client_args)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/tracing/otel.py", line 178, in sync_wrapper
(APIServer pid=1)     return func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 887, in __init__
(APIServer pid=1)     super().__init__(
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/core_client.py", line 535, in __init__
(APIServer pid=1)     with launch_core_engines(
(APIServer pid=1)          ^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
(APIServer pid=1)     next(self.gen)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 998, in launch_core_engines
(APIServer pid=1)     wait_for_engine_startup(
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/v1/engine/utils.py", line 1057, in wait_for_engine_startup
(APIServer pid=1)     raise RuntimeError(
(APIServer pid=1) RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}



---

## 评论 (2 条)

### 评论 #1 — tcgu-amd (2026-03-27T19:58:28Z)

Hi @JosefBraeuer, thanks for reaching out! The log doesn't really say why the initialization failed, but something wasn't right in the background worker process. Can you use rocm-smi and monitor the GPU vmem status, just in case the problem is with loading the model into the memory? Setting HIP_LAUNCH_BLOCKING=1 VLLM_LOG_LEVEL=DEBUG should also be helpful showing what the error in the worker process is. Thanks!


---

### 评论 #2 — tcgu-amd (2026-04-06T16:53:29Z)

Hi, I will be closing this issue since there's been no response and no similar reports indicating a problem. Please feel free to follow up with any other questions. Thanks! 

---
