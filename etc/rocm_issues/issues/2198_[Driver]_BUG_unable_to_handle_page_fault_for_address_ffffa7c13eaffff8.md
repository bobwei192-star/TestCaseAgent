# [Driver] BUG: unable to handle page fault for address: ffffa7c13eaffff8

> **Issue #2198**
> **状态**: closed
> **创建时间**: 2023-05-31T06:13:30Z
> **更新时间**: 2023-06-29T14:13:12Z
> **关闭时间**: 2023-06-29T14:13:12Z
> **作者**: geohot
> **标签**: Verified Issue, 5.5.0, 5.6.0
> **URL**: https://github.com/ROCm/ROCm/issues/2198

## 标签

- **Verified Issue** (颜色: #0052cc)
- **5.5.0** (颜色: #fbca04)
- **5.6.0** (颜色: #b60205)

## 描述

This one is the worst, only seems to occur when I put two GPUs in the system.

Sometime just happens, but easy to reproduce running https://github.com/RadeonOpenCompute/rocm_bandwidth_test

2x 7900XTX
ASROCK ROMED8-2T
EPYC 7662
Ubuntu 22.04, Kernel 6.2.14-060214-generic, ROCm 5.5

```
[   91.370818] BUG: unable to handle page fault for address: ffffa7c13eaffff8                              
[   91.370827] #PF: supervisor write access in kernel mode
[   91.370831] #PF: error_code(0x0002) - not-present page                                                  
[   91.370833] PGD 100000067 P4D 100000067 PUD 0                                                           
[   91.370838] Oops: 0002 [#1] PREEMPT SMP NOPTI
[   91.370842] CPU: 107 PID: 2937 Comm: rocm-bandwidth- Tainted: G        W  OE      6.2.14-060214-generic #202305010032                                                                                              
[   91.370847] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T, BIOS P3.50 07/19/2022            
[   91.370850] RIP: 0010:amdgpu_gmc_set_pte_pde+0x23/0x40 [amdgpu]                                         
[   91.371127] Code: 90 90 90 90 90 90 90 0f 1f 44 00 00 48 b8 00 f0 ff ff ff ff 00 00 55 48 21 c1 8d 04 d5 00 00 00 00 4c 09 c1 48 01 c6 48 89 e5 <48> 89 0e 31 c0 5d 31 d2 31 c9 31 f6 45 31 c0 e9 b9 38 ab c2 66 0f
[   91.371132] RSP: 0018:ffffa7b3ca3677c0 EFLAGS: 00010282                                                 
[   91.371136] RAX: 00000000fffffff8 RBX: 0000000000000000 RCX: 000300013c66f077                           
[   91.371139] RDX: 00000000ffffffff RSI: ffffa7c13eaffff8 RDI: ffff937f64980000                           
[   91.371142] RBP: ffffa7b3ca3677c0 R08: 0003000000000077 R09: ffffa7c03eb00000                                                                                                                                      
[   91.371145] R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000                           
[   91.371149] R13: ffff937f64980000 R14: ffff937f28d64ff0 R15: ffffa7c03eb00000                           
[   91.371152] FS:  00007f9121cd7780(0000) GS:ffff93bd4e8c0000(0000) knlGS:0000000000000000                
[   91.371156] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033                                           
[   91.371159] CR2: ffffa7c13eaffff8 CR3: 000000013ca36000 CR4: 0000000000350ee0                                                                                                                                      
[   91.371162] Call Trace:                                                                                 
[   91.371166]  <TASK>                                                                                                                                                                                                
[   91.371169]  amdgpu_gart_map+0x7c/0xc0 [amdgpu]                                                                                                                                                                    
[   91.371412]  amdgpu_gart_bind+0x1a/0x50 [amdgpu]                                                                                                                                                                   
[   91.371652]  amdgpu_ttm_gart_bind+0xa0/0xc0 [amdgpu]                                                                                                                                                               
[   91.371890]  amdgpu_ttm_recover_gart+0x5f/0x80 [amdgpu]                                                                                                                                                            
[   91.372128]  amdgpu_gtt_mgr_recover+0x46/0x80 [amdgpu]                                                                                                                                                             
[   91.372375]  gmc_v11_0_hw_init+0x29/0x100 [amdgpu]                                                                                                                                                                 
[   91.372637]  gmc_v11_0_resume+0x14/0x30 [amdgpu]                                                                                                                                                                   
[   91.372894]  amdgpu_device_ip_resume_phase1+0xe0/0x220 [amdgpu]                                                                                                                                                    
[   91.373129]  ? kgd2kfd_resume_iommu+0x4a/0x90 [amdgpu]                                                                                                                                                             
[   91.373410]  ? __pfx_pci_pm_runtime_resume+0x10/0x10                                                                                                                                                               
[   91.373417]  amdgpu_device_resume+0xb3/0x3b0 [amdgpu]                                                                                                                                                              
[   91.373654]  ? __pfx_pci_pm_runtime_resume+0x10/0x10                                                                                                                                                               
[   91.373658]  amdgpu_pmops_runtime_resume+0x84/0x100 [amdgpu]                 
[   91.373897]  pci_pm_runtime_resume+0xa3/0xf0                                                                                                                                                                       
[   91.373901]  __rpm_callback+0x50/0x170                                                                  
[   91.373906]  rpm_callback+0x6d/0x80                                                                     
[   91.373910]  ? __pfx_pci_pm_runtime_resume+0x10/0x10                         
[   91.373914]  rpm_resume+0x605/0x860                                                                     
[   91.373918]  __pm_runtime_resume+0x4e/0x80                                                              
[   91.373922]  amdgpu_driver_open_kms+0x54/0x250 [amdgpu]                      
[   91.374159]  drm_file_alloc+0x1a1/0x260 [drm]                                                           
[   91.374201]  drm_open_helper+0x6c/0x140 [drm]                                                           
[   91.374233]  ? drm_minor_acquire+0xb1/0x180 [drm]                                                       
[   91.374267]  drm_open+0x7f/0x170 [drm]
[   91.374299]  drm_stub_open+0xa9/0xe0 [drm]
[   91.374330]  chrdev_open+0xc5/0x240
[   91.374336]  ? fsnotify_perm.part.0+0x79/0x190
[   91.374341]  ? __pfx_chrdev_open+0x10/0x10
[   91.374344]  do_dentry_open+0x1f8/0x430
[   91.374348]  vfs_open+0x2d/0x40
[   91.374351]  do_open+0x200/0x4d0
[   91.374357]  ? open_last_lookups+0x8e/0x420
[   91.374361]  path_openat+0x135/0x2e0
[   91.374365]  ? mutex_lock+0x12/0x50
[   91.374370]  do_filp_open+0xaf/0x170
[   91.374377]  do_sys_openat2+0xbf/0x180
[   91.374380]  __x64_sys_openat+0x6c/0xa0
[   91.374384]  do_syscall_64+0x5b/0x90
[   91.374389]  ? exit_to_user_mode_prepare+0x30/0xb0
[   91.374396]  ? syscall_exit_to_user_mode+0x29/0x50
[   91.374400]  ? do_syscall_64+0x67/0x90
[   91.374403]  entry_SYSCALL_64_after_hwframe+0x72/0xdc
[   91.374409] RIP: 0033:0x7f91213146eb
[   91.374412] Code: 25 00 00 41 00 3d 00 00 41 00 74 4b 64 8b 04 25 18 00 00 00 85 c0 75 67 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 91 00 00 00 48 8b 54 24 28 64 48 2b 14 25
[   91.374418] RSP: 002b:00007fff42271880 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
[   91.374422] RAX: ffffffffffffffda RBX: 0000000000000002 RCX: 00007f91213146eb
[   91.374425] RDX: 0000000000080002 RSI: 00007fff42271900 RDI: 00000000ffffff9c
[   91.374428] RBP: 00007fff42271900 R08: 0000000000000000 R09: 00007fff42271695
[   91.374430] R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
[   91.374433] R13: 00007fff42271900 R14: 646e65725f6d7264 R15: 00007fff422719f0
[   91.374438]  </TASK>
[   91.374439] Modules linked in: joydev input_leds hid_generic usbhid hid xt_conntrack nft_chain_nat xt_MASQUERADE nf_nat nf_conntrack_netlink nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xfrm_user xfrm_algo xt_addr
type nft_compat nf_tables nfnetlink br_netfilter bridge stp llc overlay ipmi_ssif intel_rapl_msr intel_rapl_common amd64_edac edac_mce_amd kvm_amd mei_hdcp(OE) mei_pxp(OE) mei_iaf(OE) kvm irqbypass rapl binfmt_misc
 nls_iso8859_1 snd_hda_codec_hdmi snd_hda_intel snd_intel_dspcfg snd_intel_sdw_acpi snd_hda_codec snd_hda_core snd_hwdep mei_gsc(OE) snd_pcm mei_me(OE) snd_timer snd mei(OE) soundcore ccp acpi_ipmi ptdma k10temp ip
mi_si ipmi_devintf ipmi_msghandler mac_hid sch_fq_codel dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua msr ramoops pstore_blk reed_solomon pstore_zone efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic
 raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear cdc_ether usbnet mii
[   91.374506]  amdgpu i915 iommu_v2 gpu_sched drm_buddy video wmi i2c_algo_bit drm_ttm_helper ttm drm_display_helper cec rc_core drm_kms_helper syscopyarea sysfillrect sysimgblt nvme crct10dif_pclmul crc32_pclmul 
polyval_clmulni polyval_generic ghash_clmulni_intel sha512_ssse3 aesni_intel crypto_simd cryptd ahci nvme_core drm bnxt_en libahci xhci_pci nvme_common xhci_pci_renesas i2c_piix4
[   91.374557] CR2: ffffa7c13eaffff8
[   91.374560] ---[ end trace 0000000000000000 ]---
[   91.474884] RIP: 0010:amdgpu_gmc_set_pte_pde+0x23/0x40 [amdgpu]
[   91.475142] Code: 90 90 90 90 90 90 90 0f 1f 44 00 00 48 b8 00 f0 ff ff ff ff 00 00 55 48 21 c1 8d 04 d5 00 00 00 00 4c 09 c1 48 01 c6 48 89 e5 <48> 89 0e 31 c0 5d 31 d2 31 c9 31 f6 45 31 c0 e9 b9 38 ab c2 66 0f
[   91.475147] RSP: 0018:ffffa7b3ca3677c0 EFLAGS: 00010282
[   91.475151] RAX: 00000000fffffff8 RBX: 0000000000000000 RCX: 000300013c66f077
[   91.475154] RDX: 00000000ffffffff RSI: ffffa7c13eaffff8 RDI: ffff937f64980000
[   91.475157] RBP: ffffa7b3ca3677c0 R08: 0003000000000077 R09: ffffa7c03eb00000
[   91.475160] R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
[   91.475163] R13: ffff937f64980000 R14: ffff937f28d64ff0 R15: ffffa7c03eb00000
[   91.475166] FS:  00007f9121cd7780(0000) GS:ffff93bd4e8c0000(0000) knlGS:0000000000000000
[   91.475169] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[   91.475172] CR2: ffffa7c13eaffff8 CR3: 000000013ca36000 CR4: 0000000000350ee0
```

---

## 评论 (17 条)

### 评论 #1 — hkasivis (2023-05-31T16:15:15Z)

Is iommu is enabled? Would it be possible to test by adding iommu=off parameter in the Kernel command line? Thanks.

---

### 评论 #2 — geohot (2023-05-31T18:13:17Z)

It's off in both BIOS and on cmdline. I also fixed some PCI-E issues with `pcie_aspm=off` but it didn't fix this one.

```
tiny@tiny:~/tinygrad$ cat /proc/cmdline 
BOOT_IMAGE=/vmlinuz-6.2.14-060214-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro pcie_aspm=off amd_iommu=off
tiny@tiny:~/tinygrad$ sudo dmesg | grep -e DMAR -e IOMMU
[    3.962381] AMD-Vi: AMD IOMMUv2 functionality not available on this system - This is not a bug.
tiny@tiny:~/tinygrad$ ls -l /sys/kernel/iommu_*
total 0
tiny@tiny:~/tinygrad$
```


---

### 评论 #3 — geohot (2023-06-01T01:13:22Z)

Tried a different computer.
Clean Ubuntu 22.04, recommended 5.19.0-43-generic, ROCm 5.5 installed with your build script
2x 7900XTX
ASROCK ROMED8-2T
EPYC 7313

Might be different crash, I think this is the one that's fixed in the new kernel. But again, this is exactly your install instructions. Followed [https://docs.amd.com/bundle/ROCm-Installation-Guide-v5.5/page/Introduction_to_ROCm_Installation_Guide_for_Linux.html to a T. ](https://docs.amd.com/bundle/ROCm-Installation-Guide-v5.5/page/How_to_Install_ROCm.html#_How_to_Install) `sudo amdgpu-install --usecase=rocm`

```
[  369.214906] BUG: kernel NULL pointer dereference, address: 0000000000000130            
[  369.214926] #PF: supervisor read access in kernel mode              
[  369.214935] #PF: error_code(0x0000) - not-present page              
[  369.214943] PGD 0 P4D 0                                                                      
[  369.214950] Oops: 0000 [#1] PREEMPT SMP NOPTI                                                
[  369.214957] CPU: 31 PID: 3159 Comm: rocm-bandwidth- Tainted: G        W  OE     5.19.0-43-generic #44~22.04.1-Ubuntu                                                                         
[  369.214971] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T, BIOS P3.50 07/19/2022                                                                                                 
[  369.214980] RIP: 0010:pm_send_runlist+0x4a/0x6a0 [amdgpu]                                                                                                                                    
[  369.215126] Code: 30 65 48 8b 04 25 28 00 00 00 48 89 45 d0 31 c0 80 fb 01 0f 87 6d 1e 4b 00 83 e3 01 0f 85 64 05 00 00 49 8b 3f ba 01 00 00 00 <48> 8b 87 30 01 00 00 44 8b a7 6c 01 00 00 8
b 9f 70 01 00 00 44 8b                                                                                                                                                                          
[  369.215144] RSP: 0018:ffffb94da18f7b70 EFLAGS: 00010246                                                                                                                                      
[  369.215152] RAX: 0000000000000000 RBX: 0000000000000000 RCX: 0000000000000000                
[  369.215160] RDX: 0000000000000001 RSI: ffff980b8152cd58 RDI: 0000000000000000                                                                                                                
[  369.215169] RBP: ffffb94da18f7c00 R08: 0000000000000000 R09: 0000000000000000                
[  369.215177] R10: 0000000000000000 R11: ffff980ba9851040 R12: 0000000000000000                                                                                                                
[  369.215185] R13: ffff980b8cf76c00 R14: 0000000000000001 R15: ffff980b8152cce0               
[  369.215194] FS:  00007f40d90cd780(0000) GS:ffff981a8efc0000(0000) knlGS:0000000000000000                                                                                                     
[  369.215203] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033  
[  369.215211] CR2: 0000000000000130 CR3: 0000000152bfc005 CR4: 0000000000770ee0                                                                                                                
[  369.215221] PKRU: 55555554                                                                   
[  369.215225] Call Trace:                                                                      
[  369.215230]  <TASK>                                                                          
[  369.215236]  ? release_pages+0x155/0x670                                                     
[  369.215247]  map_queues_cpsch+0x7b/0xc0 [amdgpu]                                   
[  369.215370]  debug_map_and_unlock+0x57/0x90 [amdgpu]                               
[  369.215487]  debug_refresh_runlist+0x1f/0x30 [amdgpu]                              
[  369.215600]  kfd_dbg_runtime_disable+0x13c/0x250 [amdgpu]                                    
[  369.215718]  kfd_ioctl_dbg_set_debug_trap+0x6af/0x8e0 [amdgpu]                     
[  369.215835]  kfd_ioctl+0x3c8/0x520 [amdgpu]                                                                                                                                                  
[  369.215946]  ? kfd_mmap+0x2b0/0x2b0 [amdgpu]                                                 
[  369.216057]  ? __check_object_size.part.0+0x3a/0xf0                                          
[  369.216066]  __x64_sys_ioctl+0x9d/0xe0                                                       
[  369.216073]  do_syscall_64+0x5c/0x90                                                                                                                                                         
[  369.216080]  ? do_syscall_64+0x69/0x90                                                       
[  369.216086]  ? __task_pid_nr_ns+0x6c/0xc0                                                    
[  369.216094]  ? exit_to_user_mode_prepare+0x3b/0xd0                                 
[  369.216102]  ? exit_to_user_mode_prepare+0x3b/0xd0                                  
[  369.216109]  ? syscall_exit_to_user_mode+0x2a/0x50                                  
[  369.216117]  ? do_syscall_64+0x69/0x90                                                       
[  369.216123]  ? do_syscall_64+0x69/0x90                                                       
[  369.216129]  ? do_syscall_64+0x69/0x90                                                       
[  369.216135]  entry_SYSCALL_64_after_hwframe+0x63/0xcd                                        
[  369.216143] RIP: 0033:0x7f40d871aaff                                                         
[  369.216149] Code: 00 48 89 44 24 18 31 c0 48 8d 44 24 60 c7 04 24 10 00 00 00 48 89 44 24 08 48 8d 44 24 20 48 89 44 24 10 b8 10 00 00 00 0f 05 <41> 89 c0 3d 00 f0 ff ff 77 1f 48 8b 44 24 1
8 64 48 2b 04 25 28 00                                                                          
[  369.216167] RSP: 002b:00007ffffadb1610 EFLAGS: 00000246 ORIG_RAX: 0000000000000010           
[  369.216177] RAX: ffffffffffffffda RBX: 00007ffffadb16a0 RCX: 00007f40d871aaff                
[  369.216185] RDX: 00007ffffadb16a0 RSI: 00000000c0284b82 RDI: 0000000000000003          
[  369.216194] RBP: 00000000c0284b82 R08: 0000000000000000 R09: 0000000000000200                
[  369.216202] R10: 00007f40d8f25db0 R11: 0000000000000246 R12: 00007ffffadb16a0                
[  369.216211] R13: 0000000000000003 R14: 00007ffffadb1d18 R15: 00007f40d91b8040                
[  369.216221]  </TASK>                                                                         
[  369.216225] Modules linked in: binfmt_misc intel_rapl_msr intel_rapl_common amd64_edac edac_mce_amd kvm_amd kvm rapl wmi_bmof snd_hda_codec_hdmi nls_iso8859_1 uvcvideo snd_hda_intel snd_usb
_audio videobuf2_vmalloc videobuf2_memops snd_intel_dspcfg videobuf2_v4l2 snd_intel_sdw_acpi snd_hda_codec snd_usbmidi_lib videobuf2_common snd_rawmidi snd_hda_core videodev snd_seq_device snd
_hwdep joydev snd_pcm input_leds mc snd_timer ccp snd soundcore ptdma k10temp mac_hid dm_multipath sch_fq_codel scsi_dh_rdac scsi_dh_emc scsi_dh_alua msr ramoops reed_solomon pstore_blk pstore
_zone efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear 
hid_generic usbhid hid r8153_ecm r8152 ib_uverbs ib_core cdc_ether usbnet mii amdgpu(OE) amddrm_ttm_helper(OE) amdttm(OE) iommu_v2 amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) i2c_algo_bit drm_di
splay_helper cec rc_core drm_kms_helper                                                                                                                                                         
[  369.216265]  crct10dif_pclmul crc32_pclmul ghash_clmulni_intel syscopyarea sysfillrect aesni_intel sysimgblt crypto_simd fb_sys_fops cryptd nvme ahci drm libahci nvme_core xhci_pci i2c_piix
4 xhci_pci_renesas wmi                                                                                                                                                                          
[  369.216363] CR2: 0000000000000130                                                                                                                                                            
[  369.216369] ---[ end trace 0000000000000000 ]---                                                                                                                                             
[  369.308437] RIP: 0010:pm_send_runlist+0x4a/0x6a0 [amdgpu]                                    
[  369.308577] Code: 30 65 48 8b 04 25 28 00 00 00 48 89 45 d0 31 c0 80 fb 01 0f 87 6d 1e 4b 00 83 e3 01 0f 85 64 05 00 00 49 8b 3f ba 01 00 00 00 <48> 8b 87 30 01 00 00 44 8b a7 6c 01 00 00 8
b 9f 70 01 00 00 44 8b                                                                          
[  369.308596] RSP: 0018:ffffb94da18f7b70 EFLAGS: 00010246                                                                                                                                      
[  369.308605] RAX: 0000000000000000 RBX: 0000000000000000 RCX: 0000000000000000               
[  369.308614] RDX: 0000000000000001 RSI: ffff980b8152cd58 RDI: 0000000000000000           
[  369.308623] RBP: ffffb94da18f7c00 R08: 0000000000000000 R09: 0000000000000000
[  369.308632] R10: 0000000000000000 R11: ffff980ba9851040 R12: 0000000000000000                                                                                                                
[  369.308641] R13: ffff980b8cf76c00 R14: 0000000000000001 R15: ffff980b8152cce0                
[  369.308650] FS:  00007f40d90cd780(0000) GS:ffff981a8efc0000(0000) knlGS:0000000000000000     
[  369.308661] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033                                
[  369.308668] CR2: 0000000000000130 CR3: 0000000152bfc005 CR4: 0000000000770ee0                
[  369.308677] PKRU: 55555554   
```

---

### 评论 #4 — geohot (2023-06-01T02:13:21Z)

Switched to Linux tiny2 6.2.16-060216-generic, and now back to this crash. Same crash with `linux-image-unsigned-6.3.5-060305-generic_6.3.5-060305.202305301445_amd64.deb`

```
[  110.623513] BUG: unable to handle page fault for address: ffffa92a3eaffff8                                                                                        
[  110.623533] #PF: supervisor write access in kernel mode                                                                                                                                        
[  110.623543] #PF: error_code(0x0002) - not-present page                                                                                                                                         
[  110.623551] PGD 100000067 P4D 100000067 PUD 0                                                                                                                                                        
[  110.623559] Oops: 0002 [#1] PREEMPT SMP NOPTI                                                                                                                                                       
[  110.623568] CPU: 19 PID: 1639 Comm: rocm-bandwidth- Tainted: G        W          6.2.16-060216-generic #202305171336                                                                                              
[  110.623581] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T/BCM, BIOS P3.50 07/19/2022                                                                                                                   
[  110.623592] RIP: 0010:amdgpu_gmc_set_pte_pde+0x23/0x40 [amdgpu]              
[  110.623746] Code: 90 90 90 90 90 90 90 0f 1f 44 00 00 48 b8 00 f0 ff ff ff ff 00 00 55 48 21 c1 8d 04 d5 00 00 00 00 4c 09 c1 48 01 c6 48 89 e5 <48> 89 0e 31 c0 5d 31 d2 31 c9 31 f6 45 31 c0 c3 cc cc cc cc 66 0f
[  110.623764] RSP: 0018:ffffa91d09447790 EFLAGS: 00010282                      
[  110.623773] RAX: 00000000fffffff8 RBX: 0000000000000000 RCX: 0003000125449077           
[  110.623782] RDX: 00000000ffffffff RSI: ffffa92a3eaffff8 RDI: ffff891f969a0000           
[  110.623792] RBP: ffffa91d09447790 R08: 0003000000000077 R09: ffffa9293eb00000                 
[  110.623801] R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000                 
[  110.623810] R13: ffff891f969a0000 R14: ffff891f4dd81608 R15: ffffa9293eb00000                 
[  110.623819] FS:  00007f3849f63780(0000) GS:ffff892e4ecc0000(0000) knlGS:0000000000000000      
[  110.623830] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033                                                                              
[  110.623838] CR2: ffffa92a3eaffff8 CR3: 000000012c2e2004 CR4: 0000000000770ee0                 
[  110.623848] PKRU: 55555554                                                                    
[  110.623853] Call Trace:                                                                       
[  110.623858]  <TASK>                                                                           
[  110.623864]  amdgpu_gart_map+0x7c/0xc0 [amdgpu]        
[  110.623999]  amdgpu_gart_bind+0x1a/0x50 [amdgpu]       
[  110.624131]  amdgpu_ttm_gart_bind+0xa0/0xc0 [amdgpu]                                          
[  110.624261]  amdgpu_ttm_recover_gart+0x5f/0x80 [amdgpu]        
[  110.624392]  amdgpu_gtt_mgr_recover+0x46/0x80 [amdgpu]         
[  110.624531]  gmc_v11_0_hw_init+0x29/0x100 [amdgpu]             
[  110.624683]  gmc_v11_0_resume+0x14/0x30 [amdgpu]      
[  110.624829]  amdgpu_device_ip_resume_phase1+0xe0/0x220 [amdgpu]
[  110.624957]  ? kgd2kfd_resume_iommu+0x4a/0x90 [amdgpu]                                   
```

---

### 评论 #5 — geohot (2023-06-01T03:43:53Z)

Ahh okay. https://community.amd.com/t5/knowledge-base/iommu-advisory-for-amd-instinct/ta-p/484601

It was suggested in our discord to turn the IOMMU on (not off), then use `amd_iommu=on iommu=pt`

I got this, but I haven't seen the gart_map crash.

```
[   33.516849] ------------[ cut here ]------------
[   33.516854] WARNING: CPU: 2 PID: 479 at drivers/gpu/drm/amd/amdgpu/amdgpu_ttm.c:471 amdgpu_bo_move+0x261/0x2e0 [amdgpu]
[   33.517190] Modules linked in: ipmi_ssif binfmt_misc nls_iso8859_1 intel_rapl_msr intel_rapl_common amd64_edac edac_mce_amd kvm_amd kvm irqbypass rapl wmi_bmof snd_hda_codec_hdmi snd_hda_intel snd_intel_dspcfg snd_intel_sdw_acpi snd_hda_codec snd_hda_core snd_hwdep snd_pcm snd_timer joydev input_leds snd soundcore ccp ptdma k10temp acpi_ipmi ipmi_si ipmi_devintf ipmi_msghandler mac_hid sch_fq_codel dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua msr ramoops reed_solomon pstore_blk pstore_zone efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear hid_generic cdc_ether usbhid usbnet hid mii amdgpu iommu_v2 drm_buddy gpu_sched video i2c_algo_bit drm_ttm_helper ttm drm_display_helper cec rc_core crct10dif_pclmul crc32_pclmul polyval_clmulni polyval_generic ghash_clmulni_intel drm_kms_helper sha512_ssse3 aesni_intel syscopyarea sysfillrect crypto_simd
[   33.517271]  sysimgblt cryptd nvme ahci drm bnxt_en nvme_core libahci nvme_common xhci_pci i2c_piix4 xhci_pci_renesas wmi
[   33.517285] CPU: 2 PID: 479 Comm: kworker/u64:29 Tainted: G        W          6.2.16-060216-generic #202305171336
[   33.517290] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T/BCM, BIOS P3.50 07/19/2022
[   33.517292] Workqueue: kfd_restore_wq restore_process_worker [amdgpu]
[   33.517719] RIP: 0010:amdgpu_bo_move+0x261/0x2e0 [amdgpu]
[   33.518035] Code: 7d c8 84 c0 74 0c 4c 89 e6 e8 1b cc ff ff 84 c0 75 62 48 c7 c7 60 5b fc c0 e8 1b ee 85 c6 e9 76 fe ff ff 0f 0b e9 47 fe ff ff <0f> 0b 41 bd ea ff ff ff e9 62 fe ff ff 83 f8 02 75 87 41 8b 44 24
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
[   33.519373] ---[ end trace 0000000000000000 ]---
```

Stable for 3 minutes until

```
[  431.913374] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma0 timeout, signaled seq=87092, emitted seq=87095                                                                           
[  431.913885] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process  pid 0 thread  pid 0                                                                                   
[  431.914340] amdgpu 0000:c3:00.0: amdgpu: GPU reset begin!
```

Attempting to reset the GPU caused a kernel panic.

```
[  861.065128] amdgpu 0000:47:00.0: amdgpu: GPU reset begin!
[  861.178043] amdgpu 0000:47:00.0: amdgpu: MODE1 reset
[  861.178046] amdgpu 0000:47:00.0: amdgpu: GPU mode1 reset
[  861.178109] amdgpu 0000:47:00.0: amdgpu: GPU smu mode1 reset
[  861.702750] amdgpu 0000:47:00.0: amdgpu: GPU reset succeeded, trying to resume
[  861.702833] BUG: unable to handle page fault for address: ffffb628feaffff8
[  861.702860] #PF: supervisor write access in kernel mode
[  861.702874] #PF: error_code(0x0002) - not-present page
[  861.702888] PGD 100000067 P4D 100000067 PUD 0 
[  861.702903] Oops: 0002 [#1] PREEMPT SMP NOPTI
[  861.702918] CPU: 11 PID: 479 Comm: kworker/u64:29 Tainted: G        W          6.2.16-060216-generic #202305171336
[  861.702942] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T/BCM, BIOS P3.50 07/19/2022
[  861.702961] Workqueue: amdgpu-reset-dev amdgpu_debugfs_reset_work [amdgpu]
[  861.703255] RIP: 0010:amdgpu_gmc_set_pte_pde+0x23/0x40 [amdgpu]
[  861.703410] Code: 90 90 90 90 90 90 90 0f 1f 44 00 00 48 b8 00 f0 ff ff ff ff 00 00 55 48 21 c1 8d 04 d5 00 00 00 00 4c 09 c1 48 01 c6 48 89 e5 <48> 89 0e 31 c0 5d 31 d2 31 c9 31 f6 45 31 c0 c3 cc cc cc cc 66 0f
[  861.703428] RSP: 0018:ffffb61bca21fbf8 EFLAGS: 00010282
[  861.703437] RAX: 00000000fffffff8 RBX: 0000000000000000 RCX: 0003000136b99077
[  861.703447] RDX: 00000000ffffffff RSI: ffffb628feaffff8 RDI: ffff8de056380000
[  861.703456] RBP: ffffb61bca21fbf8 R08: 0003000000000077 R09: ffffb627feb00000
[  861.703465] R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
[  861.703474] R13: ffff8de056380000 R14: ffff8de02c52d7e0 R15: ffffb627feb00000
[  861.703483] FS:  0000000000000000(0000) GS:ffff8def0eac0000(0000) knlGS:0000000000000000
[  861.703494] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[  861.703503] CR2: ffffb628feaffff8 CR3: 0000000111680004 CR4: 0000000000770ee0
[  861.703513] PKRU: 55555554
[  861.703518] Call Trace:
[  861.703524]  <TASK>
[  861.703531]  amdgpu_gart_map+0x7c/0xc0 [amdgpu]
[  861.703665]  amdgpu_gart_bind+0x1a/0x50 [amdgpu]
[  861.703796]  amdgpu_ttm_gart_bind+0xa0/0xc0 [amdgpu]
[  861.703927]  amdgpu_ttm_recover_gart+0x5f/0x80 [amdgpu]
...
```

---

### 评论 #6 — hkasivis (2023-06-02T21:43:02Z)

I believe the following patch should fix your issue. Could you please try? Thanks. 
https://lists.freedesktop.org/archives/amd-gfx/2023-March/090084.html

---

### 评论 #7 — geohot (2023-06-02T22:24:02Z)

Sorry, I'm not working with AMD GPUs anymore. In addition to the amdgpu_gart_map issue, there's 2 others I've seen with the MES and sdma0 that may be hardware issues. The driver and hardware don't have the stability that I would feel okay selling to customers of tinyboxes, and without hardware documentation these issues are very hard to investigate.

I recommend setting up a variety of systems constantly fuzzing from user space to catch kernel driver issues. I expect no amount of running demo apps in loops to crash either the kernel or the GPU, and it seems like it's a long way from there.

Feel free to close my issues.

---

### 评论 #8 — MatPoliquin (2023-06-05T09:55:45Z)

@geohot Quite sad, I saw your RDNA3 stream the other day and I was excited seeing that your were using AMD GPUs in your tinyboxes, it would have probably help motivate AMD and the community to spend more resources on making ROCm mature in the first place

---

### 评论 #9 — youngtuotuo (2023-06-05T10:51:30Z)

@MatPoliquin The official install instruction even fails, that means the product is not ready to sale.  Compare to AMD, take a look at this [tweet](https://twitter.com/Suhail/status/1661858704629854208?s=20).

---

### 评论 #10 — johnnynunez (2023-06-05T10:54:32Z)

> Sorry, I'm not working with AMD GPUs anymore. In addition to the amdgpu_gart_map issue, there's 2 others I've seen with the MES and sdma0 that may be hardware issues. The driver and hardware don't have the stability that I would feel okay selling to customers of tinyboxes, and without hardware documentation these issues are very hard to investigate.
> 
> I recommend setting up a variety of systems constantly fuzzing from user space to catch kernel driver issues. I expect no amount of running demo apps in loops to crash either the kernel or the GPU, and it seems like it's a long way from there.
> 
> Feel free to close my issues.

next station, intel one api?

---

### 评论 #11 — mgajda (2023-06-05T11:28:18Z)

While AMD automatically closes all tickets after few months, I believe it would be beneficial to fix this anyway.

---

### 评论 #12 — nicholatian (2023-06-06T02:07:54Z)

the first thing I had to deal with in my work is the fact that this stuff is so deliberately arcane that it is structurally impossible to substantially modify from the outside. most people who are in the trenches of systems programming these days understand this sad reality.

I hope things can improve structurally so that it is not always a matter of mindshare and collective resources for people to be able to try new things with existing technology.

---

### 评论 #13 — gotzmann (2023-06-09T10:30:40Z)

There a great and promising progress with AMD ROCm / HIP support with other projects, I think it's not the end of the red game yet https://github.com/turboderp/exllama/pull/7

---

### 评论 #14 — Anyeos (2023-06-10T11:41:21Z)

I had an RX 580 the past years and at first I buyed that for the future, it supported vulkan and AMD promised to improve the software in a near future, being open and better.
Next the support was horribly, a lot of binary compatibility issues using the recommended Linux OS and AMD drivers. Then AMD started developing an open source implementarion, incorporating support slowly but promising better. Not finishing it, AMD decided droping support for my perfectly working and capable card. Meaning that they never implemented raytracing, neither OpenCL (less for AI) for that card. That was my future: no support.

In that time I got some mad and deceptioned, but then I thinks, ok it is because this does not make sense, the RX580 is not powerful enough? But and now? Really, AMD? Why dont try to effort a little more and do it better? 
AMD is doing bad with software but now with hardware too? What they are doing then? I dont understand.

I hope AMD can really solve this if not I dont expect a better future for AMD in graphics and AI.


---

### 评论 #15 — massivedynamics1 (2023-06-17T10:51:43Z)

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Thanks for connecting <a href="https://twitter.com/realGeorgeHotz?ref_src=twsrc%5Etfw">@realGeorgeHotz</a>. Appreciate the work you and tiny corp are doing. We are committed to working with the community and improving our support. More to come on ROCm on @radeon soon. Lots of work ahead but excited about what we can do together.</p>&mdash; Lisa Su (@LisaSu) <a href="https://twitter.com/LisaSu/status/1669848494637735936?ref_src=twsrc%5Etfw">June 16, 2023</a></blockquote>

---

### 评论 #16 — johnnynunez (2023-06-17T10:54:54Z)

We have to push to give us mainstream support cards

---

### 评论 #17 — saadrahim (2023-06-29T14:13:12Z)

Fixed in ROCm 5.6.0

---
