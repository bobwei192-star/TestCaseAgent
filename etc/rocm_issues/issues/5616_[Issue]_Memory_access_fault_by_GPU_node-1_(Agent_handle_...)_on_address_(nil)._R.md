# [Issue]: Memory access fault by GPU node-1 (Agent handle: ...) on address (nil). Reason: Page not present or supervisor privilege

> **Issue #5616**
> **状态**: closed
> **创建时间**: 2025-11-02T14:33:04Z
> **更新时间**: 2026-01-11T01:24:48Z
> **关闭时间**: 2025-12-29T02:10:32Z
> **作者**: da-phil
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5616

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

On my TUXEDO InfinityBook Pro 14 - Gen9 laptop I'm regularly doing image processing in darktable and make use of the OpenCL ROCr runtime which comes with ROCm.
Unfortunately I keep experiencing the following program crashes with the following error message:
```
Memory access fault by GPU node-1 (Agent handle: 0x70dcc0d7e460) on address (nil). Reason: Page not present or supervisor privilege
```

This seems to be related with mapped memory from RAM.
I allowed the iGPU to use 4 GB of RAM within the laptop BIOS.

But it looks like the OpenCL system is reporting the amount of memory incorrectly (see attached clinfo log below):

**Platform Name: AMD Accelerated Parallel Processing**
```
  Global memory size                              14599004160 (13.6GiB)
  Global free memory (AMD)                        13966156 (13.32GiB) 13966156 (13.32GiB) <--- wrong!
```

**Platform Name: Clover**
```
  Global memory size                              14599004160 (13.6GiB)
  Max memory allocation                           3649751040 (3.399GiB) <--- seems correct!
```

**Platform Name: rusticl**
No mem info in clinfo :( 

I'm currently on the mainline 6.17.6 kernel with the latest amdgpu linux firmware (from git) and use ROCm 7.0.1, but I have experienced this issues with previous versions as well.

I installed ROCm with the following command:
```
amdgpu-install --usecase=graphics,multimedia,opencl  --opencl=rocr   --no-dkms
```

Here are the system infos:
```
OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU: 
model name	: AMD Ryzen 7 8845HS w/ Radeon 780M Graphics
GPU:
  Name:                    AMD Ryzen 7 8845HS w/ Radeon 780M Graphics
  Marketing Name:          AMD Ryzen 7 8845HS w/ Radeon 780M Graphics
  Name:                    gfx1103                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1103         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    aie2                               
  Marketing Name:          AIE-ML
```

### Operating System

Ubuntu 24.04

### CPU

AMD Ryzen 7 8845HS

### GPU

Radeon 780M

### ROCm Version

ROCm 7.0.1

### ROCm Component

ROCR-Runtime

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.11
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
  Name:                    AMD Ryzen 7 8845HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 8845HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   2000                               
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
      Size:                    28513680(0x1b31590) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    28513680(0x1b31590) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    28513680(0x1b31590) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    28513680(0x1b31590) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1103                            
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
  Chip ID:                 6400(0x1900)                       
  ASIC Revision:           12(0xc)                            
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   25856                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 67                                 
  SDMA engine uCode::      23                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    14256840(0xd98ac8) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    14256840(0xd98ac8) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1103         
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
*******                  
Agent 3                  
*******                  
  Name:                    aie2                               
  Uuid:                    AIE-XX                             
  Marketing Name:          AIE-ML                             
  Vendor Name:             AMD                                
  Feature:                 AGENT_DISPATCH                     
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        1(0x1)                             
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          64(0x40)                           
  Queue Type:              SINGLE                             
  Node:                    0                                  
  Device Type:             DSP                                
  Cache Info:              
    L2:                      2048(0x800) KB                     
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          0(0x0)                             
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            0                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:0                                  
  Memory Properties:       
  Features:                AGENT_DISPATCH
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    28513680(0x1b31590) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65536(0x10000) KB                  
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    28513680(0x1b31590) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***    
```

### Additional Information

OpenCL info from `clinfo`: [clinfo.txt](https://github.com/user-attachments/files/23291781/clinfo.txt)

Kernel log (`dmesg`):
```
[229550.864052] amdgpu 0000:65:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:88 vmid:8 pasid:32787)
[229550.864069] amdgpu 0000:65:00.0: amdgpu:  Process darktable pid 70131 thread worker 0 pid 70175
[229550.864075] amdgpu 0000:65:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[229550.864079] amdgpu 0000:65:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x008012B0
[229550.864083] amdgpu 0000:65:00.0: amdgpu: 	 Faulty UTCL2 client ID: SQC (inst) (0x9)
[229550.864087] amdgpu 0000:65:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[229550.864090] amdgpu 0000:65:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[229550.864093] amdgpu 0000:65:00.0: amdgpu: 	 PERMISSION_FAULTS: 0xb
[229550.864096] amdgpu 0000:65:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[229550.864099] amdgpu 0000:65:00.0: amdgpu: 	 RW: 0x0
[229552.867660] amdgpu 0000:65:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[229552.867671] amdgpu 0000:65:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[229552.867675] amdgpu 0000:65:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[229552.867681] amdgpu 0000:65:00.0: amdgpu: Failed to evict queue 1
[229552.867727] amdgpu 0000:65:00.0: amdgpu: GPU reset begin!
[229552.867838] amdgpu 0000:65:00.0: amdgpu: Failed to evict process queues
[229552.867896] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.867925] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.867933] amdgpu 0000:65:00.0: amdgpu: Dumping IP State
[229552.867949] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.867971] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.867996] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.868019] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.868052] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[229552.868078] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.868101] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[229552.868120] amdgpu 0000:65:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[229552.870187] amdgpu 0000:65:00.0: amdgpu: Dumping IP State Completed
[229552.915324] amdgpu 0000:65:00.0: amdgpu: MODE2 reset
[229552.954067] amdgpu 0000:65:00.0: amdgpu: GPU reset succeeded, trying to resume
[229552.954617] [drm] PCIE GART of 512M enabled (table at 0x00000080FFD00000).
[229552.954744] amdgpu 0000:65:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[229552.954747] amdgpu 0000:65:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[229552.954752] amdgpu 0000:65:00.0: amdgpu: SMU is resuming...
[229552.955886] amdgpu 0000:65:00.0: amdgpu: SMU is resumed successfully!
[229552.961851] amdgpu 0000:65:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005400
[229553.668577] amdgpu 0000:65:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[229553.668593] amdgpu 0000:65:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[229553.668600] amdgpu 0000:65:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[229553.668606] amdgpu 0000:65:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[229553.668612] amdgpu 0000:65:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[229553.668617] amdgpu 0000:65:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[229553.668623] amdgpu 0000:65:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[229553.668628] amdgpu 0000:65:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[229553.668635] amdgpu 0000:65:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[229553.668640] amdgpu 0000:65:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[229553.668646] amdgpu 0000:65:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[229553.668653] amdgpu 0000:65:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[229553.668658] amdgpu 0000:65:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[229553.672192] amdgpu 0000:65:00.0: amdgpu: GPU reset(1) succeeded!
[229553.672211] amdgpu 0000:65:00.0: [drm] device wedged, but recovered through reset
[229652.878954] amdgpu: Freeing queue vital buffer 0x70db22c00000, queue evicted
[229652.878975] amdgpu: Freeing queue vital buffer 0x70dc80c00000, queue evicted
[229652.878980] amdgpu: Freeing queue vital buffer 0x70dc81200000, queue evicted
[232494.801494] amdgpu: Freeing queue vital buffer 0x7dfb2a200000, queue evicted
[232494.801506] amdgpu: Freeing queue vital buffer 0x7dfb2a800000, queue evicted
[233918.552578] amdgpu: Freeing queue vital buffer 0x7d3c2f200000, queue evicted
[233918.552591] amdgpu: Freeing queue vital buffer 0x7d3c2f800000, queue evicted
```

---

## 评论 (50 条)

### 评论 #1 — waltercool (2025-11-02T15:11:35Z)

Do you see any error at dmesg from amdgpu?

---

### 评论 #2 — da-phil (2025-11-02T15:19:37Z)

> Do you see any error at dmesg from amdgpu?

Ups, yes, I forgot to add that to the issue description, sorry. I just added it at the end.


---

### 评论 #3 — waltercool (2025-11-02T15:23:31Z)

Also, can you describe what's the workflow you are doing? Is this comfyui alike things?

---

### 评论 #4 — waltercool (2025-11-02T15:25:52Z)

NVM, I see this is darktable.

Wonder if related to https://github.com/ROCm/ROCm/issues/5590

---

### 评论 #5 — da-phil (2025-11-02T15:43:49Z)

> NVM, I see this is darktable.
> 
> Wonder if related to [#5590](https://github.com/ROCm/ROCm/issues/5590)

I'm not sure, the symptom (page fault / illegal mem access) might be the same, but the rootcause looks different. In my case the issue happens while using ROCr (OpenCL driver) and in the linked ticket some AI workload probably using the HIP backend.
Also the hardware in the linked ticket uses a Strix Halo GPU, whereas my issue is about a laptop based iGPU. But I'm not an expert hence I might be wrong.

---

### 评论 #6 — da-phil (2025-11-02T17:21:09Z)

I think the culprit is the wrong reporting of available GPU memory within the OpenCL platform, I added the `clinfo` output in my first post and here are the reported platforms with their available memory:


**Platform Name: AMD Accelerated Parallel Processing**
```
  Global memory size                              14599004160 (13.6GiB)
  Global free memory (AMD)                        13966156 (13.32GiB) 13966156 (13.32GiB) <--- wrong!
```

**Platform Name: Clover**
```
  Global memory size                              14599004160 (13.6GiB)
  Max memory allocation                           3649751040 (3.399GiB) <--- seems correct!
```

**Platform Name: rusticl**
No mem info in clinfo :( 


---

### 评论 #7 — ianbmacdonald (2025-11-10T16:32:43Z)

@da-phil  what do you see with `$ sudo dmesg | grep amdgpu | grep memory` ? .. it might be easier to let amdgpu handle the allocation completely.    Since it is a similar unified memory configuration to the strix halo, I expect you may be able to take a similar approach where just set the BIOS to `0` (or 512MB like strix halo) and let ttm/amdttm (ttm for 6.17) set the allocation limit for the GPU ; to 4GiB in your case.  This might cleanup how things look from the OpenCL platform.    

---

### 评论 #8 — da-phil (2025-11-12T13:37:39Z)

> [@da-phil](https://github.com/da-phil) what do you see with `$ sudo dmesg | grep amdgpu | grep memory` ? .. it might be easier to let amdgpu handle the allocation completely. Since it is a similar unified memory configuration to the strix halo, I expect you may be able to take a similar approach where just set the BIOS to `0` (or 512MB like strix halo) and let ttm/amdttm (ttm for 6.17) set the allocation limit for the GPU ; to 4GiB in your case. This might cleanup how things look from the OpenCL platform.

This is the output:
```
[  638.372167] amdgpu 0000:65:00.0: amdgpu: VRAM: 4096M 0x0000008000000000 - 0x00000080FFFFFFFF (4096M used)
[  638.372170] amdgpu 0000:65:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[  638.372346] amdgpu 0000:65:00.0: amdgpu: amdgpu: 4096M of VRAM memory ready
[  638.372348] amdgpu 0000:65:00.0: amdgpu: amdgpu: 13922M of GTT memory ready.
``` 

I'm currently not home, hence I cannot test the proposed settings.
So you're saying that I should not let the BIOS reserve the GPU memory, but use the ROCm tools (amdttm) for that?



---

### 评论 #9 — da-phil (2025-11-19T16:10:54Z)

> [@da-phil](https://github.com/da-phil) what do you see with `$ sudo dmesg | grep amdgpu | grep memory` ? .. it might be easier to let amdgpu handle the allocation completely. Since it is a similar unified memory configuration to the strix halo, I expect you may be able to take a similar approach where just set the BIOS to `0` (or 512MB like strix halo) and let ttm/amdttm (ttm for 6.17) set the allocation limit for the GPU ; to 4GiB in your case. This might cleanup how things look from the OpenCL platform.

After being back at home I installed amd-ttm and get the following output (still reserving 4GB of iGPU RAM in BIOS):
```
> amd-ttm
💻 Current TTM pages limit: 3564209 pages (13.60 GB)
💻 Total system memory: 27.19 GB
```

It looks like this limit of 13.6 GB is close to the clinfo memory output for the "AMD Accelerated Parallel Processing" platform...

I will now set the memory limit to the same value I set in the BIOS settings (4 GB) using this command and will report back what the outcome is:
```
> amd-ttm --set 4
🐧 Successfully set TTM pages limit to 1048576 pages (4.00 GB)
🐧 Configuration written to /etc/modprobe.d/ttm.conf
○ NOTE: You need to reboot for changes to take effect.
Would you like to reboot the system now? (y/n): 
```


---

### 评论 #10 — da-phil (2025-11-19T16:29:27Z)

After the reboot I'm getting the values I set before:
```
> amd-ttm
💻 Current TTM pages limit: 1048576 pages (4.00 GB)
💻 Total system memory: 27.19 GB
```

Checking `clinfo` also finally gives me reasonable output for the "AMD Accelerated Parallel Processing" platform:
```
  Global memory size                              4294967296 (4GiB)
  Global free memory (AMD)                        3780608 (3.605GiB) 3780608 (3.605GiB)
```

Let's see if I'm still getting page faults in the next couple of days, will update once I have done some image work in darktable again.


---

### 评论 #11 — amd-nicknick (2025-11-20T07:52:08Z)

Hi @da-phil, yes I agree with @ianbmacdonald that you should let TTM to manage instead of configuring carveout in BIOS. 

It might sound counter-intuitive, but if you carve out a relatively small amount (Less than the rest of available GTT size), you won't be able to use those carveout, it'll just be wasted.

Please also give 7.1 stack a try, there are some fixes wrt memory access and task swapping. If you still encounter this problem, please provide a reproducible script so I can take a look. Thanks!

---

### 评论 #12 — da-phil (2025-11-22T20:35:58Z)

> Hi [@da-phil](https://github.com/da-phil), yes I agree with [@ianbmacdonald](https://github.com/ianbmacdonald) that you should let TTM to manage instead of configuring carveout in BIOS.

Thanks for your reply, let me follow-up with some questions.
 
> It might sound counter-intuitive, but if you carve out a relatively small amount (Less than the rest of available GTT size), you won't be able to use those carveout, it'll just be wasted.

Could you elaborate further please? I think I don't fully understand this sentence.
Why will the carved out memory be wasted?

According to the kernel I now have 4 GiB reserved for VRAM & GTT:
```
amdgpu 0000:65:00.0: amdgpu: Trusted Memory Zone (TMZ) feature enabled
amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
amdgpu: VRAM: 4096M 0x0000008000000000 - 0x00000080FFFFFFFF (4096M used)
amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[drm] Detected VRAM RAM=4096M, BAR=4096M
[drm] RAM width 128bits DDR5
amdgpu 0000:65:00.0: amdgpu: amdgpu: 4096M of VRAM memory ready
amdgpu 0000:65:00.0: amdgpu: amdgpu: 4096M of GTT memory ready.
```

So what I did with the help of the `amd-ttm` tool is carve out a fixed amount of 4 GiB RAM for GTT memory. My BIOS setting seems to be related to the VRAM memory, where I also selected 4 GiB.

> Please also give 7.1 stack a try, there are some fixes wrt memory access and task swapping. If you still encounter this problem, please provide a reproducible script so I can take a look. Thanks!

I also upgraded to ROCm 7.1 when I got started using `amd-ttm`.

---

### 评论 #13 — da-phil (2025-11-22T20:36:08Z)

Only today I encountered another page fault which rendered my Ubuntu desktop completely unusable and required a reboot. This one however was not the typical "Memory access fault by GPU" type of page fault.
Here is the kernel log: [amdgpu-page-fault.log](https://github.com/user-attachments/files/23691571/amdgpu-page-fault.log)

For the sake of completeness, here are my amdgpu kernel boot arguments:
`amdgpu.gpu_recovery=1 amd_pstate=active amdgpu.runpm=1 amdgpu.dpm=1 amdgpu.dcdebugmask=0x10`.


---

### 评论 #14 — da-phil (2025-11-23T16:53:53Z)

Here is another kernel log file after a page fault with the classical "Memory access fault by GPU node-1" error (filtered only for amdgpu msgs): [another-page-fault.log](https://github.com/user-attachments/files/23697145/another-page-fault.log)

---

### 评论 #15 — amd-nicknick (2025-11-24T02:51:01Z)

Hi @da-phil, for a quick experiment, could you please try disabling CWSR?
Add module parameter: `cwsr_enable=0`

---

### 评论 #16 — amd-nicknick (2025-11-24T03:27:56Z)

> Thanks for your reply, let me follow-up with some questions.
> 
> > It might sound counter-intuitive, but if you carve out a relatively small amount (Less than the rest of available GTT size), you won't be able to use those carveout, it'll just be wasted.
> 
> Could you elaborate further please? I think I don't fully understand this sentence. Why will the carved out memory be wasted?
> 
> According to the kernel I now have 4 GiB reserved for VRAM & GTT:
> 
> ```
> amdgpu 0000:65:00.0: amdgpu: Trusted Memory Zone (TMZ) feature enabled
> amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
> amdgpu: VRAM: 4096M 0x0000008000000000 - 0x00000080FFFFFFFF (4096M used)
> amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
> [drm] Detected VRAM RAM=4096M, BAR=4096M
> [drm] RAM width 128bits DDR5
> amdgpu 0000:65:00.0: amdgpu: amdgpu: 4096M of VRAM memory ready
> amdgpu 0000:65:00.0: amdgpu: amdgpu: 4096M of GTT memory ready.
> ```
> 
> So what I did with the help of the `amd-ttm` tool is carve out a fixed amount of 4 GiB RAM for GTT memory. My BIOS setting seems to be related to the VRAM memory, where I also selected 4 GiB.

Yeah, that's a common misconception. Let me clarify:

The system BIOS setting for "GPU memory" is what we call "carveout". Basically, this memory is reserved for use **exclusively** for the iGPU. There are some buffers that must always resides within carveout.
Think of the bitmaps for rendering your screen, they cannot be swapped out, and in certain scenario even requires fixed hardware address, as the display hardware scans out directly from there.

For most of the 3D or compute applications, the buffers don't need to be resident at all times. We could pin the memory right before dispatching the shader code. 
This is done through GART. GART is a GPU virtual memory system where GPU could access **system memory** linearly. Pinning from the host side consolidates noncontiguous pages and maps them via GART, from the GPU's perspective, it is a linear access to a GPU VA.

It is the kfd and umd's responsibility to correctly configure and (to a certain degree) decide which domain buffer object should be mapped.

From your log file:
```
amdgpu 0000:65:00.0: amdgpu: amdgpu: 4096M of VRAM memory ready
amdgpu 0000:65:00.0: amdgpu: amdgpu: 4096M of GTT memory ready.
```
This tells you that 4GB of carveout (VRAM domain) is configured in your BIOS. And the driver is configured to map the maximum of 4GB to the GART (GTT domain).

KFD **prefers** GTT when GTT size is larger than VRAM, as GTT is more flexible (pageable, shared with system memory), and is identical to VRAM in terms of functionality on iGPU systems. Therefore, we recommend setting carveout (VRAM) size to minimum platform value (Auto or 512M), and configure GTT's max limit to your preference.

Hope I have clarified this for you, if you have any further question, please reach out and I will try to answer :)

---

### 评论 #17 — da-phil (2025-11-24T19:10:18Z)

@amd-nicknick thanks a lot for your elaborate answer, this actually helps a lot to understand the merits of the different memory mapping mechanisms going on!
Will try out the module param `cwsr_enable=0` later and report back.

In the meantime I picked up a bad amdgpu firmware (https://gitlab.com/kernel-firmware/linux-firmware/-/commit/df7ad95b388bf1408097d48cd0ad01fe651e2f5b) and could reproduce the "Memory access fault by GPU node-1" error 100% of time, even when just executing `clinfo`. After switching back to an earlier firmware version this issue is gone already. I reported it to the author (Alexander Deucher).

---

### 评论 #18 — da-phil (2025-11-24T23:09:07Z)

Now I set `cwsr_enable=0` and rebooted. Additionally I trimmed down VRAM usage to 512 MB, as recommended and increased GTT mem to 6 GiB.
After a little bit of testing (trying to stress test GPU in darktable) I didn't encounter any issues so far, but this needs a little bit more testing.

Interestingly, radeontop reports an over-utilization of VRAM (110%).
Also, instead of showing 512 MB VRAM and 6109 MB GTT of the configured values it shows slightly different values 🤔 

<img width="1372" height="737" alt="Image" src="https://github.com/user-attachments/assets/5680b81c-8a9d-400e-824a-ec54af5eb897" />

I also attached the current kernel log: [amdgpu-kernel.log](https://github.com/user-attachments/files/23733544/amdgpu-kernel.log)
If you wonder how I set the amdgpu kernel module parameter, I created /etc/modprobe.d/amdgpu.conf to the following content:
```
options amdgpu cwsr_enable=0
```

---

### 评论 #19 — amd-nicknick (2025-11-25T07:37:15Z)

The result from radeontop looks fine. The difference came from TTM's calculation of used / total. Platform code will also reserve some space if configured to 512M, leading to smaller total usable size.
The way you configured the parameter looks good. If you can get positive result with `cwsr_enable=0`, there is a fix available but will need some time to get to release.

---

### 评论 #20 — kenny8zeng (2025-11-25T16:34:43Z)

I encountered the same issue. My device is an AMD MAX 395, and run debian 13, the path to reproduce the problem is running ComfyUI in Docker, where executing the typical Wan2.2 workflow will inevitably trigger the issue.

First, save two file:

```Dockerfile
# Dockerfile
FROM rocm/pytorch:rocm7.1_ubuntu24.04_py3.12_pytorch_release_2.8.0

# 设置环境变量，避免交互式安装提示
ENV DEBIAN_FRONTEND=noninteractive
# 设置环境变量以启用 AOTriton 内核（推荐）
ENV TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
# ComfyUI的路径
ENV COMFYUI_HOME='/workspace/ComfyUI'

RUN [ ! -e "$COMFYUI_HOME" ] && \
    git clone https://github.com/comfyanonymous/ComfyUI.git ${COMFYUI_HOME} && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git ${COMFYUI_HOME}/custom_nodes/ComfyUI-Manager

RUN pip install -r ${COMFYUI_HOME}/requirements.txt && \
    pip install -r ${COMFYUI_HOME}/custom_nodes/ComfyUI-Manager/requirements.txt && \
    pip install torchsde imageio-ffmpeg soundfile

WORKDIR ${COMFYUI_HOME}

# 设置默认命令，启动 Python 交互式 shell
CMD ["python3", "main.py", "--listen", "0.0.0.0", "--use-pytorch-cross-attention"]
```

```yaml
# docker-compose.yml
services:
  rocm-comfyui:
    build: .
    privileged: true
    security_opt:
      - 'apparmor=unconfined'
    stdin_open: true
    tty: true
    ipc: host
    shm_size: 8G
    cap_add:
      - SYS_PTRACE
    devices:
      - /dev/kfd
      - /dev/dri
    group_add:
      - video
    ports:
      - "8188:8188"
    volumes:
      - "./volume:/workspace"
```

1. `docker compose up -d && docker compose logs -f`
2. Access ComfyUI by navigating to http://address:8188 in your browser. This URL can be found at the end of the logs.
3. Find any one workflow of `WAN2.2 I2V` in template, enter and run it.

---

### 评论 #21 — da-phil (2025-11-25T21:55:54Z)

> The result from radeontop looks fine. The difference came from TTM's calculation of used / total. Platform code will also reserve some space if configured to 512M, leading to smaller total usable size. The way you configured the parameter looks good. If you can get positive result with `cwsr_enable=0`, there is a fix available but will need some time to get to release.

Unfortunately I could reproduce the issue again, even though I have set `cwsr_enable=0` :(
Here is the kernel log with some details for the page fault: [kernel-amdgpu2.log](https://github.com/user-attachments/files/23756634/kernel-amdgpu2.log)

I also noticed:
```
[82808.624634] amdgpu 0000:65:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[82808.624640] amdgpu 0000:65:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
```

But unfortunately the folder `/sys/class/drm/card1/device/devcoredump` does not exist and therefore I cannot provide a coredump.

Is there more evidence I can provide to help you support to rootcause the issue?

Can it be an issue with a weird / inconsistent memory allocation after sleep/resume cycles?

---

### 评论 #22 — amd-nicknick (2025-11-26T06:22:54Z)

I forgot to check with you on the version of MES firmware you're using.
Kindly provide the output of: `cat /sys/kernel/debug/dri/<BDF of iGPU>/amdgpu_firmware_info`

If the version is > 0x80, then the CWSR flag should be available. In this case, I will need your help to provide a reproducible instruction for me to dig into the state at the failure point.

You might need to provide setup instructions and the methodology that will lead to failure. You mentioned (and seems to be present in the log provided) that there were sleep/wake cycles?

Thanks!

---

### 评论 #23 — da-phil (2025-11-27T22:39:33Z)

> I forgot to check with you on the version of MES firmware you're using. Kindly provide the output of: `cat /sys/kernel/debug/dri/<BDF of iGPU>/amdgpu_firmware_info`
> 
> If the version is > 0x80, then the CWSR flag should be available. In this case, I will need your help to provide a reproducible instruction for me to dig into the state at the failure point.
> 
> You might need to provide setup instructions and the methodology that will lead to failure. You mentioned (and seems to be present in the log provided) that there were sleep/wake cycles?
> 
> Thanks!

Sorry for the late reply, here are the requested firmware versions:

```
> cat /sys/kernel/debug/dri/0000:65:00.0/amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 35, firmware version: 0x00000063
PFP feature version: 35, firmware version: 0x00000067
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x0000008a
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x0000000f
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 35, firmware version: 0x00000043
IMU feature version: 0, firmware version: 0x0b012d00
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648378, firmware version: 0x210000fa
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x17000049
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004c5300 (76.83.0)
SDMA0 feature version: 60, firmware version: 0x00000017
VCN feature version: 0, firmware version: 0x09118016
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x08005400
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x00000106
MES feature version: 1, firmware version: 0x00000080
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-PHXGENERIC-001
```

> You might need to provide setup instructions and the methodology that will lead to failure.

This is extremely difficult as it is not deterministic, the last page fault needed quite some stress testing to provoke it. I need to understand better if there is indeed a deterministic pattern I didn't see yet.

> You mentioned (and seems to be present in the log provided) that there were sleep/wake cycles?

Yes, I usually do not shut down my laptop, I keep it in modern standby (s2idle) when not using it with the lid closed. I also need to understand if I can provoke the page fault after a clean reboot without any sleep/resume cycles in between to proof whether it is related to sleep/resume cycles or not.

---

### 评论 #24 — ianbmacdonald (2025-11-29T00:00:29Z)

Looks like a memory issue happened first `svm_range_restore_work`.   I believe this is paging in/out of GTT shared space into swap.  This is what happens using llama-cpp with models >96MB with mmap enabled on Strix Halo, and was resolved in that use case by enabling `export GGML_CUDA_ENABLE_UNIFIED_MEMORY=1`   Look for kswap activity in top.
 
```
[82597.865800] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
```

Also your kernel log did not have `cwsr_enable=0` as a parameter so we can't rule out human error.  That is why I always recommend the grub drop-in config over module drop-in config for storage or graphics modules, as it doesn't require initramfs-update to apply, and shows up in your dmesg output so you *know* it has been applied.   It seems the rest of your amdgpu parameters are set using a grub drop-in, so it probably makes sense to use it for ttm and cwsr as well for consistency. `amdgpu.gpu_recovery=1 amd_pstate=active amdgpu.runpm=1 amdgpu.dpm=1 amdgpu.dcdebugmask=0x10`


---

### 评论 #25 — waltercool (2025-12-01T07:59:55Z)

I can confirm it always fails (to me) with latest firmware (20251125). It does not happen with 20251111.

Memory access fault by GPU node-1 (Agent handle: 0x5570f8146df0) on address 0x7ff96a9ac000. Reason: Page not present or supervisor privilege

```
[   67.058794] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32786)
[   67.058806] amdgpu 0000:c4:00.0: amdgpu:  Process python3 pid 3370 thread python3 pid 3370
[   67.058809] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007fa4808cb000 from client 10
[   67.058812] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[   67.058813] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[   67.058815] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x0
[   67.058816] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
[   67.058817] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[   67.058818] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
[   67.058819] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
[  178.460145] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32786)
[  178.460156] amdgpu 0000:c4:00.0: amdgpu:  Process python3 pid 4616 thread python3 pid 4616
[  178.460159] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ff96a9ac000 from client 10
[  178.460161] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[  178.460163] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[  178.460165] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x0
[  178.460166] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
[  178.460167] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  178.460168] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  178.460169] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
```

```
  VCE feature version: 0, firmware version: 0x00000000
  UVD feature version: 0, firmware version: 0x00000000
  MC feature version: 0, firmware version: 0x00000000
  ME feature version: 35, firmware version: 0x00000020
  PFP feature version: 35, firmware version: 0x0000002e
  CE feature version: 0, firmware version: 0x00000000
  RLC feature version: 1, firmware version: 0x11530506
  RLC SRLC feature version: 0, firmware version: 0x00000000
  RLC SRLG feature version: 0, firmware version: 0x00000000
  RLC SRLS feature version: 0, firmware version: 0x00000000
  RLCP feature version: 1, firmware version: 0x11530506
  RLCV feature version: 0, firmware version: 0x00000000
  MEC feature version: 35, firmware version: 0x00000020
  IMU feature version: 0, firmware version: 0x0b352300
  SOS feature version: 0, firmware version: 0x00000000
  ASD feature version: 553648388, firmware version: 0x21000104
  TA XGMI feature version: 0x00000000, firmware version: 0x00000000
  TA RAS feature version: 0x00000000, firmware version: 0x00000000
  TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
  TA DTM feature version: 0x00000000, firmware version: 0x1200001a
  TA RAP feature version: 0x00000000, firmware version: 0x00000000
  TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
  SMC feature version: 0, program: 10, firmware version: 0x0a640200 (100.2.0)
  SDMA0 feature version: 60, firmware version: 0x00000011
  VCN feature version: 0, firmware version: 0x0911801b
  DMCU feature version: 0, firmware version: 0x00000000
  DMCUB feature version: 0, firmware version: 0x09003500
  TOC feature version: 0, firmware version: 0x0000000b
  MES_KIQ feature version: 6, firmware version: 0x0000006f
  MES feature version: 1, firmware version: 0x00000083
  VPE feature version: 60, firmware version: 0x00000017
  VBIOS version: 113-STRXLGEN-001
```

Regardless of cwsr_enable. It used to work nice as workaround

---

### 评论 #26 — da-phil (2025-12-01T08:08:13Z)

> I can confirm it always fails (to me) with latest firmware (20251125). It does not happen with 20251111.
> 
> Memory access fault by GPU node-1 (Agent handle: 0x5570f8146df0) on address 0x7ff96a9ac000. Reason: Page not present or supervisor privilege
> 
> ```
> [   67.058794] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32786)
> [   67.058806] amdgpu 0000:c4:00.0: amdgpu:  Process python3 pid 3370 thread python3 pid 3370
> [   67.058809] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007fa4808cb000 from client 10
> [   67.058812] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
> [   67.058813] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
> [   67.058815] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x0
> [   67.058816] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
> [   67.058817] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
> [   67.058818] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
> [   67.058819] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
> [  178.460145] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32786)
> [  178.460156] amdgpu 0000:c4:00.0: amdgpu:  Process python3 pid 4616 thread python3 pid 4616
> [  178.460159] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007ff96a9ac000 from client 10
> [  178.460161] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
> [  178.460163] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
> [  178.460165] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x0
> [  178.460166] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
> [  178.460167] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
> [  178.460168] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
> [  178.460169] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
> ```
> 
> ```
>   VCE feature version: 0, firmware version: 0x00000000
>   UVD feature version: 0, firmware version: 0x00000000
>   MC feature version: 0, firmware version: 0x00000000
>   ME feature version: 35, firmware version: 0x00000020
>   PFP feature version: 35, firmware version: 0x0000002e
>   CE feature version: 0, firmware version: 0x00000000
>   RLC feature version: 1, firmware version: 0x11530506
>   RLC SRLC feature version: 0, firmware version: 0x00000000
>   RLC SRLG feature version: 0, firmware version: 0x00000000
>   RLC SRLS feature version: 0, firmware version: 0x00000000
>   RLCP feature version: 1, firmware version: 0x11530506
>   RLCV feature version: 0, firmware version: 0x00000000
>   MEC feature version: 35, firmware version: 0x00000020
>   IMU feature version: 0, firmware version: 0x0b352300
>   SOS feature version: 0, firmware version: 0x00000000
>   ASD feature version: 553648388, firmware version: 0x21000104
>   TA XGMI feature version: 0x00000000, firmware version: 0x00000000
>   TA RAS feature version: 0x00000000, firmware version: 0x00000000
>   TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
>   TA DTM feature version: 0x00000000, firmware version: 0x1200001a
>   TA RAP feature version: 0x00000000, firmware version: 0x00000000
>   TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
>   SMC feature version: 0, program: 10, firmware version: 0x0a640200 (100.2.0)
>   SDMA0 feature version: 60, firmware version: 0x00000011
>   VCN feature version: 0, firmware version: 0x0911801b
>   DMCU feature version: 0, firmware version: 0x00000000
>   DMCUB feature version: 0, firmware version: 0x09003500
>   TOC feature version: 0, firmware version: 0x0000000b
>   MES_KIQ feature version: 6, firmware version: 0x0000006f
>   MES feature version: 1, firmware version: 0x00000083
>   VPE feature version: 60, firmware version: 0x00000017
>   VBIOS version: 113-STRXLGEN-001
> ```
> 
> Regardless of cwsr_enable. It used to work nice as workaround

The bad commit on the linux-firmware repo was reverted by Alex Deucher after I reported the issue last week.
I should have reported it on the [amdgpu DRM bugtracker](https://gitlab.freedesktop.org/drm/amd/-/issues) for transparency instead.
Maybe it would be good that folks also report the issue with GPUs other than the Radeon 680M iGPU.

---

### 评论 #27 — da-phil (2025-12-01T21:36:54Z)

> Looks like a memory issue happened first `svm_range_restore_work`. I believe this is paging in/out of GTT shared space into swap. This is what happens using llama-cpp with models >96MB with mmap enabled on Strix Halo, and was resolved in that use case by enabling `export GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` Look for kswap activity in top.
> 
> ```
> [82597.865800] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
> ```
> 
> Also your kernel log did not have `cwsr_enable=0` as a parameter so we can't rule out human error. That is why I always recommend the grub drop-in config over module drop-in config for storage or graphics modules, as it doesn't require initramfs-update to apply, and shows up in your dmesg output so you _know_ it has been applied. It seems the rest of your amdgpu parameters are set using a grub drop-in, so it probably makes sense to use it for ttm and cwsr as well for consistency. `amdgpu.gpu_recovery=1 amd_pstate=active amdgpu.runpm=1 amdgpu.dpm=1 amdgpu.dcdebugmask=0x10`

Of course you're completely right with having the amdgpu params in the grub drop-in config makes more sense, as the rest of the params already live there and for double checking whether they have been applied through the kernel log.
I did this now and try to provoke a page fault after a fresh reboot, without success (good!). So maybe this really has something to do with sleep/resume cycles and how (mapped) memory gets handled.
I also need to say that I pulled the latest firmware (including SMU 14.0.3), see [commit history](https://kernel.googlesource.com/pub/scm/linux/kernel/git/firmware/linux-firmware/+log).
So here are my current firmware versions:
```
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 35, firmware version: 0x00000063
PFP feature version: 35, firmware version: 0x00000067
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x0000008a
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x0000000f
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 35, firmware version: 0x00000043
IMU feature version: 0, firmware version: 0x0b012d00
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648388, firmware version: 0x21000104
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004c5300 (76.83.0)
SDMA0 feature version: 60, firmware version: 0x00000017
VCN feature version: 0, firmware version: 0x0911801b
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x08005400
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x00000106
MES feature version: 1, firmware version: 0x00000080
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-PHXGENERIC-001
```

And here is a kernel log, filtered for amgpu messages (without page faults): [amdgpu-no-crash.log](https://github.com/user-attachments/files/23866206/amdgpu-no-crash.log)

---

### 评论 #28 — amd-nicknick (2025-12-08T06:28:20Z)

@da-phil, sorry for the late response, yeah MES 0x83 has a known issue we're working on internally. You could safely disregard test result with 0x83 FW.
Just to confirm, with CWSR=0 **and** sleep/wake cycle, are you still reproducing? If so, I suspect it is a different issue. Your previous log did point hanging in `svm_range_restore_work`, but that could be a number of things already hung before that.

---

### 评论 #29 — da-phil (2025-12-09T21:44:16Z)

> Just to confirm, with CWSR=0 **and** sleep/wake cycle, are you still reproducing?

I wasn't able since my last update (new kernel, latest amdgpu firmware and CWSR=0 set). 
So I'd assume setting CWSR=0 did the trick.

I'll keep stress testing and watch out for the `svm_range_restore_work` messages in the meantime.

---

### 评论 #30 — TawusGames (2025-12-15T19:37:58Z)

same issue with rx 9060 xt 16 gb.

---

### 评论 #31 — jinnko (2025-12-15T20:07:29Z)

> same issue with rx 9060 xt 16 gb.

I too had this issue on a
Ryzen AI 9 HX 370 w/ Radeon 890M iGPU on Arch with the latest linux-zen kernel.

After downgrading to linux-firmware-amdgpu 20251111 the issue is gone. 

Unfortunately I haven't tried any of the other suggestions as I was pressed for time.

---

### 评论 #32 — TawusGames (2025-12-16T10:57:24Z)

> > same issue with rx 9060 xt 16 gb.
> 
> I too had this issue on a Ryzen AI 9 HX 370 w/ Radeon 890M iGPU on Arch with the latest linux-zen kernel.
> 
> After downgrading to linux-firmware-amdgpu 20251111 the issue is gone.
> 
> Unfortunately I haven't tried any of the other suggestions as I was pressed for time.

I use Bazzite OS. I had heard something about Bazzite OS protecting system integrity. I’m not sure whether it’s possible to change the kernel version.

---

### 评论 #33 — kresimirfijacko (2025-12-19T11:08:24Z)

I also have this issue using:
Fedora 43
AMD Ryzen AI 7 PRO 360 w/ Radeon 880M
AMD ROCm 7.10.0
torch 2.9.1+rocm7.10.0
and just trying out different models, like sam3 / siglip2

one thing: amggpu_top reports 32GB GTT (but i have 64)

is there any way to make this work now? 

---

### 评论 #34 — agronholm (2025-12-25T13:02:15Z)

> I also have this issue using: Fedora 43 AMD Ryzen AI 7 PRO 360 w/ Radeon 880M AMD ROCm 7.10.0 torch 2.9.1+rocm7.10.0 and just trying out different models, like sam3 / siglip2
> 
> one thing: amggpu_top reports 32GB GTT (but i have 64)
> 
> is there any way to make this work now?

How did you manage to install ROCm 7.10 on Fedora 43? If you enable rawhide, it needlessly updates a lot of packages you don't want to update.

---

### 评论 #35 — agronholm (2025-12-25T13:25:34Z)

I tried everything – adding the `cwsr_enable=0` kernel boot parameter, downgrading amd-gpu-firmware to `20251021`. The `clinfo` command still crashes with the error in the topic. Is my only recourse to wait for a firmware package update?

---

### 评论 #36 — da-phil (2025-12-25T23:51:31Z)

> I tried everything – adding the `cwsr_enable=0` kernel boot parameter, downgrading amd-gpu-firmware to `20251021`. The `clinfo` command still crashes with the error in the topic. Is my only recourse to wait for a firmware package update?

Looks like you're still using a bad firmware package, I only had this problem with a bad firmware, but never again.

For me it has been working quite stable.
I'm using ROCm 7.1.1 and the following amdgpu kernel parameters: `amdgpu.gpu_recovery=1 amd_pstate=active amdgpu.runpm=1 amdgpu.dpm=1 amdgpu.dcdebugmask=0x10 amdgpu.cwsr_enable=0`
And here are my firmware versions:
```
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 35, firmware version: 0x00000063
PFP feature version: 35, firmware version: 0x00000067
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x0000008a
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x0000000f
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 35, firmware version: 0x00000043
IMU feature version: 0, firmware version: 0x0b012d00
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648388, firmware version: 0x21000104
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004c5300 (76.83.0)
SDMA0 feature version: 60, firmware version: 0x00000017
VCN feature version: 0, firmware version: 0x0911801b
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x08005500
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x00000106
MES feature version: 1, firmware version: 0x00000080
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-PHXGENERIC-001
```

What are yours?


---

### 评论 #37 — agronholm (2025-12-26T00:50:52Z)

> > I tried everything – adding the `cwsr_enable=0` kernel boot parameter, downgrading amd-gpu-firmware to `20251021`. The `clinfo` command still crashes with the error in the topic. Is my only recourse to wait for a firmware package update?
> 
> Looks like you're still using a bad firmware package, I only had this problem with a bad firmware, but never again.
> 
> For me it has been working quite stable. I'm using ROCm 7.1.1 and the following amdgpu kernel parameters: `amdgpu.gpu_recovery=1 amd_pstate=active amdgpu.runpm=1 amdgpu.dpm=1 amdgpu.dcdebugmask=0x10 amdgpu.cwsr_enable=0` And here are my firmware versions:
> 
> ```
> VCE feature version: 0, firmware version: 0x00000000
> UVD feature version: 0, firmware version: 0x00000000
> MC feature version: 0, firmware version: 0x00000000
> ME feature version: 35, firmware version: 0x00000063
> PFP feature version: 35, firmware version: 0x00000067
> CE feature version: 0, firmware version: 0x00000000
> RLC feature version: 1, firmware version: 0x0000008a
> RLC SRLC feature version: 0, firmware version: 0x00000000
> RLC SRLG feature version: 0, firmware version: 0x00000000
> RLC SRLS feature version: 0, firmware version: 0x00000000
> RLCP feature version: 1, firmware version: 0x0000000f
> RLCV feature version: 0, firmware version: 0x00000000
> MEC feature version: 35, firmware version: 0x00000043
> IMU feature version: 0, firmware version: 0x0b012d00
> SOS feature version: 0, firmware version: 0x00000000
> ASD feature version: 553648388, firmware version: 0x21000104
> TA XGMI feature version: 0x00000000, firmware version: 0x00000000
> TA RAS feature version: 0x00000000, firmware version: 0x00000000
> TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
> TA DTM feature version: 0x00000000, firmware version: 0x1200001a
> TA RAP feature version: 0x00000000, firmware version: 0x00000000
> TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
> SMC feature version: 0, program: 0, firmware version: 0x004c5300 (76.83.0)
> SDMA0 feature version: 60, firmware version: 0x00000017
> VCN feature version: 0, firmware version: 0x0911801b
> DMCU feature version: 0, firmware version: 0x00000000
> DMCUB feature version: 0, firmware version: 0x08005500
> TOC feature version: 0, firmware version: 0x0000000b
> MES_KIQ feature version: 6, firmware version: 0x00000106
> MES feature version: 1, firmware version: 0x00000080
> VPE feature version: 0, firmware version: 0x00000000
> VBIOS version: 113-PHXGENERIC-001
> ```
> 
> What are yours?

I didn't know that the full name of the option was `amdgpu.cwsr_enable`, as that never came up in this thread. I will once again downgrade my firmware packages and try again.

---

### 评论 #38 — agronholm (2025-12-26T01:50:03Z)

> > I tried everything – adding the `cwsr_enable=0` kernel boot parameter, downgrading amd-gpu-firmware to `20251021`. The `clinfo` command still crashes with the error in the topic. Is my only recourse to wait for a firmware package update?
> 
> Looks like you're still using a bad firmware package, I only had this problem with a bad firmware, but never again.
> 
> For me it has been working quite stable. I'm using ROCm 7.1.1 and the following amdgpu kernel parameters: `amdgpu.gpu_recovery=1 amd_pstate=active amdgpu.runpm=1 amdgpu.dpm=1 amdgpu.dcdebugmask=0x10 amdgpu.cwsr_enable=0` And here are my firmware versions:
> 
> ```
> VCE feature version: 0, firmware version: 0x00000000
> UVD feature version: 0, firmware version: 0x00000000
> MC feature version: 0, firmware version: 0x00000000
> ME feature version: 35, firmware version: 0x00000063
> PFP feature version: 35, firmware version: 0x00000067
> CE feature version: 0, firmware version: 0x00000000
> RLC feature version: 1, firmware version: 0x0000008a
> RLC SRLC feature version: 0, firmware version: 0x00000000
> RLC SRLG feature version: 0, firmware version: 0x00000000
> RLC SRLS feature version: 0, firmware version: 0x00000000
> RLCP feature version: 1, firmware version: 0x0000000f
> RLCV feature version: 0, firmware version: 0x00000000
> MEC feature version: 35, firmware version: 0x00000043
> IMU feature version: 0, firmware version: 0x0b012d00
> SOS feature version: 0, firmware version: 0x00000000
> ASD feature version: 553648388, firmware version: 0x21000104
> TA XGMI feature version: 0x00000000, firmware version: 0x00000000
> TA RAS feature version: 0x00000000, firmware version: 0x00000000
> TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
> TA DTM feature version: 0x00000000, firmware version: 0x1200001a
> TA RAP feature version: 0x00000000, firmware version: 0x00000000
> TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
> SMC feature version: 0, program: 0, firmware version: 0x004c5300 (76.83.0)
> SDMA0 feature version: 60, firmware version: 0x00000017
> VCN feature version: 0, firmware version: 0x0911801b
> DMCU feature version: 0, firmware version: 0x00000000
> DMCUB feature version: 0, firmware version: 0x08005500
> TOC feature version: 0, firmware version: 0x0000000b
> MES_KIQ feature version: 6, firmware version: 0x00000106
> MES feature version: 1, firmware version: 0x00000080
> VPE feature version: 0, firmware version: 0x00000000
> VBIOS version: 113-PHXGENERIC-001
> ```
> 
> What are yours?

The MES version is indeed 0x83, even with `amd-gpu-firmware-20251021` installed. There is no older package I could switch to.
My `/proc/cmdline` is: `BOOT_IMAGE=(hd1,gpt2)/vmlinuz-6.17.12-300.fc43.x86_64 root=UUID=c27b11c4-b0d8-4ffe-9304-b12e3e556144 ro rootflags=subvol=root rd.luks.uuid=luks-696e6f7f-f5b7-46a6-a539-d026ea8952f7 rhgb quiet amdgpu.gpu_recovery=1 amd_pstate=active amdgpu.runpm=1 amdgpu.dpm=1 amdgpu.dcdebugmask=0x10 amdgpu.cwsr_enable=0`.

---

### 评论 #39 — amd-nicknick (2025-12-26T07:15:27Z)

Hi @agronholm, since Linux firmware 20251125 did not managed to pick up the MES revert, FC43 now ships with broken 0x83 MES FW.
Please try **updating** your Linux firmware package to **latest**, and overlay the firmware file individually.

Download the firmware directly: https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amdgpu/gc_11_5_0_mes_2.bin?id=3d5c8135206cef364e7d353711b3e7358a90d152
Place the firmware in `/lib/firmware/updates/amdgpu/` with the name `gc_11_5_0_mes_2.bin`, reboot and check with `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info` to see if it's loaded. 
Do not forget to delete it after your distro has provided the rolled-back package.

---

### 评论 #40 — agronholm (2025-12-26T12:31:04Z)

> Hi [@agronholm](https://github.com/agronholm), since Linux firmware 20251125 did not managed to pick up the MES revert, FC43 now ships with broken 0x83 MES FW. Please try **updating** your Linux firmware package to **latest**, and overlay the firmware file individually.
> 
> Download the firmware directly: https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amdgpu/gc_11_5_0_mes_2.bin?id=3d5c8135206cef364e7d353711b3e7358a90d152 Place the firmware in `/lib/firmware/updates/amdgpu/` with the name `gc_11_5_0_mes_2.bin`, reboot and check with `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info` to see if it's loaded. Do not forget to delete it after your distro has provided the rolled-back package.

Tried that, no dice. I updated to the latest fw package, then placed the firmware in the provided location (had to create the `amdgpu` directory there).
```
alex@fedora:~$ ls -l /lib/firmware/updates/amdgpu/
total 252
-rw-r--r--. 1 root root 257184 Dec 26 14:18 gc_11_5_0_mes_2.bin
alex@fedora:~$ sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 35, firmware version: 0x00000020
PFP feature version: 35, firmware version: 0x0000002e
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x11510546
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x11510341
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 35, firmware version: 0x00000020
IMU feature version: 0, firmware version: 0x0b332000
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648388, firmware version: 0x21000104
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x1700004a
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 11, firmware version: 0x0b5d0a00 (93.10.0)
SDMA0 feature version: 60, firmware version: 0x0000000e
VCN feature version: 0, firmware version: 0x0911801b
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x09003500
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000083
VPE feature version: 60, firmware version: 0x00000039
VBIOS version: 113-STRIXEMU-001
```

---

### 评论 #41 — TawusGames (2025-12-26T12:58:46Z)

`cwsr_enable=0` works like a charm.

---

### 评论 #42 — agronholm (2025-12-26T13:34:24Z)

> `cwsr_enable=0` works like a charm.

If you're not on a buggy firmware, sure.

---

### 评论 #43 — da-phil (2025-12-26T13:44:25Z)

> Hi [@agronholm](https://github.com/agronholm), since Linux firmware 20251125 did not managed to pick up the MES revert, FC43 now ships with broken 0x83 MES FW. Please try **updating** your Linux firmware package to **latest**, and overlay the firmware file individually.
> 
> Download the firmware directly: https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amdgpu/gc_11_5_0_mes_2.bin?id=3d5c8135206cef364e7d353711b3e7358a90d152 Place the firmware in `/lib/firmware/updates/amdgpu/` with the name `gc_11_5_0_mes_2.bin`, reboot and check with `cat /sys/kernel/debug/dri/1/amdgpu_firmware_info` to see if it's loaded. Do not forget to delete it after your distro has provided the rolled-back package.

I don't know about the `/lib/firmware/updates` folder. On Ubuntu, I usually pull the latest update from the linux-firmware repo, delete the `/lib/firmware/amdgpu` folder and copy the amdgpu folder there freshly and update the init ramdisk by executing `update-initramfs -u -v -a`.
This works quite well for me.

---

### 评论 #44 — agronholm (2025-12-26T13:49:22Z)

The instructions I was following did not mention running `update-initramfs`. I wonder if that's the problem in my case.

---

### 评论 #45 — waltercool (2025-12-26T14:05:27Z)

Just to stop this massive amount of comments per day. My recommendation is this:

- Create a ticket on your distro reporting this. So other people are not impacted
- Downgrade your firmware to 20251111
- Upgrade your system once a new firmware release is available

Even if you are on a Ubuntu/Fedora with singed firmware, you should be able to downgrade without problems. Don't forget to use cwsr_enable=0 until the new firmware is ready.

---

### 评论 #46 — agronholm (2025-12-26T14:12:23Z)

> Just to stop this massive amount of comments per day. My recommendation is this:
> 
> * Create a ticket on your distro reporting this. So other people are not impacted
> * Downgrade your firmware to 20251111
> * Upgrade your system once a new firmware release is available
> 
> Even if you are on a Ubuntu/Fedora with singed firmware, you should be able to downgrade without problems. Don't forget to use cwsr_enable=0 until the new firmware is ready.

If you've been following the posts so far, I've been trying to find a workaround, so telling me to "just downgrade" is not helpful. There is no working firmware package available on Fedora 43. I don't know what I'm doing w/ the firmware files so I rely completely on assistance provided by others.

---

### 评论 #47 — waltercool (2025-12-26T14:16:33Z)

By installing this, you should be fine. I don't understand where is your problem with the downgrade.

Just be aware this is not a "Linux distro" support thing, so don't expect much support according to your specific distro.

https://koji.fedoraproject.org/koji/buildinfo?buildID=2860445 

Edit: Direct link to RPM just in case, referenced in the previous link: https://kojipkgs.fedoraproject.org//packages/linux-firmware/20251111/1.fc43/src/linux-firmware-20251111-1.fc43.src.rpm

---

### 评论 #48 — drrock77 (2025-12-26T21:09:50Z)

Downgraded firmware and made the cwsr_enable=0  adjustment. Confirming fixed errors on Fedora 43. 

---

### 评论 #49 — Valiant-0 (2025-12-29T01:04:50Z)

> `cwsr_enable=0` works like a charm.

It doesn't. My system suffered a seizure, saw artifacts and almost got thrown into the matrix. I though my GPU almost caught fire.

CachyOS Linux, Kernel Version: 6.18.2-2-cachyos (64-bit)

---

### 评论 #50 — amd-nicknick (2025-12-29T02:10:32Z)

Closing this issue as it is starting to get off topic.
@da-phil, please feel free to reopen this or create a new issue if you encounter crashes after stressing. Thanks!
@Valiant-0, please open a new issue with detailed steps and configuration so we could identify the failure. A distro + kernel version is not enough, attach logs.
@agronholm, for FC43, rollback to this package `amd-gpu-firmware-20251111-1.fc43` or manually overlay the firmware matching your hardware. (Are you on Strix? You'd need 11_5_0 for STX)

---
