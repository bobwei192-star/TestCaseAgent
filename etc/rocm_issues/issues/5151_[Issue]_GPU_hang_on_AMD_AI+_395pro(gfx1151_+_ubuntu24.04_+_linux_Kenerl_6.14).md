# [Issue]: GPU hang on AMD AI+ 395pro(gfx1151 + ubuntu24.04 + linux Kenerl 6.14)

> **Issue #5151**
> **状态**: open
> **创建时间**: 2025-08-05T04:02:03Z
> **更新时间**: 2025-11-08T17:39:08Z
> **作者**: deific
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5151

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

OS:
NAME="Ubuntu"
VERSION="24.04.2 LTS (Noble Numbat)"
CPU: 
model name      : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
GPU:
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Name:                    gfx1151                            
  Marketing Name:          AMD Radeon Graphics                
      Name:                    amdgcn-amd-amdhsa--gfx1151         
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
  Name:                    aie2                               
  Marketing Name:          AIE-ML  

VRAM=64G by BIOS.

Using ollama to run the large model qwen3:30b, and continuously calling to keep the large model running, after running for a period of time, it was found that the GPU would reset. The GPU reset was not fixed. Kernel log:
```
Aug 05 08:56:22.546687 my-server kernel: amdgpu: Freeing queue vital buffer 0x78d1fa200000, queue evicted
Aug 05 08:56:22.546749 my-server kernel: amdgpu: Freeing queue vital buffer 0x78d206000000, queue evicted
Aug 05 08:56:22.546848 my-server kernel: amdgpu: Freeing queue vital buffer 0x78d37c200000, queue evicted
Aug 05 08:56:22.546867 my-server kernel: amdgpu: Freeing queue vital buffer 0x78d37e200000, queue evicted
Aug 05 08:56:22.546876 my-server kernel: amdgpu: Freeing queue vital buffer 0x78d384400000, queue evicted
Aug 05 08:56:24.669800 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Aug 05 08:56:24.670058 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1806
Aug 05 08:56:24.670111 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Aug 05 08:56:24.670186 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 4
Aug 05 08:56:24.670225 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!
Aug 05 08:56:24.670267 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 2
Aug 05 08:56:24.670660 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
Aug 05 08:56:24.670702 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 0
Aug 05 08:56:24.671654 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
Aug 05 08:56:24.671716 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
Aug 05 08:56:24.677663 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bd139400000, queue evicted
Aug 05 08:56:24.677688 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bd200200000, queue evicted
Aug 05 08:56:24.677696 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bd201600000, queue evicted
Aug 05 08:56:24.677704 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bd202400000, queue evicted
Aug 05 08:56:24.677712 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bd203200000, queue evicted
Aug 05 08:56:25.714779 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Aug 05 08:56:25.714945 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:25.715008 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Aug 05 08:56:25.715060 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Aug 05 08:56:25.715105 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MORE_FAULTS: 0x1
Aug 05 08:56:25.715142 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          WALKER_ERROR: 0x1
Aug 05 08:56:25.715180 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Aug 05 08:56:25.715222 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MAPPING_ERROR: 0x1
Aug 05 08:56:25.715265 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          RW: 0x1
Aug 05 08:56:25.715302 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Aug 05 08:56:25.715341 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:25.715378 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Aug 05 08:56:25.715413 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:25.715448 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Aug 05 08:56:25.715484 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:25.715519 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Aug 05 08:56:25.715554 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:25.715589 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Aug 05 08:56:25.715625 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:25.715668 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Aug 05 08:56:25.715703 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:25.715737 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Aug 05 08:56:25.715771 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:27.428131 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Aug 05 08:56:27.428631 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
Aug 05 08:56:27.714174 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
Aug 05 08:56:27.714699 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:27.714868 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Aug 05 08:56:27.715001 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Aug 05 08:56:27.715126 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MORE_FAULTS: 0x1
Aug 05 08:56:27.715248 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          WALKER_ERROR: 0x1
Aug 05 08:56:27.715368 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Aug 05 08:56:27.715488 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MAPPING_ERROR: 0x1
Aug 05 08:56:27.715606 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          RW: 0x1
Aug 05 08:56:27.715749 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
Aug 05 08:56:27.715870 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Aug 05 08:56:27.715987 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
Aug 05 08:56:27.747675 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
Aug 05 08:56:27.748110 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
Aug 05 08:56:27.754663 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
Aug 05 08:56:27.797668 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 05 08:56:27.797822 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Aug 05 08:56:27.797869 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Aug 05 08:56:27.797912 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Aug 05 08:56:27.797950 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Aug 05 08:56:27.797986 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Aug 05 08:56:27.798022 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Aug 05 08:56:27.798057 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Aug 05 08:56:27.798092 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Aug 05 08:56:27.798127 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Aug 05 08:56:27.798164 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Aug 05 08:56:27.798202 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Aug 05 08:56:27.798236 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Aug 05 08:56:27.798271 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Aug 05 08:56:27.798311 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Aug 05 08:56:27.798347 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Aug 05 08:56:27.838664 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset(6) succeeded!
Aug 05 09:01:42.326886 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.327198 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.327313 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58f7f000 from client 10
Aug 05 09:01:42.327410 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00901031
Aug 05 09:01:42.327516 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
Aug 05 09:01:42.327610 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MORE_FAULTS: 0x1
Aug 05 09:01:42.327720 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          WALKER_ERROR: 0x0
Aug 05 09:01:42.327812 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Aug 05 09:01:42.327904 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MAPPING_ERROR: 0x0
Aug 05 09:01:42.327995 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          RW: 0x0
Aug 05 09:01:42.328084 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.328173 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.328262 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58fda000 from client 10
Aug 05 09:01:42.328354 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00901030
Aug 05 09:01:42.328447 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          Faulty UTCL2 client ID: TCP (0x8)
Aug 05 09:01:42.328535 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MORE_FAULTS: 0x0
Aug 05 09:01:42.328629 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          WALKER_ERROR: 0x0
Aug 05 09:01:42.328723 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Aug 05 09:01:42.328813 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          MAPPING_ERROR: 0x0
Aug 05 09:01:42.328900 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:          RW: 0x0
Aug 05 09:01:42.328988 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.329075 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.329163 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58fad000 from client 10
Aug 05 09:01:42.329253 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.329341 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.329426 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58f67000 from client 10
Aug 05 09:01:42.329519 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.329605 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.329698 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58f62000 from client 10
Aug 05 09:01:42.330217 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.330394 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.330553 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58f76000 from client 10
Aug 05 09:01:42.330713 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.330841 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.330959 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58fd1000 from client 10
Aug 05 09:01:42.331078 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.331192 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.331307 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58fc2000 from client 10
Aug 05 09:01:42.331426 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.331541 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.331709 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58fc7000 from client 10
Aug 05 09:01:42.331876 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32771)
Aug 05 09:01:42.332038 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:  in process ollama pid 3678233 thread ollama pid 3678241)
Aug 05 09:01:42.332206 my-server kernel: amdgpu 0000:c5:00.0: amdgpu:   in page starting at address 0x00007f3a58fbd000 from client 10
Aug 05 09:01:44.313823 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Aug 05 09:01:44.314116 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1804
Aug 05 09:01:44.314183 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Aug 05 09:01:44.314238 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 2
Aug 05 09:01:44.314280 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!
Aug 05 09:01:44.314318 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 0
Aug 05 09:01:44.315668 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 6
Aug 05 09:01:44.315995 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 5
Aug 05 09:01:44.316129 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 4
Aug 05 09:01:44.316351 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 3
Aug 05 09:01:44.316729 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 2
Aug 05 09:01:44.316808 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
Aug 05 09:01:44.316851 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 0
Aug 05 09:01:44.316893 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 6, simd_id 0, wgp_id 0
Aug 05 09:01:44.316901 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 8, simd_id 0, wgp_id 0
Aug 05 09:01:44.316907 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 6, simd_id 0, wgp_id 0
Aug 05 09:01:44.316922 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 9, simd_id 0, wgp_id 0
Aug 05 09:01:44.316928 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
Aug 05 09:01:44.316966 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 9, simd_id 0, wgp_id 0
Aug 05 09:01:44.316975 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 8, simd_id 0, wgp_id 0
Aug 05 09:01:44.316981 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 6, simd_id 0, wgp_id 0
Aug 05 09:01:44.316986 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 7, simd_id 0, wgp_id 0
Aug 05 09:01:44.316994 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 7, simd_id 0, wgp_id 0
Aug 05 09:01:44.316998 my-server kernel: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 7, simd_id 0, wgp_id 0
Aug 05 09:01:44.317661 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
Aug 05 09:01:47.281746 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Aug 05 09:01:47.282276 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
Aug 05 09:01:50.350694 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
Aug 05 09:01:50.380672 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
Aug 05 09:01:50.381696 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
Aug 05 09:01:50.390681 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
Aug 05 09:01:50.430680 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 05 09:01:50.430979 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Aug 05 09:01:50.431123 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Aug 05 09:01:50.431244 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Aug 05 09:01:50.431361 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Aug 05 09:01:50.431476 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Aug 05 09:01:50.431589 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Aug 05 09:01:50.431804 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Aug 05 09:01:50.431891 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Aug 05 09:01:50.431955 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Aug 05 09:01:50.432012 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Aug 05 09:01:50.432066 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Aug 05 09:01:50.432124 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Aug 05 09:01:50.432175 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Aug 05 09:01:50.432227 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Aug 05 09:01:50.432280 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Aug 05 09:01:50.473714 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset(7) succeeded!
Aug 05 09:01:51.339669 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f39cd400000, queue evicted
Aug 05 09:01:51.339748 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f3a41e00000, queue evicted
Aug 05 09:01:51.339757 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f3a58200000, queue evicted
Aug 05 09:01:51.339763 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f3bc6a00000, queue evicted
Aug 05 09:01:51.339770 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f3d90400000, queue evicted
Aug 05 09:01:52.078678 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d26d1000000, queue evicted
Aug 05 09:01:52.078761 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d2798600000, queue evicted
Aug 05 09:01:52.078776 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d2799c00000, queue evicted
Aug 05 09:01:52.078782 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d279aa00000, queue evicted
Aug 05 09:01:52.078787 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d293c400000, queue evicted
Aug 05 09:03:18.738736 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Aug 05 09:03:18.739153 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1804
Aug 05 09:03:18.739296 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Aug 05 09:03:18.739413 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 2
Aug 05 09:03:18.739524 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!
Aug 05 09:03:18.739634 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 0
Aug 05 09:03:18.739768 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 6
Aug 05 09:03:18.739821 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 5
Aug 05 09:03:18.740698 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 4
Aug 05 09:03:18.740788 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 3
Aug 05 09:03:18.740849 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 2
Aug 05 09:03:18.741657 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 1
Aug 05 09:03:18.741745 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Failed to evict queue 0
Aug 05 09:03:18.741782 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Dumping IP State
Aug 05 09:03:18.742661 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: Dumping IP State Completed
Aug 05 09:03:21.858692 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MES failed to respond to msg=SUSPEND
Aug 05 09:03:21.859146 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
Aug 05 09:03:24.773689 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: MODE2 reset
Aug 05 09:03:24.804673 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset succeeded, trying to resume
Aug 05 09:03:24.805667 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: SMU is resuming...
Aug 05 09:03:24.810659 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: SMU is resumed successfully!
Aug 05 09:03:24.851669 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 05 09:03:24.851886 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Aug 05 09:03:24.852006 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Aug 05 09:03:24.852104 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Aug 05 09:03:24.852198 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Aug 05 09:03:24.852295 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Aug 05 09:03:24.852372 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Aug 05 09:03:24.852451 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Aug 05 09:03:24.852550 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Aug 05 09:03:24.852650 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Aug 05 09:03:24.852961 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Aug 05 09:03:24.853140 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Aug 05 09:03:24.853271 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Aug 05 09:03:24.853393 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Aug 05 09:03:24.853511 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Aug 05 09:03:24.853633 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Aug 05 09:03:24.888683 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: GPU reset(8) succeeded!
Aug 05 09:03:25.394693 my-server kernel: amdgpu: Freeing queue vital buffer 0x7e8d40e00000, queue evicted
Aug 05 09:03:25.394803 my-server kernel: amdgpu: Freeing queue vital buffer 0x7e8d41c00000, queue evicted
Aug 05 09:03:25.394823 my-server kernel: amdgpu: Freeing queue vital buffer 0x7e9520800000, queue evicted
Aug 05 09:03:25.394838 my-server kernel: amdgpu: Freeing queue vital buffer 0x7e9568400000, queue evicted
Aug 05 09:03:25.394851 my-server kernel: amdgpu: Freeing queue vital buffer 0x7e95e8600000, queue evicted
Aug 05 09:03:26.470702 my-server kernel: amdgpu: Freeing queue vital buffer 0x6fff6c200000, queue evicted
Aug 05 09:03:26.470837 my-server kernel: amdgpu: Freeing queue vital buffer 0x6fff88a00000, queue evicted
Aug 05 09:03:26.470855 my-server kernel: amdgpu: Freeing queue vital buffer 0x6fff8aa00000, queue evicted
Aug 05 09:03:26.470870 my-server kernel: amdgpu: Freeing queue vital buffer 0x700112800000, queue evicted
Aug 05 09:03:26.470893 my-server kernel: amdgpu: Freeing queue vital buffer 0x700218800000, queue evicted
Aug 05 09:06:22.628671 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d09f0600000, queue evicted
Aug 05 09:06:22.628876 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d09f1400000, queue evicted
Aug 05 09:06:22.628944 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d11cb200000, queue evicted
Aug 05 09:06:22.628966 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d1218400000, queue evicted
Aug 05 09:06:22.628985 my-server kernel: amdgpu: Freeing queue vital buffer 0x7d1454200000, queue evicted
Aug 05 09:06:22.662673 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f1c48400000, queue evicted
Aug 05 09:06:22.662724 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f1cb9600000, queue evicted
Aug 05 09:06:22.662736 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f1cbda00000, queue evicted
Aug 05 09:06:22.662746 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f1e3e200000, queue evicted
Aug 05 09:06:22.662754 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f1e44200000, queue evicted
Aug 05 10:12:04.048989 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: No more SDMA queue to allocate
Aug 05 10:12:04.049457 my-server kernel: amdgpu: process pid 3929525 DQM create queue type 1 failed. ret -12
Aug 05 10:22:07.785676 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bd795c00000, queue evicted
Aug 05 10:22:07.785822 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bdf6ce00000, queue evicted
Aug 05 10:22:07.785837 my-server kernel: amdgpu: Freeing queue vital buffer 0x7bdfbc400000, queue evicted
Aug 05 10:22:07.785848 my-server kernel: amdgpu: Freeing queue vital buffer 0x7be03c600000, queue evicted
Aug 05 10:22:07.785855 my-server kernel: amdgpu: Freeing queue vital buffer 0x7be03d400000, queue evicted
Aug 05 10:22:08.262724 my-server kernel: amdgpu: Freeing queue vital buffer 0x700af9400000, queue evicted
Aug 05 10:22:08.262898 my-server kernel: amdgpu: Freeing queue vital buffer 0x700b6f200000, queue evicted
Aug 05 10:22:08.262916 my-server kernel: amdgpu: Freeing queue vital buffer 0x700cecc00000, queue evicted
Aug 05 10:22:08.262930 my-server kernel: amdgpu: Freeing queue vital buffer 0x700cef200000, queue evicted
Aug 05 10:22:08.262961 my-server kernel: amdgpu: Freeing queue vital buffer 0x700cf4200000, queue evicted
Aug 05 10:22:08.541720 my-server kernel: amdgpu: Freeing queue vital buffer 0x76fe13200000, queue evicted
Aug 05 10:22:08.541766 my-server kernel: amdgpu: Freeing queue vital buffer 0x76fe23200000, queue evicted
Aug 05 10:22:08.541782 my-server kernel: amdgpu: Freeing queue vital buffer 0x76fe3ea00000, queue evicted
Aug 05 10:22:08.541798 my-server kernel: amdgpu: Freeing queue vital buffer 0x76fe44400000, queue evicted
Aug 05 10:22:08.541814 my-server kernel: amdgpu: Freeing queue vital buffer 0x76fe45200000, queue evicted
Aug 05 10:22:08.900682 my-server kernel: amdgpu: Freeing queue vital buffer 0x7b39abe00000, queue evicted
Aug 05 10:22:08.900803 my-server kernel: amdgpu: Freeing queue vital buffer 0x7b39af200000, queue evicted
Aug 05 10:22:08.900817 my-server kernel: amdgpu: Freeing queue vital buffer 0x7b39b0800000, queue evicted
Aug 05 10:22:08.900826 my-server kernel: amdgpu: Freeing queue vital buffer 0x7b39d8200000, queue evicted
Aug 05 10:22:08.900836 my-server kernel: amdgpu: Freeing queue vital buffer 0x7b39d9000000, queue evicted
Aug 05 10:28:24.811915 my-server kernel: amdgpu 0000:c5:00.0: amdgpu: No more SDMA queue to allocate
Aug 05 10:28:24.812377 my-server kernel: amdgpu: process pid 3972722 DQM create queue type 1 failed. ret -12
Aug 05 10:38:31.154667 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ef356600000, queue evicted
Aug 05 10:38:31.154810 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ef378800000, queue evicted
Aug 05 10:38:31.154841 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ef379600000, queue evicted
Aug 05 10:38:31.154866 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ef37a400000, queue evicted
Aug 05 10:38:31.154900 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ef37b200000, queue evicted
Aug 05 10:38:31.583679 my-server kernel: amdgpu: Freeing queue vital buffer 0x766ff9c00000, queue evicted
Aug 05 10:38:31.583823 my-server kernel: amdgpu: Freeing queue vital buffer 0x767042e00000, queue evicted
Aug 05 10:38:31.583843 my-server kernel: amdgpu: Freeing queue vital buffer 0x767048200000, queue evicted
Aug 05 10:38:31.583865 my-server kernel: amdgpu: Freeing queue vital buffer 0x767075600000, queue evicted
Aug 05 10:38:31.583884 my-server kernel: amdgpu: Freeing queue vital buffer 0x767076c00000, queue evicted
Aug 05 10:49:33.170710 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ede95a00000, queue evicted
Aug 05 10:49:33.170879 my-server kernel: amdgpu: Freeing queue vital buffer 0x7edea8200000, queue evicted
Aug 05 10:49:33.170896 my-server kernel: amdgpu: Freeing queue vital buffer 0x7edeaa200000, queue evicted
Aug 05 10:49:33.170910 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ee01c600000, queue evicted
Aug 05 10:49:33.170935 my-server kernel: amdgpu: Freeing queue vital buffer 0x7ee01d400000, queue evicted
Aug 05 10:49:46.725779 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f0c78e00000, queue evicted
Aug 05 10:49:46.725929 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f0c79c00000, queue evicted
Aug 05 10:49:46.725948 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f1459000000, queue evicted
Aug 05 10:49:46.725965 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f14a0400000, queue evicted
Aug 05 10:49:46.725977 my-server kernel: amdgpu: Freeing queue vital buffer 0x7f1524200000, queue evicted

```

### Operating System

ubuntu24.04

### CPU

 AMD RYZEN AI MAX+ 395

### GPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

ROCm 6.4.2

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
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
  Name:                    AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ 395 w/ Radeon 8060S
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
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    65465664(0x3e6ed40) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    65465664(0x3e6ed40) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65465664(0x3e6ed40) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    65465664(0x3e6ed40) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
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
    L3:                      16384(0x4000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   50432                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 26                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    67108864(0x4000000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    67108864(0x4000000) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
    L2:                      2048(0x800) KB                     
    L3:                      16384(0x4000) KB                   
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
      Size:                    65465664(0x3e6ed40) KB             
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
      Size:                    65465664(0x3e6ed40) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*** Done ***   

### Additional Information

_No response_

---

## 评论 (44 条)

### 评论 #1 — ppanchad-amd (2025-08-05T17:41:42Z)

Hi @deific. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — Mushoz (2025-08-07T17:56:37Z)

I have the exact same issue with a lot of different models. I am running kernel 6.15.9 under Archlinux, and have tested ROCm 6.4.1, 6.4.2 and the 7 beta, but all of them exhibit the exact same issue.

And we're definitely not the only two people. I found this Github page of a person running benchmarks with Strix Halo, and lots of entries in the benchmark table are marked as "GPU Hang": https://github.com/kyuz0/amd-strix-halo-toolboxes/blob/main/docs/benchmarks.md

I can reliably trigger this issue by running llama-bench (part of llama.cpp) with GLM4.5-Air at a Q5_K_XL quantization. Since I am able to reliably reproduce the issue, I am more than happy to try out potential fixes. I am more than happy to help test, even if it involves compiling some packages from source with .patch files applied.

---

### 评论 #3 — deific (2025-08-08T01:23:33Z)

I later switched to using a different Linux kernel (6.16) and Rocm 6.4.2、7 beat, but the problem still persists,
I found that it may be necessary to upgrade the  [Linux firmware version](https://bugs.launchpad.net/ubuntu/+source/linux-firmware/+bug/2117463）， According to the description, currently only Ubuntu Questioning has been fixed and released， I haven't tested it yet

---

### 评论 #4 — Mushoz (2025-08-08T07:55:25Z)

I upgraded to linux-firmware-git as of today (2025-08-08) but the issue persists. So unfortunately that does seem to be the solution:

```
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1006
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 4
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 2
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 1
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 0
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Dumping IP State
Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Dumping IP State Completed
Aug 08 09:51:30 ultrabook-jaap kernel: traps: rpc-server-rocm[1866] general protection fault ip:7f88d5f0e5df sp:7f88c69f71f0 error:0 in libc.so.6[255df,7f88d5f0d000+172000]
Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MODE2 reset
Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset succeeded, trying to resume
Aug 08 09:51:31 ultrabook-jaap kernel: [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Aug 08 09:51:31 ultrabook-jaap kernel: [drm] VRAM is lost due to GPU reset!
Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: SMU is resuming...
Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: SMU is resumed successfully!
Aug 08 09:51:31 ultrabook-jaap kernel: [drm] DMUB hardware initialized: version=0x09002600
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset(1) succeeded!
Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: [drm] device wedged, but recovered through reset
```

---

### 评论 #5 — deific (2025-08-08T07:58:31Z)

> I upgraded to linux-firmware-git as of today (2025-08-08) but the issue persists. So unfortunately that does seem to be 
> 
> ```
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1006
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 4
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 2
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 1
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 0
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Dumping IP State
> Aug 08 09:51:30 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Dumping IP State Completed
> Aug 08 09:51:30 ultrabook-jaap kernel: traps: rpc-server-rocm[1866] general protection fault ip:7f88d5f0e5df sp:7f88c69f71f0 error:0 in libc.so.6[255df,7f88d5f0d000+172000]
> Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MODE2 reset
> Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset succeeded, trying to resume
> Aug 08 09:51:31 ultrabook-jaap kernel: [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
> Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
> Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
> Aug 08 09:51:31 ultrabook-jaap kernel: [drm] VRAM is lost due to GPU reset!
> Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: SMU is resuming...
> Aug 08 09:51:31 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: SMU is resumed successfully!
> Aug 08 09:51:31 ultrabook-jaap kernel: [drm] DMUB hardware initialized: version=0x09002600
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset(1) succeeded!
> Aug 08 09:51:32 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: [drm] device wedged, but recovered through reset
> ```

Did you test it on Ubuntu Questioning (25.10) version?

---

### 评论 #6 — Mushoz (2025-08-08T08:01:14Z)

I am running Archlinux, not Ubuntu. But linux-firmware-git will pull the newest version available in the upstream linux-firmware repository. So I am definitely running the newest firmware versions available at this point in time 

---

### 评论 #7 — Mushoz (2025-08-08T08:31:07Z)

Not sure if this is a kernel bug, or ROCm bug. But I found a bug report on the kernel issue tracker as well. Link for reference: https://gitlab.freedesktop.org/drm/amd/-/issues/4321

---

### 评论 #8 — Mushoz (2025-08-08T09:05:13Z)

Actually, that pull request for Ubuntu Questioning might actually be newer looking at the dates of the files currently in linux-firmware-git and the dates of the files in those PRs.

I do see an open PR (opened one day before) on linux-firmware-git which updates lots of firmwares, including the one for gfx1151: https://gitlab.com/kernel-firmware/linux-firmware/-/merge_requests/636/commits

So once that one is merged, I will retry with a fresh install of linux-firmware-git. Fingers crossed!

---

### 评论 #9 — deific (2025-08-08T11:15:05Z)

> Actually, that pull request for Ubuntu Questioning might actually be newer looking at the dates of the files currently in linux-firmware-git and the dates of the files in those PRs.
> 
> I do see an open PR (opened one day before) on linux-firmware-git which updates lots of firmwares, including the one for gfx1151: https://gitlab.com/kernel-firmware/linux-firmware/-/merge_requests/636/commits
> 
> So once that one is merged, I will retry with a fresh install of linux-firmware-git. Fingers crossed!

I hope this is good news！ 


---

### 评论 #10 — Mushoz (2025-08-08T14:06:40Z)

Pull request has just been merged. Going to rebuild and test.

---

### 评论 #11 — Mushoz (2025-08-08T14:14:09Z)

```
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1006
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 4
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 2
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 1
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 0
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu: Failed to quiesce KFD
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Dumping IP State
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: Dumping IP State Completed
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: MODE2 reset
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset succeeded, trying to resume
Aug 08 16:12:02 ultrabook-jaap kernel: [drm] PCIE GART of 512M enabled (table at 0x000000801FB00000).
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: SMU is resuming...
Aug 08 16:12:02 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: SMU is resumed successfully!
Aug 08 16:12:02 ultrabook-jaap kernel: [drm] DMUB hardware initialized: version=0x09002600
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: amdgpu: GPU reset(1) succeeded!
Aug 08 16:12:03 ultrabook-jaap kernel: amdgpu 0000:c3:00.0: [drm] device wedged, but recovered through reset
```

---

### 评论 #12 — sebhofmann (2025-08-11T21:42:04Z)

I have the same issues with the same Chip + 6.16.0-5-cachyos 

**/opt/rocm/bin/rocminfo --support**
```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
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
  Name:                    AMD RYZEN AI MAX+ PRO 395 w/ Radeon 8060S
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD RYZEN AI MAX+ PRO 395 w/ Radeon 8060S
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
  Max Clock Freq. (MHz):   5187                               
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
      Size:                    49082240(0x2ecef80) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    49082240(0x2ecef80) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    49082240(0x2ecef80) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    49082240(0x2ecef80) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1151                            
  Uuid:                    GPU-XX                             
  Marketing Name:          Radeon 8060S Graphics              
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
    L3:                      32768(0x8000) KB                   
  Chip ID:                 5510(0x1586)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2900                               
  BDFID:                   49920                              
  Internal Node ID:        1                                  
  Compute Unit:            40                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
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
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 29                                 
  SDMA engine uCode::      14                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    24541120(0x17677c0) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    24541120(0x17677c0) KB             
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
      Name:                    amdgcn-amd-amdhsa--gfx1151         
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
```

**dmesg -T**
```
Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1004
[Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 3
[Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!
[Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: Failed to evict process queues
[Mo, 11. Aug 2025, 23:29:08] amdgpu: Failed to quiesce KFD
[Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: Dumping IP State
[Mo, 11. Aug 2025, 23:29:08] amdgpu 0000:c3:00.0: amdgpu: Dumping IP State Completed
[Mo, 11. Aug 2025, 23:29:10] [UFW BLOCK] IN=enp197s0f3u1u3 OUT= MAC=-- SRC=192.168.178.1 DST=224.0.0.1 LEN=36 TOS=0x00 PREC=0x00 TTL=1 ID=30516 DF PROTO=2 
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[Mo, 11. Aug 2025, 23:29:10] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: MODE2 reset
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: GPU reset succeeded, trying to resume
[Mo, 11. Aug 2025, 23:29:10] [drm] PCIE GART of 512M enabled (table at 0x00000083FFB00000).
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: [drm] Check your /sys/class/drm/card0/device/devcoredump/data
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: SMU is resuming...
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: SMU is resumed successfully!
[Mo, 11. Aug 2025, 23:29:10] amdgpu 0000:c3:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09002400
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: amdgpu: GPU reset(1) succeeded!
[Mo, 11. Aug 2025, 23:29:11] amdgpu 0000:c3:00.0: [drm] device wedged, but recovered through reset
[Mo, 11. Aug 2025, 23:29:12] amdgpu: Freeing queue vital buffer 0x7f7fb5e00000, queue evicted
[Mo, 11. Aug 2025, 23:29:12] amdgpu: Freeing queue vital buffer 0x7f7fb7400000, queue evicted
[Mo, 11. Aug 2025, 23:29:12] amdgpu: Freeing queue vital buffer 0x7f86db400000, queue evicted
```

other error
```
[Di, 12. Aug 2025, 00:07:12] systemd-journald[854]: Under memory pressure, flushing caches.
[Di, 12. Aug 2025, 00:07:30] [UFW BLOCK] IN=enp197s0f3u1u3 OUT= MAC-- SRC=192.168.178.1 DST=224.0.0.1 LEN=36 TOS=0x00 PREC=0x00 TTL=1 ID=42427 DF PROTO=2 
[Di, 12. Aug 2025, 00:07:50] [UFW BLOCK] IN=enp197s0f3u1u3 OUT= MAC=-- SRC=192.168.178.1 DST=224.0.0.1 LEN=36 TOS=0x00 PREC=0x00 TTL=1 ID=43741 DF PROTO=2 
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d76000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:        Faulty UTCL2 client ID: TCP (0x8)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:        MORE_FAULTS: 0x1
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:        WALKER_ERROR: 0x0
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:        PERMISSION_FAULTS: 0x3
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:        MAPPING_ERROR: 0x0
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:        RW: 0x0
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d8e000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03da7000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d5e000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d58000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d7a000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d9b000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d98000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d80000 from client 10
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32810)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:  in process llama-server pid 15273 thread llama-server pid 15273)
[Di, 12. Aug 2025, 00:08:06] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f2b03d86000 from client 10
[Di, 12. Aug 2025, 00:08:09] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[Di, 12. Aug 2025, 00:08:09] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[Di, 12. Aug 2025, 00:08:09] amdgpu 0000:c3:00.0: amdgpu: failed to suspend gangs from MES
[Di, 12. Aug 2025, 00:08:09] amdgpu 0000:c3:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[Di, 12. Aug 2025, 00:08:09] amdgpu 0000:c3:00.0: amdgpu: Suspending all queues failed
[Di, 12. Aug 2025, 00:08:09] amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!
[Di, 12. Aug 2025, 00:08:10] [UFW BLOCK] IN=enp197s0f3u1u3 OUT= MAC=-- SRC=192.168.178.1 DST=224.0.0.1 LEN=36 TOS=0x00 PREC=0x00 TTL=1 ID=45354 DF PROTO=2 
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1006
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 3
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 2
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 1
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: Failed to evict queue 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 1, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: Dumping IP State
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[Di, 12. Aug 2025, 00:08:11] amdgpu 0000:c3:00.0: amdgpu: Dumping IP State Completed
[Di, 12. Aug 2025, 00:08:12] amdgpu 0000:c3:00.0: amdgpu: MODE2 reset
[Di, 12. Aug 2025, 00:08:12] amdgpu 0000:c3:00.0: amdgpu: GPU reset succeeded, trying to resume
[Di, 12. Aug 2025, 00:08:12] [drm] PCIE GART of 512M enabled (table at 0x00000083FFB00000).
[Di, 12. Aug 2025, 00:08:12] amdgpu 0000:c3:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
[Di, 12. Aug 2025, 00:08:12] amdgpu 0000:c3:00.0: amdgpu: [drm] Check your /sys/class/drm/card0/device/devcoredump/data
[Di, 12. Aug 2025, 00:08:12] amdgpu 0000:c3:00.0: amdgpu: SMU is resuming...
[Di, 12. Aug 2025, 00:08:12] amdgpu 0000:c3:00.0: amdgpu: SMU is resumed successfully!
[Di, 12. Aug 2025, 00:08:12] amdgpu 0000:c3:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09002400
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: amdgpu: GPU reset(2) succeeded!
[Di, 12. Aug 2025, 00:08:13] amdgpu 0000:c3:00.0: [drm] device wedged, but recovered through reset
```

I’m a bit disappointed with the chip, considering all the hype the AMD marketing team has been putting out about AI.

---

### 评论 #13 — ndrewpj (2025-08-12T13:39:50Z)

I have the same error on different kernels, rocm version and OS. I tried Ubuntu 22.04.5, 24.04.2, 24.04.3 with stock and HWE kernels, CachyOS, Fedora Rawhide 43... all the same. Rocm 6.4.2, 6.4.3, 7.0 beta/rc, TheRock

---

### 评论 #14 — vchrizz (2025-08-13T00:44:41Z)

Same setup as in OP and same issue here. Interestingly I am 100% able to reproduce this gpu hang issue by calling ollama via "Chat API" (which afaik is required for tool calling). Using "Generate API" there is no issue (but seemingly no tool calling support).
Also I tried it with Fedora 42 and there is the same issue. Also tried several different models of different sizes, params, etc. currently trying gpt-oss but same happens to small (~8-12GB) as also large models (32GB+) where I try to use tool calling.
Mentioning just in case, if that helps to pinpoint the exact issue.

edit: it seems, that using "Chat API" on ollama with larger models >8GB gpu hangs occur (ollama process defunct). using very small models <8GB no gpu hangs, but infinte loops occur (ollama can be stopped/restarted).

edit: while trying to show a reproducible command, I noticed, with "smaller" models it does not happen always reliable and sometimes only leads to endless loops.
so to reliably reproduce the isse, you have to use larger models like gpt-oss:120b . following command reproduces the gpu hang issue, please be careful executing this command!
`curl -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{"model": "gpt-oss:120b", "stream": true, "messages": [{"role": "system", "content": "You are a helpful assistant with access to tools."}, {"role": "user", "content": "Use the shell tool to run the command '\''uptime'\'' to check system uptime."}], "tools": [{"type": "function", "function": {"name": "run_shell_command", "description": "Execute a shell command", "parameters": {"type": "object", "properties": {"command": {"type": "string", "description": "The shell command to execute"}}, "required": ["command"]}}}]}'`

---

### 评论 #15 — Mushoz (2025-08-14T07:49:00Z)

According to this comment on a similar issue raised in the drm/amd repo: https://gitlab.freedesktop.org/drm/amd/-/issues/4321#note_3048205

A fix is available, but not yet implemented in any of the ROCm stable branches. A backport to the stable branches is not planned until a 7.0.x point release, eg it won't even be available in the initial ROCm 7 release. That means with the release cadence of ROCm, worst case scenario it might be several months before the fix is available.

Quite frankly, that is unacceptable to me. Strix Halo was marketed with a big focus on AI. Having an unstable ROCm stack prevents me from using the product for which I bought it.

The AMD employee that I was chatting with in that issue tracker, Mario Limonciell, mentioned that I should raise my concerns here in the hopes that a backport could be done earlier than currently planned. @ppanchad-amd are you the right person to speak to about this? If not, would you be so kind to ask the right person to join the discussion here?

I understand new features take some time before they reach any stable branches. But surely a bug that is preventing ROCm from being usable at all has a higher priority to be included?

---

### 评论 #16 — drcongo (2025-08-14T18:14:41Z)

Having the same problem here with ROCm 7 from TheRock, Ubuntu 25.04 running ollama

---

### 评论 #17 — ethanics (2025-08-18T15:16:12Z)

OS:
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
CPU:
model name : AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

VRAM=32G by BIOS.

When I play this YouTube video on Firefox, my GPU resets.
(Firefox installed via apt: `firefox/mozilla,now 141.0.3~build1 amd64 [installed,automatic]`)
Video: https://www.youtube.com/watch?v=KY7E-pj7UYc

If I pause the video for a while and then click to play it again, the GPU resets again.

Not all YouTube videos trigger this issue, but this specific video causes the GPU to reset twice.

1st time GPU reset
Output of `journalctl -xe`
attached: `journal_xe1.log`

2nd time GPU reset
Output of `journalctl -xe`
attached: `journal_xe2.log`

amdgpu related packages.
Output of `apt list --installed`
attached: `apt_installed_amdgpu.log`

Output of `/opt/rocm/bin/rocminfo --support`
attached: `rocminfo_support.log`

[apt_installed_amdgpu.log](https://github.com/user-attachments/files/21838597/apt_installed_amdgpu.log)
[journal_xe1.log](https://github.com/user-attachments/files/21838598/journal_xe1.log)
[journal_xe2.log](https://github.com/user-attachments/files/21838595/journal_xe2.log)
[rocminfo_support.log](https://github.com/user-attachments/files/21838596/rocminfo_support.log)

---

### 评论 #18 — stormenergy91 (2025-10-07T08:07:42Z)

Any news about this issue? I have the same problem with the HP Z2 mini G1a Workstation. I try with the last ROCm version (7.0.1) but I get hang using Ollama (Ubuntu 24.04 + ollama:rocm container with podman).

In the conatiner I set this env vars:
```
Environment=HSA_OVERRIDE_GFX_VERSION=11.5.1
Environment=ROCR_VISIBLE_DEVICES=0
```
In the ollama logs it reconginx the card correctly but I get hangs. I found that the error that generate the hang is in the amdgpu dirver with the MES `MES failed to respond to msg=REMOVE_QUEUE / SUSPEND`

I try to comment the two env vars but same issue.

There is any workaround? Using Vulkan instead of ROCm may help?

EDIT
---
I try to removing the `amdgpu-dkms` package and installing `linux-generic-hwe-24.04` (using the open amdgpu driver) but i get the same amgpu error:

```
[  173.106479] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
[  173.106483] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[  173.106486] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x1
[  173.106489] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
[  173.106491] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x5
[  173.106493] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  173.106495] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x1
```
 I also tryied to add in grub `amdgpu.mes=0 amdgpu.runpm=0 amdgpu.gfxoff=0` but no success.

---

### 评论 #19 — sebhofmann (2025-10-07T08:37:22Z)

> There is any workaround? Using Vulkan instead of ROCm may help?

Ollama does not have vulkan support, but you can use llama.cpp with vulkan.

You could also use these builds: https://github.com/lemonade-sdk/llamacpp-rocm/releases

Their b1066 rocm build works for me.

---

### 评论 #20 — ndrewpj (2025-10-07T16:05:56Z)

> > There is any workaround? Using Vulkan instead of ROCm may help?
> 
> Ollama does not have vulkan support, but you can use llama.cpp with vulkan.
> 
> You could also use these builds: https://github.com/lemonade-sdk/llamacpp-rocm/releases
> 
> Their b1066 rocm build works for me.

"Ollama MUSA" has a vulkan flavor that works OKish with some issues.
https://github.com/MooreThreads/ollama-musa/issues/31#issuecomment-3375069348


---

### 评论 #21 — ndrewpj (2025-10-08T21:20:45Z)

> In the ollama logs it reconginx the card correctly but I get hangs. I found that the error that generate the hang is in the amdgpu dirver with the MES `MES failed to respond to msg=REMOVE_QUEUE / SUSPEND`
> 
> I try to comment the two env vars but same issue.
> 
> There is any workaround? Using Vulkan instead of ROCm may help?

It seems the MES issue was fixed in another 6.14 kernel for Ubuntu - the OEM kernel which has recent AMD fixes. Check this comment, I tried it and it works:
https://github.com/ROCm/ROCm/issues/4909#issuecomment-3374388972

---

### 评论 #22 — stormenergy91 (2025-10-09T12:00:33Z)

> he MES issue was fixed in another 6.14 kernel for Ubuntu - the OEM kernel which has recent AMD fixes. Check this comment, I tried it and it works:
> [#4909 (comment)](https://github.com/ROCm/ROCm/issues/4909#issuecomment-3374388972)

I tried using [the driver](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html) mentioned in the comment. It seems a little more stable, but I still keep getting the error:

```
[18149.583820] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[18149.583832] amdgpu 0000:c4:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
[18149.583834] amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[18149.583840] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
[18149.583860] amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
[18149.583942] amdgpu 0000:c4:00.0: amdgpu: Failed to evict process queues
[18149.584000] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
[18149.584806] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
[18149.650804] amdgpu: Freeing queue vital buffer 0x7bd371e00000, queue evicted
[18149.650810] amdgpu: Freeing queue vital buffer 0x7bd7d5c00000, queue evicted
[18149.650812] amdgpu: Freeing queue vital buffer 0x7bd7d6a00000, queue evicted
[18149.650814] amdgpu: Freeing queue vital buffer 0x7bd7e7200000, queue evicted
[18149.650816] amdgpu: Freeing queue vital buffer 0x7bd7ec400000, queue evicted
[18150.592263] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[18150.592287] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[18150.592294] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
[18150.592298] amdgpu 0000:c4:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[18150.592302] amdgpu 0000:c4:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[18150.592305] amdgpu 0000:c4:00.0: amdgpu: 	 WALKER_ERROR: 0x1
[18150.592308] amdgpu 0000:c4:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
[18150.592310] amdgpu 0000:c4:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
[18150.592313] amdgpu 0000:c4:00.0: amdgpu: 	 RW: 0x1
[18150.592334] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[18150.592339] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[18152.225217] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[18152.225226] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[18152.225432] amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
```
In my test i'm using `ollama/ollama:rocm` with `qwen3-coder:30b` using Cline on VS Code.

---

### 评论 #23 — ndrewpj (2025-10-09T12:08:26Z)

> > he MES issue was fixed in another 6.14 kernel for Ubuntu - the OEM kernel which has recent AMD fixes. Check this comment, I tried it and it works:
> > [#4909 (comment)](https://github.com/ROCm/ROCm/issues/4909#issuecomment-3374388972)
> 
> I tried using [the driver](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html) mentioned in the comment. It seems a little more stable, but I still keep getting the error:
> 
> ```
> [18149.583820] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> [18149.583832] amdgpu 0000:c4:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
> [18149.583834] amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
> [18149.583840] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
> [18149.583860] amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
> [18149.583942] amdgpu 0000:c4:00.0: amdgpu: Failed to evict process queues
> [18149.584000] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
> [18149.584806] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
> [18149.650804] amdgpu: Freeing queue vital buffer 0x7bd371e00000, queue evicted
> [18149.650810] amdgpu: Freeing queue vital buffer 0x7bd7d5c00000, queue evicted
> [18149.650812] amdgpu: Freeing queue vital buffer 0x7bd7d6a00000, queue evicted
> [18149.650814] amdgpu: Freeing queue vital buffer 0x7bd7e7200000, queue evicted
> [18149.650816] amdgpu: Freeing queue vital buffer 0x7bd7ec400000, queue evicted
> [18150.592263] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
> [18150.592287] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [18150.592294] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
> [18150.592298] amdgpu 0000:c4:00.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
> [18150.592302] amdgpu 0000:c4:00.0: amdgpu: 	 MORE_FAULTS: 0x1
> [18150.592305] amdgpu 0000:c4:00.0: amdgpu: 	 WALKER_ERROR: 0x1
> [18150.592308] amdgpu 0000:c4:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
> [18150.592310] amdgpu 0000:c4:00.0: amdgpu: 	 MAPPING_ERROR: 0x1
> [18150.592313] amdgpu 0000:c4:00.0: amdgpu: 	 RW: 0x1
> [18150.592334] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
> [18150.592339] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [18152.225217] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
> [18152.225226] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
> [18152.225432] amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
> ```
> 
> In my test i'm using `ollama/ollama:rocm` with `qwen3-coder:30b` using Cline on VS Code.

I believe the driver alone is not enough. It is part of rocm and I was talking about the kernel. BTW Linux firmware is also installed along the kernel

---

### 评论 #24 — stormenergy91 (2025-10-10T08:50:34Z)

> I believe the driver alone is not enough. It is part of rocm and I was talking about the kernel. BTW Linux firmware is also installed along the kernel

I made a fresh install of the system (Ubuntu 24.04 Server), and checked that the `linux-firmware` package is up to date. Then I installed the driver using `amdgpu-install -y --usecase=graphics,rocm`, but…

```
[ 4035.382416] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
[ 4035.382433] amdgpu 0000:c4:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1802
[ 4035.382441] amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 4035.382454] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
[ 4035.382473] amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
[ 4035.382577] amdgpu 0000:c4:00.0: amdgpu: Failed to evict process queues
[ 4035.382599] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 6
[ 4035.382617] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 5
[ 4035.382628] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 4
[ 4035.382637] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
[ 4035.382647] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 2
[ 4035.382657] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
[ 4035.382667] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
[ 4035.382717] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
[ 4035.384891] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
[ 4038.042400] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[ 4038.042409] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[ 4038.042566] amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
[ 4038.042930] amdgpu: Freeing queue vital buffer 0x7e12cc400000, queue evicted
[ 4038.042944] amdgpu: Freeing queue vital buffer 0x7e12cd200000, queue evicted
[ 4038.042948] amdgpu: Freeing queue vital buffer 0x7e1325a00000, queue evicted
[ 4038.042952] amdgpu: Freeing queue vital buffer 0x7e1477200000, queue evicted
[ 4038.042953] amdgpu: Freeing queue vital buffer 0x7e147c400000, queue evicted
[ 4038.047343] amdgpu: Freeing queue vital buffer 0x7c8d5b600000, queue evicted
[ 4038.047346] amdgpu: Freeing queue vital buffer 0x7c91c1600000, queue evicted
[ 4038.047347] amdgpu: Freeing queue vital buffer 0x7c91c2800000, queue evicted
[ 4038.047350] amdgpu: Freeing queue vital buffer 0x7c91d2400000, queue evicted
[ 4038.047351] amdgpu: Freeing queue vital buffer 0x7c91d3200000, queue evicted
[ 4038.480435] gmc_v11_0_process_interrupt: 113 callbacks suppressed
[ 4038.480447] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[ 4038.480465] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.480470] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
[ 4038.480474] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
[ 4038.480477] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x1
[ 4038.480480] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
[ 4038.480482] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x5
[ 4038.480484] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
[ 4038.480486] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x1
[ 4038.481837] amdgpu 0000:c4:00.0: amdgpu: MODE2 reset
[ 4038.485791] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[ 4038.485804] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485818] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[ 4038.485826] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485838] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[ 4038.485847] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485858] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[ 4038.485866] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485877] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[ 4038.485886] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485897] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[ 4038.485905] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485916] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[ 4038.485925] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485936] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[ 4038.485944] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[ 4038.485955] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[ 4038.485964] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
```

Is correct use `usecase=graphics` or is better `usecase=workstation`?

---

### 评论 #25 — ndrewpj (2025-10-10T09:13:29Z)

> > I believe the driver alone is not enough. It is part of rocm and I was talking about the kernel. BTW Linux firmware is also installed along the kernel
> 
> I made a fresh install of the system (Ubuntu 24.04 Server), and checked that the `linux-firmware` package is up to date. Then I installed the driver using `amdgpu-install -y --usecase=graphics,rocm`, but…
> 
> ```
> [ 4035.382416] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
> [ 4035.382433] amdgpu 0000:c4:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1802
> [ 4035.382441] amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
> [ 4035.382454] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
> [ 4035.382473] amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
> [ 4035.382577] amdgpu 0000:c4:00.0: amdgpu: Failed to evict process queues
> [ 4035.382599] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 6
> [ 4035.382617] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 5
> [ 4035.382628] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 4
> [ 4035.382637] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
> [ 4035.382647] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 2
> [ 4035.382657] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
> [ 4035.382667] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
> [ 4035.382717] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
> [ 4035.384891] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
> [ 4038.042400] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
> [ 4038.042409] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
> [ 4038.042566] amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
> [ 4038.042930] amdgpu: Freeing queue vital buffer 0x7e12cc400000, queue evicted
> [ 4038.042944] amdgpu: Freeing queue vital buffer 0x7e12cd200000, queue evicted
> [ 4038.042948] amdgpu: Freeing queue vital buffer 0x7e1325a00000, queue evicted
> [ 4038.042952] amdgpu: Freeing queue vital buffer 0x7e1477200000, queue evicted
> [ 4038.042953] amdgpu: Freeing queue vital buffer 0x7e147c400000, queue evicted
> [ 4038.047343] amdgpu: Freeing queue vital buffer 0x7c8d5b600000, queue evicted
> [ 4038.047346] amdgpu: Freeing queue vital buffer 0x7c91c1600000, queue evicted
> [ 4038.047347] amdgpu: Freeing queue vital buffer 0x7c91c2800000, queue evicted
> [ 4038.047350] amdgpu: Freeing queue vital buffer 0x7c91d2400000, queue evicted
> [ 4038.047351] amdgpu: Freeing queue vital buffer 0x7c91d3200000, queue evicted
> [ 4038.480435] gmc_v11_0_process_interrupt: 113 callbacks suppressed
> [ 4038.480447] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
> [ 4038.480465] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.480470] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
> [ 4038.480474] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: CPC (0x5)
> [ 4038.480477] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x1
> [ 4038.480480] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x1
> [ 4038.480482] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x5
> [ 4038.480484] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x1
> [ 4038.480486] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x1
> [ 4038.481837] amdgpu 0000:c4:00.0: amdgpu: MODE2 reset
> [ 4038.485791] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
> [ 4038.485804] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485818] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
> [ 4038.485826] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485838] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
> [ 4038.485847] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485858] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
> [ 4038.485866] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485877] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
> [ 4038.485886] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485897] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
> [ 4038.485905] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485916] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
> [ 4038.485925] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485936] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
> [ 4038.485944] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> [ 4038.485955] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
> [ 4038.485964] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
> ```
> 
> Is correct use `usecase=graphics` or is better `usecase=workstation`?

For compute I bet workstation option is better. Did you switch to OEM kernel as well?

---

### 评论 #26 — stormenergy91 (2025-10-10T09:55:31Z)

> For compute I bet workstation option is better. Did you switch to OEM kernel as well?

Yes, intealled ubuntu 24.04 server, then the pakcages `linux-firmware` and `linux-oem-24.04` (6.14.0-1013-oem) and at last `amdgpu-install -y --usecase=workstation,rocm`.  I'm using podman with the ollama image `ollama/ollama:0.12.4-rocm` and the model `qwen3-coder:30b` (I set the vram to 96GB and when ollama load the model it use 35GB so i have free vram).

But when i try to do some operation with cline form vs code:

```
[ 1288.979334] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.979403] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.979417] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb92b000 from client 10
[ 1288.979432] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
[ 1288.979443] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[ 1288.979454] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x1
[ 1288.979463] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x0
[ 1288.979472] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[ 1288.979481] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x0
[ 1288.979490] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
[ 1288.979530] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.979543] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.979555] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb838000 from client 10
[ 1288.979583] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.979598] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.979935] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8fa000 from client 10
[ 1288.980245] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.980536] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.980822] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb912000 from client 10
[ 1288.981007] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.981172] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.981336] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb820000 from client 10
[ 1288.981519] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.981684] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.981849] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb808000 from client 10
[ 1288.982031] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.982197] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.982362] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8ca000 from client 10
[ 1288.982548] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.982717] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.982887] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8e2000 from client 10
[ 1288.983077] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.983248] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.983418] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb899000 from client 10
[ 1288.983606] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
[ 1288.983775] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
[ 1288.983944] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8b1000 from client 10
[ 1291.653639] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[ 1291.653911] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[ 1291.654117] amdgpu 0000:c4:00.0: amdgpu: failed to suspend gangs from MES
[ 1291.654475] amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
[ 1291.654658] amdgpu 0000:c4:00.0: amdgpu: Suspending all queues failed
[ 1291.654682] amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
[ 1291.654876] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 6
[ 1291.655436] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 5
[ 1291.655794] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 4
[ 1291.655943] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
[ 1291.656080] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 2
[ 1291.656207] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
[ 1291.656333] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
[ 1291.656461] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656469] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656472] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656474] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656477] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656480] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656482] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656485] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656487] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656490] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
[ 1291.656516] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
[ 1291.657511] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
[ 1294.383279] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
[ 1294.383291] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
[ 1294.383495] amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
```

---

### 评论 #27 — ndrewpj (2025-10-10T10:13:38Z)

> > For compute I bet workstation option is better. Did you switch to OEM kernel as well?
> 
> Yes, intealled ubuntu 24.04 server, then the pakcages `linux-firmware` and `linux-oem-24.04` (6.14.0-1013-oem) and at last `amdgpu-install -y --usecase=workstation,rocm`. I'm using podman with the ollama image `ollama/ollama:0.12.4-rocm` and the model `qwen3-coder:30b` (I set the vram to 96GB and when ollama load the model it use 35GB so i have free vram).
> 
> But when i try to do some operation with cline form vs code:
> 
> ```
> [ 1288.979334] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.979403] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.979417] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb92b000 from client 10
> [ 1288.979432] amdgpu 0000:c4:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
> [ 1288.979443] amdgpu 0000:c4:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
> [ 1288.979454] amdgpu 0000:c4:00.0: amdgpu:      MORE_FAULTS: 0x1
> [ 1288.979463] amdgpu 0000:c4:00.0: amdgpu:      WALKER_ERROR: 0x0
> [ 1288.979472] amdgpu 0000:c4:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
> [ 1288.979481] amdgpu 0000:c4:00.0: amdgpu:      MAPPING_ERROR: 0x0
> [ 1288.979490] amdgpu 0000:c4:00.0: amdgpu:      RW: 0x0
> [ 1288.979530] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.979543] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.979555] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb838000 from client 10
> [ 1288.979583] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.979598] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.979935] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8fa000 from client 10
> [ 1288.980245] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.980536] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.980822] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb912000 from client 10
> [ 1288.981007] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.981172] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.981336] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb820000 from client 10
> [ 1288.981519] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.981684] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.981849] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb808000 from client 10
> [ 1288.982031] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.982197] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.982362] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8ca000 from client 10
> [ 1288.982548] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.982717] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.982887] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8e2000 from client 10
> [ 1288.983077] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.983248] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.983418] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb899000 from client 10
> [ 1288.983606] amdgpu 0000:c4:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32770)
> [ 1288.983775] amdgpu 0000:c4:00.0: amdgpu:  in process ollama pid 5118 thread ollama pid 5124)
> [ 1288.983944] amdgpu 0000:c4:00.0: amdgpu:   in page starting at address 0x00007e9ebb8b1000 from client 10
> [ 1291.653639] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
> [ 1291.653911] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
> [ 1291.654117] amdgpu 0000:c4:00.0: amdgpu: failed to suspend gangs from MES
> [ 1291.654475] amdgpu 0000:c4:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
> [ 1291.654658] amdgpu 0000:c4:00.0: amdgpu: Suspending all queues failed
> [ 1291.654682] amdgpu 0000:c4:00.0: amdgpu: GPU reset begin!
> [ 1291.654876] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 6
> [ 1291.655436] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 5
> [ 1291.655794] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 4
> [ 1291.655943] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 3
> [ 1291.656080] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 2
> [ 1291.656207] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 1
> [ 1291.656333] amdgpu 0000:c4:00.0: amdgpu: Failed to evict queue 0
> [ 1291.656461] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656469] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656472] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656474] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656477] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656480] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 1, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656482] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656485] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656487] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656490] amdgpu: sq_intr: error, detail 0x00000000, type 2, sh 0, priv 1, wave_id 0, simd_id 0, wgp_id 0
> [ 1291.656516] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State
> [ 1291.657511] amdgpu 0000:c4:00.0: amdgpu: Dumping IP State Completed
> [ 1294.383279] amdgpu 0000:c4:00.0: amdgpu: MES failed to respond to msg=SUSPEND
> [ 1294.383291] [drm:amdgpu_mes_suspend [amdgpu]] *ERROR* failed to suspend all gangs
> [ 1294.383495] amdgpu 0000:c4:00.0: amdgpu: suspend of IP block <mes_v11_0> failed -110
> ```

Which ROCm did you install?

---

### 评论 #28 — stormenergy91 (2025-10-10T10:17:15Z)

> Which ROCm did you install?

should be 6.4.4. I installed the one of the [above link](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/native_linux/install-radeon.html).  

EDIT
It seems that the error occurs when an operation takes longer than 4 minutes. If the operation takes less time, the error never occurs. I don't know if this information is useful.


---

### 评论 #29 — dstengle (2025-10-14T15:44:10Z)

I get the following from rocminfo:

ROCk module version 6.14.14 is loaded

I get consistent resets with ollama and gpt-oss-120b and this hangs my wayland session

---

### 评论 #30 — ndrewpj (2025-10-14T20:39:48Z)

> I get the following from rocminfo:
> 
> ROCk module version 6.14.14 is loaded
> 
> I get consistent resets with ollama and gpt-oss-120b and this hangs my wayland session

Try to disable flash attention in ollama, gpt-oss doesn't like it

---

### 评论 #31 — dstengle (2025-10-17T10:52:29Z)

Regardless of what the model likes, this shouldn't crash the GPU, should it? Is this reset caused by the model?

> > I get the following from rocminfo:
> > 
> > ROCk module version 6.14.14 is loaded
> > 
> > I get consistent resets with ollama and gpt-oss-120b and this hangs my wayland session
> 
> Try to disable flash attention in ollama, gpt-oss doesn't like it



---

### 评论 #32 — vjeson (2025-10-21T06:51:45Z)

I have the same problem with ubuntu 24 ,6.14.0-33-generic kernel ,rocm 7.0.2 , ollama 0.12.6 , Radeon RX 7900 XT 

---

### 评论 #33 — ianbmacdonald (2025-10-24T02:59:21Z)

Check your firmware.  With `amdgpu: MES failed to respond to msg=SUSPEND`, if you are not MES feature version 0x0000007f or newer, that newer kernel is not going to be able to avoid the hang.  

```
# cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080

```

---

### 评论 #34 — ndrewpj (2025-10-24T07:07:05Z)

> Check your firmware. With `amdgpu: MES failed to respond to msg=SUSPEND`, if you are not MES feature version 0x0000007f or newer, that newer kernel is not going to be able to avoid the hang.
> 
> ```
> # cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
> MES_KIQ feature version: 6, firmware version: 0x0000006f
> MES feature version: 1, firmware version: 0x00000080
> ```

Where can we get the latest firmware?

---

### 评论 #35 — ndrewpj (2025-10-26T13:11:58Z)

> Check your firmware. With `amdgpu: MES failed to respond to msg=SUSPEND`, if you are not MES feature version 0x0000007f or newer, that newer kernel is not going to be able to avoid the hang.
> 
> ```
> # cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
> MES_KIQ feature version: 6, firmware version: 0x0000006f
> MES feature version: 1, firmware version: 0x00000080
> ```

I have the 0x00000080 firmware and still have GPU hang events. But to be honest it is happening less often than in the past

---

### 评论 #36 — vchrizz (2025-10-26T18:01:58Z)

Interesting, we should have at least 0x0000007f ? How could we upgrade to that?
I updated to `AMD ROCm™ 7.0.2 for Ubuntu 24.04.3 HWE` (from https://www.amd.com/en/support/download/linux-drivers.html) and after upgrade still have the following:
```
# cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006c
MES feature version: 1, firmware version: 0x0000006e
```


---

### 评论 #37 — ianbmacdonald (2025-10-28T00:15:40Z)

Yes, it is a known issue, and the hangs still exist even on the new firmware.  Currently you have to wait for newer to ship in amdgpu-dkms-firmware ;  I gather from https://github.com/ROCm/ROCm/issues/5566 that AMD's CI does not allow them to easily drop in updates to individual files, even for binary firmware blobs which don't need much testing when they fix problems for a very specific architecture. I suspect they won't be updated until the next ROCm/Instinct release (7.0.3 / 30.10.3).  

One way to pull the upstream firmware, and stay within apt policy without any hacky wget sideloads, is to add the upstream Resolute Raccoon apt source, and pin just the newer linux-firmware package.  This will most likely always keep you ahead of amdgpu-dkms-firmware, similar to today.  Then you use dpkg-divert to keep amdgpu-dkms-firmware from overwriting it on any subsequent package updates.   Here is are the steps, with reversion steps that could be executed once you are satisfied that something equivalent is coming from either linux-firmware or amdgpu-dkms-firmware. 

add the apt source:
```
echo 'Types: deb
URIs: http://archive.ubuntu.com/ubuntu/
Suites: resolute
Components: main
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg' \
| sudo tee /etc/apt/sources.list.d/ubuntu_resolute.sources
```
create the pin that ignores all resolute packages, except linux-firmware, which it prefers:
```
echo 'Package: *
Pin: release n=resolute
Pin-Priority: 1

Package: linux-firmware
Pin: release n=resolute
Pin-Priority: 600' \
| sudo tee /etc/apt/preferences.d/linux-firwmare-resolute-pin
```
Then divert the amdgpu-dkms-firmware files so they do not get updated if you run amdgpu-install, upgrade or reinstall.
```
sudo dpkg-divert --divert /lib/firmware/updates/amdgpu/gc_11_5_1_imu.bin.amdgpu --rename /lib/firmware/updates/amdgpu/gc_11_5_1_imu.bin
sudo dpkg-divert --divert /lib/firmware/updates/amdgpu/gc_11_5_1_me.bin.amdgpu --rename /lib/firmware/updates/amdgpu/gc_11_5_1_me.bin
sudo dpkg-divert --divert /lib/firmware/updates/amdgpu/gc_11_5_1_mec.bin.amdgpu --rename /lib/firmware/updates/amdgpu/gc_11_5_1_mec.bin
sudo dpkg-divert --divert /lib/firmware/updates/amdgpu/gc_11_5_1_mes1.bin.amdgpu --rename /lib/firmware/updates/amdgpu/gc_11_5_1_mes1.bin
sudo dpkg-divert --divert /lib/firmware/updates/amdgpu/gc_11_5_1_mes_2.bin.amdgpu --rename /lib/firmware/updates/amdgpu/gc_11_5_1_mes_2.bin
sudo dpkg-divert --divert /lib/firmware/updates/amdgpu/gc_11_5_1_pfp.bin.amdgpu --rename /lib/firmware/updates/amdgpu/gc_11_5_1_pfp.bin
sudo dpkg-divert --divert /lib/firmware/updates/amdgpu/gc_11_5_1_rlc.bin.amdgpu --rename /lib/firmware/updates/amdgpu/gc_11_5_1_rlc.bin
```
Down the road, if you no longer want the newer firmware from linux-firmware, you set the linux-firmware pin to `Pin-Priority: 1` or comment out `/etc/apt/sources.list.d/ubuntu_resolute.sources` and reinstall the noble package:
```
sudo apt install linux-firmware/noble --reinstall
```
If you want to reinstate the amdgpu-dkms-firmware as the overriding firmware, you simply remove the diversion and put the original files back in place.  A the next install, they will be replaced with the packaged versions. 
```
sudo dpkg-divert --remove /lib/firmware/updates/amdgpu/gc_11_5_1_imu.bin
sudo dpkg-divert --remove /lib/firmware/updates/amdgpu/gc_11_5_1_me.bin
sudo dpkg-divert --remove /lib/firmware/updates/amdgpu/gc_11_5_1_mec.bin
sudo dpkg-divert --remove /lib/firmware/updates/amdgpu/gc_11_5_1_mes1.bin
sudo dpkg-divert --remove /lib/firmware/updates/amdgpu/gc_11_5_1_mes_2.bin
sudo dpkg-divert --remove /lib/firmware/updates/amdgpu/gc_11_5_1_pfp.bin
sudo dpkg-divert --remove /lib/firmware/updates/amdgpu/gc_11_5_1_rlc.bin

sudo mv /lib/firmware/updates/amdgpu/gc_11_5_1_imu.bin.amdgpu /lib/firmware/updates/amdgpu/gc_11_5_1_imu.bin
sudo mv /lib/firmware/updates/amdgpu/gc_11_5_1_me.bin.amdgpu /lib/firmware/updates/amdgpu/gc_11_5_1_me.bin
sudo mv /lib/firmware/updates/amdgpu/gc_11_5_1_mec.bin.amdgpu /lib/firmware/updates/amdgpu/gc_11_5_1_mec.bin
sudo mv /lib/firmware/updates/amdgpu/gc_11_5_1_mes1.bin.amdgpu /lib/firmware/updates/amdgpu/gc_11_5_1_mes1.bin
sudo mv /lib/firmware/updates/amdgpu/gc_11_5_1_mes_2.bin.amdgpu /lib/firmware/updates/amdgpu/gc_11_5_1_mes_2.bin
sudo mv /lib/firmware/updates/amdgpu/gc_11_5_1_pfp.bin.amdgpu /lib/firmware/updates/amdgpu/gc_11_5_1_pfp.bin
sudo mv /lib/firmware/updates/amdgpu/gc_11_5_1_rlc.bin.amdgpu /lib/firmware/updates/amdgpu/gc_11_5_1_rlc.bin

sudo apt install amdgpu-dkms-firmware/noble --reinstall
```
The result should look just like this
```
imac@ai2:~$ sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080
imac@ai2:~$ dpkg -l | grep linux-firmware
ii  linux-firmware                       20251009.git46a6999a-0ubuntu1        all          Firmware for Linux kernel drivers
imac@ai2:~$ dpkg-divert --list | grep amdgpu
local diversion of /lib/firmware/updates/amdgpu/gc_11_5_1_mes_2.bin to /lib/firmware/updates/amdgpu/gc_11_5_1_mes_2.bin.amdgpu
local diversion of /lib/firmware/updates/amdgpu/gc_11_5_1_mec.bin to /lib/firmware/updates/amdgpu/gc_11_5_1_mec.bin.amdgpu
local diversion of /lib/firmware/updates/amdgpu/gc_11_5_1_pfp.bin to /lib/firmware/updates/amdgpu/gc_11_5_1_pfp.bin.amdgpu
local diversion of /lib/firmware/updates/amdgpu/gc_11_5_1_me.bin to /lib/firmware/updates/amdgpu/gc_11_5_1_me.bin.amdgpu
local diversion of /lib/firmware/updates/amdgpu/gc_11_5_1_mes1.bin to /lib/firmware/updates/amdgpu/gc_11_5_1_mes1.bin.amdgpu
local diversion of /lib/firmware/updates/amdgpu/gc_11_5_1_rlc.bin to /lib/firmware/updates/amdgpu/gc_11_5_1_rlc.bin.amdgpu
local diversion of /lib/firmware/updates/amdgpu/gc_11_5_1_imu.bin to /lib/firmware/updates/amdgpu/gc_11_5_1_imu.bin.amdgpu
imac@ai2:~$ dpkg -l | grep amdgpu-dkms
ii  amdgpu-dkms                          1:6.14.14.30100200-2226257.24.04     all          amdgpu driver in DKMS format.
ii  amdgpu-dkms-firmware                 30.10.2.0.30100200-2226257.24.04     all          firmware blobs used by amdgpu driver in DKMS format
imac@ai2:~$ cat /etc/lsb-release 
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu 24.04.3 LTS"
imac@ai2:~$ uname -a
Linux ai2 6.14.0-1014-oem #14-Ubuntu SMP PREEMPT_DYNAMIC Thu Oct  2 05:10:10 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```

---

### 评论 #38 — stormenergy91 (2025-10-28T06:43:29Z)

After extensive research, I realized the issue isn’t just related to hangs with amdgpu/ROCm, but also with Ollama. Using llamacpp yielded better results.

However, with the new [ROCm 7.9 Preview](https://rocm.docs.amd.com/en/7.9.0-preview/install/rocm.html), things seem much more stable.

In any case, I’ve started using AMD’s alternative to Ollama— [Lemonade](https://github.com/lemonade-sdk/lemonade) — which is specifically developed for gfx1151 (in the Windows version, both the GPU and NPU are utilized). They also provide a [llamacpp build with ROCm](https://github.com/lemonade-sdk/llamacpp-rocm) libraries already integrated.

On my HP Z2 Mini, I reinstalled Ubuntu 24.04, installed only the OEM kernel, and by using Lemonade’s llamacpp version with integrated ROCm, I’m able to run gpt-oss:120B like a charm.

---

### 评论 #39 — hrbigelow (2025-11-04T16:33:34Z)

Just wanted to also report that on both my MSI A16 laptop and a previous Asus ROG (which I returned) I see a symptom while typing in which occasionally, a keypress doesn't echo to the screen.  But, then the next keypress makes both of them echo.  I noticed that this has been happening more frequently after I enabled the NVIDIA GPU (where previously it was disabled).

I've also noticed periodic whole-screen or half-screen turning gray for 2-5 seconds randomly.

Could these symptoms be related to the amdgpu firmware version?

I have:

```bash
lspci | grep -E "VGA|3D|Display"
c3:00.0 VGA compatible controller: NVIDIA Corporation AD106M [GeForce RTX 4070 Max-Q / Mobile] (rev a1)
c5:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Strix [Radeon 880M / 890M] (rev c4)

cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080

uname -r
6.17.6-300.fc43.x86_64
```



---

### 评论 #40 — ndrewpj (2025-11-05T19:11:39Z)

With the latest Ubuntu 24.04.3 OEM kernel 6.14.0-1015-oem + latest firmware (https://launchpad.net/ubuntu/+source/linux-firmware/20240318.git3b128b60-0ubuntu2.20), ROCm 7.9 and latest Ollama 0.12.9 I have no hangs anymore

sudo cat /sys/kernel/debug/dri/1/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006c
MES feature version: 1, firmware version: 0x00000077


---

### 评论 #41 — ianbmacdonald (2025-11-06T22:48:58Z)

@ndrewpj You should let amdgpu-dkms-firmware bring your firmware up to 0x80 .. that 0x77 is still problematic.

---

### 评论 #42 — ndrewpj (2025-11-07T06:56:05Z)

> [@ndrewpj](https://github.com/ndrewpj) You should let amdgpu-dkms-firmware bring your firmware up to 0x80 .. that 0x77 is still problematic.

I don't have any hangs and that firmware package was the newest, also having that MES fix

---

### 评论 #43 — deific (2025-11-07T07:06:19Z)

@ndrewpj Is rocm7.9 necessary? Ollama 0.12.9 with docker?
I still encounter GPU hang when using 6.14.0-1015-OEM+latest firmware 0x00000077+rocm 7.0.2. I am trying rocm7.1.0. Rocm7.9 is a preview version, and there are concerns about other hidden issues

> > [@ndrewpj](https://github.com/ndrewpj) You should let amdgpu-dkms-firmware bring your firmware up to 0x80 .. that 0x77 is still problematic.
> 
> I don't have any hangs and that firmware package was the newest, also having that MES fix



---

### 评论 #44 — ndrewpj (2025-11-08T17:39:08Z)

> [@ndrewpj](https://github.com/ndrewpj) Is rocm7.9 necessary? Ollama 0.12.9 with docker? I still encounter GPU hang when using 6.14.0-1015-OEM+latest firmware 0x00000077+rocm 7.0.2. I am trying rocm7.1.0. Rocm7.9 is a preview version, and there are concerns about other hidden issues
> 
> > > [@ndrewpj](https://github.com/ndrewpj) You should let amdgpu-dkms-firmware bring your firmware up to 0x80 .. that 0x77 is still problematic.
> > 
> > 
> > I don't have any hangs and that firmware package was the newest, also having that MES fix

rocm 7.9 seems stable to me, yes. Ollama in docker. BUT, I was wrong in here: 0x80 firmware is the best .. the 0x77 one made two brief hangs today.

---
