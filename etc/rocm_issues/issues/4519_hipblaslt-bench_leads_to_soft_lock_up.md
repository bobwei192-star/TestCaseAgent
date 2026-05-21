# hipblaslt-bench leads to soft lock up

> **Issue #4519**
> **状态**: closed
> **创建时间**: 2025-03-21T17:52:02Z
> **更新时间**: 2025-05-26T19:20:54Z
> **关闭时间**: 2025-05-26T19:20:53Z
> **作者**: mysoreanoop
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4519

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

When running hipblaslt-bench in gem5, with AMD_LOG_LEVEL=4, I see the following printed:
```
...
:3:rocvirtual.cpp           :799 : 7052618032 us: [pid:461   tid:0x7f1072d6c8c0] Arg26:  activationAlpha = val:0
:3:rocvirtual.cpp           :799 : 7052623667 us: [pid:461   tid:0x7f1072d6c8c0] Arg27:  activationBeta = val:0
:3:rocvirtual.cpp           :799 : 7052629285 us: [pid:461   tid:0x7f1072d6c8c0] Arg28:  activationType = val:0
:3:rocvirtual.cpp           :3028: 7052634827 us: [pid:461   tid:0x7f1072d6c8c0] ShaderName : Cijk_Ailk_Bljk_BBS_BH_Bias_HAS_SAV_UserArgs_MT16x16x256_MI16x16x1_SN_LDSB1_AFC1_AFEM1_AFEM1_ASEM1_CLR1_CADS0_DTVA0_DTVB0_EPS0_FDSI0_GRPM1_GRVWA8_GRVWB8_GSUAMB_GLS0_ISA942_K1_LBSPPA256_LBSPPB512_LBSPPM0_LPA16_LPB16_LPM0_LRVW8_LWPMn1_MIAV0_MIWT1_1_MO40_NTn1_NTA0_NTB0_NTC0_NTD4_NTM0_NEPBS16_NLCA1_NLCB1_ONLL1_PGR2_PLR1_PKA1_SIA3_SS1_SPO0_SRVW0_SSO0_SVW1_SK0_SKXCCM0_TLDS1_ULSGRO0_USL1_UIOFGRO0_USFGROn1_VSn1_VWA1_VWB1_WSGRA0_WSGRB0_WG16_4_4
:4:rocvirtual.cpp           :901 : 7052670730 us: [pid:461   tid:0x7f1072d6c8c0] SWq=0x7f1072cba000, HWq=0x7f0f70600000, id=2, Dispatch Header = 0xb02 (type=2, barrier=1, acquire=1, release=1), setup=3, grid=[16384, 1, 1], workgroup=[256, 1, 1], private_seg_size=0, group_seg_size=17920, kernel_obj=0x7f0f353d4680, kernarg_address=0x7f0f70900000, completion_signal=0x0, correlation_id=0, rptr=1, wptr=1
:3:hip_module.cpp           :478 : 7052689609 us: [pid:461   tid:0x7f1072d6c8c0] hipExtModuleLaunchKernel: Returned hipSuccess : [ 9697.806922] watchdog: BUG: soft lockup - CPU#0 stuck for 2464s! [hipblaslt-bench:461]
[10465.791198] Modules linked in: ib_uverbs ib_core amdgpu(OE) amddrm_ttm_helper(OE) amdttm(OE) amdxcp(OE) amddrm_buddy(OE) amd_sched(OE) amdkcl(OE) drm_kms_helper cec rc_core i2c_algo_bit fb_sys_fops syscopyarea sysfillrect sysimgblt binfmt_misc pata_acpi edac_mce_amd sha256_ssse3 input_leds mac_hid sha1_ssse3 serio_raw sch_fq_codel dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua drm efi_pstore ip_tables x_tables autofs4
[14190.498369] CPU: 0 PID: 461 Comm: hipblaslt-bench Tainted: G           OEL    5.15.0-134-generic #145-Ubuntu
[15205.735783] Hardware name:  , BIOS  06/08/2008
[15669.825901] RIP: 0010:_raw_spin_unlock_irqrestore+0x25/0x30
[16254.383545] Code: eb 8d cc cc cc 0f 1f 44 00 00 55 48 89 e5 c6 07 00 0f 1f 40 00 f7 c6 00 02 00 00 75 06 5d c3 cc cc cc cc fb 66 0f 1f 44 00 00 <5d> c3 cc cc cc cc 0f 1f 44 00 00 0f 1f 44 00 00 55 48 89 e5 8b 07
[18117.182426] RSP: 0018:ffffc9000096bb60 EFLAGS: 00000206
[18658.316008] RAX: 0000000000000007 RBX: ffffffff844294c0 RCX: 0000000000000000
[19377.874013] RDX: 00000000000003f9 R
```
What does a soft lock up indicate? I realize because I'm running it in gem5, it may not be the most pertinent issue here, but I'd really appreciate some insight into why this usually happens on the hardware. Thanks in advance!

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-03-24T15:54:36Z)

Hi @mysoreanoop. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2025-03-24T18:35:38Z)

Hi @mysoreanoop, could you provide some more output from before and after this segment? From the provided output it looks like the reported soft hang occurred when a kernel was launched on the GPU, with the CPU waiting for a completion signal. Given that the kernel eventually completed I think this is normal and that the hipblaslt-bench workload simply a takes a while to execute. Is gem5 reporting a soft hang here based on some diagnostics, or is it just raising a warning due to the long runtime?

I haven't personally seen soft hangs on baremetal in similar contexts, but I've seen hard hangs under certain conditions (usually missing PCIe atomics or bad code).

---

### 评论 #3 — schung-amd (2025-05-26T19:20:53Z)

Closing for now due to lack of response, feel free to comment if you need further guidance on this and we can reopen if necessary.

---
