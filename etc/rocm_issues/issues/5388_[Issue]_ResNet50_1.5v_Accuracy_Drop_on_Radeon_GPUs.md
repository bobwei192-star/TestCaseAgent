# [Issue]: ResNet50 1.5v Accuracy Drop on Radeon GPUs

> **Issue #5388**
> **状态**: open
> **创建时间**: 2025-09-18T20:30:32Z
> **更新时间**: 2025-10-14T13:58:38Z
> **作者**: catan2001
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5388

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- adityas-amd

## 描述

### Problem Description

# ResNet 50 1.5 Accuracy drop on Radeon 
When running the **MLPerf Inference** benchmark (**ResNet50**, **ONNX Runtime**, **reference implementation**) on several AMD GPUs (**gfx1031**/RX 6700XT, **gfx1100**/RX 7900XT/7900XTX, **gfx1201** / RX 9070XT), I have observed a **large drop in accuracy** (~57.9% - ~58.1%) compared to CPU baseline (~76.456%). The test was the accuracy run  no modifications made to the benchmark. 

The model used is **ResNet50-v1.5**, which is provided by the MLCommons/MLPerf Inference reference implementation. You can find it listed under *Supported Models* in the [MLPerf Inference repository (vision/classification_and_detection)](https://github.com/mlcommons/inference/tree/master/vision/classification_and_detection#supported-models).

## Results CPU:

### SingleStream
```bash
TestScenario.SingleStream qps=3984.50, mean=0.0153, time=12.549, acc=76.456%, queries=50000, tiles=50.0:0.0147,80.0:0.0149,90.0:0.0152,95.0:0.0165,99.0:0.0377,99.9:0.0537
```

### MultiStream
```bash
TestScenario.MultiStream qps=1128.31, mean=0.0548, time=5.539, acc=76.456%, queries=6250, tiles=50.0:0.0505,80.0:0.0513,90.0:0.0563,95.0:0.0917,99.0:0.1213,99.9:0.2381
```

## Results GPU (RX 7900XTX)
I left the SingleStream result on RX 7900XTX here just for the sake of visibility. The rest of the results can be found in attached files.

```json
{
    "TestScenario.SingleStream": {
        "accuracy": 58.096,
        "count": 50000,
        "good_items": 29048,
        "mean": 0.003753480935096741,
        "percentiles": {
            "50.0": 0.003449678421020508,
            "80.0": 0.003551959991455078,
            "90.0": 0.0036323308944702145,
            "95.0": 0.00372314453125,
            "99.0": 0.012017512321472173,
            "99.9": 0.059852007150654155
        },
        "qps": 16459.316804992344,
        "took": 3.0377931594848633,
        "total_items": 50000
    },
    "args": {
        "accuracy": true,
        "audit_conf": "audit.config",
        "backend": "onnxruntime",
        "cache": 0,
        "cache_dir": null,
        "count": null,
        "data_format": null,
        "dataset": "imagenet",
        "dataset_list": null,
        "dataset_path": "/dataset/imagenet/",
        "debug": false,
        "device": "rocm",
        "find_peak_performance": false,
        "inputs": null,
        "max_batchsize": 32,
        "max_latency": null,
        "model": "/model/resnet50_v1.onnx",
        "model_name": "resnet50",
        "output": "/root/inference/vision/classification_and_detection/results/GFX1100XTX/edge/SingleStream/accuracy/",
        "outputs": null,
        "performance_sample_count": null,
        "preprocessed_dir": null,
        "profile": null,
        "qps": null,
        "samples_per_query": 8,
        "scenario": "SingleStream",
        "threads": 24,
        "time": null,
        "use_preprocessed_dataset": false,
        "user_conf": "/root/inference/vision/classification_and_detection/user_gfx1100xtx.conf"
    },
    "cmdline": "Namespace(dataset='imagenet', dataset_path='/dataset/imagenet/', dataset_list=None, data_format=None, profile=None, scenario='SingleStream', max_batchsize=32, model='/model/resnet50_v1.onnx', output='/root/inference/vision/classification_and_detection/results/GFX1100XTX/edge/SingleStream/accuracy/', inputs=None, outputs=None, backend='onnxruntime', device='rocm', model_name='resnet50', threads=24, qps=None, cache=0, cache_dir=None, preprocessed_dir=None, use_preprocessed_dataset=False, accuracy=True, find_peak_performance=False, debug=False, user_conf='/root/inference/vision/classification_and_detection/user_gfx1100xtx.conf', audit_conf='audit.config', time=None, count=None, performance_sample_count=None, max_latency=None, samples_per_query=8)",
    "runtime": "onnxruntime",
    "time": 1756742544,
    "version": "1.21.0"
}
```
### GPU Results:

- [RX6700XT_SingleStream_accuracy.json](https://github.com/user-attachments/files/22414377/results.json)
- [RX6700XT_MultiStream_accuracy.json](https://github.com/user-attachments/files/22414399/results.json)
- [RX7900XT_SingleStream_accuracy.json](https://github.com/user-attachments/files/22414404/results.json)
- [RX7900XT_MultiStream_accuracy.json](https://github.com/user-attachments/files/22414417/results.json)
- [RX7900XTX_SingleStream_accuracy.json](https://github.com/user-attachments/files/22414429/results.json)
- [RX7900XTX_MultiStream_accuracy.json](https://github.com/user-attachments/files/22414437/results.json)
- [RX9070XT_SingleStream_accuracy.json](https://github.com/user-attachments/files/22414448/results.json)
- [RX9070XT_MultiStream_accuracy.json](https://github.com/user-attachments/files/22414452/results.json)

### Operating System

Ubuntu 24.04.2 LTS

### CPU

2x AMD EPYC 7453​

### GPU

AMD Radeon RX 6700XT, AMD Radeon RX 7900XT, AMD Radeon RX 7900XTX, AMD Radeon RX 9070XT

### ROCm Version

 ROCm version: 6.4.1 | amdgpu version: 6.12.12 

### ROCm Component

MIOpen

### Steps to Reproduce

## Steps to reproduce
I used `rocm/dev-ubuntu-24.04:6.4.1-complete` Docker Image. There are two ways you can reproduce this issue. 

### Through MLCFlow

You can use **MLCFlow** for a very simple, automated setup: it will pre-download the model and test data and configure the benchmark for you. Before running MLCFlow, install it and follow the ResNet-50 guide:

- Install MLCFlow: https://docs.mlcommons.org/inference/install/
- Run the ResNet-50 benchmark: https://docs.mlcommons.org/inference/benchmarks/image_classification/resnet50/

**Important:** to run MLPerf with ROCm on AMD GPUs, edit `backend_onnxruntime.py` in the downloaded `vision/classification_and_detection/python` folder and make sure the ONNX Runtime session is configured to use the ROCm execution provider (for example, by passing `providers=['ROCMExecutionProvider']` when creating the `InferenceSession`).


### GitHub Repo

You can use their official reference implementation on GitHub to do similar thing. The steps to reproduce this are a bit harder since you will have to thinker a bit:

- Clone the repo: https://github.com/mlcommons/inference/tree/master
- Download Model: https://github.com/mlcommons/inference/tree/master/vision/classification_and_detection#download-model-through-mlcflow-automation
- Run the ResNet-50 benchmark: https://github.com/mlcommons/inference/tree/master/vision/classification_and_detection#running-the-benchmark

**Important:** to run MLPerf with ROCm on AMD GPUs, edit `backend_onnxruntime.py` in the downloaded `vision/classification_and_detection/python` folder and make sure the ONNX Runtime session is configured to use the ROCm execution provider (for example, by passing `providers=['ROCMExecutionProvider']` when creating the `InferenceSession`).

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.12.12 is loaded
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
  Name:                    AMD EPYC 7453 28-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7453 28-Core Processor    
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
  Max Clock Freq. (MHz):   2750                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            56                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131879616(0x7dc52c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131879616(0x7dc52c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131879616(0x7dc52c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131879616(0x7dc52c0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 7453 28-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7453 28-Core Processor    
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
  Max Clock Freq. (MHz):   2750                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            56                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    132048500(0x7dee674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    132048500(0x7dee674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    132048500(0x7dee674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    132048500(0x7dee674) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    
  Marketing Name:          Radeon RX 7900 XTX                 
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
    L2:                      6144(0x1800) KB                    
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2482                               
  BDFID:                   25344                              
  Internal Node ID:        2                                  
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
  Packet Processor uCode:: 542                                
  SDMA engine uCode::      24                                 
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
Agent 4                  
*******                  
  Name:                    gfx1201                            
  Uuid:                    
  Marketing Name:          AMD Radeon RX 9070 XT              
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
    L2:                      8192(0x2000) KB                    
    L3:                      65536(0x10000) KB                  
  Chip ID:                 30032(0x7550)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          256(0x100)                         
  Max Clock Freq. (MHz):   2400                               
  BDFID:                   49920                              
  Internal Node ID:        3                                  
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
  Packet Processor uCode:: 1012                               
  SDMA engine uCode::      838                                
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
Agent 5                  
*******                  
  Name:                    gfx1031                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 6700 XT              
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
    L2:                      3072(0xc00) KB                     
    L3:                      98304(0x18000) KB                  
  Chip ID:                 29663(0x73df)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2855                               
  BDFID:                   41728                              
  Internal Node ID:        4                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 122                                
  SDMA engine uCode::      80                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12566528(0xbfc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    12566528(0xbfc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1031         
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
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic 
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

## 评论 (3 条)

### 评论 #1 — adityas-amd (2025-10-10T21:44:02Z)

@catan2001 Strange, I can’t fully reproduce yet because the MLC automation pipeline keeps trying to install an old onnxruntime-training (ROCm56) wheel that doesn’t exist for Python 3.12, which causes the run to fail. Could you share your exact Python version and how you launched the run?  I ran this: ```mlcr run-mlperf,inference,_find-performance,_full,_r5.1-dev \
   --model=resnet50 \
   --implementation=reference \
   --framework=onnxruntime \
   --category=edge \
   --scenario=Offline \
   --execution_mode=test \
   --device=rocm  \
   --quiet \
   --test_query_count=1000 --rerun```

<img width="652" height="273" alt="Image" src="https://github.com/user-attachments/assets/f6259d01-b064-40bd-bc63-39a5c6c60364" />

---

### 评论 #2 — catan2001 (2025-10-13T15:28:42Z)

@adityas-amd 

Thank you for taking the time to look into this issue! And sorry for not replying sooner, I've been caught up with a few other things the past few days.

I also tried using mlcr, but it failed multiple times for different reasons, so I eventually gave up on their automation and wrote my own scripts for handling various workloads. Interestingly, a few months ago I was able to use mlcr without any issues, so it definitely seems like something on their end has changed.

I'll send you the files and the steps to reproduce everything tomorrow.

---

### 评论 #3 — catan2001 (2025-10-14T13:58:21Z)

@adityas-amd After rereading my reply, I realized it might have caused some confusion. Just to clarify I was able to run benchmarks without any issues related to `mlcr` itself, but I was still encountering accuracy problems at the time. 

Here's the general setup I used when working with MLPerf Inference. The script `setup_resnet50_mlperf.sh`  automates the setup. To streamline the process, you can use the `run_multiple_benchmarks.sh` script, which automates the execution of both performance and accuracy benchmarks across multiple GPUs in parallel.

You can also use the `run_benchmark.sh` script to run a single benchmark. By adding the `--mode accuracy` argument, the script will execute the benchmark in accuracy mode. Please make sure to have all files inside of the `/inference/vision/classification_and_detection/` after you run setup script.

- [README.md](https://github.com/user-attachments/files/22906157/README.md)
- [run_benchmark.sh](https://github.com/user-attachments/files/22906156/run_benchmark.sh)
- [setup_resnet50_mlperf.sh](https://github.com/user-attachments/files/22906155/setup_resnet50_mlperf.sh)
- [run_multiple_benchmarks.sh](https://github.com/user-attachments/files/22906158/run_multiple_benchmarks.sh)
- [configuration_files.zip](https://github.com/user-attachments/files/22906194/configuration_files.zip)


---
