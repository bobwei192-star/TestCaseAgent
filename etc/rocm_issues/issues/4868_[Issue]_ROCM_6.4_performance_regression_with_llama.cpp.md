# [Issue]: ROCM 6.4 performance regression with llama.cpp

> **Issue #4868**
> **状态**: closed
> **创建时间**: 2025-06-01T04:52:33Z
> **更新时间**: 2025-07-14T18:42:53Z
> **关闭时间**: 2025-07-14T18:42:52Z
> **作者**: adriablo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4868

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

ROCM 6.4 inference with llama.cpp is 10x slower than ROCM 6.3 (!)
You may have to run it a few times until it becomes super slow.
There are no warnings or errors.
eg with Meta-Llama-3-8B.Q4_K_M.gguf
expected: 80 token/sec
actual: 12 token/sec

### Operating System

Ubuntu 24.04.2

### CPU

AMD Ryzen Threadripper 3970X

### GPU

2x Radeon 7900 XTX

### ROCm Version

ROCm 6.4

### ROCm Component

_No response_

### Steps to Reproduce

`llama-bench -m Meta-Llama-3-8B.Q4_K_M.gguf`

You may have to run it a few times until it becomes super slow.
Both ROCm and Vulkan llama.cpp have this issue.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (14 条)

### 评论 #1 — adriablo (2025-06-02T03:14:06Z)

It's the driver, and it's happening with ROCm 3 too!

Normal speed:
```
llama-bench  -m Meta-Llama-3-8B.Q4_K_M.gguf
ggml_vulkan: Found 2 Vulkan devices:
ggml_vulkan: 0 = Radeon RX 7900 XTX (AMD open-source driver) | uma: 0 | fp16: 1 | warp size: 64 | shared memory: 32768 | int dot: 1 | matrix cores: KHR_coopmat
ggml_vulkan: 1 = Radeon RX 7900 XTX (AMD open-source driver) | uma: 0 | fp16: 1 | warp size: 64 | shared memory: 32768 | int dot: 1 | matrix cores: KHR_coopmat
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | Vulkan,RPC |  99 |           pp512 |      1486.90 ± 14.33 |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | Vulkan,RPC |  99 |           tg128 |         81.88 ± 0.08 |
```

After a while, it slows down almost 10x:
```
llama-bench  -m Meta-Llama-3-8B.Q4_K_M.gguf
ggml_vulkan: Found 2 Vulkan devices:
ggml_vulkan: 0 = Radeon RX 7900 XTX (AMD open-source driver) | uma: 0 | fp16: 1 | warp size: 64 | shared memory: 32768 | int dot: 1 | matrix cores: KHR_coopmat
ggml_vulkan: 1 = Radeon RX 7900 XTX (AMD open-source driver) | uma: 0 | fp16: 1 | warp size: 64 | shared memory: 32768 | int dot: 1 | matrix cores: KHR_coopmat
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | Vulkan,RPC |  99 |           pp512 |       1263.88 ± 5.66 |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | Vulkan,RPC |  99 |           tg128 |         16.55 ± 0.01 |
```

**If I unload and then reload the amdgpu module, the issue is fixed - for a while:**
```
sudo rmmod amdgpu
sudo modprobe amdgpu
```

```
modinfo amdgpu                                                                                                    
filename:       /lib/modules/6.11.0-26-generic/updates/dkms/amdgpu.ko.zst                                                                    
version:        6.10.5      

```

Installed with: amdgpu-install_6.3.60304-1_all.deb

Kernel
 6.11.0-26-generic #26~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Apr 17 19:20:47 UTC 2 x86_64 x86_64 x86_64 GNU/Linux




---

### 评论 #2 — adriablo (2025-06-02T03:14:40Z)

https://github.com/ROCm/rocm-install-on-linux/issues/478

---

### 评论 #3 — ppanchad-amd (2025-06-02T14:03:10Z)

Hi @adriablo. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #4 — adriablo (2025-06-08T01:57:46Z)

amd_gpu is crashing on load, 100% of the time!
This is after installing with amdgpu-install_6.4.60401-1_all.deb :

Driver version:
> modinfo amdgpu | grep version
version:        6.12.12
srcversion:     9AB0277171A464F184AFEF4
vermagic:       6.11.0-26-generic SMP preempt mod_unload modversions 

Crash log:
> [26043.481971] [drm] Initialized amdgpu 3.63.0 for 0000:23:00.0 on minor 0
[26043.488796] ------------[ cut here ]------------                 
[26043.488798] WARNING: CPU: 16 PID: 81086 at /tmp/amd.h5ddwgbV/amd/amdgpu/../display/dc/core/dc_resource.c:3630 calculate_phy_pix_clks+0xef/
0x100 [amdgpu]                                                        
[26043.489264] Modules linked in: amdgpu(OE+) dm_crypt qrtr cmac algif_hash algif_skcipher af_alg bnep binfmt_misc snd_hda_codec_hdmi nls_iso
8859_1 snd_hda_intel snd_usb_audio snd_intel_dspcfg snd_intel_sdw_acpi snd_hda_codec snd_usbmidi_lib snd_hda_core snd_ump mc snd_hwdep btusb 
snd_pcm btrtl btintel amd_atl intel_rapl_msr btbcm snd_seq_midi intel_rapl_common btmtk snd_seq_midi_event snd_rawmidi ee1004 bluetooth snd_s
eq snd_seq_device edac_mce_amd snd_timer rapl wmi_bmof snd ccp i2c_piix4 soundcore mxm_wmi k10temp i2c_smbus joydev mac_hid sch_fq_codel msr 
parport_pc ppdev lp parport efi_pstore nfnetlink dmi_sysfs ip_tables x_tables autofs4 mlx4_ib ib_uverbs ib_core mlx4_en hid_generic usbhid hi
d amddrm_ttm_helper(OE) amdttm(OE) amddrm_buddy(OE) amdxcp(OE) drm_exec drm_suballoc_helper uas amd_sched(OE) crct10dif_pclmul amdkcl(OE) usb
_storage crc32_pclmul drm_display_helper polyval_clmulni polyval_generic cec ghash_clmulni_intel sha256_ssse3 rc_core sha1_ssse3 igb mlx4_cor
e video nvme ahci drm_ttm_helper i2c_algo_bit
[26043.489320]  libahci dca ttm xhci_pci nvme_core xhci_pci_renesas nvme_auth wmi aesni_intel crypto_simd cryptd [last unloaded: amdgpu(OE)]
[26043.489329] CPU: 16 UID: 0 PID: 81086 Comm: modprobe Tainted: G        W  OE      6.11.0-26-generic #26~24.04.1-Ubuntu
[26043.489333] Tainted: [W]=WARN, [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
[26043.489333] Hardware name: Micro-Star International Co., Ltd. MS-7C60/TRX40 PRO 10G (MS-7C60), BIOS 1.80 05/17/2022
[26043.489335] RIP: 0010:calculate_phy_pix_clks+0xef/0x100 [amdgpu]
[26043.489732] Code: ab aa aa aa c1 e1 04 48 0f af ca 48 c1 e9 24 eb a3 8d 14 f6 8d 0c 95 00 00 00 00 ba ab aa aa aa 48 0f af ca 48 c1 e9 24 
eb 8a <0f> 0b eb 86 66 66 2e 0f 1f 84 00 00 00 00 00 66 90 90 90 90 90 90
[26043.489734] RSP: 0018:ffffac0094edb370 EFLAGS: 00010297
[26043.489736] RAX: ffff9bf948948000 RBX: ffff9bf948948000 RCX: 00000000005aa320
[26043.489738] RDX: 0000000000000005 RSI: 00000000002d5190 RDI: ffff9bf948948000
[26043.489739] RBP: ffffac0094edb370 R08: 0000000000000000 R09: 0000000000000000
[26043.489740] R10: 0000000000000000 R11: 0000000000000000 R12: ffff9bec54000000
[26043.489741] R13: ffff9bf3cfd7f200 R14: ffff9bf948948068 R15: ffff9bf68187b800
[26043.489743] FS:  0000774d1368f080(0000) GS:ffff9bfafe800000(0000) knlGS:0000000000000000
[26043.489744] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[26043.489745] CR2: 000064b540457cb0 CR3: 0000000e4a7cc000 CR4: 0000000000350ef0
[26043.489747] Call Trace:
[26043.489749]  <TASK>
[26043.489752]  ? show_regs+0x6c/0x80
[26043.489756]  ? __warn+0x88/0x140
[26043.489758]  ? calculate_phy_pix_clks+0xef/0x100 [amdgpu]
[26043.490150]  ? report_bug+0x182/0x1b0
[26043.490155]  ? handle_bug+0x6e/0xb0
[26043.490158]  ? exc_invalid_op+0x18/0x80
[26043.490160]  ? asm_exc_invalid_op+0x1b/0x20
[26043.490164]  ? calculate_phy_pix_clks+0xef/0x100 [amdgpu]
[26043.490563]  dc_validate_stream+0x48/0xf0 [amdgpu]
[26043.490954]  create_validate_stream_for_sink+0x26f/0x470 [amdgpu]
[26043.491371]  amdgpu_dm_connector_mode_valid+0x65/0x200 [amdgpu]
[26043.491792]  drm_connector_mode_valid+0x4b/0x90
[26043.491796]  __drm_helper_update_and_validate+0x14b/0x460                                                               18:37:33 [93/1845]
[26043.491799]  ? amdgpu_dm_connector_get_modes+0x172/0x500 [amdgpu]
[26043.492215]  drm_helper_probe_single_connector_modes+0x2c5/0x750                                                                          
[26043.492219]  drm_client_modeset_probe+0x222/0x600                  
[26043.492224]  __drm_fb_helper_initial_config_and_unlock+0x2c/0x160                                                                         
[26043.492226]  drm_fb_helper_initial_config+0x3d/0x50                                                                                       
[26043.492229]  drm_fbdev_ttm_client_hotplug+0x7a/0xd0 [drm_ttm_helper]                                                                      
[26043.492232]  drm_client_register+0x66/0xb0                                                                                                
[26043.492234]  drm_fbdev_ttm_setup+0x101/0x180 [drm_ttm_helper]                                                                             
[26043.492237]  amdgpu_pci_probe+0x54d/0x680 [amdgpu]                                                                                        
[26043.492560]  local_pci_probe+0x47/0xb0                                                                                                    
[26043.492564]  pci_call_probe+0x55/0x1a0    
[26043.492567]  pci_device_probe+0x84/0x120                                                                                                  
[26043.492570]  really_probe+0xf1/0x3c0                                                                                                      
[26043.492574]  __driver_probe_device+0x8c/0x180                     
[26043.492577]  driver_probe_device+0x24/0xd0                                                                                                
[26043.492580]  __driver_attach+0x10b/0x210                        
[26043.492583]  ? __pfx___driver_attach+0x10/0x10                                                                                            
[26043.492585]  bus_for_each_dev+0x8d/0xf0                                                                                                   
[26043.492588]  driver_attach+0x1e/0x30                   
[26043.492590]  bus_add_driver+0x14e/0x290                                                                                                   
[26043.492592]  driver_register+0x5e/0x130                                                                                                   
[26043.492595]  ? __pfx_amdgpu_init+0x10/0x10 [amdgpu]                                                                                       
[26043.492914]  __pci_register_driver+0x5e/0x70                                                                                              
[26043.492917]  amdgpu_init+0xb8/0xff0 [amdgpu]                                                                                              
[26043.493233]  do_one_initcall+0x5e/0x340                                                                                                   
[26043.493237]  do_init_module+0x97/0x2c0                       
[26043.493240]  load_module+0x6b5/0x7d0                                                                                                      
[26043.493242]  init_module_from_file+0x96/0x100
[26043.493246]  idempotent_init_module+0x11c/0x310
[26043.493249]  __x64_sys_finit_module+0x64/0xd0
[26043.493251]  x64_sys_call+0x2580/0x25f0
[26043.493254]  do_syscall_64+0x7e/0x170                    
[26043.493256]  ? syscall_exit_to_user_mode+0x4e/0x250
[26043.493259]  ? do_syscall_64+0x8a/0x170
[26043.493261]  ? syscall_exit_to_user_mode+0x4e/0x250
[26043.493262]  ? do_syscall_64+0x8a/0x170    
[26043.493265]  ? __do_sys_newfstatat+0x44/0x90             
[26043.493269]  ? syscall_exit_to_user_mode+0x4e/0x250
[26043.493271]  ? do_syscall_64+0x8a/0x170                          
[26043.493273]  ? syscall_exit_to_user_mode+0x4e/0x250            
[26043.493275]  ? do_syscall_64+0x8a/0x170
[26043.493277]  ? __x64_sys_openat+0x55/0xa0
[26043.493280]  ? syscall_exit_to_user_mode+0x4e/0x250
[26043.493281]  ? do_syscall_64+0x8a/0x170                                                                                                   
[26043.493284]  ? do_syscall_64+0x8a/0x170                            
[26043.493286]  ? do_syscall_64+0x8a/0x170                                                                                                   
[26043.493288]  ? syscall_exit_to_user_mode+0x4e/0x250                                                                                       
[26043.493289]  ? do_syscall_64+0x8a/0x170                                                                                                   
[26043.493292]  ? do_syscall_64+0x8a/0x170                                                                                                   
[26043.493294]  entry_SYSCALL_64_after_hwframe+0x76/0x7e                                                                                     
[26043.493296] RIP: 0033:0x774d12d2725d                                                                                                      
[26043.493299] Code: ff c3 66 2e 0f 1f 84 00 00 00 00 00 90 f3 0f 1e fa 48 89 f8 48 89 f7 48 89 d6 48 89 ca 4d 89 c2 4d 89 c8 4c 8b 4c 24 08 
0f 05 <48> 3d 01 f0 ff ff 73 01 c3 48 8b 0d 8b bb 0d 00 f7 d8 64 89 01 48
[26043.493300] RSP: 002b:00007ffdb4506ca8 EFLAGS: 00000246 ORIG_RAX: 0000000000000139                                                        
[26043.493302] RAX: ffffffffffffffda RBX: 0000595512b83140 RCX: 0000774d12d2725d                                                             
[26043.493303] RDX: 0000000000000004 RSI: 000059550b159e52 RDI: 0000000000000003
[26043.493304] RBP: 00007ffdb4506d60 R08: 0000000000000040 R09: 00007ffdb4506cf0                                                             
[26043.493305] R10: 0000774d12e03b20 R11: 0000000000000246 R12: 000059550b159e52
[26043.493306] R13: 0000000000040000 R14: 0000595512b83270 R15: 0000000000000000                                                             
[26043.493308]  </TASK>                                                                                                                      
[26043.493309] ---[ end trace 0000000000000000 ]---       


---

### 评论 #5 — zichguan-amd (2025-06-09T20:23:05Z)

Hi @adriablo, how long does it take for the slow down to show up? On 6.4.1 with
```
$ modinfo amdgpu | grep version
version:        6.12.12
srcversion:     9AB0277171A464F184AFEF4
vermagic:       6.8.0-41-generic SMP preempt mod_unload modversions 
```
I've let the tests ran for over 10min on 10s interval and the max I got is
```
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 XTX, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | ROCm       |  99 |           pp512 |      2970.46 ± 17.54 |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | ROCm       |  99 |           tg128 |         90.04 ± 0.08 |

build: 7f4fbe51 (5616)
```
while the slowest is
```
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 XTX, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | ROCm       |  99 |           pp512 |      2926.40 ± 12.39 |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | ROCm       |  99 |           tg128 |         89.81 ± 0.23 |

build: 7f4fbe51 (5616)
```
And it stabilizes around 2935 for pp512 and 90 for tg128. 

---

### 评论 #6 — adriablo (2025-06-09T20:31:59Z)

Thanks for looking at this.
It's pretty random, minutes or a couple of hours.  I noticed loading different models seemed to trigger it faster.
Also I am running 2 GPUs, the models are balanced across the 2 GPUs (2x 7900 XTX ASRock).

---

### 评论 #7 — khan-faiz (2025-06-10T15:24:37Z)

I'm getting very poor results on ROCm 6.4, this is on every run:

```
llama-bench -m meta-llama-3-8b.Q4_K_M.gguf
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 ROCm devices:
  Device 0: Radeon RX 7900 XTX, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | ROCm       |  99 |           pp512 |        114.36 ± 0.27 |
```
```
version:        6.12.12
srcversion:     9AB0277171A464F184AFEF4
vermagic:       6.11.0-26-generic SMP preempt mod_unload modversions 
```

---

### 评论 #8 — adriablo (2025-06-13T22:41:56Z)

I can reproduce even on 1 GPU  (_-sm none_) - after about 5 runs:

```
llama-bench -sm none  -m Llama3/Meta-Llama-3-8B.Q4_K_M.gguf
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 2 ROCm devices:
  Device 0: Radeon RX 7900 XTX, gfx1100 (0x1100), VMM: no, Wave Size: 32
  Device 1: Radeon RX 7900 XTX, gfx1100 (0x1100), VMM: no, Wave Size: 32
| model                          |       size |     params | backend    | ngl |    sm |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ----: | --------------: | -------------------: |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | ROCm       |  99 |  none |           pp512 |        249.29 ± 0.54 |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | ROCm       |  99 |  none |           tg128 |         11.28 ± 0.00 |
```

Every time I run it I get these messages in the kernel log:

```
[Jun13 15:37] workqueue: pm_runtime_work hogged CPU for >10000us 11 times, consider switching to WQ_UNBOUND
[Jun13 15:38] [drm] PCIE GART of 512M enabled (table at 0x00000085FEB00000).
[  +0.000073] amdgpu 0000:4c:00.0: amdgpu: PSP is resuming...
[  +0.060444] amdgpu 0000:4c:00.0: amdgpu: reserve 0x1300000 from 0x85fc000000 for PSP TMR
[  +0.146263] amdgpu 0000:4c:00.0: amdgpu: RAP: optional rap ta ucode is not available
[  +0.000002] amdgpu 0000:4c:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[  +0.000002] amdgpu 0000:4c:00.0: amdgpu: SMU is resuming...
[  +0.000004] amdgpu 0000:4c:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8000 (78.128.0)
[  +0.000003] amdgpu 0000:4c:00.0: amdgpu: SMU driver if version not matched
[  +0.185936] amdgpu 0000:4c:00.0: amdgpu: SMU is resumed successfully!
[  +0.008852] [drm] DMUB hardware initialized: version=0x07002D00
[  +0.006307] amdgpu 0000:4c:00.0: [drm] Cannot find any crtc or sizes
[  +0.000009] amdgpu 0000:4c:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  +0.000002] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring jpeg_dec uses VM inv eng 4 on hub 8
[  +0.000001] amdgpu 0000:4c:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 14 on hub 0
[  +0.004464] amdgpu 0000:4c:00.0: [drm] Cannot find any crtc or sizes
```



---

### 评论 #9 — adriablo (2025-06-15T19:02:39Z)

The issue is that the main GPU (GPU 0) enters a low-power mode after a while when the monitor/display enters a low-power mode (the monitor is plugged into the main GPU).
I use this machine remotely (ssh) - I do not use the display.
The only way to reset the GPU is to reload the amdgpu driver - after which the problem repeats.
In this low-power mode the GPU power cannot go over 150W, even though the max power limit for this GPU is 350W.  
The second GPU (GPU 1) is not affected.
The problem is solved by unplugging the monitor from GPU 0. This behavior is confirmed by experimenting, there is no indication in the (kernel) log.

I recommend disabling the GPU low-power mode when a compute load (ROCm/Vulkan) is detected, regardless of the display power status.  Also there should be some indication (log, amd-smi) when the GPU is stuck in this low-power mode, and a method to disable this behavior.

Btw, llama.cpp is faster on Vulkan vs ROCm.  7900 XTX speed is comparable to an Nvidia 3090 RTX.
Leaving this comment for future reference.

```
llama-bench -sm none -mg 0 -m Meta-Llama-3-8B.Q4_K_M.gguf
ggml_vulkan: Found 2 Vulkan devices:
ggml_vulkan: 0 = Radeon RX 7900 XTX (AMD open-source driver) | uma: 0 | fp16: 1 | warp size: 64 | shared memory: 32768 | int dot: 1 | matrix cores: KHR_coopmat
ggml_vulkan: 1 = Radeon RX 7900 XTX (AMD open-source driver) | uma: 0 | fp16: 1 | warp size: 64 | shared memory: 32768 | int dot: 1 | matrix cores: KHR_coopmat
| model                          |       size |     params | backend    | ngl |    sm |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ----: | --------------: | -------------------: |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | Vulkan,RPC |  99 |  none |           pp512 |      2110.00 ± 53.19 |
| llama 8B Q4_K - Medium         |   4.58 GiB |     8.03 B | Vulkan,RPC |  99 |  none |           tg128 |        103.50 ± 0.97 |

build: 053b1539 (5558)
```


---

### 评论 #10 — zichguan-amd (2025-06-16T14:36:00Z)

Hi @adriablo, thanks for the detailed update. This looks related to https://github.com/ROCm/ROCm/issues/4134 and https://github.com/ROCm/ROCm/issues/4226. Can you provide a full dmesg log when this happens?

---

### 评论 #11 — zichguan-amd (2025-06-16T15:07:35Z)

Please also try https://github.com/ROCm/ROCm/issues/4878#issuecomment-2940197516. rocm-smi gives some level of indication for when this happens, it should throw proper warnings in future releases (see https://github.com/ROCm/rocm_smi_lib/commit/2630bf0a8c2ce64b76a6a258efadc523fbada768)

---

### 评论 #12 — adriablo (2025-06-22T03:13:38Z)

It took over 1hr for this to happen again.  Only the main GPU is affected (GPU 0).  GPU 1 runs at normal speed.

device/power/runtime_status seems unrelated:

cat /sys/class/drm/card1/device/power/runtime_status
active

cat /sys/class/drm/card2/device/power/runtime_status
active

Kernel log:
[dmesg.txt](https://github.com/user-attachments/files/20850932/dmesg.txt)

Note that unplugging the display fixes the issue with GPU 0
kernel messages from unplug:
```
Jun21 20:20] workqueue: dm_irq_work_func [amdgpu] hogged CPU for >10000us 19 times, consider switching to WQ_UNBOUND
[  +0.247399] amdgpu 0000:23:00.0: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
[  +0.253081] amdgpu 0000:23:00.0: [drm] *ERROR* dc_dmub_srv_log_diagnostic_data: DMCUB error - collecting diagnostic data
```

---

### 评论 #13 — zichguan-amd (2025-07-04T19:26:40Z)

Hi @adriablo, after some testing with 2x 7900XTX, one connected to a display, on ROCm 6.4.1, Ubuntu 22.04.4. I still could not repro the power being capped when the display goes to sleep. 
`device/power/runtime_status` should remain active as long as the card is connected to a display, even if the display is off. The other card that's not connected to a display will be suspended if there's no ROCm activity, the kernel logs about `PSP resuming` should be the suspended card waking up every time you start a llama workload. So, if your GPU 0 always remains active, it shouldn't be going into a low power state set by driver.
Do you see any change in `Perf` or `PwrCap` from `rocm-smi`? Also does the same happen if you connect the other GPU to the display?

---

### 评论 #14 — zichguan-amd (2025-07-14T18:42:52Z)

Closing the issue since there's a workaround and I can't reproduce it. Feel free to comment if you have any additional concerns.

---
