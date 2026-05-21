# [Issue]: Illegal seek for GPU arch : gfx1103 

> **Issue #2719**
> **状态**: closed
> **创建时间**: 2023-12-14T22:32:13Z
> **更新时间**: 2024-10-01T15:41:29Z
> **关闭时间**: 2024-10-01T15:41:29Z
> **作者**: deepankarsharma
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2719

## 描述

### Problem Description

I compiled llama.cpp with support for rocblas on Ubuntu 22.04. 

When I try to run llama.cpp I get the following error

>> sudo ~/llama.cpp/build/bin/main \
    -ngl 35 -m ~/llama.cpp/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf \
    --color -c 32768 --temp 0.7 --repeat_penalty 1.1 -n -1 \
    -p "<s>[INST] say hello to me in french [/INST]"

main: build = 1641 (6744dbe)
main: built with cc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0 for x86_64-linux-gnu
main: seed  = 1702592822

rocBLAS error: Cannot read /opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary.dat: Illegal seek for GPU arch : gfx1103
 List of available TensileLibrary Files : 
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx941.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx900.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx908.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx1102.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx90a.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx1101.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx1030.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx942.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx940.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx1100.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx906.dat"
"/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx803.dat"

### Operating System

22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 PRO 7940HS

### GPU

780M

### ROCm Version

5.7.0

### ROCm Component

rocBLAS

### Steps to Reproduce

Expect rocblas to work with gpu arch gfx1103

### Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    AMD Ryzen 9 PRO 7940HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 PRO 7940HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   4000                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65025468(0x3e035bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65025468(0x3e035bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65025468(0x3e035bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1103                            
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
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           9(0x9)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2799                               
  BDFID:                   49920                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
  Packet Processor uCode:: 33                                 
  SDMA engine uCode::      16                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1103         
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

---

## 评论 (7 条)

### 评论 #1 — danielzgtg (2023-12-15T06:50:15Z)

What does exist is `/opt/rocm-5.7.0/lib/rocblas/library/TensileLibrary_lazy_gfx1030.dat`.  Have you tried `sudo env HSA_OVERRIDE_GFX_VERSION=10.3.0 ~/llama.cpp/build/bin/main`?

---

### 评论 #2 — akostadinov (2024-02-19T13:50:57Z)

Maybe this thread gets you going?

https://github.com/ROCm/ROCm/discussions/2631#discussioncomment-7799697

---

### 评论 #3 — nartmada (2024-03-13T18:47:38Z)

Thanks @danielzgtg and @akostadinov for your input.
@deepankarsharma, any luck with Daniel or Aleksandar's suggestion?  

---

### 评论 #4 — deepankarsharma (2024-03-13T19:19:20Z)

@nartmada - I will give this a try soon and post an update. 

---

### 评论 #5 — badpaybad (2024-04-03T03:14:35Z)

mine same issues with laptop: AMD Ryzen 7 8845H w/ Radeon 780M Graphics

Can any one help me?

I tried many time with this guide line:

`https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/3rd-party/pytorch-install.html`

I created docker container 

`
https://github.com/badpaybad/Ner_Llm_Gpt/blob/main/mistralvn/dockerfile.base.rocm 
https://github.com/badpaybad/Ner_Llm_Gpt/blob/main/mistralvn/dockerfile 
`
run

`
docker run --user root --privileged -d --restart always -p 11111:8080 -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device=/dev/kfd --device=/dev/dri --group-add video --group-add render --ipc=host --shm-size 8G --name rocm_vistral7b_8880 rocm-vistral7b  
`
I got the error when run container 

`

2024-04-03 10:04:34 torch.cuda.is_available: False
2024-04-03 10:04:35 Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
Loading checkpoint shards:   0%|                                                                                     | 0/2 [00Loading checkpoint shards:   0%|                                                                                     | 0/2 [00:00<?, ?it/s]
2024-04-03 10:04:35 Traceback (most recent call last):
2024-04-03 10:04:35   File "/app/main.py", line 79, in <module>
2024-04-03 10:04:35     model = AutoModelForCausalLM.from_pretrained(
2024-04-03 10:04:35   File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/models/auto/auto_factory.py", line 563, in from_pretrained
2024-04-03 10:04:35     return model_class.from_pretrained(
2024-04-03 10:04:35   File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/modeling_utils.py", line 3531, in from_pretrained
2024-04-03 10:04:35     ) = cls._load_pretrained_model(
2024-04-03 10:04:35   File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/modeling_utils.py", line 3958, in _load_pretrained_model
2024-04-03 10:04:35     new_error_msgs, offload_index, state_dict_index = _load_state_dict_into_meta_model(
2024-04-03 10:04:35   File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/transformers/modeling_utils.py", line 812, in _load_state_dict_into_meta_model
2024-04-03 10:04:35     set_module_tensor_to_device(model, param_name, param_device, **set_module_kwargs)
2024-04-03 10:04:35   File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/accelerate/utils/modeling.py", line 387, in set_module_tensor_to_device
2024-04-03 10:04:35     new_value = value.to(device)
2024-04-03 10:04:35   File "/opt/conda/envs/py_3.9/lib/python3.9/site-packages/torch/cuda/__init__.py", line 298, in _lazy_init
2024-04-03 10:04:35     torch._C._cuda_init()
2024-04-03 10:04:35 RuntimeError: No HIP GPUs are available
2024-04-03 10:04:38 ____workingDir /app
2024-04-03 10:04:38 CUDA support: False (Should be "True")
2024-04-03 10:04:38 CUDA version: None (Should be "None")
2024-04-03 10:04:38 HIP version: 6.0.32830-d62f6a171 (Should contain value)
2024-04-03 10:04:38 device_type: cuda
`



---

### 评论 #6 — ppanchad-amd (2024-07-17T19:48:51Z)

@deepankarsharma Has this issue been resolved on your end? Thanks!

---

### 评论 #7 — ppanchad-amd (2024-10-01T15:41:29Z)

@deepankarsharma Closing ticket for now.  Please feel free to re-open this ticket if you still see the issue with the latest ROCm and we will further investigate. Thanks!

---
