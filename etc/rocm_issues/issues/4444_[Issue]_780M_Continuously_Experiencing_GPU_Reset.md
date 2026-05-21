# [Issue]: 780M Continuously Experiencing GPU Reset

> **Issue #4444**
> **状态**: closed
> **创建时间**: 2025-03-04T06:53:23Z
> **更新时间**: 2025-05-14T19:14:22Z
> **关闭时间**: 2025-05-14T19:12:49Z
> **作者**: MarkTsai1989
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4444

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

I am running YOLOv4 using Python and MIGraphX, and after a period of time, the GPU keeps resetting.

I have also attached the dmesg logs. Let me know if any additional information is needed. Thank you.

### Operating System

24.04.2 LTS (Noble Numbat)
6.11.0-17-generic #17~24.04.2-Ubuntu

### CPU

AMD Ryzen 7 8845HS w/ Radeon 780M Graphics

### GPU

Radeon 780M 

### ROCm Version

6.3.3

### ROCm Component

AMDMIGraphX

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
  Max Clock Freq. (MHz):   5137                               
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
      Size:                    32115312(0x1ea0a70) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32115312(0x1ea0a70) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32115312(0x1ea0a70) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32115312(0x1ea0a70) KB             
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   50688                              
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
  Packet Processor uCode:: 35                                 
  SDMA engine uCode::      16                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16057656(0xf50538) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16057656(0xf50538) KB              
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
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***           

### Additional Information

dmesg output:
[ 1696.619764] perf: interrupt took too long (2513 > 2500), lowering kernel.perf_event_max_sample_rate to 79000
[ 2341.420424] perf: interrupt took too long (3377 > 3141), lowering kernel.perf_event_max_sample_rate to 59000
[ 6703.614427] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 6703.614433] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1004
[ 6703.614435] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 6703.614438] amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 3
[ 6703.614439] amdgpu 0000:c6:00.0: amdgpu: Failed to evict process queues
[ 6703.614493] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[ 6703.614514] amdgpu 0000:c6:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 2 for dev 42086
[ 6703.668586] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 2
[ 6703.668592] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 1
[ 6703.668594] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 0
[ 6705.662884] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 6705.662890] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 6707.047933] iwlwifi 0000:03:00.0: Error sending SYSTEM_STATISTICS_CMD: time out after 2000ms.
[ 6707.047942] iwlwifi 0000:03:00.0: Current CMD queue read_ptr 2272 write_ptr 2273
[ 6707.049577] iwlwifi 0000:03:00.0: Start IWL Error Log Dump:
[ 6707.049580] iwlwifi 0000:03:00.0: Transport status: 0x0000004A, valid: 6
[ 6707.049582] iwlwifi 0000:03:00.0: Loaded firmware version: 89.202a2f7b.0 ty-a0-gf-a0-89.ucode
[ 6707.049585] iwlwifi 0000:03:00.0: 0x00000084 | NMI_INTERRUPT_UNKNOWN       
[ 6707.049587] iwlwifi 0000:03:00.0: 0x000002F0 | trm_hw_status0
[ 6707.049588] iwlwifi 0000:03:00.0: 0x00000000 | trm_hw_status1
[ 6707.049590] iwlwifi 0000:03:00.0: 0x004DAD6C | branchlink2
[ 6707.049591] iwlwifi 0000:03:00.0: 0x00016E0C | interruptlink1
[ 6707.049593] iwlwifi 0000:03:00.0: 0x00016E0C | interruptlink2
[ 6707.049594] iwlwifi 0000:03:00.0: 0x00016AD2 | data1
[ 6707.049596] iwlwifi 0000:03:00.0: 0x01000000 | data2
[ 6707.049598] iwlwifi 0000:03:00.0: 0x00000000 | data3
[ 6707.049599] iwlwifi 0000:03:00.0: 0xE2016114 | beacon time
[ 6707.049601] iwlwifi 0000:03:00.0: 0x803EDEF5 | tsf low
[ 6707.049602] iwlwifi 0000:03:00.0: 0x00000DB5 | tsf hi
[ 6707.049604] iwlwifi 0000:03:00.0: 0x00000000 | time gp1
[ 6707.049605] iwlwifi 0000:03:00.0: 0x8F867527 | time gp2
[ 6707.049613] iwlwifi 0000:03:00.0: 0x00000001 | uCode revision type
[ 6707.049614] iwlwifi 0000:03:00.0: 0x00000059 | uCode version major
[ 6707.049616] iwlwifi 0000:03:00.0: 0x202A2F7B | uCode version minor
[ 6707.049617] iwlwifi 0000:03:00.0: 0x00000420 | hw version
[ 6707.049618] iwlwifi 0000:03:00.0: 0x00C80002 | board version
[ 6707.049620] iwlwifi 0000:03:00.0: 0x80CCF400 | hcmd
[ 6707.049621] iwlwifi 0000:03:00.0: 0x00020000 | isr0
[ 6707.049623] iwlwifi 0000:03:00.0: 0x00000000 | isr1
[ 6707.049624] iwlwifi 0000:03:00.0: 0x48F04002 | isr2
[ 6707.049626] iwlwifi 0000:03:00.0: 0x00C1020C | isr3
[ 6707.049627] iwlwifi 0000:03:00.0: 0x00000000 | isr4
[ 6707.049629] iwlwifi 0000:03:00.0: 0x03D1001C | last cmd Id
[ 6707.049631] iwlwifi 0000:03:00.0: 0x00016AD2 | wait_event
[ 6707.049632] iwlwifi 0000:03:00.0: 0x00000000 | l2p_control
[ 6707.049634] iwlwifi 0000:03:00.0: 0x00000000 | l2p_duration
[ 6707.049636] iwlwifi 0000:03:00.0: 0x00000000 | l2p_mhvalid
[ 6707.049637] iwlwifi 0000:03:00.0: 0x00000000 | l2p_addr_match
[ 6707.049638] iwlwifi 0000:03:00.0: 0x00000018 | lmpm_pmg_sel
[ 6707.049640] iwlwifi 0000:03:00.0: 0x00000000 | timestamp
[ 6707.049641] iwlwifi 0000:03:00.0: 0x00004010 | flow_handler
[ 6707.049680] iwlwifi 0000:03:00.0: Start IWL Error Log Dump:
[ 6707.049682] iwlwifi 0000:03:00.0: Transport status: 0x0000004A, valid: 7
[ 6707.049683] iwlwifi 0000:03:00.0: 0x20000066 | NMI_INTERRUPT_HOST
[ 6707.049685] iwlwifi 0000:03:00.0: 0x00000000 | umac branchlink1
[ 6707.049686] iwlwifi 0000:03:00.0: 0x804838B2 | umac branchlink2
[ 6707.049688] iwlwifi 0000:03:00.0: 0xC00818F8 | umac interruptlink1
[ 6707.049689] iwlwifi 0000:03:00.0: 0x804A051A | umac interruptlink2
[ 6707.049690] iwlwifi 0000:03:00.0: 0x01000000 | umac data1
[ 6707.049691] iwlwifi 0000:03:00.0: 0x804A051A | umac data2
[ 6707.049692] iwlwifi 0000:03:00.0: 0x00000000 | umac data3
[ 6707.049694] iwlwifi 0000:03:00.0: 0x00000059 | umac major
[ 6707.049695] iwlwifi 0000:03:00.0: 0x202A2F7B | umac minor
[ 6707.049696] iwlwifi 0000:03:00.0: 0x8F867525 | frame pointer
[ 6707.049697] iwlwifi 0000:03:00.0: 0xC0886240 | stack pointer
[ 6707.049698] iwlwifi 0000:03:00.0: 0x00E0020F | last host cmd
[ 6707.049700] iwlwifi 0000:03:00.0: 0x00000400 | isr status reg
[ 6707.049711] iwlwifi 0000:03:00.0: IML/ROM dump:
[ 6707.049712] iwlwifi 0000:03:00.0: 0x00000B03 | IML/ROM error/state
[ 6707.049722] iwlwifi 0000:03:00.0: 0x000081A8 | IML/ROM data1
[ 6707.049733] iwlwifi 0000:03:00.0: 0x00000090 | IML/ROM WFPM_AUTH_KEY_0
[ 6707.049739] iwlwifi 0000:03:00.0: Fseq Registers:
[ 6707.049742] iwlwifi 0000:03:00.0: 0x60000000 | FSEQ_ERROR_CODE
[ 6707.049746] iwlwifi 0000:03:00.0: 0x00440007 | FSEQ_TOP_INIT_VERSION
[ 6707.049749] iwlwifi 0000:03:00.0: 0x00080009 | FSEQ_CNVIO_INIT_VERSION
[ 6707.049752] iwlwifi 0000:03:00.0: 0x0000A652 | FSEQ_OTP_VERSION
[ 6707.049756] iwlwifi 0000:03:00.0: 0x00000002 | FSEQ_TOP_CONTENT_VERSION
[ 6707.049759] iwlwifi 0000:03:00.0: 0x4552414E | FSEQ_ALIVE_TOKEN
[ 6707.049762] iwlwifi 0000:03:00.0: 0x00400410 | FSEQ_CNVI_ID
[ 6707.049766] iwlwifi 0000:03:00.0: 0x00400410 | FSEQ_CNVR_ID
[ 6707.049771] iwlwifi 0000:03:00.0: 0x00400410 | CNVI_AUX_MISC_CHIP
[ 6707.049777] iwlwifi 0000:03:00.0: 0x00400410 | CNVR_AUX_MISC_CHIP
[ 6707.049782] iwlwifi 0000:03:00.0: 0x00009061 | CNVR_SCU_SD_REGS_SD_REG_DIG_DCDC_VTRIM
[ 6707.049788] iwlwifi 0000:03:00.0: 0x00000061 | CNVR_SCU_SD_REGS_SD_REG_ACTIVE_VDIG_MIRROR
[ 6707.049791] iwlwifi 0000:03:00.0: 0x00080009 | FSEQ_PREV_CNVIO_INIT_VERSION
[ 6707.049794] iwlwifi 0000:03:00.0: 0x00440007 | FSEQ_WIFI_FSEQ_VERSION
[ 6707.049798] iwlwifi 0000:03:00.0: 0x00440007 | FSEQ_BT_FSEQ_VERSION
[ 6707.049801] iwlwifi 0000:03:00.0: 0x000000F0 | FSEQ_CLASS_TP_VERSION
[ 6707.049813] iwlwifi 0000:03:00.0: UMAC CURRENT PC: 0x804a5578
[ 6707.049817] iwlwifi 0000:03:00.0: LMAC1 CURRENT PC: 0xd0
[ 6707.049933] iwlwifi 0000:03:00.0: WRT: Collecting data: ini trigger 4 fired (delay=0ms).
[ 6707.049937] ieee80211 phy0: Hardware restart was requested
[ 6707.667043] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 6707.667050] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 6707.667498] iwlwifi 0000:03:00.0: HCMD_ACTIVE already clear for command SYSTEM_STATISTICS_CMD
[ 6707.668852] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State
[ 6707.669237] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State Completed
[ 6707.669240] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[ 6707.705080] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 6707.705554] [drm] PCIE GART of 512M enabled (table at 0x000000801FD00000).
[ 6707.706025] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[ 6707.707902] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[ 6707.710300] [drm] DMUB hardware initialized: version=0x08003700
[ 6707.867003] iwlwifi 0000:03:00.0: WFPM_UMAC_PD_NOTIFICATION: 0x20
[ 6707.867079] iwlwifi 0000:03:00.0: WFPM_LMAC2_PD_NOTIFICATION: 0x1f
[ 6707.867150] iwlwifi 0000:03:00.0: WFPM_AUTH_KEY_0: 0x90
[ 6707.867224] iwlwifi 0000:03:00.0: CNVI_SCU_SEQ_DATA_DW9: 0x0
[ 6707.874567] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 6707.874573] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 6707.874575] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 6707.874576] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 6707.874578] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 6707.874579] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 6707.874580] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 6707.874582] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 6707.874583] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 6707.874585] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 6707.874586] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 6707.874587] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 6707.874589] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 6707.922678] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow start
[ 6707.922686] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow done
[ 6707.922705] amdgpu 0000:c6:00.0: amdgpu: GPU reset(1) succeeded!
[ 7749.262254] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 7749.262258] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1004
[ 7749.262261] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 7749.262263] amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 3
[ 7749.262265] amdgpu 0000:c6:00.0: amdgpu: Failed to evict process queues
[ 7749.262346] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[ 7749.262360] amdgpu 0000:c6:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 2 for dev 42086
[ 7749.291865] pcieport 0000:00:08.1: PME: Spurious native interrupt!
[ 7749.352164] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 2
[ 7749.352170] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 1
[ 7749.352172] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 0
[ 7751.302105] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 7751.302110] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 7753.306259] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 7753.306266] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 7753.307989] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State
[ 7753.308375] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State Completed
[ 7753.308379] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[ 7753.343958] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 7753.344429] [drm] PCIE GART of 512M enabled (table at 0x000000801FD00000).
[ 7753.344743] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[ 7753.345725] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[ 7753.348004] [drm] DMUB hardware initialized: version=0x08003700
[ 7753.512132] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 7753.512137] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 7753.512139] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 7753.512140] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 7753.512142] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 7753.512143] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 7753.512144] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 7753.512145] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 7753.512147] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 7753.512148] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 7753.512149] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 7753.512151] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 7753.512152] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 7753.577588] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow start
[ 7753.577594] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow done
[ 7753.577619] amdgpu 0000:c6:00.0: amdgpu: GPU reset(2) succeeded!
[ 7935.484520] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 7935.484526] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1004
[ 7935.484528] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 7935.484531] amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 3
[ 7935.484533] amdgpu 0000:c6:00.0: amdgpu: Failed to evict process queues
[ 7935.484535] amdgpu: Failed to quiesce KFD
[ 7935.484555] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[ 7935.484569] amdgpu 0000:c6:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 2 for dev 42086
[ 7935.592600] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 2
[ 7935.592605] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 1
[ 7935.592607] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 0
[ 7937.520319] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 7937.520325] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 7939.524467] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 7939.524472] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 7939.526182] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State
[ 7939.526573] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State Completed
[ 7939.526579] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[ 7939.561671] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 7939.561945] [drm] PCIE GART of 512M enabled (table at 0x000000801FD00000).
[ 7939.561988] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[ 7939.562421] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[ 7939.563882] [drm] DMUB hardware initialized: version=0x08003700
[ 7939.728911] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 7939.728917] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 7939.728919] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 7939.728920] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 7939.728921] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 7939.728923] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 7939.728924] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 7939.728925] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 7939.728927] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 7939.728928] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 7939.728929] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 7939.728931] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 7939.728932] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 7939.793191] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow start
[ 7939.793197] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow done
[ 7939.793234] amdgpu 0000:c6:00.0: amdgpu: GPU reset(3) succeeded!
[ 8061.008271] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 8061.008277] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1004
[ 8061.008279] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 8061.008281] amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 3
[ 8061.008284] amdgpu 0000:c6:00.0: amdgpu: Failed to evict process queues
[ 8061.008285] amdgpu: Failed to quiesce KFD
[ 8061.008310] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[ 8061.008338] amdgpu 0000:c6:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 2 for dev 42086
[ 8061.075834] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 2
[ 8061.075839] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 1
[ 8061.075841] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 0
[ 8063.054352] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 8063.054357] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 8065.058491] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 8065.058497] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 8065.060506] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State
[ 8065.060882] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State Completed
[ 8065.060885] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[ 8065.095936] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 8065.096485] [drm] PCIE GART of 512M enabled (table at 0x000000801FD00000).
[ 8065.096584] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[ 8065.097823] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[ 8065.099417] [drm] DMUB hardware initialized: version=0x08003700
[ 8065.263088] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 8065.263093] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 8065.263095] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 8065.263096] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 8065.263098] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 8065.263099] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 8065.263100] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 8065.263102] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 8065.263103] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 8065.263104] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 8065.263106] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 8065.263107] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 8065.263108] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 8065.327894] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow start
[ 8065.327897] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow done
[ 8065.327911] amdgpu 0000:c6:00.0: amdgpu: GPU reset(4) succeeded!
[ 8186.471287] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 8186.471293] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1004
[ 8186.471295] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 8186.471298] amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 3
[ 8186.471301] amdgpu 0000:c6:00.0: amdgpu: Failed to evict process queues
[ 8186.471302] amdgpu: Failed to evict queues of pasid 0x8002
[ 8186.471320] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[ 8186.471333] amdgpu 0000:c6:00.0: amdgpu: remove_all_queues_mes: Failed to remove queue 2 for dev 42086
[ 8186.806640] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 2
[ 8186.806646] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 1
[ 8186.806647] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 0
[ 8188.506347] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 8188.506353] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 8190.510485] amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 8190.510490] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 8190.512207] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State
[ 8190.512578] amdgpu 0000:c6:00.0: amdgpu: Dumping IP State Completed
[ 8190.512580] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[ 8190.548326] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 8190.548993] [drm] PCIE GART of 512M enabled (table at 0x000000801FD00000).
[ 8190.549161] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[ 8190.552550] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[ 8190.554865] [drm] DMUB hardware initialized: version=0x08003700
[ 8190.719222] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 8190.719227] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 8190.719229] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 8190.719230] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 8190.719232] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 8190.719233] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 8190.719234] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 8190.719235] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 8190.719237] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 8190.719238] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 8190.719239] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 8190.719241] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 8190.719242] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 8190.784164] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow start
[ 8190.784168] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow done
[ 8190.784189] amdgpu 0000:c6:00.0: amdgpu: GPU reset(5) succeeded!

---

## 评论 (14 条)

### 评论 #1 — ppanchad-amd (2025-03-04T17:04:24Z)

Hi @MarkTsai1989. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — MarkTsai1989 (2025-03-05T02:48:21Z)

Hi @ppanchad-amd ,

If you need me to help with testing or if any information is missing, please let me know. Thank you!

---

### 评论 #3 — darren-amd (2025-03-11T14:17:54Z)

Hi @MarkTsai1989,

Could you please provide the complete dmesg dump, as well more details about the workload you are running? Steps to reproduce the issue would be helpful, thanks!

---

### 评论 #4 — MarkTsai1989 (2025-03-14T08:28:20Z)

Hi @darren-amd ,

We are using YOLO v4 with MIGraphX, running inference continuously in a for loop.
The system's CPU load average is around 4.

[kernel_log.txt](https://github.com/user-attachments/files/19244051/kernel_log.txt)



---

### 评论 #5 — MarkTsai1989 (2025-03-14T09:32:42Z)

This is the time spent on each reset and the time it occurred.

I use this logs:
Mar 14 07:35:34 kernel: amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
Mar 14 07:35:39 kernel: amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Mar 14 07:35:42 kernel: amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Mar 14 07:35:44 kernel: amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Mar 14 07:35:49 kernel: amdgpu 0000:c6:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Mar 14 07:35:49 kernel: amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!


![Image](https://github.com/user-attachments/assets/a9102f12-9cc7-49c9-bb05-3604dcc923f5)

---

### 评论 #6 — darren-amd (2025-03-17T15:12:32Z)

Could you provide more information on what you are running and how you are running it? Complete steps for reproduction would be helpful for me to investigate further. Also, could you try setting `HSA_OVERRIDE_GFX_VERSION=11.0.0` before running the workload? Thanks!

---

### 评论 #7 — MarkTsai1989 (2025-04-01T08:28:08Z)

Hi @darren-amd  @ppanchad-amd ,

We recently tested 20 machines of this model (AMD Ryzen 7 8845HS w/ Radeon 780M Graphics), and all of them consistently experienced GPU crashes.

Additionally, we observed that all processes utilizing the GPU, such as the process using VAAPI for decoding H.264, would be restarted.

I created a simple test program based on our usage scenario:

1. Run ai_server.py.

2. Run start_clients.sh, which starts 15 processes. Each process uses VAAPI to decode a test video and sends the frames to ai_server.

3.Increase CPU load:
stress-ng --cpu 8

https://drive.google.com/file/d/1FscP7BbW9eSoKcX1chbA1aqXpeqHRtUa/view?usp=sharing


---

### 评论 #8 — darren-amd (2025-04-01T13:40:10Z)

Hi @MarkTsai1989,

Could you upload the reproducer somewhere on github? I cannot access the drive. Thanks!

---

### 评论 #9 — MarkTsai1989 (2025-04-01T15:15:20Z)

Hi @darren-amd ,

I have uploaded the code to my private repo and invited you.
Please check it when you have time. Thanks!

---

### 评论 #10 — MarkTsai1989 (2025-04-15T05:30:29Z)

Hi @darren-amd ,

May I ask if you’ve found anything regarding this issue?

---

### 评论 #11 — MarkTsai1989 (2025-04-24T07:09:21Z)

Hi @darren-amd ,

May I ask if you’ve found anything regarding this issue?

---

### 评论 #12 — lucbruni-amd (2025-04-25T15:01:13Z)

Hi @MarkTsai1989,

The 780M is not supported by the current ROCm ecosystem as of your version according to the [compatibility requirements](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/native_linux/native_linux_compatibility.html) for ROCm on Radeon. This is consistent with your tests involving 20 machines with the same setup. If you have a supported device onsite, could you test your workload so that we can confirm whether the issue is a result of an unsupported device? Thanks!

---

### 评论 #13 — MarkTsai1989 (2025-04-28T14:46:35Z)

Your response is somewhat disappointing. It has been almost three months since I first reported this issue, and the result is simply being told that the current ROCm version does not support the 780M .

---

### 评论 #14 — darren-amd (2025-05-14T18:48:07Z)

Hi @MarkTsai1989,

I understand your frustration, however as @lucbruni-amd mentioned, as ROCm does not officially support the 780M, certain workloads may be unstable and fail as you have experienced. We do have a forum here: https://github.com/ROCm/ROCm/discussions/4276 that discusses adding further hardware support.


---
