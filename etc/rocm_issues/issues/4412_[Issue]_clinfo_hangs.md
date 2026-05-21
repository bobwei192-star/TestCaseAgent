# [Issue]: clinfo hangs

> **Issue #4412**
> **状态**: closed
> **创建时间**: 2025-02-24T13:11:29Z
> **更新时间**: 2025-04-23T17:36:09Z
> **关闭时间**: 2025-04-23T17:36:07Z
> **作者**: emotroshylov
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.3.3
> **URL**: https://github.com/ROCm/ROCm/issues/4412

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.3.3** (颜色: #aaaaaa)

## 描述

### Problem Description

VM Ubuntu 24.04
XCP-ng 8.2

OS:
NAME="Ubuntu"
VERSION="24.04.2 LTS (Noble Numbat)"

CPU: 
model name	: AMD EPYC 9374F 32-Core Processor

GPU:
  Name:                    AMD EPYC 9374F 32-Core Processor   
  Marketing Name:          AMD EPYC 9374F 32-Core Processor   
  Name:                    gfx1100                            
  Marketing Name:          AMD Radeon PRO W7900 Dual Slot     
      Name:                    amdgcn-amd-amdhsa--gfx1100

clinfo hangs

# /opt/rocm-6.3.3/bin/clinfo 
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 1
  Device Type:					 CL_DEVICE_TYPE_GPU
  Vendor ID:					 1002h
  Board name:					 AMD Radeon PRO W7900 Dual Slot 
  Device Topology:				 PCI[ B#0, D#8, F#0 ]
  Max compute units:				 48
  Max work items dimensions:			 3
    Max work items[0]:				 1024
    Max work items[1]:				 1024
    Max work items[2]:				 1024
  Max work group size:				 256
  Preferred vector width char:			 4
  Preferred vector width short:			 2
  Preferred vector width int:			 1
  Preferred vector width long:			 1
  Preferred vector width float:			 1
  Preferred vector width double:		 1
  Native vector width char:			 4
  Native vector width short:			 2
  Native vector width int:			 1
  Native vector width long:			 1
  Native vector width float:			 1
  Native vector width double:			 1
  Max clock frequency:				 1760Mhz
  Address bits:					 64
  Max memory allocation:			 41056364128
  Image support:				 Yes
  Max number of images read arguments:		 128
  Max number of images write arguments:		 8
  Max image 2D width:				 16384
  Max image 2D height:				 16384
  Max image 3D width:				 16384
  Max image 3D height:				 16384
  Max image 3D depth:				 8192
  Max samplers within kernel:			 16
  Max size of kernel argument:			 1024
  Alignment (bits) of base address:		 2048
  Minimum alignment (bytes) for any datatype:	 128
  Single precision floating point capability
    Denorms:					 Yes
    Quiet NaNs:					 Yes
    Round to nearest even:			 Yes
    Round to zero:				 Yes
    Round to +ve and infinity:			 Yes
    IEEE754-2008 fused multiply-add:		 Yes
  Cache type:					 Read/Write
  Cache line size:				 64
  Cache size:					 32768
  Global memory size:				 48301604864
  Constant buffer size:				 41056364128
  Max number of constant args:			 8
  Local memory type:				 Local
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 2401658464
  Max global variable size:			 41056364128
  Max global variable preferred total size:	 48301604864
  Max read/write image args:			 64
  Max on device events:				 1024
  Queue on device max size:			 8388608
  Max on device queues:				 1
  Queue on device preferred size:		 262144
  SVM capabilities:				 
    Coarse grain buffer:			 Yes
    Fine grain buffer:				 Yes
    Fine grain system:				 No
    Atomics:					 No
  Preferred platform atomic alignment:		 0
  Preferred global atomic alignment:		 0
  Preferred local atomic alignment:		 0
^C

### Operating System

24.04.2 LTS (Noble Numbat)

### CPU

AMD EPYC 9374F 32-Core Processor

### GPU

AMD Radeon PRO W7900 Dual Slot

### ROCm Version

ROCm 6.3.3

### ROCm Component

clr

### Steps to Reproduce

# /opt/rocm-6.3.3/bin/clinfo 
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 1
  Device Type:					 CL_DEVICE_TYPE_GPU
  Vendor ID:					 1002h
  Board name:					 AMD Radeon PRO W7900 Dual Slot 
  Device Topology:				 PCI[ B#0, D#8, F#0 ]
  Max compute units:				 48
  Max work items dimensions:			 3
    Max work items[0]:				 1024
    Max work items[1]:				 1024
    Max work items[2]:				 1024
  Max work group size:				 256
  Preferred vector width char:			 4
  Preferred vector width short:			 2
  Preferred vector width int:			 1
  Preferred vector width long:			 1
  Preferred vector width float:			 1
  Preferred vector width double:		 1
  Native vector width char:			 4
  Native vector width short:			 2
  Native vector width int:			 1
  Native vector width long:			 1
  Native vector width float:			 1
  Native vector width double:			 1
  Max clock frequency:				 1760Mhz
  Address bits:					 64
  Max memory allocation:			 41056364128
  Image support:				 Yes
  Max number of images read arguments:		 128
  Max number of images write arguments:		 8
  Max image 2D width:				 16384
  Max image 2D height:				 16384
  Max image 3D width:				 16384
  Max image 3D height:				 16384
  Max image 3D depth:				 8192
  Max samplers within kernel:			 16
  Max size of kernel argument:			 1024
  Alignment (bits) of base address:		 2048
  Minimum alignment (bytes) for any datatype:	 128
  Single precision floating point capability
    Denorms:					 Yes
    Quiet NaNs:					 Yes
    Round to nearest even:			 Yes
    Round to zero:				 Yes
    Round to +ve and infinity:			 Yes
    IEEE754-2008 fused multiply-add:		 Yes
  Cache type:					 Read/Write
  Cache line size:				 64
  Cache size:					 32768
  Global memory size:				 48301604864
  Constant buffer size:				 41056364128
  Max number of constant args:			 8
  Local memory type:				 Local
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 2401658464
  Max global variable size:			 41056364128
  Max global variable preferred total size:	 48301604864
  Max read/write image args:			 64
  Max on device events:				 1024
  Queue on device max size:			 8388608
  Max on device queues:				 1
  Queue on device preferred size:		 262144
  SVM capabilities:				 
    Coarse grain buffer:			 Yes
    Fine grain buffer:				 Yes
    Fine grain system:				 No
    Atomics:					 No
  Preferred platform atomic alignment:		 0
  Preferred global atomic alignment:		 0
  Preferred local atomic alignment:		 0
^C

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

# /opt/rocm-6.3.3/bin/rocminfo --support
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
  Name:                    AMD EPYC 9374F 32-Core Processor   
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 9374F 32-Core Processor   
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
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    65816516(0x3ec47c4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65816516(0x3ec47c4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65816516(0x3ec47c4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65816516(0x3ec47c4) KB             
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
  Uuid:                    GPU-859d9f0038035e69               
  Marketing Name:          AMD Radeon PRO W7900 Dual Slot     
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
  Chip ID:                 29770(0x744a)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1760                               
  BDFID:                   64                                 
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
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
  Packet Processor uCode:: 412                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    47169536(0x2cfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    47169536(0x2cfc000) KB             
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

_No response_

---

## 评论 (8 条)

### 评论 #1 — ppanchad-amd (2025-02-24T15:16:45Z)

Hi @emotroshylov. Internal ticket has been created to investigate the issue. Thanks!

---

### 评论 #2 — emotroshylov (2025-02-24T16:33:25Z)

> Hi [@emotroshylov](https://github.com/emotroshylov). Internal ticket has been created to investigate the issue. Thanks!

Hi @ppanchad-amd 

I have additional debug info for you
Clinfo hangs after   [hsaKmtMapMemoryToGPUNodes] address 0x77f076b30000 number of nodes 1

root@test:~# export HSAKMT_DEBUG_LEVEL=7
root@test:~# /opt/rocm-6.3.3/bin/clinfo 
acquiring VM for 403e using 8
Initialized unreserved SVM apertures: 0x200000 - 0x7fffffffffff
mem_handle_aperture start 0x2800000000000, mem_handle_aperture limit 0x3000000000000
[hsaKmtMapMemoryToGPU] address 0x77f076b68000
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f06d800000 flags 0x20040 size 0x200000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f06d800000 size 2097152 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f06d800000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x77ef6cc00000 size 4294967296 from scratch
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f07752f000 flags 0x21040 size 0x1000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f07752f000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f07752f000 number of nodes 1
[hsaKmtGetTileConfig] node 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77ef67d00000 flags 0x2040 size 0x101000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77ef67d00000 size 1052672 from host
[hsaKmtQueryPointerInfo] pointer 0x77ef67d00000
[hsaKmtMapMemoryToGPUNodes] address 0x77ef67d00000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77ef67b00000 flags 0x2040 size 0x101000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77ef67b00000 size 1052672 from host
[hsaKmtQueryPointerInfo] pointer 0x77ef67b00000
[hsaKmtMapMemoryToGPUNodes] address 0x77ef67b00000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77ef67600000 flags 0x2040 size 0x400000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77ef67600000 size 4194304 from host
[hsaKmtQueryPointerInfo] pointer 0x77ef67600000
[hsaKmtMapMemoryToGPUNodes] address 0x77ef67600000 number of nodes 1
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP (3635.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 1
  Device Type:					 CL_DEVICE_TYPE_GPU
  Vendor ID:					 1002h
  Board name:					 AMD Radeon PRO W7900 Dual Slot 
  Device Topology:				 PCI[ B#0, D#8, F#0 ]
  Max compute units:				 48
  Max work items dimensions:			 3
    Max work items[0]:				 1024
    Max work items[1]:				 1024
    Max work items[2]:				 1024
  Max work group size:				 256
  Preferred vector width char:			 4
  Preferred vector width short:			 2
  Preferred vector width int:			 1
  Preferred vector width long:			 1
  Preferred vector width float:			 1
  Preferred vector width double:		 1
  Native vector width char:			 4
  Native vector width short:			 2
  Native vector width int:			 1
  Native vector width long:			 1
  Native vector width float:			 1
  Native vector width double:			 1
  Max clock frequency:				 1760Mhz
  Address bits:					 64
  Max memory allocation:			 41056364128
  Image support:				 Yes
  Max number of images read arguments:		 128
  Max number of images write arguments:		 8
  Max image 2D width:				 16384
  Max image 2D height:				 16384
  Max image 3D width:				 16384
  Max image 3D height:				 16384
  Max image 3D depth:				 8192
  Max samplers within kernel:			 16
  Max size of kernel argument:			 1024
  Alignment (bits) of base address:		 2048
  Minimum alignment (bytes) for any datatype:	 128
  Single precision floating point capability
    Denorms:					 Yes
    Quiet NaNs:					 Yes
    Round to nearest even:			 Yes
    Round to zero:				 Yes
    Round to +ve and infinity:			 Yes
    IEEE754-2008 fused multiply-add:		 Yes
  Cache type:					 Read/Write
  Cache line size:				 64
  Cache size:					 32768
  Global memory size:				 48301604864
  Constant buffer size:				 41056364128
  Max number of constant args:			 8
  Local memory type:				 Local
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 2401658464
  Max global variable size:			 41056364128
  Max global variable preferred total size:	 48301604864
  Max read/write image args:			 64
  Max on device events:				 1024
  Queue on device max size:			 8388608
  Max on device queues:				 1
  Queue on device preferred size:		 262144
  SVM capabilities:				 
    Coarse grain buffer:			 Yes
    Fine grain buffer:				 Yes
    Fine grain system:				 No
    Atomics:					 No
  Preferred platform atomic alignment:		 0
  Preferred global atomic alignment:		 0
  Preferred local atomic alignment:		 0
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x77f077014000 size 12288 from device
[hsaKmtMapMemoryToGPUNodes] address 0x77f077014000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f076b42000 flags 0x40 size 0x3000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f076b42000 size 12288 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f076b42000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 1
[hsaKmtAllocMemoryAlign] node 1 address 0x77f07752d000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f07752d000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f077481000 flags 0x21040 size 0x1000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f077481000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f077481000 number of nodes 1
[hsaKmtMapMemoryToGPUNodes] address 0x77f07747f000 number of nodes 1
Allocating VRAM for EOP
[hsaKmtMapMemoryToGPUNodes] address 0x77f076b40000 number of nodes 1
Allocating GTT for CWSR
hsaKmtSVMSetAttr: address 0x0x77ef64600000 size 0x2c02000
[hsaKmtAvailableMemory] node 1
[hsaKmtMapMemoryToGPU] address 0x77ef6cc00000
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f076b3a000 flags 0x21040 size 0x1000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f076b3a000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f076b3a000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f076b36000 flags 0x20040 size 0x2000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f076b36000 size 8192 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f076b36000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f076b34000 flags 0x21040 size 0x1000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f076b34000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f076b34000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f076b32000 flags 0x21040 size 0x1000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f076b32000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f076b32000 number of nodes 1
[hsaKmtAllocMemoryAlign] node 0
bind_mem_to_numa mem 0x77f076b30000 flags 0x21040 size 0x1000 node_id 0
[hsaKmtAllocMemoryAlign] node 0 address 0x77f076b30000 size 4096 from host
[hsaKmtMapMemoryToGPUNodes] address 0x77f076b30000 number of nodes 1
^C

---

### 评论 #3 — schung-amd (2025-02-24T22:33:57Z)

Hi @emotroshylov, can you provide the `dmesg` output around the time of the hang?

---

### 评论 #4 — emotroshylov (2025-02-25T10:08:55Z)

> Hi [@emotroshylov](https://github.com/emotroshylov), can you provide the `dmesg` output around the time of the hang?

Hi  @schung-amd 
No new dmesg appeared during execution clinfo

Here are the last 20 lines of dmesg before and after run clinfo

 [    6.865960] audit: type=1400 audit(1740397211.283:2): apparmor="STATUS" operation="profile_load" profile="unconfined" name="buildah" pid=634 comm="apparmor_parser"
[    6.866106] audit: type=1400 audit(1740397211.283:3): apparmor="STATUS" operation="profile_load" profile="unconfined" name="brave" pid=633 comm="apparmor_parser"
[    6.866112] audit: type=1400 audit(1740397211.283:4): apparmor="STATUS" operation="profile_load" profile="unconfined" name="1password" pid=628 comm="apparmor_parser"
[    6.866158] audit: type=1400 audit(1740397211.283:5): apparmor="STATUS" operation="profile_load" profile="unconfined" name="busybox" pid=635 comm="apparmor_parser"
[    6.866307] audit: type=1400 audit(1740397211.283:6): apparmor="STATUS" operation="profile_load" profile="unconfined" name="balena-etcher" pid=632 comm="apparmor_parser"
[    6.866353] audit: type=1400 audit(1740397211.283:7): apparmor="STATUS" operation="profile_load" profile="unconfined" name="Discord" pid=629 comm="apparmor_parser"
[    6.866497] audit: type=1400 audit(1740397211.283:8): apparmor="STATUS" operation="profile_load" profile="unconfined" name=4D6F6E676F444220436F6D70617373 pid=630 comm="apparmor_parser"
[    6.866650] audit: type=1400 audit(1740397211.284:9): apparmor="STATUS" operation="profile_load" profile="unconfined" name="QtWebEngineProcess" pid=631 comm="apparmor_parser"
[    6.867585] audit: type=1400 audit(1740397211.285:10): apparmor="STATUS" operation="profile_load" profile="unconfined" name="cam" pid=637 comm="apparmor_parser"
[    6.868448] audit: type=1400 audit(1740397211.285:11): apparmor="STATUS" operation="profile_load" profile="unconfined" name="vscode" pid=641 comm="apparmor_parser"
[    7.013719] cfg80211: Loading compiled-in X.509 certificates for regulatory database
[    7.014087] Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
[    7.014190] Loaded X.509 cert 'wens: 61c038651aabdcf94bd0ac7ff06c7248db18c600'
[    7.372746] NET: Registered PF_QIPCRTR protocol family
[    8.502995] loop3: detected capacity change from 0 to 8
[    9.037637] evm: overlay not supported
[    9.052661] overlayfs: missing 'lowerdir'
[    9.095810] Initializing XFRM netlink socket
[   10.124461] workqueue: drm_fb_helper_damage_work hogged CPU for >10000us 64 times, consider switching to WQ_UNBOUND
[   99.381282] systemd-journald[378]: /var/log/journal/edeac53ea8cfb977d58ebcbdb85a3b30/user-1000.journal: Journal file uses a different sequence number ID, rotating.


---

### 评论 #5 — emotroshylov (2025-02-25T14:03:48Z)

> Hi [@emotroshylov](https://github.com/emotroshylov), can you provide the `dmesg` output around the time of the hang?

Hi @schung-amd 
Additional debug info

ltrace -C /opt/rocm-6.3.3/bin/clinfo
....
operator delete(void*, unsigned long)(0x5778a23bc890, 8, 0x577dd5b1eb0c, 5)     = 0
operator delete(void*, unsigned long)(0x5778a23bcc70, 8, 0x577dd5b1ea4c, 3)     = 0
operator new(unsigned long)(8, 0x5778a23bcc60, 0x577dd5b1eb2c, 4)               = 0x5778a23bcc70
clBuildProgram(0x5778a22c3870, 1, 0x5778a23bcc70, 0)                            = 0
clGetProgramInfo(0x5778a22c3870, 4451, 0, 0)                                    = 0
operator new(unsigned long)(8, 4451, 0x74173cbad58c, 0)                         = 0x5778a23bc890
clGetProgramInfo(0x5778a22c3870, 4451, 8, 0x5778a23bc890)                       = 0
operator new(unsigned long)(16, 0, 0x7ffffffffffffff, 0x5778a23bc890)           = 0x5778a23bcdf0
clRetainDevice(0x5778a23b2330, 0, 0x5778a23bce00, 0x5778a23bce00)               = 0
operator delete(void*, unsigned long)(0x5778a23bc890, 8, 0x74173cf440e0, 0x5778a23bce00) = 0
clGetProgramBuildInfo(0x5778a22c3870, 0x5778a23b2330, 4483, 0)                  = 0
operator new(unsigned long)(1, 0x5778a22c4168, 15, 0x74173cbad5b0)              = 0x5778a23bc890
clGetProgramBuildInfo(0x5778a22c3870, 0x5778a23b2330, 4483, 1)                  = 0
std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_replace(unsigned long, unsigned long, char const*, unsigned long)(0x7ffc1b274620, 0, 0, 0x7ffc1b274650) = 0x7ffc1b274620
operator delete(void*, unsigned long)(0x5778a23bc890, 1, 0, 0)                  = 0
clRetainDevice(0x5778a23b2330, 0x5778a23bc880, 0x577dd520b20c, 6)               = 0
operator new(unsigned long)(48, 0, 0, 0x2aaaaaaaaaaaaaa)                        = 0x5778a2477d20
clReleaseDevice(0x5778a23b2330, 0x7ffc1b274660, 0, 0x5778a2477d20)              = 0
operator delete(void*, unsigned long)(0x5778a23bcdf0, 16, 0x74173cf440e0, 0x5778a2477d20) = 0
clReleaseDevice(0x5778a23b2330, 0x5778a23bcde0, 0x577dd5b1eb2c, 7)              = 0
operator delete(void*, unsigned long)(0x5778a2477d20, 48, 0x74173cf440e0, 7)    = 2
operator delete(void*, unsigned long)(0x5778a23bcc70, 8, 0x577dd53b1fd7, 2)     = 0x5778a23bc6c0
clCreateKernel(0x5778a22c3870, 0x57787b40a690, 0x7ffc1b2748d0, 0x5778a23bc6c0^C <no return ...>
--- SIGINT (Interrupt) ---
+++ killed by SIGINT +++


---

### 评论 #6 — emotroshylov (2025-02-25T15:30:23Z)

> Hi [@emotroshylov](https://github.com/emotroshylov), can you provide the `dmesg` output around the time of the hang?

@schung-amd 
debug info from rocgdb /opt/rocm-6.3.3/bin/clinfo
```

  Global memory size:				 48301604864
  Constant buffer size:				 41056364128
  Max number of constant args:			 8
  Local memory type:				 Local
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 2401658464
  Max global variable size:			 41056364128
  Max global variable preferred total size:	 48301604864
  Max read/write image args:			 64
  Max on device events:				 1024
  Queue on device max size:			 8388608
  Max on device queues:				 1
  Queue on device preferred size:		 262144
  SVM capabilities:				 
    Coarse grain buffer:			 Yes
    Fine grain buffer:				 Yes
    Fine grain system:				 No
    Atomics:					 No
  Preferred platform atomic alignment:		 0
  Preferred global atomic alignment:		 0
  Preferred local atomic alignment:		 0
[New Thread 0x7ffee4e006c0 (LWP 28793)]
^C
Thread 1 "clinfo" received signal SIGINT, Interrupt.
0x00007fffee87731e in rocr::__rdtsc () at /usr/lib/gcc/x86_64-linux-gnu/13/include/ia32intrin.h:114
114	  return __builtin_ia32_rdtsc ();
(gdb) bt
#0  0x00007fffee87731e in rocr::__rdtsc () at /usr/lib/gcc/x86_64-linux-gnu/13/include/ia32intrin.h:114
#1  rocr::timer::fast_clock::raw_now () at /src/ROCR-Runtime/runtime/hsa-runtime/core/util/timer.h:149
#2  rocr::timer::fast_clock::now () at /src/ROCR-Runtime/runtime/hsa-runtime/core/util/timer.h:140
#3  rocr::core::InterruptSignal::WaitRelaxed (this=0x555555752f60, condition=HSA_SIGNAL_CONDITION_LT, compare_value=1, 
    timeout=<optimized out>, wait_hint=HSA_WAIT_STATE_ACTIVE)
    at /src/ROCR-Runtime/runtime/hsa-runtime/core/runtime/interrupt_signal.cpp:212
#4  0x00007fffee87717e in rocr::core::InterruptSignal::WaitAcquire (this=<optimized out>, condition=<optimized out>, 
    compare_value=<optimized out>, timeout=<optimized out>, wait_hint=<optimized out>)
    at /src/ROCR-Runtime/runtime/hsa-runtime/core/runtime/interrupt_signal.cpp:265
#5  0x00007fffee86b5f1 in rocr::HSA::hsa_signal_wait_scacquire (hsa_signal=..., 
    condition=condition@entry=HSA_SIGNAL_CONDITION_LT, compare_value=compare_value@entry=1, 
    timeout_hint=timeout_hint@entry=18446744073709551615, wait_state_hint=wait_state_hint@entry=HSA_WAIT_STATE_ACTIVE)
    at /src/ROCR-Runtime/runtime/hsa-runtime/core/runtime/hsa.cpp:1239
#6  0x00007fffee83ee30 in rocr::AMD::BlitKernel::SubmitLinearCopyCommand (this=0x5555556b91c0, dst=0x7ffff7e82000, 
    src=0x7ffff7a1a000, size=12288) at /src/ROCR-Runtime/runtime/hsa-runtime/core/runtime/amd_blit_kernel.cpp:1015
#7  0x00007fffee85f7a8 in rocr::(anonymous namespace)::RegionMemory::Freeze (this=0x555555749aa0)
    at /src/ROCR-Runtime/runtime/hsa-runtime/core/runtime/amd_loader_context.cpp:354
#8  0x00007fffee8b4db2 in rocr::amd::hsa::loader::Segment::Freeze (this=0x555555672bb0)
    at /src/ROCR-Runtime/runtime/hsa-runtime/loader/executable.cpp:706
#9  rocr::amd::hsa::loader::ExecutableImpl::Freeze (this=0x555555cded00, options=<optimized out>)
    at /src/ROCR-Runtime/runtime/hsa-runtime/loader/executable.cpp:1945
#10 0x00007fffee8b5eeb in rocr::amd::hsa::loader::AmdHsaCodeLoader::FreezeExecutable (this=0x555555587240, 
    executable=0x555555cded00, options=<optimized out>) at /src/ROCR-Runtime/runtime/hsa-runtime/loader/executable.cpp:237
#11 0x00007fffee86ddcb in rocr::HSA::hsa_executable_freeze (executable=..., options=0x0)
    at /src/ROCR-Runtime/runtime/hsa-runtime/core/runtime/hsa.cpp:2330
#12 0x00007ffff7b384e3 in amd::roc::LightningProgram::setKernels (this=0x55555557a070, binary=0x555555c37070, 
    binSize=<optimized out>, fdesc=<optimized out>, foffset=<optimized out>, uri=...)
    at /src/clr/rocclr/device/rocm/rocprogram.cpp:328
#13 0x00007ffff7b747ea in amd::device::Program::loadLC (this=this@entry=0x55555557a070)
    at /src/clr/rocclr/device/devprogram.cpp:1867
#14 0x00007ffff7b74823 in amd::device::Program::load (this=this@entry=0x55555557a070)
    at /src/clr/rocclr/device/devprogram.cpp:1878
#15 0x00007ffff7b14c07 in amd::Program::load (this=this@entry=0x555555579860, devices=...)
    at /src/clr/rocclr/platform/program.cpp:616
#16 0x00007ffff7ad79f2 in clCreateKernel (program=0x555555579870, kernel_name=0x555555562690 "hello", errcode_ret=0x7fffffffdfd0)
    at /src/clr/opencl/amdocl/cl_program.cpp:1313
#17 0x0000555555559b0e in cl::Kernel::Kernel (err=0x7fffffffdebc, name=0x555555562690 "hello", program=..., 
    this=<synthetic pointer>) at /src/clr/opencl/tools/clinfo/../../khronos/headers/opencl2.2/CL/cl2.hpp:1693
#18 main (argc=<optimized out>, argv=<optimized out>) at /src/clr/opencl/tools/clinfo/clinfo.cpp:633
(gdb)
```

---

### 评论 #7 — schung-amd (2025-02-28T15:57:28Z)

@emotroshylov Thanks for all the debug info! This looks like another recent issue with Xen-based virtualization (https://github.com/ROCm/ROCm/issues/4253, https://github.com/ROCm/ROCm/issues/4259). We don't officially support Xen-based virtualization, but it does seem to work in some configurations (that user was able to get ROCm working with XCP-ng + Fedora after setting `gfx_passthrough = 1` in xlconfig).

---

### 评论 #8 — schung-amd (2025-04-23T17:36:07Z)

Closing for now as we don't support Xen-based virtualization. Hopefully the linked issues help you find a working config, if you need further guidance feel free to comment and we can reopen if necessary.

---
