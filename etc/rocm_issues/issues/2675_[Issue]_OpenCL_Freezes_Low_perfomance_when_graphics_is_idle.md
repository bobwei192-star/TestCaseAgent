# [Issue]: OpenCL Freezes / Low perfomance when graphics is idle

> **Issue #2675**
> **状态**: closed
> **创建时间**: 2023-11-25T18:02:50Z
> **更新时间**: 2023-12-17T09:13:17Z
> **关闭时间**: 2023-12-17T09:13:17Z
> **作者**: itdimk
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2675

## 描述

### Problem Description

1 - When I'm rendering video in Davinci Resolve and I start some application which loads Graphics (firefox with youtube / mpv / resizing windows) it actually increases rendering speed like +30-50%
2 - Geekbench takes immense amount of time to complete opencl tests if graphics in idle.
But if I start video in background, again, time reduces dramatically (there's no big difference in total score tho).
3 - I got 5 seconds playback freezes in davinci resolve.
When i do anything connected with GPU load (open latte dock / resize window / start Discord) it magically un-freezes.
Playing video in background (e.g. mpv or in firefox) eliminates all freezes as well.

I haven't experienced same on Windows tho.
Capping gpu clock at max doesn't make difference

### Operating System

Arch Linux

### CPU

AMD Ryzen 3 4300U with Radeon Graphics

### GPU

AMD Ryzen 3 4300U with Radeon Graphics

### ROCm Version

5.6.1,5.7.1

### ROCm Component

_No response_

### Steps to Reproduce

Geekbench:
- Close all graphics-related apps
- Run geekbench --compute opencl, measure time
- Open looped video on any player (with hw decode support)
- While it plays, run geekbench --compute opencl
- It'll be finished 3 or 4 times faster

Davinci Resolve:
- Close all graphics-related apps
- Open video in davinci
- Put playhead somewhere on timeline
- Press play
- There's a high chance u get 4-5 sec delay
- Run any app which draws anything using gpu (even vkmark will work)
- No playback delays at all

### Output of /opt/rocm/bin/rocminfo --support

ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen 3 4300U with Radeon Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 3 4300U with Radeon Graphics
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    0                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32768(0x8000) KB                   
  Chip ID:                 0(0x0)                             
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            4                                  
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    36812276(0x231b5f4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    36812276(0x231b5f4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    36812276(0x231b5f4) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx90c                             
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon Graphics                
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    1                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
    L2:                      1024(0x400) KB                     
  Chip ID:                 5686(0x1636)                       
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1400                               
  BDFID:                   1280                               
  Internal Node ID:        1                                  
  Compute Unit:            5                                  
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        40(0x28)                           
  Max Work-item Per CU:    2560(0xa00)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 469                                
  SDMA engine uCode::      40                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    4194304(0x400000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS:                     
      Size:                    4194304(0x400000) KB               
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx90c:xnack-   
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***             

---

## 评论 (5 条)

### 评论 #1 — aagit (2023-12-13T22:48:39Z)

From your description of the problem this seems the same issue I have with darktable opencl backend on the 7730U gfx90c: if I play a video on firefox while I use darktable opencl doesn't hang, otherwise it tends to hang for a few seconds.

---

### 评论 #2 — aagit (2023-12-15T08:23:48Z)

In this old issue I found two working workarounds:

https://github.com/ROCm/ROCT-Thunk-Interface/issues/56

Either one of "export HSA_ENABLE_INTERRUPT=0" or "export HSA_ENABLE_SDMA=0" appeared to have solved the hang here, so probably it wasn't a kernel bug? HSA_ENABLED_SDMA=0 seem to perform better.

Here's how it hangs:

```
(gdb) info threads
  Id   Target Id                                           Frame
* 1    Thread 0x7ffff7a36740 (LWP 23839) "memtestCL"       0x00007ffff7abdda5 in ?? () from /lib64/libc.so.6
  2    Thread 0x7ffff74996c0 (LWP 23842) "memtestCL"       0x00007ffff7b38bfb in ioctl () from /lib64/libc.so.6
  5    Thread 0x7ffef545d6c0 (LWP 23845) "Command Queue T" 0x00007ffff7b38bfb in ioctl () from /lib64/libc.so.6
(gdb) thread 1
[Switching to thread 1 (Thread 0x7ffff7a36740 (LWP 23839))]
#0  0x00007ffff7abdda5 in ?? () from /lib64/libc.so.6
(gdb) bt
#0  0x00007ffff7abdda5 in ?? () from /lib64/libc.so.6
#1  0x00007ffff7ac8dfb in ?? () from /lib64/libc.so.6
#2  0x00007ffff794488b in amd::Semaphore::timedWait (this=this@entry=0x555555594c50, millis=millis@entry=0xa)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/thread/semaphore.cpp:130
#3  0x00007ffff79444cf in amd::Monitor::wait (this=this@entry=0x5555561ed658)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/thread/monitor.cpp:253
#4  0x00007ffff792be48 in amd::Event::awaitCompletion (this=0x5555561ed640)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/platform/command.cpp:265
#5  0x00007ffff78f0b7a in clEnqueueReadBuffer (command_queue=<optimized out>, buffer=<optimized out>, blocking_read=0x1, offset=<optimized out>,
    cb=<optimized out>, ptr=0x555555974940, num_events_in_wait_list=0x0, event_wait_list=0x0, event=0x0)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCm-OpenCL-Runtime-rocm-5.5.1/amdocl/cl_memobj.cpp:655
#6  0x000055555555b46d in memtestFunctions::verifyConstant(unsigned int, unsigned int, _cl_mem*, unsigned int, unsigned int, _cl_mem*, unsigned int*, int&) const ()
#7  0x000055555555bb4c in memtestState::gpuMovingInversionsPattern(unsigned int&, unsigned int) const ()
#8  0x000055555555bd8b in memtestMultiTester::gpuWalking8BitM86(unsigned int&, unsigned int) const ()
#9  0x00005555555582ba in main ()
(gdb) thread 2
[Switching to thread 2 (Thread 0x7ffff74996c0 (LWP 23842))]
#0  0x00007ffff7b38bfb in ioctl () from /lib64/libc.so.6
(gdb) bt
#0  0x00007ffff7b38bfb in ioctl () from /lib64/libc.so.6
#1  0x00007ffff75b59f0 in kmtIoctl () from /usr/lib64/libhsakmt.so.1
#2  0x00007ffff75af495 in hsaKmtWaitOnMultipleEvents () from /usr/lib64/libhsakmt.so.1
#3  0x00007ffff765b955 in rocr::core::Signal::WaitAny (signal_count=signal_count@entry=0x4, hsa_signals=hsa_signals@entry=0x7ffef0000be0,
    conds=conds@entry=0x555555632030, values=values@entry=0x7ffef0000c10, timeout=timeout@entry=0xffffffffffffffff, wait_hint=<optimized out>,
    wait_hint@entry=HSA_WAIT_STATE_BLOCKED, satisfying_value=0x7ffff7498e38)
    at /var/tmp/portage/dev-libs/rocr-runtime-5.5.1/work/ROCR-Runtime-rocm-5.5.1/src/core/runtime/signal.cpp:312
#4  0x00007ffff763c57e in rocr::AMD::hsa_amd_signal_wait_any (signal_count=0x4, hsa_signals=0x7ffef0000be0, conds=0x555555632030, values=0x7ffef0000c10,
    timeout_hint=timeout_hint@entry=0xffffffffffffffff, wait_hint=wait_hint@entry=HSA_WAIT_STATE_BLOCKED, satisfying_value=0x7ffff7498e38)
    at /var/tmp/portage/dev-libs/rocr-runtime-5.5.1/work/ROCR-Runtime-rocm-5.5.1/src/core/runtime/hsa_ext_amd.cpp:512
#5  0x00007ffff7652ec6 in rocr::core::Runtime::AsyncEventsLoop () at /usr/lib/gcc/x86_64-pc-linux-gnu/13/include/g++-v13/bits/stl_vector.h:1125
#6  0x00007ffff7608cb7 in rocr::os::ThreadTrampoline (arg=<optimized out>)
    at /var/tmp/portage/dev-libs/rocr-runtime-5.5.1/work/ROCR-Runtime-rocm-5.5.1/src/core/util/lnx/os_linux.cpp:77
#7  0x00007ffff7ac12b9 in ?? () from /lib64/libc.so.6
#8  0x00007ffff7b4430c in ?? () from /lib64/libc.so.6
(gdb) thread 5
[Switching to thread 5 (Thread 0x7ffef545d6c0 (LWP 23845))]
#0  0x00007ffff7b38bfb in ioctl () from /lib64/libc.so.6
(gdb) bt
#0  0x00007ffff7b38bfb in ioctl () from /lib64/libc.so.6
#1  0x00007ffff75b59f0 in kmtIoctl () from /usr/lib64/libhsakmt.so.1
#2  0x00007ffff75af495 in hsaKmtWaitOnMultipleEvents () from /usr/lib64/libhsakmt.so.1
#3  0x00007ffff75afb54 in hsaKmtWaitOnEvent () from /usr/lib64/libhsakmt.so.1
#4  0x00007ffff76401c2 in rocr::core::InterruptSignal::WaitRelaxed (this=0x7ffee859d9c0, condition=HSA_SIGNAL_CONDITION_LT, compare_value=0x1,
    timeout=<optimized out>, wait_hint=HSA_WAIT_STATE_BLOCKED)
    at /var/tmp/portage/dev-libs/rocr-runtime-5.5.1/work/ROCR-Runtime-rocm-5.5.1/src/core/runtime/interrupt_signal.cpp:212
#5  0x00007ffff764001a in rocr::core::InterruptSignal::WaitAcquire (this=<optimized out>, condition=<optimized out>, compare_value=<optimized out>,
    timeout=<optimized out>, wait_hint=<optimized out>)
    at /var/tmp/portage/dev-libs/rocr-runtime-5.5.1/work/ROCR-Runtime-rocm-5.5.1/src/core/runtime/interrupt_signal.cpp:220
#6  0x00007ffff7634481 in rocr::HSA::hsa_signal_wait_scacquire (hsa_signal=..., condition=HSA_SIGNAL_CONDITION_LT, compare_value=0x1,
    timeout_hint=0xffffffffffffffff, wait_state_hint=HSA_WAIT_STATE_BLOCKED)
    at /var/tmp/portage/dev-libs/rocr-runtime-5.5.1/work/ROCR-Runtime-rocm-5.5.1/src/core/runtime/hsa.cpp:1219
#7  0x00007ffff7962fcc in roc::WaitForSignal<false> (forced_wait=0x0, active_wait=<optimized out>, signal=...)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/cmake/../device/rocm/rocvirtual.hpp:79
#8  roc::VirtualGPU::HwQueueTracker::CpuWaitForSignal (this=<optimized out>, signal=0x7ffee859d920)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/device/rocm/rocvirtual.cpp:561
#9  0x00007ffff79b30c3 in roc::VirtualGPU::HwQueueTracker::WaitCurrent (this=<optimized out>)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/cmake/../device/rocm/rocvirtual.hpp:236
#10 roc::DmaBlitManager::hsaCopyStaged (this=this@entry=0x7ffee8002930, hostSrc=0x7ffed5800000 "", hostDst=0x555555974940 "", size=<optimized out>,
    staging=0x7ffef5100000 "", hostToDev=hostToDev@entry=0x0)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/device/rocm/rocblit.cpp:766
#11 0x00007ffff79b33a7 in roc::DmaBlitManager::readMemoryStaged (this=this@entry=0x7ffee8002930, srcMemory=..., dstHost=dstHost@entry=0x555555974940,
    xferBuf=..., origin=<optimized out>, offset=@0x7ffef545cb20: 0x0, totalSize=@0x7ffef545cb18: 0x1000, xferSize=0x1000)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/device/rocm/rocblit.cpp:57
#12 0x00007ffff79bb3bd in roc::DmaBlitManager::readBuffer (this=this@entry=0x7ffee8002930, srcMemory=..., dstHost=dstHost@entry=0x555555974940, origin=...,
    size=..., entire=entire@entry=0x1, copyMetadata=...)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/device/rocm/rocblit.cpp:138
#13 0x00007ffff79bb614 in roc::KernelBlitManager::readBuffer (this=this@entry=0x7ffee8002930, srcMemory=..., dstHost=dstHost@entry=0x555555974940,
    origin=..., size=..., entire=0x1, copyMetadata=...)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/device/rocm/rocblit.cpp:1774
#14 0x00007ffff796541a in roc::VirtualGPU::submitReadMemory (this=0x7ffee8000c70, cmd=...)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/device/rocm/rocvirtual.cpp:1558
#15 0x00007ffff793029b in amd::HostQueue::loop (this=this@entry=0x555555586f00, virtualDevice=0x7ffee8000c70)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/platform/commandqueue.cpp:215
#16 0x00007ffff793147b in amd::HostQueue::Thread::run (this=0x555555587028, data=0x555555586f00)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/platform/commandqueue.hpp:172
#17 0x00007ffff78beaed in amd::Thread::main (this=this@entry=0x555555587028)
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/thread/thread.cpp:93
#18 0x00007ffff7922b42 in amd::Thread::entry (thread=0x555555587028)
--Type <RET> for more, q to quit, c to continue without paging--
    at /var/tmp/portage/dev-libs/rocm-opencl-runtime-5.5.1/work/ROCclr-rocm-5.5.1/os/os_posix.cpp:340
#19 0x00007ffff7ac12b9 in ?? () from /lib64/libc.so.6
#20 0x00007ffff7b4430c in ?? () from /lib64/libc.so.6
(gdb)
```

---

### 评论 #3 — hkasivis (2023-12-15T11:43:04Z)

Based on the symptoms we believe the following patch should fix this issue. 

https://lists.freedesktop.org/archives/amd-gfx/2023-October/099742.html

---

### 评论 #4 — aagit (2023-12-17T02:20:14Z)

> Based on the symptoms we believe the following patch should fix this issue.
> 
> https://lists.freedesktop.org/archives/amd-gfx/2023-October/099742.html

Confirmed, I cherry-picked e341631f4a3129538cc398305649d54e6c0937d4 like below and it solved the issue. thanks a lot. I think you can close this issue.

```
+       } else if ((IP_VERSION_MAJ(adev->ip_versions[GC_HWIP][0]) == 9) &&
```

---

### 评论 #5 — itdimk (2023-12-17T09:13:17Z)

It works, thank you for help!
I just want to add that it also fixes the "broken" state of Open CL after waking up from suspend mode

---
