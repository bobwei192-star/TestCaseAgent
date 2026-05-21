# [Feature]:  ROCm Using shared memory When GPU runs out of memory

> **Issue #3681**
> **状态**: closed
> **创建时间**: 2024-09-05T03:30:38Z
> **更新时间**: 2025-07-28T15:49:06Z
> **关闭时间**: 2025-07-28T15:49:06Z
> **作者**: void-Man
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3681

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

When I paint with ComfyUI, if the workflow is more complex, more models need to be loaded, or larger images are generated, there is a **HIP out of memory**, even if there is still enough space in shared memory at that point.
But when I switch to windows and run ComfyUI with zluda, I find that when the GPU runs out of memory, it will use shared memory to continue running instead of throwing a **HIP out of memory**, I would like to know if there is a plan to support the use of shared memory in subsequent releases.

### Operating System

Ubuntu

### GPU

RX 7900xtx

### ROCm Component

ROCm 6.2.0

---

## 评论 (9 条)

### 评论 #1 — harkgill-amd (2024-09-06T17:24:49Z)

Hi @void-Man, are you able to consistently reproduce this issue with a specific model? If so, could you please share the steps to reproduce the `HIP out of memory` error?

---

### 评论 #2 — void-Man (2024-09-10T15:34:50Z)

> Hi @void-Man, are you able to consistently reproduce this issue with a specific model? If so, could you please share the steps to reproduce the `HIP out of memory` error?

Hi @harkgill-amd, thank you for your reply. After my many attempts, I found that I can't reproduce **OOM** on rx 7900xtx, but I still have a rx 7900 GRE, after testing, I can reproduce OOM stably on 7900 GRE, here is the relevant information and reproduction steps

**Operating System**
Ubuntu 22.04

**GPU**
RX 7900 GRE

**Total system memory**
80Gb

**ROCm Component**
ROCm 6.1

**ComfyUI Args**
```
--listen --use-quad-cross-attention --disable-xformers  --dont-upcast-attention 
```

**ROCm Info**
```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.13
Runtime Ext Version:     1.4
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
  Name:                    AMD Ryzen 7 3700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 3700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   3600                               
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
      Size:                    82310348(0x4e7f4cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    82310348(0x4e7f4cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    82310348(0x4e7f4cc) KB             
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
  Uuid:                    GPU-87b9f433f48ca72b               
  Marketing Name:          Radeon RX 7900 GRE                 
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
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1927                               
  BDFID:                   10240                              
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      19                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
```

**Steps to Reproduction with ROCm on Ubuntu**
1. run comfyUI with this workflow（Maybe require the installation of related plug-ins）
[workflow.json](https://github.com/user-attachments/files/16947015/workflow.json)
2. By the time you run vae decode, the following error occurs, even at this point, I have 50G of unused system memory.
```
!!! Exception during processing !!! HIP out of memory. Tried to allocate 2.25 GiB. GPU 0 has a total capacity of 15.98 GiB of which 1.09 GiB is free. Of the allocated memory 13.80 GiB is allocated by PyTorch, and 615.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
Traceback (most recent call last):
  File "/home/safendaga/ComfyUI/execution.py", line 317, in execute
    output_data, output_ui, has_subgraph = get_output_data(obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb)
  File "/home/safendaga/ComfyUI/execution.py", line 192, in get_output_data
    return_values = _map_node_over_list(obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb)
  File "/home/safendaga/ComfyUI/execution.py", line 169, in _map_node_over_list
    process_inputs(input_dict, i)
  File "/home/safendaga/ComfyUI/execution.py", line 158, in process_inputs
    results.append(getattr(obj, func)(**inputs))
  File "/home/safendaga/ComfyUI/nodes.py", line 298, in decode
    return (vae.decode_tiled(samples["samples"], tile_x=tile_size // 8, tile_y=tile_size // 8, ), )
  File "/home/safendaga/ComfyUI/comfy/sd.py", line 341, in decode_tiled
    output = self.decode_tiled_(samples, tile_x, tile_y, overlap)
  File "/home/safendaga/ComfyUI/comfy/sd.py", line 290, in decode_tiled_
    (comfy.utils.tiled_scale(samples, decode_fn, tile_x // 2, tile_y * 2, overlap, upscale_amount = self.upscale_ratio, output_device=self.output_device, pbar = pbar) +
  File "/home/safendaga/ComfyUI/comfy/utils.py", line 761, in tiled_scale
    return tiled_scale_multidim(samples, function, (tile_y, tile_x), overlap, upscale_amount, out_channels, output_device, pbar)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/utils/_contextlib.py", line 116, in decorate_context
    return func(*args, **kwargs)
  File "/home/safendaga/ComfyUI/comfy/utils.py", line 735, in tiled_scale_multidim
    ps = function(s_in).to(output_device)
  File "/home/safendaga/ComfyUI/comfy/sd.py", line 288, in <lambda>
    decode_fn = lambda a: self.first_stage_model.decode(a.to(self.vae_dtype).to(self.device)).float()
  File "/home/safendaga/ComfyUI/comfy/ldm/models/autoencoder.py", line 200, in decode
    dec = self.decoder(dec, **decoder_kwargs)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1553, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1562, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/safendaga/ComfyUI/comfy/ldm/modules/diffusionmodules/model.py", line 639, in forward
    h = self.up[i_level].upsample(h)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1553, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1562, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/safendaga/ComfyUI/comfy/ldm/modules/diffusionmodules/model.py", line 72, in forward
    x = self.conv(x)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1553, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1562, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/safendaga/ComfyUI/comfy/ops.py", line 106, in forward
    return super().forward(*args, **kwargs)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/conv.py", line 458, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/home/safendaga/miniconda3/envs/cfy/lib/python3.10/site-packages/torch/nn/modules/conv.py", line 454, in _conv_forward
    return F.conv2d(input, weight, bias, self.stride,
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 2.25 GiB. GPU 0 has a total capacity of 15.98 GiB of which 1.09 GiB is free. Of the allocated memory 13.80 GiB is allocated by PyTorch, and 615.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

Got an OOM, unloading all loaded models.
```

Strangely enough, with the same hardware configuration, startup parameters and workflow, when I switch to windows to run comfyUI with zluda, it doesn't OOM, it just takes longer to run. After observing the system resource monitor, I found that when zluda runs under windows, when there is not enough video memory, it will use the shared memory to continue to run, instead of just OOM!
I'd like to ask if it's because of my configuration, or differences between Linux ROCm and Zluda causing this problem?
- If there is a configuration problem, please tell me the correct configuration.
- If it's the difference between Linux ROCm and Zluda, in the subsequent plans for ROCm, will it be possible to implement a function similar to zluda on windows

If need any additional information, please contact me to add it!

---

### 评论 #3 — hartmark (2024-12-08T23:12:36Z)

I have the same issue, I have 64 GB system ram that sits there unused :(

---

### 评论 #4 — Schwenn2002 (2024-12-22T16:28:39Z)

the same issue:

System:
CPU AMD Ryzen 9950X
RAM 128 GB DDR5
GPU0 AMD Radeon PRO W7900
GPU1 AMD Radeon RX7900XTX
ROCM: 6.3.1
Ubuntu 24.04 LTS (currently patched)

In a multi-GPU setup, only the VRAM of one graphics card is used, the 128GB are not used by ollama (with ROCm) and only an error message: Out of Memory is given.

https://github.com/ollama/ollama/issues/8206




---

### 评论 #5 — tcgu-amd (2025-07-24T18:44:40Z)

Hi @void-Man, can you try running your workload with lowvram mode?

Automatically using shared memory when on device memory is insufficient should by no means be a responsibility of ROCm. There is no magic, as whenever shared memory is used, there will be a performance degradation, and we generally do not want to silently introduce a performance degradation at the runtime level. Rather, the user should be informed when device memory is not sufficient via an OOM error, and they could choose what to do in that case. 

In fact, hipMalloc(), which is the API used under the hood to allocate device memory, should always return OOM error if there is not enough memory on device. We actually provide another API, hipMallocManaged() to allow mixed use of both device and host memory, at a non-trivial performance cost. Choosing when to use which API appropriately should be a responsibility of a higher-level framework (e.g. PyTorch and above). 

In your case, choosing when to use shared vs device memory should be managed by ComfyUI itself. This is actually exactly what happens: before an allocation, ComfyUI will calculate the required amount of memory and available memory on the system, and then decide how to use the memory. When you see the OOM error, it is already after ComfyUI has made a decision to allocate on device, and ROCm was just following the orders. An example is here https://github.com/comfyanonymous/ComfyUI/blob/eb2f78b4e09b1970e2fc51fc5d2e062f1a826399/comfy/sd.py#L582, where you can see ComfyUI actually catching the OOM. Another instance is here https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/model_management.py#L618C28-L618C39, where ComfyUI tries to free memory before loading a model if there's not enough memory. 

However, based on your log, OOM actually occurred here https://github.com/comfyanonymous/ComfyUI/blob/d03ae077b4330f58e7caba53ff94e7fd58d0dc7d/comfy/sd.py#L509, which apparently incurs a significant memory cost that is not accounted for by comfyUI. This is a bug on ComfyUI's part, as it should have ensured there will be enough VRAM, but it didn't. 

tl;dr I would say this is rather a ComfyUI issue rather than a ROCm one. As to why different device/platforms may or may not exhibit this issue, it is probably because they way cache was managed and sometimes memory primitives are handled differently, which let ComfyUI get away with miscalculations sometimes. Either fixing on ComfyUI's side or run your workload with lowvram mode, which will allow ComfyUI to use a more reserved memory handling strategy, are better solutions for this issue in my opinion. 

---

### 评论 #6 — tcgu-amd (2025-07-25T14:31:06Z)

@void-Man A bit of additional context, the reason why on windows shared memory is automatically used seems to be a feature of the windows graphics driver as per this post (https://stackoverflow.com/questions/77321986/cudamalloc-not-allocating-to-shared-gpu-memory-on-ampere-micro-architectures-in). As such, Linux support is unlikely, at least not anytime soon. 

---

### 评论 #7 — hartmark (2025-07-25T22:51:09Z)

I have created an issue on ComfyUI, please add more details of you have any

@void-Man 

---

### 评论 #8 — void-Man (2025-07-28T09:58:28Z)

Get it, thank you very much!




------------------&nbsp;原始邮件&nbsp;------------------
发件人:                                                                                                                        "ROCm/ROCm"                                                                                    ***@***.***&gt;;
发送时间:&nbsp;2025年7月25日(星期五) 凌晨2:45
***@***.***&gt;;
***@***.******@***.***&gt;;
主题:&nbsp;Re: [ROCm/ROCm] [Feature]:  ROCm Using shared memory When GPU runs out of memory (Issue #3681)



tcgu-amd left a comment (ROCm/ROCm#3681)
 
Hi @void-Man, can you try running your workload with lowvram mode?
 
Automatically using shared memory when on device memory is insufficient should by no means be a responsibility of ROCm. There is no magic, as whenever shared memory is used, there will be a performance degradation, and we generally do not want to silently introduce a performance degradation at the runtime level. Rather, the user should be informed when device memory is not sufficient via an OOM error, and they could choose what to do in that case.
 
In fact, hipMalloc(), which is the API used under the hood to allocate device memory, should always return OOM error if there is not enough memory on device. We actually provide another API, hipMallocManaged() to allow mixed use of both device and host memory, at a non-trivial performance cost. Choosing when to use which API appropriately should be a responsibility of a higher-level framework (e.g. PyTorch and above).
 
In your case, choosing when to use shared vs device memory should be managed ComfyUI itself. This is actually exactly what happens: before an allocation, ComfyUI will calculate the required amount of memory and available memory on the system, and then decide how to use the memory. When you see the OOM error, it is already after ComfyUI has made a decision to allocate on device, and ROCm was just following the orders. An example is here https://github.com/comfyanonymous/ComfyUI/blob/eb2f78b4e09b1970e2fc51fc5d2e062f1a826399/comfy/sd.py#L582, where you can see ComfyUI actually catching the OOM. Another instance is here https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/model_management.py#L618C28-L618C39, where ComfyUI tries to free memory before loading a model if there's not enough memory.
 
However, based on your log, OOM actually occurred here https://github.com/comfyanonymous/ComfyUI/blob/d03ae077b4330f58e7caba53ff94e7fd58d0dc7d/comfy/sd.py#L509, which apparently incurs a significant memory cost that is not accounted for by comfyUI. This is a bug on ComfyUI's part, as it should have ensured there will be enough VRAM, but it didn't.
 
tl;dr I would say this is rather a ComfyUI issue rather than a ROCm one. As to why different device/platforms may or may not exhibit this issue, it is probably because they way cache was managed and sometimes memory primitives are handled differently, which lets ComfyUI get's away with miscalculations sometimes. Either fixing on ComfyUI's side or run your workload with lowvram mode, which will allow ComfyUI to use a more reserved memory handling strategy are better solutions for this issue.
 
—
Reply to this email directly, view it on GitHub, or unsubscribe.
You are receiving this because you were mentioned.Message ID: ***@***.***&gt;

---

### 评论 #9 — tcgu-amd (2025-07-28T15:49:06Z)

Hi @hartmark, @void-Man, I will be closing this issue for now since there is no action item for ROCm. Please feel free to follow up with more questions though, we will be happy to help answer them. Thanks! 

---
