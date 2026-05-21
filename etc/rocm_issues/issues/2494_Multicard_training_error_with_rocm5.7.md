# Multicard training error with rocm5.7

> **Issue #2494**
> **状态**: closed
> **创建时间**: 2023-09-21T18:42:16Z
> **更新时间**: 2024-10-02T15:41:59Z
> **关闭时间**: 2024-09-04T18:07:20Z
> **作者**: sdli1995
> **标签**: hardware:Radeon, application:pytorch, model:transformer
> **URL**: https://github.com/ROCm/ROCm/issues/2494

## 标签

- **hardware:Radeon** (颜色: #2B113F)
- **application:pytorch** (颜色: #bfdadc)
- **model:transformer** (颜色: #f9d0c4)

## 负责人

- hongxiayang

## 描述

GPU Model: 
7900XTX

OS and other system details:
CPU:
amd epyc 7542
MotherBoard:
H12SSL-i
RAM:
8*32G 
OS:
debian12  with kernel 6.1.0.11
kernel params :
amd_iommu=off
amdgpu version:
 [amdgpu_5.7.50700-1652687.22.04_amd64.deb]


Describe your Problem Provide sufficient information to reproduce your problem. Explain why the current behavior is a concern.

When i use 2 gpu run a Transformer Model with pytorch 2.0.1 it'crash and more the graphic card are not usable else the kernel dmesg show large amount of errors  and first reboot the system cannot detect the graphics card it need reset bios and redetect

command is 
`torchrun --nnodes=1 --nproc_per_node=2 --rdzv_id=100 --rdzv_backend=c10d --rdzv_endpoint=localhost:29400 task/asr/train.py`
Output:

```
Memory access fault by GPU node-2 (Agent handle: 0x5561f711dfd0) on address 0x7fb7a0d67000. Reason: Page not present or supervisor privilege.
Memory access fault by GPU node-1 (Agent handle: 0x560b9370e950) on address 0x6efcab62f000. Reason: Page not present or supervisor privilege
```




dmesg output
```
[22340.105480] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32776, for process python3 pid 172866 thread python3 pid 172866)
[22340.105491] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00000002e4cd2000 from client 10
[22340.105496] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[22340.105499] amdgpu 0000:03:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[22340.105502] amdgpu 0000:03:00.0: amdgpu:      MORE_FAULTS: 0x1
[22340.105504] amdgpu 0000:03:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.105507] amdgpu 0000:03:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[22340.105509] amdgpu 0000:03:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.105512] amdgpu 0000:03:00.0: amdgpu:      RW: 0x0
[22340.105597] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.105601] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.105620] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00006efcab62b000 from client 10
[22340.105632] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[22340.105640] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[22340.105648] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x1
[22340.105654] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.105660] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[22340.105665] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.105671] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.105683] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.105694] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00006efcab62f000 from client 10
[22340.105702] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.105708] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.105715] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.105720] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.105726] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.105732] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.105738] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.105753] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.105763] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000e200002000 from client 10
[22340.105770] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.105776] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.105782] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.105788] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.105793] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.105799] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.105805] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.105817] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.105827] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000e300002000 from client 10
[22340.105834] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.105840] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.105846] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.105852] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.105857] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.105863] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.105869] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.105880] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.105889] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000e400002000 from client 10
[22340.105896] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.105902] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.105908] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.105914] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.105920] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.105925] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.105931] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.105945] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.105954] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000e500002000 from client 10
[22340.105961] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.105967] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.105973] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.105979] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.105985] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.105990] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.105996] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.106010] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.106019] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000e600002000 from client 10
[22340.106026] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.106032] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.106038] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.106044] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.106050] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.106055] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.106061] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.106076] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.106085] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000e700002000 from client 10
[22340.106092] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.106098] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.106104] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.106109] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.106115] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.106121] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.106127] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.106141] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32775, for process python3 pid 172865 thread python3 pid 172865)
[22340.106150] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x000000e800002000 from client 10
[22340.106157] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[22340.106163] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: CB/DB (0x0)
[22340.106169] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[22340.106175] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[22340.106180] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x0
[22340.106186] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[22340.106192] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[22340.211851] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22340.212137] amdgpu: failed to remove hardware queue from MES, doorbell=0x1216
[22340.212140] amdgpu: MES might be in unrecoverable state, issue a GPU reset
[22340.212148] amdgpu: Failed to evict queue 10
[22340.212171] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212187] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212204] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212220] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[22340.212234] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212250] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[22340.212270] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[22340.212288] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212302] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212323] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[22340.212337] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212353] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212388] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.212467] amdgpu 0000:03:00.0: amdgpu: GPU reset begin!
[22340.220197] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22340.220408] amdgpu: failed to remove hardware queue from MES, doorbell=0x1216
[22340.220411] amdgpu: MES might be in unrecoverable state, issue a GPU reset
[22340.220416] amdgpu: Failed to evict queue 10
[22340.220424] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220438] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220451] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220464] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 5, simd_id 0, wgp_id 0
[22340.220477] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220490] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 4, simd_id 0, wgp_id 0
[22340.220504] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220518] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220532] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220555] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 5, simd_id 0, wgp_id 0
[22340.220568] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 6, simd_id 0, wgp_id 0
[22340.220581] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220605] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220617] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220630] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220643] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220657] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 1, simd_id 0, wgp_id 0
[22340.220670] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 5, simd_id 0, wgp_id 0
[22340.220683] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220696] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220708] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220721] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 6, simd_id 0, wgp_id 0
[22340.220735] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 6, simd_id 0, wgp_id 0
[22340.220748] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220760] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220773] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220786] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220798] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220813] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 4, simd_id 0, wgp_id 0
[22340.220825] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220838] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 5, simd_id 0, wgp_id 0
[22340.220851] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220863] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 5, simd_id 0, wgp_id 0
[22340.220876] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220890] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.220903] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220916] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[22340.220928] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 2, simd_id 0, wgp_id 0
[22340.220941] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220954] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 5, simd_id 0, wgp_id 0
[22340.220978] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 3, simd_id 0, wgp_id 0
[22340.220991] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 1, priv 1, wave_id 4, simd_id 0, wgp_id 0
[22340.221003] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 5, simd_id 0, wgp_id 0
[22340.221016] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 4, simd_id 0, wgp_id 0
[22340.221029] amdgpu: sq_intr: error, detail 0x00000000, type 1, sh 0, priv 1, wave_id 7, simd_id 0, wgp_id 0
[22340.221061] amdgpu 0000:83:00.0: amdgpu: GPU reset begin!
[22341.235735] amdgpu 0000:83:00.0: amdgpu: IP block:gfx_v11_0 is hung!
[22341.235795] amdgpu 0000:03:00.0: amdgpu: IP block:gfx_v11_0 is hung!
[22342.259763] [drm:sdma_v6_0_ring_test_ib [amdgpu]] *ERROR* amdgpu: IB test timed out
[22342.260203] amdgpu 0000:03:00.0: amdgpu: IP block:sdma_v6_0 is hung!
[22342.263690] [drm:sdma_v6_0_ring_test_ib [amdgpu]] *ERROR* amdgpu: IB test timed out
[22342.264010] amdgpu 0000:83:00.0: amdgpu: IP block:sdma_v6_0 is hung!
[22342.633518] Failed to wait all pipes clean
[22342.633568] amdgpu 0000:83:00.0: amdgpu: soft reset failed, will fallback to full reset!
[22342.675604] Failed to wait all pipes clean
[22342.675612] amdgpu 0000:03:00.0: amdgpu: soft reset failed, will fallback to full reset!
[22342.834411] amdgpu 0000:83:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:59 param:0x00000000 message:DFCstateControl?
[22342.834418] amdgpu 0000:83:00.0: amdgpu: [SetDfCstate] failed!
[22342.834421] amdgpu 0000:83:00.0: amdgpu: Failed to disallow df cstate
[22342.834432] [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=5
[22342.877202] amdgpu 0000:03:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:59 param:0x00000000 message:DFCstateControl?
[22342.877209] amdgpu 0000:03:00.0: amdgpu: [SetDfCstate] failed!
[22342.877212] amdgpu 0000:03:00.0: amdgpu: Failed to disallow df cstate
[22342.877224] [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=5
[22342.964952] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22342.965137] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.007776] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.007966] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.075161] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.075338] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.117935] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.118111] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.185372] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.185547] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.228075] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.228250] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.295587] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.295766] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.338200] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.338375] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.405795] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.405969] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.448344] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.448517] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.515985] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.516159] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.558464] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.558637] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.626170] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.626342] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.668606] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.668781] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.736379] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.736557] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.778715] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.778893] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.846554] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.846728] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22343.888824] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[22343.888997] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[22344.249704] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[22344.249947] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 000000008f2b9fb6; ring_buffer_end = 000000006e89c2b3; write_frame = 00000000d8de01da
[22344.250121] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
[22344.250291] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate ras ta
[22344.250459] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[22344.251655] amdgpu 0000:83:00.0: amdgpu: MODE1 reset
[22344.251660] amdgpu 0000:83:00.0: amdgpu: GPU mode1 reset
[22344.252662] amdgpu 0000:83:00.0: amdgpu: GPU smu mode1 reset
[22344.252666] amdgpu 0000:83:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:47 param:0x00000000 message:Mode1Reset?
[22344.252670] amdgpu 0000:83:00.0: amdgpu: GPU mode1 reset failed
[22344.292232] [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
[22344.292471] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 000000008d2bdb3a; ring_buffer_end = 00000000ff4eb044; write_frame = 000000005abb7a30
[22344.292645] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
[22344.292814] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate ras ta
[22344.292984] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[22344.294178] amdgpu 0000:03:00.0: amdgpu: MODE1 reset
[22344.294183] amdgpu 0000:03:00.0: amdgpu: GPU mode1 reset
[22344.295186] amdgpu 0000:03:00.0: amdgpu: GPU smu mode1 reset
[22344.295190] amdgpu 0000:03:00.0: amdgpu: SMU: response:0xFFFFFFFF for index:47 param:0x00000000 message:Mode1Reset?
[22344.295194] amdgpu 0000:03:00.0: amdgpu: GPU mode1 reset failed
[22344.456139] amdgpu 0000:83:00.0: amdgpu: ASIC reset failed with error, -121 for drm dev, 0000:83:00.0
[22344.498996] amdgpu 0000:03:00.0: amdgpu: ASIC reset failed with error, -121 for drm dev, 0000:03:00.0
[22348.746284] amdgpu 0000:83:00.0: amdgpu: GPU reset succeeded, trying to resume
[22348.746435] [drm] PCIE GART of 512M enabled (table at 0x00000085FEB00000).
[22348.746525] [drm] VRAM is lost due to GPU reset!
[22348.746528] [drm] PSP is resuming...
[22348.790706] amdgpu 0000:03:00.0: amdgpu: GPU reset succeeded, trying to resume
[22348.790900] [drm] PCIE GART of 512M enabled (table at 0x00000085FEB00000).
[22348.791038] [drm] VRAM is lost due to GPU reset!
[22348.791042] [drm] PSP is resuming...
[22348.967420] [drm:psp_hw_start [amdgpu]] *ERROR* PSP create ring failed!
[22348.967631] [drm:psp_resume [amdgpu]] *ERROR* PSP resume failed
[22348.967851] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[22348.999763] [drm:psp_hw_start [amdgpu]] *ERROR* PSP create ring failed!
[22349.000013] [drm:psp_resume [amdgpu]] *ERROR* PSP resume failed
[22349.000293] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[22383.942807] amdgpu: Failed to remove queue 9
[22383.942814] amdgpu: Failed to remove queue 8
[22383.942817] amdgpu: Failed to remove queue 7
[22383.942819] amdgpu: Failed to remove queue 6
[22383.942821] amdgpu: Failed to remove queue 5
[22383.942823] amdgpu: Failed to remove queue 4
[22383.942825] amdgpu: Failed to remove queue 3
[22383.942827] amdgpu: Failed to remove queue 2
[22383.942829] amdgpu: Failed to remove queue 1
[22383.942830] amdgpu: Failed to remove queue 0
[22387.880405] amdgpu: Failed to remove queue 9
[22387.880412] amdgpu: Failed to remove queue 8
[22387.880415] amdgpu: Failed to remove queue 7
[22387.880417] amdgpu: Failed to remove queue 6
[22387.880419] amdgpu: Failed to remove queue 5
[22387.880421] amdgpu: Failed to remove queue 4
[22387.880423] amdgpu: Failed to remove queue 3
[22387.880425] amdgpu: Failed to remove queue 2
[22387.880427] amdgpu: Failed to remove queue 1
[22387.880429] amdgpu: Failed to remove queue 0
[22475.343793] INFO: task kworker/u128:3:153651 blocked for more than 120 seconds.
[22475.343810]       Tainted: P           OE      6.1.0-11-amd64 #1 Debian 6.1.38-4
[22475.343819] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[22475.343824] task:kworker/u128:3  state:D stack:0     pid:153651 ppid:2      flags:0x00004000
[22475.343840] Workqueue: amdgpu-reset-dev amdgpu_amdkfd_reset_work [amdgpu]
[22475.344281] Call Trace:
[22475.344287]  <TASK>
[22475.344298]  __schedule+0x351/0xa20
[22475.344318]  schedule+0x5d/0xe0
[22475.344327]  schedule_timeout+0x118/0x150
[22475.344343]  dma_fence_default_wait+0x1a5/0x260
[22475.344356]  ? __bpf_trace_dma_fence+0x10/0x10
[22475.344369]  dma_fence_wait_timeout+0x108/0x130
[22475.344381]  amdgpu_sync_wait+0x75/0x110 [amdgpu]
[22475.344819]  amdgpu_mes_ctx_map_meta_data+0x1f0/0x2c0 [amdgpu]
[22475.345299]  amdgpu_mes_self_test+0x102/0x480 [amdgpu]
[22475.345701]  ? amdgpu_device_fw_loading+0x13e/0x150 [amdgpu]
[22475.346068]  ? __x86_return_thunk+0x5/0x6
[22475.346081]  ? __drm_err+0x7b/0xa0 [drm]
[22475.346162]  amdgpu_device_gpu_recover.cold+0x47a/0xb3f [amdgpu]
[22475.346672]  ? __ret+0x40/0x7e
[22475.346689]  amdgpu_amdkfd_reset_work+0x5e/0x80 [amdgpu]
[22475.347134]  process_one_work+0x1c7/0x380
[22475.347152]  worker_thread+0x4d/0x380
[22475.347165]  ? rescuer_thread+0x3a0/0x3a0
[22475.347174]  kthread+0xe9/0x110
[22475.347184]  ? kthread_complete_and_exit+0x20/0x20
[22475.347195]  ret_from_fork+0x22/0x30
[22475.347218]  </TASK>
[22475.347224] INFO: task kworker/u128:2:167646 blocked for more than 120 seconds.
[22475.347230]       Tainted: P           OE      6.1.0-11-amd64 #1 Debian 6.1.38-4
[22475.347236] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[22475.347240] task:kworker/u128:2  state:D stack:0     pid:167646 ppid:2      flags:0x00004000
[22475.347252] Workqueue: amdgpu-reset-dev amdgpu_amdkfd_reset_work [amdgpu]
[22475.347702] Call Trace:
[22475.347708]  <TASK>
[22475.347717]  __schedule+0x351/0xa20
[22475.347734]  schedule+0x5d/0xe0
[22475.347745]  schedule_timeout+0x118/0x150
[22475.347761]  dma_fence_default_wait+0x1a5/0x260
[22475.347774]  ? __bpf_trace_dma_fence+0x10/0x10
[22475.347789]  dma_fence_wait_timeout+0x108/0x130
[22475.347802]  amdgpu_sync_wait+0x75/0x110 [amdgpu]
[22475.348234]  amdgpu_mes_ctx_map_meta_data+0x1f0/0x2c0 [amdgpu]
[22475.348665]  amdgpu_mes_self_test+0x102/0x480 [amdgpu]
[22475.349062]  ? amdgpu_device_fw_loading+0x13e/0x150 [amdgpu]
[22475.349432]  ? __x86_return_thunk+0x5/0x6
[22475.349440]  ? __drm_err+0x7b/0xa0 [drm]
[22475.349519]  amdgpu_device_gpu_recover.cold+0x47a/0xb3f [amdgpu]
[22475.350052]  amdgpu_amdkfd_reset_work+0x5e/0x80 [amdgpu]
[22475.350474]  process_one_work+0x1c7/0x380
[22475.350489]  worker_thread+0x4d/0x380
[22475.350501]  ? rescuer_thread+0x3a0/0x3a0
[22475.350510]  kthread+0xe9/0x110
[22475.350518]  ? kthread_complete_and_exit+0x20/0x20
[22475.350530]  ret_from_fork+0x22/0x30
[22475.350552]  </TASK>
```


---

## 评论 (24 条)

### 评论 #1 — sdli1995 (2023-09-21T19:04:53Z)

RCCL seems works well  run the test is correct
```
./build/all_reduce_perf -g 2 -b 8m -e 128m -f 2
# nThreads: 1 nGpus: 2 nRanks: 1 minBytes: 8388608 maxBytes: 134217728 step: 2(factor) warmupIters: 5 iters: 20 validation: 1
#
# Using devices
#   Rank  0 Pid     46 on astrali-SuperServer device  0 [0000:83:00.0] Radeon RX 7900 XTX
#   Rank  1 Pid     46 on astrali-SuperServer device  1 [0000:03:00.0] Radeon RX 7900 XTX
#
#                                                       out-of-place                       in-place
#       size         count      type   redop     time   algbw   busbw  error     time   algbw   busbw  error
#        (B)    (elements)                       (us)  (GB/s)  (GB/s)            (us)  (GB/s)  (GB/s)
     8388608       2097152     float     sum    523.1   16.04   16.04  0e+00    552.5   15.18   15.18  0e+00
    16777216       4194304     float     sum    903.8   18.56   18.56  0e+00    869.6   19.29   19.29  0e+00
    33554432       8388608     float     sum   1719.5   19.51   19.51  0e+00   1728.2   19.42   19.42  0e+00
    67108864      16777216     float     sum   3292.1   20.38   20.38  0e+00   3307.2   20.29   20.29  0e+00
   134217728      33554432     float     sum   6439.3   20.84   20.84  0e+00   5543.4   24.21   24.21  0e+00
# Errors with asterisks indicate errors that have exceeded the maximum threshold.
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 19.3738
```


---

### 评论 #2 — hongxiayang (2023-10-02T21:15:07Z)

(1) Can you provide steps that we can reproduce?
(2) is the code working for single gpu?
(3) Have the same code worked on previous versions ?

---

### 评论 #3 — sdli1995 (2023-10-06T05:29:21Z)

> (1) Can you provide steps that we can reproduce? (2) is the code working for single gpu? (3) Have the same code worked on previous versions ?

for 1) after i remove kernel params : amd_iommu=off it's fixed casually，it‘s appear again after i set DDP gradient_view_as_buckect and cannot go back to the right behavior
for 2) it's works well 
for 3) same as rocm5.6 or 5.6.1

---

### 评论 #4 — sdli1995 (2023-10-06T05:35:00Z)

> (1) Can you provide steps that we can reproduce? (2) is the code working for single gpu? (3) Have the same code worked on previous versions ?

here is tmpl dockerfile

```
#
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
# Bring in changes from outside container to 
WORKDIR /workspace
# Change source.list if orgin source is slow
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt install -y python3 python3-pip curl vim build-essential git automake patchelf sudo apt-utils cmake bash-completion \
                   libpython3-dev libpng-dev libjpeg-dev \
                   libsndfile1 libzmq3-dev 
#5.6
# RUN curl -O https://repo.radeon.com/amdgpu-install/5.6.1/ubuntu/jammy/amdgpu-install_5.6.50601-1_all.deb\
#             && dpkg -i amdgpu-install_5.6.50601-1_all.deb\
#             && amdgpu-install --usecase=hiplibsdk,rocm --no-dkms --no-32 -y \
#             && apt clean && rm amdgpu-install_5.6.50601-1_all.deb

#5.7
RUN curl -O https://repo.radeon.com/amdgpu-install/5.7/ubuntu/jammy/amdgpu-install_5.7.50700-1_all.deb\
            && dpkg -i amdgpu-install_5.7.50700-1_all.deb\
            && amdgpu-install --usecase=hiplibsdk,rocm --no-dkms --no-32 -y \
            && apt clean && rm amdgpu-install_5.7.50700-1_all.deb


RUN echo "export PATH=/opt/rocm/bin:/opt/rocm/opencl/bin:$PATH" >> /etc/bash.bashrc
RUN echo "export HSA_FORCE_FINE_GRAIN_PCIE=1" >> /etc/bash.bashrc
RUN echo "export HSA_OVERRIDE_GFX_VERSION=11.0.0" >> /etc/bash.bashrc
RUN echo "LANG=C" >> /etc/bash.bashrc
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 100
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 100
RUN groupadd -g 105 render
RUN useradd -m  -s /bin/bash work
RUN usermod -aG sudo work && echo "work ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/work
RUN chmod 0440 /etc/sudoers.d/work
USER work:work
RUN sudo apt remove -y apt-utils
RUN DEBIAN_FRONTENDs=noninteractive sudo apt install rocm-bandwidth-test
WORKDIR /home/work
## 5.6 install torch
# RUN curl -O https://github.com/evshiron/rocm_lab/releases/download/rocm-5.6-builds/torch-2.1.0+gitf353d17-cp310-cp310-linux_x86_64.whl
# RUN sudo pip3 install torch-2.1.0+gitf353d17-cp310-cp310-linux_x86_64.whl
# RUN curl -O https://github.com/evshiron/rocm_lab/releases/download/rocm-5.6-builds/torchvision-0.16.0+2d4484f-cp310-cp310-linux_x86_64.whl
# RUN sudo pip3 install torchvision-0.16.0+2d4484f-cp310-cp310-linux_x86_64.whl

#5.7 install torch
RUN sudo pip3 install torch==2.0.1 torchvision==0.15.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-5.7/
```


here is test code 

```
import sys
import os
import torch
import time
import logging
import argparse
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.nn import Conv2d,ReLU,MaxPool2d,Linear,CrossEntropyLoss
from torch.optim import SGD
import torchvision
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(filename)s:%(lineno)d: %(message)s',
                    datefmt='[%y-%m-%d %H:%M:%S]')

def main(rank,worldsize):
    ctx = 'cuda:%d'%rank
    net = getattr(torchvision.models, 'vgg16')().to(ctx)
    net = DDP(net,device_ids=[ctx])
    loss_func = CrossEntropyLoss()
    optim = SGD(net.parameters(),lr=1e-4)
    for i in range(100):
        optim.zero_grad()
        x = torch.randn(64,3,256,256).to(ctx)
        y_hat = torch.randint(0,100,size=(64,)).to(ctx)
        y = net(x)
        l = loss_func(y,y_hat)
        print(rank,l.detach().cpu())
        l.backward()
        optim.step()
        

if __name__ == "__main__":


    worldsize = int(sys.argv[1])
    dist.init_process_group("nccl")
    rank = dist.get_rank()
    dist_worldsize = dist.get_world_size()
    if dist_worldsize != worldsize:
        print("Error used device not equal to config")
        exit(255)
    main(rank,worldsize)

```

command run is 
`torchrun --standalone --nnodes=1 --nproc-per-node=2 test.py 2`

---

### 评论 #5 — gel-crabs (2023-10-16T00:45:38Z)

I am plagued by these errors using PyTorch with Stable Diffusion on my RX 7800 XT, including on 5.7.1. It will work fine for a bit, then my dmesg logs get spammed with the sq_intr errors shown above and my GPU resets.

Is this a firmware issue? If not, is it likely to be fixed in ROCm 6.0?

---

### 评论 #6 — hongxiayang (2023-10-16T16:15:03Z)

I was able to run the test.py successfully using rocm's  pytorch-nightly docker image, but failed on other docker images including @sdli1995 's docker file. Will need to investigate further.

---

### 评论 #7 — hongxiayang (2023-10-16T18:16:34Z)

@sdli1995  Have you tested with pytorch 2.1 with rocm 5.7? 

Though I don't have access to a 7900XTX node at this time, I failed to run your code on a MI250 with your code/dockerfile, and also, I failed to run the code on older version of pytorch/rocm combinations. However, I am able to run your test code successfully on pytorch 2.1 with rocm 5.7, using rocm/pytorch:latest docker image on MI210.

Can you use ```rocm/pytorch:latest``` docker image and let us know? Thanks.

---

### 评论 #8 — sdli1995 (2023-10-17T06:30:44Z)

> @sdli1995 Have you tested with pytorch 2.1 with rocm 5.7?
> 
> Though I don't have access to a 7900XTX node at this time, I failed to run your code on a MI250 with your code/dockerfile, and also, I failed to run the code on older version of pytorch/rocm combinations. However, I am able to run your test code successfully on pytorch 2.1 with rocm 5.7, using rocm/pytorch:latest docker image on MI210.
> 
> Can you use `rocm/pytorch:latest` docker image and let us know? Thanks.

I test several times test.py in rocm/pytorch:latest docker image it's work correct in 7900XTX nodes 


---

### 评论 #9 — sdli1995 (2023-10-17T11:01:37Z)

> @sdli1995 Have you tested with pytorch 2.1 with rocm 5.7?
> 
> Though I don't have access to a 7900XTX node at this time, I failed to run your code on a MI250 with your code/dockerfile, and also, I failed to run the code on older version of pytorch/rocm combinations. However, I am able to run your test code successfully on pytorch 2.1 with rocm 5.7, using rocm/pytorch:latest docker image on MI210.
> 
> Can you use `rocm/pytorch:latest` docker image and let us know? Thanks.

@hongxiayang Additionally，I try rocm-5.7.1 and 5.7.1 amdgpu-dkms driver it's works well utill now . Weird...


---

### 评论 #10 — hongxiayang (2023-10-17T13:54:40Z)

@sdli1995 Feel free to close this issue since it works now.

---

### 评论 #11 — sdli1995 (2024-01-09T07:11:25Z)

> @sdli1995 Feel free to close this issue since it works now.
 
in ROCM 6.0 it‘s apears agin 

[ 2746.403998] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:157 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
[ 2746.404001] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007fff01252000 from client 10
[ 2746.404003] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000B3A
[ 2746.404004] amdgpu 0000:03:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[ 2746.404006] amdgpu 0000:03:00.0: amdgpu:      MORE_FAULTS: 0x0
[ 2746.404008] amdgpu 0000:03:00.0: amdgpu:      WALKER_ERROR: 0x5
[ 2746.404009] amdgpu 0000:03:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[ 2746.404011] amdgpu 0000:03:00.0: amdgpu:      MAPPING_ERROR: 0x1
[ 2746.404012] amdgpu 0000:03:00.0: amdgpu:      RW: 0x0



---

### 评论 #12 — ppanchad-amd (2024-05-14T17:41:22Z)

@sdli1995 Can you please test with latest ROCm 6.1.1 to see if it happens with this build? Thanks!

---

### 评论 #13 — codinggosu (2024-07-09T12:04:59Z)

i'm experiencing something similar on rocm-6.1.2 as well. 

the funny thing for me is that in some model architectures (i'm training a deep learning model) it works, in others it fails. 


---

### 评论 #14 — kentrussell (2024-07-09T12:59:20Z)

@codinggosu can you paste your VM fault in here so we can compare? The 2 VM faults above have different causes (vmid0 vs vmid8) so it could just be the application doing something wrong (like reading past the end of an array, for example). 

---

### 评论 #15 — codinggosu (2024-07-10T02:29:57Z)

is there a format / specific line of log or any requirement for how to share the fault?
i'm sharing the error output from the training script and some snippets of dmesg for now. tell me if you need more

also, for future reference when an error like this happens again, do you have some tips about:
1. determining whether it's an application error or not
2. if it is an application error, finding out exactly what part of the application is causing this error

error from training script:
```
[2024-07-10 11:18:53,785] [INFO] [logging.py:96:log_dist] [Rank 0] step=1, skipped=0, lr=[1.5e-07, 1.5e-07], mom=[(0.9, 0.95), (0.9,0.95)]
Memory access fault by GPU node-2 (Agent handle: 0x560f8742a5e0) on address 0x150c73c10000. Reason: Unknown.                   
Memory access fault by GPU node-3 (Agent handle: 0x5600c8ba8db0) on address 0x14d212228000. Reason: Unknown.                   
Memory access fault by GPU node-4 (Agent handle: 0x55af20ea65c0) on address 0x150eb56e8000. Reason: Unknown.
```

dmesge (other repeating lines of output exist)
```
[Wed Jul 10 11:18:55 2024] amdgpu 0000:26:00.0: amdgpu: VM_L2_PROTECTION_FAULT_STATUS:0x00301031
[Wed Jul 10 11:18:55 2024] amdgpu 0000:26:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
[Wed Jul 10 11:18:55 2024] amdgpu 0000:a6:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32792, for process python3 pid 1134315 thread python3 pid 1134315)
[Wed Jul 10 11:18:55 2024] amdgpu 0000:26:00.0: amdgpu:          MORE_FAULTS: 0x1
[Wed Jul 10 11:18:55 2024] amdgpu 0000:26:00.0: amdgpu:          WALKER_ERROR: 0x0
[Wed Jul 10 11:18:55 2024] amdgpu 0000:a6:00.0: amdgpu:   in page starting at address 0x0000149bd0608000 from IH client 0x1b (UTCL2)
[Wed Jul 10 11:18:55 2024] amdgpu 0000:26:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
[Wed Jul 10 11:18:55 2024] amdgpu 0000:a6:00.0: amdgpu:   cookie node_id 2 fault from die AID0.XCD1
[Wed Jul 10 11:18:55 2024] amdgpu 0000:26:00.0: amdgpu:          MAPPING_ERROR: 0x0
[Wed Jul 10 11:18:55 2024] amdgpu 0000:85:00.0: amdgpu: [gfxhub0] retry page fault (src_id:0 ring:0 vmid:3 pasid:32790, for process python3 pid 1134314 thread python3 pid 1134314)
[Wed Jul 10 11:18:55 2024] amdgpu 0000:26:00.0: amdgpu:          RW: 0x0
```


To give you more info about our setup, we are using 2 nodes with 8xMI300x with 8x NICs each
this error starts to appear when i increase the num layers of my llm (ex: the error doesn't appear when the num layers is below 5, but appears for cases when num layers is 6, 7, 8, and so on)

i'm using megatron-deepspeed and utilizing tensor and pipeline parallelism. 


---

### 评论 #16 — codinggosu (2024-07-10T07:59:02Z)

i tried running it with gdb and printed the backtrace after the error is thrown. 
this is the backtrace. 


```Thread 67 "pt_main_thread" hit Catchpoint 1 (exception thrown), 0x00007fff5ed5f4a1 in __cxa_throw () from /lib/x86_64-linux-gnu/libstdc++.so.6
(gdb) backtrace
#0  0x00007fff5ed5f4a1 in __cxa_throw () from /lib/x86_64-linux-gnu/libstdc++.so.6
#1  0x00007fffe3288451 in void c10d::tcputil::recvBytes<c10d::detail::QueryType>(int, c10d::detail::QueryType*, unsigned long)
    () from /somepath/venv/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#2  0x00007fffe328766d in c10d::detail::TCPStoreMasterDaemon::query(int) ()
   from /somepath/venv/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#3  0x00007fffe32878ad in c10d::detail::TCPStoreMasterDaemon::queryFds(std::vector<pollfd, std::allocator<pollfd> >&) ()
   from /somepath/venv/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#4  0x00007fffe3287c43 in c10d::detail::TCPStoreMasterDaemon::run() ()
   from /somepath/venv/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#5  0x00007ffff734e220 in execute_native_thread_routine ()
   from /somepath/venv/lib/python3.10/site-packages/torch/lib/libtorch.so
#6  0x00007ffff7ce4ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#7  0x00007ffff7d76850 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
```




---

### 评论 #17 — harkgill-amd (2024-08-28T16:03:30Z)

Hi @sdli1995, I was able to successfully run the test program provided using the latest `rocm/pytorch` image. This image contains the ROCm 6.2.0 release with PyTorch 2.4. Could you please give this a try?

@codinggosu, apologies for the lack of response, could you also please confirm if the VM faults are seen on ROCm 6.2.0?

---

### 评论 #18 — codinggosu (2024-08-29T09:28:23Z)

hey, thanks for the response. I was able to solve this issue by using a different optimizer. the issue was with apex's optimizer and after switching to a different implementation, we were able to resolve the issue. 



---

### 评论 #19 — sdli1995 (2024-08-30T00:21:24Z)

> Hi @sdli1995, I was able to successfully run the test program provided using the latest `rocm/pytorch` image. This image contains the ROCm 6.2.0 release with PyTorch 2.4. Could you please give this a try?
> 
> @codinggosu, apologies for the lack of response, could you also please confirm if the VM faults are seen on ROCm 6.2.0?

it's works and stable after i running a job yesterday until now which used 2 GPUS , but when the dmesg show error in this case it's use 4 GPUS , i cannot check it with 4 gpus  due to the other gpus was used to other usage

---

### 评论 #20 — harkgill-amd (2024-09-04T18:07:20Z)

Good to see that it is working in your current environment as well. I wasn't able to reproduce the page faults in both a 4 and 6 GPU setup. In both experiments, the test code provided ran smoothly with the loss being printed across all GPUs. 

I will close out the ticket. if you do encounter these errors again, please leave a comment and I will re-open the issue. Thanks!

---

### 评论 #21 — extraymond (2024-10-02T11:17:02Z)

Not sure if this is related, but my pytorch inference setup faced the same issue, the issue is hard to reproduce but I think I'm starting to see a pattern

system setup:
- os: ubuntu24.04 kernel 6.8
- rocm: 6.2.2
- torch 2.1.0

steps to reproduce:
- my main task involves segmenting videos into various chunks
- each chunk will call multiple torch modules and some pure cpu or io based operation in it's pipeline
- since vram is limited, I have a semaphore limit the max number of concurrent sub-tasks at any moment
- for smaller videos, where the concurrent limit is not very high, or the pipeline didn't create too many subtasks, the problem seems to be invisible
- for longer videos with richer content, seems like the concurrent torch modules are fighting something to access the gpu

> the same thing didn't happen on another setup with nvidua gpu

---

### 评论 #22 — harkgill-amd (2024-10-02T15:18:43Z)

@extraymond, which GPUs are you using in your multicard setup? Would it be possible for you to share your code or a minimal reproducible example for us to further investigate?

---

### 评论 #23 — extraymond (2024-10-02T15:25:12Z)

> @extraymond, which GPUs are you using in your multicard setup? Would it be possible for you to share your code or a minimal reproducible example for us to further investigate?

Sorry, I'm not using multicard setup, I'm with a single 6900 XT. 
It seems to me that the problem seems more relatable to how the kernel? attempts to allocate request for hardware from user code task submissions.

This error doesn't seems to trigger as much in some combination of rocm setup. I was having less error with ubuntu 22.04 kernel prior to 6.5 with rocm5.6.

---

### 评论 #24 — harkgill-amd (2024-10-02T15:41:06Z)

Ah I see, it will be hard to debug this without a sample reproducer. I would suggest creating a new issue once you're able to pinpoint a faulty configuration and provide a small sample so we can take a deeper dive into what's happening under the hood. The ouput of dmesg after the error would also be great as well.

---
