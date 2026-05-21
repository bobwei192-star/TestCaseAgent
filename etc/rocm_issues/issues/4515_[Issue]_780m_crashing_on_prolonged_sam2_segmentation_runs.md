# [Issue]: 780m crashing on prolonged sam2 segmentation runs

> **Issue #4515**
> **状态**: closed
> **创建时间**: 2025-03-19T23:18:43Z
> **更新时间**: 2025-05-14T18:44:57Z
> **关闭时间**: 2025-05-14T18:44:56Z
> **作者**: Clyde-fare
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4515

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I see GPU hangs trying to sam2 video segmentation runs on >600 frames.



### Operating System

Ubuntu 24.04.2 LTS (Noble Numbat)

### CPU

AMD Ryzen 9 7940HS

### GPU

780M

### ROCm Version

6.3.3

### ROCm Component

_No response_

### Steps to Reproduce

I'm running a fairly vanilla application of the sam2 video predictor (https://github.com/facebookresearch/sam2/blob/main/sam2/sam2_video_predictor.py) . If I try to run with  async_loading_frames=True which interleaves cpu bound and gpu operations it very rapidly crashes, while if i leave async_loading_frames=False it can sometimes succeed or atleast it has done for ~350 frames but trying to process 900 frames i've had crashes at 38% and ~55% completition.

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
  Name:                    AMD Ryzen 9 7940HS w/ Radeon 780M Graphics                                                                                                                                                                                                           
  Uuid:                    CPU-XX                                                                                                                                                                                                                                               
  Marketing Name:          AMD Ryzen 9 7940HS w/ Radeon 780M Graphics                                                                                                                                                                                                           
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
  Max Clock Freq. (MHz):   5263                                                                                                                                                                                                                                                 
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
      Segment:                 GLOBAL; FLAGS: FINE GRAINED                                                                                                                                                                                                    23:12:14 [64/1685]
      Size:                    24390916(0x1742d04) KB               
      Allocatable:             TRUE                                 
      Alloc Granule:           4KB                                  
      Alloc Recommended Granule:4KB                                                                                                     
      Alloc Alignment:         4KB                                  
      Accessible by all:       TRUE                                 
    Pool 2                                                          
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED                                                                     
      Size:                    24390916(0x1742d04) KB               
      Allocatable:             TRUE                                 
      Alloc Granule:           4KB                                  
      Alloc Recommended Granule:4KB                                                                                                     
      Alloc Alignment:         4KB                                  
      Accessible by all:       TRUE                                 
    Pool 3                                                          
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED                                                                     
      Size:                    24390916(0x1742d04) KB               
      Allocatable:             TRUE                                 
      Alloc Granule:           4KB                                  
      Alloc Recommended Granule:4KB                                                                                                     
      Alloc Alignment:         4KB                                  
      Accessible by all:       TRUE                                 
    Pool 4                                                          
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED        
      Size:                    24390916(0x1742d04) KB                                                                                   
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
  Chip ID:                 5567(0x15bf)                             
  ASIC Revision:           7(0x7)                                   
  Cacheline Size:          64(0x40)                                 
  Max Clock Freq. (MHz):   2799                                                                                                         
  BDFID:                   50432                                                                                                        
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 40                                 
  SDMA engine uCode::      21                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12195456(0xba1680) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    12195456(0xba1680) KB              
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

dmesg:

[121586.896040] workqueue: kfd_process_wq_release [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND                                                                                                                                                    
[121731.010650] workqueue: svm_range_deferred_list_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND                                                                                                                                              
[121734.463587] workqueue: kfd_process_wq_release [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND                                                                                                                                                    
[122308.716084] workqueue: svm_range_deferred_list_work [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND                                                                                                                                              
[126901.857354] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE                                                  
[126901.857364] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002                                                                                                                                                                          
[126901.857369] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset                                                                                                                                                                             
[126901.857374] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1                                                                    
[126901.857377] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues                                                                                                                                                                                                     
[126901.857417] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!                                                                                                                                                                                                                   
[126901.857441] amdgpu 0000:c5:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 0 for dev 43622                              
[126901.857469] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State                                                                           
[126901.859606] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed                                                                                                                                                                                                         
[126903.428164] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0                                                                                                                                                                                                           
[126904.526999] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND                                                       
[126904.527008] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs                                                                                                                                                                                           
[126904.527175] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <mes_v11_0> failed -110                                                                                                                                                              
[126907.204778] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE                                                                                                                                                                                          
[126907.204788] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue                                                                                                                                                                               
[126908.873132] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)                                                                                                                                                                             
[126908.873152] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                                                                                                                                                                    
[126908.873165] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53                                                                                                                                                                                         
[126908.873175] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CPC (0x5)                                                                                                                                                                                              
[126908.873184] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x1                                                                                                                                                                                                               
[126908.873191] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x1                                                                                                                                                                                                              
[126908.873198] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x5                                                                 
[126908.873206] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x1                                                                                                                                                                                                             
[126908.873213] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x1                                                                                                                                                                                                                        
[126908.873232] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)                                                                                                                                                                             
[126908.873243] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                                                                                                                                                                    
[126908.873253] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000                                                 
[126908.873262] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CB/DB (0x0)                                                    
[126908.873271] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x0   
[126908.873278] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0  
[126908.873285] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x0                                                                 
[126908.873293] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0 
[126908.873300] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0            
[126909.885470] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE                                                  
[126909.885481] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue                                       
[126910.876927] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)                                     
[126910.876949] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                            
[126910.876963] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53                                                 
[126910.876973] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CPC (0x5)                                                      
[126910.876982] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x1   
[126910.876991] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x1  
[126910.876998] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x5                                                                 
[126910.877006] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x1 
[126910.877014] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x1            
[126910.877034] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)                                     
[126910.877046] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                            
[126910.877058] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000                                                 
[126910.877067] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CB/DB (0x0)                                                    
[126910.877077] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x0   
[126910.877084] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0  
[126910.877092] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x0                                                                 
[126910.877100] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0 
[126910.877107] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0            
[126910.877126] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)                                     
[126910.877137] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                            
[126910.877148] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000                                                 
[126910.877158] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CB/DB (0x0)                                                    
[126910.877167] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x0   
[126910.877174] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0 
[126910.877174] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0  
[126910.877182] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x0                                                                 
[126910.877190] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0 
[126910.877197] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0            
[126910.877216] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)                                     
[126910.877227] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                            
[126910.877237] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000                                                 
[126910.877247] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CB/DB (0x0)                                                    
[126910.877256] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x0   
[126910.877263] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0  
[126910.877271] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x0                                                                 
[126910.877279] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0 
[126910.877286] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0            
[126910.877305] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)                                     
[126910.877315] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                            
[126910.877326] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000                                                 
[126910.877335] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CB/DB (0x0)                                                    
[126910.877344] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x0   
[126910.877352] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0  
[126910.877359] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x0                                                                 
[126910.877367] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0 
[126910.877375] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0            
[126910.877393] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)                                     
[126910.877404] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                            
[126910.877415] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000                                                 
[126910.877424] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CB/DB (0x0)                                                    
[126910.877433] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x0   
[126910.877441] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0  
[126910.877448] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x0                                                                 
[126910.877456] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0 
[126910.877464] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0            
[126910.877482] amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)                                     
[126910.877493] amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10                            
[126910.877504] amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000                                                 
[126910.877513] amdgpu 0000:c5:00.0: amdgpu:     Faulty UTCL2 client ID: CB/DB (0x0)                                                    
[126910.877522] amdgpu 0000:c5:00.0: amdgpu:     MORE_FAULTS: 0x0   
[126910.877530] amdgpu 0000:c5:00.0: amdgpu:     WALKER_ERROR: 0x0  
[126910.877537] amdgpu 0000:c5:00.0: amdgpu:     PERMISSION_FAULTS: 0x0                                                                 
[126910.877545] amdgpu 0000:c5:00.0: amdgpu:     MAPPING_ERROR: 0x0 
[126910.877553] amdgpu 0000:c5:00.0: amdgpu:     RW: 0x0            
[126912.591545] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE                                                  
[126912.591555] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue                                       
[126914.884572] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE                                                  
[126914.884583] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue                                       
[126914.886335] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset            
[126914.917110] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume                                                      
[126914.917567] [drm] PCIE GART of 512M enabled (table at 0x00000081FFD00000).                                                          
[126914.917798] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...     
[126914.920052] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!                                                               
[126914.926447] [drm] DMUB hardware initialized: version=0x08004500 
[126914.927258] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0                                                  
[126914.927260] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0                                                 
[126914.927261] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0                                                 
[126914.927262] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0                                                 
[126914.927263] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0                                                 
[126914.927265] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0   
[126914.927266] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0                                                 
[126914.927267] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0                                                
[126914.927268] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0                                                
[126914.927269] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0                                                     
[126914.927271] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8                                              
[126914.927272] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8                                                   
[126914.927273] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0                                             
[126914.928994] amdgpu 0000:c5:00.0: amdgpu: GPU reset(3) succeeded!                                

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-03-20T14:10:51Z)

Hi @Clyde-fare. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — darren-amd (2025-03-20T15:11:50Z)

Hi @Clyde-fare,

Could you please provide the full `dmesg` dump? Thanks!

---

### 评论 #3 — Clyde-fare (2025-03-21T23:50:56Z)

[dmesg.txt](https://github.com/user-attachments/files/19398711/dmesg.txt)

---

### 评论 #4 — darren-amd (2025-05-14T18:44:56Z)

Hi @Clyde-fare,

We don't officially support the 780M on ROCm, according to our [Compatibility Matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html). Because of this, you may run into instability as you have experienced.

---
