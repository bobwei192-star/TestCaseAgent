# [Driver] WARNING: CPU: 2 PID: 479 at drivers/gpu/drm/amd/amdgpu/amdgpu_ttm.c:471 amdgpu_bo_move+0x261/0x2e0 [amdgpu]

> **Issue #2204**
> **状态**: open
> **创建时间**: 2023-06-01T03:53:55Z
> **更新时间**: 2023-11-10T16:26:16Z
> **作者**: geohot
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2204

## 描述

Just a rocm_bandwidth_test. 6.2.16-060216-generic

```
[   33.516854] WARNING: CPU: 2 PID: 479 at drivers/gpu/drm/amd/amdgpu/amdgpu_ttm.c:471 amdgpu_bo_move+0x261/0x2e0 [amdgpu]                                                                    
[   33.517190] Modules linked in: ipmi_ssif binfmt_misc nls_iso8859_1 intel_rapl_msr intel_rapl_common amd64_edac edac_mce_amd kvm_amd kvm irqbypass rapl wmi_bmof snd_hda_codec_hdmi snd_hda_
intel snd_intel_dspcfg snd_intel_sdw_acpi snd_hda_codec snd_hda_core snd_hwdep snd_pcm snd_timer joydev input_leds snd soundcore ccp ptdma k10temp acpi_ipmi ipmi_si ipmi_devintf ipmi_msghand
ler mac_hid sch_fq_codel dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua msr ramoops reed_solomon pstore_blk pstore_zone efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic raid10
 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear hid_generic cdc_ether usbhid usbnet hid mii amdgpu iommu_v2 drm_buddy 
gpu_sched video i2c_algo_bit drm_ttm_helper ttm drm_display_helper cec rc_core crct10dif_pclmul crc32_pclmul polyval_clmulni polyval_generic ghash_clmulni_intel drm_kms_helper sha512_ssse3 a
esni_intel syscopyarea sysfillrect crypto_simd                                                 
[   33.517271]  sysimgblt cryptd nvme ahci drm bnxt_en nvme_core libahci nvme_common xhci_pci i2c_piix4 xhci_pci_renesas wmi                                                                  
[   33.517285] CPU: 2 PID: 479 Comm: kworker/u64:29 Tainted: G        W          6.2.16-060216-generic #202305171336                                                                          
[   33.517290] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T/BCM, BIOS P3.50 07/19/2022                                                                                           
[   33.517292] Workqueue: kfd_restore_wq restore_process_worker [amdgpu]        
[   33.517719] RIP: 0010:amdgpu_bo_move+0x261/0x2e0 [amdgpu]                               
[   33.518035] Code: 7d c8 84 c0 74 0c 4c 89 e6 e8 1b cc ff ff 84 c0 75 62 48 c7 c7 60 5b fc c0 e8 1b ee 85 c6 e9 76 fe ff ff 0f 0b e9 47 fe ff ff <0f> 0b 41 bd ea ff ff ff e9 62 fe ff ff 83
 f8 02 75 87 41 8b 44 24                                                                       
[   33.518038] RSP: 0018:ffffb61bca21fb40 EFLAGS: 00010202                                     
[   33.518042] RAX: 0000000000000000 RBX: ffff8de00d515458 RCX: ffff8de00d971c00               
[   33.518044] RDX: ffffb61bca21fc30 RSI: 0000000000000000 RDI: 0000000000000001               
[   33.518046] RBP: ffffb61bca21fb80 R08: ffffb61bca21fbf0 R09: 0000000000000000
[   33.518048] R10: 0000000000000000 R11: 0000000000000000 R12: ffff8de038d1aa80
[   33.518050] R13: ffff8de00d515458 R14: 0000000000000000 R15: ffff8de056385550
[   33.518052] FS:  0000000000000000(0000) GS:ffff8def0e880000(0000) knlGS:0000000000000000
[   33.518054] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   33.518056] CR2: 0000564e59517e40 CR3: 000000010c80e005 CR4: 0000000000770ee0
[   33.518059] PKRU: 55555554                                                                  
[   33.518060] Call Trace:                                                                     
[   33.518062]  <TASK>                                                                         
[   33.518067]  ttm_bo_handle_move_mem+0xe5/0x1f0 [ttm] 
[   33.518082]  ttm_bo_validate+0xf6/0x140 [ttm]                                               
[   33.518095]  ? ttm_bo_validate+0x50/0x140 [ttm]                                             
[   33.518107]  kfd_mem_dmaunmap_attachment+0x1fc/0x220 [amdgpu]                               
[   33.518530]  amdgpu_amdkfd_gpuvm_restore_process_bos+0x49b/0x870 [amdgpu]                   
[   33.518944]  restore_process_worker+0x30/0x130 [amdgpu]                                     
[   33.519344]  process_one_work+0x225/0x430                                                   
[   33.519350]  worker_thread+0x50/0x3e0                                                       
[   33.519353]  ? __pfx_worker_thread+0x10/0x10                                                
[   33.519357]  kthread+0xe9/0x110                                                             
[   33.519362]  ? __pfx_kthread+0x10/0x10     
[   33.519367]  ret_from_fork+0x2c/0x50                                                        
[   33.519372]  </TASK> 
```

---

## 评论 (3 条)

### 评论 #1 — massivedynamics1 (2023-06-17T10:53:36Z)

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Thanks for connecting <a href="https://twitter.com/realGeorgeHotz?ref_src=twsrc%5Etfw">@realGeorgeHotz</a>. Appreciate the work you and tiny corp are doing. We are committed to working with the community and improving our support. More to come on ROCm on @radeon soon. Lots of work ahead but excited about what we can do together.</p>&mdash; Lisa Su (@LisaSu) <a href="https://twitter.com/LisaSu/status/1669848494637735936?ref_src=twsrc%5Etfw">June 16, 2023</a></blockquote>

---

### 评论 #2 — preda (2023-06-19T13:01:48Z)

What about trying to repro on a more recent kernel, such as 6.4.0-rc6, to see if the problem has been fixed in the meantime. Of course this could be the task of an AMD employee, to first repro the issue as reported (on 6.2.16), next attempt repro changing only one variable at a time (the linux kernel in this case), and then report here the result.


---

### 评论 #3 — kentrussell (2023-11-10T16:26:15Z)

Trying the ROCm 5.7.* releases should help, since those are tested against the 6.2 Ubuntu kernel. Can you give that a shot? 5.6.* was only tested against 5.x kernels, so 5.7 should hopefully get us past this bug.

---
