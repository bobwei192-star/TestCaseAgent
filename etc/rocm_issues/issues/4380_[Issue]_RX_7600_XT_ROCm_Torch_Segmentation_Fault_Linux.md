# [Issue]: RX 7600 XT ROCm Torch Segmentation Fault Linux

> **Issue #4380**
> **状态**: closed
> **创建时间**: 2025-02-15T02:02:25Z
> **更新时间**: 2026-01-16T14:33:30Z
> **关闭时间**: 2025-03-02T22:54:13Z
> **作者**: isaaclepes
> **标签**: Under Investigation, ROCm 6.2.1
> **URL**: https://github.com/ROCm/ROCm/issues/4380

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.1** (颜色: #ededed)

## 描述

### Problem Description

Whenever I attempt to use my GPU with pytorch, it produces a Segmentation Fault.  From the information I could find online, it seemed this was the best place to ask for guidance.

### Operating System

Nobara Linux 41 6.13.2-200

### CPU

AMD Ryzen 5 5500

### GPU

AMD RX 6700 XT

### ROCm Version

ROCm 6.2.1

### ROCm Component

_No response_

### Steps to Reproduce

```python
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.randn(1000, 1000).to(device)
y = torch.randn(1000, 1000).to(device)
z = x @ y
print("Computation successful on:", device)
```
Environment Variables:
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:512
export HIP_VISIBLE_DEVICES=0
export ROCR_VISIBLE_DEVICES=0
export AMD_SERIALIZE_KERNEL=3 
export AMD_LOG_LEVEL=4
export PYTORCH_HIP_LAUNCH_BLOCKING=1 

Result:
python /opt/ComfyUI/torchtensortest.py
:3:rocdevice.cpp            :468 : 95707883831 us: [pid:2117053 tid:0x7ca06301e740] Initializing HSA stack.
:3:rocdevice.cpp            :528 : 95708205307 us: [pid:2117053 tid:0x7ca06301e740] Enumerated GPU agents = 1
:3:rocdevice.cpp            :234 : 95708205346 us: [pid:2117053 tid:0x7ca06301e740] Numa selects cpu agent[0]=0x64f8b9e88fd0(fine=0x64f8bd2f6e30,coarse=0x64f8b6927f00) for gpu agent=0x64f8b695fc80 CPU<->GPU XGMI=0
:3:comgrctx.cpp             :33  : 95708205356 us: [pid:2117053 tid:0x7ca06301e740] Loading COMGR library.
:3:rocdevice.cpp            :1772: 95708205576 us: [pid:2117053 tid:0x7ca06301e740] Gfx Major/Minor/Stepping: 11/0/0
:3:rocdevice.cpp            :1774: 95708205582 us: [pid:2117053 tid:0x7ca06301e740] HMM support: 1, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1776: 95708205586 us: [pid:2117053 tid:0x7ca06301e740] Max SDMA Read Mask: 0x3, Max SDMA Write Mask: 0x3
:4:rocdevice.cpp            :2169: 95708205884 us: [pid:2117053 tid:0x7ca06301e740] Allocate hsa host memory 0x7c9d13200000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2169: 95708207333 us: [pid:2117053 tid:0x7ca06301e740] Allocate hsa host memory 0x7c9d13000000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2169: 95708208980 us: [pid:2117053 tid:0x7ca06301e740] Allocate hsa host memory 0x7c9d12a00000, size 0x400000, numa_node = 0
:4:rocdevice.cpp            :2169: 95708209154 us: [pid:2117053 tid:0x7ca06301e740] Allocate hsa host memory 0x7ca053e71000, size 0x38, numa_node = 0
:4:runtime.cpp              :83  : 95708209272 us: [pid:2117053 tid:0x7ca06301e740] init
:3:hip_context.cpp          :49  : 95708209279 us: [pid:2117053 tid:0x7ca06301e740] Direct Dispatch: 1
:1:hip_fatbin.cpp           :255 : 95708404069 us: [pid:2117053 tid:0x7ca06301e740] Cannot find CO in the bundle /usr/local/lib64/python3.13/site-packages/torch/lib/libhipblaslt.so for ISA: amdgcn-amd-amdhsa--gfx1100
:1:hip_fatbin.cpp           :109 : 95708404081 us: [pid:2117053 tid:0x7ca06301e740] Missing CO for these ISAs - 
:1:hip_fatbin.cpp           :112 : 95708404085 us: [pid:2117053 tid:0x7ca06301e740]      amdgcn-amd-amdhsa--gfx1100
:3:hip_platform.cpp         :703 : 95708404094 us: [pid:2117053 tid:0x7ca06301e740] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
:1:hip_fatbin.cpp           :255 : 95708416541 us: [pid:2117053 tid:0x7ca06301e740] Cannot find CO in the bundle /usr/local/lib64/python3.13/site-packages/torch/lib/libhipblaslt.so for ISA: amdgcn-amd-amdhsa--gfx1100
:1:hip_fatbin.cpp           :109 : 95708416551 us: [pid:2117053 tid:0x7ca06301e740] Missing CO for these ISAs - 
:1:hip_fatbin.cpp           :112 : 95708416554 us: [pid:2117053 tid:0x7ca06301e740]      amdgcn-amd-amdhsa--gfx1100
:3:hip_platform.cpp         :703 : 95708416560 us: [pid:2117053 tid:0x7ca06301e740] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
:1:hip_fatbin.cpp           :255 : 95708417569 us: [pid:2117053 tid:0x7ca06301e740] Cannot find CO in the bundle /usr/local/lib64/python3.13/site-packages/torch/lib/libhipblaslt.so for ISA: amdgcn-amd-amdhsa--gfx1100
:1:hip_fatbin.cpp           :109 : 95708417574 us: [pid:2117053 tid:0x7ca06301e740] Missing CO for these ISAs - 
:1:hip_fatbin.cpp           :112 : 95708417576 us: [pid:2117053 tid:0x7ca06301e740]      amdgcn-amd-amdhsa--gfx1100
:3:hip_platform.cpp         :703 : 95708417580 us: [pid:2117053 tid:0x7ca06301e740] init: Returned hipErrorNoBinaryForGpu : continue parsing remaining modules
:3:hip_device_runtime.cpp   :638 : 95708470502 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDeviceCount ( 0x7ffc61b146ac ) 
:3:hip_device_runtime.cpp   :640 : 95708470518 us: [pid:2117053 tid:0x7ca06301e740] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :638 : 95708475286 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDeviceCount ( 0x7ffc61b140b0 ) 
:3:hip_device_runtime.cpp   :640 : 95708475294 us: [pid:2117053 tid:0x7ca06301e740] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :638 : 95708475311 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDeviceCount ( 0x7c9f8fda56bc ) 
:3:hip_device_runtime.cpp   :640 : 95708475317 us: [pid:2117053 tid:0x7ca06301e740] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device.cpp           :471 : 95708475323 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevicePropertiesR0600 ( 0x7ffc61b13ba8, 0 ) 
:3:hip_device.cpp           :473 : 95708475327 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevicePropertiesR0600: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708475344 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b13c8c ) 
:3:hip_device_runtime.cpp   :631 : 95708475348 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :638 : 95708475352 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDeviceCount ( 0x7ffc61b13bdc ) 
:3:hip_device_runtime.cpp   :640 : 95708475356 us: [pid:2117053 tid:0x7ca06301e740] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_context.cpp          :340 : 95708475571 us: [pid:2117053 tid:0x7ca06301e740]  hipDevicePrimaryCtxGetState ( 0, 0x7ffc61b13ca8, 0x7ffc61b13cac ) 
:3:hip_context.cpp          :354 : 95708475578 us: [pid:2117053 tid:0x7ca06301e740] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708475583 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b13cdc ) 
:3:hip_device_runtime.cpp   :631 : 95708475587 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_context.cpp          :340 : 95708475592 us: [pid:2117053 tid:0x7ca06301e740]  hipDevicePrimaryCtxGetState ( 0, 0x7ffc61b13cf8, 0x7ffc61b13cfc ) 
:3:hip_context.cpp          :354 : 95708475595 us: [pid:2117053 tid:0x7ca06301e740] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708475604 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b13c7c ) 
:3:hip_device_runtime.cpp   :631 : 95708475608 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_context.cpp          :340 : 95708475612 us: [pid:2117053 tid:0x7ca06301e740]  hipDevicePrimaryCtxGetState ( 0, 0x7ffc61b13c98, 0x7ffc61b13c9c ) 
:3:hip_context.cpp          :354 : 95708475617 us: [pid:2117053 tid:0x7ca06301e740] hipDevicePrimaryCtxGetState: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708476119 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b14364 ) 
:3:hip_device_runtime.cpp   :631 : 95708476126 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708476185 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b135a4 ) 
:3:hip_device_runtime.cpp   :631 : 95708476190 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708476195 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b13464 ) 
:3:hip_device_runtime.cpp   :631 : 95708476199 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708476210 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b1327c ) 
:3:hip_device_runtime.cpp   :631 : 95708476214 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_stream.cpp           :404 : 95708476223 us: [pid:2117053 tid:0x7ca06301e740]  hipDeviceGetStreamPriorityRange ( 0x7ffc61b13230, 0x7ffc61b13250 ) 
:3:hip_stream.cpp           :412 : 95708476228 us: [pid:2117053 tid:0x7ca06301e740] hipDeviceGetStreamPriorityRange: Returned hipSuccess : 
:3:hip_error.cpp            :36  : 95708476240 us: [pid:2117053 tid:0x7ca06301e740]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :623 : 95708476245 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b12b1c ) 
:3:hip_device_runtime.cpp   :631 : 95708476248 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_graph.cpp            :826 : 95708476257 us: [pid:2117053 tid:0x7ca06301e740]  hipStreamIsCapturing ( stream:<null>, 0x7ffc61b12d90 ) 
:3:hip_graph.cpp            :827 : 95708476263 us: [pid:2117053 tid:0x7ca06301e740] hipStreamIsCapturing: Returned hipSuccess : 
:3:hip_memory.cpp           :599 : 95708476271 us: [pid:2117053 tid:0x7ca06301e740]  hipMalloc ( 0x7ffc61b12e80, 20971520 ) 
:4:rocdevice.cpp            :2310: 95708476552 us: [pid:2117053 tid:0x7ca06301e740] Allocate hsa device memory 0x7c9d11200000, size 0x1400000
:3:rocdevice.cpp            :2349: 95708476558 us: [pid:2117053 tid:0x7ca06301e740] device=0x64f8bd30b450, freeMem_ = 0x3fdc00000
:3:hip_memory.cpp           :601 : 95708476566 us: [pid:2117053 tid:0x7ca06301e740] hipMalloc: Returned hipSuccess : 0x7c9d11200000: duration: 295 us
:3:hip_device_runtime.cpp   :653 : 95708476581 us: [pid:2117053 tid:0x7ca06301e740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :657 : 95708476585 us: [pid:2117053 tid:0x7ca06301e740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :653 : 95708476589 us: [pid:2117053 tid:0x7ca06301e740]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :657 : 95708476592 us: [pid:2117053 tid:0x7ca06301e740] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708476636 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b134d4 ) 
:3:hip_device_runtime.cpp   :631 : 95708476640 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :623 : 95708476644 us: [pid:2117053 tid:0x7ca06301e740]  hipGetDevice ( 0x7ffc61b132ec ) 
:3:hip_device_runtime.cpp   :631 : 95708476649 us: [pid:2117053 tid:0x7ca06301e740] hipGetDevice: Returned hipSuccess : 
:3:hip_memory.cpp           :685 : 95708476659 us: [pid:2117053 tid:0x7ca06301e740]  hipMemcpyWithStream ( 0x7c9d11200000, 0x7c9d1262f040, 4000000, hipMemcpyHostToDevice, stream:<null> ) 
:3:rocdevice.cpp            :2925: 95708476672 us: [pid:2117053 tid:0x7ca06301e740] number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:4:command.cpp              :347 : 95708513211 us: [pid:2117053 tid:0x7ca06301e740] Command (CopyHostToDevice) enqueued: 0x64f8bd6213e0
Segmentation fault (core dumped)

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
  Name:                    AMD Ryzen 5 5500                   
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5500                   
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
  Max Clock Freq. (MHz):   4267                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65622308(0x3e95124) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65622308(0x3e95124) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65622308(0x3e95124) KB             
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
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 7600 XT              
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2539                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
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
  Packet Processor uCode:: 462                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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

```python
import torch
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Device Count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("Current Device:", torch.cuda.current_device())
```
Output:
```
CUDA Available: True
CUDA Device Count: 1
GPU Name: AMD Radeon RX 7600 XT
Current Device: 0
```

```python
import torch
device = "cpu"  # Force CPU mode
x = torch.randn(1000, 1000).to(device)
y = torch.randn(1000, 1000).to(device)
z = x @ y
print("Computation successful on:", device)
```
Output:
` Computation successful on: cpu `

`sudo dnf list --installed | grep rocm`
Output:

![Image](https://github.com/user-attachments/assets/a6640ecd-7b12-4249-b137-97d1bd056b84)

Other Notes:

Removed Mesa clinfo package
Same result with 6.12.11-204 kernel

---

## 评论 (11 条)

### 评论 #1 — isaaclepes (2025-02-25T21:56:37Z)

Checking in to prevent the issue auto-closing.

---

### 评论 #2 — teleprint-me (2025-03-01T23:54:55Z)

What happens if you set the HSA flag as a prefix to the interpreter? The GFX version for 6700 XT is 1100, but the revision could differ depending on the environment.

You can validate this with `rocminfo` and `rocm-smi`.

```sh
18:38:34 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ rocminfo --support | grep -i gfx      
  Name:                    gfx1102                            
      Name:                    amdgcn-amd-amdhsa--gfx1102         
18:42:26 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ rocm-smi --showhw               


======================================= ROCm System Management Interface =======================================
============================================ Concise Hardware Info =============================================
GPU  NODE  DID     GUID   GFX VER   GFX RAS  SDMA RAS  UMC RAS  VBIOS              BUS           PARTITION ID  
0    1     0x7480  3799   gfx11002  N/A      N/A       N/A      113-APM7076OC-100  0000:03:00.0  0             
1    2     0x164e  39463  gfx1036   N/A      N/A       N/A      102-RAPHAEL-008    0000:12:00.0  0             
================================================================================================================
============================================= End of ROCm SMI Log ==============================================
```

If the Environment Variables are not configured properly, you can get a segfault. A common one required is `HSA_OVERRIDE_GFX_VERSION`.

```sh
18:42:30 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ HSA_OVERRIDE_GFX_VERSION=11.0.0 python
Python 3.12.8 (main, Dec 24 2024, 18:57:29) [GCC 14.2.1 20240910] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> x = torch.randn(3, 3).cuda()
[1]    22575 segmentation fault (core dumped)  HSA_OVERRIDE_GFX_VERSION=11.0.0 python
```

But aligning the versions can somewhat resolve this.

```sh
18:43:40 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ HSA_OVERRIDE_GFX_VERSION=11.0.2 python
Python 3.12.8 (main, Dec 24 2024, 18:57:29) [GCC 14.2.1 20240910] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> x = torch.randn(3, 3).cuda()
>>> x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor.py", line 568, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 704, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 621, in _str_intern
    tensor_str = _tensor_str(self, indent)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 353, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 146, in __init__
    tensor_view, torch.isfinite(tensor_view) & tensor_view.ne(0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

>>> 
```

I'm currently stuck here, but I'm running into a similar issue with the same card. I had everything configured and working about a week or two ago and I went back to work on a project and I've been running into this issue today. Been working on it over the past few hours attempting to isolate it.

```sh
18:47:13 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ pacman -Ss rocm | grep installed
extra/hipblas 6.2.4-1 [installed]
extra/hsa-rocr 6.2.1-1 [installed]
extra/rccl 6.2.4-1 [installed]
extra/rocalution 6.2.4-1 [installed]
extra/rocblas 6.2.4-1 [installed]
extra/rocfft 6.2.4-1 [installed]
extra/rocm-clang-ocl 6.1.2-1 [installed]
extra/rocm-cmake 6.2.4-1 [installed]
extra/rocm-core 6.2.4-2 [installed]
extra/rocm-device-libs 6.2.4-1 [installed]
extra/rocm-hip-libraries 6.2.2-1 [installed]
extra/rocm-hip-runtime 6.2.2-1 [installed]
extra/rocm-hip-sdk 6.2.2-1 [installed]
extra/rocm-language-runtime 6.2.2-1 [installed]
extra/rocm-llvm 6.2.4-1 [installed]
extra/rocm-ml-libraries 6.2.2-1 [installed]
extra/rocm-opencl-runtime 6.2.4-1 [installed]
extra/rocm-smi-lib 6.2.4-1 [installed]
extra/rocminfo 6.2.4-1 [installed]
extra/rocrand 6.2.4-1 [installed]
extra/rocsolver 6.2.4-1 [installed]
extra/rocsparse 6.2.4-1 [installed]
extra/rocthrust 6.2.4-1 [installed]
extra/roctracer 6.2.4-1 [installed]
```

Most of these probably aren't required, but I just never got around to removing the ones I didn't need. Python requires 3.12.8 since PyTorch is still in nightly for 3.13.x. PyTorch 2.6.0 requires ROCm 6.2.4.

```sh
18:50:03 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ python -V     
Python 3.12.8
18:50:54 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ pip -V        
pip 25.0.1 from /mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/pip (python 3.12)
18:50:58 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ pip show torch
Name: torch
Version: 2.6.0+rocm6.2.4
Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
Home-page: https://pytorch.org/
Author: PyTorch Team
Author-email: packages@pytorch.org
License: BSD-3-Clause
Location: /mnt/valerie/public/mini/.venv/lib/python3.12/site-packages
Requires: filelock, fsspec, jinja2, networkx, pytorch-triton-rocm, setuptools, sympy, typing-extensions
Required-by: 
```

I already set most of my variables.

```sh
18:51:04 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ printenv | grep -i rocm  
ROCM_PATH=/opt/rocm
LD_LIBRARY_PATH=/opt/rocm/lib:
LIBRARY_PATH=/opt/rocm/lib:
C_INCLUDE_PATH=/opt/rocm/include:
CPLUS_INCLUDE_PATH=/opt/rocm/include:
TRITON_USE_ROCM=1
PYTORCH_ROCM_ARCH=gfx11002
ROCM_HOME=/opt/rocm
```

It's possible I'm missing some configuration requirement or something more subtle is occurring that I'm currently not comprehending.

```sh
19:02:17 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ echo $PYTORCH_ROCM_ARCH $HSA_OVERRIDE_GFX_VERSION 
gfx1102 11.0.2
```

I tried enabling the serialization flag, but not sure if this is strictly compile time dependent or not.

```sh
19:03:19 | /mnt/valerie/public/mini
(.venv) git:(main | Δ) λ AMD_SERIALIZE_KERNEL=1 python                    
Python 3.12.8 (main, Dec 24 2024, 18:57:29) [GCC 14.2.1 20240910] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> x = torch.randn(3, 3).cuda()
>>> x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor.py", line 568, in __repr__
    return torch._tensor_str._str(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 704, in _str
    return _str_intern(self, tensor_contents=tensor_contents)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 621, in _str_intern
    tensor_str = _tensor_str(self, indent)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 353, in _tensor_str
    formatter = _Formatter(get_summarized_data(self) if summarize else self)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/valerie/public/mini/.venv/lib/python3.12/site-packages/torch/_tensor_str.py", line 146, in __init__
    tensor_view, torch.isfinite(tensor_view) & tensor_view.ne(0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: HIP error: invalid device function
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

>>> 
```

But it's the same issue. I did attempt a `coredumptctl gdb`, but I'm not familiar enough with the underlying code to make sense of it. Another user [reported a similar issue](https://bugs.archlinux.org/task/78306) and the output was similar as well.

<details rocminfo>
<summary>GPU Details</summary>
<br>

```sh
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 7600 XT              
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
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2539                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
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
  Packet Processor uCode:: 522                                
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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

</details>

---

### 评论 #3 — isaaclepes (2025-03-02T04:33:06Z)

the rocminfo output was in the original post, but here's the relevant part:

![Image](https://github.com/user-attachments/assets/ce5cf5ab-f33e-48f7-b8d6-5ec4912d7676)

Here's `rocm-smi --support | grep gfx`

![Image](https://github.com/user-attachments/assets/1eecb9d8-8241-4d65-9d58-5ff0869f0a92)

and just rocm-smi:

![Image](https://github.com/user-attachments/assets/ab353ebc-0fc0-49cb-bc8c-71ea2d2f6e32)

```
>printenv | grep HSA_OVERRIDE
HSA_OVERRIDE_GFX_VERSION=11.0.0
```
```
> echo $PYTORCH_ROCM_ARCH $HSA_OVERRIDE_GFX_VERSION
11.0.0
```

---

### 评论 #4 — teleprint-me (2025-03-02T04:55:49Z)

`$PYTORCH_ROCM_ARCH` isn't printing anything which means it isn't set.

I think some of these settings might work for you. Not sure.

```vim
# Paths
PATH_ROCM="/opt/rocm:/opt/rocm/lib:/opt/rocm/share:/opt/rocm/bin" # Only enable if ROCM is installed

# Export Environment Variables for ROCm and PyTorch
export PATH="${PATH_ROCM}:$PATH"
export LD_LIBRARY_PATH="/opt/rocm/lib:$LD_LIBRARY_PATH"
export LIBRARY_PATH="/opt/rocm/lib:$LIBRARY_PATH"
export C_INCLUDE_PATH="/opt/rocm/include:$C_INCLUDE_PATH"
export CPLUS_INCLUDE_PATH="/opt/rocm/include:$CPLUS_INCLUDE_PATH"

# ROCm Device Visibility
export HIP_VISIBLE_DEVICES=0  # Adjust if multiple GPUs
export ROCR_VISIBLE_DEVICES=0
export TRITON_USE_ROCM=1

# ROCm Architecture and Overrides
export AMDGPU_TARGETS="gfx1102"
export HCC_AMDGPU_TARGET="gfx1102"
export PYTORCH_ROCM_ARCH="gfx1102"
export HSA_OVERRIDE_GFX_VERSION="11.0.2" # RDNA3
export ROCM_PATH="/opt/rocm"
export ROCM_HOME="/opt/rocm"

# PyTorch ROCm Memory Management
export PYTORCH_HIP_ALLOC_CONF="expandable_segments:False,garbage_collection_threshold:0.8"

# Optional: Disable hipBLASLt if issues occur
export USE_HIPBLASLT=0
export TORCH_BLAS_PREFER_HIPBLASLT=0

# Optional: Logging for debugging
# export ROCM_LOG_LEVEL=4  # Uncomment for verbose debugging
```

These are my current settings, but you would have to swap out the GFX versions with the ones registered on your system. So, it would be `gfx1100` instead of `gfx1102`.

Your GFX version is aligning with the expected values for [supported API](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html). But our GPUs are not officially supported as far as I can tell? Not sure.

You would need to validate the location for ROCm with `whereis rocm`.

```sh
23:41:10 | ~
  λ whereis rocm               
rocm: /opt/rocm/share/rocm
```

This would differ from system to system. So you would need to adjust this according to your paths.

You can just pop this in your bashrc after a quick litmus test. e.g.

```python
$ AMDGPU_TARGETS="gfx1100" PYTORCH_ROCM_ARCH="gfx1100" HSA_OVERRIDE_GFX_VERSION="11.0.0" TRITON_USE_ROCM=1 python
Python 3.13.2 (main, Feb  5 2025, 08:05:21) [GCC 14.2.1 20250128] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.cuda.is_available())
True
>>> print(torch.cuda.device_count())
1
>>> print(torch.cuda.get_device_name(0))
AMD Radeon RX 7600 XT
>>> 
```

Then see if you can move a tensor to VRAM.

```python
x = torch.randn(3, 3).cuda()
print(x)
```

I'm just trying to see if I can replicate my success on your system to validate one of my current theories I have running since I can't figure out the runtime issue at the moment. I've been at it all evening and still no luck. I'm about to throw in the towel here.

Related Issues:

- https://github.com/ROCm/ROCm/issues/2536
- https://github.com/ROCm/ROCm/issues/4208
- https://github.com/pytorch/pytorch/issues/147626

Related PR:

- https://github.com/pytorch/pytorch/pull/147761

Related Sources:

- https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html
- https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html#architecture-support-compatibility-matrix
- https://rocm.docs.amd.com/en/docs-6.0.2/conceptual/gpu-isolation.html


---

### 评论 #5 — isaaclepes (2025-03-02T20:10:34Z)

Where do you get gfx1102?

I tried to mirror your setup, but I get an error because I don't seem to have that one.

```
> ls /usr/lib64/rocm/
gfx10  gfx11  gfx1100  gfx1103  gfx8  gfx9  gfx90a  gfx942
```



```
rocBLAS error: Cannot read /opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary.dat: No such file or directory for GPU arch : gfx1102
 List of available TensileLibrary Files : 
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx1030.dat"
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx1100.dat"
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx1101.dat"
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx900.dat"
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx906.dat"
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx908.dat"
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx90a.dat"
"/opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages/torch/lib/rocblas/library/TensileLibrary_lazy_gfx942.dat"
Aborted (core dumped)
```

I have rocm 6.2.4 installed, and python 3.12

```
>python -m pip show torch
Name: torch
Version: 2.6.0+rocm6.2.4
Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
Home-page: https://pytorch.org/
Author: PyTorch Team
Author-email: packages@pytorch.org
License: BSD-3-Clause
Location: /opt/ComfyUI/comfyvenv/lib64/python3.12/site-packages
Requires: filelock, fsspec, jinja2, networkx, pytorch-triton-rocm, setuptools, sympy, typing-extensions
Required-by: kornia, spandrel, torchaudio, torchsde, torchvision
```
```
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 7600 XT              
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
...
```
CUDA Available: True
CUDA Device Count: 1
GPU Name: AMD Radeon RX 7600 XT
Current Device: 0


---

### 评论 #6 — isaaclepes (2025-03-02T21:33:39Z)

I installed the latest torch nightly and I got a success with warning testing it.

```
UserWarning: Attempting to use hipBLASLt on an unsupported architecture! Overriding blas backend to hipblas (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:343.)
  z = x @ y
Computation successful on: cuda
```


---

### 评论 #7 — teleprint-me (2025-03-02T21:33:54Z)

You have to adjust the versions according to your systems configuration, otherwise it won't work. My system registers the card as GFX1102 for some reason. It could be the firmware, model, etc.

1. Get the GFX version.

```sh
16:09:10 | ~
  λ rocm_agent_enumerator
gfx000
gfx1102 # my card is registered as gfx1102, but others will vary
gfx1102
```

2. Validate the GFX registered model.

**rocm-smi**: I already know my card is gfx1102, not sure if this display is a bug or not since mine shows gfx11002. They seem to be treated equivalently for me.

```sh
16:10:04 | ~
  λ rocm-smi --showhw | grep -i gfx
GPU  NODE  DID     GUID   GFX VER   GFX RAS  SDMA RAS  UMC RAS  VBIOS              BUS           PARTITION ID  
0    1     0x7480  3799   gfx11002  N/A      N/A       N/A      113-APM7076OC-100  0000:03:00.0  0             
1    2     0x164e  39463  gfx1036   N/A      N/A       N/A      102-RAPHAEL-008    0000:12:00.0  0
```

**rocminfo**: You can do a sanity check with `rocminfo`.

```sh
16:11:27 | ~
  λ rocminfo | grep -i gfx         
  Name:                    gfx1102                            
      Name:                    amdgcn-amd-amdhsa--gfx1102 
```

Once you know the GFX version, you'll know what HSA override is since it's major, minor, revision.

3. Deduce what the `HSA_OVERRIDE_GFX_VERSION` is from the GFX registered model.

My model is 1102, so major is 11, minor is 0, and revision is 2. This gives me `11.0.2` which is what I need to set it to.

```sh
HSA_OVERRIDE_GFX_VERSION="11.0.2" # RDNA 3
```

4. Figure out the root path for the ROCm installation.

```sh
16:15:27 | ~
  λ whereis rocm     
rocm: /opt/rocm/share/rocm
```

The root path here is `/opt/rocm`.

I can deduce the rest by probing the directory structure.

```sh
16:15:29 | ~
  λ ll /opt/rocm    
total 28K
drwxr-xr-x  3 root root 4.0K Jan 30 16:37 amdgcn/
drwxr-xr-x  2 root root 4.0K Jan 30 16:37 bin/
drwxr-xr-x  3 root root 4.0K Jan 30 16:37 hiprand/
drwxr-xr-x 30 root root 4.0K Mar  1 18:37 include/
drwxr-xr-x  9 root root 4.0K Jan 30 20:46 lib/
drwxr-xr-x  3 root root 4.0K Jan 30 16:37 libexec/
lrwxrwxrwx  1 root root   18 Nov 12 10:50 llvm -> /opt/rocm/lib/llvm/
drwxr-xr-x 11 root root 4.0K Jan 30 16:48 share/
```

This tells me that this is the root path for my ROCm installation. So, I deduce the HOME paths from here for `ROCM_HOME` and `ROCM_PATH`. These are required.

5. Figure out where the libraries are and export the shared objects and includes to my environment.

_NOTE: This is pretty straightforward if you know what you're doing, otherwise it's a nightmare simply because it requires a lot of pre-requisite knowledge in how software works in general._

I chose a terrible variable name for this, but didn't want to overthink it, so I ran with it.

```sh
PATH_ROCM="/opt/rocm:/opt/rocm/lib:/opt/rocm/share:/opt/rocm/bin"
```

This only needs to be defined if the installer did not configure it for you. It's usually fairly obvious because `rocminfo` and `rocm-smi` don't work at all and the CLI just complains that it can't find them. So, most Debian based distros shouldn't need to worry about this at all. You can see if it's in your path by inspecting it.

```sh
echo $PATH | grep -i rocm
```

So if the binaries, libraries, and shared objects are exported properly, they should show up here. If not, you'll need to include the ones that are missing manually.

6. Tell PyTorch what model your GPU is using `PYTORCH_ROCM_ARCH`.

PyTorch uses registered information to handle the backend. This is determined at both compile and runtime.

_If your card is not supported, it's because it wasn't compiled with that GPU in mind. This is actually what was causing the runtime error I was experiencing earlier, but I was able to resolve it._

```sh
PYTORCH_ROCM_ARCH=gfx1102 # Make sure this matches with the output from your system
```

7. Validate that PyTorch supports your card.

_According to a collaborator, this is not intended for this, and is for relevant metadata instead, but it's still useful and accurate enough that actually makes a difference._

You'll need to use `get_arch_list()` to see if your registered GFX version is listed in the output.

```python
16:26:55 | /mnt/valerie/public/mini
(.venv) git:(main | θ) λ python
Python 3.12.8 (main, Dec 24 2024, 18:57:29) [GCC 14.2.1 20240910] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.cuda.get_arch_list())
['gfx900', 'gfx906', 'gfx908', 'gfx90a', 'gfx942', 'gfx1030', 'gfx1100', 'gfx1101', 'gfx1102']
>>> 
```

If you do not see your GFX version in the listed output, you'll need to find a version that does. PR #147761 fixes this for GFX1102 registered cards. The latest stable includes 1100, 1101, but excludes 1102 which was the root cause for my runtime error.

8. Test the environment variables before setting them so they do not conflict with testing.

```python
16:31:04 | /mnt/valerie/public/mini
(.venv) git:(main | θ) λ AMDGPU_TARGETS="gfx1102" PYTORCH_ROCM_ARCH="gfx1102" HSA_OVERRIDE_GFX_VERSION="11.0.2" TRITON_USE_ROCM=1 python
Python 3.12.8 (main, Dec 24 2024, 18:57:29) [GCC 14.2.1 20240910] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.cuda.is_available())       # True
True
>>> print(torch.cuda.device_count())       # 1
1
>>> print(torch.cuda.get_device_name(0))   # AMD Radeon RX 7600 XT
AMD Radeon RX 7600 XT
>>> x = torch.randn(3, 3).cuda()
>>> print(x)
tensor([[-1.4272, -0.2168, -1.3327],
        [ 0.8613, -0.7011, -1.9726],
        [-0.5833,  0.1474,  0.3193]], device='cuda:0')
>>> 
```

9. Once everything is validated and operational, then you can set the environment variables in your bashrc, zshrc, or whatever config for the terminal you use is.

**You must use the GFX model in your outputs from earlier steps, or you will encounter errors.**

See my [Knowledge Base article](https://github.com/teleprint-me/mini/blob/main/kb/rocm.md) for more information.

---

### 评论 #8 — isaaclepes (2025-03-02T21:47:26Z)

Mine showed as gfx1102, it was only showing gfx1100 because I had an override in place for that version.
My card is an Gigabyte RX 7600 XT if that helps at all.

![Image](https://github.com/user-attachments/assets/127744e5-3c3d-4f8a-897b-d668b333bf20)

![Image](https://github.com/user-attachments/assets/abee681a-42a4-4de9-a993-a750c86cff81)

![Image](https://github.com/user-attachments/assets/b2719002-7e82-4045-9412-f5593651cf80)

![Image](https://github.com/user-attachments/assets/509f244f-cd35-4f6d-9f91-1e6737aaf450)

![Image](https://github.com/user-attachments/assets/1414db75-7baa-4f67-805c-e0b14e648076)

![Image](https://github.com/user-attachments/assets/ab0a781f-aa3a-4bad-b26c-d2b0f9227175)

![Image](https://github.com/user-attachments/assets/e373f61c-d74e-4af3-9512-038a295ac800)

![Image](https://github.com/user-attachments/assets/b8f4db7c-8e2a-469b-a87c-7c84015fff54)

![Image](https://github.com/user-attachments/assets/094d4575-1533-4994-b358-9967c553c77e)

---

### 评论 #9 — isaaclepes (2025-03-02T22:08:00Z)

Used the default ComfyUI workflow as a test

![Image](https://github.com/user-attachments/assets/044459ce-7d87-4006-93e1-e3e1a77a7b69)

Thanks for the help.  Now I just need to figure out how to make Blender detect it.

---

### 评论 #10 — isaaclepes (2025-03-02T22:54:13Z)

I just needed to install the hip-runtime-amd6.2.4 packages and not use the Blender flatpack version.

![Image](https://github.com/user-attachments/assets/bdeee55f-682b-404b-98d4-12b8778a5e9a)

Closing ticket.

---

### 评论 #11 — Daviviniciusdev (2026-01-16T14:33:30Z)

I managed to install ROCM on my RX 7600, I did a basic test, look at the difference!

import torch
import time

# Definindo tamanhos grandes para medir diferença de performance
N = 8000

# Cria matrizes grandes aleatórias
x_cpu = torch.randn(N, N)
y_cpu = torch.randn(N, N)

# --- Teste CPU ---
start_cpu = time.time()
z_cpu = x_cpu @ y_cpu
end_cpu = time.time()
print(f"CPU time: {end_cpu - start_cpu:.4f} seconds")

# --- Teste GPU ---
device = "cuda" if torch.cuda.is_available() else "cpu"
x_gpu = x_cpu.to(device)
y_gpu = y_cpu.to(device)

# Necessário sincronizar a GPU porque operações CUDA são assíncronas
torch.cuda.synchronize()
start_gpu = time.time()

z_gpu = x_gpu @ y_gpu

torch.cuda.synchronize()
end_gpu = time.time()
print(f"GPU time: {end_gpu - start_gpu:.4f} seconds")

output: 
CPU time: 38.6207 seconds
GPU time: 0.5351 seconds

[Done] exited with code=0 in 41.696 seconds

---
