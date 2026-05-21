# [Issue]: 7900xtx system hang - full lock

> **Issue #2689**
> **状态**: closed
> **创建时间**: 2023-12-05T23:06:32Z
> **更新时间**: 2024-02-09T04:32:58Z
> **关闭时间**: 2024-02-09T04:28:37Z
> **作者**: terryrankine
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2689

## 描述

### Problem Description

start the machine up
start stable diffusion 
wait until the gpu gets used by chrome and pytorch
[recent.errors.txt](https://github.com/RadeonOpenCompute/ROCm/files/13573816/recent.errors.txt)

```Dec  2 22:11:34 theblob kernel: [ 2649.203914] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Dec  2 22:11:34 theblob kernel: [ 2649.204158] amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Dec  2 22:11:34 theblob kernel: [ 2649.204160] amdgpu: MES might be in unrecoverable state, issue a GPU reset
Dec  2 22:11:34 theblob kernel: [ 2649.204164] amdgpu: Failed to evict queue 1
Dec  2 22:11:34 theblob kernel: [ 2649.204166] amdgpu: Failed to evict process queues
Dec  2 22:11:34 theblob kernel: [ 2649.204195] amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
Dec  2 22:11:35 theblob kernel: [ 2650.229025] amdgpu 0000:2f:00.0: amdgpu: IP block:gfx_v11_0 is hung!
```

after using `sudo rocm-smi --gpureset -d 0` sometimes it works again - but hangs x/wayland

only real fix it cold power off


### Operating System

22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 5 3600X 6-Core Processor

### GPU

Radeon RX 7900 XTX   

### ROCm Version

5.7.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### Output of /opt/rocm/bin/rocminfo --support

```
terryr@theblob:~$ /opt/rocm/bin/rocminfo --support
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
  Name:                    AMD Ryzen 5 3600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 3600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   3800                               
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
      Size:                    98782896(0x5e34eb0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98782896(0x5e34eb0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98782896(0x5e34eb0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-f4b3a217836b48ac               
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
  BDFID:                   12032                              
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
  Packet Processor uCode:: 550                                
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

---

## 评论 (26 条)

### 评论 #1 — terryrankine (2023-12-05T23:08:30Z)

anytime you see this - its game over

```Dec  2 21:11:18 theblob kernel: [  235.579441] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
Dec  2 21:11:18 theblob kernel: [  235.579692] amdgpu: failed to add hardware queue to MES, doorbell=0x1216
Dec  2 21:11:18 theblob kernel: [  235.579694] amdgpu: MES might be in unrecoverable state, issue a GPU reset
Dec  2 21:11:18 theblob kernel: [  235.579698] amdgpu: Failed to restore queue 3
Dec  2 21:11:18 theblob kernel: [  235.579700] amdgpu: Failed to restore process queues
Dec  2 21:11:18 theblob kernel: [  235.579718] amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
Dec  2 21:11:18 theblob kernel: [  235.584623] amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow start
Dec  2 21:11:18 theblob kernel: [  235.585826] amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow done
Dec  2 21:11:18 theblob kernel: [  235.706794] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec  2 21:11:18 theblob kernel: [  235.707164] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec  2 21:11:18 theblob kernel: [  235.823092] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec  2 21:11:18 theblob kernel: [  235.823370] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec  2 21:11:18 theblob kernel: [  235.940007] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec  2 21:11:18 theblob kernel: [  235.940294] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
```

---

### 评论 #2 — terryrankine (2023-12-12T00:51:40Z)

```
ec 12 08:44:37 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Dec 12 08:44:37 theblob kernel: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Dec 12 08:44:37 theblob kernel: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Dec 12 08:44:37 theblob kernel: amdgpu: Failed to evict queue 1
Dec 12 08:44:37 theblob kernel: amdgpu: Failed to evict process queues
Dec 12 08:44:37 theblob kernel: amdgpu: Failed to evict queues of pasid 0x8005
Dec 12 08:44:37 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
Dec 12 08:44:38 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: IP block:gfx_v11_0 is hung!
Dec 12 08:44:38 theblob kernel: [drm] kiq ring mec 3 pipe 1 q 0
Dec 12 08:44:38 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow start
Dec 12 08:44:38 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow done
Dec 12 08:44:38 theblob firefox.desktop[6794]: [GFX1-]: GFX: RenderThread detected a device reset in PostUpdate
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:39 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:39 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1800
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1800
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:40 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:40 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:41 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:41 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:41 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 12 08:44:41 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 12 08:44:41 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
Dec 12 08:44:41 theblob kernel: [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1a00
Dec 12 08:44:41 theblob kernel: [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
Dec 12 08:44:41 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GPU reset(1) succeeded!
```

EXCEPT.....
The GPU pipe is at zero percent - stable diffusion is going no where, and when I close /kill stable diffusion - the pipe goes to 100% and i cant use it again till i reboot....



---

### 评论 #3 — terryrankine (2023-12-12T00:52:03Z)

looks like a timeout - three retries, a reset retry, and then dead.

---

### 评论 #4 — VeryUnstableRice (2023-12-12T13:41:12Z)

same card, same problem, same errors. It is not happening only to stable diffusion, but to torch processes that take too much VRAM. If I keep the task under 12GB of VRAM the crash does not happen. I assume what's happening is due to the card getting too hot, trying to slow down and the driver mistakes it for a card crash and restarts itself. Or maybe it is due to my motherboard(asus x570 series, I might change it at the recommendation of any rocm dev).

---

### 评论 #5 — terryrankine (2023-12-12T21:46:29Z)

Just to be clear. My GPU monitor is not showing that the GPU memory is full. 
Memory sits at about 10gb used and still crashes. 

The application `amdgpu_top` indicates most of the time full power, but still shows lots of thermal warnings. 

---

### 评论 #6 — terryrankine (2023-12-13T00:29:19Z)

[last100.txt](https://github.com/ROCm/ROCm/files/13654481/last100.txt)
[crash.json](https://github.com/ROCm/ROCm/files/13654483/crash.json)

Attached is the continous output from `amdgou_top` and the journal of the last crash.

the memory used at point of crash was 16319mb

I need know what else to supply

---

### 评论 #7 — terryrankine (2023-12-13T02:01:57Z)

trying new drivers - 5.7.3 released

---

### 评论 #8 — terryrankine (2023-12-13T07:27:43Z)

![image](https://github.com/ROCm/ROCm/assets/1403892/d3c6ed14-c293-44cd-801e-25f0c081f608)
nope - still crashing

---

### 评论 #9 — terryrankine (2023-12-13T07:28:44Z)

then once i kill the process

![image](https://github.com/ROCm/ROCm/assets/1403892/80524e8c-bdb0-468b-b7c2-afecc6d39884)


---

### 评论 #10 — terryrankine (2023-12-14T08:22:48Z)

repeated tests overnight with new 5.7.3 drivers

If the memory is kept low - the card keeps working..... 

@VeryUnstableRice is correct in the assessment....

As soon as i go to 17-20GB usage I can get it to fault within minutes....

Its not over allocation of memory from the app either - I can make it OOM fault too - which is a different error, not the driver/card crashing.


---

### 评论 #11 — terryrankine (2023-12-14T08:24:45Z)

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
  Name:                    AMD Ryzen 5 3600X 6-Core Processor 
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 5 3600X 6-Core Processor 
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
  Max Clock Freq. (MHz):   3800                               
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
      Size:                    98783208(0x5e34fe8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    98783208(0x5e34fe8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    98783208(0x5e34fe8) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-f4b3a217836b48ac               
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
  BDFID:                   12032                              
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
  Packet Processor uCode:: 550                                
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
*** Done ***  ```

---

### 评论 #12 — terryrankine (2023-12-14T08:25:52Z)

```
terryr@theblob:~$ dkms status 
amdgpu/6.2.4-1697730.22.04, 6.2.0-37-generic, x86_64: installed
amdgpu/6.2.4-1697730.22.04, 6.2.0-39-generic, x86_64: installed
terryr@theblob:~$ uname -a
Linux theblob 6.2.0-39-generic #40~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 16 10:53:04 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

---

### 评论 #13 — VeryUnstableRice (2023-12-14T18:21:11Z)

I think that I solved the issue. I don't know what fixed it, but I suspect that my current kernel would be the one which solved it. Try installing '6.7.0-rc4-1-amd-drm-fixes', maybe it will do it for you. I will train a GAN to see it how it behaves.

---

### 评论 #14 — terryrankine (2023-12-14T23:44:58Z)

where did you find this kernel? I cant seem to find that tag anywhere

---

### 评论 #15 — VeryUnstableRice (2023-12-14T23:52:56Z)

https://gitlab.freedesktop.org/agd5f/linux/-/tree/drm-fixes-6.7?ref_type=heads
yeah, it still happens at 22gb vram. The good news are that I can use more vram now, and not worry. Post your issue here too https://gitlab.freedesktop.org/drm/amd/-/issues

---

### 评论 #16 — VeryUnstableRice (2023-12-15T21:41:36Z)

the crash still happens but it's less often. Can you try running something that would normally crash you card in tty, with everything wayland or xorg related killed? I have a suspicion that xwayland is at play here, but I'm not sure


---

### 评论 #17 — terryrankine (2023-12-18T13:16:20Z)

I tried the ubuntu mesa git repo (there is a ppa for auto builds) - no joy - didnt make a difference

I tried the 6.0 rocm and driver bundle
its WAY more stable - but - I get this.... on one monitor - but no log entries when it flicks on and off...
![image](https://github.com/ROCm/ROCm/assets/1403892/85cee1ec-3a52-4fe9-8315-dd968d9d1ad9)

it flickers - you can change refresh rate, and it goes away, then comes back.

No log entries when it happens - just flicker, sometimes it recovers, sometimes it doesnt. I have tried every refresh rate going slower and slower and still not solved it.



---

### 评论 #18 — terryrankine (2023-12-19T03:51:56Z)

adding crosslink. 
https://gitlab.freedesktop.org/drm/amd/-/issues/3063

---

### 评论 #19 — terryrankine (2024-01-25T04:11:10Z)

so - running ubuntu 6.5 kernel now, 
`Linux theblob 6.5.0-17-generic #17~22.04.1-Ubuntu `

and the newest rocm 6.0.1
deb https://repo.radeon.com/amdgpu/6.0.1/ubuntu jammy main

and have the active module installed
```terryr@theblob:~$ modinfo amdgpu 
filename:       /lib/modules/6.5.0-17-generic/updates/dkms/amdgpu.ko
version:        6.3.6
license:        GPL and additional rights
description:    AMD GPU
author:         AMD linux driver team
```

and i still get this 
```Jan 25 11:50:13 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Jan 25 11:50:13 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Jan 25 11:50:13 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Jan 25 11:50:13 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: Failed to evict queue 1
Jan 25 11:50:13 theblob kernel: amdgpu: Failed to evict process queues
Jan 25 11:50:13 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
Jan 25 11:50:13 theblob kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 8 times, consider switching to WQ_UNBOUND
Jan 25 11:50:13 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 11:50:13 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 11:50:13 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 11:50:13 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: IP block:gfx_v11_0 is hung!
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          MORE_FAULTS: 0x1
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          WALKER_ERROR: 0x1
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          MAPPING_ERROR: 0x1
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          RW: 0x1
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          MORE_FAULTS: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          WALKER_ERROR: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          MAPPING_ERROR: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          RW: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          MORE_FAULTS: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          WALKER_ERROR: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          MAPPING_ERROR: 0x0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu:          RW: 0x0
Jan 25 11:50:14 theblob kernel: [drm] kiq ring mec 3 pipe 1 q 0
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow start
Jan 25 11:50:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow done
Jan 25 11:50:14 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 11:50:14 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 11:50:14 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 11:50:14 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 11:50:14 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 11:50:14 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 11:50:14 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 11:50:14 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 11:50:15 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
```
it still locks up - and it still wont let go when it crashes.

![image](https://github.com/ROCm/ROCm/assets/1403892/41a53646-7d70-42b1-8f2a-86e857456e81)



---

### 评论 #20 — terryrankine (2024-01-25T07:29:32Z)

Im doing awesome now.

I can get it to crash in 4mins....

```terryr@theblob:~$ uptime
 15:26:48 up 4 min,  1 user,  load average: 1.83, 1.13, 0.49
```

```Jan 25 15:26:24 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Jan 25 15:26:24 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Jan 25 15:26:24 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Jan 25 15:26:24 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: Failed to evict queue 1
Jan 25 15:26:24 theblob kernel: amdgpu: Failed to evict process queues
Jan 25 15:26:24 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
Jan 25 15:26:24 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 15:26:24 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 15:26:24 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Jan 25 15:26:24 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Jan 25 15:26:25 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: IP block:gfx_v11_0 is hung!
```

this is only at the 16gb used marker too - 
```   16642M / 24476M VRAM  67.99% ```

---

### 评论 #21 — VeryUnstableRice (2024-02-03T13:35:54Z)

did you do what I suggested and increase the fan speed?

---

### 评论 #22 — terryrankine (2024-02-04T13:37:45Z)

yeah - and I have a 200mm noctua fan just resting on the top of the card.

GPU edge and junction dont get past 85 deg c with the fans on... so not likely temp

---

### 评论 #23 — terryrankine (2024-02-06T13:33:04Z)

I now have pytorch compiling locally, installing into virtual env, against the 6.0.2 binaries for ROCM.

I will stress test it tomorrow (when the sun is powering the GPU)

if i have something wrong - here is the build script - and I DONT care how bad it is - its just for transparency.


```
terryr@theblob:~$ cat ./local_build.sh 

source /mnt/data/automatic1111/stable-diffusion-webui/venv/bin/activate

export PYTORCH_ROCM_ARCH=gfx1100

export USE_NINJA=1
export USE_CUDA=0 
export USE_ROCM=1 
export USE_LMDB=1 
export USE_OPENCV=1 
export MAX_JOBS=10


cd pytorch
git pull --recurse-submodules
git pull

python tools/amd_build/build_amd.py
python setup.py build install

./.ci/pytorch/build.sh


cd ..


cd vision
git pull --recurse-submodules 

python setup.py develop

python setup.py build install

cd ..


cd audio

git pull --recurse-submodules 
python setup.py develop

python setup.py build install

cd ..
```



---

### 评论 #24 — terryrankine (2024-02-09T04:27:49Z)

I have run pretty agressively over the last 3 days.

I am on stock 22.04 lts kernel - `Linux theblob 6.5.0-17-generic #17~22.04.1-Ubuntu`
I have custom pytorch/vision/audio installed
I have nightly mesa ppa

I can not fault the current driver - 6.0.2 seems to play well with my kernel, and my pytorch nightly.

I have to declare this as 'working without root-cause ever identified.....'


---

### 评论 #25 — terryrankine (2024-02-09T04:28:37Z)

Pity there is no real info here. closing.

---

### 评论 #26 — terryrankine (2024-02-09T04:32:57Z)

#rocm-5.7.1 
#rocm-5.7.2 
#rocm-5.7.3 
#rocm-6.0 
#rocm-6.0.1
#rocm-6.0.2 (working....)

---
