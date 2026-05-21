# [Driver] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:12 pasid:32773, for process rocm-bandwidth- pid 8285 thread rocm-bandwidth- pid 8285)                  

> **Issue #2205**
> **状态**: open
> **创建时间**: 2023-06-01T04:03:37Z
> **更新时间**: 2025-09-15T10:01:10Z
> **作者**: geohot
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2205

## 描述

More rocm-bandwidth-test in loops on 2 card machine.

Did `echo high > /sys/class/drm/cardN/device/power_dpm_force_performance_level` on both cards if it matters

```
[  196.550063] gmc_v11_0_process_interrupt: 19 callbacks suppressed                                                                                                                           
[  196.550067] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:12 pasid:32773, for process rocm-bandwidth- pid 8285 thread rocm-bandwidth- pid 8285)                  
[  196.550096] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f0000002000 from client 10                                                                                   
[  196.550110] amdgpu 0000:c3:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00C01A30                                                                                                        
[  196.550121] amdgpu 0000:c3:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA0 (0xd)                                                                                                          
[  196.550132] amdgpu 0000:c3:00.0: amdgpu:      MORE_FAULTS: 0x0                                                                                                                             
[  196.550141] amdgpu 0000:c3:00.0: amdgpu:      WALKER_ERROR: 0x0                                                                                                                            
[  196.550150] amdgpu 0000:c3:00.0: amdgpu:      PERMISSION_FAULTS: 0x3                                                                                                                       
[  196.550159] amdgpu 0000:c3:00.0: amdgpu:      MAPPING_ERROR: 0x0                                                                                                                           
[  196.550168] amdgpu 0000:c3:00.0: amdgpu:      RW: 0x0                                                                                                                                      
[  199.471215] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:9 pasid:32773, for process rocm-bandwidth- pid 8285 thread rocm-bandwidth- pid 8285)                   
[  199.471238] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f0000002000 from client 10                                                                                   
[  199.471251] amdgpu 0000:c3:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00901A30                                                                                                        
[  199.471260] amdgpu 0000:c3:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA0 (0xd)                                                                                                          
[  199.471270] amdgpu 0000:c3:00.0: amdgpu:      MORE_FAULTS: 0x0                                                                                                                             
[  199.471277] amdgpu 0000:c3:00.0: amdgpu:      WALKER_ERROR: 0x0                                                                                                                            
[  199.471285] amdgpu 0000:c3:00.0: amdgpu:      PERMISSION_FAULTS: 0x3                                                                                                                       
[  199.471293] amdgpu 0000:c3:00.0: amdgpu:      MAPPING_ERROR: 0x0                                                                                                                           
[  199.471300] amdgpu 0000:c3:00.0: amdgpu:      RW: 0x0                                                                                                                                      
[  202.939580] amdgpu 0000:c3:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:10 pasid:32773, for process rocm-bandwidth- pid 8285 thread rocm-bandwidth- pid 8285)                  
[  202.939615] amdgpu 0000:c3:00.0: amdgpu:   in page starting at address 0x00007f0000002000 from client 10                                                                                   
[  202.939631] amdgpu 0000:c3:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00A01C30                                                                                                        
[  202.939644] amdgpu 0000:c3:00.0: amdgpu:      Faulty UTCL2 client ID: SDMA1 (0xe)                                                                                                          
[  202.939657] amdgpu 0000:c3:00.0: amdgpu:      MORE_FAULTS: 0x0                                                                                                                             
[  202.939668] amdgpu 0000:c3:00.0: amdgpu:      WALKER_ERROR: 0x0                                                                                                                            
[  202.939678] amdgpu 0000:c3:00.0: amdgpu:      PERMISSION_FAULTS: 0x3                                                                                                                       
[  202.939690] amdgpu 0000:c3:00.0: amdgpu:      MAPPING_ERROR: 0x0                                                                                                                           
[  202.939700] amdgpu 0000:c3:00.0: amdgpu:      RW: 0x0                                                                                                                                      
[  203.051164] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=2                                                                       
[  203.051365] amdgpu: failed to add hardware queue to MES, doorbell=0x1a02                                                                                                                   
[  203.051374] amdgpu: MES might be in unrecoverable state, issue a GPU reset                                                                                                                 
[  203.051384] amdgpu: Failed to restore queue 0                                                                                                                                              
[  203.051391] amdgpu: Failed to restore process queues                                                                                                                                       
[  203.051394] amdgpu: Pasid 0x8002 destroy queue 0 failed, ret -5                                                                                                                            
[  203.051428] amdgpu: Failed to restore queues of pasid 0x8005                                                                                                                               
[  203.051575] amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!                                                                                                                                  
[  203.051590] amdgpu: Failed to evict queue 2                                                                                                                                                
[  203.058839] amdgpu 0000:c3:00.0: amdgpu: recover vram bo from shadow start                                                                                                                 
[  203.058866] amdgpu 0000:c3:00.0: amdgpu: recover vram bo from shadow done                                                                                                                  
[  203.074368] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14                                                                      
[  203.074565] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait                                                                                              
[  203.172303] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14                                                                      
[  203.172472] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait                                                                                              
[  203.188188] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14                                                                      
[  203.188338] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait                                                                                              
[  203.205376] ------------[ cut here ]------------                                                                                                                                           
[  203.205378] kernfs: can not remove 'size', no directory                                                                                                                                    
[  203.205385] WARNING: CPU: 12 PID: 1503 at fs/kernfs/dir.c:1651 kernfs_remove_by_name_ns+0xcf/0xe0                                                                                          
[  203.205392] Modules linked in: ipmi_ssif binfmt_misc nls_iso8859_1 intel_rapl_msr intel_rapl_common amd64_edac edac_mce_amd kvm_amd kvm irqbypass rapl snd_hda_codec_hdmi wmi_bmof snd_hda_
intel snd_intel_dspcfg snd_intel_sdw_acpi snd_hda_codec snd_hda_core snd_hwdep joydev input_leds snd_pcm snd_timer snd ccp soundcore ptdma k10temp acpi_ipmi ipmi_si ipmi_devintf ipmi_msghand
ler mac_hid sch_fq_codel dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua msr ramoops reed_solomon pstore_blk pstore_zone efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic raid10
 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear hid_generic cdc_ether usbhid usbnet hid mii amdgpu iommu_v2 drm_buddy 
gpu_sched video i2c_algo_bit drm_ttm_helper ttm drm_display_helper cec rc_core drm_kms_helper crct10dif_pclmul syscopyarea sysfillrect crc32_pclmul polyval_clmulni polyval_generic ghash_clmu
lni_intel sha512_ssse3 aesni_intel crypto_simd cryptd                                                                                                                                         
[  203.205447]  sysimgblt nvme drm ahci bnxt_en nvme_core libahci nvme_common xhci_pci i2c_piix4 xhci_pci_renesas wmi                                                                         
[  203.205456] CPU: 12 PID: 1503 Comm: kworker/12:3 Tainted: G        W          6.2.16-060216-generic #202305171336                                                                          
[  203.205458] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T/BCM, BIOS P3.50 07/19/2022                                                                                           
[  203.205460] Workqueue: kfd_process_wq kfd_process_wq_release [amdgpu]                                                                                                                      
[  203.205661] RIP: 0010:kernfs_remove_by_name_ns+0xcf/0xe0                                                                                                                                   
[  203.205663] Code: c3 ff 5b b8 fe ff ff ff 41 5c 41 5d 41 5e 5d 31 d2 31 f6 31 ff c3 cc cc cc cc 0f 0b eb 96 48 c7 c7 e8 25 96 91 e8 a1 c9 b9 ff <0f> 0b eb d4 66 66 2e 0f 1f 84 00 00 00 00
 00 66 90 90 90 90 90 90                                                                                                                                                                      
[  203.205665] RSP: 0018:ffffac2209b0bcf8 EFLAGS: 00010246                                                                                                                                    
[  203.205666] RAX: 0000000000000000 RBX: ffffffffc14e2d28 RCX: 0000000000000000                                                                                                              
[  203.205667] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000                                                                                                              
[  203.205668] RBP: ffffac2209b0bd18 R08: 0000000000000000 R09: 0000000000000000                                                                                                              
[  203.205668] R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000                                                                                                              
[  203.205669] R13: ffffffffc1221940 R14: ffffffffc13b7ed6 R15: dead000000000100                                                                                                              
[  203.205670] FS:  0000000000000000(0000) GS:ffff93d6ceb00000(0000) knlGS:0000000000000000                                                                                                   
[  203.205671] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033                                                                                                                              
[  203.205672] CR2: 00007f6416703c14 CR3: 0000000970a10002 CR4: 0000000000770ee0                                                                                                              
[  203.205673] PKRU: 55555554                                                                                                                                                                 
[  203.205674] Call Trace:                                                                                                                                                                    
[  203.205675]  <TASK>                                                                                                                                                                        
[  203.205679]  remove_files+0x30/0x70                                                                                                                                                        
[  203.205681]  sysfs_remove_group+0x3d/0x90                                                                                                                                                  
[  203.205683]  sysfs_remove_groups+0x2e/0x60                                                                                                                                                 
[  203.205685]  __kobject_del+0x20/0xe0                                                                                                                                                       
[  203.205688]  kobject_del+0x13/0x30                                                                                                                                                         
[  203.205690]  kfd_procfs_del_queue+0x1e/0x40 [amdgpu]                                                                                                                                       
[  203.205853]  pqm_uninit+0x7a/0xf0 [amdgpu]                                                                                                                                                 
[  203.206018]  kfd_process_wq_release+0x32/0x1e0 [amdgpu]                                                                                                                                    
[  203.206174]  ? __schedule+0x2b2/0x610                                                                                                                                                      
[  203.206178]  process_one_work+0x225/0x430                                                                                                                                                  
[  203.206182]  worker_thread+0x50/0x3e0                                                                                                                                                      
[  203.206183]  ? __pfx_worker_thread+0x10/0x10                                                                                                                                               
[  203.206184]  kthread+0xe9/0x110                                                                                                                                                            
[  203.206187]  ? __pfx_kthread+0x10/0x10                                                                                                                                                     
[  203.206189]  ret_from_fork+0x2c/0x50                                                                                                                                                       
[  203.206192]  </TASK>                                                                                                                                                                       
[  203.206192] ---[ end trace 0000000000000000 ]---                                                                                                                                           
[  203.206194] ------------[ cut here ]------------                                                                                                                                           
[  203.206194] kernfs: can not remove 'type', no directory    
```

---

## 评论 (3 条)

### 评论 #1 — massivedynamics1 (2023-06-17T10:53:29Z)

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Thanks for connecting <a href="https://twitter.com/realGeorgeHotz?ref_src=twsrc%5Etfw">@realGeorgeHotz</a>. Appreciate the work you and tiny corp are doing. We are committed to working with the community and improving our support. More to come on ROCm on @radeon soon. Lots of work ahead but excited about what we can do together.</p>&mdash; Lisa Su (@LisaSu) <a href="https://twitter.com/LisaSu/status/1669848494637735936?ref_src=twsrc%5Etfw">June 16, 2023</a></blockquote>

---

### 评论 #2 — Ethanscharlie (2025-02-04T01:59:28Z)

I'm having the same issue with retroarch

---

### 评论 #3 — mdx0111 (2025-09-15T10:01:09Z)

Probably late for the OP but in case it's happening for anyone else (as it was for me) and you haven't fixed it yet, you can try disabling the Mid Command Buffer Preemption via kernel parameters.
You can try this command to disable it for your AMD GPU:

```sudo grubby --update-kernel=ALL --args="amdgpu.mcbp=0```

Mid Command Buffer Preemption (MCBP) is a GPU scheduling feature that allows the graphics driver to interrupt and pause GPU work that's currently executing, then resume it later.

**How It Works:**
Command Buffers are sequences of GPU instructions (like "draw this triangle," "apply this shader," "copy this texture"). Normally, once a command buffer starts executing on the GPU, it runs to completion.

Preemption means the driver can:

- Interrupt a running command buffer mid-execution
- Save its current state
- Switch to execute a higher-priority command buffer
- Resume the original work later from where it left off
- Why It Exists:

**Without MCBP:**
If a low-priority task (like background rendering) is using the GPU, a high-priority task (like a video call) has to wait until the first task completely finishes. This can cause stuttering or lag.

**With MCBP:**
The driver can pause the background task, immediately handle the video call rendering, then resume the background work. This provides:

- Better responsiveness
- Smoother multitasking
- Lower latency for critical graphics operations 

**The Problem with AMD's Implementation:**
The AMD driver's MCBP implementation has bugs that cause memory protection faults when trying to save/restore GPU state during preemption. This leads to:

- Page faults (like in your log)
- GPU resets
- System crashes/freezes

**Why Disabling It Helps:**
Setting amdgpu.mcbp=0 forces the GPU to use traditional scheduling - tasks run to completion without interruption. While this might slightly reduce GPU multitasking efficiency, it eliminates the buggy preemption code that's crashing your system.

The trade-off is worth it because a slightly less optimal GPU schedule is infinitely better than constant crashes.

---
