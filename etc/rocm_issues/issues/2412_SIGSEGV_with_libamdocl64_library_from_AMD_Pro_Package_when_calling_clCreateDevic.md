# SIGSEGV with libamdocl64 library from AMD Pro Package when calling clCreateDevice

> **Issue #2412**
> **状态**: closed
> **创建时间**: 2023-08-28T21:44:58Z
> **更新时间**: 2024-04-18T23:09:03Z
> **关闭时间**: 2024-04-18T23:09:03Z
> **作者**: shadergz
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2412

## 描述

I encountered a critical issue while attempting to utilize the clCreateDevice function from the libamdocl64 library provided by the AMD Pro Package for OpenCL development. This issue seems to be affecting not only my project but also the 'hashcat' tool, indicating a potential problem with the library itself.

Steps to Reproduce:

Install the AMD Pro Package for OpenCL.
Compile and run a program that calls the clCreateDevice function using the libamdocl64 library.
Observe that a SIGSEGV (Segmentation Fault) occurs.
Expected Behavior:
The clCreateDevice function should successfully create an OpenCL device without causing a segmentation fault.

Additional Information:
When running the hashcat tool under the GDB debugger:

Thread 13 (Thread 0x7fffe01356c0 (LWP 220044) "hashcat"):
#0  __futex_abstimed_wait_common64 (private=<optimized out>, cancel=true, abstime=0x0, op=393, expected=0, futex_word=0x55555781ec68) at ./nptl/futex-internal.c:57                                                                                                                                       
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x55555781ec68, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=<optimized out>, cancel=cancel@entry=true) at ./nptl/futex-internal.c:87                                                             
#2  0x00007ffff7aa31bb in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x55555781ec68, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x0, private=<optimized out>) at ./nptl/futex-internal.c:139                                                     
#3  0x00007ffff7aadf0f in do_futex_wait (sem=sem@entry=0x55555781ec68, abstime=0x0, clockid=0) at ./nptl/sem_waitcommon.c:111
#4  0x00007ffff7aadfa0 in __new_sem_wait_slow64 (sem=0x55555781ec68, abstime=0x0, clockid=0) at ./nptl/sem_waitcommon.c:183
#5  0x00007fffc4ed86a0 in ?? () from /opt/amdgpu-pro/lib/x86_64-linux-gnu/libamdocl64.so
#6  0x00007fffc4ed84e9 in ?? () from /opt/amdgpu-pro/lib/x86_64-linux-gnu/libamdocl64.so
#7  0x00007fffc4ef25ea in ?? () from /opt/amdgpu-pro/lib/x86_64-linux-gnu/libamdocl64.so
#8  0x00007fffc4ef326d in ?? () from /opt/amdgpu-pro/lib/x86_64-linux-gnu/libamdocl64.so
#9  0x00007fffc4e09936 in ?? () from /opt/amdgpu-pro/lib/x86_64-linux-gnu/libamdocl64.so
#10 0x00007fffc4ed86ff in ?? () from /opt/amdgpu-pro/lib/x86_64-linux-gnu/libamdocl64.so
#11 0x00007ffff7aa63ec in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:444
#12 0x00007ffff7b26a1c in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81

Output Produced by `clinfo -d 1:0|head -15`:
  Platform Name                                   AMD Accelerated Parallel Processing
  Device Name                                     gfx902
  Device Vendor                                   Advanced Micro Devices, Inc.
  Device Vendor ID                                0x1002
  Device Version                                  OpenCL 2.0 AMD-APP (3110.6)
  Driver Version                                  3110.6 (PAL,HSAIL)
  Device OpenCL C Version                         OpenCL C 2.0 
  Device Type                                     GPU
  Device Board Name (AMD)                         Unknown AMD GPU
  Device PCI-e ID (AMD)                           0x15d8
  Device Topology (AMD)                           PCI-E, 0000:03:00.0
  Device Profile                                  FULL_PROFILE
  Device Available                                Yes
  Compiler Available                              Yes
  Linker Available                                Yes

Operating System: Kali Linux 2023.3
Compiler: -
hashcat version: v6.2.6

---

## 评论 (2 条)

### 评论 #1 — nartmada (2024-04-07T18:05:32Z)

@spirvdev, sorry for the lack of response :(.  I am seeing gfx092 and this is not a supported GPU.  Which GPU are you using?  



---

### 评论 #2 — shadergz (2024-04-18T23:08:53Z)

Hey thanks, I have already fixed this problem months ago, but I don't know how I did this haahahha

---
