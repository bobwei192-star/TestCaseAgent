# [Issue]: rocminfo doesn't show GPU

> **Issue #3897**
> **状态**: closed
> **创建时间**: 2024-10-15T08:11:33Z
> **更新时间**: 2024-10-18T13:36:06Z
> **关闭时间**: 2024-10-18T13:36:06Z
> **作者**: urbandroid
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3897

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

NAME="Ubuntu"
VERSION="24.04.1 LTS (Noble Numbat)"
CPU: 
model name	: Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
GPU:
  Name:                    Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
  Marketing Name:          Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz



### Operating System

24.04.1 LTS (Noble Numbat)

### CPU

amd radeon hd 8750m

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

just run rocminfo

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

/opt/rocm/bin/rocminfo --support
ROCk module version 6.8.5 is loaded
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
  Name:                    Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
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
  Max Clock Freq. (MHz):   2600                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             


### Additional Information

dpkg -l | grep rocm
ii  rocm                                             6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) software stack meta package
ii  rocm-cmake                                       0.13.0.60202-116~24.04                    amd64        rocm-cmake built using CMake
ii  rocm-core                                        6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-dbgapi                                      0.76.0.60202-116~24.04                    amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent                                 2.0.3.60202-116~24.04                     amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-developer-tools                             6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                                 1.0.0.60202-116~24.04                     amd64        Radeon Open Compute - device libraries
ii  rocm-gdb                                         14.2.60202-116~24.04                      amd64        ROCgdb
ii  rocm-hip-libraries                               6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime                                 6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev                             6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-sdk                                     6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime                            6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm                                        18.0.0.24355.60202-116~24.04              amd64        ROCm core compiler
ii  rocm-ml-libraries                                6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ml-sdk                                      6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl                                      2.0.0.60202-116~24.04                     amd64        clr built using CMake
ii  rocm-opencl-dev                                  2.0.0.60202-116~24.04                     amd64        clr built using CMake
ii  rocm-opencl-icd-loader                           1.2.60202-116~24.04                       amd64        OpenCL-ICD-Loader built using CMake
ii  rocm-opencl-runtime                              6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl-sdk                                  6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp-sdk                                  6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
ii  rocm-smi-lib                                     7.3.0.60202-116~24.04                     amd64        AMD System Management libraries
ii  rocm-utils                                       6.2.2.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocminfo                                         1.0.0.60202-116~24.04                     amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool


lsmod | grep amdgpu
amdgpu              19632128  0
amddrm_ttm_helper      12288  1 amdgpu
amdttm                110592  2 amdgpu,amddrm_ttm_helper
amddrm_buddy           20480  1 amdgpu
amdxcp                 12288  1 amdgpu
drm_exec               12288  1 amdgpu
drm_suballoc_helper    16384  1 amdgpu
amd_sched              61440  1 amdgpu
amdkcl                 32768  3 amd_sched,amdttm,amdgpu
drm_display_helper    237568  2 amdgpu,i915
i2c_algo_bit           16384  2 amdgpu,i915
video                  73728  3 acer_wmi,amdgpu,i915

---

## 评论 (16 条)

### 评论 #1 — harkgill-amd (2024-10-15T14:54:44Z)

Hi @urbandroid, could you please provide the following

1. Output of `lspci | grep VGA`
2. Output of `rocminfo`
3. dmesg output

Thanks!

---

### 评论 #2 — urbandroid (2024-10-15T15:00:22Z)

Hi there @harkgill-amd  here is the information you have asked.

amd radeon hd 8750m

lspci | grep VGA
00:02.0 VGA compatible controller: Intel Corporation Haswell-ULT Integrated Graphics Controller (rev 09)

lspci -nn | grep '\[03'
00:02.0 VGA compatible controller [0300]: Intel Corporation Haswell-ULT Integrated Graphics Controller [8086:0a16] (rev 09)
03:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Mars [Radeon HD 8670A/8670M/8750M / R7 M370] [1002:6600]


rocminfo
ROCk module version 6.8.5 is loaded
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
  Name:                    Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
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
  Max Clock Freq. (MHz):   2600                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***             

3.dmesg

inux version 6.8.0-45-generic (buildd@lcy02-amd64-115) (x86_64-linux-gnu-gcc-13 (Ubuntu 13.2.0-23ubuntu4) 13.2.0, GNU ld (GNU Binutils for Ubuntu) 2.42) #45-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 30 12:02:04 UTC 2024 (Ubuntu 6.8.0-45.45-generic 6.8.12)
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-6.8.0-45-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro quiet splash radeon.si_support=0 radeon.cik_support=0 amdgpu.si_support=1 amdgpu.cik_support=1 amdgpu.runpm=0 vt.handoff=7
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
[    0.000000]   Hygon HygonGenuine
[    0.000000]   Centaur CentaurHauls
[    0.000000]   zhaoxin   Shanghai  
[    0.000000] BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000006efff] usable
[    0.000000] BIOS-e820: [mem 0x000000000006f000-0x000000000006ffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000070000-0x0000000000087fff] usable
[    0.000000] BIOS-e820: [mem 0x0000000000088000-0x00000000000bffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x0000000094caffff] usable
[    0.000000] BIOS-e820: [mem 0x0000000094cb0000-0x00000000960affff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000960b0000-0x000000009a6befff] usable
[    0.000000] BIOS-e820: [mem 0x000000009a6bf000-0x000000009aebefff] reserved
[    0.000000] BIOS-e820: [mem 0x000000009aebf000-0x000000009afbefff] ACPI NVS
[    0.000000] BIOS-e820: [mem 0x000000009afbf000-0x000000009affefff] ACPI data
[    0.000000] BIOS-e820: [mem 0x000000009afff000-0x000000009affffff] usable
[    0.000000] BIOS-e820: [mem 0x000000009b000000-0x000000009f9fffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000e0000000-0x00000000efffffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fe101000-0x00000000fe112fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000feb00000-0x00000000feb0ffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fed00000-0x00000000fee00fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000ffc00000-0x00000000ffffffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000100000000-0x000000035f5fffff] usable
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] APIC: Static calls initialized
[    0.000000] e820: update [mem 0x93906018-0x93916057] usable ==> usable
[    0.000000] e820: update [mem 0x93906018-0x93916057] usable ==> usable
[    0.000000] e820: update [mem 0x938f7018-0x93905c57] usable ==> usable
[    0.000000] e820: update [mem 0x938f7018-0x93905c57] usable ==> usable
[    0.000000] extended physical RAM map:
[    0.000000] reserve setup_data: [mem 0x0000000000000000-0x000000000006efff] usable
[    0.000000] reserve setup_data: [mem 0x000000000006f000-0x000000000006ffff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000000070000-0x0000000000087fff] usable
[    0.000000] reserve setup_data: [mem 0x0000000000088000-0x00000000000bffff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000000100000-0x00000000938f7017] usable
[    0.000000] reserve setup_data: [mem 0x00000000938f7018-0x0000000093905c57] usable
[    0.000000] reserve setup_data: [mem 0x0000000093905c58-0x0000000093906017] usable
[    0.000000] reserve setup_data: [mem 0x0000000093906018-0x0000000093916057] usable
[    0.000000] reserve setup_data: [mem 0x0000000093916058-0x0000000094caffff] usable
[    0.000000] reserve setup_data: [mem 0x0000000094cb0000-0x00000000960affff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000960b0000-0x000000009a6befff] usable
[    0.000000] reserve setup_data: [mem 0x000000009a6bf000-0x000000009aebefff] reserved
[    0.000000] reserve setup_data: [mem 0x000000009aebf000-0x000000009afbefff] ACPI NVS
[    0.000000] reserve setup_data: [mem 0x000000009afbf000-0x000000009affefff] ACPI data
[    0.000000] reserve setup_data: [mem 0x000000009afff000-0x000000009affffff] usable
[    0.000000] reserve setup_data: [mem 0x000000009b000000-0x000000009f9fffff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000e0000000-0x00000000efffffff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000fe101000-0x00000000fe112fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000feb00000-0x00000000feb0ffff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000fed00000-0x00000000fee00fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000ffc00000-0x00000000ffffffff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000100000000-0x000000035f5fffff] usable
[    0.000000] efi: EFI v2.3.1 by INSYDE Corp.
[    0.000000] efi: ACPI=0x9affe000 ACPI 2.0=0x9affe014 SMBIOS=0x9aebef98 MOKvar=0x9a944000 INITRD=0x960be898 RNG=0x9affce18 
[    0.000000] random: crng init done
[    0.000000] efi: Remove mem109: MMIO range=[0xe0000000-0xefffffff] (256MB) from e820 map
[    0.000000] e820: remove [mem 0xe0000000-0xefffffff] reserved
[    0.000000] efi: Not removing mem111: MMIO range=[0xfeb00000-0xfeb0ffff] (64KB) from e820 map
[    0.000000] efi: Not removing mem112: MMIO range=[0xfec00000-0xfec00fff] (4KB) from e820 map
[    0.000000] efi: Remove mem113: MMIO range=[0xfed00000-0xfee00fff] (1MB) from e820 map
[    0.000000] e820: remove [mem 0xfed00000-0xfee00fff] reserved
[    0.000000] efi: Remove mem114: MMIO range=[0xffc00000-0xffffffff] (4MB) from e820 map
[    0.000000] e820: remove [mem 0xffc00000-0xffffffff] reserved
[    0.000000] secureboot: Secure boot disabled
[    0.000000] SMBIOS 2.7 present.
[    0.000000] DMI: Packard Bell EasyNote TE69HW/EG50_HW   , BIOS V2.10 10/07/2013
[    0.000000] tsc: Fast TSC calibration using PIT
[    0.000000] tsc: Detected 2294.550 MHz processor
[    0.000107] e820: update [mem 0x00000000-0x00000fff] usable ==> reserved
[    0.000111] e820: remove [mem 0x000a0000-0x000fffff] usable
[    0.000123] last_pfn = 0x35f600 max_arch_pfn = 0x400000000
[    0.000132] MTRR map: 11 entries (5 fixed + 6 variable; max 25), built from 10 variable MTRRs
[    0.000135] x86/PAT: Configuration [0-7]: WB  WC  UC- UC  WB  WP  UC- WT  
[    0.000537] last_pfn = 0x9b000 max_arch_pfn = 0x400000000
[    0.014408] Using GB pages for direct mapping
[    0.014931] secureboot: Secure boot disabled
[    0.014932] RAMDISK: [mem 0x8590b000-0x8f3d6fff]
[    0.015593] ACPI: Early table checksum verification disabled
[    0.015597] ACPI: RSDP 0x000000009AFFE014 000024 (v02 ACRSYS)
[    0.015603] ACPI: XSDT 0x000000009AFFE210 0000AC (v01 ACRSYS ACRPRDCT 00000001      01000013)
[    0.015610] ACPI: FACP 0x000000009AFF8000 00010C (v05 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015618] ACPI: DSDT 0x000000009AFE4000 0102D4 (v01 ACRSYS ACRPRDCT 00000000 1025 00040000)
[    0.015624] ACPI: FACS 0x000000009AFB9000 000040
[    0.015628] ACPI: UEFI 0x000000009AFFD000 000236 (v01 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015633] ACPI: FPDT 0x000000009AFFB000 000044 (v01 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015637] ACPI: MSDM 0x000000009AFFA000 000055 (v03 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015642] ACPI: ASF! 0x000000009AFF9000 0000A5 (v32 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015647] ACPI: HPET 0x000000009AFF7000 000038 (v01 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015651] ACPI: APIC 0x000000009AFF6000 00008C (v03 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015656] ACPI: MCFG 0x000000009AFF5000 00003C (v01 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015660] ACPI: SSDT 0x000000009AFE1000 002028 (v01 ACRSYS ACRPRDCT 00001000 1025 00040000)
[    0.015665] ACPI: BOOT 0x000000009AFDF000 000028 (v01 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015670] ACPI: ASPT 0x000000009AFDD000 000034 (v07 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015674] ACPI: DBGP 0x000000009AFDC000 000034 (v01 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015679] ACPI: SSDT 0x000000009AFDB000 000539 (v01 ACRSYS ACRPRDCT 00003000 1025 00040000)
[    0.015684] ACPI: SSDT 0x000000009AFDA000 000AD8 (v01 ACRSYS ACRPRDCT 00003000 1025 00040000)
[    0.015688] ACPI: SSDT 0x000000009AFD6000 003B45 (v01 ACRSYS ACRPRDCT 00003000 1025 00040000)
[    0.015693] ACPI: SSDT 0x000000009AFD3000 001DDA (v01 ACRSYS ACRPRDCT 00001000 1025 00040000)
[    0.015698] ACPI: BGRT 0x000000009AFD5000 000038 (v01 ACRSYS ACRPRDCT 00000001 1025 00040000)
[    0.015701] ACPI: Reserving FACP table memory at [mem 0x9aff8000-0x9aff810b]
[    0.015704] ACPI: Reserving DSDT table memory at [mem 0x9afe4000-0x9aff42d3]
[    0.015705] ACPI: Reserving FACS table memory at [mem 0x9afb9000-0x9afb903f]
[    0.015706] ACPI: Reserving UEFI table memory at [mem 0x9affd000-0x9affd235]
[    0.015708] ACPI: Reserving FPDT table memory at [mem 0x9affb000-0x9affb043]
[    0.015709] ACPI: Reserving MSDM table memory at [mem 0x9affa000-0x9affa054]
[    0.015710] ACPI: Reserving ASF! table memory at [mem 0x9aff9000-0x9aff90a4]
[    0.015711] ACPI: Reserving HPET table memory at [mem 0x9aff7000-0x9aff7037]
[    0.015713] ACPI: Reserving APIC table memory at [mem 0x9aff6000-0x9aff608b]
[    0.015714] ACPI: Reserving MCFG table memory at [mem 0x9aff5000-0x9aff503b]
[    0.015715] ACPI: Reserving SSDT table memory at [mem 0x9afe1000-0x9afe3027]
[    0.015716] ACPI: Reserving BOOT table memory at [mem 0x9afdf000-0x9afdf027]
[    0.015718] ACPI: Reserving ASPT table memory at [mem 0x9afdd000-0x9afdd033]
[    0.015719] ACPI: Reserving DBGP table memory at [mem 0x9afdc000-0x9afdc033]
[    0.015720] ACPI: Reserving SSDT table memory at [mem 0x9afdb000-0x9afdb538]
[    0.015721] ACPI: Reserving SSDT table memory at [mem 0x9afda000-0x9afdaad7]
[    0.015723] ACPI: Reserving SSDT table memory at [mem 0x9afd6000-0x9afd9b44]
[    0.015724] ACPI: Reserving SSDT table memory at [mem 0x9afd3000-0x9afd4dd9]
[    0.015725] ACPI: Reserving BGRT table memory at [mem 0x9afd5000-0x9afd5037]
[    0.015853] No NUMA configuration found
[    0.015855] Faking a node at [mem 0x0000000000000000-0x000000035f5fffff]
[    0.015867] NODE_DATA(0) allocated [mem 0x35f5d5000-0x35f5fffff]
[    0.016109] Zone ranges:
[    0.016111]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
[    0.016113]   DMA32    [mem 0x0000000001000000-0x00000000ffffffff]
[    0.016116]   Normal   [mem 0x0000000100000000-0x000000035f5fffff]
[    0.016118]   Device   empty
[    0.016119] Movable zone start for each node
[    0.016123] Early memory node ranges
[    0.016124]   node   0: [mem 0x0000000000001000-0x000000000006efff]
[    0.016126]   node   0: [mem 0x0000000000070000-0x0000000000087fff]
[    0.016127]   node   0: [mem 0x0000000000100000-0x0000000094caffff]
[    0.016129]   node   0: [mem 0x00000000960b0000-0x000000009a6befff]
[    0.016130]   node   0: [mem 0x000000009afff000-0x000000009affffff]
[    0.016131]   node   0: [mem 0x0000000100000000-0x000000035f5fffff]
[    0.016134] Initmem setup node 0 [mem 0x0000000000001000-0x000000035f5fffff]
[    0.016140] On node 0, zone DMA: 1 pages in unavailable ranges
[    0.016143] On node 0, zone DMA: 1 pages in unavailable ranges
[    0.016169] On node 0, zone DMA: 120 pages in unavailable ranges
[    0.020669] On node 0, zone DMA32: 5120 pages in unavailable ranges
[    0.020704] On node 0, zone DMA32: 2368 pages in unavailable ranges
[    0.038721] On node 0, zone Normal: 20480 pages in unavailable ranges
[    0.038753] On node 0, zone Normal: 2560 pages in unavailable ranges
[    0.038761] Reserving Intel graphics memory at [mem 0x9ba00000-0x9f9fffff]
[    0.038877] ACPI: PM-Timer IO Port: 0x1808
[    0.038898] IOAPIC[0]: apic_id 2, version 32, address 0xfec00000, GSI 0-39
[    0.038902] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
[    0.038904] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)
[    0.038910] ACPI: Using ACPI (MADT) for SMP configuration information
[    0.038912] ACPI: HPET id: 0x8086a201 base: 0xfed00000
[    0.038924] e820: update [mem 0x975ae000-0x97628fff] usable ==> reserved
[    0.038940] TSC deadline timer available
[    0.038941] smpboot: Allowing 8 CPUs, 4 hotplug CPUs
[    0.038963] PM: hibernation: Registered nosave memory: [mem 0x00000000-0x00000fff]
[    0.038966] PM: hibernation: Registered nosave memory: [mem 0x0006f000-0x0006ffff]
[    0.038968] PM: hibernation: Registered nosave memory: [mem 0x00088000-0x000bffff]
[    0.038969] PM: hibernation: Registered nosave memory: [mem 0x000c0000-0x000fffff]
[    0.038972] PM: hibernation: Registered nosave memory: [mem 0x938f7000-0x938f7fff]
[    0.038974] PM: hibernation: Registered nosave memory: [mem 0x93905000-0x93905fff]
[    0.038975] PM: hibernation: Registered nosave memory: [mem 0x93906000-0x93906fff]
[    0.038977] PM: hibernation: Registered nosave memory: [mem 0x93916000-0x93916fff]
[    0.038980] PM: hibernation: Registered nosave memory: [mem 0x94cb0000-0x960affff]
[    0.038982] PM: hibernation: Registered nosave memory: [mem 0x975ae000-0x97628fff]
[    0.038985] PM: hibernation: Registered nosave memory: [mem 0x9a6bf000-0x9aebefff]
[    0.038986] PM: hibernation: Registered nosave memory: [mem 0x9aebf000-0x9afbefff]
[    0.038987] PM: hibernation: Registered nosave memory: [mem 0x9afbf000-0x9affefff]
[    0.038989] PM: hibernation: Registered nosave memory: [mem 0x9b000000-0x9f9fffff]
[    0.038990] PM: hibernation: Registered nosave memory: [mem 0x9fa00000-0xfe100fff]
[    0.038992] PM: hibernation: Registered nosave memory: [mem 0xfe101000-0xfe112fff]
[    0.038993] PM: hibernation: Registered nosave memory: [mem 0xfe113000-0xfeafffff]
[    0.038994] PM: hibernation: Registered nosave memory: [mem 0xfeb00000-0xfeb0ffff]
[    0.038995] PM: hibernation: Registered nosave memory: [mem 0xfeb10000-0xfebfffff]
[    0.038996] PM: hibernation: Registered nosave memory: [mem 0xfec00000-0xfec00fff]
[    0.038997] PM: hibernation: Registered nosave memory: [mem 0xfec01000-0xffffffff]
[    0.038999] [mem 0x9fa00000-0xfe100fff] available for PCI devices
[    0.039001] Booting paravirtualized kernel on bare hardware
[    0.039004] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1910969940391419 ns
[    0.039015] setup_percpu: NR_CPUS:8192 nr_cpumask_bits:8 nr_cpu_ids:8 nr_node_ids:1
[    0.039735] percpu: Embedded 86 pages/cpu s229376 r8192 d114688 u524288
[    0.039746] pcpu-alloc: s229376 r8192 d114688 u524288 alloc=1*2097152
[    0.039749] pcpu-alloc: [0] 0 1 2 3 [0] 4 5 6 7 
[    0.039781] Kernel command line: BOOT_IMAGE=/vmlinuz-6.8.0-45-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro quiet splash radeon.si_support=0 radeon.cik_support=0 amdgpu.si_support=1 amdgpu.cik_support=1 amdgpu.runpm=0 vt.handoff=7
[    0.040015] Unknown kernel command line parameters "splash BOOT_IMAGE=/vmlinuz-6.8.0-45-generic", will be passed to user space.
[    0.041882] Dentry cache hash table entries: 2097152 (order: 12, 16777216 bytes, linear)
[    0.042815] Inode-cache hash table entries: 1048576 (order: 11, 8388608 bytes, linear)
[    0.042999] Fallback order for Node 0: 0 
[    0.043004] Built 1 zonelists, mobility grouping on.  Total pages: 3066269
[    0.043006] Policy zone: Normal
[    0.043014] mem auto-init: stack:all(zero), heap alloc:on, heap free:off
[    0.043019] software IO TLB: area num 8.
[    0.092662] Memory: 11893540K/12460312K available (22528K kernel code, 4442K rwdata, 14312K rodata, 4976K init, 4732K bss, 566512K reserved, 0K cma-reserved)
[    0.093968] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=8, Nodes=1
[    0.093986] Kernel/User page tables isolation: enabled
[    0.094029] ftrace: allocating 57892 entries in 227 pages
[    0.106574] ftrace: allocated 227 pages with 5 groups
[    0.107637] Dynamic Preempt: voluntary
[    0.107732] rcu: Preemptible hierarchical RCU implementation.
[    0.107733] rcu: 	RCU restricting CPUs from NR_CPUS=8192 to nr_cpu_ids=8.
[    0.107735] 	Trampoline variant of Tasks RCU enabled.
[    0.107736] 	Rude variant of Tasks RCU enabled.
[    0.107737] 	Tracing variant of Tasks RCU enabled.
[    0.107738] rcu: RCU calculated value of scheduler-enlistment delay is 100 jiffies.
[    0.107739] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=8
[    0.111383] NR_IRQS: 524544, nr_irqs: 760, preallocated irqs: 16
[    0.111609] rcu: srcu_init: Setting srcu_struct sizes based on contention.
[    0.111716] Console: colour dummy device 80x25
[    0.111720] printk: legacy console [tty0] enabled
[    0.111787] ACPI: Core revision 20230628
[    0.111972] clocksource: hpet: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 133484882848 ns
[    0.111986] APIC: Switch to symmetric I/O mode setup
[    0.112584] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.116988] clocksource: tsc-early: mask: 0xffffffffffffffff max_cycles: 0x211318dcfea, max_idle_ns: 440795247284 ns
[    0.116993] Calibrating delay loop (skipped), value calculated using timer frequency.. 4589.10 BogoMIPS (lpj=2294550)
[    0.117022] CPU0: Thermal monitoring enabled (TM1)
[    0.117061] process: using mwait in idle threads
[    0.117065] Last level iTLB entries: 4KB 1024, 2MB 1024, 4MB 1024
[    0.117067] Last level dTLB entries: 4KB 1024, 2MB 1024, 4MB 1024, 1GB 4
[    0.117071] Spectre V1 : Mitigation: usercopy/swapgs barriers and __user pointer sanitization
[    0.117074] Spectre V2 : Mitigation: Retpolines
[    0.117075] Spectre V2 : Spectre v2 / SpectreRSB mitigation: Filling RSB on context switch
[    0.117077] Spectre V2 : Spectre v2 / SpectreRSB : Filling RSB on VMEXIT
[    0.117078] Spectre V2 : Enabling Restricted Speculation for firmware calls
[    0.117080] Spectre V2 : mitigation: Enabling conditional Indirect Branch Prediction Barrier
[    0.117082] Spectre V2 : User space: Mitigation: STIBP via prctl
[    0.117084] Speculative Store Bypass: Mitigation: Speculative Store Bypass disabled via prctl
[    0.117086] MDS: Mitigation: Clear CPU buffers
[    0.117088] MMIO Stale Data: Unknown: No mitigations
[    0.117089] SRBDS: Mitigation: Microcode
[    0.117095] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    0.117097] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
[    0.117099] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
[    0.117100] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
[    0.117102] x86/fpu: Enabled xstate features 0x7, context size is 832 bytes, using 'standard' format.
[    0.147121] Freeing SMP alternatives memory: 48K
[    0.147127] pid_max: default: 32768 minimum: 301
[    0.152056] LSM: initializing lsm=lockdown,capability,landlock,yama,apparmor,integrity
[    0.152084] landlock: Up and running.
[    0.152085] Yama: becoming mindful.
[    0.152128] AppArmor: AppArmor initialized
[    0.152200] Mount-cache hash table entries: 32768 (order: 6, 262144 bytes, linear)
[    0.152221] Mountpoint-cache hash table entries: 32768 (order: 6, 262144 bytes, linear)
[    0.153063] smpboot: CPU0: Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz (family: 0x6, model: 0x45, stepping: 0x1)
[    0.153261] RCU Tasks: Setting shift to 3 and lim to 1 rcu_task_cb_adjust=1.
[    0.153282] RCU Tasks Rude: Setting shift to 3 and lim to 1 rcu_task_cb_adjust=1.
[    0.153301] RCU Tasks Trace: Setting shift to 3 and lim to 1 rcu_task_cb_adjust=1.
[    0.153318] Performance Events: PEBS fmt2+, Haswell events, 16-deep LBR, full-width counters, Intel PMU driver.
[    0.153368] ... version:                3
[    0.153370] ... bit width:              48
[    0.153371] ... generic registers:      4
[    0.153372] ... value mask:             0000ffffffffffff
[    0.153373] ... max period:             00007fffffffffff
[    0.153374] ... fixed-purpose events:   3
[    0.153376] ... event mask:             000000070000000f
[    0.153541] signal: max sigframe size: 1776
[    0.153559] Estimated ratio of average max frequency by base frequency (times 1024): 1024
[    0.155110] rcu: Hierarchical SRCU implementation.
[    0.155114] rcu: 	Max phase no-delay instances is 400.
[    0.156053] NMI watchdog: Enabled. Permanently consumes one hw-PMU counter.
[    0.156154] smp: Bringing up secondary CPUs ...
[    0.156296] smpboot: x86: Booting SMP configuration:
[    0.156298] .... node  #0, CPUs:      #2 #1 #3
[    0.160016] MDS CPU bug present and SMT on, data leak possible. See https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/mds.html for more details.
[    0.160048] smp: Brought up 1 node, 4 CPUs
[    0.160048] smpboot: Max logical packages: 2
[    0.160048] smpboot: Total of 4 processors activated (18356.40 BogoMIPS)
[    0.161442] devtmpfs: initialized
[    0.161442] x86/mm: Memory block size: 128MB
[    0.163146] ACPI: PM: Registering ACPI NVS region [mem 0x9aebf000-0x9afbefff] (1048576 bytes)
[    0.163146] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275000 ns
[    0.163159] futex hash table entries: 2048 (order: 5, 131072 bytes, linear)
[    0.163242] pinctrl core: initialized pinctrl subsystem
[    0.163336] PM: RTC time: 08:16:57, date: 2024-10-15
[    0.164191] NET: Registered PF_NETLINK/PF_ROUTE protocol family
[    0.164530] DMA: preallocated 2048 KiB GFP_KERNEL pool for atomic allocations
[    0.164701] DMA: preallocated 2048 KiB GFP_KERNEL|GFP_DMA pool for atomic allocations
[    0.164874] DMA: preallocated 2048 KiB GFP_KERNEL|GFP_DMA32 pool for atomic allocations
[    0.164901] audit: initializing netlink subsys (disabled)
[    0.164995] audit: type=2000 audit(1728980217.052:1): state=initialized audit_enabled=0 res=1
[    0.165238] thermal_sys: Registered thermal governor 'fair_share'
[    0.165241] thermal_sys: Registered thermal governor 'bang_bang'
[    0.165242] thermal_sys: Registered thermal governor 'step_wise'
[    0.165243] thermal_sys: Registered thermal governor 'user_space'
[    0.165245] thermal_sys: Registered thermal governor 'power_allocator'
[    0.165256] EISA bus registered
[    0.165300] cpuidle: using governor ladder
[    0.165300] cpuidle: using governor menu
[    0.165300] Simple Boot Flag at 0x44 set to 0x1
[    0.165300] ACPI FADT declares the system doesn't support PCIe ASPM, so disable it
[    0.165300] acpiphp: ACPI Hot Plug PCI Controller Driver version: 0.5
[    0.165300] PCI: ECAM [mem 0xe0000000-0xefffffff] (base 0xe0000000) for domain 0000 [bus 00-ff]
[    0.165300] PCI: not using ECAM ([mem 0xe0000000-0xefffffff] not reserved)
[    0.165300] PCI: Using configuration type 1 for base access
[    0.165364] core: PMU erratum BJ122, BV98, HSD29 worked around, HT is on
[    0.165468] kprobes: kprobe jump-optimization is enabled. All kprobes are optimized if possible.
[    0.166057] HugeTLB: registered 1.00 GiB page size, pre-allocated 0 pages
[    0.166057] HugeTLB: 16380 KiB vmemmap can be freed for a 1.00 GiB page
[    0.166057] HugeTLB: registered 2.00 MiB page size, pre-allocated 0 pages
[    0.166057] HugeTLB: 28 KiB vmemmap can be freed for a 2.00 MiB page
[    0.166187] ACPI: Added _OSI(Module Device)
[    0.166190] ACPI: Added _OSI(Processor Device)
[    0.166193] ACPI: Added _OSI(3.0 _SCP Extensions)
[    0.166195] ACPI: Added _OSI(Processor Aggregator Device)
[    0.188476] ACPI: 6 ACPI AML tables successfully acquired and loaded
[    0.189996] ACPI: [Firmware Bug]: BIOS _OSI(Linux) query ignored
[    0.192528] ACPI: Dynamic OEM Table Load:
[    0.192539] ACPI: SSDT 0xFFFF96608028E000 0003D3 (v01 PmRef  Cpu0Cst  00003001 INTL 20120913)
[    0.194068] ACPI: Dynamic OEM Table Load:
[    0.194077] ACPI: SSDT 0xFFFF966080FA3800 0005AA (v01 PmRef  ApIst    00003000 INTL 20120913)
[    0.195418] ACPI: Dynamic OEM Table Load:
[    0.195425] ACPI: SSDT 0xFFFF9660801F6400 000119 (v01 PmRef  ApCst    00003000 INTL 20120913)
[    0.197239] ACPI: _OSC evaluated successfully for all CPUs
[    0.197322] ACPI: EC: EC started
[    0.197323] ACPI: EC: interrupt blocked
[    0.210492] ACPI: EC: EC_CMD/EC_SC=0x66, EC_DATA=0x62
[    0.210496] ACPI: \_SB_.PCI0.LPCB.EC0_: Boot DSDT EC used to handle transactions
[    0.210499] ACPI: Interpreter enabled
[    0.210537] ACPI: PM: (supports S0 S3 S4 S5)
[    0.210538] ACPI: Using IOAPIC for interrupt routing
[    0.211783] PCI: ECAM [mem 0xe0000000-0xefffffff] (base 0xe0000000) for domain 0000 [bus 00-ff]
[    0.212509] PCI: ECAM [mem 0xe0000000-0xefffffff] reserved as ACPI motherboard resource
[    0.212524] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
[    0.212526] PCI: Using E820 reservations for host bridge windows
[    0.212986] ACPI: Enabled 8 GPEs in block 00 to 7F
[    0.253272] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-fe])
[    0.253281] acpi PNP0A08:00: _OSC: OS supports [ExtendedConfig ASPM ClockPM Segments MSI EDR HPX-Type3]
[    0.253662] acpi PNP0A08:00: _OSC: OS now controls [PCIeHotplug SHPCHotplug PME AER PCIeCapability LTR DPC]
[    0.253664] acpi PNP0A08:00: FADT indicates ASPM is unsupported, using BIOS configuration
[    0.254603] PCI host bridge to bus 0000:00
[    0.254606] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]
[    0.254609] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]
[    0.254612] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000fffff window]
[    0.254614] pci_bus 0000:00: root bus resource [mem 0x9fa00000-0xfeafffff window]
[    0.254616] pci_bus 0000:00: root bus resource [bus 00-fe]
[    0.254636] pci 0000:00:00.0: [8086:0a04] type 00 class 0x060000 conventional PCI endpoint
[    0.254723] pci 0000:00:02.0: [8086:0a16] type 00 class 0x030000 conventional PCI endpoint
[    0.254733] pci 0000:00:02.0: BAR 0 [mem 0xc0000000-0xc03fffff 64bit]
[    0.254741] pci 0000:00:02.0: BAR 2 [mem 0xb0000000-0xbfffffff 64bit pref]
[    0.254746] pci 0000:00:02.0: BAR 4 [io  0x4000-0x403f]
[    0.254761] pci 0000:00:02.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
[    0.254882] pci 0000:00:03.0: [8086:0a0c] type 00 class 0x040300 PCIe Root Complex Integrated Endpoint
[    0.254893] pci 0000:00:03.0: BAR 0 [mem 0xc0710000-0xc0713fff 64bit]
[    0.255019] pci 0000:00:14.0: [8086:9c31] type 00 class 0x0c0330 conventional PCI endpoint
[    0.255036] pci 0000:00:14.0: BAR 0 [mem 0xc0700000-0xc070ffff 64bit]
[    0.255091] pci 0000:00:14.0: PME# supported from D3hot D3cold
[    0.255214] pci 0000:00:16.0: [8086:9c3a] type 00 class 0x078000 conventional PCI endpoint
[    0.255233] pci 0000:00:16.0: BAR 0 [mem 0xc0718000-0xc071801f 64bit]
[    0.255298] pci 0000:00:16.0: PME# supported from D0 D3hot D3cold
[    0.255368] pci 0000:00:1b.0: [8086:9c20] type 00 class 0x040300 PCIe Root Complex Integrated Endpoint
[    0.255384] pci 0000:00:1b.0: BAR 0 [mem 0xc0714000-0xc0717fff 64bit]
[    0.255450] pci 0000:00:1b.0: PME# supported from D0 D3hot D3cold
[    0.255545] pci 0000:00:1c.0: [8086:9c14] type 01 class 0x060400 PCIe Root Port
[    0.255569] pci 0000:00:1c.0: PCI bridge to [bus 01]
[    0.255581] pci 0000:00:1c.0:   bridge window [mem 0xc0400000-0xc04fffff 64bit pref]
[    0.255632] pci 0000:00:1c.0: PME# supported from D0 D3hot D3cold
[    0.256047] pci 0000:00:1c.3: [8086:9c16] type 01 class 0x060400 PCIe Root Port
[    0.256072] pci 0000:00:1c.3: PCI bridge to [bus 02]
[    0.256078] pci 0000:00:1c.3:   bridge window [mem 0xc0600000-0xc06fffff]
[    0.256136] pci 0000:00:1c.3: PME# supported from D0 D3hot D3cold
[    0.256239] pci 0000:00:1c.4: [8086:9c18] type 01 class 0x060400 PCIe Root Port
[    0.256263] pci 0000:00:1c.4: PCI bridge to [bus 03]
[    0.256267] pci 0000:00:1c.4:   bridge window [io  0x3000-0x3fff]
[    0.256270] pci 0000:00:1c.4:   bridge window [mem 0xc0500000-0xc05fffff]
[    0.256279] pci 0000:00:1c.4:   bridge window [mem 0xa0000000-0xafffffff 64bit pref]
[    0.256328] pci 0000:00:1c.4: PME# supported from D0 D3hot D3cold
[    0.256447] pci 0000:00:1d.0: [8086:9c26] type 00 class 0x0c0320 conventional PCI endpoint
[    0.256811] pci 0000:00:1d.0: BAR 0 [mem 0xc071c000-0xc071c3ff]
[    0.257831] pci 0000:00:1d.0: PME# supported from D0 D3hot D3cold
[    0.257937] pci 0000:00:1f.0: [8086:9c43] type 00 class 0x060100 conventional PCI endpoint
[    0.258171] pci 0000:00:1f.2: [8086:9c03] type 00 class 0x010601 conventional PCI endpoint
[    0.258183] pci 0000:00:1f.2: BAR 0 [io  0x4088-0x408f]
[    0.258190] pci 0000:00:1f.2: BAR 1 [io  0x4094-0x4097]
[    0.258196] pci 0000:00:1f.2: BAR 2 [io  0x4080-0x4087]
[    0.258203] pci 0000:00:1f.2: BAR 3 [io  0x4090-0x4093]
[    0.258210] pci 0000:00:1f.2: BAR 4 [io  0x4060-0x407f]
[    0.258216] pci 0000:00:1f.2: BAR 5 [mem 0xc071b000-0xc071b7ff]
[    0.258249] pci 0000:00:1f.2: PME# supported from D3hot
[    0.258331] pci 0000:00:1f.3: [8086:9c22] type 00 class 0x0c0500 conventional PCI endpoint
[    0.258346] pci 0000:00:1f.3: BAR 0 [mem 0xc0719000-0xc07190ff 64bit]
[    0.258365] pci 0000:00:1f.3: BAR 4 [io  0x4040-0x405f]
[    0.258556] pci 0000:01:00.0: [14e4:16b3] type 00 class 0x020000 PCIe Endpoint
[    0.258585] pci 0000:01:00.0: BAR 0 [mem 0xc0410000-0xc041ffff 64bit pref]
[    0.258604] pci 0000:01:00.0: BAR 2 [mem 0xc0420000-0xc042ffff 64bit pref]
[    0.258638] pci 0000:01:00.0: ROM [mem 0xfffff800-0xffffffff pref]
[    0.258760] pci 0000:01:00.0: PME# supported from D0 D3hot D3cold
[    0.259015] pci 0000:01:00.1: [14e4:16bc] type 00 class 0x080501 PCIe Endpoint
[    0.259044] pci 0000:01:00.1: BAR 0 [mem 0xc0400000-0xc040ffff 64bit pref]
[    0.259190] pci 0000:01:00.1: PME# supported from D0 D3hot D3cold
[    0.259423] pci 0000:00:1c.0: PCI bridge to [bus 01]
[    0.259489] pci 0000:02:00.0: [168c:0036] type 00 class 0x028000 PCIe Endpoint
[    0.259515] pci 0000:02:00.0: BAR 0 [mem 0xc0600000-0xc067ffff 64bit]
[    0.259565] pci 0000:02:00.0: ROM [mem 0xffff0000-0xffffffff pref]
[    0.259645] pci 0000:02:00.0: supports D1 D2
[    0.259646] pci 0000:02:00.0: PME# supported from D0 D1 D2 D3hot D3cold
[    0.259776] pci 0000:00:1c.3: PCI bridge to [bus 02]
[    0.259859] pci 0000:03:00.0: [1002:6600] type 00 class 0x038000 PCIe Legacy Endpoint
[    0.259886] pci 0000:03:00.0: BAR 0 [mem 0xa0000000-0xafffffff 64bit pref]
[    0.259902] pci 0000:03:00.0: BAR 2 [mem 0xc0500000-0xc053ffff 64bit]
[    0.259912] pci 0000:03:00.0: BAR 4 [io  0x3000-0x30ff]
[    0.259929] pci 0000:03:00.0: ROM [mem 0xfffe0000-0xffffffff pref]
[    0.259939] pci 0000:03:00.0: enabling Extended Tags
[    0.260024] pci 0000:03:00.0: supports D1 D2
[    0.260026] pci 0000:03:00.0: PME# supported from D1 D2 D3hot
[    0.260078] pci 0000:03:00.0: 16.000 Gb/s available PCIe bandwidth, limited by 5.0 GT/s PCIe x4 link at 0000:00:1c.4 (capable of 63.008 Gb/s with 8.0 GT/s PCIe x8 link)
[    0.260195] pci 0000:00:1c.4: PCI bridge to [bus 03]
[    0.262991] ACPI: PCI: Interrupt link LNKA configured for IRQ 0
[    0.262994] ACPI: PCI: Interrupt link LNKA disabled
[    0.263061] ACPI: PCI: Interrupt link LNKB configured for IRQ 0
[    0.263063] ACPI: PCI: Interrupt link LNKB disabled
[    0.263127] ACPI: PCI: Interrupt link LNKC configured for IRQ 0
[    0.263129] ACPI: PCI: Interrupt link LNKC disabled
[    0.263193] ACPI: PCI: Interrupt link LNKD configured for IRQ 0
[    0.263194] ACPI: PCI: Interrupt link LNKD disabled
[    0.263258] ACPI: PCI: Interrupt link LNKE configured for IRQ 0
[    0.263260] ACPI: PCI: Interrupt link LNKE disabled
[    0.263323] ACPI: PCI: Interrupt link LNKF configured for IRQ 0
[    0.263325] ACPI: PCI: Interrupt link LNKF disabled
[    0.263388] ACPI: PCI: Interrupt link LNKG configured for IRQ 0
[    0.263390] ACPI: PCI: Interrupt link LNKG disabled
[    0.263453] ACPI: PCI: Interrupt link LNKH configured for IRQ 0
[    0.263455] ACPI: PCI: Interrupt link LNKH disabled
[    0.263786] ACPI: EC: interrupt unblocked
[    0.263788] ACPI: EC: event unblocked
[    0.263796] ACPI: EC: EC_CMD/EC_SC=0x66, EC_DATA=0x62
[    0.263797] ACPI: EC: GPE=0x22
[    0.263799] ACPI: \_SB_.PCI0.LPCB.EC0_: Boot DSDT EC initialization complete
[    0.263802] ACPI: \_SB_.PCI0.LPCB.EC0_: EC: Used to handle transactions and events
[    0.263881] iommu: Default domain type: Translated
[    0.263881] iommu: DMA domain TLB invalidation policy: lazy mode
[    0.263881] SCSI subsystem initialized
[    0.264013] libata version 3.00 loaded.
[    0.264030] ACPI: bus type USB registered
[    0.264044] usbcore: registered new interface driver usbfs
[    0.264052] usbcore: registered new interface driver hub
[    0.264061] usbcore: registered new device driver usb
[    0.264091] pps_core: LinuxPPS API ver. 1 registered
[    0.264092] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
[    0.264096] PTP clock support registered
[    0.264114] EDAC MC: Ver: 3.0.0
[    0.264287] efivars: Registered efivars operations
[    0.265251] NetLabel: Initializing
[    0.265253] NetLabel:  domain hash size = 128
[    0.265254] NetLabel:  protocols = UNLABELED CIPSOv4 CALIPSO
[    0.265278] NetLabel:  unlabeled traffic allowed by default
[    0.265299] mctp: management component transport protocol core
[    0.265299] NET: Registered PF_MCTP protocol family
[    0.265299] PCI: Using ACPI for IRQ routing
[    0.270601] PCI: pci_cache_line_size set to 64 bytes
[    0.270700] e820: reserve RAM buffer [mem 0x0006f000-0x0006ffff]
[    0.270703] e820: reserve RAM buffer [mem 0x00088000-0x0008ffff]
[    0.270705] e820: reserve RAM buffer [mem 0x938f7018-0x93ffffff]
[    0.270707] e820: reserve RAM buffer [mem 0x93906018-0x93ffffff]
[    0.270708] e820: reserve RAM buffer [mem 0x94cb0000-0x97ffffff]
[    0.270710] e820: reserve RAM buffer [mem 0x975ae000-0x97ffffff]
[    0.270711] e820: reserve RAM buffer [mem 0x9a6bf000-0x9bffffff]
[    0.270713] e820: reserve RAM buffer [mem 0x9b000000-0x9bffffff]
[    0.270714] e820: reserve RAM buffer [mem 0x35f600000-0x35fffffff]
[    0.270764] pci 0000:00:02.0: vgaarb: setting as boot VGA device
[    0.270764] pci 0000:00:02.0: vgaarb: bridge control possible
[    0.270764] pci 0000:00:02.0: vgaarb: VGA device added: decodes=io+mem,owns=io+mem,locks=none
[    0.270764] vgaarb: loaded
[    0.270764] hpet0: at MMIO 0xfed00000, IRQs 2, 8, 0, 0, 0, 0, 0, 0
[    0.270764] hpet0: 8 comparators, 64-bit 14.318180 MHz counter
[    0.272026] clocksource: Switched to clocksource tsc-early
[    0.273051] VFS: Disk quotas dquot_6.6.0
[    0.273078] VFS: Dquot-cache hash table entries: 512 (order 0, 4096 bytes)
[    0.273266] AppArmor: AppArmor Filesystem Enabled
[    0.273308] pnp: PnP ACPI init
[    0.273497] system 00:00: [io  0x0680-0x069f] has been reserved
[    0.273502] system 00:00: [io  0xfd60-0xfd63] has been reserved
[    0.273505] system 00:00: [io  0xffff] has been reserved
[    0.273507] system 00:00: [io  0xffff] has been reserved
[    0.273509] system 00:00: [io  0xffff] has been reserved
[    0.273511] system 00:00: [io  0x1800-0x18fe] has been reserved
[    0.273513] system 00:00: [io  0x164e-0x164f] has been reserved
[    0.273637] system 00:02: [io  0x1854-0x1857] has been reserved
[    0.275538] pnp 00:05: disabling [mem 0xffffffff-0x10000fffe] because it overlaps 0000:01:00.0 BAR 6 [mem 0xfffff800-0xffffffff pref]
[    0.275545] pnp 00:05: disabling [mem 0xffffffff-0x10000fffe disabled] because it overlaps 0000:02:00.0 BAR 6 [mem 0xffff0000-0xffffffff pref]
[    0.275549] pnp 00:05: disabling [mem 0xffffffff-0x10000fffe disabled] because it overlaps 0000:03:00.0 BAR 6 [mem 0xfffe0000-0xffffffff pref]
[    0.275576] system 00:05: [mem 0xfed1c000-0xfed1ffff] has been reserved
[    0.275579] system 00:05: [mem 0xfed10000-0xfed17fff] has been reserved
[    0.275581] system 00:05: [mem 0xfed18000-0xfed18fff] has been reserved
[    0.275583] system 00:05: [mem 0xfed19000-0xfed19fff] has been reserved
[    0.275585] system 00:05: [mem 0xe0000000-0xefffffff] has been reserved
[    0.275587] system 00:05: [mem 0xfed20000-0xfed3ffff] has been reserved
[    0.275589] system 00:05: [mem 0xfed90000-0xfed93fff] has been reserved
[    0.275591] system 00:05: [mem 0xff000000-0xff000fff] has been reserved
[    0.275593] system 00:05: [mem 0xff010000-0xffffffff] has been reserved
[    0.275595] system 00:05: [mem 0xfee00000-0xfeefffff] has been reserved
[    0.275597] system 00:05: [mem 0x9fa20000-0x9fa20fff] has been reserved
[    0.276704] pnp: PnP ACPI: found 7 devices
[    0.283162] clocksource: acpi_pm: mask: 0xffffff max_cycles: 0xffffff, max_idle_ns: 2085701024 ns
[    0.283238] NET: Registered PF_INET protocol family
[    0.283426] IP idents hash table entries: 262144 (order: 9, 2097152 bytes, linear)
[    0.305638] tcp_listen_portaddr_hash hash table entries: 8192 (order: 5, 131072 bytes, linear)
[    0.305675] Table-perturb hash table entries: 65536 (order: 6, 262144 bytes, linear)
[    0.305770] TCP established hash table entries: 131072 (order: 8, 1048576 bytes, linear)
[    0.306044] TCP bind hash table entries: 65536 (order: 9, 2097152 bytes, linear)
[    0.306401] TCP: Hash tables configured (established 131072 bind 65536)
[    0.306513] MPTCP token hash table entries: 16384 (order: 6, 393216 bytes, linear)
[    0.306575] UDP hash table entries: 8192 (order: 6, 262144 bytes, linear)
[    0.306626] UDP-Lite hash table entries: 8192 (order: 6, 262144 bytes, linear)
[    0.306722] NET: Registered PF_UNIX/PF_LOCAL protocol family
[    0.306731] NET: Registered PF_XDP protocol family
[    0.306736] pci 0000:01:00.0: ROM [mem 0xfffff800-0xffffffff pref]: can't claim; no compatible bridge window
[    0.306741] pci 0000:02:00.0: ROM [mem 0xffff0000-0xffffffff pref]: can't claim; no compatible bridge window
[    0.306744] pci 0000:03:00.0: ROM [mem 0xfffe0000-0xffffffff pref]: can't claim; no compatible bridge window
[    0.306758] pci 0000:00:1c.0: bridge window [mem 0x9fb00000-0x9fbfffff]: assigned
[    0.306762] pci 0000:01:00.0: ROM [mem 0x9fb00000-0x9fb007ff pref]: assigned
[    0.306765] pci 0000:00:1c.0: PCI bridge to [bus 01]
[    0.306770] pci 0000:00:1c.0:   bridge window [mem 0x9fb00000-0x9fbfffff]
[    0.306774] pci 0000:00:1c.0:   bridge window [mem 0xc0400000-0xc04fffff 64bit pref]
[    0.306780] pci 0000:02:00.0: ROM [mem 0xc0680000-0xc068ffff pref]: assigned
[    0.306782] pci 0000:00:1c.3: PCI bridge to [bus 02]
[    0.306786] pci 0000:00:1c.3:   bridge window [mem 0xc0600000-0xc06fffff]
[    0.306793] pci 0000:03:00.0: ROM [mem 0xc0540000-0xc055ffff pref]: assigned
[    0.306796] pci 0000:00:1c.4: PCI bridge to [bus 03]
[    0.306798] pci 0000:00:1c.4:   bridge window [io  0x3000-0x3fff]
[    0.306802] pci 0000:00:1c.4:   bridge window [mem 0xc0500000-0xc05fffff]
[    0.306806] pci 0000:00:1c.4:   bridge window [mem 0xa0000000-0xafffffff 64bit pref]
[    0.306812] pci_bus 0000:00: resource 4 [io  0x0000-0x0cf7 window]
[    0.306815] pci_bus 0000:00: resource 5 [io  0x0d00-0xffff window]
[    0.306817] pci_bus 0000:00: resource 6 [mem 0x000a0000-0x000fffff window]
[    0.306818] pci_bus 0000:00: resource 7 [mem 0x9fa00000-0xfeafffff window]
[    0.306821] pci_bus 0000:01: resource 1 [mem 0x9fb00000-0x9fbfffff]
[    0.306822] pci_bus 0000:01: resource 2 [mem 0xc0400000-0xc04fffff 64bit pref]
[    0.306825] pci_bus 0000:02: resource 1 [mem 0xc0600000-0xc06fffff]
[    0.306826] pci_bus 0000:03: resource 0 [io  0x3000-0x3fff]
[    0.306828] pci_bus 0000:03: resource 1 [mem 0xc0500000-0xc05fffff]
[    0.306830] pci_bus 0000:03: resource 2 [mem 0xa0000000-0xafffffff 64bit pref]
[    0.322461] pci 0000:00:1d.0: quirk_usb_early_handoff+0x0/0x190 took 11870 usecs
[    0.322518] PCI: CLS 64 bytes, default 64
[    0.322533] PCI-DMA: Using software bounce buffering for IO (SWIOTLB)
[    0.322535] software IO TLB: mapped [mem 0x000000008190b000-0x000000008590b000] (64MB)
[    0.322619] Trying to unpack rootfs image as initramfs...
[    0.326180] Initialise system trusted keyrings
[    0.326197] Key type blacklist registered
[    0.326263] workingset: timestamp_bits=36 max_order=22 bucket_order=0
[    0.326278] zbud: loaded
[    0.326663] squashfs: version 4.0 (2009/01/31) Phillip Lougher
[    0.326808] fuse: init (API version 7.39)
[    0.326990] integrity: Platform Keyring initialized
[    0.327000] integrity: Machine keyring initialized
[    0.355419] Key type asymmetric registered
[    0.355427] Asymmetric key parser 'x509' registered
[    0.355466] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 243)
[    0.355543] io scheduler mq-deadline registered
[    0.358732] pcieport 0000:00:1c.0: PME: Signaling with IRQ 40
[    0.358943] pcieport 0000:00:1c.3: PME: Signaling with IRQ 41
[    0.359137] pcieport 0000:00:1c.4: PME: Signaling with IRQ 42
[    0.359222] shpchp: Standard Hot Plug PCI Controller Driver version: 0.4
[    0.359866] ACPI: AC: AC Adapter [ACAD] (on-line)
[    0.359929] input: Lid Switch as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:01/PNP0C0D:00/input/input0
[    0.359951] ACPI: button: Lid Switch [LID0]
[    0.359984] input: Power Button as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:01/PNP0C0C:00/input/input1
[    0.360005] ACPI: button: Power Button [PWRB]
[    0.360038] input: Sleep Button as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:01/PNP0C0E:00/input/input2
[    0.360056] ACPI: button: Sleep Button [SLPB]
[    0.360100] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input3
[    0.360144] ACPI: button: Power Button [PWRF]
[    0.360703] Serial: 8250/16550 driver, 32 ports, IRQ sharing enabled
[    0.362394] ACPI: battery: Slot [BAT1] (battery absent)
[    0.363648] Linux agpgart interface v0.103
[    0.365562] loop: module loaded
[    0.365836] ACPI: bus type drm_connector registered
[    0.366121] tun: Universal TUN/TAP device driver, 1.6
[    0.366183] PPP generic driver version 2.4.2
[    0.366345] i8042: PNP: PS/2 Controller [PNP0303:KBC0,PNP0f13:MSS0] at 0x60,0x64 irq 1,12
[    0.366530] ehci-pci 0000:00:1d.0: EHCI Host Controller
[    0.366542] ehci-pci 0000:00:1d.0: new USB bus registered, assigned bus number 1
[    0.366562] ehci-pci 0000:00:1d.0: debug port 2
[    0.370514] ehci-pci 0000:00:1d.0: irq 23, io mem 0xc071c000
[    0.377373] ehci-pci 0000:00:1d.0: USB 2.0 started, EHCI 1.00
[    0.377495] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 6.08
[    0.377502] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    0.377506] usb usb1: Product: EHCI Host Controller
[    0.377509] usb usb1: Manufacturer: Linux 6.8.0-45-generic ehci_hcd
[    0.377513] usb usb1: SerialNumber: 0000:00:1d.0
[    0.377773] hub 1-0:1.0: USB hub found
[    0.377802] hub 1-0:1.0: 2 ports detected
[    0.386034] serio: i8042 KBD port at 0x60,0x64 irq 1
[    0.386048] serio: i8042 AUX port at 0x60,0x64 irq 12
[    0.386207] mousedev: PS/2 mouse device common for all mice
[    0.386481] rtc_cmos 00:01: RTC can wake from S4
[    0.386789] rtc_cmos 00:01: registered as rtc0
[    0.386826] rtc_cmos 00:01: setting system clock to 2024-10-15T08:16:57 UTC (1728980217)
[    0.386874] rtc_cmos 00:01: alarms up to one month, 242 bytes nvram, hpet irqs
[    0.386896] i2c_dev: i2c /dev entries driver
[    0.387194] device-mapper: core: CONFIG_IMA_DISABLE_HTABLE is disabled. Duplicate IMA measurements will not be recorded in the IMA log.
[    0.387230] device-mapper: uevent: version 1.0.3
[    0.387317] device-mapper: ioctl: 4.48.0-ioctl (2023-03-01) initialised: dm-devel@redhat.com
[    0.387369] platform eisa.0: Probing EISA bus 0
[    0.387380] platform eisa.0: EISA: Cannot allocate resource for mainboard
[    0.387383] platform eisa.0: Cannot allocate resource for EISA slot 1
[    0.387387] platform eisa.0: Cannot allocate resource for EISA slot 2
[    0.387390] platform eisa.0: Cannot allocate resource for EISA slot 3
[    0.387393] platform eisa.0: Cannot allocate resource for EISA slot 4
[    0.387396] platform eisa.0: Cannot allocate resource for EISA slot 5
[    0.387399] platform eisa.0: Cannot allocate resource for EISA slot 6
[    0.387403] platform eisa.0: Cannot allocate resource for EISA slot 7
[    0.387406] platform eisa.0: Cannot allocate resource for EISA slot 8
[    0.387409] platform eisa.0: EISA: Detected 0 cards
[    0.387486] intel_pstate: Intel P-state driver initializing
[    0.388164] ledtrig-cpu: registered to indicate activity on CPUs
[    0.388394] [drm] Initialized simpledrm 1.0.0 20200625 for simple-framebuffer.0 on minor 0
[    0.388856] fbcon: Deferring console take-over
[    0.388859] simple-framebuffer simple-framebuffer.0: [drm] fb0: simpledrmdrmfb frame buffer device
[    0.388932] drop_monitor: Initializing network drop monitor service
[    0.389056] NET: Registered PF_INET6 protocol family
[    0.399700] input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input4
[    0.617368] usb 1-1: new high-speed USB device number 2 using ehci-pci
[    0.745714] usb 1-1: New USB device found, idVendor=8087, idProduct=8000, bcdDevice= 0.04
[    0.745723] usb 1-1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    0.746168] hub 1-1:1.0: USB hub found
[    0.746209] hub 1-1:1.0: 8 ports detected
[    0.794783] Freeing initrd memory: 158512K
[    0.802109] Segment Routing with IPv6
[    0.802127] In-situ OAM (IOAM) with IPv6
[    0.802158] NET: Registered PF_PACKET protocol family
[    0.802223] Key type dns_resolver registered
[    0.802639] ENERGY_PERF_BIAS: Set to 'normal', was 'performance'
[    0.802697] mce: [Hardware Error]: Machine check events logged
[    0.802715] microcode: Current revision: 0x00000026
[    0.802716] microcode: Updated early from: 0x00000015
[    0.802821] IPI shorthand broadcast: enabled
[    0.804740] sched_clock: Marking stable (804002308, 352284)->(823340334, -18985742)
[    0.804932] registered taskstats version 1
[    0.805184] Loading compiled-in X.509 certificates
[    0.805911] Loaded X.509 cert 'Build time autogenerated kernel key: 7e025e0cbc510606ab90d1bfb5b71bc9263fcc8e'
[    0.806560] Loaded X.509 cert 'Canonical Ltd. Live Patch Signing: 14df34d1a87cf37625abec039ef2bf521249b969'
[    0.807167] Loaded X.509 cert 'Canonical Ltd. Kernel Module Signing: 88f752e560a1e0737e31163a466ad7b70a850c19'
[    0.807169] blacklist: Loading compiled-in revocation X.509 certificates
[    0.807191] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing: 61482aa2830d0ab2ad5af10b7250da9033ddcef0'
[    0.807207] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing (2017): 242ade75ac4a15e50d50c84b0d45ff3eae707a03'
[    0.807222] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing (ESM 2018): 365188c1d374d6b07c3c8f240f8ef722433d6a8b'
[    0.807236] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing (2019): c0746fd6c5da3ae827864651ad66ae47fe24b3e8'
[    0.807251] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing (2021 v1): a8d54bbb3825cfb94fa13c9f8a594a195c107b8d'
[    0.807269] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing (2021 v2): 4cf046892d6fd3c9a5b03f98d845f90851dc6a8c'
[    0.807285] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing (2021 v3): 100437bb6de6e469b581e61cd66bce3ef4ed53af'
[    0.807302] Loaded X.509 cert 'Canonical Ltd. Secure Boot Signing (Ubuntu Core 2019): c1d57b8f6b743f23ee41f4f7ee292f06eecadfb9'
[    0.811445] Key type .fscrypt registered
[    0.811447] Key type fscrypt-provisioning registered
[    0.818138] cryptd: max_cpu_qlen set to 1000
[    0.823059] AVX2 version of gcm_enc/dec engaged.
[    0.823106] AES CTR mode by8 optimization enabled
[    0.840227] Key type encrypted registered
[    0.840234] AppArmor: AppArmor sha256 policy hashing enabled
[    0.841704] integrity: Loading X.509 certificate: UEFI:db
[    0.841750] integrity: Loaded X.509 cert 'Acer: c4f0474ae6b5e67a509d99132f49a4ec13f7ac68'
[    0.841751] integrity: Loading X.509 certificate: UEFI:db
[    0.841775] integrity: Loaded X.509 cert 'Microsoft Windows Production PCA 2011: a92902398e16c49778cd90f99e4f9ae17c55af53'
[    0.841776] integrity: Loading X.509 certificate: UEFI:db
[    0.841810] integrity: Loaded X.509 cert 'Microsoft Corporation UEFI CA 2011: 13adbf4309bd82709c8cd54f316ed522988a1bd4'
[    0.841812] integrity: Loading X.509 certificate: UEFI:db
[    0.841814] integrity: Problem loading X.509 certificate -65
[    0.841815] integrity: Error adding keys to platform keyring UEFI:db
[    0.841816] integrity: Loading X.509 certificate: UEFI:db
[    0.841818] integrity: Problem loading X.509 certificate -65
[    0.841819] integrity: Error adding keys to platform keyring UEFI:db
[    0.845920] ima: No TPM chip found, activating TPM-bypass!
[    0.845926] Loading compiled-in module X.509 certificates
[    0.846605] Loaded X.509 cert 'Build time autogenerated kernel key: 7e025e0cbc510606ab90d1bfb5b71bc9263fcc8e'
[    0.846609] ima: Allocated hash algorithm: sha256
[    0.846620] ima: No architecture policies found
[    0.846638] evm: Initialising EVM extended attributes:
[    0.846639] evm: security.selinux
[    0.846640] evm: security.SMACK64
[    0.846641] evm: security.SMACK64EXEC
[    0.846642] evm: security.SMACK64TRANSMUTE
[    0.846643] evm: security.SMACK64MMAP
[    0.846644] evm: security.apparmor
[    0.846645] evm: security.ima
[    0.846645] evm: security.capability
[    0.846646] evm: HMAC attrs: 0x1
[    0.847086] PM:   Magic number: 12:717:270
[    0.851339] RAS: Correctable Errors collector initialized.
[    0.851441] clk: Disabling unused clocks
[    0.853155] Freeing unused decrypted memory: 2028K
[    0.853912] Freeing unused kernel image (initmem) memory: 4976K
[    0.853979] Write protecting the kernel read-only data: 36864k
[    0.854191] Freeing unused kernel image (rodata/data gap) memory: 24K
[    0.908002] x86/mm: Checked W+X mappings: passed, no W+X pages found.
[    0.908005] x86/mm: Checking user space page tables
[    0.959028] x86/mm: Checked W+X mappings: passed, no W+X pages found.
[    0.959035] Run /init as init process
[    0.959036]   with arguments:
[    0.959038]     /init
[    0.959039]     splash
[    0.959040]   with environment:
[    0.959041]     HOME=/
[    0.959042]     TERM=linux
[    0.959043]     BOOT_IMAGE=/vmlinuz-6.8.0-45-generic
[    1.168440] sdhci: Secure Digital Host Controller Interface driver
[    1.168447] sdhci: Copyright(c) Pierre Ossman
[    1.169138] xhci_hcd 0000:00:14.0: xHCI Host Controller
[    1.169153] xhci_hcd 0000:00:14.0: new USB bus registered, assigned bus number 2
[    1.170223] xhci_hcd 0000:00:14.0: hcc params 0x200077c1 hci version 0x100 quirks 0x000000000004b810
[    1.170503] xhci_hcd 0000:00:14.0: xHCI Host Controller
[    1.170511] xhci_hcd 0000:00:14.0: new USB bus registered, assigned bus number 3
[    1.170517] xhci_hcd 0000:00:14.0: Host supports USB 3.0 SuperSpeed
[    1.170590] usb usb2: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 6.08
[    1.170596] usb usb2: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    1.170599] usb usb2: Product: xHCI Host Controller
[    1.170602] usb usb2: Manufacturer: Linux 6.8.0-45-generic xhci-hcd
[    1.170604] usb usb2: SerialNumber: 0000:00:14.0
[    1.170915] hub 2-0:1.0: USB hub found
[    1.170935] hub 2-0:1.0: 9 ports detected
[    1.178203] ahci 0000:00:1f.2: version 3.0
[    1.178690] ahci 0000:00:1f.2: SSS flag set, parallel bus scan disabled
[    1.178770] ahci 0000:00:1f.2: AHCI 0001.0300 32 slots 4 ports 6 Gbps 0x3 impl SATA mode
[    1.178777] ahci 0000:00:1f.2: flags: 64bit ncq stag pm led clo only pio slum part deso sadm sds apst 
[    1.190623] sdhci-pci 0000:01:00.1: SDHCI controller found [14e4:16bc] (rev 1)
[    1.190924] tg3 0000:01:00.0 eth0: Tigon3 [partno(BCM57786) rev 57766001] (PCI Express) MAC address 20:1a:06:6e:fd:b3
[    1.190933] tg3 0000:01:00.0 eth0: attached PHY is 57765 (10/100/1000Base-T Ethernet) (WireSpeed[1], EEE[1])
[    1.190937] tg3 0000:01:00.0 eth0: RXcsums[1] LinkChgREG[0] MIirq[0] ASF[0] TSOcap[1]
[    1.190941] tg3 0000:01:00.0 eth0: dma_rwctrl[00000001] dma_mask[64-bit]
[    1.198904] mmc0: SDHCI controller on PCI [0000:01:00.1] using ADMA 64-bit
[    1.198990] scsi host0: ahci
[    1.201202] scsi host1: ahci
[    1.205609] amdkcl: loading out-of-tree module taints kernel.
[    1.205618] amdkcl: module verification failed: signature and/or required key missing - tainting kernel
[    1.210639] usb usb3: New USB device found, idVendor=1d6b, idProduct=0003, bcdDevice= 6.08
[    1.210649] usb usb3: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    1.210653] usb usb3: Product: xHCI Host Controller
[    1.210656] usb usb3: Manufacturer: Linux 6.8.0-45-generic xhci-hcd
[    1.210659] usb usb3: SerialNumber: 0000:00:14.0
[    1.211406] scsi host2: ahci
[    1.213918] scsi host3: ahci
[    1.214061] ata1: SATA max UDMA/133 abar m2048@0xc071b000 port 0xc071b100 irq 44 lpm-pol 3
[    1.214067] ata2: SATA max UDMA/133 abar m2048@0xc071b000 port 0xc071b180 irq 44 lpm-pol 3
[    1.214070] ata3: DUMMY
[    1.214072] ata4: DUMMY
[    1.231593] hub 3-0:1.0: USB hub found
[    1.231618] hub 3-0:1.0: 4 ports detected
[    1.271208] tg3 0000:01:00.0 enp1s0f0: renamed from eth0
[    1.359424] tsc: Refined TSC clocksource calibration: 2294.689 MHz
[    1.359436] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x21139c00f92, max_idle_ns: 440795293667 ns
[    1.359470] clocksource: Switched to clocksource tsc
[    1.443441] usb 2-1: new full-speed USB device number 2 using xhci_hcd
[    1.525804] ata1: SATA link up 6.0 Gbps (SStatus 133 SControl 300)
[    1.529232] ata1.00: supports DRM functions and may not be fully accessible
[    1.529239] ata1.00: ATA-11: Samsung SSD 870 QVO 1TB, SVQ02B6Q, max UDMA/133
[    1.529885] ata1.00: 1953525168 sectors, multi 1: LBA48 NCQ (depth 32), AA
[    1.535197] ata1.00: Features: Trust Dev-Sleep NCQ-sndrcv
[    1.535940] ata1.00: supports DRM functions and may not be fully accessible
[    1.541674] ata1.00: configured for UDMA/133
[    1.551816] ahci 0000:00:1f.2: port does not support device sleep
[    1.552242] scsi 0:0:0:0: Direct-Access     ATA      Samsung SSD 870  2B6Q PQ: 0 ANSI: 5
[    1.552785] sd 0:0:0:0: Attached scsi generic sg0 type 0
[    1.552801] ata1.00: Enabling discard_zeroes_data
[    1.552824] sd 0:0:0:0: [sda] 1953525168 512-byte logical blocks: (1.00 TB/932 GiB)
[    1.552842] sd 0:0:0:0: [sda] Write Protect is off
[    1.552847] sd 0:0:0:0: [sda] Mode Sense: 00 3a 00 00
[    1.552862] sd 0:0:0:0: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[    1.552892] sd 0:0:0:0: [sda] Preferred minimum I/O size 512 bytes
[    1.553395] ata1.00: Enabling discard_zeroes_data
[    1.555478]  sda: sda1 sda2 sda3
[    1.556847] sd 0:0:0:0: [sda] supports TCG Opal
[    1.556862] sd 0:0:0:0: [sda] Attached SCSI disk
[    1.861825] ata2: SATA link up 1.5 Gbps (SStatus 113 SControl 300)
[    1.864631] ata2.00: ATAPI: HL-DT-ST DVDRAM GU71N, 1.01, max UDMA/133
[    1.871840] ata2.00: configured for UDMA/133
[    1.882327] scsi 1:0:0:0: CD-ROM            HL-DT-ST DVDRAM GU71N     1.01 PQ: 0 ANSI: 5
[    1.923471] sr 1:0:0:0: [sr0] scsi3-mmc drive: 24x/24x writer dvd-ram cd/rw xa/form2 cdda tray
[    1.923487] cdrom: Uniform CD-ROM driver Revision: 3.20
[    1.941485] sr 1:0:0:0: Attached scsi CD-ROM sr0
[    1.941748] sr 1:0:0:0: Attached scsi generic sg1 type 5
[    2.164675] usb 2-1: New USB device found, idVendor=1b3f, idProduct=2008, bcdDevice= 1.00
[    2.164684] usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[    2.164688] usb 2-1: Product: USB Audio Device
[    2.164691] usb 2-1: Manufacturer: GeneralPlus
[    2.292232] usb 2-5: new full-speed USB device number 3 using xhci_hcd
[    2.401157] psmouse serio1: synaptics: queried max coordinates: x [..5708], y [..4812]
[    2.424791] usb 2-5: New USB device found, idVendor=04ca, idProduct=300b, bcdDevice= 0.01
[    2.424796] usb 2-5: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    2.463211] psmouse serio1: synaptics: queried min coordinates: x [1228..], y [1060..]
[    2.540379] usb 2-8: new high-speed USB device number 4 using xhci_hcd
[    2.579479] psmouse serio1: synaptics: Touchpad model: 1, fw: 7.5, id: 0x1e0b1, caps: 0xf00173/0x240000/0xa2400/0x0, board id: 2682, fw id: 1393679
[    2.652258] input: SynPS/2 Synaptics TouchPad as /devices/platform/i8042/serio1/input/input6
[    2.729660] usb 2-8: New USB device found, idVendor=04f2, idProduct=b3d6, bcdDevice=39.07
[    2.729667] usb 2-8: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[    2.729669] usb 2-8: Product: HD WebCam
[    2.729671] usb 2-8: Manufacturer: SunplusIT INC.
[    5.784532] hid: raw HID events driver (C) Jiri Kosina
[    5.786917] [drm] amdgpu kernel modesetting enabled.
[    5.786921] [drm] amdgpu version: 6.8.5
[    5.786923] [drm] OS DRM version: 6.8.0
[    5.786945] amdgpu: vga_switcheroo: detected switching method \_SB_.PCI0.GFX0.ATPX handle
[    5.787091] amdgpu: ATPX version 1, functions 0x00000033
[    5.787454] amdgpu: Virtual CRAT table created for CPU
[    5.787483] amdgpu: Topology: Add CPU node
[    5.789719] usbcore: registered new interface driver usbhid
[    5.789725] usbhid: USB HID core driver
[    5.792140] amdgpu 0000:03:00.0: enabling device (0000 -> 0003)
[    5.792245] [drm] initializing kernel modesetting (OLAND 0x1002:0x6600 0x1025:0x0776 0x00).
[    5.792333] [drm] register mmio base: 0xC0500000
[    5.792336] [drm] register mmio size: 262144
[    5.792418] [drm] add ip block number 0 <si_common>
[    5.792422] [drm] add ip block number 1 <gmc_v6_0>
[    5.792424] [drm] add ip block number 2 <si_ih>
[    5.792426] [drm] add ip block number 3 <gfx_v6_0>
[    5.792428] [drm] add ip block number 4 <si_dma>
[    5.792431] [drm] add ip block number 5 <si_dpm>
[    5.792433] [drm] add ip block number 6 <dce_v6_0>
[    5.792435] [drm] add ip block number 7 <uvd_v3_1>
[    5.793654] input: GeneralPlus USB Audio Device as /devices/pci0000:00/0000:00:14.0/usb2/2-1/2-1:1.3/0003:1B3F:2008.0001/input/input7
[    5.807072] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from ATRM
[    5.807078] amdgpu: ATOM BIOS: BR44905.001
[    5.807090] kfd kfd: amdgpu: OLAND  not supported in kfd
[    5.807093] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[    5.807096] amdgpu 0000:03:00.0: amdgpu: PCIE atomic ops is not supported
[    5.807100] [drm] GPU posting now...
[    5.812032] [drm] PCIE gen 2 link speeds already enabled
[    5.812039] [drm] vm size is 64 GB, 2 levels, block size is 10-bit, fragment size is 9-bit
[    5.812224] amdgpu 0000:03:00.0: amdgpu: VRAM: 2048M 0x000000F400000000 - 0x000000F47FFFFFFF (2048M used)
[    5.812228] amdgpu 0000:03:00.0: amdgpu: GART: 1024M 0x000000FF00000000 - 0x000000FF3FFFFFFF
[    5.812237] [drm] Detected VRAM RAM=2048M, BAR=256M
[    5.812239] [drm] RAM width 128bits DDR3
[    5.812325] [drm] amdgpu: 2048M of VRAM memory ready
[    5.812328] [drm] amdgpu: 5920M of GTT memory ready.
[    5.812346] [drm] GART: num cpu pages 262144, num gpu pages 262144
[    5.812975] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 1024M enabled (table at 0x000000F400000000).
[    5.814014] [drm] Internal thermal controller without fan control
[    5.814029] [drm] amdgpu: dpm initialized
[    5.814046] [drm] AMDGPU Display Connectors
[    5.815003] [drm] Found UVD firmware Version: 64.0 Family ID: 13
[    5.845567] hid-generic 0003:1B3F:2008.0001: input,hidraw0: USB HID v2.01 Device [GeneralPlus USB Audio Device] on usb-0000:00:14.0-1/input3
[    6.409185] [drm] UVD initialized successfully.
[    6.409228] amdgpu 0000:03:00.0: amdgpu: SE 1, SH per SE 1, CU per SH 6, active_cu_number 6
[    6.874359] amdgpu 0000:03:00.0: amdgpu: runtime pm is manually disabled
[    6.874362] amdgpu 0000:03:00.0: amdgpu: Runtime PM not available
[    6.874633] [drm] Initialized amdgpu 3.58.0 20150101 for 0000:03:00.0 on minor 1
[   20.844831] EXT4-fs (dm-1): mounted filesystem e0724338-ed31-40db-82b1-0339ede9c7bd ro with ordered data mode. Quota mode: none.
[   21.076789] systemd[1]: Inserted module 'autofs4'
[   21.186141] systemd[1]: systemd 255.4-1ubuntu8.4 running in system mode (+PAM +AUDIT +SELINUX +APPARMOR +IMA +SMACK +SECCOMP +GCRYPT -GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 -PWQUALITY +P11KIT +QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD -BPF_FRAMEWORK -XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified)
[   21.186159] systemd[1]: Detected architecture x86-64.
[   21.189190] systemd[1]: Hostname set to <Done>.
[   21.319508] systemd[1]: Configuration file /run/systemd/system/netplan-ovs-cleanup.service is marked world-inaccessible. This has no effect as configuration data is accessible via APIs without restrictions. Proceeding anyway.
[   21.482921] systemd[1]: Queued start job for default target graphical.target.
[   21.499690] systemd[1]: Created slice system-modprobe.slice - Slice /system/modprobe.
[   21.500714] systemd[1]: Created slice system-systemd\x2dcryptsetup.slice - Encrypted Volume Units Service Slice.
[   21.501269] systemd[1]: Created slice system-systemd\x2dfsck.slice - Slice /system/systemd-fsck.
[   21.501672] systemd[1]: Created slice user.slice - User and Session Slice.
[   21.501759] systemd[1]: Started systemd-ask-password-wall.path - Forward Password Requests to Wall Directory Watch.
[   21.501980] systemd[1]: Set up automount proc-sys-fs-binfmt_misc.automount - Arbitrary Executable File Formats File System Automount Point.
[   21.502008] systemd[1]: Expecting device dev-disk-by\x2duuid-067fc0b0\x2db8ea\x2d41e8\x2d8634\x2d812a10fe4eda.device - /dev/disk/by-uuid/067fc0b0-b8ea-41e8-8634-812a10fe4eda...
[   21.502015] systemd[1]: Expecting device dev-disk-by\x2duuid-DD9E\x2d8907.device - /dev/disk/by-uuid/DD9E-8907...
[   21.502022] systemd[1]: Expecting device dev-disk-by\x2duuid-dcbf6737\x2d6068\x2d4bd3\x2db447\x2d074e1b79ba3d.device - /dev/disk/by-uuid/dcbf6737-6068-4bd3-b447-074e1b79ba3d...
[   21.502049] systemd[1]: Reached target integritysetup.target - Local Integrity Protected Volumes.
[   21.502085] systemd[1]: Reached target remote-fs.target - Remote File Systems.
[   21.502096] systemd[1]: Reached target slices.target - Slice Units.
[   21.502113] systemd[1]: Reached target snapd.mounts-pre.target - Mounting snaps.
[   21.502138] systemd[1]: Reached target veritysetup.target - Local Verity Protected Volumes.
[   21.502246] systemd[1]: Listening on dm-event.socket - Device-mapper event daemon FIFOs.
[   21.502413] systemd[1]: Listening on lvm2-lvmpolld.socket - LVM2 poll daemon socket.
[   21.502631] systemd[1]: Listening on syslog.socket - Syslog Socket.
[   21.502757] systemd[1]: Listening on systemd-fsckd.socket - fsck to fsckd communication Socket.
[   21.502850] systemd[1]: Listening on systemd-initctl.socket - initctl Compatibility Named Pipe.
[   21.502994] systemd[1]: Listening on systemd-journald-dev-log.socket - Journal Socket (/dev/log).
[   21.503163] systemd[1]: Listening on systemd-journald.socket - Journal Socket.
[   21.503441] systemd[1]: Listening on systemd-oomd.socket - Userspace Out-Of-Memory (OOM) Killer Socket.
[   21.503485] systemd[1]: systemd-pcrextend.socket - TPM2 PCR Extension (Varlink) was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[   21.504031] systemd[1]: Listening on systemd-udevd-control.socket - udev Control Socket.
[   21.504178] systemd[1]: Listening on systemd-udevd-kernel.socket - udev Kernel Socket.
[   21.505727] systemd[1]: Mounting dev-hugepages.mount - Huge Pages File System...
[   21.506758] systemd[1]: Mounting dev-mqueue.mount - POSIX Message Queue File System...
[   21.508655] systemd[1]: Mounting sys-kernel-debug.mount - Kernel Debug File System...
[   21.512516] systemd[1]: Mounting sys-kernel-tracing.mount - Kernel Trace File System...
[   21.518753] systemd[1]: Starting systemd-journald.service - Journal Service...
[   21.519016] systemd[1]: Finished blk-availability.service - Availability of block devices.
[   21.521248] systemd[1]: Starting keyboard-setup.service - Set the console keyboard layout...
[   21.522792] systemd[1]: Starting kmod-static-nodes.service - Create List of Static Device Nodes...
[   21.527633] systemd[1]: Starting lvm2-monitor.service - Monitoring of LVM2 mirrors, snapshots etc. using dmeventd or progress polling...
[   21.532617] systemd[1]: Starting modprobe@configfs.service - Load Kernel Module configfs...
[   21.534478] systemd[1]: Starting modprobe@dm_mod.service - Load Kernel Module dm_mod...
[   21.537436] systemd[1]: Starting modprobe@drm.service - Load Kernel Module drm...
[   21.542162] systemd[1]: Starting modprobe@efi_pstore.service - Load Kernel Module efi_pstore...
[   21.547859] systemd[1]: Starting modprobe@fuse.service - Load Kernel Module fuse...
[   21.553132] systemd[1]: Starting modprobe@loop.service - Load Kernel Module loop...
[   21.553455] systemd[1]: systemd-fsck-root.service - File System Check on Root Device was skipped because of an unmet condition check (ConditionPathExists=!/run/initramfs/fsck-root).
[   21.555287] pstore: Using crash dump compression: deflate
[   21.561710] systemd[1]: Starting systemd-modules-load.service - Load Kernel Modules...
[   21.561772] systemd[1]: systemd-pcrmachine.service - TPM2 PCR Machine ID Measurement was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[   21.563725] systemd-journald[463]: Collecting audit messages is disabled.
[   21.568087] systemd[1]: Starting systemd-remount-fs.service - Remount Root and Kernel File Systems...
[   21.568193] systemd[1]: systemd-tpm2-setup-early.service - TPM2 SRK Setup (Early) was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[   21.573925] systemd[1]: Starting systemd-udev-trigger.service - Coldplug All udev Devices...
[   21.577651] systemd[1]: Mounted dev-hugepages.mount - Huge Pages File System.
[   21.577983] systemd[1]: Mounted dev-mqueue.mount - POSIX Message Queue File System.
[   21.578290] systemd[1]: Mounted sys-kernel-debug.mount - Kernel Debug File System.
[   21.578634] systemd[1]: Mounted sys-kernel-tracing.mount - Kernel Trace File System.
[   21.579258] systemd[1]: Finished kmod-static-nodes.service - Create List of Static Device Nodes.
[   21.579973] systemd[1]: modprobe@configfs.service: Deactivated successfully.
[   21.580315] systemd[1]: Finished modprobe@configfs.service - Load Kernel Module configfs.
[   21.580987] systemd[1]: modprobe@dm_mod.service: Deactivated successfully.
[   21.581346] systemd[1]: Finished modprobe@dm_mod.service - Load Kernel Module dm_mod.
[   21.582059] systemd[1]: modprobe@drm.service: Deactivated successfully.
[   21.582311] systemd[1]: Finished modprobe@drm.service - Load Kernel Module drm.
[   21.584060] systemd[1]: modprobe@fuse.service: Deactivated successfully.
[   21.584456] systemd[1]: Finished modprobe@fuse.service - Load Kernel Module fuse.
[   21.594708] pstore: Registered efi_pstore as persistent store backend
[   21.597698] systemd[1]: Mounting sys-fs-fuse-connections.mount - FUSE Control File System...
[   21.601683] systemd[1]: Mounting sys-kernel-config.mount - Kernel Configuration File System...
[   21.604643] systemd[1]: Starting systemd-tmpfiles-setup-dev-early.service - Create Static Device Nodes in /dev gracefully...
[   21.605342] systemd[1]: modprobe@efi_pstore.service: Deactivated successfully.
[   21.606738] systemd[1]: Finished modprobe@efi_pstore.service - Load Kernel Module efi_pstore.
[   21.607312] systemd[1]: modprobe@loop.service: Deactivated successfully.
[   21.607588] systemd[1]: Finished modprobe@loop.service - Load Kernel Module loop.
[   21.607891] systemd[1]: systemd-repart.service - Repartition Root Disk was skipped because no trigger condition checks were met.
[   21.617529] systemd[1]: Mounted sys-fs-fuse-connections.mount - FUSE Control File System.
[   21.617747] systemd[1]: Mounted sys-kernel-config.mount - Kernel Configuration File System.
[   21.625116] lp: driver loaded but no devices found
[   21.632921] ppdev: user-space parallel port driver
[   21.632996] EXT4-fs (dm-1): re-mounted e0724338-ed31-40db-82b1-0339ede9c7bd r/w. Quota mode: none.
[   21.636386] systemd[1]: Finished systemd-remount-fs.service - Remount Root and Kernel File Systems.
[   21.650605] systemd[1]: Activating swap swap.img.swap - /swap.img...
[   21.651673] systemd[1]: systemd-hwdb-update.service - Rebuild Hardware Database was skipped because of an unmet condition check (ConditionNeedsUpdate=/etc).
[   21.651765] systemd[1]: systemd-pstore.service - Platform Persistent Storage Archival was skipped because of an unmet condition check (ConditionDirectoryNotEmpty=/sys/fs/pstore).
[   21.655088] systemd[1]: Starting systemd-random-seed.service - Load/Save OS Random Seed...
[   21.655135] systemd[1]: systemd-tpm2-setup.service - TPM2 SRK Setup was skipped because of an unmet condition check (ConditionSecurity=measured-uki).
[   21.659202] systemd[1]: Finished lvm2-monitor.service - Monitoring of LVM2 mirrors, snapshots etc. using dmeventd or progress polling.
[   21.664531] Adding 4194300k swap on /swap.img.  Priority:-2 extents:20 across:692453376k SS
[   21.664646] systemd[1]: Activated swap swap.img.swap - /swap.img.
[   21.665483] systemd[1]: Reached target swap.target - Swaps.
[   21.667412] systemd[1]: Finished systemd-tmpfiles-setup-dev-early.service - Create Static Device Nodes in /dev gracefully.
[   21.667700] systemd[1]: systemd-sysusers.service - Create System Users was skipped because no trigger condition checks were met.
[   21.672785] systemd[1]: Starting systemd-tmpfiles-setup-dev.service - Create Static Device Nodes in /dev...
[   21.679077] systemd[1]: Finished systemd-modules-load.service - Load Kernel Modules.
[   21.682762] systemd[1]: Starting systemd-sysctl.service - Apply Kernel Variables...
[   21.696820] systemd[1]: Finished systemd-random-seed.service - Load/Save OS Random Seed.
[   21.702161] systemd[1]: Finished systemd-tmpfiles-setup-dev.service - Create Static Device Nodes in /dev.
[   21.713771] systemd[1]: Starting systemd-udevd.service - Rule-based Manager for Device Events and Files...
[   21.714715] systemd[1]: Finished keyboard-setup.service - Set the console keyboard layout.
[   21.714902] systemd[1]: Reached target local-fs-pre.target - Preparation for Local File Systems.
[   21.719114] systemd[1]: Mounting snap-audacity-1051.mount - Mount unit for audacity, revision 1051...
[   21.736585] systemd[1]: Mounting snap-bare-5.mount - Mount unit for bare, revision 5...
[   21.743842] systemd[1]: Mounting snap-code-171.mount - Mount unit for code, revision 171...
[   21.747135] loop0: detected capacity change from 0 to 510112
[   21.747970] systemd[1]: Mounting snap-code-172.mount - Mount unit for code, revision 172...
[   21.749040] loop1: detected capacity change from 0 to 8
[   21.753513] systemd[1]: Mounting snap-core-17200.mount - Mount unit for core, revision 17200...
[   21.760512] systemd[1]: Mounting snap-core20-2379.mount - Mount unit for core20, revision 2379...
[   21.761914] loop2: detected capacity change from 0 to 641200
[   21.763089] loop3: detected capacity change from 0 to 213384
[   21.765765] systemd[1]: Mounting snap-core22-1612.mount - Mount unit for core22, revision 1612...
[   21.769538] systemd[1]: Mounting snap-core22-1621.mount - Mount unit for core22, revision 1621...
[   21.773829] loop4: detected capacity change from 0 to 641200
[   21.774520] systemd[1]: Mounting snap-core24-490.mount - Mount unit for core24, revision 490...
[   21.777131] systemd[1]: Mounting snap-dnslookup-205.mount - Mount unit for dnslookup, revision 205...
[   21.780501] systemd[1]: Mounting snap-eclipse-101.mount - Mount unit for eclipse, revision 101...
[   21.781328] loop5: detected capacity change from 0 to 152112
[   21.784011] loop6: detected capacity change from 0 to 152056
[   21.785550] loop7: detected capacity change from 0 to 131016
[   21.785885] systemd[1]: Mounting snap-firefox-5014.mount - Mount unit for firefox, revision 5014...
[   21.789510] systemd[1]: Mounting snap-firefox-5091.mount - Mount unit for firefox, revision 5091...
[   21.794558] systemd[1]: Mounting snap-firmware\x2dupdater-127.mount - Mount unit for firmware-updater, revision 127...
[   21.797003] loop8: detected capacity change from 0 to 135512
[   21.797806] systemd[1]: Mounting snap-gaming\x2dgraphics\x2dcore22-166.mount - Mount unit for gaming-graphics-core22, revision 166...
[   21.800692] systemd[1]: Mounting snap-gaming\x2dgraphics\x2dcore22-184.mount - Mount unit for gaming-graphics-core22, revision 184...
[   21.803224] loop9: detected capacity change from 0 to 556304
[   21.804807] systemd[1]: Mounting snap-gnome\x2d42\x2d2204-176.mount - Mount unit for gnome-42-2204, revision 176...
[   21.805860] loop10: detected capacity change from 0 to 11104
[   21.808538] systemd[1]: Mounting snap-gnome\x2d46\x2d2404-48.mount - Mount unit for gnome-46-2404, revision 48...
[   21.811635] loop11: detected capacity change from 0 to 21952
[   21.812955] systemd[1]: Mounting snap-gtk\x2dcommon\x2dthemes-1535.mount - Mount unit for gtk-common-themes, revision 1535...
[   21.816202] systemd[1]: Mounting snap-mesa\x2d2404-143.mount - Mount unit for mesa-2404, revision 143...
[   21.822554] systemd[1]: Mounting snap-netbeans-111.mount - Mount unit for netbeans, revision 111...
[   21.825715] systemd[1]: Mounting snap-snap\x2dstore-1173.mount - Mount unit for snap-store, revision 1173...
[   21.827940] systemd[1]: Mounting snap-snap\x2dstore-1218.mount - Mount unit for snap-store, revision 1218...
[   21.829008] loop13: detected capacity change from 0 to 557016
[   21.833117] loop12: detected capacity change from 0 to 431592
[   21.833206] systemd[1]: Mounting snap-snapd-21759.mount - Mount unit for snapd, revision 21759...
[   21.837531] systemd[1]: Mounting snap-snapd-22991.mount - Mount unit for snapd, revision 22991...
[   21.843536] systemd[1]: Mounting snap-snapd\x2ddesktop\x2dintegration-247.mount - Mount unit for snapd-desktop-integration, revision 247...
[   21.848187] loop18: detected capacity change from 0 to 832024
[   21.848574] systemd[1]: Mounting snap-snapd\x2ddesktop\x2dintegration-253.mount - Mount unit for snapd-desktop-integration, revision 253...
[   21.850920] loop16: detected capacity change from 0 to 703344
[   21.850975] loop14: detected capacity change from 0 to 395216
[   21.854180] loop15: detected capacity change from 0 to 1022416
[   21.861692] systemd[1]: Mounting snap-steam-200.mount - Mount unit for steam, revision 200...
[   21.865299] loop21: detected capacity change from 0 to 187776
[   21.866034] loop20: detected capacity change from 0 to 90392
[   21.866590] loop17: detected capacity change from 0 to 1034424
[   21.870023] loop19: detected capacity change from 0 to 433128
[   21.873098] loop22: detected capacity change from 0 to 21584
[   21.875442] loop24: detected capacity change from 0 to 79520
[   21.875517] systemd[1]: Mounting snap-transmission-100.mount - Mount unit for transmission, revision 100...
[   21.875982] loop23: detected capacity change from 0 to 1128
[   21.883548] systemd[1]: Mounting snap-whois\x2dsnap-1.mount - Mount unit for whois-snap, revision 1...
[   21.887705] loop27: detected capacity change from 0 to 411536
[   21.888850] loop25: detected capacity change from 0 to 21848
[   21.889589] loop26: detected capacity change from 0 to 1136
[   21.890929] loop28: detected capacity change from 0 to 6224
[   21.896150] loop29: detected capacity change from 0 to 184
[   21.917198] systemd[1]: Started systemd-journald.service - Journal Service.
[   21.998513] systemd-journald[463]: Received client request to flush runtime journal.
[   22.030690] systemd-journald[463]: /var/log/journal/343a01cb50af40aa932f9824ef25a9b8/system.journal: Journal file uses a different sequence number ID, rotating.
[   22.030702] systemd-journald[463]: Rotating system journal.
[   22.618310] EXT4-fs (sda2): mounted filesystem 067fc0b0-b8ea-41e8-8634-812a10fe4eda r/w with ordered data mode. Quota mode: none.
[   22.855308] Bluetooth: Core ver 2.22
[   22.855461] NET: Registered PF_BLUETOOTH protocol family
[   22.855465] Bluetooth: HCI device and connection manager initialized
[   22.855475] Bluetooth: HCI socket layer initialized
[   22.855479] Bluetooth: L2CAP socket layer initialized
[   22.855491] Bluetooth: SCO socket layer initialized
[   22.958332] audit: type=1400 audit(1728980240.069:2): apparmor="STATUS" operation="profile_load" profile="unconfined" name="Discord" pid=761 comm="apparmor_parser"
[   22.958705] audit: type=1400 audit(1728980240.070:3): apparmor="STATUS" operation="profile_load" profile="unconfined" name=4D6F6E676F444220436F6D70617373 pid=762 comm="apparmor_parser"
[   22.958712] audit: type=1400 audit(1728980240.070:4): apparmor="STATUS" operation="profile_load" profile="unconfined" name="QtWebEngineProcess" pid=763 comm="apparmor_parser"
[   22.959116] audit: type=1400 audit(1728980240.070:5): apparmor="STATUS" operation="profile_load" profile="unconfined" name="1password" pid=760 comm="apparmor_parser"
[   22.963087] audit: type=1400 audit(1728980240.074:6): apparmor="STATUS" operation="profile_load" profile="unconfined" name="brave" pid=766 comm="apparmor_parser"
[   22.963279] audit: type=1400 audit(1728980240.074:7): apparmor="STATUS" operation="profile_load" profile="unconfined" name="busybox" pid=768 comm="apparmor_parser"
[   22.966519] audit: type=1400 audit(1728980240.078:8): apparmor="STATUS" operation="profile_load" profile="unconfined" name="balena-etcher" pid=765 comm="apparmor_parser"
[   22.967964] audit: type=1400 audit(1728980240.079:9): apparmor="STATUS" operation="profile_load" profile="unconfined" name="buildah" pid=767 comm="apparmor_parser"
[   22.970714] audit: type=1400 audit(1728980240.082:10): apparmor="STATUS" operation="profile_load" profile="unconfined" name="cam" pid=769 comm="apparmor_parser"
[   22.972718] audit: type=1400 audit(1728980240.084:11): apparmor="STATUS" operation="profile_load" profile="unconfined" name="chrome" pid=772 comm="apparmor_parser"
[   23.673288] mc: Linux media interface: v0.10
[   23.675764] i801_smbus 0000:00:1f.3: SPD Write Disable is set
[   23.675795] i801_smbus 0000:00:1f.3: SMBus using PCI interrupt
[   23.680009] i2c i2c-8: 2/2 memory slots populated (from DMI)
[   23.680333] i2c i2c-8: Successfully instantiated SPD at 0x50
[   23.680338] cfg80211: Loading compiled-in X.509 certificates for regulatory database
[   23.685239] Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
[   23.685653] Loaded X.509 cert 'wens: 61c038651aabdcf94bd0ac7ff06c7248db18c600'
[   23.712440] usbcore: registered new interface driver btusb
[   23.713609] acer_wmi: Acer Laptop ACPI-WMI Extras
[   23.713649] acer_wmi: Function bitmap for Communication Button: 0x801
[   23.722503] input: Acer WMI hotkeys as /devices/virtual/input/input8
[   23.729335] RAPL PMU: API unit is 2^-32 Joules, 4 fixed counters, 655360 ms ovfl timer
[   23.729343] RAPL PMU: hw unit of domain pp0-core 2^-14 Joules
[   23.729345] RAPL PMU: hw unit of domain package 2^-14 Joules
[   23.729348] RAPL PMU: hw unit of domain dram 2^-14 Joules
[   23.729350] RAPL PMU: hw unit of domain pp1-gpu 2^-14 Joules
[   23.737480] videodev: Linux video capture interface: v2.00
[   23.754228] usb 2-5: USB disconnect, device number 3
[   23.755437] usbcore: registered new interface driver ath3k
[   23.786598] i915 0000:00:02.0: vgaarb: deactivate vga console
[   23.814342] i915 0000:00:02.0: vgaarb: VGA decodes changed: olddecodes=io+mem,decodes=io+mem:owns=io+mem
[   24.011385] usb 2-5: new full-speed USB device number 5 using xhci_hcd
[   24.027874] at24 8-0050: supply vcc not found, using dummy regulator
[   24.029980] at24 8-0050: 256 byte spd EEPROM, read-only
[   24.071840] [drm] Initialized i915 1.6.0 20230929 for 0000:00:02.0 on minor 2
[   24.106400] ACPI: video: [Firmware Bug]: ACPI(PEGP) defines _DOD but not _DOS
[   24.109836] ACPI: video: Video Device [PEGP] (multi-head: yes  rom: no  post: no)
[   24.109857] ACPI BIOS Error (bug): Could not resolve symbol [\_SB.PCI0.GFX0.DD02._BCL], AE_NOT_FOUND (20230628/psargs-330)

[   24.109877] No Local Variables are initialized for Method [_BCL]

[   24.109882] No Arguments are initialized for method [_BCL]

[   24.109886] ACPI Error: Aborting method \_SB.PCI0.RP05.PEGP.DD02._BCL due to previous error (AE_NOT_FOUND) (20230628/psparse-529)
[   24.110031] input: Video Bus as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:38/LNXVIDEO:00/input/input9
[   24.111966] usb 2-8: Found UVC 1.00 device HD WebCam (04f2:b3d6)
[   24.115301] ACPI: video: Video Device [GFX0] (multi-head: yes  rom: no  post: no)
[   24.116404] input: Video Bus as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/LNXVIDEO:01/input/input10
[   24.124444] i915 display info: display version: 7
[   24.124453] i915 display info: cursor_needs_physical: no
[   24.124456] i915 display info: has_cdclk_crawl: no
[   24.124459] i915 display info: has_cdclk_squash: no
[   24.124461] i915 display info: has_ddi: yes
[   24.124464] i915 display info: has_dp_mst: yes
[   24.124466] i915 display info: has_dsb: no
[   24.124469] i915 display info: has_fpga_dbg: yes
[   24.124471] i915 display info: has_gmch: no
[   24.124473] i915 display info: has_hotplug: yes
[   24.124476] i915 display info: has_hti: no
[   24.124478] i915 display info: has_ipc: no
[   24.124480] i915 display info: has_overlay: no
[   24.124482] i915 display info: has_psr: yes
[   24.124484] i915 display info: has_psr_hw_tracking: yes
[   24.124487] i915 display info: overlay_needs_physical: no
[   24.124489] i915 display info: supports_tv: no
[   24.124491] i915 display info: has_hdcp: no
[   24.124494] i915 display info: has_dmc: no
[   24.124496] i915 display info: has_dsc: no
[   24.124757] vga_switcheroo: enabled
[   24.212382] snd_hda_codec_realtek hdaudioC0D0: autoconfig for ALC282: line_outs=1 (0x14/0x0/0x0/0x0/0x0) type:speaker
[   24.212394] snd_hda_codec_realtek hdaudioC0D0:    speaker_outs=0 (0x0/0x0/0x0/0x0/0x0)
[   24.212399] snd_hda_codec_realtek hdaudioC0D0:    hp_outs=1 (0x21/0x0/0x0/0x0/0x0)
[   24.212404] snd_hda_codec_realtek hdaudioC0D0:    mono: mono_out=0x0
[   24.212407] snd_hda_codec_realtek hdaudioC0D0:    inputs:
[   24.212410] snd_hda_codec_realtek hdaudioC0D0:      Internal Mic=0x1b
[   24.212413] snd_hda_codec_realtek hdaudioC0D0:      Mic=0x19
[   24.217418] snd_hda_intel 0000:00:03.0: bound 0000:00:02.0 (ops i915_audio_component_bind_ops [i915])
[   24.252399] usbcore: registered new interface driver uvcvideo
[   24.261418] fbcon: i915drmfb (fb0) is primary device
[   24.261425] fbcon: Deferring console take-over
[   24.261431] i915 0000:00:02.0: [drm] fb0: i915drmfb frame buffer device
[   24.268181] usbcore: registered new interface driver snd-usb-audio
[   24.274229] Creating 1 MTD partitions on "intel-spi":
[   24.274239] 0x000000000000-0x000000800000 : "BIOS"
[   24.289475] input: HDA Intel HDMI HDMI/DP,pcm=3 as /devices/pci0000:00/0000:00:03.0/sound/card2/input13
[   24.292575] input: HDA Intel HDMI HDMI/DP,pcm=7 as /devices/pci0000:00/0000:00:03.0/sound/card2/input14
[   24.297133] input: HDA Intel PCH Mic as /devices/pci0000:00/0000:00:1b.0/sound/card0/input11
[   24.297270] input: HDA Intel PCH Headphone as /devices/pci0000:00/0000:00:1b.0/sound/card0/input12
[   24.303015] ath: phy0: WB335 1-ANT card detected
[   24.303282] input: HDA Intel HDMI HDMI/DP,pcm=8 as /devices/pci0000:00/0000:00:03.0/sound/card2/input15
[   24.310360] ath: phy0: Enable LNA combining
[   24.311596] ath: phy0: ASPM enabled: 0x42
[   24.311606] ath: EEPROM regdomain: 0x65
[   24.311609] ath: EEPROM indicates we should expect a direct regpair map
[   24.311613] ath: Country alpha2 being used: 00
[   24.311616] ath: Regpair used: 0x65
[   24.314282] ieee80211 phy0: Selected rate control algorithm 'minstrel_ht'
[   24.379239] ieee80211 phy0: Atheros AR9565 Rev:1 mem=0x00000000b3d54df8, irq=19
[   24.380894] intel_rapl_common: Found RAPL domain package
[   24.380900] intel_rapl_common: Found RAPL domain core
[   24.380902] intel_rapl_common: Found RAPL domain uncore
[   24.380904] intel_rapl_common: Found RAPL domain dram
[   24.380920] intel_rapl_common: package-0:package:long_term locked by BIOS
[   24.380924] intel_rapl_common: package-0:package:short_term locked by BIOS
[   24.426214] ath9k 0000:02:00.0 wlp2s0: renamed from wlan0
[   25.282525] loop30: detected capacity change from 0 to 8
[   25.361383] NET: Registered PF_QIPCRTR protocol family
[   27.582720] wlp2s0: 80 MHz not supported, disabling VHT
[   27.594791] wlp2s0: authenticate with 50:ff:20:2d:79:16 (local address=a4:db:30:91:b5:31)
[   27.594798] wlp2s0: send auth to 50:ff:20:2d:79:16 (try 1/3)
[   27.596801] wlp2s0: authenticated
[   27.598420] wlp2s0: associate with 50:ff:20:2d:79:16 (try 1/3)
[   27.604405] wlp2s0: RX AssocResp from 50:ff:20:2d:79:16 (capab=0x1c11 status=0 aid=3)
[   27.604544] wlp2s0: associated
[   27.605280] ath: EEPROM regdomain: 0x8318
[   27.605285] ath: EEPROM indicates we should expect a country code
[   27.605287] ath: doing EEPROM country->regdmn map search
[   27.605289] ath: country maps to regdmn code: 0x36
[   27.605291] ath: Country alpha2 being used: TR
[   27.605294] ath: Regpair used: 0x36
[   27.605296] ath: regdomain 0x8318 dynamically updated by country element
[   27.670033] wlp2s0: Limiting TX power to 20 (20 - 0) dBm as advertised by 50:ff:20:2d:79:16
[   29.390620] usb 2-5: New USB device found, idVendor=04ca, idProduct=300b, bcdDevice= 0.02
[   29.390627] usb 2-5: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[   29.617553] Bluetooth: BNEP (Ethernet Emulation) ver 1.3
[   29.617561] Bluetooth: BNEP filters: protocol multicast
[   29.617567] Bluetooth: BNEP socket layer initialized
[   29.620938] Bluetooth: MGMT ver 1.22
[   29.637994] NET: Registered PF_ALG protocol family
[   29.682483] Bluetooth: RFCOMM TTY layer initialized
[   29.682496] Bluetooth: RFCOMM socket layer initialized
[   29.682505] Bluetooth: RFCOMM ver 1.11
[   31.414923] rfkill: input handler disabled
[   33.062799] kauditd_printk_skb: 176 callbacks suppressed
[   33.062805] audit: type=1400 audit(1728980250.174:188): apparmor="STATUS" operation="profile_load" profile="unconfined" name="docker-default" pid=2292 comm="apparmor_parser"
[   33.158236] evm: overlay not supported
[   34.495533] bridge: filtering via arp/ip/ip6tables is no longer available by default. Update your scripts to load br_netfilter if you need this.
[   34.498037] Bridge firewalling registered
[   34.595660] Initializing XFRM netlink socket
[   37.714599] systemd-journald[463]: /var/log/journal/343a01cb50af40aa932f9824ef25a9b8/user-1000.journal: Journal file uses a different sequence number ID, rotating.
[   37.924930] audit: type=1400 audit(1728980255.036:189): apparmor="DENIED" operation="open" class="file" profile="snap-update-ns.snapd-desktop-integration" name="/proc/2553/maps" pid=2553 comm="5" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[   38.176601] rfkill: input handler enabled
[   40.365899] rfkill: input handler disabled
[   41.227423] audit: type=1400 audit(1728980258.339:190): apparmor="DENIED" operation="open" class="file" profile="snap-update-ns.snapd-desktop-integration" name="/proc/3211/maps" pid=3211 comm="5" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[   46.906895] audit: type=1400 audit(1728980264.018:191): apparmor="DENIED" operation="capable" class="cap" profile="/usr/lib/snapd/snap-confine" pid=3451 comm="snap-confine" capability=12  capname="net_admin"
[   46.906904] audit: type=1400 audit(1728980264.018:192): apparmor="DENIED" operation="capable" class="cap" profile="/usr/lib/snapd/snap-confine" pid=3451 comm="snap-confine" capability=38  capname="perfmon"
[   47.092176] audit: type=1400 audit(1728980264.203:193): apparmor="DENIED" operation="open" class="file" profile="snap-update-ns.firefox" name="/usr/local/share/" pid=3467 comm="5" requested_mask="r" denied_mask="r" fsuid=0 ouid=0
[   47.176366] audit: type=1400 audit(1728980264.285:194): apparmor="DENIED" operation="open" class="file" profile="snap-update-ns.firefox" name="/proc/3474/maps" pid=3474 comm="5" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[   49.080769] audit: type=1107 audit(1728980266.192:195): pid=1156 uid=101 auid=4294967295 ses=4294967295 subj=unconfined msg='apparmor="DENIED" operation="dbus_method_call"  bus="system" path="/org/freedesktop/timedate1" interface="org.freedesktop.DBus.Properties" member="GetAll" mask="send" name=":1.19" pid=3451 label="snap.firefox.firefox" peer_pid=1562 peer_label="unconfined"
                exe="/usr/bin/dbus-daemon" sauid=101 hostname=? addr=? terminal=?'
[  330.111625] audit: type=1107 audit(1728980547.489:196): pid=1156 uid=101 auid=4294967295 ses=4294967295 subj=unconfined msg='apparmor="DENIED" operation="dbus_method_call"  bus="system" path="/org/freedesktop/timedate1" interface="org.freedesktop.DBus.Properties" member="GetAll" mask="send" name=":1.122" pid=3451 label="snap.firefox.firefox" peer_pid=5540 peer_label="unconfined"
                exe="/usr/bin/dbus-daemon" sauid=101 hostname=? addr=? terminal=?'
[ 2617.777124] audit: type=1400 audit(1728982835.155:197): apparmor="DENIED" operation="open" class="file" profile="snap-update-ns.firmware-updater" name="/proc/6464/maps" pid=6464 comm="5" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[ 2618.005848] audit: type=1400 audit(1728982835.383:198): apparmor="DENIED" operation="open" class="file" profile="snap.firmware-updater.firmware-notifier" name="/proc/sys/vm/max_map_count" pid=6444 comm="firmware-notifi" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[ 4798.514338] warning: `Socket Thread' uses wireless extensions which will stop working for Wi-Fi 7 hardware; use nl80211
[ 5093.762857] workqueue: delayed_fput hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
[ 6569.625561] perf: interrupt took too long (2503 > 2500), lowering kernel.perf_event_max_sample_rate to 79000
[ 8431.986331] loop30: detected capacity change from 0 to 22752
[ 8433.177521] audit: type=1400 audit(1728988650.520:199): apparmor="STATUS" operation="profile_replace" info="same as current profile, skipping" profile="unconfined" name="/snap/snapd/21759/usr/lib/snapd/snap-confine" pid=13562 comm="apparmor_parser"
[ 8433.177529] audit: type=1400 audit(1728988650.520:200): apparmor="STATUS" operation="profile_replace" info="same as current profile, skipping" profile="unconfined" name="/snap/snapd/21759/usr/lib/snapd/snap-confine//mount-namespace-capture-helper" pid=13562 comm="apparmor_parser"
[ 8433.972349] audit: type=1400 audit(1728988651.312:201): apparmor="STATUS" operation="profile_replace" profile="unconfined" name="snap.firmware-updater.firmware-notifier" pid=13565 comm="apparmor_parser"
[ 8434.117167] audit: type=1400 audit(1728988651.459:202): apparmor="STATUS" operation="profile_replace" profile="unconfined" name="snap-update-ns.firmware-updater" pid=13564 comm="apparmor_parser"
[ 8434.638097] audit: type=1400 audit(1728988651.980:203): apparmor="STATUS" operation="profile_replace" profile="unconfined" name="snap.firmware-updater.firmware-updater" pid=13566 comm="apparmor_parser"
[ 8434.893417] audit: type=1400 audit(1728988652.236:204): apparmor="STATUS" operation="profile_replace" profile="unconfined" name="snap.firmware-updater.firmware-updater-app" pid=13567 comm="apparmor_parser"
[ 8434.955599] audit: type=1400 audit(1728988652.298:205): apparmor="STATUS" operation="profile_replace" profile="unconfined" name="snap.firmware-updater.hook.configure" pid=13574 comm="apparmor_parser"
[ 8654.861402] perf: interrupt took too long (3134 > 3128), lowering kernel.perf_event_max_sample_rate to 63000
[10582.508460] perf: interrupt took too long (3926 > 3917), lowering kernel.perf_event_max_sample_rate to 50000
[13417.786918] audit: type=1400 audit(1728993635.098:206): apparmor="DENIED" operation="open" class="file" profile="snap-update-ns.firmware-updater" name="/proc/37233/maps" pid=37233 comm="5" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[13418.597303] audit: type=1400 audit(1728993635.908:207): apparmor="DENIED" operation="open" class="file" profile="snap.firmware-updater.firmware-notifier" name="/proc/sys/vm/max_map_count" pid=37219 comm="firmware-notifi" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[19164.382378] perf: interrupt took too long (4912 > 4907), lowering kernel.perf_event_max_sample_rate to 40000
[24217.687976] audit: type=1400 audit(1729004434.964:208): apparmor="DENIED" operation="open" class="file" profile="snap-update-ns.firmware-updater" name="/proc/84119/maps" pid=84119 comm="5" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
[24217.761023] audit: type=1400 audit(1729004435.037:209): apparmor="DENIED" operation="open" class="file" profile="snap.firmware-updater.firmware-notifier" name="/proc/sys/vm/max_map_count" pid=84105 comm="firmware-notifi" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0


---

### 评论 #3 — harkgill-amd (2024-10-15T15:17:03Z)

I'm thinking this may be because your GPU is in a power saving state causing your system to only report the integrated graphics. Could you try the following to wake the GPU and see if its reported?

1. `sudo apt install mesa-utils`
2. `DRI_PRIME=1 glxgears`
3. In a new terminal, run `rocminfo`

---

### 评论 #4 — urbandroid (2024-10-15T15:20:23Z)

i have run  DRI_PRIME=1 glxgears in one terminal and while its running i run the rocminfo in another terminal

rocminfo
ROCk module version 6.8.5 is loaded
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
  Name:                    Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
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
  Max Clock Freq. (MHz):   2600                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12124424(0xb90108) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                


---

### 评论 #5 — harkgill-amd (2024-10-15T15:56:20Z)

Is it possible to disable the integrated/hybrid graphics setup in the BIOS? Would be worth seeing if the dGPU appears when being the only display adapter. If you could please provide the laptop model I'll investigate this on my end as well.

---

### 评论 #6 — urbandroid (2024-10-15T16:00:55Z)

packard  bell easy note TE 
SKU Number: EasyNote TE69HW_0776_V2.10
i'm going to try disabling  integrated/hybrid in BIOS as well


---

### 评论 #7 — urbandroid (2024-10-15T16:58:50Z)

There is nothing about  integrated/hybrid in BIOS settings.
no Advanced option either is this a must? Can we move on?

---

### 评论 #8 — kentrussell (2024-10-15T17:30:29Z)

1: You're using an 8750M (Mars), but lsmod indicates using amdgpu for the driver. Does dmesg say anything regarding the GPU? lspci showing both implies that the GPU is turned on but couldn't initialize. Attaching a full dmesg here will help to confirm that, though.
2: Note that gfx6 isn't supported in ROCm, and never has been. In ROCm's initial delivery, gfx7 was the oldest GFX family that supported ROCm, and that was just on Hawaii. gfx8 was the minimum HW architecture at that time. While ROCm doesn't support gfx8 officially, the bits are all there in theory to make it work. But gfx6 was never validated and is missing key architecture functionality to support ROCm. You'll officially need gfx9 or gfx10 for ROCm, support. gfx8 could work, but it's not tested so it may have issues with newer ROCm drops.

EDIT: Sorry, I missed the dmesg earlier. This line is the signature of the issue:
[ 5.807090] kfd kfd: amdgpu: OLAND not supported in kfd
rocminfo requires KFD for information. Oland isn't supported in KFD, so rocminfo won't show any GPU info. 

---

### 评论 #9 — urbandroid (2024-10-15T18:14:22Z)

https://wiki.archlinux.org/title/AMDGPU#kfd:_amdgpu:_TOPAZ_not_supported_in_kfd
says that "If you are not planning to use [Radeon Open Compute](https://wiki.archlinux.org/title/GPGPU#ROCm), this can be safely ignored" is this info incorrect?

---

### 评论 #10 — urbandroid (2024-10-15T18:19:14Z)

Because when i try to run Gradio and load a model  it says:

rocBLAS error: Could not initialize Tensile host: No devices found


---

### 评论 #11 — harkgill-amd (2024-10-15T18:51:00Z)

>  is this info incorrect?

While this is correct, it looks like Gradio is trying to interface with rocBLAS (One of the math libraries within ROCm). Any library or package that relies on ROCm will likely fail as the kfd driver is incompatible with your GPU. 

As a workaround, you can try to run the model on your CPU in torch with
```
device = torch.device('cpu')
```

---

### 评论 #12 — urbandroid (2024-10-15T20:13:43Z)

I was able to run with cpu i was trying to run with gpu.

Is there a way that doesn't require kfd or can ability of detecting gpu without kfd added to ROC possibility?

---

### 评论 #13 — harkgill-amd (2024-10-15T20:59:13Z)

Unfortunately, there's no way to workaround the dependency on the kfd driver. It serves as the foundation for all things compute related. 

---

### 评论 #14 — urbandroid (2024-10-15T21:20:29Z)

Can OLAND support be added to kfd in the future?

---

### 评论 #15 — kentrussell (2024-10-15T21:33:17Z)

CPUs are able to get things done in KFD, but unfortunately GPUs can be restricted due to the actual HW architecture. GFX6 won't work, unfortunately. You can reference https://github.com/RadeonOpenCompute/ROCm/issues/509#issuecomment-422999215 or https://github.com/ROCm/ROCm/issues/2232 for similar responses.

---

### 评论 #16 — harkgill-amd (2024-10-18T13:36:06Z)

Closing out this ticket as the failure to detect GPU is related to incompatible hardware. @urbandroid, if you have any more questions, feel free to leave a comment on this thread. 

---
