# [Issue]: Driver not initialized (amdgpu not found in modules)

> **Issue #2767**
> **状态**: closed
> **创建时间**: 2023-12-22T04:54:40Z
> **更新时间**: 2025-02-10T07:50:49Z
> **关闭时间**: 2024-04-05T14:52:10Z
> **作者**: PatchouliPatch
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/2767

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Previously, I was able to run ROCm 5.7.1 without any issues but as soon as I installed ROCm 6.0 it would not function properly.

Upon running rocm-smi after performing an install using `sudo amdgpu-install --usecase=rocm,hiplibsdk,graphics` and rebooting, I get the following error:

cat: /sys/module/amdgpu/initstate: No such file or directory
ERROR:root:Driver not initialized (amdgpu not found in modules)

### Operating System

22.04.3 LTS (Jammy Jellyfish)

### CPU

AMD Ryzen 7 7700X 8-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### Other

_No response_

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

cannot use `rocminfo --support`, gives the error: `ROCk module is NOT loaded, possibly no GPU devices`


### Additional Information

[rocm-output.txt](https://github.com/ROCm/ROCm/files/13748456/rocm-output.txt)
Here is the terminal output when I attempted to uninstall then reinstall ROCm 6.0

---

## 评论 (25 条)

### 评论 #1 — PatchouliPatch (2023-12-22T04:55:29Z)

please let me know if I can help by giving any other bits of information

---

### 评论 #2 — kentrussell (2024-01-02T14:49:54Z)

A full dmesg would help, as well as the output of "dkms status"

---

### 评论 #3 — nartmada (2024-01-09T21:40:52Z)

@kentrussell, while waiting for @PatchouliPatch to provide the full dmesg, we will try to reproduce the issue in Markham office.

---

### 评论 #4 — nartmada (2024-01-11T20:51:01Z)

@PatchouliPatch, we are not able to reproduce your issue.  "rocminfo --support" and "rocm-smi" can run successfully.  I have attached the rocminfo and rocm-smi output for your reference.

[rocminfo--support.txt](https://github.com/ROCm/ROCm/files/13908239/rocminfo--support.txt)
[rocm-smi.txt](https://github.com/ROCm/ROCm/files/13908240/rocm-smi.txt)

Can you please share your steps on uninstall and reinstalling ROCm6.0.0 ?  Thanks.




---

### 评论 #5 — nartmada (2024-01-23T03:48:18Z)

Hi @PatchouliPatch, can you please share your steps on uninstall and reinstalling ROCm 6.0.0?  Thanks.

---

### 评论 #6 — venkat-kittu (2024-01-23T11:28:57Z)

Hi I have also the same issue when installed ROCm 5.6 from below link
https://rocm.docs.amd.com/en/docs-5.6.0/deploy/linux/installer/install.html

When execute **rocminfo** getting below output
ROCk module is NOT loaded, possibly no GPU devices

when executed **rocm-smi** getting below error
cat: /sys/module/amdgpu/initstate: No such file or directory
ERROR:root:Driver not initialized (amdgpu not found in modules)

I tried checking the **dkms status** command output and is below
amdgpu, 6.1.5-1609671.20.04, 5.15.0-1053-azure, x86_64: installed

Can you please help me with this. I need only ROCm 5.6 because I need it for PyTorch library

---

### 评论 #7 — nartmada (2024-01-23T14:20:08Z)

Hi @venkat-kittu, can you please share your CPU, GPU, and OS info?  Thanks.

---

### 评论 #8 — venkat-kittu (2024-01-24T05:42:18Z)

Hi @nartmada, Below are the details you asked for

############### **CPU info:** ##########################
            Architecture:                       x86_64
            CPU op-mode(s):                     32-bit, 64-bit
            Byte Order:                         Little Endian
            Address sizes:                      48 bits physical, 48 bits virtual
            CPU(s):                             4
            On-line CPU(s) list:                0-3
            Thread(s) per core:                 2
            Core(s) per socket:                 2
            Socket(s):                          1
            NUMA node(s):                       1
            Vendor ID:                          AuthenticAMD
            CPU family:                         23
            Model:                              49
            Model name:                         AMD EPYC 7V12 64-Core Processor
            Stepping:                           0
            CPU MHz:                            2445.448
            BogoMIPS:                           4890.89
            Hypervisor vendor:                  Microsoft
            Virtualization type:                full
            L1d cache:                          64 KiB
            L1i cache:                          64 KiB
            L2 cache:                           1 MiB
            L3 cache:                           16 MiB
            NUMA node0 CPU(s):                  0-3
            Vulnerability Gather data sampling: Not affected
            Vulnerability Itlb multihit:        Not affected
            Vulnerability L1tf:                 Not affected
            Vulnerability Mds:                  Not affected
            Vulnerability Meltdown:             Not affected
            Vulnerability Mmio stale data:      Not affected
            Vulnerability Retbleed:             Mitigation; untrained return thunk; SMT vulnerable
            Vulnerability Spec rstack overflow: Mitigation; safe RET, no microcode
            Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccomp
            Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitization
            Vulnerability Spectre v2:           Mitigation; Retpolines, STIBP disabled, RSB filling, PBRSB-eIBRS Not affected
            Vulnerability Srbds:                Not affected
            Vulnerability Tsx async abort:      Not affected
            Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm rep_good nopl cpuid extd_ap
                                              icid pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw topo
                                              ext ssbd vmmcall fsgsbase bmi1 avx2 smep bmi2 rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaveerptr arat umip rdpid




#################### **GPU info** ########################################################
               0002:00:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Vega 10 [Instinct MI25 MxGPU/MI25x2 MxGPU/V340 MxGPU/V340L MxGPU] (prog-if 00 [VGA controller])
        Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Vega 10 [Radeon Instinct MI25 MxGPU]
        Physical Slot: 1447514197
        Flags: 66MHz, user-definable features, ?? devsel, NUMA node 0
        Memory at fe0000000 (64-bit, prefetchable) [disabled] [size=256M]
        Memory at ff0000000 (64-bit, prefetchable) [disabled] [size=2M]
        Memory at 40880000 (32-bit, non-prefetchable) [disabled] [size=512K]
        Capabilities: [64] Express Legacy Endpoint, MSI 00
        Capabilities: [a0] MSI: Enable- Count=1/2 Maskable+ 64bit+
        Capabilities: [c0] MSI-X: Enable- Count=2 Masked-
        Capabilities: [100] Vendor Specific Information: ID=0001 Rev=1 Len=010 <?>
        Capabilities: [150] Advanced Error Reporting
        Capabilities: [328] Alternative Routing-ID Interpretation (ARI)

######################### **OS info:** ###########################################################
          LSB Version:    core-11.1.0ubuntu2-noarch:security-11.1.0ubuntu2-noarch
          Distributor ID: Ubuntu
          Description:    Ubuntu 20.04.6 LTS
          Release:        20.04
          Codename:       focal

---

### 评论 #9 — nartmada (2024-01-24T15:12:50Z)

Hi @venkat-kittu, thanks for your info.  Your GPU (MI25) is different from the original issue (7900XTX) reported by @PatchouliPatch.  

According to the ROCm documentation, unfortunately MI25 is no longer supported.  
https://rocm.docs.amd.com/en/docs-5.6.0/release/gpu_os_support.html
![image](https://github.com/ROCm/ROCm/assets/144284448/7f1f80a2-6de4-442f-a4cb-726f416593f8)



---

### 评论 #10 — PatchouliPatch (2024-01-25T04:16:47Z)

My apologies for not replying sooner, I had college finals. 

I managed to fix my installation by adding --no-dkms to the install command. Maybe add this to the documentation? From a friend, I learned that you were supposed to use --no-dkms when installing the software on an OS with a GUI. Is this true?


---

### 评论 #11 — nartmada (2024-01-26T04:14:44Z)

Are you adding --no-dkms after "sudo amdgpu-install --usecase=graphics,rocm --no-dkms"?  I am trying to understand what you did.  Thanks for your help.

![image](https://github.com/ROCm/ROCm/assets/144284448/e91a8e1b-dc34-4857-a121-8e5055947322)




---

### 评论 #12 — PatchouliPatch (2024-01-26T08:31:57Z)

Yes, that's what I did. 

---

### 评论 #13 — nartmada (2024-02-09T16:53:47Z)

Hi @PatchouliPatch, we need your help to provide the following info:

1)	Complete terminal log from the command used to uninstall ROCm 5.7.1 to the end of the install of ROCm 6.0.
2)	Output of “dkms status” after completing the install of 6.0.
3)	The dmesg log after install of 6.0, then another dmesg log after reboot following install.
4)	Exact steps to repo so we can test ourselves.

Thank you.

---

### 评论 #14 — PatchouliPatch (2024-02-11T13:40:32Z)

how do I get the terminal log? It's been a while since I've installed 6.0. 

---

### 评论 #15 — nartmada (2024-02-14T02:26:12Z)

For terminal log, it would be good to get a complete end-to-end copy and paste of all of the terminal commands that were run and all the output.  Basically, same thing as the rocm-output.txt file already attached, but including all terminal commands and their output.  The current rocm-output.txt is incomplete and doesn’t show all the commands.

Still, the dmesg log will be the most help.


---

### 评论 #16 — PatchouliPatch (2024-02-16T02:45:03Z)

[dmesg_log.txt](https://github.com/ROCm/ROCm/files/14304709/dmesg_log.txt)
here you are

---

### 评论 #17 — kentrussell (2024-02-16T14:28:27Z)

So the dmesg doesn't seem to show the DKMS code as installed. Can you give this info from above?
_Output of “dkms status” after completing the install of 6.0._

It looks like you're running 6.5, which isn't supported in ROCm 6.0 (see https://github.com/ROCm/ROCm/issues/2458 , https://github.com/ROCm/ROCm/issues/2694, among others)

For a list of tested configurations, you can refer to https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.0.0/reference/system-requirements.html . There are known compilation issues with the 6.5 kernel that are to be resolved in ROCm 6.1. For now, we recommend either dropping down to the 6.2 kernel, or installing the 6.6-based HWE kernel. Both have been tested (HWE kernel is listed as "preview support" for ROCm 6.0 but it should be fine), but 6.5 is known to not work with ROCm 6.0. Which is why you're unable to get the DKMS driver working, and are stuck using the stock OS driver. 

---

### 评论 #18 — dattrax (2024-02-21T13:55:38Z)

This sounds similar to what I’d battled with.  As the amd driver was proprietary it has a signing password when you build it.  It mentioned something about ‘GOK’ in the bios when I next booted, but I skipped it.  Everything launched as before but I couldn’t get the driver to load.

turns out I shouldn’t have skipped the bios setup for the signed modules.  Once I put the same key in, it loaded and worked ok.

---

### 评论 #19 — nartmada (2024-03-16T01:15:43Z)

Hi @PatchouliPatch, did you get a chance to try kentrussell's recommendation of either dropping down to the 6.2 kernel, or installing the 6.6-based HWE kernel?  Thanks.

---

### 评论 #20 — nartmada (2024-04-05T14:52:11Z)

Closing this ticket.  @PatchouliPatch, please re-open if you still observe this issue in next ROCm release.  Thanks.

---

### 评论 #21 — sammtan (2024-04-08T12:03:15Z)

hello. I did ROCm installation with amdgpu-install, by two tries. First try is for `--usecase=dkms`, then reboot, then second try is for usecase all except dkms. Then, every test command shows me this result.

rocminfo
ROCk module is NOT loaded, possibly no GPU devices

rocm-smi
cat: /sys/module/amdgpu/initstate: No such file or directory
ERROR:root:Driver not initialized (amdgpu not found in modules)

dkms status
amdgpu/6.3.6-1718217.22.04, 6.5.0-26-generic, x86_64: installed

sudo dmesg | grep kfd
(nothing)

sudo dmesg | grep amd
[    0.000000] Linux version 6.5.0-26-generic (buildd@lcy02-amd64-051) (x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #26~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Tue Mar 12 10:22:43 UTC 2 (Ubuntu 6.5.0-26.26~22.04.1-generic 6.5.13)

I'm on Ubuntu 22, Intel i5 12500H, RTX 3050 Mobile. Is this problem about my hardware? If so, I was just thinking to write GPU codes from this machine and using ROCm toolsets, to run the build output on another machine. If that's not true, please tell me why it is not possible. :)

edit: that's so dumb. my machine wont boot. then I went to TTY, uninstall all amdgpu-install packages, then reboot. back to normal with RTX GPU. I guess the problem is with amdgpu, because it is a driver (and I don't have any AMD GPU)?

---

### 评论 #22 — 18992136067 (2024-07-23T13:08:10Z)

I am in the same situation as you. I need to install the Ubuntu 6.2 kernel on my system, which currently has the 6.5 kernel.
AND you need ：sudo usermod -a -G render $LOGNAME
“LOGNAME" is your user name

---

### 评论 #23 — 18992136067 (2024-07-23T13:29:55Z)

sorry，is 6.5 HWE kernel or 5.15 
<img width="1695" alt="1721740998387" src="https://github.com/user-attachments/assets/6267b83c-fdf0-4c22-90fb-953e60c22d06">


---

### 评论 #24 — kentrussell (2024-07-29T13:32:42Z)

@sammtan You're trying ROCm without AMD HW? Then --usecase=dkms will be useless to you, since that's just the AMD kernel packages (amdgpu, amdkfd, ttm, scheduler). If you want to do ROCm stuff without AMD HW, you can try 
amdgpu-install --usecase=rocm --no-dkms
nut there's no support from our side on that, since there's no AMD HW to speak of. 

TL;DR If you don't have AMD hardware, don't install the dkms package. It won't do anything useful (and shouldn't do anything at all, unless you've got some dependencies on ttm)

---

### 评论 #25 — Phezzan (2025-02-10T07:47:44Z)

I have this problem too.

5600g + rx470

After attempting amdgpu-uninstall and a reinstall I haven't been able to get more than 1024x768 on one monitor.

the amdgpu module is not loaded... and AFAICT it never attempted to load.

rerunning amdgpu-install claims to work, but I still get no driver at all.

I need a wiki section on troubleshooting "You attempted to uninstall and now everything is FUBAR and you can't even get native monitor resolution."

---
