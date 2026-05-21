# [Issue]: Possible reduced accuracy of OpenCL calculations for Einstein@Home MeerKAT (ROCm 7.2)

> **Issue #6026**
> **状态**: open
> **创建时间**: 2026-03-09T03:29:44Z
> **更新时间**: 2026-04-06T21:56:18Z
> **作者**: Wedge009
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6026

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Problem Description

This is more of a 'red flag' than a concrete problem. With respect to the Einstein@Home BOINC project, I have been running their 'MeerKAT' BRP7 tasks for a long time now. The way E@H works is that it sends tasks to different users' computers for a given work-unit, at least two tasks per work-unit. If the results returned are aligned within some mathematical threshold, the results are deemed 'valid' and credit awarded. However, if the results don't match then further tasks are sent out until there is a matching pair of results and other results are deemed 'invalid'.

Since moving from ROCm 7.1.1 to 7.2, I noticed a sharp increase in results being marked as invalid, from 'occasional' to several dozens within a week. Since the only thing that had changed for me was the update in ROCm, I experimented with rolling back to ROCm 7.1.1 for a few days, and the invalid rate has since gone back to normal. **My concern is whether or not there is a known change to OpenCL that could be causing differences in rounding, for example.**

Unfortunately, public access to users' computer status reports are no longer available due to bot-abuse - only registered project users can view this information at present.

### Operating System

Ubuntu 24.04.4 LTS (Noble Numbat)

### CPU

AMD Ryzen Threadripper 3960X 24-Core Processor

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

I only have OpenCL components installed from ROCm: `amdgpu-install --opencl=rocr --usecase=opencl`

I accept it's not exactly reproducible due to the nature of the project's task validation, but I thought it would be good to report this in case there is a regression with OpenCL.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

While this is a problem for MeerKAT tasks, ROCm 7.2 has actually helped with excessive system memory usage on 'All-Sky' O4AS tasks. So it would be preferable not to be forced to choose between one version of ROCm over another.

@PorcelainMouse From your report #3575, I noticed you (used to) process MeerKAT tasks for E@H. If you happen to still be running them, have you noticed this issue?

---

## 评论 (23 条)

### 评论 #1 — schung-amd (2026-03-12T18:50:28Z)

Hi @Wedge009, thanks for the report. I'm not currently aware of a known issue that would cause this, but certainly sounds like a regression. Do you have a reproducer that doesn't involve running BOINC (i.e. is there a way we can run dummy meerKAT tasks to triage this, or do you have some other code that performs similar tasks and shows similar inaccuracies)?

---

### 评论 #2 — b-sumner (2026-03-12T19:21:13Z)

@Wedge009 could you point to the OpenCL C source that computes the results?  Also does "aligned within some mathematical threshold" mean "within some relative or absolute tolerance"?  Is it possible the tolerance is too tight?

---

### 评论 #3 — Wedge009 (2026-03-13T09:41:19Z)

Unlike SETI@home project, a lot of the things I've observed seems to be not easily available to public. I remember running test tasks for S@h but not for E@H. I'm also travelling at the moment, but off the top of my head the best I could do is to ask the community and direct them to this issue. Although, sadly, the majority of them use CUDA.

I'm not privy to how the E@H project runs its validation, but here's a sample work-unit:

* https://einsteinathome.org/task/1930701587: assigned to me, running on ATI/AMD application using OpenCL on Linux, marked as invalid.
* https://einsteinathome.org/task/1930701588: running on a CUDA-based host on Linux, marked as valid.
* https://einsteinathome.org/task/1930936141: running on a CUDA-based host on Linux, marked as valid.
From https://einsteinathome.org/workunit/993723490 (again, I think only registered users can access this info).

Depending on the application and the validation process, I've noticed when I'm outnumbered like this, the validator will tend to favour the NV results, by virtue of their hardware and software being similar. But the validation process has been refined such that these differences are minimal nowadays. Hence my surprise at getting so many tasks marked as invalid with ROCm 7.2 vs 7.1.1.

---

### 评论 #4 — trailwanderer360 (2026-03-13T14:48:17Z)

I can confirm a few failed BRP7 tasks. They complete successfully but I am later marked as invalid. Looks like I have around a 1% failure rate.

OS: Almalinux 10.1
GPU: 6600 XT
ROCM 7.2

https://einsteinathome.org/workunit/996473915
https://einsteinathome.org/workunit/996640002

If there is specific information that is needed to try to assist here, I can attempt to reach out to the project. They resolved issues with O4 tasks on ROCM 7.2 already.



---

### 评论 #5 — schung-amd (2026-03-13T15:20:17Z)

We really need code to run ourselves and check for a regression, E@H is a black box that isn't showing us what is being computed and why it is being marked as invalid. For example, the valid and invalid task logs shown by @Wedge009 all look the same as the canonical result log to me.

---

### 评论 #6 — KeithMyers (2026-03-13T17:05:12Z)

Source code for the BRP7 app is available from the project if you ask the admin for it.
You can run the app offline outside of Boinc from a terminal for analysis.  You just need a few test tasks with their input files to test against.  You can run the same task against each version of RocM to see where the regression is coming from.

---

### 评论 #7 — schung-amd (2026-03-13T17:07:29Z)

One thing to check as I see you're on Ubuntu 24.04, what's your kernel version and do you have the DKMS driver installed (check `dkms status`)? If so, try uninstalling the dkms driver (`sudo apt autoremove amdgpu-dkms dkms` or reinstall with `amdgpu-install --no-dkms`). I've been looking into an issue where the DKMS driver shipped with ROCm 7.2 isn't compatible with kernel >= 6.17, and wonder if this might be related.

---

### 评论 #8 — trailwanderer360 (2026-03-13T17:37:46Z)

> I've been looking into an issue where the DKMS driver shipped with ROCm 7.2 isn't compatible with kernel >= 6.17, and wonder if this might be related.

I am using EL10 with Kernel 6.12 and I have occasional failed tasks there. Edit: Actually ignore that I don't think I am using DKMS so I am probably using the red hat supplied amdgpu.

---

### 评论 #9 — b-sumner (2026-03-13T17:57:25Z)

> Source code for the BRP7 app is available from the project if you ask the admin for it. 

@KeithMyers could you expand on the "ask the admin for it"?  How should I do that?

---

### 评论 #10 — KeithMyers (2026-03-13T18:23:49Z)

You would have to join Einstein so you could send a PM to Bernd Machenschalk who is the website admin and ask for the source code location.  They have allowed access to it for our team CUDA developer who optimizes the application code for better performance.  And passes that optimization back to the project app developers to for them to choose to implement or not.  Our team has a custom BRP7 and O4AS CUDA application that locations to download are in messages in the project forums.  The apps are CUDA only and Linux  only meant to be run under the anonymous Boinc platform.

The project publishes the BRP7 source code location in a link on the project but here it is without having to join Einstein@home.  If you want the O4AS code you would have to ask as that is not publicly published.

[https://einsteinathome.org/brp-src-release.zip](url)

You can use the script build.sh to build native binaries for Windows (cross-compiled on Linux using MinGW!), Mac OS X and Linux. This script will download all 3rd-party libraries and build them before building the actual science application. The script will check whether all prerequisites are met and supports checkpointing. For CUDA or OpenCL builds, please make sure PATH as well as CUDA_INSTALL_PATH or AMDAPPSDKROOT respectively are set properly. 

If you are interested in the source code for the Gravitational Wave or Gamma-ray search application, please write to sourcecode[‑at‑]einsteinathome.org

---

### 评论 #11 — b-sumner (2026-03-13T19:00:00Z)

@schung-amd will you be requesting the BRP7 source?

---

### 评论 #12 — schung-amd (2026-03-13T19:53:24Z)

@b-sumner Sure, I'll make an account and send a message over.

---

### 评论 #13 — ahorek (2026-03-14T00:14:32Z)

Here’s a guide I prepared for app testing
1/ clone https://github.com/ahorek/eahbrp7example
2/ run the app
./brp7_opencl -i Ter5_2_sband_dns_cfbf00082_segment_1_dms_40_25.binary -l Ter5_2_sband_dns_cfbf00082_segment_1_dms_40.zap -o results.cand0 -c Ter5_2_sband_dns_cfbf00082_segment_1_dms_40_25.cpt -A 0.04 -P 1.5 -f 500.0 -W --pb_min 3600 --mc_max 1.6 --mp_min 1.1 --mismatch 0.222 --tobs 1800 --alpha 1.0 --start_template_id 8900000 --no_of_templates 50000 -z
3/ the results will be written to results.cand0
it should take about 5min on 7900 xtx

amd windows (adrenalin 26.2.2)
amd linux (rocm 6.2)
nvidia linux (590.48.01)
There are minor differences in ordering and rounding between platforms, but the validator accepts these results.

@Wedge009 could you compare your result on ROCm 7.2?

I can help debug the issue since I have access to the BRP7 source, but we’ve been asked not to share it publicly. However, if you send an email to sourcecode[‑at‑]einsteinathome.org, there should be no problem with sharing it

opencl kernels are located in ./src/opencl/app/demod_binary_ocl_kernels.h and there's also a cuda version. I’m happy to help if needed.


---

### 评论 #14 — Wedge009 (2026-03-19T22:12:13Z)

Sorry for the delay, I've been away for a week and only just got back yesterday. Still catching up.

After setting execute permission this is exactly what I ran:
```
./brp7_opencl -i Ter5_2_sband_dns_cfbf00082_segment_1_dms_40_25.binary -l Ter5_2_sband_dns_cfbf00082_segment_1_dms_40.zap -o results.cand0 -c Ter5_2_sband_dns_cfbf00082_segment_1_dms_40_25.cpt -A 0.04 -P 1.5 -f 500.0 -W --pb_min 3600 --mc_max 1.6 --mp_min 1.1 --mismatch 0.222 --tobs 1800 --alpha 1.0 --start_template_id 8900000 --no_of_templates 50000 -z
```

`stderr.txt` says:
```
09:09:02 (47068): Can't open init data file - running in standalone mode
[09:09:02][47068][INFO ] Starting data processing...
Trying OpenCL platform provided by: Advanced Micro Devices, Inc.
[09:09:02][47068][INFO ] Using OpenCL platform provided by: Advanced Micro Devices, Inc.
[09:09:02][47068][ERROR] Couldn't retrieve list of OpenCL devices (error: -1)!
[09:09:02][47068][ERROR] Couldn't find any suitable OpenCL GPU device!
[09:09:02][47068][ERROR] Demodulation failed (error: 2004)!
09:09:02 (47068): called boinc_finish(2004)
```

Which is strange since BOINC is running tasks just fine. Is it expecting `clinfo` or something like that?

Edit: Never mind, permissions issue, running the sample task now.

---

### 评论 #15 — Wedge009 (2026-03-19T22:44:20Z)

I ran the same test against ROCm 7.1.1 and ROCm 7.2. For this sample task, I found no difference in results and both matched the results in the supplied `results_amd_linux` directory. But not every task under ROCm 7.2 resulted in an invalid state, just a significantly higher proportion of them than with ROCm 7.1.1.

Since reverting to ROCm 7.1.1, the most recent task I've had be marked as invalid is dated 5 March, when I was still running on ROCm 7.2.

---

### 评论 #16 — ahorek (2026-03-20T00:20:38Z)

EaH BRP7 historically had issues validating results across different platforms (Windows, Linux, OpenCL, CUDA). You might simply be unlucky, since there are more CUDA hosts, which tend to win when the result is inconclusive.
Still, it would be helpful to have specific data files and command-line arguments that demonstrate a difference between ROCm 7.1.1 and ROCm 7.2, and that can be tested in a standalone setup.

---

### 评论 #17 — Wedge009 (2026-03-20T01:04:50Z)

I thought that at first because I've seen that pattern of invalid results before, but no, there was a definite sharp delineation of dozens of invalid results (peaked at something like 80 in less than a week) with ROCm 7.2 to next to nothing with ROCm 7.1.1. I could try running ROCm 7.2 again just to prove the point, but I'd rather avoid producing bad results.

Edit: I just reviewed the remaining invalid results I have that have yet to be purged from the database. While there are some with the usual CUDA co-validation results, there are other cases where my host has been 'out-voted' by other AMD hardware, albeit running on Windows. And as I said at the start, I recognise this is more of a warning sign than a clear indication of fault. If it was the latter, it'd be easier to come up with an easily replicated process for diagnosis.

---

### 评论 #18 — Wedge009 (2026-03-24T23:34:22Z)

I notice 7.2.1 was just released, I might give it a try at some point, see if the spike in invalid results is still there...

---

### 评论 #19 — schung-amd (2026-03-25T17:41:25Z)

On my end I'm still waiting on source code; I've made contact with Bernd but they are currently too swamped to provide a proper response to my ask.

---

### 评论 #20 — Wedge009 (2026-03-26T13:06:16Z)

I started using ROCm 7.2.1 on 2026-03-26 ~07:30 UTC. I've already seen two results marked as inconclusive, two outright errors (normally zero), and two marked as 'validate error' (presumably so bad the validator rejects the result outright). Not a great start. Comparing with the pattern of results before this, when still on ROCm 7.1.1, it seems more than just 'coincidence' that the results are so poor.

---

### 评论 #21 — Wedge009 (2026-03-27T04:09:29Z)

Confirming very poor MeerKAT results with ROCm 7.2.1. Stopped the experiment at 2026-03-27 ~01:00 UTC.

---

### 评论 #22 — schung-amd (2026-04-06T21:18:15Z)

Quick update, Bernd provided an excellent reproducer and it does appear that ROCm 7.2/7.2.1 OpenCL is producing inconsistent results with BRP7, currently investigating.

---

### 评论 #23 — Wedge009 (2026-04-06T21:52:42Z)

Thank you for confirming. Considering the upcoming release of Ubuntu 26.04, I was wondering if I'd have to make a choice on the assumption that only the most recent ROCm would have support for the newer OS/kernels.

---
