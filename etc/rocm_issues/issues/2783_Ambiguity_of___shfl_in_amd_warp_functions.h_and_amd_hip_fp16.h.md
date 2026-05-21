# Ambiguity of "__shfl*" in amd_warp_functions.h and amd_hip_fp16.h

> **Issue #2783**
> **状态**: closed
> **创建时间**: 2024-01-08T17:55:13Z
> **更新时间**: 2024-04-23T10:07:13Z
> **关闭时间**: 2024-02-02T22:04:57Z
> **作者**: buchijw
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2783

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I was tr‌ying to build [pytorch_sparse](https://github.com/rusty1s/pytorch_sparse) using ROCm 6.0.0. There were erro‌rs relating to an ambiguity of `__shfl*` as they‌‌ are present in both `amd_warp_functions.h` and `amd_hip_fp16.h`

```
/home/labhhc/Documents/pyg_dmm/pytorch_sparse/csrc/hip/spmm_hip.hip:70:21: error: call to '__shfl' is ambiguous
            vals[i] = SHFL_SYNC(FULL_MASK, val, i);
                      ^~~~~~~~~~~~~~~~~~~~~~~~~~~~
  /home/labhhc/Documents/pyg_dmm/pytorch_sparse/csrc/hip/../hip/utils.cuh:27:37: note: expanded from macro 'SHFL_SYNC'
  #define SHFL_SYNC(mask, var, delta) __shfl(var, delta)
                                      ^~~~~~
  /home/labhhc/Documents/pyg_dmm/pytorch_sparse/csrc/hip/spmm_hip.hip:149:29: note: in instantiation of function template specialization 'spmm_kernel<c10::Half, MAX, false>' requested here
         hipLaunchKernelGGL(( spmm_kernel<scalar_t, REDUCE, false>), dim3(BLOCKS), dim3(THREADS), 0, stream,
                              ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:94:7: note: candidate function
  float __shfl(float var, int src_lane, int width = warpSize) {
        ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:101:8: note: candidate function
  double __shfl(double var, int src_lane, int width = warpSize) {
         ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:80:5: note: candidate function
  int __shfl(int var, int src_lane, int width = warpSize) {
      ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:87:14: note: candidate function
  unsigned int __shfl(unsigned int var, int src_lane, int width = warpSize) {
               ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:115:6: note: candidate function
  long __shfl(long var, int src_lane, int width = warpSize)
       ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:135:15: note: candidate function
  unsigned long __shfl(unsigned long var, int src_lane, int width = warpSize) {
                ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:154:11: note: candidate function
  long long __shfl(long long var, int src_lane, int width = warpSize)
            ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:169:20: note: candidate function
  unsigned long long __shfl(unsigned long long var, int src_lane, int width = warpSize) {
                     ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_hip_fp16.h:1748:16: note: candidate function
          __half __shfl(__half var, int src_lane, int width = warpSize) {
                 ^
  /home/labhhc/Documents/pyg_dmm/pytorch_sparse/csrc/hip/spmm_hip.hip:184:14: error: call to '__shfl_down' is ambiguous
        val += SHFL_DOWN_SYNC(FULL_MASK, val, i);
               ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  /home/labhhc/Documents/pyg_dmm/pytorch_sparse/csrc/hip/../hip/utils.cuh:26:42: note: expanded from macro 'SHFL_DOWN_SYNC'
  #define SHFL_DOWN_SYNC(mask, var, delta) __shfl_down(var, delta)
                                           ^~~~~~~~~~~
  /home/labhhc/Documents/pyg_dmm/pytorch_sparse/csrc/hip/spmm_hip.hip:232:27: note: in instantiation of function template specialization 'spmm_value_bw_kernel<c10::Half, SUM>' requested here
       hipLaunchKernelGGL(( spmm_value_bw_kernel<scalar_t, REDUCE>), dim3(BLOCKS), dim3(THREADS), 0, stream,
                            ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:305:7: note: candidate function
  float __shfl_down(float var, unsigned int lane_delta, int width = warpSize) {
        ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:312:8: note: candidate function
  double __shfl_down(double var, unsigned int lane_delta, int width = warpSize) {
         ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:290:5: note: candidate function
  int __shfl_down(int var, unsigned int lane_delta, int width = warpSize) {
      ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:298:14: note: candidate function
  unsigned int __shfl_down(unsigned int var, unsigned int lane_delta, int width = warpSize) {
               ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:326:6: note: candidate function
  long __shfl_down(long var, unsigned int lane_delta, int width = warpSize)
       ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:346:15: note: candidate function
  unsigned long __shfl_down(unsigned long var, unsigned int lane_delta, int width = warpSize)
                ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:366:11: note: candidate function
  long long __shfl_down(long long var, unsigned int lane_delta, int width = warpSize)
            ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_warp_functions.h:379:20: note: candidate function
  unsigned long long __shfl_down(unsigned long long var, unsigned int lane_delta, int width = warpSize)
                     ^
  /opt/rocm-6.0.0/include/hip/amd_detail/amd_hip_fp16.h:1776:17: note: candidate function
           __half __shfl_down(__half var, unsigned int lane_delta, int width = warpSize) {
```


### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 9 3900X 12-Core Processor

### GPU

AMD Radeon RX 6900 XT

### Other

_No response_

### ROCm Version

ROCm 6.0.0

### ROCm Component

HIP

### Steps to Reproduce

1. Install ROCm 6.0.0 using amdgpu-installer:
`sudo amdgpu-install --usecase=hiplibsdk,rocm,openclsdk`
2. Reboot
3. Create conda env and install PyTorch:
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6`
4. Clone and build pytorch_sparse:
```
git clone https://github.com/rusty1s/pytorch_sparse
export PATH=$PATH:/opt/rocm/bin
export LD_LIBRARY_PATH=/opt/rocm/lib64
export DYLD_LIBRARY_PATH=/opt/rocm/lib
export CMAKE_PREFIX_PATH=/opt/rocm
CMAKE_CXX_COMPILER=/opt/rocm/bin/amdclang++ CMAKE_C_COMPILER=/opt/rocm/bin/amdclang pip install . -vvv |& tee ~/build_sparse.log
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

<details>
<summary> rocminfo </summary>
<br>
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    AMD Ryzen 9 3900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 3900X 12-Core Processor
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
  Max Clock Freq. (MHz):   3800                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98763960(0x5e304b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98763960(0x5e304b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98763960(0x5e304b8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-270b352c3aab7c1c               
  Marketing Name:          AMD Radeon RX 6900 XT              
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
  Max Clock Freq. (MHz):   2660                               
  BDFID:                   2048                               
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
  SIMDs per CU:            2                                  
  Shader Engines:          4                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
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
  Packet Processor uCode:: 116                                
  SDMA engine uCode::      83                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
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
*** Done ***
</details>

### Additional Information

_No response_

---

## 评论 (8 条)

### 评论 #1 — nartmada (2024-01-09T21:26:42Z)

Internal ticket has been created to track the issue.

---

### 评论 #2 — akondrat-amd (2024-01-15T20:44:03Z)

This is not ROCm issue, the function __shfl() is overloaded and supports multiple data types. The problem occurs in python_sparse when instantiating a function template 'spmm_kernel<c10::Half, MAX, false>', the "c10::Half" type is not known to ROCm, so it cannot find a suitable function for it.
The type "c10::Half" should be aliased to ROCm "__half" type somewhere in python_sparse code before this kernel is compiled. You should post this issue to python_sparse saying that it tries to compile ROCm kernel with "c10::Half" type which is not known to ROCm.

---

### 评论 #3 — ashwinma (2024-01-23T08:46:06Z)

@buchijw can you please pull in the latest changes from pytorch_sparse and try again? 

Details: This [PR ](https://github.com/rusty1s/pytorch_sparse/pull/360) landed on pytorch_sparse:master branch that should help resolve your issue.

---

### 评论 #4 — nartmada (2024-01-30T16:34:15Z)

Hi @buchijw, did you get a chance to try the PR as recommended by ashwinma?  Thanks.

---

### 评论 #5 — nartmada (2024-02-02T22:04:57Z)

Closing this ticket as there is no response from @buchijw.  Please re-open the ticket if you still run into this issue.  Thanks.

---

### 评论 #6 — dandingdjianjiao (2024-04-19T14:52:56Z)

@buchijw Hi,I've got the same issue while building the newest version of torch_scatter(v2.1.2)  and torch_sparse(v0.6.18) packages with ROCm6.0.2. How did you solve this issue?

---

### 评论 #7 — ashwinma (2024-04-19T17:58:04Z)

@dandingdjianjiao please pull from the `master` branch of both repos. The release tags seem to be outdated on both the repos.

---

### 评论 #8 — buchijw (2024-04-23T10:07:12Z)

> @buchijw Hi,I've got the same issue while building the newest version of torch_scatter(v2.1.2) and torch_sparse(v0.6.18) packages with ROCm6.0.2. How did you solve this issue?

@dandingdjianjiao the issues were solved thank to @ashwinma. You just need to clone the `master` branch and build with pip.

---
