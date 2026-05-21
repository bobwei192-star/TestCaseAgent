# [Issue]: Crashes / instability on Ubuntu w/ desktop environment 

> **Issue #2820**
> **状态**: closed
> **创建时间**: 2024-01-18T05:39:04Z
> **更新时间**: 2024-06-19T21:31:22Z
> **关闭时间**: 2024-06-19T18:38:32Z
> **作者**: kuhar
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/2820

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 负责人

- benrichard-amd
- nartmada

## 描述

### Problem Description

My rocm installation suffers severe instability that results in graphical artifacts, program hangs, and program / X session crashes.

These issues are intermittent; running the same program can work fine but consistently fail after a system reboot. I can reproduce it with both large ML applications (e.g., llama2 with SHARK) and with toy programs like `rocm-examples`, which makes me think it's related to the rocm installation instead of the exact application executed.

![rocm-crash](https://github.com/ROCm/ROCm/assets/4612584/383f6099-0b7a-4401-9f03-c601e67870b5)

The iGPU is disabled in the BIOS. I installed rocm using these instructions: https://rocm.docs.amd.com/en/docs-5.7.1/deploy/linux/quick_start.html.

I would like to understand what is the root cause and if this can be fixed or worked around, or confirm if running rocm in a desktop environment is not supported.

Happy to provide any additional details that can help.

### Operating System

Ubuntu 23.04

### CPU

AMD Ryzen 9 7950X

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
  Name:                    AMD Ryzen 9 7950X 16-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 7950X 16-Core Processor
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
  Max Clock Freq. (MHz):   4500                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65550296(0x3e837d8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65550296(0x3e837d8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65550296(0x3e837d8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-4e061d420fdb0000               
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
  Max Clock Freq. (MHz):   2431                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
  Packet Processor uCode:: 528                                
  SDMA engine uCode::      19                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    25149440(0x17fc000) KB             
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
```

### Additional Information

_No response_

---

## 评论 (18 条)

### 评论 #1 — GZGavinZhao (2024-01-19T18:45:51Z)

https://github.com/ROCm/ROCm/issues/2596#issuecomment-1882229291

---

### 评论 #2 — TheNexter (2024-01-22T14:06:06Z)

Same here, ubuntu 22.04 (Clean install from last week), kernel 6.2, 6600 XT

I have this bug after using ROCM with SDXL with Fooocus.

![4havfrvjrvdc1-cropped](https://github.com/ROCm/ROCm/assets/17613028/72b5858b-be3a-4269-b8bc-4a9380597534)

After ~10 images in quality settings.

My Friend with ubuntu 22.04 (Clean install from last week), kernel 6.2, 6700 have the same bug but after ~20 images in quality

99% of the time i stop fooocus, CTRL + ALT + F1 and the problem is fix, but sometime no.

---

### 评论 #3 — TheNexter (2024-01-22T22:00:32Z)

To add another detail that can explain the problem :
After image generation, by default the model is unloaded of the VRAM but no, in this case, it's unloading only 50/60%/70% but after i force stop fooocus, then the model is completely unloaded from the memory but I still need to CTRL + ALT + F1 to remove the glitch on the screen 🫠

Photo of the vram after frame generation on comfyui
![PXL_20240122_215415652](https://github.com/ROCm/ROCm/assets/17613028/170be8c3-8229-4558-9a89-44b6985bf78b)

When comfy UI try to load another model, he say to me this error :
![PXL_20240122_215428967](https://github.com/ROCm/ROCm/assets/17613028/f4cc3878-620e-43d5-9654-d76b98c43551)


---

### 评论 #4 — TheNexter (2024-01-22T22:03:37Z)

My ROCM info for 6600 XT :

[rocm-info 6600 XT.txt](https://github.com/ROCm/ROCm/files/14044396/rocm-info.6600.XT.txt)


---

### 评论 #5 — benrichard-amd (2024-01-23T01:29:12Z)

Hi,

Thank you for the info so far. If possible can you share the output of `sudo dmesg` when this happens? There should be `amdgpu` kernel module messages in there.

Thanks.

---

### 评论 #6 — kuhar (2024-01-23T03:26:58Z)

Some `dmesg` logs. This time running the application (llama2 13B with SHARK) worked for me and hang the second time. After that any rocm programs hang or fail to start.

Boot log: 
[dmesg_boot.txt](https://github.com/ROCm/ROCm/files/14043410/dmesg_boot.txt)


After running rocm-examples (`hip_matrix_multiplication`) (Validation passed.):
```
[283151.307374] amd_iommu_report_page_fault: 2 callbacks suppressed
[283151.307378] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x6bfbb000 flags=0x0000]
[283151.307379] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[283151.307382] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3A
[283151.307384] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[283151.307387] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[283151.307388] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x5
[283151.307391] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[283151.307394] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[283151.307396] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
[283151.307405] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x6bfbb000 flags=0x0020]
[283151.565454] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x6bfbb000 flags=0x0020]
```

After runnning rocm-examples (`hip_inline_assembly`) (Validation passed.)

```
[283209.022231] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x6bfbb000 flags=0x0020]
[283256.901318] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[283256.901326] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00000005f6801000 from client 10
[283256.901330] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[283256.901333] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[283256.901336] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[283256.901339] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[283256.901341] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[283256.901343] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[283256.901345] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
```

After running llama2 13B with SHARK (Succeeded):
```
[283420.875106] amd_iommu_report_page_fault: 5 callbacks suppressed
[283420.875110] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3A
[283420.875110] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bed1000 flags=0x0000]
[283420.875113] amdgpu 0000:03:00.0: amdgpu:     Faulty UTCL2 client ID: CPC (0x5)
[283420.875115] amdgpu 0000:03:00.0: amdgpu:     MORE_FAULTS: 0x0
[283420.875117] amdgpu 0000:03:00.0: amdgpu:     WALKER_ERROR: 0x5
[283420.875118] amdgpu 0000:03:00.0: amdgpu:     PERMISSION_FAULTS: 0x3
[283420.875122] amdgpu 0000:03:00.0: amdgpu:     MAPPING_ERROR: 0x1
[283420.875124] amdgpu 0000:03:00.0: amdgpu:     RW: 0x0
[283420.875132] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bed1000 flags=0x0020]
[283435.188657] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x77194000 flags=0x0000]
[283435.188679] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x77194000 flags=0x0020]
[283436.088258] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x6a67b000 flags=0x0000]
[283436.088273] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x6a67b000 flags=0x0020]
[283652.110594] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[283652.110599] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00000005e5401000 from client 10
[283652.110601] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[283652.110603] amdgpu 0000:03:00.0: amdgpu:     Faulty UTCL2 client ID: CPC (0x5)
[283652.110604] amdgpu 0000:03:00.0: amdgpu:     MORE_FAULTS: 0x0
[283652.110605] amdgpu 0000:03:00.0: amdgpu:     WALKER_ERROR: 0x1
[283652.110607] amdgpu 0000:03:00.0: amdgpu:     PERMISSION_FAULTS: 0x3
[283652.110608] amdgpu 0000:03:00.0: amdgpu:     MAPPING_ERROR: 0x1
[283652.110609] amdgpu 0000:03:00.0: amdgpu:     RW: 0x0
[283653.580650] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[283653.580658] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00000005e5401000 from client 10
[283653.580662] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[283653.580665] amdgpu 0000:03:00.0: amdgpu:     Faulty UTCL2 client ID: CPC (0x5)
[283653.580668] amdgpu 0000:03:00.0: amdgpu:     MORE_FAULTS: 0x0
[283653.580670] amdgpu 0000:03:00.0: amdgpu:     WALKER_ERROR: 0x1
[283653.580672] amdgpu 0000:03:00.0: amdgpu:     PERMISSION_FAULTS: 0x3
[283653.580674] amdgpu 0000:03:00.0: amdgpu:     MAPPING_ERROR: 0x1
[283653.580676] amdgpu 0000:03:00.0: amdgpu:     RW: 0x0
[283653.664659] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[283653.664666] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00000005e5401000 from client 10
[283653.664669] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[283653.664672] amdgpu 0000:03:00.0: amdgpu:     Faulty UTCL2 client ID: CPC (0x5)
[283653.664674] amdgpu 0000:03:00.0: amdgpu:     MORE_FAULTS: 0x0
[283653.664677] amdgpu 0000:03:00.0: amdgpu:     WALKER_ERROR: 0x1
[283653.664679] amdgpu 0000:03:00.0: amdgpu:     PERMISSION_FAULTS: 0x3
[283653.664681] amdgpu 0000:03:00.0: amdgpu:     MAPPING_ERROR: 0x1
[283653.664683] amdgpu 0000:03:00.0: amdgpu:     RW: 0x0
```

After running llama2 13b (Hang!)
```
[283817.888834] amd_iommu_int_thread: 2718 callbacks suppressed
[283817.888835] AMD-Vi: IOMMU event log overflow
[283817.890452] AMD-Vi: IOMMU event log overflow
[283817.892076] AMD-Vi: IOMMU event log overflow
[283817.893757] AMD-Vi: IOMMU event log overflow
[283817.895359] AMD-Vi: IOMMU event log overflow
[283817.896964] AMD-Vi: IOMMU event log overflow
[283817.898570] AMD-Vi: IOMMU event log overflow
[283817.900255] AMD-Vi: IOMMU event log overflow
[283817.901959] AMD-Vi: IOMMU event log overflow
[283817.903852] AMD-Vi: IOMMU event log overflow
[283822.892014] amd_iommu_report_page_fault: 1988766 callbacks suppressed
[283822.892017] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892028] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892032] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892036] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892040] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892044] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892048] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892051] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892055] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.892059] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283822.893334] amd_iommu_int_thread: 2724 callbacks suppressed
[283822.893335] AMD-Vi: IOMMU event log overflow
[283822.895226] AMD-Vi: IOMMU event log overflow
[283822.897121] AMD-Vi: IOMMU event log overflow
[283822.898739] AMD-Vi: IOMMU event log overflow
[283822.900644] AMD-Vi: IOMMU event log overflow
[283822.902375] AMD-Vi: IOMMU event log overflow
[283822.903992] AMD-Vi: IOMMU event log overflow
[283822.905943] AMD-Vi: IOMMU event log overflow
[283822.907850] AMD-Vi: IOMMU event log overflow
[283822.909592] AMD-Vi: IOMMU event log overflow
[283827.895998] amd_iommu_report_page_fault: 1992101 callbacks suppressed
[283827.896001] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896014] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896018] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896022] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896026] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896030] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896034] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896038] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896042] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896046] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x517e012f100 flags=0x0010]
[283827.896481] amd_iommu_int_thread: 2729 callbacks suppressed
[283827.896482] AMD-Vi: IOMMU event log overflow
[283827.898198] AMD-Vi: IOMMU event log overflow
[283827.899957] AMD-Vi: IOMMU event log overflow
[283827.901579] AMD-Vi: IOMMU event log overflow
[283827.903535] AMD-Vi: IOMMU event log overflow
[283827.905490] AMD-Vi: IOMMU event log overflow
[283827.907091] AMD-Vi: IOMMU event log overflow
[283827.908695] AMD-Vi: IOMMU event log overflow
[283827.910295] AMD-Vi: IOMMU event log overflow
[283827.912214] AMD-Vi: IOMMU event log overflow
```

Running llama2 13B again (Hang):
```
[283919.087877] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.088087] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.090458] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.090604] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.203594] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.203705] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.210353] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.210488] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.316675] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.316797] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.322249] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.322383] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.429328] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.429430] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.446433] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.446567] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.541963] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.542060] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.559167] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.559269] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.654788] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.654917] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.767490] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.767590] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283919.880365] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[283919.880502] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1800
[283919.880635] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[283919.993397] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283919.993511] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.106206] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.106311] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.218593] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.218726] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.270074] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.270208] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.331258] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.331358] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.383080] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.383186] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.439767] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[283920.439948] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1800
[283920.440120] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[283920.500622] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.500748] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.552825] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.552935] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.613288] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.613388] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.665529] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.665652] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.778071] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.778203] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283920.890739] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283920.890837] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283921.003015] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[283921.003150] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1a00
[283921.003281] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[283921.003694] amdgpu 0000:03:00.0: amdgpu: GPU reset(2) succeeded!
[283921.005895] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283921.006021] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283921.118420] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283921.118529] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283921.321408] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283921.321542] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283921.434104] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[283921.434204] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[283924.098156] amd_iommu_report_page_fault: 367957 callbacks suppressed
[283924.098161] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.101831] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.105470] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.110045] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.113665] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.118203] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.122699] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.126207] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.130697] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283924.135214] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.099616] amd_iommu_report_page_fault: 137 callbacks suppressed
[283930.099621] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.102138] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.106716] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.110244] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.114769] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.119265] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.122812] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.127346] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.131920] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283930.135473] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.099366] amd_iommu_report_page_fault: 137 callbacks suppressed
[283936.099372] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.103087] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.106703] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.111332] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.115964] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.119621] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.124234] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.127896] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.132522] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
[283936.136203] amdgpu 0000:03:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x000f address=0x5bbb5000 flags=0x0020]
```

Running `hip_matrix_multiplication` again fails:
```console
➜ HIP-Basic/matrix_multiplication/hip_matrix_multiplication
An error encountered: "invalid device ordinal" at /home/jakub/projects/rocm-examples/HIP-Basic/matrix_multiplication/main.hip:180
```

```
284169.428826] amdgpu: failed to add hardware queue to MES, doorbell=0x1000
[284169.428828] amdgpu: MES might be in unrecoverable state, issue a GPU reset
[284169.428845] amdgpu: Pasid 0x800d DQM create queue type 0 failed. ret -110
[284169.428855] amdgpu 0000:03:00.0: amdgpu: GPU reset begin!
[284169.434664] amdgpu 0000:03:00.0: amdgpu: recover vram bo from shadow start
[284169.436647] amdgpu 0000:03:00.0: amdgpu: recover vram bo from shadow done
[284169.548848] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.548980] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.555332] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.555481] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.661521] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.661620] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.667978] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.668090] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.774323] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.774425] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.792285] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.792399] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.887016] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.887116] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.904989] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.905091] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284169.999743] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284169.999849] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284170.112427] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284170.112530] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284170.225154] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284170.225249] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284170.337841] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284170.337937] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284170.450524] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[284170.450618] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1800
[284170.450731] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[284170.563282] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284170.563389] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284170.675863] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284170.675979] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284170.788448] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284170.788574] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284170.901069] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284170.901172] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284171.013653] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[284171.013753] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1800
[284171.013855] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[284171.126343] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284171.126451] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284171.238918] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284171.239023] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284171.351502] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284171.351599] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284171.464063] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[284171.464162] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[284171.576567] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[284171.576689] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1a00
[284171.576797] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[284171.577041] amdgpu 0000:03:00.0: amdgpu: GPU reset(9) succeeded!
```

---

### 评论 #7 — TheNexter (2024-01-24T10:07:20Z)

> Hi,
> 
> Thank you for the info so far. If possible can you share the output of `sudo dmesg` when this happens? There should be `amdgpu` kernel module messages in there.
> 
> Thanks.

Edit : This log is when everything is normal, the second one gonna be when problem append
[dmesg 6600XT.txt](https://github.com/ROCm/ROCm/files/14036611/dmesg.6600XT.txt)

This one is with glitch on screen (model fail to reload on GPU when i capture this error (and few second after fooocus app crash) :
[dmesg 6600XT GLITCH VERSION.txt](https://github.com/ROCm/ROCm/files/14044547/dmesg.6600XT.GLITCH.VERSION.txt)


---

### 评论 #8 — terryrankine (2024-01-29T02:47:26Z)

I have seen similar things - https://github.com/ROCm/ROCm/issues/2689



---

### 评论 #9 — hnarayanan (2024-01-29T22:30:52Z)

I just came to say me too: 
![image](https://github.com/ROCm/ROCm/assets/661446/e466bdc5-b479-4141-acd5-7d175f80c2c4)


---

### 评论 #10 — smirgol (2024-02-10T17:52:19Z)

I'm in the same boat. Everything that is about compute stuff / rocm will crash the driver sooner or later. It was pretty worse with 5.6, got a tad better with 5.7 and even more better with 6.0, but in the end it always crashed with logs very similar to kuha, requiring a full reboot to fix it. 
On 5.6 and 5.7 I was using a 5700 XT, on 5.7 and 6.0 it's a 7900 XTX - not that it matters, the outcome is the same.

Now, after trying to update from 6.0.0 to 6.0.2 it won't even boot into desktop any more, I assume due to the new 6.5 HWE kernel on my Ubuntu 22.04.3 - but that's a completely different story. It's just because of this I cannot provide any more logs, as it's not working at all right now (again). But, since I've stumbled upon this issue when searching for a solution and I experience the same issue I wanted to leave a comment - sorry for the noise.

Overall, SD is crashing the driver much faster than e.g. using language models, I guess due to the nature of frequent restarts. I'm happy to provide some logs if I ever get to work it again.

```
OS: Ubuntu 22.04.3 LTS x86_64 
Kernel: 6.5.0-17-generic
DE: Xfce 4.16
WM: Xfwm4
CPU: AMD Ryzen 9 3900X (24) @ 3.800GHz
GPU: AMD ATI 0e:00.0 Device 744c  (7900 XTX that is)
```

---

### 评论 #11 — nartmada (2024-02-12T22:09:52Z)

The issue has been fixed in the GPU driver.  The fix should be available in upcoming release of ROCm 6.1.

---

### 评论 #12 — TheNexter (2024-02-14T17:13:05Z)

> The issue has been fixed in the GPU driver. The fix should be available in upcoming release of ROCm 6.1.

Amazing guy, ROCm 6.1 gonna be release when ? I see Q1 2024, this is still relevant information ?

---

### 评论 #13 — giorgi1324 (2024-04-22T04:41:55Z)

I am experiencing the same issue on a fresh install of Ubuntu 22.04.4, ROCm 6.1

### Operating System
Ubuntu 22.04.4

### CPU

Intel i5-13600k
### GPU

AMD Radeon RX 7900 XT
### ROCm Version

### Steps to Reproduce

Run any tensorflow load. In my case I'm running a local jupyter notebook and training a very simple model, cell 19 in this sample: https://github.com/ageron/handson-ml3/blob/main/11_training_deep_neural_networks.ipynb

Observe jankiness, overall system instability and visual artifacts. Most of the time Gnome crashes and I am logged out.
Photo of the visual artifacts: 
![image](https://github.com/ROCm/ROCm/assets/740702/0e3b4e92-6415-4c43-8d7d-4f95fba1c90f)

Dmesg of the machine during the failure: https://drive.google.com/file/d/1hdnEkcrR4Ru0Tbq3YaysqI17ZY9b8plx/view?usp=drive_link
Essentially the kernel log is flooded with following two lines"
```
[  253.497826] [drm:amdgpu_cs_parser_bos.isra.0 [amdgpu]] *ERROR* amdgpu_vm_validate() failed.
[  253.498005] [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Not enough memory for command submission!
```


(Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support:
```
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
  Name:                    13th Gen Intel(R) Core(TM) i5-13600K
  Uuid:                    CPU-XX                             
  Marketing Name:          13th Gen Intel(R) Core(TM) i5-13600K
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
  Max Clock Freq. (MHz):   5600                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            20                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32609448(0x1f194a8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32609448(0x1f194a8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32609448(0x1f194a8) KB             
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
  Uuid:                    GPU-a6c637ccdc57df6b               
  Marketing Name:          Radeon RX 7900 XT                  
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
    L3:                      81920(0x14000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2075                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            84                                 
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
  Packet Processor uCode:: 92                                 
  SDMA engine uCode::      20                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    20955136(0x13fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    20955136(0x13fc000) KB             
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
```

---

### 评论 #14 — kuhar (2024-04-23T00:54:08Z)

@giorgi1324 as one data point, I also did a fresh install last week (22.04 + rocm 6.1) and so far it seems to be working fine for me for the first time ever. I did **not** install the dkms driver, only the rocm apt package

---

### 评论 #15 — giorgi1324 (2024-04-23T05:40:40Z)

@kuhar Confirming that this works for me as well. Uninstalled my ROCm installation and ran `sudo amdgpu-install --usecase=graphics,multimedia,rocm --no-dkms`
After this I'm able to run ROCm-backed TF without any visual artifacts.

Also just FYI to those investigating, I am using a nightly build of `tensorflow-rocm` downloaded from http://ml-ci.amd.com:21096/job/tensorflow/job/release-rocmfork-r214-rocm-enhanced/view/All/builds as the official release still has typo bug that prevents 7900 XT from being recognized by TF ROCm plugin.

---

### 评论 #16 — DemiMarie (2024-06-18T23:33:08Z)

@nartmada was the fix in the kernel or userspace driver?

---

### 评论 #17 — ppanchad-amd (2024-06-19T18:38:32Z)

@DemiMarie It was fixed in the firmware. Thanks!

---

### 评论 #18 — DemiMarie (2024-06-19T21:31:21Z)

@ppanchad-amd thanks for the information!  I asked because one of the logs indicated bad DMA transactions (blocked by IOMMU), which looked like a potential security vulnerability.

---
