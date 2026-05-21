# [Issue]: ROCm 6.0.0 : MI100 Bridge does not initalize when on virtualized host

> **Issue #2722**
> **状态**: closed
> **创建时间**: 2023-12-15T20:27:38Z
> **更新时间**: 2024-01-05T23:38:42Z
> **关闭时间**: 2024-01-04T18:23:43Z
> **作者**: TNT3530
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2722

## 描述

### Problem Description

I have a cluster of 4x AMD Instinct MI100 GPUs i recently picked up a Infinity Fabric bridge for, running on a Proxmox 7.3-3 host, Ubuntu 22.04 virtual machine, and using ROCm 6.0.0.

I can pass through the GPUs themselves fine, and even with the bridge installed they still work, but checking the interconnect speed shows they're still using PCIe.

[This Github Issue](https://github.com/ROCm/ROCm/issues/1496#issuecomment-866525188) shows there should be a log entry for when the bridge initializes, but running that search on the VM returns nothing. I dont see the bridge as its own PCIe device to pass through, so I assume its some low level thing outside of the OS's view. [This ROCm Documentation](https://rocm.docs.amd.com/en/docs-5.5.1/how_to/tuning_guides/mi100.html#hardware-verification-with-rocm) says they should print out XGMI if the bridge is in use, which mine sadly does not.

here is the `rocm-smi --showxgmierr` output
![image](https://github.com/ROCm/ROCm/assets/7338884/2fcbd9a9-ad0d-40c6-976d-8ba64a239007)

`dkms status` 
returns 
`amdgpu/6.3.6-1697589.22.04, 6.2.0-31-generic, x86_64: installed`
`amdgpu/6.3.6-1697589.22.04, 6.2.0-39-generic, x86_64: installed`

I have removed and reinstalled ROCm along with amdgpu-dkms to no avail

### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish) VM on Proxmox 7.3-3

### CPU

Dual Intel Xeon Gold 6148

### GPU

4 x AMD Instinct MI100

### ROCm Version

6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    Intel(R) Xeon(R) Gold 6148 CPU @ 2.40GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Xeon(R) Gold 6148 CPU @ 2.40GHz
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
  Max Clock Freq. (MHz):   0                                  
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    131899420(0x7dca01c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    131899420(0x7dca01c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    131899420(0x7dca01c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx908                             
  Uuid:                    GPU-dc0e3b8851938320               
  Marketing Name:          AMD Instinct MI100                 
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
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29580(0x738c)                      
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1502                               
  BDFID:                   128                                
  Internal Node ID:        1                                  
  Compute Unit:            120                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 65                                 
  SDMA engine uCode::      18                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33538048(0x1ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    33538048(0x1ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-
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
Agent 3                  
*******                  
  Name:                    gfx908                             
  Uuid:                    GPU-3c5f6e517bd6a9d4               
  Marketing Name:          AMD Instinct MI100                 
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
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29580(0x738c)                      
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1502                               
  BDFID:                   136                                
  Internal Node ID:        2                                  
  Compute Unit:            120                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 65                                 
  SDMA engine uCode::      18                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33538048(0x1ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    33538048(0x1ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-
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
  Name:                    gfx908                             
  Uuid:                    GPU-2b0018e6da689f23               
  Marketing Name:          AMD Instinct MI100                 
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
    L1:                      16(0x10) KB                        
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29580(0x738c)                      
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1502                               
  BDFID:                   216                                
  Internal Node ID:        3                                  
  Compute Unit:            120                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 65                                 
  SDMA engine uCode::      18                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33538048(0x1ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    33538048(0x1ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-
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
  Name:                    gfx908                             
  Uuid:                    GPU-a341d0fc76d661cd               
  Marketing Name:          AMD Instinct MI100                 
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
    L2:                      8192(0x2000) KB                    
  Chip ID:                 29580(0x738c)                      
  ASIC Revision:           2(0x2)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1502                               
  BDFID:                   224                                
  Internal Node ID:        4                                  
  Compute Unit:            120                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 65                                 
  SDMA engine uCode::      18                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    33538048(0x1ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    33538048(0x1ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-
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


---

## 评论 (7 条)

### 评论 #1 — kentrussell (2024-01-02T14:28:40Z)

I haven't seen ProxMox at all, but I wonder if there could be an issue with the kernel itself. Does the issue also show up in baremetal? And can you attach a full kernel log? Thanks!

---

### 评论 #2 — TNT3530 (2024-01-03T22:40:46Z)

> I haven't seen ProxMox at all, but I wonder if there could be an issue with the kernel itself. Does the issue also show up in baremetal? And can you attach a full kernel log? Thanks!

[dmesg_amd.txt](https://github.com/ROCm/ROCm/files/13824066/dmesg_amd.txt)
[full_dmesg.txt](https://github.com/ROCm/ROCm/files/13824105/full_dmesg.txt)

Here is a `sudo dmesg | grep amd` output, if you need the full `dmesg` dump that is also attached.
As for bare metal tests, I'm afraid the GPUs were added to an existing virtualization box. I sadly don't have another motherboard capable of holding 4 2 slot-width cards.

---

### 评论 #3 — kentrussell (2024-01-04T14:25:33Z)

Hmm, dmesg doesn't seem to have anything obvious. There should be lights on the top of the bridge, and should light up based on how many GPUs it sees. Does it show 4 lights? The lights should be independent of the kernel driver and should light up as soon as the GPUs receive power (can check before the GRUB menu). 

---

### 评论 #4 — TNT3530 (2024-01-04T18:23:43Z)

I wasn't aware there were LED indicators, that was my issue. 
Upon cranking the screws tight enough they no longer moved, all 4 LEDs illuminated on next power on. I just didn't push it down on the connectors hard enough originally.

![image](https://github.com/ROCm/ROCm/assets/7338884/603ce758-c50b-4286-bbe9-d5326265db57)
![image](https://github.com/ROCm/ROCm/assets/7338884/4561c31d-d6ab-4486-8406-3db7e4f83660)

Thanks for your help! 
I wish the install manual had the "please make sure it is plugged in fully and detecting cards" step, it's pretty important


---

### 评论 #5 — cgmb (2024-01-05T22:24:14Z)

> I can pass through the GPUs themselves fine, and even with the bridge installed they still work

Interesting. You don't have any issues with PCIe reset when restarting the virtual machine?

---

### 评论 #6 — TNT3530 (2024-01-05T22:28:09Z)

> > I can pass through the GPUs themselves fine, and even with the bridge installed they still work
> 
> Interesting. You don't have any issues with PCIe reset when restarting the virtual machine?

Sadly not, they work for first boot only. If i restart the guest I assume the host grabs them, requiring a full box restart. Adding `amdgpu` to `/etc/modprobe.d/blacklist.conf` on the host hasnt fixed it either

---

### 评论 #7 — cgmb (2024-01-05T23:14:12Z)

> Sadly not, they work for first boot only. If i restart the guest I assume the host grabs them, requiring a full box restart. Adding `amdgpu` to `/etc/modprobe.d/blacklist.conf` on the host hasnt fixed it either

Ok. So it's not just me. Thanks for the info!

That seems to be a bug in the PCIe reset handling. If you file a bug for that problem or find a workaround, please let me know.

---
