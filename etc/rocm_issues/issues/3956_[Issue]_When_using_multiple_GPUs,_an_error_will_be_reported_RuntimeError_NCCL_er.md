# [Issue]: When using multiple GPUs, an error will be reported: RuntimeError: NCCL error

> **Issue #3956**
> **状态**: closed
> **创建时间**: 2024-10-30T06:14:32Z
> **更新时间**: 2024-11-26T19:57:50Z
> **关闭时间**: 2024-11-26T19:57:49Z
> **作者**: dotbalo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3956

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am going to use VLLM to start a QWEN model on an AMD GPU for testing. If I use a GPU to start it, it can start and use it normally. The log after startup is as follows:
`
commad: vllm serve /data/llm_models/Qwen2.5-14B-Instruct

result:
To avoid this limit at the expense of performance run with --disable-frontend-multiprocessing
INFO:     Started server process [6323]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)`

But when I use `--tensor-parallel-size 2 --distributed-executor-backend=mp` to bind multiple GPU cards, the following error occurs:
`Process SpawnProcess-1:
ERROR 10-30 13:46:27 multiproc_worker_utils.py:120] Worker VllmWorkerProcess pid 6855 died, exit code: -15
INFO 10-30 13:46:27 multiproc_worker_utils.py:123] Killing local vLLM worker processes
Traceback (most recent call last):
  File "/opt/conda/envs/py_3.10/lib/python3.10/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/opt/conda/envs/py_3.10/lib/python3.10/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/entrypoints/openai/rpc/server.py", line 236, in run_rpc_server
    server = AsyncEngineRPCServer(async_engine_args, usage_context, rpc_path)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/entrypoints/openai/rpc/server.py", line 34, in __init__
    self.engine = AsyncLLMEngine.from_engine_args(
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/engine/async_llm_engine.py", line 735, in from_engine_args
    engine = cls(
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/engine/async_llm_engine.py", line 615, in __init__
    self.engine = self._init_engine(*args, **kwargs)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/engine/async_llm_engine.py", line 835, in _init_engine
    return engine_class(*args, **kwargs)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/engine/async_llm_engine.py", line 262, in __init__
    super().__init__(*args, **kwargs)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/engine/llm_engine.py", line 305, in __init__
    self.model_executor = executor_class(
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/executor/multiproc_gpu_executor.py", line 222, in __init__
    super().__init__(*args, **kwargs)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/executor/distributed_gpu_executor.py", line 26, in __init__
    super().__init__(*args, **kwargs)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/executor/executor_base.py", line 47, in __init__
    self._init_executor()
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/executor/multiproc_gpu_executor.py", line 124, in _init_executor
    self._run_workers("init_device")
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/executor/multiproc_gpu_executor.py", line 199, in _run_workers
    driver_worker_output = driver_worker_method(*args, **kwargs)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/worker/worker.py", line 175, in init_device
    init_worker_distributed_environment(self.parallel_config, self.rank,
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/worker/worker.py", line 450, in init_worker_distributed_environment
    ensure_model_parallel_initialized(parallel_config.tensor_parallel_size,
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/parallel_state.py", line 965, in ensure_model_parallel_initialized
    initialize_model_parallel(tensor_model_parallel_size,
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/parallel_state.py", line 931, in initialize_model_parallel
    _TP = init_model_parallel_group(group_ranks,
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/parallel_state.py", line 773, in init_model_parallel_group
    return GroupCoordinator(
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/parallel_state.py", line 154, in __init__
    self.pynccl_comm = PyNcclCommunicator(
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/device_communicators/pynccl.py", line 95, in __init__
    self.all_reduce(data)
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/device_communicators/pynccl.py", line 118, in all_reduce
    self.nccl.ncclAllReduce(buffer_type(tensor.data_ptr()),
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/device_communicators/pynccl_wrapper.py", line 257, in ncclAllReduce
    self.NCCL_CHECK(self._funcs["ncclAllReduce"](sendbuff, recvbuff, count,
  File "/opt/conda/envs/py_3.10/lib/python3.10/site-packages/vllm/distributed/device_communicators/pynccl_wrapper.py", line 223, in NCCL_CHECK
    raise RuntimeError(f"NCCL error: {error_str}")
RuntimeError: NCCL error: unhandled cuda error (run with NCCL_DEBUG=INFO for details)
ERROR 10-30 13:46:29 api_server.py:186] RPCServer process died before responding to readiness probe
`
In addition, I also tried to start it using fastchat, and the same problem occurred. As long as more than two GPU cards are configured, an error will be reported.

But I can test it normally using the following command: `python3 -m fastchat.serve.cli --model-path /data/llm_models/Qwen2.5-14B-Instruct --num-gpus 2 --gpus 0,1`
`<|im_start|>user: who a u?
<|im_start|>assistant: I'm an AI assistant named Qwen. I'm here to help you with a wide range of tasks, from answering questions and providing information to assisting with creative writing and problem-solving. How can I help you today?`
It doesn't run on both GPUs though:
```
# amd-smi process
GPU: 0
    PROCESS_INFO: No running processes detected

GPU: 1
    PROCESS_INFO:
        NAME: pt_main_thread
        PID: 1158888
        MEMORY_USAGE:
            GTT_MEM: 2.1 MB
            CPU_MEM: 69.2 MB
            VRAM_MEM: 28.8 GB
        MEM_USAGE: 28.9 GB
```

I have tried many methods, but none of them can run on more than two GPU cards. So I want to ask if there is any way to use fastChat or vllm to launch a large model on multiple AMD GPUs?

### Operating System

Docker Container NAME="Ubuntu" VERSION="22.04.4 LTS (Jammy Jellyfish)" 

### CPU

AMD Ryzen Threadripper PRO 7965WX 24-Cores

### GPU

Marketing Name:          AMD Radeon PRO W7900 Dual Slot            Name:                    amdgcn-amd-amdhsa--gfx1100

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

first: 
`docker run -ti --rm --device /dev/kfd --device /dev/dri -e HIP_VISIBLE_DEVICES=0,1 -e NCCL_CUMEM_ENABL=0 -v `pwd`/Qwen2.5-14B-Instruct:/data/llm_models/Qwen2.5-14B-Instruct ozziemoreno/rocm-vllm:ubuntu22.04_rocm6.2_py3.10_torch2.3.0_vllm0.6.0 bash`
then install fschat and pydantic（Even if it is not installed, an error will be reported if it is started directly through vllm serve）:
`
pip install  fschat==0.2.35 pydantic==2.1.1 
`
When you finally start it, you will get an error.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.8.5 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.14
Runtime Ext Version:     1.6
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen Threadripper PRO 7965WX 24-Cores
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper PRO 7965WX 24-Cores
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
  Max Clock Freq. (MHz):   6818                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    130613460(0x7c900d4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    130613460(0x7c900d4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    130613460(0x7c900d4) KB            
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
  Uuid:                    GPU-4958aa89e3e62111               
  Marketing Name:          AMD Radeon PRO W7900 Dual Slot     
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
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29770(0x744a)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1760                               
  BDFID:                   50176                              
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
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
  Packet Processor uCode:: 342                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-e78e352b64ac93f9               
  Marketing Name:          AMD Radeon PRO W7900 Dual Slot     
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
    L2:                      6144(0x1800) KB                    
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29770(0x744a)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1760                               
  BDFID:                   4096                               
  Internal Node ID:        2                                  
  Compute Unit:            96                                 
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
  Packet Processor uCode:: 342                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
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
*** Done ***     

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2024-10-31T15:29:17Z)

Hi @dotbalo, adding the `--tensor-parallel-size` flag is the correct way to launch vllm serve across multiple GPUs. I was able to run the Qwen model on your docker image with both `vllm serve "Qwen/Qwen2.5-14B-Instruct` and `vllm serve "Qwen/Qwen2.5-14B-Instruct" --tensor-parallel-size 2`. I do see some precedent on the NCCL error reported and it looks like updating the host's kernel driver resolved the issue. Could you please check that your kernel driver is up to date with the latest 6.2.2 packaged version, and upgrade it if necessary?

---

### 评论 #2 — harkgill-amd (2024-11-26T19:57:50Z)

Closing this issue due to lack of reply. Please leave a comment if you are still encountering the NCCL error and need assistance. Thanks.

---
