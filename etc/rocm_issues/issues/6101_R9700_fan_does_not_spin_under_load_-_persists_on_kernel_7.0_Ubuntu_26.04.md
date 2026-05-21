# R9700 fan does not spin under load - persists on kernel 7.0 / Ubuntu 26.04

> **Issue #6101**
> **状态**: open
> **创建时间**: 2026-03-31T13:52:36Z
> **更新时间**: 2026-05-19T10:43:14Z
> **作者**: lobsteroh
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6101

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- amd-nicknick

## 描述

**Hardware:** ASUS Turbo Radeon AI Pro R9700 32GB
**vBIOS:** 115-G287BP00-100
**OS:** Ubuntu 26.04 beta (Resolute Raccoon)
**Kernel:** 7.0.0-10-generic
**ROCm:** 7.2.1
**AMDGPU driver:** 6.16.13 (out-of-tree) and kernel built-in tested
**linux-firmware:** 20260319.git217ca6e4 (March 2026)

## Issue

The GPU fan does not spin under any load on Linux. During AI training the GPU reached 109°C and thermally throttled with the fan physically stationary throughout. This is a serious hardware safety issue.

## SMU Firmware Mismatch (root cause)

Present on every kernel and driver version tested:

```
amdgpu 0000:2d:00.0: smu driver if version = 0x0000002e (46)
amdgpu 0000:2d:00.0: smu fw if version = 0x00000032 (50)
amdgpu 0000:2d:00.0: smu fw version = 0x00684b00 (104.75.0)
amdgpu 0000:2d:00.0: SMU driver if version not matched
```

The card firmware is 4 interface versions ahead of what the AMDGPU driver supports. Fan control registers are inaccessible as a result.

## Technical Findings

- `rocm-smi --setfan` returns 'Not supported on this system'
- sysfs `pwm1` node is READ-ONLY (-r--r--r--)
- `fan1_enable` returns 'Invalid argument'
- GPU enters runtime power suspend under load, suppressing fan response
- Fan physically stationary at 109°C during AI training
- LACT 0.8.4 fan control grayed out

## Tested Configurations - Mismatch Persists On All

| Kernel | AMDGPU Driver | OS | Result |
|--------|--------------|-----|--------|
| 6.14.0-37 | 6.16.13 (out-of-tree) | Ubuntu 24.04 | SMU mismatch, fan not spinning |
| 6.17.0-19 | 6.16.6 (out-of-tree) | Ubuntu 24.04 | SMU mismatch, fan not spinning |
| 6.17.0-19 | 6.16.13 (out-of-tree) | Ubuntu 24.04 | SMU mismatch, fan not spinning |
| 6.18.20 | N/A | Ubuntu 24.04 | Kernel panic - unbootable |
| 6.19.10 | N/A | Ubuntu 24.04 | Kernel panic - unbootable |
| 7.0.0-10 | built-in | Ubuntu 26.04 beta | SMU mismatch, fan not spinning |linux-firmware updated to March 2026 (20260319) — no change.

## Request

The AMDGPU driver needs to be updated to support SMU interface version 50 (0x00000032) as shipped on the R9700 (gfx1201, RDNA 4). This issue makes the card unsafe for its primary use case of sustained AI/ML workloads on Linux.

Related: #5908

---

## 评论 (52 条)

### 评论 #1 — dvoloshyn (2026-03-31T17:38:50Z)

A have a much older laptop with Radeon RX 6800M.
On 6.19.10 kernel I also get firmware mismatch:
```
бер 30 12:38:37 cachyos kernel: amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413f00 (65.63.0)
бер 30 12:38:37 cachyos kernel: amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
```

---

### 评论 #2 — Qubitium (2026-04-01T19:57:02Z)

@amd-nicknick  @ppanchad-amd  To be frank, how can this be allowed to happen? Did the QA department fail to actually test is in a real-world Linux OS with publically accessible drivers? This is no longe a patch but a sit-down with who ever is in charge of sycning driver with hw production release. Somebody at AMD dropped the ball.

---

### 评论 #3 — lobsteroh (2026-04-03T12:47:08Z)

thanks for closing #6087, Nick, yes, this is reporting the same problem.

Hi, I've completed the purge and reinstall as recommended, and done extensive additional testing. I can now identify the root cause. And honestly i am quite puzzled and just a little bit pissed how this can be allowed to slip through the cracks where a major commercial graphics card seems to be broken right out of the box.

**Environment:**
- GPU: AMD Radeon AI PRO R9700 (Device ID: 0x7551, gfx1201)
- ROCm: 7.2.1 (`rocm/noble 7.2.1.70201-81~24.04`, installed from AMD's official repo)
- amdgpu driver: 7.2 (`amdgpu-core 1:7.2.70201-2303469.24.04`)
- amd-smi: 26.2.2+e1a6bc5663
- OS: Ubuntu 24.04 (Noble) - 26.04
- PCI Bus: `0000:2D:00.0`

**Root cause — SMU interface version mismatch:**

`dmesg` shows the following on every boot and every resume from suspend:
```
amdgpu 0000:2d:00.0: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684b00 (104.75.0)
amdgpu 0000:2d:00.0: SMU driver if version not matched
```
The driver expects SMU interface version `0x2e` (46) but the card's firmware reports `0x32` (50). The driver is 4 versions behind the firmware shipped on this card. This mismatch appears to be the cause of all symptoms below.

**Symptoms caused by the SMU mismatch:**

1. **GFX clock stuck at 0 MHz regardless of perf level** — even after `sudo amd-smi set --gpu 0 --perf-level high` reports success, the clock does not move:
```
GFX_0:
    CLK: 0 MHz
    MIN_CLK: 500 MHz   ← below its own minimum
    MAX_CLK: 2350 MHz
    DEEP_SLEEP: ENABLED
```

2. **THROTTLE_STATUS permanently THROTTLED** — not thermal (temps are 35°C), but because the SMU is not correctly responding to power management commands.

3. **Fan RPM always 0** despite fan control being active:
```
FAN:
    SPEED: 76
    MAX: 255
    RPM: 0          ← telemetry broken
    USAGE: 29.8 %
```
Fan speed does respond to perf level changes (jumped to 86 on HIGH), confirming partial SMU communication — but RPM telemetry is not functional.

4. **kernel hwmon interface inaccessible** — `cat /sys/class/drm/card1/device/hwmon/hwmon2/temp1_input` returns `Device or resource busy`, and lm-sensors reports all GPU values as N/A.

5. **PCI device suspends aggressively** — `power/runtime_status` shows `suspended` at idle; forcing it awake does not resolve the hwmon issue.

6. **GECC enabled** — `dmesg` also reports `GECC is currently enabled, which may affect performance`. This is noted but may be unrelated.

**Summary:**

This is not a firmware residue issue. The card's shipping SMU firmware (`0x32`) is newer than what the amdgpu driver in ROCm 7.2.1 supports (`0x2e`). This mismatch breaks SMU communication on every boot, resulting in a permanently throttled GFX clock at 0 MHz, broken fan RPM telemetry, and an inaccessible hwmon interface. The driver needs its SMU interface updated to match the firmware version shipped with this card.

Happy to provide any additional diagnostics.

---

### 评论 #4 — marifamd (2026-04-04T00:02:41Z)

Hi @lobsteroh we aren't planning on fixing rocm-smi for this issue. However amd-smi is planned to have the fix to the set fan issues you're seeing on the R9700 as well as newer gpus. Also have moved to rocm-systems and you can see the PR we are working on here: https://github.com/ROCm/rocm-systems/pull/3541
We're targeting TheRock 7.13 release or the following if we can't get the changes submitted in time 

FYI - you will have to set the feature mask on the newer GPUs when loading the amdgpu driver to enable the OD fan control: `sudo modprobe amdgpu ppfeaturemask=0xfff7ffff`

---

### 评论 #5 — lobsteroh (2026-04-04T14:57:25Z)

Hi, testing the suggested workaround and ppfeaturemask on an AMD Radeon AI PRO R9700 (Device ID: 0x7551, gfx1201) — wanted to report findings relevant to this PR.

**Environment:**
- GPU: AMD Radeon AI PRO R9700 (gfx1201, headless compute-only, no display connected)
- OS: Ubuntu 26.04 "Resolute Raccoon" (development branch)
- Kernel: 7.0.0-10-generic
- ROCm: 7.2.1 (`rocm/noble 7.2.1.70201-81~24.04`)
- amdgpu driver: 7.2 (`amdgpu-core 1:7.2.70201-2303469.24.04`)
- amd-smi: 26.2.2+e1a6bc5663

**ppfeaturemask not applying correctly:**

Followed the recommendation to set `ppfeaturemask=0xfff7ffff`:
```
$ cat /etc/modprobe.d/amdgpu.conf
options amdgpu ppfeaturemask=0xfff7ffff
```

After reboot, the driver loaded a different value:
```
$ cat /sys/module/amdgpu/parameters/ppfeaturemask
0xfff7bfff
```

The driver is silently overriding the requested value — bit 14 (`0x4000`, the OD feature flag) is being masked out without any log entry in dmesg. There is no other modprobe config file overriding this value:
```
$ grep -r "ppfeaturemask" /etc/modprobe.d/
/etc/modprobe.d/amdgpu.conf:options amdgpu ppfeaturemask=0xfff7ffff
$ grep -r "ppfeaturemask" /usr/lib/modprobe.d/
(no output)
$ sudo dmesg | grep -i "ppfeature\|feature mask\|overdrive"
(no output)
```

**gpu_od sysfs path does not exist on gfx1201:**

Even with the mask applied, the `gpu_od` interface this PR depends on is entirely absent:
```
$ ls /sys/class/drm/card1/device/gpu_od/
ls: cannot access '/sys/class/drm/card1/device/gpu_od/': No such file or directory
```

This means the dynamic interface detection in PR #3541 will fall through to the legacy hwmon path for this card, which is also broken on gfx1201 (pwm1_enable does not exist, pwm1 returns permission denied).

**Additional context — SMU interface version mismatch:**

On every boot and resume from suspend:
```
amdgpu 0000:2d:00.0: smu driver if version = 0x0000002e, smu fw if version = 0x00000032
amdgpu 0000:2d:00.0: SMU driver if version not matched
```
Driver expects SMU interface `0x2e` (46), firmware reports `0x32` (50). This mismatch appears to be the root cause — fans are physically not spinning under Linux (0 RPM confirmed visually, not just a telemetry issue), GFX clock is stuck at 0 MHz regardless of perf level, and THROTTLE_STATUS is permanently THROTTLED despite temps being normal.

**Summary:**

PR #3541 as currently described may not be sufficient for gfx1201 (R9700) because:
1. The OD feature bit is silently blocked by the driver regardless of ppfeaturemask
2. The `gpu_od` sysfs path does not exist for this card
3. The legacy hwmon fallback path is also non-functional on gfx1201
4. The underlying SMU interface mismatch may need to be resolved first before any fan control path can work

Happy to test any builds or provide additional diagnostics.

---

### 评论 #6 — Only8Bits (2026-04-07T10:52:41Z)

FWIW the SMU mismatch also applies to 7900 series but at least it still works (?), and RDNA3 is not exactly new anymore:

`amdgpu 0000:0c:00.0: amdgpu: detected ip block number 4 <smu>`
`amdgpu 0000:0c:00.0: amdgpu: smu driver if version = 0x0000003d, smu fw if version = 0x00000040, smu fw program = 0, smu fw version = 0x004e8200 (78.130.0)`
`amdgpu 0000:0c:00.0: amdgpu: SMU driver if version not matched`
`amdgpu 0000:0c:00.0: amdgpu: SMU is initialized successfully!`

AFAIR it has been that way in all official ROCm 7.x series, can't clearly remember 6.x but I think 6.4 was also affected.
ppfeaturemask=0xfff7ffff also works properly (I need it to reduce shader max turbo clock) but I pass it to kernel via boot argument rather than modules option. Not really sure if it makes any difference - worth a try?

The whole power/fan/clock control interface is rather poorly documented if you ask me. Some (tested and working!) examples for RDNA3 and RDNA4 series cards would be useful.

---

### 评论 #7 — lobsteroh (2026-04-08T10:18:24Z)

Update: Setting ppfeaturemask via grub boot parameter 
(amdgpu.ppfeaturemask=0xfff7ffff) correctly loads 0xfff7ffff, 
confirmed via /sys/module/amdgpu/parameters/ppfeaturemask.

However gpu_od still does not exist:
$ ls /sys/class/drm/card1/device/gpu_od/
No such file or directory

This confirms the gpu_od interface is not implemented in the 
current driver for gfx1201, independent of the feature mask. 
PR #3541 will need explicit gfx1201 support added.

---

### 评论 #8 — amd-nicknick (2026-04-08T13:26:48Z)

@lobsteroh could you please share your full dmesg log? On my system with a R9700 the gpu_od sysfs path is populated:
```
$ ls /sys/class/drm/card0/device/gpu_od/fan_ctrl
acoustic_limit_rpm_threshold  acoustic_target_rpm_threshold  fan_curve  fan_minimum_pwm  fan_target_temperature  fan_zero_rpm_enable  fan_zero_rpm_stop_temperature
```
I'm guessing something went wrong during driver initialization on your system?

---

### 评论 #9 — lobsteroh (2026-04-10T18:30:05Z)

Following up with full dmesg and additional testing after suggestions in this thread.

**Environment:**
- GPU: AMD Radeon AI PRO R9700 (Device ID: 0x7551, gfx1201, headless compute-only)
- OS: Ubuntu 26.04 "Resolute Raccoon" (development branch)
- Kernel: 7.0.0-12-generic
- ROCm: 7.2.1 (`rocm/noble 7.2.1.70201-81~24.04`)
- amdgpu driver: 7.2 (`amdgpu-core 1:7.2.70201-2303469.24.04`)
- amd-smi: 26.2.2+e1a6bc5663
- SMU firmware: 104.76.0 (`smu fw if version = 0x00000033`)

**Confirmed: `gpu_od` does not exist on this system**

I've methodically ruled out every known cause:

1. **ppfeaturemask** — set via grub boot parameter (not modprobe, which was silently capping the value):
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdgpu.ppfeaturemask=0xfff7ffff amdgpu.ras_enable=0"
```
Confirmed loaded correctly:
```
$ cat /sys/module/amdgpu/parameters/ppfeaturemask
0xfff7ffff
```

2. **GECC/ECC disabled** — was initially enabled, now confirmed off:
```
[   10.329577] amdgpu 0000:2d:00.0: GECC is disabled
```

3. **Overdrive enabled** — driver confirms it in dmesg:
```
[   10.067781] amdgpu: Overdrive is enabled, please disable it before reporting any bugs unrelated to overdrive.
```

4. **gpu_od still absent after all of the above:**
```
$ ls /sys/class/drm/card1/device/gpu_od/
ls: cannot access '/sys/class/drm/card1/device/gpu_od/': No such file or directory
```

**Full dmesg (amdgpu relevant entries):**
```
[   10.061931] amdgpu: Overdrive is enabled
[   10.066187] amdgpu 0000:2d:00.0: detected ip block number 4 <smu_v14_0_0>
[   10.329929] amdgpu 0000:2d:00.0: smu driver if version = 0x0000002e, smu fw if version = 0x00000033
[   10.329932] amdgpu 0000:2d:00.0: SMU driver if version not matched
[   10.354481] amdgpu 0000:2d:00.0: SMU is initialized successfully!
[   10.507101] amdgpu 0000:2d:00.0: Using BACO for runtime pm
[   10.329577] amdgpu 0000:2d:00.0: GECC is disabled
```

**Conclusion:**

With `ppfeaturemask=0xfff7ffff` correctly applied, GECC disabled, and overdrive confirmed enabled by the driver — the `gpu_od` sysfs interface is simply not being created for gfx1201 (R9700). The driver advertises overdrive support but never populates the interface for this chip.

The SMU driver interface mismatch (`0x2e` vs `0x33`) remains present on every boot and resume and is likely the underlying reason the `gpu_od` path is never created — the driver may be silently skipping OD interface initialization when it detects the SMU version mismatch.

PR #3541's dynamic interface detection will fall through to the legacy hwmon path on this card, which is also non-functional on gfx1201. For this fix to work on the R9700, the `gpu_od` interface needs to be explicitly implemented for gfx1201, and the SMU version mismatch needs to be resolved first.

Happy to test any builds or provide any additional diagnostics.

---

### 评论 #10 — amd-nicknick (2026-04-15T11:32:37Z)

@lobsteroh It doesn't make sense for gpu_od to not exist while the rest of sysfs interface is there. 
Could you please check if the hwmon interface actually exists on your system? `/sys/class/drm/card1/device/hwmon/hwmon*`

Also check if the fw_version interface is present:
`/sys/class/drm/card1/device/fw_version`

---

### 评论 #11 — jlninrr (2026-04-20T04:31:51Z)

I seem to have inadvertently reproduced this exact problem. I am in the same state as lobsteroh, per their last report. On my system, hwmon does not exist, nor does fw_version. Also happy to continue debug as necessary.

---

### 评论 #12 — amd-nicknick (2026-04-20T06:37:56Z)

@jlninrr, that makes more sense, it sounds like the driver did not initialize properly. Could you please share the full dmesg output so I could narrow down where it went wrong? Thanks!

---

### 评论 #13 — jlninrr (2026-04-20T16:37:02Z)

[dmesg1.txt](https://github.com/user-attachments/files/26903932/dmesg1.txt)

Here's the full dmesg output. One thing to note: since I (and lobsteroh) are on 26.04 beta, I (at least) am unable to install dkms drivers. They won't build against kernel 7.0.0.-14 (the one I have). I suspect being aggressive on OS version may be part of the issue. Holdover from getting my Strix Halo system stable - that system really benefits from uplevel kernel, etc. But perhaps the R9700 may be a bit more comfortable on a system where dkms builds. I'll hold it in this config for now while debugging is happening.

---

### 评论 #14 — lobsteroh (2026-04-20T16:50:49Z)

thank you @jlninrr and @amd-nicknick .

i am currently in the field without access to my R9700 machine at home base but was excited to see that mine wasn't the only setup that didn't support the R9700.

On kernel. i am now on Kernel 7 but that was simply a last resort when every earlier kernel from 6.14 on had produced the same outcome. these are the past attempts before it went to 26.04 as a hail mary

| Kernel | AMDGPU Driver | OS | Result |
|--------|--------------|-----|--------|
| 6.14.0-37 | 6.16.13 (out-of-tree) | Ubuntu 24.04 | SMU mismatch, fan not spinning |
| 6.17.0-19 | 6.16.6 (out-of-tree) | Ubuntu 24.04 | SMU mismatch, fan not spinning |
| 6.17.0-19 | 6.16.13 (out-of-tree) | Ubuntu 24.04 | SMU mismatch, fan not spinning |
| 6.18.20 | N/A | Ubuntu 24.04 | Kernel panic - unbootable |
| 6.19.10 | N/A | Ubuntu 24.04 | Kernel panic - unbootable |
| 7.0.0-10 | built-in | Ubuntu 26.04 beta | SMU mismatch, fan not spinning |linux-firmware updated to March 2026 (20260319) — no change.

---

### 评论 #15 — jlninrr (2026-04-20T17:06:03Z)

Worth noting, just in case, that my R9700 fan does spin, though the SMI tools show 0 rpm. And it feels like a space heater even though I am not running anything on the GPU (likely obviously, since I don’t have a working driver). Not sure why it’s so hot while completely idle. I have it powered down for the moment except when debugging.

---

### 评论 #16 — amd-nicknick (2026-04-21T09:05:12Z)

@jlninrr, @lobsteroh, at this moment we don't support kernel 7.x. Nonetheless, I am gathering a system to test this.
The fan spin issue here is odd: The driver will not command fan off without explicit input from gpu_od or hwmon interface. 
I suspect @lobsteroh you're encountering something else particularly with fan control on your card. Could you please give Windows a try and make sure the card isn't defective? Thanks!

---

### 评论 #17 — Qubitium (2026-04-21T15:41:26Z)

@lobsteroh  @jlninrr  Also can you check if you two have made any non-default changes to your motherboard bios?  I am only asking because this is entering somewhat strange territory if multiple people can reproduce it but AMD staff still has hard time recreating it. Let's rule out the hw (bios) part to elimiante the surface area. Note the motherbord, cpu, and any non-default bios settings that was performed. It doesn't hurt to rule out any hw/bios triggered issues. 

---

### 评论 #18 — lobsteroh (2026-04-21T15:47:59Z)

thank you @Qubitium . i am confirming that i have no changes to the defaults on motherboard bios. it is a bare bones lubuntu install

@amd-nicknick not sure how to go about testing on windows. we are a linux only engineering workshop. am i expected to buy a windows license just to test whether my amd card is screwed out of the box?? 


---

### 评论 #19 — amd-nicknick (2026-04-21T15:50:26Z)

@lobsteroh, got it, I'm just trying to add diversity to the setup here to eliminate any configuration errors.
Just to clarify: You have tried Clean Ubuntu 24.04 LTS Desktop install + amdgpu dkms install, and under workload the GPU fan doesn't spin?
I've never asked before: What was the workload you used to test? Is there any displays attached to the GPU?

---

### 评论 #20 — amd-nicknick (2026-04-21T15:55:35Z)

> [@lobsteroh](https://github.com/lobsteroh) [@jlninrr](https://github.com/jlninrr) Also can you check if you two have made any non-default changes to your motherboard bios? I am only asking because this is entering somewhat strange territory if multiple people can reproduce it but AMD staff still has hard time recreating it. Let's rule out the hw (bios) part to elimiante the surface area. Note the motherbord, cpu, and any non-default bios settings that was performed. It doesn't hurt to rule out any hw/bios triggered issues.

Yeah my challenge here is really on the "GPU fan not spinning at all" part. Because the fan is controlled onboard (the firmware dictates this by default with a built-in fan curve).
For the rest of comment about gpu_od and hwmon missing on kernel 7, I will check tomorrow but just like to note that we do not support 7.x kernels yet, and the dkms explicitly rejects 7.x (There are fixes needed to get Navi4 working that are only present in dkms)

---

### 评论 #21 — Qubitium (2026-04-21T15:58:27Z)

> thank you [@Qubitium](https://github.com/Qubitium) . i am confirming that i have no changes to the defaults on motherboard bios. it is a bare bones lubuntu install
> 
> [@amd-nicknick](https://github.com/amd-nicknick) not sure how to go about testing on windows. we are a linux only engineering workshop. am i expected to buy a windows license just to test whether my amd card is screwed out of the box??

Can you note your motherboard model and cpu? I am asking because hw does affect AMD gpus. For example, I have multiple intel mbs that AMD gpus 7900 XTX will crash/stall the pcie transveral during bios boot, when there are other gpus (Nvidia or Intel) on the same motherboard, and absolutely hang the workstations. I have not reported this issue because there is zero bios output/stracktrace to speak of. Nvidia and Intel gpus have zero issue co-existing with other gpus on both Intel and AMD mbs. 



---

### 评论 #22 — jlninrr (2026-04-21T16:02:50Z)

Is there a Linux kernel version / driver combo that's intended to work? @lobsteroh lists a lot of combos that didn't work. I'm not at all sure that I need fan control, but I'm also fine with installing latest TheRock builds (I've done that before on other platforms). I've seen people successfully using R9700 on Linux, but they might have downlevel firmware from my card. Primary concerns for me are proper automatic fan response and (preferably) the card not acting like a space heater when under no load at all.

I can verify that the card works properly on Windows. I don't usually use Windows on server computers, but it was worth running the test. Fan works fine, card generates images properly in Amuse, temps look reasonable under load, etc.

---

### 评论 #23 — lobsteroh (2026-04-21T16:10:07Z)

Thank you @Qubitium 
Motherboard: MSI MAG X570 TOMAHAWK WIFI
CPU: AMD Ryzen 9 5900X
Secondary GPU: NVIDIA GTX 1060 (display only, slot 2)
R9700: Slot 1 (primary PCIe x16)
Interesting point about PCIe coexistence issues. I do have both AMD R9700 and NVIDIA 1060 in the same system. However the fan issue persists even with the 1060 removed and R9700 as the only GPU. The SMU mismatch (driver 0x2e vs firmware 0x33) is present from first boot regardless of other hardware.

Thank you @amd-nicknick 
Yes, confirmed on clean Ubuntu 24.04 LTS with amdgpu DKMS installed.
Workloads tested:
- YOLO v8 AI training (primary use case) - GPU reached 109C and thermally throttled
- rocm-bandwidth-test loop (sustained bandwidth stress)
- glxgears / glmark2 (lighter GPU load)
All confirmed fan physically stationary throughout. Not a sensor reporting issue - fan was visually observed not spinning.

Thank you - this is helpful clarification.
On the fan being firmware-controlled by default: I understand the card has a built-in fan curve. My problem is that curve is not triggering on Linux under any load including 109C. The fan was visually confirmed stationary throughout.
Regarding kernel 7.x not being supported - understood. My original test environment was Ubuntu 24.04 with kernel 6.17 and amdgpu DKMS, where the issue was first confirmed. Results were identical - fan not spinning, SMU mismatch present.

---

### 评论 #24 — jlninrr (2026-04-21T16:15:31Z)

I am also running 100% default BIOS settings. No changes.

I'm using a Beelink GTi14 (Intel Ultra 9 185H), 64GB RAM, with Beelink's GPU dock pro.

It sounds like I should give Ubuntu 24.04 a try. My preference is a server install - this system is intended to be headless and used for AI compute only, so I'd rather not install a GUI unless something forces me to. I have one in 26.04, but that's because the AMD installer put one on. I probably used the wrong arguments, though.

And, again, on mine the fan spins on Linux (visually - the tools do not show fan speed, but that's expected). I have not tried any stress whatsoever on the GPU in Linux - no tools installed. I found this thread because of the driver install failures.

---

### 评论 #25 — jlninrr (2026-04-21T20:16:43Z)

I'm now on 24.04, kernel 6.17.0-22, and the driver loads, with the above mentioned /sys entries (hwmon, gpu_od, fw_version, etc) populated. That's the good news.

Bad news: the card is still pretending to be a space heater. The fan is running very fast and producing what I imagine is 300W of heat. At least the fan is running!

The reason I imagine it's 300W is that no monitoring tools seem to work. I'm using the latest (I think) ROCm. rocm-smi says:
ROCM-SMI version: 4.0.0+92b7431876
ROCM-SMI-LIB version: 7.8.0
And rocm-sdk says:
7.13.0a20260421

Looks likely to be latest. Per the changes, I would have expected the rocm-smi updates to be in this build. But virtually nothing populates - no fan speed, no power info, no nothing. And I don't have amdgpu_top, unlike on my Strix Halo (not sure where I got that, though). So I can't get any visibility into the card to know what it's doing / not doing with all of that power. The card should be 100% idle - I'm not using it at all.

Just to add some extra info, after reading the other firmware mismatch thread (https://github.com/ROCm/ROCm/issues/6155):
amdgpu-dkms-firmware/noble,noble,now 30.30.1.0.30300100-2303411.24.04 all [installed,automatic]
amdgpu-dkms/noble,noble,now 1:6.16.13.30300100-2303411.24.04 all [installed]
amdgpu-install/now 30.30.2.0.30300200-2314335.24.04 all [installed,local]
libdrm-amdgpu1/noble-updates,now 2.4.125-1ubuntu0.1~24.04.1 amd64 [installed,automatic]
amdgpu-dkms-firmware/noble,noble,now 30.30.1.0.30300100-2303411.24.04 all [installed,automatic]
firmware-sof-signed/noble-updates,now 2023.12.1-1ubuntu1.10 all [installed,automatic]
linux-firmware/noble-updates,noble-security,now 20240318.git3b128b60-0ubuntu2.26 amd64 [installed,automatic]

[firmware-info.txt](https://github.com/user-attachments/files/26946035/firmware-info.txt)

[dmesg2.txt](https://github.com/user-attachments/files/26946076/dmesg2.txt)

From the dmesg:
[    3.115568] amdgpu 0000:03:00.0: amdgpu: detected ip block number 4 <smu_v14_0_0> (smu)
[    3.425879] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684b00 (104.75.0)
[    3.425883] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[    3.462325] amdgpu 0000:03:00.0: amdgpu: SMU is initialized successfully!

I'll likely shut down since there's no reason to be running a space heater right now, and it doesn't seem like a good idea to stress the card for no reason. This does not happen on Windows - even under load, I never got it as hot as it is right now while idle under Linux.

---

### 评论 #26 — amd-nicknick (2026-04-22T02:22:56Z)

@jlninrr an Ubuntu Server install works as well, just make sure to switch to the HWE kernel instead of the generic kernel (By default Desktop install use HWE, Server use generic).

As for the idle condition, that sounds like a different issue here, let me summarize:
1. @lobsteroh card fan doesn't spin under load at all.
    Let me find the exact card you're using & flash the exact same VBIOS to check this one.
    Could you please provide the following info?
    ```
    cat /sys/kernel/debug/dri/<Device BDF>/amdgpu_firmware_info
    ```
2. @jlninrr Idle power management doesn't seem to work.
    Let's check the driver state for the power gating options. Could you please provide the following info **when the card is idle**?
   ```
    cat /sys/kernel/debug/dri/<Device BDF>/amdgpu_pm_info
   ```
   Also, share the output of amd-smi **(idle as well)**
   ```
   amd-smi
   amd-smi static
   amd-smi metric
   ```
3. Kernel 7 doesn't work at all

Please let me know if I missed anything here, I apologize if I sound repetitive and keep requesting additional information. I have several R9700 units here that do not exhibit any of these reported issues, so I will need some help to troubleshoot this further.

---

### 评论 #27 — jlninrr (2026-04-22T03:26:36Z)

I'm happy to provide additional info. Not a problem.

I'm currently using a clean install of Ubuntu 24.04.4 with HWE (kernel 6.17.0-22). Since the install, I have:
- Installed amdgpu dkms drivers
- Use amdgpu-install with usecase rocm
- Purged and reinstalled dkms drivers (just to be sure)
- Installed TheRock ROCm nightly (gfx1201 - not 100% sure that's right, but I think it is)

For this: cat /sys/kernel/debug/dri/0000\:03\:00.0/amdgpu_pm_info
I got:
cat: '/sys/kernel/debug/dri/0000:03:00.0/amdgpu_pm_info': Timer expired
Followed by (on the next try):
cat: '/sys/kernel/debug/dri/0000:03:00.0/amdgpu_pm_info': Invalid argument
All subsequent tries are 'Invalid argument'. Yes, I am running as root.

Attached is a log of the three amd-smi commands. Lots of N/A.

[smi.txt](https://github.com/user-attachments/files/26953152/smi.txt)

Pretty sure these entries hit dmesg coincident with the first amd-smi command:
[  415.579119] ACPI BIOS Error (bug): Could not resolve symbol [\_SB.PC00.PEG0.PEGP._ON], AE_NOT_FOUND (20250404/psargs-332)

[  415.579131] No Local Variables are initialized for Method [ATPX]

[  415.579132] Initialized Arguments for Method [ATPX]:  (2 arguments defined for method invocation)
[  415.579132]   Arg0:   00000000cdddbbc0 <Obj>           Integer 0000000000000002
[  415.579136]   Arg1:   00000000cc4867a9 <Obj>           Buffer(3) 03 00 01

[  415.579140] ACPI Error: Aborting method \_SB.PC00.GFX0.ATPX due to previous error (AE_NOT_FOUND) (20250404/psparse-529)
[  415.590236] amdgpu 0000:03:00.0: amdgpu: PCIE GART of 512M enabled (table at 0x00000087D6B00000).
[  415.590311] amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
[  415.818980] amdgpu 0000:03:00.0: amdgpu: GECC is disabled
[  415.824278] amdgpu 0000:03:00.0: amdgpu: RAP: optional rap ta ucode is not available
[  415.824280] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[  415.824285] amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
[  415.824288] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684b00 (104.75.0)
[  415.824292] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[  419.577708] amdgpu 0000:03:00.0: amdgpu: SMU: I'm not done with your previous command: SMN_C2PMSG_66:0x00000006 SMN_C2PMSG_82:0x00000000
[  419.577710] amdgpu 0000:03:00.0: amdgpu: Failed to enable requested dpm features!
[  419.577712] amdgpu 0000:03:00.0: amdgpu: Failed to setup smc hw!
[  419.577713] amdgpu 0000:03:00.0: amdgpu: resume of IP block <smu> failed -62
[  419.577716] amdgpu 0000:03:00.0: amdgpu: amdgpu_device_ip_resume failed (-62)

Let me know if I can provide additional info (including debug versions of whatever - this system is not doing anything of importance right now besides debugging this issue).

---

### 评论 #28 — amd-nicknick (2026-04-22T05:06:02Z)

Thanks for your help @jlninrr, I have some idea now. Some further questions: 
Does the dGPU have any display cable attached directly on it? If not, try attaching a display on it & reboot the system.
Also, let's check the device power state when failure occurs as well:
```
cat /sys/class/drm/<DRM card index>/device/power/runtime_status
cat /sys/bus/pci/devices/<Device BDF>/power_state
```
From the logs you provided, it seems like the GPU entered D3 and is unable to wake up. Furthermore, it seems to be using PX (weird because I don't recall this being the proper way to do things on dGPU, I'll check internally).
Let's try to isolate this further by disabling runtime PM, add this to the kernel parameter:
```
amdgpu.runpm=0
```
You might need to update your initramfs depending on how you added this, check `cat /sys/module/amdgpu/parameters/runpm`.
Thank you for your help on troubleshooting this issue!

---

### 评论 #29 — jlninrr (2026-04-22T05:40:35Z)

I do not have any displays attached. I have no DP cables right now. Will have some in ~12 hours, and will update. I don't want a real monitor on it, but a fake EDID device might do the trick.

amdgpu.runpm=0 seems to be a magic bullet. Totally different behavior! I added it manually on boot just to check quickly, and verified with `cat /sys/module/amdgpu/parameters/runpm` (it's zero, as expected).

Here are new amd-smi logs:

[smi2.txt](https://github.com/user-attachments/files/26955639/smi2.txt)

In this state, I get back lots of info, and the card is cool.

For a working system, runtime_status is 'active' . power_state is D0.

For a non-working system, runtime_status is 'error', power_state is D0.

Also, in the non-working state (everything up to now), I get a pile of amdgpu crashes after issuing a reboot command (it does reboot, though). In the working state, no amdgpu crashes.

Am I opening myself up to any trouble by disallowing runpm? Guessing that's normally a good thing. But I certainly don't see runtime power issues (though I'm not applying any load to the card, so I might not see anything).

For now, back to poweroff while I wait for cables to arrive and/or more debug requests.

---

### 评论 #30 — amd-nicknick (2026-04-22T06:02:38Z)

Sounds great! Thanks for helping out. I'll check to see just why the card exposes ATPX (again, I think that's incorrect, it should be BACO).
Disabling runpm will only result in slightly elevated idle power draw. 

On modern dGPUs we support BACO as the primary D3 power saving method. It basically shuts off the entire GPU core and only keeping the PCI bus active for incoming commands / doorbells etc.
If it is turned off (runpm=0), upon entry to pm suspend the driver won't do anything. 
This does NOT prevent the device from power gating various IPs and setting the DPM level to the lowest power state. So, it will only be a slight power draw increase & resume time DECREASE compared to BACO.

One last thing worth trying is to set `amdgpu_runpm=2`, this option attempts a BAMACO, if that isn't available, BACO is used.
Remember to update initramfs, reboot and **attach full dmesg.** 
**If this option works, you could keep this in as a workaround for now.** 
Please make sure to test idle cycles with this: After boot, run some workload, then let it idle for a while (or place system into S3 sleep), then run again (capture dmesg on 2nd run and look for amdgpu resuming messages).

Thanks again, glad we're making progress!

---

### 评论 #31 — jlninrr (2026-04-22T17:31:38Z)

No DP cables yet - delayed. That experiment will be later today. If it's not, probably no earlier than Friday night, maybe Saturday. Traveling most of tomorrow and Friday.

amdgpu.runpm=2 is interesting. Back to BIOS errors, but the card is cool and I get temp and fan data. It looks pretty good - the BIOS errors don't hurt anything that I can see.

dmesg:

[dmesg3.txt](https://github.com/user-attachments/files/26979532/dmesg3.txt)
 
Worth noting that the chunk from 91-98 in dmesg (at the end) repeats every time I run amd-smi. Probably because the card is idle and sleeps and that's it waking up? runpm=0 may be better, if it's safe (and it sounds safe). Or an EDID device/ghost monitor, if that helps.

[smi3.txt](https://github.com/user-attachments/files/26979554/smi3.txt)

Also worth noting that rocm-smi still returns basically nothing. This is the one interesting output line:
0       1     0x7551,   23334  N/A     N/A    N/A, N/A, 0         N/A   N/A   0%   unknown  N/A     0%     0%

I can verify that the fan is not running, so 0% looks right, at least.

---

### 评论 #32 — jlninrr (2026-04-22T18:42:52Z)

Update: I set up lemonade and ran a fairly low-stress setup. Got the fan to 20%.

dmesg after the lemonade run (lemonade is shut down, GPU should be idle):

[dmesg4.txt](https://github.com/user-attachments/files/26980323/dmesg4.txt)

I ran amd-smi a few times, and each time I get a flurry of dmesg entries. The fan has been running the whole time (at 20%).

Half an hour later: back to the original temp, still 20% fan. Not sure the fan will turn off once turned on. But I don't have a problem with that.

---

### 评论 #33 — jlninrr (2026-04-22T21:29:52Z)

And a couple of hours later: still 20% fan. Card still cool. The same  flurry in dmesg, but nothing during the idle hours.

---

### 评论 #34 — jlninrr (2026-04-23T01:53:40Z)

Booting with a monitor was interesting. It came up fine with no runpm setting (reading from the file gave me -1). amd-smi worked. No odd messages in dmesg. I didn't capture; can do later.

Removing the monitor broke things. No more amd-smi data, and the fan went to max. Interestingly, the card was cool, not blowing heat, so that changed apparently permanently with the monitor.

So, a fake EDID setup might work. Not sure. Not my preference, either, but it could be a workaround. It really feels like this card in particular should work on a headless server without faking a monitor, though. Yes, it has four video outs, but it seems likely to be used for mostly GPU compute and not display driving. My guess, anyway.

---

### 评论 #35 — amd-nicknick (2026-04-23T08:50:31Z)

@jlninrr Ok I know what's going on now. I realized you're using an external GPU box. I think this is a platform/eGPU issue here:
Our driver decides what runtime power management method is used by:
* ASIC support
* PX support
* If the device is removable (eGPU)
* Override flags
In your scenario, your system seems to be reporting to amdgpu that the GPU is **NOT** removable. In addition to additional ACPI methods attached to the bus object, this makes the driver think this is a hybrid graphics setup. (ATPX, which uses these platform ACPI methods to control mobile GPU power).
Obviously, that's not correct in your scenario, leading to all sorts of problem you see.

Based on your log with runpm=2, I can see the card suspending / resuming correctly. However, it still attempts to use the ATPX ACPI method. I'll trace a bit to see what's going on there, but it's harmless.

The amd-smi log you provided actually looks correct. Not all (in fact, only a few) of the telemetry is reported / available for non-MI cards.

The reason connecting a monitor works is because the GPU won't enter D3 in that case (The DC hardware needs to be active to drive monitor output), so it's more closely related to runpm=0.
The moment you disconnect the monitor, the GPU's power state drops to D3, causing the incorrect power control being used again.

---

### 评论 #36 — lobsteroh (2026-04-23T10:19:48Z)

I apologize for being late on my report. Not caused by a lack of interest. I am still away from our compute setup snd will only be back in my office in 10 days. I will report the requested logs then. 

---

### 评论 #37 — amd-nicknick (2026-04-23T10:21:00Z)

@lobsteroh No problem, I'll keep this issue open & in monitoring. Please ping me once you have more information to share. Thanks!

---

### 评论 #38 — jlninrr (2026-04-25T00:29:55Z)

That's correct. It's nominally an eGPU. Not quite the usual - the Beelink dock is direct connect to the device motherboard (so neither USB4 nor Oculink). But the GPU should not be 'removable' (no hot swap, etc). If there's a flag to turn off hybrid, that may make sense.

I may be moving the card to a different system. It will still be an eGPU. Not sure yet, though. I'm done traveling but it'll be a day or two before I have it back online.

---

### 评论 #39 — S3phe (2026-04-25T21:06:36Z)

Same issue here - ASUS Radeon AI Pro 9700, that there is a smu driver/firmware mismatch.

-> Main problem: Radeon AI Pro 9700 is too loud, power target < 210W impossible, also a fan speed < 30%.

```
dmesg 
[    6.260664] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000002e, smu fw if version = 0x00000032, smu fw program = 0, smu fw version = 0x00684a00 (104.74.0)
[    6.260665] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[    6.284008] amdgpu 0000:03:00.0: amdgpu: SMU is initialized successfully!

lspci | grep Navi
03:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 48 [Radeon AI PRO R9700] (rev c0)
03:00.1 Audio device: Advanced Micro Devices, Inc. [AMD/ATI] Navi 48 HDMI/DP Audio Controller

uname -r
6.17.0-113020-tuxedo
```




---

### 评论 #40 — lobsteroh (2026-05-04T14:35:18Z)

@amd-nicknick i just got back to the setup and am including requested info below.

At this point i need to figure out whether the card is broken and i need to replace it or whether framework for this card is broken and i need to switch to supported hardware. Asus support was less than helpful with suggestion to - "test and run on windows" - sigh

see more about our project with AMD on bringing AI and industrial automation to aquaculture <https://www.amd.com/en/resources/case-studies/radmantis.html>

VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b9a
PFP feature version: 29, firmware version: 0x00000bea
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000cda
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3805204, firmware version: 0x003a1014
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684c00 (104.76.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x0910c00f                                                                                                                                                      
DMCU feature version: 0, firmware version: 0x00000000                                                                                                                                                     
DMCUB feature version: 0, firmware version: 0x0a000800                                                                                                                                                    
TOC feature version: 0, firmware version: 0x00000000                                                                                                                                                      
MES_KIQ feature version: 1, firmware version: 0x00000089                                                                                                                                                  
MES feature version: 1, firmware version: 0x00000089                                                                                                                                                      
VPE feature version: 0, firmware version: 0x00000000                                                                                                                                                      
VBIOS version: 115-G287BP00-100                                         

---

### 评论 #41 — Aqua1ung (2026-05-04T14:53:47Z)

Lots of issues with 9000 amdgpus as well due to this mismatch: [here](https://pcforum.amd.com/s/question/0D5Pd00001S3Av9KAF/linux-9060xt-egpuoverthunderbolt-bugs-galore), [here](https://gitlab.freedesktop.org/drm/amd/-/work_items/5243), and [here](https://www.reddit.com/r/AMDHelp/comments/1rnmh88/linux_smu_if_mismatch_driver_0x2e_vs_firmware_0x32/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button).

---

### 评论 #42 — amd-nicknick (2026-05-05T12:22:56Z)

@lobsteroh thanks for the FW dump, I compared my setup with yours, and the system management related firmwares we're using is identical.
We have a new preview amdgpu-dkms version available with some changes, as a last step, could you please give it a try?
Purge your previous driver installation first
```
sudo apt autoremove --purge amdgpu-dkms
```
Update your APT source to use 31.20 preview by following the steps here:
https://instinct.docs.amd.com/projects/amdgpu-docs/en/31.20.0-preview/install/detailed-install/package-manager/package-manager-ubuntu.html

---

### 评论 #43 — amd-nicknick (2026-05-05T12:27:10Z)

@Aqua1ung, the SMU driver interface mismatch is harmless and irreverent. It is not an issue at all.

---

### 评论 #44 — S3phe (2026-05-05T14:16:44Z)

@amd-nicknick : Do you think it will be possible to reduce fan speed below 30% if temperatures < 50°C? That would be great!

---

### 评论 #45 — amd-nicknick (2026-05-05T14:33:01Z)

@S3phe, could you try and report back if `sudo amd-smi set --fan 30%` works on your system? Also, which card are you using? (Paste in the full `amdgpu_firmware_info` as well, that helps me confirm.)

---

### 评论 #46 — S3phe (2026-05-05T14:44:07Z)

ASUS Radeon AI Pro 9700  Turbo

```shell
cat /sys/kernel/debug/dri/1/amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x00000b9a
PFP feature version: 29, firmware version: 0x00000bea
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1000, firmware version: 0x00be7da0
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 0, firmware version: 0x00000000
RLCV feature version: 0, firmware version: 0x00000000
MEC feature version: 29, firmware version: 0x00000cda
IMU feature version: 0, firmware version: 0x0c302b00
SOS feature version: 3805204, firmware version: 0x003a1014
ASD feature version: 553648393, firmware version: 0x21000109
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b3a0001
TA HDCP feature version: 0x00000000, firmware version: 0x1700004d
TA DTM feature version: 0x00000000, firmware version: 0x1200001d
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x00684c00 (104.76.0)
SDMA0 feature version: 1081708182, firmware version: 0x00798e96
SDMA1 feature version: 1081708182, firmware version: 0x00798e96
VCN feature version: 0, firmware version: 0x0910c00f
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x0a000a00
TOC feature version: 0, firmware version: 0x00000000
MES_KIQ feature version: 1, firmware version: 0x00000089
MES feature version: 1, firmware version: 0x00000089
VPE feature version: 0, firmware version: 0x00000000
VBIOS version: 115-G287BP00-100

amd-smi: Command not found.
``` 



```shell
rocm-smi 

========================= ROCm System Management Interface =========================
=================================== Concise Info ===================================
GPU[0]          : get_power_avg, Not supported on the given system
Exception caught: map::at
ERROR: GPU[0]   : sclk clock is unsupported
====================================================================================
GPU[0]          : get_power_cap, Not supported on the given system
GPU  Temp (DieEdge)  AvgPwr  SCLK   MCLK     Fan    Perf  PwrCap       VRAM%  GPU%  
0    50.0c           N/A     None   2400Mhz  0%     auto  Unsupported    1%   0%    
1    47.0c           50.0W   72Mhz  1258Mhz  29.8%  auto  300.0W        17%   4%    
====================================================================================
=============================== End of ROCm SMI Log ================================

cat /proc/cmdline
..... mem_sleep_default=deep amd_iommu=on iommu=pt amdgpu.ppfeaturemask=0xffffffff 
``` 

--> Changing fan curve/speed/power limit via lact works.

---

### 评论 #47 — amd-nicknick (2026-05-05T15:33:12Z)

> --> Changing fan curve/speed/power limit via lact works.

@S3phe that's good. LACT uses the PMFW interface, so your setup looks good.
From the rocm-smi output you provided, the fan is spinning @ 30% and temp is at ~50. 

You could read the current fan curve manually by running `sudo cat /sys/class/drm/card1/device/gpu_od/fan_ctrl/fan_curve`, this should tell you your current GPU's applied curve and its target.

If you're asking if it's possible to reduce the fan speed to under 30% (other than turning it off completely), that might not be physically possible, fans have a RPM range and anything below its floor will stop the fan from spinning.

---

### 评论 #48 — jlninrr (2026-05-08T16:15:06Z)

I should probably chime in, since I've been quiet. I went with a DisplayPort fake monitor / EDID plug and my issues are basically gone. The card is doing what it should be, and I'm using it fairly heavily. However, there are some oddities. Right now, amd-smi shows the card at 100% used, but it's idle (meaning: two llama-cpps are running, VRAM is heavily loaded, but neither is doing any processing). amdgpu_top shows 0% for all categories for the llama-cpp processes, but GRBM-Graphics Pipe 100%, GRBM2 Fetcher and Compute at 100%, Efficiency Arbiter at 97%. Not sure if this is expected. The chip is hot (74C) but the fan is low (26%, about 1500RPM). It's pulling 100W. It's entirely possible that this is expected, but it surprised me. On my Strix Halo system, GPU use shows 0% when llama-server is loaded but doing nothing.

Other minor gripes:
It's ostensibly a server GPU. Still not sure why it has to have a fake monitor. That seems glitchy. Fine, but glitchy. 
Kernel 7.x / Ubuntu 26.04 support will be nice. I'm sure it's being worked on.

I am on amdgpu 30.30.1. Would it be worthwhile to move up to 31.20 preview? I don't want to change things just to change things, but the changes look interesting.

Thank you all again for your help!

---

### 评论 #49 — amd-nicknick (2026-05-09T07:03:05Z)

@jlninrr I wouldn’t classify the external monitor problem as the card / driver's fault. The platform should really announce the card as detachable in all eGPU scenarios. That's a platform / ebox issue. Plugging a fake edid dongle into the card has the same effect as turning runpm to off. 

Ubuntu 26 support: yes it's actively being worked on. 

For the utilization issue, we recently resolved a MES FW issue where it would get stuck if notify doorbell is used on Linux. While there is not enough info to confirm this is what you’re seeing, the symptom looks like the same. 
Could you please give 31.20 dkms & firmware a try? You should see MES FW 0x8B -> this contains the fix. 

---

### 评论 #50 — jlninrr (2026-05-09T20:32:15Z)

31.20 seems to fix the utilization issue. It's not 0% when I might expect that, but 2-5%. And temps are much lower (45C, and that's right after an inferencing run). 

I'm not sure I agree about the eGPU issue. Yes, it's technically an eGPU. However, it's connected PCI to PCI (PCI 5.0 x8). No Oculink, much less USB4 etc. It's no more detachable than any other PCI-attached GPU. Logically speaking, it would make no sense to report it as removable, unless I'm missing something. So, maybe the problem is that it's not supporting something else that it should?

---

### 评论 #51 — opticblu (2026-05-12T22:33:58Z)

> [@jlninrr](https://github.com/jlninrr) I wouldn’t classify the external monitor problem as the card / driver's fault. The platform should really announce the card as detachable in all eGPU scenarios. That's a platform / ebox issue. Plugging a fake edid dongle into the card has the same effect as turning runpm to off.
> 
> Ubuntu 26 support: yes it's actively being worked on.
> 
> For the utilization issue, we recently resolved a MES FW issue where it would get stuck if notify doorbell is used on Linux. While there is not enough info to confirm this is what you’re seeing, the symptom looks like the same. Could you please give 31.20 dkms & firmware a try? You should see MES FW 0x8B -> this contains the fix.

I tested 31.20 on Ubuntu 24.04 with amdgpu-dkms 6.19.0 and amdgpu-dkms-firmware 31.20.0.0.31200000-2307534.24.04.

The regression is worse: before 31.20 one R9700 reported stuck at 100%; after 31.20 both do, and llama.cpp decode throughput dropped about 10.8%.

The SMU mismatch is still present after reboot:
smu driver if version = 0x0000002e
smu fw if version = 0x00000032
SMU driver if version not matched

So 31.20 did not fix the root SMU interface mismatch for this R9700 setup.


---

### 评论 #52 — amd-nicknick (2026-05-19T10:43:14Z)

@jlninrr, sorry for the delayed response. Following up on your GPU setup. Do you mind explaining to me more about how your eGPU is configured? Eg. What box did you use, your platform config, what is connected to what by what...

---
