# ROCm Crashesh on Ryzen 5 5625U APU with Vega Graphics

> **Issue #2357**
> **状态**: closed
> **创建时间**: 2023-07-30T20:54:03Z
> **更新时间**: 2023-09-06T22:52:41Z
> **关闭时间**: 2023-09-06T22:52:41Z
> **作者**: HurricanePootis
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2357

## 描述

The Ryzen 5 5625U's integrated GPU is a gfx90 graphics card, code named Barceló. Whenever I load up Blender 3.6 with ROCm 5.6, my GPU does show up under the HIP settings in the blender system settings. However, whenever I go to render something, it crashes. Below, I have attached a backtrace of the crash.


```
Thread 66 "blender" received signal SIGFPE, Arithmetic exception.
[Switching to Thread 0x7ffe826d1000 (LWP 12929)]
0x00007fff82558db8 in hip_impl::ihipOccupancyMaxActiveBlocksPerMultiprocessor(int*, int*, int*, amd::Device const&, ihipModuleSymbol_t*, int, unsigned long, bool) [clone .constprop.0] (maxBlocksPerCU=maxBlocksPerCU@entry=0x7ffe826ccb48, numBlocksPerGrid=numBlocksPerGrid@entry=0x7ffe826ccb50, 
    bestBlockSize=bestBlockSize@entry=0x7ffe826ccb3c, device=..., func=func@entry=0x7ffe6ac01500, inputBlockSize=1024, inputBlockSize@entry=0, dynamicSMemSize=0, 
    bCalcPotentialBlkSz=true) at /usr/src/debug/hip-runtime-amd/clr-rocm-5.6.0/hipamd/src/hip_platform.cpp:344
Downloading source file /usr/src/debug/hip-runtime-amd/clr-rocm-5.6.0/hipamd/src/hip_platform.cpp
344         VgprWaves = maxVGPRs / amd::alignUp(wrkGrpInfo->usedVGPRs_, VgprGranularity);                                                                              
(gdb) bt
#0  0x00007fff82558db8 in hip_impl::ihipOccupancyMaxActiveBlocksPerMultiprocessor(int*, int*, int*, amd::Device const&, ihipModuleSymbol_t*, int, unsigned long, bool) [clone .constprop.0]
    (maxBlocksPerCU=maxBlocksPerCU@entry=0x7ffe826ccb48, numBlocksPerGrid=numBlocksPerGrid@entry=0x7ffe826ccb50, bestBlockSize=bestBlockSize@entry=0x7ffe826ccb3c, device=..., func=func@entry=0x7ffe6ac01500, inputBlockSize=1024, inputBlockSize@entry=0, dynamicSMemSize=0, bCalcPotentialBlkSz=true)
    at /usr/src/debug/hip-runtime-amd/clr-rocm-5.6.0/hipamd/src/hip_platform.cpp:344
#1  0x00007fff82443c35 in hipModuleOccupancyMaxPotentialBlockSize(int*, int*, hipFunction_t, size_t, int)
    (gridSize=<optimized out>, blockSize=0x7ffe8d5d1758, f=0x7ffe6ac01500, dynSharedMemPerBlk=<optimized out>, blockSizeLimit=<optimized out>)
    at /usr/src/debug/hip-runtime-amd/clr-rocm-5.6.0/hipamd/src/hip_platform.cpp:426
#2  0x0000555557e5cacb in ccl::HIPDeviceKernels::load(ccl::HIPDevice*) ()
#3  0x0000555557e5c9e7 in ccl::HIPDevice::load_kernels(unsigned int) ()
#4  0x0000555557e5e025 in ccl::MultiDevice::load_kernels(unsigned int) ()
#5  0x000055555828479d in ccl::Scene::load_kernels(ccl::Progress&) ()
#6  0x00005555583b5c56 in ccl::Session::run_update_for_next_iteration() ()
#7  0x00005555583b724b in ccl::Session::run_main_render_loop() ()
#8  0x00005555583b7d5c in ccl::Session::thread_render() ()
#9  0x00005555583b7f23 in ccl::Session::thread_run() ()
#10 0x000055555848dc7e in ccl::thread::run(void*) ()
#11 0x00007fffddae1943 in std::execute_native_thread_routine(void*) (__p=0x7ffe8d452c80) at /usr/src/debug/gcc/gcc/libstdc++-v3/src/c++11/thread.cc:104
#12 0x00007fffdd89d44b in start_thread (arg=<optimized out>) at pthread_create.c:444
#13 0x00007fffdd920e40 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
```
