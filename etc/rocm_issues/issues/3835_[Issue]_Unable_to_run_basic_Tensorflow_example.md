# [Issue]: Unable to run basic Tensorflow example

> **Issue #3835**
> **状态**: closed
> **创建时间**: 2024-09-29T23:13:09Z
> **更新时间**: 2025-11-01T11:21:14Z
> **关闭时间**: 2025-05-05T20:24:50Z
> **作者**: navendugarg
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3835

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

2024-09-29 17:59:20.236408: E external/local_xla/xla/stream_executor/plugin_registry.cc:91] Invalid plugin kind specified: FFT
2024-09-29 17:59:20.263474: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2024-09-29 17:59:20.483636: E external/local_xla/xla/stream_executor/plugin_registry.cc:91] Invalid plugin kind specified: DNN
TensorFlow version: 2.16.1
/home/loc1/.local/lib/python3.10/site-packages/keras/src/layers/reshaping/flatten.py:37: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(**kwargs)
2024-09-29 17:59:21.733612: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.733657: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.760637: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.760684: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.760703: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.760719: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.760728: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2306] Ignoring visible gpu device (device: 1, name: AMD Radeon Graphics, pci bus id: 0000:14:00.0) with AMDGPU version : gfx1036. The supported AMDGPU versions are gfx900, gfx906, gfx908, gfx90a, gfx940, gfx941, gfx942, gfx1030, gfx1100.
2024-09-29 17:59:21.761600: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.761639: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.761657: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.761702: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.761722: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.761746: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:926] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2024-09-29 17:59:21.761758: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1928] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 23512 MB memory:  -> device: 0, name: Radeon RX 7900 XTX, pci bus id: 0000:03:00.0
2024-09-29 17:59:22.205041: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205058: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205070: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205085: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205109: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205121: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205137: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205148: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205163: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205179: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205199: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205214: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
2024-09-29 17:59:22.205229: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
2024-09-29 17:59:22.206171: E tensorflow/compiler/mlir/tools/kernel_gen/tf_framework_c_interface.cc:207] INTERNAL: Generating device code failed.
2024-09-29 17:59:22.206849: W tensorflow/core/framework/op_kernel.cc:1827] UNKNOWN: JIT compilation failed.
2024-09-29 17:59:22.206862: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: UNKNOWN: JIT compilation failed.
Traceback (most recent call last):
  File "/home/loc1/workspace/test-tf/src/test.py", line 26, in <module>
    main()
  File "/home/loc1/workspace/test-tf/src/test.py", line 9, in main
    model = tf.keras.models.Sequential([
  File "/home/loc1/.local/lib/python3.10/site-packages/keras/src/models/sequential.py", line 75, in __init__
    self._maybe_rebuild()
  File "/home/loc1/.local/lib/python3.10/site-packages/keras/src/models/sequential.py", line 140, in _maybe_rebuild
    self.build(input_shape)
  File "/home/loc1/.local/lib/python3.10/site-packages/keras/src/layers/layer.py", line 226, in build_wrapper
    original_build_method(*args, **kwargs)
  File "/home/loc1/.local/lib/python3.10/site-packages/keras/src/models/sequential.py", line 186, in build
    x = layer(x)
  File "/home/loc1/.local/lib/python3.10/site-packages/keras/src/utils/traceback_utils.py", line 122, in error_handler
    raise e.with_traceback(filtered_tb) from None
  File "/home/loc1/.local/lib/python3.10/site-packages/keras/src/backend/tensorflow/random.py", line 19, in _cast_seed
    seed = tf.cast(tf.math.floormod(seed, tf.int32.max - 1), dtype="int32")
tensorflow.python.framework.errors_impl.UnknownError: {{function_node __wrapped__FloorMod_device_/job:localhost/replica:0/task:0/device:GPU:0}} JIT compilation failed. [Op:FloorMod] name: 


### Operating System

Ubuntu 24.04.1 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 7900

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

While running Tensorflow Basic Example using Tensorflow 2.16.1 I get the above error. 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.8.5 is loaded
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
  Name:                    AMD Ryzen 9 7900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7900X 12-Core Processor
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
  Max Clock Freq. (MHz):   5733                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131000804(0x7cee9e4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131000804(0x7cee9e4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131000804(0x7cee9e4) KB            
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
  Uuid:                    GPU-d65ed86a37893e85               
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
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 342                                
  SDMA engine uCode::      21                                 
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   5120                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 21                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65500400(0x3e774f0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65500400(0x3e774f0) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
*** Done ***        ROCk module version 6.8.5 is loaded
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
  Name:                    AMD Ryzen 9 7900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7900X 12-Core Processor
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
  Max Clock Freq. (MHz):   5733                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131000804(0x7cee9e4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131000804(0x7cee9e4) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131000804(0x7cee9e4) KB            
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
  Uuid:                    GPU-d65ed86a37893e85               
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
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
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
  Packet Processor uCode:: 342                                
  SDMA engine uCode::      21                                 
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
*******                  
Agent 3                  
*******                  
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   5120                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 21                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65500400(0x3e774f0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65500400(0x3e774f0) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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

I install ROCM 6.2.2

---

## 评论 (34 条)

### 评论 #1 — ppanchad-amd (2024-09-30T15:21:19Z)

Hi @navendugarg, internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2024-09-30T19:35:56Z)

Hi @navendugarg, 

> While running Tensorflow Basic Example using Tensorflow 2.16.1 I get the above error.

Are you referring to the code at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/tensorflow-install.html#running-a-basic-tensorflow-example? If so, I can't reproduce this on a 7900XTX + Ubuntu 22.04 + ROCm 6.2.2. I followed the steps at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/tensorflow-install.html to install tensorflow and then ran that code inside the docker. 

I notice you have integrated graphics enabled, which is known to cause issues with ROCm. Try disabling your integrated graphics and see if that helps. 

---

### 评论 #3 — navendugarg (2024-09-30T20:20:19Z)

I am on Ubuntu 24.04.1 LTS (Noble Numbat) and not 22.04

Please note 6.2.0 was working fine before. When I tried to downgrade to 6.2.0 I could not install the build.





---

### 评论 #4 — schung-amd (2024-09-30T21:18:39Z)

I cannot reproduce this on Ubuntu 24.04 either.

> Please note 6.2.0 was working fine before. When I tried to downgrade to 6.2.0 I could not install the build.

Do you mean you went 6.2 (working) -> 6.2.2 (broken) -> 6.2 (can't install)? And I'm assuming you mean you could not install tensorflow at all? 

---

### 评论 #5 — navendugarg (2024-09-30T21:26:08Z)

Steps:
1) I had installed 6.2.0 on Ubuntu 22.04 initially
2) Upgraded to Ubuntu 22.04 to 24.04.1. No issues with ROCM 6.2.0. I could run Tensorflow 2.16.1
3) Upgraded to ROCM 6.2.2 recently. Now I am getting the issue I shared above with Tensorflow 2.16.1
4) Uninstalled ROCM 6.2.2 and installed ROCM 6.2.0 : Could not install ROCM 6.2.0 there was an issue with during Kernel Build process.
5) Installed ROCM 6.2.2. Still getting the above error

---

### 评论 #6 — schung-amd (2024-10-01T13:29:26Z)

> Uninstalled ROCM 6.2.2 and installed ROCM 6.2.0 : Could not install ROCM 6.2.0 there was an issue with during Kernel Build process.

What version is your kernel? There is a known incompatibility between ROCm 6.2 and the recent kernel version 6.8.0-45. If you want to reinstall ROCm 6.2 you'll have to downgrade your kernel.

---

### 评论 #7 — schung-amd (2024-10-16T13:30:30Z)

Closing this for now as I can't reproduce the issue, if you are still experiencing it and require additional guidance feel free to comment and we can reopen this.

---

### 评论 #8 — keejkrej (2024-11-26T21:39:19Z)

Same issue on 7900XTX + Ubuntu 24.04 + ROCm 6.2.4 + Tensorflow 2.16.1 + Python 3.9 if installed with wheels.
`2024-11-26 22:30:21.902565: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc`
`2024-11-26 22:30:21.904130: E tensorflow/compiler/mlir/tools/kernel_gen/tf_framework_c_interface.cc:207] INTERNAL: Generating device code failed.`
On docker everything runs fine

---

### 评论 #9 — keejkrej (2024-11-26T22:28:54Z)

Rolling back to ROCm 6.2 fixes the problem

---

### 评论 #10 — schung-amd (2024-11-27T15:25:13Z)

Couldn't repro this last time I tried, but I'll take another look.

---

### 评论 #11 — schung-amd (2024-11-27T16:08:41Z)

I was able to repro on 7900XTX + Ubuntu 24.04 + ROCm 6.2.4 + tensorflow-rocm 2.16.1 + Python 3.10. Setting `ROCM_PATH=/opt/rocm` resolves this as a workaround.

It seems like ROCM_PATH is being defined explicitly by Tensorflow in several places as `/opt/rocm-6.2.0`, which would result in exactly the behavior you're seeing. Technically the wheels are contained in directories which correspond to specific ROCm versions, but I don't see a reason to explicitly remove support for other ROCm versions. I'll take a look into this.

---

### 评论 #12 — schung-amd (2024-11-27T16:54:23Z)

This was somewhat of a known issue: for example, see https://github.com/ROCm/ROCm/issues/1796. I've reached out to the internal team and we're looking into changing our build process so that the ROCm version is not strictly required. Let me know if setting `ROCM_PATH=/opt/rocm` resolves this issue for you @navendugarg @keejkrej. If you're still experiencing this issue feel free to comment and I'll reopen this to investigate further.

---

### 评论 #13 — jin-eld (2024-12-14T00:26:38Z)

Hi, @schung-amd I am basically having the same problem, I guess I was too early to confirm https://github.com/ROCm/tensorflow-upstream/issues/2374 as working, now that I tried actually using `tensorflow-rocm` I am getting pretty much the same output as the author of this issue.

Since I am using Fedora 41, I have ROCm 6.2.1 installed via `dnf`, because Fedora offers ROCm rpm packages as part of their official package repository, which in turn means that all the libraries and components are not installed to `/opt/rocm`, but live in their respective system locations like `/usr/lib` and so on, for example `opencl.bc` is part of the `rocm-device-libs-18-9.rocm6.2.1.fc41.x86_64` package and ends up in `/usr/lib/clang/18/amdgcn/bitcode/opencl.bc`

So, basically I am having a hard time setting `ROCM_PATH`, because I am not sure what is expected in my setup; I tried `export ROCM_PATH=/`, but I am still getting errors like:
```
2024-12-14 01:21:27.064331: E external/local_xla/xla/service/gpu/llvm_gpu_backend/gpu_backend_lib.cc:243] bitcode module is required by this HLO module but was not found at ./opencl.bc
error: Failure when generating HSACO
2024-12-14 01:21:27.069230: E tensorflow/compiler/mlir/tools/kernel_gen/tf_framework_c_interface.cc:207] INTERNAL: Generating device code failed.
2024-12-14 01:21:27.071437: W tensorflow/core/framework/op_kernel.cc:1827] UNKNOWN: JIT compilation failed.
```

Any chance to get away from hardcoding `/opt/rocm` in `tensorflow`? Alternatively, could anyone please post a file list/directory structure of their `/opt/rocm` installation, as a temporary hack I could probably create a fake `/opt/rocm` directory and link the files to their expected locations.

---

### 评论 #14 — schung-amd (2025-01-02T15:53:49Z)

Hi, sorry for the late response. I'll look into workarounds for the way the Fedora packages are installed, but this might be tricky at the moment because we don't officially support Fedora (and by extension, the locations that Fedora or any other unsupported distro places its ROCm files in). 

> Alternatively, could anyone please post a file list/directory structure of their /opt/rocm installation, as a temporary hack I could probably create a fake /opt/rocm directory and link the files to their expected locations.

The bitcode libraries are located in $ROCM_PATH/amdgcn/bitcode by default. We can work through any other missing file issues as they pop up.

---

### 评论 #15 — jin-eld (2025-01-02T16:02:33Z)

Well, my very naive question would be - why isn't the installation distro agnostic, i.e. wouldn't it be enough to install everything into default Linux system directories like `/usr/lib64` and so on? :)

By the way, Fedora is one of few distros with excellent ROCm support, you can install the whole ROCm stack and related tools and utilities directly from the official repository just like any other package by simply using `dnf install`, everything is packaged and available as RPM. I know the packagers had to put some effort into getting rid of `$ROCM_PATH` though ;)

Just as an example for the file list of one of the packages:
https://rpmfind.net/linux/RPM/fedora/41/x86_64/r/rocm-core-6.2.0-1.fc41.x86_64.html

---

### 评论 #16 — schung-amd (2025-01-02T16:35:20Z)

> Well, my very naive question would be - why isn't the installation distro agnostic, i.e. wouldn't it be enough to install everything into default Linux system directories like /usr/lib64 and so on?

I don't know the exact/full reasons this decision was made, but off the top of my head having the ROCm files contained entirely within a single directory (i.e. /opt/rocm-a.b.c if not set otherwise) is useful for portability and having multiple versions installed, which is probably a lot more useful in a datacenter/multiple user context than for a regular desktop consumer. This may change in the future as priorities shift, but for now this is generally a non-issue with our supported release streams.

> By the way, Fedora is one of few distros with excellent ROCm support, you can install the whole ROCm stack and related tools and utilities directly from the official repository just like any other package by simply using dnf install, everything is packaged and available as RPM.

I agree that it is convenient to have in-box ROCm packages; however, as these are unofficial they are not extensively tested (hence the issue you are observing). At the moment we are not officially supporting any in-box distributions of ROCm, so while they are probably mostly functional we cannot guarantee anything.

---

### 评论 #17 — jin-eld (2025-01-02T16:46:59Z)

Thank you for the explanation, I guess it's clearer why it is as it is, I hope at some point it could be addressed, right now I'd say Fedora is _the_ goto-distro for end-users with AMD hardware.

---

### 评论 #18 — chowdri (2025-04-24T07:52:54Z)

I'm having this exact same problem following this guide: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-tensorflow.html
I have a 7900 GRE and Vega 64, rocm 6.3.4 and tensorflow-rocm (2.17.0).
The programs execute on other versions of tensorflow using the CPU. However, getting programs to work on tensorflow-rocm is the problem. 
I have tried setting ROCM_PATH variable to /opt/rocm-6.3.4, however, this does not change the outcome of the program. 

```
$ ls -lah /opt/rocm-6.3.4/

total 40K
drwxr-xr-x  8 root root 4.0K Apr 24 01:23 .
drwxr-xr-x  4 root root 4.0K Apr 24 01:19 ..
lrwxrwxrwx  1 root root   32 Feb 21 08:51 amdgcn -> lib/llvm/lib/clang/18/lib/amdgcn
drwxr-xr-x  2 root root 4.0K Apr 24 01:23 bin
drwxr-xr-x 45 root root 4.0K Apr 24 01:23 include
drwxr-xr-x  2 root root 4.0K Apr 24 01:23 .info
drwxr-xr-x 14 root root  12K Apr 24 01:24 lib
drwxr-xr-x  9 root root 4.0K Apr 24 01:23 libexec
lrwxrwxrwx  1 root root   10 Feb 21 08:39 llvm -> ./lib/llvm
drwxr-xr-x 22 root root 4.0K Apr 24 01:23 share

$ echo $ROCM_PATH

/opt/rocm-6.3.4

$ cat tensortest.py

import tensorflow as tf
print("TensorFlow version:", tf.__version__)
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
model = tf.keras.models.Sequential([ tf.keras.layers.Flatten(input_shape=(28, 28)), tf.keras.layers.Dense(128, activation='relu'), tf.keras.layers.Dropout(0.2), tf.keras.layers.Dense(10)])
predictions = model(x_train[:1]).numpy()
tf.nn.softmax(predictions).numpy()
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
loss_fn(y_train[:1], predictions).numpy()
model.compile(optimizer='adam',loss=loss_fn, metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test,  y_test, verbose=2)

$ python3 tensortest.py 

2025-04-24 13:21:01.681428: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
TensorFlow version: 2.17.0
/usr/local/lib/python3.12/dist-packages/keras/src/layers/reshaping/flatten.py:37: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(**kwargs)
2025-04-24 13:21:02.859383: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:02.859428: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.732432: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.732472: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.732497: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.732518: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733531: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733559: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733590: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733608: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733626: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733643: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733682: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733703: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733724: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733744: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733765: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.733777: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2021] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 15320 MB memory:  -> device: 0, name: Radeon RX 7900 GRE, pci bus id: 0000:03:00.0
2025-04-24 13:21:04.883168: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-04-24 13:21:04.883190: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2021] Created device /job:localhost/replica:0/task:0/device:GPU:1 with 7660 MB memory:  -> device: 1, name: Radeon RX Vega, pci bus id: 0000:19:00.0
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
2025-04-24 13:21:05.279761: E tensorflow/compiler/mlir/tools/kernel_gen/tf_framework_c_interface.cc:228] INTERNAL: Generating device code failed.
2025-04-24 13:21:05.280424: W tensorflow/core/framework/op_kernel.cc:1828] UNKNOWN: JIT compilation failed.
2025-04-24 13:21:05.280439: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: UNKNOWN: JIT compilation failed.
Traceback (most recent call last):
  File "/home/praful/tensortest.py", line 6, in <module>
    model = tf.keras.models.Sequential([ tf.keras.layers.Flatten(input_shape=(28, 28)), tf.keras.layers.Dense(128, activation='relu'), tf.keras.layers.Dropout(0.2), tf.keras.layers.Dense(10)])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/models/sequential.py", line 76, in __init__
    self._maybe_rebuild()
  File "/usr/local/lib/python3.12/dist-packages/keras/src/models/sequential.py", line 149, in _maybe_rebuild
    self.build(input_shape)
  File "/usr/local/lib/python3.12/dist-packages/keras/src/layers/layer.py", line 230, in build_wrapper
    original_build_method(*args, **kwargs)
  File "/usr/local/lib/python3.12/dist-packages/keras/src/models/sequential.py", line 195, in build
    x = layer(x)
        ^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/utils/traceback_utils.py", line 122, in error_handler
    raise e.with_traceback(filtered_tb) from None
  File "/usr/local/lib/python3.12/dist-packages/keras/src/backend/tensorflow/random.py", line 19, in _cast_seed
    seed = tf.cast(tf.math.floormod(seed, tf.int32.max - 1), dtype="int32")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tensorflow.python.framework.errors_impl.UnknownError: {{function_node __wrapped__FloorMod_device_/job:localhost/replica:0/task:0/device:GPU:0}} JIT compilation failed. [Op:FloorMod] name: 
```

---

### 评论 #19 — schung-amd (2025-04-24T14:23:06Z)

@chowdri Are you also on Fedora, or is this a supported distro?

---

### 评论 #20 — chowdri (2025-04-24T14:33:29Z)

elementary os 8 (ubuntu 24.04). I think ubuntu 24.04 is supported (at least as per the guide I have linked).

I have also tried setting `ROCR_VISIBLE_DEVICES` environment variable to no avail. 

---

### 评论 #21 — schung-amd (2025-04-24T14:40:50Z)

Yep, should be. Setting ROCM_PATH fixed this last time I tried, but I'll revisit as something may have changed.

---

### 评论 #22 — chowdri (2025-04-24T14:44:26Z)

I have opened this issue on tensorflow also: https://github.com/tensorflow/tensorflow/issues/91845
There the response seems unclear. As if I have not clarified the problem. 
is tensorflow-rocm not maintained by tensorflow?


---

### 评论 #23 — chowdri (2025-05-02T20:37:20Z)

Let me know if there's no solution in the near term. In that case, I'll dispose my GPUs to someone who may need them. 

Much thanks for the time and effort expended on this problem. 

---

### 评论 #24 — schung-amd (2025-05-02T21:22:27Z)

Unfortunately I haven't been able to reproduce this on Ubuntu 24.04 + 7900XTX with any combination of ROCm 6.3.4 and 6.4.0 with tensorflow-rocm [2.17.1](https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4/tensorflow_rocm-2.17.1-cp312-cp312-manylinux_2_28_x86_64.whl) and [2.18.1](https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4/tensorflow_rocm-2.18.1-cp312-cp312-manylinux_2_28_x86_64.whl) after setting ROCM_PATH=/opt/rocm, with the example at https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/tensorflow-install.html#running-a-basic-tensorflow-example.

You may need to disable one of the GPUs with HIP_VISIBLE_DEVICES=0 or 1. I haven't been able to test with your specific config (7900GRE and Vega) to check for an incompatibility.

---

### 评论 #25 — chowdri (2025-05-02T23:09:08Z)

```
$ export HIP_VISIBLE_DEVICES=0

$ echo $HIP_VISIBLE_DEVICES

0

$ python3 tensortest.py

2025-05-03 04:35:40.999873: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
TensorFlow version: 2.17.0
/usr/local/lib/python3.12/dist-packages/keras/src/layers/reshaping/flatten.py:37: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(**kwargs)
2025-05-03 04:35:43.288598: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.765892: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.765929: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.766831: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.766875: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.766894: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.767335: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.767360: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.767401: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:35:45.767414: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2021] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 15300 MB memory:  -> device: 0, name: Radeon RX 7900 GRE, pci bus id: 0000:03:00.0
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
error: Failure when generating HSACO
2025-05-03 04:35:49.191219: E tensorflow/compiler/mlir/tools/kernel_gen/tf_framework_c_interface.cc:228] INTERNAL: Generating device code failed.
2025-05-03 04:35:49.192387: W tensorflow/core/framework/op_kernel.cc:1828] UNKNOWN: JIT compilation failed.
2025-05-03 04:35:49.192406: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: UNKNOWN: JIT compilation failed.
Traceback (most recent call last):
  File "/home/praful/tensortest.py", line 6, in <module>
    model = tf.keras.models.Sequential([ tf.keras.layers.Flatten(input_shape=(28, 28)), tf.keras.layers.Dense(128, activation='relu'), tf.keras.layers.Dropout(0.2), tf.keras.layers.Dense(10)])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/models/sequential.py", line 76, in __init__
    self._maybe_rebuild()
  File "/usr/local/lib/python3.12/dist-packages/keras/src/models/sequential.py", line 149, in _maybe_rebuild
    self.build(input_shape)
  File "/usr/local/lib/python3.12/dist-packages/keras/src/layers/layer.py", line 230, in build_wrapper
    original_build_method(*args, **kwargs)
  File "/usr/local/lib/python3.12/dist-packages/keras/src/models/sequential.py", line 195, in build
    x = layer(x)
        ^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/utils/traceback_utils.py", line 122, in error_handler
    raise e.with_traceback(filtered_tb) from None
  File "/usr/local/lib/python3.12/dist-packages/keras/src/backend/tensorflow/random.py", line 19, in _cast_seed
    seed = tf.cast(tf.math.floormod(seed, tf.int32.max - 1), dtype="int32")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tensorflow.python.framework.errors_impl.UnknownError: {{function_node __wrapped__FloorMod_device_/job:localhost/replica:0/task:0/device:GPU:0}} JIT compilation failed. [Op:FloorMod] name: 

$ export HIP_VISIBLE_DEVICES=1

$ echo $HIP_VISIBLE_DEVICES

1

$ python3 tensortest.py 

2025-05-03 04:37:47.243958: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
TensorFlow version: 2.17.0
/usr/local/lib/python3.12/dist-packages/keras/src/layers/reshaping/flatten.py:37: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(**kwargs)
2025-05-03 04:37:48.412352: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.134716: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.134752: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.135774: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.135811: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.135831: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.135876: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.135897: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.135919: I external/local_xla/xla/stream_executor/rocm/rocm_executor.cc:920] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2025-05-03 04:37:50.135931: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2021] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 7660 MB memory:  -> device: 0, name: Radeon RX Vega, pci bus id: 0000:19:00.0
2025-05-03 04:37:50.362458: W tensorflow/compiler/mlir/tools/kernel_gen/tf_gpu_runtime_wrappers.cc:40] 'hipModuleLoadData(&module, data)' failed with 'hipErrorNoBinaryForGpu'

2025-05-03 04:37:50.362477: W tensorflow/compiler/mlir/tools/kernel_gen/tf_gpu_runtime_wrappers.cc:40] 'hipModuleGetFunction(&function, module, kernel_name)' failed with 'hipErrorInvalidHandle'

2025-05-03 04:37:50.362485: W tensorflow/core/framework/op_kernel.cc:1828] INTERNAL: 'hipModuleLaunchKernel( function, gridX, gridY, gridZ, blockX, blockY, blockZ, 0, reinterpret_cast<hipStream_t>(stream), params, nullptr)' failed with 'hipErrorInvalidHandle'
2025-05-03 04:37:50.362494: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: INTERNAL: 'hipModuleLaunchKernel( function, gridX, gridY, gridZ, blockX, blockY, blockZ, 0, reinterpret_cast<hipStream_t>(stream), params, nullptr)' failed with 'hipErrorInvalidHandle'
Traceback (most recent call last):
  File "/home/praful/tensortest.py", line 6, in <module>
    model = tf.keras.models.Sequential([ tf.keras.layers.Flatten(input_shape=(28, 28)), tf.keras.layers.Dense(128, activation='relu'), tf.keras.layers.Dropout(0.2), tf.keras.layers.Dense(10)])
                                                                                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/layers/regularization/dropout.py", line 53, in __init__
    self.seed_generator = backend.random.SeedGenerator(seed)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/random/seed_generator.py", line 87, in __init__
    self.state = self.backend.Variable(
                 ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/backend/common/variables.py", line 186, in __init__
    self._initialize_with_initializer(initializer)
  File "/usr/local/lib/python3.12/dist-packages/keras/src/backend/tensorflow/core.py", line 48, in _initialize_with_initializer
    self._initialize(lambda: initializer(self._shape, dtype=self._dtype))
  File "/usr/local/lib/python3.12/dist-packages/keras/src/backend/tensorflow/core.py", line 39, in _initialize
    self._value = tf.Variable(
                  ^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/tensorflow/python/util/traceback_utils.py", line 153, in error_handler
    raise e.with_traceback(filtered_tb) from None
  File "/usr/local/lib/python3.12/dist-packages/keras/src/backend/tensorflow/core.py", line 48, in <lambda>
    self._initialize(lambda: initializer(self._shape, dtype=self._dtype))
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/random/seed_generator.py", line 84, in seed_initializer
    return self.backend.convert_to_tensor([seed, 0], dtype=dtype)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/keras/src/backend/tensorflow/core.py", line 139, in convert_to_tensor
    return tf.cast(x, dtype)
           ^^^^^^^^^^^^^^^^^
tensorflow.python.framework.errors_impl.InternalError: {{function_node __wrapped__Cast_device_/job:localhost/replica:0/task:0/device:GPU:0}} 'hipModuleLaunchKernel( function, gridX, gridY, gridZ, blockX, blockY, blockZ, 0, reinterpret_cast<hipStream_t>(stream), params, nullptr)' failed with 'hipErrorInvalidHandle' [Op:Cast] name: 



```

---

### 评论 #26 — chowdri (2025-05-03T09:25:09Z)

As long as the hardware is supported, shouldn't this work by default? Let me know if I can run diagnostics for installation errors or prerequisite errors. 

For clarification, the 7900 GRE is installed on PCIE 5.0 x16 slot (running at PCIE 3.0 with a PCIE 3.0 X16 riser cable). The Vega 64 is installed on a PCIE 4.0 x4 slot (with the same riser cable). 

---

### 评论 #27 — schung-amd (2025-05-05T14:50:20Z)

Thanks for checking! I don't think the Vega 64 is supported, but this should run on the 7900 GRE. Unfortunately the error message you're seeing on the 7900 isn't very descriptive, but it doesn't look like this is the same issue as previous posters who had "failure to find bitcode". Can you try ROCm 6.4.0 + tensorflow-rocm 2.18.1? Also, does this issue occur in the rocm/tensorflow:latest docker image? Another difference I can think of is the OS; while elementary OS is Ubuntu-based, we don't officially support it and there may be issues there we don't see on Ubuntu, but I understand it may not be feasible for you to install Ubuntu to test.

---

### 评论 #28 — chowdri (2025-05-05T15:06:10Z)

I've installed tensorflow-rocm using pip as per the rocm guide (https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-tensorflow.html). The guide did not provide an alternative. 

When you mean rocm 6.4.0 and tensorflow-rocm 2.18.1 for installation, are you referring to git repo or specific packages available somewhere?

The packages I have installed satisfy the compatibility matrix prescribed by rocm: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html

Would addressing this issue on tensorflow github be more appropriate? Not that they are responsive. 

---

### 评论 #29 — schung-amd (2025-05-05T15:15:07Z)

> When you mean rocm 6.4.0 and tensorflow-rocm 2.18.1 for installation, are you referring to git repo or specific packages available somewhere?

The non-Radeon-specific release channels are more up to date, and support the 7900GRE: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html, https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/tensorflow-install.html.

> Would addressing this issue on tensorflow github be more appropriate?

Potentially, depending on where this error is stemming from, but unless we rule out one of our components causing this failure it's fine to address this here.

---

### 评论 #30 — chowdri (2025-05-05T20:15:49Z)

ok, this works. Used pip for the tensorflow upgrade. 

```
$ sudo pip3 install tensorflow-rocm==2.18.1 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4 --upgrade --break-system-packages

Looking in links: https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4
Collecting tensorflow-rocm==2.18.1
  Downloading https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4/tensorflow_rocm-2.18.1-cp312-cp312-manylinux_2_28_x86_64.whl (550.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 550.8/550.8 MB 2.8 MB/s eta 0:00:00
Requirement already satisfied: absl-py>=1.0.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (2.2.2)
Requirement already satisfied: astunparse>=1.6.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (1.6.3)
Requirement already satisfied: flatbuffers>=24.3.25 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (25.2.10)
Requirement already satisfied: gast!=0.5.0,!=0.5.1,!=0.5.2,>=0.2.1 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (0.6.0)
Requirement already satisfied: google-pasta>=0.1.1 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (0.2.0)
Requirement already satisfied: libclang>=13.0.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (18.1.1)
Requirement already satisfied: opt-einsum>=2.3.2 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (3.4.0)
Requirement already satisfied: packaging in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (25.0)
Requirement already satisfied: protobuf!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<6.0.0dev,>=3.20.3 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (4.25.6)
Requirement already satisfied: requests<3,>=2.21.0 in /usr/lib/python3/dist-packages (from tensorflow-rocm==2.18.1) (2.31.0)
Requirement already satisfied: setuptools in /usr/lib/python3/dist-packages (from tensorflow-rocm==2.18.1) (68.1.2)
Requirement already satisfied: six>=1.12.0 in /usr/lib/python3/dist-packages (from tensorflow-rocm==2.18.1) (1.16.0)
Requirement already satisfied: termcolor>=1.1.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (3.0.1)
Requirement already satisfied: typing-extensions>=3.6.6 in /usr/lib/python3/dist-packages (from tensorflow-rocm==2.18.1) (4.10.0)
Requirement already satisfied: wrapt>=1.11.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (1.17.2)
Requirement already satisfied: grpcio<2.0,>=1.24.3 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (1.71.0)
Collecting tensorboard<2.19,>=2.18 (from tensorflow-rocm==2.18.1)
  Downloading tensorboard-2.18.0-py3-none-any.whl.metadata (1.6 kB)
Requirement already satisfied: keras>=3.5.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (3.9.2)
Requirement already satisfied: numpy<2.1.0,>=1.26.0 in /usr/lib/python3/dist-packages (from tensorflow-rocm==2.18.1) (1.26.4)
Requirement already satisfied: h5py>=3.11.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (3.13.0)
Requirement already satisfied: ml-dtypes<1.0.0,>=0.4.0 in /usr/local/lib/python3.12/dist-packages (from tensorflow-rocm==2.18.1) (0.4.1)
Requirement already satisfied: wheel<1.0,>=0.23.0 in /usr/lib/python3/dist-packages (from astunparse>=1.6.0->tensorflow-rocm==2.18.1) (0.42.0)
Requirement already satisfied: rich in /usr/lib/python3/dist-packages (from keras>=3.5.0->tensorflow-rocm==2.18.1) (13.7.1)
Requirement already satisfied: namex in /usr/local/lib/python3.12/dist-packages (from keras>=3.5.0->tensorflow-rocm==2.18.1) (0.0.8)
Requirement already satisfied: optree in /usr/local/lib/python3.12/dist-packages (from keras>=3.5.0->tensorflow-rocm==2.18.1) (0.15.0)
Requirement already satisfied: markdown>=2.6.8 in /usr/local/lib/python3.12/dist-packages (from tensorboard<2.19,>=2.18->tensorflow-rocm==2.18.1) (3.8)
Requirement already satisfied: tensorboard-data-server<0.8.0,>=0.7.0 in /usr/local/lib/python3.12/dist-packages (from tensorboard<2.19,>=2.18->tensorflow-rocm==2.18.1) (0.7.2)
Requirement already satisfied: werkzeug>=1.0.1 in /usr/local/lib/python3.12/dist-packages (from tensorboard<2.19,>=2.18->tensorflow-rocm==2.18.1) (3.1.3)
Requirement already satisfied: MarkupSafe>=2.1.1 in /usr/lib/python3/dist-packages (from werkzeug>=1.0.1->tensorboard<2.19,>=2.18->tensorflow-rocm==2.18.1) (2.1.5)
Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/lib/python3/dist-packages (from rich->keras>=3.5.0->tensorflow-rocm==2.18.1) (3.0.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/lib/python3/dist-packages (from rich->keras>=3.5.0->tensorflow-rocm==2.18.1) (2.17.2)
Requirement already satisfied: mdurl~=0.1 in /usr/lib/python3/dist-packages (from markdown-it-py>=2.2.0->rich->keras>=3.5.0->tensorflow-rocm==2.18.1) (0.1.2)
Downloading tensorboard-2.18.0-py3-none-any.whl (5.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.5/5.5 MB 41.4 MB/s eta 0:00:00
Installing collected packages: tensorboard, tensorflow-rocm
  Attempting uninstall: tensorboard
    Found existing installation: tensorboard 2.17.1
    Uninstalling tensorboard-2.17.1:
      Successfully uninstalled tensorboard-2.17.1
  Attempting uninstall: tensorflow-rocm
    Found existing installation: tensorflow-rocm 2.17.0
    Uninstalling tensorflow-rocm-2.17.0:
      Successfully uninstalled tensorflow-rocm-2.17.0
Successfully installed tensorboard-2.18.0 tensorflow-rocm-2.18.1
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

$ python3 -c 'import tensorflow' 2> /dev/null && echo ‘Success’ || echo ‘Failure’

‘Success’

$ python3 tensortest.py 

2025-05-06 01:41:13.642415: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
TensorFlow version: 2.18.1
/usr/local/lib/python3.12/dist-packages/keras/src/layers/reshaping/flatten.py:37: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
  super().__init__(**kwargs)
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1746475877.489612    5852 gpu_device.cc:2022] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 15106 MB memory:  -> device: 0, name: Radeon RX 7900 GRE, pci bus id: 0000:03:00.0
I0000 00:00:1746475877.504960    5852 gpu_device.cc:2022] Created device /job:localhost/replica:0/task:0/device:GPU:1 with 7456 MB memory:  -> device: 1, name: Radeon RX Vega, pci bus id: 0000:19:00.0
Epoch 1/5
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1746475878.897992    5926 service.cc:148] XLA service 0x7cf9f4003db0 initialized for platform ROCM (this does not guarantee that XLA will be used). Devices:
I0000 00:00:1746475878.898011    5926 service.cc:156]   StreamExecutor device (0): Radeon RX 7900 GRE, AMDGPU ISA version: gfx1100
I0000 00:00:1746475878.898016    5926 service.cc:156]   StreamExecutor device (1): Radeon RX Vega, AMDGPU ISA version: gfx900:xnack-
2025-05-06 01:41:18.906567: I tensorflow/compiler/mlir/tensorflow/utils/dump_mlir_util.cc:268] disabling MLIR crash reproducer, set env var `MLIR_CRASH_REPRODUCER_DIRECTORY` to enable.
I0000 00:00:1746475880.906830    5926 device_compiler.h:188] Compiled cluster using XLA!  This line is logged at most once for the lifetime of the process.
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 5s 1ms/step - accuracy: 0.8591 - loss: 0.4813    
Epoch 2/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 2s 1ms/step - accuracy: 0.9549 - loss: 0.1534 
Epoch 3/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 2s 1ms/step - accuracy: 0.9667 - loss: 0.1096 
Epoch 4/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 2s 1ms/step - accuracy: 0.9725 - loss: 0.0893 
Epoch 5/5
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 2s 1ms/step - accuracy: 0.9755 - loss: 0.0784 
313/313 - 1s - 5ms/step - accuracy: 0.9763 - loss: 0.0749
```

Much appreciated. This matter has been lingering for more than a month. Thanks for the time and effort you expended providing resolution for this problem. 


---

### 评论 #31 — schung-amd (2025-05-05T20:24:50Z)

Great, glad this worked for you. If you run into further related issues feel free to comment here or open a new issue.

---

### 评论 #32 — rabdulatipoff (2025-10-12T22:17:34Z)

Experiencing this issue with gfx1100, tensorflow-rocm 2.19.0 and ROCm 7.0.2, back then the upgrade to 6.4 also didn't work -- what else can I try out here?

---

### 评论 #33 — schung-amd (2025-10-20T14:48:12Z)

@rabdulatipoff What OS (and kernel version if a Linux flavor)? I'll try to repro and check it out.

---

### 评论 #34 — rabdulatipoff (2025-11-01T11:21:14Z)

> [@rabdulatipoff](https://github.com/rabdulatipoff) What OS (and kernel version if a Linux flavor)? I'll try to repro and check it out.

OS is KDE neon (Ubuntu 24.04), kernel is 6.8.0-51-lowlatency

---
