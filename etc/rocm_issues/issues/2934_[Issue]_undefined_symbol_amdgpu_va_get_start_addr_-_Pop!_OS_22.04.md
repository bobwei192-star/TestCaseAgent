# [Issue]: undefined symbol: amdgpu_va_get_start_addr - Pop!_OS 22.04

> **Issue #2934**
> **状态**: closed
> **创建时间**: 2024-02-27T22:15:05Z
> **更新时间**: 2024-09-17T17:36:54Z
> **关闭时间**: 2024-07-04T19:41:25Z
> **作者**: RAD750
> **标签**: ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2934

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

Hi, apologies if the bug report is of bad quality, but I am a beginner at this.
I have a RX 7600 that I'd like to use for OpenCL computing. With mesa-opencl-icd OpenCL fails with an error message `No such file or directory: /usr/lib/clc/gfx1102-amdgcn-mesa-mesa3d.bc`

Therefore, I thought that maybe I need AMDGPU-pro to make it work. So I installed it following the procedure below, and it worked flawlessly for a while, but then stopped working all of a sudden.

If I run clinfo, I get:
```
jacopo@prodesk:~$ clinfo
clinfo: symbol lookup error: /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_[radeonsi.so](http://radeonsi.so/): undefined symbol: amdgpu_va_get_start_addr
```

As soon as I run `amdgpu-uninstall` even without rebooting, clinfo starts working again (but no compute can be done due to the mesa error above)

I am at a loss, and any pointer can help. Thanks!

### Operating System

Pop!_OS 22.04 LTS

### CPU

Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz

### GPU

AMD Radeon RX 7600

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm (OpenCL)

### Steps to Reproduce

Installation steps:
```
sudo amdgpu-install --usecase=opencl --no-dkms
sudo usermod -a -G video $LOGNAME
sudo usermod -a -G render $LOGNAME
sudo apt install opencl-headers ocl-icd-libopencl1 clinfo -y
sudo apt-get install amdgpu-lib rocm-opencl-runtime rocm-hip-runtime -y
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
  Name:                    Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz
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
  Max Clock Freq. (MHz):   4400                               
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
      Size:                    32779032(0x1f42b18) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32779032(0x1f42b18) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32779032(0x1f42b18) KB             
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
  Marketing Name:          AMD Radeon RX 7600                 
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
  Max Clock Freq. (MHz):   2250                               
  BDFID:                   768                                
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

Kernel is: `6.6.10-76060610-generic #202401051437~1704728131~22.04~24d69e2` 

clinfo **WITHOUT ROCm INSTALLED** (mesa-opencl-icd)
```
DRM_IOCTL_I915_GEM_APERTURE failed: Invalid argument
Assuming 131072kB available aperture size.
May lead to reduced performance or incorrect rendering.
get chip id failed: -1 [2]
param: 4, val: 0
i915 does not support EXECBUFER2
DRM_IOCTL_I915_GEM_APERTURE failed: Invalid argument
Assuming 131072kB available aperture size.
May lead to reduced performance or incorrect rendering.
get chip id failed: -1 [2]
param: 4, val: 0
i915 does not support EXECBUFER2
beignet-opencl-icd: no supported GPU found, this is probably the wrong opencl-icd package for this hardware
(If you have multiple ICDs installed and OpenCL works, you can ignore this message)
DRM_IOCTL_I915_GEM_APERTURE failed: Invalid argument
Assuming 131072kB available aperture size.
May lead to reduced performance or incorrect rendering.
get chip id failed: -1 [2]
param: 4, val: 0
i915 does not support EXECBUFER2
DRM_IOCTL_I915_GEM_APERTURE failed: Invalid argument
Assuming 131072kB available aperture size.
May lead to reduced performance or incorrect rendering.
get chip id failed: -1 [2]
param: 4, val: 0
i915 does not support EXECBUFER2
beignet-opencl-icd: no supported GPU found, this is probably the wrong opencl-icd package for this hardware
(If you have multiple ICDs installed and OpenCL works, you can ignore this message)
Number of platforms                               2
  Platform Name                                   Clover
  Platform Vendor                                 Mesa
  Platform Version                                OpenCL 1.1 Mesa 24.0.0-1pop0~1706872735~22.04~0fa430c
  Platform Profile                                FULL_PROFILE
  Platform Extensions                             cl_khr_icd
  Platform Extensions function suffix             MESA

  Platform Name                                   Intel Gen OCL Driver
  Platform Vendor                                 Intel
  Platform Version                                OpenCL 2.0 beignet 1.3
  Platform Profile                                FULL_PROFILE
  Platform Extensions                             cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_byte_addressable_store cl_khr_3d_image_writes cl_khr_image2d_from_buffer cl_khr_depth_images cl_khr_spir cl_khr_icd cl_intel_accelerator cl_intel_subgroups cl_intel_subgroups_short
  Platform Extensions function suffix             Intel
DRM_IOCTL_I915_GEM_APERTURE failed: Invalid argument
Assuming 131072kB available aperture size.
May lead to reduced performance or incorrect rendering.
get chip id failed: -1 [2]
param: 4, val: 0
i915 does not support EXECBUFER2
beignet-opencl-icd: no supported GPU found, this is probably the wrong opencl-icd package for this hardware
(If you have multiple ICDs installed and OpenCL works, you can ignore this message)

  Platform Name                                   Clover
Number of devices                                 1
  Device Name                                     AMD Radeon RX 7600 (radeonsi, navi33, LLVM 15.0.7, DRM 3.54, 6.6.10-76060610-generic)
  Device Vendor                                   AMD
  Device Vendor ID                                0x1002
  Device Version                                  OpenCL 1.1 Mesa 24.0.0-1pop0~1706872735~22.04~0fa430c
  Device Numeric Version                          0x401000 (1.1.0)
  Driver Version                                  24.0.0-1pop0~1706872735~22.04~0fa430c
  Device OpenCL C Version                         OpenCL C 1.1 
  Device Type                                     GPU
  Device Profile                                  FULL_PROFILE
  Device Available                                Yes
  Compiler Available                              Yes
  Max compute units                               32
  Max clock frequency                             2250MHz
  Max work item dimensions                        3
  Max work item sizes                             256x256x256
  Max work group size                             256
=== CL_PROGRAM_BUILD_LOG ===
fatal error: cannot open file '/usr/lib/clc/gfx1102-amdgcn-mesa-mesa3d.bc': No such file or directory
  Preferred work group size multiple (kernel)     <getWGsizes:1504: create kernel : error -46>
  Preferred / native vector sizes                 
    char                                                16 / 16      
    short                                                8 / 8       
    int                                                  4 / 4       
    long                                                 2 / 2       
    half                                                 0 / 0        (n/a)
    float                                                4 / 4       
    double                                               2 / 2        (cl_khr_fp64)
  Half-precision Floating-point support           (n/a)
  Single-precision Floating-point support         (core)
    Denormals                                     No
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 No
    Round to infinity                             No
    IEEE754-2008 fused multiply-add               No
    Support is emulated in software               No
    Correctly-rounded divide and sqrt operations  No
  Double-precision Floating-point support         (cl_khr_fp64)
    Denormals                                     Yes
    Infinity and NANs                             Yes
    Round to nearest                              Yes
    Round to zero                                 Yes
    Round to infinity                             Yes
    IEEE754-2008 fused multiply-add               Yes
    Support is emulated in software               No
  Address bits                                    64, Little-Endian
  Global memory size                              8589934592 (8GiB)
  Error Correction support                        No
  Max memory allocation                           2147483648 (2GiB)
  Unified memory for Host and Device              No
  Minimum alignment for any data type             128 bytes
  Alignment of base address                       32768 bits (4096 bytes)
  Global Memory cache type                        None
  Image support                                   No
  Local memory type                               Local
  Local memory size                               65536 (64KiB)
  Max number of constant args                     16
  Max constant buffer size                        67108864 (64MiB)
  Max size of kernel argument                     1024
  Queue properties                                
    Out-of-order execution                        No
    Profiling                                     Yes
  Profiling timer resolution                      0ns
  Execution capabilities                          
    Run OpenCL kernels                            Yes
    Run native kernels                            No
    ILs with version                              SPIR-V                                                           0x400000 (1.0.0)
  Built-in kernels with version                   (n/a)
  Device Extensions                               cl_khr_byte_addressable_store cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_fp64 cl_khr_extended_versioning
  Device Extensions with Version                  cl_khr_byte_addressable_store                                    0x400000 (1.0.0)
                                                  cl_khr_global_int32_base_atomics                                 0x400000 (1.0.0)
                                                  cl_khr_global_int32_extended_atomics                             0x400000 (1.0.0)
                                                  cl_khr_local_int32_base_atomics                                  0x400000 (1.0.0)
                                                  cl_khr_local_int32_extended_atomics                              0x400000 (1.0.0)
                                                  cl_khr_int64_base_atomics                                        0x400000 (1.0.0)
                                                  cl_khr_int64_extended_atomics                                    0x400000 (1.0.0)
                                                  cl_khr_fp64                                                      0x400000 (1.0.0)
                                                  cl_khr_extended_versioning                                       0x400000 (1.0.0)

  Platform Name                                   Intel Gen OCL Driver
Number of devices                                 0

NULL platform behavior
  clGetPlatformInfo(NULL, CL_PLATFORM_NAME, ...)  Clover
  clGetDeviceIDs(NULL, CL_DEVICE_TYPE_ALL, ...)   Success [MESA]
  clCreateContext(NULL, ...) [default]            Success [MESA]
  clCreateContext(NULL, ...) [other]              
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_DEFAULT)  Success (1)
    Platform Name                                 Clover
    Device Name                                   AMD Radeon RX 7600 (radeonsi, navi33, LLVM 15.0.7, DRM 3.54, 6.6.10-76060610-generic)
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_CPU)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_GPU)  Success (1)
    Platform Name                                 Clover
    Device Name                                   AMD Radeon RX 7600 (radeonsi, navi33, LLVM 15.0.7, DRM 3.54, 6.6.10-76060610-generic)
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_ACCELERATOR)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_CUSTOM)  No devices found in platform
  clCreateContextFromType(NULL, CL_DEVICE_TYPE_ALL)  Success (1)
    Platform Name                                 Clover
    Device Name                                   AMD Radeon RX 7600 (radeonsi, navi33, LLVM 15.0.7, DRM 3.54, 6.6.10-76060610-generic)

ICD loader properties
  ICD loader Name                                 OpenCL ICD Loader
  ICD loader Vendor                               OCL Icd free software
  ICD loader Version                              2.2.14
  ICD loader Profile                              OpenCL 3.0
```

---

## 评论 (24 条)

### 评论 #1 — ckuethe (2024-03-05T01:38:24Z)

I stumbled over something similar trying to run FreeCAD on Pop_OS 22.04, I was able to get it to run by preloading the amdgpu module thusly:

`LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libdrm_amdgpu.so ./Freecad*.AppImage`

https://www.linuxquestions.org/questions/slackware-14/freecad-not-starting-4175733563/


---

### 评论 #2 — magicalraccoon (2024-03-09T05:21:01Z)

I am also having this issue with the RX 7900 XT. @ckuethe 's solution did not solve the issue, but it produced a different error message

```
hackoon@pop-os:~$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libdrm_amdgpu.so.1.0.0 clinfo
Segmentation fault (core dumped)
```


---

### 评论 #3 — RAD750 (2024-03-26T12:42:27Z)

This is worrying that there is still no acknowledgement after a month
I tried on another machine with PopOS and a RX6600, and there are the same symptoms.
LD_PRELOADING the library as @magicalraccoon suggested, yields the same error as her.
I dug a little deeper with gdb:
```
jacopo@prodesk:~/Scaricati$ gdb clinfo
GNU gdb (Ubuntu 12.1-0ubuntu1~22.04) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from clinfo...
(No debugging symbols found in clinfo)
(gdb) set environment LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libdrm_amdgpu.so
(gdb) r
Starting program: /usr/bin/clinfo 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7fffee3ff640 (LWP 586598)]
[New Thread 0x7fffedbfe640 (LWP 586599)]
[Thread 0x7fffedbfe640 (LWP 586599) exited]
[New Thread 0x7ffed45ff640 (LWP 586600)]
[New Thread 0x7ffed3dfe640 (LWP 586601)]
[New Thread 0x7ffed35fd640 (LWP 586602)]
[New Thread 0x7ffed2dfc640 (LWP 586603)]

Thread 1 "clinfo" received signal SIGSEGV, Segmentation fault.
0x00007ffee4d9986f in ?? () from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
(gdb) bt
#0  0x00007ffee4d9986f in ?? ()
   from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
#1  0x00007ffee4df8cf1 in ?? ()
   from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
#2  0x00007ffee4d66674 in ?? ()
   from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
#3  0x00007ffee4d67758 in ?? ()
   from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
#4  0x00007ffee4e1f266 in amdgpu_winsys_create ()
   from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
#5  0x00007ffee4d6806d in ?? ()
   from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
#6  0x00007ffee4c3aecb in ?? ()
   from /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so
#7  0x00007fffec6a9967 in ?? () from /lib/x86_64-linux-gnu/libMesaOpenCL.so.1
#8  0x00007fffec696ac6 in ?? () from /lib/x86_64-linux-gnu/libMesaOpenCL.so.1
#9  0x00007fffec6a47c8 in ?? () from /lib/x86_64-linux-gnu/libMesaOpenCL.so.1
#10 0x00007fffec67064a in ?? () from /lib/x86_64-linux-gnu/libMesaOpenCL.so.1
#11 0x00007ffff7fc947e in call_init (l=<optimized out>, argc=argc@entry=1, 
    argv=argv@entry=0x7fffffffdd68, env=env@entry=0x7fffffffdd78)
    at ./elf/dl-init.c:70
#12 0x00007ffff7fc9568 in call_init (env=0x7fffffffdd78, argv=0x7fffffffdd68, 
    argc=1, l=<optimized out>) at ./elf/dl-init.c:33
--Type <RET> for more, q to quit, c to continue without paging--
#13 _dl_init (main_map=0x5555558cd630, argc=1, argv=0x7fffffffdd68, 
    env=0x7fffffffdd78) at ./elf/dl-init.c:117
#14 0x00007ffff7d74af5 in __GI__dl_catch_exception (exception=<optimized out>, 
    operate=<optimized out>, args=<optimized out>)
    at ./elf/dl-error-skeleton.c:182
#15 0x00007ffff7fd0ff6 in dl_open_worker (a=0x7fffffffd760)
    at ./elf/dl-open.c:808
#16 dl_open_worker (a=a@entry=0x7fffffffd760) at ./elf/dl-open.c:771
#17 0x00007ffff7d74a98 in __GI__dl_catch_exception (exception=<optimized out>, 
    operate=<optimized out>, args=<optimized out>)
    at ./elf/dl-error-skeleton.c:208
#18 0x00007ffff7fd134e in _dl_open (file=<optimized out>, mode=-2147483646, 
    caller_dlopen=0x7ffff7f79a60, nsid=-2, argc=1, argv=<optimized out>, 
    env=0x7fffffffdd78) at ./elf/dl-open.c:883
#19 0x00007ffff7c9063c in dlopen_doit (a=a@entry=0x7fffffffd9d0)
    at ./dlfcn/dlopen.c:56
#20 0x00007ffff7d74a98 in __GI__dl_catch_exception (
    exception=exception@entry=0x7fffffffd930, operate=<optimized out>, 
    args=<optimized out>) at ./elf/dl-error-skeleton.c:208
#21 0x00007ffff7d74b63 in __GI__dl_catch_error (objname=0x7fffffffd988, 
    errstring=0x7fffffffd990, mallocedp=0x7fffffffd987, 
    operate=<optimized out>, args=<optimized out>)
    at ./elf/dl-error-skeleton.c:227
--Type <RET> for more, q to quit, c to continue without paging--
#22 0x00007ffff7c9012e in _dlerror_run (
    operate=operate@entry=0x7ffff7c905e0 <dlopen_doit>, 
    args=args@entry=0x7fffffffd9d0) at ./dlfcn/dlerror.c:138
#23 0x00007ffff7c906c8 in dlopen_implementation (dl_caller=<optimized out>, 
    mode=<optimized out>, file=<optimized out>) at ./dlfcn/dlopen.c:71
#24 ___dlopen (file=<optimized out>, mode=<optimized out>)
    at ./dlfcn/dlopen.c:81
#25 0x00007ffff7f79a60 in ?? () from /opt/rocm-6.0.2/lib/libOpenCL.so.1
#26 0x00007ffff7f7748b in ?? () from /opt/rocm-6.0.2/lib/libOpenCL.so.1
#27 0x00007ffff7f79937 in ?? () from /opt/rocm-6.0.2/lib/libOpenCL.so.1
#28 0x00007ffff7c99ee8 in __pthread_once_slow (once_control=0x7ffff7f7d100, 
    init_routine=0x7ffff7f797a0) at ./nptl/pthread_once.c:116
#29 0x00007ffff7f77bc6 in clGetPlatformIDs ()
   from /opt/rocm-6.0.2/lib/libOpenCL.so.1
#30 0x000055555555b765 in ?? ()
#31 0x00007ffff7c29d90 in __libc_start_call_main (
    main=main@entry=0x55555555b5a0, argc=argc@entry=1, 
    argv=argv@entry=0x7fffffffdd68)
    at ../sysdeps/nptl/libc_start_call_main.h:58
#32 0x00007ffff7c29e40 in __libc_start_main_impl (main=0x55555555b5a0, argc=1, 
    argv=0x7fffffffdd68, init=<optimized out>, fini=<optimized out>, 
    rtld_fini=<optimized out>, stack_end=0x7fffffffdd58)
    at ../csu/libc-start.c:392
--Type <RET> for more, q to quit, c to continue without paging--
#33 0x000055555555be0e in ?? ()
(gdb) 
```
But apart from this, I can't go much further.

---

### 评论 #4 — kentrussell (2024-03-26T13:15:14Z)

I saw a similar link at https://bbs.archlinux.org/viewtopic.php?id=293565 , saying the whole preload thing. 

When you eventually installed the amdgpu-dkms , did you use the amdgpu-install script, or did you manually install amdgpu-dkms and amdgpu-dkms-firmware via apt? For ROCm releases, we also include a newer libdrm that features newer features and fixes, but it doesn't get installed if you use the --no-dkms flags. 
If you list installed packages via dpkg/rpm, and grep for libdrm, does it show the ROCm ones, or the OS-distributed ones? I will have to defer to the libdrm and OCL guys after checking that, but at least it's a start. 

---

### 评论 #5 — magicalraccoon (2024-03-26T13:19:19Z)

I have only used the amdgpu installer script, with modifications to my os-release in order to get it to work in PopOS (`sed -i 's/ID=pop/ID=ubuntu/g' /etc/os-release`). I've also attempted to install without the --no-dkms flag.

---

### 评论 #6 — RAD750 (2024-03-26T13:21:07Z)

I couldn't install it without appending --no-dkms. It complains that the kernel is unsupported.
```
jacopo@prodesk:~$ sudo amdgpu-install --usecase=opencl
[sudo] password di jacopo: 
Scaricamento di:1 http://apt.pop-os.org/proprietary jammy InRelease [11,5 kB]
Scaricamento di:2 http://apt.pop-os.org/release jammy InRelease [16,6 kB]    
Scaricamento di:3 http://apt.pop-os.org/ubuntu jammy InRelease [270 kB]
Trovato:4 https://repo.radeon.com/amdgpu/6.0.2/ubuntu jammy InRelease
Trovato:5 https://repo.radeon.com/rocm/apt/6.0.2 jammy InRelease
Trovato:6 http://apt.pop-os.org/ubuntu jammy-security InRelease
Trovato:7 http://apt.pop-os.org/ubuntu jammy-updates InRelease
Scaricamento di:8 http://apt.pop-os.org/ubuntu jammy-backports InRelease [109 kB]
Recuperati 407 kB in 2s (204 kB/s)
Lettura elenco dei pacchetti... Fatto
Lettura elenco dei pacchetti... Fatto
Generazione albero delle dipendenze... Fatto
Lettura informazioni sullo stato... Fatto   
linux-headers-6.6.10-76060610-generic è già alla versione più recente (6.6.10-76060610.202401051437~1709764300~22.04~379e7a9).
I seguenti pacchetti sono stati installati automaticamente e non sono più richiesti:
  libfile-copy-recursive-perl libomxil-bellagio-bin libomxil-bellagio0
  valgrind
Usare "sudo apt autoremove" per rimuoverli.
I seguenti pacchetti aggiuntivi saranno inoltre installati:
  amdgpu-core amdgpu-dkms-firmware comgr hsa-rocr libdrm-amdgpu-amdgpu1
  libdrm-amdgpu-common libdrm2-amdgpu openmp-extras-runtime rocm-core
  rocm-language-runtime rocm-ocl-icd rocm-opencl
I seguenti pacchetti NUOVI saranno installati:
  amdgpu-core amdgpu-dkms amdgpu-dkms-firmware comgr hsa-rocr
  libdrm-amdgpu-amdgpu1 libdrm-amdgpu-common libdrm2-amdgpu
  openmp-extras-runtime rocm-core rocm-language-runtime rocm-ocl-icd
  rocm-opencl rocm-opencl-runtime
0 aggiornati, 14 installati, 0 da rimuovere e 1 non aggiornati.
È necessario scaricare 23,1 MB/217 MB di archivi.
Dopo quest'operazione, verranno occupati 993 MB di spazio su disco.
Continuare? [S/n] s
Scaricamento di:1 https://repo.radeon.com/amdgpu/6.0.2/ubuntu jammy/main amd64 amdgpu-dkms-firmware all 1:6.3.6.60002-1718217.22.04 [12,4 MB]
Scaricamento di:2 https://repo.radeon.com/amdgpu/6.0.2/ubuntu jammy/main amd64 amdgpu-dkms all 1:6.3.6.60002-1718217.22.04 [10,7 MB]
Recuperati 23,1 MB in 7s (3.251 kB/s)                                          
Selezionato il pacchetto amdgpu-core non precedentemente selezionato.
(Lettura del database... 848704 file e directory attualmente installati.)
Preparativi per estrarre .../00-amdgpu-core_1%3a6.0.60002-1718217.22.04_all.deb...
Estrazione di amdgpu-core (1:6.0.60002-1718217.22.04)...
Selezionato il pacchetto amdgpu-dkms-firmware non precedentemente selezionato.
Preparativi per estrarre .../01-amdgpu-dkms-firmware_1%3a6.3.6.60002-1718217.22.04_all.deb...
Estrazione di amdgpu-dkms-firmware (1:6.3.6.60002-1718217.22.04)...
Selezionato il pacchetto amdgpu-dkms non precedentemente selezionato.
Preparativi per estrarre .../02-amdgpu-dkms_1%3a6.3.6.60002-1718217.22.04_all.deb...
Estrazione di amdgpu-dkms (1:6.3.6.60002-1718217.22.04)...
Selezionato il pacchetto rocm-core non precedentemente selezionato.
Preparativi per estrarre .../03-rocm-core_6.0.2.60002-115~22.04_amd64.deb...
Estrazione di rocm-core (6.0.2.60002-115~22.04)...
Selezionato il pacchetto comgr non precedentemente selezionato.
Preparativi per estrarre .../04-comgr_2.6.0.60002-115~22.04_amd64.deb...
Estrazione di comgr (2.6.0.60002-115~22.04)...
Selezionato il pacchetto libdrm2-amdgpu:amd64 non precedentemente selezionato.
Preparativi per estrarre .../05-libdrm2-amdgpu_1%3a2.4.116.60002-1718217.22.04_amd64.deb...
Estrazione di libdrm2-amdgpu:amd64 (1:2.4.116.60002-1718217.22.04)...
Selezionato il pacchetto libdrm-amdgpu-common non precedentemente selezionato.
Preparativi per estrarre .../06-libdrm-amdgpu-common_1.0.0.60002-1718217.22.04_all.deb...
Estrazione di libdrm-amdgpu-common (1.0.0.60002-1718217.22.04)...
Selezionato il pacchetto libdrm-amdgpu-amdgpu1:amd64 non precedentemente selezionato.
Preparativi per estrarre .../07-libdrm-amdgpu-amdgpu1_1%3a2.4.116.60002-1718217.22.04_amd64.deb...
Estrazione di libdrm-amdgpu-amdgpu1:amd64 (1:2.4.116.60002-1718217.22.04)...
Selezionato il pacchetto hsa-rocr non precedentemente selezionato.
Preparativi per estrarre .../08-hsa-rocr_1.12.0.60002-115~22.04_amd64.deb...
Estrazione di hsa-rocr (1.12.0.60002-115~22.04)...
Selezionato il pacchetto openmp-extras-runtime non precedentemente selezionato.
Preparativi per estrarre .../09-openmp-extras-runtime_17.60.0.60002-115~22.04_amd64.deb...
Estrazione di openmp-extras-runtime (17.60.0.60002-115~22.04)...
Selezionato il pacchetto rocm-language-runtime non precedentemente selezionato.
Preparativi per estrarre .../10-rocm-language-runtime_6.0.2.60002-115~22.04_amd64.deb...
Estrazione di rocm-language-runtime (6.0.2.60002-115~22.04)...
Selezionato il pacchetto rocm-ocl-icd non precedentemente selezionato.
Preparativi per estrarre .../11-rocm-ocl-icd_2.0.0.60002-115~22.04_amd64.deb...
Estrazione di rocm-ocl-icd (2.0.0.60002-115~22.04)...
Selezionato il pacchetto rocm-opencl non precedentemente selezionato.
Preparativi per estrarre .../12-rocm-opencl_2.0.0.60002-115~22.04_amd64.deb...
Estrazione di rocm-opencl (2.0.0.60002-115~22.04)...
Selezionato il pacchetto rocm-opencl-runtime non precedentemente selezionato.
Preparativi per estrarre .../13-rocm-opencl-runtime_6.0.2.60002-115~22.04_amd64.deb...
Estrazione di rocm-opencl-runtime (6.0.2.60002-115~22.04)...
Configurazione di rocm-core (6.0.2.60002-115~22.04)...
update-alternatives: viene usato /opt/rocm-6.0.2 per fornire /opt/rocm (rocm) in modalità automatica
Configurazione di rocm-ocl-icd (2.0.0.60002-115~22.04)...
Configurazione di amdgpu-core (1:6.0.60002-1718217.22.04)...
Configurazione di amdgpu-dkms-firmware (1:6.3.6.60002-1718217.22.04)...
Configurazione di libdrm-amdgpu-common (1.0.0.60002-1718217.22.04)...
Configurazione di comgr (2.6.0.60002-115~22.04)...
Configurazione di amdgpu-dkms (1:6.3.6.60002-1718217.22.04)...
Loading new amdgpu-6.3.6-1718217.22.04 DKMS files...
Building for 6.6.10-76060610-generic 6.8.0-76060800daily20240311-generic
Building for architecture x86_64
Building initial module for 6.6.10-76060610-generic
ERROR (dkms apport): kernel package linux-headers-6.6.10-76060610-generic is not supported
Error! Bad return status for module build on kernel: 6.6.10-76060610-generic (x86_64)
Consult /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/make.log for more information.
dpkg: errore nell'elaborare il pacchetto amdgpu-dkms (--configure):
 il sottoprocesso installato pacchetto amdgpu-dkms script post-installation ha restituito lo stato di errore 10
Configurazione di hsa-rocr (1.12.0.60002-115~22.04)...
Configurazione di libdrm2-amdgpu:amd64 (1:2.4.116.60002-1718217.22.04)...
Configurazione di rocm-opencl (2.0.0.60002-115~22.04)...
Configurazione di libdrm-amdgpu-amdgpu1:amd64 (1:2.4.116.60002-1718217.22.04)...
Configurazione di openmp-extras-runtime (17.60.0.60002-115~22.04)...
Configurazione di rocm-language-runtime (6.0.2.60002-115~22.04)...
Configurazione di rocm-opencl-runtime (6.0.2.60002-115~22.04)...
update-alternatives: viene usato /opt/rocm-6.0.2/bin/clinfo per fornire /usr/bin/clinfo (clinfo) in modalità automatica
update-alternatives: attenzione: /usr/bin/clinfo non viene sostituito con un collegamento
Elaborazione dei trigger per libc-bin (2.35-0ubuntu3.6)...
/sbin/ldconfig.real: /lib/x86_64-linux-gnu/libsoundio.so.2 is not a symbolic link

Si sono verificati degli errori nell'elaborazione:
 amdgpu-dkms
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

---

### 评论 #7 — kentrussell (2024-03-26T13:26:04Z)

So the /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/make.log file there will say why it failed to compile. It might be something easy to fix (something we will handle in the 6.1 ROCm release), or it could be something in the POP 6.6 kernel that isn't in the Ubuntu HWE kernel (we say preview support is available for the HWE 6.6 kernel in the support list). 

6.1 may improve things there, but it does appear that libdrm-amdgpu2 got installed in that list. Is that package present when the errors happen? Wondering if it could be a mismatch between the libdrm that we provide and the kernel from POP.

---

### 评论 #8 — RAD750 (2024-03-26T13:30:23Z)

The file in question:
```
jacopo@prodesk:~$ cat /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/make.log 
DKMS make.log for amdgpu-6.3.6-1718217.22.04 for kernel 6.6.10-76060610-generic (x86_64)
mar 26 mar 2024, 14:27:51, CET
make: ingresso nella directory «/usr/src/linux-headers-6.6.10-76060610-generic»
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  You are using:           gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/sched_main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/sched_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/sched_entity.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_tt.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/drm_gem_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_common.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdxcp/./backport/kcl_drm_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_kernel_params.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_device.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdxcp/amdxcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/dma-buf/dma-resv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_util.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2954:31: error: ‘drm_gem_prime_handle_to_fd’ undeclared here (not in a function)
 2954 |         .prime_handle_to_fd = drm_gem_prime_handle_to_fd,
      |                               ^~~~~~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_bo_vm.o
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2955:31: error: ‘drm_gem_prime_fd_to_handle’ undeclared here (not in a function)
 2955 |         .prime_fd_to_handle = drm_gem_prime_fd_to_handle,
      |                               ^~~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:10: error: ‘struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: note: (near initialization for ‘amdgpu_kms_driver.gem_prime_import_sg_table’)
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:10: error: ‘const struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: note: (near initialization for ‘amdgpu_partition_driver.gem_prime_import_sg_table’)
cc1: some warnings being treated as errors
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu/amdgpu_drv.o] Errore 1
make[3]: *** Attesa per i processi non terminati....
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_backlight.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_ioctl.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/scheduler/amd-sched.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/drm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_kthread.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_io.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amddrm_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_module.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_execbuf_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_range_manager.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_seq_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_resource.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amddrm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_pool.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_suspend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_pci.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_memory.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_sched.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_sys_manager.o
make[2]: *** [scripts/Makefile.build:480: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdgpu] Errore 2
make[2]: *** Attesa per i processi non terminati....
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_reservation.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_cache.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_fb.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/ttm_agp_backend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_print.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_crtc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_connector.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_atomic_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_device_cgroup.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mn.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_modes.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_time.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_acpi_table.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_page_alloc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_numa.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_fs_read_write.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_aperture.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_simple_kms_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_bitmap.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/ttm/amdttm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_vmscan.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_dma_fence_chain.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mce_amd.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_workqueue.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_cpumask.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_dsc_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_mm_slab.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_irqdesc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_suballoc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_dp_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_drm_hdcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_debugfs_inode.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_debugfs_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/kcl_sysfs_emit.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build/amd/amdkcl/amdkcl.o
make[1]: *** [/usr/src/linux-headers-6.6.10-76060610-generic/Makefile:1919: /var/lib/dkms/amdgpu/6.3.6-1718217.22.04/build] Errore 2
make: *** [Makefile:234: __sub-make] Errore 2
make: uscita dalla directory «/usr/src/linux-headers-6.6.10-76060610-generic»
```

There is no libdrm-amdgpu2 package (or am I missing something here?)

```
jacopo@prodesk:~$ dpkg-query -l libdrm-amdgpu2
dpkg-query: no package matching libdrm-amdgpu2
```

---

### 评论 #9 — magicalraccoon (2024-03-26T13:41:24Z)

I have a slightly older version

```
hackoon@pop-os:~$ cat /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/make.log 
DKMS make.log for amdgpu-6.3.6-1697589.22.04 for kernel 6.6.10-76060610-generic (amd64)
Mon Mar 18 04:16:26 PM PDT 2024
make: Entering directory '/usr/src/linux-headers-6.6.10-76060610-generic'
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  You are using:           gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/scheduler/sched_main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/scheduler/sched_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/scheduler/sched_entity.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdxcp/amdgpu_xcp_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdxcp/./backport/kcl_drm_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_tt.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_bo.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/drm_gem_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_bo_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_bo_vm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/main.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_module.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_common.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_execbuf_util.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_kernel_params.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_range_manager.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_resource.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/dma-buf/dma-resv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_backlight.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_pool.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/drm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_ioctl.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_device.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_kthread.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_sys_manager.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_doorbell_mgr.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_io.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_kms.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdxcp/amdxcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_seq_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/ttm_agp_backend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_suspend.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_atombios.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/atombios_crtc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_connectors.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_pci.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_mm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_memory.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_sched.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amddrm_ttm_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/atom.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_fence.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_reservation.o
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:2954:31: error: ‘drm_gem_prime_handle_to_fd’ undeclared here (not in a function)
 2954 |         .prime_handle_to_fd = drm_gem_prime_handle_to_fd,
      |                               ^~~~~~~~~~~~~~~~~~~~~~~~~~
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_fence.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amddrm_buddy.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_cache.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_ttm.o
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:2955:31: error: ‘drm_gem_prime_fd_to_handle’ undeclared here (not in a function)
 2955 |         .prime_fd_to_handle = drm_gem_prime_fd_to_handle,
      |                               ^~~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:10: error: ‘struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 2979 |         .gem_prime_mmap = amdkcl_drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:2979:27: note: (near initialization for ‘amdgpu_kms_driver.gem_prime_import_sg_table’)
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:10: error: ‘const struct drm_driver’ has no member named ‘gem_prime_mmap’; did you mean ‘gem_prime_import’?
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |          ^~~~~~~~~~~~~~
      |          gem_prime_import
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: error: initialization of ‘struct drm_gem_object * (*)(struct drm_device *, struct dma_buf_attachment *, struct sg_table *)’ from incompatible pointer type ‘int (*)(struct drm_gem_object *, struct vm_area_struct *)’ [-Werror=incompatible-pointer-types]
 3009 |         .gem_prime_mmap = drm_gem_prime_mmap,
      |                           ^~~~~~~~~~~~~~~~~~
/var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.c:3009:27: note: (near initialization for ‘amdgpu_partition_driver.gem_prime_import_sg_table’)
cc1: some warnings being treated as errors
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_fb.o
make[3]: *** [scripts/Makefile.build:243: /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu/amdgpu_drv.o] Error 1
make[3]: *** Waiting for unfinished jobs....
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_print.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_crtc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_connector.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_atomic_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_device_cgroup.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_mn.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_modes.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_time.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/scheduler/amd-sched.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_acpi_table.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_page_alloc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_numa.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_fs_read_write.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_aperture.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/ttm/amdttm.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_simple_kms_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_bitmap.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_vmscan.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_dma_fence_chain.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_mce_amd.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_workqueue.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_cpumask.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_dsc_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_mm_slab.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_irqdesc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_suballoc.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_dp_helper.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_drm_hdcp.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_debugfs_inode.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_debugfs_file.o
  CC [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/kcl_sysfs_emit.o
  LD [M]  /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdkcl/amdkcl.o
make[2]: *** [scripts/Makefile.build:480: /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build/amd/amdgpu] Error 2
make[1]: *** [/usr/src/linux-headers-6.6.10-76060610-generic/Makefile:1919: /var/lib/dkms/amdgpu/6.3.6-1697589.22.04/build] Error 2
make: *** [Makefile:234: __sub-make] Error 2
make: Leaving directory '/usr/src/linux-headers-6.6.10-76060610-generic'
```

---

### 评论 #10 — kentrussell (2024-03-26T13:46:57Z)

Ah sorry, it's libdrm2-amdgpu . You can also just grep for libdrm and then grep for amdgpu. IE "dpkg -l|grep libdrm|grep amdgpu". Or if you want to try to isolate a bit more, try "dpkg -l|grep libdrm|grep 60" (explanation below)

As for the compile failure, there was an upstream revert to fix that issue:
https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0514f63cfff38a0dcb7ba9c5f245827edc0c5107
It's possible that it didn't make it into that 6.6-based kernel that you've got. As for the gem_prime_mmap, we have a fix for that coming in ROCm 6.1. There was some detection stuff that wasn't in the 6.0 release (which is 6.5-based), while 6.1's ROCm release is based on the 6.7 kernel, so it should work nicely with a 6.6-based kernel (even if it's not an 'officially supported distro') 

Regardless, if you have some libdrm*amdgpu* installed and the versioning is 60001 or something with some 60-thousand in the versioning name (60000, 60002, 60100, etc), then it would've come from the ROCm install. We can try to remove that package and try the application again and see how it goes. I think that we need to have the ROCm 6.0.* libdrm and amdgpu-dkms aligned, and since the install isn't working there, we can't make that work. Since we can't get amdgpu-dkms installed until 6.1 without a lot of manual patching, I think this is the best approach to try to get it to align with the OS' kernel+libdrm.

If you want a clean slate instead of just removing libdrm2-amdgpu (and any other libdrm stuff that came from the ROCm install), you can do a full "amdgpu-install --uninstall", then an "apt autoremove", then end with "amdgpu-install --usecase=rocm --no-dkms". My hope is that if we skip the DKMS altogether, it'll skip the newer libdrm stuff, and we should avoid that annoying start_addr error by aligning with what's in the distro. For reference, my install has libdrm-amdgpu-amdgpu1, libdrm-amdgpu-common, libdrm-amdgpu-dev, libdrm-amdgpu-radeon1, and libdrm2-amdgpu installed with similar (but not identical) versioning. The 6XXYY versioning is supposed to correlate to the 6.X.Y ROCm release. Keep me posted!

And sorry on the delay, when it comes to "unsupported Operating Systems", issues tend to bounce around a bit more. While POP isn't supported, the issues look to be generic enough to not be specific to POP, but specific to "mixing-and-matching libdrm and amdgpu-dkms", combined with the awkward spot that ROCm 6.0's amdgpu-dkms is in compared to the 6,6-based kernel. My dream is that 6.1 will fix everything, but we can try to get 6.0.* working until 6.1 drops.

---

### 评论 #11 — RAD750 (2024-03-26T14:29:38Z)

Appears to be 60002
```
jacopo@prodesk:~$ dpkg-query -l libdrm2-amdgpu
Voluto=U (non noto)/I (installato)/R (rimosso)/P (rimosso totale)/H (in attesa)
| Stato=Non/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(nessuno)/R (reinstallazione richiesta) (Stato,Err: maiuscolo=grave)
||/ Nome                 Versione                      Architettura Descrizione
+++-====================-=============================-============-=====================================================
ii  libdrm2-amdgpu:amd64 1:2.4.116.60002-1718217.22.04 amd64        Userspace interface to kernel DRM services -- runtime
```

I did as you suggested but it still gives the same error
```
jacopo@prodesk:~$ clinfo
clinfo: symbol lookup error: /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so: undefined symbol: amdgpu_va_get_start_addr
```

---

### 评论 #12 — kentrussell (2024-03-26T15:00:39Z)

@AlexXAmd Any ideas here? 

---

### 评论 #13 — AlexXAmd (2024-03-28T15:39:39Z)

[AMD Official Use Only - General]


You did not install ROCM version of opencl driver. You installed another opencl platform: Clover.

You may search rocm document about how to install ROCM opencl.



Let us know if you cannot install it.



Thanks.

Alex (Bin) Xie
From: Kent Russell ***@***.***>
Sent: Tuesday, March 26, 2024 11:01 AM
To: ROCm/ROCm ***@***.***>
Cc: Xie, AlexBin ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: undefined symbol: amdgpu_va_get_start_addr - Pop!_OS 22.04 (Issue #2934)


@AlexXAmd<https://github.com/AlexXAmd> Any ideas here?

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/2934#issuecomment-2020671962>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/ANBRESZTMMEKNTHCJIYMXDLY2GES7AVCNFSM6AAAAABD45OHMSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDAMRQGY3TCOJWGI>.
You are receiving this because you were mentioned.Message ID: ***@***.******@***.***>>


---

### 评论 #14 — RAD750 (2024-03-29T08:36:34Z)

@AlexXAmd I installed:
`sudo amdgpu-install --usecase=rocm --no-dkms`
However the same error occurs:

```
jacopo@prodesk:~$ clinfo
clinfo: symbol lookup error: /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so: undefined symbol: amdgpu_va_get_start_addr
```

Additionally, now software complains that there is no Open**G**L:
![immagine](https://github.com/ROCm/ROCm/assets/12469744/c77fe315-e5ed-4c98-ab5b-0d3c97cb289e)

Did I do something wrong? I followed this: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html

Of course, running `sudo amdgpu-install--uninstall` makes the OpenGL applications work again, but no OpenCL.


---

### 评论 #15 — magicalraccoon (2024-03-29T22:06:47Z)

I've had the same experience as @RAD750 as well

---

### 评论 #16 — AlexXAmd (2024-04-01T15:33:03Z)

[AMD Official Use Only - General]

Try to uninstall Clove.

From: Sara Murray ***@***.***>
Sent: Friday, March 29, 2024 6:07 PM
To: ROCm/ROCm ***@***.***>
Cc: Xie, AlexBin ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: undefined symbol: amdgpu_va_get_start_addr - Pop!_OS 22.04 (Issue #2934)


I've had the same experience as @RAD750<https://github.com/RAD750> as well

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/2934#issuecomment-2027779754>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/ANBRES3UMP3CP4P6VEE2XLLY2XQY3AVCNFSM6AAAAABD45OHMSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDAMRXG43TSNZVGQ>.
You are receiving this because you were mentioned.Message ID: ***@***.******@***.***>>


---

### 评论 #17 — AlexXAmd (2024-04-01T16:04:03Z)

[AMD Official Use Only - General]

If you can’t remove Clover, you may have a look at this folder: /etc/OpenCL/vendors.

There may be a file relevant to Clover. Move that file out of /etc folder.

This is a hacky way though.

From: Sara Murray ***@***.***>
Sent: Friday, March 29, 2024 6:07 PM
To: ROCm/ROCm ***@***.***>
Cc: Xie, AlexBin ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: undefined symbol: amdgpu_va_get_start_addr - Pop!_OS 22.04 (Issue #2934)


I've had the same experience as @RAD750<https://github.com/RAD750> as well

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/2934#issuecomment-2027779754>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/ANBRES3UMP3CP4P6VEE2XLLY2XQY3AVCNFSM6AAAAABD45OHMSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDAMRXG43TSNZVGQ>.
You are receiving this because you were mentioned.Message ID: ***@***.***>


---

### 评论 #18 — AlexXAmd (2024-04-01T18:09:05Z)

[AMD Official Use Only - General]

No OpenGL? Probably because this option. This option affects AMD kernel driver.
--no-dkms

Please see my other comments in this thread. A quick/hacky solution is to disable Clover in /etc/

I don’t know how Clove was installed in your system in the first place. If Clover is installed by you and Clover is not part of OpenGL/MESA package, you may purge Clover using package manager.

-Alex
From: Jacopo ***@***.***>
Sent: Friday, March 29, 2024 4:37 AM
To: ROCm/ROCm ***@***.***>
Cc: Xie, AlexBin ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: undefined symbol: amdgpu_va_get_start_addr - Pop!_OS 22.04 (Issue #2934)


@AlexXAmd<https://github.com/AlexXAmd> I installed:
sudo amdgpu-install --usecase=rocm --no-dkms
However the same error occurs:

***@***.***:~$ clinfo

clinfo: symbol lookup error: /usr/lib/x86_64-linux-gnu/gallium-pipe/pipe_radeonsi.so: undefined symbol: amdgpu_va_get_start_addr

Additionally, now software complains that there is no OpenGL:
immagine.png (view on web)<https://github.com/ROCm/ROCm/assets/12469744/c77fe315-e5ed-4c98-ab5b-0d3c97cb289e>

Did I do something wrong? I followed this: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/2934#issuecomment-2026878940>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/ANBRES3IQHSQ4GI2FIYOVN3Y2UKZTAVCNFSM6AAAAABD45OHMSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDAMRWHA3TQOJUGA>.
You are receiving this because you were mentioned.Message ID: ***@***.***>


---

### 评论 #19 — RAD750 (2024-04-01T19:44:25Z)

Thanks to @AlexXAmd for pointing me in the right direction. I've now managed to get OpenCL **and** OpenGL working at the same time.

1. `sudo apt remove --purge mesa-opencl-icd`
2. `sudo amdgpu-install --usecase=opencl --no-dkms`
3. `sudo apt install opencl-headers ocl-icd-libopencl1 clinfo -y`
4. `sudo apt-get install amdgpu-lib rocm-opencl-runtime rocm-hip-runtime -y`

I will try on another computer later, @magicalraccoon maybe try it too and see if it works. It seems that having the mesa-opencl-icd package installed breaks ROCm, and having the `amdgpu-lib rocm-opencl-runtime rocm-hip-runtime` packages missing breaks OpenCL.

---

### 评论 #20 — magicalraccoon (2024-04-02T20:20:00Z)

Brilliant! @RAD750 's steps allowed my card to be detected and utilized. I appreciate everyone's assistance!

---

### 评论 #21 — ghost (2024-04-10T11:48:10Z)

I have very similar issue but with `vainfo`, does anyone know if it could be related? Or it's better to open another issue?
```
libva info: VA-API version 1.14.0
libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/radeonsi_drv_video.so
libva error: dlopen of /usr/lib/x86_64-linux-gnu/dri/radeonsi_drv_video.so failed: /usr/lib/x86_64-linux-gnu/dri/radeonsi_drv_video.so: undefined symbol: amdgpu_va_get_start_addr
libva info: va_openDriver() returns -1
vaInitialize failed with error code -1 (unknown libva error),exit
```

---

### 评论 #22 — AlexXAmd (2024-04-10T15:07:54Z)

[AMD Official Use Only - General]

This is not same issue.

From: Ivan ***@***.***>
Sent: Wednesday, April 10, 2024 7:49 AM
To: ROCm/ROCm ***@***.***>
Cc: Xie, AlexBin ***@***.***>; Mention ***@***.***>
Subject: Re: [ROCm/ROCm] [Issue]: undefined symbol: amdgpu_va_get_start_addr - Pop!_OS 22.04 (Issue #2934)


I have very similar issue but with vainfo, does anyone know if it could be related? Or it's better to open another issue?

libva info: VA-API version 1.14.0

libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/radeonsi_drv_video.so

libva error: dlopen of /usr/lib/x86_64-linux-gnu/dri/radeonsi_drv_video.so failed: /usr/lib/x86_64-linux-gnu/dri/radeonsi_drv_video.so: undefined symbol: amdgpu_va_get_start_addr

libva info: va_openDriver() returns -1

vaInitialize failed with error code -1 (unknown libva error),exit

—
Reply to this email directly, view it on GitHub<https://github.com/ROCm/ROCm/issues/2934#issuecomment-2047316981>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/ANBRES62Y7CYDNKEXVSJPKDY4URJDAVCNFSM6AAAAABD45OHMSVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMZDANBXGMYTMOJYGE>.
You are receiving this because you were mentioned.Message ID: ***@***.***>


---

### 评论 #23 — ppanchad-amd (2024-06-20T14:54:32Z)

@RAD750 Has your issue been resolved? If so, please close the ticket. Thanks!
@Nekotekina Please open another ticket for your issue since it's unrelated. Thanks!

---

### 评论 #24 — ghost (2024-09-17T17:36:53Z)

@ppanchad-amd sorry for not answering right away, but after installing Rocm 6.2 it seems that the issue is gone and vainfo works as expected.

---
