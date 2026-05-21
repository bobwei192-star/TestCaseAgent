# [Issue]: Krackan Point GPU hang (gfx1152) Ryzen AI 350 (MES:0x82)

> **Issue #5844**
> **状态**: open
> **创建时间**: 2026-01-08T16:16:51Z
> **更新时间**: 2026-05-19T01:16:13Z
> **作者**: X-Ryl669
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5844

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

#### OS
**NAME** CachyOS Linux

#### CPU
**model name** AMD Ryzen AI 7 350 w/ Radeon 860M

#### GPU
```
  Name:                    AMD Ryzen AI 7 350 w/ Radeon 860M
  Marketing Name:          AMD Ryzen AI 7 350 w/ Radeon 860M
  Name:                    gfx1152
  Marketing Name:          AMD Radeon 860M Graphics
      Name:                    amdgcn-amd-amdhsa--gfx1152
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
  Name:                    aie2
  Marketing Name:          AIE-ML
```

#### KERNEL
Linux host 6.18.3-2-cachyos #1 SMP PREEMPT_DYNAMIC Sat, 03 Jan 2026 20:06:51 +0000 x86_64 GNU/Linux
Command line: `quiet zswap.enabled=0 nowatchdog splash rw root=UUID=redacted amdgpu.cwsr_enable=0 initrd=\initramfs-linux-cachyos.img`

#### FIRMWARE-INFO:
```
MES_KIQ feature version: 6, firmware version: 0x00000079
MES feature version: 1, firmware version: 0x00000082
```

### Operating System

CachyOS (arch based)

### CPU

AMD Ryzen AI 7 350

### GPU

Radeon 860M

### ROCm Version

7.1.1

### ROCm Component

_No response_

### Steps to Reproduce

Just using the desktop (no AI workload, plain dumb desktop usage) is enough

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

Output of dmesg when it happens:
```
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
[UFW BLOCK] IN=wlan0 OUT= MAC=01:00:5e:00:00:01:5c:cf:7f:0b:41:b5:08:00 SRC=192.168.0.106 DST=224.0.0.1 LEN=32 TOS=0x00 PREC=0x00 TTL=1 ID=2 PROTO=2
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:04:00.0: amdgpu: failed to reg_write_reg_wait
[...]
Plenty of:
amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
[...]
And some crashes too:
 task:kwin_wayland    state:D stack:0     pid:1159  tgid:1159  ppid:1153   task_flags:0x400100 flags:0x00080003
 Call Trace:
  <TASK>
  __schedule+0x5f3/0x1ea0
  ? drm_ioctl+0x2a6/0x510
  ? sysvec_apic_timer_interrupt+0xe/0x80
  ? asm_sysvec_apic_timer_interrupt+0x1a/0x20
  schedule+0x55/0x170
  schedule_preempt_disabled+0x15/0x30
  __ww_mutex_lock+0x823/0x1050
  modeset_lock.llvm.4911137008902742515.cold+0x38/0x63
  drm_modeset_lock_all_ctx+0x33/0x170
  drm_mode_obj_get_properties_ioctl+0xdb/0x220
  drm_ioctl+0x27b/0x510
  ? __pfx_drm_mode_obj_get_properties_ioctl+0x10/0x10
  amdgpu_drm_ioctl+0x42/0x90 [amdgpu 5b5cc9b41fade2a33a1b7e61a8bfdb18c33cf438]
  __x64_sys_ioctl+0x207/0x2c0
  do_syscall_64+0x89/0x1f0
  ? __se_sys_close.llvm.10203526816879280367+0x7a/0x90
  ? do_syscall_64+0xc9/0x1f0
  ? do_syscall_64+0xc9/0x1f0
  ? do_syscall_64+0xc9/0x1f0
  ? do_syscall_64+0xc9/0x1f0
  entry_SYSCALL_64_after_hwframe+0x76/0x7e
 RIP: 0033:0x7f4ba9f3c17f
 RSP: 002b:00007ffcdf48a1b0 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
 RAX: ffffffffffffffda RBX: 000055ffcde42110 RCX: 00007f4ba9f3c17f
 RDX: 00007ffcdf48a250 RSI: 00000000c02064b9 RDI: 0000000000000013
 RBP: 00007ffcdf48a250 R08: 4e332f279cbf46e3 R09: 0000000000000020
 R10: 0000000000000021 R11: 0000000000000246 R12: 00000000c02064b9
 R13: 0000000000000013 R14: 0000000000000013 R15: cccccccc00000056
  </TASK>
 task:eDP-1           state:D stack:0     pid:1196  tgid:1159  ppid:1153   task_flags:0x400040 flags:0x00080003
 Call Trace:
  <TASK>
  __schedule+0x5f3/0x1ea0
  ? add_hole+0x157/0x1a0
  ? common_interrupt+0x13/0xa0
  ? asm_common_interrupt+0x26/0x40
  schedule+0x55/0x170
  schedule_preempt_disabled+0x15/0x30
  __mutex_lock_slowpath+0x21a/0x440
  amdgpu_mes_reg_write_reg_wait+0x9a/0x150 [amdgpu 5b5cc9b41fade2a33a1b7e61a8bfdb18c33cf438]
  amdgpu_gmc_flush_gpu_tlb+0x19c/0x330 [amdgpu 5b5cc9b41fade2a33a1b7e61a8bfdb18c33cf438]
  amdgpu_gart_invalidate_tlb+0x8c/0xb0 [amdgpu 5b5cc9b41fade2a33a1b7e61a8bfdb18c33cf438]
  amdgpu_ttm_alloc_gart+0x1a8/0x200 [amdgpu 5b5cc9b41fade2a33a1b7e61a8bfdb18c33cf438]
  amdgpu_dm_plane_helper_prepare_fb+0xe5/0x300 [amdgpu 5b5cc9b41fade2a33a1b7e61a8bfdb18c33cf438]
  drm_atomic_helper_prepare_planes.cold+0x5a/0x66
  drm_atomic_helper_commit+0x61/0x2a0
  drm_mode_atomic_ioctl.cold+0x2d8/0x3fc
  drm_ioctl+0x27b/0x510
  ? __pfx_drm_mode_atomic_ioctl+0x10/0x10
  amdgpu_drm_ioctl+0x42/0x90 [amdgpu 5b5cc9b41fade2a33a1b7e61a8bfdb18c33cf438]
  __x64_sys_ioctl+0x207/0x2c0
  do_syscall_64+0x89/0x1f0
  ? do_syscall_64+0xc9/0x1f0
  ? __x64_sys_poll+0xb9/0x150
  ? do_syscall_64+0xc9/0x1f0
  ? __x64_sys_sendmsg+0xa0/0xe0
  ? do_syscall_64+0xc9/0x1f0
  entry_SYSCALL_64_after_hwframe+0x76/0x7e
 RIP: 0033:0x7f4ba9f3c17f
 RSP: 002b:00007f4b8ddf94f0 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
 RAX: ffffffffffffffda RBX: 00007f4b88035d00 RCX: 00007f4ba9f3c17f
 RDX: 00007f4b8ddf95e0 RSI: 00000000c03864bc RDI: 0000000000000013
 RBP: 00007f4b8ddf95e0 R08: 00007f4b8800273c R09: 00007f4b88037570
 R10: 00007f4b88002680 R11: 0000000000000246 R12: 00000000c03864bc
 R13: 0000000000000013 R14: 00007f4b88037700 R15: 0000000000000000
  </TASK>
 amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
 amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
 amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
 amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
 amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
 amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
 amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
```

Output of rocminfo:
```
ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.18
Runtime Ext Version:     1.14
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
  Name:                    AMD Ryzen AI 7 350 w/ Radeon 860M
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen AI 7 350 w/ Radeon 860M
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
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   5090
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32121744(0x1ea2390) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32121744(0x1ea2390) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32121744(0x1ea2390) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32121744(0x1ea2390) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1152
  Uuid:                    GPU-XX
  Marketing Name:          AMD Radeon 860M Graphics
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
    L2:                      1024(0x400) KB
  Chip ID:                 4372(0x1114)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   3000
  BDFID:                   1024
  Internal Node ID:        1
  Compute Unit:            8
  SIMDs per CU:            2
  Shader Engines:          1
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Memory Properties:       APU
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
    x                        2147483647(0x7fffffff)
    y                        65535(0xffff)
    z                        65535(0xffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 16
  SDMA engine uCode::      15
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16060872(0xf511c8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16060872(0xf511c8) KB
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
      Name:                    amdgcn-amd-amdhsa--gfx1152
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
    ISA 2
      Name:                    amdgcn-amd-amdhsa--gfx11-generic
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
*******
Agent 3
*******
  Name:                    aie2
  Uuid:                    AIE-XX
  Marketing Name:          AIE-ML
  Vendor Name:             AMD
  Feature:                 AGENT_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        1(0x1)
  Queue Min Size:          64(0x40)
  Queue Max Size:          64(0x40)
  Queue Type:              SINGLE
  Node:                    0
  Device Type:             DSP
  Cache Info:
    L2:                      1024(0x400) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          0(0x0)
  Max Clock Freq. (MHz):   0
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            0
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:0
  Memory Properties:
  Features:                AGENT_DISPATCH
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, COARSE GRAINED
      Size:                    32121744(0x1ea2390) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65536(0x10000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32121744(0x1ea2390) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*** Done ***
```

### Additional Information

There's also issue #5724 but I don't think it's related, since I'm not using MES firmware 0x83 and not the same gfx architecture (mine is gfx1152, vs gfx1151 in the other issue)

Yet, I've tried the *solutions* in the other thread but it doesn't work.

I might have used AI workload in some boot, but the crash I'm reporting here is definitively without any AI workload when it happened. Video decoding was running through, if it could make sense.

---

## 评论 (32 条)

### 评论 #1 — amd-nicknick (2026-01-12T02:10:56Z)

Hi @X-Ryl669, I just took a look in our FW code, the 0x82 FW is not affected by #5724. You're hitting another issue here.
Could you please provide the full dmesg output to the failure? I might need to repro it on my side and see where CP is getting stuck at.
To facilitate this, I'd like to confirm your setup:
* Will a clean CachyOS desktop trigger this issue?
* Are there any special steps (eg. running specific application / sleep wake power cycle)?

---

### 评论 #2 — X-Ryl669 (2026-01-12T06:03:51Z)

Please find the dmesg [here](https://privatebin.net/?ba8b6fafa0c10507#gkpjoZWHnmp7AYLoRB6G8FiMVw16R7Psj2cRJGmmPC2)

I've a CachyOS desktop, using KDE. There's not much I've tweaked concerning amdgpu (it's the driver in the kernel, not a dkms build). Here's the modinfo amdgpu:
```
filename:       /lib/modules/6.18.3-2-cachyos/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.zst
author:         AMD linux driver team
description:    AMD GPU
license:        GPL and additional rights
firmware:       amdgpu/vega10_gpu_info.bin
firmware:       amdgpu/vega12_gpu_info.bin
firmware:       amdgpu/raven_gpu_info.bin
firmware:       amdgpu/picasso_gpu_info.bin
firmware:       amdgpu/raven2_gpu_info.bin
firmware:       amdgpu/arcturus_gpu_info.bin
firmware:       amdgpu/navi12_gpu_info.bin
firmware:       amdgpu/cyan_skillfish_gpu_info.bin
import_ns:      DMA_BUF
firmware:       amdgpu/ip_discovery.bin
firmware:       amdgpu/vega10_ip_discovery.bin
firmware:       amdgpu/vega12_ip_discovery.bin
firmware:       amdgpu/vega20_ip_discovery.bin
firmware:       amdgpu/raven_ip_discovery.bin
firmware:       amdgpu/raven2_ip_discovery.bin
firmware:       amdgpu/picasso_ip_discovery.bin
firmware:       amdgpu/arcturus_ip_discovery.bin
firmware:       amdgpu/aldebaran_ip_discovery.bin
firmware:       amdgpu/bonaire_pfp.bin
firmware:       amdgpu/bonaire_me.bin
firmware:       amdgpu/bonaire_ce.bin
firmware:       amdgpu/bonaire_rlc.bin
firmware:       amdgpu/bonaire_mec.bin
firmware:       amdgpu/hawaii_pfp.bin
firmware:       amdgpu/hawaii_me.bin
firmware:       amdgpu/hawaii_ce.bin
firmware:       amdgpu/hawaii_rlc.bin
firmware:       amdgpu/hawaii_mec.bin
firmware:       amdgpu/kaveri_pfp.bin
firmware:       amdgpu/kaveri_me.bin
firmware:       amdgpu/kaveri_ce.bin
firmware:       amdgpu/kaveri_rlc.bin
firmware:       amdgpu/kaveri_mec.bin
firmware:       amdgpu/kaveri_mec2.bin
firmware:       amdgpu/kabini_pfp.bin
firmware:       amdgpu/kabini_me.bin
firmware:       amdgpu/kabini_ce.bin
firmware:       amdgpu/kabini_rlc.bin
firmware:       amdgpu/kabini_mec.bin
firmware:       amdgpu/mullins_pfp.bin
firmware:       amdgpu/mullins_me.bin
firmware:       amdgpu/mullins_ce.bin
firmware:       amdgpu/mullins_rlc.bin
firmware:       amdgpu/mullins_mec.bin
firmware:       amdgpu/bonaire_sdma.bin
firmware:       amdgpu/bonaire_sdma1.bin
firmware:       amdgpu/hawaii_sdma.bin
firmware:       amdgpu/hawaii_sdma1.bin
firmware:       amdgpu/kaveri_sdma.bin
firmware:       amdgpu/kaveri_sdma1.bin
firmware:       amdgpu/kabini_sdma.bin
firmware:       amdgpu/kabini_sdma1.bin
firmware:       amdgpu/mullins_sdma.bin
firmware:       amdgpu/mullins_sdma1.bin
firmware:       amdgpu/tahiti_mc.bin
firmware:       amdgpu/pitcairn_mc.bin
firmware:       amdgpu/verde_mc.bin
firmware:       amdgpu/oland_mc.bin
firmware:       amdgpu/hainan_mc.bin
firmware:       amdgpu/si58_mc.bin
firmware:       amdgpu/tahiti_pfp.bin
firmware:       amdgpu/tahiti_me.bin
firmware:       amdgpu/tahiti_ce.bin
firmware:       amdgpu/tahiti_rlc.bin
firmware:       amdgpu/pitcairn_pfp.bin
firmware:       amdgpu/pitcairn_me.bin
firmware:       amdgpu/pitcairn_ce.bin
firmware:       amdgpu/pitcairn_rlc.bin
firmware:       amdgpu/verde_pfp.bin
firmware:       amdgpu/verde_me.bin
firmware:       amdgpu/verde_ce.bin
firmware:       amdgpu/verde_rlc.bin
firmware:       amdgpu/oland_pfp.bin
firmware:       amdgpu/oland_me.bin
firmware:       amdgpu/oland_ce.bin
firmware:       amdgpu/oland_rlc.bin
firmware:       amdgpu/hainan_pfp.bin
firmware:       amdgpu/hainan_me.bin
firmware:       amdgpu/hainan_ce.bin
firmware:       amdgpu/hainan_rlc.bin
firmware:       amdgpu/bonaire_mc.bin
firmware:       amdgpu/hawaii_mc.bin
firmware:       amdgpu/topaz_mc.bin
firmware:       amdgpu/tonga_mc.bin
firmware:       amdgpu/polaris11_mc.bin
firmware:       amdgpu/polaris10_mc.bin
firmware:       amdgpu/polaris12_mc.bin
firmware:       amdgpu/polaris12_32_mc.bin
firmware:       amdgpu/polaris11_k_mc.bin
firmware:       amdgpu/polaris10_k_mc.bin
firmware:       amdgpu/polaris12_k_mc.bin
firmware:       amdgpu/vega10_sos.bin
firmware:       amdgpu/vega10_asd.bin
firmware:       amdgpu/vega10_cap.bin
firmware:       amdgpu/vega12_sos.bin
firmware:       amdgpu/vega12_asd.bin
firmware:       amdgpu/raven_asd.bin
firmware:       amdgpu/picasso_asd.bin
firmware:       amdgpu/raven2_asd.bin
firmware:       amdgpu/picasso_ta.bin
firmware:       amdgpu/raven2_ta.bin
firmware:       amdgpu/raven_ta.bin
firmware:       amdgpu/vega20_sos.bin
firmware:       amdgpu/vega20_asd.bin
firmware:       amdgpu/vega20_ta.bin
firmware:       amdgpu/navi10_sos.bin
firmware:       amdgpu/navi10_asd.bin
firmware:       amdgpu/navi10_ta.bin
firmware:       amdgpu/navi14_sos.bin
firmware:       amdgpu/navi14_asd.bin
firmware:       amdgpu/navi14_ta.bin
firmware:       amdgpu/navi12_sos.bin
firmware:       amdgpu/navi12_asd.bin
firmware:       amdgpu/navi12_ta.bin
firmware:       amdgpu/navi12_cap.bin
firmware:       amdgpu/arcturus_sos.bin
firmware:       amdgpu/arcturus_asd.bin
firmware:       amdgpu/arcturus_ta.bin
firmware:       amdgpu/sienna_cichlid_sos.bin
firmware:       amdgpu/sienna_cichlid_ta.bin
firmware:       amdgpu/sienna_cichlid_cap.bin
firmware:       amdgpu/navy_flounder_sos.bin
firmware:       amdgpu/navy_flounder_ta.bin
firmware:       amdgpu/vangogh_asd.bin
firmware:       amdgpu/vangogh_toc.bin
firmware:       amdgpu/dimgrey_cavefish_sos.bin
firmware:       amdgpu/dimgrey_cavefish_ta.bin
firmware:       amdgpu/beige_goby_sos.bin
firmware:       amdgpu/beige_goby_ta.bin
firmware:       amdgpu/renoir_asd.bin
firmware:       amdgpu/renoir_ta.bin
firmware:       amdgpu/green_sardine_asd.bin
firmware:       amdgpu/green_sardine_ta.bin
firmware:       amdgpu/aldebaran_sos.bin
firmware:       amdgpu/aldebaran_ta.bin
firmware:       amdgpu/aldebaran_cap.bin
firmware:       amdgpu/yellow_carp_toc.bin
firmware:       amdgpu/yellow_carp_ta.bin
firmware:       amdgpu/psp_13_0_5_toc.bin
firmware:       amdgpu/psp_13_0_5_ta.bin
firmware:       amdgpu/psp_13_0_8_toc.bin
firmware:       amdgpu/psp_13_0_8_ta.bin
firmware:       amdgpu/psp_13_0_0_sos.bin
firmware:       amdgpu/psp_13_0_0_sos_kicker.bin
firmware:       amdgpu/psp_13_0_0_ta.bin
firmware:       amdgpu/psp_13_0_0_ta_kicker.bin
firmware:       amdgpu/psp_13_0_7_sos.bin
firmware:       amdgpu/psp_13_0_7_ta.bin
firmware:       amdgpu/psp_13_0_10_sos.bin
firmware:       amdgpu/psp_13_0_10_ta.bin
firmware:       amdgpu/psp_13_0_11_toc.bin
firmware:       amdgpu/psp_13_0_11_ta.bin
firmware:       amdgpu/psp_13_0_6_sos.bin
firmware:       amdgpu/psp_13_0_6_ta.bin
firmware:       amdgpu/psp_13_0_12_sos.bin
firmware:       amdgpu/psp_13_0_12_ta.bin
firmware:       amdgpu/psp_13_0_14_sos.bin
firmware:       amdgpu/psp_13_0_14_ta.bin
firmware:       amdgpu/psp_14_0_0_toc.bin
firmware:       amdgpu/psp_14_0_0_ta.bin
firmware:       amdgpu/psp_14_0_1_toc.bin
firmware:       amdgpu/psp_14_0_1_ta.bin
firmware:       amdgpu/psp_14_0_4_toc.bin
firmware:       amdgpu/psp_14_0_4_ta.bin
firmware:       amdgpu/psp_13_0_4_toc.bin
firmware:       amdgpu/psp_13_0_4_ta.bin
firmware:       amdgpu/psp_14_0_2_sos.bin
firmware:       amdgpu/psp_14_0_2_ta.bin
firmware:       amdgpu/psp_14_0_3_sos.bin
firmware:       amdgpu/psp_14_0_3_sos_kicker.bin
firmware:       amdgpu/psp_14_0_3_ta.bin
firmware:       amdgpu/psp_14_0_3_ta_kicker.bin
firmware:       amdgpu/psp_14_0_5_toc.bin
firmware:       amdgpu/psp_14_0_5_ta.bin
firmware:       amdgpu/carrizo_ce.bin
firmware:       amdgpu/carrizo_pfp.bin
firmware:       amdgpu/carrizo_me.bin
firmware:       amdgpu/carrizo_mec.bin
firmware:       amdgpu/carrizo_mec2.bin
firmware:       amdgpu/carrizo_rlc.bin
firmware:       amdgpu/stoney_ce.bin
firmware:       amdgpu/stoney_pfp.bin
firmware:       amdgpu/stoney_me.bin
firmware:       amdgpu/stoney_mec.bin
firmware:       amdgpu/stoney_rlc.bin
firmware:       amdgpu/tonga_ce.bin
firmware:       amdgpu/tonga_pfp.bin
firmware:       amdgpu/tonga_me.bin
firmware:       amdgpu/tonga_mec.bin
firmware:       amdgpu/tonga_mec2.bin
firmware:       amdgpu/tonga_rlc.bin
firmware:       amdgpu/topaz_ce.bin
firmware:       amdgpu/topaz_pfp.bin
firmware:       amdgpu/topaz_me.bin
firmware:       amdgpu/topaz_mec.bin
firmware:       amdgpu/topaz_rlc.bin
firmware:       amdgpu/fiji_ce.bin
firmware:       amdgpu/fiji_pfp.bin
firmware:       amdgpu/fiji_me.bin
firmware:       amdgpu/fiji_mec.bin
firmware:       amdgpu/fiji_mec2.bin
firmware:       amdgpu/fiji_rlc.bin
firmware:       amdgpu/polaris10_ce.bin
firmware:       amdgpu/polaris10_ce_2.bin
firmware:       amdgpu/polaris10_pfp.bin
firmware:       amdgpu/polaris10_pfp_2.bin
firmware:       amdgpu/polaris10_me.bin
firmware:       amdgpu/polaris10_me_2.bin
firmware:       amdgpu/polaris10_mec.bin
firmware:       amdgpu/polaris10_mec_2.bin
firmware:       amdgpu/polaris10_mec2.bin
firmware:       amdgpu/polaris10_mec2_2.bin
firmware:       amdgpu/polaris10_rlc.bin
firmware:       amdgpu/polaris11_ce.bin
firmware:       amdgpu/polaris11_ce_2.bin
firmware:       amdgpu/polaris11_pfp.bin
firmware:       amdgpu/polaris11_pfp_2.bin
firmware:       amdgpu/polaris11_me.bin
firmware:       amdgpu/polaris11_me_2.bin
firmware:       amdgpu/polaris11_mec.bin
firmware:       amdgpu/polaris11_mec_2.bin
firmware:       amdgpu/polaris11_mec2.bin
firmware:       amdgpu/polaris11_mec2_2.bin
firmware:       amdgpu/polaris11_rlc.bin
firmware:       amdgpu/polaris12_ce.bin
firmware:       amdgpu/polaris12_ce_2.bin
firmware:       amdgpu/polaris12_pfp.bin
firmware:       amdgpu/polaris12_pfp_2.bin
firmware:       amdgpu/polaris12_me.bin
firmware:       amdgpu/polaris12_me_2.bin
firmware:       amdgpu/polaris12_mec.bin
firmware:       amdgpu/polaris12_mec_2.bin
firmware:       amdgpu/polaris12_mec2.bin
firmware:       amdgpu/polaris12_mec2_2.bin
firmware:       amdgpu/polaris12_rlc.bin
firmware:       amdgpu/vegam_ce.bin
firmware:       amdgpu/vegam_pfp.bin
firmware:       amdgpu/vegam_me.bin
firmware:       amdgpu/vegam_mec.bin
firmware:       amdgpu/vegam_mec2.bin
firmware:       amdgpu/vegam_rlc.bin
firmware:       amdgpu/vega10_ce.bin
firmware:       amdgpu/vega10_pfp.bin
firmware:       amdgpu/vega10_me.bin
firmware:       amdgpu/vega10_mec.bin
firmware:       amdgpu/vega10_mec2.bin
firmware:       amdgpu/vega10_rlc.bin
firmware:       amdgpu/vega12_ce.bin
firmware:       amdgpu/vega12_pfp.bin
firmware:       amdgpu/vega12_me.bin
firmware:       amdgpu/vega12_mec.bin
firmware:       amdgpu/vega12_mec2.bin
firmware:       amdgpu/vega12_rlc.bin
firmware:       amdgpu/vega20_ce.bin
firmware:       amdgpu/vega20_pfp.bin
firmware:       amdgpu/vega20_me.bin
firmware:       amdgpu/vega20_mec.bin
firmware:       amdgpu/vega20_mec2.bin
firmware:       amdgpu/vega20_rlc.bin
firmware:       amdgpu/raven_ce.bin
firmware:       amdgpu/raven_pfp.bin
firmware:       amdgpu/raven_me.bin
firmware:       amdgpu/raven_mec.bin
firmware:       amdgpu/raven_mec2.bin
firmware:       amdgpu/raven_rlc.bin
firmware:       amdgpu/picasso_ce.bin
firmware:       amdgpu/picasso_pfp.bin
firmware:       amdgpu/picasso_me.bin
firmware:       amdgpu/picasso_mec.bin
firmware:       amdgpu/picasso_mec2.bin
firmware:       amdgpu/picasso_rlc.bin
firmware:       amdgpu/picasso_rlc_am4.bin
firmware:       amdgpu/raven2_ce.bin
firmware:       amdgpu/raven2_pfp.bin
firmware:       amdgpu/raven2_me.bin
firmware:       amdgpu/raven2_mec.bin
firmware:       amdgpu/raven2_mec2.bin
firmware:       amdgpu/raven2_rlc.bin
firmware:       amdgpu/raven_kicker_rlc.bin
firmware:       amdgpu/arcturus_mec.bin
firmware:       amdgpu/arcturus_rlc.bin
firmware:       amdgpu/renoir_ce.bin
firmware:       amdgpu/renoir_pfp.bin
firmware:       amdgpu/renoir_me.bin
firmware:       amdgpu/renoir_mec.bin
firmware:       amdgpu/renoir_rlc.bin
firmware:       amdgpu/green_sardine_ce.bin
firmware:       amdgpu/green_sardine_pfp.bin
firmware:       amdgpu/green_sardine_me.bin
firmware:       amdgpu/green_sardine_mec.bin
firmware:       amdgpu/green_sardine_mec2.bin
firmware:       amdgpu/green_sardine_rlc.bin
firmware:       amdgpu/aldebaran_mec.bin
firmware:       amdgpu/aldebaran_mec2.bin
firmware:       amdgpu/aldebaran_rlc.bin
firmware:       amdgpu/aldebaran_sjt_mec.bin
firmware:       amdgpu/aldebaran_sjt_mec2.bin
firmware:       amdgpu/gc_9_4_3_mec.bin
firmware:       amdgpu/gc_9_4_4_mec.bin
firmware:       amdgpu/gc_9_5_0_mec.bin
firmware:       amdgpu/gc_9_4_3_rlc.bin
firmware:       amdgpu/gc_9_4_4_rlc.bin
firmware:       amdgpu/gc_9_5_0_rlc.bin
firmware:       amdgpu/gc_9_4_3_sjt_mec.bin
firmware:       amdgpu/gc_9_4_4_sjt_mec.bin
firmware:       amdgpu/navi10_ce.bin
firmware:       amdgpu/navi10_pfp.bin
firmware:       amdgpu/navi10_me.bin
firmware:       amdgpu/navi10_mec.bin
firmware:       amdgpu/navi10_mec2.bin
firmware:       amdgpu/navi10_rlc.bin
firmware:       amdgpu/navi14_ce_wks.bin
firmware:       amdgpu/navi14_pfp_wks.bin
firmware:       amdgpu/navi14_me_wks.bin
firmware:       amdgpu/navi14_mec_wks.bin
firmware:       amdgpu/navi14_mec2_wks.bin
firmware:       amdgpu/navi14_ce.bin
firmware:       amdgpu/navi14_pfp.bin
firmware:       amdgpu/navi14_me.bin
firmware:       amdgpu/navi14_mec.bin
firmware:       amdgpu/navi14_mec2.bin
firmware:       amdgpu/navi14_rlc.bin
firmware:       amdgpu/navi12_ce.bin
firmware:       amdgpu/navi12_pfp.bin
firmware:       amdgpu/navi12_me.bin
firmware:       amdgpu/navi12_mec.bin
firmware:       amdgpu/navi12_mec2.bin
firmware:       amdgpu/navi12_rlc.bin
firmware:       amdgpu/sienna_cichlid_ce.bin
firmware:       amdgpu/sienna_cichlid_pfp.bin
firmware:       amdgpu/sienna_cichlid_me.bin
firmware:       amdgpu/sienna_cichlid_mec.bin
firmware:       amdgpu/sienna_cichlid_mec2.bin
firmware:       amdgpu/sienna_cichlid_rlc.bin
firmware:       amdgpu/navy_flounder_ce.bin
firmware:       amdgpu/navy_flounder_pfp.bin
firmware:       amdgpu/navy_flounder_me.bin
firmware:       amdgpu/navy_flounder_mec.bin
firmware:       amdgpu/navy_flounder_mec2.bin
firmware:       amdgpu/navy_flounder_rlc.bin
firmware:       amdgpu/vangogh_ce.bin
firmware:       amdgpu/vangogh_pfp.bin
firmware:       amdgpu/vangogh_me.bin
firmware:       amdgpu/vangogh_mec.bin
firmware:       amdgpu/vangogh_mec2.bin
firmware:       amdgpu/vangogh_rlc.bin
firmware:       amdgpu/dimgrey_cavefish_ce.bin
firmware:       amdgpu/dimgrey_cavefish_pfp.bin
firmware:       amdgpu/dimgrey_cavefish_me.bin
firmware:       amdgpu/dimgrey_cavefish_mec.bin
firmware:       amdgpu/dimgrey_cavefish_mec2.bin
firmware:       amdgpu/dimgrey_cavefish_rlc.bin
firmware:       amdgpu/beige_goby_ce.bin
firmware:       amdgpu/beige_goby_pfp.bin
firmware:       amdgpu/beige_goby_me.bin
firmware:       amdgpu/beige_goby_mec.bin
firmware:       amdgpu/beige_goby_mec2.bin
firmware:       amdgpu/beige_goby_rlc.bin
firmware:       amdgpu/yellow_carp_ce.bin
firmware:       amdgpu/yellow_carp_pfp.bin
firmware:       amdgpu/yellow_carp_me.bin
firmware:       amdgpu/yellow_carp_mec.bin
firmware:       amdgpu/yellow_carp_mec2.bin
firmware:       amdgpu/yellow_carp_rlc.bin
firmware:       amdgpu/cyan_skillfish2_ce.bin
firmware:       amdgpu/cyan_skillfish2_pfp.bin
firmware:       amdgpu/cyan_skillfish2_me.bin
firmware:       amdgpu/cyan_skillfish2_mec.bin
firmware:       amdgpu/cyan_skillfish2_mec2.bin
firmware:       amdgpu/cyan_skillfish2_rlc.bin
firmware:       amdgpu/gc_10_3_6_ce.bin
firmware:       amdgpu/gc_10_3_6_pfp.bin
firmware:       amdgpu/gc_10_3_6_me.bin
firmware:       amdgpu/gc_10_3_6_mec.bin
firmware:       amdgpu/gc_10_3_6_mec2.bin
firmware:       amdgpu/gc_10_3_6_rlc.bin
firmware:       amdgpu/gc_10_3_7_ce.bin
firmware:       amdgpu/gc_10_3_7_pfp.bin
firmware:       amdgpu/gc_10_3_7_me.bin
firmware:       amdgpu/gc_10_3_7_mec.bin
firmware:       amdgpu/gc_10_3_7_mec2.bin
firmware:       amdgpu/gc_10_3_7_rlc.bin
firmware:       amdgpu/gc_11_0_0_imu.bin
firmware:       amdgpu/gc_11_0_0_imu_kicker.bin
firmware:       amdgpu/gc_11_0_1_imu.bin
firmware:       amdgpu/gc_11_0_2_imu.bin
firmware:       amdgpu/gc_11_0_3_imu.bin
firmware:       amdgpu/gc_11_0_4_imu.bin
firmware:       amdgpu/gc_11_5_0_imu.bin
firmware:       amdgpu/gc_11_5_1_imu.bin
firmware:       amdgpu/gc_11_5_2_imu.bin
firmware:       amdgpu/gc_11_5_3_imu.bin
firmware:       amdgpu/gc_11_0_0_pfp.bin
firmware:       amdgpu/gc_11_0_0_me.bin
firmware:       amdgpu/gc_11_0_0_mec.bin
firmware:       amdgpu/gc_11_0_0_rlc.bin
firmware:       amdgpu/gc_11_0_0_rlc_kicker.bin
firmware:       amdgpu/gc_11_0_0_rlc_1.bin
firmware:       amdgpu/gc_11_0_0_toc.bin
firmware:       amdgpu/gc_11_0_1_pfp.bin
firmware:       amdgpu/gc_11_0_1_me.bin
firmware:       amdgpu/gc_11_0_1_mec.bin
firmware:       amdgpu/gc_11_0_1_rlc.bin
firmware:       amdgpu/gc_11_0_2_pfp.bin
firmware:       amdgpu/gc_11_0_2_me.bin
firmware:       amdgpu/gc_11_0_2_mec.bin
firmware:       amdgpu/gc_11_0_2_rlc.bin
firmware:       amdgpu/gc_11_0_3_pfp.bin
firmware:       amdgpu/gc_11_0_3_me.bin
firmware:       amdgpu/gc_11_0_3_mec.bin
firmware:       amdgpu/gc_11_0_3_rlc.bin
firmware:       amdgpu/gc_11_0_4_pfp.bin
firmware:       amdgpu/gc_11_0_4_me.bin
firmware:       amdgpu/gc_11_0_4_mec.bin
firmware:       amdgpu/gc_11_0_4_rlc.bin
firmware:       amdgpu/gc_11_5_0_pfp.bin
firmware:       amdgpu/gc_11_5_0_me.bin
firmware:       amdgpu/gc_11_5_0_mec.bin
firmware:       amdgpu/gc_11_5_0_rlc.bin
firmware:       amdgpu/gc_11_5_1_pfp.bin
firmware:       amdgpu/gc_11_5_1_me.bin
firmware:       amdgpu/gc_11_5_1_mec.bin
firmware:       amdgpu/gc_11_5_1_rlc.bin
firmware:       amdgpu/gc_11_5_2_pfp.bin
firmware:       amdgpu/gc_11_5_2_me.bin
firmware:       amdgpu/gc_11_5_2_mec.bin
firmware:       amdgpu/gc_11_5_2_rlc.bin
firmware:       amdgpu/gc_11_5_3_pfp.bin
firmware:       amdgpu/gc_11_5_3_me.bin
firmware:       amdgpu/gc_11_5_3_mec.bin
firmware:       amdgpu/gc_11_5_3_rlc.bin
firmware:       amdgpu/gc_12_0_0_pfp.bin
firmware:       amdgpu/gc_12_0_0_me.bin
firmware:       amdgpu/gc_12_0_0_mec.bin
firmware:       amdgpu/gc_12_0_0_rlc.bin
firmware:       amdgpu/gc_12_0_0_toc.bin
firmware:       amdgpu/gc_12_0_1_pfp.bin
firmware:       amdgpu/gc_12_0_1_me.bin
firmware:       amdgpu/gc_12_0_1_mec.bin
firmware:       amdgpu/gc_12_0_1_rlc.bin
firmware:       amdgpu/gc_12_0_1_rlc_kicker.bin
firmware:       amdgpu/gc_12_0_1_toc.bin
firmware:       amdgpu/gc_12_0_0_imu.bin
firmware:       amdgpu/gc_12_0_1_imu.bin
firmware:       amdgpu/gc_12_0_1_imu_kicker.bin
firmware:       amdgpu/topaz_sdma.bin
firmware:       amdgpu/topaz_sdma1.bin
firmware:       amdgpu/tonga_sdma.bin
firmware:       amdgpu/tonga_sdma1.bin
firmware:       amdgpu/carrizo_sdma.bin
firmware:       amdgpu/carrizo_sdma1.bin
firmware:       amdgpu/fiji_sdma.bin
firmware:       amdgpu/fiji_sdma1.bin
firmware:       amdgpu/stoney_sdma.bin
firmware:       amdgpu/polaris10_sdma.bin
firmware:       amdgpu/polaris10_sdma1.bin
firmware:       amdgpu/polaris11_sdma.bin
firmware:       amdgpu/polaris11_sdma1.bin
firmware:       amdgpu/polaris12_sdma.bin
firmware:       amdgpu/polaris12_sdma1.bin
firmware:       amdgpu/vegam_sdma.bin
firmware:       amdgpu/vegam_sdma1.bin
firmware:       amdgpu/vega10_sdma.bin
firmware:       amdgpu/vega10_sdma1.bin
firmware:       amdgpu/vega12_sdma.bin
firmware:       amdgpu/vega12_sdma1.bin
firmware:       amdgpu/vega20_sdma.bin
firmware:       amdgpu/vega20_sdma1.bin
firmware:       amdgpu/raven_sdma.bin
firmware:       amdgpu/picasso_sdma.bin
firmware:       amdgpu/raven2_sdma.bin
firmware:       amdgpu/arcturus_sdma.bin
firmware:       amdgpu/renoir_sdma.bin
firmware:       amdgpu/green_sardine_sdma.bin
firmware:       amdgpu/aldebaran_sdma.bin
firmware:       amdgpu/sdma_4_4_2.bin
firmware:       amdgpu/sdma_4_4_4.bin
firmware:       amdgpu/sdma_4_4_5.bin
firmware:       amdgpu/navi10_sdma.bin
firmware:       amdgpu/navi10_sdma1.bin
firmware:       amdgpu/navi14_sdma.bin
firmware:       amdgpu/navi14_sdma1.bin
firmware:       amdgpu/navi12_sdma.bin
firmware:       amdgpu/navi12_sdma1.bin
firmware:       amdgpu/cyan_skillfish2_sdma.bin
firmware:       amdgpu/cyan_skillfish2_sdma1.bin
firmware:       amdgpu/sienna_cichlid_sdma.bin
firmware:       amdgpu/navy_flounder_sdma.bin
firmware:       amdgpu/dimgrey_cavefish_sdma.bin
firmware:       amdgpu/beige_goby_sdma.bin
firmware:       amdgpu/vangogh_sdma.bin
firmware:       amdgpu/yellow_carp_sdma.bin
firmware:       amdgpu/sdma_5_2_6.bin
firmware:       amdgpu/sdma_5_2_7.bin
firmware:       amdgpu/sdma_6_0_0.bin
firmware:       amdgpu/sdma_6_0_1.bin
firmware:       amdgpu/sdma_6_0_2.bin
firmware:       amdgpu/sdma_6_0_3.bin
firmware:       amdgpu/sdma_6_1_0.bin
firmware:       amdgpu/sdma_6_1_1.bin
firmware:       amdgpu/sdma_6_1_2.bin
firmware:       amdgpu/sdma_6_1_3.bin
firmware:       amdgpu/sdma_7_0_0.bin
firmware:       amdgpu/sdma_7_0_1.bin
firmware:       amdgpu/gc_11_0_0_mes.bin
firmware:       amdgpu/gc_11_0_0_mes_2.bin
firmware:       amdgpu/gc_11_0_0_mes1.bin
firmware:       amdgpu/gc_11_0_1_mes.bin
firmware:       amdgpu/gc_11_0_1_mes_2.bin
firmware:       amdgpu/gc_11_0_1_mes1.bin
firmware:       amdgpu/gc_11_0_2_mes.bin
firmware:       amdgpu/gc_11_0_2_mes_2.bin
firmware:       amdgpu/gc_11_0_2_mes1.bin
firmware:       amdgpu/gc_11_0_3_mes.bin
firmware:       amdgpu/gc_11_0_3_mes_2.bin
firmware:       amdgpu/gc_11_0_3_mes1.bin
firmware:       amdgpu/gc_11_0_4_mes.bin
firmware:       amdgpu/gc_11_0_4_mes_2.bin
firmware:       amdgpu/gc_11_0_4_mes1.bin
firmware:       amdgpu/gc_11_5_0_mes_2.bin
firmware:       amdgpu/gc_11_5_0_mes1.bin
firmware:       amdgpu/gc_11_5_1_mes_2.bin
firmware:       amdgpu/gc_11_5_1_mes1.bin
firmware:       amdgpu/gc_11_5_2_mes_2.bin
firmware:       amdgpu/gc_11_5_2_mes1.bin
firmware:       amdgpu/gc_11_5_3_mes_2.bin
firmware:       amdgpu/gc_11_5_3_mes1.bin
firmware:       amdgpu/gc_12_0_0_mes.bin
firmware:       amdgpu/gc_12_0_0_mes1.bin
firmware:       amdgpu/gc_12_0_0_uni_mes.bin
firmware:       amdgpu/gc_12_0_1_mes.bin
firmware:       amdgpu/gc_12_0_1_mes1.bin
firmware:       amdgpu/gc_12_0_1_uni_mes.bin
firmware:       amdgpu/tahiti_uvd.bin
firmware:       amdgpu/verde_uvd.bin
firmware:       amdgpu/pitcairn_uvd.bin
firmware:       amdgpu/oland_uvd.bin
firmware:       amdgpu/bonaire_uvd.bin
firmware:       amdgpu/kabini_uvd.bin
firmware:       amdgpu/kaveri_uvd.bin
firmware:       amdgpu/hawaii_uvd.bin
firmware:       amdgpu/mullins_uvd.bin
firmware:       amdgpu/tonga_uvd.bin
firmware:       amdgpu/carrizo_uvd.bin
firmware:       amdgpu/fiji_uvd.bin
firmware:       amdgpu/stoney_uvd.bin
firmware:       amdgpu/polaris10_uvd.bin
firmware:       amdgpu/polaris11_uvd.bin
firmware:       amdgpu/polaris12_uvd.bin
firmware:       amdgpu/vegam_uvd.bin
firmware:       amdgpu/vega10_uvd.bin
firmware:       amdgpu/vega12_uvd.bin
firmware:       amdgpu/vega20_uvd.bin
firmware:       amdgpu/bonaire_vce.bin
firmware:       amdgpu/kabini_vce.bin
firmware:       amdgpu/kaveri_vce.bin
firmware:       amdgpu/hawaii_vce.bin
firmware:       amdgpu/mullins_vce.bin
firmware:       amdgpu/tonga_vce.bin
firmware:       amdgpu/carrizo_vce.bin
firmware:       amdgpu/fiji_vce.bin
firmware:       amdgpu/stoney_vce.bin
firmware:       amdgpu/polaris10_vce.bin
firmware:       amdgpu/polaris11_vce.bin
firmware:       amdgpu/polaris12_vce.bin
firmware:       amdgpu/vegam_vce.bin
firmware:       amdgpu/vega10_vce.bin
firmware:       amdgpu/vega12_vce.bin
firmware:       amdgpu/vega20_vce.bin
firmware:       amdgpu/raven_vcn.bin
firmware:       amdgpu/picasso_vcn.bin
firmware:       amdgpu/raven2_vcn.bin
firmware:       amdgpu/arcturus_vcn.bin
firmware:       amdgpu/renoir_vcn.bin
firmware:       amdgpu/green_sardine_vcn.bin
firmware:       amdgpu/aldebaran_vcn.bin
firmware:       amdgpu/navi10_vcn.bin
firmware:       amdgpu/navi14_vcn.bin
firmware:       amdgpu/navi12_vcn.bin
firmware:       amdgpu/sienna_cichlid_vcn.bin
firmware:       amdgpu/navy_flounder_vcn.bin
firmware:       amdgpu/vangogh_vcn.bin
firmware:       amdgpu/dimgrey_cavefish_vcn.bin
firmware:       amdgpu/beige_goby_vcn.bin
firmware:       amdgpu/yellow_carp_vcn.bin
firmware:       amdgpu/vcn_3_1_2.bin
firmware:       amdgpu/vcn_4_0_0.bin
firmware:       amdgpu/vcn_4_0_2.bin
firmware:       amdgpu/vcn_4_0_3.bin
firmware:       amdgpu/vcn_4_0_4.bin
firmware:       amdgpu/vcn_4_0_5.bin
firmware:       amdgpu/vcn_4_0_6.bin
firmware:       amdgpu/vcn_4_0_6_1.bin
firmware:       amdgpu/vcn_5_0_0.bin
firmware:       amdgpu/vcn_5_0_1.bin
firmware:       amdgpu/vpe_6_1_0.bin
firmware:       amdgpu/vpe_6_1_1.bin
firmware:       amdgpu/vpe_6_1_3.bin
firmware:       amdgpu/umsch_mm_4_0_0.bin
firmware:       amdgpu/arcturus_smc.bin
firmware:       amdgpu/navi10_smc.bin
firmware:       amdgpu/navi14_smc.bin
firmware:       amdgpu/navi12_smc.bin
firmware:       amdgpu/sienna_cichlid_smc.bin
firmware:       amdgpu/navy_flounder_smc.bin
firmware:       amdgpu/dimgrey_cavefish_smc.bin
firmware:       amdgpu/beige_goby_smc.bin
firmware:       amdgpu/aldebaran_smc.bin
firmware:       amdgpu/smu_13_0_0.bin
firmware:       amdgpu/smu_13_0_0_kicker.bin
firmware:       amdgpu/smu_13_0_7.bin
firmware:       amdgpu/smu_13_0_10.bin
firmware:       amdgpu/smu_13_0_6.bin
firmware:       amdgpu/smu_13_0_14.bin
firmware:       amdgpu/smu_14_0_2.bin
firmware:       amdgpu/smu_14_0_3.bin
firmware:       amdgpu/smu_14_0_3_kicker.bin
firmware:       amdgpu/bonaire_smc.bin
firmware:       amdgpu/bonaire_k_smc.bin
firmware:       amdgpu/hawaii_smc.bin
firmware:       amdgpu/hawaii_k_smc.bin
firmware:       amdgpu/topaz_smc.bin
firmware:       amdgpu/topaz_k_smc.bin
firmware:       amdgpu/tonga_smc.bin
firmware:       amdgpu/tonga_k_smc.bin
firmware:       amdgpu/fiji_smc.bin
firmware:       amdgpu/polaris10_smc.bin
firmware:       amdgpu/polaris10_smc_sk.bin
firmware:       amdgpu/polaris10_k_smc.bin
firmware:       amdgpu/polaris10_k2_smc.bin
firmware:       amdgpu/polaris11_smc.bin
firmware:       amdgpu/polaris11_smc_sk.bin
firmware:       amdgpu/polaris11_k_smc.bin
firmware:       amdgpu/polaris11_k2_smc.bin
firmware:       amdgpu/polaris12_smc.bin
firmware:       amdgpu/polaris12_k_smc.bin
firmware:       amdgpu/vegam_smc.bin
firmware:       amdgpu/vega10_smc.bin
firmware:       amdgpu/vega10_acg_smc.bin
firmware:       amdgpu/vega12_smc.bin
firmware:       amdgpu/vega20_smc.bin
firmware:       amdgpu/tahiti_smc.bin
firmware:       amdgpu/pitcairn_smc.bin
firmware:       amdgpu/pitcairn_k_smc.bin
firmware:       amdgpu/verde_smc.bin
firmware:       amdgpu/verde_k_smc.bin
firmware:       amdgpu/oland_smc.bin
firmware:       amdgpu/oland_k_smc.bin
firmware:       amdgpu/hainan_smc.bin
firmware:       amdgpu/hainan_k_smc.bin
firmware:       amdgpu/banks_k_2_smc.bin
firmware:       amdgpu/renoir_dmcub.bin
firmware:       amdgpu/sienna_cichlid_dmcub.bin
firmware:       amdgpu/navy_flounder_dmcub.bin
firmware:       amdgpu/green_sardine_dmcub.bin
firmware:       amdgpu/vangogh_dmcub.bin
firmware:       amdgpu/dimgrey_cavefish_dmcub.bin
firmware:       amdgpu/beige_goby_dmcub.bin
firmware:       amdgpu/yellow_carp_dmcub.bin
firmware:       amdgpu/dcn_3_1_4_dmcub.bin
firmware:       amdgpu/dcn_3_1_5_dmcub.bin
firmware:       amdgpu/dcn_3_1_6_dmcub.bin
firmware:       amdgpu/dcn_3_2_0_dmcub.bin
firmware:       amdgpu/dcn_3_2_1_dmcub.bin
firmware:       amdgpu/raven_dmcu.bin
firmware:       amdgpu/navi12_dmcu.bin
firmware:       amdgpu/dcn_3_5_dmcub.bin
firmware:       amdgpu/dcn_3_5_1_dmcub.bin
firmware:       amdgpu/dcn_3_6_dmcub.bin
firmware:       amdgpu/dcn_4_0_1_dmcub.bin
firmware:       amdgpu/isp_4_1_1.bin
name:           amdgpu
intree:         Y
depends:        drm_display_helper,drm_ttm_helper,amdxcp,ttm,gpu-sched,i2c-algo-bit,drm_exec,video,drm_suballoc_helper,drm_buddy,cec,drm_panel_backlight_quirks
[... aliases here ...]
srcversion:     A30ECB1D9B70AEA03E5A7E3
vermagic:       6.18.3-2-cachyos SMP preempt mod_unload
retpoline:      Y
sig_id:         PKCS#7
signer:         Build time autogenerated kernel key
sig_key:        0E:66:95:0D:48:43:0A:5D:CA:B7:90:5A:17:9E:73:85:E3:68:F5:DA
sig_hashalgo:   sha512
signature:      30:65:02:30:1E:04:95:DD:38:58:56:79:66:6D:C0:E2:04:3F:21:3D:
                71:D8:58:6B:9A:09:39:28:2B:C4:8D:C6:5A:0F:EC:F1:3D:BE:64:2E:
                ED:8C:EC:48:D8:17:4A:EB:6D:FC:CC:5A:02:31:00:C0:8D:19:11:97:
                35:3D:6A:1C:91:6E:55:B0:9E:5A:7A:79:0D:81:FF:46:DD:99:63:82:
                9F:00:27:E1:6E:42:89:88:10:B3:AF:EC:CE:91:B5:1B:7D:95:37:DE:
                E8:7F:E7
parm:           user_queue:Enable user queues (-1 = auto (default), 0 = disable, 1 = enable, 2 = enable UQs and disable KQs) (int)
parm:           rebar:Resizable BAR (-1 = auto (default), 0 = disable, 1 = enable) (int)
parm:           wbrf:Enable Wifi RFI interference mitigation (0 = disabled, 1 = enabled, -1 = auto(default) (int)
parm:           agp:AGP (-1 = auto (default), 0 = disable, 1 = enable) (int)
parm:           debug_mask:debug options for amdgpu, disabled by default (uint)
parm:           seamless:Seamless boot (-1 = auto (default), 0 = disable, 1 = enable) (int)
parm:           modeset:Override nomodeset (1 = enable, -1 = auto) (int)
parm:           enforce_isolation:enforce process isolation between graphics and compute. (-1 = auto, 0 = disable, 1 = enable, 2 = enable legacy mode, 3 = enable without cleaner shader) (int)
parm:           user_partt_mode:specify partition mode to be used (-2 = AMDGPU_AUTO_COMPUTE_PARTITION_MODE(default value)                                               0 = AMDGPU_SPX_PARTITION_MODE,               1 = AMDGPU_DPX_PARTITION_MODE,                                           2 = AMDGPU_TPX_PARTITION_MODE,                                          3 = AMDGPU_QPX_PARTITION_MODE,                                       4 = AMDGPU_CPX_PARTITION_MODE) (uint)
parm:           smu_pptable_id:specify pptable id to be used (-1 = auto(default) value, 0 = use pptable from vbios, > 0 = soft pptable id) (int)
parm:           umsch_mm_fwlog:Enable umschfw log(0 = disable (default value), 1 = enable) (int)
parm:           umsch_mm:Enable Multi Media User Mode Scheduler (0 = disabled (default), 1 = enabled) (int)
parm:           sg_display:S/G Display (-1 = auto (default), 0 = disable) (int)
parm:           vcnfw_log:Enable vcnfw log(0 = disable (default value), 1 = enable) (int)
parm:           num_kcq:number of kernel compute queue user want to setup (8 if set to greater than 8 or less than 0, only affect gfx 8+) (int)
parm:           bad_page_threshold:Bad page threshold(-1 = ignore threshold (default value), 0 = disable bad page retirement, -2 = threshold determined by a formula, 0 < threshold < max records, user-defined threshold) (int)
parm:           reset_method:GPU reset method (-1 = auto (default), 0 = legacy, 1 = mode0, 2 = mode1, 3 = mode2, 4 = baco/bamaco) (int)
parm:           freesync_video:Adds additional modes via VRR for refresh changes without a full modeset (0 = off (default), 1 = on) (uint)
parm:           tmz:Enable TMZ feature (-1 = auto (default), 0 = off, 1 = on) (int)
parm:           damageclips:Damage clips support (0 = disable, 1 = enable, -1 auto (default)) (int)
parm:           backlight:Backlight control (0 = pwm, 1 = aux, -1 auto (default)) (bint)
parm:           abmlevel:ABM level (0 = off, 1-4 = backlight reduction level, -1 auto (default)) (int)
parm:           visualconfirm:Visual confirm (0 = off (default), 1 = MPO, 5 = PSR) (uint)
parm:           dcdebugmask:all debug options disabled (default)) (uint)
parm:           dcfeaturemask:all stable DC features enabled (default)) (uint)
parm:           mtype_local:MTYPE for local memory (0 = MTYPE_RW (default), 1 = MTYPE_NC, 2 = MTYPE_CC) (int)
parm:           no_queue_eviction_on_vm_fault:No queue eviction on VM fault (0 = queue eviction, 1 = no queue eviction) (int)
parm:           no_system_mem_limit:disable system memory limit (false = default) (bool)
parm:           debug_evictions:enable eviction debug messages (false = default) (bool)
parm:           queue_preemption_timeout_ms:queue preemption timeout in ms (1 = Minimum, 9000 = default) (int)
parm:           hws_gws_support:Assume MEC2 FW supports GWS barriers (false = rely on FW version check (Default), true = force supported) (bool)
parm:           halt_if_hws_hang:Halt if HWS hang is detected (0 = off (default), 1 = on) (int)
parm:           send_sigterm:Send sigterm to HSA process on unhandled exception (0 = disable, 1 = enable) (int)
parm:           max_num_of_queues_per_device:Maximum number of supported queues per device (1 = Minimum, 4096 = default) (int)
parm:           cwsr_enable:CWSR enable (0 = Off, 1 = On (Default)) (int)
parm:           hws_max_conc_proc:Max # processes HWS can execute concurrently when sched_policy=0 (0 = no concurrency, #VMIDs for KFD = Maximum(default)) (int)
parm:           sched_policy:Scheduling policy (0 = HWS (Default), 1 = HWS without over-subscription, 2 = Non-HWS (Used for debugging only) (int)
parm:           use_xgmi_p2p:Enable XGMI P2P interface (0 = disable; 1 = enable (default)) (int)
parm:           force_asic_type:A non negative value used to specify the asic type for all supported GPUs (int)
parm:           noretry:Disable retry faults (0 = retry enabled, 1 = retry disabled, -1 auto (default)) (int)
parm:           uni_mes:Enable Unified Micro Engine Scheduler (0 = disabled, 1 = enabled(default) (int)
parm:           mes_kiq:Enable Micro Engine Scheduler KIQ (0 = disabled (default), 1 = enabled) (int)
parm:           mes_log_enable:Enable Micro Engine Scheduler log (0 = disabled (default), 1 = enabled) (int)
parm:           mes:Enable Micro Engine Scheduler (0 = disabled (default), 1 = enabled) (int)
parm:           discovery:Allow driver to discover hardware IPs from IP Discovery table at the top of VRAM (int)
parm:           mcbp:Enable Mid-command buffer preemption (0 = disabled, 1 = enabled), -1 = auto (default) (int)
parm:           async_gfx_ring:Asynchronous GFX rings that could be configured with either different priorities (HP3D ring and LP3D ring), or equal priorities (0 = disabled, 1 = enabled (default)) (int)
parm:           smu_memory_pool_size:reserve gtt for smu debug usage, 0 = disable,0x1 = 256Mbyte, 0x2 = 512Mbyte, 0x4 = 1 Gbyte, 0x8 = 2GByte (uint)
parm:           cik_support:CIK support (1 = enabled, 0 = disabled (default)) (int)
parm:           si_support:SI support (1 = enabled, 0 = disabled (default)) (int)
parm:           timeout_period:watchdog timeout period (0 = timeout disabled, 1 ~ 0x23 = timeout maxcycles = (1 << period) (uint)
parm:           timeout_fatal_disable:disable watchdog timeout fatal error (false = default) (bool)
parm:           ras_mask:Mask of RAS features to enable (default 0xffffffff), only valid when ras_enable == 1 (uint)
parm:           ras_enable:Enable RAS features on the GPU (0 = disable, 1 = enable, -1 = auto (default)) (int)
parm:           emu_mode:Emulation mode, (1 = enable, 0 = disable) (int)
parm:           gpu_recovery:Enable GPU recovery mechanism, (1 = enable, 0 = disable, -1 = auto) (int)
parm:           compute_multipipe:Force compute queues to be spread across pipes (1 = enable, 0 = disable, -1 = auto) (int)
parm:           lbpw:Load Balancing Per Watt (LBPW) support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           virtual_display:Enable virtual display feature (the virtual_display will be set like xxxx:xx:xx.x,x;xxxx:xx:xx.x,x) (charp)
parm:           disable_cu:Disable CUs (se.sh.cu,...) (charp)
parm:           sdma_phase_quantum:SDMA context switch phase quantum (x 1K GPU clock cycles, 0 = no change (default 32)) (uint)
parm:           pg_mask:Powergating flags mask (0 = disable power gating) (uint)
parm:           cg_mask:Clockgating flags mask (0 = disable clock gating) (ullong)
parm:           pcie_lane_cap:PCIE Lane Caps (0: autodetect (default)) (uint)
parm:           pcie_gen_cap:PCIE Gen Caps (0: autodetect (default)) (uint)
parm:           forcelongtraining:force memory long training (uint)
parm:           ppfeaturemask:all power features enabled (default)) (hexint)
parm:           sched_hw_submission:the max number of HW submissions (default 2) (int)
parm:           sched_jobs:the max number of jobs supported in the sw queue (default 32) (int)
parm:           dc:Display Core driver (1 = enable, 0 = disable, -1 = auto (default)) (int)
parm:           exp_hw_support:experimental hw support (1 = enable, 0 = disable (default)) (int)
parm:           vm_update_mode:VM update using CPU (0 = never (default except for large BAR(LB)), 1 = Graphics only, 2 = Compute only (default for LB), 3 = Both (int)
parm:           vm_fault_stop:Stop on VM fault (0 = never (default), 1 = print first, 2 = always) (int)
parm:           vm_block_size:VM page table size in bits (default depending on vm_size) (int)
parm:           vm_fragment_size:VM fragment size in bits (4, 5, etc. 4 = 64K (default), Max 9 = 2M) (int)
parm:           vm_size:VM address space size in gigabytes (default 64GB) (int)
parm:           deep_color:Deep Color support (1 = enable, 0 = disable (default)) (int)
parm:           bapm:BAPM support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           ip_block_mask:IP Block Mask (all blocks enabled (default)) (uint)
parm:           runpm:PX runtime pm (2 = force enable with BAMACO, 1 = force enable with BACO, 0 = disable, -1 = auto, -2 = auto with displays) (int)
parm:           aspm:ASPM support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           fw_load_type:firmware loading type (3 = rlc backdoor autoload if supported, 2 = smu load if supported, 1 = psp load, 0 = force direct if supported, -1 = auto) (int)
parm:           dpm:DPM support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           lockup_timeout:GPU lockup timeout in ms (default: 10000 for all jobs. 0: keep default value. negative: infinity timeout), format: for bare metal [Non-Compute] or [GFX,Compute,SDMA,Video]; for passthrough or sriov [all jobs] or [GFX,Compute,SDMA,Video]. (string)
parm:           svm_default_granularity:SVM's default granularity in log(2^Pages), default 9 = 2^9 = 2 MiB (uint)
parm:           msi:MSI support (1 = enable, 0 = disable, -1 = auto) (int)
parm:           pcie_gen2:PCIE Gen2 mode (-1 = auto, 0 = disable, 1 = enable) (int)
parm:           hw_i2c:hw i2c engine enable (0 = disable) (int)
parm:           disp_priority:Display Priority (0 = auto, 1 = normal, 2 = high) (int)
parm:           audio:Audio enable (-1 = auto, 0 = disable, 1 = enable) (int)
parm:           moverate:Maximum buffer migration rate in MB/s. (32, 64, etc., -1=auto, 0=1=disabled) (int)
parm:           gttsize:Size of the GTT userspace domain in megabytes (-1 = auto) (int)
parm:           gartsize:Size of kernel GART to setup in megabytes (32, 64, etc., -1=auto) (uint)
parm:           vis_vramlimit:Restrict visible VRAM for testing, in megabytes (int)
parm:           vramlimit:Restrict VRAM for testing, in megabytes (int)
parm:           ignore_min_pcap:Ignore the minimum power cap (int)
```

The issue happens after some time. Most of the time the sceen freezes, then restart (dmesg then states that amdgpu triggered a page fault and it's reset). But it also happens that it hangs the whole computer, like in the pastebin above. 
The computer is used by my family, so it'll have mainly video playing usage, internet browsing and Android Studio like load.
It's sleeping most of the time, then opened, used for 40mn and put to sleep again (as you'll see in the dmesg above).

I don't have a simple "reproduce the bug" tutorial yet. But I've found some people experiencing the issue [here](https://www.reddit.com/r/framework/comments/1pxz56v/framework_13_ryzen_ai_7_350_freezing_bsod_during/) even on Windows 11. 


 


---

### 评论 #3 — argbet21 (2026-01-12T11:54:54Z)

I'd like to add that I'm getting the same exact issue here on my end as well. I got the same exact CPU + integrated graphics you got there (`AMD Ryzen AI 7 350 w/ Radeon 860M`) and get the same error message when just casually using my desktop:

```
Jan 12 13:45:35 fedora kernel: amdgpu 0000:c4:00.0: amdgpu: MES ring buffer is full.
Jan 12 13:45:35 fedora kernel: amdgpu 0000:c4:00.0: amdgpu: failed to reg_write_reg_wait
Jan 12 13:45:35 fedora kernel: amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
```

---

### 评论 #4 — amd-nicknick (2026-01-14T10:31:33Z)

Hi all, I managed to gather some KRK systems and setting up generic ACPI cycle + ROCm stress tests for now.
If anyone has found reproducible steps, please comment in this thread so I could better diagnose this potential issue.

If you managed to encounter a crash issue & is reproducible, please enable debug logging:
Choose either way:
* Add kernel module parameter `amdgpu.dyndbg=+flmpt`, either by GRUB or `/etc/modprobe.d`:
  ```
  options amdgpu dyndbg=+flmpt
  ```
* Dynamically toggle on debug log (Replace debugfs with the path it is mounted, eg. default `/sys/kernel/debug` on Ubuntu): 
  ```
  echo -n 'module amdgpu +p' > <debugfs>/dynamic_debug/control
  ```
As the log is very verbose, I suggest turning on just before the failure occurs. Provide the dmesg log dump.

---

### 评论 #5 — argbet21 (2026-01-19T15:27:06Z)

Hi @amd-nicknick, sorry for the late reply; I've gone a few days now and my system doesn't seem to freeze up anymore at all, it looks like this firmware update may have resolved it: https://bodhi.fedoraproject.org/updates/FEDORA-2026-2cebf295af

NOTE: I am using Fedora so the fix has been pushed to Fedora at least; I'd mark this issue as resolved if the case is that it's been pushed to all other Linux distros as well.

---

### 评论 #6 — X-Ryl669 (2026-01-19T18:59:19Z)

I'm using a distribution based on Arch and it's using the latest tags from official linux firmware at `git+https://gitlab.com/kernel-firmware/linux-firmware.git?signed#tag=20260110`

I did not had the same issue as mentioned here yet, but I got a complete kernel freeze (with no activity except for the led on Caps Lock that was blinking). The kernel hang haven't reached the drive so there was no log about the crash in the system log. I couldn't switch VT either, and neither Caps Lock or Num Lock toggled their led when pressed. So for me, I'm not sure it's fixed, since I already had this kernel freeze with the firmware in the OP earlier. I'm not sure they are any changes in the new linux-firmware repository for AMD either.  


---

### 评论 #7 — eiis1000 (2026-01-21T20:01:11Z)

FWIW I'm using an AI 300 HX 370 (so, gfx1150 not 1152) with the 20260110 firmware, 6.18.6 kernel, MES 0x80, and the latest version of NixOS 26.05, and I'm getting what is symptomatically the exact same issue (normal desktop use and then complete desktop hang with system grinding to a halt (`reboot` takes about half an hour)):

```
Jan 20 20:28:25 eabrnixos kernel: hid-generic 0003:413C:B06E.0015: hiddev99,hidraw5: USB HID v1.11 Device [Dell Thunderbolt Dock WD22TB4] on usb-0000:c3:00.3-1.1.5/input0
Jan 20 21:21:23 eabrnixos kernel: Bluetooth: hci0: Opcode 0x0401 failed: -16
Jan 20 21:22:43 eabrnixos kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
Jan 20 21:22:43 eabrnixos kernel: amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
[...many of those...]
Jan 20 21:23:20 eabrnixos kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
Jan 20 21:23:20 eabrnixos kernel: amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
Jan 20 21:23:22 eabrnixos kernel: amdgpu 0000:c1:00.0: amdgpu: MES ring buffer is full.
Jan 20 21:23:25 eabrnixos kernel: amdgpu 0000:c1:00.0: amdgpu: MES ring buffer is full.
[...these continue forever...]
```

For many other reports see here:
https://community.frame.work/t/amd-gpu-mes-timeouts-causing-system-hangs-on-framework-laptop-13-amd-ai-300-series/71364?page=3
and here:
https://gitlab.freedesktop.org/drm/amd/-/issues/4749

Here is my rocminfo:
```
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
Runtime Ext Version:     1.11
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
  Name:                    AMD Ryzen AI 9 HX 370 w/ Radeon 890M
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen AI 9 HX 370 w/ Radeon 890M
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
    L1:                      49152(0xc000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   5157                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            24                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    24385468(0x17417bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24385468(0x17417bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24385468(0x17417bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24385468(0x17417bc) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1150                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon 890M Graphics           
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
  Chip ID:                 5390(0x150e)                       
  ASIC Revision:           4(0x4)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   49408                              
  Internal Node ID:        1                                  
  Compute Unit:            16                                 
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       APU
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 32                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    12192732(0xba0bdc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    12192732(0xba0bdc) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1150         
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
```

---

### 评论 #8 — amd-nicknick (2026-01-22T06:57:32Z)

@eiis1000, from the dmesg, did the hang occur when you plugged in an external display? Also, could you share the full dmesg log?
I have a KRK system running combined stress for the last couple of days without issues, if it was related to display hotplus, perhaps I could mix that in. (MES itself has nothing to do with display, but perhaps something is broken upstream?)

---

### 评论 #9 — X-Ryl669 (2026-01-22T07:09:25Z)

I'm using a laptop without any external display. So it's not related.

---

### 评论 #10 — eiis1000 (2026-01-23T19:46:22Z)

In most cases (including this one I think) I had an external display (4k 144Hz through a TB dock) plugged in from the beginning, far before the hang. I haven't had the hang without the display plugged in, but I almost always use my laptop with the external display so that doesn't mean much. On the other hand, FWIW, a few of the reports that I've seen which can reliably reproduce the issue say that, when they use a lower resolution external screen (or no external screen at all), the issue is either not reproduced at all or much less frequent. Perhaps there are multiple different sources for this hang, and one of them is high-res-related and one of them is not? (Or maybe the source of this hang is different on gfx1152 vs gfx1150?) In any case, next time I get the crash I will try to remember to grab the dmesg log and send it over.

---

### 评论 #11 — eiis1000 (2026-01-26T19:29:03Z)

Here's the journalctl output from yesterday's crash. The link expires in one week https://privatebin.net/?c1e34d777ceead4a#HpnbRMRffggVPnVf1StHZQUZwaTyXJSzwVqmdYmaAVK7

---

### 评论 #12 — eiis1000 (2026-02-13T19:09:46Z)

Presumably related to https://gitlab.freedesktop.org/drm/amd/-/issues/4749?

---

### 评论 #13 — sspaeti (2026-02-15T18:06:51Z)

I have the same errors (https://github.com/basecamp/omarchy/issues/4184#issuecomment-3820100143 - were related to hibernate or suspend), but still happen without hibernation even.

I  had multiple crashes today. Very annoying. Updated to the latest versions just today, but it came back immediately. Based on this hint: 
> I am using Arch linux on Ryzen AI 9 365. From Monday Feb 09 I used kernel 6.18.8 and from Wednesday - 6.18.9, cmdline amdgpu.cwsr_enable=0. System seems works without hangs and errors (6.18.7 had page fault and 'MES ring buffer is full' problem). I didn't test stability with usage of local LLMs and without cwsr_enable parameter yet. The only problem left is rare flickering in web browsers on some websites (it is also present in kernels 6.17.*), but maybe it linked somehow with Niri or high frequency display, need to do more experiments. https://gitlab.freedesktop.org/drm/amd/-/issues/4749#note_3329617

I added `amdgpu.cwsr_enable=0` - I'm reverting to how it goes when I ran it for a while. My laptop is a Tuxedo with AMD Ryzen AI 9 HX 370 / AMD Radeon 890M.

---

### 评论 #14 — superm1 (2026-03-02T01:59:46Z)

There was recently updated microcode for gfx1152 uploaded to linux-firmware.git (https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/commit/amdgpu?id=e2d3b43db975878ff0724ea7d3806a7615e0eb71) that I believe should help this issue.  Can you please upgrade and try it?
Please drop `amdgpu.cwsr_enable=0` while trying it.

---

### 评论 #15 — devusb (2026-03-08T00:29:35Z)

just ran into what I think is the same issue on linux-firmware commit `d8e138dd8970ffc9f5f879e2d62938abe6cd3f22` which I _think_  is after the updated microcode was added?

hardware is Framework 13 with AMD Ryzen AI 9 HX 370 running kernel 6.19.6.

output from `journalctl -k`
```
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
```

let me know if I can provide any additional context or info.

---

### 评论 #16 — superm1 (2026-03-08T00:41:21Z)

You have Strix not Kraken. Strix had the correct firmware update already.

So you're seeing a different (but similar) issue.

---

### 评论 #17 — X-Ryl669 (2026-03-08T19:05:45Z)

I'm waiting for arch to sync (last sync was on 22th February, so 2 days before the new files) and I'll report back. I've removed `amdgpu.cwsr_enable=0` and got the issue again yesterday with hard freeze (still with the old firmware) 

---

### 评论 #18 — X-Ryl669 (2026-03-14T17:23:24Z)

Ok, got again the same issue, with latest firmware:
```
amdgpu: Guilty job already signaled, skipping HW reset
amdgpu 0000:04:00.0: amdgpu: GPU reset(1) succeeded!
amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
amdgpu 0000:04:00.0: amdgpu: SMU is resuming...
amdgpu 0000:04:00.0: amdgpu: SMU is resumed successfully!
amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
amdgpu 0000:04:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 1 on hub 8
amdgpu 0000:04:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
amdgpu 0000:04:00.0: amdgpu: ring vpe uses VM inv eng 4 on hub 8
amdgpu 0000:04:00.0: [drm:amdgpu_ib_ring_tests [amdgpu]] *ERROR* IB test failed on comp_1.0.1 (-110).
amdgpu 0000:04:00.0: amdgpu: ib ring test failed (-110).
amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring sdma0
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring sdma0
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring sdma0
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring sdma0
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring sdma0
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring gfx_0.0.0
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring gfx_0.0.0
amdgpu 0000:04:00.0: amdgpu: Fence fallback timer expired on ring gfx_0.0.0
amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
amdgpu 0000:04:00.0: amdgpu: MES ring buffer is full.
```

As for the firmware I have:
```
$ cat /lib/firmware/amdgpu/gc_11_5_2_me.bin.zst | zstd -d -c - | sha256sum
5def9753a2830d42d66de2b54d2de212ce8ab3e9700ce4d3c7f925b734c25149  -
$ cat /lib/firmware/amdgpu/gc_11_5_2_mes1.bin.zst | zstd -d -c - | sha256sum
09cabb2b62bf10e72de59576f0e1f823beb521d65a6c163526191391dc58f966
```

For the command line:
```
$ cat /proc/cmdline
quiet zswap.enabled=0 nowatchdog splash rw root=redacted initrd=\initramfs-linux-cachyos.img
```



---

### 评论 #19 — tremolo (2026-03-21T11:23:33Z)

Hi, i have the same issue for some time now and asked claude for help, it also crafted this report with hopefully valuable data for analysis, let me know if i can provide additional information..



# Krackan Point (gfx1152) MES hang on Framework Laptop 13 — Ryzen AI 7 350 / Radeon 860M

## System Information

| Component | Details |
|-----------|---------|
| **Laptop** | Framework Laptop 13 (AMD Ryzen AI 300 Series), SKU: FRANMGCP07 |
| **CPU** | AMD Ryzen AI 7 350 |
| **GPU** | AMD Radeon 860M (gfx1152, Krackan Point) |
| **Kernel** | 6.19.8-zen1-1-zen (Arch Linux) |
| **Firmware** | linux-firmware 20260309-1 |
| **Desktop** | GNOME on Wayland |
| **OS** | Arch Linux (x86_64) |

```
$ uname -a
Linux lpfw 6.19.8-zen1-1-zen #1 ZEN SMP PREEMPT_DYNAMIC Sat, 14 Mar 2026 01:07:31 +0000 x86_64 GNU/Linux
```

MES firmware loaded at boot:

```
amdgpu 0000:c1:00.0: amdgpu: detected ip block number 10 <mes_v11_0_0> (mes_v11_0)
amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
```

## Problem Description

Experiencing repeated full system hangs caused by MES (Micro Engine Scheduler) timeouts. The system becomes completely unresponsive and requires a hard power-off via the power button. This has occurred multiple times.

The hang typically occurs during normal desktop use — switching between GPU-accelerated applications (Firefox, Signal Desktop/Electron). Both use GPU-accelerated compositing under Wayland, alongside GNOME's Mutter compositor.

## Workarounds Attempted

All of the following kernel parameters were applied and **confirmed active** via `/sys/module/amdgpu/parameters/` — none prevent the hang:

```
amdgpu.cwsr_enable=0
amdgpu.sg_display=0
amdgpu.dcdebugmask=0x10
amdgpu.reset_method=4
```

Verification:

```
$ cat /proc/cmdline
root=ZFS=zroot/encr/ROOT  zfs=zroot/encr/ROOT fbcon=font:TER16x32   mitigations=off  zfs_force=1 rw initrd=\amd-ucode.img initrd=\initramfs-linux-zen.img zswap.enabled=1 amdgpu.cwsr_enable=0 amdgpu.sg_display=0 amdgpu.dcdebugmask=0x10 amdgpu.reset_method=4

$ for p in cwsr_enable sg_display dcdebugmask reset_method; do
    echo "$p = $(cat /sys/module/amdgpu/parameters/$p)"
done
cwsr_enable = 0
sg_display = 0
dcdebugmask = 16
reset_method = 4
```

### Summary of workaround results

| Workaround | Result |
|------------|--------|
| `amdgpu.cwsr_enable=0` alone | Still crashed |
| + `amdgpu.sg_display=0` | Still crashed |
| + `amdgpu.dcdebugmask=0x10` (disable PSR) | Still crashed |
| + `amdgpu.reset_method=4` | Driver attempted `sdma0` ring reset (new!), but MES was already unrecoverable — still crashed |

## Crash Logs

### Crash 1 — March 20, 14:20 (only `cwsr_enable=0`)

MES stopped responding and entered an unrecoverable loop:

```
Mär 20 14:20:44 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
Mär 20 14:20:44 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
Mär 20 14:20:47 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
Mär 20 14:20:47 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
[... repeated every ~3 seconds, 11 times total ...]
Mär 20 14:21:13 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
Mär 20 14:21:13 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: failed to reg_write_reg_wait
-- system frozen, hard reboot required --
```

No GPU reset was attempted. No ring buffer full messages — MES died before the ring could fill.

### Crash 2 — March 21, 11:16 (all four workarounds active)

Triggered while switching from Signal Desktop to Firefox. Full failure sequence:

**Phase 1: MES stops responding (11:16:16–11:17:00)**

```
Mär 21 11:16:16 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
[... repeated every ~3 seconds, 15 times ...]
```

**Phase 2: Ring buffer fills (11:17:00 onward)**

```
Mär 21 11:17:00 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: MES ring buffer is full.
[... repeated every ~3 seconds continuously ...]
```

**Phase 3: Hung task detector fires (11:22:07)**

```
Mär 21 11:22:07 lpfw kernel: "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
Mär 21 11:22:07 lpfw kernel:  amdgpu_mes_reg_write_reg_wait+0x70/0xf0 [amdgpu]
Mär 21 11:22:07 lpfw kernel:  ? mes_v11_0_submit_pkt_and_poll_completion.constprop.0+0x171/0x520 [amdgpu]
Mär 21 11:22:07 lpfw kernel:  ? mes_v11_0_misc_op+0x74/0x1c0 [amdgpu]
Mär 21 11:22:07 lpfw kernel:  ? amdgpu_mes_reg_write_reg_wait+0xaa/0xf0 [amdgpu]
```

**Phase 4: Driver attempts sdma0 reset — fails (11:29:06)**

With `reset_method=4`, the driver did attempt recovery, which is new compared to the default behavior:

```
Mär 21 11:29:06 lpfw kernel: amdgpu 0000:c1:00.0: amdgpu: Starting sdma0 ring reset
```

However, MES was already completely unresponsive at this point, so the reset could not proceed. The "ring buffer is full" messages continued for another 2+ minutes until I hard-rebooted.

**Additional observations:**
- USB device resets (`usb 1-1` and `usb 4-1` via xhci_hcd) appeared throughout the log, including well before the GPU hang — possibly indicating broader platform-level instability.
- The hung task detector fired twice (at 11:22:07 and 11:28:16) with stacks inside `amdgpu_mes_reg_write_reg_wait` and `mes_v11_0_misc_op`.
- Total time from first MES failure to forced reboot: ~14 minutes with no recovery.

## Interpretation

This matches the MES scheduler wedge described in the amd-gfx mailing list reports for gfx1150/gfx1151. The same failure mode applies to gfx1152 (Krackan Point):

1. MES stops responding to `MISC (WAIT_REG_MEM)` messages
2. The MES ring buffer fills and never drains
3. All dependent rings stall (GPU compute + display)
4. GPU reset is attempted (with `reset_method=4`) but fails because MES itself is the component that's hung
5. System becomes fully unresponsive — only hard reboot recovers

The `cwsr_enable=0` workaround does not prevent the hang in this case, suggesting the trigger is not limited to the CWSR code path. The crash during a window switch between two GPU-composited applications (Firefox + Signal/Electron) under Wayland points to the display/compositor path as a trigger.

## Related Issues

- ROCm/ROCm#5844 — Krackan Point GPU hang (gfx1152) Ryzen AI 350
- ROCm/ROCm#5590 — amdgpu compute wave store and resume causing MES firmware hang
- ROCm/ROCm#5724 — amdgpu firmware (MES 0x83) causing GPU Hang with Strix Halo
- [Framework Community thread](https://community.frame.work/t/amd-gpu-mes-timeouts-causing-system-hangs-on-framework-laptop-13-amd-ai-300-series/71364) — multiple users reporting same issue
- [amd-gfx mailing list: MES hang leads to global fence starvation (gfx1150)](https://lists.freedesktop.org/archives/amd-gfx/2025-December/136016.html)
- [amd-gfx mailing list: MES scheduler wedge under sustained compute (gfx1150)](https://lists.freedesktop.org/archives/amd-gfx/2025-December/135310.html)


---

### 评论 #20 — tremolo (2026-03-21T11:55:47Z)

Following up on the status it looks like it got fixed already and will be merged into next Linux release
https://lore.kernel.org/amd-gfx/20260316151636.1122226-1-alexander.deucher@amd.com/

---

### 评论 #21 — daniel-k (2026-03-23T07:57:02Z)

I think I am/was affected by the same issue (Thinkpad T14 AMD Gen 6), but for me it only appeared after updating to the March release of `linux-firmware`. In case it helps anyone: my system hasn't experienced any amdgpu induces crashes anymore since downgrading to:

```
linux 6.18.13.arch1-1
linux-firmware 20260221-1
linux-firmware-amdgpu 20260221-1
linux-firmware-whence 20260221-1
```

I'm using the following `amdgpu` related kernel options, but I'm not sure if they are strictly necessary:

```
amdgpu.gpu_recovery=1 amdgpu.cwsr_enable=0 amdgpu.dcdebugmask=0x10
```



> Following up on the status it looks like it got fixed already and will be merged into next Linux release
> https://lore.kernel.org/amd-gfx/20260316151636.1122226-1-alexander.deucher@amd.com/

Great find, will be trying it as soon as it reaches the Arch repos!

---

### 评论 #22 — kaledin (2026-03-27T17:28:11Z)

So can anyone with 6.19.10 on Arch or Fedora(testing) confirm that  this patch fixes the bug?

---

### 评论 #23 — X-Ryl669 (2026-03-27T17:38:35Z)

I have this kernel, but I haven't reproduced the bug yet. Since the reproduction is hard, I can't confirm if it's fixed or not. I'll report when I've run a very intensive AI session.

---

### 评论 #24 — tremolo (2026-04-09T09:11:03Z)

After using 6.19.10 for a while now there have been no freezes/crashes anymore, while there have been several before. So i think there is strong indication that the patch incorporated into 6.19.10 
fixed the issue (at least for me)

---

### 评论 #25 — X-Ryl669 (2026-04-09T10:06:38Z)

For now, I can confirm that I haven't reproduced the crash either.

---

### 评论 #26 — daniel-k (2026-04-22T06:38:26Z)

Same here, no more issues since 2026-04-09 when I upgraded to `6.19.11.arch1-1`.

```
[2026-04-09T11:48:57+0200] [ALPM] upgraded linux (6.18.13.arch1-1 -> 6.19.11.arch1-1)
[2026-04-09T11:48:57+0200] [ALPM] upgraded linux-firmware-amdgpu (20260221-1 -> 20260309-1)
[2026-04-20T08:43:11+0200] [ALPM] upgraded linux (6.19.11.arch1-1 -> 6.19.12.arch1-1)
[2026-04-20T08:43:43+0200] [ALPM] upgraded linux-firmware-amdgpu (20260309-1 -> 20260410-1)
```

---

### 评论 #27 — PhilMeyr (2026-04-22T12:31:09Z)

Adding a datapoint: same hardware (Radeon 860M, gfx1152), same MES-failure signature, but on **Ubuntu 25.10 + kernel 6.17.0-22-generic + Mesa 25.2.8**, and the trigger is **not compute** — it's Google Chrome, specifically when moving a Chrome window between two displays on a multi-monitor setup.

**Hardware:**
- Framework Laptop 13 (AMD Ryzen AI 300 Series), BIOS 03.05
- CPU: AMD Ryzen AI 7 350 w/ Radeon 860M
- GPU: `0000:c1:00.0`, gfx1152, VBIOS `113-STRIXEMU-001`
- IP: gfx_v11_0, mes_v11_0

**Software:**
- Ubuntu 25.10, kernel `6.17.0-22-generic`
- Mesa 25.2.8 (radeonsi), GNOME on Wayland
- Chrome (hardware acceleration enabled, default settings)

**Reproducer:** drag a Chrome window from the internal panel to an external display (or the reverse). Reproduced 4 times in ~4 hours today.

**Kernel log at the crash (2026-04-22 11:28):**

```
amdgpu 0000:c1:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:5 pasid:32772)
amdgpu 0000:c1:00.0: amdgpu:  Process chrome pid 5171 thread chrome:cs0 pid 5187
amdgpu 0000:c1:00.0: amdgpu:   in page starting at address 0x0000c3c03fc3c000 from client 10
amdgpu 0000:c1:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00501430
amdgpu 0000:c1:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
amdgpu 0000:c1:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=2801957, emitted seq=2801960
amdgpu 0000:c1:00.0: amdgpu: Starting gfx_0.0.0 ring reset
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=RESET
amdgpu 0000:c1:00.0: amdgpu: failed to reset legacy queue
amdgpu 0000:c1:00.0: amdgpu: reset via MES failed and try pipe reset -110
amdgpu 0000:c1:00.0: amdgpu: The CPFW hasn't support pipe reset yet.
amdgpu 0000:c1:00.0: amdgpu: Ring gfx_0.0.0 reset failed
amdgpu 0000:c1:00.0: amdgpu: GPU reset begin!
amdgpu 0000:c1:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
amdgpu 0000:c1:00.0: amdgpu: MODE2 reset
amdgpu 0000:c1:00.0: amdgpu: GPU reset(1) succeeded!
amdgpu 0000:c1:00.0: [drm] device wedged, but recovered through reset
```

MODE2 reset recovers the GPU but `gnome-shell` and `chrome` are killed (crash reports in `/var/crash/_usr_bin_gnome-shell.1000.crash` and `_opt_google_chrome_chrome.1000.crash`), which logs the user out.

An earlier boot the same day showed the other MES signature described in this issue: a long run of `MES failed to respond to msg=MISC (WAIT_REG_MEM)` before the hang.


---

### 评论 #28 — PhilMeyr (2026-04-22T12:41:41Z)

Filed upstream on the canonical amdgpu tracker as https://gitlab.freedesktop.org/drm/amd/-/issues/5207 for cross-visibility.

---

### 评论 #29 — marinhuz (2026-04-24T05:10:19Z)

Same bug here, confirming on a different distro. Setup matches @X-Ryl669's almost 1:1 on the hardware side.

Hardware / software:

Laptop: Lenovo IdeaPad Slim 5 14AKP10 (machine type 83NJ)
CPU: AMD Ryzen AI 7 350 w/ Radeon 860M (Family 26, Model 96)
GPU: gfx1152, PCI ID 1002:1114, VBIOS 113-STRIXEMU-001, DCN 3.5, mes_v11_0
MES FW: [CONFIRMAR — cole aqui o output do grep]
BIOS: Lenovo R0CN27WW (latest published)
OS: Linux Mint 22 (Ubuntu 24.04 base)
Kernel: 6.17.0-22-generic #22~24.04.1-Ubuntu (Ubuntu HWE, so a different kernel tree than CachyOS 6.18.3 but same issue)
Mesa: 25.2.8, radeonsi, LLVM 20.1.2
Session: X11 / Cinnamon (not Wayland / KDE like the OP, so the bug is not Wayland- or KDE-specific)
Trigger: plain desktop use, no ROCm, no AI workload, no heavy compute. Just browser + daily work. System had been up for several hours when it hung. Same failure signature as the OP (mouse cursor still moving as HW overlay, rest of UI frozen, hard reset required).

dmesg signature (same as OP):


amdgpu 0000:05:00.0: amdgpu: MES failed to respond to msg=MISC (WAIT_REG_MEM)
amdgpu 0000:05:00.0: amdgpu: failed to reg_write_reg_wait
... (repeats for ~40s)
amdgpu 0000:05:00.0: amdgpu: MES ring buffer is full.
... (repeats for minutes)
workqueue: amdgpu_tlb_fence_work [amdgpu] hogged CPU for >13333us 67 times

INFO: task kworker/14:0 blocked for more than 122 seconds.
Workqueue: events amdgpu_tlb_fence_work [amdgpu]
Call Trace:
 amdgpu_mes_reg_write_reg_wait+0x7a/0x130 [amdgpu]
 amdgpu_gmc_fw_reg_write_reg_wait+0x1ca/0x200 [amdgpu]
 gmc_v11_0_flush_gpu_tlb+0x3c1/0x500 [amdgpu]
 amdgpu_tlb_fence_work+0x73/0x140 [amdgpu]

task is blocked on a mutex likely owned by another amdgpu_tlb_fence_work worker
Also several TTM workers stuck in ttm_bo_delayed_delete → dma_fence_wait_timeout.

Confirmation this reproduces:

Without amdgpu.cwsr_enable=0 (OP had this set and still got the hang — mine reproduced without any amdgpu cmdline overrides at all).
Without KDE/Wayland (X11/Cinnamon here).
Without ROCm installed (pure desktop, the Mint base doesn't ship ROCm).
So scope is wider than just CachyOS/KDE/Wayland/compute setups — this is a plain desktop hang on stock Ubuntu HWE kernel on this hardware.

Happy to provide full journalctl -b -1 -k or test specific cmdline params if useful. Planning to apply amdgpu.mes=0 as a workaround and report back if the hang stops.

---

### 评论 #30 — X-Ryl669 (2026-04-24T19:40:55Z)

Ok, so to give an update about the current status:
1. The system is more stable but not completely stable.
2. I was able to reproduce the bug while running a long LLM session (mainly Gemma 4 based), the computer got frozen
3. I had this in the `journalctl -b -1` log (repeating ad libitum before it happened):

```
 kwin_wayland[1123]: Pageflip timed out! This is a bug in the amdgpu kernel driver
 kwin_wayland[1123]: Please report this at https://gitlab.freedesktop.org/drm/amd/-/issues
 kwin_wayland[1123]: With the output of 'sudo dmesg' and 'journalctl --user-unit plasma-kwin_wayland --boot 0'
```

The plasma-kwin-wayland log is exactly the same message in a loop.

Got this in dmesg too:
```
[43460.234219] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc llama-server(19949) task llama-server(19949) is non-zero when fini
```

My current kernel: `Linux 6.19.11-1-cachyos #1 SMP PREEMPT_DYNAMIC Thu, 02 Apr 2026 16:36:59 +0000 x86_64 GNU/Linux`

---

### 评论 #31 — X-Ryl669 (2026-04-25T20:13:22Z)

Got it again, but this time I was in front of the computer so I had time to switch VT to capture dmesg output before it froze:
```
[78989.891139] oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),cpuset=user@1000.service,mems_allowed=0,global_oom,task_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.wezfurlong.wezterm@a00df830f0b34b928e0fe7b457432534.service,task=llama-server,pid=82743,uid=1000
[78989.891201] Out of memory: Killed process 82743 (llama-server) total-vm:11548116kB, anon-rss:976kB, file-rss:24704kB, shmem-rss:0kB, UID:1000 pgtables:19388kB oom_score_adj:200
[78991.993907] systemd-journald[445]: Under memory pressure, flushing caches.
[78992.088161] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc wezterm-gui(79739) task wezterm-gu:cs0(79720) is non-zero when fini
[78992.152899] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc python3.10(82376) task python3.10:cs0(82327) is non-zero when fini
[78992.898115] oom_reaper: reaped process 82743 (llama-server), now anon-rss:848kB, file-rss:32kB, shmem-rss:0kB
[78993.167082] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc llama-server(82743) task llama-server(82743) is non-zero when fini
[78994.044749] systemd-journald[445]: Under memory pressure, flushing caches.
[79390.701590] amdxdna 0000:05:00.1: [drm] *ERROR* aie2_get_info: Not supported request parameter 4
[79445.836060] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc llama-server(87095) task llama-server(87095) is non-zero when fini
[84221.575931] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84221.683795] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84221.791166] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84221.897317] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84222.002526] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84222.108355] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84222.214465] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84222.320432] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84222.380536] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84222.472787] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84253.495631] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[84261.232952] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84261.569344] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84261.754687] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84261.955711] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84262.998073] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84265.321132] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84274.071319] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.072381] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.073435] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.074525] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.075614] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.076699] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.077783] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.078866] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.079953] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.081038] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.082115] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.083199] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.084273] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.085355] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.086440] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.087524] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84274.088608] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[84275.892743] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84277.823241] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.154038] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.219747] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.286878] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.353141] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.416374] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.475886] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.546582] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.625135] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84278.988275] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84451.444864] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84451.550564] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84451.658070] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84451.765619] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[84451.873666] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84861.719654] warn_alloc: 1616 callbacks suppressed
[84861.719659] kwin_wayland: page allocation failure: order:0, mode:0xc0de0(GFP_KERNEL|__GFP_HIGH|__GFP_ZERO|__GFP_COMP|__GFP_NOMEMALLOC), nodemask=(null),cpuset=user@1000.service,mems_allowed=0
[84861.719678] CPU: 15 UID: 1000 PID: 1118 Comm: kwin_wayland Tainted: G           OE       6.19.11-1-cachyos #1 PREEMPT(full)  745d62ba395fad5758c42976fa6ca60749ea4231
[84861.719684] Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
[84861.719685] Hardware name: LENOVO 83HY/LNVNB161216, BIOS R0CN16WW 05/06/2025
[84861.719687] Call Trace:
[84861.719689]  <TASK>
[84861.719692]  dump_stack_lvl+0x61/0x80
[84861.719699]  warn_alloc+0x183/0x200
[84861.719704]  ? CalculateSwathWidth+0x688/0x820 [amdgpu 39d4b2304846114ecd61fbe3763f7fab6c417f0e]
[84861.720054]  __alloc_frozen_pages_noprof+0x69d/0x6b0
[84861.720057]  folio_alloc_noprof+0xcf/0x170
[84861.720059]  isolate_lock_cluster+0x129/0x240
[84861.720062]  cluster_alloc_swap_entry+0xf8/0x300
[84861.720063]  folio_alloc_swap+0x1fc/0x540
[84861.720065]  shrink_folio_list+0x9f0/0x1370
[84861.720068]  ? mas_wmb_replace+0x850/0xb70
[84861.720070]  ? mod_memcg_lruvec_state.llvm.3712404722860121569+0x6d/0x140
[84861.720073]  ? lru_gen_update_size+0x15c/0x270
[84861.720074]  evict_folios+0x1621/0x1f90
[84861.720077]  try_to_shrink_lruvec+0x3e1/0x670
[84861.720078]  ? prepare_workingset_protection+0x221/0x290
[84861.720080]  shrink_one+0x203/0x440
[84861.720081]  ? folio_batch_move_lru+0x52c/0x550
[84861.720083]  shrink_node+0xe0a/0x1240
[84861.720084]  ? raw_spin_rq_lock_nested+0x1d/0x30
[84861.720086]  ? get_page_from_freelist+0x57b/0xb50
[84861.720088]  ? zone_reclaimable_pages+0x161/0x2e0
[84861.720089]  ? sched_clock+0x10/0x30
[84861.720091]  ? psi_task_switch+0x49/0x640
[84861.720092]  ? update_se.llvm.3851053827617306151+0xbb/0x160
[84861.720094]  do_try_to_free_pages+0x144/0x500
[84861.720096]  try_to_free_pages+0x46e/0x590
[84861.720098]  __alloc_pages_direct_reclaim+0x6e/0x110
[84861.720100]  __alloc_frozen_pages_noprof+0x523/0x6b0
[84861.720102]  alloc_pages_noprof+0xc9/0x160
[84861.720104]  __pollwait+0x114/0x180
[84861.720106]  eventfd_poll+0x28/0x60
[84861.720107]  __x64_sys_ppoll+0x43e/0x990
[84861.720111]  ? __pfx___pollwait+0x10/0x10
[84861.720112]  ? __pfx_pollwake+0x10/0x10
[84861.720114]  ? __pfx_pollwake+0x10/0x10
[84861.720115]  ? __pfx_pollwake+0x10/0x10
[84861.720116]  ? __pfx_pollwake+0x10/0x10
[84861.720117]  ? __pfx_pollwake+0x10/0x10
[84861.720118]  ? __pfx_pollwake+0x10/0x10
[84861.720119]  ? __pfx_pollwake+0x10/0x10
[84861.720120]  ? __pfx_pollwake+0x10/0x10
[84861.720121]  ? __pfx_pollwake+0x10/0x10
[84861.720123]  do_syscall_64+0x75/0x280
[84861.720125]  ? eventfd_read+0xc8/0x1d0
[84861.720126]  ? __x64_sys_read+0x2c9/0x3c0
[84861.720128]  ? do_syscall_64+0xb8/0x280
[84861.720129]  ? rcu_core.llvm.12871679498925100073+0x20b/0x6a0
[84861.720130]  ? sched_clock+0x10/0x30
[84861.720132]  ? sched_clock_cpu+0xf/0x20
[84861.720133]  ? irqtime_account_irq+0x2f/0xb0
[84861.720135]  ? irq_exit_rcu+0x1d0/0x290
[84861.720136]  ? irqentry_exit+0x4d/0x610
[84861.720137]  entry_SYSCALL_64_after_hwframe+0x79/0x81
[84861.720139] RIP: 0033:0x7f7e014b2422
[84861.720169] Code: 08 0f 85 81 39 ff ff 49 89 fb 48 89 f0 48 89 d7 48 89 ce 4c 89 c2 4d 89 ca 4c 8b 44 24 08 4c 8b 4c 24 10 4c 89 5c 24 08 0f 05 <c3> 66 2e 0f 1f 84 00 00 00 00 00 66 2e 0f 1f 84 00 00 00 00 00 66
[84861.720170] RSP: 002b:00007ffe7e553fd8 EFLAGS: 00000246 ORIG_RAX: 000000000000010f
[84861.720172] RAX: ffffffffffffffda RBX: 00000045d26b7002 RCX: 00007f7e014b2422
[84861.720173] RDX: 00007ffe7e554020 RSI: 000000000000000a RDI: 00007f7df402d2f0
[84861.720174] RBP: 00007ffe7e5540b0 R08: 0000000000000008 R09: 0000000000000000
[84861.720174] R10: 0000000000000000 R11: 0000000000000246 R12: 00007f7df402d2f0
[84861.720175] R13: 000000000000000a R14: 0044b82fa09b5a53 R15: 00000000000000a4
[84861.720176]  </TASK>
[84861.720184] Mem-Info:
[84861.720185] active_anon:876882 inactive_anon:298549 isolated_anon:0
                active_file:59801 inactive_file:256771 isolated_file:0
                unevictable:177 dirty:0 writeback:2048
                slab_reclaimable:24295 slab_unreclaimable:110287
                mapped:204252 shmem:811427 pagetables:25771
                sec_pagetables:971 bounce:0
                kernel_misc_reclaimable:0
                free:38923 free_pcp:8468 free_cma:0
[84861.720189] Node 0 active_anon:3507528kB inactive_anon:1194196kB active_file:239204kB inactive_file:1027084kB unevictable:708kB isolated(anon):0kB isolated(file):0kB mapped:817008kB dirty:0kB writeback:8192kB shmem:3245708kB shmem_thp:1298432kB shmem_pmdmapped:137216kB anon_thp:258048kB kernel_stack:32880kB pagetables:103084kB sec_pagetables:3884kB all_unreclaimable? no Balloon:0kB
[84861.720192] Node 0 DMA free:11264kB boost:0kB min:32kB low:44kB high:56kB reserved_highatomic:0KB free_highatomic:0KB active_anon:0kB inactive_anon:0kB active_file:0kB inactive_file:0kB unevictable:0kB writepending:0kB zspages:0kB present:15992kB managed:15360kB mlocked:0kB bounce:0kB free_pcp:0kB local_pcp:0kB free_cma:0kB
[84861.720196] lowmem_reserve[]: 0 1783 31353 31353 31353
[84861.720198] Node 0 DMA32 free:121816kB boost:0kB min:3676kB low:5416kB high:7156kB reserved_highatomic:0KB free_highatomic:0KB active_anon:42264kB inactive_anon:196396kB active_file:1508kB inactive_file:5792kB unevictable:0kB writepending:8192kB zspages:30964kB present:1892556kB managed:1826216kB mlocked:0kB bounce:0kB free_pcp:7048kB local_pcp:836kB free_cma:0kB
[84861.720201] lowmem_reserve[]: 0 0 29569 29569 29569
[84861.720203] Node 0 Normal free:22612kB boost:0kB min:63872kB low:94144kB high:124416kB reserved_highatomic:0KB free_highatomic:0KB active_anon:3465388kB inactive_anon:998468kB active_file:237780kB inactive_file:1021208kB unevictable:708kB writepending:0kB zspages:8541336kB present:30902784kB managed:30279588kB mlocked:708kB bounce:0kB free_pcp:26792kB local_pcp:4kB free_cma:0kB
[84861.720205] lowmem_reserve[]: 0 0 0 0 0
[84861.720207] Node 0 DMA: 0*4kB 0*8kB 0*16kB 0*32kB 0*64kB 0*128kB 0*256kB 0*512kB 1*1024kB (U) 1*2048kB (M) 2*4096kB (M) = 11264kB
[84861.720212] Node 0 DMA32: 1*4kB (U) 83*8kB (U) 386*16kB (U) 221*32kB (U) 287*64kB (UM) 240*128kB (UM) 183*256kB (U) 1*512kB (M) 1*1024kB (U) 3*2048kB (UM) 1*4096kB (M) = 121628kB
[84861.720219] Node 0 Normal: 0*4kB 1*8kB (U) 1*16kB (U) 1*32kB (U) 330*64kB (U) 0*128kB 0*256kB 0*512kB 0*1024kB 0*2048kB 0*4096kB = 21176kB
[84861.720224] Node 0 hugepages_total=0 hugepages_free=0 hugepages_surp=0 hugepages_size=1048576kB
[84861.720225] Node 0 hugepages_total=0 hugepages_free=0 hugepages_surp=0 hugepages_size=2048kB
[84861.720226] 1036017 total pagecache pages
[84861.720226] 3052 pages in swap cache
[84861.720227] Free swap  = 17826492kB
[84861.720227] Total swap = 32120828kB
[84861.720228] 8202833 pages RAM
[84861.720228] 0 pages HighMem/MovableOnly
[84861.720229] 172542 pages reserved
[84861.720229] 0 pages cma reserved
[84861.720230] 0 pages hwpoisoned
[84861.720230] Memory cgroup min protection 0kB -- low protection 0kB
[84903.633848] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc llama-server(114582) task llama-server(114582) is non-zero when fini
[84920.282623] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[84932.417403] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc llama-server(117707) task llama-server(117707) is non-zero when fini
[84990.354658] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[84990.354666] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85009.947775] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85010.063920] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85023.429023] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85039.420528] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85040.014324] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85053.291840] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[85053.562009] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc RDD Process(6633) task browser 4 :cs0(2700) is non-zero when fini
[85053.642486] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc firefox(2459) task firefox:cs0(2399) is non-zero when fini
[85060.990480] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[85061.093582] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[85064.166128] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85088.073684] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85088.183089] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85088.286882] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85096.382540] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85097.159039] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85124.637964] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85124.848954] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85128.363081] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85178.807623] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85274.571434] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85274.761391] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85274.830160] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85274.830883] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85274.880889] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85274.881612] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85274.931660] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85274.932359] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85274.982393] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85274.983118] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.032318] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.033018] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.082934] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.083658] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.136212] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.136852] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.187445] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.188137] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.238012] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.238641] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.288092] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.288814] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.337924] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.338634] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.388299] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.389042] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.438664] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.439389] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.487779] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.488496] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.538497] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.539235] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.588720] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.589494] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.639358] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.640095] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.690110] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.690729] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.740662] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.741453] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.791345] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.792003] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.842636] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.843366] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.893134] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.893738] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.943200] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.943895] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85275.993568] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85275.994301] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.044173] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.044898] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.095537] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.096336] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.146148] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.146732] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.192339] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.193004] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.238109] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.238781] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.286734] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.287477] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.337465] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.338197] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.387054] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.387488] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.437507] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.438229] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.488192] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.488902] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.538305] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.539020] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.588625] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.589360] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.639118] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.639715] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.689913] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.690632] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.740441] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.741110] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.791189] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.791681] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.840564] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.841303] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.890763] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.891311] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.939349] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.940133] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85276.989080] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85276.989715] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.039721] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.040430] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.090550] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.091064] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.142033] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.142678] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.192008] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.192683] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.242563] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.243288] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.293007] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.293704] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.343508] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.344241] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.394019] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.394631] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.444611] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.445273] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.494897] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.495585] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.545460] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.546122] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.596038] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.596688] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.646940] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.647648] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.697924] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.698649] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.748634] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.749296] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.799316] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.800038] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.849935] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.850605] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.900889] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.901612] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85277.951714] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85277.952428] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.002321] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.003075] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.053373] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.054120] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.104762] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.106326] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.155747] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.156464] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.206687] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.207393] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.257203] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.257817] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.308073] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.308666] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.358365] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.359076] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.408972] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.409649] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.459894] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.460607] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.509788] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.510503] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.560545] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.561257] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.611432] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.612115] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.662214] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.662757] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.712685] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.713407] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.763381] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.764106] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.814466] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.815189] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.865514] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.866196] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.877760] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.878118] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85278.894819] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85278.902450] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85279.104338] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85279.105014] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85279.110968] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85279.111143] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85279.127646] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85279.128154] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85279.144294] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85279.144470] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85279.160955] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85279.161116] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85279.177672] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85279.178174] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85279.264553] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85279.284222] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85321.614732] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85337.971025] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85338.167934] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85338.275152] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85338.380184] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85338.485029] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85338.537438] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85338.642555] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85338.748587] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85339.059276] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85339.112684] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85339.218298] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85339.271203] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85339.376978] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85339.482069] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85339.586530] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85339.692067] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85340.103873] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85340.209549] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85340.314761] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85340.419835] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85340.524587] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85340.629662] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85354.214437] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85354.289334] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85354.297707] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85354.329699] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85354.865480] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85354.972399] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85355.080563] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85355.192651] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85355.299390] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85355.405999] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85355.512289] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85355.565568] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85355.672811] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85356.039357] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85356.146666] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85356.253373] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85356.359544] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85356.465787] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85356.571609] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85356.678670] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85357.043643] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85357.151726] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85357.258850] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85357.365305] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85357.472095] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85357.578509] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85357.684965] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85358.051609] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85358.159537] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85358.266614] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85358.373475] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85358.479938] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85358.586754] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85358.640549] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85359.055963] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85359.164608] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85359.271782] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85359.379017] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85359.432650] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85359.539569] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85359.646828] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85360.066916] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85360.175552] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85360.283518] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85360.390411] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85360.497046] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85360.603931] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85360.711260] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85361.028429] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85361.136104] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85361.243117] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85361.350707] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85361.457743] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85361.564864] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85361.672460] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85362.047838] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85362.158456] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85362.267937] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85362.377304] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85362.532137] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85392.478225] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.478229] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.482452] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.482455] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.483586] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.483589] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.484673] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.484675] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.485747] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.485748] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.486820] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.486820] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.487892] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.487892] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.488964] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.488964] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.490037] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.490037] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.491108] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.491109] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.492181] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.492181] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.493254] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.493255] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.494338] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.494344] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.495495] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.495496] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.496630] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.496633] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.497774] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.497777] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.498911] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.498914] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.500049] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.500052] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.501188] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.501190] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.502331] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.502334] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.503425] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.503426] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.504559] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.504561] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.505705] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.505707] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.506842] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.506845] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.507980] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.507983] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.509073] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.509074] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.510141] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.510141] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.511206] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.511207] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.512272] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.512272] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.513292] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.513293] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.514359] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.514360] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.515425] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.515426] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.516492] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.516493] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.517558] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.517558] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.518623] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.518624] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.519689] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.519689] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.520755] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.520755] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.521820] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.521821] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.522885] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.522886] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.523951] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.523951] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.525017] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.525017] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.526083] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.526083] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.527148] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.527149] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.528214] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.528215] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.529282] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.529282] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.530301] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.530302] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.531367] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.531368] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.532434] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.532434] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.533499] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.533500] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.534565] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.534565] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.535630] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.535631] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.536701] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.536701] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.537766] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.537767] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.538832] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.538832] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.539897] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.539898] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.540963] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.540964] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.542029] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.542029] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.543094] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.543094] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.544160] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.544161] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.548928] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.548929] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.550084] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.550085] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.551196] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.551197] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.552311] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.552312] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.553379] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.553379] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85392.554444] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85392.554444] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85398.552847] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85398.552852] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85398.554099] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85398.554100] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85398.555617] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85398.555622] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85398.556884] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85398.556885] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85398.558007] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85398.558009] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85398.559082] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85398.559082] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85398.560155] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85398.560155] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85400.248707] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85400.354614] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85400.460955] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85400.567385] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85400.673357] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85400.780425] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85401.255713] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85401.362148] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85401.372644] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85402.513771] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.284864] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.409737] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.410333] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.426372] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.426947] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.442998] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.443567] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.459667] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.460216] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.476384] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.476966] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.492989] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.493549] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.509737] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.510303] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.526345] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.526916] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.542996] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.543561] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.559648] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.559899] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.576254] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.576463] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.592768] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.593054] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.609773] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.610226] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.626292] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.626836] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.642935] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.643468] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.659607] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.660153] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.676270] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.676820] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.692940] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.693477] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.709606] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.710145] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.726264] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.726805] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.742926] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.743465] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.759600] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.760138] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.776265] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.776801] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.792924] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.793459] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.809608] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.810144] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.826263] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.826804] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.842914] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.843452] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.859626] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.860167] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.876261] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.876800] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.892926] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.893461] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.909591] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.910131] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.926285] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.926830] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.942933] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.943476] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.959611] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.960150] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.976281] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.976856] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85424.992915] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85424.993451] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.009582] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.010115] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.026260] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.026800] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.042924] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.043475] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.059619] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.060158] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.076264] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.076808] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.092967] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.093303] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.109612] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.110155] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.126281] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.126797] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.143177] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.143486] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.159640] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.159936] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.176291] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.176585] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.193504] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.193779] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.319659] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.373719] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.374434] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.477828] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.478465] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.527056] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.527707] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85425.584403] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85425.585115] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85487.107027] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.161471] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.214622] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.269815] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.324112] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.376834] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.429705] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.484661] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.538763] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.592866] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.645837] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.698843] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.751371] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.804206] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.858859] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.912433] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85487.965330] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.018140] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.073170] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.127219] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.180429] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.232678] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.287833] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.341395] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.394290] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.447057] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.501720] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.555439] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.609026] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.661962] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.714972] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.767875] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.820696] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.875662] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.929517] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85488.981781] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.034758] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.089941] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.143840] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.196758] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.249653] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.304854] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.358761] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.411727] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.464571] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.519450] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.573846] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.627739] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.680852] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.733833] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.786958] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.839868] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.894600] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85489.948450] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.001139] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.053684] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.108818] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.163121] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.216244] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.268997] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.323706] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.377477] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.430072] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.483276] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.538308] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.593331] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.647214] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.699149] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.752221] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.805459] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.858433] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.913979] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85490.967461] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.020067] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.071927] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.127196] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.181401] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.234646] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.287262] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.342531] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.396560] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.449379] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.502838] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.557887] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.612875] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.666098] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.719493] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.772489] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.825652] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.878717] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.933727] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85491.987923] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.040944] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.094292] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.149434] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.162525] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.212905] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.289186] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.548231] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.641865] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85492.700352] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000fba59068 bind failed
[85503.798673] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.798677] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.799918] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.799919] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.801061] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.801061] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.802184] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.802185] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.803296] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.803297] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.804404] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.804405] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.805501] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.805501] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.806590] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.806590] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.807673] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.807673] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.812611] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.812614] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.813742] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.813743] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.814852] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.814854] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.815943] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.815944] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.817025] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.817025] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.818103] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.818103] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.819180] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.819180] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.820256] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.820257] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.821332] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.821332] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.822408] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.822409] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.823487] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.823488] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.824565] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.824566] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.825642] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.825642] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.826718] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.826718] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.827954] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.827955] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.829171] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.829174] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.830315] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.830316] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.831398] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* amdgpu_vm_validate() failed.
[85503.831399] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Not enough memory for command submission!
[85503.849004] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.849363] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85503.865026] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.865224] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85503.881731] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.881947] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85503.898367] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.898547] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85503.915020] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.915197] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85503.931678] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.931860] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85503.948343] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.948519] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85503.964989] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000e6a4bf4c bind failed
[85503.965166] [drm:amdgpu_dm_plane_helper_prepare_fb [amdgpu]] *ERROR* 00000000feac4cc7 bind failed
[85612.136017] [drm:gfx_v11_0_priv_reg_irq [amdgpu]] *ERROR* Illegal register access in command stream
[85612.136291] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85612.136861] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85612.136903] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85612.136904] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85612.136905] amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=11770374, emitted seq=11770375
[85612.136907] amdgpu 0000:04:00.0: amdgpu:  Process llama-server pid 117794 thread llama-server pid 117794
[85612.136907] amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
[85614.140694] amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=RESET
[85614.140697] amdgpu 0000:04:00.0: amdgpu: failed to reset legacy queue
[85614.140698] amdgpu 0000:04:00.0: amdgpu: reset via MES failed and try pipe reset -110
[85614.140699] amdgpu 0000:04:00.0: amdgpu: The CPFW hasn't support pipe reset yet.
[85614.140700] amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset failed
[85614.140702] amdgpu 0000:04:00.0: amdgpu: GPU reset begin!. Source:  1
[85616.630591] amdgpu 0000:04:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[85616.630596] amdgpu 0000:04:00.0: amdgpu: failed to unmap legacy queue
[85616.899534] [drm:gfx_v11_0_hw_fini.llvm.8476049994119752861 [amdgpu]] *ERROR* failed to halt cp gfx
[85616.900889] amdgpu 0000:04:00.0: amdgpu: MODE2 reset
[85616.922949] amdgpu 0000:04:00.0: amdgpu: GPU reset succeeded, trying to resume
[85616.923408] [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
[85616.923442] amdgpu 0000:04:00.0: amdgpu: VRAM is lost due to GPU reset!
[85616.923445] amdgpu 0000:04:00.0: amdgpu: SMU is resuming...
[85616.927536] amdgpu 0000:04:00.0: amdgpu: SMU is resumed successfully!
[85616.935752] amdgpu 0000:04:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09003E00
[85618.074573] amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[85618.074576] amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[85618.074577] amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[85618.074578] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[85618.074579] amdgpu 0000:04:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[85618.074579] amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[85618.074579] amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[85618.074580] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[85618.074580] amdgpu 0000:04:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[85618.074581] amdgpu 0000:04:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[85618.074581] amdgpu 0000:04:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[85618.074582] amdgpu 0000:04:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 1 on hub 8
[85618.074582] amdgpu 0000:04:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[85618.074583] amdgpu 0000:04:00.0: amdgpu: ring vpe uses VM inv eng 4 on hub 8
[85618.083426] amdgpu 0000:04:00.0: amdgpu: GPU reset(1) succeeded!
[85618.083436] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85618.083506] amdgpu 0000:04:00.0: amdgpu: [drm] *ERROR* Failed to initialize parser -125!
[85618.540439] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc wezterm-gui(86929) task wezterm-gu:cs0(86908) is non-zero when fini
[85618.592099] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc python3.10(114871) task python3.10:cs0(114832) is non-zero when fini
[85619.667739] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc kmail(110161) task kmail:cs0(110157) is non-zero when fini
[85620.486265] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85620.486998] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85620.487014] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85620.487015] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85620.487018] amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=11770377, emitted seq=11770380
[85620.487021] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85620.487023] amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
[85620.487127] amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
[85620.487129] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85622.662210] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85622.663401] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85622.663414] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85622.663416] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85622.663417] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=729739, emitted seq=729740
[85622.663419] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85622.663420] amdgpu 0000:04:00.0: amdgpu: Starting comp_1.2.1 ring reset
[85622.663458] amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:2:1)
[85622.663557] amdgpu 0000:04:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
[85622.663559] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85624.710169] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85624.711153] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85624.711169] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85624.711171] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85624.711175] amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=11770381, emitted seq=11770383
[85624.711178] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85624.711180] amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
[85624.711265] amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
[85624.711267] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85625.721499] amdgpu 0000:04:00.0: amdgpu: VM memory stats for proc llama-server(117794) task llama-server(117794) is non-zero when fini
[85626.758458] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85626.763889] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85626.763907] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85626.763909] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85626.763911] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=729741, emitted seq=729742
[85626.763913] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85626.763915] amdgpu 0000:04:00.0: amdgpu: Starting comp_1.2.1 ring reset
[85626.763942] amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:2:1)
[85626.764096] amdgpu 0000:04:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
[85626.764098] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85628.806437] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85628.809081] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85628.809100] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85628.809102] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85628.809104] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=729743, emitted seq=729744
[85628.809106] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85628.809107] amdgpu 0000:04:00.0: amdgpu: Starting comp_1.2.1 ring reset
[85628.809129] amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:2:1)
[85628.809264] amdgpu 0000:04:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
[85628.809265] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85630.854073] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85630.857946] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85630.857966] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85630.857968] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85630.857970] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=729745, emitted seq=729746
[85630.857972] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85630.857973] amdgpu 0000:04:00.0: amdgpu: Starting comp_1.2.1 ring reset
[85630.857996] amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:2:1)
[85630.858159] amdgpu 0000:04:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
[85630.858161] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85632.902256] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85632.903275] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85632.903295] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85632.903297] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85632.903299] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 timeout, signaled seq=729747, emitted seq=729750
[85632.903301] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85632.903303] amdgpu 0000:04:00.0: amdgpu: Starting comp_1.2.1 ring reset
[85632.903325] amdgpu 0000:04:00.0: amdgpu: reset compute queue (1:2:1)
[85632.903457] amdgpu 0000:04:00.0: amdgpu: Ring comp_1.2.1 reset succeeded
[85632.903459] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85634.950362] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85634.953106] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85634.953127] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85634.953129] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85634.953131] amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=11770384, emitted seq=11770386
[85634.953133] amdgpu 0000:04:00.0: amdgpu:  Process kwin_wayland pid 1118 thread kwin_wayla:cs0 pid 1147
[85634.953134] amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
[85634.953285] amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
[85634.953286] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
[85635.202202] fbcon: Taking over console
[85636.639412] Console: switching to colour frame buffer device 180x56
[85637.254455] amdgpu 0000:04:00.0: amdgpu: Dumping IP State
[85637.257037] amdgpu 0000:04:00.0: amdgpu: Dumping IP State Completed
[85637.257055] amdgpu 0000:04:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[85637.257057] amdgpu 0000:04:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[85637.257059] amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=11770393, emitted seq=11770396
[85637.257060] amdgpu 0000:04:00.0: amdgpu:  Process firefox pid 118351 thread firefox:cs0 pid 118410
[85637.257062] amdgpu 0000:04:00.0: amdgpu: Starting gfx_0.0.0 ring reset
[85637.257221] amdgpu 0000:04:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
[85637.257222] amdgpu 0000:04:00.0: [drm] device wedged, but recovered through reset
```

Notice that when it happened, the memory was ~80% used (I have a widget that was still alive).
The only MES reported errors are "MES failed to respond to msg=REMOVE_QUEUE", maybe it's unrelated to this bug and this is another bug going on.

I had a software calling llamacpp server with a batch of text to translate (something like 9000 sequential and successive calls). llamacpp is leaking memory slowly (I don't know why), so I have to unload the model and reload it once it reaches 92% of the system memory. When I'm doing this, it's giving the message in the previous post about VM memory stats being non zero.

---

### 评论 #32 — ckuethe (2026-05-19T01:16:13Z)

joining the party with a system76 pangolin - `AMD Ryzen AI 7 350 w/ Radeon 860M` .

Using the workaround mentioned [above](https://github.com/ROCm/ROCm/issues/5844#issuecomment-4108668995) has made my machine fairly stable; previously graphics would lock up within a couple of minutes, now that's gone away complete.

new problem: running inference with llama.cpp via lemonade, I get pretty frequent graphics stalls - window content (and the clock) doesn't update for a few seconds at a time - then it unfreezes but feels laggy.

---
