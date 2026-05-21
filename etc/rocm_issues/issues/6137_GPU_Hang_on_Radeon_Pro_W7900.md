# GPU Hang on Radeon Pro W7900

> **Issue #6137**
> **状态**: closed
> **创建时间**: 2026-04-09T09:06:02Z
> **更新时间**: 2026-04-16T08:41:25Z
> **关闭时间**: 2026-04-16T08:41:25Z
> **作者**: LutzRohlfing
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6137

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

I am using the AMR Radeon Pro W7900 GPU for flow simulations with the software AMR-Wind.

AMR-Wind: https://github.com/Exawind/amr-wind

Randomly during my simulations i get this error:

HW Exception by GPU node-1 (Agent handle: 0x1b0fc990) reason :GPU Hang
[windteammitarbeiter:08475] *** Process received signal ***
[windteammitarbeiter:08475] Signal: Aborted (6)
[windteammitarbeiter:08475] Signal code: (-6)
[windteammitarbeiter:08475] [ 0] /lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x750502245330]
[windteammitarbeiter:08475] [ 1] /lib/x86_64-linux-gnu/libc.so.6(pthread_kill+0x11c)[0x75050229eb2c]
[windteammitarbeiter:08475] [ 2] /lib/x86_64-linux-gnu/libc.so.6(gsignal+0x1e)[0x75050224527e]
[windteammitarbeiter:08475] [ 3] /lib/x86_64-linux-gnu/libc.so.6(abort+0xdf)[0x7505022288ff]
[windteammitarbeiter:08475] [ 4] /opt/rocm-6.4.3/lib/libhsa-runtime64.so.1(+0x2cce7)[0x75050142cce7]
[windteammitarbeiter:08475] [ 5] /opt/rocm-6.4.3/lib/libhsa-runtime64.so.1(+0xa22ac)[0x7505014a22ac]
[windteammitarbeiter:08475] [ 6] /opt/rocm-6.4.3/lib/libhsa-runtime64.so.1(+0x39251)[0x750501439251]
[windteammitarbeiter:08475] [ 7] /lib/x86_64-linux-gnu/libc.so.6(+0x9caa4)[0x75050229caa4]
[windteammitarbeiter:08475] [ 8] /lib/x86_64-linux-gnu/libc.so.6(+0x129c6c)[0x750502329c6c]
[windteammitarbeiter:08475] *** End of error message ***

I also opened an issue in the AMR-Wind Github repository:
https://github.com/Exawind/amr-wind/issues/1884

The developers there pointed out that this might not be an AMR-Wind issue, but something else. Maybe someone here is able to help me, i am unsure if this is even the right place for this issue.

Some other information:
OS: Ubuntu 24.04 LTS
ROCm: 6.4.3

I am happy to provide any other information that might be needed.

---

## 评论 (6 条)

### 评论 #1 — harkgill-amd (2026-04-10T14:40:30Z)

Hey @LutzRohlfing, coud you share the output of `sudo dmesg | grep amdgpu`. That'll give us more insight around what might be causing the hang.

---

### 评论 #2 — LutzRohlfing (2026-04-10T17:35:29Z)

Thanks for the assistance!

This is the output of: sudo dmesg | grep amdgpu
[    9.070067] amdgpu: vga_switcheroo: detected switching method \_SB_.PCI0.GP17.VGA_.ATPX handle
[    9.070206] amdgpu: ATPX version 1, functions 0x00000000
[    9.080778] amdgpu: Virtual CRAT table created for CPU
[    9.080811] amdgpu: Topology: Add CPU node
[    9.080907] amdgpu 0000:03:00.0: enabling device (0006 -> 0007)
[    9.085780] amdgpu 0000:03:00.0: amdgpu: detected ip block number 0 <soc21_common>
[    9.085784] amdgpu 0000:03:00.0: amdgpu: detected ip block number 1 <gmc_v11_0>
[    9.085785] amdgpu 0000:03:00.0: amdgpu: detected ip block number 2 <ih_v6_0>
[    9.085787] amdgpu 0000:03:00.0: amdgpu: detected ip block number 3 <psp>
[    9.085789] amdgpu 0000:03:00.0: amdgpu: detected ip block number 4 <smu>
[    9.085790] amdgpu 0000:03:00.0: amdgpu: detected ip block number 5 <dm>
[    9.085792] amdgpu 0000:03:00.0: amdgpu: detected ip block number 6 <gfx_v11_0>
[    9.085793] amdgpu 0000:03:00.0: amdgpu: detected ip block number 7 <sdma_v6_0>
[    9.085795] amdgpu 0000:03:00.0: amdgpu: detected ip block number 8 <vcn_v4_0>
[    9.085796] amdgpu 0000:03:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0>
[    9.085798] amdgpu 0000:03:00.0: amdgpu: detected ip block number 10 <mes_v11_0>
[    9.085817] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from VFCT
[    9.085821] amdgpu: ATOM BIOS: 113-D7070100-139
[    9.090157] amdgpu 0000:03:00.0: amdgpu: CP RS64 enable
[    9.120853] amdgpu 0000:03:00.0: vgaarb: deactivate vga console
[    9.120857] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
[    9.120891] amdgpu 0000:03:00.0: amdgpu: MEM ECC is active.
[    9.120893] amdgpu 0000:03:00.0: amdgpu: SRAM ECC is not presented.
[    9.120903] amdgpu 0000:03:00.0: amdgpu: RAS INFO: ras initialized successfully, hardware ability[101] ras_mask[101]
[    9.120922] amdgpu 0000:03:00.0: amdgpu: VRAM: 46064M 0x0000008000000000 - 0x0000008B3EFFFFFF (46064M used)
[    9.120924] amdgpu 0000:03:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    9.121040] [drm] amdgpu: 46064M of VRAM memory ready
[    9.121042] [drm] amdgpu: 31700M of GTT memory ready.
[    9.197828] amdgpu 0000:03:00.0: amdgpu: reserve 0x1300000 from 0x8b3c000000 for PSP TMR
[    9.344065] amdgpu 0000:03:00.0: amdgpu: GECC is enabled
[    9.361243] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[    9.361246] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[    9.361279] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8200 (78.130.0)
[    9.361281] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[    9.527724] amdgpu 0000:03:00.0: amdgpu: SMU is initialized successfully!
[    9.602934] snd_hda_intel 0000:03:00.1: bound 0000:03:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
[    9.765347] amdgpu 0000:03:00.0: amdgpu: RAS header invalid, unsupported version: 4294967295
[    9.765351] amdgpu 0000:03:00.0: amdgpu: Failed to initialize ras recovery! (-22)
[    9.884192] amdgpu: HMM registered 46064MB device memory
[    9.885299] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[    9.885311] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[    9.885354] amdgpu: Virtual CRAT table created for GPU
[    9.885614] amdgpu: Topology: Add dGPU node [0x7448:0x1002]
[    9.885615] kfd kfd: amdgpu: added device 1002:7448
[    9.885628] amdgpu 0000:03:00.0: amdgpu: SE 6, SH per SE 2, CU per SH 8, active_cu_number 96
[    9.885633] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[    9.885634] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[    9.885636] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[    9.885637] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[    9.885638] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[    9.885640] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[    9.885641] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[    9.885642] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[    9.885644] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[    9.885645] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[    9.885646] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[    9.885648] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[    9.885649] amdgpu 0000:03:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[    9.885650] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[    9.885651] amdgpu 0000:03:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[    9.901127] amdgpu 0000:03:00.0: amdgpu: Using BAMACO for runtime pm
[    9.901748] amdgpu 0000:03:00.0: [drm] Registered 4 planes with drm panic
[    9.901750] [drm] Initialized amdgpu 3.61.0 for 0000:03:00.0 on minor 1
[    9.905834] fbcon: amdgpudrmfb (fb0) is primary device
[    9.905838] amdgpu 0000:03:00.0: [drm] fb0: amdgpudrmfb frame buffer device
[    9.926719] amdgpu 0000:7b:00.0: enabling device (0006 -> 0007)
[    9.928540] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 0 <nv_common>
[    9.928543] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 1 <gmc_v10_0>
[    9.928544] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 2 <navi10_ih>
[    9.928546] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 3 <psp>
[    9.928547] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 4 <smu>
[    9.928549] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 5 <dm>
[    9.928550] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 6 <gfx_v10_0>
[    9.928552] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 7 <sdma_v5_2>
[    9.928553] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 8 <vcn_v3_0>
[    9.928554] amdgpu 0000:7b:00.0: amdgpu: detected ip block number 9 <jpeg_v3_0>
[    9.928570] amdgpu 0000:7b:00.0: amdgpu: Fetched VBIOS from VFCT
[    9.928572] amdgpu: ATOM BIOS: 102-RAPHAEL-008
[    9.933689] amdgpu 0000:7b:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
[    9.933727] amdgpu 0000:7b:00.0: amdgpu: VRAM: 512M 0x000000F400000000 - 0x000000F41FFFFFFF (512M used)
[    9.933729] amdgpu 0000:7b:00.0: amdgpu: GART: 1024M 0x0000000000000000 - 0x000000003FFFFFFF
[    9.933815] [drm] amdgpu: 512M of VRAM memory ready
[    9.933816] [drm] amdgpu: 31700M of GTT memory ready.
[    9.956692] amdgpu 0000:7b:00.0: amdgpu: reserve 0xa00000 from 0xf41e000000 for PSP TMR
[   10.021383] amdgpu 0000:7b:00.0: amdgpu: RAS: optional ras ta ucode is not available
[   10.027101] amdgpu 0000:7b:00.0: amdgpu: RAP: optional rap ta ucode is not available
[   10.027103] amdgpu 0000:7b:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[   10.028294] amdgpu 0000:7b:00.0: amdgpu: SMU is initialized successfully!
[   10.030511] snd_hda_intel 0000:7b:00.1: bound 0000:7b:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
[   10.034741] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[   10.034753] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[   10.035189] amdgpu: Virtual CRAT table created for GPU
[   10.036135] amdgpu: Topology: Add dGPU node [0x164e:0x1002]
[   10.036137] kfd kfd: amdgpu: added device 1002:164e
[   10.036146] amdgpu 0000:7b:00.0: amdgpu: SE 1, SH per SE 1, CU per SH 2, active_cu_number 2
[   10.036149] amdgpu 0000:7b:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[   10.036151] amdgpu 0000:7b:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
[   10.036152] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
[   10.036153] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
[   10.036155] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[   10.036156] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[   10.036157] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[   10.036158] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[   10.036159] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[   10.036161] amdgpu 0000:7b:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[   10.036162] amdgpu 0000:7b:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
[   10.036163] amdgpu 0000:7b:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
[   10.036164] amdgpu 0000:7b:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[   10.036165] amdgpu 0000:7b:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[   10.036167] amdgpu 0000:7b:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[   10.036168] amdgpu 0000:7b:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[   10.036461] amdgpu 0000:7b:00.0: amdgpu: Runtime PM not available
[   10.036966] amdgpu 0000:7b:00.0: [drm] Registered 4 planes with drm panic
[   10.036969] [drm] Initialized amdgpu 3.61.0 for 0000:7b:00.0 on minor 2
[   10.038927] amdgpu 0000:7b:00.0: [drm] Cannot find any crtc or sizes

---

### 评论 #3 — harkgill-amd (2026-04-10T17:46:49Z)

Thanks for sharing, couple different things to note here,

1. Looks like this dmesg output was taken shortly after a reboot and doesn't contain any clues related to the hang. Is it possible to reproduce the hang and then share the output? 
2. We've had a couple different issues that appear as `HW Exception by GPU node-1` failures resolved since ROCm 6.4.3, could you upgrade to ROCm 7.2.1 and give your workflow a try?
3. If you could share the exact steps to repro this failure, I can also give it a try on my end.

---

### 评论 #4 — LutzRohlfing (2026-04-10T17:59:49Z)

Hi, again thanks for your help!

1. Yes you are right. I think this is not possible. Usually the machine crashes and can not be reached remotly. The monitors do not turn on again until i reboot (until then they show "no signal"). I think i can not enter the command before rebooting.
2. I will try this next week
3. This might be hard. We are using this machine for simulating with the software AMR-Wind. This software uses the GPU for flow simulations. During the simulations it randomly crashes. The above output is from the logged software output. We have not experienced the issue outside of the software, but we also only use the machine for simulating. For replicating you would need to first compile AMR-Wind. I could provide you with an input file for the software, but this might all be complicated and a lot of work for you.

Can this also be a mismatch in versions between Ubuntu, ROCm and AMR-Wind. AMR-Wind is usually compiled specifically for a machine and i can not exclude for certain that i did not mess something up when compiling. (Even though the people from AMR-Wind think it is more likely a machine and not an AMR-Wind issue, see: https://github.com/Exawind/amr-wind/issues/1884#issuecomment-4158183131)

---

### 评论 #5 — harkgill-amd (2026-04-10T18:26:10Z)

> Can this also be a mismatch in versions between Ubuntu, ROCm and AMR-Wind.

It's possible but without more information it's hard to tell what exactly is going wrong here. Just going purely off the error messages, I'm leaning more towards it being one of the older ROCm 6 issues that we've since resolved but your testing next week should confirm this (make sure to pull in the ROCm 7.2.1 amdgpu-dkms package as well). You can also enable a persistent journald to collect some of the logs that were lost in your dmesg
```
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald

#Then after rebooting post hang
journalctl -b -1 | grep amdgpu
```
These logs will help narrow down what exactly is causing the failure.

As a side note, 
```
[ 10.036135] amdgpu: Topology: Add dGPU node [0x164e:0x1002]
[ 10.036137] kfd kfd: amdgpu: added device 1002:164e
```
looks like your system also has an iGPU which can sometimes get pulled into usage and cause some issues. Setting `export HIP_VISIBLE_DEVICES=0` will force all tasks onto your dGPU - try this out as well prior to bumping the ROCm version.

---

### 评论 #6 — LutzRohlfing (2026-04-16T08:41:25Z)

Ok i updated to ROCm 7.2.1 and now it seems to work. I will mark this as solved.

---
