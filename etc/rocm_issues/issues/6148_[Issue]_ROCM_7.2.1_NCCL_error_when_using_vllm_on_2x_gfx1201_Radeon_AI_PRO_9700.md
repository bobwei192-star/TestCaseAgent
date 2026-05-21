# [Issue]: ROCM 7.2.1 NCCL error when using vllm on 2x gfx1201 Radeon AI PRO 9700

> **Issue #6148**
> **状态**: open
> **创建时间**: 2026-04-14T10:36:28Z
> **更新时间**: 2026-04-15T15:58:33Z
> **作者**: big-yellow-duck
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6148

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

Inference is does not work when using `tp 2` in the `rocm/vllm-dev:nightly` image as of 2026-04-14 

could be an nccl error as shown from the logs in `qwen3-0.6b-tp2.log` uploaded. 

when installing vllm main on `rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.9.1` 
by doing 

```bash
apt update && apt install -y cmake
pip install setuptools_scm
git clone https://github.com/vllm-project/vllm
cd vllm
python use_existing_torch.py 
pip install -e . --no-build-isolation
```

then running
## qwen3-0.6B-FP8
```python 
import os

from vllm import LLM, SamplingParams
from vllm.config.compilation import CompilationConfig, CUDAGraphMode


def main():
    os.environ["VLLM_LOGGING_LEVEL"] = "DEBUG"
    os.environ["VLLM_ROCM_USE_AITER"] = "0"

    llm = LLM(
        model="Qwen/Qwen3-0.6B-FP8",
        enforce_eager=True,
        tensor_parallel_size=2,
    )

    # Define a simple prompt
    prompts = [
        "Hello, my name is",
    ]

    # Sampling parameters - PUT BREAKPOINT HERE to see sampling config
    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.95,
        max_tokens=5,
    )

    # Run inference - PUT BREAKPOINT HERE to see generation
    # llm.start_profile()
    outputs = llm.generate(prompts, sampling_params)

    # llm.stop_profile()

    # Print results
    for output in outputs:
        print(f"Prompt: {output.prompt}")
        print(f"Generated: {output.outputs[0].text}")
        print("-" * 50)


if __name__ == "__main__":
    main()
```
## Qwen35-9B
```python
import os

from vllm import LLM, SamplingParams
from vllm.config.compilation import CompilationConfig, CUDAGraphMode


def main():
    os.environ["VLLM_LOGGING_LEVEL"] = "DEBUG"
    os.environ["VLLM_ROCM_USE_AITER"] = "0"
    llm = LLM(
        model="Qwen/Qwen3.5-9B",
        tensor_parallel_size=2,
        enforce_eager=True

    )

    # Define a chat conversation
    messages = [
        {"role": "user", "content": "do you want to build a snowman?"},
    ]

    # Sampling parameters - PUT BREAKPOINT HERE to see sampling config
    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.95,
        max_tokens=5,
    )

    # Run inference using chat() method with chat_template_kwargs to disable thinking
    # llm.start_profile()
    outputs = llm.chat(
        messages=messages,
        sampling_params=sampling_params,
        chat_template_kwargs={"enable_thinking": False},
    )

    # llm.stop_profile()

    # Print results
    for output in outputs:
        print(f"Prompt: {output.prompt}")
        print(f"Generated: {output.outputs[0].text}")
        print("-" * 50)


if __name__ == "__main__":
    main()

```

Its works on this image `rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.9.1`

[qwen35-9b-tp2-rocm7.2.0.log](https://github.com/user-attachments/files/26706652/qwen35-9b-tp2-rocm7.2.0.log)

[qwen3-0.6b-tp2-rocm7.2.0.log](https://github.com/user-attachments/files/26706588/qwen3-0.6b-tp2-rocm7.2.0.log)


### Operating System

Fedora Linux 43 (Workstation Edition)

### CPU

 Intel(R) Xeon(R) w7-3565X

### GPU

2x AMD Radeon AI PRO 9700

### ROCm Version

7.2.1

### ROCm Component

_No response_

### Steps to Reproduce

1. use `rocm/vllm-dev:nightly` (2026-04-14)
```bash
docker run -it \
    --network=host \
    --group-add=video \
    --ipc=host \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --device=/dev/kfd \
    --device=/dev/dri \
    --name my-vllm-nightly \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -e HF_HOME=/root/.cache/huggingface \
    rocm/vllm-dev:nightly \
    bash
```

2.  run a model with `tensor_parallel_size=2`
## qwen3.5-9B
```python
import os

from vllm import LLM, SamplingParams
from vllm.config.compilation import CompilationConfig, CUDAGraphMode


def main():
    os.environ["VLLM_LOGGING_LEVEL"] = "DEBUG"
    os.environ["VLLM_ROCM_USE_AITER"] = "0"
    llm = LLM(
        # model="Qwen/Qwen3.5-27B",
        model="Qwen/Qwen3.5-9B",
        tensor_parallel_size=2,
        enforce_eager=True,
    )

    # Define a chat conversation
    messages = [
        {"role": "user", "content": "do you want to build a snowman?"},
    ]

    # Sampling parameters - PUT BREAKPOINT HERE to see sampling config
    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.95,
        max_tokens=5,
    )

    # Run inference using chat() method with chat_template_kwargs to disable thinking
    # llm.start_profile()
    outputs = llm.chat(
        messages=messages,
        sampling_params=sampling_params,
        chat_template_kwargs={"enable_thinking": False},
    )

    # llm.stop_profile()

    # Print results
    for output in outputs:
        print(f"Prompt: {output.prompt}")
        print(f"Generated: {output.outputs[0].text}")
        print("-" * 50)


if __name__ == "__main__":
    main()
```

## qwen3-0.6B
```python
import os

from vllm import LLM, SamplingParams
from vllm.config.compilation import CompilationConfig, CUDAGraphMode


def main():
    os.environ["VLLM_LOGGING_LEVEL"] = "DEBUG"
    # use aiter
    os.environ["FLASH_ATTENTION_TRITON_AMD_ENABLE"] = "TRUE"
    os.environ["VLLM_ROCM_USE_AITER"] = "0"
    llm = LLM(
        # model="Qwen/Qwen3.5-27B",
        model="Qwen/Qwen3-0.6B",
        tensor_parallel_size=2,
        enforce_eager=True,
    )

    # Define a chat conversation
    messages = [
        {"role": "user", "content": "do you want to build a snowman?"},
    ]

    # Sampling parameters - PUT BREAKPOINT HERE to see sampling config
    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.95,
        max_tokens=5,
    )

    # Run inference using chat() method with chat_template_kwargs to disable thinking
    # llm.start_profile()
    outputs = llm.chat(
        messages=messages,
        sampling_params=sampling_params,
        chat_template_kwargs={"enable_thinking": False},
    )

    # llm.stop_profile()

    # Print results
    for output in outputs:
        print(f"Prompt: {output.prompt}")
        print(f"Generated: {output.outputs[0].text}")
        print("-" * 50)


if __name__ == "__main__":
    main()
```

[qwen35-9B-tp2.log](https://github.com/user-attachments/files/26706329/qwen35-9B-tp2.log)
[qwen3-0.6b-tp2.log](https://github.com/user-attachments/files/26706328/qwen3-0.6b-tp2.log)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[37mROCk module is loaded[0m
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
  Name:                    Intel(R) Xeon(R) w7-3565X          
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) w7-3565X          
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
  Max Clock Freq. (MHz):   4600                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            64                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    263538308(0xfb54684) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    263538308(0xfb54684) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    263538308(0xfb54684) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    263538308(0xfb54684) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-c3b0dd770fac0c9b               
  Marketing Name:                                             
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   21504                              
  Internal Node ID:        1                                  
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
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-e60c46980656b10b               
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
  BDFID:                   29184                              
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
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
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


### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — msembinelli (2026-04-14T21:57:45Z)

Seems like this could be related to what I'm also seeing here: https://github.com/ROCm/ROCm/issues/6074

---
