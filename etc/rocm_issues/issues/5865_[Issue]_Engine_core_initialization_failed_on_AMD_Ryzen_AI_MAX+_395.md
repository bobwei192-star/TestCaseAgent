# [Issue]: Engine core initialization failed on AMD Ryzen AI MAX+ 395

> **Issue #5865**
> **状态**: closed
> **创建时间**: 2026-01-17T11:41:15Z
> **更新时间**: 2026-02-03T16:11:07Z
> **关闭时间**: 2026-02-03T16:11:07Z
> **作者**: findusl
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5865

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I'm trying to get vllm to work on my AMD RYZEN AI MAX+ 395 w Radeon 8060S. After a lot of experimenting I found [this simple guide](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedryz/linux/llm/build-docker-image.html) which explicitly mentions the gfx1151 architecture of this chip as supported. But the benchmarking demo/example fails with the same error as all my other attempts. 

> RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}

I understand that this is pretty new technology and I'm using vllm-dev, but the simple sample should work I think. I'm grateful for any support, I don't know what to try anymore. I could provide a long list of different docker containers, flags, permissions and commands that I tried, but the error message is consistently the same (if they don't crash earlier because wrong container)

Full log (I also tried sudo docker run, no difference as it should be):

```
kamino@kamino:~$ docker run -it --privileged --device=/dev/kfd --device=/dev/dri --network=host --group-add sudo -w /app/vllm/ --name vllm rocm/vllm-dev:rocm7.1.1_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1 /bin/bash
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

root@kamino:/app/vllm# cd benchmarks
root@kamino:/app/vllm/benchmarks# python3 benchmark_latency.py --model deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
INFO 01-17 11:35:32 [__init__.py:241] Automatically detected platform rocm.
/app/vllm/benchmarks/benchmark_latency.py:191: DeprecationWarning: benchmark_latency.py is deprecated and will be removed in a future version. Please use 'vllm bench latency' instead.
  main(args)
Namespace(input_len=32, output_len=128, batch_size=8, n=1, use_beam_search=False, num_iters_warmup=10, num_iters=30, profile=False, output_json=None, disable_detokenize=False, model='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', runner='auto', convert='auto', task=None, tokenizer=None, tokenizer_mode='auto', trust_remote_code=False, dtype='auto', seed=None, hf_config_path=None, allowed_local_media_path='', revision=None, code_revision=None, rope_scaling={}, rope_theta=None, tokenizer_revision=None, max_model_len=None, quantization=None, enforce_eager=False, max_seq_len_to_capture=8192, max_logprobs=20, logprobs_mode=<LogprobsMode.RAW_LOGPROBS: 'raw_logprobs'>, disable_sliding_window=False, disable_cascade_attn=False, skip_tokenizer_init=False, enable_prompt_embeds=False, served_model_name=None, disable_async_output_proc=False, config_format='auto', hf_token=None, hf_overrides={}, override_neuron_config={}, override_pooler_config=None, logits_processor_pattern=None, generation_config='auto', override_generation_config={}, enable_sleep_mode=False, model_impl='auto', override_attention_dtype=None, logits_processors=None, io_processor_plugin=None, load_format='auto', download_dir=None, model_loader_extra_config={}, ignore_patterns=None, use_tqdm_on_load=True, pt_load_map_location='cpu', guided_decoding_backend='auto', guided_decoding_disable_fallback=False, guided_decoding_disable_any_whitespace=False, guided_decoding_disable_additional_properties=False, reasoning_parser='', distributed_executor_backend=None, pipeline_parallel_size=1, tensor_parallel_size=1, data_parallel_size=1, data_parallel_rank=None, data_parallel_start_rank=None, data_parallel_size_local=None, data_parallel_address=None, data_parallel_rpc_port=None, data_parallel_backend='mp', data_parallel_hybrid_lb=False, enable_expert_parallel=False, enable_eplb=False, eplb_config=EPLBConfig(window_size=1000, step_interval=3000, num_redundant_experts=0, log_balancedness=False), num_redundant_experts=None, eplb_window_size=None, eplb_step_interval=None, eplb_log_balancedness=None, max_parallel_loading_workers=None, ray_workers_use_nsight=False, disable_custom_all_reduce=False, worker_cls='auto', worker_extension_cls='', enable_multimodal_encoder_data_parallel=False, block_size=None, gpu_memory_utilization=0.9, swap_space=4, kv_cache_dtype='auto', num_gpu_blocks_override=None, enable_prefix_caching=False, prefix_caching_hash_algo='builtin', cpu_offload_gb=0, calculate_kv_scales=False, kv_sharing_fast_prefill=False, mamba_cache_dtype='auto', mamba_ssm_cache_dtype='auto', limit_mm_per_prompt={}, media_io_kwargs={}, mm_processor_kwargs=None, mm_processor_cache_gb=4, disable_mm_preprocessor_cache=False, mm_encoder_tp_mode='weights', interleave_mm_strings=False, skip_mm_profiling=False, enable_lora=None, enable_lora_bias=False, max_loras=1, max_lora_rank=16, lora_extra_vocab_size=256, lora_dtype='auto', max_cpu_loras=None, fully_sharded_loras=False, default_mm_loras=None, show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, max_num_batched_tokens=None, max_num_seqs=None, max_num_partial_prefills=1, max_long_partial_prefills=1, cuda_graph_sizes=[], long_prefill_token_threshold=0, num_lookahead_slots=0, scheduler_delay_factor=0.0, preemption_mode=None, scheduling_policy='fcfs', enable_chunked_prefill=None, disable_chunked_mm_input=False, scheduler_cls='vllm.core.scheduler.Scheduler', disable_hybrid_kv_cache_manager=False, async_scheduling=False, speculative_config=None, kv_transfer_config=None, kv_events_config=None, compilation_config={"level":null,"debug_dump_path":"","cache_dir":"","backend":"","custom_ops":[],"splitting_ops":null,"use_inductor":true,"compile_sizes":null,"inductor_compile_config":{"enable_auto_functionalized_v2":false},"inductor_passes":{},"cudagraph_mode":null,"use_cudagraph":true,"cudagraph_num_of_warmups":0,"cudagraph_capture_sizes":null,"cudagraph_copy_inputs":false,"full_cuda_graph":false,"pass_config":{},"max_capture_size":null,"local_cache_dir":null}, additional_config={}, disable_log_stats=False)
INFO 01-17 11:35:33 [utils.py:328] non-default args: {'num_redundant_experts': None, 'eplb_window_size': None, 'eplb_step_interval': None, 'eplb_log_balancedness': None, 'enable_prefix_caching': False, 'enable_lora': None, 'model': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B'}
config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 679/679 [00:00<00:00, 4.59MB/s]
INFO 01-17 11:35:38 [__init__.py:744] Resolved architecture: Qwen2ForCausalLM
`torch_dtype` is deprecated! Use `dtype` instead!
INFO 01-17 11:35:38 [__init__.py:1773] Using max model len 131072
INFO 01-17 11:35:38 [scheduler.py:222] Chunked prefill is enabled with max_num_batched_tokens=16384.
tokenizer_config.json: 3.07kB [00:00, 9.99MB/s]
tokenizer.json: 7.03MB [00:00, 169MB/s]
generation_config.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 181/181 [00:00<00:00, 1.65MB/s]
WARNING 01-17 11:35:40 [__init__.py:2959] We must use the `spawn` multiprocessing start method. Overriding VLLM_WORKER_MULTIPROC_METHOD to 'spawn'. See https://docs.vllm.ai/en/latest/usage/troubleshooting.html#python-multiprocessing for more information. Reasons: CUDA is initialized
INFO 01-17 11:35:42 [__init__.py:241] Automatically detected platform rocm.
(EngineCore_0 pid=156) INFO 01-17 11:35:43 [core.py:648] Waiting for init message from front-end.
(EngineCore_0 pid=156) INFO 01-17 11:35:43 [core.py:75] Initializing a V1 LLM engine (v0.10.2rc2.dev3+gdff7f6f03) with config: model='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', speculative_config=None, tokenizer='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, override_neuron_config={}, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=131072, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, disable_custom_all_reduce=True, quantization=None, enforce_eager=False, kv_cache_dtype=auto, device_config=cuda, decoding_config=DecodingConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_backend=''), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None), seed=0, served_model_name=deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B, enable_prefix_caching=False, chunked_prefill_enabled=True, use_async_output_proc=True, pooler_config=None, compilation_config={"level":3,"debug_dump_path":"","cache_dir":"","backend":"","custom_ops":[],"splitting_ops":["vllm.unified_attention","vllm.unified_attention_with_output","vllm.mamba_mixer2","vllm.mamba_mixer","vllm.short_conv","vllm.linear_attention"],"use_inductor":true,"compile_sizes":[],"inductor_compile_config":{"enable_auto_functionalized_v2":false},"inductor_passes":{},"cudagraph_mode":1,"use_cudagraph":true,"cudagraph_num_of_warmups":1,"cudagraph_capture_sizes":[512,504,496,488,480,472,464,456,448,440,432,424,416,408,400,392,384,376,368,360,352,344,336,328,320,312,304,296,288,280,272,264,256,248,240,232,224,216,208,200,192,184,176,168,160,152,144,136,128,120,112,104,96,88,80,72,64,56,48,40,32,24,16,8,4,2,1],"cudagraph_copy_inputs":false,"full_cuda_graph":false,"pass_config":{},"max_capture_size":512,"local_cache_dir":null}
[W117 11:35:46.696390983 ProcessGroupNCCL.cpp:981] Warning: TORCH_NCCL_AVOID_RECORD_STREAMS is the default now, this environment variable is thus deprecated. (function operator())
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
(EngineCore_0 pid=156) INFO 01-17 11:35:46 [parallel_state.py:1134] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, TP rank 0, EP rank 0
Traceback (most recent call last):
  File "/app/vllm/benchmarks/benchmark_latency.py", line 191, in <module>
    main(args)
  File "/opt/venv/lib/python3.12/site-packages/typing_extensions.py", line 3004, in wrapper
    return arg(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^
  File "/app/vllm/benchmarks/benchmark_latency.py", line 49, in main
    llm = LLM(**dataclasses.asdict(engine_args))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/vllm/entrypoints/llm.py", line 272, in __init__
    self.llm_engine = LLMEngine.from_engine_args(
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/vllm/engine/llm_engine.py", line 492, in from_engine_args
    return engine_cls.from_vllm_config(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/vllm/v1/engine/llm_engine.py", line 127, in from_vllm_config
    return cls(vllm_config=vllm_config,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/vllm/v1/engine/llm_engine.py", line 104, in __init__
    self.engine_core = EngineCoreClient.make_client(
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/vllm/v1/engine/core_client.py", line 80, in make_client
    return SyncMPClient(vllm_config, executor_class, log_stats)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/vllm/v1/engine/core_client.py", line 600, in __init__
    super().__init__(
  File "/opt/venv/lib/python3.12/site-packages/vllm/v1/engine/core_client.py", line 446, in __init__
    with launch_core_engines(vllm_config, executor_class,
  File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
    next(self.gen)
  File "/opt/venv/lib/python3.12/site-packages/vllm/v1/engine/utils.py", line 733, in launch_core_engines
    wait_for_engine_startup(
  File "/opt/venv/lib/python3.12/site-packages/vllm/v1/engine/utils.py", line 786, in wait_for_engine_startup
    raise RuntimeError("Engine core initialization failed. "
RuntimeError: Engine core initialization failed. See root cause above. Failed core proc(s): {}
root@kamino:/app/vllm/benchmarks# 
```

### Operating System

24.04.3 LTS (Noble Numbat)

### CPU

AMD RYZEN AI MAX+ 395

### GPU

Radeon 8060S gfx1151

### ROCm Version

7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

1. docker run -it --privileged --device=/dev/kfd --device=/dev/dri --network=host --group-add sudo -w /app/vllm/ --name vllm rocm/vllm-dev:rocm7.1.1_navi_ubuntu24.04_py3.12_pytorch_2.8_vllm_0.10.2rc1 /bin/bash
2. cd benchmarks
3. python3 benchmark_latency.py --model deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
      Size:                    32490752(0x1efc500) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32490752(0x1efc500) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32490752(0x1efc500) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32490752(0x1efc500) KB             
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
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    100663296(0x6000000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    100663296(0x6000000) KB            
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
      Size:                    32490752(0x1efc500) KB             
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
      Size:                    32490752(0x1efc500) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***    

### Additional Information

Same error if I try vllm serve. The benchmark is not my final goal, but since the error is the same, I just went with whats in the official guide.
`vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2026-02-03T15:00:50Z)

Hey @findusl, these `Failed core proc(s): {}` errors with vLLM should be resolved with ROCm 7.2. Could you give this a try with the latest `rocm/vllm-dev:rocm7.2_navi_ubuntu24.04_py3.12_pytorch_2.9_vllm_0.14.0rc0` image? You can launch an interactive terminal with the image using the following and give `vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` a run.
```
sudo docker run -it     --cap-add=SYS_PTRACE     --security-opt seccomp=unconfined     --device=/dev/kfd     --device=/dev/dri     --group-add video     --ipc=host     --shm-size 8G rocm/vllm-dev:rocm7.2_navi_ubuntu24.04_py3.12_pytorch_2.9_vllm_0.14.0rc0
```

---

### 评论 #2 — findusl (2026-02-03T16:11:07Z)

Hey @harkgill-amd 

thank you very much. The first run did not crash. I cannot play more with it right now, but it looks good.

Have a good one

---
