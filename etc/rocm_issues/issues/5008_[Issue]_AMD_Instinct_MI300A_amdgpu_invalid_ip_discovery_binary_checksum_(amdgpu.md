# [Issue]: AMD Instinct MI300A: amdgpu: invalid ip discovery binary checksum (amdgpu: Fatal error during GPU init)

> **Issue #5008**
> **状态**: closed
> **创建时间**: 2025-07-08T15:47:32Z
> **更新时间**: 2025-11-14T17:41:29Z
> **关闭时间**: 2025-10-07T15:20:07Z
> **作者**: planetmija
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5008

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

After the last update last week where I updated to the Rocky 9.6 packages while staying with kernel 5.14.0-427.42.1.el9_4.x86_64 which is required for our Weka storage, rocm-smi does not see GPUs. If I revert to an older version (Rocky 9.5 packages, same kernel) of the system from May 22 with ROCm 6.4, everything works as expected. I can attach a full dmesg if needed.

```
[   57.125549] [drm] amdgpu kernel modesetting enabled.
[   57.127949] amdgpu: Virtual CRAT table created for CPU
[   57.128024] amdgpu: Topology: Add CPU node
[   57.128745] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A0 0x1458:0x1000 0x00).
[   57.128996] [drm] register mmio base: 0xD4C00000
[   57.128998] [drm] register mmio size: 2097152
[   57.129281] amdgpu 0000:01:00.0: amdgpu: invalid ip discovery binary checksum
[   57.129283] [drm:amdgpu_discovery_reg_base_init [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   57.129772] amdgpu 0000:01:00.0: amdgpu: Fatal error during GPU init
[   57.129777] amdgpu 0000:01:00.0: amdgpu: amdgpu: finishing device.
[   57.129845] amdgpu: probe of 0000:01:00.0 failed with error -22
[   57.130596] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A0 0x1458:0x1000 0x00).
[   57.130941] [drm] register mmio base: 0xC4800000
[   57.130947] [drm] register mmio size: 2097152
[   57.131272] amdgpu 0001:01:00.0: amdgpu: invalid ip discovery binary checksum
[   57.131278] [drm:amdgpu_discovery_reg_base_init [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   57.132022] amdgpu 0001:01:00.0: amdgpu: Fatal error during GPU init
[   57.132031] amdgpu 0001:01:00.0: amdgpu: amdgpu: finishing device.
[   57.132164] amdgpu: probe of 0001:01:00.0 failed with error -22
[   57.132810] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A0 0x1458:0x1000 0x00).
[   57.133109] [drm] register mmio base: 0xB8600000
[   57.133110] [drm] register mmio size: 2097152
[   57.133364] amdgpu 0002:01:00.0: amdgpu: invalid ip discovery binary checksum
[   57.133367] [drm:amdgpu_discovery_reg_base_init [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   57.133772] amdgpu 0002:01:00.0: amdgpu: Fatal error during GPU init
[   57.133777] amdgpu 0002:01:00.0: amdgpu: amdgpu: finishing device.
[   57.133842] amdgpu: probe of 0002:01:00.0 failed with error -22
[   57.134549] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x74A0 0x1458:0x1000 0x00).
[   57.134771] [drm] register mmio base: 0xB4200000
[   57.134772] [drm] register mmio size: 2097152
[   57.134965] amdgpu 0003:02:00.0: amdgpu: invalid ip discovery binary checksum
[   57.134968] [drm:amdgpu_discovery_reg_base_init [amdgpu]] *ERROR* amdgpu_discovery_init failed
[   57.135258] amdgpu 0003:02:00.0: amdgpu: Fatal error during GPU init
[   57.135262] amdgpu 0003:02:00.0: amdgpu: amdgpu: finishing device.
[   57.135321] amdgpu: probe of 0003:02:00.0 failed with error -22
```

### Operating System

Rocky 9.4 kernel / packages 9.6

### CPU

AMD Instinct MI300A

### GPU

AMD Instinct MI300A

### ROCm Version

ROCm 6.4[.1]

### ROCm Component

_No response_

### Steps to Reproduce

yum install amdgpu-dkms
yum install rocm
reboot

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
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
XNACK enabled:           YES
DMAbuf Support:          YES
VMM Support:             NO

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131219224(0x7d23f18) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131219224(0x7d23f18) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131219224(0x7d23f18) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131219224(0x7d23f18) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
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
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131809200(0x7db3fb0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    2                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        2                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131809208(0x7db3fb8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131809208(0x7db3fb8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131809208(0x7db3fb8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131809208(0x7db3fb8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 4                  
*******                  
  Name:                    AMD Instinct MI300A Accelerator    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Instinct MI300A Accelerator    
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    3                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   3700                               
  BDFID:                   0                                  
  Internal Node ID:        3                                  
  Compute Unit:            48                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131795632(0x7db0ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    131795632(0x7db0ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131795632(0x7db0ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131795632(0x7db0ab0) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — planetmija (2025-07-08T15:48:36Z)

Maybe related to issue #4454 .

---

### 评论 #2 — ppanchad-amd (2025-07-08T15:55:53Z)

Hi @planetmija. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — darren-amd (2025-07-28T14:49:17Z)

Hi @planetmija,

Thanks for reporting the issue! Could you please provide the complete dump of dmesg for us to further investigate? Also, do you have an AMD FAE helping you out?

---

### 评论 #4 — planetmija (2025-07-29T15:19:44Z)

Hi @darren-amd ,

We don't have an FAE (yet). I'll have to restart one of the machines tomorrow. They are currently running on an old image.

-- michael

---

### 评论 #5 — planetmija (2025-07-30T16:57:28Z)

[dmesg.log](https://github.com/user-attachments/files/21514388/dmesg.log)

dmesg of one of the machines

---

### 评论 #6 — darren-amd (2025-08-12T18:57:00Z)

Hi @planetmija,

Thanks for providing further logs. I can't see anything glaring from the logs and as far as I know Rocky 9.6 should be working with the MI300A on ROCm 6.4. To further diagnose the issue, would you mind providing me the output from the following steps on the failing system?

1. Provide the output of `lspci` and `lsmod | grep amdgpu`
2. [Blacklist amdgpu](https://askubuntu.com/questions/1080217/how-to-blacklist-amdgpu-driver)
3. Reboot the system
4. Run `lspci` and `lsmod | grep amdgpu` again
5. Reload the driver (`modprobe amdgpu`)

Also, do you have a point of contact at AMD? It'd be a bit easier rather than going through github.

---

### 评论 #7 — darren-amd (2025-09-23T18:29:08Z)

Hi @planetmija,

Were you able to give the above a try? Thanks!

---

### 评论 #8 — darren-amd (2025-10-07T15:20:07Z)

Hi @planetmija,

I'm going to close this ticket off but please feel free to create a new ticket if the issue persists, thanks!

---

### 评论 #9 — planetmija (2025-11-14T17:41:29Z)

This combination works again:

```
Kernel: 5.14.0-570.58.1.el9_6.x86_64

ROCM-SMI version: 3.0.0+e68c0d1
ROCM-SMI-LIB version: 7.5.0

amdgpu-core-6.4.60401-2164967.el9.noarch
libdrm-amdgpu-common-1.0.0.60401-2164967.el9.noarch
libdrm-amdgpu-2.4.124.60401-2164967.el9.x86_64
libdrm-amdgpu-devel-2.4.124.60401-2164967.el9.x86_64
```

---
