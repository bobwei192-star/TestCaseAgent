# [Driver] WARNING: CPU: 96 PID: 903 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:600 amdgpu_irq_put+0x9f/0xb0 [amdgpu]

> **Issue #2197**
> **状态**: open
> **创建时间**: 2023-05-31T04:08:28Z
> **更新时间**: 2024-07-31T23:09:45Z
> **作者**: geohot
> **标签**: 5.5.0
> **URL**: https://github.com/ROCm/ROCm/issues/2197

## 标签

- **5.5.0** (颜色: #fbca04)

## 描述

Got this launching a bunch of OpenCL kernels. I'll sometimes get it just booting the system

1x 7900XTX
ASROCK ROMED8-2T
EPYC 7662
Ubuntu 22.04, Kernel 6.2.14-060214-generic, ROCm 5.5

And it's spammed all over my dmesg, happens 10+ times.

```
[11654.666176] ------------[ cut here ]------------
[11654.666178] WARNING: CPU: 96 PID: 903 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:600 amdgpu_irq_put+0x9f/0xb0 [amdgpu]
[11654.666437] Modules linked in: tls xt_conntrack nft_chain_nat xt_MASQUERADE nf_nat nf_conntrack_netlink nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xfrm_user xfrm_algo xt_addrtype nft_compat nf_tables nfnetlink br_netfilter bridge stp llc overlay ipmi_ssif intel_rapl_msr intel_rapl_common amd64_edac edac_mce_amd kvm_amd mei_hdcp(OE) mei_pxp(OE) mei_iaf(OE) kvm irqbypass rapl binfmt_misc nls_iso8859_1 snd_hda_codec_hdmi snd_hda_intel snd_intel_dspcfg snd_intel_sdw_acpi snd_hda_codec snd_hda_core snd_hwdep snd_pcm mei_gsc(OE) joydev input_leds snd_timer mei_me(OE) snd ccp mei(OE) soundcore acpi_ipmi ptdma k10temp ipmi_si ipmi_devintf ipmi_msghandler mac_hid sch_fq_codel dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua ramoops msr reed_solomon pstore_blk pstore_zone efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear hid_generic cdc_ether usbhid usbnet hid
[11654.666481]  mii amdgpu i915 iommu_v2 gpu_sched drm_buddy video wmi drm_ttm_helper i2c_algo_bit ttm drm_display_helper cec rc_core drm_kms_helper syscopyarea sysfillrect sysimgblt crct10dif_pclmul crc32_pclmul polyval_clmulni polyval_generic ghash_clmulni_intel sha512_ssse3 aesni_intel crypto_simd cryptd nvme drm ahci bnxt_en nvme_core libahci xhci_pci nvme_common xhci_pci_renesas i2c_piix4
[11654.666498] CPU: 96 PID: 903 Comm: kworker/96:1 Tainted: G        W  OE      6.2.14-060214-generic #202305010032
[11654.666500] Hardware name: To Be Filled By O.E.M. ROMED8-2T/ROMED8-2T, BIOS P3.50 07/19/2022
[11654.666501] Workqueue: pm pm_runtime_work
[11654.666503] RIP: 0010:amdgpu_irq_put+0x9f/0xb0 [amdgpu]
[11654.666759] Code: 31 f6 31 ff e9 52 9f 66 da 44 89 e2 48 89 de 4c 89 f7 e8 94 fc ff ff 5b 41 5c 41 5d 41 5e 5d 31 d2 31 f6 31 ff e9 31 9f 66 da <0f> 0b b8 ea ff ff ff eb c3 b8 fe ff ff ff eb bc 90 90 90 90 90 90
[11654.666761] RSP: 0018:ffffbb9f02ecfc40 EFLAGS: 00010246
[11654.666763] RAX: 0000000000000000 RBX: ffffa084f0f224d8 RCX: 0000000000000000
[11654.666764] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
[11654.666765] RBP: ffffbb9f02ecfc60 R08: 0000000000000000 R09: 0000000000000000
[11654.666766] R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
[11654.666767] R13: 0000000000000001 R14: ffffa084f0f20000 R15: ffffa084f0f20000
[11654.666768] FS:  0000000000000000(0000) GS:ffffa0c30e600000(0000) knlGS:0000000000000000
[11654.666770] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[11654.666771] CR2: 00007fe81d9628e8 CR3: 0000000d93010000 CR4: 0000000000350ee0
[11654.666773] Call Trace:
[11654.666773]  <TASK>
[11654.666775]  gmc_v11_0_hw_fini+0x24/0x80 [amdgpu]
[11654.667030]  gmc_v11_0_suspend+0xe/0x20 [amdgpu]
[11654.667284]  amdgpu_device_ip_suspend_phase2+0x25d/0x490 [amdgpu]
[11654.667518]  amdgpu_device_suspend+0x142/0x1b0 [amdgpu]
[11654.667752]  amdgpu_pmops_runtime_suspend+0xdf/0x200 [amdgpu]
[11654.667989]  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
[11654.667991]  pci_pm_runtime_suspend+0x6a/0x1f0
[11654.667993]  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
[11654.667995]  __rpm_callback+0x50/0x170
[11654.667998]  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
[11654.668000]  rpm_callback+0x6d/0x80
[11654.668003]  ? __pfx_pci_pm_runtime_suspend+0x10/0x10
[11654.668004]  rpm_suspend+0x122/0x730
[11654.668007]  ? raw_spin_rq_unlock+0x10/0x40
[11654.668009]  ? finish_task_switch.isra.0+0x85/0x2a0
[11654.668012]  pm_runtime_work+0xc6/0xe0
[11654.668013]  process_one_work+0x225/0x430
[11654.668016]  worker_thread+0x50/0x3e0
[11654.668018]  ? __pfx_worker_thread+0x10/0x10
[11654.668020]  kthread+0xe9/0x110
[11654.668022]  ? __pfx_kthread+0x10/0x10
[11654.668025]  ret_from_fork+0x2c/0x50
[11654.668028]  </TASK>
[11654.668028] ---[ end trace 0000000000000000 ]---
```

---

## 评论 (7 条)

### 评论 #1 — sdli1995 (2023-06-02T03:25:54Z)

same problem . In my case
cpu:epyc 7542
motherboard:h12ssl-i
operation system: debian12
7900xtx + rx6400(only for display)
error was on boot init amdgpu driver failed after that throw error 
here is full boot logo with dmesg command grep amdgpu 

> [    3.804275] [drm] amdgpu kernel modesetting enabled.
> [    3.804670] amdgpu: Ignoring ACPI CRAT on non-APU system
> [    3.804968] amdgpu: Virtual CRAT table created for CPU
> [    3.805339] amdgpu: Topology: Add CPU node
> [    3.810953] amdgpu 0000:c3:00.0: amdgpu: Fetched VBIOS from VFCT
> [    3.811216] amdgpu: ATOM BIOS: 113-1WPG24XL210915
> [    3.811832] amdgpu 0000:c3:00.0: vgaarb: deactivate vga console
> [    3.811835] amdgpu 0000:c3:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
> [    3.811890] amdgpu 0000:c3:00.0: BAR 2: releasing [mem 0xc0000000-0xc01fffff 64bit pref]
> [    3.811895] amdgpu 0000:c3:00.0: BAR 0: releasing [mem 0xb0000000-0xbfffffff 64bit pref]
> [    3.811940] amdgpu 0000:c3:00.0: BAR 0: assigned [mem 0x10100000000-0x101ffffffff 64bit pref]
> [    3.811950] amdgpu 0000:c3:00.0: BAR 2: assigned [mem 0x10080000000-0x100801fffff 64bit pref]
> [    3.812029] amdgpu 0000:c3:00.0: amdgpu: VRAM: 4080M 0x0000008000000000 - 0x00000080FEFFFFFF (4080M used)
> [    3.812034] amdgpu 0000:c3:00.0: amdgpu: GART: 512M 0x0000000000000000 - 0x000000001FFFFFFF
> [    3.812038] amdgpu 0000:c3:00.0: amdgpu: AGP: 267894784M 0x0000008400000000 - 0x0000FFFFFFFFFFFF
> [    3.812127] [drm] amdgpu: 4080M of VRAM memory ready
> [    3.812130] [drm] amdgpu: 128891M of GTT memory ready.
> [    3.812414] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_sos.bin
> [    3.812459] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_ta.bin
> [    3.812466] amdgpu 0000:c3:00.0: amdgpu: PSP runtime database doesn't exist
> [    3.812470] amdgpu 0000:c3:00.0: amdgpu: PSP runtime database doesn't exist
> [    5.588902] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_smc.bin
> [    5.588919] amdgpu 0000:c3:00.0: amdgpu: STB initialized to 2048 entries
> [    5.589025] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_dmcub.bin
> [    5.589087] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_pfp.bin
> [    5.589138] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_me.bin
> [    5.589190] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_ce.bin
> [    5.589228] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_rlc.bin
> [    5.589283] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_mec.bin
> [    5.589337] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_mec2.bin
> [    5.589869] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_sdma.bin
> [    5.589982] amdgpu 0000:c3:00.0: firmware: direct-loading firmware amdgpu/beige_goby_vcn.bin
> [    5.589994] amdgpu 0000:c3:00.0: amdgpu: Will use PSP to load VCN firmware
> [    5.756426] amdgpu 0000:c3:00.0: amdgpu: RAS: optional ras ta ucode is not available
> [    5.771457] amdgpu 0000:c3:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
> [    5.771482] amdgpu 0000:c3:00.0: amdgpu: smu driver if version = 0x0000000d, smu fw if version = 0x0000000f, smu fw program = 0, version = 0x00491f00 (73.31.0)
> [    5.771488] amdgpu 0000:c3:00.0: amdgpu: SMU driver if version not matched
> [    5.771521] amdgpu 0000:c3:00.0: amdgpu: use vbios provided pptable
> [    5.811572] amdgpu 0000:c3:00.0: amdgpu: SMU is initialized successfully!
> [    5.860288] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
> [    5.860448] amdgpu: sdma_bitmap: ff
> [    5.860507] amdgpu: Virtual CRAT table created for GPU
> [    5.860683] amdgpu: Topology: Add dGPU node [0x743f:0x1002]
> [    5.860686] kfd kfd: amdgpu: added device 1002:743f
> [    5.860704] amdgpu 0000:c3:00.0: amdgpu: SE 1, SH per SE 2, CU per SH 8, active_cu_number 12
> [    5.860777] amdgpu 0000:c3:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
> [    5.860781] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
> [    5.860784] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
> [    5.860786] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
> [    5.860789] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
> [    5.860792] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
> [    5.860794] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
> [    5.860797] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
> [    5.860800] amdgpu 0000:c3:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
> [    5.860803] amdgpu 0000:c3:00.0: amdgpu: ring kiq_2.1.0 uses VM inv eng 11 on hub 0
> [    5.860805] amdgpu 0000:c3:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
> [    5.860808] amdgpu 0000:c3:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 1
> [    5.862389] amdgpu 0000:c3:00.0: amdgpu: Using BACO for runtime pm
> [    5.862574] [drm] Initialized amdgpu 3.49.0 20150101 for 0000:c3:00.0 on minor 0
> [    5.870286] fbcon: amdgpudrmfb (fb0) is primary device
> [    5.956825] amdgpu 0000:c3:00.0: [drm] fb0: amdgpudrmfb frame buffer device
> [    5.984592] amdgpu 0000:03:00.0: amdgpu: Fetched VBIOS from VFCT
> [    5.984634] amdgpu: ATOM BIOS: 113-3E4710U-O4O
> [    5.984735] amdgpu 0000:03:00.0: [drm:jpeg_v4_0_early_init [amdgpu]] JPEG decode is enabled in VM mode
> [    5.985010] amdgpu 0000:03:00.0: amdgpu: Trusted Memory Zone (TMZ) feature not supported
> [    5.985093] amdgpu 0000:03:00.0: amdgpu: MEM ECC is not presented.
> [    5.985131] amdgpu 0000:03:00.0: amdgpu: SRAM ECC is not presented.
> [    5.985237] amdgpu 0000:03:00.0: BAR 2: releasing [mem 0x380b0000000-0x380b01fffff 64bit pref]
> [    5.985282] amdgpu 0000:03:00.0: BAR 0: releasing [mem 0x380a0000000-0x380afffffff 64bit pref]
> [    5.985616] amdgpu 0000:03:00.0: BAR 0: assigned [mem 0x28800000000-0x28fffffffff 64bit pref]
> [    5.985666] amdgpu 0000:03:00.0: BAR 2: assigned [mem 0x28400000000-0x284001fffff 64bit pref]
> [    5.998506] amdgpu 0000:03:00.0: amdgpu: VRAM: 24560M 0x0000008000000000 - 0x00000085FEFFFFFF (24560M used)
> [    5.999736] amdgpu 0000:03:00.0: amdgpu: GART: 512M 0x0000000000000000 - 0x000000001FFFFFFF
> [    6.003567] [drm] amdgpu: 24560M of VRAM memory ready
> [    6.004772] [drm] amdgpu: 128891M of GTT memory ready.
> [    6.008707] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/psp_13_0_0_sos.bin
> [    6.010007] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/psp_13_0_0_ta.bin
> [    6.011528] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/smu_13_0_0.bin
> [    6.012900] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/dcn_3_2_0_dmcub.bin
> [    6.015368] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_imu.bin
> [    6.016576] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_pfp.bin
> [    6.017731] amdgpu 0000:03:00.0: amdgpu: CP RS64 enable
> [    6.018905] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_me.bin
> [    6.020092] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_rlc.bin
> [    6.021282] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_mec.bin
> [    6.022632] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/sdma_6_0_0.bin
> [    6.023760] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/vcn_4_0_0.bin
> [    6.025745] amdgpu 0000:03:00.0: amdgpu: Will use PSP to load VCN firmware
> [    6.027868] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_mes.bin
> [    6.028937] amdgpu 0000:03:00.0: firmware: direct-loading firmware amdgpu/gc_11_0_0_mes1.bin
> [    9.368378] [drm:psp_hw_start [amdgpu]] *ERROR* PSP load tmr failed!
> [    9.636139] [drm:psp_v13_0_ring_destroy [amdgpu]] *ERROR* Fail to stop psp ring
> [    9.638191] [drm:psp_hw_init [amdgpu]] *ERROR* PSP firmware loading failed
> [    9.640083] [drm:amdgpu_device_fw_loading [amdgpu]] *ERROR* hw_init of IP block <psp> failed -22
> [    9.641995] amdgpu 0000:03:00.0: amdgpu: amdgpu_device_ip_init failed
> [    9.643749] amdgpu 0000:03:00.0: amdgpu: Fatal error during GPU init
> [    9.645428] amdgpu 0000:03:00.0: amdgpu: amdgpu: finishing device.
> [    9.648862] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.650823] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [    9.663049] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.692734]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [    9.695381]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [    9.698056]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [    9.700696]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [    9.729629] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.732217] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [    9.747333] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.779801]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [    9.782330]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [    9.784844]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [    9.787345]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [    9.812779] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.814762] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [    9.825395] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.850771]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [    9.853207]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [    9.855564]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [    9.857900]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [    9.882978] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.884983] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [    9.895626] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.920959]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [    9.923382]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [    9.925747]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [    9.928104]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [    9.953136] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.955092] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [    9.965686] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [    9.991060]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [    9.993472]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [    9.995850]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [    9.998227]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.023310] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.025297] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.035942] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.061324]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.063691]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.066074]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.068460]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.093485] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.095465] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.106035] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.131358]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.133755]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.136057]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.138419]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.163521] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.165502] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.176177] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.201549]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.203930]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.206300]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.208645]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.233537] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.235527] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.246110] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.271312]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.273682]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.276054]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.278430]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.303408] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.305444] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.316090] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.341298]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.343659]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.345991]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.348363]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.373082] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.375054] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.385485] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.410711]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.413079]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.415378]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.417708]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.442546] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.444542] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.455152] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.480406]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.482836]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.485104]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.487442]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.512170] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.514176] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.524826] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.549831]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.552163]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.554503]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.556860]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.581723] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.583662] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.594299] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.619327]  amdgpu_fence_driver_hw_fini+0x5c/0xe0 [amdgpu]
> [   10.621657]  amdgpu_device_fini_hw+0x97/0x2af [amdgpu]
> [   10.623986]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.626353]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.651817] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.653798] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.664394] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.689658]  gmc_v11_0_hw_fini+0x20/0x70 [amdgpu]
> [   10.692010]  amdgpu_device_fini_hw+0x1cc/0x2af [amdgpu]
> [   10.694383]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.696719]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.721268] WARNING: CPU: 24 PID: 440 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:656 amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.723250] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.733705] RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
> [   10.758862]  gmc_v11_0_hw_fini+0x31/0x70 [amdgpu]
> [   10.761177]  amdgpu_device_fini_hw+0x1cc/0x2af [amdgpu]
> [   10.763543]  amdgpu_driver_load_kms.cold+0x54/0x6a [amdgpu]
> [   10.765892]  amdgpu_pci_probe+0x1cb/0x3f0 [amdgpu]
> [   10.788882] amdgpu: probe of 0000:03:00.0 failed with error -22
> [   10.869854] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   10.904089]  amdgpu_vram_mgr_fini+0x10e/0x180 [amdgpu]
> [   10.906542]  amdgpu_ttm_fini+0x118/0x190 [amdgpu]
> [   10.908887]  amdgpu_bo_fini+0x2a/0x90 [amdgpu]
> [   10.911173]  gmc_v11_0_sw_fini+0x26/0x30 [amdgpu]
> [   10.913544]  amdgpu_device_fini_sw+0xce/0x3e0 [amdgpu]
> [   10.915853]  amdgpu_driver_release_kms+0x12/0x30 [amdgpu]
> [   10.978973] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   11.007484]  amdgpu_vram_mgr_fini+0x10e/0x180 [amdgpu]
> [   11.009330]  amdgpu_ttm_fini+0x118/0x190 [amdgpu]
> [   11.011090]  amdgpu_bo_fini+0x2a/0x90 [amdgpu]
> [   11.012875]  gmc_v11_0_sw_fini+0x26/0x30 [amdgpu]
> [   11.014652]  amdgpu_device_fini_sw+0xce/0x3e0 [amdgpu]
> [   11.016473]  amdgpu_driver_release_kms+0x12/0x30 [amdgpu]
> [   11.079866] Modules linked in: hid_logitech_hidpp hid_logitech_dj rndis_host hid_generic cdc_ether usbhid usbnet sd_mod mii hid amdgpu(+) gpu_sched drm_buddy video wmi i2c_algo_bit drm_display_helper cec rc_core raid0 drm_ttm_helper ttm md_mod crc32_pclmul crc32c_intel drm_kms_helper ahci libahci xhci_pci ixgbe libata xhci_hcd nvme xfrm_algo dca mdio_devres drm nvme_core libphy t10_pi scsi_mod usbcore ptp crc64_rocksoft crc64 scsi_common pps_core crc_t10dif i2c_piix4 mdio crct10dif_generic usb_common crct10dif_pclmul crct10dif_common button
> [   11.108748]  amdgpu_vram_mgr_fini+0x10e/0x180 [amdgpu]
> [   11.110609]  amdgpu_ttm_fini+0x118/0x190 [amdgpu]
> [   11.112389]  amdgpu_bo_fini+0x2a/0x90 [amdgpu]
> [   11.114193]  gmc_v11_0_sw_fini+0x26/0x30 [amdgpu]
> [   11.115949]  amdgpu_device_fini_sw+0xce/0x3e0 [amdgpu]
> [   11.117784]  amdgpu_driver_release_kms+0x12/0x30 [amdgpu]
> [   11.184359] [drm] amdgpu: ttm finalized
> [   43.846818] snd_hda_intel 0000:c3:00.1: bound 0000:c3:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
> [   45.246533] amdgpu 0000:c3:00.0: vgaarb: changed VGA decodes: olddecodes=io+mem,decodes=none:owns=none
> 


---

### 评论 #2 — ivanstepanovftw (2023-06-03T08:22:07Z)

Fedora, opened lid after sleep and got black screen and unresponsive system.

<details><summary>Details</summary>
<p>


```
Jun 03 10:38:37 fedora kernel: ------------[ cut here ]------------
Jun 03 10:38:37 fedora kernel: WARNING: CPU: 12 PID: 1299748 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:600 amdgpu_irq_put+0x45/0x70 [amdgpu]
Jun 03 10:38:37 fedora kernel: Modules linked in: isofs option usb_wwan uas usb_storage xt_nat veth tun tls rfcomm snd_seq_dummy snd_hrtimer xt_conntrack xt_MASQUERADE nf_conntr>
Jun 03 10:38:37 fedora kernel:  snd_hwdep btbcm snd_rpl_pci_acp6x kvm_amd snd_pci_acp6x snd_seq btintel videobuf2_vmalloc libarc4 snd_seq_device snd_pci_acp5x btmtk videobuf2_me>
Jun 03 10:38:37 fedora kernel: CPU: 12 PID: 1299748 Comm: kworker/u32:16 Tainted: G        W  OE      6.2.15-200.fc37.x86_64 #1
Jun 03 10:38:37 fedora kernel: Hardware name: LENOVO 82L7/LNVNB161216, BIOS GECN32WW(V1.16) 09/19/2022
Jun 03 10:38:37 fedora kernel: Workqueue: events_unbound async_run_entry_fn
Jun 03 10:38:37 fedora kernel: RIP: 0010:amdgpu_irq_put+0x45/0x70 [amdgpu]
Jun 03 10:38:37 fedora kernel: Code: 48 8b 4e 10 48 83 39 00 74 2c 89 d1 48 8d 04 88 8b 08 85 c9 74 14 f0 ff 08 b8 00 00 00 00 74 05 c3 cc cc cc cc e9 5b fd ff ff <0f> 0b b8 ea >
Jun 03 10:38:37 fedora kernel: RSP: 0018:ffffb2060b72fd48 EFLAGS: 00010246
Jun 03 10:38:37 fedora kernel: RAX: ffff9a1740ad2eb0 RBX: 0000000000000001 RCX: 0000000000000000
Jun 03 10:38:37 fedora kernel: RDX: 0000000000000000 RSI: ffff9a17519d0380 RDI: ffff9a17519c0000
Jun 03 10:38:37 fedora kernel: RBP: ffff9a17519c0000 R08: 0000000000100000 R09: 000000000030e300
Jun 03 10:38:37 fedora kernel: R10: ffffb2060b72fc48 R11: 0000000000000000 R12: ffff9a17519d0380
Jun 03 10:38:37 fedora kernel: R13: ffff9a17519d8968 R14: ffffffffb2924aff R15: ffff9a1773cc8148
Jun 03 10:38:37 fedora kernel: FS:  0000000000000000(0000) GS:ffff9a1a3e900000(0000) knlGS:0000000000000000
Jun 03 10:38:37 fedora kernel: CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Jun 03 10:38:37 fedora kernel: CR2: 00007f50cf3603a6 CR3: 00000003be010000 CR4: 0000000000750ee0
Jun 03 10:38:37 fedora kernel: PKRU: 55555554
Jun 03 10:38:37 fedora kernel: Call Trace:
Jun 03 10:38:37 fedora kernel:  <TASK>
Jun 03 10:38:37 fedora kernel:  sdma_v4_0_hw_fini+0x38/0xa0 [amdgpu]
Jun 03 10:38:37 fedora kernel:  amdgpu_device_ip_suspend_phase2+0x101/0x1a0 [amdgpu]
Jun 03 10:38:37 fedora kernel:  amdgpu_device_suspend+0x10b/0x180 [amdgpu]
Jun 03 10:38:37 fedora kernel:  pci_pm_suspend+0x7b/0x170
Jun 03 10:38:37 fedora kernel:  ? __pfx_pci_pm_suspend+0x10/0x10
Jun 03 10:38:37 fedora kernel:  dpm_run_callback+0x8c/0x1e0
Jun 03 10:38:37 fedora kernel:  __device_suspend+0x10a/0x560
Jun 03 10:38:37 fedora kernel:  async_suspend+0x1a/0x70
Jun 03 10:38:37 fedora kernel:  async_run_entry_fn+0x30/0x130
Jun 03 10:38:37 fedora kernel:  process_one_work+0x1c8/0x3c0
Jun 03 10:38:37 fedora kernel:  worker_thread+0x4d/0x380
Jun 03 10:38:37 fedora kernel:  ? __pfx_worker_thread+0x10/0x10
Jun 03 10:38:37 fedora kernel:  kthread+0xe9/0x110
Jun 03 10:38:37 fedora kernel:  ? __pfx_kthread+0x10/0x10
Jun 03 10:38:37 fedora kernel:  ret_from_fork+0x2c/0x50
Jun 03 10:38:37 fedora kernel:  </TASK>
Jun 03 10:38:37 fedora kernel: ---[ end trace 0000000000000000 ]---
Jun 03 10:38:37 fedora kernel: ------------[ cut here ]------------
...
Jun 03 10:38:37 fedora kernel: smpboot: Booting Node 0 Processor 15 APIC 0xf
Jun 03 10:38:37 fedora kernel: ACPI: \_SB_.PLTF.C00F: Found 3 idle states
Jun 03 10:38:37 fedora kernel: CPU15 is up
Jun 03 10:38:37 fedora kernel: ACPI: PM: Waking up from system sleep state S3
Jun 03 10:38:37 fedora kernel: ACPI: EC: interrupt unblocked
Jun 03 10:38:37 fedora kernel: ACPI: EC: event unblocked
Jun 03 10:38:37 fedora kernel: pci 0000:00:00.2: can't derive routing for PCI INT A
Jun 03 10:38:37 fedora kernel: pci 0000:00:00.2: PCI INT A: no GSI
Jun 03 10:38:37 fedora kernel: [drm] PCIE GART of 1024M enabled.
Jun 03 10:38:37 fedora kernel: [drm] PTB located at 0x000000F41FC00000
Jun 03 10:38:37 fedora kernel: [drm] PSP is resuming...
Jun 03 10:38:37 fedora kernel: nvme nvme0: Shutdown timeout set to 8 seconds
Jun 03 10:38:37 fedora kernel: nvme nvme0: 16/0/0 default/read/poll queues
Jun 03 10:38:37 fedora kernel: [drm] reserve 0x400000 from 0xf41f800000 for PSP TMR
Jun 03 10:38:37 fedora kernel: [drm] psp gfx command SETUP_TMR(0x5) failed and response status is (0x80000306)
Jun 03 10:38:37 fedora kernel: [drm] failed to load ucode CP_MEC1(0x19) 
Jun 03 10:38:37 fedora kernel: [drm] psp gfx command LOAD_IP_FW(0x6) failed and response status is (0x80000203)
Jun 03 10:38:37 fedora kernel: [drm] failed to load ucode VCN(0x36) 
Jun 03 10:38:37 fedora kernel: [drm] psp gfx command LOAD_IP_FW(0x6) failed and response status is (0x80000203)
Jun 03 10:38:37 fedora kernel: [drm] failed to load ucode DMCUB(0x3C) 
Jun 03 10:38:37 fedora kernel: [drm] psp gfx command LOAD_IP_FW(0x6) failed and response status is (0x80000203)
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: amdgpu: RAS: optional ras ta ucode is not available
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: amdgpu: RAP: optional rap ta ucode is not available
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: amdgpu: SMU is resuming...
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: amdgpu: dpm has been disabled
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: amdgpu: SMU is resumed successfully!
Jun 03 10:38:37 fedora kernel: [drm] Wait for DMUB auto-load failed: 3
Jun 03 10:38:37 fedora kernel: [drm] DMUB hardware initialized: version=0x01010024
Jun 03 10:38:37 fedora kernel: [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=3
Jun 03 10:38:37 fedora kernel: [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=3
Jun 03 10:38:37 fedora kernel: [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=3
Jun 03 10:38:37 fedora kernel: [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=3
Jun 03 10:38:37 fedora kernel: [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=3
Jun 03 10:38:37 fedora kernel: ------------[ cut here ]------------
...
Jun 03 10:38:37 fedora kernel: ---[ end trace 0000000000000000 ]---
Jun 03 10:38:37 fedora kernel: [drm:dc_dmub_srv_wait_idle [amdgpu]] *ERROR* Error waiting for DMUB idle: status=3
Jun 03 10:38:37 fedora kernel: [drm] kiq ring mec 2 pipe 1 q 0
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: [drm:amdgpu_ring_test_helper [amdgpu]] *ERROR* ring kiq_2.1.0 test failed (-110)
Jun 03 10:38:37 fedora kernel: [drm:amdgpu_gfx_enable_kcq [amdgpu]] *ERROR* KCQ enable failed
Jun 03 10:38:37 fedora kernel: [drm:amdgpu_device_ip_resume_phase2 [amdgpu]] *ERROR* resume of IP block <gfx_v9_0> failed -110
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: amdgpu: amdgpu_device_ip_resume failed (-110).
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: PM: dpm_run_callback(): pci_pm_resume+0x0/0xe0 returns -110
Jun 03 10:38:37 fedora kernel: amdgpu 0000:04:00.0: PM: failed to resume async: error -110
Jun 03 10:38:37 fedora kernel: PM: resume devices took 4.090 seconds
Jun 03 10:38:37 fedora kernel: OOM killer enabled.
Jun 03 10:38:37 fedora kernel: Restarting tasks ... done.
Jun 03 10:38:37 fedora kernel: random: crng reseeded on system resumption
Jun 03 10:38:37 fedora systemd-resolved[879]: Clock change detected. Flushing caches.
Jun 03 10:38:37 fedora rtkit-daemon[931]: The canary thread is apparently starving. Taking action.
Jun 03 10:38:37 fedora google-chrome.desktop[2938]: [2932:2963:0603/103837.806054:ERROR:connection_factory_impl.cc(428)] Failed to connect to MCS endpoint with error -105
Jun 03 10:38:37 fedora systemd-logind[943]: Lid opened.
Jun 03 10:38:37 fedora rtkit-daemon[931]: Demoting known real-time threads.
Jun 03 10:38:37 fedora sssd_kcm[1230754]: Shutting down (status = 0)
Jun 03 10:38:37 fedora rtkit-daemon[931]: Successfully demoted thread 1177495 of process 1177476 (/usr/bin/telegram-desktop).
Jun 03 10:38:37 fedora rtkit-daemon[931]: Successfully demoted thread 2259 of process 2242 (/usr/bin/pipewire).
Jun 03 10:38:37 fedora rtkit-daemon[931]: Successfully demoted thread 2242 of process 2242 (/usr/bin/pipewire).
Jun 03 10:38:37 fedora rtkit-daemon[931]: Successfully demoted thread 2160 of process 2152 (/usr/bin/wireplumber).
Jun 03 10:38:37 fedora rtkit-daemon[931]: Successfully demoted thread 2152 of process 2152 (/usr/bin/wireplumber).
Jun 03 10:38:37 fedora rtkit-daemon[931]: Successfully demoted thread 2161 of process 2146 (/usr/bin/pipewire).
Jun 03 10:38:37 fedora rtkit-daemon[931]: Successfully demoted thread 2146 of process 2146 (/usr/bin/pipewire).
Jun 03 10:38:37 fedora rtkit-daemon[931]: Demoted 7 threads.
Jun 03 10:38:37 fedora systemd[1]: sssd-kcm.service: Deactivated successfully.
Jun 03 10:38:37 fedora audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=sssd-kcm comm="systemd" exe="/usr/lib/systemd>
Jun 03 10:38:37 fedora systemd[1]: sssd-kcm.service: Consumed 15.757s CPU time.
Jun 03 10:38:37 fedora systemd[1]: Starting sssd-kcm.service - SSSD Kerberos Cache Manager...
Jun 03 10:38:38 fedora systemd-sleep[1299735]: System returned from sleep state.
Jun 03 10:38:38 fedora kernel: PM: suspend exit
Jun 03 10:38:38 fedora bluetoothd[911]: Controller resume with wake event 0x0
Jun 03 10:38:38 fedora systemd[1]: systemd-suspend.service: Deactivated successfully.
...
Jun 03 10:38:48 fedora kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring gfx_low timeout, signaled seq=154193466, emitted seq=154193469
Jun 03 10:38:48 fedora kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process Xorg pid 2037 thread Xorg:cs0 pid 2038
Jun 03 10:38:48 fedora kernel: amdgpu 0000:04:00.0: amdgpu: GPU reset begin!
Jun 03 10:38:48 fedora kernel: ------------[ cut here ]------------
...
```


</p>
</details> 

---

### 评论 #3 — massivedynamics1 (2023-06-17T10:53:45Z)

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Thanks for connecting <a href="https://twitter.com/realGeorgeHotz?ref_src=twsrc%5Etfw">@realGeorgeHotz</a>. Appreciate the work you and tiny corp are doing. We are committed to working with the community and improving our support. More to come on ROCm on @radeon soon. Lots of work ahead but excited about what we can do together.</p>&mdash; Lisa Su (@LisaSu) <a href="https://twitter.com/LisaSu/status/1669848494637735936?ref_src=twsrc%5Etfw">June 16, 2023</a></blockquote>

---

### 评论 #4 — icanc0 (2023-06-24T04:20:52Z)

same issue here, seems to be crashing with a wx9100

---

### 评论 #5 — eduarddejong (2023-07-08T15:36:14Z)

Like ivanstepanovftw for me it was also while comming back from sleep mode after reopening my laptop lid, my laptop is Legion 5 Pro.
I was running using dynamic graphics mode, in which the builtin AMD gpu is the one primarilly used, not the nvidia card.

Distro: Arch Linux.
Kernel version: 6.4.2-arch1-1

Basically I see the error being logged multiple times when it happens.
The source code lines mentioned in these messages are:
- drivers/gpu/drm/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c:7698
- drivers/gpu/drm/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c:8151


---

### 评论 #6 — ahaas25 (2023-12-05T03:47:38Z)

Same issue. Happens after resuming from sleep.

```Dec  4 22:39:05 Blade kernel: [ 1118.585019] WARNING: CPU: 15 PID: 6654 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:600 amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.585162] Modules linked in: rfcomm ccm ip6t_REJECT nf_reject_ipv6 xt_hl ip6_tables ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_multiport nft_limit cmac algif_hash algif_skcipher snd_ctl_l
ed xt_limit af_alg xt_addrtype bnep xt_tcpudp xt_conntrack nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nft_compat nf_tables nfnetlink binfmt_misc zfs(PO) zunicode(PO) zzstd(O) zlua(O) zavl(PO) icp(PO) zcommon(PO) znvpair(PO) spl(O) snd_so
c_dmic snd_acp3x_pdm_dma snd_acp3x_rn snd_sof_amd_rembrandt snd_sof_amd_renoir snd_sof_amd_acp snd_sof_pci snd_sof_xtensa_dsp snd_hda_codec_realtek snd_sof snd_hda_codec_generic snd_sof_utils input_leds ledtrig_audio snd_hda_codec_hdmi s
nd_soc_core snd_hda_intel snd_compress joydev snd_intel_dspcfg ac97_bus snd_intel_sdw_acpi snd_pcm_dmaengine snd_hda_codec snd_pci_ps snd_hda_core intel_rapl_msr snd_rpl_pci_acp6x snd_hwdep intel_rapl_common snd_acp_pci btusb snd_seq_mid
i snd_pci_acp6x btrtl uvcvideo snd_seq_midi_event edac_mce_amd snd_pcm iwlmvm btbcm
Dec  4 22:39:05 Blade kernel: [ 1118.585226]  videobuf2_vmalloc snd_rawmidi snd_pci_acp5x kvm_amd btintel videobuf2_memops mac80211 snd_seq videobuf2_v4l2 btmtk snd_rn_pci_acp3x libarc4 kvm snd_seq_device videodev bluetooth snd_acp_confi
g snd_timer nvidiafb irqbypass iwlwifi dcdbas videobuf2_common nls_iso8859_1 ecdh_generic snd_soc_acpi snd vgastate rapl razerkbd(O) hid_multitouch dell_wmi_descriptor wmi_bmof mc cfg80211 k10temp ecc snd_pci_acp3x ccp fb_ddc soundcore m
ac_hid nvidia_uvm(PO) sch_fq_codel msr parport_pc ppdev lp parport efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic xor raid6_pq libcrc32c dm_mirror dm_region_hash dm_log nvidia_drm(PO) nvidia_modeset(PO) usbhid nvidia(PO) amd
gpu iommu_v2 drm_buddy gpu_sched i2c_algo_bit drm_ttm_helper ttm drm_display_helper crct10dif_pclmul cec crc32_pclmul rc_core polyval_clmulni drm_kms_helper polyval_generic syscopyarea ghash_clmulni_intel sysfillrect hid_generic nvme sha
512_ssse3 sysimgblt aesni_intel drm nvme_core crypto_simd i2c_hid_acpi xhci_pci video
Dec  4 22:39:05 Blade kernel: [ 1118.585302]  i2c_hid cryptd i2c_piix4 nvme_common xhci_pci_renesas wmi hid
Dec  4 22:39:05 Blade kernel: [ 1118.585310] CPU: 15 PID: 6654 Comm: kworker/u32:28 Tainted: P        W  O       6.2.0-37-generic #38~22.04.1-Ubuntu
Dec  4 22:39:05 Blade kernel: [ 1118.585313] Hardware name: Razer Blade 14 - RZ09-0370/PI411, BIOS 1.06 06/07/2021
Dec  4 22:39:05 Blade kernel: [ 1118.585315] Workqueue: amdgpu-reset-dev drm_sched_job_timedout [gpu_sched]
Dec  4 22:39:05 Blade kernel: [ 1118.585321] RIP: 0010:amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.585487] Code: 31 f6 31 ff e9 bd 36 7a c5 44 89 ea 4c 89 e6 4c 89 f7 e8 8f fc ff ff 5b 41 5c 41 5d 41 5e 5d 31 d2 31 f6 31 ff e9 9c 36 7a c5 <0f> 0b b8 ea ff ff ff eb c3 b8 ea ff ff ff eb bc b8 fe ff ff ff eb
Dec  4 22:39:05 Blade kernel: [ 1118.585490] RSP: 0018:ffffbf7947777c08 EFLAGS: 00010246
Dec  4 22:39:05 Blade kernel: [ 1118.585493] RAX: 0000000000000000 RBX: 0000000000000001 RCX: 0000000000000000
Dec  4 22:39:05 Blade kernel: [ 1118.585494] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
Dec  4 22:39:05 Blade kernel: [ 1118.585496] RBP: ffffbf7947777c28 R08: 0000000000000000 R09: 0000000000000000
Dec  4 22:39:05 Blade kernel: [ 1118.585497] R10: 0000000000000000 R11: 0000000000000000 R12: ffff9a1b6bc0bed8
Dec  4 22:39:05 Blade kernel: [ 1118.585499] R13: 0000000000000000 R14: ffff9a1b6bc00000 R15: ffff9a1b6bc00000
Dec  4 22:39:05 Blade kernel: [ 1118.585500] FS:  0000000000000000(0000) GS:ffff9a1e1e9c0000(0000) knlGS:0000000000000000
Dec  4 22:39:05 Blade kernel: [ 1118.585502] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Dec  4 22:39:05 Blade kernel: [ 1118.585504] CR2: 000025e0054bc000 CR3: 0000000141a10000 CR4: 0000000000750ee0
Dec  4 22:39:05 Blade kernel: [ 1118.585506] PKRU: 55555554
Dec  4 22:39:05 Blade kernel: [ 1118.585507] Call Trace:
Dec  4 22:39:05 Blade kernel: [ 1118.585509]  <TASK>
Dec  4 22:39:05 Blade kernel: [ 1118.585510]  ? show_regs+0x72/0x90
Dec  4 22:39:05 Blade kernel: [ 1118.585514]  ? amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.585676]  ? __warn+0x8d/0x160
Dec  4 22:39:05 Blade kernel: [ 1118.585680]  ? amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.585842]  ? report_bug+0x1bb/0x1d0
Dec  4 22:39:05 Blade kernel: [ 1118.585846]  ? handle_bug+0x46/0x90
Dec  4 22:39:05 Blade kernel: [ 1118.585849]  ? exc_invalid_op+0x19/0x80
Dec  4 22:39:05 Blade kernel: [ 1118.585852]  ? asm_exc_invalid_op+0x1b/0x20
Dec  4 22:39:05 Blade kernel: [ 1118.585858]  ? amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.586022]  ? amdgpu_irq_put+0x59/0xc0 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.586183]  gfx_v9_0_hw_fini+0x47/0x370 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.586356]  gfx_v9_0_suspend+0xe/0x20 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.586552]  amdgpu_device_ip_suspend_phase2+0x25d/0x490 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.586680]  amdgpu_device_ip_suspend+0x41/0x80 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.586806]  amdgpu_device_pre_asic_reset+0xd6/0x4a0 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.586934]  amdgpu_device_gpu_recover+0x49f/0xa20 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.587062]  amdgpu_job_timedout+0x13a/0x200 [amdgpu]
Dec  4 22:39:05 Blade kernel: [ 1118.587249]  drm_sched_job_timedout+0x6d/0x120 [gpu_sched]
Dec  4 22:39:05 Blade kernel: [ 1118.587255]  process_one_work+0x21f/0x440
Dec  4 22:39:05 Blade kernel: [ 1118.587259]  worker_thread+0x50/0x3f0
Dec  4 22:39:05 Blade kernel: [ 1118.587263]  ? __pfx_worker_thread+0x10/0x10
Dec  4 22:39:05 Blade kernel: [ 1118.587266]  kthread+0xee/0x120
Dec  4 22:39:05 Blade kernel: [ 1118.587269]  ? __pfx_kthread+0x10/0x10
Dec  4 22:39:05 Blade kernel: [ 1118.587272]  ret_from_fork+0x2c/0x50
Dec  4 22:39:05 Blade kernel: [ 1118.587277]  </TASK>
Dec  4 22:39:05 Blade kernel: [ 1118.587279] ---[ end trace 0000000000000000 ]---
Dec  4 22:39:05 Blade kernel: [ 1118.621285] ------------[ cut here ]------------
```

---

### 评论 #7 — aitorpazos (2024-07-31T23:09:44Z)

Getting this on our servers from time to time:

```
$ uname -a
Linux dfw1-pc1-012 5.15.149-1-pve #1 SMP PVE 5.15.149-1 (2024-03-29T14:24Z) x86_64 GNU/Linux

$ cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"

$ lspci | grep -i display
03:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
27:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
43:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
63:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
83:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
a3:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
c3:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
e3:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Arcturus GL-XL [AMD Instinct MI100] (rev 01)
```

```
[Wed Jul 31 16:25:52 2024] ------------[ cut here ]------------
[Wed Jul 31 16:25:52 2024] WARNING: CPU: 9 PID: 2194086 at /tmp/amd.D7iT57ed/amd/amdgpu/amdgpu_irq.c:624 amdgpu_irq_put+0x94/0xb0 [amdgpu]
[Wed Jul 31 16:25:52 2024] Modules linked in: ufs qnx4 hfsplus hfs minix ntfs msdos jfs cpuid udp_diag nbd rbd libceph tcp_diag inet_diag xt_CT iptable_raw ip_set cls_bpf sch_ingress nf_tables wireguard curve25519_x86_64 libchacha20poly1305 chacha_x86_64 poly1305_x86_64 libcurve25519_generic libchacha ip6_udp_tunnel udp_tunnel xt_multiport xt_nat xt_tcpudp veth ip6table_filter ip6table_nat ip6table_mangle ip6_tables xt_mark xt_comment iptable_mangle xt_conntrack xt_MASQUERADE nf_conntrack_netlink nfnetlink xfrm_user xfrm_algo iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype iptable_filter bpfilter aufs isofs nls_iso8859_1 xfs dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua intel_rapl_msr intel_rapl_common kvm_amd ccp input_leds kvm joydev serio_raw mac_hid qemu_fw_cfg sch_fq_codel msr br_netfilter bridge stp llc overlay ramoops reed_solomon pstore_blk pstore_zone efi_pstore ip_tables x_tables autofs4 btrfs blake2b_generic zstd_compress raid10 raid456 async_raid6_recov
[Wed Jul 31 16:25:52 2024]  async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear mlx5_ib ib_uverbs ib_core amdgpu(OE) hid_generic usbhid hid amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) mlx5_core amdkcl(OE) i2c_algo_bit drm_kms_helper pci_hyperv_intf crct10dif_pclmul syscopyarea crc32_pclmul sysfillrect ghash_clmulni_intel sysimgblt fb_sys_fops mlxfw sha256_ssse3 sha1_ssse3 virtio_net cec rc_core psample aesni_intel net_failover crypto_simd cryptd drm psmouse tls failover virtio_scsi i2c_piix4 pata_acpi floppy
[Wed Jul 31 16:25:52 2024] CPU: 9 PID: 2194086 Comm: kworker/u24:0 Tainted: G        W  OE     5.15.0-116-generic #126~20.04.1-Ubuntu
[Wed Jul 31 16:25:52 2024] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS rel-1.16.1-0-g3208b098f51a-prebuilt.qemu.org 04/01/2014
[Wed Jul 31 16:25:52 2024] Workqueue: amdgpu-reset-hive amdgpu_amdkfd_reset_work [amdgpu]
[Wed Jul 31 16:25:52 2024] RIP: 0010:amdgpu_irq_put+0x94/0xb0 [amdgpu]
[Wed Jul 31 16:25:52 2024] Code: 74 0d 5b 41 5c 41 5d 41 5e 5d e9 d7 c9 e1 e1 44 89 ea 4c 89 e6 4c 89 f7 e8 d9 fc ff ff 5b 41 5c 41 5d 41 5e 5d e9 bc c9 e1 e1 <0f> 0b b8 ea ff ff ff eb cf b8 ea ff ff ff eb c8 b8 fe ff ff ff eb
[Wed Jul 31 16:25:52 2024] RSP: 0018:ffffacabd5d3bc78 EFLAGS: 00010246
[Wed Jul 31 16:25:52 2024] RAX: 0000000000000000 RBX: 0000000000000001 RCX: ffff9327a86fe330
[Wed Jul 31 16:25:52 2024] RDX: 0000000000000000 RSI: ffffffffc1342680 RDI: ffff933839280000
[Wed Jul 31 16:25:52 2024] RBP: ffffacabd5d3bc98 R08: 0000000000000000 R09: 0000000000000003
[Wed Jul 31 16:25:52 2024] R10: ffffffffa4c3e80a R11: 00000000a4c3e7d6 R12: ffff9338392a4ff8
[Wed Jul 31 16:25:52 2024] R13: 0000000000000000 R14: ffff933839280000 R15: ffff933839280000
[Wed Jul 31 16:25:52 2024] FS:  0000000000000000(0000) GS:ffff9422bfc40000(0000) knlGS:0000000000000000
[Wed Jul 31 16:25:52 2024] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[Wed Jul 31 16:25:52 2024] CR2: 000000c0000a5040 CR3: 0000010017d32006 CR4: 0000000000770ee0
[Wed Jul 31 16:25:52 2024] PKRU: 55555554
[Wed Jul 31 16:25:52 2024] Call Trace:
[Wed Jul 31 16:25:52 2024]  <TASK>
[Wed Jul 31 16:25:52 2024]  ? show_regs.cold+0x1a/0x1f
[Wed Jul 31 16:25:52 2024]  ? amdgpu_irq_put+0x94/0xb0 [amdgpu]
[Wed Jul 31 16:25:52 2024]  ? __warn+0x8b/0xe0
[Wed Jul 31 16:25:52 2024]  ? amdgpu_irq_put+0x94/0xb0 [amdgpu]
[Wed Jul 31 16:25:52 2024]  ? report_bug+0xd5/0x110
[Wed Jul 31 16:25:52 2024]  ? handle_bug+0x39/0x90
[Wed Jul 31 16:25:52 2024]  ? exc_invalid_op+0x19/0x70
[Wed Jul 31 16:25:52 2024]  ? asm_exc_invalid_op+0x1b/0x20
[Wed Jul 31 16:25:52 2024]  ? amdgpu_irq_put+0x94/0xb0 [amdgpu]
[Wed Jul 31 16:25:52 2024]  ? amdgpu_irq_put+0x55/0xb0 [amdgpu]
[Wed Jul 31 16:25:52 2024]  gfx_v9_0_hw_fini+0x61/0x970 [amdgpu]
[Wed Jul 31 16:25:52 2024]  ? sdma_v4_0_hw_fini+0x73/0xb0 [amdgpu]
[Wed Jul 31 16:25:52 2024]  gfx_v9_0_suspend+0xe/0x20 [amdgpu]
[Wed Jul 31 16:25:52 2024]  amdgpu_device_ip_suspend_phase2+0x260/0x490 [amdgpu]
[Wed Jul 31 16:25:52 2024]  amdgpu_device_ip_suspend+0x47/0x80 [amdgpu]
[Wed Jul 31 16:25:52 2024]  amdgpu_device_pre_asic_reset+0xd6/0x490 [amdgpu]
[Wed Jul 31 16:25:52 2024]  amdgpu_device_gpu_recover.cold+0x4d8/0xbed [amdgpu]
[Wed Jul 31 16:25:52 2024]  amdgpu_amdkfd_reset_work+0x4c/0x70 [amdgpu]
[Wed Jul 31 16:25:52 2024]  process_one_work+0x22b/0x3d0
[Wed Jul 31 16:25:52 2024]  worker_thread+0x4d/0x3f0
[Wed Jul 31 16:25:52 2024]  ? process_one_work+0x3d0/0x3d0
[Wed Jul 31 16:25:52 2024]  kthread+0x12a/0x150
[Wed Jul 31 16:25:52 2024]  ? set_kthread_struct+0x50/0x50
[Wed Jul 31 16:25:52 2024]  ret_from_fork+0x22/0x30
[Wed Jul 31 16:25:52 2024]  </TASK>
[Wed Jul 31 16:25:52 2024] ---[ end trace 953f02f4bb8dff17 ]---
```

---
