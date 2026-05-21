# [Issue]: Host CPU memory leak with amdgpu-dkms driver during GPU compute workloads

> **Issue #5915**
> **状态**: closed
> **创建时间**: 2026-01-30T10:07:06Z
> **更新时间**: 2026-02-13T15:05:42Z
> **关闭时间**: 2026-02-13T15:05:42Z
> **作者**: alexschroeter
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5915

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- tcgu-amd

## 描述

# [Bug]: Host CPU memory leak with amdgpu-dkms driver during GPU compute workloads

## Problem Description

When running GPU compute workloads (GROMACS, OpenCL applications) with the AMD DKMS driver and ROCm 7.1.x, host CPU memory (RSS) continuously grows at ~70-90 GB/hour until the system runs out of memory. The GPU VRAM remains stable - only host memory is affected.

**The issue does NOT occur with the stock in-kernel amdgpu driver + ROCm 6.1.3.**

## Environment

- **OS:** AlmaLinux 9.7 (Moss Jungle Cat)
- **Kernel:** 5.14.0-611.9.1.el9_7.x86_64
- **GPU:** AMD Instinct MI210 (gfx90a)
- **GROMACS:** v2025.4 with SYCL backend (AdaptiveCpp)
- **MPI:** OpenMPI 5.0.9

### Driver/ROCm Versions Tested

| Configuration | amdgpu-dkms | ROCm | Leak Rate |
|---------------|-------------|------|-----------|
| Stock kernel driver | N/A (in-kernel) | 6.1.3 | ~0.02 GB/hr ✅ |
| amdgpu-dkms 30.20.1 | 6.16.6 | 7.1.1 | ~72 GB/hr ❌ |
| amdgpu-dkms 30.30 | 6.16.13 | 7.1.1 | ~90 GB/hr ❌ |
| amdgpu-dkms 30.30 + cwsr_enable=0 | 6.16.13 | 7.1.1 | ~79 GB/hr ❌ |
| amdgpu-dkms 30.30 | 6.16.13 | 7.2.0 | ~9 GB/hr ⚠️ |
| amdgpu-dkms 30.30 + cwsr_enable=0 | 6.16.13 | 7.2.0 | ~5.4 GB/hr ⚠️ |

## Symptoms

1. **Host CPU RSS memory grows continuously** during GPU compute workloads
2. GPU VRAM usage remains stable
3. Memory is not released after GPU tasks complete
4. Eventually leads to OOM conditions on long-running jobs
5. **Both SYCL and OpenCL applications are affected** (not application-specific)

## Reproduction Steps

1. Install amdgpu-dkms 30.20.1 or 30.30 with ROCm 7.1.1
2. Run any GPU compute workload (e.g., GROMACS mdrun with GPU acceleration)
3. Monitor host memory with: `watch -n 30 'ps aux | grep gmx_mpi | grep -v grep | awk "{sum+=\$6} END{print sum/1024/1024, \"GB\"}"'`
4. Observe memory growing at ~70-90 GB/hour

## Evidence

### Memory Monitoring Data

**ROCm 7.1.1 + amdgpu-dkms 30.30 (LEAKING):**
```
Time(s)   CPU RSS (GB)   GPU VRAM (MB)
0         39.26          25,609
243       46.05          25,657
485       50.41          25,657
727       54.67          25,665
1029      65.08          25,728

Leak rate: ~90 GB/hour
```

**Stock kernel driver + ROCm 6.1.3 (STABLE):**
```
Time(s)   CPU RSS (GB)   GPU VRAM (MB)
0         18.116         N/A
8575      18.164         N/A

Leak rate: ~0.02 GB/hour (essentially stable)
```

**ROCm 7.2.0 + cwsr_enable=0 (IMPROVED but still leaking):**
```
Time(s)   CPU RSS (GB)   GPU VRAM (MB)
61        24.14          25,539
969       25.71          25,547
1938      26.98          25,547

Leak rate: ~5.4 GB/hour
```

### Kernel Messages (dmesg)

During workload execution, kernel logs show repeated KFD queue buffer messages:
```
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d8c800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d90600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d94400000, queue evicted
... (many more)
```

## Analysis

1. **The leak is in the amdgpu-dkms driver**, not in ROCm userspace libraries or applications
2. **Both amdgpu-dkms 30.20.1 and 30.30 are affected** - not a regression between these versions
3. **The stock in-kernel amdgpu driver does NOT leak** - suggests the issue is specific to the DKMS driver
4. **Both SYCL and OpenCL applications leak** - confirms it's a driver-level issue, not application-specific
5. **ROCm 7.2.0 significantly reduces the leak** (~90% improvement) but doesn't fully eliminate it
6. **cwsr_enable=0 provides minor additional improvement** with ROCm 7.2.0

## Workaround

The best current workaround is:
```bash
# Use ROCm 7.2.0 with cwsr_enable=0
# Add to /etc/modprobe.d/amdgpu.conf:
options amdgpu cwsr_enable=0

# Or kernel command line:
amdgpu.cwsr_enable=0
```

This reduces the leak from ~90 GB/hr to ~5.4 GB/hr, allowing jobs to run ~88 hours instead of ~5 hours before exhausting memory.

## Expected Behavior

Host CPU memory should remain stable during GPU compute workloads, similar to the behavior observed with the stock in-kernel amdgpu driver + ROCm 6.1.3.

## Related Issues

- https://github.com/RadeonOpenCompute/ROCK-Kernel-Driver/issues/84 (similar memory leak fixed in ROCm 3.3)
- https://www.overclock.net/threads/memory-leak-rocm-4-0-kernels-5-9-14.1777323/ (ROCm 4.0 regression)

## Additional Information

Full monitoring data and scripts are available upon request. The memory monitoring was performed using a custom script that samples RSS and GPU VRAM at 60-second intervals.

---

**System Information:**
```
OS:
NAME="AlmaLinux"
VERSION="9.7 (Moss Jungle Cat)"
CPU: 
model name      : AMD EPYC 7452 32-Core Processor
GPU:
  Name:                    AMD EPYC 7452 32-Core Processor    
  Marketing Name:          AMD EPYC 7452 32-Core Processor    
  Name:                    AMD EPYC 7452 32-Core Processor    
  Marketing Name:          AMD EPYC 7452 32-Core Processor    
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
  Name:                    gfx90a                             
  Marketing Name:          AMD Instinct MI210                 
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-

$ uname -a
Linux gpu06-006 5.14.0-611.9.1.el9_7.x86_64

$ modinfo amdgpu | grep version
version:        6.16.13

$ rpm -q rocm-core
rocm-core-7.2.0.70200-XX.el9.x86_64
```


### Operating System

AlmaLinux 9.7

### CPU

AMD EPYC 7452 32-Core Processor

### GPU

MI 210

### ROCm Version

7.1.1, 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Install amdgpu-dkms 30.20.1 or 30.30 with ROCm 7.1.1
2. Run any GPU compute workload (e.g., GROMACS mdrun with GPU acceleration)
3. Monitor host memory with: `watch -n 30 'ps aux | grep gmx_mpi | grep -v grep | awk "{sum+=\$6} END{print sum/1024/1024, \"GB\"}"'`
4. Observe memory growing at ~70-90 GB/hour

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
/opt/rocm/bin/rocminfo --support
ROCk module version 6.16.13 is loaded
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
  Name:                    AMD EPYC 7452 32-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7452 32-Core Processor    
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
  Max Clock Freq. (MHz):   2350                               
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
      Size:                    263453980(0xfb3fd1c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    263453980(0xfb3fd1c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    263453980(0xfb3fd1c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    263453980(0xfb3fd1c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    AMD EPYC 7452 32-Core Processor    
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD EPYC 7452 32-Core Processor    
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
  Max Clock Freq. (MHz):   2350                               
  BDFID:                   0                                  
  Internal Node ID:        1                                  
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
      Size:                    264226860(0xfbfc82c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    264226860(0xfbfc82c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    264226860(0xfbfc82c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    264226860(0xfbfc82c) KB            
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 3                  
*******                  
  Name:                    gfx90a                             
  Uuid:                    GPU-81da0ff79916be62               
  Marketing Name:          AMD Instinct MI210                 
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
  Chip ID:                 29711(0x740f)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   1700                               
  BDFID:                   25344                              
  Internal Node ID:        2                                  
  Compute Unit:            104                                
  SIMDs per CU:            4                                  
  Shader Engines:          8                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    2048(0x800)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 98                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67092480(0x3ffc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67092480(0x3ffc000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx90a:sramecc+:xnack-
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
...
Till all for all 8 GPUs
*** Done ***    
```

### Additional Information

Maybe relevant `dmesg -T` output:

```
[Thu Jan 29 10:52:00 2026] ------------[ cut here ]------------
[Thu Jan 29 10:52:00 2026] WARNING: CPU: 63 PID: 1080365 at fs/dcache.c:2833 __d_move+0x38f/0x3a0
[Thu Jan 29 10:52:00 2026] Modules linked in: panfs(POE) acpi_ipmi ipmi_si ipmi_devintf ipmi_msghandler rpcsec_gss_krb5 nfsv4 dns_resolver nfs lockd grace fscache netfs beegfs(OE) rdma_ucm(OE) rdma_cm(OE) iw_cm(OE) rfkill ib_ipoib(OE) ib_cm(OE) ib_umad(OE) vfat fat amd_atl intel_rapl_msr intel_rapl_common amd64_edac edac_mce_amd ast rapl drm_shmem_helper pcspkr acpi_cpufreq i2c_piix4 ptdma k10temp i2c_smbus joydev auth_rpcgss fuse sunrpc xfs libcrc32c mlx5_ib(OE) macsec ib_uverbs(OE) ib_core(OE) mlx5_fwctl(OE) fwctl amdgpu(OE) mlx5_core(OE) amddrm_ttm_helper(OE) amdttm(OE) amddrm_buddy(OE) amdxcp(OE) drm_client_lib drm_ttm_helper ttm amddrm_exec(OE) drm_suballoc_helper amd_sched(OE) amdkcl(OE) drm_panel_backlight_quirks drm_display_helper drm_kms_helper sg mlxdevm(OE) cec rndis_host video ahci mlxfw(OE) mlx_compat(OE) wmi crct10dif_pclmul libahci cdc_ether psample crc32_pclmul nvme igb crc32c_intel tls nvme_core drm libata ghash_clmulni_intel usbnet dca pci_hyperv_intf nvme_keyring ccp mii nvme_auth i2c_algo_bit sp5100_tco xpmem(OE)
[Thu Jan 29 10:52:00 2026] CPU: 63 PID: 1080365 Comm: slurmstepd Tainted: P        W  OE      ------  ---  5.14.0-611.9.1.el9_7.x86_64 #1
[Thu Jan 29 10:52:00 2026] Hardware name: Supermicro AS -4124GS-TNR/H12DSG-O-CPU, BIOS 2.4 04/22/2022
[Thu Jan 29 10:52:00 2026] RIP: 0010:__d_move+0x38f/0x3a0
[Thu Jan 29 10:52:00 2026] Code: f6 c3 01 75 f1 8d 73 01 89 d8 f0 0f b1 32 39 c3 75 e4 4c 89 f7 e8 11 f9 ff ff 48 89 44 24 10 e9 2b fd ff ff 0f 0b 0f 0b 0f 0b <0f> 0b e9 83 fd ff ff 66 2e 0f 1f 84 00 00 00 00 00 90 90 90 90 90
[Thu Jan 29 10:52:00 2026] RSP: 0018:ffffba443149b720 EFLAGS: 00010246
[Thu Jan 29 10:52:00 2026] RAX: ffff9b7306c03bc0 RBX: 000000000000001c RCX: 0000000000000000
[Thu Jan 29 10:52:00 2026] RDX: 0000000000000003 RSI: ffff9b13d6569e43 RDI: ffff9b6b10f86d03
[Thu Jan 29 10:52:00 2026] RBP: ffff9b6b10f86cc0 R08: ffffba443149b860 R09: ffff9b764fbf4470
[Thu Jan 29 10:52:00 2026] R10: ffffba443149b748 R11: 00000000002849cc R12: ffff9af843656e40
[Thu Jan 29 10:52:00 2026] R13: ffff9b522a98b140 R14: ffff9b13d6569e00 R15: ffff9b13d6569e60
[Thu Jan 29 10:52:00 2026] FS:  0000153f7d43c780(0000) GS:ffff9b764fbc0000(0000) knlGS:0000000000000000
[Thu Jan 29 10:52:00 2026] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[Thu Jan 29 10:52:00 2026] CR2: 00001507400187b8 CR3: 00000041746ca000 CR4: 0000000000350ef0
[Thu Jan 29 10:52:00 2026] Call Trace:
[Thu Jan 29 10:52:00 2026]  <TASK>
[Thu Jan 29 10:52:00 2026]  ? show_trace_log_lvl+0x1c4/0x2df
[Thu Jan 29 10:52:00 2026]  ? show_trace_log_lvl+0x1c4/0x2df
[Thu Jan 29 10:52:00 2026]  ? d_move+0x2e/0x50
[Thu Jan 29 10:52:00 2026]  ? __d_move+0x38f/0x3a0
[Thu Jan 29 10:52:00 2026]  ? __warn+0x7d/0xd0
[Thu Jan 29 10:52:00 2026]  ? __d_move+0x38f/0x3a0
[Thu Jan 29 10:52:00 2026]  ? report_bug+0x102/0x140
[Thu Jan 29 10:52:00 2026]  ? handle_bug+0x3c/0x70
[Thu Jan 29 10:52:00 2026]  ? exc_invalid_op+0x14/0x70
[Thu Jan 29 10:52:00 2026]  ? asm_exc_invalid_op+0x16/0x20
[Thu Jan 29 10:52:00 2026]  ? __d_move+0x38f/0x3a0
[Thu Jan 29 10:52:00 2026]  d_move+0x2e/0x50
[Thu Jan 29 10:52:00 2026]  pan_kernel_fs_client_cache_name_coalesce_dentry_alias+0x77/0x140 [panfs]
[Thu Jan 29 10:52:00 2026]  _pan_kernel_fs_client_dir_iops_lookup+0xab9/0xc90 [panfs]
[Thu Jan 29 10:52:00 2026]  pan_kernel_fs_client_dir_iops_lookup+0x9/0x10 [panfs]
[Thu Jan 29 10:52:00 2026]  __lookup_slow+0x81/0x130
[Thu Jan 29 10:52:00 2026]  walk_component+0x158/0x1d0
[Thu Jan 29 10:52:00 2026]  link_path_walk.part.0.constprop.0+0x24e/0x390
[Thu Jan 29 10:52:00 2026]  ? path_init+0x2c4/0x3f0
[Thu Jan 29 10:52:00 2026]  path_openat+0xb0/0x280
[Thu Jan 29 10:52:00 2026]  do_filp_open+0xb0/0x160
[Thu Jan 29 10:52:00 2026]  ? __check_object_size.part.0+0x47/0xd0
[Thu Jan 29 10:52:00 2026]  ? alloc_fd+0xf6/0x1b0
[Thu Jan 29 10:52:00 2026]  do_sys_openat2+0x96/0xd0
[Thu Jan 29 10:52:00 2026]  __x64_sys_openat+0x53/0xa0
[Thu Jan 29 10:52:00 2026]  do_syscall_64+0x5c/0xe0
[Thu Jan 29 10:52:00 2026]  ? do_sys_openat2+0x81/0xd0
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_work+0xff/0x130
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_to_user_mode+0x19/0x40
[Thu Jan 29 10:52:00 2026]  ? do_syscall_64+0x6b/0xe0
[Thu Jan 29 10:52:00 2026]  ? ttwu_queue_wakelist+0x101/0x120
[Thu Jan 29 10:52:00 2026]  ? try_to_wake_up+0x1c9/0x540
[Thu Jan 29 10:52:00 2026]  ? complete_signal+0x10e/0x350
[Thu Jan 29 10:52:00 2026]  ? __send_signal_locked+0x1b8/0x3c0
[Thu Jan 29 10:52:00 2026]  ? send_signal_locked+0xc6/0x130
[Thu Jan 29 10:52:00 2026]  ? do_send_sig_info+0x6b/0xc0
[Thu Jan 29 10:52:00 2026]  ? do_send_specific+0x92/0xb0
[Thu Jan 29 10:52:00 2026]  ? do_tkill+0x87/0xb0
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_work+0xff/0x130
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_to_user_mode+0x19/0x40
[Thu Jan 29 10:52:00 2026]  ? do_syscall_64+0x6b/0xe0
[Thu Jan 29 10:52:00 2026]  ? do_send_specific+0x92/0xb0
[Thu Jan 29 10:52:00 2026]  ? do_tkill+0x87/0xb0
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_work+0xff/0x130
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_to_user_mode+0x19/0x40
[Thu Jan 29 10:52:00 2026]  ? do_syscall_64+0x6b/0xe0
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_to_user_mode+0x19/0x40
[Thu Jan 29 10:52:00 2026]  ? do_syscall_64+0x6b/0xe0
[Thu Jan 29 10:52:00 2026]  ? syscall_exit_to_user_mode+0x19/0x40
[Thu Jan 29 10:52:00 2026]  ? do_syscall_64+0x6b/0xe0
[Thu Jan 29 10:52:00 2026]  ? __irq_exit_rcu+0x45/0xc0
[Thu Jan 29 10:52:00 2026]  ? sysvec_apic_timer_interrupt+0x3c/0x90
[Thu Jan 29 10:52:00 2026]  entry_SYSCALL_64_after_hwframe+0x76/0x7e
[Thu Jan 29 10:52:00 2026] RIP: 0033:0x153f7cefee44
[Thu Jan 29 10:52:00 2026] Code: 24 20 eb 8f 66 90 44 89 54 24 0c e8 f6 8d f8 ff 44 8b 54 24 0c 44 89 e2 48 89 ee 41 89 c0 bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 77 34 44 89 c7 89 44 24 0c e8 48 8e f8 ff 8b 44
[Thu Jan 29 10:52:00 2026] RSP: 002b:00007ffc19e066b0 EFLAGS: 00000293 ORIG_RAX: 0000000000000101
[Thu Jan 29 10:52:00 2026] RAX: ffffffffffffffda RBX: 0000000001bdbcc0 RCX: 0000153f7cefee44
[Thu Jan 29 10:52:00 2026] RDX: 0000000000080641 RSI: 0000000001bdbbf0 RDI: 00000000ffffff9c
[Thu Jan 29 10:52:00 2026] RBP: 0000000001bdbbf0 R08: 0000000000000000 R09: 0000000000000000
[Thu Jan 29 10:52:00 2026] R10: 00000000000001b6 R11: 0000000000000293 R12: 0000000000080641
[Thu Jan 29 10:52:00 2026] R13: 0000000000000000 R14: 0000000000000000 R15: 0000000000080641
[Thu Jan 29 10:52:00 2026]  </TASK>
[Thu Jan 29 10:52:00 2026] ---[ end trace 0000000000000000 ]---
[Thu Jan 29 11:31:44 2026] amdgpu: Freeing queue vital buffer 0x145748200000, queue evicted
[Thu Jan 29 11:31:44 2026] amdgpu: Freeing queue vital buffer 0x145750200000, queue evicted
[Thu Jan 29 12:48:31 2026] amdgpu: Freeing queue vital buffer 0x152300200000, queue evicted
[Thu Jan 29 12:48:31 2026] amdgpu: Freeing queue vital buffer 0x15230c200000, queue evicted
[Thu Jan 29 14:44:42 2026] amdgpu: Freeing queue vital buffer 0x1503fc200000, queue evicted
[Thu Jan 29 14:44:42 2026] amdgpu: Freeing queue vital buffer 0x150408200000, queue evicted
[Thu Jan 29 16:08:58 2026] beegfs: enabling unsafe global rkey
[Thu Jan 29 16:08:58 2026] beegfs: enabling unsafe global rkey
[Thu Jan 29 16:13:56 2026] beegfs: enabling unsafe global rkey
[Thu Jan 29 16:18:14 2026] block nvme0n1: the capability attribute has been deprecated.
[Thu Jan 29 16:18:14 2026] block nvme0n1: No UUID available providing old NGUID
[Thu Jan 29 16:20:25 2026] beegfs: enabling unsafe global rkey
[Thu Jan 29 16:26:03 2026] beegfs: enabling unsafe global rkey
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1538bf200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153574a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14ccdd200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f20200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150d45200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a30200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cce1000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150f94200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f38200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150d60200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd38000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f6a600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a48200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150fac200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150d91c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd3c800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a7b600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f6ee00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150fddc00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd40000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150d96400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f73600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd41000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150d9ac00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a7fe00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150fe1a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f77e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd45800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150d9f400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f7f000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a80000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150fe5800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f80000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150da5e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150fe9600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f82e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a84600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150da9c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd4ae00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dada00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150ff5200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a88e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f87800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd4ec00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150db1800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a8f800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f8b600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150db5600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd53600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150ff9000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a93600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f8f400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150db9400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd57400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150ffce00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a97400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f93200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dbd200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd5b200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dc0000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d00400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151000000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f97c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd5f000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a9b200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151000c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d10200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f9ba00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dc1000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151005600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd63a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146a9fc00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dc4e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148f9f800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151009400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d4d400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd67800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146aa3a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148fa3600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dc8c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd6b600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146aa7800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d51c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dcca00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15100d200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148fa8000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd6f400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146aab600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dd0800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148fabe00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d56400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd73e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dd4600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151011000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146ab0000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148fafc00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150dd8400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d5ac00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151014e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146ab3e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150ddc200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd77c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146ab7c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d61600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148fb3a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151018c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd7ba00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d65400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x150de4200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146abba00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148fb8200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd7f800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15101ca00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d69200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd80000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146abfc00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd84200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151020800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d6d000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146ac0000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x148fc4200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x14cd8c200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151024600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146ac3a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d71200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151028400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146ac8200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15102c200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d75000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x146ad4200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d79200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x151038200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d7d000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d80000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d80e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d84c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d88a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d8c800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d90600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d94400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152d98200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x152da0200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153594200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535c8400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535ccc00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535d1400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535d5c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535dc200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535e0000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535e4a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535e8800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535ec600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535f0400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535f4e00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535f8c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1535fca00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153600000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153600800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153604a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153608800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15360c600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153610400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153614200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153620200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1538c0000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x1538d8200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153909800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15390e000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153912800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153917000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15391da00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153921800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153925600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153929400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15392d600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153931400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153935200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153939000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15393ce00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153940000000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153940c00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153944a00000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153948800000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15394c600000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153950400000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x153954200000, queue evicted
[Thu Jan 29 17:31:34 2026] amdgpu: Freeing queue vital buffer 0x15395c200000, queue evicted
[Thu Jan 29 17:53:13 2026] amdgpu 0000:a3:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[Thu Jan 29 17:53:13 2026] amdgpu 0000:a3:00.0: amdgpu: amdgpu: finishing device.
[Thu Jan 29 17:53:13 2026] amdgpu 0000:a3:00.0: amdgpu: amdgpu: ttm finalized
[Thu Jan 29 17:53:13 2026] amdgpu 0000:83:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[Thu Jan 29 17:53:13 2026] amdgpu 0000:83:00.0: amdgpu: amdgpu: finishing device.
[Thu Jan 29 17:53:13 2026] amdgpu 0000:83:00.0: amdgpu: amdgpu: ttm finalized
[Thu Jan 29 17:53:13 2026] amdgpu 0000:c3:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[Thu Jan 29 17:53:13 2026] amdgpu 0000:c3:00.0: amdgpu: amdgpu: finishing device.

```

---

## 评论 (5 条)

### 评论 #1 — tcgu-amd (2026-02-06T17:22:10Z)

Hi @alexschroeter, thanks for reaching out! Sorry we were still investigating the issue. I noticed that you closed #5921; is this issue resolved on your end? Thanks! 

---

### 评论 #2 — alexschroeter (2026-02-09T14:33:40Z)

Thanks for reaching out. No the problem is not solved. I just wasn't confident in the "reproducer" from that issue.
It seems that ROCm 7.2.0 solved one of the memory leaks but the one showing up in GROMACS is still leaking heavyly.
Would it be helpful if I provide the steps to reproduce the leak using GROMACS in a separate issue?

---

### 评论 #3 — tcgu-amd (2026-02-09T20:17:06Z)

Hi @alexschroeter, yes a step-by-step reproducer would definitely be helpful. Please free to open another issue, or if you can comment here directly that would work as well. Thanks! 

---

### 评论 #4 — alexschroeter (2026-02-10T15:59:20Z)

Producer (sadly not minimal at all) for the GROMACS leak can be found here: https://github.com/ROCm/ROCm/issues/5948

---

### 评论 #5 — alexschroeter (2026-02-13T15:05:42Z)

I am closing this issue since the GROMACS issue has been put into a separate ticket. And the OpenCL leak has been addressed in ROCm 7.2.0

---
