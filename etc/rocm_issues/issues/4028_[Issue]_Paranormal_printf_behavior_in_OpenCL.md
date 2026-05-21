# [Issue]: Paranormal printf behavior in OpenCL

> **Issue #4028**
> **状态**: open
> **创建时间**: 2024-11-13T18:40:13Z
> **更新时间**: 2024-11-18T20:52:27Z
> **作者**: Richardk2n
> **标签**: Under Investigation, ROCm 6.2.3, Radeon VII, Radeon Pro VII, Radeon RX 5700 XT, Radeon Instinct MI60, Radeon Instinct MI210
> **URL**: https://github.com/ROCm/ROCm/issues/4028

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **Radeon VII** (颜色: #ededed)
- **Radeon Pro VII** (颜色: #ededed)
- **Radeon RX 5700 XT** (颜色: #ededed)
- **Radeon Instinct MI60** (颜色: #ededed)
- **Radeon Instinct MI210** (颜色: #ededed)

## 描述

### Problem Description

Consider this pyopencl snippet (this also occurs using the C++ OpenCL libs from Khronos, this way is just easier to show):

```python
import pyopencl as cl

plattform = cl.get_platforms()[0]
device = plattform.get_devices()[0]

ctx = cl.Context([device])
queue = cl.CommandQueue(ctx)

src = r"""
kernel void tet() {
    const long m = get_global_id(0);
	printf("ID %ld\n", m);
}
"""

src2 = r"""
kernel void other() {
    const long n = get_global_id(0);
    printf("Do not print %ld\n", n);
}
"""

p = cl.Program(ctx, src).compile()
p2 = cl.Program(ctx, src2).compile()

program = cl.link_program(ctx, [p, p2])

program.tet(queue, (2,), None)
```

This should output:
```
ID 0
ID 1
```

But what I get is:
```
ID 0
Do not print 4294967297
(null)
```

It seems that as soon as a `printf` is present in more than one kernel it goes rogue. As far as I can tell the remaining code gets executed properly.

ROCm Version is actually 6.2.4, but I cannot select that below.

### Operating System

Manjaro Linux

### CPU

N/A

### GPU

Radeon VII, Radeon Pro VII, Radeon RX 5700 XT, Radeon Instinct MI60, Radeon Instinct MI210

### ROCm Version

ROCm 6.2.3

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    13th Gen Intel(R) Core(TM) i9-13900K
  Uuid:                    CPU-XX                             
  Marketing Name:          13th Gen Intel(R) Core(TM) i9-13900K
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
  Max Clock Freq. (MHz):   5500                               
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
      Size:                    65542380(0x3e818ec) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65542380(0x3e818ec) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65542380(0x3e818ec) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx906                             
  Uuid:                    GPU-0ba4694172da5ee7               
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
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 26273(0x66a1)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1800                               
  BDFID:                   1024                               
  Internal Node ID:        1                                  
  Compute Unit:            64                                 
  SIMDs per CU:            4                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
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
  Packet Processor uCode:: 472                                
  SDMA engine uCode::      145                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33538048(0x1ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    33538048(0x1ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
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

_No response_

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-11-13T19:30:37Z)

Hi @Richardk2n. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — jamesxu2 (2024-11-18T20:52:26Z)

Hi @Richardk2n, thanks for submitting this issue. 

This does indeed look like some paranormal behaviour, and I am looking into it. I've translated your python code into C++ just because it's easier to debug, but I do see some pretty interesting behaviour as I expand the number of threads. I'm still working on a coherent hypothesis on how this is possible. 

```
hipcc test.cc -lOpenCL -ggdb ; ./a.out
ID 0
Do not print 4294967297   (In hex: 0x1 00 00 00 01) <-- Possibly, the print buffer is not properly terminated and reads into printf's arglist containing 0x1? Something overruns the return from function and causes co-located kernels to execute together?
(null)ID 2
Do not print 12884901889  (0x3 00 00 00 01)
(null)ID 4
Do not print 21474836481  (0x5 00 00 00 01)
(null)ID 6
Do not print 30064771073  (0x7 00 00 00 01)
(null)ID 8
Do not print 38654705665  (0x9 00 00 00 01)
(null)
```

I will also add that HIP (AMD's portable C++ dialect for GPU programming, similar to CUDA) is a better supported and much simpler syntax for GPU programming. You can see a hello world example here: https://github.com/ROCm/rocm-examples/blob/develop/HIP-Basic/hello_world/main.hip . If you have no specific reason to use OCL, I'd recommend writing your application in HIP!

That being said, I'll provide more updates as I gather more information on what's going on here. 

---
