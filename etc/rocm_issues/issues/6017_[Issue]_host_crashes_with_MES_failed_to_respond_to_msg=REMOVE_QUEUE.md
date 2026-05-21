# [Issue]: host crashes with MES failed to respond to msg=REMOVE_QUEUE

> **Issue #6017**
> **状态**: open
> **创建时间**: 2026-03-03T21:04:07Z
> **更新时间**: 2026-04-16T08:22:15Z
> **作者**: ctheune
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6017

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

We experience regular (multiple times per day) soft lockups that trigger the IPMI watchdog:

```
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1806
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: Failed to evict queue 18
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: GPU reset begin!. Source:  3
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: Failed to evict process queues
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: device lost from bus!
Mar 03 14:14:04 kernel: amdgpu 0000:83:00.0: amdgpu: GPU reset end with ret = -19
Mar 03 14:14:04 kernel: ------------[ cut here ]------------
Mar 03 14:14:04 kernel: WARNING: CPU: 16 PID: 326437 at drivers/gpu/drm/amd/amdgpu/../amdkfd/kfd_device_queue_manager.c:1343 restore_process_queues_cpsch+0x229/0x270 [amdgpu]
Mar 03 14:14:04 kernel: Modules linked in: af_packet vrf bridge stp llc vxlan ip6_udp_tunnel udp_tunnel dummy msr nft_limit xt_limit nft_chain_nat xt_CT xt_conntrack ip6t_rpfilter ipt_rpfilter xt_pktty>
Mar 03 14:14:05 telegraf[3872]: 2026-03-03T13:14:05Z E! [agent] Error terminating process children: no such process
Mar 03 14:14:05 telegraf[3872]: 2026-03-03T13:14:05Z E! [inputs.amd_rocm_smi] Error in plugin: failed to execute command in pollROCmSMI: command timed out
Mar 03 14:14:05 skvaider-inference-start[3215]: 2026-03-03 14:14:05 [info     ] rocm memory total=193,206,419,456 used=116,584,169,472 free=76,622,249,984
Mar 03 14:14:05 kernel:  mlx5_fwctl sha1 snd aesni_intel i2c_piix4 rapl ib_core acpi_cpufreq einj fwctl rtc_cmos mac_hid usb_storage soundcore mii ast ipmi_msghandler rng_core k10temp i2c_smbus button >
Mar 03 14:14:05 kernel: CPU: 16 UID: 0 PID: 326437 Comm: kworker/16:0 Tainted: G S                  6.18.15 #1-NixOS PREEMPT(voluntary)
Mar 03 14:14:05 kernel: Tainted: [S]=CPU_OUT_OF_SPEC
Mar 03 14:14:05 kernel: Hardware name: ASUSTeK COMPUTER INC. RS700A-E12-RS12U/K14PP-D24 Series, BIOS 2201 05/23/2025
Mar 03 14:14:05 kernel: Workqueue: events_freezable svm_range_restore_work [amdgpu]
Mar 03 14:14:05 kernel: RIP: 0010:restore_process_queues_cpsch+0x229/0x270 [amdgpu]
Mar 03 14:14:05 kernel: Code: 85 ac d7 48 00 48 8b 4c 24 08 e9 3b ff ff ff ba ff ff ff ff be 02 00 00 00 48 89 ef e8 f0 e6 ff ff 41 89 c6 e9 47 ff ff ff 90 <0f> 0b 90 45 31 f6 e9 4f fe ff ff 45 31 f6 e>
Mar 03 14:14:05 kernel: RSP: 0018:ff7b89bafbfefd38 EFLAGS: 00010246
Mar 03 14:14:05 kernel: RAX: 0000000000000800 RBX: ff3813fee5d8e800 RCX: 0000000000000000
Mar 03 14:14:05 kernel: RDX: 0000000000000000 RSI: ff3813fee5d8e810 RDI: ff3813efb673fd40
Mar 03 14:14:05 kernel: RBP: ff3813efb673fc00 R08: 00002504885cff42 R09: 00000000000262e7
Mar 03 14:14:05 kernel: R10: ffffffffffffffa0 R11: 0075757e8bd4b330 R12: ff3813fee5d8e810
Mar 03 14:14:05 kernel: R13: ff3813efb673fd40 R14: ff3813ff04e63000 R15: ff3813fee736cc80
Mar 03 14:14:05 kernel: FS:  0000000000000000(0000) GS:ff38140ef212c000(0000) knlGS:0000000000000000
Mar 03 14:14:05 kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Mar 03 14:14:05 kernel: CR2: 000055a49c0fd008 CR3: 00000011af0a6006 CR4: 0000000000f71ef0
Mar 03 14:14:05 kernel: PKRU: 55555554
Mar 03 14:14:05 kernel: Call Trace:
Mar 03 14:14:05 kernel:  <TASK>
Mar 03 14:14:05 kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 03 14:14:05 kernel:  kfd_process_restore_queues+0x62/0xb0 [amdgpu]
Mar 03 14:14:05 kernel:  kgd2kfd_resume_mm+0x20/0x40 [amdgpu]
Mar 03 14:14:05 kernel:  svm_range_restore_work+0x1f4/0x2f0 [amdgpu]
Mar 03 14:14:05 kernel:  process_one_work+0x18d/0x340
Mar 03 14:14:05 kernel:  worker_thread+0x165/0x2d0
Mar 03 14:14:05 kernel:  ? __pfx_worker_thread+0x10/0x10
Mar 03 14:14:05 kernel:  kthread+0xfb/0x250
Mar 03 14:14:05 kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Mar 03 14:14:05 kernel:  ? finish_task_switch.isra.0+0x99/0x2e0
Mar 03 14:14:05 kernel:  ? __pfx_kthread+0x10/0x10
Mar 03 14:14:05 kernel:  ? __pfx_kthread+0x10/0x10
Mar 03 14:14:05 kernel:  ret_from_fork+0x1ce/0x200
Mar 03 14:14:05 kernel:  ? __pfx_kthread+0x10/0x10
Mar 03 14:14:05 kernel:  ret_from_fork_asm+0x1a/0x30
Mar 03 14:14:05 kernel:  </TASK>
Mar 03 14:14:05 kernel: ---[ end trace 0000000000000000 ]---
```


### Operating System

NixOS 25.11 (Xantusia)

### CPU

AMD EPYC 9124 16-Core Processor (2 sockets)

### GPU

4 x AMD Radeon Pro W7900 Dual Slot

### ROCm Version

ROCm 7.1.1 or 6.4.3 (the listed libraries are a bit confusing)

### ROCm Component

_No response_

### Steps to Reproduce

We run a number of llama-servers with various models (gpt-oss-120b, gpt-oss-20b, mistral-3.2:latest, embeddinggemma:300m, bge-m3:567m, nomic-embed-text:v1.5).



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
Runtime Ext Version:     1.7
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
  Name:                    AMD EPYC 9124 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 9124 16-Core Processor
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
  Max Clock Freq. (MHz):   3000
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
      Size:                    65561676(0x3e8644c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65561676(0x3e8644c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65561676(0x3e8644c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65561676(0x3e8644c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    AMD EPYC 9124 16-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD EPYC 9124 16-Core Processor
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
  Max Clock Freq. (MHz):   3000
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
      Size:                    65999596(0x3ef12ec) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65999596(0x3ef12ec) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65999596(0x3ef12ec) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65999596(0x3ef12ec) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 3
*******
  Name:                    gfx1100
  Uuid:                    GPU-41adee3f46c89193
  Marketing Name:          AMD Radeon Pro W7900 Dual Slot
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
    L1:                      32(0x20) KB
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29770(0x744a)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   1760
  BDFID:                   17152
  Internal Node ID:        2
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
  Packet Processor uCode:: 602
  SDMA engine uCode::      27
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 4
*******
  Name:                    gfx1100
  Uuid:                    GPU-50d0e2bf902fa866
  Marketing Name:          AMD Radeon Pro W7900 Dual Slot
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    3
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29770(0x744a)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   1760
  BDFID:                   8960
  Internal Node ID:        3
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
  Packet Processor uCode:: 602
  SDMA engine uCode::      27
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 5
*******
  Name:                    gfx1100
  Uuid:                    GPU-430f9b57535d5af6
  Marketing Name:          AMD Radeon Pro W7900 Dual Slot
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    4
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29770(0x744a)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   1760
  BDFID:                   33536
  Internal Node ID:        4
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
  Packet Processor uCode:: 602
  SDMA engine uCode::      27
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*******
Agent 6
*******
  Name:                    gfx1100
  Uuid:                    GPU-ff2958a9ef8c9140
  Marketing Name:          AMD Radeon Pro W7900 Dual Slot
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    5
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29770(0x744a)
  ASIC Revision:           0(0x0)
  Cacheline Size:          128(0x80)
  Max Clock Freq. (MHz):   1760
  BDFID:                   41728
  Internal Node ID:        5
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
  Packet Processor uCode:: 602
  SDMA engine uCode::      27
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
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***

### Additional Information

This is on Linux 6.18.15 with "the MES" patch already applied.

.supermario1 asked me to post this here again.


---

## 评论 (3 条)

### 评论 #1 — superm1 (2026-03-03T21:07:38Z)

To be clear: this is the patch I suggested picking up: https://github.com/torvalds/linux/commit/6b0d812971370c64b837a2db4275410f478272fe that it continues to reproduce with in place.

---

### 评论 #2 — ctheune (2026-03-09T07:14:50Z)

This keeps happening. Sometimes we see almost silent crashes:

```
Mar 09 07:59:40 kernel: amdgpu 0000:83:00.0: amdgpu: Dumping IP State
Mar 09 08:00:11  kernel: watchdog: BUG: soft lockup - CPU#3 stuck for 26s! [kworker/u256:0:3507322]
-- Boot 90e9d5de6b2143fa93fd5dba0a409c69 --
```


---

### 评论 #3 — kklemon (2026-04-16T08:22:15Z)

@Rmalavally @samjwu Any update on this issue? I find it insane that AMD still can't provide basic stability for their GPU compute after all those years.

---
