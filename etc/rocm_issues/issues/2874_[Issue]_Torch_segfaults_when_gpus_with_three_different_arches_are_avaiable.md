# [Issue]: Torch segfaults when gpus with three different arches are avaiable

> **Issue #2874**
> **状态**: closed
> **创建时间**: 2024-02-07T11:26:56Z
> **更新时间**: 2024-02-15T15:26:21Z
> **关闭时间**: 2024-02-13T18:28:48Z
> **作者**: IMbackK
> **标签**: Resolved, ROCm 6.0.0, AMD Instinct MI100, AMD Radeon Pro W6800, AMD Radeon Pro VII
> **URL**: https://github.com/ROCm/ROCm/issues/2874

## 标签

- **Resolved** (颜色: #6DAE35)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Instinct MI100** (颜色: #ededed)
- **AMD Radeon Pro W6800** (颜色: #ededed)
- **AMD Radeon Pro VII** (颜色: #ededed)

## 描述

### Problem Description

Hi,

I have a system with a rx6800 an mi50 and several mi100s.
Since rocm 6.0 there is a segfault in ExtractFatBinaryUsingCOMGR when more than two different gpu architectures are visible to pytorch when any operation involveing the gpus is performed (torch.cuda.is_available() and placeing any tensor on any gpu)
both the offical torch-2.3.0.dev20240207+rocm6.0-cp311-cp311-linux_x86_64 wheel and building torch from source exhibits this problem.
 
Restricting to a maximum of any 2 architectures using ROCR_VISIBLE_DEVICES works around this issue.

Below is a backtrace of the issue:

```
hip::FatBinaryInfo::ExtractFatBinaryUsingCOMGR (this=0x55555b582d50, devices=std::vector of length 3, capacity 4 = {...}) at /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_fatbin.cpp:230
230           query_list_array[isa_idx].isa = isa_it->first.c_str();                                                                                                                                          
(gdb) bt
#0  hip::FatBinaryInfo::ExtractFatBinaryUsingCOMGR (this=0x55555b582d50, devices=std::vector of length 3, capacity 4 = {...}) at /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_fatbin.cpp:230
#1  0x00007fff7f2cefae in hip::StatCO::digestFatBinary (this=this@entry=0x55555575a1a8, data=0x7fffe13b3000, programs=@0x55555981a240: 0x55555b582d50)
    at /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_code_object.cpp:752
#2  0x00007fff7f2cfaba in PlatformState::digestFatBinary (programs=@0x55555981a240: 0x55555b582d50, data=<optimized out>, this=<optimized out>)
    at /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_platform.cpp:829
#3  PlatformState::init (this=0x55555575a0a0) at /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_platform.cpp:670
#4  hip::init (status=0x7fffffffc807) at /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_context.cpp:76
#5  0x00007ffff76ae6af in __pthread_once_slow (once_control=0x7fff80911e78 <g_ihipInitialized>, init_routine=0x7fff46ae0230 <std::__once_proxy()>) at pthread_once.c:116
#6  0x00007fff7f2f0313 in __gthread_once (__func=<optimized out>, __once=<optimized out>) at /usr/include/c++/13.2.1/x86_64-pc-linux-gnu/bits/gthr-default.h:700
#7  std::call_once<void (&)(bool*), bool*> (__once=<optimized out>, __f=<optimized out>) at /usr/include/c++/13.2.1/mutex:907
#8  hipGetDeviceCount (count=0x7fffffffcea0) at /usr/src/debug/hip-runtime-amd/clr-rocm-6.0.0/hipamd/src/hip_device_runtime.cpp:637
#9  0x00007ffff517bb8a in c10::hip::device_count_ensure_non_zero() () at /usr/lib/libc10_hip.so
#10 0x00007fff821c0f2a in ??? () at /usr/lib/libtorch_hip.so
#11 0x00007fffee7bc984 in ??? () at /usr/lib/python3.11/site-packages/torch/lib/libtorch_python.so
#12 0x00007ffff79de349 in cfunction_vectorcall_NOARGS (func=0x7ffff6c984a0, args=<optimized out>, nargsf=<optimized out>, kwnames=<optimized out>) at ./Include/cpython/methodobject.h:52
#13 0x00007ffff79f2987 in _PyObject_VectorcallTstate (kwnames=<optimized out>, nargsf=<optimized out>, args=<optimized out>, callable=0x7ffff6c984a0, tstate=0x7ffff7d89378 <_PyRuntime+166328>)
    at ./Include/internal/pycore_call.h:92
#14 PyObject_Vectorcall (callable=0x7ffff6c984a0, args=<optimized out>, nargsf=<optimized out>, kwnames=<optimized out>) at Objects/call.c:299
#15 0x00007ffff79e4c23 in _PyEval_EvalFrameDefault (tstate=<optimized out>, frame=<optimized out>, throwflag=<optimized out>) at Python/ceval.c:4760
#16 0x00007ffff7a9c484 in _PyEval_EvalFrame (throwflag=0, frame=0x7ffff7f7d020, tstate=0x7ffff7d89378 <_PyRuntime+166328>) at ./Include/internal/pycore_ceval.h:73
#17 _PyEval_Vector
    (tstate=tstate@entry=0x7ffff7d89378 <_PyRuntime+166328>, func=func@entry=0x7ffff6ec7ce0, locals=locals@entry=0x7ffff71f31c0, args=args@entry=0x0, argcount=argcount@entry=0, kwnames=kwnames@entry=0x0)
    at Python/ceval.c:6425
#18 0x00007ffff7a9be6c in PyEval_EvalCode (co=0x7ffc65a35b30, globals=<optimized out>, locals=0x7ffff71f31c0) at Python/ceval.c:1140
#19 0x00007ffff7ab9fc3 in run_eval_code_obj (tstate=tstate@entry=0x7ffff7d89378 <_PyRuntime+166328>, co=co@entry=0x7ffc65a35b30, globals=globals@entry=0x7ffff71f31c0, locals=locals@entry=0x7ffff71f31c0)
    at Python/pythonrun.c:1710
#20 0x00007ffff7ab63ea in run_mod
    (mod=mod@entry=0x5555555cb710, filename=filename@entry=0x7ffff71f3330, globals=0x7ffff71f31c0, locals=0x7ffff71f31c0, flags=flags@entry=0x7fffffffd4f8, arena=arena@entry=0x7ffff711b750)
    at Python/pythonrun.c:1731
#21 0x00007ffff79be02a in PyRun_InteractiveOneObjectEx (fp=fp@entry=0x7ffff77f68e0 <_IO_2_1_stdin_>, filename=filename@entry=0x7ffff71f3330, flags=flags@entry=0x7fffffffd4f8) at Python/pythonrun.c:261
#22 0x00007ffff79be2f2 in _PyRun_InteractiveLoopObject (fp=0x7ffff77f68e0 <_IO_2_1_stdin_>, filename=0x7ffff71f3330, flags=0x7fffffffd4f8) at Python/pythonrun.c:138
#23 0x00007ffff793556b in _PyRun_AnyFileObject (fp=0x7ffff77f68e0 <_IO_2_1_stdin_>, filename=0x7ffff71f3330, closeit=0, flags=0x7fffffffd4f8) at Python/pythonrun.c:73
#24 0x00007ffff79be417 in PyRun_AnyFileExFlags (fp=0x7ffff77f68e0 <_IO_2_1_stdin_>, filename=<optimized out>, closeit=0, flags=0x7fffffffd4f8) at Python/pythonrun.c:105
#25 0x00007ffff792fc28 in pymain_run_stdin (config=0x7ffff7d6f3c0 <_PyRuntime+59904>) at Modules/main.c:509
#26 pymain_run_python (exitcode=0x7fffffffd4f0) at Modules/main.c:604
#27 Py_RunMain () at Modules/main.c:680
#28 0x00007ffff7a8e79b in Py_BytesMain (argc=<optimized out>, argv=<optimized out>) at Modules/main.c:734
#29 0x00007ffff7643cd0 in __libc_start_call_main (main=main@entry=0x555555555120 <main>, argc=argc@entry=1, argv=argv@entry=0x7fffffffd748) at ../sysdeps/nptl/libc_start_call_main.h:58
#30 0x00007ffff7643d8a in __libc_start_main_impl (main=0x555555555120 <main>, argc=1, argv=0x7fffffffd748, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffd738)
    at ../csu/libc-start.c:360
#31 0x0000555555555045 in _start ()
```

some more info on the crashed environment:

```
(gdb) p *query_list_array
$7 = {isa = 0x55555b584160 "amdgcn-amd-amdhsa--gfx908:sramecc+:xnack-", size = 0, offset = 0}
(gdb) p isa_idx
$8 = <optimized out>
(gdb) p devices
$9 = std::vector of length 3, capacity 4 = {0x55555b581220, 0x55555b5814a0, 0x55555b5818a0}
(gdb) p devices[0]
gdb hangs
```

 

### Operating System

Arch Linux

### CPU

AMD EPYC 7502P

### GPU

AMD Instinct MI100, AMD Radeon Pro W6800, AMD Radeon Pro VII

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — nartmada (2024-02-08T03:01:48Z)

An internal ticket has been created to track the investigation.

---

### 评论 #2 — IMbackK (2024-02-10T22:30:06Z)

i can also confirm that this problem is reproducible with just rocblas

---

### 评论 #3 — nartmada (2024-02-13T17:52:03Z)

This is a known internal issue which has been fixed.  The fix should be available in upcoming ROCm 6.1 release.

---

### 评论 #4 — ipanfilo (2024-02-13T18:28:48Z)

The fix is applied and should be available in upcoming ROCm-6.1

---

### 评论 #5 — IMbackK (2024-02-15T15:26:19Z)

Could we have the patch in question to apply to our own builds of rocm?

---
