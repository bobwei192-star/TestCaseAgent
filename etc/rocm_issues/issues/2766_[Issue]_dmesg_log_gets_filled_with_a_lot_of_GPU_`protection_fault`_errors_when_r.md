# [Issue]: dmesg log gets filled with a lot of GPU `protection fault` errors when running OpenCL applications 

> **Issue #2766**
> **状态**: closed
> **创建时间**: 2023-12-21T23:30:34Z
> **更新时间**: 2024-06-19T10:04:16Z
> **关闭时间**: 2024-06-19T10:04:16Z
> **作者**: illwieckz
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2766

## 描述

### Problem Description

The dmesg kernel log gets filled with a lot of GPU `protection fault` errors when running OpenCL applications. It happens whatever the application, even the simple `clinfo` tool triggers it (sometime you have to retry, but even this triggers it). Other applications like Darktable or Luxmark produce those GPU protection faults. This do not prevent to use OpenCL and applications are working, but something going is reported.

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

```
wget 'https://repo.radeon.com/amdgpu-install/6.0/ubuntu/jammy/amdgpu-install_6.0.60000-1_all.deb'
sudo gdebi 'amdgpu-install_6.0.60000-1_all.deb'
sudo apt-get update
sudo apt-get install 'amdgpu-dkms' 'rocm-opencl-runtime' 'clinfo'
sudo reboot
```

```
sudo dmesg -w &
clinfo --list
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

Example of error log with clinfo:

```
$ clinfo --list
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
```

Example of error log with luxmark:

```
LuxMark v3.1
Based on LuxCore v1.5
[429716.853652] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[429716.853662] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000401000 from client 10
[429716.853666] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[429716.853668] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[429716.853671] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[429716.853673] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[429716.853675] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[429716.853677] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[429716.853679] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
```

Example of error log with Darktable:

```
$ luxmark
[428875.282803] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428875.282818] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000001000 from client 10
[428875.282824] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428875.282829] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428875.282834] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428875.282838] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428875.282842] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428875.282846] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428875.282850] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
[428889.464701] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[428889.464716] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x0000000000001000 from client 10
[428889.464722] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[428889.464728] amdgpu 0000:83:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[428889.464733] amdgpu 0000:83:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[428889.464737] amdgpu 0000:83:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[428889.464742] amdgpu 0000:83:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[428889.464746] amdgpu 0000:83:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[428889.464751] amdgpu 0000:83:00.0: amdgpu: 	 RW: 0x0
```

```
$ darktable -d opencl --conf opencl=TRUE


I managed to force Darktable to run with OpenCL on the Radeon Pro W7600 by using the -config opencl=TRUE option. I rendered some images properly.

So I can confirm it works. The dmesg is still full of GPU faults, this would deserve a decated thread.

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

## 评论 (5 条)

### 评论 #1 — terryrankine (2023-12-22T03:10:23Z)

have you tried the this kernel param? - `amdgpu.vm_update_mode=3` 
I find it hides a bunch of these page faults - which makes me wonder whats actually happening.....


---

### 评论 #2 — sid-cypher (2023-12-26T08:07:42Z)

Same issue on the supported Ubuntu 22.04, with Radeon RX 7900 XTX (gfx1100), ROCm 6.0.0.
```
sudo dmesg -Hw
...
[Dez26 08:58] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  +0,000007] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000000000b91000 from client 10
[  +0,000004] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[  +0,000003] amdgpu 0000:09:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[  +0,000002] amdgpu 0000:09:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  +0,000002] amdgpu 0000:09:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[  +0,000002] amdgpu 0000:09:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  +0,000002] amdgpu 0000:09:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  +0,000002] amdgpu 0000:09:00.0: amdgpu: 	 RW: 0x0
```
Running `clinfo` many times does not produce the error repeatedly, but the initial attempt does, and the error occurs frequently with Stable Diffusion work.

---

### 评论 #3 — ppanchad-amd (2024-05-17T19:10:33Z)

@illwieckz Can you please check if you are still seeing the same error messages with latest ROCm 6.1.1? Thanks!

---

### 评论 #4 — illwieckz (2024-06-17T04:34:02Z)

> @illwieckz Can you please check if you are still seeing the same error messages with latest ROCm 6.1.1? Thanks!

Since the comment suggestion above by `terryrankine` I'm running the kernel with `amdgpu.vm_update_mode=3` and that was good enough to silence the message.

I'll have to reboot the computer to test without that option and see if the error is now silenced without that option.

I'll test later when it's possible for me to reboot the machine and report back.

---

### 评论 #5 — illwieckz (2024-06-19T10:04:16Z)

@ppanchad-amd I confirm that with ROCm 6.1.2 I don't need the `amdgpu.vm_update_mode=3` kernel option anymore to avoid the previously experienced page faults.

---
