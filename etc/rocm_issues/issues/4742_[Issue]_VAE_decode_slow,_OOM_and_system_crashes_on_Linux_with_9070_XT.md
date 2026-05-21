# [Issue]: VAE decode slow, OOM and system crashes on Linux with 9070 XT

> **Issue #4742**
> **状态**: closed
> **创建时间**: 2025-05-15T08:54:20Z
> **更新时间**: 2026-01-05T15:49:03Z
> **关闭时间**: 2025-06-09T14:37:56Z
> **作者**: zeFresk
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4742

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

When using  ComfyUI with any parameters with any workflow, you should get OOM or complete system crashes if using the standard VAEDecode node, same with the tiled decoder. Even 64x64 tiled decoder can result in crashes, but less frequently.

I could mitigate this by forcing all models but the VAE to unload, but even in that case, I get a lot of full system crashes and OOM. Sometimes, running the same workflow 2-3 times works...

Using --cpu-vae works but should not have to be used IMO.

I tried using torch 2.7 with ROCm 6.3, but I got the same issues. Before posting, I also read https://github.com/ROCm/ROCm/issues/4729 and https://github.com/ROCm/ROCm/issues/4443, but I believe this should be an issue on its own, as stated in https://github.com/ROCm/ROCm/issues/4729, because this is not limited to WSL.

EDIT: I could reproduce the crash, but I noticed nvtop reporting my GPU using PCIe 5.0x8, I will try to fix that and report back.
EDIT2: Switching to 5.0x16 improved loading times, but did not fix the error.
EDIT3: for t2v, --cpu-vae can be faster than tiled vae on the GPU.

I will update with comfyUI logs.

### Operating System

Arch Linux (6.14.6-arch1-1)

### CPU

AMD Ryzen 9 9950X3D 16-Core Processor

### GPU

AMD Radeon 9070 XT

### ROCm Version

6.4

### ROCm Component

_No response_

### Steps to Reproduce

- Install ROCm 6.4 on a fresh Arch Linux install from [opencl-amd-dev](https://aur.archlinux.org/packages/opencl-amd-dev), 
- Install pytorch for ROCm 6.4 from https://pytorch.org/get-started/locally/,
- Install latest version of ComfyUI and download required models,
- Launch ComfyUI with any parameters (I tried a lot of combination, none solve the problem, maybe ` TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 PYTORCH_HIP_ALLOC_CONF=expandable_segments:True micromamba run -n comfyui python main.py --use-pytorch-cross-attention --lowvram` is a bit better? still OOM and crashes)
- Try any workflow, I could reproduce this for text2video with Hunyuan and all the text2image with Flux.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    AMD Ryzen 9 9950X3D 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 9950X3D 16-Core Processor
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
  Max Clock Freq. (MHz):   5756                               
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
      Size:                    96337528(0x5bdfe78) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    96337528(0x5bdfe78) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    96337528(0x5bdfe78) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    96337528(0x5bdfe78) KB             
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
  Uuid:                    GPU-48cef9f706c81cb8               
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2400                               
  BDFID:                   768                                
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 1012                               
  SDMA engine uCode::      838                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5056(0x13c0)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   30208                              
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 22                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    48168764(0x2deff3c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    48168764(0x2deff3c) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic 
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

### Additional Information

When the system crashes, this is an example of one `journalctl -k -b -1`:
```
amdgpu 0000:03:00.0: amdgpu: 000000009f89a48b pin failed
 [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
 amdgpu 0000:03:00.0: amdgpu: 000000000c9ee1f9 pin failed
 [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
 [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
 [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
 amdgpu 0000:03:00.0: amdgpu: 00000000b1a398a4 pin failed
 [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
 amdgpu 0000:03:00.0: amdgpu: 000000002d5ba482 pin failed
 [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
 amdgpu 0000:03:00.0: amdgpu: 0000000080f7bf1c pin failed
 [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
 amdgpu 0000:03:00.0: amdgpu: 000000000c9ee1f9 pin failed
 [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* Failed to pin framebuffer with error -12
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc firefox(2852) task firefox:cs0(2770) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc plasma-systemmo(4082) task plasma-sys:cs0(4078) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc Xorg(1010) task Xorg:cs0(987) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc plasmashell(1362) task plasmashel:cs0(1342) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc Xwayland(1233) task Xwayland:cs0(1218) is non-zero when fini
 amdgpu 0000:03:00.0: amdgpu: VM memory stats for proc kwin_wayland(1163) task kwin_wayla:cs0(1116) is non-zero when fini
```

ComfyUI logs:
```
!!! Exception during processing !!! Allocation on device 
Traceback (most recent call last):
  File "/home/zefresk/Documents/ComfyUI/execution.py", line 349, in execute
    output_data, output_ui, has_subgraph = get_output_data(obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb)
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/execution.py", line 224, in get_output_data
    return_values = _map_node_over_list(obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/execution.py", line 196, in _map_node_over_list
    process_inputs(input_dict, i)
  File "/home/zefresk/Documents/ComfyUI/execution.py", line 185, in process_inputs
    results.append(getattr(obj, func)(**inputs))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/nodes.py", line 1598, in decode
    video = vae.decode(
            ^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/diffusers/utils/accelerate_utils.py", line 46, in wrapper
    return method(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/autoencoder_kl_causal_3d.py", line 345, in decode
    decoded = self._decode(z).sample
              ^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/autoencoder_kl_causal_3d.py", line 309, in _decode
    return self.temporal_tiled_decode(z, return_dict=return_dict)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/autoencoder_kl_causal_3d.py", line 536, in temporal_tiled_decode
    decoded = self.spatial_tiled_decode(
              ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/autoencoder_kl_causal_3d.py", line 462, in spatial_tiled_decode
    decoded = self.decoder(tile)
              ^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1755, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1766, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/vae.py", line 299, in forward
    sample = up_block(sample, latent_embeds)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1755, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1766, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/unet_causal_3d_blocks.py", line 795, in forward
    hidden_states = upsampler(hidden_states)
                    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1755, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1766, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/unet_causal_3d_blocks.py", line 194, in forward
    hidden_states = self.conv(hidden_states)
                    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1755, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1766, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/Documents/ComfyUI/custom_nodes/comfyui-hunyuanvideowrapper/hyvideo/vae/unet_causal_3d_blocks.py", line 78, in forward
    return self.conv(x)
           ^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1755, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1766, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/conv.py", line 725, in forward
    return self._conv_forward(input, self.weight, self.bias)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zefresk/.local/share/mamba/envs/comfyui/lib/python3.12/site-packages/torch/nn/modules/conv.py", line 720, in _conv_forward
    return F.conv3d(
           ^^^^^^^^^
torch.OutOfMemoryError: Allocation on device 

Got an OOM, unloading all loaded models.
```

---

## 评论 (10 条)

### 评论 #1 — ppanchad-amd (2025-05-15T16:13:25Z)

Hi @zeFresk. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — OrsoEric (2025-05-17T08:43:26Z)

I did additional testing, I report here too since it's a linked issue (https://github.com/ROCm/ROCm/issues/4729#issuecomment-2888209739)

- Adrenaline 25.5.1
- WSL
- Ubuntu 22.04
- Python 3.12
- UV portable environment

Tests:

- ROCm 6.3 + default MIOPEN_FIND_MODE : VAE decode driver timeout above 1024px
- ROCm 6.3.4 + default MIOPEN_FIND_MODE : VAE decode driver timeout above 1024px
- ROCm 6.3 + MIOPEN_FIND_MODE=2 : VAE decode works fine at 2048px
- ROCm 6.3.4 + MIOPEN_FIND_MODE=2 : VAE decode works fine at 2048px


---

### 评论 #3 — tcgu-amd (2025-05-26T14:33:01Z)

Hi @zeFresk, thanks for reaching out! I am sorry that you are experiencing issues with ROCm on our 9070XT hardware. We will try to reproduce your issue on our end and see what we can do. Thanks! 

---

### 评论 #4 — zeFresk (2025-06-01T09:33:58Z)

Hi, by compiling a lot of information in multiple threads I was able to considerably mitigate this issue.

**Most importantly**, using @kasper93 bfloat16 fix improved things a lot. Using some environment variables also helped a lot in boosting performance, reducing OOM and limiting crashes.

For people with the same problem, here is the launch script I'm running:
```
export PYTHONPATH=/opt/rocm/lib:$PYTHONPATH
export MIGRAPHX_MLIR_USE_SPECIFIC_OPS="attention"
export PYTORCH_TUNABLEOP_ENABLED=1
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export MIOPEN_FIND_MODE=2
export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True

python main.py --use-pytorch-cross-attention
```


---

### 评论 #5 — tcgu-amd (2025-06-04T17:34:37Z)

Hi @zeFresk, glad that you were able to find a temporary workaround, and I am sorry for the delayed update. I tried to reproduce the issue on a ubuntu system using your instructions, and even without the workaround, things did seem to work as intended, at least with flux-dev at default 1024px. However, we did managed to get the OOM issue with image size at 2048 px. We also noticed a slow down in prompt completion time compared using a 7900XT card. However, since the two systems we tested on do have different variations other than graphics cards, more tests would be needed in order to determine if this is an actual performance regression. 

In the mean time, it would help with the investigation if you could reproduce your problematic runs with `export MIOPEN_LOG_LEVEL=5`, which can show what stage MIOPEN was stuck in before the crash. 

Please keep in mind that the Arch ROCm repo is not maintained by us. This issue, specifically the crash and OOM part, could potentially be a result of the discrepancy between the Arch and official ROCm versions. In any case, the MIOpen Logs should be able to helps us search for the root cause. 

Thanks! 

---

### 评论 #6 — tcgu-amd (2025-06-09T14:33:44Z)

@zeFresk, some update after further investigation. I was able to reproduce the OOM issue after repeatedly running the same default flux-dev workload without stopping the server. After stepping through the source code and profiling the memory, the issue seems to be characteristic of an memory fragmentation issue, since in all case the the pytorch reserved memory - allocated memory + the system free memory is greater than the required memory, but allocation still fail. This is probably why using `export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True` was suggested as one of the fixes. However, this option can only mitigate the issue to some extent. 

To actually fix the issue, you would need to use @kasper's https://github.com/comfyanonymous/ComfyUI/pull/8289, as you mentioned, or manually clear pytorch cache between subsequent decodes. With these solutions applied, the speed of generation on 9070xt appears to be consistent with 7900xt. 

Since both solutions needs to be applied on ComfyUI's side, I will be closing this issue on ROCm for now. However, please feel free to follow up if you encounter further issues. 

Thanks! 

---

### 评论 #7 — kasper93 (2025-06-09T18:04:39Z)

For the record, I think ROCm is also responsible for performance degradation in convolution workloads, because of missing Winograd solvers for gfx12 https://github.com/ROCm/MIOpen/issues/3750 I've seen micro benchmarks where mobile gfx1151 is 3 times faster than gfx1201. Hopefully once those are bring up for gfx1201 we will see performance parity with older architectures.

---

### 评论 #8 — markg85 (2025-08-05T20:17:08Z)

This definitely is still an issue, even with the fixes from @kasper93 

I have a 7900XT here and i applied all these fixes along with a default `Flux.1 Krea Dev` workflow (it loads an fp8 model). The default resolution is 1024x1024. With all these fixes applied the first run is - though freaking slow at ~121 seconds - runs without a warning. The second run (literally just pressing `Run` again gives the dreaded `Warning: Ran out of memory when regular VAE decoding, retrying with tiled VAE decoding.`.

I'm running on the docker rocm pytorch latest from today.

I did notice one thing though.
Preview images. If you don't have them at all then it all seems to work but complains a bit.
If you enable them as **TAESD** (the slow method) then your first generation works just fine. The second one will, as soon as it goes into the `VAE Decode` step, crash.

```
torch.OutOfMemoryError: HIP out of memory. Tried to allocate 1.12 GiB. GPU 0 has a total capacity of 19.98 GiB of which 32.00 MiB is free. Of the allocated memory 18.09 GiB is allocated by PyTorch, and 1.43 GiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_HIP_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
```

Setting `PYTORCH_HIP_ALLOC_CONF=expandable_segments:True` won't help one thing. It will crash on the second run.

---

### 评论 #9 — Taikakim (2025-12-07T22:29:26Z)

Just chipping in here with a similar experience with Stable Audio Tools: with a RX 9070 XT, VAE decoding takes forever unless I prepend with MIOPEN_FIND_MODE=2 

Using that, the decoding is practically instantaneous.

I'm running EndeavourOS, RoCM 7.11

---

### 评论 #10 — RadeonVega-56 (2026-01-05T13:35:48Z)

Setting export PYTORCH_TUNABLEOP_ENABLED=1 before running comfyui results in a slow image generation and slow vae encoding. That option triggers the internal performance tuning option in pytorch as mentioned here: https://docs.pytorch.org/docs/stable/cuda.tunable.html.  It results in a long run for image and vae. A table gets written in the comfyui folder: tunableop_results0.csv.

Removing that option from the startup script after it had ran once in that slow mode results in faster image generation and faster vae decoding. You only need to generate ONE image using that variable, then stop comfyui, unset PYTORCH_TUNABLEOP_ENABLED=1 and generate FAST.

If performance is still bad and you get OOM set these in your comfyui launch script, **##all those paths below are set for NOBARA/FEDORA LINUX 43## use your own paths for your installed distribution.**:



export CMAKE_PREFIX_PATH="${VIRTUAL_ENV}:${CMAKE_PREFIX_PATH}"

export HIP_VISIBLE_DEVICES=0
export ROCM_VISIBLE_DEVICES=0
export HIP_TARGET="gfx1201"
export PYTORCH_ROCM_ARCH="gfx1201"
export TORCH_HIP_ARCH_LIST="gfx1201"
export HCC_AMDGPU_TARGET="gfx1201"
export PYTORCH_ROCM_ARCH="gfx1201"

export MESA_LOADER_DRIVER_OVERRIDE=amdgpu
export RADV_PERFTEST="aco,nggc,sam"

export PYTORCH_HIP_ALLOC_CONF="max_split_size_mb:6144,garbage_collection_threshold:0.85"
export PYTORCH_HIP_FREE_MEMORY_THRESHOLD_MB=128

export TORCH_COMPILE=0

export TORCH_BLAS_PREFER_HIPBLASLT=1
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS="CK,TRITON,ROCBLAS"
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_SEARCH_SPACE="BEST"
export TORCHINDUCTOR_FORCE_FALLBACK=1

export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
export FLASH_ATTENTION_TRITON_AMD_AUTOTUNE="TRUE"
export FLASH_ATTENTION_BACKEND="flash_attn_triton_amd"
export FLASH_ATTENTION_TRITON_AMD_SEQ_LEN=4096
export USE_CK=ON
export TRANSFORMERS_USE_FLASH_ATTENTION=1
export TRITON_USE_ROCM=ON
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1


export OMP_NUM_THREADS=14
export MKL_NUM_THREADS=14
export NUMEXPR_NUM_THREADS=14


export HIP_GRAPH=1

---------------------------------------------------------------------
#set for debugging, will result in slightly slower it/sec. but performance is VERY CONSISTENT:

#export HIP_LAUNCH_BLOCKING=1
#export AMD_SERIALIZE_KERNEL=1
#export AMD_SERIALIZE_COPY=1

----------------------------------------------------------------------


export AMD_DIRECT_DISPATCH=1
export GPU_MAX_HW_QUEUES=32

export HSA_ENABLE_ASYNC_COPY=1
export HSA_ENABLE_SDMA=1
export HSA_ENABLE_PEER_SDMA=1
export HSA_ENABLE_SDMA_COPY=1
export HSA_ENABLE_SDMA_KERNEL_COPY=1

export MIOPEN_FIND_MODE=2
export MIOPEN_ENABLE_CACHE=1
export MIOPEN_CHECK_NUMERICS=0x02


export HIP_FORCE_DEV_KERNARG=1

export ROCBLAS_STREAM_ORDER_ALLOC=1

export ROCBLAS_INTERNAL_FP16_ALT_IMPL=1
export ROCBLAS_LAYER=0
export ROCBLAS_INTERNAL_USE_SUBTENSILE=1

export SAFETENSORS_FAST_GPU=1

python main.py --disable-cuda-malloc --lowvram --use-pytorch-cross-attention --cache-lru 10 --reserve-vram 0.8 --preview-method none --listen --port 8188

in addition to this i also set in .bashrc:

export ROCM_PATH=/usr
export HIP_PATH=$ROCM_PATH
export PATH="$ROCM_PATH/bin:$PATH"
export LD_LIBRARY_PATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$LD_LIBRARY_PATH"
export PYTHONPATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$PYTHONPATH"

export HIP_CLANG_PATH=/usr/lib64/rocm/llvm/bin
export DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HIP_DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HSA_PATH=/usr
export LLVM_PATH=/usr/lib64/rocm/llvm/bin

export MIOPEN_USER_DB_PATH="$HOME/.cache/miopen"
export ROCBLAS_TENSILE_LIBPATH="$ROCM_PATH/lib64/rocblas/library"

export HIP_PLATFORM=amd
export HIP_RUNTIME=rocclr
export HIP_COMPILER=clang

export HSA_OVERRIDE_GFX_VERSION=12.0.1
export PYTORCH_ROCM_ARCH=gfx1201
export GFX_ARCH=gfx1201
export USE_ROCM=1

Setting those variables i got rid of ALL error messages, crashes and OOM messages generating images with comfyui except this one: https://github.com/ROCm/ROCm/issues/5833.

Before i set those i was seeing errors like: HIPBLASLT algo not supported and many others. You will also need to set those .bashrc variables for compiling ROCm programs, like https://github.com/YellowRoseCx/koboldcpp-rocm which does not compile with those variables not set.

Speedwise it bumped my generation speed with flux1.dev-fp8 up to 1.02 it/sec, flux-dev.safetensors (22 GB) suffers almost NO additional speed penalty from offloading. Using the weight_dtype fp8_e4m3fn_fast flux-dev.safetensors runs at the same speed as flux1.dev-fp8.safetensors.

---
