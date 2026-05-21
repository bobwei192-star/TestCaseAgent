# [Feature]: rocminfo should give more warning info when a second incompatible GPU installed

> **Issue #5942**
> **状态**: closed
> **创建时间**: 2026-02-07T12:17:36Z
> **更新时间**: 2026-04-14T16:31:50Z
> **关闭时间**: 2026-04-14T16:31:50Z
> **作者**: MartinEmrich
> **标签**: Feature Request, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5942

## 标签

- **Feature Request** (颜色: #fbca04)
- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

I installed an older GPU as a secondary GPU (in the hopes of playing around with multi GPU running LLMs).

Doing more research, it seems unlikely getting this to work (I find various reports from "should work, and use lower-complexity upper layers on the smaller GPU, deeper higher-complexity-layers on the bigger GPU" to "RX580/gfx803 support has been abandoned or completely removed")...

But at least `rocminfo` should either detect and show both cards, or at least only the primary (RX 7800 XT).

Instead, I get this message:

```
# rocminfo
ROCk module version 6.16.13 is loaded
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:1329
Call returned HSA_STATUS_ERROR: A generic error has occurred.
```

### Operating System

Debian 13

### CPU

Ryzen 7 2700X

### GPU

Primary: RX 7800 XT, Secondary: RX 580

### ROCm Version

7.2.0

### ROCm Component

rocminfo

### Steps to Reproduce

* Install two GPUs, one of them old and likely unsupported by ROCm?
* Install ROCm 7.2.0
* Run `rocminfo`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

same output as without `--support`

### Additional Information

Both cards are present:
# lspci | grep VGA
0c:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 32 [Radeon RX 7700 XT / 7800 XT] (rev c8)
0d:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] (rev e7)

Mainboard: Gigabyte Aorus X370 Ultra Gaming

They are in the (according to the motherboard) correct PCIe-Slots, both directly connected to the CPU.
Primary:
```
  LnkSta: Speed 16GT/s, Width x16
                        TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
```
Secondary:
```
LnkSta: Speed 2.5GT/s (downgraded), Width x8 (downgraded)
                        TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
```

---

## 评论 (17 条)

### 评论 #1 — MartinEmrich (2026-02-08T12:10:24Z)

Additional Info: 

Using llama.cpp, it detects and uses both cards via vulkan, so both cards are working (should rule out most if any power or PCIe related issues).

I noticed that `rocm-smi` does detect both cards, and displays valid information:
(This is llama.cpp putting too many layers on the RX580, likely limiting overall performance... but it works).

```

WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

============================================ ROCm System Management Interface ============================================
====================================================== Concise Info ======================================================
Device  Node  IDs              Temp    Power    Partitions          SCLK     MCLK     Fan     Perf  PwrCap  VRAM%  GPU%
              (DID,     GUID)  (Edge)  (Avg)    (Mem, Compute, ID)
==========================================================================================================================
0       1     0x747e,   3950   49.0°C  64.0W    N/A, N/A, 0         1372Mhz  456Mhz   0%      auto  236.0W  95%    29%
1       2     0x67df,   40407  58.0°C  92.165W  N/A, N/A, 0         1365Mhz  2000Mhz  33.73%  auto  145.0W  83%    100%
==========================================================================================================================
================================================== End of ROCm SMI Log ===================================================
```



---

### 评论 #2 — huanrwan-amd (2026-02-10T20:40:45Z)

Hi @MartinEmrich , thanks for posting. Can you please check the driver version using `dkms status` ?

---

### 评论 #3 — MartinEmrich (2026-02-10T20:43:35Z)

@huanrwan-amd sure:

```
$ sudo dkms status
amdgpu/6.16.13-2278356.24.04, 6.12.57+deb13-amd64, x86_64: installed (Original modules exist)
amdgpu/6.16.13-2278356.24.04, 6.12.63+deb13-amd64, x86_64: installed (Original modules exist)
$ uname -a
Linux aurora 6.12.63+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.63-1 (2025-12-30) x86_64 GNU/Linux
```

---

### 评论 #4 — huanrwan-amd (2026-02-10T21:06:39Z)

@MartinEmrich Seems driver are new. So, it works through vulkan.
For ROCm, https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html showing RX 580 is not supported...

---

### 评论 #5 — MartinEmrich (2026-02-10T21:24:28Z)

Yes, both cards work with vulkan, even simultaneously! (I run a ~30GB model (Gwen3-coder-30B) spread across the RX7800XT, the RX580 and some layers on the CPU with ~12-15tokens/s.)

The RX 7800XT is supported by ROCm (it worked before adding the second card). The pure presence of an unsupported card should IMHO not throw it off. Fixing that would cover the Issue/Bug part.

I had hoped to use ROCm for the first (naively expecting higher performance than Vulkan; though in the meantime I also saw reports of the opposite).

It would of course be great when support for older cards would not have been removed... but that's more of a wishlist item.


---

### 评论 #6 — huanrwan-amd (2026-02-10T22:24:38Z)

> Yes, both cards work with vulkan, even simultaneously! (I run a ~30GB model (Gwen3-coder-30B) spread across the RX7800XT, the RX580 and some layers on the CPU with ~12-15tokens/s.)
> 
> The RX 7800XT is supported by ROCm (it worked before adding the second card). The pure presence of an unsupported card should IMHO not throw it off. Fixing that would cover the Issue/Bug part.
> 
> I had hoped to use ROCm for the first (naively expecting higher performance than Vulkan; though in the meantime I also saw reports of the opposite).
> 
> It would of course be great when support for older cards would not have been removed... but that's more of a wishlist item.

If you remove the RX580, rocminfo works? Since RX580 uses GCN architecture which is not supported by ROCm anymore...

---

### 评论 #7 — MartinEmrich (2026-02-11T09:35:43Z)

> If you remove the RX580, rocminfo works? Since RX580 uses GCN architecture which is not supported by ROCm anymore...

Yes, before I installed it, `rocminfo` worked as expected, and I could use llama.cpp with ROCm support.
After I added it, `rocminfo` produces the above error message, and llama.cpp does not even detect the supported RX7800XT card as a ROCm target (and thus uses everything via Vulkan).

So to speculate, probably the code in ROCm enumerating the available card(s), instead of skipping unsupported cards, tries to do things with them that do not work and produce an error?

---

### 评论 #8 — huanrwan-amd (2026-02-11T15:29:16Z)

> > If you remove the RX580, rocminfo works? Since RX580 uses GCN architecture which is not supported by ROCm anymore...
> 
> Yes, before I installed it, `rocminfo` worked as expected, and I could use llama.cpp with ROCm support. After I added it, `rocminfo` produces the above error message, and llama.cpp does not even detect the supported RX7800XT card as a ROCm target (and thus uses everything via Vulkan).
> 
> So to speculate, probably the code in ROCm enumerating the available card(s), instead of skipping unsupported cards, tries to do things with them that do not work and produce an error?

You can refer to rocminfo: https://github.com/ROCm/rocm-systems/blob/develop/projects/rocminfo/rocminfo.cc
It does what you said to init and detect GPU and fails when GPU is not supported.

---

### 评论 #9 — MartinEmrich (2026-02-11T16:05:47Z)

Ok, then that's the issue: whereever `hsa_init()` comes from, it should not return an error if both a supported and a not supported card is present.

https://github.com/ROCm/rocm-systems/blob/develop/projects/rocminfo/rocminfo.cc#L1323-L1329


---

### 评论 #10 — huanrwan-amd (2026-02-11T16:12:28Z)

@MartinEmrich thanks for the message. What is your suggestion? If both a supported and an unsupported card is detected.

---

### 评论 #11 — MartinEmrich (2026-02-11T16:36:11Z)

I would suggest that it at least just ignores the unsupported card(s), and proceeds as if only the supported card(s) were installed.

Ideally, it should issue a warning, listing the unsupported cards (as older cards seem to be removed at random with newer releases, this might help people upgrading, and loosing support for their older card in the future).

---

### 评论 #12 — huanrwan-amd (2026-02-11T16:48:22Z)

@MartinEmrich Thanks, I will forward the message to the internal team.

---

### 评论 #13 — huanrwan-amd (2026-02-12T15:44:52Z)

Hi @MartinEmrich, an internal ticket is created to track this.

---

### 评论 #14 — MartinEmrich (2026-03-15T16:38:24Z)

Quick Update: I just discovered the 7.11 release and tried it; same issue remains (as expected, it is said it's just a prerelease of 7.2 built with TheRock).

Also I just noticed that the issue title is now a bit misleading: Not only rocminfo crashes with the unsupported secondary card, but any ROCm application (tried llama.ccp as well as LlamaFactory) fails to discover or use the  primary, supported card as well (I suspect all use the same detection logic via a ROCm library, resulting in 0 cards instead of 1).

---

### 评论 #15 — Sundance636 (2026-03-18T18:43:46Z)

Hi @MartinEmrich I've created a proposed patch here https://github.com/ROCm/rocm-systems/pull/4198, it should address the issues with the unsupported GPUs by skipping over the unsupported once  as suggested. If you're able to feel free to test it out since I dont have a set up to repro the exact issue.

---

### 评论 #16 — MartinEmrich (2026-03-18T18:49:41Z)

@Sundance636 Thanks! Would love to test this. I tried building ROCm with "TheRock" a few weeks ago but was just overwhelmed with both the size (it cloned myriads of subrepositories and filled up the device) and complexity... and did not succeed.

If you have some super quick instructions on how to build this to Debian packages to try here, I'd love to test!

---

### 评论 #17 — huanrwan-amd (2026-04-14T16:31:50Z)

Internal ticket is done. So close the ticket for now.

---
