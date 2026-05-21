# [Issue]: Is there a ROCm version that supports gfx1151?

> **Issue #4499**
> **状态**: open
> **创建时间**: 2025-03-14T11:44:36Z
> **更新时间**: 2025-06-03T20:37:12Z
> **作者**: moonshadow-25
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4499

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

When I build the Pytorch with ROCm6.3.4,there are many errors!
[29/616] cd /home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels && /home/moon/miniconda3/envs/ktransformers/lib/python3.12/site-packages/cmake/data/bin/cmake -E make_directory /home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/. && /home/moon/miniconda3/envs/ktransformers/lib/python3.12/site-packages/cmake/data/bin/cmake -D verbose:BOOL=OFF -D build_configuration:STRING=RELEASE -D generated_file:STRING=/home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/./torch_hip_generated_bgemm_kernel_bf16bf16bf16_256_16x256x64_16x16_1x4_8x16x1_8x16x1_1x16x1x16_4_Intrawave_v2.hip.o -P /home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/torch_hip_generated_bgemm_kernel_bf16bf16bf16_256_16x256x64_16x16_1x4_8x16x1_8x16x1_1x16x1x16_4_Intrawave_v2.hip.o.cmake
FAILED: caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/torch_hip_generated_bgemm_kernel_bf16bf16bf16_256_16x256x64_16x16_1x4_8x16x1_8x16x1_1x16x1x16_4_Intrawave_v2.hip.o /home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/torch_hip_generated_bgemm_kernel_bf16bf16bf16_256_16x256x64_16x16_1x4_8x16x1_8x16x1_1x16x1x16_4_Intrawave_v2.hip.o 
cd /home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels && /home/moon/miniconda3/envs/ktransformers/lib/python3.12/site-packages/cmake/data/bin/cmake -E make_directory /home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/. && /home/moon/miniconda3/envs/ktransformers/lib/python3.12/site-packages/cmake/data/bin/cmake -D verbose:BOOL=OFF -D build_configuration:STRING=RELEASE -D generated_file:STRING=/home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/./torch_hip_generated_bgemm_kernel_bf16bf16bf16_256_16x256x64_16x16_1x4_8x16x1_8x16x1_1x16x1x16_4_Intrawave_v2.hip.o -P /home/moon/kt/pytorch/build/caffe2/CMakeFiles/torch_hip.dir/__/aten/src/ATen/native/hip/bgemm_kernels/torch_hip_generated_bgemm_kernel_bf16bf16bf16_256_16x256x64_16x16_1x4_8x16x1_8x16x1_1x16x1x16_4_Intrawave_v2.hip.o.cmake
In file included from /home/moon/kt/pytorch/aten/src/ATen/native/hip/bgemm_kernels/bgemm_kernel_bf16bf16bf16_256_16x256x64_16x16_1x4_8x16x1_8x16x1_1x16x1x16_4_Intrawave_v2.hip:3:
In file included from /home/moon/kt/pytorch/aten/src/ATen/native/hip/bgemm_kernels/bgemm_kernel_template.h:11:
In file included from /home/moon/kt/pytorch/aten/src/ATen/../../../third_party/composable_kernel/include/ck/tensor_operation/gpu/device/impl/device_batched_gemm_multiple_d_xdl_cshuffle_v3.hpp:9:
In file included from /home/moon/kt/pytorch/aten/src/ATen/../../../third_party/composable_kernel/include/ck/utility/common_header.hpp:36:
/home/moon/kt/pytorch/aten/src/ATen/../../../third_party/composable_kernel/include/ck/utility/amd_buffer_addressing.hpp:32:48: error: use of undeclared identifier 'CK_BUFFER_RESOURCE_3RD_DWORD'
   32 |     wave_buffer_resource.config(Number<3>{}) = CK_BUFFER_RESOURCE_3RD_DWORD;
      |                                                ^
/home/moon/kt/pytorch/aten/src/ATen/../../../third_party/composable_kernel/include/ck/utility/amd_buffer_addressing.hpp:47:48: error: use of undeclared identifier 'CK_BUFFER_RESOURCE_3RD_DWORD'
   47 |     wave_buffer_resource.config(Number<3>{}) = CK_BUFFER_RESOURCE_3RD_DWORD;
      |                                                ^


### Operating System

NAME="Ubuntu" VERSION="22.04.5 LTS (Jammy Jellyfish)"

### CPU

AMD Eng Sample: 100-000001243-50_Y

### GPU

 amdgcn-amd-amdhsa--gfx1151   

### ROCm Version

ROCm 6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.10.5 is loaded
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
  Name:                    AMD Eng Sample: 100-000001243-50_Y 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Eng Sample: 100-000001243-50_Y 
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
  Max Clock Freq. (MHz):   5172                               
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
      Size:                    131015728(0x7cf2430) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131015728(0x7cf2430) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131015728(0x7cf2430) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131015728(0x7cf2430) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
  Uuid:                    GPU-XX                             
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
    L1:                      32(0x20) KB                        
    L2:                      2048(0x800) KB                     
    L3:                      16384(0x4000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2799                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
  Packet Processor uCode:: 25                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65507864(0x3e79218) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65507864(0x3e79218) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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

## 评论 (14 条)

### 评论 #1 — darren-amd (2025-03-20T15:22:34Z)

Hi @moonshadow-25,

This issue seems to be related to: https://github.com/ROCm/composable_kernel/issues/775, as CK currently does not have official support for gfx1151. Could you try using the Pytorch [wheels](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-a-wheels-package) or [docker](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-the-pytorch-rocm-base-docker-image) instead? Thanks!

---

### 评论 #2 — moonshadow-25 (2025-03-22T07:16:10Z)

Ok, I'm now using the hipblaslt instead it.
But another question,I can't load data on my VRAM,they move to the GTT,and the calculation is very slow, why?
when I use the vulkan, all thing will be correct,but rocm is not!
I want to use my gfx1151 with rocm,which version will be stability?

---

### 评论 #3 — darren-amd (2025-03-24T18:47:29Z)

Hi @moonshadow-25,

Could you elaborate more about the issue you are running into? We don't officially support gfx1151 on ROCm according to the [compatibility matrix](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html), but I will try my best to help, thanks!

---

### 评论 #4 — Mar2ck (2025-04-01T13:39:33Z)

Given that AMD gave a ROCm presentation at the Framework Desktop launch event, which uses gfx1151 (8050S/8060S), I assume we will see official support for this ISA in a future release?

---

### 评论 #5 — darren-amd (2025-04-01T15:43:08Z)

We do have plans to expand ROCm support, however there is no confirmed timeline at the moment.

---

### 评论 #6 — moonshadow-25 (2025-04-07T14:04:12Z)

# Performance Report: PyTorch Matrix Multiplication Issue on AMD GPUs with ROCm

## System Information
- **GPU**: AMD Radeon Graphics (gfx1151)
- **OS**: Linux 6.11.0-1019-oem
- **ROCm Version**: 6.3.42134-a9a80e791
- **PyTorch Version**: 2.6.0+git2fd46f8

## Issue Summary
When using PyTorch with ROCm backend on AMD GPUs, there is a significant performance discrepancy between FP16 and FP32 matrix multiplication operations. While FP16 performance is acceptable, FP32 performance is unexpectedly poor. This report details our findings after investigating this behavior with various backend configurations.

## Benchmark Results

### Performance Comparison (matrix size: 4096×4096)

| Configuration            | FP16 Performance | FP32 Performance | FP16/FP32 Ratio |
|--------------------------|------------------|------------------|-----------------|
| hipBLASLT Enabled (default) | 18.71 TFLOPS     | 0.49 TFLOPS      | 38.2x           |
| hipBLASLT Disabled       | 23.42 TFLOPS     | 0.49 TFLOPS      | 47.8x           |

### Extended Testing Results for Different Matrix Sizes

| Matrix Size | Data Type | hipBLASLT | Performance (TFLOPS) |
|-------------|-----------|-----------|----------------------|
| 1024x1024   | FP16      | Enabled   | 11.56                |
| 1024x1024   | FP16      | Disabled  | 17.33                |
| 1024x1024   | FP32      | Enabled   | 1.14                 |
| 1024x1024   | FP32      | Disabled  | 1.22                 |
| 2048x2048   | FP16      | Enabled   | 30.87                |
| 2048x2048   | FP16      | Disabled  | 29.30                |
| 2048x2048   | FP32      | Enabled   | 1.06                 |
| 2048x2048   | FP32      | Disabled  | 1.07                 |
| 4096x4096   | FP16      | Enabled   | 18.71                |
| 4096x4096   | FP16      | Disabled  | 23.42                |
| 4096x4096   | FP32      | Enabled   | 0.49                 |
| 4096x4096   | FP32      | Disabled  | 0.49                 |

## Observed Issues

1. **Extremely Low FP32 Performance**: FP32 matrix multiplication performance is unexpectedly low (0.49 TFLOPS) compared to FP16 performance (18.71-23.42 TFLOPS), with a massive 38-48x difference.

2. **Inconsistent hipBLASLT Performance**: Interestingly, disabling hipBLASLT (using `HIPBLASLT_DISABLE=1`) increases FP16 performance by approximately 25% for 4096×4096 matrices, suggesting the default configuration is not optimal.

3. **No Impact on FP32 Performance**: Various environment configurations we tested had almost no impact on FP32 performance, indicating a deeper issue with the FP32 implementation.

## Additional Configurations Tested

We tested several ROCm/HIP environment configurations without significant improvement in FP32 performance:

1. Force rocBLAS (`HIPBLASLT_DISABLE=1`, `ROCBLAS_LAYER=4`)
2. Use hipBLASLT with GEMM optimization (`ROCBLAS_TENSILE_LIBPATH`, `HIPBLASLT_TENSILE_LIBPATH`, `ROCBLAS_TENSILE_GEMM_OPTIMIZE=1`)
3. Enable fast FP16 kernels (`ROCBLAS_FAST_16BIT_KERNELS=1`, etc.)
4. Various logging levels

None of these configurations significantly improved FP32 performance, suggesting a possible underlying issue with the FP32 implementation in the ROCm/PyTorch stack.

## Comparison with Other Frameworks

For reference, we also tested the same matrix multiplications using a native GGML-based implementation (llama.cpp), which showed much more balanced performance:

| Framework       | FP32 Performance   | FP16 Performance     | FP16/FP32 Ratio |
|-----------------|--------------------|-----------------------|-----------------|
| PyTorch         | 0.49 TFLOPS        | 18.71-23.42 TFLOPS    | 38-48x          |
| GGML (llama.cpp)| 3.3-4.3 TFLOPS     | 2.7-4.7 TFLOPS        | 0.64-1.12x      |

This suggests the issue is specific to PyTorch's implementation on ROCm rather than a hardware limitation.

## Concluding Observations

1. PyTorch on ROCm appears to heavily optimize for FP16 operations, potentially at the expense of FP32 performance.

2. The extreme discrepancy between FP16 and FP32 performance does not appear to be inherent to the hardware, as other frameworks show more balanced performance.

3. This behavior presents significant challenges for workloads that require mixed precision or depend on FP32 operations, as the performance difference is far larger than what would be expected from hardware characteristics alone.

We recommend the ROCm team investigate the FP32 matrix multiplication implementation in PyTorch to identify potential optimization opportunities or underlying issues causing this significant performance gap.

---

### 评论 #7 — lhl (2025-05-02T08:01:20Z)

@darren-amd 

Hi, I am doing some testing on gfx1151. I am using:
```
Fedora Linux 43 (Workstation Edition Prerelease)
Linux 6.15.0-0.rc3.20250422gita33b5a08cbbd.29.fc43.x86_64
PyTorch HIP Version: 6.3.42134-0
```
I am using PyTorch 2.5.0a0 built by Fedora w/ gfx1151 support. I am able to run `mamf-finder.py` but quite frankly the perf sucks:

```
Tried  3375 shapes => the best outcomes were:
mean:   5.0 TFLOPS @ 4096x9216x1024 (MxNxK)
median: 5.0 TFLOPS @ 12288x3072x1024 (MxNxK)
max:    5.1 TFLOPS @ 11264x3072x1024 (MxNxK)
```

Top theoretical should be 29 FP16 TFLOPs or 58 FP16 TFLOPS w/ wave32 vopd dual issue?

This system does not have ROCm setup and I can't build hipBLASlt w/ the repo script... Just curious what my options are, and if there's an ETA for gfx1151 ROCm support?

Also, is there any plan on optimizing the llama.cpp ROCm/HIP backend? In initial testing it looks like pp is <1/2 the speed of Vulkan. It actually barely beats out running on the CPU backend...

---

### 评论 #8 — lhl (2025-05-13T07:19:05Z)

@darren-amd A quick followup, I managed to build PyTorch (jeez that sucked) from HEAD within one of @scottt Fedora 41 dockers: https://llm-tracker.info/_TOORG/Strix-Halo#pytorch

I built w/ AOTriton (again from HEAD) and using the hipBLASLt included in docker (but checked to make sure it was built w/ gfx1151 - it is!).  Perf still sucks though:

```
# python 03-test_aotriton_pytorch.py
PyTorch version: 2.8.0a0+git8511d21
CUDA available: True
ROCm version: 6.4.43480-9f04e2822
Environment variables:
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: Not set
LD_LIBRARY_PATH: /opt/rocm/lib:/home/lhl/aotriton/build/install_dir/lib:/opt/rocm/lib:
PYTORCH_ROCM_ARCH: gfx1151
pyaotriton imported successfully
torch.ops.aotriton is available
Registered aten ops: 834
Testing scaled_dot_product_attention...
Success! Result shape: torch.Size([1, 1, 128, 64])

# python 04-test_attention_small.py
Testing with sizes: batch=1, heads=1, seq_len=128, head_dim=64
Basic attention success! Result shape: torch.Size([1, 1, 128, 64])
AOTriton attention success! Result shape: torch.Size([1, 1, 128, 64])

# python 05-attention-bench.py
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                                  AOTriton Status Check                                  ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
PyTorch version: 2.8.0a0+git8511d21
CUDA available: True
ROCm version: 6.4.43480-9f04e2822
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: 1
pyaotriton imported successfully
torch.ops.aotriton is available
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                           Testing Tiny: B=1, H=1, S=128, D=64                           ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.00 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         0.0886 |              0.02 |         0.125  |              0.04 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.0689 |              0.03 |         0.1241 |              0.04 |
+--------------+----------------+-------------------+----------------+-------------------+
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                           Testing Small: B=2, H=4, S=512, D=64                          ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.00 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         0.5034 |              0.53 |         0.6336 |              1.06 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.4589 |              0.58 |         0.6298 |              1.07 |
+--------------+----------------+-------------------+----------------+-------------------+
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                          Testing Medium: B=4, H=8, S=1024, D=64                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.01 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |        16.2504 |              0.26 |        16.0349 |              0.67 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |        15.5982 |              0.28 |        16.0953 |              0.67 |
+--------------+----------------+-------------------+----------------+-------------------+
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                          Testing Large: B=8, H=16, S=2048, D=64                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.03 GB
Total QKV memory: 0.09 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |        151.853 |              0.45 |        131.531 |              1.31 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |        120.143 |              0.57 |        131.255 |              1.31 |
+--------------+----------------+-------------------+----------------+-------------------+
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                         Testing XLarge: B=16, H=16, S=4096, D=64                        ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.12 GB
Total QKV memory: 0.38 GB
Memory access fault by GPU node-1 (Agent handle: 0x55b017570c40) on address 0x7fcd499e6000. Reason: Page not present or supervisor privilege.
Aborted (core dumped)

# python 08-test-hipblaslt-perf.py
Environment check:
PYTORCH_ROCM_ARCH: gfx1151
HIPBLASLT_TENSILE_LIBPATH: /opt/rocm/lib/hipblaslt/library
TORCH_BLAS_PREFER_HIPBLASLT: 1
Testing GEMM performance...
GEMM 4096x4096x4096: 21.613 ms, 6.36 TFLOPS
Testing Attention performance...
Attention 8x16x2048x64: 150.233 ms, 0.91 TFLOPS
WARNING: GEMM performance is low. hipBLASLt may not be properly configured.
Check that:
1. The correct architecture kernels are in /opt/rocm/lib/hipblaslt/library
2. HIPBLASLT_TENSILE_LIBPATH is set correctly
3. Your GPU architecture matches the available kernels
### They are...
# /opt/rocm/lib/hipblaslt/library/TensileLibrary_lazy_gfx1151.dat
# /opt/rocm/lib/hipblaslt/library/extop_gfx1151.co

# python 09-test-attention-backend.py
=== Environment ===
PYTORCH_ROCM_ARCH: gfx1151
HIPBLASLT_TENSILE_LIBPATH: /opt/rocm/lib/hipblaslt/library
TORCH_BLAS_PREFER_HIPBLASLT: 1
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: 1
=== Backend Check ===
PyTorch version: 2.8.0a0+git8511d21
CUDA available: True
Current device: 0
Device name: AMD Radeon Graphics
=== AOTriton Check ===
pyaotriton imported successfully
torch.ops.aotriton is available
AOTriton ops: ['__doc__', '__loader__', '__name__', '__package__', '__spec__', '_dir', 'name']
=== SDPA Backends ===
Flash SDPA enabled: True
Memory efficient SDPA enabled: True
Math SDPA enabled: True
=== Testing Attention Variants ===
1. Standard SDPA (no causal):
Standard SDPA: 118.740 ms, 1.16 TFLOPS
2. Causal SDPA:
Causal SDPA: 149.004 ms, 0.92 TFLOPS
3. SDPA with attn_mask:
SDPA with mask: 149.673 ms, 0.92 TFLOPS
4. Force Flash Attention backend:
/usr/lib64/python3.13/contextlib.py:109: FutureWarning: `torch.backends.cuda.sdp_kernel()` is deprecated. In the future, this context manager will be removed. Please see `torch.nn.attention.sdpa_kernel()` for the new context manager, with updated signature.
  self.gen = func(*args, **kwds)
/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py:95: UserWarning: Memory efficient kernel not used because: (Triggered internally at /home/lhl/torch/pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:859.)
  lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py:95: UserWarning: Memory Efficient attention has been runtime disabled. (Triggered internally at /home/lhl/torch/pytorch/aten/src/ATen/native/transformers/sdp_utils_cpp.h:550.)
  lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py:95: UserWarning: Flash attention kernel not used because: (Triggered internally at /home/lhl/torch/pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:861.)
  lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py:95: UserWarning: Flash attention was not compiled for current AMD GPU architecture. Attempting to run on architecture gfx1151 (Triggered internally at /home/lhl/torch/pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:241.)
  lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py:95: UserWarning: CuDNN attention kernel not used because: (Triggered internally at /home/lhl/torch/pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:863.)
  lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py:95: UserWarning: Torch was not compiled with cuDNN attention. (Triggered internally at /home/lhl/torch/pytorch/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:618.)
  lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
Traceback (most recent call last):
  File "/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py", line 93, in <module>
    test_attention_variant(
    ~~~~~~~~~~~~~~~~~~~~~~^
        "Flash Attention",
        ^^^^^^^^^^^^^^^^^^
        lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py", line 58, in test_attention_variant
    _ = func(q, k, v)
  File "/home/lhl/framework-desktop-testing/fa/09-test-attention-backend.py", line 95, in <lambda>
    lambda q, k, v: F.scaled_dot_product_attention(q, k, v, is_causal=True)
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: No available kernel. Aborting execution.
```

Also is the FA2 still broken? I was under the impression that `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1` would use AOTRITON FA2 for AMD?


---

### 评论 #9 — scottt (2025-05-13T10:13:24Z)

@lhl , I could take a look. Do you have your benchmark scripts in a public repo?

---

### 评论 #10 — lhl (2025-05-13T15:37:01Z)

> [@lhl](https://github.com/lhl) , I could take a look. Do you have your benchmark scripts in a public repo?

I've just pushed the testing scripts to a public repo now: https://github.com/lhl/strix-halo-testing/tree/main/flash-attention

The benchmark script was adapted from: https://github.com/pytorch-labs/attention-gym/blob/main/examples/benchmark.py

BTW, you can use these scripts to look at memory usage: https://llm-tracker.info/_TOORG/Strix-Halo#flash-attention

---

### 评论 #11 — scottt (2025-05-19T22:51:55Z)

@lhl , use this self-contained Pytorch wheel with aotriton support and you should get much further https://github.com/ROCm/TheRock/discussions/655

On the Asus Z13, with a peak power usage ~85W I get:

```
$ python 03-test_aotriton_pytorch.py
PyTorch version: 2.7.0a0+gitbfd8155
CUDA available: True
ROCm version: 6.5.25190-39c57805b

Environment variables:
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: Not set
LD_LIBRARY_PATH: Not set
PYTORCH_ROCM_ARCH: Not set
Could not import pyaotriton

Testing scaled_dot_product_attention...
Success! Result shape: torch.Size([1, 1, 128, 64])
```

```
$ python 05-attention-bench.py
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                                  AOTriton Status Check                                  ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
PyTorch version: 2.7.0a0+gitbfd8155
CUDA available: True
ROCm version: 6.5.25190-39c57805b
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: 1
Could not import pyaotriton

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                           Testing Tiny: B=1, H=1, S=128, D=64                           ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.00 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         0.0369 |              0.06 |         0.053  |               0.1 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.0347 |              0.06 |         0.0525 |               0.1 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                           Testing Small: B=2, H=4, S=512, D=64                          ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.00 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         0.1266 |              2.12 |         0.3277 |              2.05 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.1313 |              2.04 |         0.2778 |              2.42 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                          Testing Medium: B=4, H=8, S=1024, D=64                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.01 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         1.0218 |              4.2  |         2.3149 |              4.64 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.9775 |              4.39 |         2.7291 |              3.93 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                          Testing Large: B=8, H=16, S=2048, D=64                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.03 GB
Total QKV memory: 0.09 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |        14.338  |              4.79 |        30.9319 |              5.55 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |        14.2997 |              4.81 |        41.8988 |              4.1  |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                         Testing XLarge: B=16, H=16, S=4096, D=64                        ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.12 GB
Total QKV memory: 0.38 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |        108.445 |              5.07 |        231.295 |              5.94 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |        102.022 |              5.39 |        382.383 |              3.59 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                                         Summary                                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Tiny:
  Causal FA2: 0.0369 ms
  Regular SDPA: 0.0347 ms
Small:
  Causal FA2: 0.1266 ms
  Regular SDPA: 0.1313 ms
Medium:
  Causal FA2: 1.0218 ms
  Regular SDPA: 0.9775 ms
Large:
  Causal FA2: 14.3380 ms
  Regular SDPA: 14.2997 ms
XLarge:
  Causal FA2: 108.4451 ms
  Regular SDPA: 102.0224 ms
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                              Testing with different dtypes                              ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝

Testing with torch.float16
Success with torch.float16

Testing with torch.bfloat16
Success with torch.bfloat16
```

```
$ python 08-test-hipblaslt-perf.py
Environment check:
PYTORCH_ROCM_ARCH: gfx1151
HIPBLASLT_TENSILE_LIBPATH: /opt/rocm/lib/hipblaslt/library
TORCH_BLAS_PREFER_HIPBLASLT: 1
Testing GEMM performance...
GEMM 4096x4096x4096: 25.462 ms, 5.40 TFLOPS

Testing Attention performance...
Attention 8x16x2048x64: 13.512 ms, 10.17 TFLOPS

WARNING: GEMM performance is low. hipBLASLt may not be properly configured.
Check that:
1. The correct architecture kernels are in /opt/rocm/lib/hipblaslt/library
2. HIPBLASLT_TENSILE_LIBPATH is set correctly
3. Your GPU architecture matches the available kernels
```

In a container with both the Pytorch wheel and ROCm installed in `/opt/rocm`, the "Backend Selection Debug" part would show "torch.compile successful":
(Otherwise it'd show a message warning about missing `/opt/rocm/llvm/bin/ld.lld`)

```
$ python 09-test-attention-backend.py
=== Environment ===
PYTORCH_ROCM_ARCH: gfx1151
HIPBLASLT_TENSILE_LIBPATH: /opt/rocm/lib/hipblaslt/library
TORCH_BLAS_PREFER_HIPBLASLT: 1
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: 1

=== Backend Check ===
PyTorch version: 2.7.0a0+gitbfd8155
CUDA available: True
Current device: 0
Device name: AMD Radeon Graphics

=== AOTriton Check ===
Could not import pyaotriton: No module named 'pyaotriton'

=== SDPA Backends ===
Flash SDPA enabled: True
Memory efficient SDPA enabled: True
Math SDPA enabled: True

=== Testing Attention Variants ===

1. Standard SDPA (no causal):
Standard SDPA: 13.608 ms, 10.10 TFLOPS

2. Causal SDPA:
Causal SDPA: 13.983 ms, 9.83 TFLOPS

3. SDPA with attn_mask:
/var/home/scottt/work/strix-halo-testing/flash-attention/09-test-attention-backend.py:84: UserWarning: Efficient attention on ROCM requires attn_mask be boolean, or has the same datatype as of q,k,v (Triggered internally at /var/home/scottt/work/rocm-therock/external-builds/pytorch/src/aten/src/ATen/native/transformers/hip/sdp_utils.cpp:775.)
  return F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
SDPA with mask: 151.923 ms, 0.90 TFLOPS

4. Force Flash Attention backend:
/home/scottt/.local/share/uv/python/cpython-3.11.11-linux-x86_64-gnu/lib/python3.11/contextlib.py:105: FutureWarning: `torch.backends.cuda.sdp_kernel()` is deprecated. In the future, this context manager will be removed. Please see `torch.nn.attention.sdpa_kernel()` for the new context manager, with updated signature.
  self.gen = func(*args, **kwds)
Flash Attention: 13.600 ms, 10.11 TFLOPS

5. Force Math backend:
Math backend: 152.518 ms, 0.90 TFLOPS

=== Backend Selection Debug ===
JIT trace successful
torch.compile successful

=== Additional Debug Info ===
CUDA arch list: ['gfx1151']
CUDA capability: (11, 5)
Flash Attention forward function is NOT available
```

Though `09-test-attention-backend.py` would freeze up my machine when the script gets to where it should exit. (I suspect bad kernel memory management interactions)

Your benchmark choices are informative as usual. Thanks for sharing them.

---

### 评论 #12 — lhl (2025-05-20T05:02:52Z)

Hey @scottt awesome work getting the PyTorch working! 

I've also confirmed w/ the new wheel is running a lot faster (alas, nowhere near where the hardware is supposed to be. I've filed a separate issue since it appears that gfx1151 kernels seem to have a huge perf regression vs gfx1100: https://github.com/ROCm/ROCm/issues/4748):

```
(torch-scottt) lhl@cluster4:~/strix-halo-testing/flash-attention (main)$ python 05-attention-bench.py
/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_subclasses/functional_tensor.py:276: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /var/home/scottt/work/rocm-therock/external-builds/pytorch/src/torch/csrc/utils/tensor_numpy.cpp:81.)
  cpu = _conversion_method_template(device=torch.device("cpu"))
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                                  AOTriton Status Check                                  ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
PyTorch version: 2.7.0a0+gitbfd8155
CUDA available: True
ROCm version: 6.5.25190-39c57805b
TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL: 1
Could not import pyaotriton

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                           Testing Tiny: B=1, H=1, S=128, D=64                           ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.00 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         0.0197 |              0.11 |         0.0292 |              0.18 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.0169 |              0.12 |         0.0317 |              0.17 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                           Testing Small: B=2, H=4, S=512, D=64                          ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.00 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         0.0955 |              2.81 |         0.2661 |              2.52 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.1012 |              2.65 |         0.2546 |              2.64 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                          Testing Medium: B=4, H=8, S=1024, D=64                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.00 GB
Total QKV memory: 0.01 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |         0.8574 |              5.01 |         1.6965 |              6.33 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         0.7898 |              5.44 |         2.0618 |              5.21 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                          Testing Large: B=8, H=16, S=2048, D=64                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.03 GB
Total QKV memory: 0.09 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |        12.2018 |              5.63 |        23.2092 |              7.4  |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |         9.7758 |              7.03 |        28.6672 |              5.99 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                         Testing XLarge: B=16, H=16, S=4096, D=64                        ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Estimated memory per QKV tensor: 0.12 GB
Total QKV memory: 0.38 GB
+--------------+----------------+-------------------+----------------+-------------------+
| Operation    |   FW Time (ms) |   FW FLOPS (TF/s) |   BW Time (ms) |   BW FLOPS (TF/s) |
+==============+================+===================+================+===================+
| Causal FA2   |        95.0835 |              5.78 |        183.861 |              7.48 |
+--------------+----------------+-------------------+----------------+-------------------+
| Regular SDPA |        75.1058 |              7.32 |        333.403 |              4.12 |
+--------------+----------------+-------------------+----------------+-------------------+

╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                                         Summary                                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝
Tiny:
  Causal FA2: 0.0197 ms
  Regular SDPA: 0.0169 ms
Small:
  Causal FA2: 0.0955 ms
  Regular SDPA: 0.1012 ms
Medium:
  Causal FA2: 0.8574 ms
  Regular SDPA: 0.7898 ms
Large:
  Causal FA2: 12.2018 ms
  Regular SDPA: 9.7758 ms
XLarge:
  Causal FA2: 95.0835 ms
  Regular SDPA: 75.1058 ms
╔═════════════════════════════════════════════════════════════════════════════════════════╗
║                              Testing with different dtypes                              ║
╚═════════════════════════════════════════════════════════════════════════════════════════╝

Testing with torch.float16
Success with torch.float16

Testing with torch.bfloat16
Success with torch.bfloat16
```

BTW, https://github.com/pytorch-labs/attention-gym benchmark still seems to fail, not quite sure where that bug does to (I'm using stable upstream triton 3.3.0 btw)...
```
(torch-scottt)  2 lhl@cluster4:~/attention-gym (main)$ python examples/benchmark.py
Using the default sparsity block size: 128
Traceback (most recent call last):
  File "/home/lhl/attention-gym/examples/benchmark.py", line 262, in <module>
    main(**vars(args))
  File "/home/lhl/attention-gym/examples/benchmark.py", line 238, in main
    AVAILABLE_EXAMPLES[ex]()
  File "/home/lhl/attention-gym/examples/benchmark.py", line 30, in <lambda>
    "causal": lambda: test_mask(mask_mod=causal_mask),
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/attention-gym/examples/benchmark.py", line 117, in test_mask
    fwd_time = do_bench(attn)
               ^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/triton/testing.py", line 145, in do_bench
    fn()
  File "/home/lhl/attention-gym/examples/benchmark.py", line 105, in <lambda>
    flex_attention_call = lambda: flex_attention(*qkv, score_mod=score_mod, block_mask=block_mask)
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_dynamo/eval_frame.py", line 663, in _fn
    raise e.remove_dynamo_frames() from None  # see TORCHDYNAMO_VERBOSE=1
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/compile_fx.py", line 760, in _compile_fx_inner
    raise InductorError(e, currentframe()).with_traceback(
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/compile_fx.py", line 745, in _compile_fx_inner
    mb_compiled_graph = fx_codegen_and_compile(
                        ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/compile_fx.py", line 1295, in fx_codegen_and_compile
    return scheme.codegen_and_compile(gm, example_inputs, inputs_to_check, graph_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/compile_fx.py", line 1119, in codegen_and_compile
    graph.run(*example_inputs)
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/graph.py", line 877, in run
    return super().run(*args)
           ^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/fx/interpreter.py", line 171, in run
    self.env[node] = self.run_node(node)
                     ^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/graph.py", line 1527, in run_node
    result = super().run_node(n)
             ^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/fx/interpreter.py", line 240, in run_node
    return getattr(self, n.op)(n.target, args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/graph.py", line 1198, in call_function
    raise LoweringException(e, target, args, kwargs).with_traceback(
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/graph.py", line 1188, in call_function
    out = lowerings[target](*args, **kwargs)  # type: ignore[index]
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/lowering.py", line 466, in wrapped
    out = decomp_fn(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/kernel/flex_attention.py", line 1511, in flex_attention
    error = flex_attention_template.maybe_append_choice(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/codegen/common.py", line 2263, in maybe_append_choice
    choices.append(self.generate(**kwargs))
                   ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/select_algorithm.py", line 1151, in generate
    code = template.finalize_all()
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/select_algorithm.py", line 183, in finalize_all
    self.code = self.code.replace(key, fn())
                                       ^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/select_algorithm.py", line 543, in hook
    code.splice(self.jit_lines())
                ^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/select_algorithm.py", line 454, in jit_lines
    **TritonKernel.inductor_meta_common(),
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/_inductor/codegen/triton.py", line 3447, in inductor_meta_common
    "backend_hash": torch.utils._triton.triton_hash_with_backend(),
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/torch/utils/_triton.py", line 112, in triton_hash_with_backend
    key = f"{triton_key()}-{backend.hash()}"
                            ^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/triton/backends/amd/compiler.py", line 418, in hash
    version = subprocess.check_output([HIPBackend.path_to_rocm_lld(), "--version"], encoding='utf-8')
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lhl/miniforge3/envs/torch-scottt/lib/python3.11/site-packages/triton/backends/amd/compiler.py", line 197, in path_to_rocm_lld
    raise Exception("ROCm linker /opt/rocm/llvm/bin/ld.lld not found. Set 'TRITON_HIP_LLD_PATH' to its path.")
torch._inductor.exc.InductorError: LoweringException: Exception: ROCm linker /opt/rocm/llvm/bin/ld.lld not found. Set 'TRITON_HIP_LLD_PATH' to its path.
  target: flex_attention
  args[0]: TensorBox(StorageBox(
    InputBuffer(name='primals_1', layout=FixedLayout('cuda:0', torch.float16, size=[16, 16, 8192, 64], stride=[8388608, 524288, 64, 1]))
  ))
  args[1]: TensorBox(StorageBox(
    InputBuffer(name='primals_2', layout=FixedLayout('cuda:0', torch.float16, size=[16, 16, 8192, 64], stride=[8388608, 524288, 64, 1]))
  ))
  args[2]: TensorBox(StorageBox(
    InputBuffer(name='primals_3', layout=FixedLayout('cuda:0', torch.float16, size=[16, 16, 8192, 64], stride=[8388608, 524288, 64, 1]))
  ))
  args[3]: Subgraph(name='sdpa_score0', graph_module=<lambda>(), graph=None)
  args[4]: (8192, 8192, TensorBox(StorageBox(
    InputBuffer(name='primals_5', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64], stride=[64, 64, 1]))
  )), TensorBox(StorageBox(
    InputBuffer(name='primals_4', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64, 64], stride=[4096, 4096, 64, 1]))
  )), TensorBox(StorageBox(
    InputBuffer(name='primals_6', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64], stride=[64, 64, 1]))
  )), TensorBox(StorageBox(
    InputBuffer(name='primals_7', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64, 64], stride=[4096, 4096, 64, 1]))
  )), TensorBox(StorageBox(
    InputBuffer(name='primals_8', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64], stride=[64, 64, 1]))
  )), TensorBox(StorageBox(
    InputBuffer(name='primals_9', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64, 64], stride=[4096, 4096, 64, 1]))
  )), TensorBox(StorageBox(
    InputBuffer(name='primals_10', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64], stride=[64, 64, 1]))
  )), TensorBox(StorageBox(
    InputBuffer(name='primals_11', layout=FixedLayout('cuda:0', torch.int32, size=[1, 1, 64, 64], stride=[4096, 4096, 64, 1]))
  )), 128, 128, Subgraph(name='sdpa_mask0', graph_module=<lambda>(), graph=None))
  args[5]: 0.125
  args[6]: {'PRESCALE_QK': False, 'ROWS_GUARANTEED_SAFE': False, 'BLOCKS_ARE_CONTIGUOUS': False, 'WRITE_DQ': True, 'OUTPUT_LOGSUMEXP': True}
  args[7]: ()
  args[8]: ()

Set TORCHDYNAMO_VERBOSE=1 for the internal stack trace (please do this especially if you're reporting a bug to PyTorch). For even more developer context, set TORCH_LOGS="+dynamo"
```

I'll let mamf-finder run overnight and see how it does.

---

### 评论 #13 — lhl (2025-05-21T05:00:59Z)

> I'll let mamf-finder run overnight and see how it does.

@scottt btw so mamf-finder is at about 4 TFLOPS - I believe this means that the PyTorch isn't leveraging hipBLASLt properly? Do you have a build recipe I can look at? Mine had hipBLASLt working but SDPA wasn't picking up my AOTriton...  combining both together should in theory create a much more performant wheel.

Also would love to be able to build a 3.12 or newer wheels...

---

### 评论 #14 — scottt (2025-05-23T19:26:16Z)

Hi @lhl, 

# attention-gym benchmark.py failure

[`attention-gym/examples/benchmark.py`](https://github.com/pytorch-labs/attention-gym/blob/a710e189d601cb2c7c7676fa95582626da44775b/examples/benchmark.py#L50) calls `torch.compile()` on line [50](https://github.com/pytorch-labs/attention-gym/blob/a710e189d601cb2c7c7676fa95582626da44775b/examples/benchmark.py#L50)

`torch.compile()` expects an LLVM toolchain targetting AMD gpus, in particular the linker that combines the GPU and host CPU code to reside in `/opt/rocm`

See message `Exception("ROCm linker /opt/rocm/llvm/bin/ld.lld not found. Set 'TRITON_HIP_LLD_PATH' to its path.")`

So you could download a gfx1151 nightly build from TheRock and place that in `/opt/rocm` in your testing container image or point `TRITON_HIP_LLD_PATH` to the `ld.lld` linker.

# mamf-finder stuck at 4 TFLOPS

* ~~I'd investigate if this Pytorch [patch])(https://github.com/scottt/rocm-TheRock/commit/ea1500c11eb165af229c0fbfd65686c3de8a9509_ got applied successfully by see if Pytorch is calling into rocBLAS instead of hipBLASLt during run time by invstigating the libraries that got mapped in when the test is run by perhaps setting [`LD_DEBUG`](https://man7.org/linux/man-pages/man8/ld.so.8.html)~~  The latest Pytorch wheel is defaulting to using rocBLAS instead of hipBLASLt, the one you first tested defaulted to the latter. We'll change the default in the next build. You could set the `TORCH_BLAS_PREFER_HIPBLASLT` environment variable to `1` to request the use of hipBLASLt.

# AOTriton Enabled Pytorch build procedure

For aotriton enabled Pytorch, my build procedure for Linux is:

1. Build [`rocm_manylinux.Dockerfile`](https://github.com/scottt/rocm-TheRock/blob/gfx1151/dockerfiles/pytorch-dev/rocm_manylinux.Dockerfile): put TheRock nightly builds into an image
2. Build [`pytorch_build_manylinux.Dockerfile`](https://github.com/scottt/rocm-TheRock/blob/gfx1151/dockerfiles/pytorch-dev/pytorch_build_manylinux.Dockerfile): use the previous image but switch the host CPU compiler toolchain for building Pytorch
3. I then use a variant of this process adapted to Linux https://github.com/ROCm/TheRock/discussions/409#discussioncomment-13135490
(It's a step backwards from having a rebuildable Dockefile, I know)


---
