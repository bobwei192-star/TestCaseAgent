# [Issue]: ROCm Horovod Installation Failure: CMake Error hip_add_library and Missing rccl.h

> **Issue #4865**
> **状态**: closed
> **创建时间**: 2025-05-31T12:31:14Z
> **更新时间**: 2025-06-19T01:39:17Z
> **关闭时间**: 2025-06-19T01:36:30Z
> **作者**: jjasoncool
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4865

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

## Environment
- **Operating System**: Ubuntu 24.04.2 LTS (Codename: noble)
- **GPU**: 2x AMD Radeon RX 9070 XT (detected as `gfx1201` by ROCm)
- **ROCm Version**: 6.4.1.60401-83~24.04
- **PyTorch Version**: Installed via `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3` (exact version pending confirmation)
- **Python Version**: 3.10 (in Conda environment)
- **Horovod Version**: Latest (installed via `pip install horovod[pytorch]`)
- **CMake Version**: 3.30 (in Conda), system CMake version unknown
- **Compiler**: GCC 12.1.0 (in Conda)
- **MPI**: mpi4py (in Conda), OpenMPI (in Docker)
- **Installed ROCm Packages**:
  ```
  rocm, rocm-cmake, rocm-core, rocm-dbgapi, rocm-debug-agent, rocm-dev, rocm-developer-tools,
  rocm-device-libs, rocm-gdb, rocm-hip-libraries, rocm-hip-runtime, rocm-hip-runtime-dev,
  rocm-hip-sdk, rocm-language-runtime, rocm-llvm, rocm-ml-libraries, rocm-ml-sdk,
  rocm-opencl, rocm-opencl-dev, rocm-opencl-runtime, rocm-opencl-sdk, rocm-openmp-sdk,
  rocm-smi-lib, rocm-utils, rocminfo
  ```

## Description
I am attempting to install Horovod with PyTorch and ROCm support to enable distributed deep learning on two AMD Radeon RX 9070 XT GPUs. I have set up both a Conda environment and a Docker environment, both using ROCm 6.4.1 and PyTorch with ROCm support. However, the Horovod installation fails in both environments with the following errors:

1. **Initial Error**:
   ```
   CMake Error at horovod/common/ops/rocm/CMakeLists.txt:21 (hip_add_library):
     Unknown CMake command "hip_add_library".
   ```
2. **Subsequent Error (after modifying source code)**:
   ```
   In file included from /workspace/src/horovod/horovod/common/operations.cc:63:
   /workspace/src/horovod/horovod/common/ops/nccl_operations.h:30:10: fatal error: rccl.h: No such file or directory
      30 | #include <rccl.h>
   ```

### Conda Environment Setup
1. Created a Conda environment:
   ```bash
   conda create -p ./env python=3.10
   conda activate ./env
   ```
2. Installed dependencies:
   ```bash
   conda install -c conda-forge gcc=12.1.0
   conda install -c conda-forge cmake=3.30
   conda install mpi4py
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3 --no-cache-dir
   ```
3. Set Horovod environment variables:
   ```bash
   export HOROVOD_GPU=ROCM
   export HOROVOD_ROCM_HOME=/opt/rocm
   export HOROVOD_GPU_OPERATIONS=NCCL
   export HOROVOD_WITHOUT_TENSORFLOW=1
   export HOROVOD_WITH_PYTORCH=1
   export HOROVOD_WITH_MPI=1
   export HOROVOD_WITHOUT_MXNET=1
   ```
4. Attempted to install Horovod:
   ```bash
   pip install horovod[pytorch] --no-cache-dir
   ```

### Docker Environment Setup
1. Used the following `docker-compose.yml`:
   ```yaml
   services:
     rocm-horovod:
       build:
         context: "./rocm/"
         args:
           VERSION: ${VERSION}  # Pending confirmation of exact tag
       container_name: rocm-horovod
       network_mode: host
       cap_add:
         - SYS_PTRACE
       security_opt:
         - seccomp=unconfined
       devices:
         - /dev/kfd:/dev/kfd
         - /dev/dri:/dev/dri
       group_add:
         - video
       ipc: host
       shm_size: 16g
       tty: true
       stdin_open: true
       volumes:
         - ./src:/workspace/src
       command: bash
   ```
2. Used the following `Dockerfile`:
   ```dockerfile
   ARG VERSION
   FROM rocm/pytorch:${VERSION}

   # Update package list and install OpenMPI
   RUN apt-get update && apt-get install -y \
       openmpi-bin \
       openmpi-common \
       libopenmpi-dev

   RUN apt-get install -y \
       cmake \
       && rm -rf /var/lib/apt/lists/*

   # Set Horovod environment variables
   ENV HOROVOD_GPU=ROCM \
       HOROVOD_ROCM_HOME=/opt/rocm \
       HOROVOD_GPU_OPERATIONS=NCCL \
       HOROVOD_WITHOUT_TENSORFLOW=1 \
       HOROVOD_WITH_PYTORCH=1 \
       HOROVOD_WITH_MPI=1 \
       HOROVOD_WITHOUT_MXNET=1\
       CMAKE_MODULE_PATH=/opt/rocm:/opt/rocm/lib/cmake/hip:${CMAKE_MODULE_PATH}

   # Install Horovod and other dependencies
   # RUN pip install --no-cache-dir horovod

   # Set working directory
   WORKDIR /workspace
   ```
3. Confirmed that ROCm is fully installed in the container, and GPU-related commands (e.g., `rocminfo`) work.

### Issue Details
- **Primary Error**:
  - The `hip_add_library` CMake command is not recognized during Horovod’s build process, suggesting a potential incompatibility between Horovod’s CMake configuration and ROCm 6.4.1’s HIP implementation.
- **Secondary Error**:
  - After modifying Horovod’s source code to fix paths (exact changes pending confirmation), the build fails due to a missing `rccl.h` header, indicating that the RCCL library or its development headers are not properly installed or detected.
- **ROCm Detection**:
  - Both GPUs (AMD Radeon RX 9070 XT, `gfx1201`) are correctly detected by ROCm, as shown in the `rocminfo` output:
    ```
    Agent 2: AMD Radeon RX 9070 XT (gfx1201, 16GB VRAM, 64 CUs)
    Agent 3: AMD Radeon RX 9070 XT (gfx1201, 16GB VRAM, 64 CUs)
    ```
- **Attempts to Resolve**:
  - Modified Horovod source code paths to point to `/opt/rocm` and other ROCm directories (details pending).
  - Searched for similar issues on GitHub. Found a related TensorFlow issue ([ROCm/ROCm#3987](https://github.com/ROCm/ROCm/issues/3987)), but it does not address PyTorch or Horovod specifically.

- **Suspected Causes**:
  - **Path Changes in ROCm 6.x**: It is suspected that ROCm 6.x (compared to ROCm 5.x) has modified package paths, causing Horovod’s build system to fail to locate required libraries or headers (e.g., HIP or RCCL). This may break compatibility with packages expecting ROCm 5.x’s directory structure.

### Steps to Reproduce
1. Set up Ubuntu 24.04.2 LTS with ROCm 6.4.1 and two RX 9070 XT GPUs.
2. Create a Conda environment with Python 3.10, GCC 12.1.0, CMake 3.30, and mpi4py.
3. Install PyTorch with ROCm support using `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3`.
4. Set Horovod environment variables as listed.
5. Run `pip install horovod[pytorch] --no-cache-dir`.
6. Alternatively, set up the Docker environment using the provided `docker-compose.yml` and `Dockerfile`, then attempt to install Horovod inside the container.
7. Observe the `hip_add_library` CMake error, and after modifying source code, the `rccl.h` error.

### Expected Behavior
Horovod installs successfully with PyTorch and ROCm 6.4.1 support, enabling distributed training on two RX 9070 XT GPUs.

### Actual Behavior
Horovod installation fails due to:
1. Missing `hip_add_library` CMake command.
2. Missing `rccl.h` header after source code modifications.

### Additional Notes
- The RX 9070 XT is supported in ROCm 6.4.1, as confirmed by `rocminfo`.
- The Docker container is properly configured for GPU access (`/dev/kfd`, `/dev/dri`, `video` group).

### Operating System

Ubuntu 24.04.2 LTS (Codename: noble)

### CPU

AMD Ryzen 7 5700X 8-Core Processor

### GPU

2x AMD Radeon RX 9070 XT (detected as `gfx1201` by ROCm)

### ROCm Version

ROCm 6.3

### ROCm Component

rccl

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
```log
/opt/rocm/bin/rocminfo --support
ROCk module version 6.10.5 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
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
  Name:                    AMD Ryzen 7 5700X 8-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5700X 8-Core Processor 
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
  Max Clock Freq. (MHz):   3400                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    98777268(0x5e338b4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98777268(0x5e338b4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98777268(0x5e338b4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98777268(0x5e338b4) KB             
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
  Uuid:                    GPU-4bddfac79195db6d               
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
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2570                               
  BDFID:                   15616                              
  Internal Node ID:        1                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 872                                
  SDMA engine uCode::      749                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*******                  
Agent 3                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    GPU-acb74c6050d6a547               
  Marketing Name:          AMD Radeon RX 9070 XT              
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
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2520                               
  BDFID:                   16384                              
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 872                                
  SDMA engine uCode::      749                                
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16695296(0xfec000) KB              
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***  
```

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — jjasoncool (2025-05-31T12:59:10Z)

https://github.com/ROCm/ROCm/issues/3987


---

### 评论 #2 — jjasoncool (2025-05-31T13:17:12Z)

1. 
>I changed
>https://github.com/horovod/horovod/blob/master/cmake/Modules/FindROCM.cmake#L16
>to
>```
>set(HIP_PATH "${HOROVOD_ROCM_HOME}/lib/cmake/hip")
>```
>Then it doesn't show  ` Unknown CMake command "hip_add_library".`

2.  
>But I don't know how to find the rccl's relay.
>Even I changed
>https://github.com/horovod/horovod/blob/master/CMakeLists.txt#L217-L244
>It still doesn't work.
>I can't find any other solutions.
  
Please help.



---

### 评论 #3 — ppanchad-amd (2025-06-02T14:14:02Z)

Hi @jjasoncool. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #4 — schung-amd (2025-06-02T16:14:13Z)

Hi @jjasoncool, the workaround provided in the linked issue addresses both the missing `hip_add_library` and the missing `rccl.h`; I reproduced both of your issues and the fix with your Dockerfile based on `rocm/pytorch:latest` (without a conda environment as I don't think that would make a difference) on gfx1201 and ROCm 6.4.1:
 ```
$ git clone --recursive https://github.com/horovod/horovod.git
$ cd horovod
$ ln -s $ROCM_PATH/lib/cmake/hip/FindHIP* cmake/Modules/
$ sed -i 's/rccl\.h/rccl\/rccl\.h/' horovod/common/ops/nccl_operations.h
$ <horovod env vars> pip install .
```


---

### 评论 #5 — jjasoncool (2025-06-19T01:36:30Z)

The issue has been solved.

---
