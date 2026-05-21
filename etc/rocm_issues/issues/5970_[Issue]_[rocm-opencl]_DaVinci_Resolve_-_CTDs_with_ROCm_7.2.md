# [Issue]: [rocm-opencl] DaVinci Resolve - CTDs with ROCm 7.2

> **Issue #5970**
> **状态**: closed
> **创建时间**: 2026-02-16T15:35:49Z
> **更新时间**: 2026-04-07T13:14:38Z
> **关闭时间**: 2026-04-01T15:35:32Z
> **作者**: Vikingtons
> **标签**: status: fix submitted
> **URL**: https://github.com/ROCm/ROCm/issues/5970

## 标签

- **status: fix submitted** (颜色: #75d97e)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Several end users are reporting that ROCm 7.2 introduces an issue with the DFP application [Davinci Resolve Studio](https://www.blackmagicdesign.com/products/davinciresolve/studio).

They note that rolling back to ROCm 7.11 works around these failures. There are several posts describing this issue across various forums and communities:

- [Lemmy.world | PSA for those using DaVinci Resolve with AMD GPUs, don't install ROCM 7.2, stay on 7.1.1](https://lemmy.world/post/43115302)
- [EndeavourOS Forums | Can´t use Davinci Resolve Studio | Crash to Desktop](https://forum.endeavouros.com/t/can-t-use-davinci-resolve-studio-crash-to-desktop/77870/11)
- [ArchLinux Pacages | davinci-resolve-studio 20.3.2-1](https://aur.archlinux.org/packages/davinci-resolve-studio#comment-1058336)

The last resource notes:

<img width="1241" height="165" alt="Image" src="https://github.com/user-attachments/assets/59164246-c943-4143-a223-4584a84d2671" />

...this seems to be related to rocm-opencl in the 7.2 package.

I'll borrow one of the system configurations from the forum posts as I've not directly reproduced the issue.

(any AMDers with questions can reach out to Vik (UserExp.&StrategyUK) on teams)

### Operating System

EndeavourOS

### CPU

AMD Ryzen 5 3600

### GPU

EndeavourOS Graphics card: AMD

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

1. (Borrowing repro steps from https://forum.endeavouros.com/t/can-t-use-davinci-resolve-studio-crash-to-desktop/77870 )
2. Provision any contemporary linux distro with hw / sw support for ROCm 7.2. Ubuntu should reproduce this issue as well as others
3. Install DaVinci Resolve Studio (will require sign-up)
4. Launch DaVinci Resolve Studio and create a new project
5. Once the environment has loaded, attempt to import any video, or click on the cut or edit menu options
6. Observe CTD

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

Console & log output:
```[sfox~]$ /opt/resolve/bin/resolve  
ActCCMessage Already in Table: Code= c005, Mode= 13, Level=  1, CmdKey= -1, Option= 0  
ActCCMessage Already in Table: Code= c006, Mode= 13, Level=  1, CmdKey= -1, Option= 0  
ActCCMessage Already in Table: Code= c007, Mode= 13, Level=  1, CmdKey= -1, Option= 0  
ActCCMessage Already in Table: Code= 2282, Mode=  0, Level=  0, CmdKey= 8, Option= 0  
20.3.1.0006 Linux/Clang x86_64  
Main thread starts: D71D0000  
0x7fd5d71d0000 | Undefined            | INFO  | 2026-01-30 16:11:01,630 | --------------------------------------------------------------------------------  
0x7fd5d71d0000 | Undefined            | INFO  | 2026-01-30 16:11:01,630 | Loaded log config from /home/sfox/.local/share/DaVinciResolve/configs/log-conf.xml  
0x7fd5d71d0000 | Undefined            | INFO  | 2026-01-30 16:11:01,630 | --------------------------------------------------------------------------------  
FusionScript Server [36924] Started  
Host 'Resolve' [36476] Added  
Host 'Resolve' Killed  
FusionScript Server [36924] Terminated  
[sfox~]$



==========[CRASH DUMP]==========  
#TIME Fri Jan 30 16:00:08 2026 - Uptime 00:00:15 (hh:mm:ss)  
#PROGRAM_NAME DaVinci Resolve Studio v20.3.1.0006 (Linux/Clang x86_64)  
#BMD_ARCHITECTURE x86_64  
#BMD_BUILD_UUID 5f90fb54-d661-4f14-9db1-3148eb6eb0f  
#BMD_GIT_COMMIT d031039b09e055f0d8d437a51ff3d87f364f4765  
#BMD_UTIL_VERSION 20.3.1.0006  
#OS Linux  
  
/opt/resolve/bin/resolve() [0x6087e49]  
/opt/resolve/bin/resolve() [0x6087012]  
/usr/lib/libc.so.6(+0x3e4d0) [0x7f4543c4d4d0]  
/opt/resolve/bin/../libs/libProResRAW.so(_ZNSt10filesystem7__cxx114path14_M_split_cmptsEv+0x38) [0x7f45358da708]  
/usr/lib/libRusticlOpenCL.so.1(+0xb17c39) [0x7f44e9517c39]  
/usr/lib/libRusticlOpenCL.so.1(+0xb1fcea) [0x7f44e951fcea]  
/usr/lib/libRusticlOpenCL.so.1(+0xb109b6) [0x7f44e95109b6]  
/usr/lib/libRusticlOpenCL.so.1(+0x25a902) [0x7f44e8c5a902]  
/usr/lib/libRusticlOpenCL.so.1(+0x235bf7) [0x7f44e8c35bf7]  
/usr/lib/libRusticlOpenCL.so.1(+0x2350a4) [0x7f44e8c350a4]  
/usr/lib/libRusticlOpenCL.so.1(+0x170400) [0x7f44e8b70400]  
/usr/lib/libRusticlOpenCL.so.1(+0x4039e5) [0x7f44e8e039e5]  
/usr/lib/libRusticlOpenCL.so.1(+0x44c2dd) [0x7f44e8e4c2dd]  
/usr/lib/libc.so.6(+0x9698b) [0x7f4543ca598b]  
/usr/lib/libc.so.6(+0x11aa0c) [0x7f4543d29a0c]  
Signal Number = 11  
  
================================

---

## 评论 (16 条)

### 评论 #1 — alexschroeter (2026-02-17T15:16:33Z)

Can you post the output of `clinfo` on your machine?

---

### 评论 #2 — huanrwan-amd (2026-02-17T18:28:23Z)

Hi @Vikingtons, thanks for posting. 
In https://forum.endeavouros.com/t/can-t-use-davinci-resolve-studio-crash-to-desktop/77870 . It uses AMD Radeon 6700 XT which is not supported by ROCm: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

---

### 评论 #3 — Vikingtons (2026-02-17T19:34:00Z)

Hey there @huanrwan-amd  - they're likely using the HSA workaround. I'm seeing one other affected user leveraging [NV33](https://forum.endeavouros.com/t/can-t-use-davinci-resolve-studio-crash-to-desktop/77870/5) (likely also employing the same); others have not offered their system config, though I'm willing to wager this will reproduce on supported hw like NV32,31,44 and 48.

Could we please attempt to repro on those targets?

---

### 评论 #4 — harkgill-amd (2026-02-17T19:42:18Z)

Hey @Vikingtons, we're aware of the DaVinci (specifically `libProResRAW.so`) issue being reported here with https://github.com/ROCm/rocm-systems/pull/2586 currently being reviewed as a potential solution for this conflict. 

---

### 评论 #5 — alexschroeter (2026-02-18T09:03:05Z)

@Vikingtons Can you ask people check the output of `clinfo` in these forums? We see some issue with ROCm 7.2.0 where the GPU devices are not detected because there is some issue with vendor detection. https://github.com/ROCm/ROCm/issues/5977 It would be interesting to know if the Error people experience is caused/related by this.

---

### 评论 #6 — Vikingtons (2026-02-18T13:36:07Z)

Hey there @alexschroeter - I'll reach out to the reporters in the lemmy community I'm present in and see what they get back with.

Not sure if it helps, for #5977, but I can also provide my output from NV48 using 6.4.4. (packaged with Fedora 43)?

---

### 评论 #7 — jixbo (2026-02-22T21:25:32Z)

I'm also impacted, with the igpu 780m.
[clinfo.txt](https://github.com/user-attachments/files/25472691/clinfo.txt) 

---

### 评论 #8 — RyantheKing (2026-03-04T04:39:44Z)

Also having the issue on my 7900 XTX, which should be supported. Reverting to 7.1.1 did fix the issue, but I just reverted a bunch of the ROCm packages. I'll check later specifically what packages needed to be reverted to fix it and report back. 
[clinfo.txt](https://github.com/user-attachments/files/25732345/clinfo.txt)

---

### 评论 #9 — inode64 (2026-03-13T18:48:07Z)

Same problem

* Kernel 6.18.12
* ROCm version: 7.2
* Radeon AI PRO R9700
* DaVinci Resolve version: 20.3.2 (Studio)

---

### 评论 #10 — harkgill-amd (2026-03-13T19:14:58Z)

Quick update here - https://github.com/ROCm/rocm-systems/pull/2586 has been merged which resolves the crashing seen with ROCm+DaVinci. This fix will be present in the next ROCm release scheduled at which point we can test to see if the crashing is no longer present and close out this issue. Thanks for all the reports and patience! 

---

### 评论 #11 — harkgill-amd (2026-03-25T15:17:11Z)

7.2.1 has been released and it contains the fix for the DaVinci conflict. @Vikingtons, could you please give this release a try with DaVinci and close out the issue if the crashing has been resolved?

https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.1/install/quick-start.html

---

### 评论 #12 — Jonathan03ant (2026-03-25T16:09:29Z)

@harkgill-amd there is a similar issue here https://github.com/ROCm/rocm-systems/issues/3730 , since 7.2.1 has ben released with the fix, I will link the above issue to yours and close is as a duplicate. 

Thanks

---

### 评论 #13 — inode64 (2026-03-26T19:29:39Z)

I updated my Gento to ROCM 7.2.1 and now DaVinci Resolve opens, but videos won't play.

---

### 评论 #14 — NIICKTCHUNS (2026-03-26T21:40:41Z)

For me its working as intended on Arch Linux, using the AUR [opencl-amd](https://aur.archlinux.org/packages/opencl-amd) package, thanks for the workaround!

---

### 评论 #15 — harkgill-amd (2026-04-01T15:35:33Z)

We've verified that the ROCm 7.2.0 crashing/conflict with DaVinci Resolve is no longer seen with ROCm 7.2.1 thanks to https://github.com/ROCm/rocm-systems/pull/2586. For the sake of clarity I'll be closing this issue out as it's been resolved - we can use https://github.com/ROCm/ROCm/issues/5982 to track any further issues related to video playback.

---

### 评论 #16 — inode64 (2026-04-07T13:14:38Z)

After updating to ROCm 7.2.1, DaVinci Resolve now launches, but it takes almost 60 seconds to load video images and display the video. Video playback is also slow, and rendering, which previously took 20 minutes with an Nvidia card, now takes about 20 hours.
It also generated a kernel error.

* Kernel 6.18.21
* ROCm version: 7.2.1
* Radeon AI PRO R9700
* DaVinci Resolve version: 20.3.2 (Studio)
* Mesa 26.0.4

<pre>
amdgpu 0000:12:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:45)
amdgpu 0000:12:00.0: amdgpu:  Process resolve pid 40416 thread resolve pid 40416
amdgpu 0000:12:00.0: amdgpu:   in page starting at address 0x00007f663a63d000 from client 0x1b (UTCL2)
amdgpu 0000:12:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801031
amdgpu 0000:12:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
amdgpu 0000:12:00.0: amdgpu: 	 MORE_FAULTS: 0x1
amdgpu 0000:12:00.0: amdgpu: 	 WALKER_ERROR: 0x0
amdgpu 0000:12:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
amdgpu 0000:12:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
amdgpu 0000:12:00.0: amdgpu: 	 RW: 0x0
amdgpu 0000:12:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:45)
amdgpu 0000:12:00.0: amdgpu:  Process resolve pid 40416 thread resolve pid 40416
amdgpu 0000:12:00.0: amdgpu:   in page starting at address 0x00007f663a5c1000 from client 0x1b (UTCL2)
amdgpu 0000:12:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00801030
amdgpu 0000:12:00.0: amdgpu: 	 Faulty UTCL2 client ID: TCP (0x8)
amdgpu 0000:12:00.0: amdgpu: 	 MORE_FAULTS: 0x0
amdgpu 0000:12:00.0: amdgpu: 	 WALKER_ERROR: 0x0
amdgpu 0000:12:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
amdgpu 0000:12:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
amdgpu 0000:12:00.0: amdgpu: 	 RW: 0x0
amdgpu 0000:12:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:45)
amdgpu 0000:12:00.0: amdgpu:  Process resolve pid 40416 thread resolve pid 40416
amdgpu 0000:12:00.0: amdgpu:   in page starting at address 0x00007f663a6b9000 from client 0x1b (UTCL2)
amdgpu 0000:12:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:45)
amdgpu 0000:12:00.0: amdgpu:  Process resolve pid 40416 thread resolve pid 40416
amdgpu 0000:12:00.0: amdgpu:   in page starting at address 0x00007f6b9ea9a000 from client 0x1b (UTCL2)
amdgpu 0000:12:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:8 pasid:45)
amdgpu 0000:12:00.0: amdgpu:  Process resolve pid 40416 thread resolve pid 40416
amdgpu 0000:12:00.0: amdgpu:   in page starting at address 0x00007f663a734000 from client 0x1b (UTCL2)
amdgpu: Freeing queue vital buffer 0x7f66f1800000, queue evicted
</pre>

---
