# [Issue]: amdgpu compute wave store and resume causing MES firmware 0x80 hang

> **Issue #5590**
> **状态**: closed
> **创建时间**: 2025-10-28T17:17:08Z
> **更新时间**: 2026-03-04T11:33:50Z
> **关闭时间**: 2025-11-16T16:54:22Z
> **作者**: ianbmacdonald
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5590

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

Updated 11/14 w/ new image references, use cases against ROCm 7.1
Updated 11/16 jump to the bottom for the workaround `amdgpu.cwsr_enable=0`

Strix Halo, even with the MES kernel patches, and the latest MES firmware (0x80) is still experiencing problems.   The goal here is to create a simple scenario, without building anything against a constantly changing upstream git repository or a dynamic set of pytorch wheels, in order to allow AMD developers to focus on consistently reproducing this issue in a static environment, so they can get it fixed.  

Ubuntu 24.04 includes a patched kernel with the MES fixes, and depends on the Instinct amdgpu-dkms packages so it is a good candidate distro.   

The steps to reproduce are:
1) Prepare the system following the docs, [using the linux-oem-24.04c kernel](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html#prepare-the-system) 
2) ROCm 7.1 amdgpu-dkms installs the new MES firmware, so we can now skip [pinning upstream cleanly against Ubuntu 24.04](https://github.com/ROCm/ROCm/issues/5151#issuecomment-3453898122) using the resolute linux-firmware package
3) Pull AMD's most recent pre-built vLLM dev image from docker based on ROCm 7.1 (`docker pull rocm/vllm-dev:preview7.1_1117_rc1_20251112`) 
4) Serve up the new [IBM Granite 4 H Small ](https://huggingface.co/ibm-granite/granite-4.0-h-small); A new flagship model we were happy to see [AMD support day 0](https://www.amd.com/en/developer/resources/technical-articles/2025/run-granite-4-0-models-with-amd-instinct-gpus.html). 

On the vLLM cli, we get the cleanly emitted `HW Exception by GPU node-1 (Agent handle: 0x2f0fbb70) reason :GPU Hang`  and on the kernel console we see `amdgpu: MES failed to respond to msg=REMOVE_QUEUE`

After posting an example in [a related ticket](https://github.com/ROCm/ROCm/issues/5443#issuecomment-3454127614), it seemed like a good use case to focus resolution around. 

Our setup uses a [large 125 GiB unified memory configuration](https://github.com/ROCm/ROCm/issues/5562#issuecomment-3457153637)

```
# /etc/default/grub.d/amd_ttm.cfg
GRUB_CMDLINE_LINUX="${GRUB_CMDLINE_LINUX:+$GRUB_CMDLINE_LINUX }ttm.pages_limit=32768000 ttm.page_pool_size=32768000 amdttm.pages_limit=32768000 amdttm.page_pool_size=32768000"
```

You can actually now serve up the new Nano Series (newly released 10/28) of the IBM Mamba hybrids `ibm-granite/granite-4.0-h-350m`  as the CUDA graph is captured quickly enough to avoid the GPU hang.   If you go larger, you are hung. 

You can pick your preffered attention backend. 

ROCm Attention (default):
```
vllm serve ibm-granite/granite-4.0-h-350m --compilation-config '{"cudagraph_mode":"PIECEWISE"}'  #works
vllm serve ibm-granite/granite-4.0-h-small --compilation-config '{"cudagraph_mode":"PIECEWISE"}'   #hangs
```

Triton Attention:
```
export VLLM_ROCM_USE_AITER=0
export VLLM_V1_USE_PREFILL_DECODE_ATTENTION=0
vllm serve ibm-granite/granite-4.0-h-350m   #works
vllm serve ibm-granite/granite-4.0-h-small    #hangs    
```

```
 docker run -it \
    --network host \
    --ipc host \
    --privileged \
    --cap-add=CAP_SYS_ADMIN \
    --cap-add=SYS_PTRACE \
    --device=/dev/kfd \
    --device=/dev/dri \
    --device=/dev/mem \
    --security-opt seccomp=unconfined \
    --shm-size 4G \
    -e TERM=xterm-256color \
    -v /mnt/models/huggingface/:/root/.cache/huggingface/ \
    --name vllm-strixhalohang \
    rocm/vllm-dev:preview7.1_1117_rc1_20251112
```
And here is what you will see on the console
```
root@ai2:/app# vllm serve ibm-granite/granite-4.0-h-small --compilation-config '{"cudagraph_mode":"PIECEWISE"}'
(APIServer pid=733) INFO 11-14 21:01:38 [api_server.py:1961] vLLM API server version 0.11.1rc6.dev115+gbc926c122
(APIServer pid=733) INFO 11-14 21:01:38 [utils.py:253] non-default args: {'model_tag': 'ibm-granite/granite-4.0-h-small', 'model': 'ibm-granite/granite-4.0-h-small', 'compilation_config': {'level': None, 'mode': None, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['+rms_norm', '+silu_and_mul', '+quant_fp8'], 'splitting_ops': None, 'use_inductor': None, 'compile_sizes': None, 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.PIECEWISE: 1>, 'use_cudagraph': True, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': None, 'cudagraph_copy_inputs': False, 'full_cuda_graph': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {}, 'max_cudagraph_capture_size': None, 'local_cache_dir': None}}
(APIServer pid=733) INFO 11-14 21:01:39 [model.py:630] Resolved architecture: GraniteMoeHybridForCausalLM
(APIServer pid=733) INFO 11-14 21:01:39 [model.py:1728] Using max model len 131072
(APIServer pid=733) INFO 11-14 21:01:39 [scheduler.py:226] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=733) INFO 11-14 21:01:39 [config.py:309] Disabling cascade attention since it is not supported for hybrid models.
(APIServer pid=733) INFO 11-14 21:01:39 [config.py:422] Setting attention block size to 528 tokens to ensure that attention page size is >= mamba page size.
(APIServer pid=733) INFO 11-14 21:01:39 [config.py:446] Padding mamba page size by 0.69% to ensure that mamba page size and attention page size are exactly equal.
(EngineCore_DP0 pid=809) INFO 11-14 21:01:43 [core.py:93] Initializing a V1 LLM engine (v0.11.1rc6.dev115+gbc926c122) with config: model='ibm-granite/granite-4.0-h-small', speculative_config=None, tokenizer='ibm-granite/granite-4.0-h-small', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=131072, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=0, served_model_name=ibm-granite/granite-4.0-h-small, enable_prefix_caching=False, chunked_prefill_enabled=True, pooler_config=None, compilation_config={'level': None, 'mode': 3, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['+rms_norm', '+silu_and_mul', '+quant_fp8', 'none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention', 'vllm::kda_attention', 'vllm::sparse_attn_indexer'], 'use_inductor': None, 'compile_sizes': [], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.PIECEWISE: 1>, 'use_cudagraph': True, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'full_cuda_graph': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {}, 'max_cudagraph_capture_size': 512, 'local_cache_dir': None}
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
(EngineCore_DP0 pid=809) INFO 11-14 21:01:43 [parallel_state.py:1325] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, TP rank 0, EP rank 0
(EngineCore_DP0 pid=809) INFO 11-14 21:01:44 [gpu_model_runner.py:2932] Starting to load model ibm-granite/granite-4.0-h-small...
(EngineCore_DP0 pid=809) INFO 11-14 21:01:44 [rocm.py:292] Using Rocm Attention backend.
(EngineCore_DP0 pid=809) WARNING 11-14 21:01:47 [compilation.py:908] Op 'quant_fp8' not present in model, enabling with '+quant_fp8' has no effect
Loading safetensors checkpoint shards:   0% Completed | 0/14 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:   7% Completed | 1/14 [00:02<00:31,  2.44s/it]
Loading safetensors checkpoint shards:  14% Completed | 2/14 [00:07<00:48,  4.01s/it]
Loading safetensors checkpoint shards:  21% Completed | 3/14 [00:12<00:50,  4.55s/it]
Loading safetensors checkpoint shards:  29% Completed | 4/14 [00:17<00:47,  4.79s/it]
Loading safetensors checkpoint shards:  36% Completed | 5/14 [00:22<00:43,  4.89s/it]
Loading safetensors checkpoint shards:  43% Completed | 6/14 [00:28<00:39,  4.96s/it]
Loading safetensors checkpoint shards:  50% Completed | 7/14 [00:33<00:35,  5.05s/it]
Loading safetensors checkpoint shards:  57% Completed | 8/14 [00:38<00:30,  5.09s/it]
Loading safetensors checkpoint shards:  64% Completed | 9/14 [00:43<00:25,  5.13s/it]
Loading safetensors checkpoint shards:  71% Completed | 10/14 [00:48<00:20,  5.14s/it]
Loading safetensors checkpoint shards:  79% Completed | 11/14 [00:54<00:15,  5.22s/it]
Loading safetensors checkpoint shards:  86% Completed | 12/14 [00:59<00:10,  5.27s/it]
Loading safetensors checkpoint shards:  93% Completed | 13/14 [01:05<00:05,  5.55s/it]
Loading safetensors checkpoint shards: 100% Completed | 14/14 [01:11<00:00,  5.51s/it]
Loading safetensors checkpoint shards: 100% Completed | 14/14 [01:11<00:00,  5.09s/it]
(EngineCore_DP0 pid=809) 
(EngineCore_DP0 pid=809) INFO 11-14 21:02:59 [default_loader.py:314] Loading weights took 71.42 seconds
(EngineCore_DP0 pid=809) INFO 11-14 21:03:04 [gpu_model_runner.py:2997] Model loading took 78.4272 GiB and 77.370219 seconds
(EngineCore_DP0 pid=809) /usr/local/lib/python3.12/dist-packages/torch/_dynamo/variables/functions.py:1652: UserWarning: Dynamo detected a call to a `functools.lru_cache`-wrapped function. Dynamo ignores the cache wrapper and directly traces the wrapped function. Silent incorrectness is only a *potential* risk, not something we have observed. Enable TORCH_LOGS="+dynamo" for a DEBUG stack trace.
(EngineCore_DP0 pid=809)   torch._dynamo.utils.warn_once(msg)
(EngineCore_DP0 pid=809) INFO 11-14 21:03:08 [backends.py:620] Using cache directory: /root/.cache/vllm/torch_compile_cache/4f6a0d7a6e/rank_0_0/backbone for vLLM's torch.compile
(EngineCore_DP0 pid=809) INFO 11-14 21:03:08 [backends.py:636] Dynamo bytecode transform time: 3.07 s
(EngineCore_DP0 pid=809) INFO 11-14 21:03:09 [backends.py:250] Cache the graph for dynamic shape for later use
(EngineCore_DP0 pid=809) INFO 11-14 21:03:23 [backends.py:281] Compiling a graph for dynamic shape takes 15.78 s
(EngineCore_DP0 pid=809) WARNING 11-14 21:03:24 [fused_moe.py:887] Using default MoE config. Performance might be sub-optimal! Config file not found at ['/usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fused_moe/configs/E=72,N=768,device_name=0x1586.json']
(EngineCore_DP0 pid=809) INFO 11-14 21:03:26 [monitor.py:34] torch.compile takes 18.85 s in total
HW Exception by GPU node-1 (Agent handle: 0x2f0fbb70) reason :GPU Hang
HW Exception by GPU node-1 (Agent handle: 0x1f62da10) reason :GPU Hang
Aborted (core dumped)
root@ai2:/app# /usr/lib/python3.12/multiprocessing/resource_tracker.py:279: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
```
And the dmesg is going to be similar to the following
```
[  990.479743] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[  990.479760] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[  990.479768] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  990.479779] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[  990.479799] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[  990.479898] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[  990.479920] amdgpu: Failed to quiesce KFD
[  990.479967] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[  990.486732] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[  990.520342] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[  990.549888] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[  990.550342] [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
[  990.550415] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[  990.550417] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[  990.550419] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[  990.564041] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[  990.580876] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09002F00
[  990.640096] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  990.640105] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  990.640106] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  990.640107] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  990.640108] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  990.640109] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  990.640110] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  990.640111] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  990.640112] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  990.640113] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  990.640114] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  990.640115] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[  990.640116] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[  990.640117] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[  990.640118] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  990.640119] amdgpu 0000:c5:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[  990.712022] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[  990.712038] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[ 1019.947543] amdgpu: Freeing queue vital buffer 0x79c031400000, queue evicted
[ 1019.947554] amdgpu: Freeing queue vital buffer 0x79c032a00000, queue evicted
```
```
OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU: 
model name	: AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    aie2                               
  Marketing Name:          AIE-ML     
```
```
root@ai2:~# dpkg -l | grep amdgpu
root@ai2:~# dpkg -l | grep amdgpu
ii  amdgpu-core                          1:7.1.70100-2238427.24.04               all          Core meta package for unified amdgpu driver.
ii  amdgpu-dkms                          1:6.16.6.30200000-2238411.24.04         all          amdgpu driver in DKMS format.
ii  amdgpu-dkms-firmware                 30.20.0.0.30200000-2238411.24.04        all          firmware blobs used by amdgpu driver in DKMS format
ii  amdgpu-install                       30.20.0.0.30200000-2238411.24.04        all          AMDGPU driver repository and installer
ii  libdrm-amdgpu-amdgpu1:amd64          1:2.4.125.70100-2238427.24.04           amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm-amdgpu-common                 1.0.0.70100-2238427.24.04               all          List of AMD/ATI cards' device IDs, revision IDs and marketing names
ii  libdrm-amdgpu-dev:amd64              1:2.4.125.70100-2238427.24.04           amd64        Userspace interface to kernel DRM services -- development files
ii  libdrm-amdgpu-radeon1:amd64          1:2.4.125.70100-2238427.24.04           amd64        Userspace interface to radeon-specific kernel DRM services -- runtime
ii  libdrm-amdgpu1:amd64                 2.4.122-1~ubuntu0.24.04.1               amd64        Userspace interface to amdgpu-specific kernel DRM services -- runtime
ii  libdrm2-amdgpu:amd64                 1:2.4.125.70100-2238427.24.04           amd64        Userspace interface to kernel DRM services -- runtime

root@ai2:~# cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
```


### Operating System

Ubuntu 24.04.3 LTS

### CPU

Strix Halo

### GPU

Strix Halo

### ROCm Version

ROCm 7.1

### ROCm Component

_No response_

### Steps to Reproduce


Described in the problem description 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module version 6.16.6 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
      Size:                    131009800(0x7cf0d08) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131009800(0x7cf0d08) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131009800(0x7cf0d08) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131009800(0x7cf0d08) KB            
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
  BDFID:                   50432                              
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
      Size:                    125829120(0x7800000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    125829120(0x7800000) KB            
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
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
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
      Size:                    131009800(0x7cf0d08) KB            
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
      Size:                    131009800(0x7cf0d08) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***              
```

### Additional Information

_No response_

---

## 评论 (22 条)

### 评论 #1 — Epliz (2025-11-01T10:01:52Z)

Hi @ianbmacdonald ,

I had some system freezes on strix halo as mentioned at https://github.com/ROCm/TheRock/issues/1937 .
Updating the kernel to 6.17 + using amdgpu-dkms from ROCM 7.1 + using the latest firmware from linux-firmware.git + rocm 7.10 through pip to run my app solves the hangs for me at least.
I hope it helps on your side as well.

Best,
Epliz

---

### 评论 #2 — waltercool (2025-11-01T14:17:10Z)

I been using kernel 6.17.5 and now 6.17.6 and latest stable firmware (20251021) still can reproduce the issue tho. Using ROCM 7.0.2 compiled for my system, haven't tried 7.1 yet.

If you say this is fixed, then it's not a kernel thing, but ROCM 7.1. Will try later using 7.1 and provide any updates on my end.

---

### 评论 #3 — darkbasic (2025-11-01T14:32:49Z)

Try ROCm 7.10 not 7.1: https://github.com/kyuz0/amd-strix-halo-toolboxes/pull/11

I suggest you to try the improved flavor of the container (it has llama.cpp fixes) if your crashes happen with llama.cpp because it fixes many of them. Unfortunately they won't merge it because they plan to deprecate the wmma kernel and don't feel like making AMD users' life better in the meantime.

---

### 评论 #4 — waltercool (2025-11-01T16:47:03Z)

Just tried using ROCM 7.1 and still fails, it is very easy to reproduce using Qwen Image.

@darkbasic How can I test this ROCm 7.10? Your PR to md-strix-halo-toolboxes seems very "alpha" to me.

---

### 评论 #5 — ianbmacdonald (2025-11-02T16:24:02Z)

FYI, if you want to test 25.10 ([6.17.x](https://launchpad.net/ubuntu/+source/linux/6.17.0-7.7)), instead of 24.04 (6.14.x), using fully patched distribution kernel packages, you will have to increase the AMD repo recommended preference of 600 (I use 1001) to allow apt to downgrade a few 25.10 `rocprofiler` packages, that are actually ahead of ROCm 7.1.   The reason being that the ROCm 7.1 dependencies have been hard pinned to specific versions and will create conflicts using the [documented process for 24.04](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/install-methods/package-manager/package-manager-ubuntu.html).  

```
$sudo apt install rocm -s

Solving dependencies... Error!  
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

Unsatisfied dependencies:
 rocm : Depends: rocminfo (= 1.0.0.70100-20~24.04) but 1.0.0.70002-56~24.04 is to be installed
        Depends: rocm-cmake (= 0.14.0.70100-20~24.04) but 0.14.0.70002-56~24.04 is to be installed
        Depends: rocm-developer-tools (= 7.1.0.70100-20~24.04) but 7.0.2.70002-56~24.04 is to be installed
        Depends: rocm-openmp (= 7.1.0.70100-20~24.04) but 7.0.2.70002-56~24.04 is to be installed
        Depends: rocm-opencl-sdk (= 7.1.0.70100-20~24.04) but 7.0.2.70002-56~24.04 is to be installed
        Depends: rocm-hip (= 7.1.0.70100-20~24.04) but 7.0.2.70002-56~24.04 is to be installed
        Depends: mivisionx (= 3.4.0.70100-20~24.04) but 3.3.0.70002-56~24.04 is to be installed
        Depends: migraphx (= 2.14.0.70100-20~24.04) but 2.13.0.70002-56~24.04 is to be installed
        Depends: rpp (= 2.1.0.70100-20~24.04) but 2.0.0.70002-56~24.04 is to be installed
        Depends: rocm-core (= 7.1.0.70100-20~24.04) but 7.0.2.70002-56~24.04 is to be installed
        Depends: miopen-hip (= 3.5.1.70100-20~24.04) but 3.5.0.70002-56~24.04 is to be installed
        Depends: half (= 1.12.0.70100-20~24.04) but 1.12.0.70002-56~24.04 is to be installed
        Depends: rocm-llvm (= 20.0.0.25425.70100-20~24.04) but 20.0.0.25385.70002-56~24.04 is to be installed
        Depends: migraphx-dev (= 2.14.0.70100-20~24.04) but 2.13.0.70002-56~24.04 is to be installed
        Depends: mivisionx-dev (= 3.4.0.70100-20~24.04) but 3.3.0.70002-56~24.04 is to be installed
        Depends: rpp-dev (= 2.1.0.70100-20~24.04) but 2.0.0.70002-56~24.04 is to be installed
        Depends: miopen-hip-dev (= 3.5.1.70100-20~24.04) but 3.5.0.70002-56~24.04 is to be installed
Error: Unable to satisfy dependencies. Reached two conflicting decisions:
   1. rocm-developer-tools:amd64=7.1.0.70100-20~24.04 Depends rocprofiler-sdk (= 1.0.0-20~24.04)
      but none of the choices are installable:
      - rocprofiler-sdk:amd64=1.0.0-20~24.04 is not selected for install
   2. rocm-developer-tools:amd64=7.1.0.70100-20~24.04 is selected as an upgrade because:
      1. rocm:amd64=7.1.0.70100-20~24.04 is selected as an upgrade
      2. rocm:amd64=7.1.0.70100-20~24.04 Depends rocm-developer-tools (= 7.1.0.70100-20~24.04)

$sudo apt policy rocprofiler-sdk
rocprofiler-sdk:
  Installed: 1.0.0-56~24.04
  Candidate: 1.0.0-56~24.04
  Version table:
 *** 1.0.0-56~24.04 100
        100 /var/lib/dpkg/status
     1.0.0-20~24.04 600
        600 https://repo.radeon.com/rocm/apt/7.1 noble/main amd64 Packages
```

Making the adjustment from 600 to 1001, works around the issue with some of these hard version pins in the ROCm 7.1 packages. 

```
$ cat /etc/apt/preferences.d/repo-radeon-pin
Package: *
Pin: release o=repo.radeon.com
Pin-Priority: 1001


$sudo apt upgrade

The following package was automatically installed and is no longer required:
  rocm-hip-runtime-dev
Use 'apt autoremove' to remove it.

Upgrading:
  amd-smi-lib           hipblas-dev    hiprand-dev         hsa-rocr               rccl            rocm-core             rocm-hip-runtime-dev   rocminfo              rocsolver
  comgr                 hipblaslt      hipsolver           hsa-rocr-dev           rccl-dev        rocm-dbgapi           rocm-hip-sdk           rocprim-dev           rocsolver-dev
  composablekernel-dev  hipblaslt-dev  hipsolver-dev       migraphx               rocalution      rocm-debug-agent      rocm-language-runtime  rocprofiler           rocsparse
  half                  hipcc          hipsparse           migraphx-dev           rocalution-dev  rocm-dev              rocm-llvm              rocprofiler-compute   rocsparse-dev
  hip-dev               hipcub-dev     hipsparse-dev       miopen-hip             rocblas         rocm-developer-tools  rocm-opencl            rocprofiler-dev       rocthrust-dev
  hip-doc               hipfft         hipsparselt         miopen-hip-dev         rocblas-dev     rocm-device-libs      rocm-opencl-dev        rocprofiler-plugins   roctracer
  hip-runtime-amd       hipfft-dev     hipsparselt-dev     mivisionx              rocfft          rocm-gdb              rocm-opencl-sdk        rocprofiler-register  roctracer-dev
  hip-samples           hipfort-dev    hiptensor           mivisionx-dev          rocfft-dev      rocm-hip              rocm-openmp            rocprofiler-systems   rocwmma-dev
  hipblas               hipify-clang   hiptensor-dev       openmp-extras-dev      rocm            rocm-hip-libraries    rocm-smi-lib           rocrand               rpp
  hipblas-common-dev    hiprand        hsa-amd-aqlprofile  openmp-extras-runtime  rocm-cmake      rocm-hip-runtime      rocm-utils             rocrand-dev           rpp-dev

DOWNGRADING:
  rocprofiler-sdk  rocprofiler-sdk-rocpd  rocprofiler-sdk-roctx
...
Inst rocprofiler [2.0.70002.70002-56~24.04] (2.0.70100.70100-20~24.04 repo.radeon.com:7.1/noble [amd64]) []
Inst rocprofiler-plugins [2.0.70002.70002-56~24.04] (2.0.70100.70100-20~24.04 repo.radeon.com:7.1/noble [amd64]) []
Inst rocprofiler-sdk-roctx [1.0.0-56~24.04] (1.0.0-20~24.04 repo.radeon.com:7.1/noble [amd64]) []
Inst rocprofiler-sdk-rocpd [1.0.0-56~24.04] (1.0.0-20~24.04 repo.radeon.com:7.1/noble [amd64]) []
Inst rocprofiler-sdk [1.0.0-56~24.04] (1.0.0-20~24.04 repo.radeon.com:7.1/noble [amd64]) []
Inst rocprofiler-compute [3.2.3.70002-56~24.04] (3.3.0.70100-20~24.04 repo.radeon.com:7.1/noble [amd64]) []
Inst rocprofiler-systems [1.1.1.70002-56~24.04] (1.2.0.70100-20~24.04 repo.radeon.com:7.1/noble [amd64]) []
Inst rocprofiler-dev [2.0.70002.70002-56~24.04] (2.0.70100.70100-20~24.04 repo.radeon.com:7.1/noble [amd64]) []

```


---

### 评论 #6 — ianbmacdonald (2025-11-03T17:03:13Z)

> I had some system freezes on strix halo as mentioned at [ROCm/TheRock#1937](https://github.com/ROCm/TheRock/issues/1937) .
> Updating the kernel to 6.17 + using amdgpu-dkms from ROCM 7.1 + using the latest firmware from linux-firmware.git + rocm 7.10 through pip to run my app solves the hangs for me at least.
> I hope it helps on your side as well.

I was able to reproduce the hang scenarios described above, and a couple of new ones.  TLDR below; details follow.

- amdgpu-dkms matches versions with the in-kernel amdgpu module already present in Ubuntu 25.10 (6.17.2+)
- amdgpu-dkms-firmware matches MES version from the upstream linux-firmware present in Ubuntu 26.04 preview
- switching between in-kernel and amdgpu-dkms requires [moving module params from ttm to amdttm in concert with the kernel module package switch](https://github.com/ROCm/ROCm/issues/5595)
- no change for the two previously described crash/hang scenarios
- additionally, using the current AMD vLLM nightly (`nightly_main_20251103 / v0.11.1rc6.dev53+g0ce743f4e`) in the 2nd scenario produces the page fault (`amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801030`)
- additionally, I added a five line uv recipe to reproduce `amdgpu: MES failed to respond to msg=REMOVE_QUEUE` on a matched set of theRock 7.10 nightlies with Qwen-Image-Edit-2509

The amdgpu-dkms package now builds against 6.17, which is great;  It actually brings the same amdgpu 6.16.6 module that ships with the newest Ubuntu Questing kernel package.  The amdgpu-dkms depends on the amdgpu-dkms-firmware package as well, which now includes the new 0x80 MES firmware, also great (it will preempt linux-firmware by default when using standard packages).   This means on Ubuntu 25.10, you can now switch back to amdgpu-dkms if you were previously using the in-kernel amdgpu and pinning upstream firmware for MES or even just install amdgpu-dkms-firmware to get the firmware alongside the in-kernel amdgpu.   This is great work by AMD, and might represent alpha support for Ubuntu 25.10.  For anything newer than kernel 6.17, stick with the newer in-kernel amdgpu.   If you are a Debian/Ubuntu user adding back in amdgpu-dkms on 6.17, in addition to no longer having to pin and divert to the firmware as explained in the steps above, you also will need to define a module configuration for amdttm in addition to ttm.  I define both to keep things constant regardless of my package configuration and/or source of amdgpu. 

```
$ cat /etc/modprobe.d/ttm.conf 
# 125 GiB
options ttm pages_limit=32768000

$ cat /etc/modprobe.d/amdttm.conf 
# 125 GiB
options amdttm pages_limit=32768000

$sudo update-initramfs -u -k all
update-initramfs: Generating /boot/initrd.img-6.17.0-7-generic

```
You can tell if you have in-kernel amdgpu loaded by inspecting amd-smi and noting the `6.17.0-7` kernel version in place of the amdgpu version.
```
$sudo amd-smi 
+------------------------------------------------------------------------------+
| AMD-SMI 26.1.0+5df6c765      amdgpu version: 6.17.0-7 ROCm version: 7.1.0    |
| VBIOS version: 023.011.000.039.000001                                        |
| Platform: Linux Baremetal                                                    |
...
```
If you are using amdgpu-dkms, the same command will output the module version rather than the kernel version (I am of two minds on this as a feature.. it helps to ID in-kernel use for support, but obfuscates the actual version, potentially confusing end users)
```
+------------------------------------------------------------------------------+
| AMD-SMI 26.1.0+5df6c765      amdgpu version: 6.16.6   ROCm version: 7.1.0    |
| VBIOS version: 00107962                                                      |
| Platform: Linux Baremetal                                                    |
...
```
It may seem like in-kernel is newer based on this output, however, **in both cases (using amdgpu-dkms OR in-kernel amdgpu)  you are actually using the same module** version in Ubuntu 25.10, with both scenarios emitting the same version number `6.16.6` shown below

```
$sudo modinfo amdgpu | head -n 3
filename:       /lib/modules/6.17.0-7-generic/updates/dkms/amdgpu.ko.zst
version:        6.16.6
license:        GPL and additional rights
```

The firmware now shipped in amdgpu-dkms-firmware also overrides linux-firmware by default (without following the steps I linked to above using dpkg-divert and apt pinning) and provides MES version 0x80, shown below from the Instinct 30.20.0 packages. 

```
$ sudo cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
```
In terms of testing for the crash/hang scenario, it seems to still be present with the scenarios above, and here the 5 line reproducable uv setup I ran on 25.10 against TheRock ROCm 7.10 nightlies that can generate the hang with Qwen-Image-Edit-2509 and a couple of images.   I have run this in the past sucessfully on ROCm 6.4.4 on Strix Halo and on a [MI300X using ROCm 7.0.2](https://netstatz.com/rocm-7-quickstart-cloudrift-mi300x/#Qwen_Image_Edit_2509)

```
export PYTORCH_ROCM_ARCH=gfx1151
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
uv init --python 3.13
uv add --index therock_nightly=https://rocm.nightlies.amd.com/v2/gfx1151/ --index-strategy unsafe-best-match --prerelease allow "rocm-sdk-core==7.10.0a20251015" "rocm[libraries]==7.10.0a20251015" "torch==2.10.0a0+rocm7.10.0a20251015" "torchvision==0.25.0a0+rocm7.10.0a20251015" "torchaudio==2.8.0a0+rocm7.10.0a20251015" "pytorch-triton-rocm==3.5.0+gitb0cf18f2.rocm7.10.0a20251015"
uv add git+https://github.com/huggingface/diffusers.git
uv add git+https://github.com/ivanfioravanti/qwen-image-mps.git
uv run qwen-image-mps edit -i mushroom1.png mouse1.png -p "The mouse is under the mushroom."
```
The console error `torch.AcceleratorError: HIP error: unspecified launch failure` and resulting dmesg output with the familiar `MES failed to respond to msg=REMOVE_QUEUE`
```
[22944.953268] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[22944.953287] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[22944.953296] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[22944.953305] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[22944.953325] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!
```

---

### 评论 #7 — ianbmacdonald (2025-11-05T21:01:28Z)

I found the current set of ROCm 7 nightly pytorch wheels (TheRock nightly still failing and lacking AOTriton) are no longer causing this page faults after several iterations (previously was 100% reproducable), and it notably appears to be using memory efficient flash attention.  This seems to be just the hang now. 

```
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
uv init --python 3.13
uv add --index rocm7_nightly=https://download.pytorch.org/whl/nightly/rocm7.0/ --index-strategy unsafe-best-match --prerelease allow "torch==2.10.0.dev20251102+rocm7.0" "torchvision==0.25.0.dev20251105+rocm7.0" "torchaudio==2.10.0.dev20251105+rocm7.0"
uv add git+https://github.com/huggingface/diffusers.git
uv add git+https://github.com/ivanfioravanti/qwen-image-mps.git
uv run qwen-image-mps edit -i mushroom1.png mouse1.png -p "The mouse is under the mushroom."
```



---

### 评论 #8 — ianbmacdonald (2025-11-14T22:05:22Z)

I updated the problem description to reflect current state, with ROCm 7.1 with prebuilt images using ROCm 7.1 libraries.    Notably, the new nano series models are small enough to load before the hang, which may provide some clearer insights as to the root cause.   This is also reproducable with locally built vllm (vllm-0.11.1rc7.dev147+gda14ae0fa.rocm710-cp312) and torch (torch-2.9.0+git7e899b7-cp312). 

---

### 评论 #9 — ianbmacdonald (2025-11-16T05:33:58Z)

Well, it seems this is simply fixed by passing a kernel parameter `amdgpu.cwsr_enable=0` to amdgpu.   The following config will add this to grub without causing any unnecessary prompts about modified configuration at the next distribution upgrade.  Tested on Ubuntu 24.x, 25.x and Debian 13. 

```
# /etc/default/grub.d/amd_cwsr.cfg
GRUB_CMDLINE_LINUX="${GRUB_CMDLINE_LINUX:+$GRUB_CMDLINE_LINUX }amdgpu.cwsr_enable=0"
```
Followed by a simple `update-grub` and reboot. 

Thanks to @majed over in the Strix Halo Homelab discord community.  Seems I missed this [thread ](https://community.frame.work/t/amd-gpu-mes-timeouts-causing-system-hangs-on-framework-laptop-13-amd-ai-300-series/71364/43?page=3) just as the new firmware dropped.   

According to the [docs](https://www.kernel.org/doc/html/latest/gpu/amdgpu/module-parameters.html), CWSR(compute wave store and resume) allows the GPU to preempt shader execution in the middle of a compute wave. Default is 1 to enable this feature. Setting 0 disables it.

So perhaps there is a bug here after all .. tripping on this using an HDMI monitor plugged into headless systems without any UI doing 'shader execution' seems like a problem. 


   

---

### 评论 #10 — hammmmy (2025-11-16T11:49:50Z)

There are two patches that may be worth trying (they should be applied together):

1. https://gitlab.freedesktop.org/agd5f/linux/-/commit/d15deafab5d722afb9e2f83c5edcdef9d9d98bd1
2. https://github.com/ROCm/rocm-systems/pull/1807 (not merged yet, CI waiting to pick up the kernel patch)

These two patches fix a mismatch between userspace and kernel space on the size of the VGPR region


---

### 评论 #11 — waltercool (2025-11-16T14:57:15Z)

I just tried a diffusion interference (Chrono Edit) with those patches, but eventually got a MES issue. Not sure if the same issue.

```
[ 1830.944470] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32789)
[ 1830.944486] amdgpu 0000:c4:00.0: amdgpu:  Process python3 pid 3497 thread python3 pid 3497
[ 1830.944490] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007fa7b5161000 from client 10
[ 1830.944494] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[ 1830.944496] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[ 1830.944499] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x1
[ 1830.944501] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1830.944502] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[ 1830.944503] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1830.944504] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
[ 1830.944516] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32789)
[ 1830.944519] amdgpu 0000:c4:00.0: amdgpu:  Process python3 pid 3497 thread python3 pid 3497
[ 1830.944520] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007fa7b5156000 from client 10
[ 1833.574721] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[ 1833.574733] amdgpu 0000:c4:00.0: amdgpu: failed to suspend all gangs
[ 1833.574736] amdgpu 0000:c4:00.0: amdgpu: failed to suspend gangs from MES
[ 1833.574737] amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 1833.574743] amdgpu 0000:c4:00.0: amdgpu: Suspending all queues failed
[ 1833.574757] amdgpu 0000:c4:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1833.574987] amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
[ 1833.950387] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
[ 1833.950397] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
[ 1833.950401] amdgpu: Failed to quiesce KFD
[ 1833.950413] amdgpu 0000:c4:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0

```

Question, do I have to rebuild any specific libraries like pytorch after building to get those changes? On my scenario I just had rebuilt kernel and rocr-runtime.

Edit: I can confirm no issues disabling cwsr

---

### 评论 #12 — ianbmacdonald (2025-11-16T16:54:22Z)

> Edit: I can confirm no issues disabling cwsr

Great, I am closing this one as I can't reproduce it any longer.   

---

### 评论 #13 — waltercool (2025-11-16T17:02:03Z)

I don't think disabling cwsr is a solution but rather a workaround.

A solution should move in the direction provided by @hammmmy, by effectively fixing the crashes caused by cwsr enabled.

Well, up to AMD or ROCm team to proceed on this, especially if the issue requires kernel and rocr fixes.

---

### 评论 #14 — nktice (2025-11-25T02:49:24Z)

First of all thank you for tracking this issue down - my crashes have stopped!

I wrote the maker of the hardware I purchased and mentioned this thread - they wrote back to me asking me more about it, and I realized that the instructions could be re-written to assist less technical folks with solution. 

So the winner is this post that turns off feature that seems to stop them : 
https://github.com/ROCm/ROCm/issues/5590#issuecomment-3481580910

Here's those instructions re-written as a shell script to copy and paste - 
```bash
sudo tee --append /etc/default/grub.d/amd_cwsr.cfg  <<EOF
# /etc/default/grub.d/amd_cwsr.cfg
GRUB_CMDLINE_LINUX="${GRUB_CMDLINE_LINUX:+$GRUB_CMDLINE_LINUX }amdgpu.cwsr_enable=0"
EOF
sudo update-grub
```
Settings take effect at the next system reboot ( restart required... ) 
Folks could restart now, or apply the code below and restart after... 

Worthy of mention are these details to setup dynamic mem use - 
If you actually need to maximize access to the memory, 
the following can allocate shared memory for model usage...
from observation, this comes at performance cost that's significant.
Better performance is found through BIOS settings dedicating mem.  
https://github.com/ROCm/ROCm/issues/5590#issuecomment-3481580910
```bash
sudo tee --append /etc/modprobe.d/ttm.conf  <<EOF
# 125 GiB
options ttm pages_limit=32768000
EOF

sudo tee --append /etc/modprobe.d/amdttm.conf   <<EOF
# 125 GiB
options amdttm pages_limit=32768000
EOF

sudo update-initramfs -u -k all
#update-initramfs: Generating /boot/initrd.img-6.17.0-7-generic 
sudo update-grub
```
Reboot is required for changes to take effect.   Thanks for those details. 



---

### 评论 #15 — hammmmy (2025-11-25T03:22:17Z)

Disabling CWSR may cause side effects. This issue appears similar to https://gitlab.freedesktop.org/drm/amd/-/issues/4632, which was fixed through matching user-mode and kernel-mode changes that must be applied together:
- ROCm PR merged into the develop branch: https://github.com/ROCm/rocm-systems/pull/1807
- OEM kernel 6.18-rc6 includes this commit: https://github.com/torvalds/linux/commit/d15deafab5d722afb9e2f83c5edcdef9d9d98bd1

Could you retest using the ROCm TheRock nightlies together with kernel 6.18-rc6?

---

### 评论 #16 — darkbasic (2025-11-25T09:46:18Z)

https://github.com/ROCm/TheRock/actions/workflows/release_portable_linux_packages.yml?query=branch%3Amain

---

### 评论 #17 — laichiaheng (2025-12-21T11:21:18Z)

> Disabling CWSR may cause side effects. This issue appears similar to https://gitlab.freedesktop.org/drm/amd/-/issues/4632, which was fixed through matching user-mode and kernel-mode changes that must be applied together:
> 
>     * ROCm PR merged into the develop branch: [hsakmt: bump vgpr count for gfx1151 rocm-systems#1807](https://github.com/ROCm/rocm-systems/pull/1807)
> 
>     * OEM kernel 6.18-rc6 includes this commit: [torvalds/linux@d15deaf](https://github.com/torvalds/linux/commit/d15deafab5d722afb9e2f83c5edcdef9d9d98bd1)
> 
> 
> Could you retest using the ROCm TheRock nightlies together with kernel 6.18-rc6?

It's way much worse with 6.18 for ROCm.

---

### 评论 #18 — hammmmy (2025-12-21T12:33:29Z)

> It's way much worse with 6.18 for ROCm.

6.18 doesn't work with existing ROCm releases unfortunately and 6.17 without the fix is the only option with them (see the note on https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html).

In the short term (before ROCm 7.2 and 7.11 releases), the only option is to try the nightlies with this ROCm-systems bump https://github.com/ROCm/TheRock/pull/2643 and oem kernel 6.18

---

### 评论 #19 — ndrewpj (2025-12-21T14:39:14Z)

> > It's way much worse with 6.18 for ROCm.
> 
> 6.18 doesn't work with existing ROCm releases unfortunately and 6.17 without the fix is the only option with them (see the note on https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-pytorch.html).
> 
> In the short term (before ROCm 7.2 and 7.11 releases), the only option is to try the nightlies with this ROCm-systems bump [ROCm/TheRock#2643](https://github.com/ROCm/TheRock/pull/2643) and oem kernel 6.18

ROCm 7.1.1 works for me on CachyOS with kernel 6.18, firmware 0x80

---

### 评论 #20 — waltercool (2025-12-28T22:12:37Z)

Don't abuse of AI for bug reports dude, it's way too obvious.

It's fixed in upstream firmware and TheRock (develop branch). You have to wait until a new snapshot of Linux Firmware or ROCm is released with the fixes, or just test by yourself with the nightly releases

---

### 评论 #21 — nktice (2026-02-21T07:03:51Z)

I would like to note that with the introduction of Linux Kernel 6.19 and the latest ROCm theRock nightly drivers  - https://github.com/ROCm/TheRock - it appears that this issue has been resolved.  I've been able to get a fair amount of use without the workaround(s), and without crashes.  

---

### 评论 #22 — woct0rdho (2026-02-23T05:57:36Z)

I can confirm that with Ubuntu 26.04, Linux kernel 6.19.0-6-generic, in-kernel driver (not dkms), rocm 7.12.0a20260218 from TheRock, this issue seems resolved.

~~However, when I switch from dkms driver to in-kernel driver, there is visible regression (from 30 to 28 TFLOPS) in some simple PyTorch large matmul benchmark, which may be related to PyTorch's hipBLAS backend (hipBLASLt is even slower). Some HIP kernels I've written are unaffected though. Anyway, this regression is not directly related to this issue.~~ There is no regression after the firmware update on 20260227.

---
