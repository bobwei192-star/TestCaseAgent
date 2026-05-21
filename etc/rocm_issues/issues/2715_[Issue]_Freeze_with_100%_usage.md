# [Issue]: Freeze with 100% usage

> **Issue #2715**
> **状态**: closed
> **创建时间**: 2023-12-14T20:53:12Z
> **更新时间**: 2024-05-26T03:15:10Z
> **关闭时间**: 2024-05-26T03:15:10Z
> **作者**: tada123
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2715

## 描述

### Problem Description

When trying to move a buffer to GPU, the code freezes with 100% CPU usage in hsa library (probably an infinite loop).
I use ArchLinux and the problem disappears, when using `linux-lts` (older) kernel.
When debugging with GDB, i get following info (when i interrupt the program in the 100% usage state):

```
(gdb) r
Starting program: /usr/bin/python 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
Python 3.11.6 (main, Nov 14 2023, 09:36:21) [GCC 13.2.1 20230801] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> t = torch.tensor([0.1, 0.5])
>>> c = t.to('cuda')
[New Thread 0x7ffeb02296c0 (LWP 11107)]
[New Thread 0x7ffeafa286c0 (LWP 11108)]
[Thread 0x7ffeafa286c0 (LWP 11108) exited]
^C
Thread 1 "python" received signal SIGINT, Interrupt.
0x00007fff4e6501d1 in rocr::core::InterruptSignal::WaitRelaxed(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
(gdb) bt
#0  0x00007fff4e6501d1 in rocr::core::InterruptSignal::WaitRelaxed(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#1  0x00007fff4e65006a in rocr::core::InterruptSignal::WaitAcquire(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#2  0x00007fff4e643d49 in rocr::HSA::hsa_signal_wait_scacquire(hsa_signal_s, hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#3  0x00007fff88c0ad45 in roctracer::hsa_support::detail::hsa_signal_wait_scacquire_callback(hsa_signal_s, hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libroctracer64.so
#4  0x00007fffa66a8b83 in bool roc::WaitForSignal<false>(hsa_signal_s, bool, bool) () from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#5  0x00007fffa669fd68 in roc::VirtualGPU::HwQueueTracker::CpuWaitForSignal(roc::ProfilingSignal*) () from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#6  0x00007fffa66ce13d in roc::DmaBlitManager::hsaCopyStaged(unsigned char const*, unsigned char*, unsigned long, unsigned char*, bool) const ()
   from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#7  0x00007fffa66cffc7 in roc::DmaBlitManager::writeBuffer(void const*, device::Memory&, amd::Coord3D const&, amd::Coord3D const&, bool, amd::CopyMetadata) const ()
   from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#8  0x00007fffa66d026b in roc::KernelBlitManager::writeBuffer(void const*, device::Memory&, amd::Coord3D const&, amd::Coord3D const&, bool, amd::CopyMetadata) const ()
   from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#9  0x00007fffa66a0c79 in roc::VirtualGPU::submitWriteMemory(amd::WriteMemoryCommand&) () from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#10 0x00007fffa667761a in amd::Command::enqueue() () from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#11 0x00007fffa65239a0 in ihipMemcpy(void*, void const*, unsigned long, hipMemcpyKind, hip::Stream&, bool, bool) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#12 0x00007fffa65684c0 in hipMemcpyWithStream () from /usr/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#13 0x00007fffa863c97a in at::native::copy_kernel_cuda(at::TensorIterator&, bool) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_hip.so
#14 0x00007fffdecb43bf in at::native::copy_impl(at::Tensor&, at::Tensor const&, bool) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#15 0x00007fffdecb56f2 in at::native::copy_(at::Tensor&, at::Tensor const&, bool) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#16 0x00007fffdf98ea1f in at::_ops::copy_::call(at::Tensor&, at::Tensor const&, bool) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#17 0x00007fffdef843c5 in at::native::_to_copy(at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#18 0x00007fffdfd2069b in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd___to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#19 0x00007fffdf489fb5 in at::_ops::_to_copy::redispatch(c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#20 0x00007fffdfb4fd03 in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>), &at::(anonymous namespace)::_to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#21 0x00007fffdf489fb5 in at::_ops::_to_copy::redispatch(c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#22 0x00007fffe121d94f in torch::autograd::VariableType::(anonymous namespace)::_to_copy(c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#23 0x00007fffe121defe in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>), &torch::autograd::VariableType::(anonymous namespace)::_to_copy>, at::Tensor, c10::guts::typelist::typelist<c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat> > >, at::Tensor (c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#24 0x00007fffdf5114de in at::_ops::_to_copy::call(at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#25 0x00007fffdef7bd1b in at::native::to(at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#26 0x00007fffdfef8a41 in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, bool, c10::optional<c10::MemoryFormat>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeImplicitAutograd_dtype_layout_to>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, bool, c10::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, bool, c10::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, bool, c10::optional<c10::MemoryFormat>) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#27 0x00007fffdf6a6183 in at::_ops::to_dtype_layout::call(at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, bool, c10::optional<c10::MemoryFormat>) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#28 0x00007ffff56a2308 in torch::autograd::dispatch_to(at::Tensor const&, c10::Device, bool, bool, c10::optional<c10::MemoryFormat>) ()
   from /usr/lib/python3.11/site-packages/torch/lib/libtorch_python.so
#29 0x00007ffff56ff0d4 in torch::autograd::THPVariable_to(_object*, _object*, _object*) () from /usr/lib/python3.11/site-packages/torch/lib/libtorch_python.so
#30 0x00007ffff7a058a5 in ?? () from /usr/lib/libpython3.11.so.1.0
#31 0x00007ffff79f2987 in PyObject_Vectorcall () from /usr/lib/libpython3.11.so.1.0
#32 0x00007ffff79e4c23 in _PyEval_EvalFrameDefault () from /usr/lib/libpython3.11.so.1.0
#33 0x00007ffff7a9c484 in ?? () from /usr/lib/libpython3.11.so.1.0
#34 0x00007ffff7a9be6c in PyEval_EvalCode () from /usr/lib/libpython3.11.so.1.0
#35 0x00007ffff7ab9fc3 in ?? () from /usr/lib/libpython3.11.so.1.0
#36 0x00007ffff7ab63ea in ?? () from /usr/lib/libpython3.11.so.1.0
#37 0x00007ffff79be02a in ?? () from /usr/lib/libpython3.11.so.1.0
#38 0x00007ffff79be2f2 in _PyRun_InteractiveLoopObject () from /usr/lib/libpython3.11.so.1.0
#39 0x00007ffff793556b in ?? () from /usr/lib/libpython3.11.so.1.0
#40 0x00007ffff79be417 in PyRun_AnyFileExFlags () from /usr/lib/libpython3.11.so.1.0
#41 0x00007ffff792fc28 in ?? () from /usr/lib/libpython3.11.so.1.0
#42 0x00007ffff7a8e79b in Py_BytesMain () from /usr/lib/libpython3.11.so.1.0
#43 0x00007ffff7645cd0 in ?? () from /usr/lib/libc.so.6
#44 0x00007ffff7645d8a in __libc_start_main () from /usr/lib/libc.so.6
#45 0x0000555555555045 in _start ()
(gdb) 
```

Also, i see difference of `rocminfo` outputs on those two kernels (on the same computer). Looks like this (compared with `diff`):

```
11c11
< DMAbuf Support:          YES
---
> DMAbuf Support:          NO
49c49
<       Size:                    16305612(0xf8cdcc) KB              
---
>       Size:                    16306580(0xf8d194) KB              
56c56
<       Size:                    16305612(0xf8cdcc) KB              
---
>       Size:                    16306580(0xf8d194) KB              
63c63
<       Size:                    16305612(0xf8cdcc) KB              
---
>       Size:                    16306580(0xf8d194) KB     
```

Is there any known fix, or is that a bug?

### Operating System

ArchLinux amd64

### CPU

AMD Ryzen 3 2200G with Radeon Vega Graphics

### GPU

gfx803

### ROCm Version

5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

Copy buffer GPU (using PyTorch library)

```python
import torch
t = torch.tensor([0.1, 0.3])
print("cuda")
c = t.cuda() #This line freezes whole process ()
# OR
c = t.to(torch.device('cuda:0'))
# OR
c = t.to('cuda:0')
```

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
  Name:                    AMD Ryzen 3 2200G with Radeon Vega Graphics
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen 3 2200G with Radeon Vega Graphics
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
  Max Clock Freq. (MHz):   3500                               
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
      Size:                    16305612(0xf8cdcc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16305612(0xf8cdcc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16305612(0xf8cdcc) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx803                             
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 560 Series           
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
  Chip ID:                 26607(0x67ef)                      
  ASIC Revision:           1(0x1)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1176                               
  BDFID:                   256                                
  Internal Node ID:        1                                  
  Compute Unit:            14                                 
  SIMDs per CU:            4                                  
  Shader Engines:          2                                  
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
  Packet Processor uCode:: 730                                
  SDMA engine uCode::      58                                 
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
      Name:                    amdgcn-amd-amdhsa--gfx803          
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

Update:
Also on the working LTS kernel, there is still problem with 100% CPU usage (,,only´´ for about 10 seconds, when moving to/from GPU after some chain of mathematical operations). That looks like a problem of sync implementation (using while loop (also without sleep function) eating CPU, instead of some `poll`/`epoll` syscall)

---

## 评论 (8 条)

### 评论 #1 — Artefact2 (2024-02-02T10:30:28Z)

I hit a similar issue with `llama-bench` from llama.cpp. The system doesn't freeze, but a single CPU core is always runnining at 100%. Most of the CPU time is spent in `rocr::core::InterruptSignal::WaitRelaxed(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t)`. Needless to say, this makes the CPU generate a lot of heat and consume extra power for nothing.

I use ROCm 5.7 on Arch Linux, with gfx1030.

---

### 评论 #2 — jin-eld (2024-02-09T21:16:59Z)

I also see a 100% CPU hog and hanging, the backtraces always lead via `roc::DmaBlitManager::hsaCopyStaged ` ending up in `rocr::core::InterruptSignal::WaitRelaxed`

I can reproduce it with the ROCm Validation  Suite with ROCm 6.0.0 on Fedora 40 Rawhide with a gfx900.

The test suite log started to hang here:

```
[RESULT] [  6732.572901] [action_7] babel 24213  Starting the Memory stress test 
Running kernels 5000 times
Precision: double
Array size: 268.4 MB (=0.3 GB)
Total size: 805.3 MB (=0.8 GB)
Using HIP device AMD Radeon Instinct MI25
Driver: 60032830
```

The PyTorch example which was posted by the topic starter does work for me though.

---

### 评论 #3 — jin-eld (2024-02-18T00:22:52Z)

I updated to kernel `6.8.0-0.rc4.20240215git8d3dea210042.38.fc41.x86_64` and now the `rvs` test fails with a coredump:

```
Running kernels 5000 times
Precision: double
Array size: 268.4 MB (=0.3 GB)
Total size: 805.3 MB (=0.8 GB)
Using HIP device AMD Radeon Instinct MI25
Driver: 60032830
Memory access fault by GPU node-1 (Agent handle: 0xf8ab70) on address 0x800008000. Reason: Page not present or supervisor privilege.
Aborted (core dumped)
```

I tried exporting these env vars which I found in some older issue:
```
export HCC_SERIALIZE_KERNEL=0x3
export HCC_SERIALIZE_COPY=0x3
export HIP_TRACE_API=0x2
```

however I did not see more output.

I tried running the test from within `gdb`, but then I end up in the 100% CPU hogging scenario instead of a coredump, interrupting shows:
```
hread 1 "rvs" received signal SIGINT, Interrupt.
0x00007fffb16a5959 in __futex_abstimed_wait_common64 (private=128, 
    cancel=true, abstime=0x0, op=265, expected=1590, futex_word=0x7ffe9f400990)
    at futex-internal.c:57
Downloading source file /usr/src/debug/glibc-2.39-2.fc40.x86_64/nptl/futex-internal.c
57          return INTERNAL_SYSCALL_CANCEL (futex_time64, futex_word, op, expected,
```

I then enabled coredumps and got a backtrace from the core file, I'm attaching it to the issue.
[rvs_coredump_backtrace.txt](https://github.com/ROCm/ROCm/files/14320619/rvs_coredump_backtrace.txt)

I understand that gfx900 / MI25 is no longer supported, however judging by one of the posts above it also happens on a gfx1030. If there is anything I can do, to provide more information or if someone has hints on how to debug this - please tell.

EDIT: I found yet another option `export HSAKMT_DEBUG_LEVEL=7` which leads to more output:

```
[RESULT] [  6987.88931 ] Action name :action_7
[RESULT] [  6987.89877 ] Module name :babel                                     
[INFO  ] [  6987.89901 ] Missing 'device_index' key.                            
[RESULT] [  6987.90024 ] [action_7] babel 24213  Starting the Memory stress test 
Running kernels 5000 times                                                      
Precision: double                                                               
Array size: 268.4 MB (=0.3 GB)                                                  
Total size: 805.3 MB (=0.8 GB)                                                  
Using HIP device AMD Radeon Instinct MI25                                       
Driver: 60032830                                                                
[hsaKmtAllocMemory] node 1                                                      
[hsaKmtMapMemoryToGPUNodes] address 0x7feda9800000 number of nodes 1            
[hsaKmtAllocMemory] node 1                                                      
[hsaKmtMapMemoryToGPUNodes] address 0x7fed99600000 number of nodes 1            
[hsaKmtAllocMemory] node 1                                                      
[hsaKmtMapMemoryToGPUNodes] address 0x7fed89400000 number of nodes 1            
[hsaKmtAllocMemory] node 1                                                      
[hsaKmtMapMemoryToGPUNodes] address 0x7fee43c00000 number of nodes 1            
[hsaKmtAllocMemory] node 1                                                      
[hsaKmtMapMemoryToGPUNodes] address 0x7fef62488000 number of nodes 1            
[hsaKmtAllocMemory] node 0                                                      
bind_mem_to_numa mem 0x7fef621a8000 flags 0x40 size 0x6000 node_id 0            
[hsaKmtMapMemoryToGPUNodes] address 0x7fef621a8000 number of nodes 1            
[hsaKmtQueryPointerInfo] pointer 0x7fee48005aa0                                 
[hsaKmtQueryPointerInfo] pointer 0x7fee48005aa0                                 
[hsaKmtQueryPointerInfo] pointer 0x7fee48005aa0                                 
... message repeats a gazillion times                                           
[hsaKmtQueryPointerInfo] pointer 0x7fee48005aa0                                 
[hsaKmtQueryPointerInfo] pointer 0x7fee48005aa0                                 
Memory exception on virtual address 0x800008000, node id 1 : Page not present   
op get range attrs failed Bad address                                           
Address does not belong to a known buffer                                       
Memory access fault by GPU node-1 (Agent handle: 0x10ceb70) on address 0x800008000. Reason: Page not present or supervisor privilege.
Aborted (core dumped)
```

---

### 评论 #4 — jin-eld (2024-02-18T23:51:12Z)

I kept poking at this, tried out the examples from the HIP-examples repo and basically I can see that any code that is taking the path via `roc::DmaBlitManager::hsaCopyStaged` ends up hanging with 100% CPU, for instance the issue also happens with the `gpu-burn` example, it does not crash but will just hang with 100% CPU.

I came up with a minimal reproducer, I never did any HIP coding before, so I hope the code is valid. It basically allocates a huge chunk of memory on the host and on the GPU, fills it with a pattern on the host, copies it to the GPU and then launches a kernel to test if the pattern still matches.

Interestingly enough the first iteration succeeds, but then on the second iteration it just hangs with 100% CPU. Here is the backtrace when I interrupt it in `gdb`:

```
(gdb) bt
#0  rocr::core::InterruptSignal::WaitRelaxed (this=0x622ab0, 
    condition=HSA_SIGNAL_CONDITION_LT, compare_value=1, 
    timeout=<optimized out>, wait_hint=HSA_WAIT_STATE_ACTIVE)
    at /usr/src/debug/rocm-runtime-6.0.0-3.fc40.x86_64/src/core/runtime/interrupt_signal.cpp:217
#1  0x00007ffff545cb4e in rocr::core::InterruptSignal::WaitAcquire (
    this=<optimized out>, condition=<optimized out>, 
    compare_value=<optimized out>, timeout=<optimized out>, 
    wait_hint=<optimized out>)
    at /usr/src/debug/rocm-runtime-6.0.0-3.fc40.x86_64/src/core/runtime/interrupt_signal.cpp:251
#2  0x00007ffff544c93f in rocr::HSA::hsa_signal_wait_scacquire (
    hsa_signal=..., condition=<optimized out>, compare_value=<optimized out>, 
    timeout_hint=<optimized out>, wait_state_hint=<optimized out>)
    at /usr/src/debug/rocm-runtime-6.0.0-3.fc40.x86_64/src/core/runtime/hsa.cpp:1220
#3  0x00007ffff6b0e11b in roc::WaitForSignal<false> (forced_wait=false, 
    active_wait=<optimized out>, signal=...)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocvirtual.hpp:70
#4  roc::VirtualGPU::HwQueueTracker::CpuWaitForSignal (this=<optimized out>, 
    signal=0x622a10)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocvirtual.cpp:558
#5  0x00007ffff6b3580e in roc::VirtualGPU::HwQueueTracker::WaitCurrent (
    this=<optimized out>)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocvirtual.hpp:240
#6  roc::DmaBlitManager::hsaCopyStaged (this=this@entry=0x40efe0, 
    hostSrc=hostSrc@entry=0x7fffffffd578 "", hostDst=0x7ffee3a00000 "", 
    size=<optimized out>, size@entry=4, staging=0x7ffee8300000 "", 
    hostToDev=hostToDev@entry=true)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocblit.cpp:808
#7  0x00007ffff6b36455 in roc::DmaBlitManager::writeMemoryStaged (xferSize=4, 
    totalSize=<synthetic pointer>: <optimized out>, 
    offset=<synthetic pointer>: <optimized out>, origin=<optimized out>, 
    xferBuf=..., dstMemory=..., srcHost=0x7fffffffd578, this=0x40efe0)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocblit.cpp:229
#8  roc::DmaBlitManager::writeBuffer (this=0x40efe0, srcHost=<optimized out>, 
    dstMemory=..., origin=..., size=..., entire=<optimized out>, 
--Type <RET> for more, q to quit, c to continue without paging--
    copyMetadata=...)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocblit.cpp:314
#9  0x00007ffff6b389b0 in roc::KernelBlitManager::writeBuffer (
    this=this@entry=0x40efe0, srcHost=srcHost@entry=0x7fffffffd578, 
    dstMemory=..., origin=..., size=..., entire=<optimized out>, 
    copyMetadata=...)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocblit.cpp:1944
#10 0x00007ffff6b1164b in roc::VirtualGPU::submitWriteMemory (this=0x577460, 
    cmd=...)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/device/rocm/rocvirtual.cpp:1705
#11 0x00007ffff6aedcf4 in amd::Command::enqueue (this=0xa5ef70)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/rocclr/platform/command.cpp:391
#12 0x00007ffff699f7d6 in ihipMemcpy (dst=dst@entry=0x7ffee3a00000, 
    src=src@entry=0x7fffffffd578, sizeBytes=sizeBytes@entry=4, 
    kind=kind@entry=hipMemcpyHostToDevice, stream=..., 
    isHostAsync=isHostAsync@entry=false, isGPUAsync=true)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/hipamd/src/hip_memory.cpp:522
#13 0x00007ffff69a53d2 in hipMemcpy_common (stream=0x0, 
    kind=hipMemcpyHostToDevice, sizeBytes=4, src=0x7fffffffd578, 
    dst=0x7ffee3a00000)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/hipamd/src/hip_memory.cpp:657
#14 hipMemcpy_common (stream=0x0, kind=hipMemcpyHostToDevice, sizeBytes=4, 
    src=0x7fffffffd578, dst=0x7ffee3a00000)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/hipamd/src/hip_memory.cpp:643
#15 hipMemcpy (dst=<optimized out>, src=<optimized out>, 
    sizeBytes=<optimized out>, kind=hipMemcpyHostToDevice)
    at /usr/src/debug/rocclr-6.0.0-3.fc40.x86_64/hipamd/src/hip_memory.cpp:662
#16 0x0000000000401523 in runtest () at memtest.cpp:99
#17 0x0000000000401776 in main () at memtest.cpp:169
```

Rename to `memtest.cpp`, I had to add the `.txt` extension so that github would accept the attachment: 
[memtest.cpp.txt](https://github.com/ROCm/ROCm/files/14324937/memtest.cpp.txt)


---

### 评论 #5 — jin-eld (2024-02-26T00:18:52Z)

I installed Fedora 39 in a docker container (host is running Rawhide/Fedora 40) and checked with ROCm 5.7.1, the problem is **not** present there, both, the validation suite as well as my test program work just fine there. I also tried compiling ROCm 6.0.0 for Fedora 39 and updating ROCm in the same container and I was immediately able to reproduce the problem. It seems it's not a kernel/driver issue, but something in userspace.

```
$ ./rvs -d 3 -c conf/babel.conf 
[RESULT] [  3920.504831] Action name :action_1
[RESULT] [  3920.505461] Module name :babel
[INFO  ] [  3920.505483] Missing 'device_index' key.
Running kernels 5000 times
Precision: double
Array size: 268.4 MB (=0.3 GB)
Total size: 805.3 MB (=0.8 GB)
Using HIP device AMD Radeon Instinct MI25
Driver: 50731921
Function    MBytes/sec  Min (sec)   Max         Average     
Copy :      387715.009  0.00138     0.00165     0.00151 
```

So, this seems to be a regression in ROCm 6.0.0

Could perhaps someone familiar with the codebase give at least some hints on where to look? I am trying to go through the changes between 5.7.1 and 6.0.0, but being unfamiliar with what's going on I am somewhat lost.



---

### 评论 #6 — ppanchad-amd (2024-05-17T17:41:21Z)

@jin-eld Can you please test with ROCm 6.1.1 and see if it still occurs? Thanks!

---

### 评论 #7 — jin-eld (2024-05-17T18:20:38Z)

@ppanchad-amd OK, but it will take a while since I will have to compile ROCm 6.1.1 myself, back then 5.7.1 and 6.0.0 were packaged in Fedora 39 and Rawhide pre-40, so it was easy to switch between the docker images. I'll get back to you once I managed to do it.

---

### 评论 #8 — jin-eld (2024-05-25T20:24:33Z)

@ppanchad-amd I was lucky, ROCm 6.1.1 has recently made it into Rawhide 41, so did not have to recompile anything myself, but was able to retest with a docker image. I can confirm that the freeze is now gone and that my test application now runs without errors. The `HSA_ENABLE_SDMA=0` setting is no longer required.

Tested on an Instinct MI25 / ROCm 6.1.1 / Fedora Rawhide 41

Thank you for fixing this!

---
