# [Issue]: RX 6800 GPU reset when using ROCm (GPU not listed but I think it's in error)

> **Issue #2935**
> **状态**: closed
> **创建时间**: 2024-02-28T05:11:03Z
> **更新时间**: 2024-07-04T19:41:49Z
> **关闭时间**: 2024-07-04T19:41:49Z
> **作者**: nonetrix
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT, ROCm 5.5.1
> **URL**: https://github.com/ROCm/ROCm/issues/2935

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 5.5.1** (颜色: #ededed)

## 描述

### Problem Description

note: this GPU isn't listed, but older GPUs like Radeon VII are and they are not enterprise cards so I can only assume this is in error please fix. The RX 6800 is also listed as supported to my understanding by ROCm, so I am very confused why it's not listed in the issue template. If anyone can reproduce this on a card listed in the issue template that would be great I think it's likely issue with all cards, but for now the card listed in the issue template is inaccurate since it's required

I have been having constant crashes where my system will just reboot when trying to generate a image in Stable Diffusion, my screen goes black suddenly, then resets and I usually get a MCE error after that looks like this. I also noticed audio will keep playing, then become distorted and stutter as if the CPU is having a hard time keeping up until it stops completely then resets shortly after 
```
Feb 27 15:09:35 nixos kernel: mce: [Hardware Error]: Machine check events logged
Feb 27 15:09:35 nixos kernel: mce: [Hardware Error]: CPU 9: Machine Check: 0 Bank 5: bea0000000000108
Feb 27 15:09:35 nixos kernel: mce: [Hardware Error]: TSC 0 ADDR 1ffffc0754f4a MISC d012000100000000 SYND 4d000000 IPID 500b000000000
Feb 27 15:09:35 nixos kernel: mce: [Hardware Error]: PROCESSOR 2:870f10 TIME 1709068166 SOCKET 0 APIC 3 microcode 8701030
Feb 27 15:09:36 nixos kernel: MCE: In-kernel MCE decoding enabled.
```
My system is otherwise very stable so it seemed odd not to mention I have played full length games and had zero issues whatsoever, also I have tested the memory it is not the problem. so I decided to try to ssh into my computer from my phone when I get this error and discovered this
```
Feb 27 22:08:15 nixos systemd[1]: Starting Cleanup of Temporary Directories...
Feb 27 22:08:15 nixos systemd[1]: systemd-tmpfiles-clean.service: Deactivated successfully.
Feb 27 22:08:15 nixos systemd[1]: Finished Cleanup of Temporary Directories.
Feb 27 22:08:24 nixos kernel: amdgpu 0000:09:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000028 SMN_C2PMSG_82:0x00000000
Feb 27 22:08:24 nixos kernel: amdgpu 0000:09:00.0: amdgpu: Failed to enable gfxoff!
Feb 27 22:08:29 nixos kernel: amdgpu 0000:09:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000028 SMN_C2PMSG_82:0x00000000
Feb 27 22:08:29 nixos kernel: amdgpu 0000:09:00.0: amdgpu: Failed to enable gfxoff!
Feb 27 22:08:30 nixos kernel: amdgpu 0000:09:00.0: [drm] *ERROR* [CRTC:95:crtc-1] flip_done timed out
Feb 27 22:08:31 nixos kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma0 timeout, signaled seq=3400, emitted seq=3401
Feb 27 22:08:31 nixos kernel: [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process  pid 0 thread  pid 0
Feb 27 22:08:31 nixos kernel: amdgpu 0000:09:00.0: amdgpu: GPU reset begin!
Feb 27 22:08:31 nixos kernel: amdgpu: Failed to suspend process 0x800c
```
I am not a expert in drivers but this seems to be a issue with AMDGPU, but it could also be ROCm or Torch issue, since I am not sure I am reporting it here and I have reported it to the respective projects. Thanks

### Operating System

NixOS VERSION 24.05 (Uakari)

### CPU

AMD Ryzen 7 3700X 8-Core Processor

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0, ROCm 5.5.1

### ROCm Component

ROCm

### Steps to Reproduce

1. Install mostly any Stable Diffusion WebUI e.g. ComfyUI, InvokeAI, Automatic1111, etc.
2. Install a SDXL model
3. Generate a image, crashes seem to depend on resolution used. e.g. 1024x1024 is fine, 512x512 also fine, but 832x1152 will crash
4. See crash

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    AMD Ryzen 7 3700X 8-Core Processor
  Uuid:                    CPU-XX
  Marketing Name:          AMD Ryzen 7 3700X 8-Core Processor
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   3600
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65773952(0x3eba180) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65773952(0x3eba180) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65773952(0x3eba180) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1030
  Uuid:                    GPU-6200dec08b9272cf
  Marketing Name:          AMD Radeon RX 6800
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      16(0x10) KB
  Chip ID:                 29631(0x73bf)
  ASIC Revision:           1(0x1)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2475
  BDFID:                   2304
  Internal Node ID:        1
  Compute Unit:            60
  SIMDs per CU:            2
  Shader Engines:          4
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 116
  SDMA engine uCode::      83
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1030
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***

### Additional Information

Issue on AMDGPU: https://gitlab.freedesktop.org/drm/amd/-/issues/3220
Issue on PyTorch: https://github.com/pytorch/pytorch/issues/120775

---

## 评论 (13 条)

### 评论 #1 — nartmada (2024-02-29T17:24:29Z)

Internal ticket has been created for investigation.

---

### 评论 #2 — nonetrix (2024-02-29T19:31:52Z)

For more context here is a [video of it happening](https://youtu.be/EDWfEKL7iZU), I was trying to use a ComfyUI workflow upscaling low resolution images. It uses SDXL to do so, but just generating a large image seems to trigger it. I'm confused as to why there is no other error reports if it's so easy to trigger, I'm slightly worried it's my card perhaps, but running LLMs on it etc. is completely stable. Unfortunately my experience has been riddled with GPU resets on Linux, I encountered another one relating to video decoding which forced me to go back to software decoding, but this is a known [AMDGPU issue](https://gitlab.freedesktop.org/drm/amd/-/issues/2156#note_2211728) maybe someone can dedicate time into finally getting it fixed though and making my GPU reset free? It's just a shot in the dark, but many people seem to be encountering the same thing in this instance and it hasn't really gone anywhere. But that is related to ROCm



---

### 评论 #3 — nonetrix (2024-03-02T20:35:35Z)

With some further testing I have found that not running a desktop like in my case Hyprland significantly reduces crashes, not sure if Hyprland is to blame. I don't think the issue is gone probably, just significantly reduced as the GPU isn't doing much else. I will keep generating until I have a crash if at all

---

### 评论 #4 — nonetrix (2024-03-02T21:17:25Z)

Yep can confirm issue is still present but greatly reduced, this works as a temporary fix at least for me

---

### 评论 #5 — nonetrix (2024-03-02T21:28:20Z)

`dmesg --follow` reveals more information
```
[  327.006239] sched: RT throttling activated
[  327.385240] iwlwifi 0000:04:00.0: Error sending STATISTICS_CMD: time out after 2000ms.
[  327.385245] iwlwifi 0000:04:00.0: Current CMD queue read_ptr 245 write_ptr 246
[  327.387395] iwlwifi 0000:04:00.0: Start IWL Error Log Dump:
[  327.387398] iwlwifi 0000:04:00.0: Transport status: 0x0000004A, valid: 6
[  327.387400] iwlwifi 0000:04:00.0: Loaded firmware version: 29.198743027.0 3168-29.ucode
[  327.387402] iwlwifi 0000:04:00.0: 0x00000084 | NMI_INTERRUPT_UNKNOWN
[  327.387404] iwlwifi 0000:04:00.0: 0x00000230 | trm_hw_status0
[  327.387406] iwlwifi 0000:04:00.0: 0x00000000 | trm_hw_status1
[  327.387408] iwlwifi 0000:04:00.0: 0x00043D6C | branchlink2
[  327.387410] iwlwifi 0000:04:00.0: 0x0004AFA2 | interruptlink1
[  327.387412] iwlwifi 0000:04:00.0: 0x0004D1FA | interruptlink2
[  327.387414] iwlwifi 0000:04:00.0: 0x00000000 | data1
[  327.387415] iwlwifi 0000:04:00.0: 0x00000080 | data2
[  327.387417] iwlwifi 0000:04:00.0: 0x07030000 | data3
[  327.387419] iwlwifi 0000:04:00.0: 0xEEC0D022 | beacon time
[  327.387421] iwlwifi 0000:04:00.0: 0x51DE7FE1 | tsf low
[  327.387423] iwlwifi 0000:04:00.0: 0x00000178 | tsf hi
[  327.387424] iwlwifi 0000:04:00.0: 0x00000000 | time gp1
[  327.387426] iwlwifi 0000:04:00.0: 0x12E81DDC | time gp2
[  327.387428] iwlwifi 0000:04:00.0: 0x00000001 | uCode revision type
[  327.387430] iwlwifi 0000:04:00.0: 0x0000001D | uCode version major
[  327.387432] iwlwifi 0000:04:00.0: 0x0BD893F3 | uCode version minor
[  327.387433] iwlwifi 0000:04:00.0: 0x00000220 | hw version
[  327.387435] iwlwifi 0000:04:00.0: 0x00C89200 | board version
[  327.387437] iwlwifi 0000:04:00.0: 0x0000001C | hcmd
[  327.387439] iwlwifi 0000:04:00.0: 0x24022000 | isr0
[  327.387441] iwlwifi 0000:04:00.0: 0x01800000 | isr1
[  327.387442] iwlwifi 0000:04:00.0: 0x0000000A | isr2
[  327.387444] iwlwifi 0000:04:00.0: 0x00417CC0 | isr3
[  327.387446] iwlwifi 0000:04:00.0: 0x00000000 | isr4
[  327.387448] iwlwifi 0000:04:00.0: 0x0DAB001C | last cmd Id
[  327.387449] iwlwifi 0000:04:00.0: 0x00000000 | wait_event
[  327.387451] iwlwifi 0000:04:00.0: 0x00004208 | l2p_control
[  327.387453] iwlwifi 0000:04:00.0: 0x00010030 | l2p_duration
[  327.387455] iwlwifi 0000:04:00.0: 0x0000033F | l2p_mhvalid
[  327.387456] iwlwifi 0000:04:00.0: 0x000000EE | l2p_addr_match
[  327.387458] iwlwifi 0000:04:00.0: 0x00000005 | lmpm_pmg_sel
[  327.387460] iwlwifi 0000:04:00.0: 0x14100601 | timestamp
[  327.387462] iwlwifi 0000:04:00.0: 0x00348090 | flow_handler
[  327.387464] iwlwifi 0000:04:00.0: Fseq Registers:
[  327.387470] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_ERROR_CODE
[  327.387477] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_TOP_INIT_VERSION
[  327.387483] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_CNVIO_INIT_VERSION
[  327.387489] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_OTP_VERSION
[  327.387496] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_TOP_CONTENT_VERSION
[  327.387502] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_ALIVE_TOKEN
[  327.387508] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_CNVI_ID
[  327.387514] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_CNVR_ID
[  327.387521] iwlwifi 0000:04:00.0: 0x00000000 | CNVI_AUX_MISC_CHIP
[  327.387527] iwlwifi 0000:04:00.0: 0x00000000 | CNVR_AUX_MISC_CHIP
[  327.387533] iwlwifi 0000:04:00.0: 0x00000000 | CNVR_SCU_SD_REGS_SD_REG_DIG_DCDC_VTRIM
[  327.387540] iwlwifi 0000:04:00.0: 0x00000000 | CNVR_SCU_SD_REGS_SD_REG_ACTIVE_VDIG_MIRROR
[  327.387546] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_PREV_CNVIO_INIT_VERSION
[  327.387552] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_WIFI_FSEQ_VERSION
[  327.387559] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_BT_FSEQ_VERSION
[  327.387565] iwlwifi 0000:04:00.0: 0x00000000 | FSEQ_CLASS_TP_VERSION
[  327.387568] iwlwifi 0000:04:00.0: Collecting data: trigger 2 fired.
[  327.387571] ieee80211 phy0: Hardware restart was requested
[  327.833248] iwlwifi 0000:04:00.0: Queue 0 is active on fifo 7 and stuck for 2500 ms. SW [245, 246] HW [246, 246] FH TRB=0x07000f5
[  329.779379] amdgpu 0000:09:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000029 SMN_C2PMSG_82:0x00000000
[  329.779384] amdgpu 0000:09:00.0: amdgpu: Failed to disable gfxoff!
[  329.854545] ACPI: \: failed to evaluate _DSM bf0212f2-788f-c64d-a5b3-1f738e285ade (0x1001)
[  329.854550] ACPI: \: failed to evaluate _DSM bf0212f2-788f-c64d-a5b3-1f738e285ade (0x1001)
[  329.854552] ACPI: \: failed to evaluate _DSM bf0212f2-788f-c64d-a5b3-1f738e285ade (0x1001)
[  329.854554] ACPI: \: failed to evaluate _DSM bf0212f2-788f-c64d-a5b3-1f738e285ade (0x1001)
[  329.854556] ACPI: \: failed to evaluate _DSM bf0212f2-788f-c64d-a5b3-1f738e285ade (0x1001)
[  329.854557] ACPI: \: failed to evaluate _DSM bf0212f2-788f-c64d-a5b3-1f738e285ade (0x1001)
[  329.854559] ACPI: \: failed to evaluate _DSM bf0212f2-788f-c64d-a5b3-1f738e285ade (0x1001)
[  329.869707] wlp4s0: HW problem - can not stop rx aggregation for f8:9b:6e:76:9c:cc tid 0
[  329.869711] wlp4s0: HW problem - can not stop rx aggregation for f8:9b:6e:76:9c:cc tid 2
[  329.869713] wlp4s0: HW problem - can not stop rx aggregation for f8:9b:6e:76:9c:cc tid 3
[  333.273197] amdgpu 0000:09:00.0: [drm] *ERROR* [CRTC:91:crtc-0] flip_done timed out
[  335.321158] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma2 timeout, signaled seq=1812, emitted seq=1813
[  335.321414] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process  pid 0 thread  pid 0
[  335.321641] amdgpu 0000:09:00.0: amdgpu: GPU reset begin!
[  335.321661] amdgpu: Failed to suspend process 0x800c
[  339.962525] amdgpu 0000:09:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000029 SMN_C2PMSG_82:0x00000000
[  339.962529] amdgpu 0000:09:00.0: amdgpu: Failed to disable gfxoff!
[  342.086691] amdgpu 0000:09:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - hubp2_set_blank_regs line:961
[  342.339891] amdgpu 0000:09:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - hubp2_set_blank_regs line:961
[  342.598748] amdgpu 0000:09:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - hubp2_set_blank_regs line:961
[  342.852513] amdgpu 0000:09:00.0: [drm] REG_WAIT timeout 1us * 100000 tries - hubp2_set_blank_regs line:961
[  345.317259] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* ring_buffer_start = 00000000585cd929; ring_buffer_end = 00000000ed2149dc; write_frame = 000000000d3fef63
[  345.317478] [drm:psp_ring_cmd_submit [amdgpu]] *ERROR* write_frame is pointing to address out of bounds
```

---

### 评论 #6 — nonetrix (2024-03-05T21:02:05Z)

I was able to reproduce this issue with the Vulkan backend of llama cpp interestingly as well, this time with just Mistral-7B-Instruct at 8 bits. Should easily fit on my GPU since it has 16GBs of VRAM but it almost instantly crashes. Actually much faster to reproduce and constant, I also checked the VRAM usage and it never goes above 8GBs. Just like ROCm running in a TTY eliminates my crashes mostly, this issue is really odd, but then I have zero crashes running a LLM with ROCm and PyTorch only llama cpp Vulkan and PyTorch Stable Diffusion. I guess it's some instruction or something that's completely broken or something perhaps? I don't even know anymore, I really hope my GPU isn't defective but only with compute or something weird like that. Should I close this issue and just keep the Gitlab one open since it's clearly not a ROCm or PyTorch issue but either amdfkd or my GPU

---

### 评论 #7 — dogbarfs (2024-04-11T23:27:00Z)

Try increasing your cpu DDR RAM voltage to 1.35v

---

### 评论 #8 — nonetrix (2024-04-12T01:47:23Z)

I have pretty much confirmed it's not memory related, but I will try that anyway when I get the chance. Also, since making this issue I've actually upgraded my RAM so extra sure it's not that, at least according to @agd5f on Gitlab seems to be firmware related unfortunately, very similar situation that Tinycorp ran into but unrelated expect they are both possibly firmware bugs. Me just reading the errors tells me it's most likely some kind of race condition that crashes the card and leaves it in a unrecoverable state

https://gitlab.freedesktop.org/drm/amd/-/issues/3220

If it is the case don't really know when this is going to be fixed unfortunately, but on the bright side AMD seems to be open sourcing more of their firmware. I am pretty sure my issue is due to the SMU though which is still closed source, unlike what is at least planned with the MES. And not sure if AMD feels comfortable open sourcing it as it has to do with power management (I think?) so could perhaps damage cards, but I would still urge them to do it anyway. Also, it's definitely not like my PSU is the issue because I was having this issue on a older PSU I had and this newer one, both well excess of what my system should draw at max. The latter being a old 1000W and the newer one being a 850W since it was again way over what I needed anyway, I got it as a hand me down from a Bitcoin mining operation the first one

---

### 评论 #9 — nonetrix (2024-06-16T14:47:58Z)

I might have just got lucky then, check dmesg etc. should give you more insight, I think similar bugs still exist but they might be unrelated 

---

### 评论 #10 — jamesxu2 (2024-06-21T15:34:49Z)

Hi @nonetrix, I tried this configuration and I wasn't able to reproduce your crash. Please have a look at my configuration and steps and tell me if there's something I'm missing.

**System Configuration**
- RX6800XT
- Ubuntu 22.04
- Python 3.10.12 + Torch 2.3.1 + rocm5.7 (Launcher default install)
- ROCm 6.1.2, ROCm 6.0.0
- Automatic1111 WebUI + VAE/Model from [this ticket](https://github.com/ROCm/ROCm/issues/3166) 

**Execution Steps**
- Install ROCm 6.X.X using [amdgpu-install](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/amdgpu-install.html)
- Install Automatic1111 following their [setup instructions on Linux](https://github.com/AUTOMATIC1111/stable-diffusion-webui?tab=readme-ov-file#automatic-installation-on-linux)
- Run using python launch.py from inside the webui directory.
- Generate images using the web UI with 2048 x 2048 resolution

**Results**

I am able to generate 512x512 up to 2048x2048 images without issue while simultaneously running the webui GUI. My GPU edge temperature does not exceed 68C during image generation. 

---

### 评论 #11 — jamesxu2 (2024-07-04T14:17:37Z)

Hi @nonetrix, do you have any update? 

Note that a similar issue has been resolved recently (https://github.com/ROCm/ROCm/issues/3166) and you may find the investigation there helpful in your case. Please let me know if you're still encountering issues, or if I can close this ticket. 


---

### 评论 #12 — nonetrix (2024-07-04T19:38:07Z)

Likely safe to close I think

---

### 评论 #13 — jamesxu2 (2024-07-04T19:41:49Z)

Great, thanks!

---
