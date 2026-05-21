# [Issue]: OpenCL Crashes & Unexpected Behavior

> **Issue #5678**
> **状态**: closed
> **创建时间**: 2025-11-20T00:12:33Z
> **更新时间**: 2026-01-14T18:40:04Z
> **关闭时间**: 2026-01-14T18:40:03Z
> **作者**: mattpuchala
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5678

## 描述

### Problem Description

I am experiencing issues with OpenCL and AMD GPUs where it crashes on Linux and on Windows it does not crash but results are clearly not correct. I'm not quite sure what part is failing but it seems like maybe it is memory copies...? From what I've gathered from the crash files maybe it is switching between fine and corse grain memory types? I'm not an expert that is just from googling and trying to look for causes.

I am the developer of this software and these issues are being reported by some of my users. 

Please see the attached crash file.

Are there any steps to follow to troubleshoot this?

[crash.untitled.loris_53861_log.txt](https://github.com/user-attachments/files/23639476/crash.untitled.loris_53861_log.txt)

It does work properly on CPUs and on other GPU vendors. 

### Operating System

ALL

### CPU

ALL

### GPU

ALL

### ROCm Version

 6.4.x

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (10 条)

### 评论 #1 — b-sumner (2025-11-20T02:32:07Z)

@mattpuchala is it possible for us to build and run your software?

---

### 评论 #2 — mattpuchala (2025-11-20T04:46:38Z)

Hi @b-sumner,

You won't be able to build it as it's proprietary but I'm happy to share as much as I can and provide relevant source code if need be.

You can run it however it will be a bit tricky as it's actually a plug-in for a 3D animation app called Houdini.

Houdini (You can run it in a non-commercial mode called "Apprentice"): https://www.sidefx.com/download

My Plug-in (Axiom 3D Fluid Simulation): https://www.theoryaccelerated.com/axiom-download-latest

How To Install: https://theoryaccelerated.notion.site/axiom-4-installation-houdini

Test File (Should simply crash after opening it on Linux. It will try to run the first frame of the simulation hence the instant crash): https://www.dropbox.com/scl/fo/l66knwb18w62al6cpzqca/AAZOV2_j6dsXNUZCSCiU6hA?rlkey=nf7a9a8cnq4rham6uam6dkv2z&dl=0

Please let me know if you need any help getting setup!

---

### 评论 #3 — b-sumner (2025-11-20T15:36:08Z)

Hi @mattpuchala.  This environment sounds complex, and as a plugin I assume you don't have full control of the environment.  Is there any way you could create a standalone example that exhibits the problem?

---

### 评论 #4 — mattpuchala (2025-11-20T22:44:52Z)

@b-sumner, I would love to give you a standalone however that will quite impossible currently. There are far too many dependencies to the parent app. We do actually have a fair amount of control over the environment the app runs in. I also have a direct line of communication with the parent app's developers should we need something from their end. 

Is there something we can do to get you the information you need? 

---

### 评论 #5 — b-sumner (2025-11-20T23:18:29Z)

One thing that might help would be for you to install the (relevant) debuginfo packages so we can see more clearly what's going on in your stack traces.  Another thing to consider would be to examine the log produced by setting environment  AMD_LOG_LEVEL=2 or higher to see if any errors or other problems show up before the crash.  I would have no idea what is relevant or not so I think it would be better for you to filter it down to the relevant subset.

---

### 评论 #6 — mattpuchala (2025-11-20T23:30:13Z)

Ok, I will give it a shot. Can you give an example of which packages might be relevant and how I might know if it is or not? 

Also, when setting AMD_LOG_LEVEL=2 is that supposed to enable something in the driver and it will print to stdout, or will it write the log somewhere specific?

---

### 评论 #7 — b-sumner (2025-11-21T00:17:34Z)

I see only the OpenCL runtime and the HSA/ROCr runtime in the crash log so maybe only the debuginfo packages for those would be sufficient.

AMD_LOG_LEVEL enables the OpenCL runtime to log information about its internal actions.  You can see more information about logging at https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/logging.html .   Note that OpenCL is identical to HIP with respect to logging.  There's also an AMD_LOG_LEVEL_FILE which defaults to stderr.

---

### 评论 #8 — mattpuchala (2025-11-25T23:12:52Z)

Setting AMD_LOG_LEVEL=2 gives us this now which we did not see before:

Memory access fault by GPU node-1 (Agent handle: 0x7f495d8df200) on address 0x7f47428b0000. Reason: Page not present or supervisor privilege.
Failed to create GPU coredump: Permission denied
GPU core dump failed
Warning: Missing charsets in String to FontSet conversion
46052 ThreadId=0x7f49497ff680: 
46052:  (sent by pid 46052)
Saving application data to /tmp/houdini_temp/crash.untitled.loris_46052.hiplc
Warning: Missing charsets in String to FontSet conversion
Crash log saved to /tmp/houdini_temp/crash.untitled.loris_46052_log.txt

Not sure if this is useful? I do know that all memory copies and accesses I do are within valid bounds. 

---

### 评论 #9 — b-sumner (2025-11-26T02:50:17Z)

Do you see any other mention of 0x7f47428b0000 in the log?  Maybe with level 3 or 4?

---

### 评论 #10 — ppanchad-amd (2026-01-14T18:40:04Z)

@mattpuchala Closing ticket as there has been no activity for some time.  Please let us know if you are still having issues and we can re-open the ticket for investigation. Thanks!

---
