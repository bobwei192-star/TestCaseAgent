# [Issue]: kernel NULL pointer dereference and device open freeze

> **Issue #2596**
> **状态**: closed
> **创建时间**: 2023-10-23T04:43:49Z
> **更新时间**: 2024-09-23T19:33:40Z
> **关闭时间**: 2024-09-23T19:33:40Z
> **作者**: danielzgtg
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2596

## 描述

### Problem Description

I get "BUG: kernel NULL pointer dereference, address: 0000000000000000", and clinfo freezes halfway through. After running a few other programs, all GPU-based applications freeze while starting. This is after upgrading from Ubuntu 23.04 and ROCm 5.7 to Ubuntu 23.10 and ROCm 5.7.1

[dmesg.txt](https://github.com/RadeonOpenCompute/ROCm/files/13066143/dmesg.txt). The problem also occurred on the next boot with the vboxdrv module blocklisted.


### Operating System

Ubuntu 23.10 (Mantic Minotaur)

### CPU

AMD Ryzen 9 5900X 12-Core Processor

### GPU

RX 6650 XT

### ROCm Version

5.7.1

### ROCm Component

Kernel

### Steps to Reproduce

1. Run firefox, glxinfo, glxgears, vulkaninfo, and vkcube. These do not crash
2. Run /opt/rocm/bin/clinfo. It crashes after the first bit of output, saying it cannot compile the program
3. Run a script using transformers/pytorch-rocm
4. At the same time, start gpt4all. On the previous version of Ubuntu and ROCm, it crashed the first time I run it, but should have worked the second time
5. While the transformers script is still running, run gpt4all again. Both freeze after this
6. Now everything that needs the GPU will freeze when they try to open the device on startup

### Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
(output suddenly freezes here)
(after reboot:)
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
  Name:                    AMD Ryzen 9 5900X 12-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 9 5900X 12-Core Processor
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
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    32770204(0x1f4089c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32770204(0x1f4089c) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    32770204(0x1f4089c) KB             
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
  Marketing Name:          AMD Radeon RX 6650 XT              
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
  Chip ID:                 29679(0x73ef)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2765                               
  BDFID:                   12032                              
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
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
  Packet Processor uCode:: 109                                
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
*** Done ***
```

---

## 评论 (78 条)

### 评论 #1 — danielzgtg (2023-10-23T11:22:18Z)

The situation is worse on Linux 6.6-rc7:

```
Oct 23 07:17:04 daniel-desktop3 kernel: amdgpu 0000:2f:00.0: amdgpu: bo 00000000b0b9bc73 va 0x0800000000-0x0800000001 conflict with 0x0800000000-0x0800000200
Oct 23 07:17:04 daniel-desktop3 kernel: amdgpu: Failed to map VA 0x800000000000 in vm. ret -22
Oct 23 07:17:04 daniel-desktop3 kernel: amdgpu: Failed to map bo to gpuvm
Oct 23 07:17:04 daniel-desktop3 kernel: ------------[ cut here ]------------
Oct 23 07:17:04 daniel-desktop3 kernel: refcount_t: addition on 0; use-after-free.
Oct 23 07:17:04 daniel-desktop3 kernel: WARNING: CPU: 20 PID: 88093 at lib/refcount.c:25 refcount_warn_saturate+0x12e/0x150
Oct 23 07:17:04 daniel-desktop3 kernel: Modules linked in:
Oct 23 07:17:04 daniel-desktop3 kernel: CPU: 20 PID: 88093 Comm: clinfo Not tainted 6.6.0-rc7 #2
Oct 23 07:17:04 daniel-desktop3 kernel: Hardware name: Micro-Star International Co., Ltd. MS-7C37/X570-A PRO (MS-7C37), BIOS H.I0 08/10/2022
Oct 23 07:17:04 daniel-desktop3 kernel: RIP: 0010:refcount_warn_saturate+0x12e/0x150
Oct 23 07:17:04 daniel-desktop3 kernel: Code: 1d b3 85 70 02 80 fb 01 0f 87 d7 2f 23 01 83 e3 01 0f 85 52 ff ff ff 48 c7 c7 18 24 91 94 c6 05 93 85 70 02 01 e8 02 f4 8e >
Oct 23 07:17:04 daniel-desktop3 kernel: RSP: 0018:ffffc900066cbc60 EFLAGS: 00010246
Oct 23 07:17:04 daniel-desktop3 kernel: RAX: 0000000000000000 RBX: 0000000000000000 RCX: 0000000000000000
Oct 23 07:17:04 daniel-desktop3 kernel: RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
Oct 23 07:17:04 daniel-desktop3 kernel: RBP: ffffc900066cbc68 R08: 0000000000000000 R09: 0000000000000000
Oct 23 07:17:04 daniel-desktop3 kernel: R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
Oct 23 07:17:04 daniel-desktop3 kernel: R13: ffff888100f62338 R14: 0000000000000000 R15: ffff8881661e8000
Oct 23 07:17:04 daniel-desktop3 kernel: FS:  00007fa3ac472740(0000) GS:ffff8887fef00000(0000) knlGS:0000000000000000
Oct 23 07:17:04 daniel-desktop3 kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Oct 23 07:17:04 daniel-desktop3 kernel: CR2: 00005573ed2b1000 CR3: 000000014ae64000 CR4: 0000000000750ee0
Oct 23 07:17:04 daniel-desktop3 kernel: PKRU: 55555554
Oct 23 07:17:04 daniel-desktop3 kernel: Call Trace:
Oct 23 07:17:04 daniel-desktop3 kernel:  <TASK>
Oct 23 07:17:04 daniel-desktop3 kernel:  ? show_regs+0x6d/0x80
Oct 23 07:17:04 daniel-desktop3 kernel:  ? __warn+0x89/0x160
Oct 23 07:17:04 daniel-desktop3 kernel:  ? refcount_warn_saturate+0x12e/0x150
Oct 23 07:17:04 daniel-desktop3 kernel:  ? report_bug+0x17e/0x1b0
Oct 23 07:17:04 daniel-desktop3 kernel:  ? handle_bug+0x51/0xa0
Oct 23 07:17:04 daniel-desktop3 kernel:  ? exc_invalid_op+0x18/0x80
Oct 23 07:17:04 daniel-desktop3 kernel:  ? asm_exc_invalid_op+0x1b/0x20
Oct 23 07:17:04 daniel-desktop3 kernel:  ? refcount_warn_saturate+0x12e/0x150
Oct 23 07:17:04 daniel-desktop3 kernel:  dma_resv_add_fence+0x1f0/0x240
Oct 23 07:17:04 daniel-desktop3 kernel:  amdgpu_amdkfd_gpuvm_acquire_process_vm+0x223/0x540
Oct 23 07:17:04 daniel-desktop3 kernel:  kfd_process_device_init_vm+0xc0/0x320
Oct 23 07:17:04 daniel-desktop3 kernel:  ? kfd_ioctl_get_process_apertures_new+0x190/0x380
Oct 23 07:17:04 daniel-desktop3 kernel:  kfd_ioctl_acquire_vm+0x96/0xd0
Oct 23 07:17:04 daniel-desktop3 kernel:  kfd_ioctl+0x44a/0x580
Oct 23 07:17:04 daniel-desktop3 kernel:  ? __pfx_kfd_ioctl_acquire_vm+0x10/0x10
Oct 23 07:17:04 daniel-desktop3 kernel:  __x64_sys_ioctl+0xa3/0xf0
Oct 23 07:17:04 daniel-desktop3 kernel:  do_syscall_64+0x5c/0x90
Oct 23 07:17:04 daniel-desktop3 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Oct 23 07:17:04 daniel-desktop3 kernel:  ? syscall_exit_to_user_mode+0x37/0x60
Oct 23 07:17:04 daniel-desktop3 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Oct 23 07:17:04 daniel-desktop3 kernel:  ? do_syscall_64+0x68/0x90
Oct 23 07:17:04 daniel-desktop3 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Oct 23 07:17:04 daniel-desktop3 kernel:  ? do_syscall_64+0x68/0x90
Oct 23 07:17:04 daniel-desktop3 kernel:  ? do_syscall_64+0x68/0x90
Oct 23 07:17:04 daniel-desktop3 kernel:  ? do_syscall_64+0x68/0x90
Oct 23 07:17:04 daniel-desktop3 kernel:  entry_SYSCALL_64_after_hwframe+0x6e/0xd8
Oct 23 07:17:04 daniel-desktop3 kernel: RIP: 0033:0x7fa3abf238ef
Oct 23 07:17:04 daniel-desktop3 kernel: Code: 00 48 89 44 24 18 31 c0 48 8d 44 24 60 c7 04 24 10 00 00 00 48 89 44 24 08 48 8d 44 24 20 48 89 44 24 10 b8 10 00 00 00 0f >
Oct 23 07:17:04 daniel-desktop3 kernel: RSP: 002b:00007ffc754e4830 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
Oct 23 07:17:04 daniel-desktop3 kernel: RAX: ffffffffffffffda RBX: 00007ffc754e49a0 RCX: 00007fa3abf238ef
Oct 23 07:17:04 daniel-desktop3 kernel: RDX: 00007ffc754e49a0 RSI: 0000000040084b15 RDI: 0000000000000008
Oct 23 07:17:04 daniel-desktop3 kernel: RBP: 0000000040084b15 R08: 0000000000000007 R09: 0000000000000001
Oct 23 07:17:04 daniel-desktop3 kernel: R10: 00005573ed285ac0 R11: 0000000000000246 R12: 00005573ed281250
Oct 23 07:17:04 daniel-desktop3 kernel: R13: 0000000000000008 R14: 00007fa39d0bd040 R15: 0000000000000060
Oct 23 07:17:04 daniel-desktop3 kernel:  </TASK>
Oct 23 07:17:04 daniel-desktop3 kernel: ---[ end trace 0000000000000000 ]---
```

Now the TTY shows those three lines. After a few moments, the screen freezes, and once the ssh did as well. Not only is the ROCm unusable and my computer unable to shutdown, but now my entire computer is unusable after those moments pass with the new kernel.

---

### 评论 #2 — danielzgtg (2023-10-23T13:14:35Z)

I bisected this, resulting in https://lists.freedesktop.org/archives/amd-gfx/2023-October/100298.html

---

### 评论 #3 — kentrussell (2023-11-10T15:34:19Z)

Updating here for clarity. Christian is taking a look at the issue internally. Seems like some of the page tables aren't CPU accessible.

---

### 评论 #4 — napaalm (2023-11-23T13:58:40Z)

@kentrussell is there any update on this issue?

---

### 评论 #5 — kentrussell (2023-11-23T14:25:03Z)

I pinged Christian to see if there is any update. I'll post here (or get him to update the amdgfx thread) once I hear back

---

### 评论 #6 — htfy96 (2023-11-26T17:03:54Z)

Slightly different stacktrace that ends up with NULL pointer dereference. Reproducible with Arch Linux + AMD Ryzen 7 6800H. Happens when I switch Blender 4.1's render engine to HIP.

Steps to reproduce:
1. Download Blender 4.1.0 Alpha from https://builder.blender.org/download/daily/blender-4.1.0-alpha+main.1b6cd937ffc8-linux.x86_64-release.tar.xz
2. Launch. Switch world rendering engine from Eevee to Cycles
3. Open Preference - systems. Switch the rendering engine from CPU to HIP
4. Kernel crashes


Kernel: 6.6.2-arch1-1 #1 SMP PREEMPT_DYNAMIC

Rocm version:
```
extra/rocm-hip-libraries 5.7.1-2 [installed]
    Develop certain applications using HIP and libraries for AMD platforms
extra/rocm-hip-runtime 5.7.1-2 [installed]
    Packages to run HIP applications on the AMD platform
extra/rocm-hip-sdk 5.7.1-2 [installed]
    Develop applications using HIP and libraries for AMD platforms
extra/rocprim 5.7.1-1 [installed]
    Header-only library providing HIP parallel primitives
extra/rocthrust 5.7.1-1 [installed]
    Port of the Thrust parallel algorithm library atop HIP/ROCm
```

<details>
  <summary>dmesg</summary>

```
Nov 26 01:10:31 code01 kernel: amdgpu 0000:62:00.0: amdgpu: bo 000000004fd46f03 va 0x0800000000-0x0800000001 conflict with 0x0800000000-0x0800000200
Nov 26 01:10:31 code01 kernel: amdgpu: Failed to map VA 0x800000000000 in vm. ret -22
Nov 26 01:10:31 code01 kernel: amdgpu: Failed to map bo to gpuvm
Nov 26 01:10:31 code01 kernel: BUG: kernel NULL pointer dereference, address: 0000000000000002
Nov 26 01:10:31 code01 kernel: #PF: supervisor read access in kernel mode
Nov 26 01:10:31 code01 kernel: #PF: error_code(0x0000) - not-present page
Nov 26 01:10:31 code01 kernel: PGD 29631b067 P4D 29631b067 PUD 53a5da067 PMD 0 
Nov 26 01:10:31 code01 kernel: Oops: 0000 [#1] PREEMPT SMP NOPTI
Nov 26 01:10:31 code01 kernel: CPU: 2 PID: 27379 Comm: blender-4.1 Not tainted 6.6.2-arch1-1 #1 11215f9ba7ddfb51644674a5b2ced71612c62fe9
Nov 26 01:10:31 code01 kernel: Hardware name: MECHREVO Code01 Ver2.0/Code01 Ver2.0, BIOS 0016.006.9 08/23/2022
Nov 26 01:10:31 code01 kernel: RIP: 0010:__list_add_valid_or_report+0x1a/0xa0
Nov 26 01:10:31 code01 kernel: Code: 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 f3 0f 1e fa 48 89 d0 48 85 f6 74 2a 48 85 d2 74 3a 48 8b 52 08 48 39 f2 75 41 <4c> 8b 02 49 39 c0 75 4c 48 >
Nov 26 01:10:31 code01 kernel: RSP: 0018:ffffa3b295777af0 EFLAGS: 00010246
Nov 26 01:10:31 code01 kernel: RAX: ffff90d99373e350 RBX: ffffa3b295777b30 RCX: ffff90d9880a0000
Nov 26 01:10:31 code01 kernel: RDX: 0000000000000002 RSI: 0000000000000002 RDI: ffffa3b295777b30
Nov 26 01:10:31 code01 kernel: RBP: ffff90d99373e350 R08: 0000000000000040 R09: ffff90da178c7b00
Nov 26 01:10:31 code01 kernel: R10: 00000000000390a0 R11: ffff90d985064840 R12: ffff90d99373e340
Nov 26 01:10:31 code01 kernel: R13: 0000000000000002 R14: ffffa3b295777b30 R15: 0000000000000000
Nov 26 01:10:31 code01 kernel: FS:  00007f6d332ef580(0000) GS:ffff90e09ee80000(0000) knlGS:0000000000000000
Nov 26 01:10:31 code01 kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Nov 26 01:10:31 code01 kernel: CR2: 0000000000000002 CR3: 00000003b1b9e000 CR4: 0000000000f50ee0
Nov 26 01:10:31 code01 kernel: PKRU: 55555554
Nov 26 01:10:31 code01 kernel: Call Trace:
Nov 26 01:10:31 code01 kernel:  <TASK>
Nov 26 01:10:31 code01 kernel:  ? __die+0x23/0x70
Nov 26 01:10:31 code01 kernel:  ? page_fault_oops+0x171/0x4e0
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? amdgpu_ttm_tt_populate+0x7c/0xb0 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  ? exc_page_fault+0x7f/0x180
Nov 26 01:10:31 code01 kernel:  ? asm_exc_page_fault+0x26/0x30
Nov 26 01:10:31 code01 kernel:  ? __list_add_valid_or_report+0x1a/0xa0
Nov 26 01:10:31 code01 kernel:  __mutex_add_waiter+0x23/0x60
Nov 26 01:10:31 code01 kernel:  __mutex_lock.constprop.0+0x2a4/0x6a0
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  add_kgd_mem_to_kfd_bo_list+0x23/0xa0 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  amdgpu_amdkfd_gpuvm_alloc_memory_of_gpu+0x660/0xa40 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  kfd_process_alloc_gpuvm+0x32/0x100 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  kfd_process_device_init_vm+0x267/0x320 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  kfd_ioctl_acquire_vm+0x89/0xc0 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  kfd_ioctl+0x3cc/0x4e0 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  ? __pfx_kfd_ioctl_acquire_vm+0x10/0x10 [amdgpu 0401721894ca8f32d5d0b424349ce03960632e80]
Nov 26 01:10:31 code01 kernel:  __x64_sys_ioctl+0x97/0xd0
Nov 26 01:10:31 code01 kernel:  do_syscall_64+0x60/0x90
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? syscall_exit_to_user_mode+0x2b/0x40
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? do_syscall_64+0x6c/0x90
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? syscall_exit_to_user_mode+0x2b/0x40
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? do_syscall_64+0x6c/0x90
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? syscall_exit_to_user_mode+0x2b/0x40
Nov 26 01:10:31 code01 kernel:  ? srso_alias_return_thunk+0x5/0x7f
Nov 26 01:10:31 code01 kernel:  ? do_syscall_64+0x6c/0x90
Nov 26 01:10:31 code01 kernel:  entry_SYSCALL_64_after_hwframe+0x6e/0xd8
Nov 26 01:10:31 code01 kernel: RIP: 0033:0x7f6d32f2a3af
Nov 26 01:10:31 code01 kernel: Code: 00 48 89 44 24 18 31 c0 48 8d 44 24 60 c7 04 24 10 00 00 00 48 89 44 24 08 48 8d 44 24 20 48 89 44 24 10 b8 10 00 00 00 0f 05 <89> c2 3d 00 f0 ff ff 77 18 >
Nov 26 01:10:31 code01 kernel: RSP: 002b:00007ffd309e1fd0 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
Nov 26 01:10:31 code01 kernel: RAX: ffffffffffffffda RBX: 00007ffd309e20c0 RCX: 00007f6d32f2a3af
Nov 26 01:10:31 code01 kernel: RDX: 00007ffd309e2140 RSI: 0000000040084b15 RDI: 0000000000000017
Nov 26 01:10:31 code01 kernel: RBP: 00007ffd309e2140 R08: 0000000000000015 R09: 0000000000000008
Nov 26 01:10:31 code01 kernel: R10: 0000000000000001 R11: 0000000000000246 R12: 0000000040084b15
Nov 26 01:10:31 code01 kernel: R13: 0000000000000017 R14: 00007f6c22304560 R15: 00007f6d1c4ae180
Nov 26 01:10:31 code01 kernel:  </TASK>
Nov 26 01:10:31 code01 kernel: Modules linked in: ccm snd_seq_dummy snd_hrtimer snd_seq snd_seq_device intel_rapl_msr intel_rapl_common snd_soc_acp6x_mach snd_soc_dmic snd_acp6x_pdm_dma snd_so>
Nov 26 01:10:31 code01 kernel:  videobuf2_common snd_soc_acpi ledtrig_audio mdio_devres sp5100_tco hid_multitouch snd cryptd ecdh_generic mc rapl pcspkr sparse_keymap wmi_bmof thunderbolt k10t>
Nov 26 01:10:31 code01 kernel: CR2: 0000000000000002
Nov 26 01:10:31 code01 kernel: ---[ end trace 0000000000000000 ]---
Nov 26 01:10:31 code01 kernel: RIP: 0010:__list_add_valid_or_report+0x1a/0xa0
Nov 26 01:10:31 code01 kernel: Code: 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 f3 0f 1e fa 48 89 d0 48 85 f6 74 2a 48 85 d2 74 3a 48 8b 52 08 48 39 f2 75 41 <4c> 8b 02 49 39 c0 75 4c 48 >
Nov 26 01:10:31 code01 kernel: RSP: 0018:ffffa3b295777af0 EFLAGS: 00010246
Nov 26 01:10:31 code01 kernel: RAX: ffff90d99373e350 RBX: ffffa3b295777b30 RCX: ffff90d9880a0000
Nov 26 01:10:31 code01 kernel: RDX: 0000000000000002 RSI: 0000000000000002 RDI: ffffa3b295777b30
Nov 26 01:10:31 code01 kernel: RBP: ffff90d99373e350 R08: 0000000000000040 R09: ffff90da178c7b00
Nov 26 01:10:31 code01 kernel: R10: 00000000000390a0 R11: ffff90d985064840 R12: ffff90d99373e340
Nov 26 01:10:31 code01 kernel: R13: 0000000000000002 R14: ffffa3b295777b30 R15: 0000000000000000
Nov 26 01:10:31 code01 kernel: FS:  00007f6d332ef580(0000) GS:ffff90e09ee80000(0000) knlGS:0000000000000000
Nov 26 01:10:31 code01 kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Nov 26 01:10:31 code01 kernel: CR2: 0000000000000002 CR3: 00000003b1b9e000 CR4: 0000000000f50ee0
Nov 26 01:10:31 code01 kernel: PKRU: 55555554
Nov 26 01:10:31 code01 kernel: note: blender-4.1[27379] exited with irqs disabled
Nov 26 01:10:31 code01 kernel: note: blender-4.1[27379] exited with preempt_count 2
```
</details> 

<details>
<summary>clinfo</summary>

```
Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.1 AMD-APP.dbg (3590.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 1
  Device Type:					 CL_DEVICE_TYPE_GPU
  Vendor ID:					 1002h
  Board name:					 AMD Radeon Graphics
  Device Topology:				 PCI[ B#98, D#0, F#0 ]
  Max compute units:				 6
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
  Max clock frequency:				 2200Mhz
  Address bits:					 64
  Max memory allocation:			 912680544
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
  Alignment (bits) of base address:		 1024
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
  Cache size:					 16384
  Global memory size:				 1073741824
  Constant buffer size:				 912680544
  Max number of constant args:			 8
  Local memory type:				 Scratchpad
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 912680544
  Max global variable size:			 912680544
  Max global variable preferred total size:	 1073741824
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
  Kernel Preferred work group size multiple:	 32
  Error correction support:			 0
  Unified memory for Host and Device:		 0
  Profiling timer resolution:			 1
  Device endianess:				 Little
  Available:					 Yes
  Compiler available:				 Yes
  Execution capabilities:				 
    Execute OpenCL kernels:			 Yes
    Execute native function:			 No
  Queue on Host properties:				 
    Out-of-Order:				 No
    Profiling :					 Yes
  Queue on Device properties:				 
    Out-of-Order:				 Yes
    Profiling :					 Yes
  Platform ID:					 0x7fe994e0f010
  Name:						 gfx1035
  Vendor:					 Advanced Micro Devices, Inc.
  Device OpenCL C version:			 OpenCL C 2.0 
  Driver version:				 3590.0 (HSA1.1,LC)
  Profile:					 FULL_PROFILE
  Version:					 OpenCL 2.0 
  Extensions:					 cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 
```
</details>

rocminfo --support: [rocminfo.txt](https://github.com/RadeonOpenCompute/ROCm/files/13467479/rocminfo.txt)

---

### 评论 #7 — xstraok (2023-12-06T03:14:59Z)

Exact same problem also happens on RX 6600 + Ryzen 5 7600. 
Happens when Blender 4.0 tries to load anything ROCm related, 

- has a 80% chance to instantly kernel panic, 
- 15% chance to kernel oops, 
- 5% chance to "stuck" 2 CPU cores and then completely freeze the system afterwards (but kernel is still alive).

This seems to only affect AMD CPUs, I don't see any Intel CPUs around here....

[dmesg.txt](https://github.com/RadeonOpenCompute/ROCm/files/13575375/dmesg.txt)
[rocminfo.txt](https://github.com/RadeonOpenCompute/ROCm/files/13575381/rocminfo.txt)

---

### 评论 #8 — xstraok (2023-12-13T08:43:08Z)

> I bisected this, resulting in https://lists.freedesktop.org/archives/amd-gfx/2023-October/100298.html

Tried this out, system no longer crashes, but blender does not see the GPU.

In dmesg, I get this:

 `[   35.561058] amdgpu: Failed to create process VM object`
 `[   35.564749] amdgpu: Failed to create process VM object`

---

### 评论 #9 — danielzgtg (2023-12-13T09:46:27Z)

@xstraok We are still waiting for AMD to reply to my thread on that mailing list.

I said in the commit message "Although [...] were working in v6.2 and ROCm 5.6, broke, and are not fixed by this revert," so blender not seeing the GPU is sadly expected. I would rather have a few programs (PyTorch, browsers, and games) work on my computer, than my entire computer freeze.

---

### 评论 #10 — napaalm (2023-12-13T09:58:24Z)

@kentrussell any update from Christian?

EDIT: I found out that there's an open issue about this bug on drm/amd (https://gitlab.freedesktop.org/drm/amd/-/issues/2991), so I pinged him [there](https://gitlab.freedesktop.org/drm/amd/-/issues/2991#note_2205612).

---

### 评论 #11 — danielzgtg (2023-12-13T13:11:30Z)

Interesting that their bisect finished on a different commit. I haven't gotten around to applying it yet, but does their `git revert 96c211f1f9ef82183493f4ceed4e347b52849149` solution (maybe start with a clean kernel source without my revert patch while doing this) fix the GPU problems for the people using blender and other frameworks here?

---

### 评论 #12 — danielzgtg (2023-12-22T12:54:46Z)

I found a workaround! I got things to work without crashing with `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.runpm=0 amdgpu.vm_update_mode=3"` in `/etc/default/grub`. I updated to ROCM 6.0.

Thank you @terryrankine for https://github.com/ROCm/ROCm/issues/2766#issuecomment-1867179386 . Btw, the "what is actually happening" might be explained by https://lists.freedesktop.org/archives/amd-gfx/2023-October/100322.html .

I've also noticed that I can reproduce `GCVM_L2_PROTECTION_FAULT_STATUS` if I tell ROCm to use the wrong GPU model. My GPU uses `HSA_OVERRIDE_GFX_VERSION=10.3.0`, but if I set `HSA_OVERRIDE_GFX_VERSION=11.0.0` or something, I get those errors. Docker is another environment where I get different errors in dmesg, so there seems to be a large userspace aspect to this bug (although userspace shouldn't be able to freeze kernelspace).

# Pytorch

Stable diffusion and LlamaIndex are working after recompiling pytorch-rocm and bitsandbytes-rocm. https://github.com/ROCmSoftwarePlatform/pytorch/issues/1340

# Hashcat

The Ubuntu repos' version doesn't work, as seen with `hashcat -b`. It might work if I tried recompiling it, but I do not have a use case to bother trying.

# llama.cpp

llama.cpp and gpt4all work after putting `target_compile_options(ggml-rocm PRIVATE --offload-arch=gfx1030)` in some CMakeLists.txt. Debug mode is now so slow (looks like #2625 and https://github.com/ROCm/ROCK-Kernel-Driver/issues/153 , when backtracing in gdb or with `AMD_LOG_LEVEL=5 HSA_ENABLE_SDMA=0` but this is an illusion) that it looks frozen, but release mode is somewhat fine. I am worried that the performance is not as good as it as before, because I was getting 47 tokens/s in April, and now it sometimes goes down to 30 tokens/s.

# OpenCL

clinfo doesn't freeze the computer anymore, however I haven't tested any OpenCL programs. Other peoples should test Blender, darktable, and DaVinci Resolve. I want to get into those programs and I have a few installed, but I didn't have enough time to get familiar with how to use them properly.

# Kernel

I will not close the issue yet. Blender and other apps still need to be tested by other people. Userspace should not be able to crash kernelspace with default options. This workaround apparently moves something to the CPU so it will slow things down, and the root cause needs to be addressed as someone mentioned on the mailing list.

---

### 评论 #13 — sofiageo (2023-12-22T16:44:05Z)

For me `vm_update_mode=3` made it worse, now also processes will stay stuck until I reset my PC. (Arch Linux + 5900x CPU + 5700xt GPU)

---

### 评论 #14 — road2react (2023-12-23T07:53:58Z)

@sofiageo which kernel version did you use ?

---

### 评论 #15 — xstraok (2023-12-23T08:08:59Z)

> I found a workaround! I got things to work without crashing with `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.runpm=0 amdgpu.vm_update_mode=3"` in `/etc/default/grub`. I updated to ROCM 6.0.

Sadly it didn't change anything in my case. Tried both stock kernel and patched kernel. Although I've noticed that on the patched kernel + ROCM 6.0, blender does not recognize the GPU, but this time there are no errors at all in dmesg. Downgrading to rocm 5.7 brought back the vm error message.

Linux-zen 6.6.7


---

### 评论 #16 — road2react (2023-12-23T08:26:18Z)

I added `amdgpu.runpm=0 amdgpu.vm_update_mode=3` to kernel cmdline, and it made things slower (GNOME overview animation becomes very laggy). Can't find any other differences.

On kernel version 6.6.8, with or without these kernel parameters, `clinfo` does not crash, no stuck processes, but Davinci Resolve does not work.

![image](https://github.com/ROCm/ROCm/assets/93143714/2f9a2856-627d-481f-938e-a5d7b3fcec70)


---

### 评论 #17 — sofiageo (2023-12-23T09:28:28Z)

> @sofiageo which kernel version did you use ?

I tried with both 6.6.7-zen and 6.6.8 - I get the same behaviour. I also noticed that large bar was not being used by my system because of a warning, I had to turn off CSM from BIOS.

Here is a sum of warnings / errors from journalctl

```
Dec 23 11:09:09 home kernel: CPU update of VM recommended only for large BAR system
Dec 23 11:09:09 home kernel: WARNING: CPU: 22 PID: 2764 at drivers/gpu/drm/amd/amdgpu/amdgpu_vm.c:2269 amdgpu_vm_make_compute+0x246/0x270 [amdgpu]
Dec 23 11:09:09 home kernel: CPU: 22 PID: 2764 Comm: hashcat.bin Tainted: G        W          6.6.8-arch1-1 #1 2ffcc416f976199fcae9446e8159d64f5aa7b1db

Dec 23 11:10:28 home kernel: amdgpu 0000:0d:00.0: amdgpu: bo 00000000cc5cdb22 va 0x0800000000-0x0800000001 conflict with 0x0800000000-0x0800000200
Dec 23 11:10:28 home kernel: amdgpu: Failed to map VA 0x800000000000 in vm. ret -22
Dec 23 11:10:28 home kernel: amdgpu: Failed to map bo to gpuvm
Dec 23 11:10:28 home kernel: BUG: kernel NULL pointer dereference, address: 0000000000000008
Dec 23 11:10:28 home kernel: #PF: supervisor read access in kernel mode
Dec 23 11:10:28 home kernel: #PF: error_code(0x0000) - not-present page
Dec 23 11:10:28 home kernel: note: blender[3503] exited with irqs disabled
Dec 23 11:10:28 home kernel: BUG: kernel NULL pointer dereference, address: 0000000000000001

```


---

### 评论 #18 — dominik-code (2023-12-23T16:36:30Z)

Can confirm. Issue also exists with rocm-6 + RX 5700XT on Manjaro with kernel 6.6.8 the opencl tool I use crashes when trying to select the GPU. `clinfo` works but any opencl workload crashes. Worked before with old version 5.6.1.

```
[   74.465236] amdgpu 0000:0b:00.0: amdgpu: bo 00000000b6ffc157 va 0x0800000000-0x0800000001 conflict with 0x0800000000-0x0800000200
[   74.465244] amdgpu: Failed to map VA 0x800000000000 in vm. ret -22
[   74.465247] amdgpu: Failed to map bo to gpuvm
[   74.471568] BUG: kernel NULL pointer dereference, address: 0000000000000008
[   74.471573] #PF: supervisor read access in kernel mode
[   74.471577] #PF: error_code(0x0000) - not-present page
[   74.471579] PGD 23edd4067 P4D 23edd4067 PUD 263f2f067 PMD 0 
[   74.471587] Oops: 0000 [#1] PREEMPT SMP NOPTI
[   74.471591] CPU: 8 PID: 3518 Comm: metashape Tainted: P           OE      6.6.8-2-MANJARO #1 146dce4c0b8863ad44f28ec2edb37ecbadc944c7
[   74.471596] Hardware name: System manufacturer System Product Name/PRIME X470-PRO, BIOS 6042 04/28/2022
[   74.471599] RIP: 0010:dma_resv_add_fence+0x47/0x1f0
[   74.471608] Code: 89 54 24 04 48 85 f6 74 21 48 8d 7e 38 b8 01 00 00 00 f0 0f c1 46 38 85 c0 0f 84 59 01 00 00 8d 50 01 09 c2 0f 88 5d 01 00 00 <49> 8b 46 08 48 3d c0 73 3b b3 0f 84 c9 00 00 00 48 3d 60 73 3b b3
[   74.471612] RSP: 0018:ffffacb4a343bcc8 EFLAGS: 00010246
[   74.471616] RAX: ffff9a0e0a170000 RBX: ffff9a0e0a170158 RCX: ffff9a0cc8b97b00
[   74.471619] RDX: 0000000000000003 RSI: 0000000000000000 RDI: ffff9a0e0a170158
[   74.471621] RBP: ffff9a0d708fd000 R08: 0000000000000002 R09: 0000000000000000
[   74.471624] R10: 0000000000000000 R11: 0000000000000000 R12: ffff9a0db99c1b38
[   74.471626] R13: ffff9a0db99c1b40 R14: 0000000000000000 R15: ffff9a0e0a170000
[   74.471629] FS:  00007f24719db1c0(0000) GS:ffff9a1baec00000(0000) knlGS:0000000000000000
[   74.471632] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   74.471635] CR2: 0000000000000008 CR3: 00000002039dc000 CR4: 0000000000f50ee0
[   74.471638] PKRU: 55555554
[   74.471641] Call Trace:
[   74.471645]  <TASK>
[   74.471651]  ? __die+0x23/0x70
[   74.471661]  ? page_fault_oops+0x171/0x4e0
[   74.471673]  ? exc_page_fault+0x7f/0x180
[   74.471682]  ? asm_exc_page_fault+0x26/0x30
[   74.471692]  ? dma_resv_add_fence+0x47/0x1f0
[   74.471701]  amdgpu_amdkfd_gpuvm_acquire_process_vm+0x212/0x530 [amdgpu 52694bdeee024ab6bd56aaaf8af75da9203d43d5]
[   74.472068]  kfd_process_device_init_vm+0xb0/0x320 [amdgpu 52694bdeee024ab6bd56aaaf8af75da9203d43d5]
[   74.472408]  kfd_ioctl_acquire_vm+0x89/0xc0 [amdgpu 52694bdeee024ab6bd56aaaf8af75da9203d43d5]
[   74.472750]  kfd_ioctl+0x3cc/0x4e0 [amdgpu 52694bdeee024ab6bd56aaaf8af75da9203d43d5]
[   74.473072]  ? __pfx_kfd_ioctl_acquire_vm+0x10/0x10 [amdgpu 52694bdeee024ab6bd56aaaf8af75da9203d43d5]
[   74.473399]  __x64_sys_ioctl+0x97/0xd0
[   74.473406]  do_syscall_64+0x60/0x90
[   74.473412]  ? srso_alias_return_thunk+0x5/0x7f
[   74.473417]  ? syscall_exit_to_user_mode+0x2b/0x40
[   74.473421]  ? srso_alias_return_thunk+0x5/0x7f
[   74.473424]  ? do_syscall_64+0x6c/0x90
[   74.473428]  ? syscall_exit_to_user_mode+0x2b/0x40
[   74.473431]  ? srso_alias_return_thunk+0x5/0x7f
[   74.473435]  ? do_syscall_64+0x6c/0x90
[   74.473439]  ? srso_alias_return_thunk+0x5/0x7f
[   74.473442]  ? do_syscall_64+0x6c/0x90
[   74.473447]  entry_SYSCALL_64_after_hwframe+0x6e/0xd8
[   74.473453] RIP: 0033:0x7f246fd2a3af
[   74.473477] Code: 00 48 89 44 24 18 31 c0 48 8d 44 24 60 c7 04 24 10 00 00 00 48 89 44 24 08 48 8d 44 24 20 48 89 44 24 10 b8 10 00 00 00 0f 05 <89> c2 3d 00 f0 ff ff 77 18 48 8b 44 24 18 64 48 2b 04 25 28 00 00
[   74.473480] RSP: 002b:00007ffee7400dc0 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
[   74.473484] RAX: ffffffffffffffda RBX: 00007ffee7400f30 RCX: 00007f246fd2a3af
[   74.473487] RDX: 00007ffee7400f30 RSI: 0000000040084b15 RDI: 0000000000000016
[   74.473490] RBP: 0000000040084b15 R08: 0000000000000013 R09: 0000000000000001
[   74.473492] R10: 00000000093dde50 R11: 0000000000000246 R12: 00000000093d9550
[   74.473495] R13: 0000000000000016 R14: 00007f23f44c37a0 R15: 0000000000000060
[   74.473502]  </TASK>
[   74.473505] Modules linked in: xt_CHECKSUM xt_MASQUERADE xt_conntrack ipt_REJECT nf_reject_ipv4 xt_tcpudp nft_compat nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nf_tables libcrc32c nfnetlink bridge stp llc cmac nls_utf8 cifs cifs_arc4 nls_ucs2_utils cifs_md4 dns_resolver fscache netfs mlx5_ib ib_uverbs macsec ib_core joydev mousedev usbhid qrtr squashfs uvcvideo videobuf2_vmalloc uvc videobuf2_memops snd_usb_audio videobuf2_v4l2 snd_usbmidi_lib videodev snd_ump snd_rawmidi videobuf2_common snd_seq_device mc intel_rapl_msr intel_rapl_common edac_mce_amd kvm_amd amdgpu kvm eeepc_wmi snd_hda_codec_realtek asus_wmi snd_hda_codec_generic irqbypass vfat ledtrig_audio sparse_keymap crct10dif_pclmul snd_hda_codec_hdmi fat platform_profile crc32_pclmul polyval_clmulni i8042 polyval_generic snd_hda_intel drm_exec serio asus_wmi_sensors gf128mul amdxcp snd_intel_dspcfg rfkill wmi_bmof mxm_wmi ghash_clmulni_intel asus_ec_sensors drm_buddy snd_intel_sdw_acpi sha512_ssse3 mlx5_core snd_hda_codec sha256_ssse3
[   74.473611]  gpu_sched drm_suballoc_helper sha1_ssse3 snd_hda_core drm_ttm_helper aesni_intel ttm snd_hwdep crypto_simd snd_pcm drm_display_helper mlxfw cryptd igb snd_timer psample cec snd sp5100_tco video i2c_algo_bit rapl acpi_cpufreq pcspkr soundcore tls i2c_piix4 ccp dca zenpower(OE) pci_hyperv_intf wmi gpio_amdpt gpio_generic mac_hid uinput zfs(POE) spl(OE) i2c_dev crypto_user fuse loop dm_mod bpf_preload ip_tables x_tables ext4 crc32c_generic crc16 mbcache jbd2 nvme crc32c_intel nvme_core sr_mod xhci_pci xhci_pci_renesas cdrom nvme_common
[   74.473685] CR2: 0000000000000008
[   74.473688] ---[ end trace 0000000000000000 ]---
[   74.473691] RIP: 0010:dma_resv_add_fence+0x47/0x1f0
[   74.473697] Code: 89 54 24 04 48 85 f6 74 21 48 8d 7e 38 b8 01 00 00 00 f0 0f c1 46 38 85 c0 0f 84 59 01 00 00 8d 50 01 09 c2 0f 88 5d 01 00 00 <49> 8b 46 08 48 3d c0 73 3b b3 0f 84 c9 00 00 00 48 3d 60 73 3b b3
[   74.473700] RSP: 0018:ffffacb4a343bcc8 EFLAGS: 00010246
[   74.473703] RAX: ffff9a0e0a170000 RBX: ffff9a0e0a170158 RCX: ffff9a0cc8b97b00
[   74.473706] RDX: 0000000000000003 RSI: 0000000000000000 RDI: ffff9a0e0a170158
[   74.473708] RBP: ffff9a0d708fd000 R08: 0000000000000002 R09: 0000000000000000
[   74.473711] R10: 0000000000000000 R11: 0000000000000000 R12: ffff9a0db99c1b38
[   74.473713] R13: ffff9a0db99c1b40 R14: 0000000000000000 R15: ffff9a0e0a170000
[   74.473716] FS:  00007f24719db1c0(0000) GS:ffff9a1baec00000(0000) knlGS:0000000000000000
[   74.473719] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   74.473722] CR2: 0000000000000008 CR3: 00000002039dc000 CR4: 0000000000f50ee0
[   74.473725] PKRU: 55555554
[   74.473727] note: metashape[3518] exited with irqs disabled
```



---

### 评论 #19 — jkcdarunday (2023-12-24T18:28:54Z)

Can confirm that this also happens on RX 7900 XTX + Ryzen 7950X on 6.6.8-arch1-1. Crashes when running blender and going to Edit -> Preferences. Also happens when running SVPManager. This leaves a zombie process that indefinitely blocks shutdown. 
```
[39435.607525] amdgpu 0000:03:00.0: amdgpu: bo 00000000da340e9d va 0x0800000000-0x0800000001 conflict with 0x0800000000-0x0800000840
[39435.607529] amdgpu: Failed to map VA 0x800000000000 in vm. ret -22
[39435.607530] amdgpu: Failed to map bo to gpuvm
[39435.613925] BUG: kernel NULL pointer dereference, address: 0000000000000008
[39435.613927] #PF: supervisor read access in kernel mode
[39435.613929] #PF: error_code(0x0000) - not-present page
[39435.613930] PGD 0 P4D 0 
[39435.613932] Oops: 0000 [#1] PREEMPT SMP NOPTI
[39435.613934] CPU: 30 PID: 178800 Comm: blender Tainted: G           OE      6.6.8-arch1-1 #1 2ffcc416f976199fcae9446e8159d64f5aa7b1db
[39435.613936] Hardware name: ASUS System Product Name/ROG CROSSHAIR X670E HERO, BIOS 1602 08/15/2023
[39435.613938] RIP: 0010:dma_resv_add_fence+0x47/0x1f0
[39435.613943] Code: 89 54 24 04 48 85 f6 74 21 48 8d 7e 38 b8 01 00 00 00 f0 0f c1 46 38 85 c0 0f 84 59 01 00 00 8d 50 01 09 c2 0f 88 5d 01 00 00 <49> 8b 46 08 48 3d 00 73 7b 9d 0f 84 c9 00 00 00 48 3d a0 72 7b 9d
[39435.613944] RSP: 0018:ffffc9001af23cf0 EFLAGS: 00010246
[39435.613946] RAX: ffff8883d36b8000 RBX: ffff8883d36b8158 RCX: 00000001ca242a1e
[39435.613947] RDX: 0000000000000003 RSI: 0000000000000000 RDI: ffff8883d36b8158
[39435.613948] RBP: ffff88837ceff000 R08: 0000000000000000 R09: 000000000003a5f0
[39435.613949] R10: 000000000003a5f0 R11: 0000000000000100 R12: ffff888113b27b38
[39435.613950] R13: ffff888113b27b40 R14: 0000000000000000 R15: ffff8883d36b8000
[39435.613951] FS:  00007f8b4b430000(0000) GS:ffff88903df80000(0000) knlGS:0000000000000000
[39435.613952] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[39435.613953] CR2: 0000000000000008 CR3: 0000000bfa7da000 CR4: 0000000000f50ee0
[39435.613955] PKRU: 55555554
[39435.613956] Call Trace:
[39435.613957]  <TASK>
[39435.613960]  ? __die+0x23/0x70
[39435.613964]  ? page_fault_oops+0x171/0x4e0
[39435.613968]  ? exc_page_fault+0x7f/0x180
[39435.613971]  ? asm_exc_page_fault+0x26/0x30
[39435.613976]  ? dma_resv_add_fence+0x47/0x1f0
[39435.613980]  amdgpu_amdkfd_gpuvm_acquire_process_vm+0x212/0x530 [amdgpu fd8186640f20c9957c4ed5bc533f74908ab57ec4]
[39435.614122]  kfd_process_device_init_vm+0xb0/0x320 [amdgpu fd8186640f20c9957c4ed5bc533f74908ab57ec4]
[39435.614245]  ? srso_alias_return_thunk+0x5/0x7f
[39435.614248]  kfd_ioctl_acquire_vm+0x89/0xc0 [amdgpu fd8186640f20c9957c4ed5bc533f74908ab57ec4]
[39435.614363]  kfd_ioctl+0x3c9/0x4e0 [amdgpu fd8186640f20c9957c4ed5bc533f74908ab57ec4]
[39435.614470]  ? __pfx_kfd_ioctl_acquire_vm+0x10/0x10 [amdgpu fd8186640f20c9957c4ed5bc533f74908ab57ec4]
[39435.614579]  __x64_sys_ioctl+0x94/0xd0
[39435.614582]  do_syscall_64+0x5d/0x90
[39435.614585]  ? do_syscall_64+0x6c/0x90
[39435.614587]  ? srso_alias_return_thunk+0x5/0x7f
[39435.614588]  ? do_syscall_64+0x6c/0x90
[39435.614590]  ? exc_page_fault+0x7f/0x180
[39435.614592]  entry_SYSCALL_64_after_hwframe+0x6e/0xd8
[39435.614595] RIP: 0033:0x7f8b5f92a3af
[39435.614614] Code: 00 48 89 44 24 18 31 c0 48 8d 44 24 60 c7 04 24 10 00 00 00 48 89 44 24 08 48 8d 44 24 20 48 89 44 24 10 b8 10 00 00 00 0f 05 <89> c2 3d 00 f0 ff ff 77 18 48 8b 44 24 18 64 48 2b 04 25 28 00 00
[39435.614615] RSP: 002b:00007fffcfe541c0 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
[39435.614617] RAX: ffffffffffffffda RBX: 00007fffcfe542b0 RCX: 00007f8b5f92a3af
[39435.614618] RDX: 00007fffcfe54330 RSI: 0000000040084b15 RDI: 000000000000000d
[39435.614619] RBP: 00007fffcfe54330 R08: 000000000000000b R09: 0000000000000008
[39435.614620] R10: 0000000000000001 R11: 0000000000000246 R12: 0000000040084b15
[39435.614621] R13: 000000000000000d R14: 00007f8acae29f10 R15: 00007f8b18e3a180
[39435.614624]  </TASK>
[39435.614625] Modules linked in: uinput rfcomm snd_seq_dummy snd_hrtimer snd_seq xt_nat xt_tcpudp veth xt_conntrack xt_MASQUERADE nf_conntrack_netlink iptable_nat xt_addrtype iptable_filter br_netfilter bridge stp llc wireguard curve25519_x86_64 libchacha20poly1305 chacha_x86_64 poly1305_x86_64 libcurve25519_generic libchacha ip6_udp_tunnel udp_tunnel ccm cmac algif_hash algif_skcipher af_alg overlay bnep btusb btrtl btintel btbcm btmtk snd_usb_audio bluetooth snd_usbmidi_lib snd_ump xpad mousedev snd_rawmidi joydev ecdh_generic apple_mfi_fastcharge ff_memless crc16 snd_seq_device intel_rapl_msr intel_rapl_common edac_mce_amd kvm_amd vfat fat kvm iwlmvm irqbypass crct10dif_pclmul crc32_pclmul mac80211 polyval_clmulni polyval_generic gf128mul ghash_clmulni_intel libarc4 sha512_ssse3 sha1_ssse3 eeepc_wmi asus_nb_wmi snd_hda_codec_hdmi aesni_intel asus_wmi iwlwifi ledtrig_audio crypto_simd sparse_keymap cryptd snd_hda_intel platform_profile i8042 snd_intel_dspcfg sp5100_tco snd_intel_sdw_acpi asus_ec_sensors rapl serio
[39435.614675]  intel_wmi_thunderbolt wmi_bmof cfg80211 thunderbolt snd_hda_codec pcspkr i2c_piix4 ccp ucsi_acpi snd_hda_core typec_ucsi igc rfkill snd_hwdep typec gpio_amdpt roles gpio_generic mac_hid nft_reject_inet nf_reject_ipv4 nf_reject_ipv6 nft_reject nft_masq nft_ct nft_chain_nat vboxnetflt(OE) nf_nat vboxnetadp(OE) nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 vboxdrv(OE) pkcs8_key_parser k10temp snd_aloop snd_pcm snd_timer snd soundcore v4l2loopback_dc(OE) nf_tables videodev mc i2c_dev loop fuse dm_mod nfnetlink ip_tables x_tables sr_mod cdrom hid_apple usbhid uas usb_storage amdgpu btrfs blake2b_generic i2c_algo_bit libcrc32c drm_ttm_helper crc32c_generic xor ttm raid6_pq drm_exec drm_suballoc_helper amdxcp drm_buddy gpu_sched nvme crc32c_intel drm_display_helper sha256_ssse3 nvme_core xhci_pci xhci_pci_renesas cec nvme_common video wmi
[39435.614721] CR2: 0000000000000008
[39435.614723] ---[ end trace 0000000000000000 ]---
[39435.614724] RIP: 0010:dma_resv_add_fence+0x47/0x1f0
[39435.614726] Code: 89 54 24 04 48 85 f6 74 21 48 8d 7e 38 b8 01 00 00 00 f0 0f c1 46 38 85 c0 0f 84 59 01 00 00 8d 50 01 09 c2 0f 88 5d 01 00 00 <49> 8b 46 08 48 3d 00 73 7b 9d 0f 84 c9 00 00 00 48 3d a0 72 7b 9d
[39435.614727] RSP: 0018:ffffc9001af23cf0 EFLAGS: 00010246
[39435.614729] RAX: ffff8883d36b8000 RBX: ffff8883d36b8158 RCX: 00000001ca242a1e
[39435.614730] RDX: 0000000000000003 RSI: 0000000000000000 RDI: ffff8883d36b8158
[39435.614731] RBP: ffff88837ceff000 R08: 0000000000000000 R09: 000000000003a5f0
[39435.614732] R10: 000000000003a5f0 R11: 0000000000000100 R12: ffff888113b27b38
[39435.614733] R13: ffff888113b27b40 R14: 0000000000000000 R15: ffff8883d36b8000
[39435.614734] FS:  00007f8b4b430000(0000) GS:ffff88903df80000(0000) knlGS:0000000000000000
[39435.614735] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[39435.614736] CR2: 0000000000000008 CR3: 0000000bfa7da000 CR4: 0000000000f50ee0
[39435.614737] PKRU: 55555554
[39435.614738] note: blender[178800] exited with irqs disabled
```

---

### 评论 #20 — road2react (2023-12-24T21:47:28Z)

I wonder if using `opencl-rusticl-mesa` vs `opencl-clover-mesa` makes a difference here:

- Kernel 6.1 lts with `opencl-clover-mesa`, `clinfo` runs properly, DaVinci Resolve shows the GPUs in the settings, but I cannot play videos in DaVinci Resolve.
- Kernel 6.1 lts with `opencl-rusticl-mesa`, `clinfo` runs properly, DaVinci Resolve works as expected
- Kernel 6.6.8 with `opencl-rusticl-mesa`, `clinfo` runs properly, but DaVinci Resolve would close with an error

![image](https://github.com/ROCm/ROCm/assets/93143714/8d0388c6-79bc-4427-94d1-cdf825068822)

All of these are done with ROCm 5.7.1, I haven't yet tested with ROCm 6. Also, I uninstalled `opencl-clover-mesa` to get DaVinci Resolve to use `opencl-rusticl-mesa`, with both installed, DaVinci Resolve seems to use `opencl-clover-mesa`

---

### 评论 #21 — OzzyHelix (2024-01-01T23:59:02Z)

this patch could fix it 
https://lists.freedesktop.org/archives/amd-gfx/2023-October/100298.html

---

### 评论 #22 — fee1-dead (2024-01-02T18:09:19Z)

(crossposted from drm/amd issue for anyone looking for a workaround)

I am on NixOS with Linux 6.6.8, with RX 7900 XT and Ryzen 9 7900x. I've applied the following patch, given rcrisostomo's bisected commit (`96c211f1f9ef82183493f4ceed4e347b52849149`):

```patch
diff --git a/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c b/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
index 62b205dac..efb05acea 100644
--- a/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
+++ b/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
@@ -330,12 +330,6 @@ static void kfd_init_apertures_vi(struct kfd_process_device *pdd, uint8_t id)
        pdd->gpuvm_limit =
                pdd->dev->kfd->shared_resources.gpuvm_size - 1;

-       /* dGPUs: the reserved space for kernel
-        * before SVM
-        */
-       pdd->qpd.cwsr_base = SVM_CWSR_BASE;
-       pdd->qpd.ib_base = SVM_IB_BASE;
-
        pdd->scratch_base = MAKE_SCRATCH_APP_BASE_VI();
        pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
 }
@@ -345,18 +339,18 @@ static void kfd_init_apertures_v9(struct kfd_process_device *pdd, uint8_t id)
        pdd->lds_base = MAKE_LDS_APP_BASE_V9();
        pdd->lds_limit = MAKE_LDS_APP_LIMIT(pdd->lds_base);

-       pdd->gpuvm_base = PAGE_SIZE;
+       /* Raven needs SVM to support graphic handle, etc. Leave the small
+        * reserved space before SVM on Raven as well, even though we don't
+        * have to.
+        * Set gpuvm_base and gpuvm_limit to CANONICAL addresses so that they
+        * are used in Thunk to reserve SVM.
+        */
+       pdd->gpuvm_base = SVM_USER_BASE;
        pdd->gpuvm_limit =
                pdd->dev->kfd->shared_resources.gpuvm_size - 1;

        pdd->scratch_base = MAKE_SCRATCH_APP_BASE_V9();
        pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
-
-       /*
-        * Place TBA/TMA on opposite side of VM hole to prevent
-        * stray faults from triggering SVM on these pages.
-        */
-       pdd->qpd.cwsr_base = pdd->dev->kfd->shared_resources.gpuvm_size;
 }

 int kfd_init_apertures(struct kfd_process *process)
@@ -413,6 +407,12 @@ int kfd_init_apertures(struct kfd_process *process)
                                        return -EINVAL;
                                }
                        }
+
+                       /* dGPUs: the reserved space for kernel
+                        * before SVM
+                        */
+                       pdd->qpd.cwsr_base = SVM_CWSR_BASE;
+                       pdd->qpd.ib_base = SVM_IB_BASE;
                }

                dev_dbg(kfd_device, "node id %u\n", id);
```

After applying this patch to 6.6.8 the issue is fixed for me, with Blender correctly recognizing my GPU and being able to render with Cycles.

---

### 评论 #23 — OzzyHelix (2024-01-02T18:15:27Z)

I will try applying the same patch to the zen kernel

---

### 评论 #24 — OzzyHelix (2024-01-02T19:18:52Z)

> (crossposted from drm/amd issue for anyone looking for a workaround)
> 
> I am on NixOS with Linux 6.6.8, with RX 7900 XT and Ryzen 9 7900x. I've applied the following patch, given rcrisostomo's bisected commit (`96c211f1f9ef82183493f4ceed4e347b52849149`):
> 
> ```diff
> diff --git a/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c b/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
> index 62b205dac..efb05acea 100644
> --- a/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
> +++ b/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
> @@ -330,12 +330,6 @@ static void kfd_init_apertures_vi(struct kfd_process_device *pdd, uint8_t id)
>         pdd->gpuvm_limit =
>                 pdd->dev->kfd->shared_resources.gpuvm_size - 1;
> 
> -       /* dGPUs: the reserved space for kernel
> -        * before SVM
> -        */
> -       pdd->qpd.cwsr_base = SVM_CWSR_BASE;
> -       pdd->qpd.ib_base = SVM_IB_BASE;
> -
>         pdd->scratch_base = MAKE_SCRATCH_APP_BASE_VI();
>         pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
>  }
> @@ -345,18 +339,18 @@ static void kfd_init_apertures_v9(struct kfd_process_device *pdd, uint8_t id)
>         pdd->lds_base = MAKE_LDS_APP_BASE_V9();
>         pdd->lds_limit = MAKE_LDS_APP_LIMIT(pdd->lds_base);
> 
> -       pdd->gpuvm_base = PAGE_SIZE;
> +       /* Raven needs SVM to support graphic handle, etc. Leave the small
> +        * reserved space before SVM on Raven as well, even though we don't
> +        * have to.
> +        * Set gpuvm_base and gpuvm_limit to CANONICAL addresses so that they
> +        * are used in Thunk to reserve SVM.
> +        */
> +       pdd->gpuvm_base = SVM_USER_BASE;
>         pdd->gpuvm_limit =
>                 pdd->dev->kfd->shared_resources.gpuvm_size - 1;
> 
>         pdd->scratch_base = MAKE_SCRATCH_APP_BASE_V9();
>         pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
> -
> -       /*
> -        * Place TBA/TMA on opposite side of VM hole to prevent
> -        * stray faults from triggering SVM on these pages.
> -        */
> -       pdd->qpd.cwsr_base = pdd->dev->kfd->shared_resources.gpuvm_size;
>  }
> 
>  int kfd_init_apertures(struct kfd_process *process)
> @@ -413,6 +407,12 @@ int kfd_init_apertures(struct kfd_process *process)
>                                         return -EINVAL;
>                                 }
>                         }
> +
> +                       /* dGPUs: the reserved space for kernel
> +                        * before SVM
> +                        */
> +                       pdd->qpd.cwsr_base = SVM_CWSR_BASE;
> +                       pdd->qpd.ib_base = SVM_IB_BASE;
>                 }
> 
>                 dev_dbg(kfd_device, "node id %u\n", id);
> ```
> 
> After applying this patch to 6.6.8 the issue is fixed for me, with Blender correctly recognizing my GPU and being able to render with Cycles.

Applying this patch to the Linux Zen Kernel version 6.6.8 makes blender work for me 

---

### 评论 #25 — OzzyHelix (2024-01-02T19:19:45Z)

if this can get merged into the linux kernel the issue should be resolved for a lot of folks

---

### 评论 #26 — desolatorxxl (2024-01-03T20:31:54Z)

> After applying this patch to 6.6.8 the issue is fixed for me, with Blender correctly recognizing my GPU and being able to render with Cycles.

Can confirm this as well on Gentoo with `sys-kernel/gentoo-kernel-6.6.8`.
To save the next poor Gentoo user from staring at their screen, questioning their sanity why the patch just won't apply, here is the patch with tabs instead of spaces :sweat_smile: 

```patch
diff --git a/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c b/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
index 62b205dac..efb05acea 100644
--- a/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
+++ b/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
@@ -330,12 +330,6 @@ static void kfd_init_apertures_vi(struct kfd_process_device *pdd, uint8_t id)
	pdd->gpuvm_limit =
		pdd->dev->kfd->shared_resources.gpuvm_size - 1;

-	/* dGPUs: the reserved space for kernel
-	 * before SVM
-	 */
-	pdd->qpd.cwsr_base = SVM_CWSR_BASE;
-	pdd->qpd.ib_base = SVM_IB_BASE;
-
	pdd->scratch_base = MAKE_SCRATCH_APP_BASE_VI();
	pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
 }
@@ -345,18 +339,18 @@ static void kfd_init_apertures_v9(struct kfd_process_device *pdd, uint8_t id)
	pdd->lds_base = MAKE_LDS_APP_BASE_V9();
	pdd->lds_limit = MAKE_LDS_APP_LIMIT(pdd->lds_base);

-	pdd->gpuvm_base = PAGE_SIZE;
+	/* Raven needs SVM to support graphic handle, etc. Leave the small
+	 * reserved space before SVM on Raven as well, even though we don't
+	 * have to.
+	 * Set gpuvm_base and gpuvm_limit to CANONICAL addresses so that they
+	 * are used in Thunk to reserve SVM.
+	 */
+	pdd->gpuvm_base = SVM_USER_BASE;
	pdd->gpuvm_limit =
		pdd->dev->kfd->shared_resources.gpuvm_size - 1;

	pdd->scratch_base = MAKE_SCRATCH_APP_BASE_V9();
	pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
-
-	/*
-	 * Place TBA/TMA on opposite side of VM hole to prevent
-	 * stray faults from triggering SVM on these pages.
-	 */
-	pdd->qpd.cwsr_base = pdd->dev->kfd->shared_resources.gpuvm_size;
 }

 int kfd_init_apertures(struct kfd_process *process)
@@ -413,6 +407,12 @@ int kfd_init_apertures(struct kfd_process *process)
					return -EINVAL;
				}
			}
+
+			/* dGPUs: the reserved space for kernel
+			 * before SVM
+			 */
+			pdd->qpd.cwsr_base = SVM_CWSR_BASE;
+			pdd->qpd.ib_base = SVM_IB_BASE;
		}

		dev_dbg(kfd_device, "node id %u\n", id);
```
(Just throw it into `/etc/portage/patches/sys-kernel/gentoo-kernel`)

---

### 评论 #27 — OzzyHelix (2024-01-03T20:33:46Z)

I had to compile the kernel on Arch to get it working that will work for the gentoo folks but having it fixed in the mainline linux kernel would fix it for everyone

---

### 评论 #28 — napaalm (2024-01-03T20:47:32Z)

> if this can get merged into the linux kernel the issue should be resolved for a lot of folks

@OzzyHelix if you look at the replies on that thread from AMD maintainers you'll read

> This revert is just a roundabout way of disabling CPU page table updates for compute VMs. But I don't think it really addresses the root cause. 

Evidently the AMD developers believe this is not the right solution, so let's leave it to them to write the proper fix to this bug. This patch is a good workaround we can continue to use in the meantime, but we can't expect to have it merged as is.

Instead, @kentrussell do you have any updates for us?

---

### 评论 #29 — OzzyHelix (2024-01-03T20:51:07Z)

> > if this can get merged into the linux kernel the issue should be resolved for a lot of folks
> 
> @OzzyHelix if you look at the replies on that thread from AMD maintainers you'll read
> 
> > This revert is just a roundabout way of disabling CPU page table updates for compute VMs. But I don't think it really addresses the root cause.
> 
> Evidently the AMD developers believe this is not the right solution, so let's leave it to them to write the proper fix to this bug. This patch is a good workaround we can continue to use in the meantime, but we can't pretend to have it merged.
> 
> Instead, @kentrussell do you have any updates for us?

I was not aware of this because I'm I don't know of these channels they talk in I'd be happy to take a look at these channels I just care the the problem is fixed so that I can continue to use blender on linux

---

### 评论 #30 — DGdev91 (2024-01-04T03:39:58Z)

> (crossposted from drm/amd issue for anyone looking for a workaround)

Just tested this on ArchLinux, using the linux-mainline linux package.

i had to adjust it a bit because the patch command was failing, but after that i can confirm the workaround works. clinfo gets still freezes sometimes, but when it does doesn't make the system crash

here is my version for that patch, if someone needs it


```
---- a/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
+++ b/drivers/gpu/drm/amd/amdkfd/kfd_flat_memory.c
@@ -330,11 +330,6 @@
 	pdd->gpuvm_limit =
 		pdd->dev->kfd->shared_resources.gpuvm_size - 1;
 
-	/* dGPUs: the reserved space for kernel
-	 * before SVM
-	 */
-	pdd->qpd.cwsr_base = SVM_CWSR_BASE;
-	pdd->qpd.ib_base = SVM_IB_BASE;
 
 	pdd->scratch_base = MAKE_SCRATCH_APP_BASE_VI();
 	pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
@@ -345,18 +340,18 @@
 	pdd->lds_base = MAKE_LDS_APP_BASE_V9();
 	pdd->lds_limit = MAKE_LDS_APP_LIMIT(pdd->lds_base);
 
-	pdd->gpuvm_base = PAGE_SIZE;
+	/* Raven needs SVM to support graphic handle, etc. Leave the small
+	* reserved space before SVM on Raven as well, even though we don't
+	* have to.
+	* Set gpuvm_base and gpuvm_limit to CANONICAL addresses so that they
+	* are used in Thunk to reserve SVM.
+	*/
+	pdd->gpuvm_base = SVM_USER_BASE;
 	pdd->gpuvm_limit =
 		pdd->dev->kfd->shared_resources.gpuvm_size - 1;
 
 	pdd->scratch_base = MAKE_SCRATCH_APP_BASE_V9();
 	pdd->scratch_limit = MAKE_SCRATCH_APP_LIMIT(pdd->scratch_base);
-
-	/*
-	 * Place TBA/TMA on opposite side of VM hole to prevent
-	 * stray faults from triggering SVM on these pages.
-	 */
-	pdd->qpd.cwsr_base = pdd->dev->kfd->shared_resources.gpuvm_size;
 }
 
 int kfd_init_apertures(struct kfd_process *process)
@@ -413,6 +408,12 @@
 					return -EINVAL;
 				}
 			}
+			
+			/* dGPUs: the reserved space for kernel
+			* before SVM
+			*/
+			pdd->qpd.cwsr_base = SVM_CWSR_BASE;
+			pdd->qpd.ib_base = SVM_IB_BASE;
 		}
 
 		dev_dbg(kfd_device, "node id %u\n", id);

```

---

### 评论 #31 — kentrussell (2024-01-04T13:46:48Z)

It's always fun, because we've got multiple locations for bug reports depending on the component. Since the kernel is shared between ROCm and amdgpu-pro, we've got the ROCm side here (and in the ROCK-driver subrepo), and we have gitlab for amdgpu-pro. The actual discussion was happening on the amdgfx mailing list (https://lists.freedesktop.org/mailman/listinfo/amd-gfx , you can subscribe there to get emails on that list, which is where the patches go).

Note that on the Gitlab ticket, the patch was regressed to a patch from Jay Cornwall about moving the TBA/TVA. We just reverted that yesterday (https://lists.freedesktop.org/archives/amd-gfx/2024-January/102810.html). 
Can you try to revert that patch and see if that fixes it? We moved the TBA/TVA because there were some possible conditions where you could cause some issues using a bad low address, so we moved it higher to make it to make it less likely to get hit. But we're seeing more issues from that, so try to apply that revert and see if that fixes it. Let me know!

---

### 评论 #32 — OzzyHelix (2024-01-04T20:36:56Z)

> It's always fun, because we've got multiple locations for bug reports depending on the component. Since the kernel is shared between ROCm and amdgpu-pro, we've got the ROCm side here (and in the ROCK-driver subrepo), and we have gitlab for amdgpu-pro. The actual discussion was happening on the amdgfx mailing list (https://lists.freedesktop.org/mailman/listinfo/amd-gfx , you can subscribe there to get emails on that list, which is where the patches go).
> 
> Note that on the Gitlab ticket, the patch was regressed to a patch from Jay Cornwall about moving the TBA/TVA. We just reverted that yesterday (https://lists.freedesktop.org/archives/amd-gfx/2024-January/102810.html). Can you try to revert that patch and see if that fixes it? We moved the TBA/TVA because there were some possible conditions where you could cause some issues using a bad low address, so we moved it higher to make it to make it less likely to get hit. But we're seeing more issues from that, so try to apply that revert and see if that fixes it. Let me know!

from what I can gather this issue should be made known to the Linux Kernel maintainers or to AMD so that it can be fixed. its frustrating that this bug has persisted for as long as it has because it has limited what I can do with my hardware due to the bug. I just care that its fixed for everyone so that people can use blender and rocm without issue

---

### 评论 #33 — kentrussell (2024-01-04T21:10:20Z)

The maintainers watch gitlab far more closely, so that's the best way to get the amdgpu-side of things seen more effectively. Normally I'll try to cross-reference the two where possible, but opening a ticket on gitlab tends to go well for amdgpu-specific issues (like memory management, etc). Github here is good for KFD-specific, but the separation is suboptimal (to say the least)

---

### 评论 #34 — kouta-kun (2024-01-05T01:16:19Z)

I applied @fee1-dead 's patch on the gitlab issue to Kernel Version 6.6.9 and while it does fix initialization and stops the system from hanging, it still crashes on trying to render:
https://pastebin.com/jatcc69d

Also gitlab detects this comment as spam and won't let me comment :P 

---

### 评论 #35 — xstraok (2024-01-05T02:09:25Z)

Tried the patch, everything works perfectly well! Only problem is when trying to use the integrated gpu and dedicated gpu at the same time, blender crashes (page fault in dmesg), but I feel like that's an unrelated issue.

Edit: After additional testing, blender seems to crash when trying to render complex scenes. Rendering the default scene works though. This error seems to be related to blender/HIP.
`blender: /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_memory.cpp:2194: hipError_t ihipGetMemcpyParam3DCommand(amd::Command*&, const HIP_MEMCPY3D*, hip::Stream*): Assertion false && "ShouldNotReachHere()"' failed.
zsh: IOT instruction (core dumped)`

---

### 评论 #36 — kentrussell (2024-01-05T14:02:35Z)

Which version of Blender are you using where you see that crash? Blender had an issue when doing iGPU+dGPU that we raised a PR for (https://projects.blender.org/blender/blender/pulls/110512). It's apparently resolved in v4.0, according to some internal tickets.

---

### 评论 #37 — xstraok (2024-01-05T14:37:38Z)

Using Blender 4.0. iGPU+dGPU rendering is broken, dGPU only breaks at complex scenes, but renders the default cube with no problems. Same results for viewport, and final rendering. I'll do more testing soon

---

### 评论 #38 — kentrussell (2024-01-05T14:55:59Z)

Good to know. I'll also relay that in our internal ticket as well. I don't have that system config available to try out, so I'm going off of the internal tickets that I can find with the same issues to try to find some commonality.

---

### 评论 #39 — GZGavinZhao (2024-01-05T15:30:04Z)

I applied the mentioned patch on Solus's 6.6.9 [kernel](https://github.com/getsolus/linux). Now Blender can detect my GPU (`hipInit` no longer fails), but I get a SIGSEV error when trying to do any GPU rendering with cycles. The following crash log is obtained when trying to render the BMW27 example with cycles GPU compute. 
<details>
<summary>gdb</summary>

```
#0  0x00007f98cdd481ac in amd::HostQueue::Thread::vdev (this=0x128) at /home/build/YPKG/root/rocm-clr/build/clr-rocm-6.0.0/rocclr/platform/commandqueue.hpp:190
#1  amd::HostQueue::vdev (this=0x0) at /home/build/YPKG/root/rocm-clr/build/clr-rocm-6.0.0/rocclr/platform/commandqueue.hpp:240
#2  amd::Command::enqueue (this=this@entry=0x7f98ffdfe298) at /home/build/YPKG/root/rocm-clr/build/clr-rocm-6.0.0/rocclr/platform/command.cpp:362
#3  0x00007f98cdb9c342 in ihipMemcpyCmdEnqueue (isAsync=false, command=<optimized out>) at /home/build/YPKG/root/rocm-clr/build/clr-rocm-6.0.0/hipamd/src/hip_memory.cpp:2205
#4  ihipMemcpyParam3D (pCopy=pCopy@entry=0x7f98ffdfd130, stream=<optimized out>, stream@entry=0x0, isAsync=isAsync@entry=false) at /home/build/YPKG/root/rocm-clr/build/clr-rocm-6.0.0/hipamd/src/hip_memory.cpp:2310
#5  0x00007f98cdba9bb1 in hipDrvMemcpy2DUnaligned (pCopy=0x7f98ffdfd950) at /home/build/YPKG/root/rocm-clr/build/clr-rocm-6.0.0/hipamd/src/hip_memory.cpp:3965
#6  0x000055dabdc6de49 in ccl::HIPDevice::tex_alloc (this=0x7f97b9bf8a00, mem=...) at /home/build/YPKG/root/blender/build/blender-4.0.2/intern/cycles/device/hip/device_impl.cpp:789
#7  0x000055dabdab46e4 in ccl::ImageManager::device_load_image (this=0x7f97b98af280, device=0x7f97b9bf8a00, scene=0x7f97b9b1b800, slot=2, progress=<optimized out>)
    at /home/build/YPKG/root/blender/build/blender-4.0.2/intern/cycles/scene/image.cpp:820
#8  0x000055dabe22d880 in std::function<void ()>::operator()() const (this=0x7f98ffdfe298) at /usr/bin/../lib64/gcc/x86_64-solus-linux/13/../../../../include/c++/13/bits/std_function.h:591
#9  tbb::detail::d2::(anonymous namespace)::task_ptr_or_nullptr<std::function<void ()> const&>(std::function<void ()> const&) (f=...) at /usr/include/tbb/../oneapi/tbb/task_group.h:135
#10 tbb::detail::d1::function_task<std::function<void ()> >::execute(tbb::detail::d1::execution_data&) (this=0x7f9933acf500, ed=...) at /usr/include/tbb/../oneapi/tbb/task_group.h:466
#11 0x00007f9964828d83 in ?? () from /usr/lib64/libtbb.so.12
#12 0x00007f996482af62 in ?? () from /usr/lib64/libtbb.so.12
#13 0x00007f996429a10a in start_thread (arg=<optimized out>) at pthread_create.c:444
#14 0x00007f9964327a8c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:78
```

</details>

When loggin with `AMD_LOG_LEVEL=1`, I noticed that `hsa_amd_pointer_info()` returns a NULL address:
<details>
<summary>log with AMD_LOG_LEVEL=1</summary>

```
Switching to fully guarded memory allocator.
Blender 4.0.2
argv[0] = blender
argv[1] = --debug
argv[2] = --debug-cycles
Read prefs: "/home/gavinzhao/.config/blender/4.0/config/userpref.blend"
Read blend: "/home/gavinzhao/Downloads/blender-tests/BMW27.blend"
Warning: region type 4 missing in space type "Info" (id: 7) - removing region
I0105 10:21:13.161340  3022 device.cpp:37] HIPEW initialization succeeded
I0105 10:21:13.161379  3022 device.cpp:39] Found precompiled kernels
I0105 10:21:13.176532  3022 device.cpp:197] Device has compute preemption or is not used for display.
I0105 10:21:13.176550  3022 device.cpp:201] Added device "AMD Radeon RX 6600M" with id "HIP_AMD Radeon RX 6600M_0000:03:00".
I0105 10:21:16.216749  3105 device.cpp:541] Mapped host memory limit set to 62,987,644,928 bytes. (58.66G)
I0105 10:21:16.217029  3105 device_impl.cpp:63] Using AVX2 CPU kernels.
I0105 10:21:16.642376  3105 sync.cpp:295] Total time spent synchronizing data: 0.268328
I0105 10:21:16.645419  3076 colorspace.cpp:145] Colorspace sRGB is sRGB
:1:rocdevice.cpp            :3229: 0256155438 us: [pid:3022  tid:0x7fd1de9fd680] hsa_amd_pointer_info() failed
:1:rocdevice.cpp            :3229: 0256158431 us: [pid:3022  tid:0x7fd1de9fd680] hsa_amd_pointer_info() failed
```

</details>

This is more obvious when logging with `AMD_LOG_LEVEL=4`, though interestingly with this logging level Blender no longer SIGSEV, it just treats it as if the GPU doesn't have enough memory.
<details>
<summary>log with AMD_LOG_LEVEL=4</summary>

```
Switching to fully guarded memory allocator.
Blender 4.0.2
argv[0] = blender
argv[1] = --debug
argv[2] = --debug-cycles
Read prefs: "/home/gavinzhao/.config/blender/4.0/config/userpref.blend"
Read blend: "/home/gavinzhao/Downloads/blender-tests/BMW27.blend"
Warning: region type 4 missing in space type "Info" (id: 7) - removing region
I0105 10:22:03.095731  3158 device.cpp:37] HIPEW initialization succeeded
I0105 10:22:03.095764  3158 device.cpp:39] Found precompiled kernels
:3:rocdevice.cpp            :445 : 0302603870 us: [pid:3158  tid:0x7fbd2fc58900] Initializing HSA stack.
:3:rocdevice.cpp            :211 : 0302616389 us: [pid:3158  tid:0x7fbd2fc58900] Numa selects cpu agent[0]=0x7fbd2cdf7800(fine=0x7fbce5f0dc40,coarse=0x7fbce5f0dec0) for gpu agent=0x7fbcd2a10400 CPU<->GPU XGMI=0
:3:rocdevice.cpp            :1715: 0302617347 us: [pid:3158  tid:0x7fbd2fc58900] Gfx Major/Minor/Stepping: 10/3/2
:3:rocdevice.cpp            :1717: 0302617357 us: [pid:3158  tid:0x7fbd2fc58900] HMM support: 0, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1719: 0302617366 us: [pid:3158  tid:0x7fbd2fc58900] Max SDMA Read Mask: 0x3, Max SDMA Write Mask: 0x3
:4:rocdevice.cpp            :2099: 0302617450 us: [pid:3158  tid:0x7fbd2fc58900] Allocate hsa host memory 0x7fbd16749000, size 0x38
:4:rocdevice.cpp            :2099: 0302618022 us: [pid:3158  tid:0x7fbd2fc58900] Allocate hsa host memory 0x7fbbc1200000, size 0x101000
:4:rocdevice.cpp            :2099: 0302618487 us: [pid:3158  tid:0x7fbd2fc58900] Allocate hsa host memory 0x7fbbc1000000, size 0x101000
:4:runtime.cpp              :83  : 0302618515 us: [pid:3158  tid:0x7fbd2fc58900] init
:3:hip_context.cpp          :48  : 0302618520 us: [pid:3158  tid:0x7fbd2fc58900] Direct Dispatch: 1
:3:hip_context.cpp          :142 : 0302618552 us: [pid:3158  tid:0x7fbd2fc58900]  hipInit ( 0 ) 
:3:hip_context.cpp          :148 : 0302618558 us: [pid:3158  tid:0x7fbd2fc58900] hipInit: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :637 : 0302618576 us: [pid:3158  tid:0x7fbd2fc58900]  hipGetDeviceCount ( 0x7ff,c4a,275,70c ) 
:3:hip_device_runtime.cpp   :639 : 0302618583 us: [pid:3158  tid:0x7fbd2fc58900] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device.cpp           :238 : 0302618590 us: [pid:3158  tid:0x7fbd2fc58900]  hipDeviceGetName ( 0x7ff,c4a,275,7e0, 256, 0 ) 
:3:hip_device.cpp           :258 : 0302618596 us: [pid:3158  tid:0x7fbd2fc58900] hipDeviceGetName: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0302618604 us: [pid:3158  tid:0x7fbd2fc58900]  hipDeviceGetAttribute ( 0x7ff,c4a,275,740, 23, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0302618610 us: [pid:3158  tid:0x7fbd2fc58900] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0302618617 us: [pid:3158  tid:0x7fbd2fc58900]  hipDeviceGetAttribute ( 0x7ff,c4a,275,720, 61, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0302618623 us: [pid:3158  tid:0x7fbd2fc58900] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0302618630 us: [pid:3158  tid:0x7fbd2fc58900]  hipDeviceGetAttribute ( 0x7ff,c4a,275,710, 69, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0302618636 us: [pid:3158  tid:0x7fbd2fc58900] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0302618642 us: [pid:3158  tid:0x7fbd2fc58900]  hipDeviceGetAttribute ( 0x7ff,c4a,275,714, 67, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0302618647 us: [pid:3158  tid:0x7fbd2fc58900] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0302618653 us: [pid:3158  tid:0x7fbd2fc58900]  hipDeviceGetAttribute ( 0x7ff,c4a,275,718, 68, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0302618660 us: [pid:3158  tid:0x7fbd2fc58900] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0302618669 us: [pid:3158  tid:0x7fbd2fc58900]  hipDeviceGetAttribute ( 0x7ff,c4a,275,6ec, 18, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0302618675 us: [pid:3158  tid:0x7fbd2fc58900] hipDeviceGetAttribute: Returned hipSuccess : 
I0105 10:22:03.110661  3158 device.cpp:197] Device has compute preemption or is not used for display.
I0105 10:22:03.110672  3158 device.cpp:201] Added device "AMD Radeon RX 6600M" with id "HIP_AMD Radeon RX 6600M_0000:03:00".
:3:hip_context.cpp          :142 : 0305305273 us: [pid:3158  tid:0x7fbbb6579680]  hipInit ( 0 ) 
:3:hip_context.cpp          :148 : 0305305290 us: [pid:3158  tid:0x7fbbb6579680] hipInit: Returned hipSuccess : 
:3:hip_device.cpp           :173 : 0305305307 us: [pid:3158  tid:0x7fbbb6579680]  hipDeviceGet ( 0x7fb,bb5,5c2,3f8, 0 ) 
:3:hip_device.cpp           :175 : 0305305313 us: [pid:3158  tid:0x7fbbb6579680] hipDeviceGet: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0305305324 us: [pid:3158  tid:0x7fbbb6579680]  hipDeviceGetAttribute ( 0x7fb,bb6,574,4b4, 3, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0305305332 us: [pid:3158  tid:0x7fbbb6579680] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0305305338 us: [pid:3158  tid:0x7fbbb6579680]  hipDeviceGetAttribute ( 0x7fb,bb5,5c2,410, 82, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0305305344 us: [pid:3158  tid:0x7fbbb6579680] hipDeviceGetAttribute: Returned hipSuccess : 
I0105 10:22:05.797335  3240 device.cpp:541] Mapped host memory limit set to 62,987,644,928 bytes. (58.66G)
:3:hip_context.cpp          :152 : 0305305373 us: [pid:3158  tid:0x7fbbb6579680]  hipCtxCreate ( 0x7fb,bb5,5c2,400, 24, 0 ) 
:3:hip_context.cpp          :164 : 0305305381 us: [pid:3158  tid:0x7fbbb6579680] hipCtxCreate: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0305305386 us: [pid:3158  tid:0x7fbbb6579680]  hipDeviceGetAttribute ( 0x7fb,bb6,574,4b8, 23, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0305305394 us: [pid:3158  tid:0x7fbbb6579680] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :163 : 0305305400 us: [pid:3158  tid:0x7fbbb6579680]  hipDeviceGetAttribute ( 0x7fb,bb6,574,4b0, 61, 0 ) 
:3:hip_device_runtime.cpp   :448 : 0305305407 us: [pid:3158  tid:0x7fbbb6579680] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_context.cpp          :239 : 0305305412 us: [pid:3158  tid:0x7fbbb6579680]  hipCtxPopCurrent ( char array:<null> ) 
:3:hip_context.cpp          :252 : 0305305418 us: [pid:3158  tid:0x7fbbb6579680] hipCtxPopCurrent: Returned hipSuccess : 
I0105 10:22:05.797633  3240 device_impl.cpp:63] Using AVX2 CPU kernels.
:3:hip_context.cpp          :256 : 0305305861 us: [pid:3158  tid:0x7fbbb6579680]  hipCtxPushCurrent ( context:0x7fb,d15,fe5,d00 ) 
:3:hip_context.cpp          :266 : 0305305871 us: [pid:3158  tid:0x7fbbb6579680] hipCtxPushCurrent: Returned hipSuccess : 
:3:hip_stream.cpp           :353 : 0305305879 us: [pid:3158  tid:0x7fbbb6579680]  hipStreamCreateWithFlags ( 0x7fb,bb5,801,fe0, 1 ) 
:3:rocdevice.cpp            :2768: 0305305889 us: [pid:3158  tid:0x7fbbb6579680] number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
:3:rocdevice.cpp            :2846: 0305311204 us: [pid:3158  tid:0x7fbbb6579680] created hardware queue 0x7fbd11443000 with size 16384 with priority 1, cooperative: 0
:3:rocdevice.cpp            :2938: 0305311220 us: [pid:3158  tid:0x7fbbb6579680] acquireQueue refCount: 0x7fbd11443000 (1)
:4:rocdevice.cpp            :2099: 0305311649 us: [pid:3158  tid:0x7fbbb6579680] Allocate hsa host memory 0x7fbbaae00000, size 0x100000
:3:devprogram.cpp           :2686: 0305461737 us: [pid:3158  tid:0x7fbbb6579680] Using Code Object V5.
:3:hip_stream.cpp           :359 : 0305470658 us: [pid:3158  tid:0x7fbbb6579680] hipStreamCreateWithFlags: Returned hipSuccess : stream:0x7fb,bb5,821,380
:3:hip_context.cpp          :239 : 0305470672 us: [pid:3158  tid:0x7fbbb6579680]  hipCtxPopCurrent ( char array:<null> ) 
:3:hip_context.cpp          :252 : 0305470681 us: [pid:3158  tid:0x7fbbb6579680] hipCtxPopCurrent: Returned hipSuccess : 
I0105 10:22:06.230752  3240 sync.cpp:295] Total time spent synchronizing data: 0.267369
I0105 10:22:06.234824  3209 colorspace.cpp:145] Colorspace sRGB is sRGB
:3:hip_context.cpp          :256 : 0305745182 us: [pid:3158  tid:0x7fbce550b680]  hipCtxPushCurrent ( context:0x7fb,d15,fe5,d00 ) 
:3:hip_context.cpp          :266 : 0305745198 us: [pid:3158  tid:0x7fbce550b680] hipCtxPushCurrent: Returned hipSuccess : 
:3:hip_context.cpp          :256 : 0305745209 us: [pid:3158  tid:0x7fbce550b680]  hipCtxPushCurrent ( context:0x7fb,d15,fe5,d00 ) 
:3:hip_context.cpp          :266 : 0305745219 us: [pid:3158  tid:0x7fbce550b680] hipCtxPushCurrent: Returned hipSuccess : 
:3:hip_memory.cpp           :764 : 0305745239 us: [pid:3158  tid:0x7fbce550b680]  hipMemGetInfo ( 0x7fb,ce5,509,7d8, 0x7fb,ce5,509,7e0 ) 
:3:hip_memory.cpp           :788 : 0305745254 us: [pid:3158  tid:0x7fbce550b680] hipMemGetInfo: Returned hipSuccess : 
:3:hip_context.cpp          :239 : 0305745262 us: [pid:3158  tid:0x7fbce550b680]  hipCtxPopCurrent ( char array:<null> ) 
:3:hip_context.cpp          :252 : 0305745272 us: [pid:3158  tid:0x7fbce550b680] hipCtxPopCurrent: Returned hipSuccess : 
:3:hip_context.cpp          :256 : 0305745279 us: [pid:3158  tid:0x7fbce550b680]  hipCtxPushCurrent ( context:0x7fb,d15,fe5,d00 ) 
:3:hip_context.cpp          :266 : 0305745288 us: [pid:3158  tid:0x7fbce550b680] hipCtxPushCurrent: Returned hipSuccess : 
:3:hip_memory.cpp           :586 : 0305753341 us: [pid:3158  tid:0x7fbce550b680]  hipMalloc ( 0x7fb,ce5,509,7e8, 1536000 ) 
:4:rocdevice.cpp            :2227: 0305753592 us: [pid:3158  tid:0x7fbce550b680] Allocate hsa device memory 0x7fbb93400000, size 0x177000
:3:rocdevice.cpp            :2266: 0305753600 us: [pid:3158  tid:0x7fbce550b680] device=0x7fbcf905a000, freeMem_ = 0x1fee89000
:3:hip_memory.cpp           :588 : 0305753633 us: [pid:3158  tid:0x7fbce550b680] hipMalloc: Returned hipSuccess : 0x7fb,b93,400,000: duration: 292 us
:3:hip_context.cpp          :239 : 0305753643 us: [pid:3158  tid:0x7fbce550b680]  hipCtxPopCurrent ( char array:<null> ) 
:3:hip_context.cpp          :252 : 0305753649 us: [pid:3158  tid:0x7fbce550b680] hipCtxPopCurrent: Returned hipSuccess : 
:3:hip_memory.cpp           :3961: 0305753656 us: [pid:3158  tid:0x7fbce550b680]  hipDrvMemcpy2DUnaligned ( 0x7fb,ce5,509,950 ) 
:1:rocdevice.cpp            :3229: 0305753664 us: [pid:3158  tid:0x7fbce550b680] hsa_amd_pointer_info() failed
:3:rocdevice.cpp            :2768: 0305753673 us: [pid:3158  tid:0x7fbce550b680] number of allocated hardware queues with low priority: 0, with normal priority: 1, with high priority: 0, maximum per priority is: 4
:3:rocdevice.cpp            :2846: 0305755944 us: [pid:3158  tid:0x7fbce550b680] created hardware queue 0x7fbd11410000 with size 16384 with priority 1, cooperative: 0
:3:rocdevice.cpp            :2938: 0305755954 us: [pid:3158  tid:0x7fbce550b680] acquireQueue refCount: 0x7fbd11410000 (1)
:4:rocdevice.cpp            :2099: 0305756323 us: [pid:3158  tid:0x7fbce550b680] Allocate hsa host memory 0x7fbb92600000, size 0x100000
:1:rocdevice.cpp            :3229: 0305756396 us: [pid:3158  tid:0x7fbce550b680] hsa_amd_pointer_info() failed
:3:hip_memory.cpp           :3965: 0305756402 us: [pid:3158  tid:0x7fbce550b680] hipDrvMemcpy2DUnaligned: Returned hipErrorOutOfMemory : 
Out of memory in hipDrvMemcpy2DUnaligned(&param) (intern/cycles/device/hip/device_impl.cpp:789)

Refer to the Cycles GPU rendering documentation for possible solutions:
https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
```

</details>

This is with ROCm 6.0. Tested with both Solus' version of Blender 4.0.2 and the official Blender 4.0.2 binaries.

Edit: on the GitLab ticket someone mentioned that this crash only appears when a GPU is involved, but this crash still occurs when running headless Blender: `blender -b BMW27.blend -f 0 -- --cycles-device HIP`

---

### 评论 #40 — ofekd (2024-01-08T15:53:42Z)

Davinci Resolve is solved for me by applying the patch on 6.6.10, Radeon VII

https://gitlab.freedesktop.org/mesa/mesa/-/issues/10303

---

### 评论 #41 — GZGavinZhao (2024-01-09T02:34:29Z)

There seems to be a wide variety of issues appearing with ROCm 5.5+, Blender, and the kernel, so here is what I've gathered. Hopefully this will help guide people to some existing solutions.

1. You do something and your entire computer freezes
    - Kernel >= 6.6: you're here, apply the revert patch mentioned above
    - Else: open an issue
2. Blender cannot even find HIP (hipInit failed)
    - Kernel >= 6.6: you're here, apply the revert patch mentioned above
    - ROCm >= 6: if neither `libamdhip64.so.5` nor `libamdhip64.so` exists on your computer (usually at `$ROCM_PATH/lib64` or `$ROCM_PATH/lib`), try installing the package that provides that file or manually create a symlink to `libamdhip64.so.6`
    - Else: open an issue
3. Your whatever program (Blender, PyTorch, etc.) can find and select your GPU but crashes when running/rendering
    - ROCm >= 6:
      - SIGSEV, assertion error, "ShouldNotReachHere", "HIP out of memory": 
          - Blender: try any Blender version that contains commit [d2e91fb](https://projects.blender.org/blender/blender/commit/d2e91fb0d72fe565e6fcab9a1c071dce83aca0db), as of 2024-01-08 the official daily builds provides 4.0.3 RC which contains the commit.
          - Any other software: use whatever version that contains support for HIP 6.0. This issue is mostly caused by a breaking change in the `hipMemoryType` enum.
      - SIGABORT, GPU memory access fault, `dmesg` shows `GCVM_L2_PROTECTION_FAULT_STATUS`: 
          - Blender: the Blender daily builds mentioned above also fix this problem, but this issue is more severe than above because the patch doesn't fix this issue with ROCm 6; through my investigation it seems like the only reason the official binaries work is because the fatbins are compiled with ROCm 5.5
    - ROCm < 6: 
       - Blender: try the 4.0.3 RC daily builds; if that doesn't work, open an issue

---

### 评论 #42 — ericek111 (2024-01-15T10:27:46Z)

I can confirm, applying the patch https://patchwork.freedesktop.org/patch/573129/ to Linux 6.7 (cachyos, Arch) makes OpenCL apps (such as `clinfo`) and ROCm (Stable Diffusion) behave properly on my RX 6700 XT.

---

### 评论 #43 — Headcrabed (2024-01-15T14:12:20Z)

> I can confirm, applying the patch https://patchwork.freedesktop.org/patch/573129/ to Linux 6.7 (cachyos, Arch) makes OpenCL apps (such as `clinfo`) and ROCm (Stable Diffusion) behave properly on my RX 6700 XT.

As discussed in the link you provided, this patch is just to hide the problem, not fix it. Felix said a new patch would be created to properly fix this problem.

---

### 评论 #44 — danielzgtg (2024-01-19T20:14:00Z)

I am currently downgraded to `Linux daniel-desktop3 6.5.0-14-generic #14-Ubuntu SMP PREEMPT_DYNAMIC Tue Nov 14 14:59:49 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux`, `Package: linux-image-generic Version: 6.5.0.14.16`. "Kernel >= 6.6" is false for me so perhaps that's why it still works for me. llama.cpp and Stable Diffusion are working with a custom PyTorch build on ROCm 6.

The Blender headless benchmark works. The actual Blender GUI crashes, and this seems related to the compute-graphics interop.

I would try the other patch, but I'm in the middle of a lot of work. A quick skim tells me it is more ambitious and tries to fix a deeper problem. This is contrasted with mine, which more or less seems to just disable the host-visible compute memory feature. By the way, the 6.5.0 kernel I'm using now is completely unpatched and works for my pytorch use case. I'm concerned about the comments in the thread about refcount stability, but I might try it later.

---

### 评论 #45 — Headcrabed (2024-01-26T09:36:02Z)

Maybe this patch would help? Rather than just reverting that commit.
https://patchwork.freedesktop.org/patch/575997/

---

### 评论 #46 — OzzyHelix (2024-01-26T16:48:21Z)

I'll try applying this patch and trying it out

---

### 评论 #47 — OzzyHelix (2024-01-26T18:27:51Z)

> Maybe this patch would help? Rather than just reverting that commit. https://patchwork.freedesktop.org/patch/575997/

do we know what Linux kernel version this patch is for I'm trying to find it but I am just confused

---

### 评论 #48 — OzzyHelix (2024-01-26T18:43:59Z)

I can't apply this patch to 6.7.1 or 6.7.2 because the file `amdgpu_seq64.c` doesn't exist so I can't test if this exist I'm really confused but I hope this fix works and that it makes its way into 6.8

---

### 评论 #49 — Headcrabed (2024-01-26T18:50:26Z)

> > Maybe this patch would help? Rather than just reverting that commit. https://patchwork.freedesktop.org/patch/575997/
> 
> do we know what Linux kernel version this patch is for I'm trying to find it but I am just confused

@OzzyHelix It can be applied to newest linux-next (next-20240125). It seems works on my side and seems also fixes rocm-OpenGL interop problem while using blender.

---

### 评论 #50 — OzzyHelix (2024-01-26T18:57:38Z)

> > > Maybe this patch would help? Rather than just reverting that commit. https://patchwork.freedesktop.org/patch/575997/
> > 
> > 
> > do we know what Linux kernel version this patch is for I'm trying to find it but I am just confused
> 
> @OzzyHelix It can be applied to newest linux-next (next-20240125). It seems works on my side and seems also fixes rocm-OpenGL interop problem while using blender.

I attempted to apply it to 6.7.1 and the patch command and git apply kept failing so then I tried to apply it by hand and then realized I didn't have the files in the source tree of 6.7.1 that the patch mentioned and was just very confused if someone could figure out how to get this applied to mainline or even stable so 6.7 or 6.8 that would be great

---

### 评论 #51 — OzzyHelix (2024-01-26T19:03:05Z)

I largely want this bug to be fixed for all users so having this patch backported the mainline and stable would be great

---

### 评论 #52 — kdarkhan (2024-01-28T16:51:41Z)

Just upgraded `linux` package to `6.7.2.arch1-1` on Archlinux and the issue seem to be resolved at least for Blender.

---

### 评论 #53 — xstraok (2024-01-28T20:34:44Z)

Can confirm, after upgrading to 6.7.2, the issue is gone completely. Everything now seems to work! Although I've only tested on Blender, but I'm assuming that it works fine for other compute loads too.

Update: Blender often crashes when it's trying to render with an iGPU + dGPU. Individual GPU rendering works perfectly well so far!
`Memory access fault by GPU node-2 (Agent handle: 0x781767d00400) on address 0x7815cb5fe000. Reason: Page not present or supervisor privilege.
zsh: IOT instruction (core dumped)  blender`
dmesg:
```
[ 3301.257727] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257732] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x000078154cf9f000 from client 0x1b (UTCL2)
[ 3301.257735] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841051
[ 3301.257737] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: TCP (0x8)
[ 3301.257738] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x1
[ 3301.257739] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257740] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x5
[ 3301.257741] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257742] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x1
[ 3301.257747] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257749] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7a5c000 from client 0x1b (UTCL2)
[ 3301.257751] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257752] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257754] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257755] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257756] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257757] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257758] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257762] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257764] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7abc000 from client 0x1b (UTCL2)
[ 3301.257765] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257767] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257768] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257769] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257770] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257771] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257772] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257776] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257778] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7a5d000 from client 0x1b (UTCL2)
[ 3301.257779] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257780] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257781] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257782] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257783] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257784] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257785] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257789] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257791] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7abd000 from client 0x1b (UTCL2)
[ 3301.257792] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257793] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257794] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257795] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257796] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257797] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257798] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257803] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257805] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb5fe000 from client 0x1b (UTCL2)
[ 3301.257806] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257807] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257809] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257810] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257811] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257812] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257813] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257817] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257819] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb61e000 from client 0x1b (UTCL2)
[ 3301.257821] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257822] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257823] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257824] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257825] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257826] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257827] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257831] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257833] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb6de000 from client 0x1b (UTCL2)
[ 3301.257835] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257836] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257837] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257838] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257839] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257840] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257841] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257845] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257847] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb6be000 from client 0x1b (UTCL2)
[ 3301.257849] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257850] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257851] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257852] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257853] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257854] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257855] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
[ 3301.257860] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
[ 3301.257861] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x000078154cf9f000 from client 0x1b (UTCL2)
[ 3301.257863] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[ 3301.257864] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
[ 3301.257865] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
[ 3301.257866] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
[ 3301.257867] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
[ 3301.257868] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
[ 3301.257869] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
```

---

### 评论 #54 — Headcrabed (2024-01-29T01:52:02Z)

> Can confirm, after upgrading to 6.7.2, the issue is gone completely. Everything now seems to work! Although I've only tested on Blender, but I'm assuming that it works fine for other compute loads too.
> 
> Update: Blender often crashes when it's trying to render with an iGPU + dGPU. Individual GPU rendering works perfectly well so far! `Memory access fault by GPU node-2 (Agent handle: 0x781767d00400) on address 0x7815cb5fe000. Reason: Page not present or supervisor privilege. zsh: IOT instruction (core dumped) blender` dmesg:
> 
> ```
> [ 3301.257727] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257732] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x000078154cf9f000 from client 0x1b (UTCL2)
> [ 3301.257735] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00841051
> [ 3301.257737] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: TCP (0x8)
> [ 3301.257738] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x1
> [ 3301.257739] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257740] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x5
> [ 3301.257741] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257742] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x1
> [ 3301.257747] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257749] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7a5c000 from client 0x1b (UTCL2)
> [ 3301.257751] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257752] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257754] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257755] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257756] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257757] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257758] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257762] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257764] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7abc000 from client 0x1b (UTCL2)
> [ 3301.257765] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257767] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257768] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257769] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257770] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257771] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257772] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257776] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257778] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7a5d000 from client 0x1b (UTCL2)
> [ 3301.257779] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257780] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257781] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257782] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257783] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257784] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257785] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257789] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257791] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007817c7abd000 from client 0x1b (UTCL2)
> [ 3301.257792] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257793] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257794] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257795] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257796] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257797] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257798] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257803] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257805] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb5fe000 from client 0x1b (UTCL2)
> [ 3301.257806] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257807] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257809] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257810] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257811] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257812] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257813] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257817] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257819] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb61e000 from client 0x1b (UTCL2)
> [ 3301.257821] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257822] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257823] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257824] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257825] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257826] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257827] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257831] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257833] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb6de000 from client 0x1b (UTCL2)
> [ 3301.257835] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257836] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257837] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257838] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257839] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257840] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257841] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257845] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257847] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x00007815cb6be000 from client 0x1b (UTCL2)
> [ 3301.257849] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257850] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257851] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257852] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257853] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257854] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257855] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> [ 3301.257860] amdgpu 0000:11:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:40 vmid:8 pasid:32802, for process blender pid 9571 thread blender pid 9571)
> [ 3301.257861] amdgpu 0000:11:00.0: amdgpu:   in page starting at address 0x000078154cf9f000 from client 0x1b (UTCL2)
> [ 3301.257863] amdgpu 0000:11:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [ 3301.257864] amdgpu 0000:11:00.0: amdgpu: 	Faulty UTCL2 client ID: CB/DB (0x0)
> [ 3301.257865] amdgpu 0000:11:00.0: amdgpu: 	MORE_FAULTS: 0x0
> [ 3301.257866] amdgpu 0000:11:00.0: amdgpu: 	WALKER_ERROR: 0x0
> [ 3301.257867] amdgpu 0000:11:00.0: amdgpu: 	PERMISSION_FAULTS: 0x0
> [ 3301.257868] amdgpu 0000:11:00.0: amdgpu: 	MAPPING_ERROR: 0x0
> [ 3301.257869] amdgpu 0000:11:00.0: amdgpu: 	RW: 0x0
> ```

Can you check whether the new patch I mentioned is applied to your kernel or not? If your kernel just revert the old commit, the interop problem still exists.

---

### 评论 #55 — OzzyHelix (2024-01-29T02:10:33Z)

> Just upgraded `linux` package to `6.7.2.arch1-1` on Archlinux and the issue seem to be resolved at least for Blender.

I'll try that but if it doesn't work I will just continue to bisect the broken code til the issue is fixed that means I'm compiling my kernel

---

### 评论 #56 — OzzyHelix (2024-01-29T04:21:42Z)

the issue appears to be fixed on the `linux-zen` package on version `6.7.2-zen1-1-zen` on Arch Linux but idk if the issue will return 

---

### 评论 #57 — OzzyHelix (2024-01-29T19:42:55Z)

its fixed on Arch Linux from what I can tell but we need confirmation on other distros before I think it might be safe to close this issue as complete. The issue has been closed on Gitlab but I think it would be best to confirm that its fixed on other distros running 6.7.2 before closing the thread here. My concern is that people running not rolling release distros will have a bad time with this bug

---

### 评论 #58 — dreirund (2024-02-07T16:54:58Z)

I have it too. When I run `clinfo`, nothing is output, but `dmesg` shows severe kernel issues.

System continues to function for a while, but when I want to switch from Xorg to text console, it hangs (SysRq works).

When I am at the text console while in Xorg a timed `clinfo` fires, system freezes after a few seconds.

* Kernel: 6.7[-pf5](https://codeberg.org/pf-kernel/linux/releases),
* SoC: AMD 7840U (Zen 4 "Phoenix", integrated graphics: Radeon 780M),
* ROCm version: 6.0.2 (via [`opencl-amd` AUR package](https://aur.archlinux.org/packages/opencl-amd)),
* `clinfo --version`: `clinfo version 3.0.21.02.21`,
* `rocminfo`:  
  ```
  [...]
  Runtime Version:         1.1
  [...]
  ```

Attached a `dmesg` output from after issuing `clinfo`: [`winmax2-clinfo-error.dmesg.log`](https://github.com/ROCm/ROCm/files/14196844/felics-winmax2-clinfo-error.dmesg.log). Excerpt:  
```
[10651.492646] amdgpu 0000:65:00.0: amdgpu: bo 00000000961b6633 va 0x0800000000-0x0800000001 conflict with 0x0800000000-0x08000000c0
[10651.492652] amdgpu: Failed to map VA 0x800000000000 in vm. ret -22
[10651.492654] amdgpu: Failed to map bo to gpuvm
[10651.495405] BUG: kernel NULL pointer dereference, address: 0000000000000002
[10651.495408] #PF: supervisor read access in kernel mode
[10651.495410] #PF: error_code(0x0000) - not-present page
[10651.495411] PGD 0 P4D 0 
[10651.495414] Oops: 0000 [#1] PREEMPT SMP NOPTI
[10651.495416] CPU: 5 PID: 379 Comm: clinfo Tainted: G           OE      6.7.0-pf4 #1 13dd90f6874895da32c433ea3570c1c5313a99d9
[10651.495419] Hardware name: GPD G1619-04/G1619-04, BIOS 0.35 09/12/2023
[10651.495421] RIP: 0010:__list_add_valid_or_report+0x1a/0xa0
[10651.495425] Code: 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 f3 0f 1e fa 48 89 d0 48 85 f6 74 2a 48 85 d2 74 3a 48 8b 52 08 48 39 f2 75 41 <4c> 8b 02 49 39 c0 75 4c 48 39 fa 74 60 49 39 f8 74 5b b8 01 00 00
[10651.495427] RSP: 0018:ffffac46619a7bc8 EFLAGS: 00010246
[10651.495429] RAX: ffff976852087650 RBX: 0000000000000002 RCX: ffff976852087600
[10651.495431] RDX: 0000000000000002 RSI: 0000000000000002 RDI: ffffac46619a7bf0
[10651.495432] RBP: ffffac46619a7c50 R08: ffff976852087640 R09: 0000000000000000
[10651.495433] R10: ffff976b03663cc0 R11: 0000000000000000 R12: ffffac46619a7bf0
[10651.495434] R13: ffff976852087648 R14: ffff976852087640 R15: ffff976852087600
[10651.495435] FS:  00007c00fb49fdc0(0000) GS:ffff976cae140000(0000) knlGS:0000000000000000
[10651.495436] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[10651.495438] CR2: 0000000000000002 CR3: 0000000717442000 CR4: 0000000000f50ef0
[10651.495439] PKRU: 55555554
[10651.495440] Call Trace:
[10651.495443]  <TASK>
[10651.495445]  ? __die+0x10f/0x120
[10651.495448]  ? page_fault_oops+0x171/0x4e0
[10651.495451]  ? srso_alias_return_thunk+0x5/0xfbef5
[10651.495457]  ? ttm_bo_validate+0x151/0x370 [ttm a30eb089ff7975d288e9c5b1f7b7ce58036990fd]
[10651.495465]  ? exc_page_fault+0x7f/0x180
[10651.495467]  ? asm_exc_page_fault+0x26/0x30
[10651.495471]  ? __list_add_valid_or_report+0x1a/0xa0
[10651.495473]  ? srso_alias_return_thunk+0x5/0xfbef5
[10651.495475]  __mutex_lock.constprop.0+0x29c/0x770
[10651.495478]  ? kmalloc_trace+0x2a/0xa0
[10651.495483]  amdgpu_amdkfd_gpuvm_alloc_memory_of_gpu+0x744/0xde0 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[10651.495672]  ? amdgpu_bo_sync_wait_resv+0x9f/0xb0 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[10651.495816]  kfd_process_alloc_gpuvm+0x32/0x100 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[10651.495985]  kfd_process_device_init_vm+0x2d8/0x390 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[10651.496144]  kfd_ioctl_acquire_vm+0x89/0xc0 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[10651.496288]  kfd_ioctl+0x3c8/0x4e0 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[10651.496426]  ? __pfx_kfd_ioctl_acquire_vm+0x10/0x10 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[10651.496572]  __x64_sys_ioctl+0x94/0xd0
[10651.496575]  do_syscall_64+0x61/0xe0
[10651.496578]  ? syscall_exit_to_user_mode+0x2b/0x40
[10651.496580]  ? srso_alias_return_thunk+0x5/0xfbef5
[10651.496582]  ? do_syscall_64+0x70/0xe0
[10651.496583]  ? do_syscall_64+0x70/0xe0
[10651.496585]  entry_SYSCALL_64_after_hwframe+0x6e/0x76
[10651.496588] RIP: 0033:0x7c00fb69d4ff
[10651.496621] Code: 00 48 89 44 24 18 31 c0 48 8d 44 24 60 c7 04 24 10 00 00 00 48 89 44 24 08 48 8d 44 24 20 48 89 44 24 10 b8 10 00 00 00 0f 05 <89> c2 3d 00 f0 ff ff 77 18 48 8b 44 24 18 64 48 2b 04 25 28 00 00
[10651.496623] RSP: 002b:00007ffde2875520 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
[10651.496625] RAX: ffffffffffffffda RBX: 00007ffde2875690 RCX: 00007c00fb69d4ff
[10651.496626] RDX: 00007ffde2875690 RSI: 0000000040084b15 RDI: 000000000000000b
[10651.496627] RBP: 0000000040084b15 R08: 0000000000000007 R09: 0000000000000001
[10651.496628] R10: 0000564e27434870 R11: 0000000000000246 R12: 0000564e27434220
[10651.496629] R13: 000000000000000b R14: 00007c00e9cc37a0 R15: 0000000000000060
[10651.496632]  </TASK>
[10651.496633] Modules linked in: snd_seq_dummy snd_hrtimer snd_seq snd_seq_device xt_CHECKSUM xt_MASQUERADE xt_conntrack ipt_REJECT nf_reject_ipv4 xt_tcpudp nft_compat x_tables nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nf_tables nfnetlink bridge stp llc ccm fuse qrtr r8153_ecm cdc_ether r8152 vfat fat pktcdvd usbnet option mii usb_wwan uvcvideo videobuf2_vmalloc uvc videobuf2_memops videobuf2_v4l2 videobuf2_common btusb btrtl btintel btbcm btmtk bluetooth ecdh_generic xpad crc16 ff_memless v4l2loopback videodev mc loop vboxnetflt(OE) vboxnetadp(OE) vboxdrv(OE) dm_multipath iwlmvm intel_rapl_msr snd_hda_codec_conexant intel_rapl_common keymash(OE) snd_hda_codec_generic mac80211 g_cdc ledtrig_audio u_ether snd_hda_codec_hdmi joydev libcomposite libarc4 udc_core snd_hda_intel snd_intel_dspcfg edac_mce_amd snd_intel_sdw_acpi snd_hda_codec i2c_dev iwlwifi kvm_amd snd_hda_core bmi260_i2c(OE) snd_hwdep sg bmi260_core(OE) snd_pcm kvm cfg80211 snd_timer crypto_user snd irqbypass sp5100_tco
[10651.496698]  industrialio_triggered_buffer hid_multitouch acpi_call(OE) rapl kfifo_buf thunderbolt pcspkr soundcore i2c_piix4 rfkill i2c_hid_acpi industrialio mac_hid i2c_hid amd_pmc dm_crypt cbc encrypted_keys trusted asn1_encoder tee dm_mod sr_mod cdrom usb_storage amdgpu crct10dif_pclmul crc32_pclmul polyval_clmulni amdxcp polyval_generic i2c_algo_bit gf128mul drm_ttm_helper ghash_clmulni_intel ttm sha512_ssse3 sha256_ssse3 drm_exec sdhci_pci serio_raw sha1_ssse3 gpu_sched cqhci aesni_intel drm_suballoc_helper drm_buddy sdhci crypto_simd drm_display_helper cryptd xhci_pci mmc_core ccp cec xhci_pci_renesas video i8042 wmi usbhid psmouse mousedev btrfs blake2b_generic libcrc32c crc32c_generic crc32c_intel xor raid6_pq nvme nvme_core nvme_auth atkbd libps2 serio vivaldi_fmap [last unloaded: bmi160_core]
[10651.496748] CR2: 0000000000000002
[10651.496750] ---[ end trace 0000000000000000 ]---
[10651.496751] RIP: 0010:__list_add_valid_or_report+0x1a/0xa0
[10651.496753] Code: 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 f3 0f 1e fa 48 89 d0 48 85 f6 74 2a 48 85 d2 74 3a 48 8b 52 08 48 39 f2 75 41 <4c> 8b 02 49 39 c0 75 4c 48 39 fa 74 60 49 39 f8 74 5b b8 01 00 00
[10651.496755] RSP: 0018:ffffac46619a7bc8 EFLAGS: 00010246
[10651.496756] RAX: ffff976852087650 RBX: 0000000000000002 RCX: ffff976852087600
[10651.496757] RDX: 0000000000000002 RSI: 0000000000000002 RDI: ffffac46619a7bf0
[10651.496758] RBP: ffffac46619a7c50 R08: ffff976852087640 R09: 0000000000000000
[10651.496759] R10: ffff976b03663cc0 R11: 0000000000000000 R12: ffffac46619a7bf0
[10651.496760] R13: ffff976852087648 R14: ffff976852087640 R15: ffff976852087600
[10651.496762] FS:  00007c00fb49fdc0(0000) GS:ffff976cae140000(0000) knlGS:0000000000000000
[10651.496763] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[10651.496764] CR2: 0000000000000002 CR3: 0000000717442000 CR4: 0000000000f50ef0
[10651.496766] PKRU: 55555554
[10651.496767] note: clinfo[379] exited with irqs disabled
[10651.496768] note: clinfo[379] exited with preempt_count 2
[10678.326591] watchdog: BUG: soft lockup - CPU#3 stuck for 26s! [kworker/u32:11:24687]
[...]
[11002.326581] watchdog: BUG: soft lockup - CPU#3 stuck for 328s! [kworker/u32:11:24687]
[11002.326587] Modules linked in: snd_seq_dummy snd_hrtimer snd_seq snd_seq_device xt_CHECKSUM xt_MASQUERADE xt_conntrack ipt_REJECT nf_reject_ipv4 xt_tcpudp nft_compat x_tables nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nf_tables nfnetlink bridge stp llc ccm fuse qrtr r8153_ecm cdc_ether r8152 vfat fat pktcdvd usbnet option mii usb_wwan uvcvideo videobuf2_vmalloc uvc videobuf2_memops videobuf2_v4l2 videobuf2_common btusb btrtl btintel btbcm btmtk bluetooth ecdh_generic xpad crc16 ff_memless v4l2loopback videodev mc loop vboxnetflt(OE) vboxnetadp(OE) vboxdrv(OE) dm_multipath iwlmvm intel_rapl_msr snd_hda_codec_conexant intel_rapl_common keymash(OE) snd_hda_codec_generic mac80211 g_cdc ledtrig_audio u_ether snd_hda_codec_hdmi joydev libcomposite libarc4 udc_core snd_hda_intel snd_intel_dspcfg edac_mce_amd snd_intel_sdw_acpi snd_hda_codec i2c_dev iwlwifi kvm_amd snd_hda_core bmi260_i2c(OE) snd_hwdep sg bmi260_core(OE) snd_pcm kvm cfg80211 snd_timer crypto_user snd irqbypass sp5100_tco
[11002.326654]  industrialio_triggered_buffer hid_multitouch acpi_call(OE) rapl kfifo_buf thunderbolt pcspkr soundcore i2c_piix4 rfkill i2c_hid_acpi industrialio mac_hid i2c_hid amd_pmc dm_crypt cbc encrypted_keys trusted asn1_encoder tee dm_mod sr_mod cdrom usb_storage amdgpu crct10dif_pclmul crc32_pclmul polyval_clmulni amdxcp polyval_generic i2c_algo_bit gf128mul drm_ttm_helper ghash_clmulni_intel ttm sha512_ssse3 sha256_ssse3 drm_exec sdhci_pci serio_raw sha1_ssse3 gpu_sched cqhci aesni_intel drm_suballoc_helper drm_buddy sdhci crypto_simd drm_display_helper cryptd xhci_pci mmc_core ccp cec xhci_pci_renesas video i8042 wmi usbhid psmouse mousedev btrfs blake2b_generic libcrc32c crc32c_generic crc32c_intel xor raid6_pq nvme nvme_core nvme_auth atkbd libps2 serio vivaldi_fmap [last unloaded: bmi160_core]
[11002.326710] CPU: 3 PID: 24687 Comm: kworker/u32:11 Tainted: G      D    OEL     6.7.0-pf4 #1 13dd90f6874895da32c433ea3570c1c5313a99d9
[11002.326714] Hardware name: GPD G1619-04/G1619-04, BIOS 0.35 09/12/2023
[11002.326716] Workqueue: kfd_restore_wq restore_process_worker [amdgpu]
[11002.327051] RIP: 0010:native_queued_spin_lock_slowpath+0x71/0x2e0
[11002.327056] Code: 0f ba 2b 08 0f 92 c2 8b 03 0f b6 d2 c1 e2 08 30 e4 09 d0 3d ff 00 00 00 77 5b 85 c0 74 10 0f b6 03 84 c0 74 09 f3 90 0f b6 03 <84> c0 75 f7 b8 01 00 00 00 66 89 03 65 48 ff 05 23 8a c1 43 5b 5d
[11002.327058] RSP: 0018:ffffac464983bbf0 EFLAGS: 00000202
[11002.327060] RAX: 0000000000000001 RBX: ffff976852087648 RCX: 0000000000000000
[11002.327061] RDX: 0000000000000000 RSI: 0000000000000001 RDI: ffff976852087648
[11002.327062] RBP: ffffac464983bca0 R08: ffff9767bb665580 R09: 000000000000000f
[11002.327064] R10: fefefefefefefeff R11: 0000000000000008 R12: ffff976195547200
[11002.327065] R13: ffff976852087648 R14: ffff976852087640 R15: ffff976a9c084ba8
[11002.327066] FS:  0000000000000000(0000) GS:ffff976cae0c0000(0000) knlGS:0000000000000000
[11002.327067] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[11002.327069] CR2: 000074b4c4df8490 CR3: 0000000528e20000 CR4: 0000000000f50ef0
[11002.327070] PKRU: 55555554
[11002.327071] Call Trace:
[11002.327073]  <IRQ>
[11002.327074]  ? watchdog_timer_fn+0x1b8/0x220
[11002.327078]  ? __pfx_watchdog_timer_fn+0x10/0x10
[11002.327080]  ? __hrtimer_run_queues+0x123/0x2b0
[11002.327084]  ? hrtimer_interrupt+0xfb/0x440
[11002.327085]  ? srso_alias_return_thunk+0x5/0xfbef5
[11002.327089]  ? __sysvec_apic_timer_interrupt+0x4d/0x140
[11002.327091]  ? sysvec_apic_timer_interrupt+0x6d/0x90
[11002.327093]  </IRQ>
[11002.327094]  <TASK>
[11002.327095]  ? asm_sysvec_apic_timer_interrupt+0x1a/0x20
[11002.327099]  ? native_queued_spin_lock_slowpath+0x71/0x2e0
[11002.327102]  _raw_spin_lock+0x29/0x30
[11002.327104]  __mutex_lock.constprop.0+0xe0/0x770
[11002.327106]  ? srso_alias_return_thunk+0x5/0xfbef5
[11002.327109]  amdgpu_amdkfd_gpuvm_restore_process_bos+0x71/0x730 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[11002.327293]  ? srso_alias_return_thunk+0x5/0xfbef5
[11002.327296]  ? srso_alias_return_thunk+0x5/0xfbef5
[11002.327297]  ? psi_group_change+0x27d/0x440
[11002.327303]  restore_process_worker+0x34/0x170 [amdgpu 0d5f626b08fccc4c668e7a8de931cf086fc93e69]
[11002.327466]  process_one_work+0x171/0x330
[11002.327470]  worker_thread+0x3ef/0x580
[11002.327473]  ? __pfx_worker_thread+0x10/0x10
[11002.327475]  kthread+0xe5/0x120
[11002.327477]  ? __pfx_kthread+0x10/0x10
[11002.327479]  ret_from_fork+0x31/0x50
[11002.327481]  ? __pfx_kthread+0x10/0x10
[11002.327483]  ret_from_fork_asm+0x1b/0x30
[11002.327486]  </TASK>
```

In which mainline kernel version did the fix flow in? (I think I do not have backports by distributions since I use [`-pf`-kernel](https://pfkernel.natalenko.name/), it only follows closely official kernel releases.)

Regards!

---

### 评论 #59 — OzzyHelix (2024-02-07T19:22:43Z)

try the rocm-hip-runtime instead of opencl-amd if you can

---

### 评论 #60 — sofiageo (2024-02-07T20:26:39Z)

> try the rocm-hip-runtime instead of opencl-amd if you can

For my GPU (5700xt) and `opencl-amd` the issue was fixed when the kernel update 6.7.2+ was released.

---

### 评论 #61 — OzzyHelix (2024-02-07T20:28:12Z)

I've had trouble with opencl-amd on my RX 6600 mostly just some janky weird behavior its hard to describe for RDNA 2 and 3 I recommend using rocm-hip-runtime instead

---

### 评论 #62 — dreirund (2024-02-07T21:38:08Z)

> *try the rocm-hip-runtime instead of opencl-amd if you can*

Anyway, calling a user space programme should not make the kernel crash in any circumstance, so in my understanding here is a kernel issue present.

Am I wrong (and if so, why?)?


---

### 评论 #63 — dreirund (2024-02-08T07:57:13Z)

> _I have it too. When I run `clinfo`, nothing is output, but `dmesg` shows severe kernel issues._
> _[...]_
>     * _Kernel: 6.7[-pf5](https://codeberg.org/pf-kernel/linux/releases),_
>     * _SoC: AMD 7840U (Zen 4 "Phoenix", integrated graphics: Radeon 780M),_
>     * _ROCm version: 6.0.2 (via [`opencl-amd` AUR package](https://aur.archlinux.org/packages/opencl-amd)),_
>     * _[...]_
> 
> _Attached a `dmesg` output from after issuing `clinfo`: [`winmax2-clinfo-error.dmesg.log`](https://github.com/ROCm/ROCm/files/14196844/felics-winmax2-clinfo-error.dmesg.log)._
> _[...]_

Fixed for me with [vanilla kernel 6.7.4](https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.7.4.tar.xz).

---

### 评论 #64 — OzzyHelix (2024-02-08T17:10:32Z)

> > _try the rocm-hip-runtime instead of opencl-amd if you can_
> 
> Anyway, calling a user space programme should not make the kernel crash in any circumstance, so in my understanding here is a kernel issue present.
> 
> Am I wrong (and if so, why?)?

the issue wasn't resolved until stable 6.7.2 6.7[-pf5](https://codeberg.org/pf-kernel/linux/releases), probably isn't caught up with that

---

### 评论 #65 — OzzyHelix (2024-02-08T17:12:08Z)

it was a problem from 6.5.x to 6.7.1

---

### 评论 #66 — Headcrabed (2024-02-08T19:46:16Z)

https://patchwork.freedesktop.org/patch/573129/
This patch should make this kernel panic not happen, but just hide the real problem rather than actually fix it. 
https://patchwork.freedesktop.org/series/129339/
And this series should be the real fix?

---

### 评论 #67 — kouta-kun (2024-02-13T23:58:48Z)

Just updated to Linux 6.7.4-arch1-1 + ROCm 6.0.32830 and the issue is back in full. Blender crashes with this dmesg log:
```
[  190.955679] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32782, for process blender pid 1875 thread blender:cs0 pid 1894)
[  190.955685] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007b16dd404000 from client 10
[  190.955687] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[  190.955689] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
[  190.955691] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[  190.955693] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  190.955694] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  190.955695] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  190.955697] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
[  190.955702] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32782, for process blender pid 1875 thread blender:cs0 pid 1894)
[  190.955705] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007b16dd404000 from client 10
[  190.955707] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[  190.955708] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[  190.955710] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  190.955711] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[  190.955712] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[  190.955714] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[  190.955715] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
```

And while clinfo works, I get an even weirder dmesg log after it runs:
```
[  395.348596] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[  395.348603] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x000072c931137000 from client 10
[  395.348606] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
[  395.348608] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[  395.348610] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[  395.348612] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[  395.348613] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[  395.348614] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[  395.348616] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
```

---

### 评论 #68 — GZGavinZhao (2024-02-14T00:09:31Z)

> Just updated to Linux 6.7.4-arch1-1 + ROCm 6.0.0 and the issue is back in full. Blender crashes with this dmesg log:
> ```
> [  190.955679] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32782, for process blender pid 1875 thread blender:cs0 pid 1894)
> [  190.955685] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007b16dd404000 from client 10
> [  190.955687] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
> [  190.955689] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
> [  190.955691] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x1
> [  190.955693] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
> [  190.955694] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
> [  190.955695] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
> [  190.955697] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
> [  190.955702] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32782, for process blender pid 1875 thread blender:cs0 pid 1894)
> [  190.955705] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007b16dd404000 from client 10
> [  190.955707] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [  190.955708] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
> [  190.955710] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
> [  190.955711] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
> [  190.955712] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
> [  190.955714] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
> [  190.955715] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
> ```
> 
> And while clinfo works, I get an even weirder dmesg log after it runs:
> ```
> [  395.348596] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
> [  395.348603] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x000072c931137000 from client 10
> [  395.348606] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
> [  395.348608] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
> [  395.348610] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
> [  395.348612] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x1
> [  395.348613] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
> [  395.348614] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
> [  395.348616] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
> ```

The only solution for this error that I know of is to download and run any official Blender binaries with version > 4.0.2 (instead of getting Blender from your distributuon). Note that you may need to download Blender daily builds if 4.0.3 has not been released yet. If you are already doing so, then as far as I know there are no solutions to this problem :( Just seems to be a problem with ROCm 6.

---

### 评论 #69 — terryrankine (2024-02-14T00:13:31Z)

Last I checked, the current stable was 6.0.2

What is the point of testing software which has already been found faulty
and patch releases made?

On Wed, 14 Feb 2024, 8:09 am Gavin Zhao, ***@***.***> wrote:

> Just updated to Linux 6.7.4-arch1-1 + ROCm 6.0.0 and the issue is back in
> full. Blender crashes with this dmesg log:
>
> [  190.955679] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32782, for process blender pid 1875 thread blender:cs0 pid 1894)
> [  190.955685] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007b16dd404000 from client 10
> [  190.955687] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
> [  190.955689] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
> [  190.955691] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x1
> [  190.955693] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
> [  190.955694] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
> [  190.955695] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
> [  190.955697] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
> [  190.955702] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32782, for process blender pid 1875 thread blender:cs0 pid 1894)
> [  190.955705] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007b16dd404000 from client 10
> [  190.955707] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
> [  190.955708] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
> [  190.955710] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
> [  190.955711] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
> [  190.955712] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
> [  190.955714] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
> [  190.955715] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
>
> And while clinfo works, I get an even weirder dmesg log after it runs:
>
> [  395.348596] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
> [  395.348603] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x000072c931137000 from client 10
> [  395.348606] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B32
> [  395.348608] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
> [  395.348610] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x0
> [  395.348612] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x1
> [  395.348613] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
> [  395.348614] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
> [  395.348616] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
>
> The only solution for this error that I know of is to download and run the
> official Blender binaries (instead of getting Blender from your
> distributuon). If you are already doing so, then as far as I know there are
> no solutions to this problem :( Just seems to be a problem with ROCm 6.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2596#issuecomment-1942883662>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AAKWX5G2QFTE6XXRBE4B26TYTP6ETAVCNFSM6AAAAAA6LORYMCVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTSNBSHA4DGNRWGI>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #70 — kouta-kun (2024-02-14T00:14:38Z)

@terryrankine sorry it seems my distribution is mislabeling some packages, I do in fact have 6.0.32830 and not 6.0.0:
```
LANG=C /opt/rocm/bin/hipconfig --full
HIP version  : 6.0.32830-

== hipconfig
HIP_PATH     : /opt/rocm
ROCM_PATH    : /opt/rocm
HIP_COMPILER : clang
HIP_PLATFORM : amd
HIP_RUNTIME  : rocclr
CPP_CONFIG   :  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm/include -I/opt/rocm/lib/llvm/lib/clang/17.0.0
 

== hip-clang
HIP_CLANG_PATH   : /opt/rocm/llvm/bin
clang version 17.0.0
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm/llvm/bin
AOMP-16.0-45 (http://github.com/ROCm-Developer-Tools/aomp):
 Source ID:16.0-45-6b875fb548b9ded0f07df02bc2af6e12568504a9
  LLVM version 17.0.0git
  Optimized build with assertions.
  Default target: x86_64-pc-linux-gnu
  Host CPU: znver3

  Registered Targets:
    amdgcn  - AMD GCN GPUs
    nvptx   - NVIDIA PTX 32-bit
    nvptx64 - NVIDIA PTX 64-bit
    r600    - AMD GPUs HD2XXX-HD6XXX
    x86     - 32-bit X86: Pentium-Pro and above
    x86-64  - 64-bit X86: EM64T and AMD64
hip-clang-cxxflags :  -isystem "/opt/rocm/include" -O3
hip-clang-ldflags  : --driver-mode=g++ -O3 --hip-link --rtlib=compiler-rt -unwindlib=libgcc

=== Environment Variables
PATH=/home/kouta/.nvm/versions/node/v16.15.0/bin:/sbin:/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/opt/android-sdk/platform-tools:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/usr/lib/rustup/bin:/home/kouta/.local/bin/:/opt/ps2dev/bin:/opt/ps2dev/ee/bin:/opt/ps2dev/iop/bin:/opt/ps2dev/dvp/bin:/opt/ps2dev/ps2sdk/bin
egrep: warning: egrep is obsolescent; using grep -E

== Linux Kernel
Hostname     : Can't exec "hostname": No such file or directory at /opt/rocm/bin//hipconfig.pl line 211.
Linux arch-kouta 6.7.4-arch1-1 #1 SMP PREEMPT_DYNAMIC Mon, 05 Feb 2024 22:07:49 +0000 x86_64 GNU/Linux
LSB Version:	n/a
Distributor ID:	Arch
Description:	Arch Linux
Release:	rolling
Codename:	n/a
```

---

### 评论 #71 — kouta-kun (2024-02-14T00:17:21Z)

@GZGavinZhao using daily Blender 4.1.0 beta does in fact fix my issue, thanks for suggesting! I'd tried their build of 4.0.2 and gave up because it crashed with the same issue.

---

### 评论 #72 — GZGavinZhao (2024-02-14T00:19:11Z)

The official binaries contain GPU libraries that were compiled with ROCm 5.5, so it is not affected by ROCm 6.0 bugs, and 4.0.2 fails simply because it doesn't have support for running on a ROCm 6.0 system, which was introduced in 4.0.3.

---

### 评论 #73 — terryrankine (2024-02-14T00:23:14Z)

ROCM put the numbers at the end of the packages in Ubuntu.... Don't get me
started on #semanticnaming....

`amdgpu-install_6.0.60002-1_all.deb`
That's 6.0.2 which installs the 6.0.2 repo, which has the 6.0.2 packages on
Ubuntu.

https://repo.radeon.com/amdgpu-install/

And latest pointer in there was never latest....

All the tricks that are not written anywhere....



You may be right, but I'm just calling out the gap in package/release name
and software version tag in the libraries.

Good luck


On Wed, 14 Feb 2024, 8:14 am kouta-kun, ***@***.***> wrote:

> @terryrankine <https://github.com/terryrankine> sorry it seems my
> distribution is mislabeling some packages, I do in fact have 6.0.32830 and
> not 6.0.0:
>
> LANG=C /opt/rocm/bin/hipconfig --full
> HIP version  : 6.0.32830-
>
> == hipconfig
> HIP_PATH     : /opt/rocm
> ROCM_PATH    : /opt/rocm
> HIP_COMPILER : clang
> HIP_PLATFORM : amd
> HIP_RUNTIME  : rocclr
> CPP_CONFIG   :  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm/include -I/opt/rocm/lib/llvm/lib/clang/17.0.0
>
>
> == hip-clang
> HIP_CLANG_PATH   : /opt/rocm/llvm/bin
> clang version 17.0.0
> Target: x86_64-pc-linux-gnu
> Thread model: posix
> InstalledDir: /opt/rocm/llvm/bin
> AOMP-16.0-45 (http://github.com/ROCm-Developer-Tools/aomp):
>  Source ID:16.0-45-6b875fb548b9ded0f07df02bc2af6e12568504a9
>   LLVM version 17.0.0git
>   Optimized build with assertions.
>   Default target: x86_64-pc-linux-gnu
>   Host CPU: znver3
>
>   Registered Targets:
>     amdgcn  - AMD GCN GPUs
>     nvptx   - NVIDIA PTX 32-bit
>     nvptx64 - NVIDIA PTX 64-bit
>     r600    - AMD GPUs HD2XXX-HD6XXX
>     x86     - 32-bit X86: Pentium-Pro and above
>     x86-64  - 64-bit X86: EM64T and AMD64
> hip-clang-cxxflags :  -isystem "/opt/rocm/include" -O3
> hip-clang-ldflags  : --driver-mode=g++ -O3 --hip-link --rtlib=compiler-rt -unwindlib=libgcc
>
> === Environment Variables
> PATH=/home/kouta/.nvm/versions/node/v16.15.0/bin:/sbin:/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/opt/android-sdk/platform-tools:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/usr/lib/rustup/bin:/home/kouta/.local/bin/:/opt/ps2dev/bin:/opt/ps2dev/ee/bin:/opt/ps2dev/iop/bin:/opt/ps2dev/dvp/bin:/opt/ps2dev/ps2sdk/bin
> egrep: warning: egrep is obsolescent; using grep -E
>
> == Linux Kernel
> Hostname     : Can't exec "hostname": No such file or directory at /opt/rocm/bin//hipconfig.pl line 211.
> Linux arch-kouta 6.7.4-arch1-1 #1 SMP PREEMPT_DYNAMIC Mon, 05 Feb 2024 22:07:49 +0000 x86_64 GNU/Linux
> LSB Version:	n/a
> Distributor ID:	Arch
> Description:	Arch Linux
> Release:	rolling
> Codename:	n/a
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ROCm/ROCm/issues/2596#issuecomment-1942888286>, or
> unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AAKWX5AYQ4Y5Y2VJOKSQBRLYTP6XZAVCNFSM6AAAAAA6LORYMCVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHMYTSNBSHA4DQMRYGY>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>


---

### 评论 #74 — danielzgtg (2024-03-10T04:00:38Z)

GPT4All/llama.cpp is working on my 6.8-rc7 kernel. I will close after Ubuntu 24.04 comes out and I test clinfo and Blender.

---

### 评论 #75 — ppanchad-amd (2024-06-18T20:39:44Z)

@danielzgtg Can you please test with Ubuntu 24.04 when you get a chance and close issue if it's fixed? Thanks!

---

### 评论 #76 — extraymond (2024-06-27T04:32:59Z)

I face the same issue on ubuntu 22.04 with kernel 6.5.

For anyone having the same setup as I:
Installed the HWE kernel(6.8) in 22.04 and it's not triggering any more.

---

### 评论 #77 — ppanchad-amd (2024-07-19T17:04:12Z)

@danielzgtg Can you please test with HWE kernel(6.8) in 22.04 and verify if your issue still exists? If not, please close the ticket. Thanks!

---

### 评论 #78 — OzzyHelix (2024-07-20T00:22:58Z)

so I'm confused I thought this was fixed 6.7.1. are people still having trouble with this due to LTS kernels and Ubuntu and Debian lagging behind?

---
