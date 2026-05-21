# [Issue]: vLLM multi-node fails to start

> **Issue #5567**
> **状态**: closed
> **创建时间**: 2025-10-24T13:59:23Z
> **更新时间**: 2025-11-12T15:30:05Z
> **关闭时间**: 2025-10-29T18:23:45Z
> **作者**: rksawyer
> **标签**: ROCm 6.3.1, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5567

## 标签

- **ROCm 6.3.1** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

Cannot launch rocm vLLM as a ray cluster for multi-node distributed tensor parallelism or pipeline parallelism.

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD EPYC 9115 16-Core Processor

### GPU

AMD Radeon AI PRO R9700

### ROCm Version

6.3.1

### ROCm Component

_No response_

### Steps to Reproduce

### vLLM Distributed

Reference: https://docs.vllm.ai/en/v0.8.0/serving/distributed_serving.html#running-vllm-on-multiple-nodes 

1. Setup
  a. Download run_cluster.sh
```
wget https://raw.githubusercontent.com/vllm-project/vllm/refs/heads/main/examples/online_serving/run_cluster.sh
chmod +x run_cluster.sh
```
  b. Edit run_cluster.sh
    i. Remove the `--gpus all` where the script runs the container
  c. Create a conda environment and install ray
```
conda create -n vllm python=3.13
conda activate vllm
pip install -U "ray[default]"
```

2. Start the Ray cluster
Start the head node
```
./run_cluster.sh \
                rocm/vllm-dev:open-r9700-08052025 \
                10.20.1.126 \
                --head \
                /opt/huggingface \
                -e VLLM_HOST_IP=10.20.1.126 \
                --ipc=host \
				--device=/dev/kfd \
				--device=/dev/dri \
				--security-opt seccomp=unconfined \
				--group-add video \
				--shm-size 32G \
				-w /workspace
```
Start the worker node
```
./run_cluster.sh \
                rocm/vllm-dev:open-r9700-08052025 \
                10.20.1.126 \
                --worker \
                /opt/huggingface \
                -e VLLM_HOST_IP=10.20.1.125 \
                --ipc=host \
				--device=/dev/kfd \
				--device=/dev/dri \
				--security-opt seccomp=unconfined \
				--group-add video \
				--shm-size 32G \
				-w /workspace
```

3. Open a shell to the container and fix-up the python environment
```
docker exec -it node-25259 /bin/bash

pip install -U openai
pip install colorama
```

4. Check the ray status
```
# ray status
======== Autoscaler status: 2025-10-24 13:45:19.314803 ========
Node status
---------------------------------------------------------------
Active:
 1 node_431228bf8660e91ac26066f299dd5cc688a69e89f8454a1d8043e3a4
 1 node_39b0692786b5fadc8e0a1e2ab8e55df0c9165473be451456e97a7b35
Pending:
 (no pending nodes)
Recent failures:
 (no failures)

Resources
---------------------------------------------------------------
Usage:
 0.0/128.0 CPU
 0.0/2.0 GPU
 0B/351.66GiB memory
 0B/150.71GiB object_store_memory

Demands:
 (no resource demands)
```

5. Start vLLM serve from inside a container
```
docker exec -it node-25259 /bin/bash

NCCL_DEBUG=TRACEvllm serve Qwen/Qwen3-8B-FP8 --tensor-parallel 2
```

Error message

```
INFO 10-24 13:47:33 [__init__.py:235] Automatically detected platform rocm.

             LL          LL          MMM       MMM 
             LL          LL          MMMM     MMMM
         V   LL          LL          MM MM   MM MM
vvvv  VVVV   LL          LL          MM  MM MM  MM
vvvv VVVV    LL          LL          MM   MMM   MM
 vvv VVVV    LL          LL          MM    M    MM
  vvVVVV     LL          LL          MM         MM
    VVVV     LLLLLLLLLL  LLLLLLLLL   M           M

INFO 10-24 13:47:42 [api_server.py:1776] vLLM API server version 0.1.dev8023+g894bed8
INFO 10-24 13:47:42 [cli_args.py:264] non-default args: {'model_tag': 'Qwen/Qwen3-8B-FP8', 'model': 'Qwen/Qwen3-8B-FP8', 'tensor_parallel_size': 2}
INFO 10-24 13:47:53 [config.py:1605] Using max model len 40960
INFO 10-24 13:47:53 [config.py:2416] Chunked prefill is enabled with max_num_batched_tokens=2048.
INFO 10-24 13:47:56 [__init__.py:235] Automatically detected platform rocm.
INFO 10-24 13:48:03 [core.py:581] Waiting for init message from front-end.
INFO 10-24 13:48:03 [core.py:73] Initializing a V1 LLM engine (v0.1.dev8023+g894bed8) with config: model='Qwen/Qwen3-8B-FP8', speculative_config=None, tokenizer='Qwen/Qwen3-8B-FP8', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, override_neuron_config={}, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=40960, download_dir=None, load_format=auto, tensor_parallel_size=2, pipeline_parallel_size=1, disable_custom_all_reduce=True, quantization=fp8, enforce_eager=False, kv_cache_dtype=auto,  device_config=cuda, decoding_config=DecodingConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_backend=''), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=0, served_model_name=Qwen/Qwen3-8B-FP8, num_scheduler_steps=1, multi_step_stream_outputs=True, enable_prefix_caching=True, chunked_prefill_enabled=True, use_async_output_proc=True, pooler_config=None, compilation_config={"level":3,"debug_dump_path":"","cache_dir":"","backend":"","custom_ops":[],"splitting_ops":["vllm.unified_attention","vllm.unified_attention_with_output","vllm.mamba_mixer2"],"use_inductor":true,"compile_sizes":[],"inductor_compile_config":{"enable_auto_functionalized_v2":false},"inductor_passes":{},"use_cudagraph":true,"cudagraph_num_of_warmups":1,"cudagraph_capture_sizes":[512,504,496,488,480,472,464,456,448,440,432,424,416,408,400,392,384,376,368,360,352,344,336,328,320,312,304,296,288,280,272,264,256,248,240,232,224,216,208,200,192,184,176,168,160,152,144,136,128,120,112,104,96,88,80,72,64,56,48,40,32,24,16,8,4,2,1],"cudagraph_copy_inputs":false,"full_cuda_graph":false,"max_capture_size":512,"local_cache_dir":null}
WARNING 10-24 13:48:03 [multiproc_worker_utils.py:307] Reducing Torch parallelism from 32 threads to 1 to avoid unnecessary CPU contention. Set OMP_NUM_THREADS in the external environment to tune this value as needed.
INFO 10-24 13:48:03 [shm_broadcast.py:289] vLLM message queue communication handle: Handle(local_reader_ranks=[0, 1], buffer_handle=(2, 16777216, 10, 'psm_0d95fd4a'), local_subscribe_addr='ipc:///tmp/1ec8eae6-fe99-4789-a4c5-15255a88c0d6', remote_subscribe_addr=None, remote_addr_ipv6=False)
INFO 10-24 13:48:05 [__init__.py:235] Automatically detected platform rocm.
INFO 10-24 13:48:05 [__init__.py:235] Automatically detected platform rocm.
(VllmWorker rank=0 pid=838) INFO 10-24 13:48:14 [shm_broadcast.py:289] vLLM message queue communication handle: Handle(local_reader_ranks=[0], buffer_handle=(1, 10485760, 10, 'psm_8c43294e'), local_subscribe_addr='ipc:///tmp/005d9b75-b6e0-4f3c-aca5-21f0f6e59372', remote_subscribe_addr=None, remote_addr_ipv6=False)
(VllmWorker rank=1 pid=839) INFO 10-24 13:48:14 [shm_broadcast.py:289] vLLM message queue communication handle: Handle(local_reader_ranks=[0], buffer_handle=(1, 10485760, 10, 'psm_b8fd4178'), local_subscribe_addr='ipc:///tmp/2953ad71-f8a7-4cf9-8a76-0ff8d2779651', remote_subscribe_addr=None, remote_addr_ipv6=False)
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514] WorkerProc failed to start.
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514] Traceback (most recent call last):
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]   File "/app/vllm-os-mini/vllm/v1/executor/multiproc_executor.py", line 488, in worker_main
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]     worker = WorkerProc(*args, **kwargs)
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]   File "/app/vllm-os-mini/vllm/v1/executor/multiproc_executor.py", line 384, in __init__
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]     self.worker.init_device()
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]   File "/app/vllm-os-mini/vllm/worker/worker_base.py", line 603, in init_device
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]     self.worker.init_device()  # type: ignore
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]     ^^^^^^^^^^^^^^^^^^^^^^^^^
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]   File "/app/vllm-os-mini/vllm/v1/worker/gpu_worker.py", line 156, in init_device
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]     current_platform.set_device(self.device)
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]   File "/app/vllm-os-mini/vllm/platforms/rocm.py", line 252, in set_device
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]     torch.cuda.set_device(device)
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]   File "/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py", line 541, in set_device
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514]     torch._C._cuda_setDevice(device)
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514] torch.AcceleratorError: HIP error: invalid device ordinal
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514] HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514] For debugging consider passing AMD_SERIALIZE_KERNEL=3
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514] Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
(VllmWorker rank=1 pid=839) ERROR 10-24 13:48:14 [multiproc_executor.py:514] 
ERROR 10-24 13:48:16 [core.py:641] EngineCore failed to start.
ERROR 10-24 13:48:16 [core.py:641] Traceback (most recent call last):
ERROR 10-24 13:48:16 [core.py:641]   File "/app/vllm-os-mini/vllm/v1/engine/core.py", line 632, in run_engine_core
ERROR 10-24 13:48:16 [core.py:641]     engine_core = EngineCoreProc(*args, **kwargs)
ERROR 10-24 13:48:16 [core.py:641]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 10-24 13:48:16 [core.py:641]   File "/app/vllm-os-mini/vllm/v1/engine/core.py", line 450, in __init__
ERROR 10-24 13:48:16 [core.py:641]     super().__init__(vllm_config, executor_class, log_stats,
ERROR 10-24 13:48:16 [core.py:641]   File "/app/vllm-os-mini/vllm/v1/engine/core.py", line 79, in __init__
ERROR 10-24 13:48:16 [core.py:641]     self.model_executor = executor_class(vllm_config)
ERROR 10-24 13:48:16 [core.py:641]                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 10-24 13:48:16 [core.py:641]   File "/app/vllm-os-mini/vllm/executor/executor_base.py", line 53, in __init__
ERROR 10-24 13:48:16 [core.py:641]     self._init_executor()
ERROR 10-24 13:48:16 [core.py:641]   File "/app/vllm-os-mini/vllm/v1/executor/multiproc_executor.py", line 94, in _init_executor
ERROR 10-24 13:48:16 [core.py:641]     self.workers = WorkerProc.wait_for_ready(unready_workers)
ERROR 10-24 13:48:16 [core.py:641]                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ERROR 10-24 13:48:16 [core.py:641]   File "/app/vllm-os-mini/vllm/v1/executor/multiproc_executor.py", line 449, in wait_for_ready
ERROR 10-24 13:48:16 [core.py:641]     raise e from None
ERROR 10-24 13:48:16 [core.py:641] Exception: WorkerProc initialization failed due to an exception in a background process. See stack trace for root cause.
Process EngineCore_0:
Traceback (most recent call last):
  File "/usr/lib/python3.12/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib/python3.12/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/app/vllm-os-mini/vllm/v1/engine/core.py", line 645, in run_engine_core
    raise e
  File "/app/vllm-os-mini/vllm/v1/engine/core.py", line 632, in run_engine_core
    engine_core = EngineCoreProc(*args, **kwargs)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/v1/engine/core.py", line 450, in __init__
    super().__init__(vllm_config, executor_class, log_stats,
  File "/app/vllm-os-mini/vllm/v1/engine/core.py", line 79, in __init__
    self.model_executor = executor_class(vllm_config)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/executor/executor_base.py", line 53, in __init__
    self._init_executor()
  File "/app/vllm-os-mini/vllm/v1/executor/multiproc_executor.py", line 94, in _init_executor
    self.workers = WorkerProc.wait_for_ready(unready_workers)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/v1/executor/multiproc_executor.py", line 449, in wait_for_ready
    raise e from None
Exception: WorkerProc initialization failed due to an exception in a background process. See stack trace for root cause.
Traceback (most recent call last):
  File "/usr/local/bin/vllm", line 33, in <module>
    sys.exit(load_entry_point('vllm', 'console_scripts', 'vllm')())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/entrypoints/cli/main.py", line 54, in main
    args.dispatch_function(args)
  File "/app/vllm-os-mini/vllm/entrypoints/cli/serve.py", line 52, in cmd
    uvloop.run(run_server(args))
  File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 109, in run
    return __asyncio.run(
           ^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/usr/local/lib/python3.12/dist-packages/uvloop/__init__.py", line 61, in wrapper
    return await main
           ^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/entrypoints/openai/api_server.py", line 1812, in run_server
    await run_server_worker(listen_address, sock, args, **uvicorn_kwargs)
  File "/app/vllm-os-mini/vllm/entrypoints/openai/api_server.py", line 1832, in run_server_worker
    async with build_async_engine_client(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/entrypoints/openai/api_server.py", line 166, in build_async_engine_client
    async with build_async_engine_client_from_engine_args(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/entrypoints/openai/api_server.py", line 206, in build_async_engine_client_from_engine_args
    async_llm = AsyncLLM.from_vllm_config(
                ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/v1/engine/async_llm.py", line 164, in from_vllm_config
    return cls(
           ^^^^
  File "/app/vllm-os-mini/vllm/v1/engine/async_llm.py", line 118, in __init__
    self.engine_core = EngineCoreClient.make_async_mp_client(
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/v1/engine/core_client.py", line 99, in make_async_mp_client
    return AsyncMPClient(*client_args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm-os-mini/vllm/v1/engine/core_client.py", line 690, in __init__
    super().__init__(
  File "/app/vllm-os-mini/vllm/v1/engine/core_client.py", line 418, in __init__
    with launch_core_engines(vllm_config, executor_class,
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
    next(self.gen)
  File "/app/vllm-os-mini/vllm/v1/engine/utils.py", line 697, in launch_core_engines
    wait_for_engine_startup(
  File "/app/vllm-os-mini/vllm/v1/engine/utils.py", line 750, in wait_for_engine_startup
    raise RuntimeError("Engine core initialization failed. "
RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
```

### Troubleshooting

1. Test that vLLM starts on 1 workstation with 1 GPU
```
docker exec -it node-25259 /bin/bash

NCCL_DEBUG=TRACEvllm serve Qwen/Qwen3-8B-FP8 --tensor-parallel 1
```

```
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen3-8B-FP8",
        "prompt": "The future of AI is",
        "max_tokens": 100,
        "temperature": 0
}'
```



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:                    AMD EPYC 9115 16-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 9115 16-Core Processor    
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
  Max Clock Freq. (MHz):   4118                               
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
      Size:                    131621284(0x7d861a4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131621284(0x7d861a4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131621284(0x7d861a4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131621284(0x7d861a4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 9115 16-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 9115 16-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   4118                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
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
      Size:                    132012312(0x7de5918) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    132012312(0x7de5918) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132012312(0x7de5918) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132012312(0x7de5918) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-0d06b080997bb300               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L1:                      32(0x20) KB                        
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   1792                               
  Internal Node ID:        2                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 752                                
  SDMA engine uCode::      749                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33406976(0x1fdc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1201         
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
      Name:                    amdgcn-amd-amdhsa--gfx12-generic   
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
*** Done *** 
```

### Additional Information

Same results with these other docker images

- rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006
- rocm/vllm-dev:rocm7.0.2_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1

---

## 评论 (11 条)

### 评论 #1 — schung-amd (2025-10-27T22:19:20Z)

Hi @rksawyer, I'll try to repro this. Do all of your nodes have the same hardware configuration as listed?

e: Ok, I can repro this; checked with rocm/vllm:latest. Investigating.

---

### 评论 #2 — schung-amd (2025-10-27T23:55:23Z)

I think you have to add `--distributed_executor_backend="ray"` to the `vllm serve` command to specify that `vllm` should connect to the `ray` cluster. Please try that and see if it helps. 

On my local test systems with this option appended, the output shows connection to the ray cluster and distribution of the tensor parallelism among the nodes. I am running into a NCCL error though, but I didn't check beforehand to make sure the connection between my nodes was good and I haven't looked into that aspect yet. I'm curious to see if you run into the same problem.

---

### 评论 #3 — schung-amd (2025-10-28T15:51:32Z)

Ok, got this working; in addition to the above, I had to set NCCL_SOCKET_IFNAME and GLOO_SOCKET_IFNAME to the correct interfaces on both of my nodes (i.e. the ones corresponding to the IP addresses I was passing). I did this both in the shell before running the script and also inserted these into the ray start command in `run_cluster.py` as I wasn't sure if they would carry over into the container. I also set `--enforce-eager` as I was running into some memory issue with my test setup, I think that's just from me trying to use too large of a model and has nothing to do with ray/distributed inference though.

Give this a try and let me know if you run into any issues.

---

### 评论 #4 — rksawyer (2025-10-29T10:31:08Z)

Thank you so much for helping me out.

Yes, all of my nodes use the same hardware.

I modified the steps as you suggested.
- Added NCCL_SOCKET_IFNAME and GLOO_SOCKET_IFNAME to the run_cluster.sh docker environment variables
- Added `--enforce-eager` and `--distributed_executor_backend="ray"` to the `vllm serve` command

vLLM launches with these changes.  I also switched to the rocm/vllm:latest image.

However, I do not see any debug prints from RCCL.

This makes me suspect that it is using the GLOO backend instead of the RCCL backend.  Do you see that RCCL is being used in your setup?

--- 
Other notes:
Before adding the `--enforce-eager` parameter, I was seeing this error with `rocm/vllm:latest`:
`(EngineCore_DP0 pid=691) (RayWorkerWrapper pid=876) Memory access fault by GPU node-2 (Agent handle: 0x123afa90) on address 0x7a6b607ff000. Reason: Page not present or supervisor privilege.`


---

### 评论 #5 — schung-amd (2025-10-29T14:32:19Z)

You might be right, I had assumed RCCL was being used since I was running into NCCL errors before setting the SOCKET_IFNAMEs. I'm also seeing some Gloo outputs in the log.

> Other notes:

Was also seeing this. I'll look closer at it once we have everything else working.

e: I'm seeing:
```
(EngineCore_DP0 pid=1317) (RayWorkerWrapper pid=1493) INFO 10-29 15:10:49 [__init__.py:1382] Found nccl from library librccl.so.1
(EngineCore_DP0 pid=1317) (RayWorkerWrapper pid=1493) INFO 10-29 15:10:49 [pynccl.py:103] vLLM is using nccl==2.26.6
```
The NCCL_DEBUG environment variable doesn't seem to be providing debug output but I think it might not be propagating into the containers.

---

### 评论 #6 — schung-amd (2025-10-29T15:23:30Z)

Added NCCL_DEBUG=TRACE to the `ray` invocation in `run_cluster.sh` and now see NCCL debug output, so I think it is being used. Not sure why there is a Gloo connection message in the logs, might be something `ray` is doing behind the scenes to set up a fallback.

---

### 评论 #7 — schung-amd (2025-10-29T16:24:50Z)

Regarding the memory access fault with `--enforce-eager`, it looks like we've been seeing this in some of our vLLM containers as of last week. Currently checking to see if this issue is present in older images.

e: In limited testing, `rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909` seems to work without `--enforce-eager`; however, capturing the graph is extremely slow in my test configuration (both nodes have 1x 9070XT) so I would probably enable it anyway in practice.

---

### 评论 #8 — rksawyer (2025-10-29T17:55:15Z)

That was my issue, I needed to set the environment variable at the ray invocation.

I can see the RCCL logs and that it is picking a different network interface than expected.  Thanks so much for your help.

---

### 评论 #9 — schung-amd (2025-10-29T18:23:45Z)

Great, glad to hear that. I'll close this for now then as it sounds like things are working on your end, but if I've missed something or you're running into further issues please follow up here and we can reopen if necessary. Thanks for the report as well, that vLLM documentation doesn't seem to be giving correct instructions and we should look into getting it revised upstream.

---

### 评论 #10 — rksawyer (2025-11-12T13:31:47Z)

Adding a link to a new issue.  These steps are not working with the new rocm/vllm latest tag.

---

### 评论 #11 — schung-amd (2025-11-12T15:30:04Z)

Thanks, I'll take a look.

---
