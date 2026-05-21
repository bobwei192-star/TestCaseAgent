# [Issue]: Radeon AI PRO R9700 support for Peer-2-Peer GDRMA using rccl-tests

> **Issue #5571**
> **状态**: closed
> **创建时间**: 2025-10-24T23:48:40Z
> **更新时间**: 2026-01-21T20:57:56Z
> **关闭时间**: 2026-01-21T20:57:56Z
> **作者**: rksawyer
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5571

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- tcgu-amd

## 描述

### Problem Description

all_reduce_perf is the same when P2P GRDMA is enabled or disabled.  Given the bandwidth numbers, it appears P2P is not being used.

**P2P DMABUF enabled**

```
$ NCCL_DMABUF_ENABLE=1  mpirun -H 10.20.1.125,10.20.1.126 -np 2 --mca btl_tcp_if_include enp165s0f1np1 ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 1
# Collective test starting: all_reduce_perf
# nThread 1 nGpus 1 minBytes 8 maxBytes 134217728 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
#
rccl-tests: Version develop:33cc4df
# Using devices
#  Rank  0 Group  0 Pid   4791 on     corona device  0 [0000:07:00] AMD Radeon AI PRO R9700
#  Rank  1 Group  0 Pid   5418 on     bootes device  0 [0000:07:00] AMD Radeon AI PRO R9700
#
#                                                              out-of-place                       in-place          
#       size         count      type   redop    root     time   algbw   busbw #wrong     time   algbw   busbw #wrong                               
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)                                      
           8             2     float     sum      -1    47.35    0.00    0.00      0    45.17    0.00    0.00      0
          16             4     float     sum      -1    42.05    0.00    0.00      0    42.05    0.00    0.00      0
          32             8     float     sum      -1    44.49    0.00    0.00      0    43.13    0.00    0.00      0
          64            16     float     sum      -1    60.08    0.00    0.00      0    43.34    0.00    0.00      0
         128            32     float     sum      -1    47.99    0.00    0.00      0    44.35    0.00    0.00      0
         256            64     float     sum      -1    44.09    0.01    0.01      0    44.22    0.01    0.01      0
         512           128     float     sum      -1    44.14    0.01    0.01      0    43.33    0.01    0.01      0
        1024           256     float     sum      -1    44.34    0.02    0.02      0    43.50    0.02    0.02      0
        2048           512     float     sum      -1    43.28    0.05    0.05      0    44.41    0.05    0.05      0
        4096          1024     float     sum      -1    54.46    0.08    0.08      0    44.41    0.09    0.09      0
        8192          2048     float     sum      -1    45.50    0.18    0.18      0    45.42    0.18    0.18      0
       16384          4096     float     sum      -1    47.31    0.35    0.35      0    48.31    0.34    0.34      0
       32768          8192     float     sum      -1    50.34    0.65    0.65      0    47.04    0.70    0.70      0
       65536         16384     float     sum      -1    50.96    1.29    1.29      0    52.38    1.25    1.25      0
      131072         32768     float     sum      -1    61.35    2.14    2.14      0    71.90    1.82    1.82      0
      262144         65536     float     sum      -1    77.56    3.38    3.38      0    81.61    3.21    3.21      0
      524288        131072     float     sum      -1    85.53    6.13    6.13      0    83.31    6.29    6.29      0
     1048576        262144     float     sum      -1    163.8    6.40    6.40      0    169.3    6.19    6.19      0
     2097152        524288     float     sum      -1    280.7    7.47    7.47      0    269.0    7.80    7.80      0
     4194304       1048576     float     sum      -1    455.6    9.21    9.21      0    429.4    9.77    9.77      0
     8388608       2097152     float     sum      -1    869.2    9.65    9.65      0   1149.4    7.30    7.30      0
    16777216       4194304     float     sum      -1   1648.6   10.18   10.18      0   1646.1   10.19   10.19      0
    33554432       8388608     float     sum      -1   3241.1   10.35   10.35      0   3229.6   10.39   10.39      0
    67108864      16777216     float     sum      -1   6406.3   10.48   10.48      0   6434.8   10.43   10.43      0
   134217728      33554432     float     sum      -1    12463   10.77   10.77      0    12457   10.77   10.77      0
# Errors with asterisks indicate errors that have exceeded the maximum threshold.
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 3.51213 
#
# Collective test concluded: all_reduce_perf
```

**P2P Disabled**
```
$ NCCL_NET_GDR_LEVEL=LOC  mpirun -H 10.20.1.125,10.20.1.126 -np 2 --mca btl_tcp_if_include enp165s0f1np1 ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 1
# Collective test starting: all_reduce_perf
# nThread 1 nGpus 1 minBytes 8 maxBytes 134217728 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
#
rccl-tests: Version develop:33cc4df
# Using devices
#  Rank  0 Group  0 Pid   6081 on     corona device  0 [0000:07:00] AMD Radeon AI PRO R9700
#  Rank  1 Group  0 Pid   6768 on     bootes device  0 [0000:07:00] AMD Radeon AI PRO R9700
#
#                                                              out-of-place                       in-place          
#       size         count      type   redop    root     time   algbw   busbw #wrong     time   algbw   busbw #wrong                               
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)                                      
           8             2     float     sum      -1    45.44    0.00    0.00      0    38.77    0.00    0.00      0
          16             4     float     sum      -1    36.88    0.00    0.00      0    36.16    0.00    0.00      0
          32             8     float     sum      -1    46.92    0.00    0.00      0    38.49    0.00    0.00      0
          64            16     float     sum      -1    40.10    0.00    0.00      0    37.26    0.00    0.00      0
         128            32     float     sum      -1    40.10    0.00    0.00      0    39.75    0.00    0.00      0
         256            64     float     sum      -1    38.49    0.01    0.01      0    37.23    0.01    0.01      0
         512           128     float     sum      -1    37.78    0.01    0.01      0    38.37    0.01    0.01      0
        1024           256     float     sum      -1    38.07    0.03    0.03      0    38.41    0.03    0.03      0
        2048           512     float     sum      -1    37.55    0.05    0.05      0    37.45    0.05    0.05      0
        4096          1024     float     sum      -1    39.15    0.10    0.10      0    37.39    0.11    0.11      0
        8192          2048     float     sum      -1    38.17    0.21    0.21      0    39.40    0.21    0.21      0
       16384          4096     float     sum      -1    38.77    0.42    0.42      0    39.83    0.41    0.41      0
       32768          8192     float     sum      -1    45.86    0.71    0.71      0    44.36    0.74    0.74      0
       65536         16384     float     sum      -1    49.07    1.34    1.34      0    49.06    1.34    1.34      0
      131072         32768     float     sum      -1    60.00    2.18    2.18      0    61.93    2.12    2.12      0
      262144         65536     float     sum      -1    86.53    3.03    3.03      0    87.10    3.01    3.01      0
      524288        131072     float     sum      -1    80.17    6.54    6.54      0    79.16    6.62    6.62      0
     1048576        262144     float     sum      -1    158.1    6.63    6.63      0    157.9    6.64    6.64      0
     2097152        524288     float     sum      -1    283.8    7.39    7.39      0    257.5    8.14    8.14      0
     4194304       1048576     float     sum      -1    464.2    9.04    9.04      0    442.4    9.48    9.48      0
     8388608       2097152     float     sum      -1    962.7    8.71    8.71      0    937.7    8.95    8.95      0
    16777216       4194304     float     sum      -1   1709.6    9.81    9.81      0   1696.8    9.89    9.89      0
    33554432       8388608     float     sum      -1   3322.5   10.10   10.10      0   3344.6   10.03   10.03      0
    67108864      16777216     float     sum      -1   6380.6   10.52   10.52      0   6368.7   10.54   10.54      0
   134217728      33554432     float     sum      -1    12402   10.82   10.82      0    12396   10.83   10.83      0
# Errors with asterisks indicate errors that have exceeded the maximum threshold.
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 3.53671 
#
# Collective test concluded: all_reduce_perf
```

### Operating System

Ubuntu 24.04.3 LTS (Noble Numbat)

### CPU

AMD EPYC 9115 16-Core Processor

### GPU

AMD Radeon AI PRO R9700

### ROCm Version

ROCm 7.0.2

### ROCm Component

rccl

### Steps to Reproduce

1. Run rccl-test between 2 nodes with NCCL_DMABUF_ENABLE=1
```
NCCL_DMABUF_ENABLE=1  mpirun -H 10.20.1.125,10.20.1.126 -np 2 --mca btl_tcp_if_include enp165s0f1np1 ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 1
```
2. Run rccl-test with NCCL_NET_GDR_LEVEL=LOC : Never use GPU Direct RDMA (always disabled).
```
NCCL_NET_GDR_LEVEL=LOC  mpirun -H 10.20.1.125,10.20.1.126 -np 2 --mca btl_tcp_if_include enp165s0f1np1 ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 1
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:                    AMD EPYC 9115 16-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 9115 16-Core Processor    
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
  Max Clock Freq. (MHz):   4118                               
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
      Size:                    131577580(0x7d7b6ec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131577580(0x7d7b6ec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131577580(0x7d7b6ec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131577580(0x7d7b6ec) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 9115 16-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 9115 16-Core Processor    
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   4118                               
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
      Size:                    132056040(0x7df03e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    132056040(0x7df03e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132056040(0x7df03e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132056040(0x7df03e8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-0d06b080997bb300               
  Marketing Name:          AMD Radeon AI PRO R9700            
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
    L1:                      32(0x20) KB                        
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30033(0x7551)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   1792                               
  Internal Node ID:        2                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 752                                
  SDMA engine uCode::      749                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33406976(0x1fdc000) KB             
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

## 评论 (6 条)

### 评论 #1 — tcgu-amd (2025-10-27T15:31:25Z)

Hi @rksawyer, thanks for reaching out! Currently gfx12 (which includes R9700) support for RDMA is still a work in progress (https://github.com/ROCm/rccl/pull/2000). The feature is currently estimated to land around ROCm 7.1. Please let me know if you have any other questions. Thanks! 

---

### 评论 #2 — rksawyer (2025-10-27T20:57:36Z)

@tcgu-amd Thank you.  Do you know the estimated release schedule for ROCm 7.1?

---

### 评论 #3 — tcgu-amd (2025-10-28T14:55:54Z)

@rksawyer I don't have the exact dates, but I would say sometime mid to late November perhaps? 

---

### 评论 #4 — rksawyer (2025-12-09T17:40:15Z)

@tcgu-amd It looks like (https://github.com/ROCm/rccl/pull/2000) was closed.  Do you know if there is another solution to gfx12 support for RDMA?

---

### 评论 #5 — tcgu-amd (2025-12-09T19:08:05Z)

Hi @rksawyer yes, I believe it is now covered by https://github.com/ROCm/rocm-systems/pull/1670 in rocm libraries instead. It should be merged now so please feel free to test it out. The official release should come out by ROCm 7.2 (expected). 

Edit: Another PR in ROCR runtime is required as well https://github.com/ROCm/rocm-systems/pull/674

---

### 评论 #6 — tcgu-amd (2026-01-21T20:57:56Z)

Hi @rksawyer, I will be closing this issue since both PRs are now merged. Please feel free to let me know if further assistance is needed. Thanks! 

---
