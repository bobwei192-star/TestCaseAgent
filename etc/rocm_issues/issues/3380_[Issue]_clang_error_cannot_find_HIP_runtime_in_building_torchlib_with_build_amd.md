# [Issue]: clang: error: cannot find HIP runtime in building torchlib with build_amd.py

> **Issue #3380**
> **状态**: closed
> **创建时间**: 2024-07-01T11:53:24Z
> **更新时间**: 2025-02-23T23:09:11Z
> **关闭时间**: 2024-07-18T17:29:58Z
> **作者**: minzhezhou
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3380

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

OS:
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
CPU: 
model name      : AMD Ryzen 7 5800X3D 8-Core Processor
GPU:
Marketing Name:          Radeon RX 7900 XTX                 
      Name:                    amdgcn-amd-amdhsa--gfx1100 



### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 7 5800X3D 8-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

HIPCC

### Steps to Reproduce

I installed AMD kernel driver and rocm following the the official guide.
I have my env variable setup:
export PATH=$PATH:/opt/rocm/bin
export HIP_PLATFORM=amd
export USE_ROCM=1
export ROCM_PATH=/opt/rocm
export HIP_CLANG_PATH=/opt/rocm/llvm/bin
export DEVICE_LIB_PATH=/opt/rocm/lib
export LD_LIBRARY_PATH=/opt/rocm/lib:$LD_LIBRARY_PATH
export HIP_PATH=$ROCM_PATH/hip
export ROCM_DEVICE_LIB_PATH=$ROCM_PATH/lib

and hipconfig --cpp_config shows:
-D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm/hip/include -I/opt/rocm-6.1.3/lib/llvm/lib/clang/17

Then I started to build torchlib:
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
sudo apt-get update
sudo apt-get install python3-dev python3-pip libyaml-dev
pip3 install -r requirements.txt
python3 tools/amd_build/build_amd.py
USE_ROCM=1 USE_NINJA=1 python3 setup.py install

I got the following error, at this stage:
[5748/8642] Building HIPCC object third_party/gloo/gloo/CMakeFiles/gloo_hip.dir/__/__/__/build/third_party/gloo/hip/gloo/gloo_hip_generated_hip.hip.o
FAILED: third_party/gloo/gloo/CMakeFiles/gloo_hip.dir/__/__/__/build/third_party/gloo/hip/gloo/gloo_hip_generated_hip.hip.o /home/jack/code/pytorch/build/third_party/gloo/gloo/CMakeFiles/gloo_hip.dir/__/__/__/build/third_party/gloo/hip/gloo/gloo_hip_generated_hip.hip.o 
cd /home/jack/code/pytorch/build/third_party/gloo/gloo/CMakeFiles/gloo_hip.dir/__/__/__/build/third_party/gloo/hip/gloo && /home/jack/code/miniconda3/lib/python3.12/site-packages/cmake/data/bin/cmake -E make_directory /home/jack/code/pytorch/build/third_party/gloo/gloo/CMakeFiles/gloo_hip.dir/__/__/__/build/third_party/gloo/hip/gloo/. && /home/jack/code/miniconda3/lib/python3.12/site-packages/cmake/data/bin/cmake -D verbose:BOOL=OFF -D build_configuration:STRING=RELEASE -D generated_file:STRING=/home/jack/code/pytorch/build/third_party/gloo/gloo/CMakeFiles/gloo_hip.dir/__/__/__/build/third_party/gloo/hip/gloo/./gloo_hip_generated_hip.hip.o -P /home/jack/code/pytorch/build/third_party/gloo/gloo/CMakeFiles/gloo_hip.dir/__/__/__/build/third_party/gloo/hip/gloo/gloo_hip_generated_hip.hip.o.cmake
clang: error: cannot find HIP runtime; provide its path via '--rocm-path', or pass '-nogpuinc' to build without HIP runtime



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.7.0 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.13
Runtime Ext Version:     1.4
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
  Name:                    AMD Ryzen 7 5800X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5800X3D 8-Core Processor
  Vendor Name:             CPU                                

  .......


Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-9758f813d851a86f               
  Marketing Name:          Radeon RX 7900 XTX                 
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
    L2:                      6144(0x1800) KB                    
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   3584                               
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 202                                
  SDMA engine uCode::      20                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1100         
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

## 评论 (7 条)

### 评论 #1 — minzhezhou (2024-07-02T13:11:00Z)

I can only compile with:
/opt/rocm-6.1.3/bin/hipcc  --hip-device-lib-path=/opt/rocm-6.1.3/amdgcn/bitcode -L/usr/lib/gcc/x86_64-linux-gnu/11 test.cpp -o testout
1.--hip-device-lib-path=/opt/rocm-6.1.3/amdgcn/bitcode, (cannot find ROCm device library if removed)
2.-L/usr/lib/gcc/x86_64-linux-gnu/11 (unable to find library -lstdc++ if removed)

---

### 评论 #2 — minzhezhou (2024-07-03T01:17:52Z)

After adding the two flags into CMakelist.txt, still got another error:
In file included from /opt/rocm-6.1.3/lib/llvm/lib/clang/17/include/__clang_hip_runtime_wrapper.h:50:
/opt/rocm-6.1.3/lib/llvm/lib/clang/17/include/cuda_wrappers/cmath:27:15: fatal error: 'cmath' file not found
   27 | #include_next < cmath >
      |               ^~~~~~~
1 error generated when compiling for host.
CMake Error at gloo_hip_generated_nccl.hip.o.cmake:146 (message):

What is the next cmath it is looking for?

---

### 评论 #3 — minzhezhou (2024-07-04T23:07:54Z)

The error was due to lack of stdlibc++-13dev, can be fixed by:
apt install libstdc++-13-dev

---

### 评论 #4 — ppanchad-amd (2024-07-17T15:16:22Z)

@minzhezhou Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #5 — schung-amd (2024-07-18T17:29:58Z)

Hi @minzhezhou,

I was able to reproduce your issue following the steps you provided. 

The environment variable HIP_PATH, which is set to $ROCM_PATH/hip, should instead be set to $ROCM_PATH, which with your other environment variables will result in hipconfig --cpp_config showing:
 -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm/include -I/opt/rocm-6.1.3/lib/llvm/lib/clang/17
Using this configuration I was able to complete the pytorch installation.

Additionally, in general, you do not need to set any environment variables explicitly when installing ROCm on a fresh install of Ubuntu 22. I was able to install pytorch using the steps you provided without setting any of the environment variables. The HIP runtime specifically will automatically be detected unless you override its path using environment variables; see https://releases.llvm.org/18.1.0/tools/clang/docs/HIPSupport.html#order-of-precedence-for-hip-path for details.

I'm marking this issue as closed, but feel free to reopen it if you experience further issues. Thanks!

---

### 评论 #6 — minzhezhou (2024-07-18T22:56:18Z)

Got it, thanks for pointing out the root cause!

---

### 评论 #7 — numpde (2025-02-23T23:09:10Z)

> The environment variable HIP_PATH, which is set to $ROCM_PATH/hip, should instead be set to $ROCM_PATH

Holy smokes!

🙏🏼

---
