# [Issue]: GPU detected for both rocminfo and torch.cuda.is_available(), but torch inference is falling back to CPU

> **Issue #6206**
> **状态**: open
> **创建时间**: 2026-05-09T03:34:22Z
> **更新时间**: 2026-05-16T00:21:36Z
> **作者**: mengweili02
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6206

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Followed the instructions here to install rocm 7.2 + adrenalin edition 26.1.1
https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/install/installrad/wsl/install-radeon.html

Followed this instruction to install pytorch
https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/install/installrad/wsl/install-pytorch.html

rocminfo can detect the GPU and torch.cuda.is_available() returns True

However when I run inference on GPU adrenalin shows GPU memory increase (model is loaded) but no GPU utilization. Inference is falling back on CPU instead. Have tried inference using both a simple CNN model and Qwen/Qwen2.5-0.5B-Instruct from Huggingface

### Operating System

Windows version: 10.0.19045.6466 WSL2 Ubuntu 24.04.4 LTS (Noble Numbat)

### CPU

12th Gen Intel(R) Core(TM) i5-12600K

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

```
import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleCNN(nn.Module):
    """
    Simple CNN for image classification (e.g., MNIST, CIFAR10)
    """
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        # Conv layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        # Fully connected layers
        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        # Conv block 1
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool(x)  # 32x32 -> 16x16
        
        # Conv block 2
        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool(x)  # 16x16 -> 8x8
        
        # Flatten and FC layers
        x = x.view(-1, 64 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}\n")
    
    # Initialize model
    model = SimpleCNN(num_classes=10).to(device)
    
    # Create dummy input (batch_size=4, channels=3, height=32, width=32)
    dummy_input = torch.randn(4, 3, 32, 32).to(device)
    
    # Run inference
    model.eval()
    with torch.inference_mode():
        output = model(dummy_input)
    
    print(f"\n✓ Inference successful!")
    print(f"✓ Output shape: {output.shape}")


if __name__ == "__main__":
    main()

```

Running above code shows the following and adrenaline software shows no GPU usage
```
Device: cuda

pid:15000 tid:0x76d22e303b80 [GetSegmentId] Failed to get segment id for type 1
pid:15000 tid:0x76d22e303b80 [GetSegmentId] Failed to get segment id for type 1
pid:15000 tid:0x76d22e303b80 [GetSegmentId] Failed to get segment id for type 1

✓ Inference successful!
✓ Output shape: torch.Size([4, 10])
Warning: Resource leak detected by SharedSignalPool, 2 Signals leaked.
```


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

WSL environment detected.
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    12th Gen Intel(R) Core(TM) i5-12600K
  Uuid:                    CPU-XX                             
  Marketing Name:          12th Gen Intel(R) Core(TM) i5-12600K
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
  Cacheline Size:          64(0x40)                           
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16257204(0xf810b4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16257204(0xf810b4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16257204(0xf810b4) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16257204(0xf810b4) KB              
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
  Uuid:                    GPU-9b3f75c5d9eeca3a               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2400                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 108                                
  SDMA engine uCode::      0                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16589344(0xfd2220) KB              
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

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2026-05-12T18:41:19Z)

Hey @mengweili02, this looks to be the same root cause as what's discussed in https://github.com/ROCm/rocm-install-on-linux/issues/685#issuecomment-4206985823. Your Windows version `10.0.19045.6466` carries an outdated WDDM version which can lead to the `GetSegmentId` errors and downstream torch failures in WSL. Any chance you can update to Windows 11 (WDDM 3.1) and give this a try?

---

### 评论 #2 — mengweili02 (2026-05-16T00:21:35Z)

@harkgill-amd thank you for looking into this. Yeah I've found another issue in the similar scenario https://github.com/ROCm/librocdxg/issues/22

I'd prefer not to upgrade to Win 11. For other folks that are stuck with Win 10 WSL2 like me, downgrading rocm to 6.4 resolved the memory issue for me using this guide https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-6.4.4/docs/install/installrad/wsl/install-radeon.html

---
