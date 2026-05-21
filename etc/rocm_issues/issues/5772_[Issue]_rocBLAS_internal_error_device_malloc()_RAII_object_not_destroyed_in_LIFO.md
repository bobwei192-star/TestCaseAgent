# [Issue]: rocBLAS internal error: device_malloc() RAII object not destroyed in LIFO order.

> **Issue #5772**
> **状态**: closed
> **创建时间**: 2025-12-13T07:38:09Z
> **更新时间**: 2026-01-30T20:00:58Z
> **关闭时间**: 2026-01-30T18:08:29Z
> **作者**: asenzz
> **标签**: ROCm 6.2.2, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5772

## 标签

- **ROCm 6.2.2** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description


GPU:

  Name:                    AMD EPYC 7A53 64-Core Processor    
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI250X                
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI250X                
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI250X                
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-


I'm getting the following error:

rocBLAS internal error: device_malloc() RAII object not destroyed in LIFO order.
Objects returned by device_malloc() must be 0-sized, unsuccessfully allocated,
or destroyed in the reverse order that they are created.
device_malloc() objects cannot be assigned to unless they are 0-sized
or they were unsuccessfully allocated previously.
 
Program crashed code looks like this:

```
...
HIP_ERRCHK(hipSetDevice(dev_phy_id));
    HIP_ERRCHK(hipMemcpyAsync(ctx_stream.weights, weights, W_size, hipMemcpyHostToDevice, ctx_stream.hipstream));
    HIP_ERRCHK(hipMemcpyAsync(ctx_stream.tmp_L, ctx_dev.L_mask, L_size, hipMemcpyDeviceToDevice, ctx_stream.hipstream));
    HIP_ERRCHK(hipStreamSynchronize(ctx_stream.hipstream));
    for (DTYPE(layers) i = 0; i < layers; ++i) {
        HB_ERRCHK(hipblasDgemm(ctx_stream.hipblas_H, HIPBLAS_OP_N, HIPBLAS_OP_N, m, n, k, &one, ctx_dev.K, m, ctx_stream.weights + i * nk, k,
                               &oneminus, ctx_stream.tmp_L, m));
        if (i < layers - 1) HB_ERRCHK(hipblasDscal(ctx_stream.hipblas_H, mn, &oneminus, ctx_stream.tmp_L, 1));
    }
    double total;
    HB_ERRCHK(hipblasDasum(ctx_stream.hipblas_H, mn, ctx_stream.tmp_L, 1, &total));
...
```

### Operating System

NAME="SLES" VERSION="15-SP5"

### CPU

model name      : AMD EPYC 7A53 64-Core Processor

### GPU

AMD Instinct MI250X

### ROCm Version

ROCm 6.2.2

### ROCm Component

hipBLAS

### Steps to Reproduce

Call stack:

#0  0x0000145f36850d2b in raise () from /lib64/libc.so.6                                                                                                                                                                                      #1  0x0000145f368523e5 in abort () from /lib64/libc.so.6                                                                                                                                                                                      
#2  0x0000145ec4a7bebf in rocblas_abort_once() () from /appl/lumi/SW/LUMI-24.03/G/EB/rocm/6.2.2/lib/librocblas.so.4                                                                                                                           
#3  0x0000145ec4a7be39 in rocblas_abort () from /appl/lumi/SW/LUMI-24.03/G/EB/rocm/6.2.2/lib/librocblas.so.4
#4  0x0000145ec41be139 in _rocblas_handle::_device_malloc::~_device_malloc() () from /appl/lumi/SW/LUMI-24.03/G/EB/rocm/6.2.2/lib/librocblas.so.4                                                                                             
#5  0x0000145ec49b1aed in rocblas_dasum () from /appl/lumi/SW/LUMI-24.03/G/EB/rocm/6.2.2/lib/librocblas.so.4  
#6  0x0000145f37198b9b in hipblasDasum () from /appl/lumi/SW/LUMI-24.03/G/EB/rocm/6.2.2/lib/libhipblas.so.2            
#7  0x0000145f399d054a in svr::solvers::score_weights::operator()(double const*) const () from ./libOnlineSVR.so       
#8  0x0000145f39c4932a in svr::datamodel::OnlineSVR::calc_weights(arma::Mat<double>&, arma::Mat<double> const&, arma::Mat<double> const&, unsigned int, unsigned short)::{lambda(double const*, double*)#3}::operator()(double const*, double*) const (x=0x1451049ae640, f=0x1451049aef18, this=<optimized out>) at /project/project_465002455/repo/tempus-core/SVRRoot/OnlineSVR/src/onlinesvr_train.cpp:396 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

[37mROCk module version 6.3.6 is loaded[0m
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
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
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
  Max Clock Freq. (MHz):   2000                               
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
      Size:                    131342572(0x7d420ec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131342572(0x7d420ec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131342572(0x7d420ec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
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
      Size:                    132063852(0x7df226c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132063852(0x7df226c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132063852(0x7df226c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        2                                  
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
      Size:                    132111292(0x7dfdbbc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132111292(0x7dfdbbc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132111292(0x7dfdbbc) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 4                  
*******                  
  Name:                    AMD EPYC 7A53 64-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7A53 64-Core Processor    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   0                                  
  Internal Node ID:        3                                  
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
      Size:                    132056216(0x7df0498) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132056216(0x7df0498) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132056216(0x7df0498) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 5                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-be39e3c4fae43a0e               
  Marketing Name:          AMD Instinct MI250X                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    4                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29704(0x7408)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   51456                              
  Internal Node ID:        4                                  
  Compute Unit:            110                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 78                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
Agent 6                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-74a5c2e324728f2d               
  Marketing Name:          AMD Instinct MI250X                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    5                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29704(0x7408)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   53504                              
  Internal Node ID:        5                                  
  Compute Unit:            110                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 78                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
Agent 7                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-083cc982efa6e8a3               
  Marketing Name:          AMD Instinct MI250X                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    6                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29704(0x7408)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   54784                              
  Internal Node ID:        6                                  
  Compute Unit:            110                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    TRUE                               
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 78                                 
  SDMA engine uCode::      8                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 4                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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

ROCm BLAS seems to be crashing every time I call this function for no apparent reason.

---

## 评论 (5 条)

### 评论 #1 — asenzz (2025-12-13T09:03:01Z)

Update: 
- The same code works on CUDA 12.6 - tested with 4 x NVidia A100 and 4 x V100. 
- The code works if I only use 1 HIP stream in parallel per-GPU, crashes when using 2 or 4 HIP streams, it doesn't seem like a memory issue.

---

### 评论 #2 — tcgu-amd (2025-12-18T20:52:01Z)

Hi @asenzz, thank you for reaching out! Did you create separate rocBLAS handle for each stream or did you share the same handle across multiple streams? Also can you please try with export ROCBLAS_STREAM_ORDER_ALLOC=1?

Thanks! 

---

### 评论 #3 — asenzz (2025-12-19T03:05:53Z)

This is how each stream is associated with a special HIP BLAS handle:

```
constexpr uint32_t C_hip_default_stream_flags = hipStreamDefault;
hipStream_t hipstream_j;
HIP_ERRCHK(hipStreamCreateWithFlags(&hipstream_j, C_hip_default_stream_flags));
hipblasHandle_t hipblas_H;
HB_ERRCHK(hipblasCreate(&hipblas_H));
HB_ERRCHK(hipblasSetStream(hipblas_H, hipstream_j));
HB_ERRCHK(hipblasSetPointerMode(hipblas_H, HIPBLAS_POINTER_MODE_HOST));
double *tmp_L, *weights;
HIP_ERRCHK(hipMallocAsync((void **) &tmp_L, L_size, hipstream_j));
HIP_ERRCHK(hipMallocAsync((void **) &weights, W_size, hipstream_j));
K_rhs_dev[i].stream_hipblas.emplace_back(dev_ctx::stream_ctx{hipstream_j, hipblas_H, tmp_L, weights});


```
I'll try ROCBLAS_STREAM_ORDER_ALLOC=1 and report back


---

### 评论 #4 — tcgu-amd (2026-01-30T18:08:29Z)

Hi, this issue is going to be closed due to inactivity. Please feel free to follow up below if further assistance is needed. Thanks!

---

### 评论 #5 — asenzz (2026-01-30T20:00:58Z)

Thanks for following up.

regards,

Žarko ASEN

***@***.***
[image: https://www.zarkoasen.com/tempus] <https://www.zarkoasen.com/tempus>


On Fri, Jan 30, 2026 at 6:08 PM Tim Gu ***@***.***> wrote:

> *tcgu-amd* left a comment (ROCm/ROCm#5772)
> <https://github.com/ROCm/ROCm/issues/5772#issuecomment-3824998579>
>
> Hi, this issue is going to be closed due to inactivity. Please feel free
> to follow up below if further assistance is needed. Thanks!
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/5772#issuecomment-3824998579>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ACS4YPNPCJMPQ6QB4Z6WZH34JOM3HAVCNFSM6AAAAACO5SBMSKVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZTQMRUHE4TQNJXHE>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---
