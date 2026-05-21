# RDNA 3 - ROCm 5.7 GPU resets

> **Issue #2533**
> **状态**: closed
> **创建时间**: 2023-10-07T11:17:33Z
> **更新时间**: 2023-12-26T07:33:20Z
> **关闭时间**: 2023-11-09T20:35:22Z
> **作者**: arch-user-france1
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2533

## 描述

Unfortunately, there seem to be issues with the driver relating to GPU resets on the AMD Radeon RX 7900 XT, and I have not managed to run any model without the graphics card crashing after some time. Language models do work most of the time, however, they are evaluated at a speed slower than the CPU achieves. The resets may result in a completely frozen user interface or the python process continuing to run forever (see log).

```
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2237.944235] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma0 timeout, signaled seq=16060, emitted seq=16062
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2237.944505] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process  pid 0 thread  pid 0
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2237.944732] amdgpu 0000:0a:00.0: amdgpu: GPU reset begin!
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.057431] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=3
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.057611] amdgpu: failed to remove hardware queue from MES, doorbell=0x1002
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.057613] amdgpu: MES might be in unrecoverable state, issue a GPU reset
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.057615] amdgpu: Failed to evict queue 1
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.057616] amdgpu: Failed to evict process queues
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.057618] amdgpu: Failed to suspend process 0x800d
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.057715] amdgpu 0000:0a:00.0: amdgpu: Guilty job already signaled, skipping HW reset
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.169415] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.169683] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.186831] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:23 Ubuntu-Desktop kernel: [ 2238.187108] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.279554] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.279780] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.294247] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.294514] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.391966] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.392182] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.504348] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.504571] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.616691] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.616902] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.625656] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.625855] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.728998] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.729234] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.738281] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.738458] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.841477] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.841674] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.858356] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] *ERROR* MES failed to response msg=14
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.858552] [drm:amdgpu_mes_reg_write_reg_wait [amdgpu]] *ERROR* failed to reg_write_reg_wait
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.947496] [drm] ring gfx_32782.1.1 was added
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.947895] [drm] ring compute_32782.2.2 was added
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2238.948260] [drm] ring sdma_32782.3.3 was added
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2239.204243] amdgpu 0000:0a:00.0: [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* ring gfx_32782.1.1 test failed (-110)
Oct  7 12:58:24 Ubuntu-Desktop kernel: [ 2239.204868] amdgpu 0000:0a:00.0: amdgpu: GPU reset(1) succeeded!
```


```python
def label_func(filePath):
  return filePath.parent.name

if Augment_Data: # was on False
  # define augmentations
  augmentation_tfms = aug_transforms(
      do_flip=False,
      flip_vert=False,
      max_rotate=10.0, 
      max_zoom=0, 
      max_lighting=0.3, 
      max_warp=0.1,
      p_affine=0.75,
      p_lighting=0.75
  )

dls = ImageDataLoaders.from_path_func(
    image_directory_path,
    get_image_files(image_directory_path),
    valid_pct=0.2,
    bs=train_batchSize, # set to 256, working well on GeForce 1660 Super (below this GPU's total vram available)
    shuffle=True,
    label_func=label_func,
    device=device, # "cuda:0"
    batch_tfms=augmentation_tfms if Augment_Data else None, # load augmentations if Augment_Data=True
)

dls.show_batch()
batch_data, batch_labels = dls.one_batch()
print(batch_data.shape)
print(batch_labels)
```

Result:
![image](https://github.com/RadeonOpenCompute/ROCm/assets/72965843/c0480024-2e15-4bea-91aa-6d06060affb5)


This model was run on FastAI and PyTorch nightly (for rocm 5.7). The device, which was selected by FastAI, is `cuda:0`.


Following information was collected from the logs after the occurrence:
```
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081108] ------------[ cut here ]------------
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081112] WARNING: CPU: 18 PID: 0 at drivers/gpu/drm/amd/amdgpu/amdgpu_irq.c:600 amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081319] Modules linked in: tls xt_conntrack nft_chain_nat xt_MASQUERADE nf_nat nf_conntrack_netlink nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xfrm_user xfrm_algo xt_addrtype nft_compat nf_tables libcrc32c nfnetlink br_netfilter bridge stp llc nvme_fabrics input_leds overlay binfmt_misc zfs(PO) zunicode(PO) zzstd(O) zlua(O) zavl(PO) icp(PO) zcommon(PO) znvpair(PO) spl(O) snd_hda_codec_realtek snd_hda_codec_generic snd_hda_codec_hdmi intel_rapl_msr intel_rapl_common nls_iso8859_1 snd_hda_intel edac_mce_amd snd_intel_dspcfg snd_intel_sdw_acpi snd_hda_codec snd_hda_core snd_hwdep snd_pcm kvm irqbypass snd_seq_midi crct10dif_pclmul polyval_clmulni polyval_generic snd_seq_midi_event ghash_clmulni_intel sha512_ssse3 aesni_intel snd_rawmidi crypto_simd cryptd rapl snd_seq joydev snd_seq_device snd_timer eeepc_wmi wmi_bmof snd k10temp ccp soundcore mac_hid sch_fq_codel msr parport_pc ppdev lp parport efi_pstore ip_tables x_tables autofs4 amdgpu i2c_algo_bit drm_ttm_helper ttm iommu_v2
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081400]  drm_buddy ses gpu_sched enclosure scsi_transport_sas drm_display_helper hid_generic drm_kms_helper mfd_aaeon asus_wmi ucsi_ccg syscopyarea ledtrig_audio sysfillrect typec_ucsi uas sparse_keymap sysimgblt usbhid hid usb_storage typec platform_profile drm nvme cec crc32_pclmul rc_core nvme_core igc i2c_designware_pci video i2c_ccgx_ucsi nvme_common i2c_piix4 ahci xhci_pci libahci xhci_pci_renesas wmi gpio_amdpt
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081442] CPU: 18 PID: 0 Comm: swapper/18 Tainted: P           O       6.2.0-34-generic #34~22.04.1-Ubuntu
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081445] Hardware name: ASUS System Product Name/ROG STRIX B550-A GAMING, BIOS 3002 02/23/2023
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081446] RIP: 0010:amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081596] Code: 31 f6 31 ff e9 ed ba 8d e2 44 89 ea 4c 89 e6 4c 89 f7 e8 8f fc ff ff 5b 41 5c 41 5d 41 5e 5d 31 d2 31 f6 31 ff e9 cc ba 8d e2 <0f> 0b b8 ea ff ff ff eb c3 b8 ea ff ff ff eb bc b8 fe ff ff ff eb
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081598] RSP: 0018:ffffbfa10062cdb0 EFLAGS: 00010046
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081601] RAX: 0000000000000000 RBX: 0000000000000001 RCX: 0000000000000000
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081603] RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081604] RBP: ffffbfa10062cdd0 R08: 0000000000000000 R09: 0000000000000000
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081606] R10: 0000000000000000 R11: 0000000000000000 R12: ffff9a0e5cfa65b8
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081607] R13: 0000000000000000 R14: ffff9a0e5cfa0000 R15: ffff9a0fcfdddc00
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081609] FS:  0000000000000000(0000) GS:ffff9a154ee80000(0000) knlGS:0000000000000000
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081611] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081612] CR2: 00007f602c61ba50 CR3: 0000000114476000 CR4: 0000000000750ee0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081614] PKRU: 55555554
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081615] Call Trace:
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081617]  <IRQ>
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081620]  ? show_regs+0x72/0x90
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081625]  ? amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081769]  ? __warn+0x8d/0x160
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081774]  ? amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081920]  ? report_bug+0x1bb/0x1d0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081925]  ? handle_bug+0x46/0x90
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081929]  ? exc_invalid_op+0x19/0x80
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081932]  ? asm_exc_invalid_op+0x1b/0x20
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.081938]  ? amdgpu_irq_put+0xa4/0xc0 [amdgpu]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082084]  dm_set_vblank+0x1ae/0x1d0 [amdgpu]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082317]  dm_disable_vblank+0x10/0x20 [amdgpu]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082540]  drm_vblank_disable_and_save+0xfd/0x150 [drm]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082565]  vblank_disable_fn+0x74/0xa0 [drm]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082585]  ? __pfx_vblank_disable_fn+0x10/0x10 [drm]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082604]  call_timer_fn+0x2c/0x160
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082608]  ? __pfx_vblank_disable_fn+0x10/0x10 [drm]
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082626]  __run_timers.part.0+0x1fb/0x2b0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082629]  ? ktime_get+0x46/0xc0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082632]  ? __pfx_tick_sched_timer+0x10/0x10
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082635]  ? srso_alias_return_thunk+0x5/0x7f
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082639]  ? srso_alias_return_thunk+0x5/0x7f
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082641]  ? lapic_next_event+0x20/0x30
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082645]  ? srso_alias_return_thunk+0x5/0x7f
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082648]  ? clockevents_program_event+0xb5/0x140
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082651]  run_timer_softirq+0x2a/0x60
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082654]  __do_softirq+0xdd/0x330
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082656]  ? hrtimer_interrupt+0x12b/0x250
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082661]  __irq_exit_rcu+0xa2/0xd0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082663]  irq_exit_rcu+0xe/0x20
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082666]  sysvec_apic_timer_interrupt+0x96/0xb0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082669]  </IRQ>
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082670]  <TASK>
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082672]  asm_sysvec_apic_timer_interrupt+0x1b/0x20
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082675] RIP: 0010:cpuidle_enter_state+0xde/0x6f0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082678] Code: 61 31 5d e8 a4 2b 45 ff 8b 53 04 49 89 c7 0f 1f 44 00 00 31 ff e8 52 0a 44 ff 80 7d d0 00 0f 85 e8 00 00 00 fb 0f 1f 44 00 00 <45> 85 f6 0f 88 0f 02 00 00 4d 63 ee 49 83 fd 09 0f 87 c4 04 00 00
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082680] RSP: 0018:ffffbfa100217e28 EFLAGS: 00000246
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082682] RAX: 0000000000000000 RBX: ffff9a0e45cc4800 RCX: 0000000000000000
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082684] RDX: 0000000000000012 RSI: 0000000000000000 RDI: 0000000000000000
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082685] RBP: ffffbfa100217e78 R08: 0000000000000000 R09: 0000000000000000
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082687] R10: 0000000000000000 R11: 0000000000000000 R12: ffffffffa44d5b60
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082688] R13: 0000000000000002 R14: 0000000000000002 R15: 0000022fbe6590c7
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082693]  ? cpuidle_enter_state+0xce/0x6f0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082697]  cpuidle_enter+0x2e/0x50
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082699]  cpuidle_idle_call+0x14f/0x1e0
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082704]  do_idle+0x82/0x110
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082706]  cpu_startup_entry+0x20/0x30
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082709]  start_secondary+0x122/0x160
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082713]  secondary_startup_64_no_verify+0xe5/0xeb
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082719]  </TASK>
Oct  7 13:01:09 Ubuntu-Desktop kernel: [ 2404.082720] ---[ end trace 0000000000000000 ]---
```


`rocm-smi` reports the following:
```bash
(base) ➜  ~ rocm-smi 


========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU  Temp (DieEdge)  AvgPwr  SCLK    MCLK     Fan     Perf  PwrCap  VRAM%  GPU%  
0    61.0c           70.0W   472Mhz  1249Mhz  24.71%  auto  0.0W      5%   31%   <-------- first call of rocm-smi
====================================================================================
=============================== End of ROCm SMI Log ================================
(base) ➜  ~ rocm-smi


========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU  Temp (DieEdge)  AvgPwr  SCLK    MCLK     Fan     Perf  PwrCap  VRAM%  GPU%  
0    67.0c           77.0W   524Mhz  1249Mhz  27.84%  auto  0.0W      5%   100%  <---------- values stuck in the calls following the first
====================================================================================
=============================== End of ROCm SMI Log ================================
(base) ➜  ~ rocm-smi


========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU  Temp (DieEdge)  AvgPwr  SCLK    MCLK     Fan     Perf  PwrCap  VRAM%  GPU%  
0    67.0c           77.0W   524Mhz  1249Mhz  27.84%  auto  0.0W      5%   100%  
====================================================================================
=============================== End of ROCm SMI Log ================================
```
In this case, the crash has resulted in the GPU being used by 100%, which commonly happens. Killing the python process does not decrease the GPU's utilization. The GPU does not seem to be used by 100% in reality, as its frequency is on a low level.


Suspending the system may temporarily unfreeze these values. Subsequent runs without suspending first of the code results in the same error, but without GPU resets and 100% CPU usage of one thread.

---

## 评论 (11 条)

### 评论 #1 — sdli1995 (2023-10-08T09:11:58Z)

it's a driver problem  it‘s sleep and awake failed it will cause rocm program freeze 
try call rocm-smi 1 time per second 


---

### 评论 #2 — arch-user-france1 (2023-10-08T09:21:23Z)

@sdli1995, I think this indeed may be a driver problem, however, it has nothing to do with sleep/awake. The problem appears while doing ROCm operations, such as seen in creating a PyTorch Dataloader.

---

### 评论 #3 — terryrankine (2023-10-17T02:53:30Z)

I have the same card.
I am happy to replicate/debug
I am having all sorts of issues with 5.7.1 and kernel calls driver reset - card still hangs blocking.

i call hard reset `rocm-smi --gpureset -d 0` and sometimes it resets - other times it still blocks on the next launch and a full power cycle is needed.

running 5.7.1 repo, pytorch nightly, ubuntu 22.04

let me know what other info you need for me to help this out

---

### 评论 #4 — cwjyu (2023-11-05T05:55:29Z)

I had a similar situation with rocm5.7.1 on my 7900xtx, after a few days of trying, I almost solved the problem, but encountered a new problem.
First I tried uninstalling the driver and reinstall it using the following command:
`sudo amdgpu-install --usecase=rocm --rocmrelease=5.7.1 --no-dkms`
Then I ran into the following problem while running my pytorch code
```
 [ 4280.134636] amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:32769, for process python pid 4860 thread python pid 4860)
[ 4280.134637] amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00007f8e3a509000 from client 10
[ 4280.134638] amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801A31
[ 4280.134639] amdgpu 0000:03:00.0: amdgpu: 	 Faulty UTCL2 client ID: SDMA0 (0xd)
[ 4280.134640] amdgpu 0000:03:00.0: amdgpu: 	 MORE_FAULTS: 0x1
[ 4280.134640] amdgpu 0000:03:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[ 4280.134641] amdgpu 0000:03:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[ 4280.134642] amdgpu 0000:03:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[ 4280.134642] amdgpu 0000:03:00.0: amdgpu: 	 RW: 0x0
```
Fortunately, this no longer seems to interrupt the code I'm running

---

### 评论 #5 — arch-user-france1 (2023-11-05T07:57:23Z)

@cwjyu, I am not seeing any crashes in the logs anymore after reinstalling ROCm like you suggested, however, apart from that, I am still observing the code being stuck and `rocm-smi` reporting 100% GPU usage.

---

### 评论 #6 — pingplug (2023-11-05T13:44:54Z)

got the same problem with iGPU in 7840HS while running waifu2x with openCL

---

### 评论 #7 — cwjyu (2023-11-06T05:43:24Z)

> @cwjyu, I am not seeing any crashes in the logs anymore after reinstalling ROCm like you suggested, however, apart from that, I am still observing the code being stuck and `rocm-smi` reporting 100% GPU usage.

@arch-user-france1 After I uninstalled the rocm driver, I also removed the 6.0.26 kernel it installed. Here are the versions of the operating system I use:
`Linux wjy-MS-7D97 6.2.0-36-generic #37~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  9 15:34:04 UTC 2 x86_64 x86_64 x86_64 GNU/Linux`
And I am running my code in another character terminal, because this driver will cause my graphical interface to die, I need to use ctrl+alt+F1 to restart the graphical interface on my operating system, and even ssh to kill the graphical terminal in serious cases.


---

### 评论 #8 — arch-user-france1 (2023-11-09T20:35:22Z)

It seems to be working if the drivers are installed with the `--no-dkms` option. On my Ubuntu 22.04 system, the DKMS does not compile anymore. I think this problem has nothing to do with ROCm itself but rather the installation program, which is why I'll close this issue. I didn't have to remove any kernels, but I did not restart my system but merely run `sudo modprobe amdgpu` after installing the drivers in the apparently correct way.

---

### 评论 #9 — pingplug (2023-11-11T14:56:18Z)

@arch-user-france1  How to do this in arch linux? I'm not using dkms driver but still got this issue.

update:
I switched kernel version from `6.6.1.arch1-1` to `6.5.2.8.realtime1-1-rt`, and the issue was gone.

update:
I still meet this issue, and have tried `iommu=soft`, `sg_display=0` to kernel config. The later one seems to work.

---

### 评论 #10 — plasticchris (2023-12-11T03:46:39Z)

Leaving some links here for the next person who has this problem:

See also https://github.com/ROCm/ROCm/issues/2642 which links to https://github.com/ROCm/ROCm/issues/2596 which links to the kernel patch https://lists.freedesktop.org/archives/amd-gfx/2023-October/100298.html which resolved a similar resetting problem I was having. 

---

### 评论 #11 — sid-cypher (2023-12-26T07:33:19Z)

The issue is closed, but would like to confirm that this bug does not occur for me after upgrading to ROCm 6.0 anymore (my chip is Radeon RX 7900 XTX).
Stable Diffusion with torch-2.3.0+rocm5.7 still works on ROCm 6.0, and without crashes now.

The non-critical GCVM_L2_PROTECTION_FAULT_STATUS errors (mentioned by @cwjyu in the comments above) are still there, but they don't force me to restart after a failed GPU reset.

---
