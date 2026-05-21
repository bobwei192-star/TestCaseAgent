# [Issue]: vLLM multi-node fails to start Radeon R9700

> **Issue #5656**
> **状态**: closed
> **创建时间**: 2025-11-12T13:30:51Z
> **更新时间**: 2026-04-01T15:20:04Z
> **关闭时间**: 2026-04-01T15:20:04Z
> **作者**: rksawyer
> **标签**: AMD Radeon AI PRO R9700, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5656

## 标签

- **AMD Radeon AI PRO R9700** (颜色: #007c97)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

Distributed vLLM was working with the flags as discussed in this previous ticket: https://github.com/ROCm/ROCm/issues/5567

The `rocm/vllm:latest` image ID `fdb0ad05db4b` fails with the error described in the steps to reproduce.

Previously, these steps worked with `rocm/vllm:rocm7.0.0_vllm_0.10.2_20251006` Image ID `beeea916d4a4`

The two systems in this test have the same hardware.

### Operating System

24.04.3 LTS (Noble Numbat)

### CPU

AMD EPYC 9115 16-Core Processor

### GPU

AMD Radeon AI PRO R9700 

### ROCm Version

ROCm 7.0

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
                rocm/vllm:latest \
                10.20.1.126 \
                --head \
                /opt/huggingface \
                -e VLLM_HOST_IP=10.20.1.126 \
                -e NCCL_SOCKET_IFNAME=enp165s0f1np1 \
                -e GLOO_SOCKET_IFNAME=enp165s0f1np1 \
                -e NCCL_DEBUG=TRACE \
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
                rocm/vllm:latest \
                10.20.1.126 \
                --worker \
                /opt/huggingface \
                -e VLLM_HOST_IP=10.20.1.125 \
                -e NCCL_SOCKET_IFNAME=enp165s0f1np1 \
                -e GLOO_SOCKET_IFNAME=enp165s0f1np1 \
                -e NCCL_DEBUG=TRACE \
                --ipc=host \
				--device=/dev/kfd \
				--device=/dev/dri \
				--security-opt seccomp=unconfined \
				--group-add video \
				--shm-size 32G \
				-w /workspace
```

4. Check the ray status
```
# ray status
======== Autoscaler status: 2025-11-12 13:23:16.804602 ========
Node status
---------------------------------------------------------------
Active:
 1 node_35afdf3ae762c5562e26215333773093338dabcd47b9f5ae4d1081b0
 1 node_104ceb8ab69f5a9e0339138fd49a4152e58b48bbbc7e0998853aebe5
Pending:
 (no pending nodes)
Recent failures:
 (no failures)

Resources
---------------------------------------------------------------
Total Usage:
 0.0/128.0 CPU
 0.0/2.0 GPU
 0B/351.65GiB memory
 0B/150.71GiB object_store_memory

From request_resources:
 (none)
Pending Demands:
 (no resource demands)
```

5. Start vLLM serve from inside a container
```
docker exec -it node-25259 /bin/bash

vllm serve openai/gpt-oss-20b --enforce-eager --tensor-parallel 2 --distributed_executor_backend="ray"
```

Error message
```
INFO 11-12 11:11:28 [__init__.py:225] Automatically detected platform rocm.
(APIServer pid=445) INFO 11-12 11:11:32 [api_server.py:1876] vLLM API server version 0.11.1rc2.dev141+g38f225c2a
(APIServer pid=445) INFO 11-12 11:11:32 [utils.py:243] non-default args: {'model_tag': 'openai/gpt-oss-20b', 'model': 'openai/gpt-oss-20b', 'enforce_eager': True, 'distributed_executor_backend': 'ray', 'tensor_parallel_size': 2}
(APIServer pid=445) INFO 11-12 11:11:39 [model.py:658] Resolved architecture: GptOssForCausalLM
Parse safetensors files: 
[00:02<00:00,  1.06it/s]
(APIServer pid=445) INFO 11-12 11:11:42 [model.py:1745] Using max model len 131072
(APIServer pid=445) INFO 11-12 11:11:43 [scheduler.py:225] Chunked prefill is enabled with max_num_batched_tokens=2048.
(APIServer pid=445) INFO 11-12 11:11:43 [config.py:273] Overriding max cuda graph capture size to 992 for performance.
(APIServer pid=445) INFO 11-12 11:11:43 [vllm.py:375] Cudagraph is disabled under eager mode
INFO 11-12 11:11:45 [__init__.py:225] Automatically detected platform rocm.
(EngineCore_DP0 pid=742) INFO 11-12 11:11:48 [core.py:730] Waiting for init message from front-end.
(EngineCore_DP0 pid=742) INFO 11-12 11:11:48 [core.py:97] Initializing a V1 LLM engine (v0.11.1rc2.dev141+g38f225c2a) with config: model='openai/gpt-oss-20b', speculative_config=None, tokenizer='openai/gpt-oss-20b', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=131072, download_dir=None, load_format=auto, tensor_parallel_size=2, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=mxfp4, enforce_eager=True, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='openai_gptoss'), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=0, served_model_name=openai/gpt-oss-20b, enable_prefix_caching=True, chunked_prefill_enabled=True, pooler_config=None, compilation_config={'level': None, 'mode': 0, 'debug_dump_path': None, 'cache_dir': '', 'backend': 'inductor', 'custom_ops': ['+rms_norm', '+silu_and_mul', '+quant_fp8', 'all', '+rms_norm'], 'splitting_ops': None, 'use_inductor': None, 'compile_sizes': [], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.NONE: 0>, 'use_cudagraph': False, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': [], 'cudagraph_copy_inputs': False, 'full_cuda_graph': False, 'use_inductor_graph_partition': False, 'pass_config': {}, 'max_capture_size': 0, 'local_cache_dir': None}
(EngineCore_DP0 pid=742) 2025-11-12 11:11:48,752	INFO worker.py:1833 -- Connecting to existing Ray cluster at address: 10.20.1.126:6379...
(EngineCore_DP0 pid=742) 2025-11-12 11:11:48,762	INFO worker.py:2013 -- Connected to Ray cluster.
(EngineCore_DP0 pid=742) /usr/local/lib/python3.12/dist-packages/ray/_private/worker.py:2052: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
(EngineCore_DP0 pid=742)   warnings.warn(
(EngineCore_DP0 pid=742) INFO 11-12 11:11:49 [ray_utils.py:378] No current placement group found. Creating a new placement group.
(EngineCore_DP0 pid=742) WARNING 11-12 11:11:49 [ray_utils.py:227] tensor_parallel_size=2 is bigger than a reserved number of GPUs (1 GPUs) in a node 105bc4e57711c6d8124de9ca4ea66c94df13653ce39ff1f0179e31c3. Tensor parallel workers can be spread out to 2+ nodes which can degrade the performance unless you have fast interconnect across nodes, like Infiniband. To resolve this issue, make sure you have more than 2 GPUs available at each node.
(EngineCore_DP0 pid=742) WARNING 11-12 11:11:49 [ray_utils.py:227] tensor_parallel_size=2 is bigger than a reserved number of GPUs (1 GPUs) in a node ead2c3ac59a39ba02e4fcabc212b72c1eab038705586247e7fb5bda7. Tensor parallel workers can be spread out to 2+ nodes which can degrade the performance unless you have fast interconnect across nodes, like Infiniband. To resolve this issue, make sure you have more than 2 GPUs available at each node.
(EngineCore_DP0 pid=742) INFO 11-12 11:11:49 [ray_distributed_executor.py:179] use_ray_spmd_worker: True
(EngineCore_DP0 pid=742) (pid=927) INFO 11-12 11:11:50 [__init__.py:225] Automatically detected platform rocm.
(EngineCore_DP0 pid=742) INFO 11-12 11:11:56 [ray_env.py:66] RAY_NON_CARRY_OVER_ENV_VARS from config: set()
(EngineCore_DP0 pid=742) INFO 11-12 11:11:56 [ray_env.py:69] Copying the following environment variables to workers: ['VLLM_USE_RAY_COMPILED_DAG', 'VLLM_USE_V1', 'LD_LIBRARY_PATH', 'VLLM_WORKER_MULTIPROC_METHOD', 'VLLM_USE_RAY_SPMD_WORKER']
(EngineCore_DP0 pid=742) INFO 11-12 11:11:56 [ray_env.py:74] If certain env vars should NOT be copied, add them to /root/.config/vllm/ray_non_carry_over_env_vars.json file
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) WARNING 11-12 11:11:56 [worker_base.py:309] Missing `shared_worker_lock` argument from executor. This argument is needed for mm_processor_cache_type='shm'.
(EngineCore_DP0 pid=742) (pid=233, ip=10.20.1.125) INFO 11-12 11:11:51 [__init__.py:225] Automatically detected platform rocm.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) [Gloo] Rank 0 is connected to 1 peer ranks. Expected number of connected peer ranks is : 1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) INFO 11-12 11:11:57 [pynccl.py:111] vLLM is using nccl==2.26.6
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) [2025-11-12 11:11:57] corona:927:927 [0] /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/out/ubuntu-22.04/22.04/build/rccl/hipify/src/init.cc:140 NCCL WARN NUMA auto balancing enabled which can lead to variability in the RCCL performance! Disable by "sudo sysctl kernel.numa_balancing=0"
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Kernel version: 6.14.0-35-generic
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO NCCL_SOCKET_IFNAME set by environment to enp165s0f1np1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Bootstrap: Using enp165s0f1np1:10.20.1.126<0>
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO ROCr version 1.18
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Dmabuf feature disabled without NCCL_DMABUF_ENABLE=1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) [2025-11-12 11:11:57] corona:927:927 [0] /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/out/ubuntu-22.04/22.04/build/rccl/hipify/src/init.cc:140 NCCL WARN NUMA auto balancing enabled which can lead to variability in the RCCL performance! Disable by "sudo sysctl kernel.numa_balancing=0"
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Kernel version: 6.14.0-35-generic
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO RCCL version : 2.26.6-HEAD:f224e2c
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) HIP version  : 7.0.51831-a3e329ad8
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) ROCm version : 7.0.0.0-38-9428210
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) Hostname     : corona
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) Librccl path : /opt/rocm/lib/librccl.so.1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO NET/Plugin: Could not find: librccl-net.so. Using internal net plugin.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Failed to open libibverbs.so[.1]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO NCCL_SOCKET_IFNAME set by environment to enp165s0f1np1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO NET/Socket : Using [0]enp165s0f1np1:10.20.1.126<0>
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO PROFILER/Plugin: Could not find: librccl-profiler.so. 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Using network Socket
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO [node_id = 2; gpu_id = 28209; unique_id = 938631638730650368; location_id = 1792; bdf = 1792; domain = 0; partition = 0], 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO initialized internal alternative rsmi functionality
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO ncclCommInitRank_impl comm 0x2083dd50 rank 0 nranks 2 cudaDev 0 nvmlDev 0 busId 7000 commId 0x9110735f21e7cb02 - Init START
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO RAS client listening socket at 127.0.0.1<28028>
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Bootstrap timings total 0.059598 (create 0.000043, send 0.000099, recv 0.039276, ring 0.019702, delay 0.000001)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO initialized internal alternative rsmi functionality
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Setting affinity for GPU 0 to ffff,0000ffff
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO comm 0x2083dd50 rank 0 nRanks 2 nNodes 2 localRanks 1 localRank 0 MNNVL 0
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Channel 00/02 : 0 1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Channel 01/02 : 0 1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Trees [0] 1/-1/-1->0->-1 [1] -1/-1/-1->0->1 comm 0x2083dd50 nRanks 02 busId 7000
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO P2P Chunksize set to 131072
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Check P2P Type intraNodeP2pSupport 0 directMode 0
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:4796 [0] NCCL INFO [Proxy Service] Device 0 CPU core 42
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:4797 [0] NCCL INFO [Proxy Service UDS] Device 0 CPU core 2
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:4798 [0] NCCL INFO [Proxy Progress] Device 0 CPU core 42
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Channel 00/0 : 1[0] -> 0[0] [receive] via NET/Socket/0 comm 0x2083dd50 nRanks 02
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Channel 01/0 : 1[0] -> 0[0] [receive] via NET/Socket/0 comm 0x2083dd50 nRanks 02
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Channel 00/0 : 0[0] -> 1[0] [send] via NET/Socket/0 comm 0x2083dd50 nRanks 02
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Channel 01/0 : 0[0] -> 1[0] [send] via NET/Socket/0 comm 0x2083dd50 nRanks 02
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Connected all rings, use ring PXN 0 GDR 0
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Connected all trees
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Connected binomial trees
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO threadThresholds 8/8/64 | 16/8/64 | 256 | 256
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO 2 coll channels, 2 collnet channels, 0 nvls channels, 2 p2p channels, 2 p2p channels per peer
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO CC Off, workFifoBytes 4194304
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO RCCL Unroll Factor (pre-set): 4
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL IINFO 11-12 11:12:00 [shm_broadcast.py:313] vLLM message queue communication handle: Handle(local_reader_ranks=[], buffer_handle=None, local_subscribe_addr=None, remote_subscribe_addr='tcp://10.20.1.126:36983', remote_addr_ipv6=False)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) NFO TUNER/Plugin: Could not find: librccl-tuner.so. Using internal tuner plugin.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO ncclCommInitRank_impl comm 0x2083dd50 rank 0 nranks 2 cudaDev 0 nvmlDev 0 busId 7000 commId 0x9110735f21e7cb02 - Init COMPLETE
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) corona:927:927 [0] NCCL INFO Init timings - ncclCommInitRank_impl: rank 0 nranks 2 total 3.18 (kernels 2.81, alloc 0.26, bootstrap 0.06, allgathers 0.00, topo 0.04, graphs 0.00, connections 0.01, rest 0.00)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) INFO 11-12 11:12:00 [pynccl.py:111] vLLM is using nccl==2.26.6
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) Hostname     : bootes
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO TUNER/Plugin: Could not find: librccl-tuner.so. Using internal tuner plugin.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) INFO 11-12 11:12:00 [parallel_state.py:1325] rank 0 in world size 2 is assigned as DP rank 0, PP rank 0, TP rank 0, EP rank 0
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) INFO 11-12 11:12:00 [gpu_model_runner.py:2843] Starting to load model openai/gpt-oss-20b...
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) INFO 11-12 11:12:01 [rocm.py:298] Using Rocm Attention backend on V1 engine.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) INFO 11-12 11:12:01 [mxfp4.py:131] Using Triton backend
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) WARNING 11-12 11:12:01 [compilation.py:874] Op 'silu_and_mul' not present in model, enabling with '+silu_and_mul' has no effect
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) WARNING 11-12 11:12:01 [compilation.py:874] Op 'quant_fp8' not present in model, enabling with '+quant_fp8' has no effect
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) INFO 11-12 11:12:01 [weight_utils.py:419] Using model weights format ['*.safetensors']
Loading safetensors checkpoint shards:   0% Completed | 0/3 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:  33% Completed | 1/3 [00:03<00:06,  3.06s/it]
Loading safetensors checkpoint shards:  67% Completed | 2/3 [00:06<00:03,  3.19s/it]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) INFO 11-12 11:12:10 [default_loader.py:314] Loading weights took 8.59 seconds
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) WARNING 11-12 11:11:57 [worker_base.py:309] Missing `shared_worker_lock` argument from executor. This argument is needed for mm_processor_cache_type='shm'.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [Gloo] Rank 1 is connected to 1 peer ranks. Expected number of connected peer ranks is : 1 [repeated 11x across cluster] (Ray deduplicates logs by default. Set RAY_DEDUP_LOGS=0 to disable log deduplication, or see https://docs.ray.io/en/master/ray-observability/user-guides/configure-logging.html#log-deduplication for more options.)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:11:57] bootes:233:233 [0] /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/out/ubuntu-22.04/22.04/build/rccl/hipify/src/init.cc:140 NCCL WARN NUMA auto balancing enabled which can lead to variability in the RCCL performance! Disable by "sudo sysctl kernel.numa_balancing=0"
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Kernel version: 6.14.0-35-generic
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO NCCL_SOCKET_IFNAME set by environment to enp165s0f1np1 [repeated 2x across cluster]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Bootstrap: Using enp165s0f1np1:10.20.1.125<0>
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO ROCr version 1.18
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Dmabuf feature disabled without NCCL_DMABUF_ENABLE=1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO RCCL version : 2.26.6-HEAD:f224e2c
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) HIP version  : 7.0.51831-a3e329ad8
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) ROCm version : 7.0.0.0-38-9428210
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) Librccl path : /opt/rocm/lib/librccl.so.1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO NET/Plugin: Could not find: librccl-net.so. Using internal net plugin.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Failed to open libibverbs.so[.1]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO NET/Socket : Using [0]enp165s0f1np1:10.20.1.125<0>
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO PROFILER/Plugin: Could not find: librccl-profiler.so. 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Using network Socket
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO [node_id = 2; gpu_id = 28209; unique_id = 5818553147422564044; location_id = 1792; bdf = 1792; domain = 0; partition = 0], 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO initialized internal alternative rsmi functionality [repeated 2x across cluster]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO ncclCommInitRank_impl comm 0x3ef16db0 rank 1 nranks 2 cudaDev 0 nvmlDev 0 busId 7000 commId 0x9110735f21e7cb02 - Init START
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO RAS client listening socket at 127.0.0.1<28028>
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Bootstrap timings total 0.021221 (create 0.000055, send 0.000246, recv 0.000305, ring 0.000056, delay 0.000001)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Setting affinity for GPU 0 to ffff,0000ffff
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO comm 0x3ef16db0 rank 1 nRanks 2 nNodes 2 localRanks 1 localRank 0 MNNVL 0
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Trees [0] -1/-1/-1->1->0 [1] 0/-1/-1->1->-1 comm 0x3ef16db0 nRanks 02 busId 7000
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO P2P Chunksize set to 131072
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:340 [0] NCCL INFO [Proxy Service] Device 0 CPU core 36
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:341 [0] NCCL INFO [Proxy Service UDS] Device 0 CPU core 10
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:342 [0] NCCL INFO [Proxy Progress] Device 0 CPU core 38
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Channel 01/0 : 0[0] -> 1[0] [receive] via NET/Socket/0 comm 0x3ef16db0 nRanks 02 [repeated 2x across cluster]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Channel 01/0 : 1[0] -> 0[0] [send] via NET/Socket/0 comm 0x3ef16db0 nRanks 02 [repeated 2x across cluster]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Connected all rings, use ring PXN 0 GDR 0
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Connected all trees
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Connected binomial trees
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO threadThresholds 8/8/64 | 16/8/64 | 256 | 256
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO 2 coll channels, 2 collnet channels, 0 nvls channels, 2 p2p channels, 2 p2p channels per peer
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO RCCL Unroll Factor (pre-set): 4
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO ncclCommInitRank_impl comm 0x3ef16db0 rank 1 nranks 2 cudaDev 0 nvmlDev 0 busId 7000 commId 0x9110735f21e7cb02 - Init COMPLETE
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) bootes:233:233 [0] NCCL INFO Init timings - ncclCommInitRank_impl: rank 1 nranks 2 total 3.18 (kernels 2.85, alloc 0.25, bootstrap 0.02, allgathers 0.00, topo 0.04, graphs 0.00, connections 0.01, rest 0.00)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) INFO 11-12 11:12:00 [parallel_state.py:1325] rank 1 in world size 2 is assigned as DP rank 0, PP rank 0, TP rank 1, EP rank 1
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) INFO 11-12 11:12:00 [gpu_model_runner.py:2843] Starting to load model openai/gpt-oss-20b...
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) INFO 11-12 11:12:01 [rocm.py:298] Using Rocm Attention backend on V1 engine.
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) INFO 11-12 11:12:01 [mxfp4.py:131] Using Triton backend
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) WARNING 11-12 11:12:01 [compilation.py:874] Op 'silu_and_mul' not present in model, enabling with '+silu_and_mul' has no effect
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) WARNING 11-12 11:12:01 [compilation.py:874] Op 'quant_fp8' not present in model, enabling with '+quant_fp8' has no effect
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) INFO 11-12 11:12:01 [weight_utils.py:419] Using model weights format ['*.safetensors']
Loading safetensors checkpoint shards: 100% Completed | 3/3 [00:08<00:00,  2.89s/it]
Loading safetensors checkpoint shards: 100% Completed | 3/3 [00:08<00:00,  2.96s/it]
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=927) 
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) INFO 11-12 11:12:10 [gpu_model_runner.py:2904] Model loading took 7.2637 GiB and 9.390913 seconds
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [aiter] type hints mismatch, override to --> rmsnorm2d_fwd(input: torch.Tensor, weight: torch.Tensor, epsilon: float, use_model_sensitive_rmsnorm: int = 0) -> torch.Tensor
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17] WARNING core.py:622: type hints mismatch, override to --> rmsnorm2d_fwd(input: torch.Tensor, weight: torch.Tensor, epsilon: float, use_model_sensitive_rmsnorm: int = 0) -> torch.Tensor
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) *** SIGSEGV received at time=1762945937 on cpu 6 ***
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) PC: @     0x71bd29eb3ab5  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71d139f9e520  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd07e0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd07d8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd07d0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd07c8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0710  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0708       1472  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0718  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0700  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd04c0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd04b8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0408  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0400  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd03f8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd03f0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd03e8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd03e0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd03d8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd03d0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0318  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0310       3024  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0308  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0300  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd02f8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd02f0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd02e8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0320  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd02e0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0230       6944  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0228  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0220  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @     0x71bb1bfd0218  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125)     @ ... and at least 1000 more frames
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,145 E 233 233] logging.cc:474: *** SIGSEGV received at time=1762945937 on cpu 6 ***
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,146 E 233 233] logging.cc:474: PC: @     0x71bd29eb3ab5  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,146 E 233 233] logging.cc:474:     @     0x71d139f9e520  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,147 E 233 233] logging.cc:474:     @     0x71bb1bfd07e0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,149 E 233 233] logging.cc:474:     @     0x71bb1bfd07d8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,150 E 233 233] logging.cc:474:     @     0x71bb1bfd07d0  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,152 E 233 233] logging.cc:474:     @     0x71bb1bfd07c8  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,154 E 233 233] logging.cc:474:     @     0x71bb1bfd0710  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,156 E 233 233] logging.cc:474:     @     0x71bb1bfd0708       1472  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,158 E 233 233] logging.cc:474:     @     0x71bb1bfd0718  (unknown)  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,181 E 233 233] logging.cc:474:     @     0x71bb1bfd0310       3024  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,195 E 233 233] logging.cc:474:     @     0x71bb1bfd0230       6944  (unknown)
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) [2025-11-12 11:12:17,200 E 233 233] logging.cc:474:     @ ... and at least 1000 more frames
(EngineCore_DP0 pid=742) (RayWorkerWrapper pid=233, ip=10.20.1.125) Fatal Python error: Segmentation fault
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

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
      Size:                    131577576(0x7d7b6e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131577576(0x7d7b6e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131577576(0x7d7b6e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131577576(0x7d7b6e8) KB            
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
      Size:                    132056036(0x7df03e4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    132056036(0x7df03e4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132056036(0x7df03e4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132056036(0x7df03e4) KB            
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
  Marketing Name:                                             
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

---

## 评论 (19 条)

### 评论 #1 — ianbmacdonald (2025-11-13T16:30:19Z)

You could try the ROCm 7.1 dev build below, 2nd preview, so it is likely to become the stable shortly;  I believe the current vllm-dev nightlies are still on the ROCm 7.0 path but have not peeked in a few days. 
- docker pull rocm/vllm-dev:preview7.1_1117_rc1_20251112

I believe the aiter knob was turned off between -rc5 and -rc6, so that [ROCm attention + AITer path](https://github.com/ROCm/aiter/issues/900) may not be present for gfx12 


---

### 评论 #2 — rksawyer (2025-11-14T02:55:58Z)

That preview fails here in the aiter package.  I tried setting VLLM_ROCM_USE_AITER=0, but same result.

```
(APIServer pid=437) Traceback (most recent call last):
(APIServer pid=437)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/utils/chip_info.py", line 63, in get_gfx_custom_op_core
(APIServer pid=437)     return gfx_mapping[line.split(":")[-1].strip()]
(APIServer pid=437)            ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=437) KeyError: 'gfx1201'

...

(APIServer pid=437) RuntimeError: Get GPU arch from rocminfo failed "Unknown GPU architecture: gfx1201. Supported architectures: ['native', 'gfx90a', 'gfx908', 'gfx940', 'gfx941', 'gfx942', 'gfx945', 'gfx1100', 'gfx950']"
```

---

### 评论 #3 — schung-amd (2025-11-14T17:08:11Z)

I also haven't gotten this to work on the preview image yet. I did get past the originally reported segfault on `rocm/vllm:latest` with `VLLM_ROCM_USE_AITER=0` (passed through `run_cluster.sh` with -e like the other env vars) as the issue seems to originate from AITER:
```
Stack (most recent call first):
(EngineCore_DP0 pid=822) (RayWorkerWrapper pid=224, ip=10.7.46.85)   File "/usr/local/lib/python3.12/dist-packages/aiter/jit/core.py", line 635 in wrapper
(EngineCore_DP0 pid=822) (RayWorkerWrapper pid=224, ip=10.7.46.85)   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/layernorm.py", line 72 in rocm_aiter_rms_norm_impl
(EngineCore_DP0 pid=822) (RayWorkerWrapper pid=224, ip=10.7.46.85)   File "/usr/local/lib/python3.12/dist-packages/torch/_ops.py", line 1254 in __call__
(EngineCore_DP0 pid=822) (RayWorkerWrapper pid=224, ip=10.7.46.85)   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/layernorm.py", line 272 in forward_hip
(EngineCore_DP0 pid=822) (RayWorkerWrapper pid=224, ip=10.7.46.85)   File "/usr/local/lib/python3.12/dist-packages/vllm/model_executor/custom_op.py", line 46 in forward
...
```
I suspect this is related to the aforementioned lack of gfx12 support. If support isn't coming in the short term then vLLM should probably avoid using AITER for this hardware, but you can manually disable it as a workaround for now. Let me know if this works for you, as I haven't extensively tested it yet.

---

### 评论 #4 — ianbmacdonald (2025-11-17T06:19:14Z)

> That preview fails here in the aiter package. I tried setting VLLM_ROCM_USE_AITER=0, but same result.

That is just your Envs .. if you share the last part of `collect_env`  I can probably eyeball it from the Envs.  There are some AITer triggers in Envs beyond VLLM_ROCM_USE_AITER=0 that can be environment dependent;  possibly you need to just `unset` other AITER Envs or set an X_ ARCH correctly (a gfx942 env may invoke it in vLLM logic, only to have the AITer throw-up if it gets included in the eval logic as different parts use Envs, amd-smi or pccids to ID hardware, so it can be inconsistent).  The right Envs should allow you to skip AITer on the gfx1201, if you don't want to rebuild with it enabled, just to get through the logic.   Its one of those things where efforts to make it simpler for the data center GPUs by increasing the logic complexity to rely less on Envs, only to muck up some consumer GPU use cases in the process. 

gfx1100 is enabled for the AITer path, but skips it by default.  A a lot of gfx11/12 paths don't work which is why it is currently disabled.   The bottom line is whatever you were doing before should just work, or can.

`wget https://raw.githubusercontent.com/vllm-project/vllm/main/vllm/collect_env.py`


---

### 评论 #5 — schung-amd (2025-11-17T17:47:33Z)

It looks like the `rocm/vllm:latest` docker has vllm/envs.py setting VLLM_ROCM_USE_AITER to True by default:

```
> cat /usr/local/lib/python3.12/dist-packages/vllm/envs.py | grep VLLM_ROCM_USE_AITER:
> VLLM_ROCM_USE_AITER: bool = True
```
in contrast with [upstream main](https://github.com/vllm-project/vllm/blob/e42bd8c2e3bfecdaf9c5a7ad99d7c7d7cb75a7b5/vllm/envs.py#L104) which has `VLLM_ROCM_USE_AITER: bool = False`. You can check this in the Docker container in Python:

```
>>> import vllm.envs as envs
>>> envs.VLLM_ROCM_USE_AITER
True
```
@rksawyer Until AITER has support for your hardware, I recommend just passing `-e VLLM_ROCM_USE_AITER=0` in the Docker invocation by default. Let me know if this works for you.

---

### 评论 #6 — briansp2020 (2025-11-17T18:23:41Z)

@schung-amd When will Radeon AI PRO R9700 get proper support? It's the only pro radeon card for AI AMD sells and it does not have proper AI framework support. This is getting ridiculous. I got mine 3 months ago and still can't use ROCm and PyTorch with proper acceleration...

---

### 评论 #7 — schung-amd (2025-11-17T19:09:36Z)

@briansp2020 I'm happy to look into enablement, but don't have answers for that at this place and time... for AITER specifically refer to https://github.com/ROCm/aiter/issues/900, and for other inquiries about using ROCm and Pytorch please submit a new issue or look for an existing issue. I was not aware of a general lack of support for the R9700, but can investigate and push for support in the appropriate places once I understand where the gaps are.

---

### 评论 #8 — briansp2020 (2025-11-17T19:40:50Z)

From what I can gather, RDNA4 does not have support for neither MIOpen or AITER and is much slower than RDNA3 in AI because of the software does not support its full capability. As I said, since it had AI Pro in the name. I had high hopes that it will be properly supported in pytorch. But after 3 month of AI Pro version and more than 6 month after the architecture release to the market, the AI support is worse than previous generation consumer card...
/rant off

What is a proper channel to request and follow the development on RDNA4? I see a few issues mentioning RDNA4/9070XT/R7000 support but I could not find the issue that tracks them all. Is there a person in AMD who is in charge of RDNA4 support? If not, shouldn't there be one?

Issues I found that mentions RDNA4/GFX12

https://github.com/ROCm/rocm-libraries/issues/2233
https://github.com/ROCm/rocm-libraries/issues/2302
https://github.com/ROCm/rocm-libraries/issues/897
https://github.com/ROCm/ROCm/issues/5657
https://github.com/ROCm/ROCm/issues/5216
https://github.com/ROCm/ROCm/issues/4846
https://github.com/ROCm/ROCm/issues/5581
https://github.com/ROCm/ROCm/issues/5571
https://github.com/ROCm/ROCm/issues/5536
https://github.com/ROCm/ROCm/issues/5442
https://github.com/ROCm/ROCm/issues/5388
https://github.com/ROCm/ROCm/issues/4121

Since it is the first AMD hardware that claims to support AI which I could afford, I had high hopes but the reality is not living up to the hype...

---

### 评论 #9 — schung-amd (2025-11-17T20:09:25Z)

> MIOpen

We are aware of the MIOpen performance issues; see also https://github.com/ROCm/rocm-libraries/issues/2218. I'm not sure what the status of the investigation on that end is.

> since it had AI Pro in the name.

Yes, unfortunately with this card and Strix Point/Strix Halo it seems we have a common trend of "AI" being put in the marketing names of devices that need a lot more work. I can't speak for the marketing decisions, but I understand and sympathize with your situation and many others have run into similar.

> I had high hopes that it will be properly supported in pytorch

If you have specific issues with pytorch support on gfx12, please open an issue for them. AFAIK we have pytorch support for the 9070, I don't know about the R9700 though.

> What is a proper channel to request and follow the development on RDNA4? I see a few issues mentioning RDNA4/9070XT/R7000 support but I could not find the issue that tracks them all. Is there a person in AMD who is in charge of RDNA4 support? If not, shouldn't there be one?

In general the appropriate channel would be opening specific issues on ROCm/ROCm (or rocm-libraries if you can isolate the issue to a component); describing a specific usecase which exhibits errors or poor performance is helpful to narrow the scope of our investigations as well as to signal boost the issues to people who can help. I don't think we have a parent issue for gfx12 roadmap items at the moment, I'll bring that up to my team. I don't think there's a singular point of contact for RDNA4; while a person or team may have ownership of the hardware it's up to the ROCm component teams to add software support for their component.

So as not to clutter this issue, please open a new issue or issues with specific usecases where you encounter deficiencies with the R9700, and we can investigate there. You can also comment in the issues you found and linked if you experience similar problems, signal boosting is always helpful.

---

### 评论 #10 — briansp2020 (2025-11-18T00:59:26Z)

@schung-amd Thanks for your reply. I created a new issue regarding Radeon AI Pro PyTorch performance. Putting a link to it so that I can easily refer back to this.

https://github.com/ROCm/ROCm/issues/5674

---

### 评论 #11 — dimon777 (2025-11-18T08:26:50Z)

I'll add here my (mostly negative) experience so far working with AMD stack here, with the hope that folks who drive AMD AI strategy read this. First of all - you don't build great things off the bat focusing on MI3xx, MI4xx, etc chips and your "datacenter" products only. You start small and grow it or at least you don't prevent people who want to build, hack and otherwise contribute evolving the platform from doing so (read below).

Few days ago I had an opportunity to work with another developer on [this issue](https://github.com/vllm-project/vllm/issues/28649). This is essentially a hack to allow native FP8 support on RDNA4. I build a docker image using another developer work validating performance numbers he initially claimed. Due to very dynamic nature of the AITER code base I built my image from specific commit of the VLLM repo, where this import worked just fine in my docker container:

```
$ docker run -it dimon747/vllm-r9700:issue-28649 /bin/bash
root@625dbb95c25f:/app# python3
Python 3.12.12 (main, Oct 10 2025, 08:52:57) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import aiter.ops.triton.utils.arch_info as arch_info;
>>> 
```

Building the same container on the latest VLLM repo (which uses more recent AITER) gives this:
```
$ docker run -it vllm-r9700:latest /bin/bash
root@06e7efa7d4f5:/app# python3
Python 3.12.12 (main, Oct 10 2025, 08:52:57) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import aiter.ops.triton.utils.arch_info as arch_info;
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/dist-packages/aiter/ops/triton/utils/_triton/arch_info.py", line 13, in get_arch
    triton.runtime.driver.active.get_current_target().arch
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 30, in __getattr__
    return getattr(self._initialize_obj(), name)
                   ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/triton/runtime/driver.py", line 26, in _initialize_obj
    self._obj = self._init_fn()
```

Simple import statement invokes now a chain of commands in AITER, quickly breaking right on spot, thereby preventing this experimental work. So, my question is: If you design your AITER stack this way, do you really expect opensource developers contribute to it? It seems impossible thing! If you can not provide timely support for your most novel professional arch (RDNA4 atm), build AITER (and any other platform in your ecosystem for this matter) to allow experimentation and hacking (in a good sense of course). Don't make things more obscure, complex (aka logic inside Python imports) and difficult to build on (learn from Tinygrad folks). 

P.S.
Not selling my R9700 yet! :)

---

### 评论 #12 — schung-amd (2025-11-18T15:23:44Z)

@dimon777 Thank you for your input, this is another issue that I haven't seen yet and would benefit from reporting in a more structured manner; can you please file an issue against ROCm/aiter for this? It looks like something we can investigate and may be able to resolve for you. We appreciate any and all feedback, but this isn't the place for it; cluttering existing issues with tangential discussions is detrimental to future viewers of said issues. You can link your issue back here once opened and I'll get eyes on it. 

Speaking of, I'm going to close this issue as discussions have derailed from the original vLLM Docker image issue, which I believe is now resolved/worked around. @rksawyer please comment here if passing `-e VLLM_ROCM_USE_AITER=0` to the Docker-invoking script does not work for you and we can reopen if necessary.

---

### 评论 #13 — cjrolo (2025-12-12T18:25:45Z)

Hello, latest vLLM AMD image (https://hub.docker.com/layers/rocm/vllm/latest/images/sha256-e7f02dd2ce3824959658bc0391296f6158638e3ebce164f6c019c4eca8150ec7) is broken for R9700. It doesn't work even with `-e VLLM_ROCM_USE_AITER=0`. 

Currently I have to have a mix-and-match of container hashes x models x configurations to run models with my R9700 cards. It's becoming quickly unusable at this point.

I can provide testing and/or developed if pointed in the right direction, let me know how can I provide help to sort this cards.

EDIT: The same happens with the `vllm-dev:nightly` image.




---

### 评论 #14 — schung-amd (2025-12-12T18:47:05Z)

Thanks for the report, we'll look into it and I'll reopen this until I have a good answer. A few weeks ago we were wrestling with a change which made it so that VLLM_ROCM_USE_AITER was no longer disabling AITER imports (and thereby breaking vLLM entirely on Radeon cards), and this sounds like it might be the same issue surfacing in the images.

One workaround we had at the time was to uninstall AITER in the Docker container, but this is pretty clumsy and doesn't lend itself well to common vLLM workflows where the container is expected to be plug and play. You can give this a try in the meanwhile while I check in with internal teams on the status of this.

---

### 评论 #15 — schung-amd (2025-12-17T19:28:08Z)

We do have a fix merged in AITER but are discussing if this is the correct way to go about things. We can resolve the KeyError with that change but this wouldn't equate to having supported kernels. Until that discussion is resolved, I don't think this will be fixed in our Docker images.

Another option here in the meanwhile is using the Radeon Docker image: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedrad/linux/vllm/build-docker-image.html#download-docker-image. This doesn't have AITER installed so you shouldn't run into this issue there.

---

### 评论 #16 — schung-amd (2025-12-17T22:02:53Z)

gfx11/12 performance boosts from AITER are being upstreamed: https://github.com/vllm-project/vllm/pull/28497. Once that is done, if we aren't using AITER imports for anything on gfx11/12 we can add a guard to the imports in vLLM and this should be resolved.

---

### 评论 #17 — cjrolo (2025-12-17T23:31:38Z)

Thanks, this is a great update. I will track this and keep an eye out. In the meanwhile I'm publishing what images work with what on the following repo: https://github.com/cjrolo/local-ai-recipes

Loving to see the fast updates. 

Thanks for the work.

---

### 评论 #18 — schung-amd (2025-12-22T21:55:38Z)

The error should be fixed upstream in VLLM now via https://github.com/vllm-project/vllm/pull/30952.

---

### 评论 #19 — schung-amd (2026-04-01T15:20:04Z)

Forgot to close this off, let me know if there's any lingering issues here and we can reopen if necessary.

---
