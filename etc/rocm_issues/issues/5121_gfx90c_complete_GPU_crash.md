# gfx90c complete GPU crash

> **Issue #5121**
> **状态**: closed
> **创建时间**: 2025-07-30T14:40:12Z
> **更新时间**: 2025-10-31T22:31:03Z
> **关闭时间**: 2025-07-31T20:53:36Z
> **作者**: DocMAX
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5121

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I try to run ollama / comfyui accelerated with ROCM on older Cezanne APU. I am using HSA_OVERRIDE_GFX_VERSION=9.0.0. But as soon i use ROCM anywhere i get a terrible crash. GPU driver doesn't work anymore. I can't reset/reload the kernel module. GPU is completly out of action. All i can do is reboot. How can software crash a GPU so badly??
```
[Mi Jul 30 16:12:30 2025]  </TASK>
[Mi Jul 30 16:12:30 2025] ---[ end trace 0000000000000000 ]---
[Mi Jul 30 16:12:30 2025] ------------[ cut here ]------------
[Mi Jul 30 16:12:30 2025] WARNING: CPU: 6 PID: 157011 at drivers/gpu/drm/amd/amdgpu/../display/amdgpu_dm/amdgpu_dm.c:8815 amdgpu_dm_atomic_commit_tail+0x36b5/0x3770 [amdgpu]
[Mi Jul 30 16:12:30 2025] Modules linked in: nft_chain_nat nft_compat wireguard curve25519_x86_64 libchacha20poly1305 chacha_x86_64 poly1305_x86_64 libcurve25519_generic libchacha udp_diag tcp_diag inet_diag ib_core nf_conntrack_netlink xt_nat xt_tcpudp xt_conntrack xt_MASQ
UERADE ip6table_nat xt_set iptable_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype xfrm_user xfrm_algo overlay cfg80211 veth rpcsec_gss_krb5 nfsv4 nfs netfs ebtable_filter ebtables ip_set ip6table_raw iptable_raw ip6table_filter ip6_tables iptable_filter s
ctp ip6_udp_tunnel udp_tunnel scsi_transport_iscsi nf_tables nvme_fabrics nvme_keyring bonding tls hid_logitech_hidpp qrtr hid_logitech_dj joydev input_leds cmac algif_hash algif_skcipher af_alg bnep softdog vhost_net vhost vhost_iotlb tap nbd hid_generic usbmouse usbkbd us
bhid hid hwmon_vid vhci_hcd amd_atl intel_rapl_msr intel_rapl_common amdgpu edac_mce_amd snd_sof_amd_acp70 snd_sof_amd_acp63 snd_sof_amd_vangogh snd_sof_amd_rembrandt snd_sof_amd_renoir snd_hda_codec_realtek snd_sof_amd_acp
[Mi Jul 30 16:12:30 2025]  snd_sof_pci snd_hda_codec_generic snd_sof_xtensa_dsp snd_hda_scodec_component snd_sof snd_hda_codec_hdmi snd_sof_utils snd_pci_ps snd_hda_intel snd_soc_acpi_amd_match snd_amd_sdw_acpi vfio_pci kvm_amd soundwire_amd vfio_pci_core soundwire_generic_
allocation binfmt_misc soundwire_bus vfio_iommu_type1 snd_soc_sdca vfio kvm iommufd snd_soc_core snd_intel_dspcfg amdxcp snd_intel_sdw_acpi irqbypass gpu_sched polyval_clmulni snd_compress btusb polyval_generic drm_panel_backlight_quirks ac97_bus snd_hda_codec ghash_clmulni
_intel drm_buddy snd_pcm_dmaengine btrtl sha256_ssse3 drm_ttm_helper snd_rpl_pci_acp6x sha1_ssse3 btintel snd_acp_pci snd_hda_core ttm aesni_intel snd_acp_legacy_common btbcm nfnetlink_log snd_pci_acp6x drm_exec btmtk snd_hwdep snd_pci_acp5x crypto_simd drm_suballoc_helper
nfnetlink bluetooth drm_display_helper snd_pcm cryptd snd_rn_pci_acp3x snd_acp_config snd_timer cec rapl snd_soc_acpi rc_core ee1004 pcspkr snd i2c_algo_bit eeepc_wmi snd_pci_acp3x ccp soundcore ucsi_acpi k10temp zfs(PO)
[Mi Jul 30 16:12:30 2025]  asus_nb_wmi wmi_bmof typec_ucsi typec serial_multi_instantiate spl(O) mac_hid nfsd auth_rpcgss nfs_acl lockd usbip_host usbip_core grace msr efi_pstore sunrpc dmi_sysfs ip_tables x_tables autofs4 uas btrfs blake2b_generic usb_storage raid10 raid45
6 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq raid1 raid0 linear mfd_aaeon nvme asus_wmi sparse_keymap xhci_pci platform_profile ahci r8169 nvme_core i2c_piix4 libahci xhci_hcd i2c_smbus nvme_auth realtek video wmi
[Mi Jul 30 16:12:30 2025] CPU: 6 UID: 0 PID: 157011 Comm: kworker/6:0 Tainted: P      D W  O       6.14.8-2-bpo12-pve #1
[Mi Jul 30 16:12:30 2025] Tainted: [P]=PROPRIETARY_MODULE, [D]=DIE, [W]=WARN, [O]=OOT_MODULE
[Mi Jul 30 16:12:30 2025] Hardware name: ASUSTeK COMPUTER INC. MINIPC PN52/PN52, BIOS 12100 02/15/2024
[Mi Jul 30 16:12:30 2025] Workqueue: events drm_fb_helper_damage_work
[Mi Jul 30 16:12:30 2025] RIP: 0010:amdgpu_dm_atomic_commit_tail+0x36b5/0x3770 [amdgpu]
[Mi Jul 30 16:12:30 2025] Code: f1 b6 67 cd 41 83 7c 24 7c 01 48 8b 85 58 fe ff ff 41 0f 94 c6 e9 66 db ff ff 0f 0b e9 0c f9 ff ff 0f 0b 0f 0b e9 87 d0 ff ff <0f> 0b e9 1b f9 ff ff 48 8b 85 38 fe ff ff be 01 00 00 00 4c 89 9d
[Mi Jul 30 16:12:30 2025] RSP: 0018:ffffb692a0a93998 EFLAGS: 00010086
[Mi Jul 30 16:12:30 2025] RAX: 0000000000000001 RBX: 0000000000000246 RCX: 0000000000000000
[Mi Jul 30 16:12:30 2025] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
[Mi Jul 30 16:12:30 2025] RBP: ffffb692a0a93be0 R08: 0000000000000000 R09: 0000000000000000
[Mi Jul 30 16:12:30 2025] R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
[Mi Jul 30 16:12:30 2025] R13: ffff906afa480010 R14: ffff906e06b6be00 R15: ffff906ad8b5c000
[Mi Jul 30 16:12:30 2025] FS:  0000000000000000(0000) GS:ffff90798af00000(0000) knlGS:0000000000000000
[Mi Jul 30 16:12:30 2025] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[Mi Jul 30 16:12:30 2025] CR2: 00007d29338a8000 CR3: 0000000fcda38000 CR4: 0000000000f50ef0
[Mi Jul 30 16:12:30 2025] PKRU: 55555554
[Mi Jul 30 16:12:30 2025] Call Trace:
[Mi Jul 30 16:12:30 2025]  <TASK>
[Mi Jul 30 16:12:30 2025]  ? srso_alias_return_thunk+0x5/0xfbef5
[Mi Jul 30 16:12:30 2025]  ? dev_printk_emit+0xa1/0xe0
[Mi Jul 30 16:12:30 2025]  ? srso_alias_return_thunk+0x5/0xfbef5
[Mi Jul 30 16:12:30 2025]  ? __dev_printk+0x39/0xa0
[Mi Jul 30 16:12:30 2025]  ? srso_alias_return_thunk+0x5/0xfbef5
[Mi Jul 30 16:12:30 2025]  ? _dev_err+0x75/0xa0
[Mi Jul 30 16:12:30 2025]  commit_tail+0xc2/0x190
[Mi Jul 30 16:12:30 2025]  ? srso_alias_return_thunk+0x5/0xfbef5
[Mi Jul 30 16:12:30 2025]  ? drm_atomic_helper_swap_state+0x2f4/0x390
[Mi Jul 30 16:12:30 2025]  drm_atomic_helper_commit+0x11d/0x150
[Mi Jul 30 16:12:30 2025]  drm_atomic_commit+0xb0/0xf0
[Mi Jul 30 16:12:30 2025]  ? __pfx___drm_printfn_info+0x10/0x10
[Mi Jul 30 16:12:30 2025]  drm_atomic_helper_dirtyfb+0x1a2/0x290
[Mi Jul 30 16:12:30 2025]  amdgpu_dirtyfb+0x13/0x40 [amdgpu]
[Mi Jul 30 16:12:30 2025]  drm_fbdev_ttm_helper_fb_dirty+0x272/0x367 [drm_ttm_helper]
[Mi Jul 30 16:12:30 2025]  drm_fb_helper_damage_work+0x97/0x180
[Mi Jul 30 16:12:30 2025]  process_one_work+0x17b/0x3b0
[Mi Jul 30 16:12:30 2025]  worker_thread+0x2b8/0x3e0
[Mi Jul 30 16:12:30 2025]  ? __pfx_worker_thread+0x10/0x10
[Mi Jul 30 16:12:30 2025]  kthread+0xfe/0x230
[Mi Jul 30 16:12:30 2025]  ? __pfx_kthread+0x10/0x10
[Mi Jul 30 16:12:30 2025]  ret_from_fork+0x47/0x70
[Mi Jul 30 16:12:30 2025]  ? __pfx_kthread+0x10/0x10
[Mi Jul 30 16:12:30 2025]  ret_from_fork_asm+0x1a/0x30
[Mi Jul 30 16:12:30 2025]  </TASK>
[Mi Jul 30 16:12:30 2025] ---[ end trace 0000000000000000 ]---
[Mi Jul 30 16:12:31 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x000B4140, 0x0002D500, 0x00034160)
[Mi Jul 30 16:12:32 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x000A12C0, 0x0001D8E0, 0x000212E0)
[Mi Jul 30 16:12:32 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x000A1240, 0x000216C0, 0x00021260)
[Mi Jul 30 16:12:32 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x00081100, 0x0003B440, 0x00001120)
[Mi Jul 30 16:12:32 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x00091060, 0x000098C0, 0x00011080)
[Mi Jul 30 16:12:35 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x00088080, 0x000065A0, 0x000080A0)
[Mi Jul 30 16:12:35 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x00097FE0, 0x0000B300, 0x00018000)
[Mi Jul 30 16:12:36 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x000888E0, 0x0003F1E0, 0x00008900)
[Mi Jul 30 16:12:36 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x00098840, 0x000127E0, 0x00018860)
[Mi Jul 30 16:12:36 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x000A8820, 0x00021F80, 0x00028840)
[Mi Jul 30 16:12:36 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x000850E0, 0x0003EC60, 0x00005100)
[Mi Jul 30 16:12:36 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x00095040, 0x00008B20, 0x00015060)
[Mi Jul 30 16:12:39 2025] amdgpu 0000:06:00.0: amdgpu: ih ring buffer overflow (0x000B8200, 0x000315C0, 0x00038220)
```

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-07-30T14:43:03Z)

Hi @DocMAX. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — tcgu-amd (2025-07-31T17:48:12Z)

Hi @DocMAX, thank you for reaching out, and sorry that you are experiencing crashes. Which version of ROCm and driver are you running? Both gfx900 and gfx90c has been out of support for a while. Also, please use `HSA_OVERRIDE_GFX_VERSION=9.0.0` with caution; it might look magical but it is really forcing the device to run binaries compiled for a different architecture, which might cause corruptions and lead to crashes such as this. 

---

### 评论 #3 — DocMAX (2025-07-31T19:01:56Z)

I am using this project https://github.com/rjmalagon/ollama-linux-amd-apu which offers versions with ROCm 6.4.2 and 6.3.4 (for older cards). It used to work without crashes a while ago. But now both versions crash. After research it seems i have to stick with ROCm 5.7.3, which has last gfx90c support.
It's ok if hardware gets out of support, but please don't let the driver crash so badly that even a GPU reset doesn't prevent you from doing a force reboot.
Edit: ROCm 5.7.3 seems to work. So thank you for the hint to check ROCm's version. Too bad you drop support so quickly for "old" CPUs.

---

### 评论 #4 — tcgu-amd (2025-07-31T20:53:36Z)

> I am using this project https://github.com/rjmalagon/ollama-linux-amd-apu which offers versions with ROCm 6.4.2 and 6.3.4 (for older cards). It used to work without crashes a while ago. But now both versions crash. After research it seems i have to stick with ROCm 5.7.3, which has last gfx90c support. It's ok if hardware gets out of support, but please don't let the driver crash so badly that even a GPU reset doesn't prevent you from doing a force reboot. Edit: ROCm 5.7.3 seems to work. So thank you for the hint to check ROCm's version. Too bad you drop support so quickly for "old" CPUs.

Hi @DocMAX, yes...dropped support for (not so much) "older" cards has been a major complaint for a while, and we have been actually shifting focus to improve this aspect (https://github.com/ROCm/ROCm/discussions/4276). Hopefully, things will improve in the near future and we can revitalize cards from some of our older lineups.  

As for driver stability, we are always working on improving it. However. ROCm compiles directly to instructions, so when env vars such as `HSA_OVERRIDE_GFX_VERSION` are used with binary compiled for majorly different instruction sets, it can really derail the entire stack. The use of this env variable is suggested a lot, but it was frankly never really meant to be an official workaround. It is worth keep a note of this and use the override env var carefully. 

Still, we really appreciate your feedback, and hopefully your experience with ROCm will only improve from now on. 

I will be closing this issue for now, but please feel free to follow up with more questions!

Thanks! 

---

### 评论 #5 — DocMAX (2025-07-31T21:10:22Z)

All right, thank YOU. Much clearer to me now how all works. Better backward compatibility would be great. Keep up the good work.

---

### 评论 #6 — yhojann-cl (2025-10-31T22:28:57Z)

For `ih ring buffer overflow` or `ring gfx timeout` using amdgpu says this tikcet: https://gitlab.freedesktop.org/drm/amd/-/issues/3067

As mentioned, the problem is not the driver error itself, but rather that the environment is unable to handle the error and recover. This causes the entire system to crash under different conditions when the GPU fails to process information from the shader compiler, RDNA, and similar sources. GDM, GNOME, Wayland, X, and everything else crashes, causing a massive process shutdown—essentially forcing the user to log out. The same thing happens in some AI processing equipment with ROCM; there is a lack of control in the handling of this type of error.

---
