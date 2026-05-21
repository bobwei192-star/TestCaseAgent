# [Issue]: Strix Halo (gfx1151) - ROCm only seeing 62.2GB instead of allocated VRAM with ROCm 7.0.2

> **Issue #5595**
> **状态**: open
> **创建时间**: 2025-10-29T11:07:53Z
> **更新时间**: 2025-10-29T14:53:06Z
> **作者**: jeremyyx
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5595

## 描述

### Problem Description

sudo dmesg | grep amdgpu
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.14.0-1014-oem root=UUID=d55f0c3f-88f5-4c65-a93a-285c1a30361c ro quiet splash amdgpu.gtt_size=122880 vt.handoff=7
[    0.070283] Kernel command line: BOOT_IMAGE=/boot/vmlinuz-6.14.0-1014-oem root=UUID=d55f0c3f-88f5-4c65-a93a-285c1a30361c ro quiet splash amdgpu.gtt_size=122880 vt.handoff=7
[    3.636913] amdgpu: unknown parameter 'gtt_size' ignored
[    3.646006] amdgpu 0000:c6:00.0: amdgpu: [drm] Configuring gttsize via module parameter is deprecated, please use ttm.pages_limit
(base) tiiny@mais-axb3502:~$ sudo dmesg | grep amdgpu
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.14.0-1014-oem root=UUID=d55f0c3f-88f5-4c65-a93a-285c1a30361c ro quiet splash amdgpu.gtt_size=122880 vt.handoff=7
[    0.070283] Kernel command line: BOOT_IMAGE=/boot/vmlinuz-6.14.0-1014-oem root=UUID=d55f0c3f-88f5-4c65-a93a-285c1a30361c ro quiet splash amdgpu.gtt_size=122880 vt.handoff=7
[    3.636913] amdgpu: unknown parameter 'gtt_size' ignored
[    3.637316] [drm] amdgpu kernel modesetting enabled.
[    3.637316] [drm] amdgpu version: 6.14.14
[    3.638704] amdgpu: Virtual CRAT table created for CPU
[    3.638710] amdgpu: Topology: Add CPU node
[    3.641089] amdgpu 0000:c6:00.0: enabling device (0006 -> 0007)
[    3.644221] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 0 <soc21_common>
[    3.644223] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 1 <gmc_v11_0>
[    3.644223] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 2 <ih_v6_1>
[    3.644224] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 3 <psp>
[    3.644224] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 4 <smu>
[    3.644225] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 5 <dm>
[    3.644226] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 6 <gfx_v11_0>
[    3.644226] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 7 <sdma_v6_0>
[    3.644227] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 8 <vcn_v4_0_5>
[    3.644228] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 9 <jpeg_v4_0_5>
[    3.644228] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 10 <mes_v11_0>
[    3.644229] amdgpu 0000:c6:00.0: amdgpu: detected ip block number 11 <vpe_v6_1>
[    3.644252] amdgpu 0000:c6:00.0: amdgpu: Fetched VBIOS from VFCT
[    3.644253] amdgpu: ATOM BIOS: 113-STRXLGEN-001
[    3.645840] amdgpu 0000:c6:00.0: amdgpu: VPE: collaborate mode true
[    3.645844] amdgpu 0000:c6:00.0: amdgpu: Trusted Memory Zone (TMZ) feature disabled as experimental (default)
[    3.645917] amdgpu 0000:c6:00.0: amdgpu: VRAM: 1024M 0x0000008000000000 - 0x000000803FFFFFFF (1024M used)
[    3.645918] amdgpu 0000:c6:00.0: amdgpu: GART: 512M 0x00007FFF00000000 - 0x00007FFF1FFFFFFF
[    3.646006] [drm] amdgpu: 1024M of VRAM memory ready
[    3.646006] amdgpu 0000:c6:00.0: amdgpu: [drm] Configuring gttsize via module parameter is deprecated, please use ttm.pages_limit
[    3.646007] amdgpu 0000:c6:00.0: amdgpu: [drm] GTT size has been set as 128849018880 but TTM size has been set as 66818834432, this is unusual
[    3.646008] [drm] amdgpu: 122880M of GTT memory ready.
[    3.647114] amdgpu 0000:c6:00.0: amdgpu: [drm] Loading DMUB firmware via PSP: version=0x09002600
[    3.647494] amdgpu 0000:c6:00.0: amdgpu: Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 11
[    3.647535] amdgpu 0000:c6:00.0: amdgpu: Found VCN firmware Version ENC: 1.24 DEC: 9 VEP: 0 Revision: 11
[    3.670790] amdgpu 0000:c6:00.0: amdgpu: reserve 0x8c00000 from 0x8020000000 for PSP TMR
[    4.005583] amdgpu 0000:c6:00.0: amdgpu: RAS: optional ras ta ucode is not available
[    4.009481] amdgpu 0000:c6:00.0: amdgpu: RAP: optional rap ta ucode is not available
[    4.009482] amdgpu 0000:c6:00.0: amdgpu: SECUREDISPLAY: optional securedisplay ta ucode is not available
[    4.046228] amdgpu 0000:c6:00.0: amdgpu: SMU is initialized successfully!
[    4.047574] amdgpu 0000:c6:00.0: amdgpu: [drm] Display Core v3.2.339 initialized on DCN 3.5.1
[    4.047575] amdgpu 0000:c6:00.0: amdgpu: [drm] DP-HDMI FRL PCON supported
[    4.050541] amdgpu 0000:c6:00.0: amdgpu: [drm] DMUB hardware initialized: version=0x09002600
[    4.053502] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.053695] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.053861] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.054015] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.054171] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.054255] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.054336] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.054415] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.054492] amdgpu 0000:c6:00.0: amdgpu: [drm] PSR support 0, DC PSR ver -1, sink PSR ver 0 DPCD caps 0x0 su_y_granularity 0
[    4.063403] kfd kfd: amdgpu: Allocated 3969056 bytes on gart
[    4.063408] kfd kfd: amdgpu: Total number of KFD nodes to be created: 1
[    4.064324] amdgpu: Virtual CRAT table created for GPU
[    4.065195] amdgpu: Topology: Add dGPU node [0x1586:0x1002]
[    4.065196] kfd kfd: amdgpu: added device 1002:1586
[    4.065204] amdgpu 0000:c6:00.0: amdgpu: SE 2, SH per SE 2, CU per SH 10, active_cu_number 40
[    4.065207] amdgpu 0000:c6:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[    4.065208] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[    4.065208] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[    4.065209] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[    4.065209] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[    4.065209] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[    4.065210] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[    4.065210] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[    4.065211] amdgpu 0000:c6:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[    4.065211] amdgpu 0000:c6:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[    4.065211] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_0 uses VM inv eng 0 on hub 8
[    4.065212] amdgpu 0000:c6:00.0: amdgpu: ring vcn_unified_1 uses VM inv eng 1 on hub 8
[    4.065212] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec_0 uses VM inv eng 4 on hub 8
[    4.065212] amdgpu 0000:c6:00.0: amdgpu: ring jpeg_dec_1 uses VM inv eng 6 on hub 8
[    4.065213] amdgpu 0000:c6:00.0: amdgpu: ring mes_kiq_3.1.0 uses VM inv eng 13 on hub 0
[    4.065213] amdgpu 0000:c6:00.0: amdgpu: ring vpe uses VM inv eng 7 on hub 8
[    4.066375] amdgpu 0000:c6:00.0: amdgpu: Runtime PM not available
[    4.066881] amdgpu 0000:c6:00.0: [drm] Registered 4 planes with drm panic
[    4.066882] [drm] Initialized amdgpu 3.64.0 for 0000:c6:00.0 on minor 0
[    4.079409] amdgpu 0000:c6:00.0: [drm] Cannot find any crtc or sizes
[    6.681111] snd_hda_intel 0000:c6:00.1: bound 0000:c6:00.0 (ops amdgpu_dm_audio_component_bind_ops [amdgpu])
And with 
`amd-ttm`
💻 Current TTM pages limit: 31457280 pages (120.00 GB)
💻 Total system memory: 124.46 GB

But with the following code:
```
    hipDeviceProp_t prop;
    CHECK_HIP(hipGetDeviceProperties(&prop, 0)); 
    
    std::cout << "\nDevice 0: " << prop.name << std::endl;
    std::cout << "Total Global Memory: " << (double)prop.totalGlobalMem / (1024*1024*1024) << " GB" << std::endl;
    std::cout << "Max allocation size: " << (double)prop.totalGlobalMem / (1024*1024*1024) << " GB" << std::endl;
```
The output is:
```
Device 0: AMD Radeon Graphics
Total Global Memory: 62.2299 GB
Max allocation size: 62.2299 GB
```

### Operating System

Linux mais-axb3502 6.14.0-1014-oem #14-Ubuntu SMP PREEMPT_DYNAMIC Thu Oct  2 05:10:10 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux

### CPU

AIMAX395+

### GPU

AIMAX395+

### ROCm Version

7.0.2

### ROCm Component

HIP

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — ianbmacdonald (2025-10-29T11:18:46Z)

The clue is `[ 3.646007] amdgpu 0000:c6:00.0: amdgpu: [drm] GTT size has been set as 128849018880 but TTM size has been set as 66818834432, this is unusual `

You need to tweak the kernel parameter ; https://github.com/ROCm/ROCm/issues/5562

---

### 评论 #2 — jeremyyx (2025-10-29T11:27:14Z)

Thanks for you help!
I set in file /etc/modprobe.d/amdgpu_llm_optimized.conf  with the following command
options ttm pages_limit=31457280
options ttm page_pool_size=15728640

And amd-ttm tool tell me that 
💻 Current TTM pages limit: 31457280 pages (120.00 GB)
💻 Total system memory: 124.46 GB

So I'm confused.

Could you give me more advice?


---

### 评论 #3 — ianbmacdonald (2025-10-29T13:30:32Z)

Sure;  I actually rewrote this comment after confusing myself.  amd-ttm is handy in that it does the pages to memory in GiB conversion for you.  It really should say `GiB` to avoid even more confusion with GB!=GiB.  

The fact that you see ` amdgpu: 122880M of GTT memory ready` does not align with your code's output.  I am wondering if that dmesg output and your test were possibly in different sessions.   Here are some places where the confusion might arise. 

amd-ttm in amd-debug-tools 0.2.9 updates parameters for ttm module in the version I pulled from PyPI.  I think it is confused when both ttm and amdttm are present, which is the case with `linux-oem-24.04c` on my 24.04 instance.  It doesn't emit a version at runtime, so hard to know if it always worked this way;  I hope it does in future versions. 

```
imac@ai2:~/src/amd$ lsmod | grep ttm
amddrm_ttm_helper      12288  1 amdgpu
amdttm                131072  2 amdgpu,amddrm_ttm_helper
amdkcl                 49152  4 amd_sched,amdttm,amddrm_exec,amdgpu
drm_ttm_helper         16384  2 amdgpu
ttm                   118784  1 drm_ttm_helper
```

To be safe, replicate your ttm.conf to amdttm.conf to be sure parameters apply to both modules.   I was under the impression these do the same thing, and amdttm was just around for legacy kernels (<6.16) requiring the amdgpu-dkms package to provide a modern amdgpu kernel module.  

```
# /etc/modprobe.d/amdttm.conf
options amdttm pages_limit=31457280
```

The amd-ttm output can also be confusing as it is not clear if it is presenting the defined configuration (what it configured in ttm.conf / amdttm.conf), the installed configuration (what was installed into initramfs to load on next boot) or the running configuration (what is currently booted).   

The tool should also run `update-initramfs -u -k all`, as without this step you are going to just be rebooting with whatever happened to be in that module configuration file the last time initramfs was updated.  

In your case, things are further confused because you are using the amdgpu.gtt_size parameter (widely published in outofdate howtos), probably in your grub configuration.  This setting is deprecated,  and is overriding the pages_limit setting.  This is creating the warning messages.  I would recommend removing it. 

In my case, I can run your program with the expected output. 


```
$ cat /etc/modprobe.d/amdttm.conf 
# /etc/modprobe.d/amdttm.conf
options amdttm pages_limit=31457280

$ cat /etc/modprobe.d/ttm.conf 
# /etc/modprobe.d/ttm.conf
options ttm pages_limit=31457280

$ uname -a
Linux ai2 6.14.0-1014-oem #14-Ubuntu SMP PREEMPT_DYNAMIC Thu Oct  2 05:10:10 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux

$sudo  cat /sys/kernel/debug/dri/128/amdgpu_firmware_info | grep MES
MES_KIQ feature version: 6, firmware version: 0x0000006f
MES feature version: 1, firmware version: 0x00000080

$ sudo dmesg | grep amdgpu | grep memory
[    4.120197] [drm] amdgpu: 512M of VRAM memory ready
[    4.120199] [drm] amdgpu: 122880M of GTT memory ready.

$ ./device_info 

Device 0: AMD Radeon Graphics
Total Global Memory: 120 GiB
Max allocation size: 120 GiB
```


---
