# [Issue]: cmake under "/opt/rocm/lib/cmake/hsa-runtime64/" in wsl2 not correctly set the library

> **Issue #3606**
> **状态**: closed
> **创建时间**: 2024-08-17T01:02:51Z
> **更新时间**: 2024-08-21T14:20:49Z
> **关闭时间**: 2024-08-21T14:20:49Z
> **作者**: ghost
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3606

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

using rocm under WSL2.
install following instruct under https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html.

when I tried build llama.cpp using cmake, I got an error:

 CMake Error at /opt/rocm/lib/cmake/hsa-runtime64/hsa-runtime64Targets.cmake:80 (message):
 The imported target "hsa-runtime64::hsa-runtime64" references the file
         /opt/rocm/lib/libhsa-runtime64.so.1.13.60103
        but this file does not exist.  Possible reasons include:
...

then llama.cpp will failed to build.

but when I use makefile, everything is OK.

I list the lib in `/opt/rocm/lib/` but only got `libhsa-runtime64.so.1.2`, so I replace all `1.13.60103` to  `1.2` in  `/opt/rocm/lib/cmake/hsa-runtime64`, then cmake check passed and build success.

I want to know this is a common issue or just an install error? 


### Operating System

22.04.4 LTS (Jammy Jellyfish) under Windows 10.0.22631

### CPU

AMD Ryzen 7 7700

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

rocm-cmake

### Steps to Reproduce

1. setup wsl2
2. install rocm using `amdgpu-install -y --usecase=wsl,rocm --no-dkms`
3. install llama.cpp-python using `CC=hipcc CXX=hipcc CMAKE_ARGS="-DGGML_HIPBLAS=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir`, using cmake to build llama.cpp is also affected
4. cmake will report the error
5. execute `ls /opt/rocm/lib/`, only got 'libhsa-runtime64.so.1.2'
6. modify cmake under /opt/rocm/lib/cmake/hsa-runtime64
7. build passed


### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          NO

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    CPU                                
  Uuid:                    CPU-XX                             
  Marketing Name:          CPU                                
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
  Chip ID:                 0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    15841624(0xf1b958) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15841624(0xf1b958) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Marketing Name:          AMD Radeon RX 7900 XT              
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        16(0x10)                           
  Queue Min Size:          4096(0x1000)                       
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      6144(0x1800) KB                    
    L3:                      81920(0x14000) KB                  
  Chip ID:                 29772(0x744c)                      
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2075                               
  Internal Node ID:        1                                  
  Compute Unit:            84                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
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
  Packet Processor uCode:: 2250                               
  SDMA engine uCode::      20                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20906156(0x13f00ac) KB             
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

windows driver version is 24.7.1

---

## 评论 (9 条)

### 评论 #1 — Kademo15 (2024-08-19T15:52:38Z)

I have the exact same error trying to build bitsandbytes from source with the new multi-backend-refactor branch. 
https://github.com/bitsandbytes-foundation/bitsandbytes/issues/1323

---

### 评论 #2 — harkgill-amd (2024-08-19T18:33:12Z)

Hi @null-define, thank you for providing the steps to reproduce. We will try to repro the issue internally to further investigate.

@Kademo15, are you also experiencing the issue on a WSL environment?

---

### 评论 #3 — schung-amd (2024-08-19T19:37:09Z)

Hi @null-define, I was able to reproduce your issue with your exact process. From a fresh install, I was able to install llama-cpp-python without issues with the following:

1. Set up Adrenalin 24.6.1 and ROCm 6.1.3 for WSL according to the official docs (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html); you've stated your Windows driver version is 24.7.1, but currently only Adrenalin 24.6.1 is supported for WSL2 + ROCm.
2. Install torch for WSL according to the official docs (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html), ensuring that libhsa-runtime64 is copied over to the torch/lib folder in step 4.
3. Install llama-cpp-python using the provided command, but without --no-cache-dir; i.e. `CC=hipcc CXX=hipcc CMAKE_ARGS="-DGGML_HIPBLAS=on" pip install llama-cpp-python --upgrade --force-reinstall`.

I was also able to install llama-cpp-python without any additional flags, i.e. `pip install llama-cpp-python`; by trial and error I found that `--no-cache-dir` was the problem. Let me know if following this process and removing this flag doesn't work for you, either for llama-python-cpp or llama.cpp itself.

---

### 评论 #4 — Kademo15 (2024-08-20T03:26:34Z)

> Hi @null-define, thank you for providing the steps to reproduce. We will try to repro the issue internally to further investigate.
> 
> @Kademo15, are you also experiencing the issue on a WSL environment?

Yes as mentioned in my bitsandbytes issue i was using wsl. I got it working with the fix @null-define suggested by manually replacing all 1.13.60103 to 1.2 in /opt/rocm/lib/cmake/hsa-runtime64

---

### 评论 #5 — ghost (2024-08-20T14:51:42Z)

> Hi @null-define, I was able to reproduce your issue with your exact process. From a fresh install, I was able to install llama-cpp-python without issues with the following:
> 
> 1. Set up Adrenalin 24.6.1 and ROCm 6.1.3 for WSL according to the official docs (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html); you've stated your Windows driver version is 24.7.1, but currently only Adrenalin 24.6.1 is supported for WSL2 + ROCm.
> 2. Install torch for WSL according to the official docs (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html), ensuring that libhsa-runtime64 is copied over to the torch/lib folder in step 4.
> 3. Install llama-cpp-python using the provided command, but without --no-cache-dir; i.e. `CC=hipcc CXX=hipcc CMAKE_ARGS="-DGGML_HIPBLAS=on" pip install llama-cpp-python --upgrade --force-reinstall`.
> 
> I was also able to install llama-cpp-python without any additional flags, i.e. `pip install llama-cpp-python`; by trial and error I found that `--no-cache-dir` was the problem. Let me know if following this process and removing this flag doesn't work for you, either for llama-python-cpp or llama.cpp itself.

Thanks for your reply.

### for driver version mismatch, it's my fault.
- I thought 24.7.1 is newer than 24.6.1, it should be compatible for wsl2, so I use the latest version.
- if the version is not  compatible ,I thought it should have an error or warning on installation.
- I will switch to the 24.6.1 if I meet any new problems.
### for the build flag.
-  if you do not use `--no-cache-dir`, pip may use previous wheel already built on your machine. please make sure your pip cache do not contains llama.cpp if you build with cache.
- if you use `pip install llama-cpp-python` without any flag, ROCM feature will not be included, only CPU feature will be used. 
- I tried to clean all my pip cache and build llama-cpp-python with your flag and original hsa-runtime64 cmake, problem is still there.

it seems it's just a simple cmake script error or a installation/compatible issue.

by execute `ls /opt/rocm/lib/ | grep libhsa-runtime64`, I can only get 
libhsa-runtime64.so
libhsa-runtime64.so.1
libhsa-runtime64.so.1.2
but all cmake under /opt/rocm/lib/cmake/hsa-runtime64 set the lib to libhsa-runtime64.so.1.13.60103.

I searched ROCm project but can't find the source code which build the libhsa-runtime64.so

can you check the result of `ls /opt/rocm/lib/ | grep libhsa-runtime64` and the version string in `/opt/rocm/lib/cmake/hsa-runtime64` is match or not? thanks a lot

if your result is match, maybe It's just my personal installation issue or personal env problem. I will close this issue.

Thanks for your reply again.




---

### 评论 #6 — schung-amd (2024-08-20T20:40:09Z)

Thanks for the followup! I can reproduce your issue with pip install llama-cpp-python and flags set to build with hipBLAS. The issue seems to be that ROCm 6.1.3 is building the HSA runtime to *.so.1.2 instead of *.so.1.13.60103 as would be expected from the ROCm version number. You can see as well that other libraries in /opt/rocm/lib have the version 1.13.60103 as expected, and installing ROCm 6.1.3 from the same files on native Ubuntu 22.04 also results in this extension. I'm reaching out to our WSL team to figure out why this is happening.

In the meantime, you have found a workaround by altering files to refer to *.so.1.2 specifically, but are you able to use llama with this installation? I'm curious as to whether this works. You also mentioned being able to install llama from the makefile without issue; I can reproduce this as well. This makes it seem like the issue is on the llama-cpp-python end, but I'd like to make sure this is actually a working installation using the hipBLAS backend and not just the installation suppressing errors.

Regarding the Windows driver version, in my experience it's currently possible to build everything with the wrong drivers without an error, and the only sign will be if/when things break. I strongly recommend switching to 24.6.1 for WSL support, although this is not the root cause of your issue as I can reproduce it with the supported Windows driver.

---

### 评论 #7 — ghost (2024-08-21T03:24:24Z)

> Thanks for the followup! I can reproduce your issue with pip install llama-cpp-python and flags set to build with hipBLAS. The issue seems to be that ROCm 6.1.3 is building the HSA runtime to *.so.1.2 instead of *.so.1.13.60103 as would be expected from the ROCm version number. You can see as well that other libraries in /opt/rocm/lib have the version 1.13.60103 as expected, and installing ROCm 6.1.3 from the same files on native Ubuntu 22.04 also results in this extension. I'm reaching out to our WSL team to figure out why this is happening.
> 
> In the meantime, you have found a workaround by altering files to refer to *.so.1.2 specifically, but are you able to use llama with this installation? I'm curious as to whether this works. You also mentioned being able to install llama from the makefile without issue; I can reproduce this as well. This makes it seem like the issue is on the llama-cpp-python end, but I'd like to make sure this is actually a working installation using the hipBLAS backend and not just the installation suppressing errors.
> 
> Regarding the Windows driver version, in my experience it's currently possible to build everything with the wrong drivers without an error, and the only sign will be if/when things break. I strongly recommend switching to 24.6.1 for WSL support, although this is not the root cause of your issue as I can reproduce it with the supported Windows driver.


I am able to run llama.cpp after changing the cmake. output seems right but I have not test the precision.
Install llama from the makefile is Okay, this may because makefile dose not use cmake to define the library usgae(I guess).

I also noticed other libraries in /opt/rocm/lib have the version 1.13.60103 as expected, so I guessed it should be an installation issue in the first time(like HSA installed from a wrong package, mirror for HSA is not the latest,  etc). then I tried to reinstall ROCm with different flags, results are same.

About  the Windows driver version, I will switch back to 24.6.1 if I have time.
Thanks a lot.


---

### 评论 #8 — schung-amd (2024-08-21T13:27:45Z)

After speaking with the internal team, your workaround should function correctly. 1.2 is the WSL-specific version of the HSA runtime, but cmake does not know about this and is still looking for the native linux version. An easier way to implement the workaround is to create a link:
```
cd /opt/rocm/lib/
ln -s libhsa-runtime64.so.1.2 libhsa-runtime64.so.1.13.60103
```
This should be part of the WSL + ROCm guide, as otherwise HIP applications will not build using cmake, and we're discussing this internally. In the future, these runtimes will hopefully be unified, but for now this link will have to be created and updated for each ROCm version that gets WSL support.

Thanks again for bringing this to our attention, as while this is a known issue internally there is certainly a lack of documentation we need to address.

---

### 评论 #9 — ghost (2024-08-21T14:20:49Z)

> After speaking with the internal team, your workaround should function correctly. 1.2 is the WSL-specific version of the HSA runtime, but cmake does not know about this and is still looking for the native linux version. An easier way to implement the workaround is to create a link:
> 
> ```
> cd /opt/rocm/lib/
> ln -s libhsa-runtime64.so.1.2 libhsa-runtime64.so.1.13.60103
> ```
> 
> This should be part of the WSL + ROCm guide, as otherwise HIP applications will not build using cmake, and we're discussing this internally. In the future, these runtimes will hopefully be unified, but for now this link will have to be created and updated for each ROCm version that gets WSL support.
> 
> Thanks again for bringing this to our attention, as while this is a known issue internally there is certainly a lack of documentation we need to address.

@schung-amd  Thanks for your confirmation and solution. hope the official doc could be updated soon.

@Kademo15 you can try the solution provided by AMD friends. my solution may not work in other projects.


---
