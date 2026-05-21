# [Issue]: Loop unrolling leads to terrible optimization

> **Issue #4202**
> **状态**: open
> **创建时间**: 2024-12-27T00:36:29Z
> **更新时间**: 2025-01-02T16:24:56Z
> **作者**: gwoltman
> **标签**: Under Investigation, Radeon VII, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4202

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Radeon VII** (颜色: #ededed)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

I have a good sized kernel with a loop that is executed just twice.    If the loop is not unrolled, 63 VGPRs are used with an occupancy of 4.  If the loop is unrolled 135 VGPRs are used for occupancy of 1.  As you can imagine, performance suffers.

Using attributes to tell ROCm to only use a specific number of registers simply leads to spilling registers and performance is even worse.

There are several optimizations that could be made by unrolling the loop, but only if ROCm does not go a bit nuts allocating VGPRs.

Source code is available at https://github.com/gwoltman/gpuowl or https://github.com/preda/gpuowl 
The offending kernel is carryFused (in src/cl/carryfused.cl) .  The offending loop is fft_WIDTH (at the end of src/cl/fftwidth.cl).

System info:

OS:
NAME="Ubuntu"
VERSION="24.04.1 LTS (Noble Numbat)"
CPU:
model name      : Intel(R) Celeron(R) CPU G3900 @ 2.80GHz
GPU:
  Name:                    Intel(R) Celeron(R) CPU G3900 @ 2.80GHz
  Marketing Name:          Intel(R) Celeron(R) CPU G3900 @ 2.80GHz
  Name:                    gfx906
  Marketing Name:          AMD Radeon VII
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
  Name:                    gfx906
  Marketing Name:          AMD Radeon VII
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-


### Operating System

Ubuntu 24.04.1

### CPU

Intel Celeron

### GPU

Radeon VII

### ROCm Version

ROCm 6.3.0

### ROCm Component

_No response_

### Steps to Reproduce

Download the git sources named above.  Run make.
Make a directory called asm.
Create a config.txt file with this line:
-device 0 -workers 1 -block 1000 -user XXX -use BIGLIT=1 -use BCAST=0 -use FAST_BARRIER -use NONTEMPORAL=1

If the save-temps bug has been fixed, this command line should generate the asm/*carryfused*.s assembly file. 

Loop left as is:
./build-release/prpll -prp 136279841 -iters 1000 -dump asm  -fft 512:15:512:2 -use UNROLL_W=0

Loop unrolled:
./build-release/prpll -prp 136279841 -iters 1000 -dump asm  -fft 512:15:512:2 -use UNROLL_W=1



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (11 条)

### 评论 #1 — b-sumner (2024-12-27T16:14:20Z)

Hi @gwoltman, would you please describe the "several optimizations that could be made"?  If you carry out those optimizations by hand, how does its performance compare to the not-unrolled version?  And if you have that hand-optimized code, would you share that too?

Since this is a performance concern, would you also provide directions on how to build and run this app, and what to run to make the performance measurements?

---

### 评论 #2 — gwoltman (2024-12-27T17:28:05Z)

The original submission explains how to download and build the program.  It also describes how to look at the assembly dump of the offending carryFused kernel.  

To get timings comparing rolled vs. unrolled, I ran the program twice.  The first run is no unrolling and the third line from the end shows 1029 microseconds average for 10000 "iterations".  The second run with loop unrolling shows 1180 microseconds average for the same 10000 "iterations".
george@ewmayer2:~/nfs/gpuowl43/gpuowl$ rm -rf 136*;./build-release/prpll -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=0
20241227 17:02:25  PRPLL 41ff84a-dirty starting
20241227 17:02:25  config: -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=0
20241227 17:02:25  device 0, OpenCL 3635.0 (HSA1.1,LC), unique id '95b2786172df888e'
20241227 17:02:25 136279841 config:  -DUNROLL_W=0
20241227 17:02:25 136279841 FFT: 7.50M 512:15:512:0 (17.33 bpw)
20241227 17:02:31 136279841 OK         0 on-load: blockSize 1000, 0000000000000003
20241227 17:02:31 136279841 Proof of power 10 requires about 17.1GB of disk space
20241227 17:02:34 136279841 OK      2000 05d6515c416b83e2 1268 ETA 2d 00:00; Z=106 (avg 106.5)
20241227 17:02:42 136279841 Stopping, please wait..
20241227 17:02:44 136279841 OK     10000 52316d51aa52e6b7 1029 ETA 1d 14:57; Z=108 (avg 106.8)
20241227 17:02:44  Exception "stop requested"
20241227 17:02:44  Bye
george@ewmayer2:~/nfs/gpuowl43/gpuowl$ rm -rf 136*;./build-release/prpll -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=1
20241227 17:03:16  PRPLL 41ff84a-dirty starting
20241227 17:03:16  config: -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=1
20241227 17:03:16  device 0, OpenCL 3635.0 (HSA1.1,LC), unique id '95b2786172df888e'
20241227 17:03:16 136279841 config:  -DUNROLL_W=1
20241227 17:03:17 136279841 FFT: 7.50M 512:15:512:0 (17.33 bpw)
20241227 17:03:22 136279841 OK         0 on-load: blockSize 1000, 0000000000000003
20241227 17:03:22 136279841 Proof of power 10 requires about 17.1GB of disk space
20241227 17:03:26 136279841 OK      2000 05d6515c416b83e2 1328 ETA 2d 02:16; Z=106 (avg 106.5)
20241227 17:03:35 136279841 Stopping, please wait..
20241227 17:03:37 136279841 OK     10000 52316d51aa52e6b7 1180 ETA 1d 20:39; Z=108 (avg 106.8)
20241227 17:03:38  Exception "stop requested"
20241227 17:03:38  Bye

The loop causing the trouble (in src/cl/fftwidth.cl) is:
  for (u32 s = 1; s < WIDTH / NW; s *= NW) {
    if (s > 1) { bar(); }
    fft_NW(u);
    tabMul(WIDTH / NW, trig, u, NW, s, me);
    shufl( WIDTH / NW, lds,  u, NW, s);
  }
where WIDTH=512, NW=8.  So the loop is executed twice with s=1 and s=8.
Obviously, the "if (s==1)" test can be eliminated if unrolled.  Also, the shufl routine could avoid a few multiplies, shifts, and adds when s == 1.

My main point is that unrolling should not adversely affect VGPR register usage and occupancy. 

While one might be tempted to say that the optimizations from unrolling are rather minor, just don't unroll.  The major problem for me is that I want to change the algorithm that handles the s==1 case.  To do this I will have to unroll the loop thusly:
  SPECIAL_S_IS_ONE_fft_NW(u);
  SPECIAL_S_IS_ONE_tabMul(WIDTH / NW, trig, u, NW, s, me);
  SPECIAL_S_IS_ONE_shufl( WIDTH / NW, lds,  u, NW, s);
  for (u32 s = NW; s < WIDTH / NW; s *= NW) {
    bar(); 
    fft_NW(u);
    tabMul(WIDTH / NW, trig, u, NW, s, me);
    shufl( WIDTH / NW, lds,  u, NW, s);
  }
This will result in the same VGPR/occupancy penalty, more than negating the significant algorithmic improvements I can make in the SPECIAL_S_IS_ONE versions.

---

### 评论 #3 — gwoltman (2024-12-27T18:14:47Z)

One might argue that since the launch bounds are (64,1,1) the optimizer thinks VGPR/occupancy is not a concern.

So, go to src/cl/base.cl and add the line:
#define KERNEL2(x) kernel __attribute__((reqd_work_group_size(x, 1024, 1))) void
and in src/cl/carryfused.cl change the kernel to use KERNEL2 instead of KERNEL.

Now the optimizer gives us the 64 VGPR usage we want but achieves it by creating 50+ spills.  And the timings are equally unsatisfying:

george@ewmayer2:~/nfs/gpuowl43/gpuowl$ rm -rf 136*;./build-release/prpll -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=1
20241227 18:02:19  PRPLL 41ff84a-dirty starting
20241227 18:02:19  config: -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=1
20241227 18:02:19  device 0, OpenCL 3635.0 (HSA1.1,LC), unique id '95b2786172df888e'
20241227 18:02:20 136279841 config:  -DUNROLL_W=1
20241227 18:02:20 136279841 FFT: 7.50M 512:15:512:0 (17.33 bpw)
20241227 18:02:28 136279841 OK         0 on-load: blockSize 1000, 0000000000000003
20241227 18:02:28 136279841 Proof of power 10 requires about 17.1GB of disk space
20241227 18:02:33 136279841 OK      2000 05d6515c416b83e2 1602 ETA 2d 12:38; Z=104 (avg 104.4)
20241227 18:02:42 136279841 Stopping, please wait..
20241227 18:02:43 136279841 OK     10000 52316d51aa52e6b7 1148 ETA 1d 19:28; Z=106 (avg 104.7)
20241227 18:02:44  Exception "stop requested"
20241227 18:02:44  Bye

In summary, we know a spill-less occupancy=4 solution is possible.  We know unrolling should give us more efficient code.  There is no way to get rocm to produce this result.  This problem is preventing further optimization efforts.

---

### 评论 #4 — b-sumner (2024-12-27T19:26:12Z)

> My main point is that unrolling should not adversely affect VGPR register usage and occupancy.

But it often does.  Unrolling presents more work to do, and exposes more memory operations that can be combined into memory clauses.  That's why I asked if you had tried unrolling by hand and applied the optimizations you mentioned and were able to observe a performance benefit.

---

### 评论 #5 — gwoltman (2024-12-27T19:40:47Z)

I must disagree.  Unrolling does not change the amount of work done by the kernel.  Unrolling gives the optimizer more options to produce a faster executable.  Unfortunately, given this freedom the rocm optimizer is producing significantly slower executables.


---

### 评论 #6 — gwoltman (2024-12-27T20:59:27Z)

As noted before, unrolling by hand also leads to 135 VGPRs (or 64 VGPRs with expensive spills) with a corresponding reduction in performance.

At its core this kernel is massaging the data in 16 doubles (32 VGPRs).  There are conversions to and from int, shuffling of data, multiplying by sin/cos data from memory, atomics to coordinate with other workgroups, etc.  But at no time is there really more than 32 VGPRs of data being actively worked on.   That gives the compiler a very reasonable 32 or 52 VGPRs to use for optimizations to achieve occupancy of 4 or 3.   

The fact that the optimizer thinks 103 VGPRs could be usefully applied to optimization leads me to speculate that either
1)  The compiler is somehow losing track of when some data in VGPRs will no longer be used  - thus making the VGPR available for reuse, or
2)  The compiler is saving nearly every reusable intermediate calculation no matter how trivially it can be recomputed.
This is complete speculation on my part -- I have no understanding of rocm internals. 

---

### 评论 #7 — gwoltman (2024-12-28T16:19:09Z)

Good news, I've dug into the assembly language output to find the culprit.  First a simplified description of the kernel:

read data
call routine that contains unrolling loop
lots and lots of code where peak of 135 VGPRs is reached
call routine again that contains unrolling loop
write data

Loop unrolling allows rocm to discover some 56 VGPRs of data that can be reused in the second unrolled loop.

There are two sets of 28 VGPRs that are getting saved.  Each set, consists of 4 VGPRs read from global memory.  The global memory address does not depend on the group_id, so it is highly likely the global data is in a GPU cache.  The code then goes on to compute 6 more sets of 4 VGPRs at a cost of four F64 FMA instructions for each set of 4 VGPRs.

So, my bug report is amended to "is it wise for rocm save these 56 VGPRs of data?".  Benchmarking shows the answer is clearly no.  And in the case where launch bounds are specified,  it cannot possibly be correct to create 51 spills to save 2 memory loads and 56 FMA ops.

I contend the optimizer should either:
1) Save none of the 56 VGPRs,
or 2) Save only the 8 VGPRs read from cached global memory.
Better yet would be to choose 1 or 2 based on how close the overall kernel is to an occupancy boundary.

Moving forward I tried slapping "volatile" on the memory pointer to work around the problem.  Rocm does indeed create a kernel that uses only 61 VGPRs but mysteriously creates a 16-byte private segment (why?) that impacts performance.
Next I tried adding zero to the memory pointer in way the compiler could not know I was adding zero.  Rocm now creates a kernel that uses 66 VGPRs.  Tantalizingly close to the theoretically possible occupancy 4, but perhaps occupancy 3 is good enough on this GPU:

george@ewmayer2:~/nfs/gpuowl43/gpuowl$ rm -rf 136*;./build-release/prpll -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=1
20241228 16:02:04  PRPLL 41ff84a-dirty starting
20241228 16:02:04  config: -prp 136279841 -iters 10000 -fft 512:15:512:0 -use UNROLL_W=1
20241228 16:02:04  device 0, OpenCL 3635.0 (HSA1.1,LC), unique id '95b2786172df888e'
20241228 16:02:04 136279841 config:  -DUNROLL_W=1
20241228 16:02:04 136279841 FFT: 7.50M 512:15:512:0 (17.33 bpw)
20241228 16:02:10 136279841 OK         0 on-load: blockSize 1000, 0000000000000003
20241228 16:02:10 136279841 Proof of power 10 requires about 17.1GB of disk space
20241228 16:02:14 136279841 OK      2000 05d6515c416b83e2 1278 ETA 2d 00:22; Z=104 (avg 104.4)
20241228 16:02:21 136279841 Stopping, please wait..
20241228 16:02:23 136279841 OK     10000 52316d51aa52e6b7 1024 ETA 1d 14:45; Z=106 (avg 104.7)
20241228 16:02:24  Exception "stop requested"
20241228 16:02:24  Bye

Indeed a small savings of 5 microseconds.  I have an adequate work around that will allow me to proceed with future work.

In conclusion, I've tried to explain some situations where the rocm optimizer is making rather poor decisions.  It would be beneficial to many users if rocm improved it decisions about VGPR usage by understanding occupancy boundaries, amount of work saved by each common sub-expression elimination, duration of the VGPRs holding saved common sub-expressions, and the high costs of spills.


---

### 评论 #8 — gwoltman (2024-12-28T16:41:32Z)

Correction., I ran several more test cases and occupancy=4 provides a significant improvement in many cases.  So, I'll continue my quest to trick the rocm optimizer into creating 64 VGPR kernels when unrolling is enabled.  I'm close, only 2 VGPRs away...

---

### 评论 #9 — b-sumner (2024-12-28T21:02:49Z)

@gwoltman unrolling forms larger basic blocks and hence larger and harder NP-complete scheduling problems.  There isn't a compiler out there that finds optimal solutions in all cases, but improving the AMDGPU scheduler is an ongoing effort.  And, unfortunately, tuning for one workload may negatively impact other workloads, so we are not likely to ever completely satisfy all developers.

I'm expecting a colleague will create an internal ticket for this after the holidays and we will look at this case.

---

### 评论 #10 — gwoltman (2024-12-28T22:11:21Z)

I understand the considerable difficulties the optimizer faces.  Hopefully, I've described the situation in enough detail that it can lead to improved heuristics that benefit (nearly) all users.  

P.S. After several hours, I did find a way to get the unrolled kernel down to a satisfying 62 VGPRs.  I found very few "knobs" one "turn" to influence the optimizer.  Adding pragmas, builtins, or other "tricks" to influence optimizer behavior would be very welcome.   Though I understand I would be in the distinct minority of developers willing to fine tune the assembly language for a few percent improvement. 

---

### 评论 #11 — ppanchad-amd (2025-01-02T16:24:55Z)

Hi @gwoltman. Internal ticket has been created to investigate this issue. Thanks!

---
