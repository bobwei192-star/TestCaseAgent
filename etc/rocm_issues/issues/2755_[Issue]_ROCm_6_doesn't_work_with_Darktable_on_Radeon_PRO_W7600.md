# [Issue]: ROCm 6 doesn't work with Darktable on Radeon PRO W7600

> **Issue #2755**
> **状态**: closed
> **创建时间**: 2023-12-19T21:29:52Z
> **更新时间**: 2023-12-21T23:31:19Z
> **关闭时间**: 2023-12-21T23:17:02Z
> **作者**: illwieckz
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2755

## 描述

### Problem Description

Running Darktable with ROCm OpenCL fills the `dmesg` log with errors and makes Darktable crash.

I run a professionnal workstation sporting an AMD Radeon PRO W7600 and an AMD Ryzen Threadripper PRO 3955WX.
I installed AMDGPU-PRO 6.0 with ROCm 6.0, I installed the dkms module and the ROCm OpenCL stack.

### Operating System

Ubuntu 23.10 Mantic Minautor

### CPU

AMD Ryzen Threadripper PRO 3955WX

### GPU

Other

### Other

AMD Radeon PRO W7600

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

```sh
wget 'https://repo.radeon.com/amdgpu-install/6.0/ubuntu/jammy/amdgpu-install_6.0.60000-1_all.deb'
sudo gdebi 'amdgpu-install_6.0.60000-1_all.deb'
sudo apt-get update
sudo apt-get install 'amdgpu-dkms' 'rocm-opencl-runtime'
sudo reboot

sudo apt-get install 'darktable'
darktable
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

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
  Name:                    AMD Ryzen Threadripper PRO 3955WX 16-Cores
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper PRO 3955WX 16-Cores
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
  Max Clock Freq. (MHz):   3900                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            32                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    263724068(0xfb81c24) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    263724068(0xfb81c24) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    263724068(0xfb81c24) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon PRO W7600               
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
  Max Clock Freq. (MHz):   1940                               
  BDFID:                   33536                              
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
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      16                                 
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
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
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

Some `dmesg` log:

```
[245121.541853] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[245121.541869] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000019e601000 from client 10
[245121.541876] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[245121.541881] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[245121.541886] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[245121.541891] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[245121.541895] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[245121.541899] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[245121.541903] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[245192.524439] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[245192.524452] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000801000 from client 10
[245192.524458] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[245192.524463] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[245192.524468] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[245192.524472] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[245192.524476] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[245192.524480] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[245192.524484] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[245214.965680] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[245214.965691] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007f086c002000 from client 10
[245214.965695] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[245214.965698] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[245214.965701] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[245214.965704] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[245214.965707] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[245214.965710] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[245214.965713] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[245219.905322] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[245219.905336] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007f086c002000 from client 10
[245219.905342] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[245219.905346] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[245219.905351] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[245219.905355] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[245219.905359] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[245219.905363] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[245219.905367] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[245220.301490] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[245220.301503] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007f086c002000 from client 10
[245220.301508] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[245220.301512] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[245220.301517] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[245220.301520] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[245220.301524] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[245220.301527] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[245220.301531] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[245287.498754] darktable[423198]: segfault at 0 ip 0000000000000000 sp 00007ffe371c06d8 error 14 in darktable[5582f96ce000+1000] likely on CPU 16 (core 0, socket 0)
[245287.498771] Code: Unable to access opcode bytes at 0xffffffffffffffd6.
[245296.577249] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[245296.577263] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007f086c002000 from client 10
[245296.577269] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[245296.577274] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[245296.577279] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[245296.577283] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[245296.577287] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[245296.577291] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[245296.577296] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[245297.009658] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[245297.009671] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007f086c002000 from client 10
[245297.009677] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[245297.009682] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[245297.009687] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[245297.009691] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[245297.009695] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[245297.009699] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[245297.009703] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
```

---

## 评论 (9 条)

### 评论 #1 — illwieckz (2023-12-19T21:31:48Z)

It didn't work with ROCm 5.7 either.

---

### 评论 #2 — b-sumner (2023-12-20T00:33:22Z)

@illwieckz have you raised an issue on the darktable repo?  Could you do a debug build and catch he memory fault with rocgdb?  If you could help narrow down the problem it could probably be addressed faster.

---

### 评论 #3 — illwieckz (2023-12-20T02:15:47Z)

It looks like the crash itself is in darktable in some preferences code, not in ROCm. It maybe caused by ROCm (for example if some string is nullptr or I don't know what), but rocgdb shows absolutely nothing useful, and the default backtrace of darktable no more (this darktable build is a debug build with a mechanism to automatically dump backtraces in case of crash).

Especially, Darktable says it doesn't use ROCm because ROCm is detected to be too slow to be usable, that's not normal but I don't know yet if that's a darktable or ROCm fault yet.

What remains that is sure, and that is a ROCm fault for sure, are all those page faults:

```
$ sudo dmesg -w &
$ darktable -d opencl
     0.7204 [dt_get_sysresource_level] switched to 1 as `default'
     0.7205   total mem:       257543MB
     0.7205   mipmap cache:    32192MB
     0.7205   available mem:   128771MB
     0.7205   singlebuff:      2012MB
     0.7205   OpenCL tune mem: OFF
     0.7205   OpenCL pinned:   OFF
[opencl_init] opencl related configuration options:
[opencl_init] opencl: OFF
[opencl_init] opencl_scheduling_profile: 'very fast GPU'
[opencl_init] opencl_library: 'default path'
[opencl_init] opencl_device_priority: '*/!0,*/*/*'
[opencl_init] opencl_mandatory_timeout: 200
[opencl_init] opencl library 'libOpenCL' found on your system and loaded
[opencl_init] found 1 platform
[opencl_init] found 1 device
[dt_opencl_device_init]
   DEVICE:                   0: 'gfx1102'
   PLATFORM NAME & VENDOR:   AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc.
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx1102
   DRIVER VERSION:           3602.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 2.0 
   DEVICE_TYPE:              GPU
   GLOBAL MEM SIZE:          8176 MB
   MAX MEM ALLOC:            6950 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   MEMORY TUNING:            NO
   FORCED HEADROOM:          400
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH:            16
   ROUNDUP HEIGHT:           16
   CHECK EVENT HANDLES:      128
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /opt/illwieckz/.cache/darktable/cached_v1_kernels_for_AMDAcceleratedParallelProcessinggfx1102_36020HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
[266010.479083] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.479097] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.479103] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.479107] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.479112] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.479116] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.479120] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.479123] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.479127] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
   KERNEL LOADING TIME:       0.0248 sec
[opencl_init] OpenCL successfully initialized. Internal numbers and names of available devices:
[opencl_init]		0	'AMD Accelerated Parallel Processing gfx1102'
[opencl_init] FINALLY: opencl is AVAILABLE and NOT ENABLED.
[266010.504446] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.504459] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.504466] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.504472] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.504477] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.504482] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.504487] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.504491] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.504496] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.508273] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.508285] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.508292] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.508297] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.508303] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.508308] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.508312] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.508317] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.508321] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.511398] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.511404] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.511407] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.511410] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.511412] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.511414] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.511416] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.511418] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.511420] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.514873] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.514878] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.514881] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.514883] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.514885] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.514888] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.514890] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.514892] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.514894] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.518453] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.518459] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.518462] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.518465] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.518467] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.518469] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.518472] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.518474] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.518476] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.521809] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.521818] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.521823] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.521828] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.521832] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.521836] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.521840] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.521844] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.521848] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.524879] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.524886] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.524891] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.524895] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.524899] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.524902] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.524906] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.524909] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.524913] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.527429] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.527438] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.527443] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.527447] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.527451] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.527456] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.527460] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.527464] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.527468] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266010.529906] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266010.529914] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266010.529919] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266010.529926] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266010.529934] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266010.529937] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266010.529941] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266010.529944] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266010.529949] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[opencl_init] due to a slow GPU the opencl flag has been set to OFF.
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
[266016.114062] gmc_v11_0_process_interrupt: 16 callbacks suppressed
[266016.114069] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266016.114083] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266016.114090] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266016.114095] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266016.114100] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266016.114105] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266016.114109] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266016.114114] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266016.114118] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266016.125821] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266016.125830] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266016.125836] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266016.125840] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266016.125844] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266016.125847] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266016.125851] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266016.125854] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266016.125858] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266016.219515] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266016.219529] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266016.219535] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266016.219540] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266016.219545] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266016.219549] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266016.219553] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266016.219557] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266016.219561] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266016.355095] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266016.355108] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266016.355114] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266016.355119] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266016.355124] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266016.355128] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266016.355132] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266016.355136] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266016.355140] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266016.439643] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266016.439658] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266016.439665] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266016.439670] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266016.439675] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266016.439680] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266016.439684] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266016.439688] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266016.439693] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266016.577729] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266016.577741] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266016.577746] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266016.577750] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266016.577755] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266016.577758] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266016.577762] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266016.577765] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266016.577769] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266017.022868] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266017.022882] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266017.022888] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266017.022893] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266017.022898] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266017.022902] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266017.022907] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266017.022911] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266017.022914] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266017.033202] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266017.033213] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266017.033219] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266017.033224] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266017.033229] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266017.033234] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266017.033238] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266017.033242] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266017.033246] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266017.672945] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266017.672958] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266017.672964] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266017.672969] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266017.672973] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266017.672978] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266017.672981] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266017.672985] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266017.672989] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266017.691320] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266017.691336] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266017.691344] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266017.691350] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266017.691356] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266017.691362] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266017.691367] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266017.691373] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266017.691378] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266024.458431] gmc_v11_0_process_interrupt: 2 callbacks suppressed
[266024.458436] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266024.458445] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266024.458449] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266024.458452] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266024.458455] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266024.458457] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266024.458460] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266024.458462] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266024.458464] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[266291.156157] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266291.156171] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007fffec27d000 from client 10
[266291.156178] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266291.156184] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266291.156189] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266291.156194] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266291.156198] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266291.156203] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266291.156207] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
```

Actually just listing OpenCL devices produce such page fault:

```
$ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
[266981.949740] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[266981.949754] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000d8a01000 from client 10
[266981.949761] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[266981.949766] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[266981.949772] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[266981.949776] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[266981.949781] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[266981.949785] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[266981.949789] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
```

Darktable is not responsible for such page fault, since even `clinfo` triggers them.

---

### 评论 #4 — illwieckz (2023-12-20T02:40:31Z)

I noticed that `/opt/rocm-6.0.0/bin/clinfo` doesn't trigger any page fault. And my own build of another software (luxmark 3.1) doesn't trigger page fault.

So it looks like some ROCm library is incompatible with some software for some unknown reason, and when that happens this triggers page faults.

So I investigated more, if I use ROCm's libOpenCL.so I don't get page faults with system's clinfo:

```
$ LD_LIBRARY_PATH=/opt/rocm-6.0.0/lib/ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
```

If I do the same with Darktable, it doesn't triggers page faults anymore:

```
$ LD_LIBRARY_PATH=/opt/rocm-6.0.0/lib/ darktable -d opencl
     0.7095 [dt_get_sysresource_level] switched to 1 as `default'
     0.7095   total mem:       257543MB
     0.7095   mipmap cache:    32192MB
     0.7095   available mem:   128771MB
     0.7095   singlebuff:      2012MB
     0.7095   OpenCL tune mem: OFF
     0.7095   OpenCL pinned:   OFF
[opencl_init] opencl related configuration options:
[opencl_init] opencl: OFF
[opencl_init] opencl_scheduling_profile: 'very fast GPU'
[opencl_init] opencl_library: 'default path'
[opencl_init] opencl_device_priority: '*/!0,*/*/*'
[opencl_init] opencl_mandatory_timeout: 200
[opencl_init] opencl library 'libOpenCL' found on your system and loaded
[opencl_init] found 1 platform
[opencl_init] found 1 device

[dt_opencl_device_init]
   DEVICE:                   0: 'gfx1102'
   PLATFORM NAME & VENDOR:   AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc.
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx1102
   DRIVER VERSION:           3602.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 2.0 
   DEVICE_TYPE:              GPU
   GLOBAL MEM SIZE:          8176 MB
   MAX MEM ALLOC:            6950 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   MEMORY TUNING:            NO
   FORCED HEADROOM:          400
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH:            16
   ROUNDUP HEIGHT:           16
   CHECK EVENT HANDLES:      128
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /opt/illwieckz/.cache/darktable/cached_v1_kernels_for_AMDAcceleratedParallelProcessinggfx1102_36020HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
   KERNEL LOADING TIME:       0.0245 sec
[opencl_init] OpenCL successfully initialized. Internal numbers and names of available devices:
[opencl_init]		0	'AMD Accelerated Parallel Processing gfx1102'
[opencl_init] FINALLY: opencl is AVAILABLE and NOT ENABLED.
[opencl_init] due to a slow GPU the opencl flag has been set to OFF.
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
```

I still get the crash in Darktable's preferences but we may now ignore this, unless I miss something this one looks to be Darktable's fault.

So what's left is ROCm being broken with other libOpenCL, this may be other libOpenCL's fault, I now have a workaround to avoid them.

I don't know yet if Darktable considering an AMD Radeon Pro W7600 to be slow is a problem on ROCm's side or Darktable's side.

---

### 评论 #5 — b-sumner (2023-12-20T17:51:12Z)

@illwieckz I'm glad you have a workaround.  I would definitely recommend preferring ROCm supplied libraries over others.  I'm actually not clear how you picked up another libOpenCL.so since that ships with ROCm along with libamdocl64.so which has the OpenCL runtime.  I would assume that the Darktable developers have not tuned for AMD GFX11 GPUs...hopefully that will change.

---

### 评论 #6 — illwieckz (2023-12-21T22:26:14Z)

Unfortunately there is no workaround. I was tricked by the fact the faults do not happen everytime.

> I'm actually not clear how you picked up another libOpenCL.so since that ships with ROCm along with libamdocl64.so which has the OpenCL runtime.

Ubuntu has a standard libOpenCL, and other OpenCL drivers may do the same thing as ROCm and also install their own libOpenCL. It should not be needed to ship its own libOpenCL, but if it happens, OpenCL drivers should be compatible with any libOpenCL. Also, it's perfectly normal to use more than one OpenCL drivers (there can be other devices to use), and if those drivers tend to do like ROCm, you end with multiple libOpenCL, each of them fighting for priority. But anyway all of this is not important with the current problem, as the GPU faults happen with ROCm-provided libOpenCL anyway. For example with this simple `clinfo --list` command, I usually have to wait some seconds to reproduce the error, whatever the libOpenCL used.

In the next example I will list ROCm OpenCL devices with ROCm OpenCL drivers with, 1. AMD ROCm-provided libOpenCL, 2. Ubuntu standard libOpenCL, 3. Intel OneAPI libOpenCL. ROCm triggers GPU faults with all of those libOpenCL, even with the one provided with ROCm. The following test runs `clinfo --list` for 5 times every 4s. Some `clinfo --list` commands triggers GPU faults, some other don't:

### AMD ROCm libOpenCL with ROCm OpenCL `libamdocl64.so` driver and Radeon PRO W7600 ROCm device:

```
$ ( export LD_PRELOAD=/opt/rocm-6.0.0/lib/libOpenCL.so.1.2 ; for i in {1..5} ; do ( set -x ; date --iso-8601=s ; clinfo --list ) ; sleep 4s; done )
+ date --iso-8601=s
2023-12-21T22:27:50+01:00
+ clinfo --list
[422569.632195] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[422569.632209] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[422569.632214] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[422569.632214] amdgpu 0000:83:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0027 address=0xb05f5000 flags=0x0000]
[422569.632220] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[422569.632223] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[422569.632227] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[422569.632231] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[422569.632235] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[422569.632238] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[422569.632266] amdgpu 0000:83:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x0027 address=0xb05f5000 flags=0x0020]
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:27:54+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:27:58+01:00
+ clinfo --list
[422577.765138] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[422577.765152] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000001d1c01000 from client 10
[422577.765157] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[422577.765162] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[422577.765166] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[422577.765170] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[422577.765173] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[422577.765177] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[422577.765180] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:28:02+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:28:06+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
```

### Ubuntu standard libOpenCL with ROCm OpenCL `libamdocl64.so` driver and Radeon PRO W7600 ROCm device:

```
$ ( export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libOpenCL.so.1.0.0 ; for i in {1..5} ; do ( set -x ; date --iso-8601=s ; clinfo --list ) ; sleep 4s; done )
+ date --iso-8601=s
2023-12-21T22:26:54+01:00
+ clinfo --list
[422513.797031] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[422513.797045] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000001eea01000 from client 10
[422513.797052] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[422513.797057] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[422513.797062] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[422513.797066] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[422513.797070] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[422513.797074] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[422513.797078] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:26:58+01:00
+ clinfo --list
[422517.867940] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[422517.867951] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000001db601000 from client 10
[422517.867955] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[422517.867959] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[422517.867962] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[422517.867965] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[422517.867968] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[422517.867971] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[422517.867973] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:27:02+01:00
+ clinfo --list
[422521.936505] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[422521.936518] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000001eec01000 from client 10
[422521.936525] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[422521.936529] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[422521.936534] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[422521.936538] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[422521.936543] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[422521.936547] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[422521.936550] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:27:06+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:27:10+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
```

### Intel OneAPI libOpenCL with ROCm OpenCL `libamdocl64.so` driver and Radeon PRO W7600 ROCm device:

```
$ ( export LD_PRELOAD=/opt/intel/oneapi/lib/libOpenCL.so.1.2 ; for i in {1..5} ; do ( set -x ; date --iso-8601=s ; clinfo --list ) ; sleep 4s; done )
+ date --iso-8601=s
2023-12-21T22:30:15+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:30:19+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:30:23+01:00
+ clinfo --list
[422722.381314] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[422722.381327] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000001eec01000 from client 10
[422722.381333] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[422722.381337] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[422722.381342] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[422722.381346] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[422722.381349] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[422722.381353] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[422722.381356] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
+ date --iso-8601=s
2023-12-21T22:30:27+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
[422726.454882] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[422726.454896] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000001eec01000 from client 10
[422726.454902] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[422726.454907] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[422726.454912] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[422726.454917] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[422726.454921] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[422726.454925] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[422726.454929] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
+ date --iso-8601=s
2023-12-21T22:30:31+01:00
+ clinfo --list
Platform #0: AMD Accelerated Parallel Processing
 `-- Device #0: gfx1102
```

The common denominator to those GPU fault is always the `amdgpu-dkms` kernel module, the ROCm `libamdocl64.so` OpenCL driver, and the Radeon PRO W7600 ROCm device.

---

### 评论 #7 — illwieckz (2023-12-21T23:10:04Z)

I believe the GPU fault problem happens with any OpenCL too, here is what I get with `darktable-cltest`:

```
( export LD_PRELOAD=/opt/rocm-6.0.0/lib/libOpenCL.so.1.2 ; darktable-cltest )
     0.0230 [dt_get_sysresource_level] switched to 1 as `default'
     0.0231   total mem:       257543MB
     0.0231   mipmap cache:    32192MB
     0.0231   available mem:   128771MB
     0.0231   singlebuff:      2012MB
     0.0231   OpenCL tune mem: OFF
     0.0231   OpenCL pinned:   OFF
[opencl_init] opencl related configuration options:
[opencl_init] opencl: OFF
[opencl_init] opencl_scheduling_profile: 'very fast GPU'
[opencl_init] opencl_library: 'default path'
[opencl_init] opencl_device_priority: '*/!0,*/*/*'
[opencl_init] opencl_mandatory_timeout: 200
[opencl_init] opencl library 'libOpenCL' found on your system and loaded
[428464.665471] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428464.665484] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000b7a01000 from client 10
[428464.665490] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428464.665494] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428464.665498] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428464.665502] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428464.665505] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428464.665509] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428464.665512] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[opencl_init] found 1 platform
[opencl_init] found 1 device

[dt_opencl_device_init]
   DEVICE:                   0: 'gfx1102'
   PLATFORM NAME & VENDOR:   AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc.
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx1102
   DRIVER VERSION:           3602.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 2.0 
   DEVICE_TYPE:              GPU
   GLOBAL MEM SIZE:          8176 MB
   MAX MEM ALLOC:            6950 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   MEMORY TUNING:            NO
   FORCED HEADROOM:          400
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH:            16
   ROUNDUP HEIGHT:           16
   CHECK EVENT HANDLES:      128
   PERFORMANCE:              0.000
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /opt/illwieckz/.cache/darktable/cached_v1_kernels_for_AMDAcceleratedParallelProcessinggfx1102_36020HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
   KERNEL LOADING TIME:       0.0291 sec
[opencl_init] OpenCL successfully initialized. Internal numbers and names of available devices:
[opencl_init]		0	'AMD Accelerated Parallel Processing gfx1102'
[opencl_init] FINALLY: opencl is AVAILABLE and NOT ENABLED.
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
```

Here is what I get with `luxmark` v3.1:

```
[428544.555988] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428544.556000] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000b7a01000 from client 10
[428544.556006] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428544.556010] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428544.556014] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428544.556018] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428544.556022] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428544.556025] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428544.556029] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
```

Though LuxMark computes the render properly.

We may then rename the issue or open a new one for those GPU faults.

---

### 评论 #8 — illwieckz (2023-12-21T23:16:45Z)

I managed to force Darktable to run with OpenCL on the Radeon Pro W7600 by using the `-config opencl=TRUE` option. I rendered some images properly.

So I can confirm it works. The `dmesg` is still full of GPU faults, this would deserve a decated thread.

```
( export LD_PRELOAD=/opt/rocm-6.0.0/lib/libOpenCL.so.1.2 ; darktable-cltest --conf opencl=TRUE )
     0.0237 [dt_get_sysresource_level] switched to 1 as `default'
     0.0237   total mem:       257543MB
     0.0237   mipmap cache:    32192MB
     0.0237   available mem:   128771MB
     0.0237   singlebuff:      2012MB
     0.0237   OpenCL tune mem: OFF
     0.0237   OpenCL pinned:   OFF
[opencl_init] opencl related configuration options:
[opencl_init] opencl: ON
[opencl_init] opencl_scheduling_profile: 'very fast GPU'
[opencl_init] opencl_library: 'default path'
[opencl_init] opencl_device_priority: '*/!0,*/*/*'
[opencl_init] opencl_mandatory_timeout: 200
[opencl_init] opencl library 'libOpenCL' found on your system and loaded
[428815.091244] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428815.091253] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000015d801000 from client 10
[428815.091256] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428815.091259] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428815.091261] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428815.091263] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428815.091265] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428815.091267] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428815.091269] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[opencl_init] found 1 platform
[opencl_init] found 1 device

[dt_opencl_device_init]
   DEVICE:                   0: 'gfx1102'
   PLATFORM NAME & VENDOR:   AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc.
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx1102
   DRIVER VERSION:           3602.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 2.0 
   DEVICE_TYPE:              GPU
   GLOBAL MEM SIZE:          8176 MB
   MAX MEM ALLOC:            6950 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   MEMORY TUNING:            NO
   FORCED HEADROOM:          400
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH:            16
   ROUNDUP HEIGHT:           16
   CHECK EVENT HANDLES:      128
   PERFORMANCE:              0.000
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /opt/illwieckz/.cache/darktable/cached_v1_kernels_for_AMDAcceleratedParallelProcessinggfx1102_36020HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
   KERNEL LOADING TIME:       0.0306 sec
[opencl_init] OpenCL successfully initialized. Internal numbers and names of available devices:
[opencl_init]		0	'AMD Accelerated Parallel Processing gfx1102'
[opencl_init] FINALLY: opencl is AVAILABLE and ENABLED.
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
```

```
( export LD_PRELOAD=/opt/rocm-6.0.0/lib/libOpenCL.so.1.2 ; darktable -d opencl --conf opencl=TRUE )
     9.8147 [dt_get_sysresource_level] switched to 1 as `default'
     9.8147   total mem:       257543MB
     9.8147   mipmap cache:    32192MB
     9.8147   available mem:   128771MB
     9.8147   singlebuff:      2012MB
     9.8147   OpenCL tune mem: OFF
     9.8147   OpenCL pinned:   OFF
[opencl_init] opencl related configuration options:
[opencl_init] opencl: ON
[opencl_init] opencl_scheduling_profile: 'very fast GPU'
[opencl_init] opencl_library: 'default path'
[opencl_init] opencl_device_priority: '*/!0,*/*/*'
[opencl_init] opencl_mandatory_timeout: 200
[opencl_init] opencl library 'libOpenCL' found on your system and loaded
[428875.282803] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428875.282818] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000001000 from client 10
[428875.282824] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428875.282829] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428875.282834] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428875.282838] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428875.282842] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428875.282846] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428875.282850] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[opencl_init] found 1 platform
[opencl_init] found 1 device

[dt_opencl_device_init]
   DEVICE:                   0: 'gfx1102'
   PLATFORM NAME & VENDOR:   AMD Accelerated Parallel Processing, Advanced Micro Devices, Inc.
   CANONICAL NAME:           amdacceleratedparallelprocessinggfx1102
   DRIVER VERSION:           3602.0 (HSA1.1,LC)
   DEVICE VERSION:           OpenCL 2.0 
   DEVICE_TYPE:              GPU
   GLOBAL MEM SIZE:          8176 MB
   MAX MEM ALLOC:            6950 MB
   MAX IMAGE SIZE:           16384 x 16384
   MAX WORK GROUP SIZE:      256
   MAX WORK ITEM DIMENSIONS: 3
   MAX WORK ITEM SIZES:      [ 1024 1024 1024 ]
   ASYNC PIXELPIPE:          NO
   PINNED MEMORY TRANSFER:   NO
   MEMORY TUNING:            NO
   FORCED HEADROOM:          400
   AVOID ATOMICS:            NO
   MICRO NAP:                250
   ROUNDUP WIDTH:            16
   ROUNDUP HEIGHT:           16
   CHECK EVENT HANDLES:      128
   PERFORMANCE:              0.000
   TILING ADVANTAGE:         0.000
   DEFAULT DEVICE:           NO
   KERNEL BUILD DIRECTORY:   /usr/share/darktable/kernels
   KERNEL DIRECTORY:         /opt/illwieckz/.cache/darktable/cached_v1_kernels_for_AMDAcceleratedParallelProcessinggfx1102_36020HSA11LC
   CL COMPILER OPTION:       -cl-fast-relaxed-math
   KERNEL LOADING TIME:       0.0289 sec
[opencl_init] OpenCL successfully initialized. Internal numbers and names of available devices:
[opencl_init]		0	'AMD Accelerated Parallel Processing gfx1102'
[opencl_init] FINALLY: opencl is AVAILABLE and ENABLED.
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
[dt_opencl_update_priorities] these are your device priorities:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		0	0	0	0	0
[dt_opencl_update_priorities] show if opencl use is mandatory for a given pixelpipe:
[dt_opencl_update_priorities] 		image	preview	export	thumbs	preview2
[dt_opencl_update_priorities]		1	1	1	1	1
[opencl_synchronization_timeout] synchronization timeout set to 0
[428889.464701] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428889.464716] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000001000 from client 10
[428889.464722] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428889.464728] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428889.464733] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428889.464737] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428889.464742] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428889.464746] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428889.464751] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
    50.3435 [dt_opencl_check_tuning] use 5315MB (tunemem=OFF, pinning=OFF) on device `AMD Accelerated Parallel Processing gfx1102' id=0
[428915.922901] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428915.922912] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428915.922916] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428915.922919] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428915.922922] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428915.922924] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428915.922927] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428915.922929] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428915.922931] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428916.216043] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428916.216057] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428916.216063] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428916.216068] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428916.216073] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428916.216077] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428916.216082] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428916.216086] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428916.216090] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428916.236082] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428916.236095] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428916.236101] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428916.236106] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428916.236111] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428916.236115] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428916.236119] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428916.236123] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428916.236127] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428916.248713] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428916.248726] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428916.248732] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428916.248737] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428916.248742] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428916.248746] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428916.248750] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428916.248754] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428916.248758] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
    50.8802 [pixelpipe_process_CL]       [preview]      colorout               (   0/   0) 1197x 900 scale=1.0000 --> (   0/   0) 1197x 900 scale=1.0000 cl input data to host
[428916.318235] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428916.318244] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428916.318247] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428916.318250] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428916.318252] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428916.318254] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428916.318256] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428916.318259] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428916.318260] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428919.994856] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428919.994870] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428919.994877] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428919.994883] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428919.994888] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428919.994893] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428919.994897] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428919.994901] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428919.994906] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428921.235533] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428921.235547] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428921.235554] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428921.235559] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428921.235564] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428921.235568] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428921.235572] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428921.235576] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428921.235580] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428921.277958] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428921.277970] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428921.277976] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428921.277980] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428921.277985] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428921.277989] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428921.277993] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428921.277997] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428921.278001] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428921.293036] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428921.293048] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00000000e8601000 from client 10
[428921.293053] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428921.293058] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428921.293063] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428921.293067] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428921.293071] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428921.293075] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428921.293079] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
 [opencl_summary_statistics] device 'AMD Accelerated Parallel Processing gfx1102' (0): 276 out of 276 events were successful and 0 events lost. max event=143
```

---

### 评论 #9 — illwieckz (2023-12-21T23:31:18Z)

The protection fault issue is now tracked in its own dedicated thread:

- https://github.com/ROCm/ROCm/issues/2766

---
