# [Issue]: rocm 6.1.0 with wheel pytorch at rx7600xt  and running stable diffusion => HSA_STATUS_ERROR_INVALID_ISA: The instruction set architecture is invalid. code: 0x100f

> **Issue #3054**
> **状态**: closed
> **创建时间**: 2024-04-22T13:27:40Z
> **更新时间**: 2025-01-24T11:39:28Z
> **关闭时间**: 2024-06-21T19:21:22Z
> **作者**: neem693
> **标签**: ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/3054

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

Hi, I have rx 7600 xt. I install rocm 6.1. and today i install wheel pytorch version at venv
http://repo.radeon.com/rocm/manylinux/rocm-rel-6.1/torch-2.1.2%2Brocm6.1-cp310-cp310-linux_x86_64.whl

but when i run that, 
`:0:rocdevice.cpp            :2879: 3764010792 us: [pid:10952 tid:0x75a40ebff640] Callback: Queue 0x75a278c00000 aborting with error : HSA_STATUS_ERROR_INVALID_ISA: The instruction set architecture is invalid. code: 0x100f`
the error occur

Stable diffusion is work with **pytorch with rocm 5.7 version** at venv environment.
but only that is not work at  rocm 6.0 and rocm6.1 pytorch environment 
https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/15434

### Operating System

OS: NAME="Ubuntu" VERSION="22.04.4 LTS (Jammy Jellyfish)"

### CPU

CPU:  model name	: AMD Ryzen 5 5600 6-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen 5 5600 6-Core Processor  
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 5600 6-Core Processor  
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
  Max Clock Freq. (MHz):   3500                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            12                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32775244(0x1f41c4c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32775244(0x1f41c4c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32775244(0x1f41c4c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon™ RX 7600 XT           
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
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2539                               
  BDFID:                   10240                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  SDMA engine uCode::      17                                 
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

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — lovenemesis (2024-04-26T07:44:55Z)

Same issue with Radeon 780M IGP inside 7840U, which is gfx1103.

---

### 评论 #2 — kouta-kun (2024-04-30T19:02:30Z)

Same with RX 7600 on ROCm 6.0.2 on Arch.

---

### 评论 #3 — jnolck (2024-05-07T14:23:11Z)

Same issue here with a SER7 mini pc. AMD Ryzen 7 7840HS w/ Radeon 780M Graphics. rocm 6.0.0 that's bundled with fedora 40. 

One thing that I've noticed is that it won't get triggered if you use 32bit models. The issue only arises when playing with fp16 models or doing fp16 operations. I get so many amdgpu crashes with confyui :(, sometimes it recovers, sometimes it doesn't. 

```shell
May 06 20:52:06.678044 fedora kernel: amdgpu: amdgpu_amdkfd_restore_userptr_worker: Failed to resume KFD
May 06 20:57:48.841133 fedora kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
May 06 20:57:48.842808 fedora kernel: amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
May 06 20:57:48.843368 fedora kernel: amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
May 06 20:57:48.843488 fedora kernel: amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 1
May 06 20:57:48.843587 fedora kernel: amdgpu: Failed to evict process queues
May 06 20:57:48.843598 fedora kernel: amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!

``` 

if I run Confyui like this it'll crash amdgpu during first generation. python main.py --use-split-cross-attention --disable-cuda-malloc --force-fp16 --fp16-unet --fp16-vae. 

```shell
[ 2244.423381] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2244.423555] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[ 2244.423557] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 2244.423562] amdgpu 0000:c6:00.0: amdgpu: Failed to evict queue 1
[ 2244.423563] amdgpu: Failed to evict process queues
[ 2244.423584] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[ 2244.557162] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2244.557331] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2244.686375] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2244.686519] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2244.722199] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2244.826144] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2244.826296] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2244.937723] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2244.955289] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2244.955425] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.084781] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2245.085321] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.153317] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2245.214478] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2245.214612] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.290256] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2245.290416] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2245.345326] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2245.345467] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.419315] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2245.419459] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2245.474638] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2245.474770] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.548276] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2245.548417] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2245.605132] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2245.605280] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.677534] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2245.677671] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2245.734707] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2245.734884] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.805152] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2245.805363] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2245.868985] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2245.869187] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2245.938470] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2245.938672] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2246.002419] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2246.002644] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2246.070654] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2246.070854] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2246.137502] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2246.137685] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2246.203915] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2246.204114] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2246.270888] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 2246.271065] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 2246.337204] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2246.337389] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[ 2246.338964] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[ 2246.373708] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 2246.374197] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[ 2246.374380] [drm] VRAM is lost due to GPU reset!
[ 2246.374383] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[ 2246.375639] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[ 2246.377051] [drm] DMUB hardware initialized: version=0x08003700
[ 2246.600168] [drm] kiq ring mec 3 pipe 1 q 0
[ 2246.601916] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[ 2246.602002] amdgpu 0000:c6:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[ 2246.602537] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 2246.602539] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 2246.602541] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 2246.602543] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 2246.602545] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 2246.602547] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 2246.602549] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 2246.602550] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 2246.602552] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 2246.602554] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 2246.602555] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 2246.602557] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 2246.602559] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 2246.603835] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow start
[ 2246.603837] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow done
[ 2246.603855] amdgpu 0000:c6:00.0: amdgpu: GPU reset(1) succeeded!
[ 2248.012487] rfkill: input handler enabled
[ 2248.272906] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2248.488619] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2248.704623] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2250.079124] rfkill: input handler disabled
[ 2259.685882] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[ 2259.686054] amdgpu 0000:c6:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[ 2259.686057] amdgpu 0000:c6:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 2259.686059] amdgpu 0000:c6:00.0: amdgpu: Failed to remove queue 0
[ 2259.686103] amdgpu 0000:c6:00.0: amdgpu: GPU reset begin!
[ 2259.916472] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2260.133458] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2260.350076] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2260.430349] amdgpu 0000:c6:00.0: amdgpu: MODE2 reset
[ 2260.465620] amdgpu 0000:c6:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 2260.466077] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[ 2260.466159] [drm] VRAM is lost due to GPU reset!
[ 2260.466170] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[ 2260.467166] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[ 2260.468603] [drm] DMUB hardware initialized: version=0x08003700
[ 2260.691721] [drm] kiq ring mec 3 pipe 1 q 0
[ 2260.694214] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[ 2260.694304] amdgpu 0000:c6:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[ 2260.694879] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 2260.694882] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 2260.694884] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 2260.694886] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 2260.694888] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 2260.694889] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 2260.694892] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 2260.694893] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 2260.694894] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 2260.694896] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 2260.694898] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 2260.694900] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 2260.694901] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 2260.696172] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow start
[ 2260.696175] amdgpu 0000:c6:00.0: amdgpu: recover vram bo from shadow done
[ 2260.696194] amdgpu 0000:c6:00.0: amdgpu: GPU reset(2) succeeded!
[ 2261.704123] rfkill: input handler enabled
[ 2261.980781] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2262.196811] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
[ 2262.413335] amdgpu 0000:c6:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - optc1_wait_for_state line:839
``` 
Got lucky it recouped, didn't have to resart!

If I run it like this python main.py --use-split-cross-attention --disable-cuda-malloc I can make a couple of runs before it crashes. If I run it two or three times and then restart the server I can keep it running without bringing down the system for quite a while. 

I have 16gigs of ram assigned as vram via the BIOS. I have this is my .bashrc. 

```shell
export PYTORCH_ROCM_ARCH="gfx1100"
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export HSA_ENABLE_SDMA=0
export PYTORCH_HIP_ALLOC_CONF="garbage_collection_threshold:0.7,max_split_size_mb:1024"

``` 

So frustrated :/. I have question, does this happened with dedicated cards that are unsuported? It it less likely to be like this if I had a real computer with say a 7900GRE? This is just pytorch 6.0 on ROCM 6.0. It's less buggy if I use the ROCM 5.7 version of pytorch. That combo usually just crashes when I run out of memory. 

---

### 评论 #4 — lovenemesis (2024-05-18T04:59:45Z)

> So frustrated :/. I have question, does this happened with dedicated cards that are unsuported? It it less likely to be like this if I had a real computer with say a 7900GRE? This is just pytorch 6.0 on ROCM 6.0. It's less buggy if I use the ROCM 5.7 version of pytorch. That combo usually just crashes when I run out of memory.

Tested the same setup on a 7800XT equipped desktop, Fedora 40 with ROCm 6.0. No such issue.
This mainly affects for integrated GPU, I guess.



---

### 评论 #5 — neem693 (2024-05-18T05:02:39Z)

Seems like same with rx7600 (xt)

2024년 5월 18일 (토) 오후 2:00, Tommy He ***@***.***>님이 작성:

> So frustrated :/. I have question, does this happened with dedicated cards
> that are unsuported? It it less likely to be like this if I had a real
> computer with say a 7900GRE? This is just pytorch 6.0 on ROCM 6.0. It's
> less buggy if I use the ROCM 5.7 version of pytorch. That combo usually
> just crashes when I run out of memory.
>
> Tested the same setup on a 7800XT equipped desktop, Fedora 40 with ROCm
> 6.0. No such issue.
> This mainly affects for integrated GPU, I guess.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/3054#issuecomment-2118641611>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AI5IJS3OXIEEBXT4MTWRQKDZC3N5PAVCNFSM6AAAAABGSZJNPOVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDCMJYGY2DCNRRGE>
> .
> You are receiving this because you authored the thread.Message ID:
> ***@***.***>
>


---

### 评论 #6 — ppanchad-amd (2024-06-21T19:21:10Z)

@neem693 RX 7600XT and is not supported with latest ROCm 6.1.2. Thanks!
@lovenemesis Integrated GPU is not supported with latest ROCm 6.1.2. Thanks!
Closing ticket.

---

### 评论 #7 — david-morris (2024-12-06T13:38:36Z)

> @neem693 RX 7600XT and is not supported with latest ROCm 6.1.2. Thanks! @lovenemesis Integrated GPU is not supported with latest ROCm 6.1.2. Thanks! Closing ticket.

Which ROCm versions support the RX 7600XT?  Is there a container build that should work?  Do specific drivers need to be loaded?  Thanks.

---

### 评论 #8 — staltux (2025-01-24T03:15:44Z)

> > [@neem693](https://github.com/neem693) RX 7600XT and is not supported with latest ROCm 6.1.2. Thanks! [@lovenemesis](https://github.com/lovenemesis) Integrated GPU is not supported with latest ROCm 6.1.2. Thanks! Closing ticket.
> 
> Which ROCm versions support the RX 7600XT? Is there a container build that should work? Do specific drivers need to be loaded? Thanks.

5.7 works, 6.2 not

---

### 评论 #9 — david-morris (2025-01-24T11:35:55Z)

> > > [@neem693](https://github.com/neem693) RX 7600XT and is not supported with latest ROCm 6.1.2. Thanks! [@lovenemesis](https://github.com/lovenemesis) Integrated GPU is not supported with latest ROCm 6.1.2. Thanks! Closing ticket.
> > 
> > 
> > Which ROCm versions support the RX 7600XT? Is there a container build that should work? Do specific drivers need to be loaded? Thanks.
> 
> 5.7 works, 6.2 not

I asked because the 5.7 container did not work.

Oddly enough, since then, the 6.x AUR packages worked.  I'm guessing there's some build-time issues where similar microcodes may have been supported by old firmware?  And then supplying the right microcodes specific to the hardware at build-time lets it run despite being unsupported?

So if anyone is looking at similar problems, the answer might be to figure out which `gfx` version your card takes, make sure that that's supplied in the compile args, and then build against that.  On arch that was just a matter of installing the AUR package and building a venv which included external packages with `--system-site-packages`.

---
