# 7900xt limited to 265W

> **Issue #2256**
> **状态**: closed
> **创建时间**: 2023-06-20T13:23:07Z
> **更新时间**: 2025-06-16T16:36:51Z
> **关闭时间**: 2024-01-02T18:31:12Z
> **作者**: nesdeq
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2256

## 描述

I am trying to use 7900xt with rocm to full potential and noticed, that 

```
========================ROCm System Management Interface========================
================================================================================
GPU  Temp   AvgPwr  SCLK   MCLK   Fan   Perf  PwrCap  VRAM%  GPU%  
1    46.0c  18.0W   23Mhz  96Mhz  0.0%  auto  265.0W    4%   0%    
================================================================================
==============================End of ROCm SMI Log ==============================
```

the card is running with a PowerCap of 265W when the spec says it should at least be 300W. I tried setting manually with 

`~ rocm-smi --setpoweroverdrive 300` but result is

`ERROR: GPU[1]	: Value cannot be greater than 265W`.

I am running a fairly current kernel `6.3.8-200.fc38.x86_64`.

The only info i could find similar to this is an old issue from 2018 regarding a VEGA GPU that was also limited to 265 and fixed in upstream drivers later on. 

Any guidance on this?


---

## 评论 (6 条)

### 评论 #1 — nesdeq (2023-06-27T06:29:52Z)

rocm* from fedora38 repos and torch nightlies with rocm5.5 do the trick for my ml needs...

Sent from Proton Mail mobile

-------- Original Message --------
On 21 Jun 2023, 23:12, qinanO wrote:

> How did you do it? My rocm5.5 didn't find my 7900xt
>
> —
> Reply to this email directly, [view it on GitHub](https://github.com/RadeonOpenCompute/ROCm/issues/2256#issuecomment-1601683784), or [unsubscribe](https://github.com/notifications/unsubscribe-auth/A6YTL5EHX4DYGCBQ2IVZBETXMNPTHANCNFSM6AAAAAAZNJENDQ).
> You are receiving this because you authored the thread.Message ID: ***@***.***>

---

### 评论 #2 — kentrussell (2023-11-10T16:18:55Z)

Which partner made your 7900XT? They may have set the power cap lower in their VBIOS due to some small tweaks to the card. The max wattage comes from the VBIOS, so that is where the kernel determines what the max TDP is supposed to be.

---

### 评论 #3 — kentrussell (2024-01-02T18:31:12Z)

Closing off due to no response. Please reopen once you can get me that info!

---

### 评论 #4 — andrew-aladjev (2025-06-14T07:10:10Z)

@kentrussell I am interested in buying new AMD GPUs for AI inference. But I want to be sure that I will be able to set good minimal TDP. Can you please point me to the list of minimal/maximum TDP for supported and new GPUs? For example it can be the source code file. Thank you.

---

### 评论 #5 — nesdeq (2025-06-14T07:51:56Z)

@kentrussell , @andrew-aladjev - sorry for not updating. i could solve the issues they had nothing to do with rocm. reported powerlevel (in watts) on linux has different baseline than on windows which is just weird. one takes board pcie power draw into account the other does not, that's where my original confusion came from (see above).

nvm, setting the following kernel parameters: amdgpu.ppfeaturemask=0xffffffff amd_pstate=active amdgpu.msi=1 amdgpu.sched_jobs=64 amdgpu.sched_hw_submission=4 amdgpu.cwsr_enable=1 amdgpu.mes=1 amdgpu.uni_mes=1 amdgpu.vm_update_mode=0

i am able to set power limit to up to 305w. i have stable long time inference (via ollama) at 290w powerlimit (vs 265 default), and -75mv voltage offset (to achieve higher clock speed).

---

### 评论 #6 — kentrussell (2025-06-16T16:35:35Z)

@nesdeq Glad to see that you were able to figure that out. The Windows vs Linux driver will always be a fun thing to try to nail down, so I'm glad you were able to get that working the way you wanted!

@andrew-aladjev The TDP is kept inside the VBIOS, so there's no source-code file to dump specifically. As an example, showing the max cap calls amdgpu_hwmon_show_power_cap_generic , which calls amdgpu_dpm_get_power_limit which calls  pp_funcs->get_power_limit , 
which would call a function like smu_v13_0_7_get_power_limit for NV33. The NV33 function looks like:
https://github.com/ROCm/ROCK-Kernel-Driver/blob/master/drivers/gpu/drm/amd/pm/swsmu/smu13/smu_v13_0_7_ppt.c#L2408
That all comes out of the SMU, which interacts directly with the VBIOS.
To find the TDP, you're going to have to go through the card manufacturer, since they can (and do) modify their own VBIOS to suit their use case. We will put the TDP specs on our site for cards we manufacture in totality, like the MI300A (https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300a-data-sheet.pdf showing 550W for air+liquid cooled, and 760W for liquid cooled). For the Radeon cards, it can vary since we have partners who make the actual card. For example, on the 7900XT, they were made by Sapphire, ASUS, XFX, PowerColor, Gigabyte, MSI, etc.

Sapphire says 308W: https://www.sapphiretech.com/en/consumer/21323-01-20g-radeon-rx-7900-xt-20g-gddr6#Specification
MSI says 315W: https://storage-asset.msi.com/datasheet/vga/global/Radeon-RX-7900-XT-GAMING-TRIO-CLASSIC-20G.pdf
TechPowerup (not an official source) says 300W for the generic review: https://www.techpowerup.com/gpu-specs/radeon-rx-7900-xt.c3912
Asus, XFX, PowerColor and Gigabyte don't say on their respective product pages. 

Thus, it's always good to check with the manufacturing partner to verify the specs though, since each VBIOS can have its own unique value. And in the end, that's what the kernel driver will reference during Power Management actions.

---
