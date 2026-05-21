# Radeon RX 7900 XTX ROCm 5.4.3 - HSA_STATUS_OUT_OF_RESOURCES

> **Issue #2191**
> **状态**: closed
> **创建时间**: 2023-05-30T07:14:34Z
> **更新时间**: 2023-05-30T11:24:23Z
> **关闭时间**: 2023-05-30T11:24:23Z
> **作者**: bondhugula
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2191

## 描述

On an Ubuntu 22.04 system with an AMD Radeon RX 7900 XTX with ROCm 5.4.3 installed via apt, I see the errors below while running basic utilities/tests:

```
apt list --installed | grep rocm

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

rocm-bandwidth-test/jammy,now 1.4.0.50403-121~22.04 amd64 [installed]
rocm-clang-ocl/jammy,now 0.5.0.50403-121~22.04 amd64 [installed,automatic]
rocm-cmake/jammy,now 0.8.0.50403-121~22.04 amd64 [installed,automatic]
rocm-core/jammy,now 5.4.3.50403-121~22.04 amd64 [installed,automatic]
rocm-dbgapi/jammy,now 0.68.0.50403-121~22.04 amd64 [installed,automatic]
rocm-debug-agent/jammy,now 2.0.3.50403-121~22.04 amd64 [installed,automatic]
rocm-dev/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-developer-tools/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-device-libs/jammy,now 1.0.0.50403-121~22.04 amd64 [installed,automatic]
rocm-dkms/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-gdb/jammy,now 12.1.50403-121~22.04 amd64 [installed,automatic]
rocm-hip-libraries/jammy,now 5.4.3.50403-121~22.04 amd64 [installed,automatic]
rocm-hip-runtime-dev/jammy,now 5.4.3.50403-121~22.04 amd64 [installed,automatic]
rocm-hip-runtime/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-hip-sdk/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-language-runtime/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-llvm/jammy,now 15.0.0.23045.50403-121~22.04 amd64 [installed,automatic]
rocm-ml-libraries/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-ml-sdk/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-ocl-icd/jammy,now 2.0.0.50403-121~22.04 amd64 [installed,automatic]
rocm-opencl-dev/jammy,now 2.0.0.50403-121~22.04 amd64 [installed]
rocm-opencl-runtime/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-opencl-sdk/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocm-opencl/jammy,now 2.0.0.50403-121~22.04 amd64 [installed]
rocm-smi-lib/jammy,now 5.0.0.50403-121~22.04 amd64 [installed,automatic]
rocm-utils/jammy,now 5.4.3.50403-121~22.04 amd64 [installed]
rocminfo/jammy,now 1.0.0.50403-121~22.04 amd64 [installed,automatic]
rocmtools-dev/jammy,now 1.5.0.50403-121~22.04 amd64 [installed]
```

```
$ rocminfo 
ROCk module is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1148
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```

```
/opt/rocm/bin/rocm-bandwidth-test 
HSA Error Found!  In file: /long_pathname_so_that_rpms_can_package_the_debug_info/src/tests/rocm_bandwidth_test/rocm_bandwidth_test_parse.cpp;   At line: 519
Error: HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```

``` 
$ lshw -class video
*-display
       description: VGA compatible controller
       product: Advanced Micro Devices, Inc. [AMD/ATI]
       vendor: Advanced Micro Devices, Inc. [AMD/ATI]
       physical id: 0
       bus info: pci@0000:83:00.0
       version: c8
       width: 64 bits
       clock: 33MHz
       capabilities: pm pciexpress msi vga_controller bus_master cap_list rom
       configuration: driver=amdgpu latency=0
       resources: iomemory:2c00-2bff iomemory:2c80-2c7f irq:199 memory:2c000000000-2c7ffffffff memory:2c800000000-2c8001fffff ioport:9000(size=256) memory:d0d00000-d0dfffff memory:d0e00000-d0e1ffff
```

`clinfo` lists the NVIDIA GPU card that I have in one of the slots but does not list the Radeon card.

The user here is added to both the `video` and `render` groups.

---

## 评论 (2 条)

### 评论 #1 — bondhugula (2023-05-30T07:18:46Z)

Some information from the kernel ogs when the above failure happens:
```
[  164.984413] amdgpu 0000:83:00.0: amdgpu: SMU driver if version not matched
[  164.984459] amdgpu 0000:83:00.0: amdgpu: dpm has been enabled
[  164.984460] amdgpu 0000:83:00.0: amdgpu: SMU is resumed successfully!
[  164.986450] [drm] DMUB hardware initialized: version=0x07000A01
[  164.990828] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:92
[  164.993409] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:100
[  164.995988] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:108
[  164.998570] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:116
[  165.001267] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:92
[  165.003855] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:100
[  165.006447] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:108
[  165.009040] [drm] REG_WAIT timeout 1us * 1000 tries - dcn32_dsc_pg_control line:116
[  165.374627] amdgpu 0000:83:00.0: amdgpu: rlc autoload: gc ucode autoload timeout
[  165.374630] amdgpu 0000:83:00.0: amdgpu: (-110) failed to wait rlc autoload complete
[  165.374631] [drm:amdgpu_device_ip_resume_phase2 [amdgpu]] *ERROR* resume of IP block <gfx_v11_0> failed -110
[  165.374720] amdgpu 0000:83:00.0: amdgpu: amdgpu_device_ip_resume failed (-110).
```

---

### 评论 #2 — bondhugula (2023-05-30T08:52:36Z)

I've found the cause of this and managed to fix it. The kernel log above indicated this was an issue with the kernel. I had the kernel `linux-image-5.19.0-41-generic:amd64`, which was the latest available in the Ubuntu 22.04 repo.

A Google search on the actual error led me to https://forums.linuxmint.com/viewtopic.php?t=389134&start=20, which suggested that upgrading to 6.1.x may solve the issue. Another search revealed that kernel 6.1 was already available in the Ubuntu 22.04 repo (not installed by default). https://askubuntu.com/questions/1445894/when-can-i-update-22-04-to-kernel-6-1
(note that the exact version has changed)

```
$ apt search linux-image-6.1
Sorting... Done
Full Text Search... Done
linux-image-6.1.0-1012-oem/jammy-updates,jammy-security,now 6.1.0-1012.12 amd64 [installed]
  Signed kernel image oem

linux-image-6.1.0-1013-oem/jammy-updates,jammy-security 6.1.0-1013.13 amd64
  Signed kernel image oem
```

Installing this one:

```
sudo apt install linux-image-6.1.0-1012-oem linux-headers-6.1.0-1012-oem
```

and rebooting resolves the issue and the GPU correctly initializes/resumes.

```
$ rocminfo 
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen Threadripper PRO 5975WX 32-Cores
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Threadripper PRO 5975WX 32-Cores
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
  Max Clock Freq. (MHz):   3600                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            64                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    263731960(0xfb83af8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    263731960(0xfb83af8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    263731960(0xfb83af8) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-XX                             
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
  BDFID:                   33536                              
  Internal Node ID:        1                                  
  Compute Unit:            96                                 
  SIMDs per CU:            2                                  
  Shader Engines:          12                                 
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
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    25149440(0x17fc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
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

`rocm-bandwidth-test` runs correctly.

`sensors` correctly report temperature.
```
amdgpu-pci-8300
Adapter: PCI adapter
vddgfx:      750.00 mV 
fan1:           0 RPM  (min =    0 RPM, max = 65519 RPM)
edge:         +35.0°C  (crit = +65535.0°C, hyst = -273.1°C)
                       (emerg = +65540.0°C)
junction:     +39.0°C  (crit = +65535.0°C, hyst = -273.1°C)
                       (emerg = +65540.0°C)
mem:          +50.0°C  (crit = +65535.0°C, hyst = -273.1°C)
                       (emerg = +65540.0°C)
PPT:          75.00 W  (cap = 327.00 W)

```

---
