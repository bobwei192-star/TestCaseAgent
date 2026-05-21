# [Issue]: MIOpen convolution operations fail with 'free(): invalid pointer' error on RX 7800 XT (RDNA 3/gfx11xx)

> **Issue #4466**
> **状态**: closed
> **创建时间**: 2025-03-08T06:45:30Z
> **更新时间**: 2025-05-26T19:37:01Z
> **关闭时间**: 2025-05-26T19:37:00Z
> **作者**: Mubarak-11
> **标签**: Under Investigation, ROCm 6.3.4
> **URL**: https://github.com/ROCm/ROCm/issues/4466

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.4** (颜色: #aaaaaa)

## 描述

### Problem Description

When using PyTorch with ROCm on my AMD Radeon RX 7800 XT (RDNA 3/gfx11xx architecture), any convolution operations result in a "free(): invalid pointer" error and program crash. The issue appears to be related to the absence of precompiled kernel packages for RDNA 3 GPUs in the current ROCm 6.3 release.
Simple matrix operations and basic custom CNNs work correctly, but any model using standard CNN architectures like ResNet, VGG, or MobileNetV2 crashes during the forward pass at the convolution operations.

### Operating System

OS: NAME="Ubuntu" VERSION="24.04 (Noble Numbat)"

### CPU

model name      : 13th Gen Intel(R) Core(TM) i5-13600KF

### GPU

AMD Radeon RX 7800 XT                    

### ROCm Version

6.3.4

### ROCm Component

MIOpen

### Steps to Reproduce

Attempt to load and run a pretrained model with convolution operations
Create a minimal test case as follows:

import os
import torch
import torch.nn as nn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

device = torch.device("cuda")
logger.info(f"Using device: {device}")

# Test with simple CNN components
class ComponentTestCNN(nn.Module):
    def __init__(self):
        super(ComponentTestCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        
    def forward(self, x):
        return self.conv1(x)

# Test components
model = ComponentTestCNN().to(device)
x = torch.randn(1, 3, 64, 64, device=device)

# This line causes "free(): invalid pointer" crash
y = model(x)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

bruno@PC:~$ /opt/rocm/bin/rocminfo
ROCk module is loaded
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
  Name:                    13th Gen Intel(R) Core(TM) i5-13600KF
  Uuid:                    CPU-XX                             
  Marketing Name:          13th Gen Intel(R) Core(TM) i5-13600KF
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
  Max Clock Freq. (MHz):   5100                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            20                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65664792(0x3e9f718) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65664792(0x3e9f718) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65664792(0x3e9f718) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65664792(0x3e9f718) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1101                            
  Uuid:                    GPU-6a249ead25ccfaeb               
  Marketing Name:          AMD Radeon RX 7800 XT              
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
    L2:                      4096(0x1000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29822(0x747e)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2169                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            60                                 
  SIMDs per CU:            2                                  
  Shader Engines:          3                                  
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
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      21                                 
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
      Name:                    amdgcn-amd-amdhsa--gfx1101         
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
bruno@PC:~$ 

### Additional Information

**No packages for RDNA 3 (gfx11xx) are available, which appears to be the root cause of the issue.**

$ apt-cache search miopen-hip | grep kdb
miopen-hip-gfx1030kdb - AMD DNN Library
miopen-hip-gfx1030kdb-rpath6.3.4 - AMD DNN Library
miopen-hip-gfx1030kdb6.3.4 - AMD DNN Library
miopen-hip-gfx900kdb - AMD DNN Library
miopen-hip-gfx900kdb-rpath6.3.4 - AMD DNN Library
miopen-hip-gfx900kdb6.3.4 - AMD DNN Library
miopen-hip-gfx906kdb - AMD DNN Library
miopen-hip-gfx906kdb-rpath6.3.4 - AMD DNN Library
miopen-hip-gfx906kdb6.3.4 - AMD DNN Library
miopen-hip-gfx908kdb - AMD DNN Library
miopen-hip-gfx908kdb-rpath6.3.4 - AMD DNN Library
miopen-hip-gfx908kdb6.3.4 - AMD DNN Library
miopen-hip-gfx90akdb - AMD DNN Library
miopen-hip-gfx90akdb-rpath6.3.4 - AMD DNN Library
miopen-hip-gfx90akdb6.3.4 - AMD DNN Library
miopen-hip-gfx942kdb - AMD DNN Library
miopen-hip-gfx942kdb-rpath6.3.4 - AMD DNN Library
miopen-hip-gfx942kdb6.3.4 - AMD DNN Library

**Installed MIOpen Packages**
$ apt list --installed | grep miopen
miopen-hip-dev6.3.4/noble,now 3.3.0.60304-76~24.04 amd64 [installed,automatic]
miopen-hip6.3.4/noble,now 3.3.0.60304-76~24.04 amd64 [installed,automatic]

**My Pytorch/ROCm details:**
$ python3 -c "import torch; print(torch.__version__); print(torch.version.hip)"
2.7.0.dev20250306+rocm6.3
6.3.42131-fa1d09cbd

**The exact Error message**
free(): invalid pointer
Aborted (core dumped)

**I've tried various MIOpen environment variable settings including:**

MIOPEN_DEBUG_CONV_DIRECT=0
MIOPEN_DEBUG_CONV_GEMM=1
MIOPEN_FIND_ENFORCE=3
MIOPEN_DEBUG_CONV_IMPLICIT_GEMM=1
MIOPEN_FIND_MODE=NORMAL
MIOPEN_DEBUG_CONV_WINOGRAD=0

None of these resolved the issue, suggesting the fundamental problem is the missing architecture support in MIOpen for RDNA 3 GPUs.
A workaround that allows me to continue development is to use a custom CNN implementation that avoids complex convolution operations, but this severely limits the architectures that can be used effectively.


---

## 评论 (7 条)

### 评论 #1 — james-banks (2025-03-09T14:27:21Z)

Those architecture-specific miopen packages denote additional tuning for specific architectures but the package you have installed should have gfx1100 binaries included, which can be used by your card with a small tweak. 

Have you tried the following environment variable?

```
HSA_OVERRIDE_GFX_VERSION=11.0.0
```

---

### 评论 #2 — Mubarak-11 (2025-03-09T16:29:48Z)

Thank you for your suggestion. I tried setting the HSA_OVERRIDE_GFX_VERSION=11.0.0 environment variable as recommended, but I'm still encountering the same "free(): invalid pointer" error when attempting to use convolution operations on my RX 7800 XT.
Here's what I've tried:

1. Setting HSA_OVERRIDE_GFX_VERSION=11.0.0 in .bashrc and verifying it's set correctly:

`$ echo $HSA_OVERRIDE_GFX_VERSION
11.0.0`

2. Directly setting the variable when running the script:

`$ HSA_OVERRIDE_GFX_VERSION=11.0.0 python3.10 test_conv.py
free(): invalid pointer
Aborted (core dumped)`

3. Trying with additional MIOpen settings:

`$ MIOPEN_DEBUG_HIP_VERSION=11.0.0 HSA_OVERRIDE_GFX_VERSION=11.0.0 python3.10 test_conv.py
free(): invalid pointer
Aborted (core dumped)`

I'm using a minimal reproducible test case that simply creates a single convolution layer and tries to run a forward pass:

`import os
import torch
import torch.nn as nn

os.environ['HSA_OVERRIDE_GFX_VERSION'] = '11.0.0'
os.environ['MIOPEN_DEBUG_CONV_DIRECT'] = '1'  
os.environ['MIOPEN_DEBUG_CONV_WINOGRAD'] = '0'
os.environ['MIOPEN_FIND_MODE'] = 'NORMAL'

device = torch.device("cuda")
x = torch.randn(1, 3, 32, 32, device=device)
conv = nn.Conv2d(3, 16, 3, padding=1).to(device)
y = conv(x)  # This line causes the crash
print("Convolution successful!")
print(f"Output shape: {y.shape}")`

---

### 评论 #3 — ppanchad-amd (2025-03-10T13:59:50Z)

Hi @mubarakderie. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #4 — james-banks (2025-03-10T15:14:54Z)

> Thank you for your suggestion. I tried setting the HSA_OVERRIDE_GFX_VERSION=11.0.0 environment variable as recommended, but I'm still encountering the same "free(): invalid pointer" error when attempting to use convolution operations on my RX 7800 XT.

Sorry to hear it's still not working. I would recommend adding the following environment variables and seeing if the additional verbosity can shine any light: 

```
export MIOPEN_ENABLE_LOGGING=1
export MIOPEN_ENABLE_LOGGING_CMD=1
export MIOPEN_LOG_LEVEL=6
```

Good to see an internal ticket is filed and hopefully they can get this sorted for you soon. 

---

### 评论 #5 — Mubarak-11 (2025-03-10T17:39:34Z)

Thank you for filing a ticket @ppanchad-amd . Thanks for the additional verbosity commands @james-banks 

I've done more in-depth debugging with the logging environment variables you suggested, and I've been able to identify exactly where the crash is occurring.
Using these flags: `ROCBLAS_LAYER=3 MIOPEN_ENABLE_LOGGING=1 MIOPEN_ENABLE_LOGGING_CMD=1 MIOPEN_LOG_LEVEL=6` 

I've collected a detailed log file that shows the following:

1. My GPU is correctly identified as gfx1100/RX 7800 XT
2. The architecture-specific kernels are being correctly compiled with -mcpu=gfx1100
3. Several steps of the convolution process work correctly
4. The crash happens specifically at the point where MIOpen calls rocBLAS for a GEMM operation

The exact line where the crash occurs: 
`MIOpen(HIP): Info2 [CallGemm] rocBLAS
rocblas_gemm_ex,N,N,1024,16,27,1,0x7be683213a00,f32_r,1024,0x7be683203000,f32_r,27,0,0x7be683203a00,f32_r,1024,0x7be683203a00,f32_r,1024,f32_r,0,0,none,atomics_allowed
./rocblas-bench -f gemm_ex --transposeA N --transposeB N -m 1024 -n 16 -k 27 --alpha 1 --a_type f32_r --lda 1024 --b_type f32_r --ldb 27 --beta 0 --c_type f32_r --ldc 1024 --d_type f32_r --ldd 1024 --compute_type f32_r --algo 0 --solution_index 0 --flags 0
free(): invalid pointer`

The HSA_OVERRIDE_GFX_VERSION=11.0.0 environment variable didn't resolve the issue since the GPU is already being correctly identified.
I've attached the full debug log file for your reference. It appears to be a bug in the interaction between MIOpen and rocBLAS when running on RDNA 3 GPUs. Let me know if you need any additional information to help diagnose and fix this issue.
 
[debug_output.txt](https://github.com/user-attachments/files/19167984/debug_output.txt)


---

### 评论 #6 — Mubarak-11 (2025-04-16T12:14:14Z)

**Update: Issue Resolved in PyTorch 2.8 Pre-Alpha**
I wanted to update this ticket with some exciting news. I've been able to successfully run CNN operations including convolutions on my RX 7800 XT using a newer PyTorch build, while still using the same ROCm 6.3 version.
I tested this fix by pulling the latest PyTorch nightly Docker image (docker pull rocm/pytorch-nightly) and running my CNN code inside the container. This approach allowed me to quickly verify that newer PyTorch builds resolve the issue without modifying my host system.
Environment where issue occurs:

GPU: AMD Radeon RX 7800 XT (RDNA 3/gfx1100)
ROCm version: 6.3.42131-fa1d09cbd
PyTorch version: 2.7.0.dev20250306+rocm6.3
Result: "free(): invalid pointer" errors when using convolution operations

Environment where issue is FIXED:

GPU: AMD Radeon RX 7800 XT (RDNA 3/gfx1100)
ROCm version: 6.3.42131-fa1d09cbd (same as above)
PyTorch version: 2.8 pre-alpha (from rocm/pytorch-nightly Docker image)
Result: Successfully runs convolution operations including pre-trained models

I tested various CNN architectures in the working environment:

VGG16 (pre-trained model): ✅ SUCCESS
Basic convolutions: ✅ SUCCESS
Batch normalization: ✅ SUCCESS
Depthwise separable convolutions: ✅ SUCCESS
Residual connections (ResNet-style): ✅ SUCCESS
Dilated convolutions: ✅ SUCCESS

Here's a sample of the successful tests:
`
import torch
import torchvision.models as models

#####  Load pre-trained VGG-16 model
model = models.vgg16(pretrained=True).to(torch.device("cuda"))

#####  Create a random input tensor
x = torch.randn(1, 3, 224, 224, device=torch.device("cuda"))

#####  Run the model
y = model(x)

#####  Output result
print(f"Output shape: {y.shape}")
##### Result: Output shape: torch.Size([1, 1000])`

Since the ROCm version is identical between my two environments, this suggests the issue was fixed in the PyTorch code rather than requiring changes to ROCm itself. The bug appears to have been in how PyTorch interfaces with MIOpen/rocBLAS for convolution operations. I hope this information is helpful for your team. I'm now able to proceed with using my GPU for deep learning tasks thanks to this newer PyTorch build.


---

### 评论 #7 — harkgill-amd (2025-05-26T19:37:00Z)

@Mubarak-11, I'm glad to hear the issue was resolved with the latest PyTorch release. Thanks for the in-depth summary as well, I'm sure it will be helpful to anyone passing through this thread. Will close this issue out as it's been fixed but feel free to leave a comment if it persists or if you have any questions.

---
