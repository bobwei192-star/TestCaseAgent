# torch.cuda.is_available() return false with ROCm5.4.3 and RX6800

> **Issue #2354**
> **状态**: closed
> **创建时间**: 2023-07-30T02:12:45Z
> **更新时间**: 2024-08-02T09:04:38Z
> **关闭时间**: 2023-07-31T02:21:47Z
> **作者**: HGGshiwo
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2354

## 描述

I install ROCm, use the tutorial: https://rocmdocs.amd.com/en/latest/deploy/linux/os-native/install.html
it seems success. when I input ```rocminfo```, that is the output:
```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 5 5600G with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5600G with Radeon Graphics
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
  Max Clock Freq. (MHz):   3900                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    15738992(0xf02870) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    15738992(0xf02870) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15738992(0xf02870) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-362702d6dbbf2d1d               
  Marketing Name:          AMD Radeon RX 6800                 
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
    L1:                      16(0x10) KB                        
    L2:                      4096(0x1000) KB                    
    L3:                      131072(0x20000) KB                 
  Chip ID:                 29631(0x73bf)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2475                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            60                                 
  SIMDs per CU:            2                                  
  Shader Engines:          8                                  
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
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1030         
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
  Name:                    gfx90c                             
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
    L2:                      1024(0x400) KB                     
  Chip ID:                 5688(0x1638)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1900                               
  BDFID:                   3072                               
  Internal Node ID:        2                                  
  Compute Unit:            7                                  
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx90c:xnack-   
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

when I input ```dpkg -l | grep rocm```

```
ii  rocm-clang-ocl                             0.5.0.50403-121~22.04                   amd64        OpenCL compilation with clang compiler.
ii  rocm-cmake                                 0.8.0.50403-121~22.04                   amd64        rocm-cmake built using CMake
ii  rocm-core                                  5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-dbgapi                                0.68.0.50403-121~22.04                  amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent                           2.0.3.50403-121~22.04                   amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-developer-tools                       5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                           1.0.0.50403-121~22.04                   amd64        Radeon Open Compute - device libraries
ii  rocm-gdb                                   12.1.50403-121~22.04                    amd64        ROCgdb
ii  rocm-hip-libraries                         5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime                           5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev                       5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-sdk                               5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime                      5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm                                  15.0.0.23045.50403-121~22.04            amd64        ROCm compiler
ii  rocm-ml-libraries                          5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ml-sdk                                5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ocl-icd                               2.0.0.50403-121~22.04                   amd64        opencl built using CMake
ii  rocm-opencl                                2.0.0.50403-121~22.04                   amd64        opencl built using CMake
ii  rocm-opencl-dev                            2.0.0.50403-121~22.04                   amd64        opencl built using CMake
ii  rocm-opencl-runtime                        5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl-sdk                            5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp-sdk                            5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
ii  rocm-smi-lib                               5.0.0.50403-121~22.04                   amd64        AMD System Management libraries
ii  rocm-utils                                 5.4.3.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocminfo                                   1.0.0.50403-121~22.04                   amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool

```

Then I install pytorch, follow: https://rocmdocs.amd.com/en/latest/how_to/pytorch_install/pytorch_install.html

use the command:
```
pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/rocm5.4.3/
```

Is seems success too, because when I input ```python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'```. It returns Success

But when I input ```python3 -c 'import torch; print(torch.cuda.is_available())'```, It returns false.

So could anyone tell me how to fix it? Much much thanks.


---

## 评论 (5 条)

### 评论 #1 — evshiron (2023-07-30T09:38:14Z)

I have no idea why as everything seems to work fine.

Maybe `export HIP_VISIBLE_DEVICES=0` and `export HSA_OVERRIDE_GFX_VERSION=10.3.0` might help.

However, if ROCm 5.4.3 doesn't work, why don't we try ROCm 5.6 instead?

You can also double check the version of installed `torch` by `import torch; print(torch.__version__)`.

---

### 评论 #2 — Jan-Huber (2023-07-30T13:10:49Z)

try:
https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/7152#issuecomment-1402619240

---

### 评论 #3 — evshiron (2023-07-30T13:26:13Z)

The user group stuff can be found here:

* https://rocmdocs.amd.com/en/latest/deploy/linux/prerequisites.html#setting-permissions-for-groups

Here is a [tutorial](https://are-we-gfx1100-yet.github.io/post/a1111-webui/#the-easy-approach) for RX 7900 XTX, and the steps should be obvious and common for AMD GPUs. Except that `launch.sh` will not work for Navi 2x without changing `HSA_OVERRIDE_GFX_VERSION`.

---

### 评论 #4 — HGGshiwo (2023-07-31T02:21:44Z)

Thanks for your advice. Finally I find the problem is that I use torch-cpu rather than torch-gpu. But it is wired that I use the command on the official website to install pytorch, just change the rocm version like below:

```
pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/rocm5.4.3/
```

Maybe that is because I use python 3.7, So there is no sutiable torch-gpu for me. When I change my python version to 3.8, the problem is solved.

---

### 评论 #5 — DragonOV12341 (2024-08-02T09:04:37Z)

Hi，I met the similar problem. My ROCm version is 6.1, and I installed pytorch for rocm through official website of pytorch. I checked my installed torch through `pip list` and returns:
```
torch                    2.4.0+rocm6.1
torchaudio               2.4.0+rocm6.1
torchvision              0.19.0+rocm6.1
```
My ROCM is installed in local system, and pytorch is installed in Anaconda virtual env I created. My output of 'torch.cuda.is_available()' is also False. How can I solve the problem? Thx

---
