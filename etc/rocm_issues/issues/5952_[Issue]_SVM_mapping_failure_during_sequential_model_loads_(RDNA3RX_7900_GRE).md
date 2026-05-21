# [Issue]:  SVM mapping failure during sequential model loads (RDNA3/RX 7900 GRE)

> **Issue #5952**
> **状态**: open
> **创建时间**: 2026-02-11T01:49:03Z
> **更新时间**: 2026-05-10T10:24:58Z
> **作者**: PsiloaxinV
> **标签**: AMD Radeon RX 7900 GRE, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5952

## 标签

- **AMD Radeon RX 7900 GRE** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- zichguan-amd

## 描述

### Problem Description

I'm currently using the nightly builds from TheRock, but this issue happens even with 7.1 and 7.2.

Note: I've also filed a bug with ComfyUI, but I think this may be more an ROCm issue since I've tried multiple ComfyUI committs and settings.

My ComfyUI WAN 2.2 Image-to-Video workflow fails consistently when transitioning between different AI models (high noise → low noise or vice versa) due to possible SVM mapping failures. The system experiences RAM exhaustion, partial VRAM loading, and eventual process termination or system crash when using FP8 models; when using GGUFs, it simply sits in the loading phase forever seemingly (the VRAM crawls up from 3gb VERY slowly). I was able to run my workflow without issues dozens of times, but now I can barely get past the first high-noise phase. The issue started within the last 3-4 days. I can get it to SOMETIMES run, but I can't pin down any rhyme or reason to when it decides to work.

Specs:

GPU: AMD Radeon RX 7900 GRE
CPU: AMD Ryzen 7 7800X3D
RAM: 32GB DDR5
Motherboard: MSI MAG B650 Tomahawk
OS: Ubuntu 25.10

I've tried:

Kernels: 6.8.0-51, 6.17.0-8, 6.17.0-12, 6.17.0-14, 6.18.7
ROCm: 7.1, 7.2, 7.3 (nightly 7.12.0a20260206)
PyTorch: 2.9.1, 2.10.0
ComfyUI: 0.11.0 through 0.12.3

I'm currently using the built-in graphics drivers and not the ones installed with amdgpu-install, but I've tested both.

dmesg:

```
[Tue Feb 10 19:23:20 2026] [drm] amdgpu kernel modesetting enabled.
[Tue Feb 10 19:23:20 2026] amdgpu: vga_switcheroo: detected switching method \_SB_.PCI0.GP17.VGA_.ATPX handle
[Tue Feb 10 19:23:20 2026] amdgpu: ATPX version 1, functions 0x00000000
[Tue Feb 10 19:23:20 2026] amdgpu: Virtual CRAT table created for CPU
[Tue Feb 10 19:23:20 2026] amdgpu: Topology: Add CPU node
[Tue Feb 10 19:23:20 2026] amdgpu: Overdrive is enabled, please disable it before reporting any bugs unrelated to overdrive.
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: enabling device (0006 -> 0007)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x744C 0x1EAE:0x790A 0xCE).
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: register mmio base: 0xF6B00000
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: register mmio size: 1048576
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 0 <common_v1_0_0> (soc21_common)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 1 <gmc_v11_0_0> (gmc_v11_0)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 2 <ih_v6_0_0> (ih_v6_0)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 3 <psp_v13_0_0> (psp)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 4 <smu_v13_0_0> (smu)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 5 <dce_v1_0_0> (dm)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 6 <gfx_v11_0_0> (gfx_v11_0)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 7 <sdma_v6_0_0> (sdma_v6_0)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 8 <vcn_v4_0_0> (vcn_v4_0)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0_0> (jpeg_v4_0)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: detected ip block number 10 <mes_v11_0_0> (mes_v11_0)
[Tue Feb 10 19:23:20 2026] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from VFCT
[Tue Feb 10 19:23:20 2026] amdgpu: ATOM BIOS: 113-EXT91535-100
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: CP RS64 enable
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: vgaarb: deactivate vga console
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: MEM ECC is not presented.
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: SRAM ECC is not presented.
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: VRAM: 16368M 0x0000008000000000 - 0x00000083FEFFFFFF (16368M used)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: amdgpu: 16368M of VRAM memory ready
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: amdgpu: 15335M of GTT memory ready.
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x07002F00
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 22
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [VCN instance 1] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 22
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: reserve 0x1300000 from 0x83fc000000 for PSP TMR
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8200 (78.130.0)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: SMU is initialized successfully!
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] Display Core v3.2.351 initialized on DCN 3.2
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002F00
[Tue Feb 10 19:23:21 2026] snd_hda_intel 0000:03:00.1: bound 0000:03:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] DP-1: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] DP-2: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] DP-3: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] HDMI-A-1: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu: HMM registered 16368MB device memory
[Tue Feb 10 19:23:21 2026] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[Tue Feb 10 19:23:21 2026] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[Tue Feb 10 19:23:21 2026] amdgpu: Virtual CRAT table created for GPU
[Tue Feb 10 19:23:21 2026] amdgpu: Topology: Add dGPU node [0x744c:0x1002]
[Tue Feb 10 19:23:21 2026] kfd kfd: amdgpu: added device 1002:744c
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: SE 6, SH per SE 2, CU per SH 8, active_cu_number 80
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: Using BACO for runtime pm
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: [drm] Registered 4 planes with drm panic
[Tue Feb 10 19:23:21 2026] [drm] Initialized amdgpu 3.64.0 for 0000:03:00.0 on minor 1
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: amdgpu: [drm] Failed to setup vendor infoframe on connector HDMI-A-1: -22
[Tue Feb 10 19:23:21 2026] fbcon: amdgpudrmfb (fb0) is primary device
[Tue Feb 10 19:23:21 2026] amdgpu 0000:03:00.0: [drm] fb0: amdgpudrmfb frame buffer device
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: enabling device (0006 -> 0007)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x164E 0x1462:0x7D75 0xCB).
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: register mmio base: 0xF6A00000
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: register mmio size: 524288
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 0 <common_v1_0_0> (nv_common)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 1 <gmc_v10_0_0> (gmc_v10_0)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 2 <ih_v5_0_0> (navi10_ih)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 3 <psp_v13_0_0> (psp)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 4 <smu_v13_0_0> (smu)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 5 <dce_v1_0_0> (dm)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 6 <gfx_v10_0_0> (gfx_v10_0)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 7 <sdma_v5_2_0> (sdma_v5_2)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 8 <vcn_v3_0_0> (vcn_v3_0)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: detected ip block number 9 <jpeg_v3_0_0> (jpeg_v3_0)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: Fetched VBIOS from VFCT
[Tue Feb 10 19:23:21 2026] amdgpu: ATOM BIOS: 102-RAPHAEL-008
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: VRAM: 512M 0x000000F400000000 - 0x000000F41FFFFFFF (512M used)
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: GART: 1024M 0x0000000000000000 - 0x000000003FFFFFFF
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: amdgpu: 512M of VRAM memory ready
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: amdgpu: 15335M of GTT memory ready.
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x05002A00
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.33 DEC: 4 VEP: 0 Revision: 12
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: reserve 0xa00000 from 0xf41e000000 for PSP TMR
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: RAS: optional ras ta ucode is not available
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: RAP: optional rap ta ucode is not available
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: SMU is initialized successfully!
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] Display Core v3.2.351 initialized on DCN 3.1.5
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x05002A00
[Tue Feb 10 19:23:21 2026] snd_hda_intel 0000:12:00.1: bound 0000:12:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] HDMI-A-2: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] DP-4: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] DP-5: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: [drm] DP-6: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: kiq ring mec 2 pipe 1 q 0
[Tue Feb 10 19:23:21 2026] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[Tue Feb 10 19:23:21 2026] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[Tue Feb 10 19:23:21 2026] amdgpu: Virtual CRAT table created for GPU
[Tue Feb 10 19:23:21 2026] amdgpu: Topology: Add dGPU node [0x164e:0x1002]
[Tue Feb 10 19:23:21 2026] kfd kfd: amdgpu: added device 1002:164e
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: SE 1, SH per SE 1, CU per SH 2, active_cu_number 2
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: amdgpu: Runtime PM not available
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: [drm] Registered 4 planes with drm panic
[Tue Feb 10 19:23:21 2026] [drm] Initialized amdgpu 3.64.0 for 0000:12:00.0 on minor 0
[Tue Feb 10 19:23:21 2026] amdgpu 0000:12:00.0: [drm] Cannot find any crtc or sizes
[Tue Feb 10 19:23:31 2026] workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:23:31 2026] workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:23:32 2026] workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:23:32 2026] workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:27:11 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:27:11 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:27:11 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:27:12 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:27:14 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 19 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:31:42 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 35 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:32:03 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 67 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:34:57 2026] workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:34:58 2026] workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:35:31 2026] workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:35:34 2026] workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 131 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:37:42 2026] workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
[Tue Feb 10 19:43:40 2026] amdgpu: Freeing queue vital buffer 0x7fc107400000, queue evicted
[Tue Feb 10 19:43:40 2026] amdgpu: Freeing queue vital buffer 0x7fc109a00000, queue evicted

```

sudo journalctl -k -b -0 | grep -iE "amdgpu|ring|timeout|mes|kfd|reset"

```
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: Command line: BOOT_IMAGE=/boot/vmlinuz-6.18.7-061807-generic root=UUID=496c7494-fdff-4521-9069-60d99636feb1 ro quiet splash fsck.mode=force nvme_load=YES amdgpu.ppfeaturemask=0xffffffff amdgpu.cwsr_enable=0 crashkernel=2G-4G:320M,4G-32G:512M,32G-64G:1024M,64G-128G:2048M,128G-:4096M vt.handoff=7
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: Kernel command line: BOOT_IMAGE=/boot/vmlinuz-6.18.7-061807-generic root=UUID=496c7494-fdff-4521-9069-60d99636feb1 ro quiet splash fsck.mode=force nvme_load=YES amdgpu.ppfeaturemask=0xffffffff amdgpu.cwsr_enable=0 crashkernel=2G-4G:320M,4G-32G:512M,32G-64G:1024M,64G-128G:2048M,128G-:4096M vt.handoff=7
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: NMI watchdog: Enabled. Permanently consumes one hw-PMU counter.
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: smp: Bringing up secondary CPUs ...
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: ACPI: PM: Registering ACPI NVS region [mem 0x0a200000-0x0a20ffff] (65536 bytes)
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: ACPI: PM: Registering ACPI NVS region [mem 0xad47f000-0xaf47efff] (33554432 bytes)
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: PCI: Ignoring E820 reservations for host bridge windows
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: PCI-DMA: Using software bounce buffering for IO (SWIOTLB)
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: Initialise system trusted keyrings
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: workingset: timestamp_bits=36 max_order=23 bucket_order=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: integrity: Platform Keyring initialized
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: integrity: Machine keyring initialized
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: Estimated ratio of average max frequency by base frequency (times 1024): 1127
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: Serial: 8250/16550 driver, 32 ports, IRQ sharing enabled
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb usb2: New USB device strings: Mfr=3, Product=2, SerialNumber=1
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb usb3: New USB device strings: Mfr=3, Product=2, SerialNumber=1
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb usb4: New USB device strings: Mfr=3, Product=2, SerialNumber=1
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb usb5: New USB device strings: Mfr=3, Product=2, SerialNumber=1
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb usb6: New USB device strings: Mfr=3, Product=2, SerialNumber=1
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb usb7: New USB device strings: Mfr=3, Product=2, SerialNumber=1
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: fbcon: Deferring console take-over
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: x86/amd: Previous system reset reason [0x01000800]: system failed to boot before failed boot timer expired
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: resctrl: L3 monitoring detected
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: r8169 0000:0e:00.0 eth0: jumbo features [frames: 16362 bytes, tx checksumming: ko]
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 5-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 6-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 1-5: New USB device strings: Mfr=2, Product=3, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 2-5: New USB device strings: Mfr=2, Product=3, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 5-1.1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 1-5.1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 1-6: New USB device strings: Mfr=3, Product=1, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 5-1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 1-10: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: usb 1-12: New USB device strings: Mfr=0, Product=1, SerialNumber=0
Feb 10 19:23:19 vsekar92-MS-7D75 systemd[1]: Reached target integritysetup.target - Local Integrity Protected Volumes.
Feb 10 19:23:19 vsekar92-MS-7D75 systemd[1]: Reached target veritysetup.target - Local Verity Protected Volumes.
Feb 10 19:23:19 vsekar92-MS-7D75 systemd[1]: Mounting dev-mqueue.mount - POSIX Message Queue File System...
Feb 10 19:23:19 vsekar92-MS-7D75 systemd[1]: Mounted dev-mqueue.mount - POSIX Message Queue File System.
Feb 10 19:23:19 vsekar92-MS-7D75 systemd-journald[671]: Collecting audit messages is disabled.
Feb 10 19:23:19 vsekar92-MS-7D75 kernel: bridge: filtering via arp/ip/ip6tables is no longer available by default. Update your scripts to load br_netfilter if you need this.
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: [drm] amdgpu kernel modesetting enabled.
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu: vga_switcheroo: detected switching method \_SB_.PCI0.GP17.VGA_.ATPX handle
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu: ATPX version 1, functions 0x00000000
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu: Virtual CRAT table created for CPU
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu: Topology: Add CPU node
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu: Overdrive is enabled, please disable it before reporting any bugs unrelated to overdrive.
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: enabling device (0006 -> 0007)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x744C 0x1EAE:0x790A 0xCE).
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: register mmio base: 0xF6B00000
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: register mmio size: 1048576
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 0 <common_v1_0_0> (soc21_common)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 1 <gmc_v11_0_0> (gmc_v11_0)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 2 <ih_v6_0_0> (ih_v6_0)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 3 <psp_v13_0_0> (psp)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 4 <smu_v13_0_0> (smu)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 5 <dce_v1_0_0> (dm)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 6 <gfx_v11_0_0> (gfx_v11_0)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 7 <sdma_v6_0_0> (sdma_v6_0)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 8 <vcn_v4_0_0> (vcn_v4_0)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0_0> (jpeg_v4_0)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: detected ip block number 10 <mes_v11_0_0> (mes_v11_0)
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from VFCT
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu: ATOM BIOS: 113-EXT91535-100
Feb 10 19:23:20 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: CP RS64 enable
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: vgaarb: deactivate vga console
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: MEM ECC is not presented.
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: SRAM ECC is not presented.
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: VRAM: 16368M 0x0000008000000000 - 0x00000083FEFFFFFF (16368M used)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: amdgpu: 16368M of VRAM memory ready
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: amdgpu: 15335M of GTT memory ready.
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x07002F00
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 22
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [VCN instance 1] Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 22
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: reserve 0x1300000 from 0x83fc000000 for PSP TMR
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8200 (78.130.0)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: SMU is initialized successfully!
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Display Core v3.2.351 initialized on DCN 3.2
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x07002F00
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: snd_hda_intel 0000:03:00.1: bound 0000:03:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DP-1: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DP-2: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] DP-3: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] HDMI-A-1: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu: HMM registered 16368MB device memory
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: kfd kfd: amdgpu: Allocated 3969056 bytes on gart
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu: Virtual CRAT table created for GPU
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu: Topology: Add dGPU node [0x744c:0x1002]
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: kfd kfd: amdgpu: added device 1002:744c
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: SE 6, SH per SE 2, CU per SH 8, active_cu_number 80
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: Using BACO for runtime pm
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: [drm] Registered 4 planes with drm panic
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: [drm] Initialized amdgpu 3.64.0 for 0000:03:00.0 on minor 1
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Failed to setup vendor infoframe on connector HDMI-A-1: -22
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: fbcon: amdgpudrmfb (fb0) is primary device
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: fbcon: Deferring console take-over
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:03:00.0: [drm] fb0: amdgpudrmfb frame buffer device
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: enabling device (0006 -> 0007)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: initializing kernel modesetting (IP DISCOVERY 0x1002:0x164E 0x1462:0x7D75 0xCB).
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: register mmio base: 0xF6A00000
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: register mmio size: 524288
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 0 <common_v1_0_0> (nv_common)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 1 <gmc_v10_0_0> (gmc_v10_0)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 2 <ih_v5_0_0> (navi10_ih)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 3 <psp_v13_0_0> (psp)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 4 <smu_v13_0_0> (smu)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 5 <dce_v1_0_0> (dm)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 6 <gfx_v10_0_0> (gfx_v10_0)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 7 <sdma_v5_2_0> (sdma_v5_2)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 8 <vcn_v3_0_0> (vcn_v3_0)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: detected ip block number 9 <jpeg_v3_0_0> (jpeg_v3_0)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: Fetched VBIOS from VFCT
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu: ATOM BIOS: 102-RAPHAEL-008
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: VRAM: 512M 0x000000F400000000 - 0x000000F41FFFFFFF (512M used)
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: GART: 1024M 0x0000000000000000 - 0x000000003FFFFFFF
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: amdgpu: 512M of VRAM memory ready
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: amdgpu: 15335M of GTT memory ready.
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x05002A00
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [VCN instance 0] Found VCN firmware Version ENC: 1.33 DEC: 4 VEP: 0 Revision: 12
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: reserve 0xa00000 from 0xf41e000000 for PSP TMR
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: RAS: optional ras ta ucode is not available
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: RAP: optional rap ta ucode is not available
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: SMU is initialized successfully!
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] Display Core v3.2.351 initialized on DCN 3.1.5
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x05002A00
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: snd_hda_intel 0000:12:00.1: bound 0000:12:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] HDMI-A-2: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] DP-4: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] DP-5: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: [drm] DP-6: PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: kiq ring mec 2 pipe 1 q 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: kfd kfd: amdgpu: Allocated 3969056 bytes on gart
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu: Virtual CRAT table created for GPU
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu: Topology: Add dGPU node [0x164e:0x1002]
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: kfd kfd: amdgpu: added device 1002:164e
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: SE 1, SH per SE 1, CU per SH 2, active_cu_number 2
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: amdgpu: Runtime PM not available
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: [drm] Registered 4 planes with drm panic
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: [drm] Initialized amdgpu 3.64.0 for 0000:12:00.0 on minor 0
Feb 10 19:23:21 vsekar92-MS-7D75 kernel: amdgpu 0000:12:00.0: [drm] Cannot find any crtc or sizes
Feb 10 19:23:31 vsekar92-MS-7D75 kernel: workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
Feb 10 19:23:31 vsekar92-MS-7D75 kernel: workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
Feb 10 19:23:32 vsekar92-MS-7D75 kernel: workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
Feb 10 19:23:32 vsekar92-MS-7D75 kernel: workqueue: dm_handle_vmin_vmax_update [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
Feb 10 19:23:44 vsekar92-MS-7D75 kernel: usb 6-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
Feb 10 19:23:54 vsekar92-MS-7D75 kernel: usb 5-1.2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Feb 10 19:27:10 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
Feb 10 19:27:11 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
Feb 10 19:27:11 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
Feb 10 19:27:11 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
Feb 10 19:27:13 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 19 times, consider switching to WQ_UNBOUND
Feb 10 19:31:41 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 35 times, consider switching to WQ_UNBOUND
Feb 10 19:32:02 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 67 times, consider switching to WQ_UNBOUND
Feb 10 19:34:56 vsekar92-MS-7D75 kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 4 times, consider switching to WQ_UNBOUND
Feb 10 19:34:57 vsekar92-MS-7D75 kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 5 times, consider switching to WQ_UNBOUND
Feb 10 19:35:30 vsekar92-MS-7D75 kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 7 times, consider switching to WQ_UNBOUND
Feb 10 19:35:33 vsekar92-MS-7D75 kernel: workqueue: svm_range_restore_work [amdgpu] hogged CPU for >10000us 131 times, consider switching to WQ_UNBOUND
Feb 10 19:37:41 vsekar92-MS-7D75 kernel: workqueue: amdgpu_amdkfd_restore_userptr_worker [amdgpu] hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
Feb 10 19:43:40 vsekar92-MS-7D75 kernel: amdgpu: Freeing queue vital buffer 0x7fc107400000, queue evicted
Feb 10 19:43:40 vsekar92-MS-7D75 kernel: amdgpu: Freeing queue vital buffer 0x7fc109a00000, queue evicted
```


### Operating System

Ubuntu 25.10

### CPU

AMD Ryzen 7800X3D

### GPU

RX 7900 GRE

### ROCm Version

7.x

### ROCm Component

_No response_

### Steps to Reproduce

1) Run any Wan2.2 I2V workflow
2) High noise sampler will run normally
3) The workflow never starts sampling in the low noise sampler - ComfyUI gets killed due to OOM or system crash if using fp8/fp16 models, or it just stays stuck loading the model into VRAM if using GGUF.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

```
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.16
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
  Name:                    AMD Ryzen 7 7800X3D 8-Core Processor
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 7 7800X3D 8-Core Processor
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
  Max Clock Freq. (MHz):   5053                               
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
      Size:                    31406488(0x1df3998) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31406488(0x1df3998) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    31406488(0x1df3998) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31406488(0x1df3998) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-2d9493875069a81b               
  Marketing Name:          AMD Radeon RX 7900 GRE             
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
    L3:                      65536(0x10000) KB                  
  Chip ID:                 29772(0x744c)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2052                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            80                                 
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 602                                
  SDMA engine uCode::      27                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
  Name:                    gfx1036                            
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
  Node:                    2                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      256(0x100) KB                      
  Chip ID:                 5710(0x164e)                       
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2200                               
  BDFID:                   4608                               
  Internal Node ID:        2                                  
  Compute Unit:            2                                  
  SIMDs per CU:            2                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
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
  Packet Processor uCode:: 26                                 
  SDMA engine uCode::      9                                  
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    15703244(0xef9ccc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    15703244(0xef9ccc) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1036         
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
      Name:                    amdgcn-amd-amdhsa--gfx10-3-generic 
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
### Additional Information

_No response_

---

## 评论 (14 条)

### 评论 #1 — zichguan-amd (2026-02-11T19:45:30Z)

Hi @PsiloaxinV, I was able to run https://docs.comfy.org/tutorials/video/wan/wan2_2#wan2-2-14b-i2v-image-to-video-workflow-example on gfx1100 with `torch==2.10.0+rocm7.12.0a20260206` (therock wheels) on ubuntu 24.04 kernel 6.8.0-41 with the in-kernel driver `amdgpu/6.16.6-2234103.24.04`, producing a complete 5s video as expected. Do note that it took me ~50G ram and ~20G vram, if your system has less memory available, it could be just running oom. The 7900 GRE has only 16G of vram. Can you provide error logs with `AMD_LOG_LEVEL=5` when the workload crashes? Please also include any environment variables and ComfyUI flags used.

---

### 评论 #2 — PsiloaxinV (2026-02-11T20:27:25Z)

Hey @zichguan-amd, I do not think it is an issue with lack of RAM/VRAM. I've run the same resolutions and frame counts dozens of times - this is a recent issue, and it actually does work *sometimes* (I still don't know what the condition for this is). For the fp8_scaled models, when it's working,  RAM usage always clears to around 8-12gb after high noise before loading the next model. When it fails, it sits at 23-24 gb (so the memory never gets cleared?), RAM and Swap fill up completely, and the process eventually gets killed by gnome. VRAM does get cleared before it tries to load the second model.

The behavior with GGUFs is different, but it ultimately still hangs at the second model load. VRAM gets properly cleared and fills to a certain extent (3-7 gb usually) before stalling at the load phase. As far as I can tell it is still trying to load into VRAM, just very, very slowly. 

Here are the logs with AMD_LOG_LEVEL=5. The snippet is from when it was stalling during the low noise model load. I used  Q6_K ggufs.


```
:5:hip_device.cpp           :36  : 38362352065 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38362352071 us: [pid:309675 tid: 0x73e303fff6c0] Command (CopyHostToDevice) enqueued: 0x73e22159fe90 to queue: 0x73e2ec01cb20
:5:rocvirtual.cpp           :1594: 38362352077 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x73e4ce7ddc80, rptr=638183, wptr=638183
:5:rocblit.cpp              :681 : 38362352082 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy Using Staging resource size 27648
:5:rocblit.cpp              :727 : 38362352086 us: [pid:309675 tid: 0x73e303fff6c0] memcpy stg buf=0x73e294ef7c00, host src=0x73d5d26ea468, size=27648
:4:rocblit.cpp              :731 : 38362352575 us: [pid:309675 tid: 0x73e303fff6c0] HSA Async Copy staged H2D, Async=1
:4:rocblit.cpp              :521 : 38362352579 us: [pid:309675 tid: 0x73e303fff6c0] Using assigned SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2
:4:rocblit.cpp              :556 : 38362352584 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy copy_engine=0x1, dst=0x73e31b861000, src=0x73e294ef7c00, size=27648, forceSDMA=0, engineType=2, wait_event=0x0, completion_signal=0x73e4ce7e1c80
:3:hip_memory.cpp           :1619: 38362352590 us: [pid:309675 tid: 0x73e303fff6c0] hipMemcpyAsync: Returned hipSuccess : : duration: 529 us
:3:hip_device_runtime.cpp   :779 : 38362352595 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352597 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362352602 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc944 ) 
:3:hip_device_runtime.cpp   :705 : 38362352605 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352608 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc28c ) 
:3:hip_device_runtime.cpp   :705 : 38362352611 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352614 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc2cc ) 
:3:hip_device_runtime.cpp   :705 : 38362352616 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38362352621 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {7,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38362352625 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38362352629 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {0,0,0}, {0,0,0}, 0x73e303ffc508, 0x73e303ffc4f8 ) 
:3:hip_platform.cpp         :284 : 38362352633 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38362352638 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bd75e0, {7,1,1}, {256,1,1}, 0x73e303ffc530, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38362352643 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38362352647 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e2213ee450 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38362352651 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38362352653 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x0 (size:0x1)
:4:rocvirtual.cpp           :981 : 38362352657 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 38 85 1b e3 73 00 00 00 10 86 1b e3 73 00 00  (size:0x10)
:3:rocvirtual.cpp           :3668: 38362352661 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::bfloat16tofloat32_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(c10::BFloat16)#1}, std::array<char*, 2ul> >(int, at::native::bfloat16tofloat32_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(c10::BFloat16)#1}, std::array<char*, 2ul>)
:5:rocvirtual.cpp           :3867: 38362352667 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 24 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1208: 38362352672 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0x1502 (type=2, barrier=1, acquire=2, release=2), setup=3, grid=[1792, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e18aa72f80, kernarg_address=0x73e2a4a01580, completion_signal=0x0, correlation_id=0, rptr=638184, wptr=638184
:3:hip_module.cpp           :827 : 38362352678 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 40 us
:3:hip_error.cpp            :34  : 38362352682 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_error.cpp            :34  : 38362352685 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38362352688 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352691 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38362352696 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352698 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362352715 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd48c ) 
:3:hip_device_runtime.cpp   :705 : 38362352718 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352721 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd184 ) 
:3:hip_device_runtime.cpp   :705 : 38362352724 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352727 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffceac ) 
:3:hip_device_runtime.cpp   :705 : 38362352730 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38362352734 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352736 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362352743 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd13c ) 
:3:hip_device_runtime.cpp   :705 : 38362352745 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352748 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd17c ) 
:3:hip_device_runtime.cpp   :705 : 38362352750 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38362352754 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {14,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38362352757 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38362352762 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {67097768,29667,589796994}, {0,0,926328864}, 0x73e303ffd3a8, 0x73e303ffd370 ) 
:3:hip_platform.cpp         :284 : 38362352765 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38362352770 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bd40e8, {14,1,1}, {256,1,1}, 0x73e303ffd3d0, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38362352774 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38362352777 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e221478fe0 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38362352781 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38362352784 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x3f800000def87540 (size:0x8)
:4:rocvirtual.cpp           :981 : 38362352787 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 10 86 1b e3 73 00 00 00 38 85 1b e3 73 00 00  (size:0x10)
:3:rocvirtual.cpp           :3668: 38362352791 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::AUnaryFunctor<float, float, float, at::native::binary_internal::MulFunctor<float> >, std::array<char*, 2ul> >(int, at::native::AUnaryFunctor<float, float, float, at::native::binary_internal::MulFunctor<float> >, std::array<char*, 2ul>)
:5:rocvirtual.cpp           :3867: 38362352797 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 32 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1208: 38362352802 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[3584, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e29444ae40, kernarg_address=0x73e2a4a01600, completion_signal=0x0, correlation_id=0, rptr=638185, wptr=638185
:3:hip_module.cpp           :827 : 38362352808 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 38 us
:3:hip_error.cpp            :34  : 38362352812 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38362352814 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352817 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362352831 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc80c ) 
:3:hip_device_runtime.cpp   :705 : 38362352834 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352839 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc44c ) 
:3:hip_device_runtime.cpp   :705 : 38362352842 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352844 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc48c ) 
:3:hip_device_runtime.cpp   :705 : 38362352847 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38362352851 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {14,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38362352854 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38362352858 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {2,0,1}, {1,0,3}, 0x73e303ffc6c8, 0x73e303ffc6b8 ) 
:3:hip_platform.cpp         :284 : 38362352862 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38362352868 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bbace0, {14,1,1}, {256,1,1}, 0x73e303ffc6f0, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38362352873 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38362352876 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e21eb8b160 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38362352880 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38362352883 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x3f800000 (size:0x4)
:4:rocvirtual.cpp           :981 : 38362352887 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 d8 80 1b e3 73 00 00 00 d8 80 1b e3 73 00 00 00 10 86 1b e3 73 00 00  (size:0x18)
:3:rocvirtual.cpp           :3668: 38362352891 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::CUDAFunctor_add<float>, std::array<char*, 3ul> >(int, at::native::CUDAFunctor_add<float>, std::array<char*, 3ul>)
:5:rocvirtual.cpp           :3867: 38362352896 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 32 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1208: 38362352900 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[3584, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e1e8265700, kernarg_address=0x73e2a4a01680, completion_signal=0x0, correlation_id=0, rptr=638186, wptr=638186
:3:hip_module.cpp           :827 : 38362352907 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 39 us
:3:hip_error.cpp            :34  : 38362352910 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38362352913 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352916 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362352935 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc284 ) 
:3:hip_device_runtime.cpp   :705 : 38362352938 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352940 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc144 ) 
:3:hip_device_runtime.cpp   :705 : 38362352943 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352945 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbfac ) 
:3:hip_device_runtime.cpp   :705 : 38362352948 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38362352952 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352954 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38362352957 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362352960 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362352963 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbef4 ) 
:3:hip_device_runtime.cpp   :705 : 38362352966 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352969 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffb83c ) 
:3:hip_device_runtime.cpp   :705 : 38362352972 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362352974 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffb87c ) 
:3:hip_device_runtime.cpp   :705 : 38362352977 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38362352980 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {7,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38362352984 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38362352988 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {67091248,29667,406109151}, {67091472,29667,265927800}, 0x73e303ffbab8, 0x73e303ffbaa8 ) 
:3:hip_platform.cpp         :284 : 38362352992 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38362352996 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bd7580, {7,1,1}, {256,1,1}, 0x73e303ffbae0, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38362353006 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38362353009 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e21eb9d5c0 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38362353014 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38362353016 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x4a (size:0x1)
:4:rocvirtual.cpp           :981 : 38362353020 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 38 85 1b e3 73 00 00 00 d8 80 1b e3 73 00 00  (size:0x10)
:3:rocvirtual.cpp           :3668: 38362353024 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::float16_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(float)#1}, std::array<char*, 2ul> >(int, at::native::float16_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(float)#1}, std::array<char*, 2ul>)
:5:rocvirtual.cpp           :3867: 38362353029 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 24 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1208: 38362353034 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[1792, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e18aa72c80, kernarg_address=0x73e2a4a01700, completion_signal=0x0, correlation_id=0, rptr=638187, wptr=638187
:3:hip_module.cpp           :827 : 38362353040 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 44 us
:3:hip_error.cpp            :34  : 38362353044 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_error.cpp            :34  : 38362353047 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38362353050 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362353053 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362353113 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc214 ) 
:3:hip_device_runtime.cpp   :705 : 38362353116 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362353734 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc0d4 ) 
:3:hip_device_runtime.cpp   :705 : 38362353736 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362353739 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbf3c ) 
:3:hip_device_runtime.cpp   :705 : 38362353742 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38362353748 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362353751 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38362353753 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38362353755 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38362353760 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbe74 ) 
:3:hip_device_runtime.cpp   :705 : 38362353763 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38362353765 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbc8c ) 
:3:hip_device_runtime.cpp   :705 : 38362353768 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 38362353773 us: [pid:309675 tid: 0x73e303fff6c0]  hipStreamGetCaptureInfo ( char array:<null>, 0x73e303ffbe7c, char array:<null> ) 
:3:hip_graph.cpp            :2062: 38362353777 us: [pid:309675 tid: 0x73e303fff6c0] hipStreamGetCaptureInfo: Returned hipSuccess : 
:3:hip_memory.cpp           :827 : 38362353783 us: [pid:309675 tid: 0x73e303fff6c0]  hipMemcpyWithStream ( 0x73dda7b7c000, 0x73d8e5768d80, 58060800, hipMemcpyHostToDevice, char array:<null> ) 
:5:hip_device.cpp           :36  : 38362353787 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38362353793 us: [pid:309675 tid: 0x73e303fff6c0] Command (CopyHostToDevice) enqueued: 0x73e20a19d340 to queue: 0x73e2ec01cb20
:5:rocvirtual.cpp           :1594: 38362353799 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x73e4ce7df780, rptr=638188, wptr=638188
:4:rocdevice.cpp            :2113: 38362394742 us: [pid:309675 tid: 0x73e303fff6c0] Locking to pool 0xde6cc00, size 0x2001000, hostMem = 0x73d8e5768000, deviceMemory = 0x73d8e5768000, memSegment = 0
:5:rocblit.cpp              :670 : 38362394751 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy Using Pinned resource size 33554432
:4:rocblit.cpp              :731 : 38362394756 us: [pid:309675 tid: 0x73e303fff6c0] HSA Async Copy staged H2D, Async=0
:4:rocblit.cpp              :521 : 38362394763 us: [pid:309675 tid: 0x73e303fff6c0] Using assigned SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2
:4:rocblit.cpp              :556 : 38362394769 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy copy_engine=0x1, dst=0x73dda7b7c000, src=0x73d8e5768d80, size=33554432, forceSDMA=0, engineType=2, wait_event=0x0, completion_signal=0x73e4ce7e0f80
:4:rocdevice.cpp            :2113: 38362457161 us: [pid:309675 tid: 0x73e303fff6c0] Locking to pool 0xde6cc00, size 0x1760000, hostMem = 0x73d8e7768000, deviceMemory = 0x73d8e7768000, memSegment = 0
:5:rocblit.cpp              :670 : 38362457169 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy Using Pinned resource size 24506368
:4:rocblit.cpp              :731 : 38362457173 us: [pid:309675 tid: 0x73e303fff6c0] HSA Async Copy staged H2D, Async=0
:4:rocblit.cpp              :521 : 38362457180 us: [pid:309675 tid: 0x73e303fff6c0] Using assigned SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2
:4:rocblit.cpp              :556 : 38362457184 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy copy_engine=0x1, dst=0x73dda9b7c000, src=0x73d8e7768d80, size=24506368, forceSDMA=0, engineType=2, wait_event=0x73e4ce7e0f80, completion_signal=0x73e4ce7e2780
:4:rocvirtual.cpp           :714 : 38362457190 us: [pid:309675 tid: 0x73e303fff6c0] Host wait on completion_signal=0x73e4ce7e2780
:3:hip_memory.cpp           :844 : 38370560630 us: [pid:309675 tid: 0x73e303fff6c0] hipMemcpyWithStream: Returned hipSuccess : : duration: 8206847 us
:3:hip_device_runtime.cpp   :779 : 38370560647 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370560650 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38370560824 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd9bc ) 
:3:hip_device_runtime.cpp   :705 : 38370560828 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370560832 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffda1c ) 
:3:hip_device_runtime.cpp   :705 : 38370560835 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :677 : 38370560841 us: [pid:309675 tid: 0x73e303fff6c0]  hipDeviceSynchronize (  ) 
:5:commandqueue.cpp         :189 : 38370560844 us: [pid:309675 tid: 0x73e303fff6c0] finish() called with batch size: 8, cpu_wait: 0, fence dirty: 0
:5:command.cpp              :354 : 38370560850 us: [pid:309675 tid: 0x73e303fff6c0] Command (InternalMarker) enqueued: 0x73e2237d6a50 to queue: 0x73e2ec01cb20
:3:rocvirtual.cpp           :640 : 38370560865 us: [pid:309675 tid: 0x73e303fff6c0] Set Handler: handle(0x73e4ce7f4800), timestamp(0x73e265090250), blocking CB=0
:5:rocvirtual.cpp           :1594: 38370560872 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x73e4ce7f4800, rptr=638189, wptr=638189
:4:rocdevice.cpp            :3761: 38370560951 us: [pid:309675 tid: 0x73e303fff6c0] Released SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1
:4:commandqueue.cpp         :236 : 38370560955 us: [pid:309675 tid: 0x73e303fff6c0] All commands finished for host queue : 0x73e2ec01cb20
:3:hip_device_runtime.cpp   :681 : 38370560961 us: [pid:309675 tid: 0x73e303fff6c0] hipDeviceSynchronize: Returned hipSuccess : : duration: 120 us
:3:hip_device_runtime.cpp   :693 : 38370560967 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffda1c ) 
:3:hip_device_runtime.cpp   :705 : 38370560970 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:rocvirtual.cpp           :304 : 38370560955 us: [pid:309675 tid: 0x73e4ce5ff6c0] Handler: value(0), timestamp(0x73e20fdc8000), handle(0x73e4ce7f4800)
:5:command.cpp              :166 : 38370560982 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e21e6b2140 complete
:5:command.cpp              :166 : 38370560988 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e2214399e0 complete
:5:command.cpp              :166 : 38370560993 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e22159fe90 complete
:5:command.cpp              :166 : 38370560997 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e2213ee450 complete
:5:command.cpp              :166 : 38370561005 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e221478fe0 complete
:5:command.cpp              :166 : 38370561009 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e21eb8b160 complete
:5:command.cpp              :166 : 38370561013 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e21eb9d5c0 complete
:5:command.cpp              :166 : 38370561016 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e20a19d340 complete
:5:command.cpp              :164 : 38370561027 us: [pid:309675 tid: 0x73e4ce5ff6c0] Command 0x73e2237d6a50 complete (Wall: 68047876632, CPU: 0, GPU: 36 us)
:3:hip_device_runtime.cpp   :693 : 38370561155 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffcb04 ) 
:3:hip_device_runtime.cpp   :705 : 38370561160 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561164 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc9c4 ) 
:3:hip_device_runtime.cpp   :705 : 38370561167 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561172 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc82c ) 
:3:hip_device_runtime.cpp   :705 : 38370561175 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38370561185 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561188 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38370561191 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561193 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38370561204 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd084 ) 
:3:hip_device_runtime.cpp   :705 : 38370561207 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561223 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbf44 ) 
:3:hip_device_runtime.cpp   :705 : 38370561226 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561229 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbe44 ) 
:3:hip_device_runtime.cpp   :705 : 38370561232 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561235 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbb6c ) 
:3:hip_device_runtime.cpp   :705 : 38370561238 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38370561242 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561244 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38370561247 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561250 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38370561262 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbd64 ) 
:3:hip_device_runtime.cpp   :705 : 38370561264 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561268 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbb7c ) 
:3:hip_device_runtime.cpp   :705 : 38370561271 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_memory.cpp           :1618: 38370561278 us: [pid:309675 tid: 0x73e303fff6c0]  hipMemcpyAsync ( 0x73e31b85a400, 0x73d8d4458d80, 27648, hipMemcpyHostToDevice, char array:<null> ) 
:5:hip_device.cpp           :36  : 38370561283 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38370561291 us: [pid:309675 tid: 0x73e303fff6c0] Command (CopyHostToDevice) enqueued: 0x73e1f61e9a80 to queue: 0x73e2ec01cb20
:5:rocblit.cpp              :681 : 38370561297 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy Using Staging resource size 27648
:5:rocvirtual.cpp           :1962: 38370561300 us: [pid:309675 tid: 0x73e303fff6c0] Issue barrier to flush chunk 6
:5:rocvirtual.cpp           :1594: 38370561305 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x73e4ce7fcc80, rptr=638190, wptr=638190
:5:rocblit.cpp              :727 : 38370561311 us: [pid:309675 tid: 0x73e303fff6c0] memcpy stg buf=0x73e294f00000, host src=0x73d8d4458d80, size=27648
:4:rocblit.cpp              :731 : 38370561532 us: [pid:309675 tid: 0x73e303fff6c0] HSA Async Copy staged H2D, Async=1
:4:rocdevice.cpp            :3691: 38370561541 us: [pid:309675 tid: 0x73e303fff6c0] Engine query for VirtualGPU 0x73e2ec02d280: status=0, free_mask=0x3, preferred_mask=0x0, valid_mask=0x3, engine_type=2
:3:rocdevice.cpp            :3748: 38370561547 us: [pid:309675 tid: 0x73e303fff6c0] Assigned SDMA engine to VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2, valid_mask=0x3, preferred_mask=0x0, allocated_mask=0x0, is_inter_gpu=0
:3:rocblit.cpp              :532 : 38370561551 us: [pid:309675 tid: 0x73e303fff6c0] Allocated new SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2
:4:rocblit.cpp              :556 : 38370561555 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy copy_engine=0x1, dst=0x73e31b85a400, src=0x73e294f00000, size=27648, forceSDMA=0, engineType=2, wait_event=0x0, completion_signal=0x73e4ce7de280
:3:hip_memory.cpp           :1619: 38370561563 us: [pid:309675 tid: 0x73e303fff6c0] hipMemcpyAsync: Returned hipSuccess : : duration: 285 us
:3:hip_device_runtime.cpp   :779 : 38370561569 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561572 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38370561577 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbd74 ) 
:3:hip_device_runtime.cpp   :705 : 38370561580 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561584 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffb6bc ) 
:3:hip_device_runtime.cpp   :705 : 38370561586 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561589 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffb6fc ) 
:3:hip_device_runtime.cpp   :705 : 38370561592 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38370561601 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {7,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38370561605 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38370561609 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {0,0,0}, {0,0,0}, 0x73e303ffb938, 0x73e303ffb928 ) 
:3:hip_platform.cpp         :284 : 38370561613 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38370561620 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bd7610, {7,1,1}, {256,1,1}, 0x73e303ffb960, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38370561626 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38370561631 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e2214c6960 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38370561635 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38370561638 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x0 (size:0x1)
:4:rocvirtual.cpp           :981 : 38370561642 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 d8 80 1b e3 73 00 00 00 a4 85 1b e3 73 00 00  (size:0x10)
:3:rocvirtual.cpp           :3668: 38370561646 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::float16tofloat32_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(c10::Half)#1}, std::array<char*, 2ul> >(int, at::native::float16tofloat32_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(c10::Half)#1}, std::array<char*, 2ul>)
:5:rocvirtual.cpp           :3867: 38370561653 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 24 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1594: 38370561658 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x103 (type=3, barrier=1, acquire=0, release=0), dep_signal=[0x73e4ce7de280, 0x0, 0x0, 0x0, 0x0], completion_signal=0x0, rptr=638191, wptr=638191
:5:rocvirtual.cpp           :1208: 38370561665 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0x1502 (type=2, barrier=1, acquire=2, release=2), setup=3, grid=[1792, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e18aa73100, kernarg_address=0x73e2a4a01780, completion_signal=0x0, correlation_id=0, rptr=638191, wptr=638192
:3:hip_module.cpp           :827 : 38370561671 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 51 us
:3:hip_error.cpp            :34  : 38370561676 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_error.cpp            :34  : 38370561678 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38370561681 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561684 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38370561689 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561692 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38370561818 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd5b4 ) 
:3:hip_device_runtime.cpp   :705 : 38370561821 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561824 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd474 ) 
:3:hip_device_runtime.cpp   :705 : 38370561827 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561830 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd2dc ) 
:3:hip_device_runtime.cpp   :705 : 38370561833 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38370561837 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561840 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38370561843 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561845 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38370561849 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffdc54 ) 
:3:hip_device_runtime.cpp   :705 : 38370561852 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561857 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffcb14 ) 
:3:hip_device_runtime.cpp   :705 : 38370561859 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561863 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffca14 ) 
:3:hip_device_runtime.cpp   :705 : 38370561865 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561868 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc73c ) 
:3:hip_device_runtime.cpp   :705 : 38370561870 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38370561876 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561878 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38370561882 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38370561884 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38370561891 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc934 ) 
:3:hip_device_runtime.cpp   :705 : 38370561894 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38370561897 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc74c ) 
:3:hip_device_runtime.cpp   :705 : 38370561899 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_memory.cpp           :1618: 38370561903 us: [pid:309675 tid: 0x73e303fff6c0]  hipMemcpyAsync ( 0x73e31b867c00, 0x73d5d1596868, 27648, hipMemcpyHostToDevice, char array:<null> ) 
:5:hip_device.cpp           :36  : 38370561907 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38370561911 us: [pid:309675 tid: 0x73e303fff6c0] Command (CopyHostToDevice) enqueued: 0x73e21eb92e10 to queue: 0x73e2ec01cb20
:5:rocvirtual.cpp           :1594: 38370561917 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x73e4ce7e2d80, rptr=638193, wptr=638193
:5:rocblit.cpp              :681 : 38370561922 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy Using Staging resource size 27648
:5:rocblit.cpp              :727 : 38370561925 us: [pid:309675 tid: 0x73e303fff6c0] memcpy stg buf=0x73e294f06c00, host src=0x73d5d1596868, size=27648
:4:rocblit.cpp              :731 : 38370562387 us: [pid:309675 tid: 0x73e303fff6c0] HSA Async Copy staged H2D, Async=1
:4:rocblit.cpp              :521 : 38370562392 us: [pid:309675 tid: 0x73e303fff6c0] Using assigned SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2
:4:rocblit.cpp              :556 : 38370562396 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy copy_engine=0x1, dst=0x73e31b867c00, src=0x73e294f06c00, size=27648, forceSDMA=0, engineType=2, wait_event=0x0, completion_signal=0x73e4ce7dd180
:3:hip_memory.cpp           :1619: 38395623027 us: [pid:309675 tid: 0x73e303fff6c0] hipMemcpyAsync: Returned hipSuccess : : duration: 25061124 us
:3:hip_device_runtime.cpp   :779 : 38395623048 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623054 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395623079 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc944 ) 
:3:hip_device_runtime.cpp   :705 : 38395623083 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623091 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc28c ) 
:3:hip_device_runtime.cpp   :705 : 38395623096 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623100 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc2cc ) 
:3:hip_device_runtime.cpp   :705 : 38395623103 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38395623114 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {7,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38395623121 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38395623129 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {0,0,0}, {0,0,0}, 0x73e303ffc508, 0x73e303ffc4f8 ) 
:3:hip_platform.cpp         :284 : 38395623136 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38395623147 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bd75e0, {7,1,1}, {256,1,1}, 0x73e303ffc530, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38395623156 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38395623167 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e221439e90 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38395623176 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38395623180 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x0 (size:0x1)
:4:rocvirtual.cpp           :981 : 38395623187 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 a4 85 1b e3 73 00 00 00 7c 86 1b e3 73 00 00  (size:0x10)
:3:rocvirtual.cpp           :3668: 38395623194 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::bfloat16tofloat32_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(c10::BFloat16)#1}, std::array<char*, 2ul> >(int, at::native::bfloat16tofloat32_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(c10::BFloat16)#1}, std::array<char*, 2ul>)
:5:rocvirtual.cpp           :3867: 38395623205 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 24 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1594: 38395623219 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x103 (type=3, barrier=1, acquire=0, release=0), dep_signal=[0x73e4ce7dd180, 0x0, 0x0, 0x0, 0x0], completion_signal=0x0, rptr=638194, wptr=638194
:5:rocvirtual.cpp           :1208: 38395623230 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0x1502 (type=2, barrier=1, acquire=2, release=2), setup=3, grid=[1792, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e18aa72f80, kernarg_address=0x73e2a4a01800, completion_signal=0x0, correlation_id=0, rptr=638194, wptr=638195
:3:hip_module.cpp           :827 : 38395623241 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 94 us
:3:hip_error.cpp            :34  : 38395623249 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_error.cpp            :34  : 38395623252 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38395623256 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623261 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38395623279 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623283 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395623321 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd48c ) 
:3:hip_device_runtime.cpp   :705 : 38395623325 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623331 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd184 ) 
:3:hip_device_runtime.cpp   :705 : 38395623336 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623342 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffceac ) 
:3:hip_device_runtime.cpp   :705 : 38395623346 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38395623356 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623360 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395623370 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd13c ) 
:3:hip_device_runtime.cpp   :705 : 38395623374 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623379 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffd17c ) 
:3:hip_device_runtime.cpp   :705 : 38395623384 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38395623391 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {14,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38395623398 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38395623406 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {67097768,29667,589796994}, {0,0,926328864}, 0x73e303ffd3a8, 0x73e303ffd370 ) 
:3:hip_platform.cpp         :284 : 38395623413 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38395623421 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bd40e8, {14,1,1}, {256,1,1}, 0x73e303ffd3d0, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38395623430 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38395623435 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e2237aa270 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38395623443 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38395623447 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x3f800000def87540 (size:0x8)
:4:rocvirtual.cpp           :981 : 38395623454 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 7c 86 1b e3 73 00 00 00 a4 85 1b e3 73 00 00  (size:0x10)
:3:rocvirtual.cpp           :3668: 38395623461 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::AUnaryFunctor<float, float, float, at::native::binary_internal::MulFunctor<float> >, std::array<char*, 2ul> >(int, at::native::AUnaryFunctor<float, float, float, at::native::binary_internal::MulFunctor<float> >, std::array<char*, 2ul>)
:5:rocvirtual.cpp           :3867: 38395623471 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 32 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1208: 38395623480 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[3584, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e29444ae40, kernarg_address=0x73e2a4a01880, completion_signal=0x0, correlation_id=0, rptr=638196, wptr=638196
:3:hip_module.cpp           :827 : 38395623492 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 71 us
:3:hip_error.cpp            :34  : 38395623498 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38395623503 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623508 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395623546 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc80c ) 
:3:hip_device_runtime.cpp   :705 : 38395623549 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623557 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc44c ) 
:3:hip_device_runtime.cpp   :705 : 38395623562 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623567 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc48c ) 
:3:hip_device_runtime.cpp   :705 : 38395623571 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38395623578 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {14,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38395623584 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38395623592 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {2,0,1}, {1,0,3}, 0x73e303ffc6c8, 0x73e303ffc6b8 ) 
:3:hip_platform.cpp         :284 : 38395623599 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38395623609 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bbace0, {14,1,1}, {256,1,1}, 0x73e303ffc6f0, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38395623618 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38395623623 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e2214c6650 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38395623631 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38395623636 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x3f800000 (size:0x4)
:4:rocvirtual.cpp           :981 : 38395623643 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 d8 80 1b e3 73 00 00 00 d8 80 1b e3 73 00 00 00 7c 86 1b e3 73 00 00  (size:0x18)
:3:rocvirtual.cpp           :3668: 38395623650 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::CUDAFunctor_add<float>, std::array<char*, 3ul> >(int, at::native::CUDAFunctor_add<float>, std::array<char*, 3ul>)
:5:rocvirtual.cpp           :3867: 38395623659 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 32 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1208: 38395623667 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[3584, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e1e8265700, kernarg_address=0x73e2a4a01900, completion_signal=0x0, correlation_id=0, rptr=638197, wptr=638197
:3:hip_module.cpp           :827 : 38395623678 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 69 us
:3:hip_error.cpp            :34  : 38395623685 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38395623690 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623694 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395623735 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc284 ) 
:3:hip_device_runtime.cpp   :705 : 38395623738 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623744 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc144 ) 
:3:hip_device_runtime.cpp   :705 : 38395623748 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623754 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbfac ) 
:3:hip_device_runtime.cpp   :705 : 38395623758 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38395623764 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623769 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38395623774 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623778 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395623785 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbef4 ) 
:3:hip_device_runtime.cpp   :705 : 38395623790 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623795 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffb83c ) 
:3:hip_device_runtime.cpp   :705 : 38395623799 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395623804 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffb87c ) 
:3:hip_device_runtime.cpp   :705 : 38395623809 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_platform.cpp         :266 : 38395623815 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPushCallConfiguration ( {7,1,1}, {256,1,1}, 0, char array:<null> ) 
:3:hip_platform.cpp         :270 : 38395623821 us: [pid:309675 tid: 0x73e303fff6c0] __hipPushCallConfiguration: Returned hipSuccess : 
:3:hip_platform.cpp         :275 : 38395623829 us: [pid:309675 tid: 0x73e303fff6c0]  __hipPopCallConfiguration ( {67091248,29667,406109151}, {67091472,29667,265918296}, 0x73e303ffbab8, 0x73e303ffbaa8 ) 
:3:hip_platform.cpp         :284 : 38395623837 us: [pid:309675 tid: 0x73e303fff6c0] __hipPopCallConfiguration: Returned hipSuccess : 
:3:hip_module.cpp           :825 : 38395623845 us: [pid:309675 tid: 0x73e303fff6c0]  hipLaunchKernel ( 0x73e528bd7580, {7,1,1}, {256,1,1}, 0x73e303ffbae0, 0, char array:<null> ) 
:5:hip_device.cpp           :36  : 38395623853 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38395623858 us: [pid:309675 tid: 0x73e303fff6c0] Command (KernelExecution) enqueued: 0x73e223765d60 to queue: 0x73e2ec01cb20
:4:rocvirtual.cpp           :990 : 38395623866 us: [pid:309675 tid: 0x73e303fff6c0] Arg0:   = val:0x3600 (size:0x4)
:4:rocvirtual.cpp           :990 : 38395623870 us: [pid:309675 tid: 0x73e303fff6c0] Arg1:   = val:0x4a (size:0x1)
:4:rocvirtual.cpp           :981 : 38395623877 us: [pid:309675 tid: 0x73e303fff6c0] Arg2:   = 0x00 a4 85 1b e3 73 00 00 00 d8 80 1b e3 73 00 00  (size:0x10)
:3:rocvirtual.cpp           :3668: 38395623883 us: [pid:309675 tid: 0x73e303fff6c0] ShaderName : void at::native::vectorized_elementwise_kernel<4, at::native::float16_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(float)#1}, std::array<char*, 2ul> >(int, at::native::float16_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda(float)#1}, std::array<char*, 2ul>)
:5:rocvirtual.cpp           :3867: 38395623892 us: [pid:309675 tid: 0x73e303fff6c0] KernargSegmentByteSize = 24 KernargSegmentAlignment = 128
:5:rocvirtual.cpp           :1208: 38395623901 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[1792, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=0, kernel_obj=0x73e18aa72c80, kernarg_address=0x73e2a4a01980, completion_signal=0x0, correlation_id=0, rptr=638198, wptr=638198
:3:hip_module.cpp           :827 : 38395623911 us: [pid:309675 tid: 0x73e303fff6c0] hipLaunchKernel: Returned hipSuccess : : duration: 66 us
:3:hip_error.cpp            :34  : 38395623918 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_error.cpp            :34  : 38395623922 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetLastError (  ) 
:3:hip_device_runtime.cpp   :779 : 38395623926 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395623931 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395624045 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc214 ) 
:3:hip_device_runtime.cpp   :705 : 38395624049 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395624055 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffc0d4 ) 
:3:hip_device_runtime.cpp   :705 : 38395624059 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395624064 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbf3c ) 
:3:hip_device_runtime.cpp   :705 : 38395624068 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :779 : 38395624076 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395624081 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :779 : 38395624085 us: [pid:309675 tid: 0x73e303fff6c0]  hipSetDevice ( 0 ) 
:3:hip_device_runtime.cpp   :785 : 38395624090 us: [pid:309675 tid: 0x73e303fff6c0] hipSetDevice: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :693 : 38395624098 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbe74 ) 
:3:hip_device_runtime.cpp   :705 : 38395624102 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :693 : 38395624107 us: [pid:309675 tid: 0x73e303fff6c0]  hipGetDevice ( 0x73e303ffbc8c ) 
:3:hip_device_runtime.cpp   :705 : 38395624112 us: [pid:309675 tid: 0x73e303fff6c0] hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 38395624120 us: [pid:309675 tid: 0x73e303fff6c0]  hipStreamGetCaptureInfo ( char array:<null>, 0x73e303ffbe7c, char array:<null> ) 
:3:hip_graph.cpp            :2062: 38395624127 us: [pid:309675 tid: 0x73e303fff6c0] hipStreamGetCaptureInfo: Returned hipSuccess : 
:3:hip_memory.cpp           :827 : 38395624138 us: [pid:309675 tid: 0x73e303fff6c0]  hipMemcpyWithStream ( 0x73ddab2db000, 0x73d8d445f980, 58060800, hipMemcpyHostToDevice, char array:<null> ) 
:5:hip_device.cpp           :36  : 38395624145 us: [pid:309675 tid: 0x73e303fff6c0] NullStream 0x73e2ec01cb20, wait 1
:5:command.cpp              :354 : 38395624157 us: [pid:309675 tid: 0x73e303fff6c0] Command (CopyHostToDevice) enqueued: 0x73e21eb96f30 to queue: 0x73e2ec01cb20
:5:rocvirtual.cpp           :1594: 38395624170 us: [pid:309675 tid: 0x73e303fff6c0] SWq=0x73e376a26000, HWq=0x73e2c8300000, id=1, BarrierAND Header = 0x1503 (type=3, barrier=1, acquire=2, release=2), dep_signal=[0x0, 0x0, 0x0, 0x0, 0x0], completion_signal=0x73e4ce7deb00, rptr=638199, wptr=638199
:4:rocdevice.cpp            :2113: 38395660539 us: [pid:309675 tid: 0x73e303fff6c0] Locking to pool 0xde6cc00, size 0x2001000, hostMem = 0x73d8d445f000, deviceMemory = 0x73d8d445f000, memSegment = 0
:5:rocblit.cpp              :670 : 38395660548 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy Using Pinned resource size 33554432
:4:rocblit.cpp              :731 : 38395660554 us: [pid:309675 tid: 0x73e303fff6c0] HSA Async Copy staged H2D, Async=0
:4:rocblit.cpp              :521 : 38395660560 us: [pid:309675 tid: 0x73e303fff6c0] Using assigned SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2
:4:rocblit.cpp              :556 : 38395660565 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy copy_engine=0x1, dst=0x73ddab2db000, src=0x73d8d445f980, size=33554432, forceSDMA=0, engineType=2, wait_event=0x0, completion_signal=0x73e4ce7ddb00
:4:rocdevice.cpp            :2113: 38395679206 us: [pid:309675 tid: 0x73e303fff6c0] Locking to pool 0xde6cc00, size 0x1760000, hostMem = 0x73d8d645f000, deviceMemory = 0x73d8d645f000, memSegment = 0
:5:rocblit.cpp              :670 : 38395679215 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy Using Pinned resource size 24506368
:4:rocblit.cpp              :731 : 38395679220 us: [pid:309675 tid: 0x73e303fff6c0] HSA Async Copy staged H2D, Async=0
:4:rocblit.cpp              :521 : 38395679227 us: [pid:309675 tid: 0x73e303fff6c0] Using assigned SDMA engine for VirtualGPU 0x73e2ec02d280: mask=0x1, engine_type=2
:4:rocblit.cpp              :556 : 38395679232 us: [pid:309675 tid: 0x73e303fff6c0] HSA Copy copy_engine=0x1, dst=0x73ddad2db000, src=0x73d8d645f980, size=24506368, forceSDMA=0, engineType=2, wait_event=0x73e4ce7ddb00, completion_signal=0x73e4ce7ddd80
:4:rocvirtual.cpp           :714 : 38395679242 us: [pid:309675 tid: 0x73e303fff6c0] Host wait on completion_signal=0x73e4ce7ddd80
```

Here is my startup script for ComfyUI:

```
#!/bin/bash
source .venv/bin/activate
#source venv6.4/bin/activate

BASE_URL="$HOME/ComfyUI-Test/ComfyUI"
#BASE_URL="$HOME/ComfyUI-Test/ComfyUI/6.4.2"

# === ROCm paths ===
#export ROCM_PATH="/opt/rocm-7.2.0"
#export HIP_PATH="$ROCM_PATH"
export HIP_VISIBLE_DEVICES=0
export ROCM_VISIBLE_DEVICES=0

# === GPU targeting ===
export HCC_AMDGPU_TARGET="gfx1100"   
export PYTORCH_ROCM_ARCH="gfx1100"   
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export PYTORCH_ROCM_ARCH="gfx1100"
export TORCH_HIP_ARCH_LIST="gfx1100"
export TRITON_OVERRIDE_ARCH="gfx1100"

# === Memory allocator tuning ===
#export PYTORCH_ALLOC_CONF="garbage_collection_threshold:0.6,max_split_size_mb:128,expandable_segments:True"
export PYTORCH_ALLOC_CONF="garbage_collection_threshold:0.7,expandable_segments:True"

# === TunableOps ===
export PYTORCH_TUNABLEOP_ENABLED=1
export PYTORCH_TUNABLEOP_TUNING=0
export PYTORCH_TUNABLEOP_VERBOSE=1

# === Precision and performance ===
export TORCH_BLAS_PREFER_HIPBLASLT=0
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS="CK,Triton,ROCBLAS"
export TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_SEARCH_SPACE="DEFAULT"
export TORCHINDUCTOR_FORCE_FALLBACK=0
export TORCHINDUCTOR_CACHE_DIR="$BASE_URL/.torchinductor"

# === Flash Attention ===
export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"
export FLASH_ATTENTION_TRITON_AMD_AUTOTUNE="FALSE" 
#export FLASH_ATTENTION_SKIP_AUTOTUNE=1
export FLASH_ATTENTION_TRITON_AMD_PERF=TRUE
export FLASH_ATTENTION_BACKEND="flash_attn_triton_amd"
export FLASH_ATTENTION_TRITON_AMD_SEQ_LEN=4096
export USE_CK=ON
export TRANSFORMERS_USE_FLASH_ATTENTION=1

# === Triton/AOTriton ===
export TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
export TRITON_AUTOTUNE=0
export TRITON_LOG_LEVEL=info
export TRITON_USE_ROCM=ON
export TRITON_PRINT_AUTOTUNING=1
export TRITON_CACHE_AUTOTUNING=1
export TRITON_DISABLE_BACKEND=0
export TRITON_HOME="$BASE_URL/.triton"

# === CPU threading ===
#export OMP_NUM_THREADS=8
#export MKL_NUM_THREADS=8
#export NUMEXPR_NUM_THREADS=8

# === Experimental ROCm flags ===
#export HSA_ENABLE_ASYNC_COPY=0
#export HSA_ENABLE_SDMA=0
export HSA_XNACK=1

# === MIOpen ===
export MIOPEN_FIND_MODE=FAST
export MIOPEN_ENABLE_CACHE=1
export MIOPEN_FIND_ENFORCE=1
#export MIOPEN_ENABLE_LOGGING=1

# === MIOpen cache ===
export MIOPEN_USER_DB_PATH="$BASE_URL/.miopen"
export MIOPEN_CUSTOM_CACHE_DIR="$BASE_URL/.miopen"

#export LD_LIBRARY_PATH=/home/vsekar92/ComfyUI-Test/ComfyUI/.venv/lib/python3.12/site-packages/_rocm_sdk_core/lib:$LD_LIBRARY_PATH
export AMD_LOG_LEVEL=5

# === Launch ComfyUI ===
#--disable-smart-memory --disable-pinned-memory --async-offload --reserve-vram .9
python3 main.py --cache-none --use-flash-attention

```



---

### 评论 #3 — Only8Bits (2026-02-11T23:53:22Z)

[PsiloaxinV](https://github.com/PsiloaxinV), FWIW I had a similar issue on 32GiB RAM with my 7900XT. I think it's a ComfyUI specific and --cache-none does not fully resolve it because Comfy still tries to load all models and LoRAs into RAM. So actually I belive it's RAM not VRAM issue. In short:
 
* I observed some extreme RAM swapping, and I even tried to make the swap bigger (up to 8GiB) but that only made the model load a bit more before it would pretty much crawl to stop again.
* Tried a lot of Comfy settings, nothing helped, their caching system is just broken like that. The only thing that helps is keeping as little RAM occupied as possible, for example no apps and browser with minimum tabs open.
* In the end I just added 16GiB of RAM to have 48GiB total and now it all works, without --cache-none too. I'm still on DD4 though and this was before the most of the RAM price hikes.

Try sudo swapoff -a and see if you get more OOM crashes rather than these "hangs". This setting is not permanent so no need to worry about it after reboot. IMO 32GiB RAM is just barely enough for WAN 2.2 unless you limit yourself to Q4 GGUFs (or worse) and even then with careful selection of LoRAs.

---

### 评论 #4 — PsiloaxinV (2026-02-12T00:02:00Z)

Problem is, though, it was working fine a few days ago; it's not like I'm trying this for the first time and running into OOM errors. 

I appreciate your input, though, and I'll try turning swap off sometime just to see what happens.

And good luck getting RAM nowadays lol. The RAM I bought 1.5 years ago is like $350 now.

---

### 评论 #5 — Only8Bits (2026-02-12T08:55:04Z)

It mostly worked for me too, these slowdowns were actually rare as most of the time it would either load fine or crash the python process. But when I noticed the swapping I decided I didn't want to cause premature SSD wear so I got more RAM.

Out of curiosity, how are you using fp8_scaled with just 16G of VRAM? That requires some serious block swapping to RAM? I mostly use Q6 GGUF and even then 832x480 already needs block swapping because once I get too close to 20G limit there is a chance it'll spike at some random point and amdgpu will hang or reboot the system rather than gracefully OOM. The --reserve-vram option does next to nothing for me.

---

### 评论 #6 — PsiloaxinV (2026-02-12T13:50:28Z)

Nope, I didn't use any block swapping. Before I switched to Ubuntu I ran with ZLUDA then eventually the native pytorch libraries on Windows 11, all using the fp8_scaled model. On Ubuntu, after some tinkering, I was getting around 2.5-3x the speed that I was getting on Windows (still using fp8_scaled). Note that, on Windows, I was basically stuck at 33 frames per generation. On Ubuntu, I was able to do 81 frames for resolutions like 973x665 (I would get like ~100 - 105 s/it). No OOMs or crashes. I noticed that while the Q6_K was slightly slower in lower frame counts like 33, it was actually much faster with higher frame counts like 81. I was running 970x730 with like ~85 s/it.

Even now, I *really* think this isn't an OOM issue. It's like the memory is being locked so the system can't free it properly. If I run, say, just the high noise model for both KSampler passes, the workflows run without a hitch. It's the transition between models that's killing me now.

---

### 评论 #7 — PsiloaxinV (2026-02-13T16:08:50Z)

So I've done a complete reinstall of Ubuntu (only restored my home folder) and ran GPU stress tests to make sure nothing was wrong. GPU passed stress tests, and no change in behavior in ComfyUI. 

Also tried these environment variables with no success:

export HSA_XNACK=0
export HSA_ENABLE_SDMA=0
export HSA_ENABLE_ASYNC_COPY=0
export HIP_FORCE_HOST_MEMORY=1
export ROCR_VISIBLE_DEVICES=0

No clue what else to do at this point.

---

### 评论 #8 — zichguan-amd (2026-02-18T21:02:00Z)

Looking at the logs the async memcpy is oddly slow: 27648 copy took 25061124 us, and the last synced copy didn't finish but didn't run out of memory either so it's indeed copying really slowly. Seems like the host thread is blocked or spin locked. The issue might be how ComfyUI handles the model load/unload when the vram/ram doesn't fit it all. I can't repro with my current system, so I'll try to take out some ram sticks. As for ComfyUI flags, maybe you can try `--async-offload` and `--force-non-blocking` to verify if the issue is the blocking memcpy.

---

### 评论 #9 — PsiloaxinV (2026-02-18T21:29:31Z)

What ended up working was making a new workflow. I made one that was more minimalist and streamlined without get/set nodes, for loops, etc. Also cut down on the number of different custom nodes I used. I'm able to run now without too many issues.

That doesn't explain why my original workflow suddenly had these issues though, which is why I'll keep this thread open for now. I'm still dealing with RAM and Swap filling up when using fp8_scaled models - it doesn't crash my system, but RAM usage is at 99%+ at the second sampling stage. This tells me memory still isn't being offloaded properly, but at least it runs. After the workflow finishes, RAM drops back to normal. I've been using Q6_K quants as a result - much more stable and RAM rarely goes above 20gb.

---

### 评论 #10 — PsiloaxinV (2026-02-19T20:03:29Z)

Dealing with similar stalls now on my new workflow on the low noise part. It's different from before in that a ComfyUI restart fixes it, so I've been restarting ComfyUI after every generation. I didn't see any noticeable difference with --force-non-blocking and --async-upload. It sometimes gets past the model loading phase, but never completes sampling; GPU usage sits at less than 5%.

I'll enable logging again and try to post some logs here later when I get a chance.

---

### 评论 #11 — zichguan-amd (2026-02-19T20:11:40Z)

> GPU usage sits at less than 5%.

Looks like something from host side is spin locked so the GPU is just sitting there with no work to do. Does CPU utilization stay high? It could also be that ROCm doesn't fully support Ubuntu 25 yet, can you try any supported distros?

---

### 评论 #12 — PsiloaxinV (2026-02-19T20:14:43Z)

Yeah I was thinking the same thing. I was considering rolling back to a kernel like 6.14 - is that a stable kernel to work with? I'd really rather not have to reinstall an entire OS for this, haha.

CPU utilization isn't maxed either. I see some cores spike up and down but most are idle.

---

### 评论 #13 — zichguan-amd (2026-02-19T20:22:46Z)

It's hard to say for Ubuntu 25, but we have official support for Ubuntu 24 on 6.8 [GA] and 6.14 [HWE] kernels, so perhaps you can give those a try. They are not 100% the same so there's no guarantee there. If you are using TheRock you might also want to check https://rocm.docs.amd.com/en/7.11.0-preview/compatibility/compatibility-matrix.html?fam=radeon&gpu=rx-7900-gre&os=ubuntu&os-version=24.04&i=pip

---

### 评论 #14 — Deaththegrim (2026-05-10T10:24:30Z)


Reproducing this on RX 9070 XT (RDNA4, gfx1201) under a sustained ComfyUI SDXL + multi-pass detailer workload. After tracing through the kernel side I'm seeing **two independent bugs** in the KFD restore path that compound to produce this signature, and I have patches for both classes that have stabilized my test bed across 24+ h soaks.

### Class 1 — head-of-line block + 1 ms reschedule (the runaway workqueue)

`svm_range_restore_work` and `amdgpu_amdkfd_restore_userptr_worker` both abandon the entire restore walk on the first per-entry failure (`goto out_reschedule` / `return -EAGAIN`), then reschedule themselves with `AMDGPU_SVM_RANGE_RESTORE_DELAY_MS = 1` (or `AMDGPU_USERPTR_RESTORE_DELAY_MS = 1`). The failing entry stays at the head of the list, so the next invocation hits the same failure first and reschedules again. The workqueue framework reports it as escalating `workqueue: ... hogged CPU for >10000us N times` warnings (`svm_range_restore_work` doubles each time: 67 → 131 → 259 → 515 → 1027). After enough cycles the GPU starts page-faulting on still-unmapped VAs:

```
amdgpu 0000:03:00.0: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801D3B
amdgpu 0000:03:00.0:    Faulty UTCL2 client ID: SDMA0 (0xd)
amdgpu 0000:03:00.0: [gfxhub] page fault (src_id:0 ring:173 vmid:8 pasid:32779)
```

Fix: convert per-entry `goto`/`return` head-of-line aborts into `failed = true; continue;` (or `goto next_iter;` where lock state requires it), then return `-EAGAIN` from the function once if any entry failed so the caller still reschedules. Spin-rate drops from ~1 kHz to "approximately one per genuinely-failing entry per cycle." Two-patch series: `kfd_svm.c` (~50 lines diff), `amdgpu_amdkfd_gpuvm.c` (~225 lines diff).

### Class 2 — restore workers run on `system_freezable_wq` (per-CPU)

Both restore workers are queued via `queue_delayed_work(system_freezable_wq, ...)`. `system_freezable_wq` is bound; under host RAM pressure or when the assigned CPU is busy, the worker stalls and `kgd2kfd_resume_mm` eventually fails:

```
amdgpu: amdgpu_amdkfd_restore_userptr_worker: Failed to resume KFD
```

The in-tree comment at `amdgpu_amdkfd_gpuvm.c:3354-3356` admits no recovery (*"Probably the CP is hanging. No point trying again."*) — but the CP isn't hanging, the workqueue is. Subsequent CS submissions then flood:

```
amdgpu 0000:03:00.0: [drm] *ERROR* Not enough memory for command submission!
```

at ~3.7/sec, un-ratelimited, until the system freezes (~30 s).

Fix: 5-line `system_freezable_wq` → `system_unbound_wq` swap across both files. Loses freezability on suspend/resume; for KFD restore that's the lesser evil since a stalled restore is unrecoverable anyway. If freezability matters for laptop deployments, the alternative is `alloc_workqueue(name, WQ_UNBOUND | WQ_FREEZABLE | WQ_MEM_RECLAIM, 0)`.

### Attaching

- Detailed bug reports (full reproduction, dmesg traces, diff context, environment): I have these as Markdown locally and can post the full text in a follow-up comment on request, or email them.
- Patches: 4 `.patch` files (head-of-line ×2, WQ_UNBOUND ×2), all dry-run-clean against DKMS `amdgpu/6.18.4-2286447.24.04` source tree.

Happy to run additional traces, swap to `alloc_workqueue` style if upstream prefers freezability preserved, or split the series differently. Filing this here since it's the most-active thread for the user-visible signature; will mirror to gitlab.fd.o/drm/amd issues for the kernel maintainers.

Environment: AMD RX 9070 XT (gfx1201), Ryzen 9 9950X3D, 32 GB DDR5, kernel 6.17.0-1020-oem, DKMS amdgpu/6.18.4-2286447.24.04, ROCm 7.2.3, PyTorch 2.10.0.dev (rocm6.3).


---
