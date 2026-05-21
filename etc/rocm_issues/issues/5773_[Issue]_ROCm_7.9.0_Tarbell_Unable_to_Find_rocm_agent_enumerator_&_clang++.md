# [Issue]: ROCm 7.9.0 Tarbell Unable to Find rocm_agent_enumerator & clang++

> **Issue #5773**
> **状态**: closed
> **创建时间**: 2025-12-14T21:23:44Z
> **更新时间**: 2025-12-22T18:02:16Z
> **关闭时间**: 2025-12-22T18:02:16Z
> **作者**: nsatch
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5773

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Trying to compile a HIP program results in the following error. 

```
user@host:~/aipc_programming/gpu_program/mat_mul2$ hipcc hip_debug.cpp 
sh: 1: /home/user/aipc_programming/gpu_program/therock-tarball/lib/llvm/bin/clang++: not found
sh: 1: /usr/local/cuda/bin/nvcc: not found
sh: 1: nvcc: not found
Device not supported - Defaulting to AMD
sh: 1: /home/user/aipc_programming/gpu_program/therock-tarball/bin/rocm_agent_enumerator: not found
sh: 1: /home/user/aipc_programming/gpu_program/therock-tarball/lib/llvm/bin/clang++: not found
failed to execute:/home/user/aipc_programming/gpu_program/therock-tarball/lib/llvm/bin/clang++  -O3 --driver-mode=g++ -O3 --hip-link  -x hip hip_debug.cpp
```

I see that rocm_agent_enumerator can be found at `/home/user/aipc_programming/gpu_program/therock-tarball/install/bin/rocm_agent_enumerator`(note this has `install` in its path while the output path from the error does not.

I tried revising the exported paths to look like 
```
export ROCM_PATH=#PWD/install
export PATH=$PATH:$ROCM_PATH/bin
export LD_LIBRARY_PATH=$ROCM_PATH/lib

```
instead of the installation guide's
```
export ROCM_PATH=$PWD
export PATH=$PATH:$ROCM_PATH/install/bin
export LD_LIBRARY_PATH=$ROCM_PATH/install/lib
```

but then I receive this error
```
clang++: error: cannot find ROCm device library; provide its path via '--rocm-path' or '--rocm-device-lib-path', or pass '-nogpulib' to build without ROCm device l
ibrary
failed to execute:/home/user/aipc_programming/gpu_program/therock-tarball/install/lib/llvm/bin/clang++  --offload-arch=gfx1150 -O3 --driver-mode=g++ -O3 --hip-l
ink  -x hip hip_debug.cpp
```

The target program looks like

```
#include <hip/hip_runtime.h>
#include <iostream>

int main() {
    float* d_ptr = nullptr;
    hipError_t err = hipMalloc(&d_ptr, 1024);
    std::cout << "hipMalloc returned: " << hipGetErrorString(err) << std::endl;
    if (err == hipSuccess) {
        hipFree(d_ptr);
        std::cout << "hipFree succeeded\n";
    }
}
```

I do receive this error for other programs (including some from AMD provided ROCm examples at https://github.com/ROCm/rocm-examples), so I don't believe the target code is the issue. 

### Operating System

"Ubuntu" VERSION="24.04.3 LTS (Noble Numbat)"

### CPU

AMD Ryzen AI 9 HX 370 w/ Radeon 890M

### GPU

Radeon 890M

### ROCm Version

ROCm 7.9.0

### ROCm Component

_No response_

### Steps to Reproduce

Follow the steps outlined at https://rocm.docs.amd.com/en/7.9.0-preview/install/rocm.html for installation. Then try to compile a HIP program. 

### Install ROCm via tarbell

```
sudo usermod -a -G render,video $LOGNAME # Add the current user to the render and video groups

mkdir therock-tarball && cd therock-tarball

wget https://repo.amd.com/rocm/tarball/therock-dist-linux-gfx1151-7.9.0rc1.tar.gz
mkdir install
tar -xf *.tar.gz -C install

export ROCM_PATH=$PWD
export PATH=$PATH:$ROCM_PATH/install/bin
export LD_LIBRARY_PATH=$ROCM_PATH/install/lib
```

Compile a HIP program
`hipcc hip_debug.cpp`

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
  Max Clock Freq. (MHz):   5157                               
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
      Size:                    63380940(0x3c71dcc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    63380940(0x3c71dcc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    63380940(0x3c71dcc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    63380940(0x3c71dcc) KB             
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
  Chip ID:                 5390(0x150e)                       
  ASIC Revision:           4(0x4)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
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
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31690468(0x1e38ee4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31690468(0x1e38ee4) KB             
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
      Size:                    63380940(0x3c71dcc) KB             
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
      Size:                    63380940(0x3c71dcc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             
```

### Additional Information

This issue also occurs on ROCm 7.10.0. This would also pass `test_hip_api` while displaying the same issue during compilation.

---

## 评论 (3 条)

### 评论 #1 — harkgill-amd (2025-12-16T20:49:41Z)

Hey @nsatch, thanks for bringing this up. The path setup should definitely have ROCM_PATH set to wherever the actual install is located (`therock-tarball/install`) and not just at `therock-tarball`. The following you mentioned is correct,
```
export ROCM_PATH=$PWD/install
export PATH=$PATH:$ROCM_PATH/bin
export LD_LIBRARY_PATH=$ROCM_PATH/lib
```
Will get this updated on our install page.

From there, the `cannot find ROCm device library; provide its path` error is caused by clang expecting the libraries at `$ROCM_PATH/amdgcn/bitcode/` while they're actually at `$ROCM_PATH/lib/llvm/amdgcn/bitcode/`. You can fix this by manually setting 
```
export ROCM_PATH=/<path_to_install>/therock-tarball/install
export HIP_DEVICE_LIB_PATH=$ROCM_PATH/lib/llvm/amdgcn/bitcode
hipcc test.cpp
```
We're in the process of scoping out a better solution for all of the environment variable setup in both the tarball and pip install methods https://github.com/ROCm/TheRock/issues/1658.

---

### 评论 #2 — nsatch (2025-12-19T04:17:35Z)

Thanks for the quick reply! After editing the bashrc as you suggested, everything seems to be in working order for any HIP program I throw at it. The original issue is resolved as far as I see.

Thanks 🙏!

---

### 评论 #3 — harkgill-amd (2025-12-22T16:03:17Z)

No problemo! https://rocm.docs.amd.com/en/7.9.0-preview/install/rocm.html has also been updated with the correct steps so I'll go ahead and close this out. 

---
