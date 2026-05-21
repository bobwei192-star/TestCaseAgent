# [Issue]: Build instructions are wrong, don't work.

> **Issue #4190**
> **状态**: closed
> **创建时间**: 2024-12-23T11:05:12Z
> **更新时间**: 2025-01-07T14:35:18Z
> **关闭时间**: 2025-01-07T14:35:18Z
> **作者**: ETJAKEOC
> **标签**: Under Investigation, ROCm 6.3.0, MSI Radeon RX 560 4GB OC Edition
> **URL**: https://github.com/ROCm/ROCm/issues/4190

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.3.0** (颜色: #ededed)
- **MSI Radeon RX 560 4GB OC Edition** (颜色: #ededed)

## 描述

### Problem Description

The build instructions provided in this main repository simply don't work. There is no `tools` directory to run, there is no `ROCm` folder, I have no idea what these instructions are written for, but it seems clear to me that they are completely out of date and need to be updated appropriately, since I cannot run a single command in this build sequence past `repo init && repo sync`

### Operating System

Arch

### CPU

AMD A8-6600K APU with Radeon(tm) HD Graphics

### GPU

MSI Radeon RX 560 4GB OC Edition

### ROCm Version

ROCm 6.3.0

### ROCm Component

_No response_

### Steps to Reproduce

```bash
mkdir ROCM && cd ROCM
repo init -u http://github.com/ROCm/ROCm.git
repo sync -j1
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
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
  Name:                    AMD A8-6600K APU with Radeon(tm) HD Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD A8-6600K APU with Radeon(tm) HD Graphics
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
    L1:                      16384(0x4000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3900                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    31888000(0x1e69280) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31888000(0x1e69280) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31888000(0x1e69280) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***

### Additional Information

```bash
cat /etc/environment

ROC_ENABLE_PRE_VEGA=1
RUSTICLE_ENABLE=amdgpu
OCL_ICD_VENDORS=/etc/OpenCL/vendors/amd.icd

GPU_ARCHS=gfx803
GPU_FORCE_64BIT_PTR=1
GPU_MAX_HEAP_SIZE=100
GPU_MAX_ALLOC_PERCENT=100
GPU_SINGLE_ALLOC_PERCENT=100

MAKEFLAGS="-j$(nproc)"
NINJAFLAGS="-j$(nproc)"

CCACHE_MAXSIZE=50G
CCACHE_NOCOMPRESS=true
CCACHE_COMPRESSLEVEL=9
CCACHE_DIR=/STORAGE/ccache

CC=clang
CPP=clang-cpp
CXX=clang++
LD=lld
CC_LD=lld
CXX_LD=lld
AR=llvm-ar
NM=llvm-nm
STRIP=llvm-strip
OBJCOPY=llvm-objcopy
OBJDUMP=llvm-objdump
READELF=llvm-readelf
RANLIB=llvm-ranlib
HOSTCC=clang
HOSTCXX=clang++
HOSTAR=llvm-ar
HOSTLD=lld

CPPFLAGS="-march=bdver2 -mtune=bdver2 -pipe"
CFLAGS="$CPPFLAGS -O3 -flto -pthread -fPIC -g0"
CXXFLAGS="$CFLAGS"
LDFLAGS="-fuse-ld=lld -fPIC -flto -O3 -pipe -pthread"
RUSTFLAGS="-C link-dead-code=off -C opt-level=3 -C target-cpu=bdver2 -C codegen-units=4 -C linker-plugin-lto -C panic=abort -C lto -C debuginfo=1 -C target-feature=+aes,+sse4.2,+clzero,+mmx,+3dnow"

CPPFLAGS32="-m32 $CPPFLAGS"
CFLAGS32="-m32 $CFLAGS"
CXXFLAGS32="$CFLAGS32"
LDFLAGS32="-m32 $LDFLAGS"

DEBUG_CFLAGS="-fasynchronous-unwind-tables -g1"
DEBUG_CXXFLAGS="$DEBUG_CFLAGS"
DEBUG_RUSTFLAGS="-C debuginfo=2"
```

```bash
ROCM → ls
 .repo               hipBLASLt     hipTensor       ROCdbgapi             rocm_smi_lib           ROCR-Runtime       TransferBench
 AMDMIGraphX         hipCUB        llvm-project    rocDecode             rocminfo               rocr_debug_agent  
 amdsmi              hipFFT        MIOpen          rocFFT                ROCmValidationSuite    rocRAND           
 clr                 hipfort       MIVisionX       ROCgdb                rocPRIM                rocSOLVER         
 composable_kernel   HIPIFY        openmp-extras   rocJPEG               rocprofiler            rocSPARSE         
 half                hipother      rccl            ROCK-Kernel-Driver    rocprofiler-compute    rocThrust         
 HIP                 hipRAND       rdc             rocm-cmake            rocprofiler-register   roctracer         
 hip-tests           hipSOLVER     rocAL           rocm-core             rocprofiler-sdk        rocWMMA           
 hipBLAS             hipSPARSE     rocALUTION      rocm-examples         rocprofiler-systems    rpp               
 hipBLAS-common      hipSPARSELt   rocBLAS         rocm_bandwidth_test   rocPyDecode            Tensile
```

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2024-12-23T13:26:46Z)

Hi @ETJAKEOC. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #2 — leonelhs (2024-12-24T14:00:39Z)

There is no folder "tools" under ROCm source three, I guess all the scripts needed to build the ecosystem should be here. 

---

### 评论 #3 — jamesxu2 (2024-12-24T20:31:08Z)

Hi @ETJAKEOC, I do see those instructions are a bit confusing. 

I'm not sure why the `repo sync` steps are recorded twice in our readme, but the manifest must be specified to grab both the ROCm + ROCm/tools folder: https://github.com/ROCm/ROCm?tab=readme-ov-file#build-rocm-from-source

```
export ROCM_VERSION=6.3.1
~/bin/repo init -u http://github.com/ROCm/ROCm.git -b roc-6.3.x -m tools/rocm-build/rocm-${ROCM_VERSION}.xml
~/bin/repo sync
```

Also, I see another error in these instructions, ROCM_VERSION should be set into **6.3.0**, otherwise it will fail to fetch the tools/rocm-build/rocm-${ROCM_VERSION}.xml as there is no 6.3.1 version of this file yet. 

I'll speak to the docs team running this page and help get this fixed. 

Additionally, I see your iGPU is detected, [you should disable it in BIOS](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/prerequisites.html#disable-igpu). It's recommended to do this because ROCm may detect it as a device and try to run code on that instead of your dGPU. Your rx560 is also not supported so you may run into additional issues downstream.

Let me know if you run into other issues. Building all of ROCm is going to take a _long_ time and I don't recommend doing it if you don't absolutely need to. While Arch is not officially supported by ROCm, I believe there are third-party ROCm packages that others have built.  

---

### 评论 #4 — vdualb (2024-12-26T15:41:14Z)

Hi @jamesxu2, I have rx 570 8gb and it's an unsupported card too. I need to run my OpenCL programs and my machines are running Fedora. I tried `rocm-opencl` package from distro repos, but it fails to create command queue with error -6. I think my only solution is building rocm 3.5.1, isn't it?

---

### 评论 #5 — jamesxu2 (2024-12-30T14:34:25Z)

@RocketRide9 As you've said, this is unsupported both because ROCm >= 4 doesn't support gfx8 and AMD doesn't officially package ROCm for Fedora either (the `rocm-opencl` package is not officially supported either). 

You may want to try using alternative OpenCL platforms like discussed in issue https://github.com/ROCm/ROCm/issues/3664, or you could try building ROCm from source. However, this is far outside our testing/support matrix for the past few years so you may run into additional issues as you try this. 

You are welcome to create separate issues on Github for the problems you encounter, and our team will do our best to assess them. 

---

### 评论 #6 — jamesxu2 (2025-01-07T14:35:18Z)

Build instructions have been patched for clarity, feel free to reopen this if you need more help @ETJAKEOC or @leonelhs.


---
