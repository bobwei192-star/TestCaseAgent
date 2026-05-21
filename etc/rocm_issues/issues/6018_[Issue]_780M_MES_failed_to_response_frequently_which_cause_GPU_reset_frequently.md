# [Issue]: 780M  MES failed to response frequently which cause GPU reset frequently with doorbell 0x1002,0x1000

> **Issue #6018**
> **状态**: open
> **创建时间**: 2026-03-04T15:20:44Z
> **更新时间**: 2026-05-10T10:25:04Z
> **作者**: zw963
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6018

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

### Problem Description

Run ollama with translategemma 12b for local translate, MES failed to response frequently which cause GPU reset frequently, check following log.

### Operating System

Arch linux

### CPU

7840hs

### GPU

780M

### ROCm Version

7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

```
[73314.889668] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73314.889675] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[73314.889677] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73314.889681] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[73314.889682] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[73314.889684] amdgpu: Failed to quiesce KFD
[73314.889701] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73314.891684] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 49700
[73314.891708] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73314.893432] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73316.994500] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73316.994507] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.998481] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73318.998487] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73318.999856] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73319.031470] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73319.031938] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73319.032193] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73319.032198] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73319.032202] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73319.033702] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73319.039404] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73319.185138] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73319.185150] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73319.185153] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73319.185155] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73319.185157] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73319.185158] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73319.185160] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73319.185162] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73319.185163] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73319.185165] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73319.185167] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73319.185169] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73319.185171] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73319.187263] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[73319.187276] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[73327.541061] amdgpu: Freeing queue vital buffer 0x7f2e27400000, queue evicted
[73327.541067] amdgpu: Freeing queue vital buffer 0x7f3041200000, queue evicted
[73327.541070] amdgpu: Freeing queue vital buffer 0x7f3047400000, queue evicted
[73327.541071] amdgpu: Freeing queue vital buffer 0x7f3047a00000, queue evicted
[73327.541075] amdgpu: Freeing queue vital buffer 0x7f3196600000, queue evicted
[73327.649199] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73327.649205] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[73327.649207] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73327.649211] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[73327.649212] amdgpu: Resetting wave fronts (cpsch) on dev 0000000058c303b6
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[73327.649214] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73327.649312] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73327.652804] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73327.758867] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73327.793270] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73327.793923] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73327.793983] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73327.793985] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73327.793988] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73327.796093] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73327.803519] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73328.541797] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73328.541804] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73328.541807] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73328.541808] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73328.541810] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73328.541811] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73328.541813] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73328.541814] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73328.541815] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73328.541817] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73328.541819] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73328.541820] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73328.541822] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73328.543914] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[73328.543927] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[73819.930091] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73819.930100] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[73819.930102] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73819.930107] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[73819.930111] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[73819.930135] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73819.933292] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 49700
[73819.933323] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73819.934978] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73822.026089] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73822.026096] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73824.030060] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73824.030066] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[73824.031435] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73824.063114] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73824.063599] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73824.063826] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73824.063832] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73824.063839] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73824.065380] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73824.071356] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73824.193078] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73824.193087] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73824.193090] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73824.193092] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73824.193094] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73824.193095] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73824.193097] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73824.193099] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73824.193101] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73824.193103] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73824.193105] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73824.193107] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73824.193109] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73824.195332] amdgpu 0000:c5:00.0: amdgpu: GPU reset(3) succeeded!
[73824.195345] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[73838.829061] amdgpu: Freeing queue vital buffer 0x7fe58f200000, queue evicted
[73838.829068] amdgpu: Freeing queue vital buffer 0x7fe59fc00000, queue evicted
[73838.829070] amdgpu: Freeing queue vital buffer 0x7fe5a0000000, queue evicted
[73838.829071] amdgpu: Freeing queue vital buffer 0x7fe909c00000, queue evicted
[73838.829073] amdgpu: Freeing queue vital buffer 0x7fe90a200000, queue evicted
[73838.829080] amdgpu: Freeing queue vital buffer 0x7fe99a200000, queue evicted
[73838.921111] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[73838.921122] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[73838.921124] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[73838.921129] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[73838.921132] amdgpu: Resetting wave fronts (cpsch) on dev 0000000058c303b6
[73838.921135] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[73838.921148] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[73838.921240] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[73838.925110] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[73839.018046] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[73839.051567] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[73839.052262] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[73839.052325] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[73839.052328] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[73839.052332] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[73839.053887] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[73839.060470] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[73839.816239] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[73839.816247] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[73839.816250] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[73839.816251] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[73839.816253] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[73839.816254] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[73839.816255] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[73839.816257] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[73839.816258] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[73839.816260] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[73839.816262] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[73839.816263] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[73839.816265] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[73839.818312] amdgpu 0000:c5:00.0: amdgpu: GPU reset(4) succeeded!
[73839.818325] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[74121.237443] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74121.237451] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[74121.237453] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[74121.237457] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[74121.237459] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[74121.237480] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[74121.241693] amdgpu 0000:c5:00.0: amdgpu: Failed to restore queue 5
[74121.241696] amdgpu 0000:c5:00.0: amdgpu: Failed to restore process queues
[74121.242215] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 5 for dev 49700
[74121.242244] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[74121.243864] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[74123.339950] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74123.339957] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[74125.343943] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74125.343950] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[74125.345332] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[74125.375969] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[74125.376466] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[74125.376550] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[74125.376562] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[74125.376576] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[74125.378181] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[74125.383901] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[74125.505881] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[74125.505890] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[74125.505893] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[74125.505895] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[74125.505897] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[74125.505898] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[74125.505900] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[74125.505901] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[74125.505903] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[74125.505911] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[74125.505913] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[74125.505914] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[74125.505916] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[74125.508081] amdgpu 0000:c5:00.0: amdgpu: GPU reset(5) succeeded!
[74125.508096] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[74127.209515] amdgpu: Freeing queue vital buffer 0x7f5407400000, queue evicted
[74127.209521] amdgpu: Freeing queue vital buffer 0x7f5621800000, queue evicted
[74127.209524] amdgpu: Freeing queue vital buffer 0x7f5634400000, queue evicted
[74127.209525] amdgpu: Freeing queue vital buffer 0x7f5634a00000, queue evicted
[74127.209529] amdgpu: Freeing queue vital buffer 0x7f5776600000, queue evicted
[74127.261547] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74127.261554] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1008
[74127.261557] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[74127.261560] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 5
[74127.261564] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[74127.261614] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74127.261617] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[74127.261619] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[74127.261621] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[74127.261647] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[74127.264687] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[74127.362731] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[74127.396007] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[74127.396641] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[74127.396721] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[74127.396724] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[74127.396727] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[74127.397656] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[74127.404264] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[74128.026595] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[74128.026603] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[74128.026606] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[74128.026607] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[74128.026609] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[74128.026610] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[74128.026611] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[74128.026613] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[74128.026614] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[74128.026616] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[74128.026617] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[74128.026619] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[74128.026621] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[74128.028737] amdgpu 0000:c5:00.0: amdgpu: GPU reset(6) succeeded!
[74128.028751] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[74147.033117] amdgpu: Freeing queue vital buffer 0x7fb3bac00000, queue evicted
[74154.953981] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74154.953988] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[74154.953990] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[74154.953994] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[74154.953996] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[74154.953998] amdgpu: Failed to quiesce KFD
[74154.954014] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[74154.954766] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 49700
[74154.954795] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[74154.956754] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[74157.055311] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74157.055318] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[74159.059304] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74159.059311] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[74159.060798] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[74159.092363] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[74159.092883] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[74159.093096] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[74159.093098] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[74159.093101] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[74159.094614] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[74159.100208] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[74159.222235] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[74159.222243] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[74159.222246] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[74159.222247] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[74159.222249] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[74159.222250] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[74159.222252] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[74159.222253] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[74159.222255] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[74159.222257] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[74159.222258] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[74159.222260] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[74159.222262] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[74159.224396] amdgpu 0000:c5:00.0: amdgpu: GPU reset(7) succeeded!
[74159.224410] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[74159.900878] amdgpu: Freeing queue vital buffer 0x7f5a35a00000, queue evicted
[74159.900886] amdgpu: Freeing queue vital buffer 0x7f5a46000000, queue evicted
[74159.900890] amdgpu: Freeing queue vital buffer 0x7f5c6ca00000, queue evicted
[74159.900891] amdgpu: Freeing queue vital buffer 0x7f5da4600000, queue evicted
[74159.900896] amdgpu: Freeing queue vital buffer 0x7f5dae600000, queue evicted
[74159.940895] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74159.940908] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[74159.940912] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[74159.940920] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[74159.940924] amdgpu: Resetting wave fronts (cpsch) on dev 0000000058c303b6
[74159.940927] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[74159.940927] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[74159.941031] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[74159.944284] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[74160.044686] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[74160.079198] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[74160.079924] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[74160.079969] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[74160.079971] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[74160.079974] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[74160.080853] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[74160.088019] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[74160.709700] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[74160.709708] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[74160.709710] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[74160.709712] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[74160.709713] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[74160.709715] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[74160.709716] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[74160.709717] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[74160.709719] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[74160.709721] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[74160.709722] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[74160.709724] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[74160.709725] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[74160.711825] amdgpu 0000:c5:00.0: amdgpu: GPU reset(8) succeeded!
[74160.711837] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[74243.815136] amdgpu: Freeing queue vital buffer 0x7f8741400000, queue evicted
[74257.667205] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74257.667212] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[74257.667214] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[74257.667217] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[74257.667219] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[74257.667221] amdgpu: Failed to quiesce KFD
[74257.667239] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[74257.667254] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 49700
[74257.667278] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[74257.669273] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[74259.772206] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74259.772214] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[74261.776183] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74261.776191] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[74261.777671] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[74261.808782] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[74261.809266] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[74261.809349] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[74261.809360] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[74261.809373] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[74261.811030] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[74261.816743] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[74261.938533] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[74261.938541] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[74261.938543] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[74261.938545] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[74261.938546] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[74261.938548] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[74261.938549] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[74261.938551] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[74261.938552] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[74261.938554] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[74261.938555] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[74261.938557] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[74261.938558] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[74261.940336] amdgpu 0000:c5:00.0: amdgpu: GPU reset(9) succeeded!
[74261.940348] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[74262.586736] amdgpu: Freeing queue vital buffer 0x7f526d400000, queue evicted
[74262.586744] amdgpu: Freeing queue vital buffer 0x7f527d800000, queue evicted
[74262.586747] amdgpu: Freeing queue vital buffer 0x7f55d4200000, queue evicted
[74262.586749] amdgpu: Freeing queue vital buffer 0x7f55d4800000, queue evicted
[74262.586752] amdgpu: Freeing queue vital buffer 0x7f55dd600000, queue evicted
[74262.630844] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[74262.630850] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[74262.630852] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[74262.630855] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[74262.630857] amdgpu: Resetting wave fronts (cpsch) on dev 0000000058c303b6
[74262.630859] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[74262.630859] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[74262.630938] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[74262.634581] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[74262.726752] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[74262.761776] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[74262.762445] [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[74262.762517] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[74262.762521] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[74262.762525] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[74262.764668] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[74262.771408] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[74263.510407] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[74263.510415] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[74263.510417] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[74263.510419] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[74263.510421] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[74263.510422] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[74263.510423] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[74263.510425] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[74263.510426] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[74263.510428] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[74263.510430] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[74263.510431] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[74263.510433] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[74263.512637] amdgpu 0000:c5:00.0: amdgpu: GPU reset(10) succeeded!
[74263.512650] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
```

```
$: cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap zswap.enabled=0 sysrq_always_enabled=1 amdgpu.gpu_recovery=1 initrd=\boot\initramfs-linux-xanmod.img
```

```
 ╰──➤ $ pacman -Q |grep -E 'rocm|amd'
amd-ucode 20260221-1
amdgpu_top 0.11.2-1
hip-runtime-amd 7.2.0-1
lib32-vulkan-amdgpu-pro 25.10_2202160-1
linux-amd-drm-fixes 6.19.2026.02.05-1
linux-amd-drm-fixes-headers 6.19.2026.02.05-1
linux-firmware-amdgpu 20260221-1
ollama-rocm 0.17.0-1
python-pytorch-rocm 2.10.0-2
python-torchaudio-rocm 2.10.0-3
rocm-cmake 7.2.0-1
rocm-core 7.2.0-2
rocm-device-libs 2:7.2.0-1
rocm-hip-libraries 7.2.0-1
rocm-hip-runtime 7.2.0-1
rocm-hip-sdk 7.2.0-1
rocm-language-runtime 7.2.0-1
rocm-llvm 2:7.2.0-1
rocm-opencl-runtime 7.2.0-1
rocm-opencl-sdk 7.2.0-1
rocm-smi-lib 7.2.0-1
rocminfo 7.2.0-1
vulkan-amdgpu-pro 25.10_2202160-1
xf86-video-amdgpu 25.0.0-1
```

```
 ╰──➤ $ uname -a
Linux mingfan 6.18.13-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Fri, 20 Feb 2026 05:25:15 +0000 x86_64 GNU/Linux
```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
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
  Name:                    AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
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
  Max Clock Freq. (MHz):   5137                               
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
      Size:                    49116096(0x2ed73c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49116096(0x2ed73c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49116096(0x2ed73c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    49116096(0x2ed73c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1103                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon 780M Graphics           
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
  Chip ID:                 5567(0x15bf)                       
  ASIC Revision:           7(0x7)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            12                                 
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
  Packet Processor uCode:: 67                                 
  SDMA engine uCode::      23                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24558048(0x176b9e0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24558048(0x176b9e0) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1103         
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
  Marketing Name:          RyzenAI-npu1                       
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
    L2:                      2048(0x800) KB                     
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
      Size:                    49116096(0x2ed73c0) KB             
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
      Size:                    49116096(0x2ed73c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***
```


### Additional Information

_No response_

---

## 评论 (21 条)

### 评论 #1 — chejh-amd (2026-03-05T03:37:46Z)

This is a known issue when running ROCm ML workloads on the 780M (gfx1103 iGPU). AMD engineers have already submitted patches that address MES hangs occurring during queue evict/restore operations. Some distributions have already integrated the gfx1103 fix into their drm-fixes / amdgpu-fixes kernel, so you may want to try running on one of those kernels.

---

### 评论 #2 — zw963 (2026-03-05T13:17:32Z)

Switch to use amd drm fixes, still same.

```
 ╰──➤ $ uname -a
Linux mingfan 7.0.0-rc1-1-amd-drm-fixes-g6b0d81297137 #1 SMP PREEMPT_DYNAMIC Fri, 27 Feb 2026 05:48:09 +0000 x86_64 GNU/Linux
```

```
[ 9439.851420] amdgpu 0000:c5:00.0: MES failed to respond to msg=REMOVE_QUEUE
[ 9439.851426] amdgpu 0000:c5:00.0: failed to remove hardware queue from MES, doorbell=0x1002
[ 9439.851428] amdgpu 0000:c5:00.0: MES might be in unrecoverable state, issue a GPU reset
[ 9439.851432] amdgpu 0000:c5:00.0: Failed to evict queue 1
[ 9439.851435] amdgpu 0000:c5:00.0: Failed to evict process queues
[ 9439.851435] amdgpu 0000:c5:00.0: GPU reset begin!. Source:  3
[ 9439.852814] amdgpu 0000:c5:00.0: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 24135
[ 9439.852838] amdgpu 0000:c5:00.0: Dumping IP State
[ 9439.854637] amdgpu 0000:c5:00.0: Dumping IP State Completed
[ 9441.949835] amdgpu 0000:c5:00.0: MES failed to respond to msg=REMOVE_QUEUE
[ 9441.949842] amdgpu 0000:c5:00.0: failed to unmap legacy queue
[ 9443.953834] amdgpu 0000:c5:00.0: MES failed to respond to msg=REMOVE_QUEUE
[ 9443.953842] amdgpu 0000:c5:00.0: failed to unmap legacy queue
[ 9443.955231] amdgpu 0000:c5:00.0: MODE2 reset
[ 9443.987962] amdgpu 0000:c5:00.0: GPU reset succeeded, trying to resume
[ 9443.988441] amdgpu 0000:c5:00.0: [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[ 9443.988667] amdgpu 0000:c5:00.0: [drm] AMDGPU device coredump file has been created
[ 9443.988670] amdgpu 0000:c5:00.0: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[ 9443.988674] amdgpu 0000:c5:00.0: SMU is resuming...
[ 9443.990930] amdgpu 0000:c5:00.0: SMU is resumed successfully!
[ 9443.996975] amdgpu 0000:c5:00.0: [drm] DMUB hardware initialized: version=0x08005700
[ 9444.118781] amdgpu 0000:c5:00.0: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 9444.118790] amdgpu 0000:c5:00.0: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 9444.118793] amdgpu 0000:c5:00.0: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 9444.118794] amdgpu 0000:c5:00.0: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 9444.118795] amdgpu 0000:c5:00.0: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 9444.118797] amdgpu 0000:c5:00.0: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 9444.118798] amdgpu 0000:c5:00.0: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 9444.118799] amdgpu 0000:c5:00.0: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 9444.118801] amdgpu 0000:c5:00.0: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 9444.118802] amdgpu 0000:c5:00.0: ring sdma0 uses VM inv eng 12 on hub 0
[ 9444.118804] amdgpu 0000:c5:00.0: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 9444.118806] amdgpu 0000:c5:00.0: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 9444.118807] amdgpu 0000:c5:00.0: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 9444.121042] amdgpu 0000:c5:00.0: GPU reset(1) succeeded!
[ 9444.121066] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[ 9445.867892] rfkill: input handler enabled
[ 9446.428379] amdgpu 0000:c5:00.0: MES failed to respond to msg=REMOVE_QUEUE
[ 9446.428564] amdgpu 0000:c5:00.0: failed to remove hardware queue from MES, doorbell=0x1000
[ 9446.428706] amdgpu 0000:c5:00.0: MES might be in unrecoverable state, issue a GPU reset
[ 9446.428814] amdgpu 0000:c5:00.0: Failed to remove queue 0
[ 9446.428846] amdgpu 0000:c5:00.0: GPU reset begin!. Source:  3
[ 9446.428849] amdgpu: Resetting wave fronts (cpsch) on dev 0000000060d4ac61
[ 9446.428853] amdgpu 0000:c5:00.0: no vmid pasid mapping supported
[ 9446.452257] amdgpu 0000:c5:00.0: Dumping IP State
[ 9446.455412] amdgpu 0000:c5:00.0: Dumping IP State Completed
[ 9446.554798] amdgpu 0000:c5:00.0: MODE2 reset
[ 9446.589953] amdgpu 0000:c5:00.0: GPU reset succeeded, trying to resume
[ 9446.590624] amdgpu 0000:c5:00.0: [drm] PCIE GART of 512M enabled (table at 0x00000083FFD00000).
[ 9446.590682] amdgpu 0000:c5:00.0: [drm] AMDGPU device coredump file has been created
[ 9446.590684] amdgpu 0000:c5:00.0: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[ 9446.590687] amdgpu 0000:c5:00.0: SMU is resuming...
[ 9446.592819] amdgpu 0000:c5:00.0: SMU is resumed successfully!
[ 9446.599507] amdgpu 0000:c5:00.0: [drm] DMUB hardware initialized: version=0x08005700
[ 9446.721686] amdgpu 0000:c5:00.0: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 9446.721702] amdgpu 0000:c5:00.0: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 9446.721707] amdgpu 0000:c5:00.0: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 9446.721711] amdgpu 0000:c5:00.0: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 9446.721714] amdgpu 0000:c5:00.0: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 9446.721718] amdgpu 0000:c5:00.0: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 9446.721721] amdgpu 0000:c5:00.0: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 9446.721724] amdgpu 0000:c5:00.0: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 9446.721727] amdgpu 0000:c5:00.0: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 9446.721731] amdgpu 0000:c5:00.0: ring sdma0 uses VM inv eng 12 on hub 0
[ 9446.721734] amdgpu 0000:c5:00.0: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 9446.721738] amdgpu 0000:c5:00.0: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 9446.721741] amdgpu 0000:c5:00.0: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 9446.763324] amdgpu 0000:c5:00.0: GPU reset(2) succeeded!
[ 9446.763340] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
```

---

### 评论 #3 — jdelgadoalfonso (2026-03-05T13:58:25Z)

Same with 
```
uname -a
Linux Kaleta-pcbox 7.0.0-rc2-1-amd-drm-fixes #1 SMP PREEMPT_DYNAMIC Thu, 05 Mar 2026 12:42:59 +0000 x86_64 **GNU/Linux**
```
```
[  287.444743] amdgpu 0000:c6:00.0: MES failed to respond to msg=REMOVE_QUEUE
[  287.444748] amdgpu 0000:c6:00.0: failed to remove hardware queue from MES, doorbell=0x1004
[  287.444749] amdgpu 0000:c6:00.0: MES might be in unrecoverable state, issue a GPU reset
[  287.444752] amdgpu 0000:c6:00.0: Failed to evict queue 2
[  287.444754] amdgpu 0000:c6:00.0: Failed to evict process queues
[  287.444755] amdgpu: Failed to quiesce KFD
[  287.444775] amdgpu 0000:c6:00.0: GPU reset begin!. Source:  3
[  287.444789] amdgpu 0000:c6:00.0: remove_all_kfd_queues_mes: Failed to remove queue 1 for dev 60136
[  287.444815] amdgpu 0000:c6:00.0: Dumping IP State
[  287.447988] amdgpu 0000:c6:00.0: Dumping IP State Completed
[  289.539493] amdgpu 0000:c6:00.0: MES failed to respond to msg=REMOVE_QUEUE
[  289.539498] amdgpu 0000:c6:00.0: failed to unmap legacy queue
[  291.543352] amdgpu 0000:c6:00.0: MES failed to respond to msg=REMOVE_QUEUE
[  291.543356] amdgpu 0000:c6:00.0: failed to unmap legacy queue
[  293.547309] amdgpu 0000:c6:00.0: MES failed to respond to msg=REMOVE_QUEUE
[  293.547313] amdgpu 0000:c6:00.0: failed to unmap legacy queue
[  293.754859] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[  293.756407] amdgpu 0000:c6:00.0: MODE2 reset
[  293.788982] amdgpu 0000:c6:00.0: GPU reset succeeded, trying to resume
[  293.789585] amdgpu 0000:c6:00.0: [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[  293.789877] amdgpu 0000:c6:00.0: [drm] AMDGPU device coredump file has been created
[  293.789889] amdgpu 0000:c6:00.0: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[  293.789903] amdgpu 0000:c6:00.0: SMU is resuming...
[  293.792598] amdgpu 0000:c6:00.0: SMU is resumed successfully!
[  293.799672] amdgpu 0000:c6:00.0: [drm] DMUB hardware initialized: version=0x08005700
[  293.871607] amdgpu 0000:c6:00.0: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  293.871616] amdgpu 0000:c6:00.0: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  293.871618] amdgpu 0000:c6:00.0: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  293.871620] amdgpu 0000:c6:00.0: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  293.871622] amdgpu 0000:c6:00.0: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  293.871623] amdgpu 0000:c6:00.0: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  293.871624] amdgpu 0000:c6:00.0: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  293.871626] amdgpu 0000:c6:00.0: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  293.871627] amdgpu 0000:c6:00.0: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  293.871628] amdgpu 0000:c6:00.0: ring sdma0 uses VM inv eng 12 on hub 0
[  293.871630] amdgpu 0000:c6:00.0: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  293.871632] amdgpu 0000:c6:00.0: ring jpeg_dec uses VM inv eng 1 on hub 8
[  293.871633] amdgpu 0000:c6:00.0: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  293.873529] amdgpu 0000:c6:00.0: GPU reset(1) succeeded!
[  293.873539] amdgpu 0000:c6:00.0: [drm] device wedged, but recovered through reset
[  297.427663] amdgpu 0000:c6:00.0: MES failed to respond to msg=REMOVE_QUEUE
[  297.427689] amdgpu 0000:c6:00.0: failed to remove hardware queue from MES, doorbell=0x1002
[  297.427704] amdgpu 0000:c6:00.0: MES might be in unrecoverable state, issue a GPU reset
[  297.427724] amdgpu 0000:c6:00.0: Failed to remove queue 1
[  297.427743] amdgpu 0000:c6:00.0: GPU reset begin!. Source:  3
[  297.427817] amdgpu 0000:c6:00.0: MES failed to respond to msg=REMOVE_QUEUE
[  297.427835] amdgpu 0000:c6:00.0: failed to remove hardware queue from MES, doorbell=0x1000
[  297.427849] amdgpu 0000:c6:00.0: MES might be in unrecoverable state, issue a GPU reset
[  297.427864] amdgpu 0000:c6:00.0: Failed to remove queue 0
[  297.427986] amdgpu 0000:c6:00.0: Dumping IP State
[  297.433257] amdgpu 0000:c6:00.0: Dumping IP State Completed
[  297.526150] amdgpu 0000:c6:00.0: MODE2 reset
[  297.561680] amdgpu 0000:c6:00.0: GPU reset succeeded, trying to resume
[  297.562373] amdgpu 0000:c6:00.0: [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[  297.562503] amdgpu 0000:c6:00.0: [drm] AMDGPU device coredump file has been created
[  297.562510] amdgpu 0000:c6:00.0: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[  297.562518] amdgpu 0000:c6:00.0: SMU is resuming...
[  297.564436] amdgpu 0000:c6:00.0: SMU is resumed successfully!
[  297.571330] amdgpu 0000:c6:00.0: [drm] DMUB hardware initialized: version=0x08005700
[  297.643104] amdgpu 0000:c6:00.0: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  297.643114] amdgpu 0000:c6:00.0: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  297.643116] amdgpu 0000:c6:00.0: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  297.643118] amdgpu 0000:c6:00.0: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  297.643120] amdgpu 0000:c6:00.0: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  297.643121] amdgpu 0000:c6:00.0: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  297.643122] amdgpu 0000:c6:00.0: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  297.643124] amdgpu 0000:c6:00.0: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  297.643125] amdgpu 0000:c6:00.0: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  297.643127] amdgpu 0000:c6:00.0: ring sdma0 uses VM inv eng 12 on hub 0
[  297.643129] amdgpu 0000:c6:00.0: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  297.643131] amdgpu 0000:c6:00.0: ring jpeg_dec uses VM inv eng 1 on hub 8
[  297.643133] amdgpu 0000:c6:00.0: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  297.645518] amdgpu 0000:c6:00.0: GPU reset(2) succeeded!
[  297.645534] amdgpu 0000:c6:00.0: [drm] device wedged, but recovered through reset
```

---

### 评论 #4 — amd-nicknick (2026-03-11T09:26:36Z)

Hi @zw963, may I ask which build of Ollama you're currently using? Since Ollama uses pre-packaged ROCm dependency during build time, it is likely that it is not using the latest ROCm release.
The change has been merged into Ollama https://github.com/ollama/ollama/pull/14391, but is is not yet in any release at this time. 
Could you please try rebuilding Ollama with latest main branch and give it another try? Thanks!

---

### 评论 #5 — zw963 (2026-03-11T09:49:59Z)

I install ollama use arch linux package manager (pacman), this issue created when use ollama/ollama-rocm 0.17.0, and can reproduce on 0.17.5 too, current use 0.17.7, tested no luck too.(if ran with amdgpu.cwsr_enable=0 no issue)

---

### 评论 #6 — zw963 (2026-03-11T10:59:20Z)

Hi, @amd-nicknick , I try to build ollama with: `go build` on git hash 87d21c7f, then copy it into /usr/local/bin, Then fix my ollama user service to use this version

```
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
Environment="OLLAMA_KEEP_ALIVE=-1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_QUEUE=1"
Environment="OLLAMA_FLASH_ATTENTION=1"
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

But this version never use rOCm, instead of, use 100% CPU.

```
● ollama.service - Ollama Service
     Loaded: loaded (/home/zw963/.config/systemd/user/ollama.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-03-11 18:53:39 CST; 1min 22s ago
 Invocation: ddf190efda054d229738f9657e82c933
   Main PID: 1223 (ollama)
      Tasks: 13 (limit: 75644)
     Memory: 38.7M (peak: 51.6M)
        CPU: 39ms
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/ollama.service
             └─1223 /usr/local/bin/ollama serve

Mar 11 18:53:39 mingfan ollama[1223]: [GIN-debug] GET    /v1/models/:model         --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (7 handlers)
Mar 11 18:53:39 mingfan ollama[1223]: [GIN-debug] POST   /v1/responses             --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
Mar 11 18:53:39 mingfan ollama[1223]: [GIN-debug] POST   /v1/images/generations    --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
Mar 11 18:53:39 mingfan ollama[1223]: [GIN-debug] POST   /v1/images/edits          --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
Mar 11 18:53:39 mingfan ollama[1223]: [GIN-debug] POST   /v1/messages              --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
Mar 11 18:53:39 mingfan ollama[1223]: time=2026-03-11T18:53:39.324+08:00 level=INFO source=routes.go:1796 msg="Listening on 127.0.0.1:11434 (version 0.0.0)"
Mar 11 18:53:39 mingfan ollama[1223]: time=2026-03-11T18:53:39.342+08:00 level=INFO source=runner.go:67 msg="discovering available GPUs..."
Mar 11 18:53:39 mingfan ollama[1223]: time=2026-03-11T18:53:39.345+08:00 level=INFO source=server.go:430 msg="starting runner" cmd="/usr/local/bin/ollama runner --ollama-engine --port 12517"
Mar 11 18:53:39 mingfan ollama[1223]: time=2026-03-11T18:53:39.362+08:00 level=INFO source=types.go:60 msg="inference compute" id=cpu library=cpu compute="" name=cpu description=cpu libdirs=ollama driver="" pci_>
Mar 11 18:53:39 mingfan ollama[1223]: time=2026-03-11T18:53:39.362+08:00 level=INFO source=routes.go:1846 msg="vram-based default context" total_vram="0 B" default_num_ctx=4096
```

Any idea how to build a supported to use GPU version?

Thanks

---

### 评论 #7 — amd-nicknick (2026-03-11T11:04:20Z)

Try using Docker build & running ollama directly inside a docker container
See: https://github.com/ollama/ollama/blob/main/docs/development.md#docker
`docker build --build-arg FLAVOR=rocm -t <YOUR IMAGE TAG> .`
Run with
`docker run -d --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama -p 11434:11434 --name ollama <YOUR IMAGE TAG>`

---

### 评论 #8 — zw963 (2026-03-11T12:03:22Z)

crashed.

```
docker run --rm --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama -p 11434:11434 --name ollama rocm_build
time=2026-03-11T12:00:16.009Z level=INFO source=routes.go:1741 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GGML_VK_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:0 OLLAMA_DEBUG:INFO OLLAMA_EDITOR: OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://0.0.0.0:11434 OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/root/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NO_CLOUD:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA_SCHED_SPREAD:false OLLAMA_VULKAN:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
time=2026-03-11T12:00:16.009Z level=INFO source=routes.go:1743 msg="Ollama cloud disabled: false"
time=2026-03-11T12:00:16.009Z level=INFO source=images.go:477 msg="total blobs: 0"
time=2026-03-11T12:00:16.009Z level=INFO source=images.go:484 msg="total unused blobs removed: 0"
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:   export GIN_MODE=release
 - using code:  gin.SetMode(gin.ReleaseMode)

[GIN-debug] HEAD   /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func1 (5 handlers)
[GIN-debug] GET    /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func2 (5 handlers)
[GIN-debug] HEAD   /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func3 (5 handlers)
[GIN-debug] GET    /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func4 (5 handlers)
[GIN-debug] GET    /api/status               --> github.com/ollama/ollama/server.(*Server).StatusHandler-fm (5 handlers)
[GIN-debug] POST   /api/pull                 --> github.com/ollama/ollama/server.(*Server).PullHandler-fm (5 handlers)
[GIN-debug] POST   /api/push                 --> github.com/ollama/ollama/server.(*Server).PushHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] GET    /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] POST   /api/show                 --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (5 handlers)
[GIN-debug] DELETE /api/delete               --> github.com/ollama/ollama/server.(*Server).DeleteHandler-fm (5 handlers)
[GIN-debug] POST   /api/me                   --> github.com/ollama/ollama/server.(*Server).WhoamiHandler-fm (5 handlers)
[GIN-debug] POST   /api/signout              --> github.com/ollama/ollama/server.(*Server).SignoutHandler-fm (5 handlers)
[GIN-debug] DELETE /api/user/keys/:encodedKey --> github.com/ollama/ollama/server.(*Server).SignoutHandler-fm (5 handlers)
[GIN-debug] POST   /api/create               --> github.com/ollama/ollama/server.(*Server).CreateHandler-fm (5 handlers)
[GIN-debug] POST   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).CreateBlobHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).HeadBlobHandler-fm (5 handlers)
[GIN-debug] POST   /api/copy                 --> github.com/ollama/ollama/server.(*Server).CopyHandler-fm (5 handlers)
[GIN-debug] GET    /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).ListAliasesHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).CreateAliasHandler-fm (5 handlers)
[GIN-debug] DELETE /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).DeleteAliasHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/web_search --> github.com/ollama/ollama/server.(*Server).WebSearchExperimentalHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/web_fetch --> github.com/ollama/ollama/server.(*Server).WebFetchExperimentalHandler-fm (5 handlers)
[GIN-debug] GET    /api/ps                   --> github.com/ollama/ollama/server.(*Server).PsHandler-fm (5 handlers)
[GIN-debug] POST   /api/generate             --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (5 handlers)
[GIN-debug] POST   /api/chat                 --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (5 handlers)
[GIN-debug] POST   /api/embed                --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (5 handlers)
[GIN-debug] POST   /api/embeddings           --> github.com/ollama/ollama/server.(*Server).EmbeddingsHandler-fm (5 handlers)
[GIN-debug] POST   /v1/chat/completions      --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
[GIN-debug] POST   /v1/completions           --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/embeddings            --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (7 handlers)
[GIN-debug] GET    /v1/models                --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (6 handlers)
[GIN-debug] GET    /v1/models/:model         --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (7 handlers)
[GIN-debug] POST   /v1/responses             --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
[GIN-debug] POST   /v1/images/generations    --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/images/edits          --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/messages              --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
time=2026-03-11T12:00:16.010Z level=INFO source=routes.go:1796 msg="Listening on [::]:11434 (version 0.0.0)"
time=2026-03-11T12:00:16.010Z level=INFO source=runner.go:67 msg="discovering available GPUs..."
time=2026-03-11T12:00:16.010Z level=INFO source=server.go:430 msg="starting runner" cmd="/usr/bin/ollama runner --ollama-engine --port 33191"
time=2026-03-11T12:00:16.076Z level=INFO source=server.go:430 msg="starting runner" cmd="/usr/bin/ollama runner --ollama-engine --port 40427"
time=2026-03-11T12:00:16.598Z level=INFO source=runner.go:464 msg="failure during GPU discovery" OLLAMA_LIBRARY_PATH="[/usr/lib/ollama /usr/lib/ollama/rocm]" extra_envs="map[GGML_CUDA_INIT:1 ROCR_VISIBLE_DEVICES:0]" error="runner crashed"
time=2026-03-11T12:00:16.598Z level=INFO source=types.go:60 msg="inference compute" id=cpu library=cpu compute="" name=cpu description=cpu libdirs=ollama driver="" pci_id="" type="" total="61.6 GiB" available="61.6 GiB"
time=2026-03-11T12:00:16.598Z level=INFO source=routes.go:1846 msg="vram-based default context" total_vram="0 B" default_num_ctx=4096
```

I try copy ollama binary out of container, no luck.

```
 ╰──➤ $ ./ollama serve
time=2026-03-11T19:59:06.151+08:00 level=INFO source=routes.go:1741 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GGML_VK_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:0 OLLAMA_DEBUG:INFO OLLAMA_EDITOR: OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/home/zw963/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NO_CLOUD:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA_SCHED_SPREAD:false OLLAMA_VULKAN:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
time=2026-03-11T19:59:06.151+08:00 level=INFO source=routes.go:1743 msg="Ollama cloud disabled: false"
time=2026-03-11T19:59:06.153+08:00 level=INFO source=images.go:477 msg="total blobs: 53"
time=2026-03-11T19:59:06.154+08:00 level=INFO source=images.go:484 msg="total unused blobs removed: 0"
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:   export GIN_MODE=release
 - using code:  gin.SetMode(gin.ReleaseMode)

[GIN-debug] HEAD   /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func1 (5 handlers)
[GIN-debug] GET    /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func2 (5 handlers)
[GIN-debug] HEAD   /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func3 (5 handlers)
[GIN-debug] GET    /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func4 (5 handlers)
[GIN-debug] GET    /api/status               --> github.com/ollama/ollama/server.(*Server).StatusHandler-fm (5 handlers)
[GIN-debug] POST   /api/pull                 --> github.com/ollama/ollama/server.(*Server).PullHandler-fm (5 handlers)
[GIN-debug] POST   /api/push                 --> github.com/ollama/ollama/server.(*Server).PushHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] GET    /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] POST   /api/show                 --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (5 handlers)
[GIN-debug] DELETE /api/delete               --> github.com/ollama/ollama/server.(*Server).DeleteHandler-fm (5 handlers)
[GIN-debug] POST   /api/me                   --> github.com/ollama/ollama/server.(*Server).WhoamiHandler-fm (5 handlers)
[GIN-debug] POST   /api/signout              --> github.com/ollama/ollama/server.(*Server).SignoutHandler-fm (5 handlers)
[GIN-debug] DELETE /api/user/keys/:encodedKey --> github.com/ollama/ollama/server.(*Server).SignoutHandler-fm (5 handlers)
[GIN-debug] POST   /api/create               --> github.com/ollama/ollama/server.(*Server).CreateHandler-fm (5 handlers)
[GIN-debug] POST   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).CreateBlobHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).HeadBlobHandler-fm (5 handlers)
[GIN-debug] POST   /api/copy                 --> github.com/ollama/ollama/server.(*Server).CopyHandler-fm (5 handlers)
[GIN-debug] GET    /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).ListAliasesHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).CreateAliasHandler-fm (5 handlers)
[GIN-debug] DELETE /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).DeleteAliasHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/web_search --> github.com/ollama/ollama/server.(*Server).WebSearchExperimentalHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/web_fetch --> github.com/ollama/ollama/server.(*Server).WebFetchExperimentalHandler-fm (5 handlers)
[GIN-debug] GET    /api/ps                   --> github.com/ollama/ollama/server.(*Server).PsHandler-fm (5 handlers)
[GIN-debug] POST   /api/generate             --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (5 handlers)
[GIN-debug] POST   /api/chat                 --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (5 handlers)
[GIN-debug] POST   /api/embed                --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (5 handlers)
[GIN-debug] POST   /api/embeddings           --> github.com/ollama/ollama/server.(*Server).EmbeddingsHandler-fm (5 handlers)
[GIN-debug] POST   /v1/chat/completions      --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
[GIN-debug] POST   /v1/completions           --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/embeddings            --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (7 handlers)
[GIN-debug] GET    /v1/models                --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (6 handlers)
[GIN-debug] GET    /v1/models/:model         --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (7 handlers)
[GIN-debug] POST   /v1/responses             --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
[GIN-debug] POST   /v1/images/generations    --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/images/edits          --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/messages              --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
time=2026-03-11T19:59:06.154+08:00 level=INFO source=routes.go:1796 msg="Listening on 127.0.0.1:11434 (version 0.0.0)"
time=2026-03-11T19:59:06.154+08:00 level=INFO source=runner.go:67 msg="discovering available GPUs..."
time=2026-03-11T19:59:06.155+08:00 level=INFO source=server.go:430 msg="starting runner" cmd="/home/zw963/.local/share/containers/ollama runner --ollama-engine --port 14037"
time=2026-03-11T19:59:06.168+08:00 level=INFO source=types.go:60 msg="inference compute" id=cpu library=cpu compute="" name=cpu description=cpu libdirs=ollama driver="" pci_id="" type="" total="61.6 GiB" available="56.4 GiB"
time=2026-03-11T19:59:06.168+08:00 level=INFO source=routes.go:1846 msg="vram-based default context" total_vram="0 B" default_num_ctx=4096
^C
```

---

### 评论 #9 — amd-nicknick (2026-03-12T08:17:38Z)

Is the GPU crashing when the runner crashes? Share the dmesg log and ollama log (Set the env variable `OLLAMA_DEBUG=1`)
In the meantime, let me find a PHX machine to test this. Could you provide the make & model of your system?

---

### 评论 #10 — zw963 (2026-03-12T19:08:43Z)

Sorry for confusing, what i means crashed is just a notification like following when start ollama, but the server still keep running not exit.(need Ctrl + C to exit)

<img width="871" height="326" alt="Image" src="https://github.com/user-attachments/assets/3c5bcc69-bda1-457e-b313-c5efcb636fd6" />

But, this not happen when run directly use binary copied from docker, following is the log:

```
 ╰──➤ $ OLLAMA_DEBUG=1 ./ollama serve
time=2026-03-13T02:55:17.881+08:00 level=INFO source=routes.go:1741 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GGML_VK_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:0 OLLAMA_DEBUG:DEBUG OLLAMA_EDITOR: OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/home/zw963/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NO_CLOUD:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA_SCHED_SPREAD:false OLLAMA_VULKAN:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
time=2026-03-13T02:55:17.882+08:00 level=INFO source=routes.go:1743 msg="Ollama cloud disabled: false"
time=2026-03-13T02:55:17.883+08:00 level=INFO source=images.go:477 msg="total blobs: 53"
time=2026-03-13T02:55:17.884+08:00 level=INFO source=images.go:484 msg="total unused blobs removed: 0"
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:   export GIN_MODE=release
 - using code:  gin.SetMode(gin.ReleaseMode)

[GIN-debug] HEAD   /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func1 (5 handlers)
[GIN-debug] GET    /                         --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func2 (5 handlers)
[GIN-debug] HEAD   /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func3 (5 handlers)
[GIN-debug] GET    /api/version              --> github.com/ollama/ollama/server.(*Server).GenerateRoutes.func4 (5 handlers)
[GIN-debug] GET    /api/status               --> github.com/ollama/ollama/server.(*Server).StatusHandler-fm (5 handlers)
[GIN-debug] POST   /api/pull                 --> github.com/ollama/ollama/server.(*Server).PullHandler-fm (5 handlers)
[GIN-debug] POST   /api/push                 --> github.com/ollama/ollama/server.(*Server).PushHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] GET    /api/tags                 --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (5 handlers)
[GIN-debug] POST   /api/show                 --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (5 handlers)
[GIN-debug] DELETE /api/delete               --> github.com/ollama/ollama/server.(*Server).DeleteHandler-fm (5 handlers)
[GIN-debug] POST   /api/me                   --> github.com/ollama/ollama/server.(*Server).WhoamiHandler-fm (5 handlers)
[GIN-debug] POST   /api/signout              --> github.com/ollama/ollama/server.(*Server).SignoutHandler-fm (5 handlers)
[GIN-debug] DELETE /api/user/keys/:encodedKey --> github.com/ollama/ollama/server.(*Server).SignoutHandler-fm (5 handlers)
[GIN-debug] POST   /api/create               --> github.com/ollama/ollama/server.(*Server).CreateHandler-fm (5 handlers)
[GIN-debug] POST   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).CreateBlobHandler-fm (5 handlers)
[GIN-debug] HEAD   /api/blobs/:digest        --> github.com/ollama/ollama/server.(*Server).HeadBlobHandler-fm (5 handlers)
[GIN-debug] POST   /api/copy                 --> github.com/ollama/ollama/server.(*Server).CopyHandler-fm (5 handlers)
[GIN-debug] GET    /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).ListAliasesHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).CreateAliasHandler-fm (5 handlers)
[GIN-debug] DELETE /api/experimental/aliases --> github.com/ollama/ollama/server.(*Server).DeleteAliasHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/web_search --> github.com/ollama/ollama/server.(*Server).WebSearchExperimentalHandler-fm (5 handlers)
[GIN-debug] POST   /api/experimental/web_fetch --> github.com/ollama/ollama/server.(*Server).WebFetchExperimentalHandler-fm (5 handlers)
[GIN-debug] GET    /api/ps                   --> github.com/ollama/ollama/server.(*Server).PsHandler-fm (5 handlers)
[GIN-debug] POST   /api/generate             --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (5 handlers)
[GIN-debug] POST   /api/chat                 --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (5 handlers)
[GIN-debug] POST   /api/embed                --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (5 handlers)
[GIN-debug] POST   /api/embeddings           --> github.com/ollama/ollama/server.(*Server).EmbeddingsHandler-fm (5 handlers)
[GIN-debug] POST   /v1/chat/completions      --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
[GIN-debug] POST   /v1/completions           --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/embeddings            --> github.com/ollama/ollama/server.(*Server).EmbedHandler-fm (7 handlers)
[GIN-debug] GET    /v1/models                --> github.com/ollama/ollama/server.(*Server).ListHandler-fm (6 handlers)
[GIN-debug] GET    /v1/models/:model         --> github.com/ollama/ollama/server.(*Server).ShowHandler-fm (7 handlers)
[GIN-debug] POST   /v1/responses             --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
[GIN-debug] POST   /v1/images/generations    --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/images/edits          --> github.com/ollama/ollama/server.(*Server).GenerateHandler-fm (7 handlers)
[GIN-debug] POST   /v1/messages              --> github.com/ollama/ollama/server.(*Server).ChatHandler-fm (7 handlers)
time=2026-03-13T02:55:17.884+08:00 level=INFO source=routes.go:1796 msg="Listening on 127.0.0.1:11434 (version 0.0.0)"
time=2026-03-13T02:55:17.884+08:00 level=DEBUG source=sched.go:145 msg="starting llm scheduler"
time=2026-03-13T02:55:17.885+08:00 level=INFO source=runner.go:67 msg="discovering available GPUs..."
time=2026-03-13T02:55:17.886+08:00 level=INFO source=server.go:430 msg="starting runner" cmd="/home/common/Git/ollama/ollama runner --ollama-engine --port 33083"
time=2026-03-13T02:55:17.886+08:00 level=DEBUG source=server.go:431 msg=subprocess OLLAMA_DEBUG=1 ROCM_PATH=/opt/rocm PATH=/home/zw963/.asdf/shims:/home/zw963/.rvm/gems/ruby-4.0.1/bin:/home/zw963/.rvm/gems/ruby-4.0.1@global/bin:/home/zw963/.rvm/rubies/ruby-4.0.1/bin:/home/zw963/.cargo/bin:/home/zw963/.asdf/bin:/home/zw963/go/bin:/emulator:/platform-tools:/cmdline-tools/latest/bin:/home/zw963/utils/docker/dockerwrapper:/home/zw963/.local/bin:/home/zw963/Dropbox/common/sh:/home/zw963/.rvm/bin:/home/zw963/Dropbox/common/wrapper:/home/zw963/Dropbox/common/git:/opt/rocm/bin:/opt/pgsql-16/bin:/opt/containerd/bin:/opt/wemeet/bin:/home/zw963/Dropbox/common/rails/bin:/home/zw963/Dropbox/common/crystal/not_used_scripts/bin:/home/zw963/Dropbox/common/crystal/bin:/home/zw963/Dropbox/common/ruby/ruby_parser/bin:/home/zw963/Dropbox/common/ruby/ruby2d/bin:/home/zw963/Dropbox/common/ruby/rbtrace/bin:/home/zw963/Dropbox/common/ruby/pry/bin:/home/zw963/Dropbox/common/ruby/prof/bin:/home/zw963/Dropbox/common/ruby/nanoc/bin:/home/zw963/Dropbox/common/ruby/mruby/bin:/home/zw963/Dropbox/common/ruby/lib/bin:/home/zw963/Dropbox/common/ruby/invoice_printer/bin:/home/zw963/Dropbox/common/ruby/haskell/bin:/home/zw963/Dropbox/common/ruby/gems/bin:/home/zw963/Dropbox/common/ruby/debugger/bin:/home/zw963/Dropbox/common/ruby/debride/bin:/home/zw963/Dropbox/common/ruby/bin:/home/zw963/Dropbox/common/ruby/autotest/bin:/home/zw963/utils/ruby_tools/bin:/home/zw963/utils/go/bin:/home/zw963/utils/python_tools/bin:/home/zw963/utils/python_tools.old/bin:/home/zw963/utils/npm-packages/bin:/home/zw963/utils/node/bin:/home/zw963/utils/watchman/bin:/home/zw963/utils/zen_browser/bin:/home/zw963/utils/llms/sbin:/home/zw963/utils/llms/bin:/home/zw963/utils/charles/bin:/home/zw963/utils/xdotool/bin:/home/zw963/utils/unzip_gb18030/bin:/home/zw963/utils/tidy/bin:/home/zw963/utils/sensors/bin:/home/zw963/utils/scss/bin:/home/zw963/utils/rar/bin:/home/zw963/utils/qrencode/bin:/home/zw963/utils/proxy/bin:/home/zw963/utils/pgbouncer/bin:/home/zw963/utils/pg_backup/bin:/home/zw963/utils/parallel/bin:/home/zw963/utils/ngrok/bin:/home/zw963/utils/ncdu/bin:/home/zw963/utils/nano/bin:/home/zw963/utils/modern-unix-commands/sbin:/home/zw963/utils/modern-unix-commands/bin:/home/zw963/utils/mail/bin:/home/zw963/utils/linux_key_rebinding/bin:/home/zw963/utils/keyszer/bin:/home/zw963/utils/julia/bin:/home/zw963/utils/image_compresser/bin:/home/zw963/utils/htop/bin:/home/zw963/utils/dockerinit/sbin:/home/zw963/utils/dockerinit/bin:/home/zw963/utils/docker/bin:/home/zw963/utils/docker/sbin:/home/zw963/utils/deploy_tools/bin:/home/zw963/utils/ccal/bin:/home/zw963/utils/bin:/home/zw963/utils/bc3/bin:/home/zw963/utils/bats/bin:/home/zw963/utils/ag/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/opt/rocm/bin:/home/zw963/Dropbox/common/functions:/home/zw963/Dropbox/common/functions/linux:/home/zw963/Dropbox/common/functions/linux/bash_completions:/home/zw963/Dropbox/common/functions/langs:/home/zw963/Dropbox/common/functions/global:/home/zw963/Dropbox/common/functions/global/menu:/home/zw963/Dropbox/common/personal/functions:/home/zw963/Crystal/bin LD_LIBRARY_PATH=/home/common/Git/ollama OLLAMA_LIBRARY_PATH=/home/common/Git/ollama
time=2026-03-13T02:55:17.899+08:00 level=DEBUG source=runner.go:437 msg="bootstrap discovery took" duration=13.778145ms OLLAMA_LIBRARY_PATH=[/home/common/Git/ollama] extra_envs=map[]
time=2026-03-13T02:55:17.899+08:00 level=DEBUG source=runner.go:124 msg="evaluating which, if any, devices to filter out" initial_count=0
time=2026-03-13T02:55:17.899+08:00 level=DEBUG source=runner.go:40 msg="GPU bootstrap discovery took" duration=14.621965ms
time=2026-03-13T02:55:17.899+08:00 level=INFO source=types.go:60 msg="inference compute" id=cpu library=cpu compute="" name=cpu description=cpu libdirs=ollama driver="" pci_id="" type="" total="61.6 GiB" available="57.8 GiB"
time=2026-03-13T02:55:17.899+08:00 level=INFO source=routes.go:1846 msg="vram-based default context" total_vram="0 B" default_num_ctx=4096
```

What I said `no luck` is, as you can see in the log, it still can't find out the 780M GPU, it is TOO LONG to `ollama run qwen3.5:35b --think=false --hidethinking`

there is no error log output on dmesg.

>  Could you provide the make & model of your system?

What is the make & model ? if you said the pc, I use MINISFORUM U780xtx (7840hs + hynix DDR5 5600 32G x 2) mini pc, and bought 2 years ago.

--------

BTW, I built use `/usr/bin/podman --runtime runc` instead of docker, but without any error.

When use official released ollama, I can use 100% GPU for speed.

```
 ╰──➤ $ ollama ps
NAME                 ID              SIZE     PROCESSOR    CONTEXT    UNTIL
qwen3.5:35b-en2zh    54c9095f78d4    27 GB    100% GPU     32768      Forever
```

This mini PC support set max memory to 16G in the BIOS, but I select to use auto, because ollama can use GTT automatically.

<img width="1414" height="1242" alt="Image" src="https://github.com/user-attachments/assets/550572ec-3e1f-4e1b-b1ac-eb97510266d7" />





---

### 评论 #11 — zw963 (2026-03-17T11:11:29Z)

Hi, I updated to ollama/ollama-rocm 0.18.0, and testing.

```
 ╰──➤ $ pacman -Q |grep 'ollama\|rocm\|amd'
amd-ucode 20260309-1
amdgpu_top 0.11.2-1
hip-runtime-amd 7.2.0-1
lib32-vulkan-amdgpu-pro 25.10_2202160-1
linux-amd-drm-fixes 7.0.2026.02.26-1
linux-amd-drm-fixes-headers 7.0.2026.02.26-1
linux-firmware-amdgpu 20260309-1
ollama 0.18.0-1
ollama-rocm 0.18.0-1
python-pytorch-rocm 2.10.0-3
python-torchaudio-rocm 2.10.0-3
rocm-cmake 7.2.0-1
rocm-core 7.2.0-2
rocm-device-libs 2:7.2.0-1
rocm-hip-libraries 7.2.0-1
rocm-hip-runtime 7.2.0-1
rocm-hip-sdk 7.2.0-1
rocm-language-runtime 7.2.0-1
rocm-llvm 2:7.2.0-1
rocm-opencl-runtime 7.2.0-1
rocm-opencl-sdk 7.2.0-1
rocm-smi-lib 7.2.0-1
rocminfo 7.2.0-1
vulkan-amdgpu-pro 25.10_2202160-1
xf86-video-amdgpu 25.0.0-1
```

---

### 评论 #12 — choiman1559 (2026-03-17T11:55:22Z)

Try Rocm 7.1.1 with dkms module. This version will work because it has MES version 0x80 instead of MES version 0x83, which is the cause of the problem.

---

### 评论 #13 — zw963 (2026-03-18T02:56:37Z)

> it is likely that it is not using the latest ROCm release.
> The change has been merged into Ollama [ollama/ollama#14391](https://github.com/ollama/ollama/pull/14391), but is is not yet in any release at this time.
> Could you please try rebuilding Ollama with latest main branch and give it another try? Thanks!

Hi, @amd-nicknick , I updated to  ollama/ollama-rocm 0.18.0, it not broken yesterday, then I suspend my laptop and go to sleep, but, when the first time use ollama today morning after wakeup, it broken again.

Following is the log:

<details>
<summary>dmesg broken log since suspend until broken and relogin</summary>

```
[25888.355513] printk: Suspending console(s) (use no_console_suspend to debug)
[25888.495390] pcieport 0000:00:08.3: quirk: disabling D3cold for suspend
[25888.496253] ACPI: EC: interrupt blocked
[56586.962000] ACPI: EC: interrupt unblocked
[56587.132318] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[56587.132402] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[56587.135603] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[56587.135789] nvme nvme0: 16/0/0 default/read/poll queues
[56587.434490] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[56587.434496] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[56587.434498] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[56587.434499] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[56587.434501] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[56587.434502] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[56587.434503] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[56587.434504] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[56587.434505] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[56587.434507] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[56587.434508] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[56587.434509] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[56587.434510] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[56587.441718] OOM killer enabled.
[56587.441720] Restarting tasks: Starting
[56587.442886] Restarting tasks: Done
[56587.442899] efivarfs: resyncing variable state
[56587.444874] efivarfs: finished resyncing variable state
[56587.444962] random: crng reseeded on system resumption
[56587.452090] PM: suspend exit
[56587.563432] Realtek Internal NBASE-T PHY r8169-0-200:00: attached PHY driver (mii_bus:phy_addr=r8169-0-200:00, irq=MAC)
[56587.739535] r8169 0000:02:00.0 enp2s0: Link is Down
[56587.767417] Realtek Internal NBASE-T PHY r8169-0-300:00: attached PHY driver (mii_bus:phy_addr=r8169-0-300:00, irq=MAC)
[56587.951547] r8169 0000:03:00.0 enp3s0: Link is Down
[56590.677054] r8169 0000:02:00.0 enp2s0: Link is Up - 1Gbps/Full - flow control rx/tx
[56590.877206] userif-6: sent link down event.
[56590.877211] userif-6: sent link up event.
[56592.914223] userif-6: sent link down event.
[56592.914233] userif-6: sent link up event.
[56723.626615] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[56723.626620] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[56723.626623] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[56723.626626] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[56723.626628] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[56723.626630] amdgpu: Failed to quiesce KFD
[56723.626631] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[56723.626641] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 29984
[56723.626668] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[56723.628599] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[56725.734847] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[56725.734854] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[56727.738858] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[56727.738864] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[56727.740259] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[56727.772168] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[56727.772988] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[56727.773060] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[56727.773062] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[56727.773064] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[56727.774486] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[56727.780461] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[56727.926140] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[56727.926144] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[56727.926146] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[56727.926147] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[56727.926149] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[56727.926151] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[56727.926152] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[56727.926153] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[56727.926155] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[56727.926156] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[56727.926158] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[56727.926159] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[56727.926161] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[56727.928238] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[56727.928251] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[56737.668208] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[56737.668240] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[56737.668257] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[56737.668280] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[56737.668295] amdgpu: Resetting wave fronts (cpsch) on dev 000000005fe8a83f
[56737.668301] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[56737.668308] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[56737.668454] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[56737.672388] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[56737.769635] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[56737.803580] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[56737.804763] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[56737.804807] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[56737.804809] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[56737.804812] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[56737.805817] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[56737.812509] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[56737.934703] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[56737.934710] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[56737.934713] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[56737.934714] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[56737.934716] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[56737.934717] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[56737.934718] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[56737.934720] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[56737.934722] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[56737.934723] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[56737.934725] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[56737.934726] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[56737.934728] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[56737.936791] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[56737.936803] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[56738.480636] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc Xwayland(2105) task Xwayland:cs0(2048) is non-zero when fini
[56738.482144] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[56738.490279] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc xwaylandvideobr(3613) task xwaylandvi:cs0(1722) is non-zero when fini
[56738.490503] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc (0) task (0) is non-zero when fini
[56738.544415] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc wezterm-gui(4540) task wezterm-gu:cs0(1721) is non-zero when fini
[56738.699256] gnome-shell[1496]: segfault at 5635e1e8fc21 ip 00007f7add92d044 sp 00007ffc7a434468 error 4 in libmutter-17.so.0.0.0[12d044,7f7add83c000+1dc000] likely on CPU 4 (core 4, socket 0)
[56738.699267] Code: 1a 00 f3 0f 1e fa 48 89 c3 e9 f7 49 f1 ff f3 0f 1e fa 48 89 c3 e9 eb 49 f1 ff 90 66 66 2e 0f 1f 84 00 00 00 00 00 f3 0f 1e fa <48> 8b 47 30 c3 0f 1f 80 00 00 00 00 f3 0f 1e fa 48 8b 47 38 c3 0f
[56740.950362] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc gnome-shell(1527) task gnome-shel:cs0(1496) is non-zero when fini
[56740.953573] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc RDD Process(22937) task browser 4 :cs0(8713) is non-zero when fini
[56741.027023] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc firefox(8295) task firefox:cs0(8165) is non-zero when fini
[56741.068860] rfkill: input handler enabled
[56744.425115] drkonqi-coredum[236693]: segfault at 0 ip 00007f4db27e4e53 sp 00007ffea4c4fad8 error 4 in libQt6Core.so.6.10.2[1e4e53,7f4db2691000+3e9000] likely on CPU 1 (core 1, socket 0)
[56744.425126] Code: c0 74 04 f0 83 00 01 c3 90 0f 1f 00 66 66 2e 0f 1f 84 00 00 00 00 00 f3 0f 1e fa 48 8d 05 35 eb 43 00 48 83 e0 fc 48 89 47 18 <f3> 0f 6f 06 48 8b 56 10 66 48 0f 7e c0 0f 11 07 48 89 57 10 48 85
[56744.477312] amdgpu 0000:c5:00.0: amdgpu: VM memory stats for proc Xorg(1007) task Xorg:cs0(998) is non-zero when fini
[56745.078432] drkonqi-coredum[236774]: segfault at 0 ip 00007f8f8e9e4e53 sp 00007ffc88389c48 error 4 in libQt6Core.so.6.10.2[1e4e53,7f8f8e891000+3e9000] likely on CPU 2 (core 2, socket 0)
[56745.078440] Code: c0 74 04 f0 83 00 01 c3 90 0f 1f 00 66 66 2e 0f 1f 84 00 00 00 00 00 f3 0f 1e fa 48 8d 05 35 eb 43 00 48 83 e0 fc 48 89 47 18 <f3> 0f 6f 06 48 8b 56 10 66 48 0f 7e c0 0f 11 07 48 89 57 10 48 85
[56749.725092] rfkill: input handler disabled
[56750.789764] userif-6: sent link down event.
[56750.789770] userif-6: sent link up event.
[56751.712541] input: xremap as /devices/virtual/input/input28
[56755.850421] userif-6: sent link down event.
[56755.850426] userif-6: sent link up event.
```

</details>



---

### 评论 #14 — zw963 (2026-03-18T02:58:36Z)

> Try Rocm 7.1.1 with dkms module. This version will work because it has MES version 0x80 instead of MES version 0x83, which is the cause of the problem.

It's is hard to keep still stable after revert to old version when use rolling linux like Arch, thanks

---

### 评论 #15 — zw963 (2026-03-18T04:21:10Z)

I am current update to ollama 0.18.1, and still testing.

```
 ╰──➤ $ pacman -Q |grep 'amd\|rocm\|ollama'
amd-ucode 20260309-1
amdgpu_top 0.11.2-1
hip-runtime-amd 7.2.0-1
lib32-vulkan-amdgpu-pro 25.10_2202160-1
linux-amd-drm-fixes 7.0.2026.02.26-1
linux-amd-drm-fixes-headers 7.0.2026.02.26-1
linux-firmware-amdgpu 20260309-1
ollama 0.18.1-1
ollama-rocm 0.18.1-1
python-pytorch-rocm 2.10.0-3
python-torchaudio-rocm 2.10.0-3
rocm-cmake 7.2.0-1
rocm-core 7.2.0-2
rocm-device-libs 2:7.2.0-1
rocm-hip-libraries 7.2.0-1
rocm-hip-runtime 7.2.0-1
rocm-hip-sdk 7.2.0-1
rocm-language-runtime 7.2.0-1
rocm-llvm 2:7.2.0-1
rocm-opencl-runtime 7.2.0-1
rocm-opencl-sdk 7.2.0-1
rocm-smi-lib 7.2.0-1
rocminfo 7.2.0-1
vulkan-amdgpu-pro 25.10_2202160-1
xf86-video-amdgpu 25.0.0-1
```

```
 ╰──➤ $ uname -a
Linux mingfan 6.19.8-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Sun, 15 Mar 2026 17:26:13 +0000 x86_64 GNU/Linux
```

---

### 评论 #16 — amd-nicknick (2026-03-18T12:46:46Z)

Hi @zw963, it looks like you're hitting a known MES issue with older kernel + ROCm runtime.
Could you please try the following?
1. Disable CWSR
  Add `amdgpu.cwsr_enable=0` to your boot flag in GRUB, or create a modprobe file to add this parameter.
2. Check your MES version
  Provide the output of `sudo cat /sys/kernel/debug/dri/<Device BDF>/amdgpu_firmware_info`. the MES FW version should NOT be 0x83.

---

### 评论 #17 — zw963 (2026-03-18T13:52:18Z)


```
[root@mingfan dri]# cat  /sys/kernel/debug/dri/0000\:c5\:00.0/amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 35, firmware version: 0x00000064
PFP feature version: 35, firmware version: 0x0000006a
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x0000008b
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x0000000f
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 35, firmware version: 0x00000044
IMU feature version: 0, firmware version: 0x0b012d00
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004c4900 (76.73.0)
SDMA0 feature version: 60, firmware version: 0x00000018
VCN feature version: 0, firmware version: 0x09118010
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x08005700
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x00000109
MES feature version: 1, firmware version: 0x00000086
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-PHXGENERIC-001
```

```
[root@mingfan dri]# cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap zswap.enabled=0 sysrq_always_enabled=1 amdgpu.gpu_recovery=1 amdgpu.cwsr_enable=0 initrd=\boot\initramfs-linux-xanmod.img
```

---

### 评论 #18 — zw963 (2026-03-31T14:04:57Z)

This issue still happen a latest Arch linux update.

```
[98687.212075] perf: interrupt took too long (2552 > 2500), lowering kernel.perf_event_max_sample_rate to 78250
[98747.249509] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[98747.249516] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[98747.249519] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[98747.249523] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[98747.249525] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[98747.249528] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[98747.249541] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 29984
[98747.249569] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[98747.251319] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[98749.354479] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[98749.354498] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[98751.358569] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[98751.358581] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[98751.359970] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[98751.394414] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[98751.396066] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[98751.396205] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[98751.396207] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[98751.396210] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[98751.396581] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[98751.403438] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[98751.549148] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[98751.549156] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[98751.549158] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[98751.549160] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[98751.549162] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[98751.549164] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[98751.549166] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[98751.549167] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[98751.549170] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[98751.549172] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[98751.549173] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[98751.549176] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[98751.549178] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[98751.551201] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[98751.551214] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[98755.550522] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[98755.550531] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[98755.550534] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[98755.550538] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[98755.550540] amdgpu: Resetting wave fronts (cpsch) on dev 0000000028ca7dfd
[98755.550542] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[98755.550542] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[98755.550630] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[98755.553625] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[98755.657919] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[98755.690433] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[98755.691502] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[98755.691533] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[98755.691535] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[98755.691538] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[98755.692644] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[98755.698431] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[98755.820080] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[98755.820086] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[98755.820088] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[98755.820089] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[98755.820091] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[98755.820092] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[98755.820093] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[98755.820094] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[98755.820096] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[98755.820097] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[98755.820099] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[98755.820100] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[98755.820102] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[98755.822313] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
[98755.822321] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
```

---

### 评论 #19 — zw963 (2026-04-10T01:43:24Z)

```
[37583.630475] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[37583.630482] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[37583.630484] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[37583.630488] amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
[37583.630490] amdgpu 0000:c5:00.0: amdgpu: Failed to evict process queues
[37583.630491] amdgpu: Failed to quiesce KFD
[37583.630509] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[37583.630519] amdgpu 0000:c5:00.0: amdgpu: remove_all_kfd_queues_mes: Failed to remove queue 0 for dev 30175
[37583.630544] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[37583.632501] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[37585.732087] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[37585.732094] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[37587.736080] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[37587.736088] amdgpu 0000:c5:00.0: amdgpu: failed to unmap legacy queue
[37587.737457] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[37587.769019] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[37587.769932] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[37587.770000] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[37587.770002] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[37587.770004] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[37587.771256] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[37587.777121] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[37587.922770] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[37587.922779] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[37587.922782] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[37587.922783] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[37587.922784] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[37587.922786] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[37587.922788] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[37587.922789] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[37587.922791] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[37587.922793] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[37587.922795] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[37587.922797] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[37587.922798] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[37587.924808] amdgpu 0000:c5:00.0: amdgpu: GPU reset(1) succeeded!
[37587.924820] amdgpu 0000:c5:00.0: [drm] device wedged, but recovered through reset
[37589.664711] amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[37589.664719] amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
[37589.664723] amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[37589.664727] amdgpu 0000:c5:00.0: amdgpu: Failed to remove queue 0
[37589.664730] amdgpu: Resetting wave fronts (cpsch) on dev 0000000064df9925
[37589.664732] amdgpu 0000:c5:00.0: amdgpu: no vmid pasid mapping supported
[37589.664749] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!. Source:  3
[37589.664839] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
[37589.668235] amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
[37589.762179] amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
[37589.796652] amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
[37589.797853] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[37589.797894] amdgpu 0000:c5:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[37589.797896] amdgpu 0000:c5:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
[37589.797899] amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
[37589.798324] amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
[37589.805206] amdgpu 0000:c5:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x08005700
[37589.926936] amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[37589.926944] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[37589.926946] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[37589.926948] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[37589.926949] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[37589.926950] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[37589.926952] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[37589.926953] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[37589.926955] amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[37589.926957] amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[37589.926958] amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[37589.926960] amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[37589.926961] amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[37589.929158] amdgpu 0000:c5:00.0: amdgpu: GPU reset(2) succeeded!
```

This issue still happen after one month since last report?  quite disappointing.

```
 ╰──➤ $ pacman -Q |grep 'amd\|rocm\|ollama'
amd-ucode 20260309-1
amdgpu_top 0.11.3-1
hip-runtime-amd 7.2.1-2
lib32-vulkan-amdgpu-pro 25.10_2202160-1
linux-firmware-amdgpu 20260309-1
ollama 0.20.4-1
ollama-rocm 0.20.4-1
python-pytorch-rocm 2.11.0-3
python-torchaudio-rocm 2.10.0-3
rocm-cmake 7.2.1-1
rocm-core 7.2.1-2
rocm-device-libs 2:7.2.1-1
rocm-hip-libraries 7.2.1-1
rocm-hip-runtime 7.2.1-1
rocm-hip-sdk 7.2.1-1
rocm-language-runtime 7.2.1-1
rocm-llvm 2:7.2.1-1
rocm-opencl-runtime 7.2.1-1
rocm-opencl-sdk 7.2.1-1
rocm-smi-lib 7.2.0-2
rocminfo 7.2.1-2
vulkan-amdgpu-pro 25.10_2202160-1
xf86-video-amdgpu 25.0.0-1
```

```
 ╰──➤ $ uname -a
Linux mingfan 6.19.11-x64v3-xanmod1-1 #1 SMP PREEMPT_DYNAMIC Fri, 03 Apr 2026 21:56:26 +0000 x86_64 GNU/Linux
```

```
[root@mingfan procodile]# cat /proc/cmdline
root=LABEL=ArchLinux rw initrd=boot\amd-ucode.img resume=LABEL=swap zswap.enabled=0 sysrq_always_enabled=1 amdgpu.gpu_recovery=1 initrd=\boot\initramfs-linux-xanmod.im
```

---

### 评论 #20 — zw963 (2026-04-10T01:44:50Z)

```
[root@mingfan procodile]# cat /sys/kernel/debug/dri/0000\:c5\:00.0/amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 35, firmware version: 0x00000064
PFP feature version: 35, firmware version: 0x0000006a
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x0000008b
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x0000000f
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 35, firmware version: 0x00000044
IMU feature version: 0, firmware version: 0x0b012d00
SOS feature version: 0, firmware version: 0x00000000
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x00000000
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004c4900 (76.73.0)
SDMA0 feature version: 60, firmware version: 0x00000018
VCN feature version: 0, firmware version: 0x09118010
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x08005700
TOC feature version: 0, firmware version: 0x0000000b
MES_KIQ feature version: 6, firmware version: 0x00000109
MES feature version: 1, firmware version: 0x00000086
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-PHXGENERIC-001
```

@amd-nicknick 

---

### 评论 #21 — Deaththegrim (2026-05-10T10:25:04Z)


Hitting the same `MES failed to respond to msg=INVALIDATE_TLBS` class on RX 9070 XT (RDNA4, gfx1201) under sustained ComfyUI SDXL inference. The fallback-to-register-path message lands but the recovery is incomplete — subsequent VM operations on the same context still see stale TLB entries, and the failure cascades into `Not enough memory for command submission!` floods minutes later when the now-unmapped pages would have been re-resolved by the TLB invalidate.

I have a patch for `gmc_v12_0_flush_gpu_tlb` (the gfx1201 / RDNA4 path) that hardens the fallback: when the MES message times out and the code falls back to the register path, it now also explicitly waits for the `KIQ`/PSP-side acknowledgement before returning, instead of returning success on register-write completion alone. That closes the window where the kernel believed the TLB was clean but a pending invalidate from MES was still in flight.

Reproduction signature (from one of my crash logs):
```
amdgpu 0000:03:00.0: MES(1) failed to respond to msg=INVALIDATE_TLBS
amdgpu 0000:03:00.0: MES TLB invalidation failed (r=-110), falling back to register path
... (minutes later)
amdgpu 0000:03:00.0: [drm] *ERROR* Not enough memory for command submission!  (×100+, ~3.7/sec)
```

Patch and full bug report (reproduction, dmesg traces, diff context) available — happy to post the full text in a follow-up comment or attach. Same file/function exists for gfx1100/gfx1101/gfx1151 variants under `gmc_v11_0.c`; the same hardening should be straightforward to apply, but I haven't tested those.

Environment: AMD RX 9070 XT (gfx1201), Ryzen 9 9950X3D, kernel 6.17.0-1020-oem, DKMS amdgpu/6.18.4-2286447.24.04, ROCm 7.2.3.


---
