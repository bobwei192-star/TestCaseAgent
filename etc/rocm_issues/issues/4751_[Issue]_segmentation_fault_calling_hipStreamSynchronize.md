# [Issue]: segmentation fault calling hipStreamSynchronize

> **Issue #4751**
> **状态**: closed
> **创建时间**: 2025-05-18T08:34:51Z
> **更新时间**: 2025-10-07T21:48:23Z
> **关闭时间**: 2025-07-25T15:08:42Z
> **作者**: fwyzard
> **标签**: Under Investigation, ROCm 6.2.4, ROCm 6.3.2
> **URL**: https://github.com/ROCm/ROCm/issues/4751

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.4** (颜色: #ededed)
- **ROCm 6.3.2** (颜色: #ededed)

## 描述

### Problem Description

On a Radeon Pro W7800 (`gfx1100`), calling `hipLaunchHostFunc` or `hipStreamAddCallback` more than ~53000 times on a stream causes a subsequent `hipStreamSynchronize` to crash with a segmentation fault.

Up to 52000 operations seem to work.
More than 53000 operations always fail.
Other values in between fail of succeed seemingly at random.

See the test program below to reproduce the issue.

On an Instinct MI250X the same test program works correctly, tested up to 1000000 operations.

Another symptom is that the call stack looks corrupted: running the test program in `gdb` and looking at the stack trace after the segmentation fault yields an infinite repetition of:
```
#0  0x00007ffff6762651 in amd::Command::releaseResources() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#1  0x00007ffff650a186 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#2  0x00007ffff6771ab0 in amd::ReferenceCountedObject::release() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#3  0x00007ffff676267c in amd::Command::releaseResources() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#4  0x00007ffff650a186 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#5  0x00007ffff6771ab0 in amd::ReferenceCountedObject::release() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#6  0x00007ffff676267c in amd::Command::releaseResources() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#7  0x00007ffff650a186 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#8  0x00007ffff6771ab0 in amd::ReferenceCountedObject::release() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#9  0x00007ffff676267c in amd::Command::releaseResources() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#10 0x00007ffff650a186 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
...
```



### Operating System

Red Hat Enterprise Linux 8.10

### CPU

AMD EPYC 9454 (×2)

### GPU

AMD Radeon PRO W7800

### ROCm Version

5.7.1, 6.2.4, 6.3.2, 6.4.0

### ROCm Component

HIP

### Steps to Reproduce

1. Save this as `test.cc`:
```c++
// C++ standard headers
#include <cassert>
#include <cstdlib>
#include <iostream>

// ROCm headers
#include <hip/hip_runtime.h>

#define HIP_CHECK(ARG, ...) assert((ARG) == hipSuccess) 

int main(int argc, char** argv)
{
    int reps = 55000;
    if (argc > 1) {
        reps = std::atoi(argv[1]);
    }

    std::cout << "select the first device... " << std::flush;
    HIP_CHECK(hipSetDevice(0));
    std::cout << "done" << std::endl;

    std::cout << "create the stream... " << std::flush;
    hipStream_t queue;
    HIP_CHECK(hipStreamCreate(&queue));
    std::cout << "done" << std::endl;

    std::cout << "enqueue " << reps << " host functions" << std::endl;
    for (int i = 0; i < reps; i++) {
        if (i % 1000 == 0) {
          std::cout << "... enqueued " << i << " host functions ..." << std::endl;
        }
        HIP_CHECK(hipLaunchHostFunc(
            queue,
            [](void*) {},
            nullptr)
        );
    }
    std::cout << "... enqueued " << reps << " host functions ..." << std::endl;
    std::cout << "done" << std::endl;

    std::cout << "synchronise the stream... " << std::flush;
    // if reps > ~53000, this calls causes a segmentation fault 
    HIP_CHECK(hipStreamSynchronize(queue));
    std::cout << "done" << std::endl;

    std::cout << "destroy the stream... " << std::flush;
    HIP_CHECK(hipStreamDestroy(queue));
    std::cout << "done" << std::endl;

    std::cout << "reset the device... " << std::flush;
    HIP_CHECK(hipDeviceReset());
    std::cout << "done" << std::endl;

    std::cout << "all done" << std::endl;
}
```

2. Compile with
```bash
/opt/rocm/bin/hipcc -O2 -g --offload-arch=gfx1100 test.cc -o test
```

3. Run with
```bash
./test
```

4. I get
```
select the first device... done
create the stream... done
enqueue 55000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
... enqueued 3000 host functions ...
... enqueued 4000 host functions ...
... enqueued 5000 host functions ...
... enqueued 6000 host functions ...
... enqueued 7000 host functions ...
... enqueued 8000 host functions ...
... enqueued 9000 host functions ...
... enqueued 10000 host functions ...
... enqueued 11000 host functions ...
... enqueued 12000 host functions ...
... enqueued 13000 host functions ...
... enqueued 14000 host functions ...
... enqueued 15000 host functions ...
... enqueued 16000 host functions ...
... enqueued 17000 host functions ...
... enqueued 18000 host functions ...
... enqueued 19000 host functions ...
... enqueued 20000 host functions ...
... enqueued 21000 host functions ...
... enqueued 22000 host functions ...
... enqueued 23000 host functions ...
... enqueued 24000 host functions ...
... enqueued 25000 host functions ...
... enqueued 26000 host functions ...
... enqueued 27000 host functions ...
... enqueued 28000 host functions ...
... enqueued 29000 host functions ...
... enqueued 30000 host functions ...
... enqueued 31000 host functions ...
... enqueued 32000 host functions ...
... enqueued 33000 host functions ...
... enqueued 34000 host functions ...
... enqueued 35000 host functions ...
... enqueued 36000 host functions ...
... enqueued 37000 host functions ...
... enqueued 38000 host functions ...
... enqueued 39000 host functions ...
... enqueued 40000 host functions ...
... enqueued 41000 host functions ...
... enqueued 42000 host functions ...
... enqueued 43000 host functions ...
... enqueued 44000 host functions ...
... enqueued 45000 host functions ...
... enqueued 46000 host functions ...
... enqueued 47000 host functions ...
... enqueued 48000 host functions ...
... enqueued 49000 host functions ...
... enqueued 50000 host functions ...
... enqueued 51000 host functions ...
... enqueued 52000 host functions ...
... enqueued 53000 host functions ...
... enqueued 54000 host functions ...
... enqueued 55000 host functions ...
done
synchronise the stream... Segmentation fault (core dumped)
```

**Note**: running `./test 52000` completes successfully:
```
select the first device... done
create the stream... done
enqueue 52000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 51000 host functions ...
... enqueued 52000 host functions ...
done
synchronise the stream... done
destroy the stream... done
reset the device... done
all done
```

The segmentation fault starts to happen between 52000 and 53000 operations.


**Note**: the same test works fine on an Instinct MI250X, tested up to 100k operations. 

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support
```
ROCk module version 6.12.12 is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.15
Runtime Ext Version:     1.7
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
[... skipping CPU agents ...]
*******                  
Agent 9                  
*******                  
  Name:                    gfx1100                            
  Uuid:                    GPU-c6afa01f760b6075               
  Marketing Name:          AMD Radeon PRO W7800               
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 BASE_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          64(0x40)                           
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    8                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
  Chip ID:                 29790(0x745e)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1895                               
  BDFID:                   768                                
  Internal Node ID:        8                                  
  Compute Unit:            70                                 
  SIMDs per CU:            2                                  
  Shader Engines:          6                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
  Coherent Host Access:    FALSE                              
  Memory Properties:       
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      TRUE                               
  Wavefront Size:          32(0x20)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        32(0x20)                           
  Max Work-item Per CU:    1024(0x400)                        
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 542                                
  SDMA engine uCode::      24                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    31440896(0x1dfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    31440896(0x1dfc000) KB             
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 3                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Recommended Granule:0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx1100         
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
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
```

### Additional Information

_No response_

---

## 评论 (16 条)

### 评论 #1 — fwyzard (2025-05-18T08:51:41Z)

Adding a breakpoint on `amd::Command::terminate` shows the initial stack:
```
#0  0x00007ffff650a170 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#1  0x00007ffff6771ab0 in amd::ReferenceCountedObject::release() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#2  0x00007ffff6766acf in amd::HostQueue::finish(bool) () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#3  0x00007ffff66b3613 in hip::hipStreamSynchronize_common(ihipStream_t*) () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#4  0x00007ffff66b52b4 in hip::hipStreamSynchronize(ihipStream_t*) () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#5  0x000000000020233a in main (argc=<optimized out>, argv=<optimized out>) at test.cc:43
```

Hitting `continue` a couple of time shows that the stack trace is getting corrupted:
```
#0  0x00007ffff650a170 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#1  0x00007ffff6771ab0 in amd::ReferenceCountedObject::release() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#2  0x00007ffff676267c in amd::Command::releaseResources() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#3  0x00007ffff650a186 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#4  0x00007ffff6771ab0 in amd::ReferenceCountedObject::release() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#5  0x00007ffff676267c in amd::Command::releaseResources() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#6  0x00007ffff650a186 in amd::Command::terminate() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#7  0x00007ffff6771ab0 in amd::ReferenceCountedObject::release() () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#8  0x00007ffff6766acf in amd::HostQueue::finish(bool) () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#9  0x00007ffff66b3613 in hip::hipStreamSynchronize_common(ihipStream_t*) () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#10 0x00007ffff66b52b4 in hip::hipStreamSynchronize(ihipStream_t*) () from /opt/rocm-6.4.0/lib/llvm/bin/../../../lib/libamdhip64.so.6
#11 0x000000000020233a in main (argc=<optimized out>, argv=<optimized out>) at test.cc:43
```

So it seem that the corruption is an unrelated problem (?).

---

### 评论 #2 — ppanchad-amd (2025-05-20T20:51:16Z)

Hi @fwyzard. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #3 — zichguan-amd (2025-07-08T14:32:44Z)

Hi @fwyzard, after some investigation, this seems to be a simple stack overflow. I was observing the same limit (~52000) on 7900XTX and MI300X machines.

The segfault always occurs at the same address `0x7fffff7feff8` with `#0  0x00007ffff66c28fc in __gnu_cxx::__normal_iterator<amd::Event* const*, std::vector<amd::Event*, std::allocator<amd::Event*> > >::__normal_iterator (this=<error reading variable: Cannot access memory at address 0x7fffff7feff8>, __i=<error reading variable: Cannot access memory at address 0x7fffff7feff0>) at /usr/include/c++/13/bits/stl_iterator.h:1076`

Looking at the `info proc map` with gdb
` 0x7fffff7ff000     0x7ffffffff000   0x800000        0x0  rw-p   [stack]`
and `0x7fffff7feff8` is right below the start of the stack. 

I believe the MI250X system that you were able to run up to 100k has a larger stack size. You can verify with `ulimit -s`, the standard should be 8192, 8MB. Increasing it will allow a larger limit: with `ulimit -Ss 1048576` (1GB), I can run `./test 100000` with no issue.

---

### 评论 #4 — fwyzard (2025-07-08T14:39:31Z)

The function calls are sequential, not nested, so why should they use such a deep stack ?

---

### 评论 #5 — zichguan-amd (2025-07-08T14:50:33Z)

I'm not sure yet, but looking at the stack trace, it seems that releases of resources are nested and that seems to be the reason. When there's too many resources to be freed, the stack gets deeper.

---

### 评论 #6 — zichguan-amd (2025-07-21T14:50:11Z)

Here's a quick breakdown of the recursive destruction chain:
- HostQueue::finish calls into command->release() to release the last command
- this release() is a ReferenceCountedObject::release, which calls Command::terminate to release dependent event resources before destroying the command
- terminate calls releaseResources to clear it's eventWaitList by iterating through the list and release() each event
- releasing each event will call into Command::terminate to release their dependencies
- recursively continues -> deepens the stack

Hope this helps. Let me know if you have any additional concerns, otherwise I'll close the issue.

---

### 评论 #7 — fwyzard (2025-07-21T15:04:47Z)

So... you're saying the current implementation is fine and the software is supposed to crash 🤔 ?

---

### 评论 #8 — zichguan-amd (2025-07-21T17:38:51Z)

I mean if you push it to the limit then yea it's going to overflow. You can always change the stack size or batch the function launches. Do you have any workload that requires this many resources to be freed at the same time?

---

### 评论 #9 — LiamfBerry (2025-07-21T17:52:01Z)

Is there a limit that could be documented so users can prevent overflow, otherwise it is under assumed that there is none.

---

### 评论 #10 — zichguan-amd (2025-07-21T18:05:17Z)

The limit depends on your system stack size settings, you can verify it with `ulimit -s`. The sample program crashed with a depth of ~142878 with a stack size of 8192. In a realistic workload it's unlikely to have that many resources to be freed together.

---

### 评论 #11 — fwyzard (2025-07-21T19:23:02Z)

For comparison, here are some test on different GPUs on the same class of machines (AlmaLinux release 9.6, linux 6.8.4-200, recent version of the GPU drivers and software stack).

### Test with an AMD Instinct MI300X
```
$ ./test.mi300
select the first device... done
create the stream... done
enqueue 55000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 54000 host functions ...
... enqueued 55000 host functions ...
done
synchronise the stream... Segmentation fault (core dumped)
```
With only 50'000 events:
```
$ time ./test.mi300 50000
select the first device... done
create the stream... done
enqueue 50000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 49000 host functions ...
... enqueued 50000 host functions ...
done
synchronise the stream... done
destroy the stream... done
reset the device... done
all done

real    0m12.852s
user    0m23.617s
sys     0m1.340s
```

### Test with an AMD Radeon Pro W7900
```
$ ./test.w7900 
select the first device... done
create the stream... done
enqueue 55000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 54000 host functions ...
... enqueued 55000 host functions ...
done
synchronise the stream... Segmentation fault (core dumped)
```

With only 50'000 events:
```
$ time ./test.w7900 50000
select the first device... done
create the stream... done
enqueue 50000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 49000 host functions ...
... enqueued 50000 host functions ...
done
synchronise the stream... done
destroy the stream... done
reset the device... done
all done

real    0m12.205s
user    0m22.497s
sys     0m1.281s
```

### Test with an NVIDA L40S
```
$ ./test.l40s 
select the first device... done
create the stream... done
enqueue 55000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 54000 host functions ...
... enqueued 55000 host functions ...
done
synchronise the stream... done
destroy the stream... done
reset the device... done
all done
```

With only 50'000 events:
```
$ time ./test.l40s 50000
select the first device... done
create the stream... done
enqueue 50000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 49000 host functions ...
... enqueued 50000 host functions ...
done
synchronise the stream... done
destroy the stream... done
reset the device... done
all done

real    0m0.479s
user    0m0.153s
sys     0m0.514s
```

With 4'000'000 (!) events:
```
$ time ./test.l40s 4000000
select the first device... done
create the stream... done
enqueue 4000000 host functions
... enqueued 0 host functions ...
... enqueued 1000 host functions ...
... enqueued 2000 host functions ...
...
... enqueued 3999000 host functions ...
... enqueued 4000000 host functions ...
done
synchronise the stream... done
destroy the stream... done
reset the device... done
all done

real    0m12.364s
user    0m12.064s
sys     0m15.667s
```

---

### 评论 #12 — fwyzard (2025-07-21T19:32:52Z)

I don't have a concrete, production use case: we ran into the issue while investigating the performance of the events and callbacks in the various GPUs. 

---

### 评论 #13 — zichguan-amd (2025-07-25T14:48:22Z)

Hi @fwyzard, I've spoken with internal teams about this, and they have decided to not make changes at this time because it would involve significant re-architecture of the entire stack, so the functionality will remain limited by your stack size. You are of course welcomed to propose changes by opening PRs. We appreciate your understanding.

---

### 评论 #14 — fwyzard (2025-07-25T15:02:11Z)

Understood.

---

### 评论 #15 — zichguan-amd (2025-07-25T15:08:42Z)

Thanks, I'll close this as not planned.

---

### 评论 #16 — fwyzard (2025-10-07T21:48:23Z)

In case anybody else lands here while searching for a workaround: with ROCm 6.4.1 on Alma 9.6, with an MI300X and the default stack size of 8192, this is now happening when submitting just 1000 host operations.

---
