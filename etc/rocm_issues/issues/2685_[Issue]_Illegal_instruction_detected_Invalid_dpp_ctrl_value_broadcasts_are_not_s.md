# [Issue]: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+

> **Issue #2685**
> **状态**: closed
> **创建时间**: 2023-12-01T06:57:03Z
> **更新时间**: 2024-06-19T17:13:32Z
> **关闭时间**: 2024-06-19T17:13:32Z
> **作者**: fromtheeast710
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2685

## 描述

### Problem Description

I'm trying to compile LAMMPS and [JAX](https://jax.readthedocs.io/en/latest/developer.html#additional-notes-for-building-a-rocm-jaxlib-for-amd-gpus) for ROCm support. However, both compilations failed with these errors:

```
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr45 = V_MOV_B32_dpp undef $vgpr45(tied-def 0), $vgpr12, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr5 = V_MOV_B32_dpp undef $vgpr5(tied-def 0), $vgpr3, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr60 = V_MOV_B32_dpp undef $vgpr60(tied-def 0), $vgpr21, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr57 = V_MOV_B32_dpp undef $vgpr57(tied-def 0), $vgpr2, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr60 = V_MOV_B32_dpp undef $vgpr60(tied-def 0), $vgpr21, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr57 = V_MOV_B32_dpp undef $vgpr57(tied-def 0), $vgpr2, 322, 15, 15, 0, implicit $exec
6 errors generated when compiling for gfx1032.
```

I tried `export HSA_OVERRIDE_GFX_VERSION=10.3.0` but to no avail.

### Operating System

Artix Linux 6.6.2-artix1-1

### CPU

AMD Ryzen 7 5800H with Radeon Graphics

### GPU

AMD Radeon RX 6600M

### ROCm Version

5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

For JAX compilation:

1. git clone https://github.com/google/jax && cd jax
2. yay -Syyu opencl-amd opencl-amd-dev
3. python build/build.py --enable_rocm --rocm_path=/opt/rocm-5.7.1

For LAMMPS compilation:

1. cd ~/LAMMPS
2. mkpkg -fsic

### Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen 7 5800H with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 5800H with Radeon Graphics
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
  Max Clock Freq. (MHz):   4463                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    23974348(0x16dd1cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    23974348(0x16dd1cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    23974348(0x16dd1cc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1030                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 6600M                
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
    L2:                      2048(0x800) KB                     
    L3:                      32768(0x8000) KB                   
  Chip ID:                 29695(0x73ff)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            28                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 115                                
  SDMA engine uCode::      76                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    8372224(0x7fc000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    8372224(0x7fc000) KB               
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
      Name:                    amdgcn-amd-amdhsa--gfx1030         
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
  Name:                    gfx1030                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      1024(0x400) KB                     
  Chip ID:                 5688(0x1638)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   1792                               
  Internal Node ID:        2                                  
  Compute Unit:            8                                  
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
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
  Packet Processor uCode:: 469                                
  SDMA engine uCode::      40                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    524288(0x80000) KB                 
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    524288(0x80000) KB                 
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
      Name:                    amdgcn-amd-amdhsa--gfx1030         
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

## 评论 (9 条)

### 评论 #1 — b-sumner (2023-12-01T15:12:24Z)

Hi @fromtheeast710 .  I'm not sure why this is being reported to ROCm and not the LAMMPS developers who probably have not updated their code to handle GFX10+.

---

### 评论 #2 — fromtheeast710 (2023-12-02T09:26:07Z)

@b-sumner I did report it to LAMMPS [here](https://github.com/lammps/lammps/issues/3785) and they said it was because of AMD's hardware support. Also, the problem occur with JAX so I believe it's on AMD.

---

### 评论 #3 — b-sumner (2023-12-02T17:09:26Z)

Hello @fromtheeast710 the compiler is correctly stating that the source code is attempting to use an instruction field that is not supported by gfx1030.   This is much preferable to the hardware failing to execute the instruction at runtime.

The source code needs to be updated for gfx1030.  That will have to be done by the LAMMPS developers.

---

### 评论 #4 — fromtheeast710 (2023-12-03T11:23:47Z)

@b-sumner So just to be clear, the 6600M (gfx1032) is supported by ROCm 5.7.1 via overwriting it to gfx1030 right?

---

### 评论 #5 — b-sumner (2023-12-03T16:36:06Z)

@fromtheeast710 the compiler treats gfx1030 and gfx1032 as separate targets; they have different names after all.  Forcing ISA from one to run on another is risky.

---

### 评论 #6 — fromtheeast710 (2023-12-07T01:15:44Z)

@b-sumner So is gfx1032 supported at all? From my understanding the answer is no.

---

### 评论 #7 — unoexperto (2024-02-20T17:16:10Z)

Folks, I have similar problem when I'm trying to compile jax for gfx1103. Here is my error output:

```
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr53 = V_MOV_B32_dpp undef $vgpr53(tied-def 0), $vgpr12, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr4 = V_MOV_B32_dpp undef $vgpr4(tied-def 0), killed $vgpr3, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr3 = V_MOV_B32_dpp undef $vgpr3(tied-def 0), $vgpr2, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr66 = V_MOV_B32_dpp undef $vgpr66(tied-def 0), $vgpr44, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr64 = V_MOV_B32_dpp undef $vgpr64(tied-def 0), $vgpr62, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr66 = V_MOV_B32_dpp undef $vgpr66(tied-def 0), $vgpr44, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr64 = V_MOV_B32_dpp undef $vgpr64(tied-def 0), $vgpr62, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr53 = V_MOV_B32_dpp undef $vgpr53(tied-def 0), $vgpr16, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr66 = V_MOV_B32_dpp undef $vgpr66(tied-def 0), $vgpr44, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr64 = V_MOV_B32_dpp undef $vgpr64(tied-def 0), $vgpr62, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr66 = V_MOV_B32_dpp undef $vgpr66(tied-def 0), $vgpr44, 322, 15, 15, 0, implicit $exec
error: Illegal instruction detected: Invalid dpp_ctrl value: broadcasts are not supported on GFX10+
renamable $vgpr64 = V_MOV_B32_dpp undef $vgpr64(tied-def 0), $vgpr62, 322, 15, 15, 0, implicit $exec
12 errors generated when compiling for gfx1103.
```

Could you please advice what to do to fix it ? I'm using ROCm 6.0.2

Thank you.

---

### 评论 #8 — ppanchad-amd (2024-05-17T16:42:35Z)

@unoexperto gfx1103 is not supported. Thanks!

---

### 评论 #9 — ppanchad-amd (2024-05-17T16:44:45Z)

@fromtheeast710 gfx1032 is not supported. Please close ticket if issue no longer relevant. Thanks!

---
