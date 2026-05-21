# [Issue]: Kernel crash when using TORCH_BLAS_PREFER_HIPBLASLT with pytorch

> **Issue #6271**
> **状态**: open
> **创建时间**: 2026-05-18T17:20:36Z
> **更新时间**: 2026-05-18T17:21:09Z
> **作者**: Lama-Thematique
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6271

## 描述

### Problem Description

I was looking at performance in fp32 of the radeon 890M in pytorch (CPU HX 370) on framework laptop 16 running endeavourOS.
when setting `TORCH_BLAS_PREFER_HIPBLASLT=1` and running pytorch code leads to black/white/corrupted screen with ring `ring gfx_0.0.0 timeout` kernel crash.

### Operating System

EndeavourOS (Kernel : Linux 7.0.9-arch1-1)

### CPU

AMD Ryzen AI 9 HX 370 w/ Radeon 890M

### GPU

Radeon 890M

### ROCm Version

7.1.*, 7.2.1, 7.2.3

### ROCm Component

hipBLASLt

### Steps to Reproduce


Using the following code:
```python
import torch
a = torch.randn(4096, 4096, device='cuda', dtype=torch.float32)
b = torch.randn(4096, 4096, device='cuda', dtype=torch.float32)
for _ in range(10):
     c = a @ b

torch.cuda.synchronize()
import time
start = time.perf_counter()
for _ in range(100):
     c = a @ b

torch.cuda.synchronize()
elapsed = time.perf_counter() - start
flops = 100 * 2 * 4096**3 / elapsed / 1e12
print(f"{flops:.1f} TFLOPS")
```
with `TORCH_BLAS_PREFER_HIPBLASLT=1` in my env.

I can reproduce the issue 100% of the time on my system, across all  kernel, rocm and pytorch version I tested. 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
  Name:                    AMD Ryzen AI 9 HX 370 w/ Radeon 890M
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen AI 9 HX 370 w/ Radeon 890M
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
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    48583244(0x2e5524c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    48583244(0x2e5524c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    48583244(0x2e5524c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    48583244(0x2e5524c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1150                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon 890M Graphics           
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
  Chip ID:                 5390(0x150e)                       
  ASIC Revision:           4(0x4)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   49408                              
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
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
  Packet Processor uCode:: 34                                 
  SDMA engine uCode::      15                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24291620(0x172a924) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24291620(0x172a924) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1150         
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
  Name:                    aie2p                              
  Uuid:                    AIE-XX                             
  Marketing Name:          RyzenAI-npu4                       
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
      Size:                    48583244(0x2e5524c) KB             
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
      Size:                    48583244(0x2e5524c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***  

### Additional Information

Device : Framework laptop 16 without dedicated GPU.

software versions: 
```bash
> pip freeze | grep torch     
pytorch-triton-rocm==3.5.1+gitbfeb0668
torch==2.13.0.dev20260517+rocm7.2
torchaudio==2.11.0.dev20260518+rocm7.2
torchmetrics==1.6.2
torchvision==0.28.0.dev20260518+rocm7.2

> pacman -Q | grep rocm
ollama-rocm 0.23.3-1
rocm-cmake 7.2.3-1
rocm-core 7.2.3-1
rocm-device-libs 2:7.2.3-1
rocm-hip-libraries 7.2.3-1
rocm-hip-runtime 7.2.3-1
rocm-hip-sdk 7.2.3-1
rocm-language-runtime 7.2.3-1
rocm-llvm 2:7.2.3-1
rocm-smi-lib 7.2.0-2
rocminfo 7.2.3-1
 
> pacman -Q | grep hip
hip-runtime-amd 7.2.3-1
hipblas 7.2.3-1
hipblas-common 7.2.3-1
hipblaslt 7.2.3-1
hipcub 7.2.3-1
hipfft 7.2.3-1
hiprand 7.2.3-1
hipsolver 7.2.3-1
hipsparse 7.2.3-1
miopen-hip 7.2.3-1
rocm-hip-libraries 7.2.3-1
rocm-hip-runtime 7.2.3-1
rocm-hip-sdk 7.2.3-1
``` 

Systemctl log:
```kernel: amdgpu 0000:c1:00.0: Dumping IP State
kernel: amdgpu 0000:c1:00.0: Dumping IP State Completed
kernel: amdgpu 0000:c1:00.0: [drm] AMDGPU device coredump file has been created
kernel: amdgpu 0000:c1:00.0: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
kernel: amdgpu 0000:c1:00.0: ring gfx_0.0.0 timeout, signaled seq=51534, emitted seq=51537
kernel: amdgpu 0000:c1:00.0:  Process kwin_wayland pid 1765 thread kwin_wayla:cs0 pid 1804
kernel: amdgpu 0000:c1:00.0: Starting gfx_0.0.0 ring reset
kernel: amdgpu 0000:c1:00.0: Ring gfx_0.0.0 reset succeeded
kernel: amdgpu 0000:c1:00.0: [drm] device wedged, but recovered through reset
```
