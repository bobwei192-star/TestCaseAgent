# [Issue]: "HIP error - no kernel image is available for execution on the device "  when trying to use 2nd GPU. 

> **Issue #3518**
> **状态**: closed
> **创建时间**: 2024-08-05T01:04:17Z
> **更新时间**: 2024-09-14T01:40:43Z
> **关闭时间**: 2024-09-14T01:40:43Z
> **作者**: nktice
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3518

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

New ROCm 6.2 appears to not support the use of multiple GPUs, giving the following error when such actions are attempted.   "HIP error: no kernel image is available for execution on the device" 
This is a regression from 6.1.3 where these features were working. 


### Operating System

NAME="Ubuntu" VERSION="24.04 LTS (Noble Numbat)"

### CPU

model name	: AMD Ryzen 9 5950X 16-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIP

### Steps to Reproduce

I maintain this guide, it has install instructions to get Stable Diffusion and Oobabooga's TextGenerationWebUI working on AMD's GPUs. These are the instructions I follow to setup my own system.  
https://github.com/nktice/AMD-AI/
I recently updated to make use of the new ROCm 6.2, and have discovered an error that appears when I try to use the 2nd of my 2 GPUs.  This issue did not arise with 6.1.3.  

# Stable Diffusion : 
In order to get this working, I have until now had to include this command in the configuration in order to have it disable access to one of the two cards 
```
export CUDA_VISIBLE_DEVICES="1" 
```
With ROCm 6.2, it crashes as follows with it, but runs normally without it. 
```bash
Traceback (most recent call last):
  File "/usr/lib/python3.10/threading.py", line 973, in _bootstrap
    self._bootstrap_inner()
  File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.10/threading.py", line 953, in run
    self._target(*self._args, **self._kwargs)
  File "/home/n/stable-diffusion-webui/modules/initialize.py", line 149, in load_model
    shared.sd_model  # noqa: B018
  File "/home/n/stable-diffusion-webui/modules/shared_items.py", line 175, in sd_model
    return modules.sd_models.model_data.get_sd_model()
  File "/home/n/stable-diffusion-webui/modules/sd_models.py", line 693, in get_sd_model
    load_model()
  File "/home/n/stable-diffusion-webui/modules/sd_models.py", line 845, in load_model
    load_model_weights(sd_model, checkpoint_info, state_dict, timer)
  File "/home/n/stable-diffusion-webui/modules/sd_models.py", line 440, in load_model_weights
    model.load_state_dict(state_dict, strict=False)
  File "/home/n/stable-diffusion-webui/modules/sd_disable_initialization.py", line 223, in <lambda>
    module_load_state_dict = self.replace(torch.nn.Module, 'load_state_dict', lambda *args, **kwargs: load_state_dict(module_load_state_dict, *args, **kwargs))
  File "/home/n/stable-diffusion-webui/modules/sd_disable_initialization.py", line 221, in load_state_dict
    original(module, state_dict, strict=strict)
  File "/home/n/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 2548, in load_state_dict
    load(self, state_dict)
  File "/home/n/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 2536, in load
    load(child, child_state_dict, child_prefix)  # noqa: F821
  File "/home/n/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 2536, in load
    load(child, child_state_dict, child_prefix)  # noqa: F821
  File "/home/n/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 2536, in load
    load(child, child_state_dict, child_prefix)  # noqa: F821
  [Previous line repeated 1 more time]
  File "/home/n/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/nn/modules/module.py", line 2519, in load
    module._load_from_state_dict(
  File "/home/n/stable-diffusion-webui/modules/sd_disable_initialization.py", line 225, in <lambda>
    linear_load_from_state_dict = self.replace(torch.nn.Linear, '_load_from_state_dict', lambda *args, **kwargs: load_from_state_dict(linear_load_from_state_dict, *args, **kwargs))
  File "/home/n/stable-diffusion-webui/modules/sd_disable_initialization.py", line 191, in load_from_state_dict
    module._parameters[name] = torch.nn.parameter.Parameter(torch.zeros_like(param, device=device, dtype=dtype), requires_grad=param.requires_grad)
  File "/home/n/stable-diffusion-webui/venv/lib/python3.10/site-packages/torch/_meta_registrations.py", line 4820, in zeros_like
    res.fill_(0)
RuntimeError: HIP error: no kernel image is available for execution on the device
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

# With Oobabooga's TextGenerationWebUI : 
Works normally when I am using just one video card... when I try to load something that would make use of the 2nd card, I get a similar error... 
```bash
Traceback (most recent call last):
  File "/home/n/text-generation-webui/modules/ui_model_menu.py", line 231, in load_model_wrapper
    shared.model, shared.tokenizer = load_model(selected_model, loader)
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/n/text-generation-webui/modules/models.py", line 93, in load_model
    output = load_func_map[loader](model_name)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/n/text-generation-webui/modules/models.py", line 303, in ExLlamav2_loader
    model, tokenizer = Exllamav2Model.from_pretrained(model_name)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/n/text-generation-webui/modules/exllamav2.py", line 72, in from_pretrained
    model.load_autosplit(cache)
  File "/home/n/miniconda3/envs/textgen/lib/python3.11/site-packages/exllamav2/model.py", line 484, in load_autosplit
    for item in f:
  File "/home/n/miniconda3/envs/textgen/lib/python3.11/site-packages/exllamav2/model.py", line 578, in load_autosplit_gen
    cache.update_cache_tensors()
  File "/home/n/miniconda3/envs/textgen/lib/python3.11/site-packages/exllamav2/cache.py", line 123, in update_cache_tensors
    p_key_states = torch.zeros(self.shape_wk, dtype = self.dtype, device = v).contiguous()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: no kernel image is available for execution on the device
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```
I have tried running with those parameters, alas they don't reveal any meaningful details.  


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
  Name:                    AMD Ryzen 9 5950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5950X 16-Core Processor
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
  Max Clock Freq. (MHz):   3400                               
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
      Size:                    65747228(0x3eb391c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65747228(0x3eb391c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65747228(0x3eb391c) KB             
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
  Uuid:                    GPU-[REDACTED]    
  Marketing Name:          Radeon RX 7900 XTX                 
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
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2431                               
  BDFID:                   3072                               
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
  Packet Processor uCode:: 232                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
  Uuid:                    GPU-[REDACTED]
  Marketing Name:          Radeon RX 7900 XTX                 
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
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2431                               
  BDFID:                   3840                               
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
  Packet Processor uCode:: 232                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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

Note that I've selected 6.1 as a version in the options here, because 6.2 is not listed yet, and such selection is required to submit.  Please correct this too.  

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2024-08-08T18:56:25Z)

Hi @nktice, thank you providing your install instructions. An internal ticket has been created to further investigate this issue.

---

### 评论 #2 — jamesxu2 (2024-09-12T18:16:03Z)

Hi @nktice , I've been following your install instructions and I cannot reproduce the issue. The model generates successfully regardless of whether I set ```CUDA_VISIBLE_DEVICES=1``` or not, and I can verify through ```rocm-smi```  that the specified GPU is being loaded.

Config: Ubuntu 24.04 + ROCm 6.2 with 2@RX7900XTX 


Note that in your install instructions, the torch command you specify installs a pytorch build for ROCm 6.1 (https://github.com/nktice/AMD-AI/?tab=readme-ov-file#edit-environment-settings)

Please try installing a pytorch build for ROCm 6.2 and let me know what happens. 
```export TORCH_COMMAND="pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.2/"```
(ref: [Baremetal Pytorch Wheel Install Instructions for ROCm 6.2 ](https://rocm.docs.amd.com/projects/install-on-linux/en/develop/install/3rd-party/pytorch-install.html#using-a-wheels-package))

I did try downgrading to the Pytorch+rocm6.1 build and noticed some system instability and occasional hangs, so this may be the cause of the issue. I have not however encountered the "no kernel image" issue in my testing.

Another note is that the default model installed with the stable diffusion webui from RunwayML was [taken down](https://www.reddit.com/r/StableDiffusion/comments/1f4epto/runway_took_down_15_and_15_inpainting/) in recent days (though it seems to be back now?) so I installed a different model, but I think this is probably irrelevant to the case.


---

### 评论 #3 — nktice (2024-09-14T01:40:43Z)

Thanks for your reply.  Appreciate that you took time to respond.  

It does appear now multi-gpu works fine with ver 6.2. 
I think my report was from the very start of 6.2's release, before PyTorch had specific support for it, so it does make sense, these issues resolved with further development.  Wonderful to see. 
I'll be updating my guide(s) to reflect changes to the new versions.  [ It's complicated by kernel version issues that need work around... ] 

---
