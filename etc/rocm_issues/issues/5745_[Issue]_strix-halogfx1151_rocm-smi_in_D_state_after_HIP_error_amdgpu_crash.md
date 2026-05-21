# [Issue]: strix-halo/gfx1151: rocm-smi in D state after HIP error / amdgpu crash

> **Issue #5745**
> **状态**: closed
> **创建时间**: 2025-12-06T01:04:12Z
> **更新时间**: 2026-01-06T16:35:23Z
> **关闭时间**: 2026-01-06T16:35:23Z
> **作者**: nickwitha-k
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5745

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Not sure if this is a known issue or not. I currently am experiencing frequent crashes when using the ROCm stack instead of Vulkan. I did a little digging after the most recent one and found rocm-smi stuck in a D state, requiring physical reboot.

```$ ps auxf | grep "\WD\W"
root       29481  0.0  0.0      0     0 ?        D    15:11   0:00  \_ [kworker/0:0+events]
root       39438  0.1  0.0      0     0 ?        D    15:53   0:05  \_ [kworker/18:3+events]
root        1261  0.0  0.0 283976 19416 ?        Ss   13:11   0:00 /usr/bin/abrt-dump-journal-core -D -T -f -e
root        1331  0.0  0.0   8880  6512 ?        Ss   13:11   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root       39976  0.0  0.0  19812  7396 pts/3    D+   16:02   0:00  |                   \_ reboot -f
root       40170  0.0  0.0  19820  7496 pts/4    D+   16:07   0:00  |                   \_ reboot -f now
user    39734  0.6  0.0  35924 30892 ?        D    15:54   0:18  \_ python3 /opt/venv/lib64/python3.13/site-packages/_rocm_sdk_core/bin/rocm-smi --showproductname --csv```

Please let me know if there are any logs/files that would be helpful.

### Operating System

Fedora Linux 43 (Server Edition)

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

ROCm nightly: 7.10.0a20251015

### ROCm Component

rocm_smi_lib, HIP

### Steps to Reproduce

Flux image generation via ComfyUI (also observed using Wan2.2). Seems more likely to occur when running larger workloads but that may or may not just be due to the longer runtime.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```$ rocminfo --support
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    131151212(0x7d1356c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131151212(0x7d1356c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131151212(0x7d1356c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131151212(0x7d1356c) KB            
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
  Marketing Name:          Radeon 8060S Graphics              
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
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   49408                              
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    130023424(0x7c00000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130023424(0x7c00000) KB            
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
    L3:                      32768(0x8000) KB                   
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
      Size:                    131151212(0x7d1356c) KB            
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
      Size:                    131151212(0x7d1356c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***  ```

### Additional Information

Workload was run in docker container built from https://github.com/kyuz0/amd-strix-halo-image-video-toolboxes, using v2, rather than v2-staging nightly build.


[dstate-stacktrace.txt](https://github.com/user-attachments/files/23972984/dstate-stacktrace.txt)

---

## 评论 (8 条)

### 评论 #1 — nickwitha-k (2025-12-09T02:34:25Z)

I think this might be a dupe of [5151](https://github.com/ROCm/ROCm/issues/5151) or [5190](https://github.com/ROCm/ROCm/issues/5590). When looking in dmesg, I'm seeing similar `MES failed to respond to msg=REMOVE_QUEUE` entries. Probably the rocm-smi program getting called at a bad time during the HIP/MES crash. If it looks the same, this can probably be closed. If you any other sample logs/dmesg/etc would be helpful, please let me know.

---

### 评论 #2 — harkgill-amd (2025-12-09T16:22:38Z)

Hey @nickwitha-k, could you share outputs of 

- `dmesg`
- `sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info`
- `uname -r`

Will give this a try on my end in the meantime.

---

### 评论 #3 — harkgill-amd (2025-12-09T20:25:05Z)

> Workload was run in docker container built from https://github.com/kyuz0/amd-strix-halo-image-video-toolboxes, using v2, rather than v2-staging nightly build.

Are you overriding the ROCm/torch packages already installed in the toolbox with v2-staging builds? The toolbox has `7.11.0a20251123` by default on my end.

---

### 评论 #4 — nickwitha-k (2025-12-10T01:23:09Z)

To clarify, I edited the Dockerfile to use `https://rocm.nightlies.amd.com/v2/gfx1151/`  (hence the `ROCm nightly: 7.10.0a20251015`) as the v2-staging builds were causing nearly constant crashes when attempting to run any image generation or LLM workloads. I forced a crash so that I could have a fresh dmesg and sar, just to be sure it wasn't an OOM. At the time of the crash, unified RAM utilization was only at 87.72% and there were no OOMKiller entries.

Is this an issue w/ memory over-commitment causing the proc to try accessing unallocated memory?

An additional observation from forcing a repro: I was unable to repro when using GGUF models but quickly able to repro using an FP8 safetensor.   

```
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae772000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:          MORE_FAULTS: 0x1
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:          WALKER_ERROR: 0x0
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:          RW: 0x0
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae794000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae759000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae784000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae761000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae762000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae77c000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae774000 from client 10
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 135872 thread python pid 135872
[Tue Dec  9 17:04:29 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007fc0ae756000 from client 10
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: failed to suspend all gangs
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: failed to suspend gangs from MES
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: Suspending all queues failed
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 4, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset begin!. Source:  3
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 2, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 4, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 2 for dev 6567
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 2, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 2, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 2, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 4, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 4, simd_id 0, wgp_id 0
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State
[Tue Dec  9 17:04:31 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State Completed
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: Register(0) [regVPEC_QUEUE_RESET_REQ_6_1_1] failed to reach value 0x00000000 != 0x00000001n
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: VPE queue reset failed
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: Register(1) [regVPEC_QUEUE_RESET_REQ_6_1_1] failed to reach value 0x00000000 != 0x00000001n
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: VPE queue reset failed
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: MODE2 reset
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset succeeded, trying to resume
[Tue Dec  9 17:04:32 2025] [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09003400
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[Tue Dec  9 17:04:32 2025] amdgpu 0000:c1:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: [drm:amdgpu_ib_ring_tests [amdgpu]] *ERROR* IB test failed on vpe (-110).
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ib ring test failed (-110).
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State Completed
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: MODE2 reset
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset succeeded, trying to resume
[Tue Dec  9 17:04:33 2025] [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09003400
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset(7) succeeded!
[Tue Dec  9 17:04:33 2025] amdgpu 0000:c1:00.0: [drm] device wedged, but recovered through reset
```


```
$ sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info
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
ASD feature version: 553648378, firmware version: 0x210000fa
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x17000049
TA DTM feature version: 0x00000000, firmware version: 0x1200001a
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 10, firmware version: 0x0a640200 (100.2.0)
SDMA0 feature version: 60, firmware version: 0x00000011
VCN feature version: 0, firmware version: 0x09118016
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x09003400
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
VPE feature version: 60, firmware version: 0x00000017
VBIOS version: 113-STRXLGEN-001
```

Note on the above: I was forced to revert the `linux-firmware` package to 20251111 as the Fedora Rawhide repo still contains the 20251125-1 build.

```
$ uname -r
6.18.0-364.vanilla.fc43.x86_64
```

---

### 评论 #5 — harkgill-amd (2025-12-10T21:16:04Z)

So you're seeing the same issue as https://gitlab.freedesktop.org/drm/amd/-/issues/4632#note_3205202. In order to get the user space fix, https://github.com/ROCm/rocm-systems/pull/1807, you'd need to use newer nightlies than the 10/15 v2 build. 

I see you mentioned,

>  the v2-staging builds were causing nearly constant crashes when attempting to run any image generation or LLM workloads.

Could you share some more information regarding these failures. It'd make more sense to go forward and investigate these given that the current MES failure is a known issue with a fix.

---

### 评论 #6 — nickwitha-k (2025-12-11T05:10:12Z)

Certainly. I've just built a fresh container from v2-staging and was able to trigger a crash pretty quickly. The same GGUF-based workload that I was unable to readily crash with the non-staging version was used.:

```
rocminfo --support
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.15
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    131151204(0x7d13564) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131151204(0x7d13564) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131151204(0x7d13564) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131151204(0x7d13564) KB            
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
  Marketing Name:          Radeon 8060S Graphics              
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
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   49408                              
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      17                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    130023424(0x7c00000) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    130023424(0x7c00000) KB            
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
  Name:                    aie2p                              
  Uuid:                    AIE-XX                             
  Marketing Name:          RyzenAI-npu5                       
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
    L3:                      32768(0x8000) KB                   
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
      Size:                    131151204(0x7d13564) KB            
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
      Size:                    131151204(0x7d13564) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             
```

```
# dmesg| grep amdgpu from crash
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f94000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          MORE_FAULTS: 0x1
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          WALKER_ERROR: 0x0
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          RW: 0x0
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f72000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801030
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          MORE_FAULTS: 0x0
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          WALKER_ERROR: 0x0
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:          RW: 0x0
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f59000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f62000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f7c000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f61000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f84000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f74000 from client 10
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32771)
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:  Process python pid 523991 thread python pid 523991
[Wed Dec 10 21:01:03 2025] amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x00007f9510f56000 from client 10
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: failed to suspend all gangs
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: failed to suspend gangs from MES
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: Suspending all queues failed
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset begin!. Source:  3
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 2 for dev 6567
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State Completed
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: Register(0) [regVPEC_QUEUE_RESET_REQ_6_1_1] failed to reach value 0x00000000 != 0x00000001n
[Wed Dec 10 21:01:05 2025] amdgpu 0000:c1:00.0: amdgpu: VPE queue reset failed
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: Register(1) [regVPEC_QUEUE_RESET_REQ_6_1_1] failed to reach value 0x00000000 != 0x00000001n
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: VPE queue reset failed
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: MODE2 reset
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset succeeded, trying to resume
[Wed Dec 10 21:01:06 2025] [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09003400
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[Wed Dec 10 21:01:06 2025] amdgpu 0000:c1:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: [drm:amdgpu_ib_ring_tests [amdgpu]] *ERROR* IB test failed on vpe (-110).
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ib ring test failed (-110).
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: Dumping IP State Completed
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: MODE2 reset
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset succeeded, trying to resume
[Wed Dec 10 21:01:07 2025] [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09003400
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: amdgpu: GPU reset(13) succeeded!
[Wed Dec 10 21:01:07 2025] amdgpu 0000:c1:00.0: [drm] device wedged, but recovered through reset




---

### 评论 #7 — harkgill-amd (2025-12-16T19:17:53Z)

Can you try to run the workload with cwsr disabled, `amdgpu.cwsr_enable=0`? We're aware of some issues with MES version 0x80 and this'll help narrow down whether this issue is the same.

---

### 评论 #8 — harkgill-amd (2026-01-06T16:35:23Z)

Closing this issue out for now but feel free to leave a comment if the error persists on your end.

---
