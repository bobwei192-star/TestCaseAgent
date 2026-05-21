# [Issue]: LLVM offload failure Ryzen 7 PRO 7840U

> **Issue #5669**
> **状态**: closed
> **创建时间**: 2025-11-16T02:40:52Z
> **更新时间**: 2025-11-21T20:03:42Z
> **关闭时间**: 2025-11-21T18:52:00Z
> **作者**: ZuseZ4
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5669

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

```
OS:
NAME="Linux Mint"
VERSION="22 (Wilma)"
CPU: 
model name	: AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics
```
(rocminfo below)


I'm currently adding GPU support to rustc via LLVM offload. I am building LLVM/clang/rustc/lld from source.
I have installed rocm twice, once via the rock, and once via apt.
Instructions for the current state of rust offload are at https://rustc-dev-guide.rust-lang.org/offload/usage.html
I've managed to run Rust code on an MI 250X, an NVIDIA GPU, as well as a `Ryzen AI 9 HX 370 w/ Radeon 890M`. 

However, I've failed to run it on my own Laptop, despite various efforts. After the last kernel update from 6.8 to 6.14 I now at least get the right number of devices reported by openmp (1), previously it was 0.
Nevertheless, every openmp offload launch causes my screen to turn dark or black, and freezes my system.

I am also not able to use the clang shipped by either of the two rocm instances:
```
➜  offload_test git:(main) /opt/rocm-7.1.0/llvm/bin/clang++ -fuse-ld=lld -O3 -fopenmp --offload-arch=gfx1103 omp_tgt.cpp -o main --rocm-path=/home/manuel/.software/therock-tarball/install/llvm -L /home/manuel/prog/rust_gpu/build/x86_64-unknown-linux-gnu/llvm/lib/x86_64-unknown-linux-gnu
➜  offload_test git:(main) LIBOMPTARGET_INFO=-1  ./main
Call                is_plugin_compatible:       21us              1 (0x000024667bb0)
Call                   number_of_devices:        0us              1 )
Call                   number_of_devices:        0us              1 )
Call                is_device_compatible:       42us              1 (             0, 0x000024667bb0)
Call                         init_device:    20599us              0 (             0)
Call                number_of_team_procs:        0us             12 (             0)
Call                   number_of_devices:        0us              1 )
Call                  use_auto_zero_copy:        0us              0 (             0)
Call                      has_apu_device:        0us              0 (             0)
Call               get_num_multi_devices:        0us              0 )
Number of available devices 1
omptarget device 0 info: Entering OpenMP kernel at unknown:0:0 with 0 arguments:
"PluginInterface" error: Failure to load binary image 0x24667bb0 on device 0: Error in hsa_amd_memory_async_copy_on_engine: HSA_STATUS_ERROR_INVALID_ARGUMENT: One of the actual arguments does not meet a precondition stated in the documentation of the corresponding formal argument.
Call                         load_binary:    54208us             -1 (             0, 0x000024667bb0, 0x7ffc64855340)
omptarget error: Failed to load image Failed to load binary 0x24667bb0
omptarget fatal error 0: Failed to load images on device '0'
[1]    86452 IOT instruction (core dumped)  LIBOMPTARGET_INFO=-1 ./main
```
Using my self-build clang, it reports the number of devices (1), but no error or following prints:
```
➜  offload_test git:(main) LIBOMPTARGET_INFO=-1  ./main
Number of available devices 1
omptarget device 0 info: Entering OpenMP kernel at unknown:0:0 with 0 arguments:
"PluginInterface" device 0 info: Launching kernel __omp_offloading_fc01_1ba6424_main_l20 with [1,1,1] blocks and [256,1,1] threads in Generic-SPMD mode
AMDGPU device 0 info: #Args: 1 Teams x Thrds:    1x 256 (MaxFlatWorkGroupSize: 256) LDS Usage: 0B #SGPRs/VGPRs: 0/0 #SGPR/VGPR Spills: 0/0 Tripcount: 0
omptarget device 0 info: OpenMP Host-Device pointer mappings table empty
omptarget device 0 info: OpenMP Host-Device pointer mappings table empty
```
Here is the test program, but other c++ tests yield similar output:
```
#include <stdio.h>
#include <omp.h>

int main() 

{
  int num_devices = omp_get_num_devices();
  printf("Number of available devices %d\n", num_devices);
  #pragma omp target 
  {
      if (omp_is_initial_device()) {
        printf("Running on host\n");    
      } else {
        int nteams= omp_get_num_teams(); 
        int nthreads= omp_get_num_threads();
        printf("Running on device with %d teams in total and %d threads in each team\n",nteams,nthreads);
      }
  }

}
```
cc @jplehr

### Operating System

Linux Mint 22 Cinnamon, Kernel 6.14.0-35-generic

### CPU

AMD Ryzen 7 PRO 7840U 

### GPU

Radeon 780M integrated

### ROCm Version

ROCm 7.1.0

### ROCm Component

_No response_

### Steps to Reproduce

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
  Name:                    AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 PRO 7840U w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5134                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    61348948(0x3a81c54) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    61348948(0x3a81c54) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    61348948(0x3a81c54) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    61348948(0x3a81c54) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
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
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   25600                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
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
  Packet Processor uCode:: 67                                 
  SDMA engine uCode::      23                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    30674472(0x1d40e28) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    30674472(0x1d40e28) KB             
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
      Size:                    61348948(0x3a81c54) KB             
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
      Size:                    61348948(0x3a81c54) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***            
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — tcgu-amd (2025-11-17T20:06:18Z)

Hi @ZuseZ4, thanks for reaching out! Awesome stuff you are working on! Regarding the error you are seeing, unfortunately I think it is just that ROCm doesn't really support the 780M iGPU, which is why the official clang returns the error message you are seeing. On the other hand, MI250 (gfx90a) and Strix Point (gfx 1150) are both supported, and the fact that your code works on them means there's nothing wrong with the code itself. Your system hang is probably because the graphics kernel got stuck while processing unsupported instructions..

---

### 评论 #2 — ZuseZ4 (2025-11-21T20:03:42Z)

Thank you! I guess I had gotten too hopeful once I got my system to at least report the correct number of GPU devices, but I returned to work on my server then. Since Strix Point seems to work, I'll ask my PI if I can get a newer 395 APU Laptop for some local experiment once availability improves.

---
