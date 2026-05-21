# [Issue]: comfyui Memory access fault by GPU node-1 (Agent handle: 0x55dd6172f440) on address 0x7f639e2a6000. Reason: Page not present or supervisor privilege.

> **Issue #5833**
> **状态**: closed
> **创建时间**: 2026-01-05T12:03:22Z
> **更新时间**: 2026-01-07T18:14:39Z
> **关闭时间**: 2026-01-07T18:14:39Z
> **作者**: RadeonVega-56
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5833

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

### Problem Description

OS:
NAME="Nobara Linux"
VERSION="43 (KDE Plasma Desktop Edition)"
CPU: 
model name      : AMD Ryzen 9 9950X 16-Core Processor
GPU:
Name:                    AMD Ryzen 9 9950X 16-Core Processor
Marketing Name:          AMD Ryzen 9 9950X 16-Core Processor
Name:                    gfx1201                            
Marketing Name:          AMD Radeon RX 9070 XT              
Name:                    amdgcn-amd-amdhsa--gfx1201         
Name:                    amdgcn-amd-amdhsa--gfx12-generic   


### Operating System

Nobara Linux 43

### CPU

AMD Ryzen 9 9950X
+ 96 GB RAM

### GPU

AMD RX 9070 XT

### ROCm Version

ROCm 7.1.1 - from nobara repo

### ROCm Component

_No response_ 

### Steps to Reproduce

I am running comfyui on python 3.12 with a venv.

I keep getting this error running comfyui: comfyui Memory access fault by GPU node-1 (Agent handle: 0x55dd6172f440) on address 0x7f639e2a6000. Reason: Page not present or supervisor privilege.

When this error occurs my comfyui server crashes or stops working and i have to restart the comfyui server.

This happens when running comfyui since kernel update to 6.18.2-200. The kernel version i had before is working without that error, kernel 6.17.12-200. Whenever i use that kernel the error is gone, even with the latest firmware packages installed.

Today i recieved a new kernel update to 6.18.3-201. It shows the same error.  

**To start comfyui i wrote a small script that does that for me. Whenever i start that scipt with the "sudo" command the error does not occur.**

 ./comfy.sh -> error,   sudo ./comfy.sh -> no error

Another temporary workaround is to downgrade the amdgpu-firmware package: sudo dnf downgrade amd-gpu-firmware. Comfyui then works without the sudo command on the latest kernel without error. **<- OK. This seems wrong, after testing further today i got the error while running comfyui for several hours**

I set those kernel parameters but i am not sure if they do anything:

amdgpu.mcbp=0 amdgpu.cwsr_enable=0 amdgpu.queue_preemption_timeout_ms=1

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

rocminfo --support
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.14
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
  Name:                    AMD Ryzen 9 9950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 9950X 16-Core Processor
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
  Max Clock Freq. (MHz):   5756                               
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
      Size:                    98448848(0x5de35d0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    98448848(0x5de35d0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98448848(0x5de35d0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98448848(0x5de35d0) KB             
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
  Uuid:                    GPU-d2f5f7ecc66d071c               
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
  Max Clock Freq. (MHz):   2400                               
  BDFID:                   768                                
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 128                                
  SDMA engine uCode::      662                                
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

------------------------------------------------------------------
my .bashrc set of variables:
------------------------------------------------------------------

export ROCM_PATH=/usr
export HIP_PATH=$ROCM_PATH
export PATH="$ROCM_PATH/bin:$PATH"
export LD_LIBRARY_PATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$LD_LIBRARY_PATH"
export PYTHONPATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$PYTHONPATH"

export HIP_CLANG_PATH=/usr/lib64/rocm/llvm/bin
export DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HIP_DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HSA_PATH=/usr
export LLVM_PATH=/usr/lib64/rocm/llvm/bin

export MIOPEN_USER_DB_PATH="$HOME/.cache/miopen"
export ROCBLAS_TENSILE_LIBPATH="$ROCM_PATH/lib64/rocblas/library"

export HIP_PLATFORM=amd
export HIP_RUNTIME=rocclr
export HIP_COMPILER=clang

export HSA_OVERRIDE_GFX_VERSION=12.0.1
export PYTORCH_ROCM_ARCH=gfx1201
export GFX_ARCH=gfx1201
export USE_ROCM=1

--------------------------------------------------------------------------------
my comfyui startup script:
--------------------------------------------------------------------------------

#!/bin/bash
cd ComfyUI/
source my312_venv/bin/activate

export CMAKE_PREFIX_PATH="${VIRTUAL_ENV}:${CMAKE_PREFIX_PATH}"

export HIP_VISIBLE_DEVICES=0
export ROCM_VISIBLE_DEVICES=0
export HIP_TARGET="gfx1201"
export PYTORCH_ROCM_ARCH="gfx1201"
export TORCH_HIP_ARCH_LIST="gfx1201"
export HCC_AMDGPU_TARGET="gfx1201"
export PYTORCH_ROCM_ARCH="gfx1201"

export MESA_LOADER_DRIVER_OVERRIDE=amdgpu
export RADV_PERFTEST="aco,nggc,sam"

export PYTORCH_HIP_ALLOC_CONF="max_split_size_mb:6144,garbage_collection_threshold:0.85"
export PYTORCH_HIP_FREE_MEMORY_THRESHOLD_MB=128

export TORCH_COMPILE=0

export TORCH_BLAS_PREFER_HIPBLASLT=1
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS="CK,TRITON,ROCBLAS"
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_SEARCH_SPACE="BEST"
export TORCHINDUCTOR_FORCE_FALLBACK=1

export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
export FLASH_ATTENTION_TRITON_AMD_AUTOTUNE="TRUE"
export FLASH_ATTENTION_BACKEND="flash_attn_triton_amd"
export FLASH_ATTENTION_TRITON_AMD_SEQ_LEN=4096
export USE_CK=ON
export TRANSFORMERS_USE_FLASH_ATTENTION=1
export TRITON_USE_ROCM=ON
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1



export OMP_NUM_THREADS=14
export MKL_NUM_THREADS=14
export NUMEXPR_NUM_THREADS=14



export HIP_GRAPH=1

#export HIP_LAUNCH_BLOCKING=1
#export AMD_SERIALIZE_KERNEL=1
#export AMD_SERIALIZE_COPY=1

export AMD_DIRECT_DISPATCH=1
export GPU_MAX_HW_QUEUES=32

export HSA_ENABLE_ASYNC_COPY=1
export HSA_ENABLE_SDMA=1
export HSA_ENABLE_PEER_SDMA=1
export HSA_ENABLE_SDMA_COPY=1
export HSA_ENABLE_SDMA_KERNEL_COPY=1

export MIOPEN_FIND_MODE=2
export MIOPEN_ENABLE_CACHE=1
export MIOPEN_CHECK_NUMERICS=0x02


export HIP_FORCE_DEV_KERNARG=1

export ROCBLAS_STREAM_ORDER_ALLOC=1

export ROCBLAS_INTERNAL_FP16_ALT_IMPL=1
export ROCBLAS_LAYER=0
export ROCBLAS_INTERNAL_USE_SUBTENSILE=1

export SAFETENSORS_FAST_GPU=1

python main.py --disable-cuda-malloc --lowvram --use-pytorch-cross-attention --cache-lru 10 --reserve-vram 0.8 --preview-method none --listen --port 8188

deactivate


---

## 评论 (4 条)

### 评论 #1 — RadeonVega-56 (2026-01-05T12:44:08Z)

In addition to the above error i get an insane amount of free memory displayed when loading a model in ComfyUI:

got prompt
Requested to load FluxClipModel_
loaded completely; **95367431640625005117571072.00 MB usable**, 9319.23 MB loaded, full load: True


Maybe that is the culprit for the gobal RAM crysis?  :D

Could that be related to the torch version i am using? It is:  torch 2.11.0.dev20251227+rocm7.1.



---

### 评论 #2 — RadeonVega-56 (2026-01-05T15:24:42Z)

Another observation i made: a friend of mine got a similar machine, same OS, AMD Ryzen 9 3900X, 92 GB RAM, RX 9060 XT

On his machine he always gets the error, even with kernel 6.17.12-200, i did not try yet to launch comfyui with sudo or downgrading the firmware at all on that machine. The only difference i see is that he got the AM4 platform and i got the AM5 platform. Maybe those are firmware related issues?

---

### 评论 #3 — RadeonVega-56 (2026-01-07T11:46:40Z)

Reading this thread helped a lot: https://www.reddit.com/r/comfyui/comments/1nuipsu/finally_my_comfyui_setup_works/


Yesterday i reinstalled the latest firmware and added some more kernel options to my command line. Now it looks like this:

quiet splash resume=UUID=dcc22aa9-bdce-435f-b290-d2223c679419 amdgpu.ppfeaturemask=0xffffffff amdgpu.mcbp=0 amdgpu.cwsr_enable=0 amdgpu.queue_preemption_timeout_ms=1 iommu=pt amd_iommu=force_isolation amd_iommu=on above4g_decoding resizable_bar hpet=disable

This helped a lot with the new 6.18.3-201 kernel. I could generate for serveral hours running comfyui without sudo and testing workflows with SD1.5, SDXL, FLUX1-dev, Video WAN 2.2 before the error occured again.

Modified startup script:

#!/bin/bash
cd ComfyUI/
source my312_venv/bin/activate

export CMAKE_PREFIX_PATH="${VIRTUAL_ENV}:${CMAKE_PREFIX_PATH}"

export HIP_VISIBLE_DEVICES=0
export ROCM_VISIBLE_DEVICES=0
export HIP_TARGET="gfx1201"
export PYTORCH_ROCM_ARCH="gfx1201"
export TORCH_HIP_ARCH_LIST="gfx1201"
export HCC_AMDGPU_TARGET="gfx1201"
export PYTORCH_ROCM_ARCH="gfx1201"

export MESA_LOADER_DRIVER_OVERRIDE=amdgpu
export RADV_PERFTEST="aco,nggc,sam"

export PYTORCH_HIP_ALLOC_CONF="max_split_size_mb:6144,garbage_collection_threshold:0.6"
export PYTORCH_HIP_FREE_MEMORY_THRESHOLD_MB=128
export PYTORCH_ALLOC_CONF=expandable_segments:True

export TORCH_COMPILE=1


export TORCH_DEVICE_BACKEND_AUTOLOAD=1

export TORCH_BLAS_PREFER_HIPBLASLT=1
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS="CK,TRITON,ROCBLAS"
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_SEARCH_SPACE="BEST"
export TORCHINDUCTOR_FORCE_FALLBACK=0

export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
export FLASH_ATTENTION_TRITON_AMD_AUTOTUNE="TRUE"
export FLASH_ATTENTION_BACKEND="flash_attn_triton_amd"
export FLASH_ATTENTION_TRITON_AMD_SEQ_LEN=4096
export USE_CK=ON
export TRANSFORMERS_USE_FLASH_ATTENTION=1
export TRITON_USE_ROCM=ON
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1



export OMP_NUM_THREADS=14
export MKL_NUM_THREADS=14
export NUMEXPR_NUM_THREADS=14



#export HIP_GRAPH=1
#export HIP_LAUNCH_BLOCKING=1
#export AMD_SERIALIZE_KERNEL=1
#export AMD_SERIALIZE_COPY=1


export PYTORCH_TUNABLEOP_ENABLED="1"
export PYTORCH_TUNABLEOP_TUNING="0"
export PYTORCH_TUNABLEOP_FILENAME="tunableop_results0.csv"

export AMD_DIRECT_DISPATCH=1
export TORCH_NCCL_HIGH_PRIORITY=1
export GPU_MAX_HW_QUEUES=32

export HSA_ENABLE_ASYNC_COPY=1
export HSA_ENABLE_SDMA=1
export HSA_ENABLE_PEER_SDMA=1
export HSA_ENABLE_SDMA_COPY=1
export HSA_ENABLE_SDMA_KERNEL_COPY=1
export HSA_FORCE_FINE_GRAIN_PCIE=1

export MIOPEN_FIND_MODE=2
export MIOPEN_ENABLE_CACHE=1
export MIOPEN_CHECK_NUMERICS=0x02
export MIOPEN_CONV_WINOGRAD=1
export MIOPEN_DEBUG_CONV_FFT=0
export MIOPEN_ENABLE_LOGGING_CMD=0
export MIOPEN_DEBUG_CONV_IMPLICIT_GEMM=1

export HIP_FORCE_DEV_KERNARG=1

export ROCBLAS_STREAM_ORDER_ALLOC=1

export ROCBLAS_INTERNAL_FP16_ALT_IMPL=1
export ROCBLAS_LAYER=0
export ROCBLAS_INTERNAL_USE_SUBTENSILE=1

export SAFETENSORS_FAST_GPU=1

python main.py --disable-cuda-malloc  --fast fp16_accumulation fp8_matrix_mult --lowvram --use-pytorch-cross-attention --cache-lru 10 --preview-method none --listen --port 8188

deactivate


Modified .bashrc:


export ROCM_PATH=/usr
export HIP_PATH=$ROCM_PATH
export PATH="$ROCM_PATH/bin:$PATH"
export LD_LIBRARY_PATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$LD_LIBRARY_PATH"
export PYTHONPATH="$ROCM_PATH/lib:$ROCM_PATH/lib64:$PYTHONPATH"

export HIP_CLANG_PATH=/usr/lib64/rocm/llvm/bin
export DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HIP_DEVICE_LIB_PATH=/usr/lib64/rocm/llvm/lib/clang/20/amdgcn/bitcode
export HSA_PATH=/usr
export LLVM_PATH=/usr/lib64/rocm/llvm/bin

export MIOPEN_USER_DB_PATH="$HOME/.cache/miopen"

export MIOPEN_USER_DB_PATH="$HOME/.config/miopen"

export ROCBLAS_TENSILE_LIBPATH="$ROCM_PATH/lib64/rocblas/library"

export HIP_PLATFORM=amd
export HIP_RUNTIME=rocclr
export HIP_COMPILER=clang

export HSA_OVERRIDE_GFX_VERSION=12.0.1
export PYTORCH_ROCM_ARCH=gfx1201
export GFX_ARCH=gfx1201
export USE_ROCM=1



---

### 评论 #4 — tcgu-amd (2026-01-07T18:14:39Z)

Hi @RadeonVega-56, looks like it is the same issue as https://github.com/ROCm/ROCm/issues/5245? 

I will close this ticket for now. But please feel free to let me know if you think this is a separate issue. Thanks! 

---
