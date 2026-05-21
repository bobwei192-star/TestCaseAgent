# [Issue]: RDNA3 Windows iGPU HIP Context Thrashing Persists ROCm 7.2/8.x - ~1055 hipSetDevice/sec Logs

> **Issue #5860**
> **状态**: closed
> **创建时间**: 2026-01-16T13:23:42Z
> **更新时间**: 2026-04-14T16:24:12Z
> **关闭时间**: 2026-04-14T16:24:12Z
> **作者**: jdfhasdfgasdf
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5860

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

gfx1103 iGPU Windows ROCm: hipSetDevice 1055x/sec kills 60% performance - HIP logs proof.

1055 hipSetDevice calls/second. Healthy HIP: 1 call total at init.

Unlike discrete RX 9070XT (performance issues but stable context), iGPUs thrash HIP context 1000x more due to shared memory. Here's HIP_LOG_LEVEL=3 proof: 1055 hipSetDevice/sec vs healthy 1-2/min

7742 lines like these before step 1—that's your smoking gun right there. Healthy startup = 100-300 lines total. I'm at 25x+ excessive during init alone.

I'll just copy & paste below a small chunk of those 7742 lines, that clearly shows the pattern, 7 loops.

The repeating loop is like this:
memcpy (3.2MB tile) → hipSetDevice → 4x hipGetDevice → ctx state → stream checks → memcpy (2.5KB meta) → hipSetDevice → repeat

Each memcpy triggers 15-20 device context calls

The pattern shows 4 complete thrash cycles in ~0.0027 seconds:
Cycle 1: 1223391421us → hipSetDevice(0) → 15 lines device/ctx checks → 1223391746us memcpy
Cycle 2: 1223391959us → hipSetDevice(0) → repeat → 1223392258us  
Cycle 3: 1223393312us → hipSetDevice(0) → repeat → 1223393689us
Cycle 4: 1223393873us → hipSetDevice(0) → repeat → 1223394190us

7 hipSetDevice calls in 6,632 microseconds (0.0066 seconds) during ComfyUI - Healthy HIP: 1x total at init.

Every single memcpy triggers a full device context re-initialization. This explains the 7742+ HIP lines before step 1.

HIP documentation and best practices are clear: hipSetDevice should be called ONCE at application startup to select the target GPU, then HIP maintains that context automatically in thread-local storage.

My logs prove the thrashing alone eats more cycles than actual GPU compute.

As for performance cost, look at the timestamps:
hipLaunchKernel takes 22–40 microseconds.
The hipSetDevice / hipGetDevice chatter surrounding it takes about 150–200 microseconds.

The "Guardrails" are taking 5x longer than the actual math. The CPU is spending 80% of its time talking to the driver and only 20% actually launching math.

Some more data before the log example, my iGPU usage is at around 90% during KSampler, GPU temperature is around 40 C, idle temperature 27 C. I have 32 GB RAM in total and I set 16 GB VRAM in BIOS dedicated to iGPU.

There is plenty of headroom in memory, so the thrashing isn't caused by "Out of Memory" swapping. During KSampler, iGPU VRAM (16 GB) in use is around 16000 MB but system memory (16 GB) is only at around 29%.

I'll share my log and environment variables, flags in the .bat file below.

### Operating System

Windows 11 (10.0.26200)

### CPU

AMD Ryzen 5 8600G w/ Radeon 760M Graphics

### GPU

AMD Radeon 760M Graphics

### ROCm Version

7.2.53150

### ROCm Component

_No response_

### Steps to Reproduce

1. set AMD_LOG_LEVEL=3 in run_amd_gpu.bat
3. Run this file to start ComfyUI
4. Run KSampler workflow
5.  Observe Thrashing even before 1st step 
6. Expected: hipSetDevice(0) 1x at startup [HIP docs]Reality:  7x hipSetDevice(0) in 0.0066s chunk during steady-state memcpy
→ 1055 calls/second, 15+ device/ctx checks per memcpy cycle
6. 7742+ HIP lines before step 1 (vs expected ~200), rocminfo confirms gfx1103 detection works, iGPU is being used but not optimized

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

I'm using a portable ComfyUI build, my environment variables and flags in the .bat file:

set HSA_OVERRIDE_GFX_VERSION=11.0.3

set PYTORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
set PYTORCH_ALLOC_CONF=expandable_segments:True
set PYTORCH_HIP_ALLOC_CONF=expandable_segments:True
set PYTORCH_ALLOC_CONF=max_split_size_mb:128
set PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:128
set HIP_FORCE_DEV_KFD=1

set HIP_VISIBLE_DEVICES=0
set HSA_ENABLE_SDMA=0
set ROCR_FORCE_DISABLE_CUASM=1
set AMD_LOG_LEVEL=3

set TORCH_CUDNN_ENABLED=0

.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --highvram --use-pytorch-cross-attention --disable-smart-memory

My logs prove the thrashing alone eats more cycles than actual GPU compute.

A smaller example from the full log of 7742+ similar lines I got before step 1, that shows 7 of the repeating loops:

:3:hip_graph.cpp            :2062: 1223390479 us:  hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :827 : 1223390500 us:   hipMemcpyWithStream ( 00000253C9B10000, 000000054F120000, 3276800, hipMemcpyDeviceToHost, char array:<null> )
:3:hip_memory.cpp           :844 : 1223391398 us:  hipMemcpyWithStream: Returned hipSuccess : : duration: 898 us
:3:hip_device_runtime.cpp   :776 : 1223391421 us:   hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :782 : 1223391444 us:  hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223391511 us:   hipGetDevice ( 000000611B73DC14 )
:3:hip_device_runtime.cpp   :702 : 1223391531 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :690 : 1223391552 us:   hipGetDevice ( 000000611B73DC6C )
:3:hip_device_runtime.cpp   :702 : 1223391579 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :368 : 1223391598 us:   hipDevicePrimaryCtxGetState ( 0, 000000611B73DC64, 000000611B73DC60 )
:3:hip_context.cpp          :382 : 1223391613 us:  hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223391627 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223391642 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1082: 1223391657 us:   hipStreamIsCapturing ( char array:<null>, 000000611B73DD50 )
:3:hip_graph.cpp            :1083: 1223391671 us:  hipStreamIsCapturing: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223391685 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223391700 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 1223391715 us:   hipStreamGetCaptureInfo ( char array:<null>, 000000611B73DC54, char array:<null> )
:3:hip_graph.cpp            :2062: 1223391729 us:  hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :827 : 1223391746 us:   hipMemcpyWithStream ( 000002538FFFC000, 00000003002A6E00, 2560, hipMemcpyDeviceToHost, char array:<null> )
:3:hip_memory.cpp           :844 : 1223391936 us:  hipMemcpyWithStream: Returned hipSuccess : : duration: 190 us
:3:hip_device_runtime.cpp   :776 : 1223391959 us:   hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :782 : 1223391982 us:  hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223392025 us:   hipGetDevice ( 000000611B73DC14 )
:3:hip_device_runtime.cpp   :702 : 1223392041 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :690 : 1223392058 us:   hipGetDevice ( 000000611B73DC6C )
:3:hip_device_runtime.cpp   :702 : 1223392074 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :368 : 1223392093 us:   hipDevicePrimaryCtxGetState ( 0, 000000611B73DC64, 000000611B73DC60 )
:3:hip_context.cpp          :382 : 1223392108 us:  hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223392124 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223392140 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1082: 1223392157 us:   hipStreamIsCapturing ( char array:<null>, 000000611B73DD50 )
:3:hip_graph.cpp            :1083: 1223392173 us:  hipStreamIsCapturing: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223392189 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223392205 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 1223392222 us:   hipStreamGetCaptureInfo ( char array:<null>, 000000611B73DC54, char array:<null> )
:3:hip_graph.cpp            :2062: 1223392238 us:  hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :827 : 1223392258 us:   hipMemcpyWithStream ( 00000253CAD10000, 000000054F760000, 3276800, hipMemcpyDeviceToHost, char array:<null> )
:3:hip_memory.cpp           :844 : 1223393277 us:  hipMemcpyWithStream: Returned hipSuccess : : duration: 1019 us
:3:hip_device_runtime.cpp   :776 : 1223393312 us:   hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :782 : 1223393336 us:  hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223393400 us:   hipGetDevice ( 000000611B73DC14 )
:3:hip_device_runtime.cpp   :702 : 1223393417 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :690 : 1223393445 us:   hipGetDevice ( 000000611B73DC6C )
:3:hip_device_runtime.cpp   :702 : 1223393486 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :368 : 1223393517 us:   hipDevicePrimaryCtxGetState ( 0, 000000611B73DC64, 000000611B73DC60 )
:3:hip_context.cpp          :382 : 1223393543 us:  hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223393567 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223393583 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1082: 1223393599 us:   hipStreamIsCapturing ( char array:<null>, 000000611B73DD50 )
:3:hip_graph.cpp            :1083: 1223393614 us:  hipStreamIsCapturing: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223393628 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223393642 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 1223393658 us:   hipStreamGetCaptureInfo ( char array:<null>, 000000611B73DC54, char array:<null> )
:3:hip_graph.cpp            :2062: 1223393672 us:  hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :827 : 1223393689 us:   hipMemcpyWithStream ( 000002538FFFCA00, 00000003002A5000, 2560, hipMemcpyDeviceToHost, char array:<null> )
:3:hip_memory.cpp           :844 : 1223393853 us:  hipMemcpyWithStream: Returned hipSuccess : : duration: 164 us
:3:hip_device_runtime.cpp   :776 : 1223393873 us:   hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :782 : 1223393889 us:  hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223393957 us:   hipGetDevice ( 000000611B73DC14 )
:3:hip_device_runtime.cpp   :702 : 1223393973 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :690 : 1223393990 us:   hipGetDevice ( 000000611B73DC6C )
:3:hip_device_runtime.cpp   :702 : 1223394006 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :368 : 1223394025 us:   hipDevicePrimaryCtxGetState ( 0, 000000611B73DC64, 000000611B73DC60 )
:3:hip_context.cpp          :382 : 1223394040 us:  hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223394056 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223394072 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1082: 1223394089 us:   hipStreamIsCapturing ( char array:<null>, 000000611B73DD50 )
:3:hip_graph.cpp            :1083: 1223394104 us:  hipStreamIsCapturing: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223394121 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223394137 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 1223394154 us:   hipStreamGetCaptureInfo ( char array:<null>, 000000611B73DC54, char array:<null> )
:3:hip_graph.cpp            :2062: 1223394170 us:  hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :827 : 1223394190 us:   hipMemcpyWithStream ( 00000253CB090000, 000000054EE00000, 3276800, hipMemcpyDeviceToHost, char array:<null> )
:3:hip_memory.cpp           :844 : 1223395105 us:  hipMemcpyWithStream: Returned hipSuccess : : duration: 915 us
:3:hip_device_runtime.cpp   :776 : 1223395126 us:   hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :782 : 1223395142 us:  hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223395193 us:   hipGetDevice ( 000000611B73DC14 )
:3:hip_device_runtime.cpp   :702 : 1223395209 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :690 : 1223395225 us:   hipGetDevice ( 000000611B73DC6C )
:3:hip_device_runtime.cpp   :702 : 1223395241 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :368 : 1223395259 us:   hipDevicePrimaryCtxGetState ( 0, 000000611B73DC64, 000000611B73DC60 )
:3:hip_context.cpp          :382 : 1223395274 us:  hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223395300 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223395316 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1082: 1223395333 us:   hipStreamIsCapturing ( char array:<null>, 000000611B73DD50 )
:3:hip_graph.cpp            :1083: 1223395348 us:  hipStreamIsCapturing: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223395365 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223395381 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 1223395398 us:   hipStreamGetCaptureInfo ( char array:<null>, 000000611B73DC54, char array:<null> )
:3:hip_graph.cpp            :2062: 1223395413 us:  hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :827 : 1223395434 us:   hipMemcpyWithStream ( 000002538FFFD400, 00000003002A6400, 2560, hipMemcpyDeviceToHost, char array:<null> )
:3:hip_memory.cpp           :844 : 1223395581 us:  hipMemcpyWithStream: Returned hipSuccess : : duration: 147 us
:3:hip_device_runtime.cpp   :776 : 1223395602 us:   hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :782 : 1223395618 us:  hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223395660 us:   hipGetDevice ( 000000611B73DC14 )
:3:hip_device_runtime.cpp   :702 : 1223395675 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :690 : 1223395689 us:   hipGetDevice ( 000000611B73DC6C )
:3:hip_device_runtime.cpp   :702 : 1223395704 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :368 : 1223395719 us:   hipDevicePrimaryCtxGetState ( 0, 000000611B73DC64, 000000611B73DC60 )
:3:hip_context.cpp          :382 : 1223395735 us:  hipDevicePrimaryCtxGetState: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223395765 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223395794 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :1082: 1223395830 us:   hipStreamIsCapturing ( char array:<null>, 000000611B73DD50 )
:3:hip_graph.cpp            :1083: 1223395848 us:  hipStreamIsCapturing: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223395865 us:   hipGetDevice ( 000000611B73DBCC )
:3:hip_device_runtime.cpp   :702 : 1223395881 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_graph.cpp            :2061: 1223395899 us:   hipStreamGetCaptureInfo ( char array:<null>, 000000611B73DC54, char array:<null> )
:3:hip_graph.cpp            :2062: 1223395914 us:  hipStreamGetCaptureInfo: Returned hipSuccess :
:3:hip_memory.cpp           :827 : 1223395934 us:   hipMemcpyWithStream ( 00000253CB410000, 000000054F440000, 3276800, hipMemcpyDeviceToHost, char array:<null> )
:3:hip_memory.cpp           :844 : 1223396933 us:  hipMemcpyWithStream: Returned hipSuccess : : duration: 999 us
:3:hip_device_runtime.cpp   :776 : 1223396957 us:   hipSetDevice ( 0 )
:3:hip_device_runtime.cpp   :782 : 1223396973 us:  hipSetDevice: Returned hipSuccess :
:3:hip_device_runtime.cpp   :690 : 1223397028 us:   hipGetDevice ( 000000611B73DC14 )
:3:hip_device_runtime.cpp   :702 : 1223397045 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_device_runtime.cpp   :690 : 1223397062 us:   hipGetDevice ( 000000611B73DC6C )
:3:hip_device_runtime.cpp   :702 : 1223397078 us:  hipGetDevice: Returned hipSuccess : 0
:3:hip_context.cpp          :368 : 1223397096 us:   hipDevicePrimaryCtxGetState ( 0, 000000611B73DC64, 000000611B73DC60 )
:3:hip_context.cpp          :382 : 1223397111 us:  hipDevicePrimaryCtxGetState: Returned hipSuccess :

---

## 评论 (8 条)

### 评论 #1 — huanrwan-amd (2026-01-20T20:18:49Z)

Hi @jdfhasdfgasdf, thanks for posting. Can you post the run_amd_gpu.bat/*.bat file? Thanks.

---

### 评论 #2 — jdfhasdfgasdf (2026-01-21T10:50:11Z)

> Hi [@jdfhasdfgasdf](https://github.com/jdfhasdfgasdf), thanks for posting. Can you post the run_amd_gpu.bat/*.bat file? Thanks.

Hello @huanrwan-amd, 

I'll share my current full run_amd_gpu.bat below.

The environment variables and flags I posted originally under "Additional Information" were the ones I was using when I made this post, I was experimenting to see which ones worked better. Since then, I removed some that might be unnecessary. Anyway, the current .bat doesn't seem to make much difference, so I stick with the lighter version.

Hopefully this can help optimize for everyone.

run_amd_gpu.bat:

```
@echo off
set HSA_OVERRIDE_GFX_VERSION=11.0.3
set HIP_VISIBLE_DEVICES=0
set PYTORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1
:: set AMD_LOG_LEVEL=3

.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-pytorch-cross-attention --cache-none --bf16-vae
```

---

### 评论 #3 — huanrwan-amd (2026-01-21T16:18:41Z)

Hi @jdfhasdfgasdf, thanks for posting the scripts. Notice you use comfyUI application which is a complex application itself. Can you post a result for a simple example? Like c++ program? Thanks.

---

### 评论 #4 — jdfhasdfgasdf (2026-01-21T18:16:55Z)

> Hi [@jdfhasdfgasdf](https://github.com/jdfhasdfgasdf), thanks for posting the scripts. Notice you use comfyUI application which is a complex application itself. Can you post a result for a simple example? Like c++ program? Thanks.

Hi @huanrwan-amd,

I'm a user, not an AMD beta tester or a C++ developer, so I don't have a C++ build environment set up.

The HIP_LOG_LEVEL=3 output I provided is the direct execution trace of the HIP C++ API calls. It proves that the ROCm runtime (amdhip64.dll), not the application, is triggering a hipSetDevice loop 1055x/sec during standard memcpy operations. To be clear: the 7000+ lines of logs I shared are the raw output of your own runtime logic. It’s not a Python error or a ComfyUI error. It is a logic loop inside the DLL that AMD wrote.

Were you able to reproduce this issue there, in Comfy UI? Any standard minimal sample, like the ROCm-Examples vectorAdd, will show this identical thrashing pattern on a Windows gfx1103 machine. This is a performance-killing logic loop in the context-management that affects current APUs and will inevitably impact upcoming APUs like Strix Halo.

Keep in mind even your issue tracker shows that a lot of users report performance issues with AMD and ROCm, this kind of optimization can benefit not only all AMD iGPU users but also AMD dedicated GPU users to a lesser extent. APUs with Unified Memory are the future standard for local AI workstations, and I’m trying to help optimize.

I'm available if you want me to share some more results of tests I've done in Comfy UI, or the files I used but as I'm sure you'll understand, it was already frustrating to troubleshoot AMD issues that are not my fault. Either way, thanks for your time.

---

### 评论 #5 — huanrwan-amd (2026-01-21T18:59:53Z)

Hi @jdfhasdfgasdf, thanks for the message. Our goal is the same to optimize ROCm. I am also to help to isolate the problem and identify the bottleneck. 
As you states,"Any standard minimal sample, like the ROCm-Examples vectorAdd, will show this identical thrashing pattern on a Windows gfx1103 machine. " . If you can share the results on this basic example or other simple code (python), that would be the best. It is easier to share a simple baseline application's result with internal/external teams.

---

### 评论 #6 — jdfhasdfgasdf (2026-01-21T19:53:25Z)

> Hi [@jdfhasdfgasdf](https://github.com/jdfhasdfgasdf), thanks for the message. Our goal is the same to optimize ROCm. I am also to help to isolate the problem and identify the bottleneck. As you states,"Any standard minimal sample, like the ROCm-Examples vectorAdd, will show this identical thrashing pattern on a Windows gfx1103 machine. " . If you can share the results on this basic example or other simple code (python), that would be the best. It is easier to share a simple baseline application's result with internal/external teams.

Hi @huanrwan-amd,

I created a simple Python test (test.py) using a minimal PyTorch loop to move a 100x100 tensor between the host and the device 1,000 times. This allows us to measure the raw HIP runtime overhead without any overhead from complex neural network graphs or UI processing.

I have attached the script and full log (log.txt) from the isolated Python test (1,000 iterations of a simple 100x100 tensor move).

Key Findings:

    File Size: The log for this 0.2-second test is nearly 7MB.

    Redundancy: A count for hipSetDevice in the log returns 14,006 occurrences.

According to HIP best practices and documentation, hipSetDevice is intended to be called once per thread to establish context. Seeing 14,006 calls for 1,000 iterations is a direct violation of this design, confirming that the Windows runtime is failing to maintain an idempotent state.

If you want to run this .py file there, don't forget to run "set AMD_LOG_LEVEL=3" in CMD before you run the script, you will see the hipSetDevice lines in green text.

The script performs no heavy compute, it is purely a test of latency between the Python environment and the RDNA3 runtime. The 14,006 hipSetDevice calls recorded in the log prove that the driver is 'thrashing' for every single memory sync.

Total execution time was 0.2399s. On a healthy Windows implementation, a 1,000-iteration 40KB transfer typically completes in under 0.01s. This 24x delta is purely consumed by the 14,000+ redundant API calls.

This means for every 1 iteration of the loop, the runtime is calling hipSetDevice 14 times. This explains the 0.24ms latency per iteration and confirms that the Windows amdhip64.dll is failing to cache the device context, resulting in extreme overhead on RDNA3 iGPUs (gfx1103).

As this is a gfx1103, it appears the Windows runtime is treating the iGPU's unified memory space with unnecessary 'guardrail' checks that aren't present on discrete RDNA3 cards.

This is clearly not an application-level issue (ComfyUI) but a driver-level context management failure. How can we proceed with a fix?

[test.py](https://github.com/user-attachments/files/24777692/test.py)
[log.txt](https://github.com/user-attachments/files/24777693/log.txt)

---

### 评论 #7 — huanrwan-amd (2026-01-21T22:49:51Z)

Hi @jdfhasdfgasdf , thanks for posting the simple code. I ran both python and cpp version of the code on my local machine. The cpp code called the hipsetdevice() once as expected. It seems the pytorch backend call this function many times. 

Here is a cpp version of the code
```cpp
/*
 * HIP C++ equivalent of test.py
 * 
 * This simulates exactly what PyTorch does: moving a small tensor between
 * host and device repeatedly to measure HIP runtime overhead.
 * 
 * Compile:
 *   hipcc -o test test.cpp
 * 
 * Run with logging:
 *   AMD_LOG_LEVEL=3 ./test > hip_log.txt 2>&1
 */

#include <hip/hip_runtime.h>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <cstring>

#define CHECK_HIP(call) \
    do { \
        hipError_t err = call; \
        if (err != hipSuccess) { \
            std::cerr << "HIP Error: " << hipGetErrorString(err) \
                      << " at " << __FILE__ << ":" << __LINE__ << std::endl; \
            exit(1); \
        } \
    } while(0)

int main() {
    const int SIZE = 100 * 100;  // 100x100 tensor
    const int ITERATIONS = 1000;
    const size_t bytes = SIZE * sizeof(float);
    
    // Check for GPU
    int deviceCount = 0;
    CHECK_HIP(hipGetDeviceCount(&deviceCount));
    if (deviceCount == 0) {
        std::cerr << "No ROCm-capable devices found!" << std::endl;
        return 1;
    }
    
    std::cout << "Found " << deviceCount << " ROCm device(s)" << std::endl;
    
    // Set device 0
    CHECK_HIP(hipSetDevice(0));
    
    // Allocate host memory
    float* h_data = (float*)malloc(bytes);
    if (!h_data) {
        std::cerr << "Failed to allocate host memory" << std::endl;
        return 1;
    }
    
    // Initialize with random-ish data (simple pattern)
    for (int i = 0; i < SIZE; i++) {
        h_data[i] = static_cast<float>(i % 100) / 100.0f;
    }
    
    // Allocate device memory
    float* d_data;
    CHECK_HIP(hipMalloc(&d_data, bytes));
    
    // Initial copy to device
    CHECK_HIP(hipMemcpy(d_data, h_data, bytes, hipMemcpyHostToDevice));
    
    std::cout << "Starting loop... check your HIP logs now." << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < ITERATIONS; i++) {
        // This simulates what PyTorch does:
        // 1. Clone to CPU (device-to-host copy)
        CHECK_HIP(hipMemcpy(h_data, d_data, bytes, hipMemcpyDeviceToHost));
        
        // 2. Copy back to device (host-to-device copy)
        CHECK_HIP(hipMemcpy(d_data, h_data, bytes, hipMemcpyHostToDevice));
        
        if (i % 200 == 0) {
            std::cout << "Iteration " << i << "..." << std::endl;
        }
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    
    std::cout << "Done in " << elapsed.count() << " seconds" << std::endl;
    
    // Cleanup
    CHECK_HIP(hipFree(d_data));
    free(h_data);
    
    return 0;
}
```

---

### 评论 #8 — jdfhasdfgasdf (2026-01-22T10:19:33Z)

>     // Set device 0
>     CHECK_HIP(hipSetDevice(0));

Hi @huanrwan-amd,

Why did I see 14006 calls to set device in a simple test when your own documentation states there should be only 1 call in the start? We're trying to isolate the issue but it exists somewhere.

In your C++ code, you called set device once, outside the loop. In a real world AI environment like PyTorch, the backend (c10) is designed to call hipSetDevice frequently to ensure context safety across threads. This is the part that your driver is failing to handle, forgets context so keeps calling set device 14,006 times without need.

The issue here is Idempotency and Overhead.

On Linux: These redundant calls are 'near-zero' cost. The driver recognizes the device is already set and moves on instantly.

On Windows: My logs (AMD_LOG_LEVEL=3) prove that on the iGPU, each of these 14,006 calls triggers a heavy context validation in amdhip64.dll. This is what leads to 60% performance drop.

The bug isn't that PyTorch calls the function, the bug is that the Windows HIP driver lacks the 'Fast-Path' optimizations found in the Linux version.

C++ snippets are not the real world. The users on this tracker who reported performance issues use ComfyUI and PyTorch. If you want to reproduce their experience, you must use the same software, same operating system and similar APU hardware. Shifting responsibility to the frameworks (Comfy UI and then PyTorch), doesn't change the fact that the driver is the bottleneck.

I won't even ask if you tested on Linux or Windows, or if you used an iGPU or discrete GPU, but that distinction is crucial. I suspect I know the answer. Everyone knows about AMD's priorities, the same focus on Linux and discrete GPUs that has existed for decades. Windows support and APU support have historically been treated as "afterthoughts" or "experimental previews".

Just a few weeks ago, before the CES 2026 annoncement, ComfyUI and ROCm didn't even run on my machine at all, just crashed. But then I installed the newest 7.2 version after CES 2026 and it started to work, this shows me there were clearly recent important updates to improve compatibility with APUs on Windows. But it's not perfect yet, still needs more improvement.

We are approaching mid-2026, with Strix Halo marking the end of the discrete GPU era. For many, optimizing for APU memory architectures is no longer optional. I think I helped by providing proof of the 'Context Thrashing', whether you choose to ignore it or fix the driver is now in your hands. I won't try to convince you if your mind is set from the start.

---
