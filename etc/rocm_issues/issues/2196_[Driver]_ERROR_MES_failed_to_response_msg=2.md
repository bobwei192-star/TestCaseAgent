# [Driver] *ERROR* MES failed to response msg=2

> **Issue #2196**
> **状态**: open
> **创建时间**: 2023-05-30T23:40:56Z
> **更新时间**: 2025-10-15T11:04:01Z
> **作者**: geohot
> **标签**: 5.5.0
> **URL**: https://github.com/ROCm/ROCm/issues/2196

## 标签

- **5.5.0** (颜色: #fbca04)

## 描述

Triggered by running https://github.com/RadeonOpenCompute/rocm_bandwidth_test in a loop while running https://github.com/ROCm-Developer-Tools/HIP-Examples/tree/master/gpu-burn in a loop.

1x 7900XTX
ASROCK ROMED8-2T
EPYC 7662
Ubuntu 22.04, Kernel 6.2.14-060214-generic, ROCm 5.5

`sudo cat /sys/kernel/debug/dri/1/amdgpu_gpu_recover` will recover the GPU.

```
[  111.406216] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:10 pasid:32769, for process rocm-bandwidth- pid 3286 thread rocm-bandwidth- pid 3286)
[  111.406237] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007f0000000000 from client 10
[  111.406246] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00A01A30
[  111.406253] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA0 (0xd)
[  111.406259] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[  111.406265] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[  111.406270] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  111.406275] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  111.406280] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[  114.188710] amdgpu 0000:83:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:10 pasid:32769, for process rocm-bandwidth- pid 3286 thread rocm-bandwidth- pid 3286)
[  114.188729] amdgpu 0000:83:00.0: amdgpu:   in page starting at address 0x00007f0000000000 from client 10
[  114.188738] amdgpu 0000:83:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00A01A30
[  114.188746] amdgpu 0000:83:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA0 (0xd)
[  114.188754] amdgpu 0000:83:00.0: amdgpu:      MORE_FAULTS: 0x0
[  114.188759] amdgpu 0000:83:00.0: amdgpu:      WALKER_ERROR: 0x0
[  114.188765] amdgpu 0000:83:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  114.188770] amdgpu 0000:83:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  114.188776] amdgpu 0000:83:00.0: amdgpu:      RW: 0x0
[  114.302856] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[  114.303173] amdgpu: failed to add hardware queue to MES, doorbell=0x1202
[  114.303176] amdgpu: MES might be in unrecoverable state, issue a GPU reset
[  114.303179] amdgpu: Failed to restore queue 0
[  114.303182] amdgpu: Failed to restore process queues
[  114.303184] amdgpu: Failed to restore queues of pasid 0x8001
[  114.303450] amdgpu 0000:83:00.0: amdgpu: GPU reset begin!
[  114.303477] amdgpu: Failed to evict queue 1
[  114.303483] amdgpu: Failed to suspend process 0x8002
[  114.309700] amdgpu 0000:83:00.0: amdgpu: recover vram bo from shadow start
[  114.309705] amdgpu 0000:83:00.0: amdgpu: recover vram bo from shadow done
[  114.412749] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[  114.413073] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[  114.420094] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[  114.420379] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[  114.523222] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[  114.523499] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[  114.530476] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[  114.530750] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[  114.634108] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[  114.634391] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
...
[  117.293167] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
[  117.293439] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x2200
[  117.293712] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[  117.294161] amdgpu 0000:83:00.0: amdgpu: GPU reset(1) succeeded!
```

---

## 评论 (42 条)

### 评论 #1 — massivedynamics1 (2023-06-17T10:53:51Z)

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Thanks for connecting <a href="https://twitter.com/realGeorgeHotz?ref_src=twsrc%5Etfw">@realGeorgeHotz</a>. Appreciate the work you and tiny corp are doing. We are committed to working with the community and improving our support. More to come on ROCm on @radeon soon. Lots of work ahead but excited about what we can do together.</p>&mdash; Lisa Su (@LisaSu) <a href="https://twitter.com/LisaSu/status/1669848494637735936?ref_src=twsrc%5Etfw">June 16, 2023</a></blockquote>

---

### 评论 #2 — CorvetteCole (2023-10-15T02:18:01Z)

I can reproduce this on my 7900 XTX as well

---

### 评论 #3 — LefterisJP (2023-11-12T00:10:46Z)

I am also hitting this

---

### 评论 #4 — aenertia (2023-11-17T07:41:58Z)

I am seeing similar messages from kernel on boot with phoenix apu based system and without the ROCM Stack

` 1637.604718] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 1637.605055] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 1637.607290] [drm] PCIE GART of 512M enabled (table at 0x00000080FFD00000).
[ 1637.607422] amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
[ 1637.610838] amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
[ 1637.803597] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[ 1637.803867] amdgpu 0000:c1:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[ 1637.804227] amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 1637.804231] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 1637.804234] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 1637.804235] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 1637.804237] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 1637.804239] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 1637.804241] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 1637.804243] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 1637.804245] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 1637.804246] amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 1637.804248] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 1637.804250] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 1637.804252] amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 1637.809886] [drm] ring gfx_32803.1.1 was added
[ 1637.810426] [drm] ring compute_32803.2.2 was added
[ 1637.810934] [drm] ring sdma_32803.3.3 was added
[ 1637.810962] [drm] ring gfx_32803.1.1 ib test pass
[ 1637.810991] [drm] ring compute_32803.2.2 ib test pass
[ 1637.811092] [drm] ring sdma_32803.3.3 ib test pass
[ 1637.820482] PM: resume devices took 0.362 seconds
[ 1637.820898] OOM killer enabled.
[ 1637.820902] Restarting tasks ... done.
[ 1637.822675] random: crng reseeded on system resumption
[ 1637.829255] PM: suspend exit
[ 1640.456439] wlp1s0: authenticate with 24:4b:fe:62:67:04 (local address=14:ac:60:46:7b:f9)
[ 1640.479251] wlp1s0: send auth to 24:4b:fe:62:67:04 (try 1/3)
[ 1640.499491] wlp1s0: authenticate with 24:4b:fe:62:67:04 (local address=14:ac:60:46:7b:f9)
[ 1640.508904] wlp1s0: send auth to 24:4b:fe:62:67:04 (try 1/3)
[ 1640.512391] wlp1s0: authenticated
[ 1640.515427] wlp1s0: associate with 24:4b:fe:62:67:04 (try 1/3)
[ 1640.526627] wlp1s0: RX AssocResp from 24:4b:fe:62:67:04 (capab=0x1511 status=0 aid=1)
[ 1640.558571] wlp1s0: associated
[ 1640.613407] wlp1s0: Limiting TX power to 27 (30 - 3) dBm as advertised by 24:4b:fe:62:67:04
[ 1642.696635] ucsi_acpi USBC000:00: ucsi_handle_connector_change: ACK failed (-110)
[ 1648.577999] ucsi_acpi USBC000:00: ucsi_handle_connector_change: ACK failed (-110)
[ 2325.112034] i2c_designware AMDI0010:00: i2c_dw_handle_tx_abort: lost arbitration
[ 2531.128560] wlp1s0: deauthenticating from 24:4b:fe:62:67:04 by local choice (Reason: 3=DEAUTH_LEAVING)
[ 2531.678155] PM: suspend entry (s2idle)
[ 2531.701397] Filesystems sync: 0.023 seconds
[ 2531.710174] Freezing user space processes
[ 2531.712040] Freezing user space processes completed (elapsed 0.001 seconds)
[ 2531.712044] OOM killer disabled.
[ 2531.712045] Freezing remaining freezable tasks
[ 2531.713066] Freezing remaining freezable tasks completed (elapsed 0.001 seconds)
[ 2531.713070] printk: Suspending console(s) (use no_console_suspend to debug)
[ 2532.645147] PM: suspend devices took 0.932 seconds
[ 2532.647493] ACPI: EC: interrupt blocked
[ 9429.864695] ACPI: EC: interrupt unblocked
[ 9430.036343] nvme nvme0: 16/0/0 default/read/poll queues
[ 9430.088770] atkbd serio0: Unknown key pressed (translated set 2, code 0x6b on isa0060/serio0).
[ 9430.088779] atkbd serio0: Use 'setkeycodes 6b <keycode>' to make it known.
[ 9430.089328] atkbd serio0: Unknown key released (translated set 2, code 0x6b on isa0060/serio0).
[ 9430.089336] atkbd serio0: Use 'setkeycodes 6b <keycode>' to make it known.
[ 9430.175277] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[ 9430.175614] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[ 9430.177835] [drm] PCIE GART of 512M enabled (table at 0x00000080FFD00000).
[ 9430.177942] amdgpu 0000:c1:00.0: amdgpu: SMU is resuming...
[ 9430.181299] amdgpu 0000:c1:00.0: amdgpu: SMU is resumed successfully!
[ 9430.286638] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[ 9430.286884] amdgpu 0000:c1:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[ 9430.287225] amdgpu 0000:c1:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 9430.287229] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[ 9430.287231] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[ 9430.287233] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 9430.287234] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 9430.287236] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 9430.287237] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 9430.287239] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 9430.287241] amdgpu 0000:c1:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 9430.287242] amdgpu 0000:c1:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[ 9430.287244] amdgpu 0000:c1:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[ 9430.287246] amdgpu 0000:c1:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 8
[ 9430.287247] amdgpu 0000:c1:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[ 9430.292387] [drm] ring gfx_32803.1.1 was added
[ 9430.292929] [drm] ring compute_32803.2.2 was added
[ 9430.293440] [drm] ring sdma_32803.3.3 was added
[ 9430.293469] [drm] ring gfx_32803.1.1 ib test pass
[ 9430.293499] [drm] ring compute_32803.2.2 ib test pass
[ 9430.293598] [drm] ring sdma_32803.3.3 ib test pass
`

💻 Framework Laptop 13 (AMD Ryzen 7040Series) (Laptop) running BIOS 3.3 (03.03) released 10/17/2023 and EC unknown
🐧 Fedora Linux 40 (KDE Plasma Prerelease)
🐧 Kernel 6.7.0fw13ec-rc1+
✅ AMD Ryzen 7 7840U w/ Radeon  780M Graphics (family 19 model 74)
✅ HSMP driver `amd_hsmp` not detected (blocked: False)
✅ PMC driver `amd_pmc` loaded (Program 0 Firmware 76.70.0)
OpenGL core profile version string: 4.6 (Core Profile) Mesa 24.0.0-devel




---

### 评论 #5 — excieve (2023-11-19T13:19:59Z)

Similar issue with 7900 XT, ROCm 5.7, kernel 6.5.11 (Fedora 39)

Although GPU recovery doesn't fully help it seems. While there are no MES errors and GPU stats (usage, power draw) seem to be back to normal, there's a lot of the following in the kernel logs:
> [drm] Skip scheduling IBs!

Which keeps happening until a reboot.

---

### 评论 #6 — kean0048 (2023-12-04T02:56:43Z)

I have got the same msg during suspend the device based on RHEL9.3 which kernel is 'Linux localhost.localdomain 5.14.0-362.8.1.el9_3.x86_64 #1 SMP PREEMPT_DYNAMIC Tue Oct 3 11:12:36 EDT 2023 x86_64 x86_64 x86_64 GNU/Linux'

hardware info:
1) VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Phoenix1 [1002:15bf] (rev d3) (prog-if 00 [VGA controller])
2) 3D controller [0302]: NVIDIA Corporation AD107GLM [RTX 2000 Ada Generation Laptop GPU] [10de:28b8] (rev a1)


[  232.371283] OOM killer disabled.
[  232.371284] Freezing remaining freezable tasks ... (elapsed 0.001 seconds) done.
[  232.372385] printk: Suspending console(s) (use no_console_suspend to debug)
[  232.846688] ACPI: EC: interrupt blocked
[  233.975847] ACPI: EC: interrupt unblocked
[  234.994441] nvme nvme0: 16/0/0 default/read/poll queues
[  234.995443] nvme nvme1: 16/0/0 default/read/poll queues
[  235.106268] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
[  235.106526] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
[  235.108935] [drm] PCIE GART of 512M enabled (table at 0x000000803FD00000).
[  235.109033] amdgpu 0000:c6:00.0: amdgpu: SMU is resuming...
[  235.112006] amdgpu 0000:c6:00.0: amdgpu: SMU is resumed successfully!
[  235.114265] [drm] Watermarks table not configured properly by SMU
[  235.167424] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  235.167510] amdgpu 0000:c6:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
[  235.167631] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  235.167632] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  235.167632] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  235.167633] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  235.167634] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  235.167634] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  235.167634] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  235.167635] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  235.167635] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  235.167636] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  235.167636] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 1
[  235.167637] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec uses VM inv eng 1 on hub 1
[  235.167637] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[  235.173037] [drm] ring gfx_32770.1.1 was added
[  235.173947] [drm] ring compute_32770.2.2 was added
[  235.174822] [drm] ring sdma_32770.3.3 was added
[  235.174828] [drm] ring gfx_32770.1.1 test pass
[  235.174845] [drm] ring gfx_32770.1.1 ib test pass
[  235.174850] [drm] ring compute_32770.2.2 test pass
[  235.174871] [drm] ring compute_32770.2.2 ib test pass
[  235.175007] [drm] ring sdma_32770.3.3 test pass
[  235.175039] [drm] ring sdma_32770.3.3 ib test pass
[  235.312399] OOM killer enabled.

and suspend failed.

---

### 评论 #7 — terryrankine (2023-12-05T13:32:33Z)

```Dec 05 21:26:14 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Dec 05 21:26:14 theblob kernel: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Dec 05 21:26:14 theblob kernel: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Dec 05 21:26:14 theblob kernel: amdgpu: Failed to evict queue 1
Dec 05 21:26:14 theblob kernel: amdgpu: Failed to evict process queues
Dec 05 21:26:14 theblob kernel: amdgpu: Failed to evict queues of pasid 0x8001
Dec 05 21:26:14 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
Dec 05 21:26:14 theblob google-chrome.desktop[11352]: [21438:21449:1205/212614.765940:ERROR:vulkan_swap_chain.cc(443)] vkAcquireNextImageKHR() hangs.
Dec 05 21:26:14 theblob google-chrome.desktop[11352]: [21438:21438:1205/212614.766188:ERROR:gpu_service_impl.cc(1105)] Exiting GPU process because some drivers can't recover from errors. GPU process will restart shortly.
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: IP block:gfx_v11_0 is hung!
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa00200 flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa002b4 flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa002f4 flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa00208 flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa00200 flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa0025c flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa0029c flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa002dc flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa00208 flags=0x0020]
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: AMD-Vi: Event logged [IO_PAGE_FAULT domain=0x001e address=0xffc5fa00200 flags=0x0020]
Dec 05 21:26:15 theblob kernel: [drm] kiq ring mec 3 pipe 1 q 0
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow start
Dec 05 21:26:15 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow done
Dec 05 21:26:15 theblob google-chrome.desktop[11352]: [11346:11346:1205/212615.493041:ERROR:gpu_process_host.cc(990)] GPU process exited unexpectedly: exit_code=8704
Dec 05 21:26:15 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 05 21:26:15 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
```
snip

```Dec 05 21:26:17 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Dec 05 21:26:17 theblob kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Dec 05 21:26:17 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2
Dec 05 21:26:17 theblob kernel: [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x1a00
Dec 05 21:26:17 theblob kernel: [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
Dec 05 21:26:17 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GPU reset(1) succeeded!
Dec 05 21:26:31 theblob kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Dec 05 21:26:31 theblob kernel: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
Dec 05 21:26:31 theblob kernel: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Dec 05 21:26:31 theblob kernel: amdgpu: Failed to remove queue 0
Dec 05 21:26:33 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
Dec 05 21:26:33 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow start
Dec 05 21:26:33 theblob kernel: amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow done
Dec 05 21:26:33 theblob google-chrome.desktop[11352]: [22281:22281:1205/212633.285036:ERROR:vulkan_swap_chain.cc(404)] vkQueuePresentKHR() failed: -4
Dec 05 21:26:33 theblob google-chrome.desktop[11352]: [22281:22281:1205/212633.285264:ERROR:gpu_service_impl.cc(1105)] Exiting GPU process because some drivers can't recover from errors. GPU process will restart shortly.
Dec 05 21:26:33 theblob google-chrome.desktop[11352]: [11346:11346:1205/212633.301983:ERROR:gpu_process_host.cc(990)] GPU process exited unexpectedly: exit_code=8704
```

only way i can recover is with a full power cycle (off for a few seconds)

``` Linux theblob 6.2.0-37-generic #38~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov  2 18:01:13 UTC 2 x86_64 x86_64 x86_64 GNU/Linux```

```dpkg --list amdgpu*
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                 Version                     Architecture Description
+++-====================-===========================-============-====================================================
ii  amdgpu-core          1:5.7.50702-1683306.22.04   all          Core meta package for unified amdgpu driver.
ii  amdgpu-dkms          1:6.2.4.50702-1683306.22.04 all          amdgpu driver in DKMS format.
ii  amdgpu-dkms-firmware 1:6.2.4.50702-1683306.22.04 all          firmware blobs used by amdgpu driver in DKMS format
ii  amdgpu-dkms-headers  1:6.2.4.50702-1683306.22.04 all          amdgpu driver linux kernel headers
ii  amdgpu-install       5.7.50702-1683306.22.04     all          AMDGPU driver repository and installer
ii  amdgpu-lib           1:5.7.50702-1683306.22.04   amd64        Meta package to install amdgpu userspace components.
ii  amdgpu-top           0.2.3                       amd64        Tool to displays AMDGPU usage.
```



---

### 评论 #8 — sid-cypher (2023-12-26T07:54:24Z)

I've had this exact issue frequently with ROCm 5.7 on Radeon RX 7900 XTX.

Upgrading to ROCm 6.0 has solved it for me.
At least Stable Diffusion with torch-2.3.0+rocm5.7 still works on ROCm 6.0, and without crashes now, no need to restart after a failed GPU reset.

The non-critical GCVM_L2_PROTECTION_FAULT_STATUS errors are still there, but they don't force me to restart after MES failure and a GPU reset attempt.

Currently working: 
`Linux moon 6.2.0-39-generic #40~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 16 10:53:04 UTC 2 x86_64 x86_64 x86_64 GNU/Linux`
```
amdgpu-dkms/jammy,now 1:6.3.6.60000-1697589.22.04 all [installed]
amdgpu-install/jammy,now 6.0.60000-1697589.22.04 all [installed]
```


---

### 评论 #9 — selenologist (2024-01-29T14:38:35Z)

I am still seeing this on both ROCm 6.0 and the 6.0.1 packages at https://repo.radeon.com/rocm/apt/6.0.1 / https://repo.radeon.com/amdgpu/apt/6.0.1 on fresh Ubuntu 22.04.

`Linux amdsux 6.5.0-15-generic #15~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Jan 12 18:54:30 UTC 2 x86_64 x86_64 x86_64 GNU/Linux`

I realize it does no good for everyone else experiencing this issue to add yet another "yeah, same here" and some venting, so the rest of you may stop reading now. But AMD, you really need to know this is not acceptable.

It's been over a year since the card was released and still the software isn't even stable, let alone all the trouble it takes to get set up vs nVidia. All whilst AMD releases these frankly patronizing announcements about how great and open and "ready" ROCm 6.0 is, "driving an inflection with developers". Erm, yeah... it's making us run away.

Please understand developer sentiment towards AMD is very poor and getting worse, not better. Everyone else like me who is trying to do research but they bought an AMD card because they couldn't afford a nVidia card, is never ever going to buy an AMD GPU again. And we will tell our employers to never ever buy AMD too, and they will listen, *because developer time is far more expensive than nVidia's hardware*. We should have listened to our friends who told us to just buy nVidia cards, but we won't make this mistake again. This will last years and years. The best you can do now is admit your failures and try to salvage your reputation for CPUs. Because it doesn't matter how good or cheap your GPUs get, we will never risk wasting our time again.

For all this talk about openness, we're all here seeing this issue and does anyone outside AMD even understand what this message *means*? For that matter, does anyone INSIDE AMD understand what it means? Please explain it to us.

So far as I can tell, "MES" is the MicroEngine Scheduler, and https://docs.kernel.org/gpu/amdgpu/driver-core.html#graphics-and-compute-microcontrollers says it is "unused". Mumblings on the internet suggest it is used now, and well, we're in this GitHub issue together aren't we? Beyond that, things get extremely hazy. The kernel code that actually produces that log message is completely opaque. None of these functions are documented. MES is... a separate microcontroller controlled by a firmware blob? Do I have that right? And what *exactly* does this mean? https://github.com/torvalds/linux/blob/41bccc98fb7931d63d03f326a746ac4d429c1dd3/drivers/gpu/drm/amd/amdgpu/mes_v11_0.c#L563

Is this AMD's "open software approach"? Hanging binary blobs and sending tarballs to geohot that he's not allowed to distribute?!

PS: I'm still not over the terrible software support for the RX480 last time. I hoped things had changed. Fool me twice, shame on me. But never again. I'm losing my mind over this because I've lost months of productivity... I can't stress enough, my experiment seems to be working whilst I can get it to run. But the reason I cannot publish is because I chose the wrong GPU. I'm going to have to go get a "real job" instead.

---

### 评论 #10 — mgolub2 (2024-02-12T23:20:00Z)

Also seeing this issue, on ROCm 6.0.2, Ubuntu 22.04 fresh setup when running llama.cpp. Hardware is a AMD 7940HS CPU w/ Radeon 780M GPU. When loading up larger models and offloading more layers to the GPU, most of the time the GPU will reset with the MES panic, or just hang with hundreds of `[drm] Skip scheduling IBs!` messages. When the GPU hangs like this, modprobe -r amdgpu causes a segfault (!?), and a dmesg report about a kernel bug (!?x2): 
```text
[ 6854.988626] ------------[ cut here ]------------                                                                          
[ 6854.988627] kernel BUG at mm/slub.c:384!                                                                                  
[ 6854.988635] invalid opcode: 0000 [#1] SMP NOPTI                                                                           
[ 6854.988637] CPU: 1 PID: 193444 Comm: modprobe Tainted: G           OE     5.15.0-94-generic #104-Ubuntu                   
[ 6854.988640] Hardware name: Micro Computer (HK) Tech Limited Venus series/F7BSC, BIOS 1.09 11/20/2023                      
[ 6854.988641] RIP: 0010:__slab_free+0x1f3/0x370     
```        

If an AMD engineer (or anyone else!) could point to a place to investigate, or has any other idea, that would be helpful!                                                                 

---

### 评论 #11 — terryrankine (2024-02-13T01:00:56Z)

> 5.15.0-94-generic

Any reason you want to run the older kernel?

A few people are experiencing better results on the newer kernels, and the 6.0.2 drivers.

I got to a running setup (with some minor issues) with the 6.5.x stock one - ended up closing my ticket too. #2689 

---

### 评论 #12 — mgolub2 (2024-02-13T19:21:47Z)

> > 5.15.0-94-generic
> 
> Any reason you want to run the older kernel?
> 
> A few people are experiencing better results on the newer kernels, and the 6.0.2 drivers.
> 
> I got to a running setup (with some minor issues) with the 6.5.x stock one - ended up closing my ticket too. #2689

I have no idea actually, I just went through a standard ubuntu server 22.04 setup from what I recall (via a netboot, so maybe the installer is missing the HWE option? I did not see it at least), after a quick `sudo apt install -y linux-image-generic-hwe-22.04` and reboot, now on kernel `6.5.0-17-generic #17~22.04.1-Ubuntu` things don't seem to have improved for me - I still get gpu resets: 

```bash
│[33693.746423] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
│[33693.746596] amdgpu: failed to remove hardware queue from MES, doorbell=0x1002                
│[33693.746606] amdgpu: MES might be in unrecoverable state, issue a GPU reset                                          
│[33693.746614] amdgpu: Failed to evict queue 1                                                                              
│[33693.746620] amdgpu: Failed to evict process queues                                                                       
│[33693.746949] amdgpu 0000:c5:00.0: amdgpu: GPU reset begin!                                                                
│[33693.917504] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
│[33693.917664] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
│[33693.924953] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
│[33693.925108] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
│[33694.045099] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
│[33694.045218] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
│[33694.052583] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
│[33694.052702] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
│[33694.172644] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
```

After that happens, the GPU is unusable until a full reboot. 

---

### 评论 #13 — selenologist (2024-02-13T20:00:26Z)

Okay what the fuck. I've just captured a log with MES-related messages (and some others) from a system that was idle and hadn't even run a real workload yet. I don't know if this bug is related (because I don't have a clue what's on the other side of your blob wall or what much of this opaque code does) but there are MES messages, so, well, here we go.

```
[31317.644104] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
[31317.644111] amdgpu 0000:0d:00.0: amdgpu: Failed to export SMU metrics table!
[31317.644112] amdgpu 0000:0d:00.0: amdgpu: Failed to get current clock freq!
[31321.920024] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
[31321.920028] amdgpu 0000:0d:00.0: amdgpu: Failed to export SMU metrics table!
[31326.191767] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
[31326.191772] amdgpu 0000:0d:00.0: amdgpu: Failed to export SMU metrics table!
[31327.729436] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring gfx_0.0.0 timeout, signaled seq=613206, emitted seq=613208
[31327.729995] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process plasmashell pid 3182 thread plasmashel:cs0 pid 3224
[31327.730545] amdgpu 0000:0d:00.0: amdgpu: GPU reset begin!
[31328.743414] amdgpu 0000:0d:00.0: amdgpu: IP block:gfx_v11_0 is hung!
[31329.767382] [drm:sdma_v6_0_ring_test_ib [amdgpu]] *ERROR* amdgpu: IB test timed out
[31329.767916] amdgpu 0000:0d:00.0: amdgpu: IP block:sdma_v6_0 is hung!
[31329.768161] [drm] kiq ring mec 3 pipe 1 q 0
[31330.008807] amdgpu 0000:0d:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring mes_kiq_3.1.0 test failed (-110)
[31330.009039] [drm:amdgpu_gfx_enable_kcq [amdgpu]] *ERROR* KCQ enable failed
[31330.009290] amdgpu 0000:0d:00.0: amdgpu: soft reset failed, will fallback to full reset!
[31330.479483] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
[31330.479487] amdgpu 0000:0d:00.0: amdgpu: Failed to export SMU metrics table!
[31334.746500] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
[31334.746505] amdgpu 0000:0d:00.0: amdgpu: Failed to disable gfxoff!
[31339.013104] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
[31339.013107] amdgpu 0000:0d:00.0: amdgpu: [SetDfCstate] failed!
[31339.013109] amdgpu 0000:0d:00.0: amdgpu: Failed to disallow df cstate
[31341.566559] [drm] psp gfx command INVOKE_CMD(0x3) failed and response status is (0x0)
[31345.514564] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31345.514834] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31345.636256] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31345.636512] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31345.757963] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31345.758218] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31345.879631] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31345.879887] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31346.001297] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31346.001552] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31346.122973] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31346.123230] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31346.244645] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31346.244900] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31346.366313] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31346.366568] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31346.487977] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
[31346.488232] [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
[31348.539759] [drm] psp gfx command UNLOAD_TA(0x2) failed and response status is (0x0)
[31348.539764] [drm:psp_suspend [amdgpu]] *ERROR* Failed to terminate ras ta
[31348.540218] [drm:amdgpu_device_ip_suspend_phase2 [amdgpu]] *ERROR* suspend of IP block <psp> failed -22
[31348.541779] amdgpu 0000:0d:00.0: amdgpu: MODE1 reset
[31348.541783] amdgpu 0000:0d:00.0: amdgpu: GPU mode1 reset
[31348.541843] amdgpu 0000:0d:00.0: amdgpu: GPU smu mode1 reset
[31352.825254] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
[31352.825259] amdgpu 0000:0d:00.0: amdgpu: GPU mode1 reset failed
[31352.825334] amdgpu 0000:0d:00.0: amdgpu: ASIC reset failed with error, -62 for drm dev, 0000:0d:00.0
[31357.080573] amdgpu 0000:0d:00.0: amdgpu: GPU reset succeeded, trying to resume
[31357.080830] [drm] PCIE GART of 512M enabled (table at 0x0000008000800000).
[31357.080897] [drm] VRAM is lost due to GPU reset!
[31357.080898] [drm] PSP is resuming...
[31357.320464] [drm:psp_hw_start [amdgpu]] *ERROR* PSP create ring failed!
[31357.320721] [drm:psp_resume [amdgpu]] *ERROR* PSP resume failed
[31357.320968] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* resume of IP block <psp> failed -62
[31357.321238] [drm] Skip scheduling IBs!
[31357.321257] [drm] Skip scheduling IBs!
```

I'm thinking it's time to RMA my card. This is unfair to the card manufacturer and retailer who have to deal with this, only reason I've been putting it off. But come on, really, what is this?

Full details:
I returned to my Kubuntu install that I was trying to do real work on, but after cold booting the system and logging in, I ended up just going to bed. Aside from displaying a KDE plasma desktop on Wayland, the GPU didn't do anything taxing. I woke up to find my screen off and system unresponsive, so I logged in over SSH from another computer and retrieved this log from `dmesg`. Kernel is `6.5.0-17-generic`.

So, wait... AMD cards aren't even stable handling a basic plasmashell desktop? Really?

Also I want to take this opportunity to clarify my position to AMD's engineers. I'm not mad at you. You guys probably hate this too. I think we're on the same team. I'm furious at the company and the situation though, because I feel lied to, scammed even. My messages here are not intended to be hostile, however, and I want to indicate that I am, you know, capable of calm discussion. I'm not going to just jump on anyone who tries to help.

PS: if recent kernels help, with patches not backported into the fresh-install Ubuntu kernel the AMD documentation implicitly assumes, then said documentation should include instructions on installing an updated kernel. Thanks for bringing that up terryrankine.

---

### 评论 #14 — mgolub2 (2024-02-13T21:05:38Z)

> PS: if recent kernels help, with patches not backported into the fresh-install Ubuntu kernel the AMD documentation implicitly assumes, then said documentation should include instructions on installing an updated kernel. Thanks for bringing that up terryrankine.

Sadly it did not help me :( High VRAM workloads still cause the MES unrecoverable error, every time, which requires a reboot to solve. 

---

### 评论 #15 — selenologist (2024-02-13T21:14:33Z)

> Sadly it did not help me :( High VRAM workloads still cause the MES unrecoverable error, every time, which requires a reboot to solve.

That is also the case for me - hey, it's weird how using more VRAM makes it more likely, isn't? Maybe some allocator race? ... really though, AMD should be paying me even to speculate about what's going wrong on the proprietary side.

Also I said before that I thought it wasn't helpful for me to add a "same here" but I've realized, anyone having this issue should absolutely post about it here. Let 'em see us.

From statements like "We are hoping that this will improve your perception of AMD products and this will be reflected in your public messaging", we know that public perception is what the company cares about, not whether people are having an issue. Let your public messaging reflect your actual perception.

---

### 评论 #16 — terryrankine (2024-02-14T08:22:33Z)

and just checking - you are on new kernels with the 6.0.2 binaries or your code compiled against the 6.0.2 libs?
(yes - i have had to compile pytorch against 6.0.2).

mainly because i finally got there - and closed my ticket....  #2689 

Im not saying it wasnt easy or simple but I can hit 20-22Gb consistently somehow now.... and Im over like 3 days of uptime too... which is a first since november last year...


```
terryr@theblob:~$ uname -a
Linux theblob 6.5.0-18-generic #18~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Feb  7 11:40:03 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```




```
terryr@theblob:~$ hipconfig
HIP version  : 6.0.32831-204d35d16

== hipconfig
HIP_PATH     : /opt/rocm-6.0.2
ROCM_PATH    : /opt/rocm-6.0.2
HIP_COMPILER : clang
HIP_PLATFORM : amd
HIP_RUNTIME  : rocclr
CPP_CONFIG   :  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.0.2/include -I/opt/rocm-6.0.2/lib/llvm/lib/clang/17.0.0
```

and here is the worst ever way to show what ubuntu libs got me there....
```
terryr@theblob:~$ dpkg -l | grep -E "rocm|hip|AMD "
ii  amd-smi-lib                                    23.4.2.60002-115~22.04                     amd64        AMD System Management libraries
ii  amd64-microcode                                3.20191218.1ubuntu2.2                      amd64        Processor microcode firmware for AMD CPUs
ii  composablekernel-dev                           1.1.0.60002-115~22.04                      amd64        High Performance Composable Kernel for AMD GPUs
ii  hip-dev                                        6.0.32831.60002-115~22.04                  amd64        HIP:Heterogenous-computing Interface for Portability
ii  hip-doc                                        6.0.32831.60002-115~22.04                  amd64        HIP:Heterogenous-computing Interface for Portability
ii  hip-runtime-amd                                6.0.32831.60002-115~22.04                  amd64        HIP:Heterogenous-computing Interface for Portability
ii  hip-samples                                    6.0.32831.60002-115~22.04                  amd64        HIP: Heterogenous-computing Interface for Portability [HIP SAMPLES]
ii  hipblas                                        2.0.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
ii  hipblas-dev                                    2.0.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
ii  hipblaslt                                      0.6.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
ii  hipblaslt-dev                                  0.6.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
ii  hipcc                                          1.0.0.60002-115~22.04                      amd64        HIP Compiler Driver
ii  hipcub-dev                                     3.0.0.60002-115~22.04                      amd64        hipCUB (rocPRIM backend)
ii  hipfft                                         1.0.13.60002-115~22.04                     amd64        ROCm FFT marshalling library
ii  hipfft-dev                                     1.0.13.60002-115~22.04                     amd64        ROCm FFT marshalling library
ii  hipfort-dev                                    0.4.0.60002-115~22.04                      amd64        Fortran Interface For GPU Kernel Libraries
ii  hipify-clang                                   17.0.0.60002-115~22.04                     amd64        Hipify CUDA source
ii  hiprand                                        2.10.16.60002-115~22.04                    amd64        Radeon Open Compute RAND library
ii  hiprand-dev                                    2.10.16.60002-115~22.04                    amd64        Radeon Open Compute RAND library
ii  hipsolver                                      2.0.0.60002-115~22.04                      amd64        Radeon Open Compute LAPACK marshalling library
ii  hipsolver-dev                                  2.0.0.60002-115~22.04                      amd64        Radeon Open Compute LAPACK marshalling library
ii  hipsparse                                      3.0.0.60002-115~22.04                      amd64        ROCm SPARSE library
ii  hipsparse-dev                                  3.0.0.60002-115~22.04                      amd64        ROCm SPARSE library
ii  hiptensor                                      1.1.0.60002-115~22.04                      amd64        Adaptation library of tensor contraction with composable_kernel backend
ii  hiptensor-dev                                  1.1.0.60002-115~22.04                      amd64        Adaptation library of tensor contraction with composable_kernel backend
ii  hsa-amd-aqlprofile                             1.0.0.60002.60002-115~22.04                amd64        AQLPROFILE library for AMD HSA runtime API extension support
ii  hsa-rocr                                       1.12.0.60002-115~22.04                     amd64        AMD Heterogeneous System Architecture HSA - Linux HSA Runtime for Boltzmann (ROCm) platforms
ii  hsa-rocr-dev                                   1.12.0.60002-115~22.04                     amd64        AMD Heterogeneous System Architecture HSA development package.
ii  libflashrom1:amd64                             1.2-5build1                                amd64        Identify, read, write, erase, and verify BIOS/ROM/flash chips - library
ii  libresid-builder0c2a                           2.1.1-15ubuntu2                            amd64        SID chip emulation class based on resid
ii  miopen-hip                                     3.00.0.60002-115~22.04                     amd64        AMD's DNN Library
ii  miopen-hip-dev                                 3.00.0.60002-115~22.04                     amd64        AMD's DNN Library
ii  mivisionx                                      2.5.0.60002-115~22.04                      amd64        AMD MIVisionX is a comprehensive Computer Vision and ML Inference Toolkit
ii  rocblas                                        4.0.0.60002-115~22.04                      amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
ii  rocblas-dev                                    4.0.0.60002-115~22.04                      amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
ii  rocm                                           6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) software stack meta package
ii  rocm-clang-ocl                                 0.5.0.60002-115~22.04                      amd64        OpenCL compilation with clang compiler.
ii  rocm-cmake                                     0.11.0.60002-115~22.04                     amd64        rocm-cmake built using CMake
ii  rocm-core                                      6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-dbgapi                                    0.71.0.60002-115~22.04                     amd64        Library to provide AMD GPU debugger API
ii  rocm-debug-agent                               2.0.3.60002-115~22.04                      amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
ii  rocm-dev                                       6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-developer-tools                           6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-device-libs                               1.0.0.60002-115~22.04                      amd64        Radeon Open Compute - device libraries
ii  rocm-gdb                                       13.2.60002-115~22.04                       amd64        ROCgdb
ii  rocm-hip-libraries                             6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime                               6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-runtime-dev                           6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-hip-sdk                                   6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-language-runtime                          6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-libs                                      6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-llvm                                      17.0.0.24012.60002-115~22.04               amd64        ROCm compiler
ii  rocm-ml-libraries                              6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ml-sdk                                    6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-ocl-icd                                   2.0.0.60002-115~22.04                      amd64        clr built using CMake
ii  rocm-opencl                                    2.0.0.60002-115~22.04                      amd64        clr built using CMake
ii  rocm-opencl-dev                                2.0.0.60002-115~22.04                      amd64        clr built using CMake
ii  rocm-opencl-runtime                            6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-opencl-sdk                                6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocm-openmp-sdk                                6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
ii  rocm-smi-lib                                   6.0.0.60002-115~22.04                      amd64        AMD System Management libraries
ii  rocm-utils                                     6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
ii  rocminfo                                       1.0.0.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool
ii  rocprofiler                                    2.0.60002.60002-115~22.04                  amd64        ROCPROFILER library for AMD HSA runtime API extension support
ii  rocprofiler-dev                                2.0.60002.60002-115~22.04                  amd64        ROCPROFILER library for AMD HSA runtime API extension support
ii  rocprofiler-plugins                            2.0.60002.60002-115~22.04                  amd64        ROCPROFILER library for AMD HSA runtime API extension support
ii  rocsolver                                      3.24.0.60002-115~22.04                     amd64        AMD ROCm SOLVER library
ii  rocsolver-dev                                  3.24.0.60002-115~22.04                     amd64        AMD ROCm SOLVER library
ii  roctracer                                      4.1.60002.60002-115~22.04                  amd64        AMD ROCTRACER library
ii  roctracer-dev                                  4.1.60002.60002-115~22.04                  amd64        AMD ROCTRACER library
```

and then made pytorch find the folder and run the special pytorch convert from cuda to hip and then build, and then build and install, and then build pytorchvision and audio after.... so much faf.....

But - I run now.... 

---

### 评论 #17 — mergmann (2024-02-14T20:32:38Z)

On my arch installation I have run into this issue multiple times with rocm 5.6-6.0. I can't even open blender or libreoffice with hardware acceleration enabled. llama.cpp (with CLBlast) crashes even without offloading layers to GPU Especially OpenCL workloads seem to be problematic. Running a very simple kernel `arr[get_global_id(0)] += num;` triggers the page fault error, but that seems to not be a problem. Looping over that code 1024\*1024\*1024 times causes the driver to timeout and reset recoverably. I even tried allocating a 16GB buffer, which worked fine. I wasn't able to reproduce the MES error. However starting llama.cpp caused it again. On ubuntu pytorch mostly works, but blender and llama.cpp still cause unrecoverable gpu crashes. I hope this gets fixed soon as I wasn't able to use my card for anything else than graphics. I never really had problems with vulkan or OpenGL, it's just ROCm that appears to be broken.

---

### 评论 #18 — mgolub2 (2024-02-17T17:07:51Z)

> and just checking - you are on new kernels with the 6.0.2 binaries or your code compiled against the 6.0.2 libs? (yes - i have had to compile pytorch against 6.0.2).
> 
> mainly because i finally got there - and closed my ticket.... #2689
> 
> Im not saying it wasnt easy or simple but I can hit 20-22Gb consistently somehow now.... and Im over like 3 days of uptime too... which is a first since november last year...
> 
> ```
> terryr@theblob:~$ uname -a
> Linux theblob 6.5.0-18-generic #18~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Wed Feb  7 11:40:03 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
> ```
> 
>  ```
> terryr@theblob:~$ hipconfig
> HIP version  : 6.0.32831-204d35d16
> 
> == hipconfig
> HIP_PATH     : /opt/rocm-6.0.2
> ROCM_PATH    : /opt/rocm-6.0.2
> HIP_COMPILER : clang
> HIP_PLATFORM : amd
> HIP_RUNTIME  : rocclr
> CPP_CONFIG   :  -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm-6.0.2/include -I/opt/rocm-6.0.2/lib/llvm/lib/clang/17.0.0
> ```
> 
> and here is the worst ever way to show what ubuntu libs got me there....
> 
> ```
> terryr@theblob:~$ dpkg -l | grep -E "rocm|hip|AMD "
> ii  amd-smi-lib                                    23.4.2.60002-115~22.04                     amd64        AMD System Management libraries
> ii  amd64-microcode                                3.20191218.1ubuntu2.2                      amd64        Processor microcode firmware for AMD CPUs
> ii  composablekernel-dev                           1.1.0.60002-115~22.04                      amd64        High Performance Composable Kernel for AMD GPUs
> ii  hip-dev                                        6.0.32831.60002-115~22.04                  amd64        HIP:Heterogenous-computing Interface for Portability
> ii  hip-doc                                        6.0.32831.60002-115~22.04                  amd64        HIP:Heterogenous-computing Interface for Portability
> ii  hip-runtime-amd                                6.0.32831.60002-115~22.04                  amd64        HIP:Heterogenous-computing Interface for Portability
> ii  hip-samples                                    6.0.32831.60002-115~22.04                  amd64        HIP: Heterogenous-computing Interface for Portability [HIP SAMPLES]
> ii  hipblas                                        2.0.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
> ii  hipblas-dev                                    2.0.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
> ii  hipblaslt                                      0.6.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
> ii  hipblaslt-dev                                  0.6.0.60002-115~22.04                      amd64        Radeon Open Compute BLAS marshalling library
> ii  hipcc                                          1.0.0.60002-115~22.04                      amd64        HIP Compiler Driver
> ii  hipcub-dev                                     3.0.0.60002-115~22.04                      amd64        hipCUB (rocPRIM backend)
> ii  hipfft                                         1.0.13.60002-115~22.04                     amd64        ROCm FFT marshalling library
> ii  hipfft-dev                                     1.0.13.60002-115~22.04                     amd64        ROCm FFT marshalling library
> ii  hipfort-dev                                    0.4.0.60002-115~22.04                      amd64        Fortran Interface For GPU Kernel Libraries
> ii  hipify-clang                                   17.0.0.60002-115~22.04                     amd64        Hipify CUDA source
> ii  hiprand                                        2.10.16.60002-115~22.04                    amd64        Radeon Open Compute RAND library
> ii  hiprand-dev                                    2.10.16.60002-115~22.04                    amd64        Radeon Open Compute RAND library
> ii  hipsolver                                      2.0.0.60002-115~22.04                      amd64        Radeon Open Compute LAPACK marshalling library
> ii  hipsolver-dev                                  2.0.0.60002-115~22.04                      amd64        Radeon Open Compute LAPACK marshalling library
> ii  hipsparse                                      3.0.0.60002-115~22.04                      amd64        ROCm SPARSE library
> ii  hipsparse-dev                                  3.0.0.60002-115~22.04                      amd64        ROCm SPARSE library
> ii  hiptensor                                      1.1.0.60002-115~22.04                      amd64        Adaptation library of tensor contraction with composable_kernel backend
> ii  hiptensor-dev                                  1.1.0.60002-115~22.04                      amd64        Adaptation library of tensor contraction with composable_kernel backend
> ii  hsa-amd-aqlprofile                             1.0.0.60002.60002-115~22.04                amd64        AQLPROFILE library for AMD HSA runtime API extension support
> ii  hsa-rocr                                       1.12.0.60002-115~22.04                     amd64        AMD Heterogeneous System Architecture HSA - Linux HSA Runtime for Boltzmann (ROCm) platforms
> ii  hsa-rocr-dev                                   1.12.0.60002-115~22.04                     amd64        AMD Heterogeneous System Architecture HSA development package.
> ii  libflashrom1:amd64                             1.2-5build1                                amd64        Identify, read, write, erase, and verify BIOS/ROM/flash chips - library
> ii  libresid-builder0c2a                           2.1.1-15ubuntu2                            amd64        SID chip emulation class based on resid
> ii  miopen-hip                                     3.00.0.60002-115~22.04                     amd64        AMD's DNN Library
> ii  miopen-hip-dev                                 3.00.0.60002-115~22.04                     amd64        AMD's DNN Library
> ii  mivisionx                                      2.5.0.60002-115~22.04                      amd64        AMD MIVisionX is a comprehensive Computer Vision and ML Inference Toolkit
> ii  rocblas                                        4.0.0.60002-115~22.04                      amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
> ii  rocblas-dev                                    4.0.0.60002-115~22.04                      amd64        rocBLAS is AMD's library for BLAS on ROCm. It is implemented in HIP and optimized for AMD GPUs.
> ii  rocm                                           6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) software stack meta package
> ii  rocm-clang-ocl                                 0.5.0.60002-115~22.04                      amd64        OpenCL compilation with clang compiler.
> ii  rocm-cmake                                     0.11.0.60002-115~22.04                     amd64        rocm-cmake built using CMake
> ii  rocm-core                                      6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-dbgapi                                    0.71.0.60002-115~22.04                     amd64        Library to provide AMD GPU debugger API
> ii  rocm-debug-agent                               2.0.3.60002-115~22.04                      amd64        Radeon Open Compute Debug Agent (ROCdebug-agent)
> ii  rocm-dev                                       6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-developer-tools                           6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-device-libs                               1.0.0.60002-115~22.04                      amd64        Radeon Open Compute - device libraries
> ii  rocm-gdb                                       13.2.60002-115~22.04                       amd64        ROCgdb
> ii  rocm-hip-libraries                             6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-hip-runtime                               6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-hip-runtime-dev                           6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-hip-sdk                                   6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-language-runtime                          6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-libs                                      6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-llvm                                      17.0.0.24012.60002-115~22.04               amd64        ROCm compiler
> ii  rocm-ml-libraries                              6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-ml-sdk                                    6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-ocl-icd                                   2.0.0.60002-115~22.04                      amd64        clr built using CMake
> ii  rocm-opencl                                    2.0.0.60002-115~22.04                      amd64        clr built using CMake
> ii  rocm-opencl-dev                                2.0.0.60002-115~22.04                      amd64        clr built using CMake
> ii  rocm-opencl-runtime                            6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-opencl-sdk                                6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocm-openmp-sdk                                6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) OpenMP Software development Kit.
> ii  rocm-smi-lib                                   6.0.0.60002-115~22.04                      amd64        AMD System Management libraries
> ii  rocm-utils                                     6.0.2.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime software stack
> ii  rocminfo                                       1.0.0.60002-115~22.04                      amd64        Radeon Open Compute (ROCm) Runtime rocminfo tool
> ii  rocprofiler                                    2.0.60002.60002-115~22.04                  amd64        ROCPROFILER library for AMD HSA runtime API extension support
> ii  rocprofiler-dev                                2.0.60002.60002-115~22.04                  amd64        ROCPROFILER library for AMD HSA runtime API extension support
> ii  rocprofiler-plugins                            2.0.60002.60002-115~22.04                  amd64        ROCPROFILER library for AMD HSA runtime API extension support
> ii  rocsolver                                      3.24.0.60002-115~22.04                     amd64        AMD ROCm SOLVER library
> ii  rocsolver-dev                                  3.24.0.60002-115~22.04                     amd64        AMD ROCm SOLVER library
> ii  roctracer                                      4.1.60002.60002-115~22.04                  amd64        AMD ROCTRACER library
> ii  roctracer-dev                                  4.1.60002.60002-115~22.04                  amd64        AMD ROCTRACER library
> ```
> 
> and then made pytorch find the folder and run the special pytorch convert from cuda to hip and then build, and then build and install, and then build pytorchvision and audio after.... so much faf.....
> 
> But - I run now....

Yes, I made sure to reinstall rocm 6.0.2, and do a clean build of llama.cpp - No change for me sadly. I might try it again to see if I missed something, always possible. 

Out of curiosity, what mode is you apu in for VRAM? auto or do you have it set to dedicated mode? 

---

### 评论 #19 — selenologist (2024-02-17T21:25:02Z)

I might have a workaround that maybe helps a little, or it might just be placebo / luck so far. **There are potential drawbacks, though**.

I noticed that sometimes, but not always, there would be IOMMU fault messages prior to the ones from the amdgpu driver itself. So I thought, hey why not, let's try disabling IOMMU in BIOS. And so far, I've been able to run things ... I don't trust it, obviously even if this works it's not a solution, but I thought I'd share. Those faults were obviously happening for a reason and this seems to just be putting a blindfold on.

Here's a chat with Gemini about the consequences of disabling IOMMU https://g.co/gemini/share/5d21ada997c1 , **please weigh it up yourself before trying it**. I don't understand IOMMU properly myself.

PS: I captured this earlier after booting my system and leaving it idle, not even logging in yet:
```
[  555.894238] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
```
(and then the usual circus follows - this is just the start for demonstration)
So not even 10 minutes, under no load, with nothing loaded except a Kubuntu login screen. Something is very wrong.

---

### 评论 #20 — mergmann (2024-02-22T15:26:43Z)

Yesterday I tried running some AI workloads with ROCm 6.0.0 and PyTorch ROCm 6.0 on my main system, but already very simple tensor operations with pytorch crashed the driver with the `MES failed to response` messages. I then booted into ubuntu (the same version of ROCm), retried the same tensor operations there and it worked mostly fine. I then upgraded to ROCm on ubuntu to the newest version and it still worked. Today I booted into my arch installation again, which still has ROCm 6.0.0, but even running heavy workloads like Stable Diffusion and llama.cpp work fine, even at 18/20GB VRAM. My best guess is that upgrading ROCm on ubuntu also installed a firmware update for the GPU, but I'm not certain that the firmware was the root cause.
Anyways, I'll watch how well ROCm performs over the next few days as there are still harmless page faults appearing out of nowhere.

---

### 评论 #21 — briansp2020 (2024-02-22T17:24:00Z)

@MattisBergmann
Did you try ROCm 6.0.2? I think it fixed some driver issues and it was much more stable for me.

---

### 评论 #22 — FeepingCreature (2024-03-20T18:37:29Z)

I'm getting "MES failed to response" with ROCM 6.0.2, freshly updated.

---

### 评论 #23 — Disty0 (2024-03-24T19:51:15Z)

Using an RX 7900 XTX with no monitor attached, training a diffusion model or just running inference.
(Getting monitor output from another GPU.)

Still seeing the same MES hangs with Arch Linux 6.8.1-arch1-1 / ROCm 6.0.2 / PyTorch 2.4.0.dev20240323+rocm6.0
This MES hang causes other unrelated Python programs to core dump too and GPU keeps pulling 120W~ of power when it hangs.

Only way to recover from the hang is running `rocm-smi --gpureset -id 0` if you have no monitor attached to the AMD GPU.
If you have a monitor attached, only way to recover is hard rebooting.

Adding `amdgpu.mes=0 amdgpu.mes_kiq=1` to the grub config doesn't seem to be doing anything either.

Log on PyTorch when MES hangs:
```
HW Exception by GPU node-1 (Agent handle: 0x62e2bc7e39b0) reason :GPU Hang                                            
HW Exception by GPU node-1 (Agent handle: 0x5fb477fb5bd0) reason :GPU Hang
```

Journalctl in reverse order:
<details>

```

Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset(6) succeeded!
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow done
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow start
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: [drm:jpeg_v4_0_hw_init [amdgpu]] JPEG decode initialized successfully.
Mar 24 23:48:30 ArchDesktop kernel: [drm] VCN decode and encode initialized successfully(under DPG Mode).
Mar 24 23:48:30 ArchDesktop kernel: [drm] kiq ring mec 3 pipe 1 q 0
Mar 24 23:48:30 ArchDesktop kernel: [drm] DMUB hardware initialized: version=0x07002600
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: SMU is resumed successfully!
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: SMU driver if version not matched
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x0000003f, smu fw program = 0, smu fw version = 0x004e7900 (78.121.0)
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: SMU is resuming...
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: RAP: optional rap ta ucode is not available
Mar 24 23:48:30 ArchDesktop kernel: [drm] reserve 0x1300000 from 0x85fc000000 for PSP TMR
Mar 24 23:48:30 ArchDesktop kernel: [drm] PSP is resuming...
Mar 24 23:48:30 ArchDesktop kernel: [drm] VRAM is lost due to GPU reset!
Mar 24 23:48:30 ArchDesktop kernel: [drm] PCIE GART of 512M enabled (table at 0x00000085FEB00000).
Mar 24 23:48:30 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: failed to write reg 1a774 wait reg 1a786
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.9952] device (enp9s0): state change: config -> ip-config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.9944] device (enp9s0): state change: prepare -> config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.9942] device (enp9s0): state change: disconnected -> prepare (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.9942] device (enp9s0): Activation: starting connection 'Wired connection 2' (62e3e280-6724-3d24-acb4-5a448d676dc1)
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.9939] policy: auto-activating connection 'Wired connection 2' (62e3e280-6724-3d24-acb4-5a448d676dc1)
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.9899] device (enp9s0): state change: failed -> disconnected (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <warn>  [1711313300.9897] device (enp9s0): Activation: failed for connection 'Wired connection 2'
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.9894] device (enp9s0): state change: ip-config -> failed (reason 'ip-config-unavailable', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.0051] device (enp17s0f3u1u4c2): state change: config -> ip-config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.0048] device (enp17s0f3u1u4c2): state change: prepare -> config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.0046] device (enp17s0f3u1u4c2): state change: disconnected -> prepare (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.0046] device (enp17s0f3u1u4c2): Activation: starting connection 'Wired connection 1' (cee10dfa-cf9b-30c9-bb69-b8483b0cb52e)
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.0044] policy: auto-activating connection 'Wired connection 1' (cee10dfa-cf9b-30c9-bb69-b8483b0cb52e)
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.0028] device (enp17s0f3u1u4c2): state change: failed -> disconnected (reason 'none', sys-iface-state: 'managed')
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <warn>  [1711313300.0027] device (enp17s0f3u1u4c2): Activation: failed for connection 'Wired connection 1'
Mar 24 23:48:20 ArchDesktop NetworkManager[650]: <info>  [1711313300.0025] device (enp17s0f3u1u4c2): state change: ip-config -> failed (reason 'ip-config-unavailable', sys-iface-state: 'managed')
Mar 24 23:48:11 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset succeeded, trying to resume
Mar 24 23:48:11 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU smu mode1 reset
Mar 24 23:48:11 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU mode1 reset
Mar 24 23:48:11 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: MODE1 reset
Mar 24 23:48:11 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset begin!
Mar 24 23:48:11 ArchDesktop sudo[715870]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Mar 24 23:48:11 ArchDesktop sudo[715870]:    disty : TTY=pts/11 ; PWD=/home/disty ; USER=root ; COMMAND=/opt/rocm/bin/rocm-smi --gpureset -id 0
Mar 24 23:48:01 ArchDesktop polkitd[799]: Unregistered Authentication Agent for unix-process:715300:1283849 (system bus name :1.293, object path /org/freedesktop/PolicyKit1/AuthenticationAgent, locale C)
Mar 24 23:48:01 ArchDesktop polkitd[799]: Registered Authentication Agent for unix-process:715300:1283849 (system bus name :1.293 [flatpak list], object path /org/freedesktop/PolicyKit1/AuthenticationAgent, locale C)
Mar 24 23:48:01 ArchDesktop systemd[1423]: Started VTE child process 715193 launched by terminator process 3301.
Mar 24 23:48:01 ArchDesktop systemd[1423]: Started Application launched by gsd-media-keys.
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.9684] device (enp9s0): state change: config -> ip-config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.9676] device (enp9s0): state change: prepare -> config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.9674] device (enp9s0): state change: disconnected -> prepare (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.9674] device (enp9s0): Activation: starting connection 'Wired connection 2' (62e3e280-6724-3d24-acb4-5a448d676dc1)
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.9671] policy: auto-activating connection 'Wired connection 2' (62e3e280-6724-3d24-acb4-5a448d676dc1)
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.9635] device (enp9s0): state change: failed -> disconnected (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <warn>  [1711313268.9633] device (enp9s0): Activation: failed for connection 'Wired connection 2'
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.9630] device (enp9s0): state change: ip-config -> failed (reason 'ip-config-unavailable', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.8883] device (enp17s0f3u1u4c2): state change: config -> ip-config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.8880] device (enp17s0f3u1u4c2): state change: prepare -> config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.8878] device (enp17s0f3u1u4c2): state change: disconnected -> prepare (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.8877] device (enp17s0f3u1u4c2): Activation: starting connection 'Wired connection 1' (cee10dfa-cf9b-30c9-bb69-b8483b0cb52e)
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.8875] policy: auto-activating connection 'Wired connection 1' (cee10dfa-cf9b-30c9-bb69-b8483b0cb52e)
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.8858] device (enp17s0f3u1u4c2): state change: failed -> disconnected (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <warn>  [1711313268.8856] device (enp17s0f3u1u4c2): Activation: failed for connection 'Wired connection 1'
Mar 24 23:47:48 ArchDesktop NetworkManager[650]: <info>  [1711313268.8853] device (enp17s0f3u1u4c2): state change: ip-config -> failed (reason 'ip-config-unavailable', sys-iface-state: 'managed')
Mar 24 23:47:36 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-14bb5ff055db7dcdcc06326f2fa7fbb6d76de5cfea69cc5b21c77f71c6196aa1-runc.sgPTpd.mount: Deactivated successfully.
Mar 24 23:47:21 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:47:21 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:47:20 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-5a1186cf6856d30309d76d966166ed3cc7784062ee5ef6ab1bc95cb08f9f63b2-runc.RwPFQ6.mount: Deactivated successfully.
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0344] device (enp9s0): state change: config -> ip-config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0340] device (enp17s0f3u1u4c2): state change: config -> ip-config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0332] device (enp9s0): state change: prepare -> config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0330] device (enp9s0): state change: disconnected -> prepare (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0327] device (enp17s0f3u1u4c2): state change: prepare -> config (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0325] device (enp17s0f3u1u4c2): state change: disconnected -> prepare (reason 'none', sys-iface-state: 'managed')
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0325] device (enp9s0): Activation: starting connection 'Wired connection 2' (62e3e280-6724-3d24-acb4-5a448d676dc1)
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0323] device (enp17s0f3u1u4c2): Activation: starting connection 'Wired connection 1' (cee10dfa-cf9b-30c9-bb69-b8483b0cb52e)
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0321] policy: auto-activating connection 'Wired connection 2' (62e3e280-6724-3d24-acb4-5a448d676dc1)
Mar 24 23:47:17 ArchDesktop NetworkManager[650]: <info>  [1711313237.0320] policy: auto-activating connection 'Wired connection 1' (cee10dfa-cf9b-30c9-bb69-b8483b0cb52e)
Mar 24 23:47:10 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-14bb5ff055db7dcdcc06326f2fa7fbb6d76de5cfea69cc5b21c77f71c6196aa1-runc.M1x50P.mount: Deactivated successfully.
Mar 24 23:46:57 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:46:57 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:46:45 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-14bb5ff055db7dcdcc06326f2fa7fbb6d76de5cfea69cc5b21c77f71c6196aa1-runc.7mvaDi.mount: Deactivated successfully.
Mar 24 23:46:09 ArchDesktop systemd[1423]: app-gnome-gnome\x2dsystem\x2dmonitor-708305.scope: Consumed 1.044s CPU time.
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:5339:3-19: No property named "-gtk-icon-effect"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser warning: gtk.css:5308:3-5309:1: Expected ';' at end of block
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:5107:12-15: "mix" is not a valid color name.
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:5103:12-15: "mix" is not a valid color name.
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:5076:12-17: "shade" is not a valid color name.
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:5016:12-17: "shade" is not a valid color name.
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4337:3-35: No property named "-gtk-outline-bottom-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4335:3-34: No property named "-gtk-outline-bottom-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4328:3-32: No property named "-gtk-outline-top-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4326:3-31: No property named "-gtk-outline-top-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4287:23-37: Not a valid image
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4213:7-38: No property named "-gtk-outline-bottom-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4211:7-35: No property named "-gtk-outline-top-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4208:7-39: No property named "-gtk-outline-bottom-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4206:7-36: No property named "-gtk-outline-top-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4200:5-37: No property named "-gtk-outline-bottom-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4198:5-36: No property named "-gtk-outline-bottom-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4195:5-34: No property named "-gtk-outline-top-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4193:5-33: No property named "-gtk-outline-top-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4190:9-41: No property named "-gtk-outline-bottom-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4188:9-40: No property named "-gtk-outline-bottom-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4185:9-38: No property named "-gtk-outline-top-right-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4183:9-37: No property named "-gtk-outline-top-left-radius"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4169:3-29: No property named "-GtkWidget-window-dragging"
Mar 24 23:46:05 ArchDesktop gnome-system-mo[708305]: Theme parser error: gtk.css:4052:3-22: No property named "-gtk-outline-radius"
Mar 24 23:46:05 ArchDesktop systemd[1423]: Started Application launched by gsd-media-keys.
Mar 24 23:46:04 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-14bb5ff055db7dcdcc06326f2fa7fbb6d76de5cfea69cc5b21c77f71c6196aa1-runc.7b7AEz.mount: Deactivated successfully.
Mar 24 23:45:58 ArchDesktop systemd[1423]: app-gnome-nautilus-377396.scope: Consumed 11.167s CPU time.
Mar 24 23:45:26 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:45:26 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:44:37 ArchDesktop kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
Mar 24 23:44:37 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Mar 24 23:44:34 ArchDesktop systemd[1]: systemd-coredump@7-697800-0.service: Consumed 1min 1.180s CPU time.
Mar 24 23:44:34 ArchDesktop systemd[1]: systemd-coredump@7-697800-0.service: Deactivated successfully.
Mar 24 23:44:33 ArchDesktop systemd-coredump[697802]: Process 452664 (python) of user 1000 dumped core.
                                                      
                                                      Module libmkl_vml_def.so.2 without build-id.
                                                      Module libpi_level_zero.so without build-id.
                                                      Module libpi_opencl.so without build-id.
                                                      Module libsycl.so.7 without build-id.
                                                      Module libintlc.so.5 without build-id.
                                                      Module libimf.so without build-id.
                                                      Module libirng.so without build-id.
                                                      Module libsvml.so without build-id.
                                                      Module libOpenCL.so.1 without build-id.
                                                      Module libmkl_sycl_data_fitting.so.4 without build-id.
                                                      Module libmkl_sycl_stats.so.4 without build-id.
                                                      Module libmkl_sycl_rng.so.4 without build-id.
                                                      Module libmkl_sycl_vm.so.4 without build-id.
                                                      Module libmkl_sycl_dft.so.4 without build-id.
                                                      Module libmkl_sycl_sparse.so.4 without build-id.
                                                      Module libmkl_sycl_lapack.so.4 without build-id.
                                                      Module libmkl_sycl_blas.so.4 without build-id.
                                                      Module libxetla_kernels.so without build-id.
                                                      Module libintel-ext-pt-gpu.so without build-id.
                                                      Stack trace of thread 452949:
                                                      #0  0x00007c914a8ab32c n/a (libc.so.6 + 0x8d32c)
                                                      #1  0x00007c914a85a6c8 raise (libc.so.6 + 0x3c6c8)
                                                      #2  0x00007c914a8424b8 abort (libc.so.6 + 0x244b8)
                                                      #3  0x00007c8f7f216d52 n/a (libhsa-runtime64.so.1 + 0x16d52)
                                                      #4  0x00007c8f7f274642 n/a (libhsa-runtime64.so.1 + 0x74642)
                                                      #5  0x00007c8f7f21ca6c n/a (libhsa-runtime64.so.1 + 0x1ca6c)
                                                      #6  0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #7  0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 452664:
                                                      #0  0x00007c9008f3d05d urQueueFinish (libpi_level_zero.so + 0xab05d)
                                                      #1  0x00007c9008f49c6b piQueueFinish (libpi_level_zero.so + 0xb7c6b)
                                                      #2  0x00007c9053698952 _ZNK4sycl3_V16detail6plugin4callILNS1_9PiApiKindE23EJP9_pi_queueEEEvDpT0_ (libsycl.so.7 + 0x298952)
                                                      #3  0x00007c9053698025 _ZN4sycl3_V16detail10queue_impl4waitERKNS1_13code_locationE (libsycl.so.7 + 0x298025)
                                                      #4  0x00007c90841ae544 _ZN3xpu5dpcpp17deviceSynchronizeEa (libintel-ext-pt-gpu.so + 0x1fae544)
                                                      #5  0x00007c9128dc3b09 _ZZN8pybind1112cpp_function10initializeIZN3xpu15init_xpu_moduleERNS_7module_EEUlRKiE_vJS6_EJNS_4nameENS_5scopeENS_7siblingEEEEvOT_PFT0_DpT1_EDpRKT2_ENUlRNS_6detail13function_callEE1_4_FUNESO_ (libintel-ext-pt-python.so + 0x6db09)
                                                      #6  0x00007c9128d8d87d _ZN8pybind1112cpp_function10dispatcherEP7_objectS2_S2_ (libintel-ext-pt-python.so + 0x3787d)
                                                      #7  0x00007c914ab4a3c1 cfunction_call (libpython3.10.so.1.0 + 0x14a3c1)
                                                      #8  0x00007c914ab438d3 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x1438d3)
                                                      #9  0x00007c914ab3ee5e _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13ee5e)
                                                      #10 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #11 0x00007c914ab3e5ac _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13e5ac)
                                                      #12 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #13 0x00007c914ab3addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #14 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #15 0x00007c914ab3addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #16 0x00007c914ab55496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #17 0x00007c914ab3e5ac _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13e5ac)
                                                      #18 0x00007c914ab3890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #19 0x00007c914ab555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #20 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #21 0x00007c914ab3890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #22 0x00007c914ab555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #23 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #24 0x00007c914ab42b3b _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x142b3b)
                                                      #25 0x00007c914ab52b7d _PyObject_Call_Prepend (libpython3.10.so.1.0 + 0x152b7d)
                                                      #26 0x00007c914ac1a802 slot_tp_call (libpython3.10.so.1.0 + 0x21a802)
                                                      #27 0x00007c914ab438d3 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x1438d3)
                                                      #28 0x00007c914ab3ee5e _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13ee5e)
                                                      #29 0x00007c914ab3890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #30 0x00007c914ab555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #31 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #32 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #33 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #34 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #35 0x00007c9141efbe8b _Z17THPFunction_applyP7_objectS0_ (libtorch_python.so + 0x6fbe8b)
                                                      #36 0x00007c914ab4a3e8 cfunction_call (libpython3.10.so.1.0 + 0x14a3e8)
                                                      #37 0x00007c914ab55e9c _PyObject_Call (libpython3.10.so.1.0 + 0x155e9c)
                                                      #38 0x00007c914ab3f5bc do_call_core (libpython3.10.so.1.0 + 0x13f5bc)
                                                      #39 0x00007c914ab3890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #40 0x00007c914ab555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #41 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #42 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #43 0x00007c914ab55f10 PyVectorcall_Call (libpython3.10.so.1.0 + 0x155f10)
                                                      #44 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #45 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #46 0x00007c914ab55f10 PyVectorcall_Call (libpython3.10.so.1.0 + 0x155f10)
                                                      #47 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #48 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #49 0x00007c914ab55f10 PyVectorcall_Call (libpython3.10.so.1.0 + 0x155f10)
                                                      #50 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #51 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #52 0x00007c914ab3addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #53 0x00007c914ab55496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #54 0x00007c914ab55f10 PyVectorcall_Call (libpython3.10.so.1.0 + 0x155f10)
                                                      #55 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #56 0x00007c914ab55496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #57 0x00007c914ab55f10 PyVectorcall_Call (libpython3.10.so.1.0 + 0x155f10)
                                                      #58 0x00007c914ab3c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #59 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #60 0x00007c914ab42bf7 _PyObject_FastCallDictTstate (libpython3.10.so.1.0 + 0x142bf7)
                                                      #61 0x00007c914ab52b7d _PyObject_Call_Prepend (libpython3.10.so.1.0 + 0x152b7d)
                                                      #62 0x00007c914ac1a802 slot_tp_call (libpython3.10.so.1.0 + 0x21a802)
                                                      #63 0x00007c914ab438d3 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x1438d3)
                                                      
                                                      Stack trace of thread 452951:
                                                      #0  0x00007c914a8a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007c914a8a8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007c91336ae2a8 __gthread_cond_wait (libstdc++.so.6 + 0xae2a8)
                                                      #3  0x00007c8e76f1b22f n/a (libigdrcl.so + 0x71b22f)
                                                      #4  0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #5  0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 452867:
                                                      #0  0x00007c914a8a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007c914a8a8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007c900d7407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 453071:
                                                      #0  0x00007c914a8a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007c914a8b0836 n/a (libc.so.6 + 0x92836)
                                                      #2  0x00007c914ab1a653 PyThread_acquire_lock_timed (libpython3.10.so.1.0 + 0x11a653)
                                                      #3  0x00007c914abe959f acquire_timed (libpython3.10.so.1.0 + 0x1e959f)
                                                      #4  0x00007c914abe935f lock_PyThread_acquire_lock (libpython3.10.so.1.0 + 0x1e935f)
                                                      #5  0x00007c914aa6d325 method_vectorcall_VARARGS_KEYWORDS (libpython3.10.so.1.0 + 0x6d325)
                                                      #6  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #7  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #8  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #9  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #10 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #11 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #12 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #13 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #14 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #15 0x00007c914ab55692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #16 0x00007c914ac3e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #17 0x00007c914ac06a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #18 0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #19 0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 453144:
                                                      #0  0x00007c91483d27ae futex_wait (libgomp.so.1 + 0x237ae)
                                                      #1  0x00007c91483cfc70 gomp_simple_barrier_wait (libgomp.so.1 + 0x20c70)
                                                      #2  0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #3  0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 452782:
                                                      #0  0x00007c914a9190bf __poll (libc.so.6 + 0xfb0bf)
                                                      #1  0x00007c914ae7bb6c poll (select.cpython-310-x86_64-linux-gnu.so + 0x3b6c)
                                                      #2  0x00007c914ab5692c method_vectorcall_FASTCALL (libpython3.10.so.1.0 + 0x15692c)
                                                      #3  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #4  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #5  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #6  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #7  0x00007c914ab3e5ac _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13e5ac)
                                                      #8  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #9  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #10 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #11 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #12 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #13 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #14 0x00007c914ab55692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #15 0x00007c914ac3e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #16 0x00007c914ac06a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #17 0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #18 0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 453920:
                                                      #0  0x00007c914a8a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007c914a8b0836 n/a (libc.so.6 + 0x92836)
                                                      #2  0x00007c914ab1a653 PyThread_acquire_lock_timed (libpython3.10.so.1.0 + 0x11a653)
                                                      #3  0x00007c914abe959f acquire_timed (libpython3.10.so.1.0 + 0x1e959f)
                                                      #4  0x00007c914abe935f lock_PyThread_acquire_lock (libpython3.10.so.1.0 + 0x1e935f)
                                                      #5  0x00007c914aa6d325 method_vectorcall_VARARGS_KEYWORDS (libpython3.10.so.1.0 + 0x6d325)
                                                      #6  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #7  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #8  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #9  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #10 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #11 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #12 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #13 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #14 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #15 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #16 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #17 0x00007c914ab55692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #18 0x00007c914ac3e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #19 0x00007c914ac06a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #20 0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #21 0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 452815:
                                                      #0  0x00007c914a9190bf __poll (libc.so.6 + 0xfb0bf)
                                                      #1  0x00007c914ae7bb6c poll (select.cpython-310-x86_64-linux-gnu.so + 0x3b6c)
                                                      #2  0x00007c914ab5692c method_vectorcall_FASTCALL (libpython3.10.so.1.0 + 0x15692c)
                                                      #3  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #4  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #5  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #6  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #7  0x00007c914ab3e5ac _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13e5ac)
                                                      #8  0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #9  0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #10 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #11 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #12 0x00007c914ab4a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #13 0x00007c914ab3a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #14 0x00007c914ab55692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #15 0x00007c914ac3e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #16 0x00007c914ac06a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #17 0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #18 0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 454141:
                                                      #0  0x00007c914a8a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007c914a8a8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007c91336ae2a8 __gthread_cond_wait (libstdc++.so.6 + 0xae2a8)
                                                      #3  0x00007c9137d52413 _ZN5torch8autograd10ReadyQueue3popEv (libtorch_cpu.so + 0x4352413)
                                                      #4  0x00007c9137d5600d _ZN5torch8autograd6Engine11thread_mainERKSt10shared_ptrINS0_9GraphTaskEE (libtorch_cpu.so + 0x435600d)
                                                      #5  0x00007c9137d4d979 _ZN5torch8autograd6Engine11thread_initEiRKSt10shared_ptrINS0_10ReadyQueueEEb (libtorch_cpu.so + 0x434d979)
                                                      #6  0x00007c9141ef1621 _ZN5torch8autograd6python12PythonEngine11thread_initEiRKSt10shared_ptrINS0_10ReadyQueueEEb (libtorch_python.so + 0x6f1621)
                                                      #7  0x00007c91336e1943 execute_native_thread_routine (libstdc++.so.6 + 0xe1943)
                                                      #8  0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 452960:
                                                      #0  0x00007c914a9224ff ioctl (libc.so.6 + 0x1044ff)
                                                      #1  0x00007c8e750b16cd n/a (libze_intel_gpu.so.1 + 0x6b16cd)
                                                      #2  0x00007c8e750ac4cc n/a (libze_intel_gpu.so.1 + 0x6ac4cc)
                                                      #3  0x00007c8e75097b03 n/a (libze_intel_gpu.so.1 + 0x697b03)
                                                      #4  0x00007c8e7509a138 n/a (libze_intel_gpu.so.1 + 0x69a138)
                                                      #5  0x00007c914a8a955a n/a (libc.so.6 + 0x8b55a)
                                                      #6  0x00007c914a926a3c n/a (libc.so.6 + 0x108a3c)
                                                      ELF object binary architecture: AMD x86-64
Mar 24 23:44:33 ArchDesktop systemd-coredump[697802]: Removed old coredump core.pt_main_thread.1000.5d311d5205994f3cb6ed8404eb3ea076.473734.1711312982000000.zst.
Mar 24 23:44:33 ArchDesktop systemd-coredump[697802]: Removed old coredump core.tensorboard.1000.5d311d5205994f3cb6ed8404eb3ea076.466340.1711312982000000.zst.
Mar 24 23:44:33 ArchDesktop systemd-coredump[697802]: Removed old coredump core.tensorboard.1000.5d311d5205994f3cb6ed8404eb3ea076.473234.1711312982000000.zst.
Mar 24 23:44:33 ArchDesktop systemd-coredump[697802]: Removed old coredump core.pt_main_thread.1000.5d311d5205994f3cb6ed8404eb3ea076.472902.1711312982000000.zst.
Mar 24 23:44:33 ArchDesktop systemd-coredump[697802]: Removed old coredump core.python.1000.5d311d5205994f3cb6ed8404eb3ea076.17831.1711307047000000.zst.
Mar 24 23:44:04 ArchDesktop kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
Mar 24 23:44:04 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Mar 24 23:44:04 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset(5) succeeded!
Mar 24 23:44:04 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow done
Mar 24 23:44:04 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow start
Mar 24 23:44:04 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset begin!
Mar 24 23:44:04 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: Failed to remove queue 0
Mar 24 23:44:04 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Mar 24 23:44:04 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1000
Mar 24 23:44:04 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Mar 24 23:43:58 ArchDesktop systemd[1]: systemd-coredump@6-697795-0.service: Consumed 40.219s CPU time.
Mar 24 23:43:58 ArchDesktop systemd[1]: systemd-coredump@6-697795-0.service: Deactivated successfully.
Mar 24 23:43:58 ArchDesktop systemd-coredump[697801]: Process 473734 (pt_main_thread) of user 1000 dumped core.
                                                      
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module /tmp/miopen-interim-hsaco-d747-df67-356d-dcd9/file (deleted) without build-id.
                                                      Module [dso] without build-id.
                                                      Module /tmp/miopen-interim-hsaco-c843-3a3b-ec7b-f716/file (deleted) without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module /tmp/miopen-interim-hsaco-6fd1-ebf1-c36c-a0e1/file (deleted) without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module /tmp/miopen-interim-hsaco-e7ed-7ce7-8263-b6db/file (deleted) without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module [dso] without build-id.
                                                      Module /tmp/miopen-interim-hsaco-0f0a-3c98-3b27-e358/file (deleted) without build-id.
                                                      Module [dso] without build-id.
                                                      Module libz.b38cb0f0.so.1 without build-id.
                                                      Module librocsparse.so without build-id.
                                                      Module librocrand.so without build-id.
                                                      Module librocfft.so without build-id.
                                                      Module librocsolver.so without build-id.
                                                      Module librocblas.so without build-id.
                                                      Module libmagma.so without build-id.
                                                      Module librccl.so without build-id.
                                                      Module libhiprand.so without build-id.
                                                      Module libhipfft.so without build-id.
                                                      Module libhipblaslt.so without build-id.
                                                      Module libMIOpen.so without build-id.
                                                      Stack trace of thread 473905:
                                                      #0  0x00007dee874ab32c n/a (libc.so.6 + 0x8d32c)
                                                      #1  0x00007dee8745a6c8 raise (libc.so.6 + 0x3c6c8)
                                                      #2  0x00007dee874424b8 abort (libc.so.6 + 0x244b8)
                                                      #3  0x00007dedaa46c259 _ZN4rocr4core7Runtime18HwExceptionHandlerElPv (libhsa-runtime64.so + 0x6c259)
                                                      #4  0x00007dedaa4685d9 _ZN4rocr4core7Runtime15AsyncEventsLoopEPv (libhsa-runtime64.so + 0x685d9)
                                                      #5  0x00007dedaa419f57 _ZN4rocr2os16ThreadTrampolineEPv (libhsa-runtime64.so + 0x19f57)
                                                      #6  0x00007dee874a955a n/a (libc.so.6 + 0x8b55a)
                                                      #7  0x00007dee87526a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473734:
                                                      #0  0x00007dee874f2335 clock_nanosleep (libc.so.6 + 0xd4335)
                                                      #1  0x00007dee874fd3e7 __nanosleep (libc.so.6 + 0xdf3e7)
                                                      #2  0x00007dee87526569 usleep (libc.so.6 + 0x108569)
                                                      #3  0x00007dedaa44329a _ZN4rocr4core14BusyWaitSignal11WaitRelaxedE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x4329a)
                                                      #4  0x00007dedaa442eda _ZN4rocr4core14BusyWaitSignal11WaitAcquireE22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x42eda)
                                                      #5  0x00007dedaa4465b9 _ZN4rocr3HSA25hsa_signal_wait_scacquireE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libhsa-runtime64.so + 0x465b9)
                                                      #6  0x00007dedec40acd5 _ZN9roctracer11hsa_support6detailL34hsa_signal_wait_scacquire_callbackE12hsa_signal_s22hsa_signal_condition_tlm16hsa_wait_state_t (libroctracer64.so + 0xacd5)
                                                      #7  0x00007dee25698103 _ZN3roc10VirtualGPU12allocKernArgEmm (libamdhip64.so + 0x298103)
                                                      #8  0x00007dee2569b7fc _ZN3roc10VirtualGPU20submitKernelInternalERKN3amd16NDRangeContainerERKNS1_6KernelEPKhPvjPNS1_20NDRangeKernelCommandEP28hsa_kernel_dispatch_packet_s (libamdhip64.so + 0x29b7fc)
                                                      #9  0x00007dee2569be25 _ZN3roc10VirtualGPU12submitKernelERN3amd20NDRangeKernelCommandE (libamdhip64.so + 0x29be25)
                                                      #10 0x00007dee2566a66a _ZN3amd7Command7enqueueEv (libamdhip64.so + 0x26a66a)
                                                      #11 0x00007dee2559b3e4 _Z22ihipModuleLaunchKernelP18ihipModuleSymbol_tjjjjjjjP12ihipStream_tPPvS4_P11ihipEvent_tS6_jjjjmmj (libamdhip64.so + 0x19b3e4)
                                                      #12 0x00007dee255aab59 _Z24hipExtModuleLaunchKernelP18ihipModuleSymbol_tjjjjjjmP12ihipStream_tPPvS4_P11ihipEvent_tS6_j (libamdhip64.so + 0x1aab59)
                                                      #13 0x00007deda9ca9101 _ZN7Tensile3hip15SolutionAdapter12launchKernelERKNS_16KernelInvocationEP12ihipStream_tP11ihipEvent_tS8_ (librocblas.so + 0x320a9101)
                                                      #14 0x00007deda9ca93bc _ZN7Tensile3hip15SolutionAdapter13launchKernelsERKSt6vectorINS_16KernelInvocationESaIS3_EEP12ihipStream_tP11ihipEvent_tSB_ (librocblas.so + 0x320a93bc)
                                                      #15 0x00007deda907e5a8 _Z21runContractionProblemIDF16_DF16_fDF16_DF16_DF16_E15rocblas_status_RK25RocblasContractionProblemIT_T0_T1_T2_T3_T4_E18rocblas_gemm_algo_i (librocblas.so + 0x3147e5a8)
                                                      #16 0x00007deda9176d48 _Z24gemm_ex_batched_templateIDF16_DF16_fE15rocblas_status_P15_rocblas_handle18rocblas_operation_S3_iiiPKT1_PKT_lilS9_lilS6_PKT0_lilPSA_lili18rocblas_gemm_algo_i19rocblas_gemm_flags_ (librocblas.so + 0x31576d48)
                                                      #17 0x00007deda91748f9 _Z19gemm_ex_typecastingILb0EDF16_DF16_fE15rocblas_status_P15_rocblas_handle18rocblas_operation_S3_iiiPKvS5_lilS5_lilS5_S5_lilPvlili18rocblas_gemm_algo_i19rocblas_gemm_flags_ (librocblas.so + 0x315748f9)
                                                      #18 0x00007deda916f2de _Z24rocblas_gemm_ex_templateILb0EE15rocblas_status_P15_rocblas_handle18rocblas_operation_S3_iiiPKvS5_17rocblas_datatype_lilS5_S6_lilS5_S5_S6_lilPvS6_liliS6_18rocblas_gemm_algo_ij (librocblas.so + 0x3156f2de)
                                                      #19 0x00007deda916bc45 rocblas_gemm_ex (librocblas.so + 0x3156bc45)
                                                      #20 0x00007dee28a4bbc5 _ZN2at4cuda4blas13gemm_internalIN3c104HalfEEEvcclllNS_10OpMathTypeIT_E4typeEPKS6_lSA_lS8_PS6_l (libtorch_hip.so + 0x1a4bbc5)
                                                      #21 0x00007dee28a4f8b7 _ZN2at4cuda4blas4gemmIN3c104HalfEEEvcclllNS_10OpMathTypeIT_E4typeEPKS6_lSA_lS8_PS6_l (libtorch_hip.so + 0x1a4f8b7)
                                                      #22 0x00007dee28b66a74 _ZN2at6native12_GLOBAL__N_119addmm_out_cuda_implERNS_6TensorERKS2_S5_S5_RKN3c106ScalarES9_NS1_10ActivationE (libtorch_hip.so + 0x1b66a74)
                                                      #23 0x00007dee28ca7c5c _ZN2at12_GLOBAL__N_118wrapper_CUDA_addmmERKNS_6TensorES3_S3_RKN3c106ScalarES7_ (libtorch_hip.so + 0x1ca7c5c)
                                                      #24 0x00007dee28ca7d2d _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_S8_RKNS_6ScalarESB_EXadL_ZNS5_12_GLOBAL__N_118wrapper_CUDA_addmmES8_S8_S8_SB_SB_EEEES6_NS_4guts8typelist8typelistIJS8_S8_S8_SB_SB_EEEEESC_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES8_S8_S8_SB_SB_ (libtorch_hip.so + 0x1ca7d2d)
                                                      #25 0x00007dee6e2f4576 _ZN2at4_ops5addmm10redispatchEN3c1014DispatchKeySetERKNS_6TensorES6_S6_RKNS2_6ScalarES9_ (libtorch_cpu.so + 0x24f4576)
                                                      #26 0x00007dee703035f1 _ZN5torch8autograd12VariableType12_GLOBAL__N_15addmmEN3c1014DispatchKeySetERKN2at6TensorES8_S8_RKNS3_6ScalarESB_ (libtorch_cpu.so + 0x45035f1)
                                                      #27 0x00007dee703045f3 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorENS_14DispatchKeySetERKS6_S9_S9_RKNS_6ScalarESC_EXadL_ZN5torch8autograd12VariableType12_GLOBAL__N_15addmmES7_S9_S9_S9_SC_SC_EEEES6_NS_4guts8typelist8typelistIJS7_S9_S9_S9_SC_SC_EEEEESD_E4callEPNS_14OperatorKernelES7_S9_S9_S9_SC_SC_ (libtorch_cpu.so + 0x45045f3)
                                                      #28 0x00007dee6e36921e _ZN2at4_ops5addmm4callERKNS_6TensorES4_S4_RKN3c106ScalarES8_ (libtorch_cpu.so + 0x256921e)
                                                      #29 0x00007dee6db71d83 _ZN2at6nativeL18_flatten_nd_linearERKNS_6TensorES3_S3_ (libtorch_cpu.so + 0x1d71d83)
                                                      #30 0x00007dee6db72c13 _ZN2at6native6linearERKNS_6TensorES3_RKSt8optionalIS1_E (libtorch_cpu.so + 0x1d72c13)
                                                      #31 0x00007dee6edda733 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail24WrapFunctionIntoFunctor_INS_26CompileTimeFunctionPointerIFN2at6TensorERKS6_S8_RKSt8optionalIS6_EEXadL_ZNS5_12_GLOBAL__N_112_GLOBAL__N_141wrapper_CompositeImplicitAutograd__linearES8_S8_SC_EEEES6_NS_4guts8typelist8typelistIJS8_S8_SC_EEEEESD_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES8_S8_SC_ (libtorch_cpu.so + 0x2fda733)
                                                      #32 0x00007dee6e3510fc _ZN2at4_ops6linear4callERKNS_6TensorES4_RKSt8optionalIS2_E (libtorch_cpu.so + 0x25510fc)
                                                      #33 0x00007dee6d769e1a _ZN2at8autocast13WrapFunction_ILNS0_10CastPolicyE0ELN3c1010DeviceTypeE1EFNS_6TensorERKS5_S7_RKSt8optionalIS5_EEXadL_ZNS_4_ops6linear4callES7_S7_SB_EES5_NS3_4guts8typelist8typelistIJS7_S7_SB_EEEE4callES7_S7_SB_ (libtorch_cpu.so + 0x1969e1a)
                                                      #34 0x00007dee6d7502e5 _ZN3c104impl28wrap_kernel_functor_unboxed_INS0_6detail31WrapFunctionIntoRuntimeFunctor_IPFN2at6TensorERKS5_S7_RKSt8optionalIS5_EES5_NS_4guts8typelist8typelistIJS7_S7_SB_EEEEESC_E4callEPNS_14OperatorKernelENS_14DispatchKeySetES7_S7_SB_ (libtorch_cpu.so + 0x19502e5)
                                                      #35 0x00007dee6e3510fc _ZN2at4_ops6linear4callERKNS_6TensorES4_RKSt8optionalIS2_E (libtorch_cpu.so + 0x25510fc)
                                                      #36 0x00007dee84b087e5 _ZN5torch8autogradL18THPVariable_linearEP7_objectS2_S2_ (libtorch_python.so + 0x7087e5)
                                                      #37 0x00007dee8774a3c1 cfunction_call (libpython3.10.so.1.0 + 0x14a3c1)
                                                      #38 0x00007dee877438d3 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x1438d3)
                                                      #39 0x00007dee8773ee5e _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13ee5e)
                                                      #40 0x00007dee8773890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #41 0x00007dee877555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #42 0x00007dee8773c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #43 0x00007dee8773890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #44 0x00007dee877555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #45 0x00007dee8773c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #46 0x00007dee87742b3b _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x142b3b)
                                                      #47 0x00007dee87752b7d _PyObject_Call_Prepend (libpython3.10.so.1.0 + 0x152b7d)
                                                      #48 0x00007dee8781a802 slot_tp_call (libpython3.10.so.1.0 + 0x21a802)
                                                      #49 0x00007dee877438d3 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x1438d3)
                                                      #50 0x00007dee8773e87f _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13e87f)
                                                      #51 0x00007dee8773890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #52 0x00007dee877555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #53 0x00007dee8773c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #54 0x00007dee8773890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #55 0x00007dee877555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      #56 0x00007dee8773c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #57 0x00007dee87742b3b _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x142b3b)
                                                      #58 0x00007dee87752b7d _PyObject_Call_Prepend (libpython3.10.so.1.0 + 0x152b7d)
                                                      #59 0x00007dee8781a802 slot_tp_call (libpython3.10.so.1.0 + 0x21a802)
                                                      #60 0x00007dee877438d3 _PyObject_MakeTpCall (libpython3.10.so.1.0 + 0x1438d3)
                                                      #61 0x00007dee8773ee5e _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13ee5e)
                                                      #62 0x00007dee8773890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #63 0x00007dee877555bd _PyFunction_Vectorcall (libpython3.10.so.1.0 + 0x1555bd)
                                                      
                                                      Stack trace of thread 474617:
                                                      #0  0x00007dee874a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007dee874b0836 n/a (libc.so.6 + 0x92836)
                                                      #2  0x00007dee8771a653 PyThread_acquire_lock_timed (libpython3.10.so.1.0 + 0x11a653)
                                                      #3  0x00007dee877e959f acquire_timed (libpython3.10.so.1.0 + 0x1e959f)
                                                      #4  0x00007dee877e935f lock_PyThread_acquire_lock (libpython3.10.so.1.0 + 0x1e935f)
                                                      #5  0x00007dee8766d325 method_vectorcall_VARARGS_KEYWORDS (libpython3.10.so.1.0 + 0x6d325)
                                                      #6  0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #7  0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #8  0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #9  0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #10 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #11 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #12 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #13 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #14 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #15 0x00007dee87755692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #16 0x00007dee8783e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #17 0x00007dee87806a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #18 0x00007dee874a955a n/a (libc.so.6 + 0x8b55a)
                                                      #19 0x00007dee87526a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 477093:
                                                      #0  0x00007dee874a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007dee874b0836 n/a (libc.so.6 + 0x92836)
                                                      #2  0x00007dee8771a653 PyThread_acquire_lock_timed (libpython3.10.so.1.0 + 0x11a653)
                                                      #3  0x00007dee877e959f acquire_timed (libpython3.10.so.1.0 + 0x1e959f)
                                                      #4  0x00007dee877e935f lock_PyThread_acquire_lock (libpython3.10.so.1.0 + 0x1e935f)
                                                      #5  0x00007dee8766d325 method_vectorcall_VARARGS_KEYWORDS (libpython3.10.so.1.0 + 0x6d325)
                                                      #6  0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #7  0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #8  0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #9  0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #10 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #11 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #12 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #13 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #14 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #15 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #16 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #17 0x00007dee87755692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #18 0x00007dee8783e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #19 0x00007dee87806a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #20 0x00007dee874a955a n/a (libc.so.6 + 0x8b55a)
                                                      #21 0x00007dee87526a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 477135:
                                                      #0  0x00007dee874a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007dee874b1470 n/a (libc.so.6 + 0x93470)
                                                      #2  0x00007dee8771a58c PyThread_acquire_lock_timed (libpython3.10.so.1.0 + 0x11a58c)
                                                      #3  0x00007dee877e959f acquire_timed (libpython3.10.so.1.0 + 0x1e959f)
                                                      #4  0x00007dee877e935f lock_PyThread_acquire_lock (libpython3.10.so.1.0 + 0x1e935f)
                                                      #5  0x00007dee8766d325 method_vectorcall_VARARGS_KEYWORDS (libpython3.10.so.1.0 + 0x6d325)
                                                      #6  0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #7  0x00007dee87755496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #8  0x00007dee87739d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #9  0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #10 0x00007dee8773c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #11 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #12 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #13 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #14 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #15 0x00007dee87755692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #16 0x00007dee8783e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #17 0x00007dee87806a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #18 0x00007dee874a955a n/a (libc.so.6 + 0x8b55a)
                                                      #19 0x00007dee87526a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 477136:
                                                      #0  0x00007dee874a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007dee874b1470 n/a (libc.so.6 + 0x93470)
                                                      #2  0x00007dee8771a58c PyThread_acquire_lock_timed (libpython3.10.so.1.0 + 0x11a58c)
                                                      #3  0x00007dee877e959f acquire_timed (libpython3.10.so.1.0 + 0x1e959f)
                                                      #4  0x00007dee877e935f lock_PyThread_acquire_lock (libpython3.10.so.1.0 + 0x1e935f)
                                                      #5  0x00007dee8766d325 method_vectorcall_VARARGS_KEYWORDS (libpython3.10.so.1.0 + 0x6d325)
                                                      #6  0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #7  0x00007dee87755496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #8  0x00007dee87739d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #9  0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #10 0x00007dee8773c4df do_call_core (libpython3.10.so.1.0 + 0x13c4df)
                                                      #11 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #12 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #13 0x00007dee8774a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #14 0x00007dee8773a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #15 0x00007dee87755692 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155692)
                                                      #16 0x00007dee8783e877 thread_run (libpython3.10.so.1.0 + 0x23e877)
                                                      #17 0x00007dee87806a58 pythread_wrapper (libpython3.10.so.1.0 + 0x206a58)
                                                      #18 0x00007dee874a955a n/a (libc.so.6 + 0x8b55a)
                                                      #19 0x00007dee87526a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 477504:
                                                      #0  0x00007dee874a5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007dee874a8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007dedecaae2a8 __gthread_cond_wait (libstdc++.so.6 + 0xae2a8)
                                                      #3  0x00007dee70f436d3 _ZN5torch8autograd10ReadyQueue3popEv (libtorch_cpu.so + 0x51436d3)
                                                      #4  0x00007dee70f48165 _ZN5torch8autograd6Engine11thread_mainERKSt10shared_ptrINS0_9GraphTaskEE (libtorch_cpu.so + 0x5148165)
                                                      #5  0x00007dee70f3f6ff _ZN5torch8autograd6Engine11thread_initEiRKSt10shared_ptrINS0_10ReadyQueueEEb (libtorch_cpu.so + 0x513f6ff)
                                                      #6  0x00007dee84c3418c _ZN5torch8autograd6python12PythonEngine11thread_initEiRKSt10shared_ptrINS0_10ReadyQueueEEb (libtorch_python.so + 0x83418c)
                                                      #7  0x00007dee861aa220 execute_native_thread_routine (libtorch.so + 0x1c220)
                                                      #8  0x00007dee874a955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x00007dee87526a3c n/a (libc.so.6 + 0x108a3c)
                                                      ELF object binary architecture: AMD x86-64
Mar 24 23:43:28 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-5a1186cf6856d30309d76d966166ed3cc7784062ee5ef6ab1bc95cb08f9f63b2-runc.NbVFGN.mount: Deactivated successfully.
Mar 24 23:43:15 ArchDesktop kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
Mar 24 23:43:15 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Mar 24 23:43:14 ArchDesktop systemd[1]: systemd-coredump@9-697805-0.service: Consumed 6.297s CPU time.
Mar 24 23:43:14 ArchDesktop systemd[1]: systemd-coredump@9-697805-0.service: Deactivated successfully.
Mar 24 23:43:14 ArchDesktop systemd-coredump[697807]: Process 466340 (tensorboard) of user 1000 dumped core.
                                                      
                                                      Module libpi_level_zero.so without build-id.
                                                      Module libpi_opencl.so without build-id.
                                                      Module libintlc.so.5 without build-id.
                                                      Module libirng.so without build-id.
                                                      Module libsvml.so without build-id.
                                                      Module libmkl_sycl_data_fitting.so.4 without build-id.
                                                      Module libmkl_sycl_stats.so.4 without build-id.
                                                      Module libmkl_sycl_rng.so.4 without build-id.
                                                      Module libmkl_sycl_vm.so.4 without build-id.
                                                      Module libmkl_sycl_dft.so.4 without build-id.
                                                      Module libmkl_sycl_sparse.so.4 without build-id.
                                                      Module libmkl_sycl_lapack.so.4 without build-id.
                                                      Module libmkl_sycl_blas.so.4 without build-id.
                                                      Module libOpenCL.so.1 without build-id.
                                                      Module libsycl.so.7 without build-id.
                                                      Module libimf.so without build-id.
                                                      Stack trace of thread 466444:
                                                      #0  0x0000765efceab32c n/a (libc.so.6 + 0x8d32c)
                                                      #1  0x0000765efce5a6c8 raise (libc.so.6 + 0x3c6c8)
                                                      #2  0x0000765efce5a770 n/a (libc.so.6 + 0x3c770)
                                                      #3  0x0000765efceab32c n/a (libc.so.6 + 0x8d32c)
                                                      #4  0x0000765efce5a6c8 raise (libc.so.6 + 0x3c6c8)
                                                      #5  0x0000765efce424b8 abort (libc.so.6 + 0x244b8)
                                                      #6  0x0000765db5216d52 n/a (libhsa-runtime64.so.1 + 0x16d52)
                                                      #7  0x0000765db5274642 n/a (libhsa-runtime64.so.1 + 0x74642)
                                                      #8  0x0000765db521ca6c n/a (libhsa-runtime64.so.1 + 0x1ca6c)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466357:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466340:
                                                      #0  0x0000765efcf190bf __poll (libc.so.6 + 0xfb0bf)
                                                      #1  0x0000765efd3fdb6c poll (select.cpython-310-x86_64-linux-gnu.so + 0x3b6c)
                                                      #2  0x0000765efd15692c method_vectorcall_FASTCALL (libpython3.10.so.1.0 + 0x15692c)
                                                      #3  0x0000765efd13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #4  0x0000765efd14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #5  0x0000765efd13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #6  0x0000765efd155496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #7  0x0000765efd13addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #8  0x0000765efd14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #9  0x0000765efd13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #10 0x0000765efd155496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #11 0x0000765efd139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #12 0x0000765efd155496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #13 0x0000765efd139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #14 0x0000765efd14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #15 0x0000765efd139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #16 0x0000765efd14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #17 0x0000765efd13addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #18 0x0000765efd14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #19 0x0000765efd139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #20 0x0000765efd13890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #21 0x0000765efd1e3954 PyEval_EvalCode (libpython3.10.so.1.0 + 0x1e3954)
                                                      #22 0x0000765efd1f3393 run_eval_code_obj (libpython3.10.so.1.0 + 0x1f3393)
                                                      #23 0x0000765efd1eed4a run_mod (libpython3.10.so.1.0 + 0x1eed4a)
                                                      #24 0x0000765efd09c08d pyrun_file (libpython3.10.so.1.0 + 0x9c08d)
                                                      #25 0x0000765efd09bd2c _PyRun_SimpleFileObject (libpython3.10.so.1.0 + 0x9bd2c)
                                                      #26 0x0000765efd09c911 _PyRun_AnyFileObject (libpython3.10.so.1.0 + 0x9c911)
                                                      #27 0x0000765efd1ffac7 pymain_run_file_obj (libpython3.10.so.1.0 + 0x1ffac7)
                                                      #28 0x0000765efd1d528b Py_BytesMain (libpython3.10.so.1.0 + 0x1d528b)
                                                      #29 0x0000765efce43cd0 n/a (libc.so.6 + 0x25cd0)
                                                      #30 0x0000765efce43d8a __libc_start_main (libc.so.6 + 0x25d8a)
                                                      #31 0x00005ef23f626045 _start (python3.10 + 0x1045)
                                                      
                                                      Stack trace of thread 466359:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466361:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466362:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466363:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466366:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466413:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466418:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466360:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466415:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466364:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466370:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466417:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466416:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466371:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466537:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa12210e n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32210e)
                                                      #6  0x0000765efa129c42 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x329c42)
                                                      #7  0x0000765efa127b20 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327b20)
                                                      #8  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #9  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #10 0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #11 0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #12 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466425:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466931:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e417 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e417)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa1318dd n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3318dd)
                                                      #6  0x0000765efa16c175 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x36c175)
                                                      #7  0x0000765efa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466414:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466421:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466540:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa1291d6 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3291d6)
                                                      #6  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #7  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #8  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466419:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466420:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466529:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466427:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466527:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466524:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466368:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466528:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466447:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef9aae2a8 __gthread_cond_wait (libstdc++.so.6 + 0xae2a8)
                                                      #3  0x0000765cadf1b22f n/a (libigdrcl.so + 0x71b22f)
                                                      #4  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #5  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466539:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466369:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466535:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466448:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef9aae2a8 __gthread_cond_wait (libstdc++.so.6 + 0xae2a8)
                                                      #3  0x0000765c9849a0bf n/a (libze_intel_gpu.so.1 + 0x69a0bf)
                                                      #4  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #5  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466536:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466358:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466423:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466522:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e417 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e417)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa1318dd n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3318dd)
                                                      #6  0x0000765efa15483d n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x35483d)
                                                      #7  0x0000765efa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466530:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466523:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa131868 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x331868)
                                                      #6  0x0000765efa16c175 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x36c175)
                                                      #7  0x0000765efa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466422:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466426:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466424:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765e949407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466531:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466534:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466538:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466532:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466525:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466521:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e417 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e417)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa1318dd n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3318dd)
                                                      #6  0x0000765efa15483d n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x35483d)
                                                      #7  0x0000765efa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466367:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466526:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466533:
                                                      #0  0x0000765efcf2488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x0000765efa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x0000765efa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x0000765efa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x0000765ef9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x0000765efa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x0000765efa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x0000765efa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x0000765efa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 466365:
                                                      #0  0x0000765efcea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x0000765efcea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x0000765ef753743b blas_thread_server (libopenblas64_p-r0-15028c96.3.21.so + 0x33743b)
                                                      #3  0x0000765efcea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x0000765efcf26a3c n/a (libc.so.6 + 0x108a3c)
                                                      ELF object binary architecture: AMD x86-64
Mar 24 23:43:10 ArchDesktop kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
Mar 24 23:43:10 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Mar 24 23:43:10 ArchDesktop systemd[1]: systemd-coredump@8-697804-0.service: Consumed 5.236s CPU time.
Mar 24 23:43:10 ArchDesktop systemd[1]: systemd-coredump@8-697804-0.service: Deactivated successfully.
Mar 24 23:43:10 ArchDesktop systemd-coredump[697806]: Process 473234 (tensorboard) of user 1000 dumped core.
                                                      
                                                      Module librocrand.so without build-id.
                                                      Module librocfft.so.0 without build-id.
                                                      Module libhipfft.so without build-id.
                                                      Module libMIOpen.so without build-id.
                                                      Module librocblas.so without build-id.
                                                      Module librccl.so.1 without build-id.
                                                      Stack trace of thread 473533:
                                                      #0  0x00007e92ad44b32c n/a (libc.so.6 + 0x8d32c)
                                                      #1  0x00007e92ad3fa6c8 raise (libc.so.6 + 0x3c6c8)
                                                      #2  0x00007e92ad3fa770 n/a (libc.so.6 + 0x3c770)
                                                      #3  0x00007e92ad44b32c n/a (libc.so.6 + 0x8d32c)
                                                      #4  0x00007e92ad3fa6c8 raise (libc.so.6 + 0x3c6c8)
                                                      #5  0x00007e92ad3e24b8 abort (libc.so.6 + 0x244b8)
                                                      #6  0x00007e927ac16d52 n/a (libhsa-runtime64.so.1 + 0x16d52)
                                                      #7  0x00007e927ac74642 n/a (libhsa-runtime64.so.1 + 0x74642)
                                                      #8  0x00007e927ac1ca6c n/a (libhsa-runtime64.so.1 + 0x1ca6c)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473234:
                                                      #0  0x00007e92ad4b90bf __poll (libc.so.6 + 0xfb0bf)
                                                      #1  0x00007e92acec5b6c poll (select.cpython-310-x86_64-linux-gnu.so + 0x3b6c)
                                                      #2  0x00007e92ad15692c method_vectorcall_FASTCALL (libpython3.10.so.1.0 + 0x15692c)
                                                      #3  0x00007e92ad13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #4  0x00007e92ad14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #5  0x00007e92ad13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #6  0x00007e92ad155496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #7  0x00007e92ad13addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #8  0x00007e92ad14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #9  0x00007e92ad13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #10 0x00007e92ad155496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #11 0x00007e92ad139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #12 0x00007e92ad155496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #13 0x00007e92ad139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #14 0x00007e92ad14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #15 0x00007e92ad139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #16 0x00007e92ad14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #17 0x00007e92ad13addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #18 0x00007e92ad14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #19 0x00007e92ad139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #20 0x00007e92ad13890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #21 0x00007e92ad1e3954 PyEval_EvalCode (libpython3.10.so.1.0 + 0x1e3954)
                                                      #22 0x00007e92ad1f3393 run_eval_code_obj (libpython3.10.so.1.0 + 0x1f3393)
                                                      #23 0x00007e92ad1eed4a run_mod (libpython3.10.so.1.0 + 0x1eed4a)
                                                      #24 0x00007e92ad09c08d pyrun_file (libpython3.10.so.1.0 + 0x9c08d)
                                                      #25 0x00007e92ad09bd2c _PyRun_SimpleFileObject (libpython3.10.so.1.0 + 0x9bd2c)
                                                      #26 0x00007e92ad09c911 _PyRun_AnyFileObject (libpython3.10.so.1.0 + 0x9c911)
                                                      #27 0x00007e92ad1ffac7 pymain_run_file_obj (libpython3.10.so.1.0 + 0x1ffac7)
                                                      #28 0x00007e92ad1d528b Py_BytesMain (libpython3.10.so.1.0 + 0x1d528b)
                                                      #29 0x00007e92ad3e3cd0 n/a (libc.so.6 + 0x25cd0)
                                                      #30 0x00007e92ad3e3d8a __libc_start_main (libc.so.6 + 0x25d8a)
                                                      #31 0x00005f167621f045 _start (python3.10 + 0x1045)
                                                      
                                                      Stack trace of thread 473252:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473251:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473260:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473257:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473486:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473262:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473487:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473495:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473493:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473494:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473256:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473254:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473488:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473258:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473489:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473255:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473261:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473259:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473499:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473497:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473263:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473498:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473616:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e417 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e417)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa1318dd n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3318dd)
                                                      #6  0x00007e92aa16c175 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x36c175)
                                                      #7  0x00007e92aa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473631:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473623:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473264:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473615:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e417 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e417)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa1318dd n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3318dd)
                                                      #6  0x00007e92aa15483d n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x35483d)
                                                      #7  0x00007e92aa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473617:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473624:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473492:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473496:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473619:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473632:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473490:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473626:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473622:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473618:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473265:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473620:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473629:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473621:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473630:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473966:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa131868 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x331868)
                                                      #6  0x00007e92aa16c175 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x36c175)
                                                      #7  0x00007e92aa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473628:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473491:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473633:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa1291d6 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3291d6)
                                                      #6  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #7  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #8  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473500:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e91f41407db blas_thread_server (libopenblasp-r0-23e5df77.3.21.dev.so + 0x3407db)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473614:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e417 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e417)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa1318dd n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3318dd)
                                                      #6  0x00007e92aa15483d n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x35483d)
                                                      #7  0x00007e92aa133e69 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333e69)
                                                      #8  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #9  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473627:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa127cd9 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327cd9)
                                                      #6  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #7  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #8  0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #9  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #10 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473625:
                                                      #0  0x00007e92ad4c488d syscall (libc.so.6 + 0x10688d)
                                                      #1  0x00007e92aa50e464 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e464)
                                                      #2  0x00007e92aa50e4e3 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x70e4e3)
                                                      #3  0x00007e92aa511fe2 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x711fe2)
                                                      #4  0x00007e92a9ed5070 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0xd5070)
                                                      #5  0x00007e92aa12210e n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32210e)
                                                      #6  0x00007e92aa129c42 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x329c42)
                                                      #7  0x00007e92aa127b20 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x327b20)
                                                      #8  0x00007e92aa12987f n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x32987f)
                                                      #9  0x00007e92aa1299dc n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x3299dc)
                                                      #10 0x00007e92aa133eb7 n/a (cygrpc.cpython-310-x86_64-linux-gnu.so + 0x333eb7)
                                                      #11 0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #12 0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473253:
                                                      #0  0x00007e92ad445ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007e92ad448750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007e92a73506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007e92ad44955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007e92ad4c6a3c n/a (libc.so.6 + 0x108a3c)
                                                      ELF object binary architecture: AMD x86-64
Mar 24 23:43:09 ArchDesktop kernel: [drm:amdgpu_mes_flush_shader_debugger [amdgpu]] *ERROR* failed to set_shader_debugger
Mar 24 23:43:09 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Mar 24 23:43:08 ArchDesktop systemd[1]: systemd-coredump@5-697796-0.service: Consumed 3.288s CPU time.
Mar 24 23:43:08 ArchDesktop systemd[1]: systemd-coredump@5-697796-0.service: Deactivated successfully.
Mar 24 23:43:08 ArchDesktop systemd-coredump[697799]: Process 472902 (pt_main_thread) of user 1000 dumped core.
                                                      
                                                      Module libz.b38cb0f0.so.1 without build-id.
                                                      Module librocsparse.so without build-id.
                                                      Module librocrand.so without build-id.
                                                      Module librocfft.so without build-id.
                                                      Module librocsolver.so without build-id.
                                                      Module librocblas.so without build-id.
                                                      Module libmagma.so without build-id.
                                                      Module librccl.so without build-id.
                                                      Module libhiprand.so without build-id.
                                                      Module libhipfft.so without build-id.
                                                      Module libhipblaslt.so without build-id.
                                                      Module libMIOpen.so without build-id.
                                                      Stack trace of thread 473424:
                                                      #0  0x00007f8ab9eab32c n/a (libc.so.6 + 0x8d32c)
                                                      #1  0x00007f8ab9e5a6c8 raise (libc.so.6 + 0x3c6c8)
                                                      #2  0x00007f8ab9e424b8 abort (libc.so.6 + 0x244b8)
                                                      #3  0x00007f89dd26c259 _ZN4rocr4core7Runtime18HwExceptionHandlerElPv (libhsa-runtime64.so + 0x6c259)
                                                      #4  0x00007f89dd2685d9 _ZN4rocr4core7Runtime15AsyncEventsLoopEPv (libhsa-runtime64.so + 0x685d9)
                                                      #5  0x00007f89dd219f57 _ZN4rocr2os16ThreadTrampolineEPv (libhsa-runtime64.so + 0x19f57)
                                                      #6  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #7  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473547:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 472902:
                                                      #0  0x00007f8ab9f0fec7 wait4 (libc.so.6 + 0xf1ec7)
                                                      #1  0x00007f8aba22f2f0 os_waitpid_impl (libpython3.10.so.1.0 + 0x22f2f0)
                                                      #2  0x00007f8aba14aa6f cfunction_vectorcall_FASTCALL (libpython3.10.so.1.0 + 0x14aa6f)
                                                      #3  0x00007f8aba13e5ac _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13e5ac)
                                                      #4  0x00007f8aba14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #5  0x00007f8aba13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #6  0x00007f8aba155496 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x155496)
                                                      #7  0x00007f8aba13addb _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13addb)
                                                      #8  0x00007f8aba14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #9  0x00007f8aba13a120 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13a120)
                                                      #10 0x00007f8aba14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #11 0x00007f8aba139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #12 0x00007f8aba14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #13 0x00007f8aba13e5ac _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x13e5ac)
                                                      #14 0x00007f8aba14a879 _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x14a879)
                                                      #15 0x00007f8aba139d02 _PyObject_VectorcallTstate (libpython3.10.so.1.0 + 0x139d02)
                                                      #16 0x00007f8aba13890c _PyEval_EvalFrame (libpython3.10.so.1.0 + 0x13890c)
                                                      #17 0x00007f8aba1e3954 PyEval_EvalCode (libpython3.10.so.1.0 + 0x1e3954)
                                                      #18 0x00007f8aba1f3393 run_eval_code_obj (libpython3.10.so.1.0 + 0x1f3393)
                                                      #19 0x00007f8aba1eed4a run_mod (libpython3.10.so.1.0 + 0x1eed4a)
                                                      #20 0x00007f8aba09c08d pyrun_file (libpython3.10.so.1.0 + 0x9c08d)
                                                      #21 0x00007f8aba09bd2c _PyRun_SimpleFileObject (libpython3.10.so.1.0 + 0x9bd2c)
                                                      #22 0x00007f8aba09c911 _PyRun_AnyFileObject (libpython3.10.so.1.0 + 0x9c911)
                                                      #23 0x00007f8aba1ffac7 pymain_run_file_obj (libpython3.10.so.1.0 + 0x1ffac7)
                                                      #24 0x00007f8aba1d528b Py_BytesMain (libpython3.10.so.1.0 + 0x1d528b)
                                                      #25 0x00007f8ab9e43cd0 n/a (libc.so.6 + 0x25cd0)
                                                      #26 0x00007f8ab9e43d8a __libc_start_main (libc.so.6 + 0x25d8a)
                                                      #27 0x00005fb47709b045 _start (python3.10 + 0x1045)
                                                      
                                                      Stack trace of thread 473546:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473549:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473552:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473551:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473550:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473553:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473548:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473554:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473556:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473555:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473558:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473559:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473560:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      
                                                      Stack trace of thread 473557:
                                                      #0  0x00007f8ab9ea5ebe n/a (libc.so.6 + 0x87ebe)
                                                      #1  0x00007f8ab9ea8750 pthread_cond_wait (libc.so.6 + 0x8a750)
                                                      #2  0x00007f87f4f506fb blas_thread_server (libopenblas64_p-r0-0cf96a72.3.23.dev.so + 0x3506fb)
                                                      #3  0x00007f8ab9ea955a n/a (libc.so.6 + 0x8b55a)
                                                      #4  0x00007f8ab9f26a3c n/a (libc.so.6 + 0x108a3c)
                                                      ELF object binary architecture: AMD x86-64
Mar 24 23:43:07 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-14bb5ff055db7dcdcc06326f2fa7fbb6d76de5cfea69cc5b21c77f71c6196aa1-runc.Agh3rj.mount: Deactivated successfully.
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset(4) succeeded!
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow done
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow start
Mar 24 23:43:03 ArchDesktop kernel: [drm] kiq ring mec 3 pipe 1 q 0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          RW: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MAPPING_ERROR: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          WALKER_ERROR: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MORE_FAULTS: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          RW: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MAPPING_ERROR: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          WALKER_ERROR: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MORE_FAULTS: 0x0
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          RW: 0x1
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MAPPING_ERROR: 0x1
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          WALKER_ERROR: 0x1
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MORE_FAULTS: 0x1
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Mar 24 23:43:03 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: IP block:gfx_v11_0 is hung!
Mar 24 23:43:03 ArchDesktop systemd[1]: Started Process Core Dump (PID 697805/UID 0).
Mar 24 23:43:02 ArchDesktop systemd[1]: Started Process Core Dump (PID 697804/UID 0).
Mar 24 23:43:02 ArchDesktop systemd[1]: Started Process Core Dump (PID 697800/UID 0).
Mar 24 23:43:02 ArchDesktop systemd[1]: Started Process Core Dump (PID 697795/UID 0).
Mar 24 23:43:02 ArchDesktop systemd[1]: Started Process Core Dump (PID 697796/UID 0).
Mar 24 23:43:02 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset begin!
Mar 24 23:43:02 ArchDesktop kernel: amdgpu: Failed to evict process queues
Mar 24 23:43:02 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: Failed to evict queue 1
Mar 24 23:43:02 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Mar 24 23:43:02 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Mar 24 23:43:02 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Mar 24 23:42:32 ArchDesktop systemd[1]: run-docker-runtime\x2drunc-moby-5a1186cf6856d30309d76d966166ed3cc7784062ee5ef6ab1bc95cb08f9f63b2-runc.OiJMsS.mount: Deactivated successfully.
Mar 24 23:42:18 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:42:18 ArchDesktop rtkit-daemon[933]: Supervising 8 threads of 6 processes of 1 users.
Mar 24 23:42:16 ArchDesktop NetworkManager[650]: <info>  [1711312936.9100] device (enp17s0f3u1u4c2): state change: failed -> disconnected (reason 'none', sys-iface-state: 'managed')
Mar 24 23:42:16 ArchDesktop NetworkManager[650]: <warn>  [1711312936.9099] device (enp17s0f3u1u4c2): Activation: failed for connection 'Wired connection 1'
Mar 24 23:42:16 ArchDesktop NetworkManager[650]: <info>  [1711312936.9096] device (enp17s0f3u1u4c2): state change: ip-config -> failed (reason 'ip-config-unavailable', sys-iface-state: 'managed')
Mar 24 23:42:16 ArchDesktop NetworkManager[650]: <info>  [1711312936.7249] device (enp9s0): state change: failed -> disconnected (reason 'none', sys-iface-state: 'managed')
Mar 24 23:42:16 ArchDesktop NetworkManager[650]: <warn>  [1711312936.7248] device (enp9s0): Activation: failed for connection 'Wired connection 2'
Mar 24 23:42:16 ArchDesktop NetworkManager[650]: <info>  [1711312936.7245] device (enp9s0): state change: ip-config -> failed (reason 'ip-config-unavailable', sys-iface-state: 'managed')

```

<\details>

---

### 评论 #24 — FeepingCreature (2024-03-24T21:59:57Z)

Yeah it keeps happening here with 6.0.2 as well.

---

### 评论 #25 — nonetrix (2024-03-25T06:53:07Z)

> I might have a workaround that maybe helps a little, or it might just be placebo / luck so far. **There are potential drawbacks, though**.
> 
> I noticed that sometimes, but not always, there would be IOMMU fault messages prior to the ones from the amdgpu driver itself. So I thought, hey why not, let's try disabling IOMMU in BIOS. And so far, I've been able to run things ... I don't trust it, obviously even if this works it's not a solution, but I thought I'd share. Those faults were obviously happening for a reason and this seems to just be putting a blindfold on.
> 
> Here's a chat with Gemini about the consequences of disabling IOMMU https://g.co/gemini/share/5d21ada997c1 , **please weigh it up yourself before trying it**. I don't understand IOMMU properly myself.
> 
> PS: I captured this earlier after booting my system and leaving it idle, not even logging in yet:
> 
> ```
> [  555.894238] amdgpu 0000:0d:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000012 SMN_C2PMSG_82:0x00000005
> ```
> 
> (and then the usual circus follows - this is just the start for demonstration) So not even 10 minutes, under no load, with nothing loaded except a Kubuntu login screen. Something is very wrong.

Hey, I got the same issue that you are having somewhat with my RX 6800 same error you mentioned and exact same command it's trying to sent(SMN_C2PMSG_66 and SMN_C2PMSG_82) https://gitlab.freedesktop.org/drm/amd/-/issues/3220 but on my issue they mentioned that a fix is there but hasn't been released maybe relevant? It's not available for testing though :/

Something tells me this is a race condition perhaps lol 

---

### 评论 #26 — romeo4934 (2024-03-31T20:37:07Z)

Same issue. Any help? 

---

### 评论 #27 — yshui (2024-04-07T00:17:42Z)

from my own observations, the MES seems to destabilize as the usable VRAM becomes low. I could be very wrong about this, but I tried limiting the amount of usable VRAM with module parameters (`vramlimit`, `vis_vramlimit`), and that does seem to help.

Interested to see if this works for others.

---

### 评论 #28 — FeepingCreature (2024-04-18T18:29:14Z)

~~Okay, I don't want to hype anybody up unduly, but I haven't seen a MES hang in two days since I installed the [week-old AMD firmware update](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/). Can anyone repro on that?~~

edit: Nope, still happens.

---

### 评论 #29 — nonetrix (2024-04-18T19:02:50Z)

Will see if it fixes my unrelated issue as well, apparently they where working on fixing mine already and had a fixed testing unreleased firmware as of month ago. Hoping AMD gets their act together in general which is why I mention, not sure if my distro is running it though how could I even tell exactly? 

---

### 评论 #30 — FeepingCreature (2024-04-18T19:09:25Z)

You can just clone the repo, `git clone git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git --depth 1`, then `sudo cp linux-firmware/amdgpu/* /lib/firmware/updates/amdgpu/` and reboot. Thanks @saffroy at https://gitlab.freedesktop.org/drm/amd/-/issues/3175 for pointing this out; note that this firmware is relatively untested, hot off the presses, and also your system will overwrite this when it updates anyway, I take no responsibility for damages etc. But also I've been running it for two days and my PC hasn't caught fire yet.

If you've installed it correctly, you should note a numeric change in `grep MES /sys/kernel/debug/dri/{0,1}/amdgpu_firmware_info`. Mine is at MES `0x0000004b`, MES_KIQ `0x00000075`.

edit: But it crashes anyway.

---

### 评论 #31 — nonetrix (2024-04-18T20:10:50Z)

So far not having any crashes with my distros latest, still having the cursor stutters bug perhaps unrelated and if so that's just mildly annoying and can live with that. Don't want to jinx it though so going to let to generate idle, if it crashes I guess I'll look into updating my firmware. Again, I suspect my issue is unrelated but seems others in thread where having mine

Edit: got a crash, seems more stable at least though 

---

### 评论 #32 — FeepingCreature (2024-04-18T20:41:40Z)

Nevermind everyone, sorry for the premature excitement. Two days later, there it goes again.

```
amdgpu 0000:03:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
```

Of course, it had to wait for me to post this to crash...

---

### 评论 #33 — nonetrix (2024-04-26T21:19:58Z)

> `grep MES /sys/kernel/debug/dri/{0,1}/amdgpu_firmware_info`

Huh mine seems to say 
```
/sys/kernel/debug/dri/1/amdgpu_firmware_info:MES_KIQ feature version: 0, firmware version: 0x00000000
/sys/kernel/debug/dri/1/amdgpu_firmware_info:MES feature version: 0, firmware version: 0x00000000
```
Could it be that my card is too old or something? Pretty sure it was applied though, running Ubuntu just for testing, also going to try to run ROCm 6.1 which might have some fixes for issue I am having as well as others. I did have to change the command to use `/lib/firmware/amdgpu/` instead though. Here is the full output of that
```
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 44, firmware version: 0x00000040
PFP feature version: 44, firmware version: 0x00000062
CE feature version: 44, firmware version: 0x00000025
RLC feature version: 1, firmware version: 0x00000060
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 44, firmware version: 0x00000076
MEC2 feature version: 44, firmware version: 0x00000076
IMU feature version: 0, firmware version: 0x00000000
SOS feature version: 0, firmware version: 0x00210e64
ASD feature version: 553648338, firmware version: 0x210000d2
TA XGMI feature version: 0x00000000, firmware version: 0x2000000f
TA RAS feature version: 0x00000000, firmware version: 0x1b00013e
TA HDCP feature version: 0x00000000, firmware version: 0x1700003e
TA DTM feature version: 0x00000000, firmware version: 0x12000016
TA RAP feature version: 0x00000000, firmware version: 0x07000016
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x003a5900 (58.89.0)
SDMA0 feature version: 52, firmware version: 0x00000053
SDMA1 feature version: 52, firmware version: 0x00000053
SDMA2 feature version: 52, firmware version: 0x00000053
SDMA3 feature version: 52, firmware version: 0x00000053
VCN feature version: 0, firmware version: 0x0311e008
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x02020020
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 0, firmware version: 0x00000000
MES feature version: 0, firmware version: 0x00000000
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 113-1MS21XL203W_210810
```
I manually reinstalled the `linux-firmware` package and nothing changed, so I think I am doing it wrong

---

### 评论 #34 — Disty0 (2024-04-28T22:22:00Z)

This MES crash tends to segfault other unrelated programs as well.

This one in particular was interesting. Entire system locked up shortly after this screenshot:
(I use an Intel dGPU for video out.)

![Screenshot from 2024-04-29 01-01-13](https://github.com/ROCm/ROCm/assets/47277141/27be96e2-6e0e-4a1c-9a14-5da6712ec77c)

OS: Arch Linux 6.8.4
CPU: AMD Ryzen 7 5800X3D
GPU0: AMD RX 7900 XTX Sapphire Pulse (No video output, runs only PyTorch)
GPU1: Intel ARC A770 LE (Used for video output and genral use)

ROCm: 6.0.2
PyTorch: 2.3.0+rocm6.0

Journalctl in reverse order:

<details>

```
(Physically cutted power at this point since nothing on the system was responding to anything)

Apr 29 00:58:23 ArchDesktop kernel: general protection fault, probably for non-canonical address 0x1293823692cd285f: 0000 [#4] PREEMPT SMP NOPTI
Apr 29 00:58:23 ArchDesktop sudo[1733267]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:23 ArchDesktop sudo[1733267]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:23 ArchDesktop sudo[1733187]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:22 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:22 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:22 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:22 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:22 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:22 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:22 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:22 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:22 ArchDesktop sudo[1733187]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:22 ArchDesktop sudo[1733187]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:22 ArchDesktop sudo[1733115]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:21 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:21 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:20 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:20 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:20 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:20 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:20 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:20 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:20 ArchDesktop sudo[1733115]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:20 ArchDesktop sudo[1733115]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:20 ArchDesktop sudo[1732935]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:20 ArchDesktop kernel: ---[ end trace 0000000000000000 ]---
Apr 29 00:58:20 ArchDesktop kernel:  </TASK>
Apr 29 00:58:20 ArchDesktop kernel: R13: 000000c000a8a530 R14: 000000c000a08380 R15: 0000000fffffffff
Apr 29 00:58:20 ArchDesktop kernel: R10: 0000000000000000 R11: 0000000000000000 R12: 000000000264cfa4
Apr 29 00:58:20 ArchDesktop kernel: RBP: 000070489b3ffd78 R08: 0000000000000020 R09: 0000000000000001
Apr 29 00:58:20 ArchDesktop kernel: RDX: 000070489b3ffdb8 RSI: 0000000000000000 RDI: 0000000000d13d44
Apr 29 00:58:20 ArchDesktop kernel: RAX: 0000000000000000 RBX: 0000000003484420 RCX: 000000000264cfa4
Apr 29 00:58:20 ArchDesktop kernel: RSP: 002b:000070489b3ffc08 EFLAGS: 00010287
Apr 29 00:58:20 ArchDesktop kernel: Code: 36 45 31 db eb 31 4c 63 de 66 0f 1f 84 00 00 00 00 00 0f 1f 00 49 81 fb 00 00 10 00 0f 83 9b 00 00 00 4c 8b a4 24 68 01 00 00 <41> 84 04 24 49 c1 e3 04 47 0f b6 1c 1c 41 80 fb 16 75 24 44 0f b6
Apr 29 00:58:20 ArchDesktop kernel: RIP: 0033:0xd69e95
Apr 29 00:58:20 ArchDesktop kernel:  rewind_stack_and_make_dead+0x17/0x20
Apr 29 00:58:20 ArchDesktop kernel:  make_task_dead+0x83/0x170
Apr 29 00:58:20 ArchDesktop kernel:  ? do_exit+0x70/0xb70
Apr 29 00:58:20 ArchDesktop kernel:  ? do_exit+0x90f/0xb70
Apr 29 00:58:20 ArchDesktop kernel:  ? asm_exc_invalid_op+0x1a/0x20
Apr 29 00:58:20 ArchDesktop kernel:  ? exc_invalid_op+0x19/0xc0
Apr 29 00:58:20 ArchDesktop kernel:  ? handle_bug+0x3c/0x80
Apr 29 00:58:20 ArchDesktop kernel:  ? report_bug+0x202/0x270
Apr 29 00:58:20 ArchDesktop kernel:  ? do_exit+0x90f/0xb70
Apr 29 00:58:20 ArchDesktop kernel:  ? __warn+0x81/0x1b0
Apr 29 00:58:20 ArchDesktop kernel:  <TASK>
Apr 29 00:58:20 ArchDesktop kernel: Call Trace:
Apr 29 00:58:20 ArchDesktop kernel: PKRU: 55555554
Apr 29 00:58:20 ArchDesktop kernel: CR2: 000000000264cfa4 CR3: 00000001432c2000 CR4: 0000000000f50ef0
Apr 29 00:58:20 ArchDesktop kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Apr 29 00:58:20 ArchDesktop kernel: FS:  000070489b4006c0(0000) GS:ffff899c7edc0000(0000) knlGS:0000000000000000
Apr 29 00:58:20 ArchDesktop kernel: R13: ffff899181094a40 R14: 0000000000000000 R15: 0000000000000000
Apr 29 00:58:20 ArchDesktop kernel: R10: ffff899caf2478c0 R11: 0000000000000003 R12: 000000000000000b
Apr 29 00:58:20 ArchDesktop kernel: RBP: ffff8991810a3600 R08: 00000000ffffffea R09: 000000010001bdd0
Apr 29 00:58:20 ArchDesktop kernel: RDX: 0000000000000001 RSI: 0000000000002710 RDI: ffff899181094a40
Apr 29 00:58:20 ArchDesktop kernel: RAX: 0000000000000000 RBX: ffff8991e52ba380 RCX: 0000000000000000
Apr 29 00:58:20 ArchDesktop kernel: RSP: 0000:ffff9db8518d3ed8 EFLAGS: 00010282
Apr 29 00:58:20 ArchDesktop kernel: Code: 47 0c 6c 00 e9 f5 fd ff ff 48 8d 7d 18 e8 d9 7e 08 00 e9 fd f7 ff ff 48 8b bb 08 06 00 00 31 f6 e8 76 e0 ff ff e9 42 fd ff ff <0f> 0b e9 68 f7 ff ff 0f 0b e9 25 f7 ff ff 4c 89 e6 bf 05 06 00 00
Apr 29 00:58:20 ArchDesktop kernel: RIP: 0010:do_exit+0x90f/0xb70
Apr 29 00:58:20 ArchDesktop kernel: Hardware name: System manufacturer System Product Name/ROG STRIX X570-F GAMING, BIOS 5003 10/07/2023
Apr 29 00:58:20 ArchDesktop kernel: CPU: 15 PID: 1432 Comm: containerd Tainted: G      D    OE      6.8.4-zen1-1-zen #1 4a88f2661038c2a3bb69aa70fb41a5735338823c
Apr 29 00:58:20 ArchDesktop kernel:  acpi_cpufreq k10temp i2c_piix4 mei snd_hwdep ptp xor pps_core raid6_pq dca mousedev joydev libcrc32c ryzen_smu(OE) mac_hid snd_aloop snd_pcm snd_timer snd soundcore i2c_dev sr_mod cdrom v4l2loopback(OE) videodev mc sg crypto_user dm_mod loop fuse nfnetlink ip_tables x_tables ext4 crc32c_generic crc16 mbcache jbd2 hid_generic xe drm_gpuvm usbhid amdgpu i915 amdxcp drm_ttm_helper intel_gtt drm_exec video gpu_sched i2c_algo_bit ttm drm_suballoc_helper nvme drm_buddy crc32c_intel drm_display_helper nvme_core xhci_pci cec nvme_auth xhci_pci_renesas wmi
Apr 29 00:58:20 ArchDesktop kernel: Modules linked in: ip6table_filter ip6_tables xt_nat xt_tcpudp veth xt_conntrack xt_MASQUERADE nf_conntrack_netlink xfrm_user xfrm_algo iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype iptable_filter br_netfilter snd_seq_dummy snd_hrtimer snd_seq snd_seq_device macvtap macvlan vhost_net vhost vhost_iotlb tap tun overlay bridge stp llc nct6775 nct6775_core hwmon_vid jc42 snd_hda_codec_realtek snd_hda_codec_generic snd_hda_codec_hdmi mei_pxp mei_hdcp cdc_mbim cdc_wdm intel_rapl_msr intel_rapl_common kvm_amd kvm irqbypass crct10dif_pclmul crc32_pclmul polyval_clmulni polyval_generic gf128mul ghash_clmulni_intel eeepc_wmi sha512_ssse3 asus_wmi sha256_ssse3 ledtrig_audio sha1_ssse3 nls_iso8859_1 platform_profile aesni_intel vfat cdc_ncm i8042 crypto_simd sparse_keymap cdc_ether fat asus_ec_sensors snd_hda_intel cryptd serio usbnet snd_intel_dspcfg mii btrfs rapl rfkill snd_intel_sdw_acpi mei_gsc snd_hda_codec mxm_wmi sp5100_tco igb mei_me pcspkr snd_hda_core ccp wmi_bmof blake2b_generic
Apr 29 00:58:20 ArchDesktop kernel: WARNING: CPU: 15 PID: 1432 at kernel/exit.c:820 do_exit+0x90f/0xb70
Apr 29 00:58:20 ArchDesktop kernel: ------------[ cut here ]------------
Apr 29 00:58:20 ArchDesktop kernel: PKRU: 55555554
Apr 29 00:58:20 ArchDesktop kernel: CR2: 000000000264cfa4 CR3: 00000001432c2000 CR4: 0000000000f50ef0
Apr 29 00:58:20 ArchDesktop kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Apr 29 00:58:20 ArchDesktop kernel: FS:  000070489b4006c0(0000) GS:ffff899c7edc0000(0000) knlGS:0000000000000000
Apr 29 00:58:20 ArchDesktop kernel: R13: ffff899180245500 R14: 0000000000000068 R15: 1293823692cd282f
Apr 29 00:58:20 ArchDesktop kernel: R10: 0000000000000001 R11: ffff899caf37bd80 R12: 0000000000408d40
Apr 29 00:58:20 ArchDesktop kernel: RBP: ffff9db855d07a58 R08: 0000000000000001 R09: 0000000000000000
Apr 29 00:58:20 ArchDesktop kernel: RDX: 00000000671fb80f RSI: 000000000003b580 RDI: ffff89988cf8e3c0
Apr 29 00:58:20 ArchDesktop kernel: RAX: 1293823692cd285f RBX: 5247cd920044d7d0 RCX: 0000000000000001
Apr 29 00:58:20 ArchDesktop kernel: RSP: 0018:ffff9db855d07a20 EFLAGS: 00010206
Apr 29 00:58:20 ArchDesktop kernel: Code: 08 48 83 78 10 00 4c 8b 38 0f 84 ab 01 00 00 4d 85 ff 0f 84 a2 01 00 00 41 8b 45 28 49 8b 9d b8 00 00 00 49 8b 75 00 4c 01 f8 <48> 33 18 48 89 c1 4c 89 f8 48 0f c9 48 31 cb 48 8d 8a 00 02 00 00
Apr 29 00:58:20 ArchDesktop kernel: RIP: 0010:kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:20 ArchDesktop kernel: ---[ end trace 0000000000000000 ]---
Apr 29 00:58:20 ArchDesktop kernel:  acpi_cpufreq k10temp i2c_piix4 mei snd_hwdep ptp xor pps_core raid6_pq dca mousedev joydev libcrc32c ryzen_smu(OE) mac_hid snd_aloop snd_pcm snd_timer snd soundcore i2c_dev sr_mod cdrom v4l2loopback(OE) videodev mc sg crypto_user dm_mod loop fuse nfnetlink ip_tables x_tables ext4 crc32c_generic crc16 mbcache jbd2 hid_generic xe drm_gpuvm usbhid amdgpu i915 amdxcp drm_ttm_helper intel_gtt drm_exec video gpu_sched i2c_algo_bit ttm drm_suballoc_helper nvme drm_buddy crc32c_intel drm_display_helper nvme_core xhci_pci cec nvme_auth xhci_pci_renesas wmi
Apr 29 00:58:20 ArchDesktop kernel: Modules linked in: ip6table_filter ip6_tables xt_nat xt_tcpudp veth xt_conntrack xt_MASQUERADE nf_conntrack_netlink xfrm_user xfrm_algo iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype iptable_filter br_netfilter snd_seq_dummy snd_hrtimer snd_seq snd_seq_device macvtap macvlan vhost_net vhost vhost_iotlb tap tun overlay bridge stp llc nct6775 nct6775_core hwmon_vid jc42 snd_hda_codec_realtek snd_hda_codec_generic snd_hda_codec_hdmi mei_pxp mei_hdcp cdc_mbim cdc_wdm intel_rapl_msr intel_rapl_common kvm_amd kvm irqbypass crct10dif_pclmul crc32_pclmul polyval_clmulni polyval_generic gf128mul ghash_clmulni_intel eeepc_wmi sha512_ssse3 asus_wmi sha256_ssse3 ledtrig_audio sha1_ssse3 nls_iso8859_1 platform_profile aesni_intel vfat cdc_ncm i8042 crypto_simd sparse_keymap cdc_ether fat asus_ec_sensors snd_hda_intel cryptd serio usbnet snd_intel_dspcfg mii btrfs rapl rfkill snd_intel_sdw_acpi mei_gsc snd_hda_codec mxm_wmi sp5100_tco igb mei_me pcspkr snd_hda_core ccp wmi_bmof blake2b_generic
Apr 29 00:58:20 ArchDesktop kernel:  </TASK>
Apr 29 00:58:20 ArchDesktop kernel: R13: 000000c000a8a530 R14: 000000c000a08380 R15: 0000000fffffffff
Apr 29 00:58:20 ArchDesktop kernel: R10: 0000000000000000 R11: 0000000000000000 R12: 000000000264cfa4
Apr 29 00:58:20 ArchDesktop kernel: RBP: 000070489b3ffd78 R08: 0000000000000020 R09: 0000000000000001
Apr 29 00:58:20 ArchDesktop kernel: RDX: 000070489b3ffdb8 RSI: 0000000000000000 RDI: 0000000000d13d44
Apr 29 00:58:20 ArchDesktop kernel: RAX: 0000000000000000 RBX: 0000000003484420 RCX: 000000000264cfa4
Apr 29 00:58:20 ArchDesktop kernel: RSP: 002b:000070489b3ffc08 EFLAGS: 00010287
Apr 29 00:58:20 ArchDesktop kernel: Code: 36 45 31 db eb 31 4c 63 de 66 0f 1f 84 00 00 00 00 00 0f 1f 00 49 81 fb 00 00 10 00 0f 83 9b 00 00 00 4c 8b a4 24 68 01 00 00 <41> 84 04 24 49 c1 e3 04 47 0f b6 1c 1c 41 80 fb 16 75 24 44 0f b6
Apr 29 00:58:20 ArchDesktop kernel: RIP: 0033:0xd69e95
Apr 29 00:58:20 ArchDesktop kernel:  asm_exc_page_fault+0x26/0x30
Apr 29 00:58:20 ArchDesktop kernel:  exc_page_fault+0x7f/0x180
Apr 29 00:58:20 ArchDesktop kernel:  do_user_addr_fault+0x1e1/0xb50
Apr 29 00:58:20 ArchDesktop kernel:  handle_mm_fault+0x1468/0x1510
Apr 29 00:58:20 ArchDesktop kernel:  do_read_fault+0x44/0x1c0
Apr 29 00:58:20 ArchDesktop kernel:  __do_fault+0x35/0x120
Apr 29 00:58:20 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:20 ArchDesktop kernel:  ? try_to_wake_up+0x343/0xcd0
Apr 29 00:58:20 ArchDesktop kernel:  ? filemap_map_pages+0x443/0x500
Apr 29 00:58:20 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:20 ArchDesktop kernel:  filemap_fault+0x54d/0x1240
Apr 29 00:58:20 ArchDesktop kernel:  page_cache_ra_unbounded+0x106/0x180
Apr 29 00:58:20 ArchDesktop kernel:  read_pages+0x85/0x250
Apr 29 00:58:20 ArchDesktop kernel:  ext4_mpage_readpages+0x68e/0xb60 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:20 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:20 ArchDesktop kernel:  ext4_map_blocks+0x270/0x730 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:20 ArchDesktop kernel:  ext4_ext_map_blocks+0xa1/0x1b00 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:20 ArchDesktop kernel:  ext4_find_extent.constprop.0+0x142/0x2f0 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:20 ArchDesktop kernel:  __read_extent_tree_block+0x68/0x170 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:20 ArchDesktop kernel:  ? select_task_rq_fair+0x6c4/0x1ae0
Apr 29 00:58:20 ArchDesktop kernel:  bdev_getblk+0x13b/0x270
Apr 29 00:58:20 ArchDesktop kernel:  folio_alloc_buffers+0xee/0x230
Apr 29 00:58:20 ArchDesktop kernel:  ? folio_alloc_buffers+0xee/0x230
Apr 29 00:58:20 ArchDesktop kernel:  ? kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:20 ArchDesktop kernel:  ? asm_exc_general_protection+0x26/0x30
Apr 29 00:58:20 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:20 ArchDesktop kernel:  ? exc_general_protection+0x388/0x4a0
Apr 29 00:58:20 ArchDesktop kernel:  ? die_addr+0x128/0x130
Apr 29 00:58:20 ArchDesktop kernel:  <TASK>
Apr 29 00:58:20 ArchDesktop kernel: Call Trace:
Apr 29 00:58:20 ArchDesktop kernel: PKRU: 55555554
Apr 29 00:58:20 ArchDesktop kernel: CR2: 000000000264cfa4 CR3: 00000001432c2000 CR4: 0000000000f50ef0
Apr 29 00:58:20 ArchDesktop kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Apr 29 00:58:20 ArchDesktop kernel: FS:  000070489b4006c0(0000) GS:ffff899c7edc0000(0000) knlGS:0000000000000000
Apr 29 00:58:20 ArchDesktop kernel: R13: ffff899180245500 R14: 0000000000000068 R15: 1293823692cd282f
Apr 29 00:58:20 ArchDesktop kernel: R10: 0000000000000001 R11: ffff899caf37bd80 R12: 0000000000400d48
Apr 29 00:58:20 ArchDesktop kernel: RBP: ffff9db8518d3838 R08: 0000000000000001 R09: 000000000000000f
Apr 29 00:58:20 ArchDesktop kernel: RDX: 00000000671fb80f RSI: 000000000003b580 RDI: ffff8991c7b61280
Apr 29 00:58:20 ArchDesktop kernel: RAX: 1293823692cd285f RBX: 5247cd920044d7d0 RCX: 0000000000000001
Apr 29 00:58:20 ArchDesktop kernel: RSP: 0000:ffff9db8518d3800 EFLAGS: 00010206
Apr 29 00:58:20 ArchDesktop kernel: Code: 08 48 83 78 10 00 4c 8b 38 0f 84 ab 01 00 00 4d 85 ff 0f 84 a2 01 00 00 41 8b 45 28 49 8b 9d b8 00 00 00 49 8b 75 00 4c 01 f8 <48> 33 18 48 89 c1 4c 89 f8 48 0f c9 48 31 cb 48 8d 8a 00 02 00 00
Apr 29 00:58:20 ArchDesktop kernel: RIP: 0010:kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:20 ArchDesktop kernel: Hardware name: System manufacturer System Product Name/ROG STRIX X570-F GAMING, BIOS 5003 10/07/2023
Apr 29 00:58:20 ArchDesktop kernel: CPU: 15 PID: 1432 Comm: containerd Tainted: G      D    OE      6.8.4-zen1-1-zen #1 4a88f2661038c2a3bb69aa70fb41a5735338823c
Apr 29 00:58:20 ArchDesktop kernel: general protection fault, probably for non-canonical address 0x1293823692cd285f: 0000 [#3] PREEMPT SMP NOPTI
Apr 29 00:58:19 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:19 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:19 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:19 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:19 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:19 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:19 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:19 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:19 ArchDesktop sudo[1732935]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:19 ArchDesktop sudo[1732935]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:19 ArchDesktop sudo[1732870]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:18 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:18 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:17 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:17 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:17 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:17 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:17 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:17 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:17 ArchDesktop sudo[1732870]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:17 ArchDesktop sudo[1732870]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:17 ArchDesktop sudo[1732798]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:16 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:16 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:16 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:16 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:16 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:16 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:16 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:16 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:16 ArchDesktop sudo[1732798]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:16 ArchDesktop sudo[1732798]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:16 ArchDesktop sudo[1732696]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:15 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:15 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:14 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:14 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:14 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:14 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:14 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:14 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:14 ArchDesktop sudo[1732696]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:14 ArchDesktop sudo[1732696]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:14 ArchDesktop sudo[1732634]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:14 ArchDesktop kernel: PKRU: 55555554
Apr 29 00:58:14 ArchDesktop kernel: CR2: 00000e8c5a203d88 CR3: 000000045cd72000 CR4: 0000000000f50ef0
Apr 29 00:58:14 ArchDesktop kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Apr 29 00:58:14 ArchDesktop kernel: FS:  000070311b6a6080(0000) GS:ffff899c7edc0000(0000) knlGS:0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: R13: ffff899180245500 R14: 0000000000000068 R15: 1293823692cd282f
Apr 29 00:58:14 ArchDesktop kernel: R10: 0000000000000001 R11: ffff899caf37bd80 R12: 0000000000408d40
Apr 29 00:58:14 ArchDesktop kernel: RBP: ffff9db855d07a58 R08: 0000000000000001 R09: 0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: RDX: 00000000671fb80f RSI: 000000000003b580 RDI: ffff89988cf8e3c0
Apr 29 00:58:14 ArchDesktop kernel: RAX: 1293823692cd285f RBX: 5247cd920044d7d0 RCX: 0000000000000001
Apr 29 00:58:14 ArchDesktop kernel: RSP: 0018:ffff9db855d07a20 EFLAGS: 00010206
Apr 29 00:58:14 ArchDesktop kernel: Code: 08 48 83 78 10 00 4c 8b 38 0f 84 ab 01 00 00 4d 85 ff 0f 84 a2 01 00 00 41 8b 45 28 49 8b 9d b8 00 00 00 49 8b 75 00 4c 01 f8 <48> 33 18 48 89 c1 4c 89 f8 48 0f c9 48 31 cb 48 8d 8a 00 02 00 00
Apr 29 00:58:14 ArchDesktop kernel: RIP: 0010:kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:14 ArchDesktop kernel: ---[ end trace 0000000000000000 ]---
Apr 29 00:58:14 ArchDesktop kernel:  acpi_cpufreq k10temp i2c_piix4 mei snd_hwdep ptp xor pps_core raid6_pq dca mousedev joydev libcrc32c ryzen_smu(OE) mac_hid snd_aloop snd_pcm snd_timer snd soundcore i2c_dev sr_mod cdrom v4l2loopback(OE) videodev mc sg crypto_user dm_mod loop fuse nfnetlink ip_tables x_tables ext4 crc32c_generic crc16 mbcache jbd2 hid_generic xe drm_gpuvm usbhid amdgpu i915 amdxcp drm_ttm_helper intel_gtt drm_exec video gpu_sched i2c_algo_bit ttm drm_suballoc_helper nvme drm_buddy crc32c_intel drm_display_helper nvme_core xhci_pci cec nvme_auth xhci_pci_renesas wmi
Apr 29 00:58:14 ArchDesktop kernel: Modules linked in: ip6table_filter ip6_tables xt_nat xt_tcpudp veth xt_conntrack xt_MASQUERADE nf_conntrack_netlink xfrm_user xfrm_algo iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype iptable_filter br_netfilter snd_seq_dummy snd_hrtimer snd_seq snd_seq_device macvtap macvlan vhost_net vhost vhost_iotlb tap tun overlay bridge stp llc nct6775 nct6775_core hwmon_vid jc42 snd_hda_codec_realtek snd_hda_codec_generic snd_hda_codec_hdmi mei_pxp mei_hdcp cdc_mbim cdc_wdm intel_rapl_msr intel_rapl_common kvm_amd kvm irqbypass crct10dif_pclmul crc32_pclmul polyval_clmulni polyval_generic gf128mul ghash_clmulni_intel eeepc_wmi sha512_ssse3 asus_wmi sha256_ssse3 ledtrig_audio sha1_ssse3 nls_iso8859_1 platform_profile aesni_intel vfat cdc_ncm i8042 crypto_simd sparse_keymap cdc_ether fat asus_ec_sensors snd_hda_intel cryptd serio usbnet snd_intel_dspcfg mii btrfs rapl rfkill snd_intel_sdw_acpi mei_gsc snd_hda_codec mxm_wmi sp5100_tco igb mei_me pcspkr snd_hda_core ccp wmi_bmof blake2b_generic
Apr 29 00:58:14 ArchDesktop kernel:  </TASK>
Apr 29 00:58:14 ArchDesktop kernel: R13: 00007ffed58b5380 R14: 0000000000000005 R15: 0000000000000006
Apr 29 00:58:14 ArchDesktop kernel: R10: 0000000000000000 R11: 0000000000000202 R12: 00000007f167e000
Apr 29 00:58:14 ArchDesktop kernel: RBP: 00007ffed58b5240 R08: 00000007f167e000 R09: 0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: RDX: 0000000000000006 RSI: 0000000000000000 RDI: 0000000000000005
Apr 29 00:58:14 ArchDesktop kernel: RAX: ffffffffffffffda RBX: 00000007f167e000 RCX: 000070311c054647
Apr 29 00:58:14 ArchDesktop kernel: RSP: 002b:00007ffed58b5198 EFLAGS: 00000202 ORIG_RAX: 0000000000000113
Apr 29 00:58:14 ArchDesktop kernel: Code: ff ff ff ff c3 66 2e 0f 1f 84 00 00 00 00 00 0f 1f 40 00 f3 0f 1e fa 80 3d 05 6a 0d 00 00 49 89 ca 74 10 b8 13 01 00 00 0f 05 <48> 3d 00 f0 ff ff 77 71 c3 55 48 83 ec 30 44 89 4c 24 2c 4c 89 44
Apr 29 00:58:14 ArchDesktop kernel: RIP: 0033:0x70311c054647
Apr 29 00:58:14 ArchDesktop kernel:  entry_SYSCALL_64_after_hwframe+0x73/0x7b
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? syscall_exit_to_user_mode+0x80/0x230
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? switch_fpu_return+0x50/0xe0
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  do_syscall_64+0x89/0x170
Apr 29 00:58:14 ArchDesktop kernel:  __x64_sys_splice+0xb2/0x120
Apr 29 00:58:14 ArchDesktop kernel:  __do_splice+0x1f0/0x220
Apr 29 00:58:14 ArchDesktop kernel:  do_splice+0x312/0x8e0
Apr 29 00:58:14 ArchDesktop kernel:  iter_file_splice_write+0x33d/0x570
Apr 29 00:58:14 ArchDesktop kernel:  ext4_buffered_write_iter+0xa3/0x170 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  ? finish_wait+0x3c/0xa0
Apr 29 00:58:14 ArchDesktop kernel:  generic_perform_write+0xd9/0x240
Apr 29 00:58:14 ArchDesktop kernel:  ext4_da_write_begin+0x1a2/0x2f0 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? __pfx_ext4_da_get_block_prep+0x10/0x10 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ext4_block_write_begin+0x41c/0x520 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  create_empty_buffers+0x1d/0xb0
Apr 29 00:58:14 ArchDesktop kernel:  folio_alloc_buffers+0xee/0x230
Apr 29 00:58:14 ArchDesktop kernel:  ? folio_alloc_buffers+0xee/0x230
Apr 29 00:58:14 ArchDesktop kernel:  ? kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:14 ArchDesktop kernel:  ? asm_exc_general_protection+0x26/0x30
Apr 29 00:58:14 ArchDesktop kernel:  ? exc_general_protection+0x388/0x4a0
Apr 29 00:58:14 ArchDesktop kernel:  ? die_addr+0x128/0x130
Apr 29 00:58:14 ArchDesktop kernel:  <TASK>
Apr 29 00:58:14 ArchDesktop kernel: Call Trace:
Apr 29 00:58:14 ArchDesktop kernel: PKRU: 55555554
Apr 29 00:58:14 ArchDesktop kernel: CR2: 00000e8c5a203d88 CR3: 000000045cd72000 CR4: 0000000000f50ef0
Apr 29 00:58:14 ArchDesktop kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Apr 29 00:58:14 ArchDesktop kernel: FS:  000070311b6a6080(0000) GS:ffff899c7edc0000(0000) knlGS:0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: R13: ffff899180245500 R14: 0000000000000068 R15: 1293823692cd282f
Apr 29 00:58:14 ArchDesktop kernel: R10: 0000000000000000 R11: 0000000000000019 R12: 0000000000408d40
Apr 29 00:58:14 ArchDesktop kernel: RBP: ffff9db85597fa38 R08: 0000000000000001 R09: 0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: RDX: 00000000671fb80f RSI: 000000000003b580 RDI: ffff8992490ac700
Apr 29 00:58:14 ArchDesktop kernel: RAX: 1293823692cd285f RBX: 5247cd920044d7d0 RCX: 0000000000000034
Apr 29 00:58:14 ArchDesktop kernel: RSP: 0018:ffff9db85597fa00 EFLAGS: 00010206
Apr 29 00:58:14 ArchDesktop kernel: Code: 08 48 83 78 10 00 4c 8b 38 0f 84 ab 01 00 00 4d 85 ff 0f 84 a2 01 00 00 41 8b 45 28 49 8b 9d b8 00 00 00 49 8b 75 00 4c 01 f8 <48> 33 18 48 89 c1 4c 89 f8 48 0f c9 48 31 cb 48 8d 8a 00 02 00 00
Apr 29 00:58:14 ArchDesktop kernel: RIP: 0010:kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:14 ArchDesktop kernel: Hardware name: System manufacturer System Product Name/ROG STRIX X570-F GAMING, BIOS 5003 10/07/2023
Apr 29 00:58:14 ArchDesktop kernel: CPU: 15 PID: 1729933 Comm: systemd-coredum Tainted: G      D    OE      6.8.4-zen1-1-zen #1 4a88f2661038c2a3bb69aa70fb41a5735338823c
Apr 29 00:58:14 ArchDesktop kernel: general protection fault, probably for non-canonical address 0x1293823692cd285f: 0000 [#2] PREEMPT SMP NOPTI
Apr 29 00:58:14 ArchDesktop kernel: PKRU: 55555554
Apr 29 00:58:14 ArchDesktop kernel: CR2: 00007fae5030cb80 CR3: 00000005ab238000 CR4: 0000000000f50ef0
Apr 29 00:58:14 ArchDesktop kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Apr 29 00:58:14 ArchDesktop kernel: FS:  000074a9583b8080(0000) GS:ffff899c7edc0000(0000) knlGS:0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: R13: ffff899180245500 R14: 0000000000000068 R15: 1293823692cd282f
Apr 29 00:58:14 ArchDesktop kernel: R10: 0000000000000001 R11: ffff899caf37bd80 R12: 0000000000408d40
Apr 29 00:58:14 ArchDesktop kernel: RBP: ffff9db855d07a58 R08: 0000000000000001 R09: 0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: RDX: 00000000671fb80f RSI: 000000000003b580 RDI: ffff89988cf8e3c0
Apr 29 00:58:14 ArchDesktop kernel: RAX: 1293823692cd285f RBX: 5247cd920044d7d0 RCX: 0000000000000001
Apr 29 00:58:14 ArchDesktop kernel: RSP: 0018:ffff9db855d07a20 EFLAGS: 00010206
Apr 29 00:58:14 ArchDesktop kernel: Code: 08 48 83 78 10 00 4c 8b 38 0f 84 ab 01 00 00 4d 85 ff 0f 84 a2 01 00 00 41 8b 45 28 49 8b 9d b8 00 00 00 49 8b 75 00 4c 01 f8 <48> 33 18 48 89 c1 4c 89 f8 48 0f c9 48 31 cb 48 8d 8a 00 02 00 00
Apr 29 00:58:14 ArchDesktop kernel: RIP: 0010:kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:14 ArchDesktop kernel: ---[ end trace 0000000000000000 ]---
Apr 29 00:58:14 ArchDesktop kernel:  acpi_cpufreq k10temp i2c_piix4 mei snd_hwdep ptp xor pps_core raid6_pq dca mousedev joydev libcrc32c ryzen_smu(OE) mac_hid snd_aloop snd_pcm snd_timer snd soundcore i2c_dev sr_mod cdrom v4l2loopback(OE) videodev mc sg crypto_user dm_mod loop fuse nfnetlink ip_tables x_tables ext4 crc32c_generic crc16 mbcache jbd2 hid_generic xe drm_gpuvm usbhid amdgpu i915 amdxcp drm_ttm_helper intel_gtt drm_exec video gpu_sched i2c_algo_bit ttm drm_suballoc_helper nvme drm_buddy crc32c_intel drm_display_helper nvme_core xhci_pci cec nvme_auth xhci_pci_renesas wmi
Apr 29 00:58:14 ArchDesktop kernel: Modules linked in: ip6table_filter ip6_tables xt_nat xt_tcpudp veth xt_conntrack xt_MASQUERADE nf_conntrack_netlink xfrm_user xfrm_algo iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype iptable_filter br_netfilter snd_seq_dummy snd_hrtimer snd_seq snd_seq_device macvtap macvlan vhost_net vhost vhost_iotlb tap tun overlay bridge stp llc nct6775 nct6775_core hwmon_vid jc42 snd_hda_codec_realtek snd_hda_codec_generic snd_hda_codec_hdmi mei_pxp mei_hdcp cdc_mbim cdc_wdm intel_rapl_msr intel_rapl_common kvm_amd kvm irqbypass crct10dif_pclmul crc32_pclmul polyval_clmulni polyval_generic gf128mul ghash_clmulni_intel eeepc_wmi sha512_ssse3 asus_wmi sha256_ssse3 ledtrig_audio sha1_ssse3 nls_iso8859_1 platform_profile aesni_intel vfat cdc_ncm i8042 crypto_simd sparse_keymap cdc_ether fat asus_ec_sensors snd_hda_intel cryptd serio usbnet snd_intel_dspcfg mii btrfs rapl rfkill snd_intel_sdw_acpi mei_gsc snd_hda_codec mxm_wmi sp5100_tco igb mei_me pcspkr snd_hda_core ccp wmi_bmof blake2b_generic
Apr 29 00:58:14 ArchDesktop kernel:  </TASK>
Apr 29 00:58:14 ArchDesktop kernel: R13: 00007fff0370fde0 R14: 0000000000000005 R15: 0000000000000006
Apr 29 00:58:14 ArchDesktop kernel: R10: 0000000000000000 R11: 0000000000000202 R12: 000000064b326000
Apr 29 00:58:14 ArchDesktop kernel: RBP: 00007fff0370fca0 R08: 000000064b326000 R09: 0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: RDX: 0000000000000006 RSI: 0000000000000000 RDI: 0000000000000005
Apr 29 00:58:14 ArchDesktop kernel: RAX: ffffffffffffffda RBX: 000000064b326000 RCX: 000074a958db6647
Apr 29 00:58:14 ArchDesktop kernel: RSP: 002b:00007fff0370fbf8 EFLAGS: 00000202 ORIG_RAX: 0000000000000113
Apr 29 00:58:14 ArchDesktop kernel: Code: ff ff ff ff c3 66 2e 0f 1f 84 00 00 00 00 00 0f 1f 40 00 f3 0f 1e fa 80 3d 05 6a 0d 00 00 49 89 ca 74 10 b8 13 01 00 00 0f 05 <48> 3d 00 f0 ff ff 77 71 c3 55 48 83 ec 30 44 89 4c 24 2c 4c 89 44
Apr 29 00:58:14 ArchDesktop kernel: RIP: 0033:0x74a958db6647
Apr 29 00:58:14 ArchDesktop kernel:  entry_SYSCALL_64_after_hwframe+0x73/0x7b
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? syscall_exit_to_user_mode+0x80/0x230
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? do_syscall_64+0x96/0x170
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  do_syscall_64+0x89/0x170
Apr 29 00:58:14 ArchDesktop kernel:  __x64_sys_splice+0xb2/0x120
Apr 29 00:58:14 ArchDesktop kernel:  __do_splice+0x1f0/0x220
Apr 29 00:58:14 ArchDesktop kernel:  do_splice+0x312/0x8e0
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  iter_file_splice_write+0x33d/0x570
Apr 29 00:58:14 ArchDesktop kernel:  ext4_buffered_write_iter+0xa3/0x170 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  generic_perform_write+0xd9/0x240
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? ext4_da_write_end+0xad/0x370 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  ext4_da_write_begin+0x1a2/0x2f0 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  ? __block_commit_write+0x78/0xb0
Apr 29 00:58:14 ArchDesktop kernel:  ? srso_alias_return_thunk+0x5/0xfbef5
Apr 29 00:58:14 ArchDesktop kernel:  ? __pfx_ext4_da_get_block_prep+0x10/0x10 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  ext4_block_write_begin+0x41c/0x520 [ext4 4c370ef18dc92096340e0c399349e782617d846c]
Apr 29 00:58:14 ArchDesktop kernel:  create_empty_buffers+0x1d/0xb0
Apr 29 00:58:14 ArchDesktop kernel:  folio_alloc_buffers+0xee/0x230
Apr 29 00:58:14 ArchDesktop kernel:  ? folio_alloc_buffers+0xee/0x230
Apr 29 00:58:14 ArchDesktop kernel:  ? kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:14 ArchDesktop kernel:  ? asm_exc_general_protection+0x26/0x30
Apr 29 00:58:14 ArchDesktop kernel:  ? exc_general_protection+0x388/0x4a0
Apr 29 00:58:14 ArchDesktop kernel:  ? die_addr+0x128/0x130
Apr 29 00:58:14 ArchDesktop kernel:  <TASK>
Apr 29 00:58:14 ArchDesktop kernel: Call Trace:
Apr 29 00:58:14 ArchDesktop kernel: PKRU: 55555554
Apr 29 00:58:14 ArchDesktop kernel: CR2: 00007fae5030cb80 CR3: 00000005ab238000 CR4: 0000000000f50ef0
Apr 29 00:58:14 ArchDesktop kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Apr 29 00:58:14 ArchDesktop kernel: FS:  000074a9583b8080(0000) GS:ffff899c7edc0000(0000) knlGS:0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: R13: ffff899180245500 R14: 0000000000000068 R15: 1293823692cd282f
Apr 29 00:58:14 ArchDesktop kernel: R10: 0000000000000001 R11: ffff899caf37bd80 R12: 0000000000408d40
Apr 29 00:58:14 ArchDesktop kernel: RBP: ffff9db855d07a58 R08: 0000000000000001 R09: 0000000000000000
Apr 29 00:58:14 ArchDesktop kernel: RDX: 00000000671fb80f RSI: 000000000003b580 RDI: ffff89988cf8e3c0
Apr 29 00:58:14 ArchDesktop kernel: RAX: 1293823692cd285f RBX: 5247cd920044d7d0 RCX: 0000000000000001
Apr 29 00:58:14 ArchDesktop kernel: RSP: 0018:ffff9db855d07a20 EFLAGS: 00010206
Apr 29 00:58:14 ArchDesktop kernel: Code: 08 48 83 78 10 00 4c 8b 38 0f 84 ab 01 00 00 4d 85 ff 0f 84 a2 01 00 00 41 8b 45 28 49 8b 9d b8 00 00 00 49 8b 75 00 4c 01 f8 <48> 33 18 48 89 c1 4c 89 f8 48 0f c9 48 31 cb 48 8d 8a 00 02 00 00
Apr 29 00:58:14 ArchDesktop kernel: RIP: 0010:kmem_cache_alloc+0xc2/0x450
Apr 29 00:58:14 ArchDesktop kernel: Hardware name: System manufacturer System Product Name/ROG STRIX X570-F GAMING, BIOS 5003 10/07/2023
Apr 29 00:58:14 ArchDesktop kernel: CPU: 15 PID: 1729951 Comm: systemd-coredum Tainted: G           OE      6.8.4-zen1-1-zen #1 4a88f2661038c2a3bb69aa70fb41a5735338823c
Apr 29 00:58:14 ArchDesktop kernel: general protection fault, probably for non-canonical address 0x1293823692cd285f: 0000 [#1] PREEMPT SMP NOPTI
Apr 29 00:58:13 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:13 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:13 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:13 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:13 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:13 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:13 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:13 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:13 ArchDesktop sudo[1732634]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:13 ArchDesktop sudo[1732634]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:13 ArchDesktop sudo[1732574]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:12 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:12 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:11 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:11 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:11 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:11 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:11 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:11 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:11 ArchDesktop sudo[1732574]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:11 ArchDesktop sudo[1732574]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:11 ArchDesktop sudo[1732373]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:10 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:10 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:10 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:10 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:10 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:10 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:10 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:10 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:10 ArchDesktop sudo[1732373]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:10 ArchDesktop sudo[1732373]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:10 ArchDesktop sudo[1732241]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:09 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:09 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:08 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:08 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:08 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:08 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:08 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:08 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:08 ArchDesktop sudo[1732241]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:08 ArchDesktop sudo[1732241]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:08 ArchDesktop sudo[1732176]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:07 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:07 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:07 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:07 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:07 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:07 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:07 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:07 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:07 ArchDesktop sudo[1732176]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:07 ArchDesktop sudo[1732176]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:07 ArchDesktop sudo[1732037]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:06 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:06 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:05 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:05 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:05 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:05 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:05 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:05 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop sudo[1732037]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:05 ArchDesktop sudo[1732037]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop sudo[1731333]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:05 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: Failed to spawn the underlying wsdd daemon.
Apr 29 00:58:05 ArchDesktop gvfsd-wsdd[1731771]: Failed to spawn the wsdd daemon: Failed to execute child process “wsdd” (No such file or directory)
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:04 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:04 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:04 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:04 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop sudo[1731333]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:04 ArchDesktop sudo[1731333]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:04 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:04 ArchDesktop sudo[1730715]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: Failed to spawn the underlying wsdd daemon.
Apr 29 00:58:03 ArchDesktop gvfsd-wsdd[1731296]: Failed to spawn the wsdd daemon: Failed to execute child process “wsdd” (No such file or directory)
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:03 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:03 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: Failed to spawn the underlying wsdd daemon.
Apr 29 00:58:02 ArchDesktop gvfsd-wsdd[1730857]: Failed to spawn the wsdd daemon: Failed to execute child process “wsdd” (No such file or directory)
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:02 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:02 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop kernel: [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Apr 29 00:58:02 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop sudo[1730715]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:02 ArchDesktop sudo[1730715]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop sudo[1730017]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:02 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: Failed to spawn the underlying wsdd daemon.
Apr 29 00:58:02 ArchDesktop gvfsd-wsdd[1730551]: Failed to spawn the wsdd daemon: Failed to execute child process “wsdd” (No such file or directory)
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset(52) succeeded!
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow done
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: recover vram bo from shadow start
Apr 29 00:58:01 ArchDesktop kernel: [drm] kiq ring mec 3 pipe 1 q 0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          RW: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MAPPING_ERROR: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          WALKER_ERROR: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MORE_FAULTS: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          RW: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MAPPING_ERROR: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          PERMISSION_FAULTS: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          WALKER_ERROR: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MORE_FAULTS: 0x0
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          Faulty UTCL2 client ID: CB/DB (0x0)
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          RW: 0x1
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MAPPING_ERROR: 0x1
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          PERMISSION_FAULTS: 0x5
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          WALKER_ERROR: 0x1
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          MORE_FAULTS: 0x1
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:          Faulty UTCL2 client ID: CPC (0x5)
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0, for process  pid 0 thread  pid 0)
Apr 29 00:58:01 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: IP block:gfx_v11_0 is hung!
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:01 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-wsdd[1730225]: Failed to spawn the wsdd daemon: Failed to execute child process “wsdd” (No such file or directory)
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop sudo[1730017]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:58:00 ArchDesktop sudo[1730017]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:58:00 ArchDesktop sudo[1729509]: pam_unix(sudo:session): session closed for user root
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop systemd[1]: Started Process Core Dump (PID 1729924/UID 0).
Apr 29 00:58:00 ArchDesktop systemd[1]: Started Process Core Dump (PID 1729925/UID 0).
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: GPU reset begin!
Apr 29 00:58:00 ArchDesktop kernel: amdgpu: Failed to evict process queues
Apr 29 00:58:00 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: Failed to evict queue 1
Apr 29 00:58:00 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: MES might be in unrecoverable state, issue a GPU reset
Apr 29 00:58:00 ArchDesktop kernel: amdgpu 0000:0f:00.0: amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Apr 29 00:58:00 ArchDesktop kernel: [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:58:00 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: Failed to spawn the underlying wsdd daemon.
Apr 29 00:57:59 ArchDesktop gvfsd-wsdd[1729737]: Failed to spawn the wsdd daemon: Failed to execute child process “wsdd” (No such file or directory)
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop sudo[1729509]: pam_unix(sudo:session): session opened for user root(uid=0) by disty(uid=1000)
Apr 29 00:57:59 ArchDesktop sudo[1729509]:    disty : TTY=pts/8 ; PWD=/home/disty ; USER=root ; COMMAND=/usr/bin/xpu-smi stats -d 0
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop sudo[1728972]: pam_unix(sudo:session): session closed for user root
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop gvfsd-network[1708472]: Couldn't create directory monitor on wsdd:///. Error: Automount failed: mountpoint for org.gtk.vfs.mountpoint_wsdd already running
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
Apr 29 00:57:59 ArchDesktop kernel: [drm] Skip scheduling IBs!
```

</details>


---

### 评论 #35 — galister (2024-05-19T13:31:18Z)

I've switched my desktop to use the iGPU (7800X3D) and it seems like the driver doesn't hang anymore, as long as PyTorch is the only thing using the XTX.

Edit: I also forced the iGPU to be the primary graphics device via BIOS and plugged all displays into mobo.

ROCm 6.1 in an Ubuntu 22.04 distrobox under Gentoo with `torch-2.4.0.dev20240518+rocm6.1`

Edit: 2 days later, no sign of issue

---

### 评论 #36 — hartmark (2024-08-18T23:55:05Z)

I still get this error. Especially with Stable Diffusion generation with FLUX. Is there any update on this issue?

I have this hardware:
AMD Ryzen 9 5900X 12-Core
32 GB RAM
AMD 7800 XT 16 GB VRAM

I have gotten it to hang consistently 6 times in row now.

I have created a docker image for ComfyUI.
1. https://github.com/hartmark/sd-rocm
2. follow instructions for installing this workflow: https://www.reddit.com/r/StableDiffusion/comments/1euz2a9/comment/lio2fte/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
3. just generate and it will hang.

journal:
[journalctl.txt](https://github.com/user-attachments/files/16653263/journalctl.txt)


---

### 评论 #37 — Disty0 (2024-08-19T00:02:04Z)

Use Linux 6.10, I am using it sine 6.10-rc4 and no crash so far.

---

### 评论 #38 — hartmark (2024-08-19T10:08:54Z)

> Use Linux 6.10, I am using it sine 6.10-rc4 and no crash so far.

Arch linux is at 6.10 already:
```
% uname -a
Linux bernard 6.10.5-arch1-1 #1 SMP PREEMPT_DYNAMIC Thu, 15 Aug 2024 00:25:30 +0000 x86_64 GNU/Linux
```


---

### 评论 #39 — AlexLJordan (2025-04-07T21:50:46Z)

Hello, I'm observing this issue on my 7940HS w/ Radeon 780M Graphics.
Any time I'm using compute (via OpenCL, i think?), I run a gamble that my whole system locks up. Or sometimes when Steam is running the background for a while, weirdly.

The only way I've found to recover is external ssh login to kill the compute-using program and restart my display manager.

I'm on this kernel: 
`Linux 6.6.77-rt50 #1-NixOS SMP PREEMPT_RT Tue Feb 11 08:37:33 UTC 2025` on Nixos 24.11.

Is the Kernel update to 6.10+ known to fix the MES crash?

---

### 评论 #40 — AlexLJordan (2025-04-14T13:07:01Z)

I now switched to `Linux 6.12.16 #1-NixOS SMP PREEMPT_DYNAMIC Fri Feb 21 13:01:47 UTC 2025`

My theory after observing the issue **was**, that if I do something engaging OpenCL _and_ some kind of rendering task (like playing a video) at the same time, the crash occurs.

On 6.12, at first I was unable to reproduce the issue, but then, while doing something else GPU intensive, I experienced the crash again.

After this first instance of the crash, it didn't happen again.

**A log before switching to 6.12:**

[gpu-crash2.log](https://github.com/user-attachments/files/19735837/gpu-crash2.log)

**Todays log after switching to 6.12:**

[6_12-crash.log](https://github.com/user-attachments/files/19735843/6_12-crash.log)

---

### 评论 #41 — Disty0 (2025-04-14T15:46:44Z)

Try 6.13 or 6.14.
6.12 still crashes after 3~ days of uptime for me. 6.13 can go on for a few weeks.
I am using an RX 7900 XTX.

---

### 评论 #42 — futursolo (2025-10-15T10:50:34Z)

I have also been observing this error with my Radeon Pro W7900, which happened with both Ryzen 3700X and EPYC 7C13.

Symptoms with my setup: error messages in dmesg, GPU reset, random hangs (no generation from program, cannot poweroff normally)

Things I have tried: Debian / Ubuntu, 6.12 / 6.14, with/without amdgpu-dkms, turn off ASPM, etc.
The relatively stable setting I have settled with are: Ubuntu HWE (6.14), dkms, no ASPM.

Like the comment above, I can run for a couple weeks without crashing.

After that, I switched to an i9-13900K which I retired from my primary PC for about 1 month and I haven’t observed any gpu crashes or amdgpu related errors in dmesg, which I observe on a regular basis with the previous 2 AMD setups even without it crashing.

I am not confident that this is the only factor since I have also upgraded to ROCm 7.0 when it came out.

Hope this helps with the investigation.

---
