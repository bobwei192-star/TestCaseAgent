# [Feature]: Xen-HVM Environment Support

> **Issue #4259**
> **状态**: closed
> **创建时间**: 2025-01-14T20:41:27Z
> **更新时间**: 2025-02-04T14:45:11Z
> **关闭时间**: 2025-02-04T02:43:04Z
> **作者**: rsta79
> **标签**: Feature Request, Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4259

## 标签

- **Feature Request** (颜色: #fbca04)
- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

Adding support to ~Xen-HVM~(QubesOS) environment with GPU passthrough. btw, CUDA seems can works well in ~Xen-HVM~(QubesOS) . ~and right now ROCm can only works in QEMU/KVM and VMWare ESXi.~

Related: #4253 #4254 

### Operating System

QubesOS, ~XCP-ng~

### GPU

AMD Radeon RX7800XT

### ROCm Component

ROCm

Edit: Correct information

---

## 评论 (7 条)

### 评论 #1 — rsta79 (2025-01-15T08:25:12Z)

Short update: the [terminal hangs issue](#4253) seems to be caused by libhsa-runtime.

```
Starting program: /home/user/whisper/venv/bin/python main.py
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7ffd9ffff6c0 (LWP 2572)]
[New Thread 0x7ffd9f7fe6c0 (LWP 2573)]
[New Thread 0x7ffd9affd6c0 (LWP 2574)]
[New Thread 0x7ffd9a7fc6c0 (LWP 2575)]
[New Thread 0x7ffd97ffb6c0 (LWP 2576)]
[New Thread 0x7ffd957fa6c0 (LWP 2577)]
[New Thread 0x7ffd92ff96c0 (LWP 2578)]
[New Thread 0x7ffd907f86c0 (LWP 2579)]
[New Thread 0x7ffd8dff76c0 (LWP 2580)]
[New Thread 0x7ffd8b7f66c0 (LWP 2581)]
[New Thread 0x7ffd88ff56c0 (LWP 2582)]
[New Thread 0x7ffd7b5ff6c0 (LWP 2583)]
[New Thread 0x7ffc7abff6c0 (LWP 2584)]
[Thread 0x7ffc7abff6c0 (LWP 2584) exited]
/home/user/whisper/venv/lib/python3.11/site-packages/whisper/__init__.py:150: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  checkpoint = torch.load(fp, map_location=device)
^C
Thread 1 "python" received signal SIGINT, Interrupt.
0x00007ffe69a63067 in rocr::core::InterruptSignal::WaitRelaxed(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /home/user/whisper/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so

```

---

### 评论 #2 — rsta79 (2025-01-15T18:25:12Z)

Update: after hours of testing, ROCm seems to be working in Xen, the issue might not be the compatibility, but the CPU scheduling. again, not sure if its Xen's or the ROCm's . single vCPU core in the VM goes 100% when I starting to call ROCm (both in hashcat, pytorch). and the GPU usage spike every few seconds, I believe that CPU bottleneck is the real issue. btw, Xen will disable CPU hyper-threading for security reasons. not sure if it's related.

Not sure how to fix it, but yeah, at least it's working. even though right now it's exact opposite of accelerate. the performance is much much much worse than just using CPU.

the heating issue might be caused by the kernel version. probably the debian-12 kernel (Linux 6.1) is too old for my GPU. Linux Kernel 6.1 is released in 2022 Dec. early before RX7800XT is released, and using archlinux template in QubesOS fixed the heating issue.

---

### 评论 #3 — tcgu-amd (2025-01-17T16:18:54Z)

@rsta79, thanks for the update! Glad it is working at least! I am curious what changes did you make to get it to work?

> Single vCPU core in the VM goes 100% when I starting to call ROCm (both in hashcat, pytorch). and the GPU usage spike every few seconds, I believe that CPU bottleneck is the real issue. btw, Xen will disable CPU hyper-threading for security reasons. not sure if it's related.

This indeed sounds like the workload is being bottlenecked by the vCPU. The single core going to 100% is likely the only one being used, and the GPU spikes is probably a sign that it is being bottlenecked. 

It is hard to tell what the issue might be, but if  torch/hashcat has no issue working without ROCm, then it is likely that something down the stack of ROCm is being blocked from spawning more threads due to XVM specific configurations.

By the way, it might be useful to set AMD_LOG_LEVEL=5 in you environment to enable verbose logs from HSA runtime for debugging. 

Hope this helps. Thanks!

---

### 评论 #4 — rsta79 (2025-01-17T20:18:52Z)

> [@rsta79](https://github.com/rsta79), thanks for the update! Glad it is working at least! I am curious what changes did you make to get it to work?

@tcgu-amd, I only switch to archlinux template, which provides bleeding-edge kernels. just to see if its something related to the kernel. 

and It's not actually _working_. it did occupying GPU but takes forever to finish. and now, it's looks like an existing issue #2715. I got almost same stacks in gdb when running pytorch. and the backtraces suggest it might be issue related with signal locks in `CopyHostToDevice` command? probably it's spinning to waiting for interrupt signal so the CPU goes 100%? debugging on such huge stack is driving me insane. However, thank you guys for the hard works on ROCm stacks! 

pytorch/examples/mnist stacks:
```
(gdb) bt
#0  0x00007ffe69463051 in rocr::core::InterruptSignal::WaitRelaxed(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#1  0x00007ffe69462eba in rocr::core::InterruptSignal::WaitAcquire(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#2  0x00007ffe69458f19 in rocr::HSA::hsa_signal_wait_scacquire(hsa_signal_s, hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#3  0x00007ffe69430c10 in rocr::AMD::BlitKernel::SubmitLinearCopyCommand(void*, void const*, unsigned long) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#4  0x00007ffe6944e4af in rocr::(anonymous namespace)::RegionMemory::Freeze() () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#5  0x00007ffe694a1dc4 in rocr::amd::hsa::loader::Segment::Freeze() [clone .part.0] () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#6  0x00007ffe694a1e36 in rocr::amd::hsa::loader::ExecutableImpl::Freeze(char const*) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#7  0x00007ffe694a1586 in rocr::amd::hsa::loader::AmdHsaCodeLoader::FreezeExecutable(rocr::amd::hsa::loader::Executable*, char const*) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#8  0x00007ffe6945b938 in rocr::HSA::hsa_executable_freeze(hsa_executable_s, char const*) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
#9  0x00007fff47ba4460 in roctracer::hsa_support::(anonymous namespace)::ExecutableFreezeIntercept(hsa_executable_s, char const*) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libroctracer64.so
#10 0x00007fff47bae33c in roctracer::hsa_support::detail::hsa_executable_freeze_callback(hsa_executable_s, char const*) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libroctracer64.so
#11 0x00007fff47f57fd9 in amd::roc::LightningProgram::setKernels(void*, unsigned long, int, unsigned long, std::basic_string<char, std::char_traits<char>, std::allocator<char> >) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#12 0x00007fff47f10443 in amd::device::Program::loadLC() () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#13 0x00007fff47f104af in amd::device::Program::load() () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#14 0x00007fff47f3d87f in amd::Program::load(std::vector<amd::Device*, std::allocator<amd::Device*> > const&) ()
--Type <RET> for more, q to quit, c to continue without paging--
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#15 0x00007fff47f0dc23 in amd::Device::BlitProgram::create(amd::Device*, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#16 0x00007fff47f48aba in amd::roc::Device::createBlitProgram() () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#17 0x00007fff47f96f50 in amd::roc::KernelBlitManager::createProgram(amd::roc::Device&) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#18 0x00007fff47f65e1d in amd::roc::VirtualGPU::create() () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#19 0x00007fff47f483e9 in amd::roc::Device::createVirtualDevice(amd::CommandQueue*) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#20 0x00007fff47f35b2a in amd::HostQueue::HostQueue(amd::Context&, amd::Device&, unsigned long, unsigned int, amd::CommandQueue::Priority, std::vector<unsigned int, std::allocator<unsigned int> > const&) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#21 0x00007fff47e80618 in hip::Stream::Stream(hip::Device*, hip::Stream::Priority, unsigned int, bool, std::vector<unsigned int, std::allocator<unsigned int> > const&, hipStreamCaptureStatus) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#22 0x00007fff47ce77c4 in hip::Device::NullStream(bool) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#23 0x00007fff47de4612 in hip::hipMemcpyWithStream(void*, void const*, unsigned long, hipMemcpyKind, ihipStream_t*) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libamdhip64.so
#24 0x00007fffa0dd52b6 in at::native::copy_kernel_cuda(at::TensorIterator&, bool) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_hip.so
#25 0x00007fffe1a6a313 in at::native::copy_impl(at::Tensor&, at::Tensor const&, bool) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#26 0x00007fffe1a6bcb2 in at::native::copy_(at::Tensor&, at::Tensor const&, bool) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#27 0x00007fffe2832ebc in at::_ops::copy_::call(at::Tensor&, at::Tensor const&, bool) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#28 0x00007fffe1d90729 in at::native::_to_copy(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#29 0x00007fffe2bd8ecb in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd___to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::opt--Type <RET> for more, q to quit, c to continue without paging--
ional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#30 0x00007fffe22d2f65 in at::_ops::_to_copy::redispatch(c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#31 0x00007fffe2a16b23 in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>), &at::(anonymous namespace)::_to_copy>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#32 0x00007fffe22d2f65 in at::_ops::_to_copy::redispatch(c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#33 0x00007fffe47d251f in torch::autograd::VariableType::(anonymous namespace)::_to_copy(c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#34 0x00007fffe47d295e in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>), &torch::autograd::VariableType::(anonymous namespace)::_to_copy>, at::Tensor, c10::guts::typelist::typelist<c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
--Type <RET> for more, q to quit, c to continue without paging--
#35 0x00007fffe23629cb in at::_ops::_to_copy::call(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#36 0x00007fffe1d8bcad in at::native::to(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#37 0x00007fffe2ddff61 in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeImplicitAutograd_dtype_layout_to>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat> > >, at::Tensor (at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#38 0x00007fffe2513710 in at::_ops::to_dtype_layout::call(at::Tensor const&, std::optional<c10::ScalarType>, std::optional<c10::Layout>, std::optional<c10::Device>, std::optional<bool>, bool, bool, std::optional<c10::MemoryFormat>) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_cpu.so
#39 0x00007ffff5590f3b in torch::autograd::dispatch_to(at::Tensor const&, c10::Device, bool, bool, std::optional<c10::MemoryFormat>) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_python.so
#40 0x00007ffff55e5557 in torch::autograd::THPVariable_to(_object*, _object*, _object*) () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libtorch_python.so
#41 0x00007ffff7961aaf in method_vectorcall_VARARGS_KEYWORDS (func=0x7ffff6c5f560, args=0x7ffff7fb4508, nargsf=<optimized out>, kwnames=<optimized out>) at Objects/descrobject.c:364
#42 0x00007ffff7954363 in _PyObject_VectorcallTstate (tstate=0x7ffff7d96698 <_PyRuntime+166328>, callable=0x7ffff6c5f560, args=<optimized out>, nargsf=<optimized out>, 
    kwnames=<optimized out>) at ./Include/internal/pycore_call.h:92
#43 PyObject_Vectorcall (callable=0x7ffff6c5f560, args=<optimized out>, nargsf=<optimized out>, kwnames=<optimized out>) at Objects/call.c:299
#44 0x00007ffff7a5e579 in _PyEval_EvalFrameDefault (tstate=0x7ffff7d96698 <_PyRuntime+166328>, frame=0x7ffff7fb4488, throwflag=0) at Python/ceval.c:4769
#45 0x00007ffff7a64e60 in _PyEval_EvalFrame (tstate=0x7ffff7d96698 <_PyRuntime+166328>, frame=0x7ffff7fb4020, throwflag=0) at ./Include/internal/pycore_ceval.h:73
#46 _PyEval_Vector (args=0x0, argcount=0, kwnames=0x0, tstate=0x7ffff7d96698 <_PyRuntime+166328>, func=0x7ffff70116c0, locals=0x7ffff71f2b80) at Python/ceval.c:6434
--Type <RET> for more, q to quit, c to continue without paging--
#47 PyEval_EvalCode (co=co@entry=0x7ffff7144310, globals=globals@entry=0x7ffff71f2b80, locals=locals@entry=0x7ffff71f2b80) at Python/ceval.c:1148
#48 0x00007ffff7aaf82d in run_eval_code_obj (tstate=0x7ffff7d96698 <_PyRuntime+166328>, co=0x7ffff7144310, globals=0x7ffff71f2b80, locals=0x7ffff71f2b80) at Python/pythonrun.c:1741
#49 run_mod (mod=<optimized out>, filename=filename@entry=0x7ffff71523d0, globals=globals@entry=0x7ffff71f2b80, locals=locals@entry=0x7ffff71f2b80, flags=flags@entry=0x7fffffffe318, 
    arena=arena@entry=0x7ffff711b7b0) at Python/pythonrun.c:1762
#50 0x00007ffff7ab117c in pyrun_file (fp=0x55555557f2d0, filename=0x7ffff71523d0, start=257, globals=0x7ffff71f2b80, locals=0x7ffff71f2b80, closeit=1, flags=0x7fffffffe318)
    at Python/pythonrun.c:1657
#51 _PyRun_SimpleFileObject (fp=fp@entry=0x55555557f2d0, filename=filename@entry=0x7ffff71523d0, closeit=closeit@entry=1, flags=flags@entry=0x7fffffffe318) at Python/pythonrun.c:440
#52 0x00007ffff7ab17cc in _PyRun_AnyFileObject (fp=0x55555557f2d0, filename=filename@entry=0x7ffff71523d0, closeit=closeit@entry=1, flags=flags@entry=0x7fffffffe318)
    at Python/pythonrun.c:79
#53 0x00007ffff7ad2d30 in pymain_run_file_obj (program_name=0x7ffff71fb4b0, filename=0x7ffff71523d0, skip_source_first_line=0) at Modules/main.c:360
#54 pymain_run_file (config=0x7ffff7d7c6e0 <_PyRuntime+59904>) at Modules/main.c:379
#55 pymain_run_python (exitcode=0x7fffffffe314) at Modules/main.c:605
#56 Py_RunMain () at Modules/main.c:684
#57 0x00007ffff7ad3306 in pymain_main (args=0x7fffffffe430) at Modules/main.c:714
#58 Py_BytesMain (argc=<optimized out>, argv=<optimized out>) at Modules/main.c:738
#59 0x00007ffff7634e08 in __libc_start_call_main (main=main@entry=0x555555555040 <main>, argc=argc@entry=2, argv=argv@entry=0x7fffffffe5c8)
    at ../sysdeps/nptl/libc_start_call_main.h:58
#60 0x00007ffff7634ecc in __libc_start_main_impl (main=0x555555555040 <main>, argc=2, argv=0x7fffffffe5c8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, 
    stack_end=0x7fffffffe5b8) at ../csu/libc-start.c:360
#61 0x0000555555555075 in _start ()
(gdb) 
(gdb) info threads
  Id   Target Id                                 Frame 
* 1    Thread 0x7ffff7eb6b80 (LWP 2613) "python" 0x00007ffe69463051 in rocr::core::InterruptSignal::WaitRelaxed(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
   from /home/user/venv/lib/python3.11/site-packages/torch/lib/libhsa-runtime64.so
  2    Thread 0x7ffd9f9ff6c0 (LWP 2620) "python" 0x00007ffff769fa19 in __futex_abstimed_wait_common64 (private=0, futex_word=0x7ffda23cade0 <thread_status+96>, expected=0, op=393, 
    abstime=0x0, cancel=true) at futex-internal.c:57
  3    Thread 0x7ffd9f1fe6c0 (LWP 2621) "python" 0x00007ffff769fa19 in __futex_abstimed_wait_common64 (private=0, futex_word=0x7ffda23cae60 <thread_status+224>, expected=0, op=393, 
    abstime=0x0, cancel=true) at futex-internal.c:57
  4    Thread 0x7ffd9a7ff6c0 (LWP 2622) "python" 0x00007ffff769fa19 in __futex_abstimed_wait_common64 (private=0, futex_word=0x7ffda23caee0 <thread_status+352>, expected=0, op=393, 
    abstime=0x0, cancel=true) at futex-internal.c:57
  5    Thread 0x7ffd97dff6c0 (LWP 2623) "python" 0x00007ffff769fa19 in __futex_abstimed_wait_common64 (private=0, futex_word=0x7ffda23caf60 <thread_status+480>, expected=0, op=393, 
    abstime=0x0, cancel=true) at futex-internal.c:57
  6    Thread 0x7ffd953ff6c0 (LWP 2624) "python" 0x00007ffff769fa19 in __futex_abstimed_wait_common64 (private=0, futex_word=0x7ffda23cafe0 <thread_status+608>, expected=0, op=393, 
    abstime=0x0, cancel=true) at futex-internal.c:57
  7    Thread 0x7ffd929ff6c0 (LWP 2625) "python" 0x00007ffff769fa19 in __futex_abstimed_wait_common64 (private=0, futex_word=0x7ffda23cb060 <thread_status+736>, expected=0, op=393, 
    abstime=0x0, cancel=true) at futex-internal.c:57
  8    Thread 0x7ffd921fe6c0 (LWP 2626) "python" 0x00007ffff769fa19 in __futex_abstimed_wait_common64 (private=0, futex_word=0x7ffda23cb0e0 <thread_status+864>, expected=0, op=393, 
    abstime=0x0, cancel=true) at futex-internal.c:57
  9    Thread 0x7ffd805ff6c0 (LWP 2627) "python" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
  11   Thread 0x7ffc7e9ff6c0 (LWP 2629) "python" 0x00007ffff6818b31 in ?? () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libgomp.so
  12   Thread 0x7ffc7e1fe6c0 (LWP 2630) "python" 0x00007ffff6818b31 in ?? () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libgomp.so
  13   Thread 0x7ffc7d9fd6c0 (LWP 2631) "python" 0x00007ffff6818b31 in ?? () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libgomp.so
  14   Thread 0x7ffc7d1fc6c0 (LWP 2632) "python" 0x00007ffff6818b31 in ?? () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libgomp.so
  15   Thread 0x7ffc7c9fb6c0 (LWP 2633) "python" 0x00007ffff6818b31 in ?? () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libgomp.so
--Type <RET> for more, q to quit, c to continue without paging--
  16   Thread 0x7ffc77fff6c0 (LWP 2634) "python" 0x00007ffff6818b31 in ?? () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libgomp.so
  17   Thread 0x7ffc777fe6c0 (LWP 2635) "python" 0x00007ffff6818b31 in ?? () from /home/user/venv/lib/python3.11/site-packages/torch/lib/libgomp.so
(gdb) 

```

hashcat stacks: 
```
(gdb) r
Starting program: /usr/bin/hashcat --benchmark
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
hashcat (v6.2.6) starting in benchmark mode

Benchmarking uses hand-optimized kernel code by default.
You can use it in your cracking session by setting the -O option.
Note: Using optimized kernel code limits the maximum supported password length.
To disable the optimized kernel code in benchmark mode, use the -w option.

:3:rocdevice.cpp            :468 : 3326407335 us: [pid:2539  tid:0x7ffff7e53740] Initializing HSA stack.
[New Thread 0x7fffd41ff6c0 (LWP 2542)]
[New Thread 0x7fffd39fe6c0 (LWP 2543)]
:3:rocdevice.cpp            :554 : 3326422269 us: [pid:2539  tid:0x7ffff7e53740] Enumerated GPU agents = 1
:3:rocdevice.cpp            :232 : 3326422304 us: [pid:2539  tid:0x7ffff7e53740] Numa selects cpu agent[0]=0x555555588800(fine=0x5555555872a0,coarse=0x555555688400) for gpu agent=0x555555688800 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :290 : 3326422315 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:comgrctx.cpp             :33  : 3326422326 us: [pid:2539  tid:0x7ffff7e53740] Loading COMGR library.
:3:comgrctx.cpp             :126 : 3326422353 us: [pid:2539  tid:0x7ffff7e53740] Loaded COMGR library version 2.8.
[Thread 0x7fffd39fe6c0 (LWP 2543) exited]
:3:rocdevice.cpp            :1809: 3326422514 us: [pid:2539  tid:0x7ffff7e53740] Gfx Major/Minor/Stepping: 11/0/1
:3:rocdevice.cpp            :1811: 3326422520 us: [pid:2539  tid:0x7ffff7e53740] HMM support: 1, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1813: 3326422522 us: [pid:2539  tid:0x7ffff7e53740] Max SDMA Read Mask: 0x3, Max SDMA Write Mask: 0x3
:4:rocdevice.cpp            :2221: 3326422764 us: [pid:2539  tid:0x7ffff7e53740] Allocate hsa host memory 0x7fffd3000000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2221: 3326427127 us: [pid:2539  tid:0x7ffff7e53740] Allocate hsa host memory 0x7fffd2e00000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2221: 3326431876 us: [pid:2539  tid:0x7ffff7e53740] Allocate hsa host memory 0x7fffd2800000, size 0x400000, numa_node = 0
:4:rocdevice.cpp            :2221: 3326432227 us: [pid:2539  tid:0x7ffff7e53740] Allocate hsa host memory 0x7ffff7fbb000, size 0x38, numa_node = 0
:4:runtime.cpp              :85  : 3326433181 us: [pid:2539  tid:0x7ffff7e53740] init
:3:hip_context.cpp          :49  : 3326433205 us: [pid:2539  tid:0x7ffff7e53740] Direct Dispatch: 1
:3:hip_context.cpp          :268 : 3326433232 us: [pid:2539  tid:0x7ffff7e53740]  hipDriverGetVersion ( 0x7fffffffe3e0 ) 
:3:hip_context.cpp          :277 : 3326433267 us: [pid:2539  tid:0x7ffff7e53740] hipDriverGetVersion: Returned hipSuccess : 
:3:hip_context.cpp          :200 : 3326433298 us: [pid:2539  tid:0x7ffff7e53740]  hipRuntimeGetVersion ( 0x7fffffffe3dc ) 
:3:hip_context.cpp          :209 : 3326433325 us: [pid:2539  tid:0x7ffff7e53740] hipRuntimeGetVersion: Returned hipSuccess : 
:3:hip_context.cpp          :139 : 3326436913 us: [pid:2539  tid:0x7ffff7e53740]  hipInit ( 0 ) 
:3:hip_context.cpp          :145 : 3326436947 us: [pid:2539  tid:0x7ffff7e53740] hipInit: Returned hipSuccess : 
:3:rocdevice.cpp            :468 : 3326487714 us: [pid:2539  tid:0x7ffff7e53740] Initializing HSA stack.
:3:rocdevice.cpp            :554 : 3326488618 us: [pid:2539  tid:0x7ffff7e53740] Enumerated GPU agents = 1
:3:rocdevice.cpp            :232 : 3326488650 us: [pid:2539  tid:0x7ffff7e53740] Numa selects cpu agent[0]=0x555555588800(fine=0x5555555872a0,coarse=0x555555688400) for gpu agent=0x555555688800 CPU<->GPU XGMI=0
:3:rocsettings.cpp          :290 : 3326488662 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:comgrctx.cpp             :126 : 3326488673 us: [pid:2539  tid:0x7ffff7e53740] Loaded COMGR library version 2.8.
:3:rocdevice.cpp            :1809: 3326488768 us: [pid:2539  tid:0x7ffff7e53740] Gfx Major/Minor/Stepping: 11/0/1
:3:rocdevice.cpp            :1811: 3326488778 us: [pid:2539  tid:0x7ffff7e53740] HMM support: 1, XNACK: 0, Direct host access: 0
:3:rocdevice.cpp            :1813: 3326488784 us: [pid:2539  tid:0x7ffff7e53740] Max SDMA Read Mask: 0x3, Max SDMA Write Mask: 0x3
:4:rocdevice.cpp            :2221: 3326489049 us: [pid:2539  tid:0x7ffff7e53740] Allocate hsa host memory 0x7fffd2600000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2221: 3326493183 us: [pid:2539  tid:0x7ffff7e53740] Allocate hsa host memory 0x7fffd2400000, size 0x101000, numa_node = 0
:4:rocdevice.cpp            :2221: 3326497667 us: [pid:2539  tid:0x7ffff7e53740] Allocate hsa host memory 0x7fffd1e00000, size 0x400000, numa_node = 0
:3:rocsettings.cpp          :290 : 3326497924 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326497956 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326497966 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326497991 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326497999 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498024 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498031 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498055 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498063 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498087 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498095 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498119 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498126 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498151 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498158 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498182 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498190 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498214 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498222 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498246 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498254 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498278 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498285 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498309 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498317 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498341 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498348 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498372 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498380 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498404 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498412 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498436 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498444 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498468 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498476 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498500 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498507 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498530 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498539 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498562 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498571 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498595 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498602 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498626 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498634 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498658 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498667 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498673 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498698 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498705 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498729 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498737 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498761 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498769 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498793 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498800 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498824 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498832 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498856 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498864 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498888 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498895 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498920 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498927 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498952 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498959 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 2
:3:rocsettings.cpp          :290 : 3326498984 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326498992 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499016 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499024 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499048 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499055 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499079 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499087 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499111 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499119 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499143 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499150 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499174 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499182 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499206 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499213 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499246 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499270 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499278 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499303 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499310 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499333 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499342 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499369 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499376 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499400 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499408 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499432 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:3:rocsettings.cpp          :290 : 3326499440 us: [pid:2539  tid:0x7ffff7e53740] Using dev kernel arg wa = 0
:4:runtime.cpp              :85  : 3326499464 us: [pid:2539  tid:0x7ffff7e53740] init
:3:hip_device_runtime.cpp   :651 : 3326499535 us: [pid:2539  tid:0x7ffff7e53740]  hipGetDeviceCount ( 0x7fffffffe334 ) 
:3:hip_device_runtime.cpp   :653 : 3326499581 us: [pid:2539  tid:0x7ffff7e53740] hipGetDeviceCount: Returned hipSuccess : 
:3:hip_device.cpp           :333 : 3326499608 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGet ( 0x7fffffffe398, 0 ) 
:3:hip_device.cpp           :335 : 3326499633 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGet: Returned hipSuccess : 
:3:hip_device.cpp           :398 : 3326499687 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetName ( 0x5555556ed1c0, 4096, 0 ) 
:3:hip_device.cpp           :418 : 3326499718 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetName: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499726 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe390, 63, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326499754 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device.cpp           :339 : 3326499762 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceTotalMem ( 0x7fffffffe3b8, 0 ) 
:3:hip_device.cpp           :354 : 3326499788 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceTotalMem: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499795 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe388, 87, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326499822 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499829 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe380, 23, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326499855 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499862 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe378, 61, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326499888 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499894 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe374, 56, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326499921 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499928 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe370, 5, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326499955 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499961 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe36c, 67, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326499988 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326499994 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe368, 68, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326500020 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326500027 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe364, 18, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326500053 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326500059 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe360, 87, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326500085 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326500092 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe35c, 74, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326500118 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_device_runtime.cpp   :161 : 3326500125 us: [pid:2539  tid:0x7ffff7e53740]  hipDeviceGetAttribute ( 0x7fffffffe358, 83, 0 ) 
:3:hip_device_runtime.cpp   :452 : 3326500151 us: [pid:2539  tid:0x7ffff7e53740] hipDeviceGetAttribute: Returned hipSuccess : 
:3:hip_context.cpp          :149 : 3326500159 us: [pid:2539  tid:0x7ffff7e53740]  hipCtxCreate ( 0x7fffffffe3b0, 4, 0 ) 
:3:hip_context.cpp          :162 : 3326500185 us: [pid:2539  tid:0x7ffff7e53740] hipCtxCreate: Returned hipSuccess : 
:3:hip_context.cpp          :254 : 3326500208 us: [pid:2539  tid:0x7ffff7e53740]  hipCtxPushCurrent ( context:0x555555587fe0 ) 
:3:hip_context.cpp          :264 : 3326500218 us: [pid:2539  tid:0x7ffff7e53740] hipCtxPushCurrent: Returned hipSuccess : 
:3:hip_memory.cpp           :793 : 3326500247 us: [pid:2539  tid:0x7ffff7e53740]  hipMemGetInfo ( 0x7fffffffe3a8, 0x7fffffffe3a0 ) 
:3:hip_memory.cpp           :817 : 3326500277 us: [pid:2539  tid:0x7ffff7e53740] hipMemGetInfo: Returned hipSuccess : 
:3:hip_context.cpp          :237 : 3326500285 us: [pid:2539  tid:0x7ffff7e53740]  hipCtxPopCurrent ( 0x7fffffffe3b0 ) 
:3:hip_context.cpp          :250 : 3326500307 us: [pid:2539  tid:0x7ffff7e53740] hipCtxPopCurrent: Returned hipSuccess : 
:3:hip_context.cpp          :213 : 3326500315 us: [pid:2539  tid:0x7ffff7e53740]  hipCtxDestroy ( context:0x555555587fe0 ) 
:3:hip_context.cpp          :233 : 3326500341 us: [pid:2539  tid:0x7ffff7e53740] hipCtxDestroy: Returned hipSuccess : 
[New Thread 0x7fffd1dff6c0 (LWP 2544)]
[Thread 0x7fffd1dff6c0 (LWP 2544) exited]
[New Thread 0x7fffd49786c0 (LWP 2545)]
:3:rocdevice.cpp            :3026: 3326501680 us: [pid:2539  tid:0x7fffd49786c0] Number of allocated hardware queues with low priority: 0, with normal priority: 0, with high priority: 0, maximum per priority is: 4
[New Thread 0x7fffd1dff6c0 (LWP 2546)]
:3:rocdevice.cpp            :3104: 3326522300 us: [pid:2539  tid:0x7fffd49786c0] Created SWq=0x7fffe01ac000 to map on HWq=0x7fffd1400000 with size 16384 with priority 1, cooperative: 0
:3:rocdevice.cpp            :3197: 3326522331 us: [pid:2539  tid:0x7fffd49786c0] acquireQueue refCount: 0x7fffd1400000 (1)
:4:rocdevice.cpp            :2221: 3326522532 us: [pid:2539  tid:0x7fffd49786c0] Allocate hsa host memory 0x7fffd1200000, size 0x100000, numa_node = 0
:3:devprogram.cpp           :2648: 3326723158 us: [pid:2539  tid:0x7fffd49786c0] Using Code Object V5.
^C
Thread 1 "hashcat" received signal SIGINT, Interrupt.
0x00007ffff7a9fa19 in __futex_abstimed_wait_common64 (private=<optimized out>, futex_word=0x5555556f5808, expected=0, op=393, abstime=0x7fffffffdfe0, cancel=true)
    at futex-internal.c:57
57	    return INTERNAL_SYSCALL_CANCEL (futex_time64, futex_word, op, expected,
(gdb) bt
#0  0x00007ffff7a9fa19 in __futex_abstimed_wait_common64 (private=<optimized out>, futex_word=0x5555556f5808, expected=0, op=393, abstime=0x7fffffffdfe0, cancel=true)
    at futex-internal.c:57
#1  __futex_abstimed_wait_common (futex_word=futex_word@entry=0x5555556f5808, expected=expected@entry=0, clockid=clockid@entry=0, abstime=abstime@entry=0x7fffffffdfe0, 
    private=<optimized out>, cancel=cancel@entry=true) at futex-internal.c:87
#2  0x00007ffff7a9fa9f in __GI___futex_abstimed_wait_cancelable64 (futex_word=futex_word@entry=0x5555556f5808, expected=expected@entry=0, clockid=clockid@entry=0, 
    abstime=abstime@entry=0x7fffffffdfe0, private=<optimized out>) at futex-internal.c:139
#3  0x00007ffff7aab5a0 in do_futex_wait (sem=sem@entry=0x5555556f5808, abstime=abstime@entry=0x7fffffffdfe0, clockid=0) at /usr/src/debug/glibc/glibc/nptl/sem_waitcommon.c:111
#4  0x00007ffff7aab63b in __new_sem_wait_slow64 (sem=0x5555556f5808, abstime=0x7fffffffdfe0, clockid=0) at /usr/src/debug/glibc/glibc/nptl/sem_waitcommon.c:183
#5  0x00007fffd4542f6d in amd::Semaphore::timedWait (millis=10, this=<optimized out>) at /usr/src/debug/rocm-opencl-runtime/clr-rocm-6.2.4/rocclr/thread/semaphore.cpp:130
#6  amd::Semaphore::timedWait (millis=10, this=0x5555556f5800) at /usr/src/debug/rocm-opencl-runtime/clr-rocm-6.2.4/rocclr/thread/semaphore.cpp:104
#7  amd::Monitor::wait (this=0x5555556ee200) at /usr/src/debug/rocm-opencl-runtime/clr-rocm-6.2.4/rocclr/thread/monitor.cpp:253
#8  0x00007fffd4599d83 in amd::HostQueue::HostQueue(amd::Context&, amd::Device&, unsigned long, unsigned int, amd::CommandQueue::Priority, std::vector<unsigned int, std::allocator<unsigned int> > const&) [clone .constprop.0] (this=0x5555556ee1d0, context=..., device=..., props=<optimized out>, queueRTCUs=<optimized out>, priority=<optimized out>, cuMask=...)
    at /usr/src/debug/rocm-opencl-runtime/clr-rocm-6.2.4/rocclr/platform/commandqueue.cpp:54
#9  0x00007fffd4507507 in clCreateCommandQueueWithProperties (context=context@entry=0x5555556ee3e0, device=0x55555579a2f0, queue_properties=queue_properties@entry=0x0, 
    errcode_ret=<optimized out>) at /usr/include/c++/14.2.1/bits/stl_vector.h:98
#10 0x00007fffd45076f3 in clCreateCommandQueue (context=0x5555556ee3e0, device=<optimized out>, properties=0, errcode_ret=<optimized out>)
    at /usr/src/debug/rocm-opencl-runtime/clr-rocm-6.2.4/opencl/amdocl/cl_command.cpp:191
#11 0x00007fffd498307b in clCreateCommandQueue (context=0x5555556ee3e0, device=0x55555579a2f0, properties=0, errcode_ret=0x7fffffffe214)
    at /usr/src/debug/ocl-icd/ocl-icd-2.3.2/ocl_icd_loader_gen.c:1760
#12 0x00007ffff7c588ad in hc_clCreateCommandQueue () from /usr/lib/libhashcat.so.6.2.6
#13 0x00007ffff7c3a7f8 in backend_ctx_devices_init () from /usr/lib/libhashcat.so.6.2.6
#14 0x00007ffff7c5ec16 in hashcat_session_init () from /usr/lib/libhashcat.so.6.2.6
--Type <RET> for more, q to quit, c to continue without paging--
#15 0x00005555555560ff in ?? ()
#16 0x00007ffff7a34e08 in __libc_start_call_main (main=main@entry=0x555555556020, argc=argc@entry=2, argv=argv@entry=0x7fffffffe5d8) at ../sysdeps/nptl/libc_start_call_main.h:58
#17 0x00007ffff7a34ecc in __libc_start_main_impl (main=0x555555556020, argc=2, argv=0x7fffffffe5d8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, 
    stack_end=0x7fffffffe5c8) at ../csu/libc-start.c:360
#18 0x0000555555556275 in ?? ()
(gdb) 
``` 

---

### 评论 #5 — rsta79 (2025-01-18T17:30:18Z)

> [!NOTE]
> This is not reproducible, possibly noise.

Update: Now, that the issue seems not caused by ROCm directly. but the IO or the amdgpu module. and the ROCm runtime just spinning waiting for an operation that probably never going to be complete. here is what I found in dmesg when I called ROCm to trying to allocating something on GPU:

```
[   99.954439] amdgpu 0000:00:06.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[   99.954461] amdgpu 0000:00:06.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   99.954470] amdgpu 0000:00:06.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00040B53
[   99.954477] amdgpu 0000:00:06.0: amdgpu: 	 Faulty UTCL2 client ID: CPC (0x5)
[   99.954483] amdgpu 0000:00:06.0: amdgpu: 	 MORE_FAULTS: 0x1
[   99.954488] amdgpu 0000:00:06.0: amdgpu: 	 WALKER_ERROR: 0x1
[   99.954493] amdgpu 0000:00:06.0: amdgpu: 	 PERMISSION_FAULTS: 0x5
[   99.954497] amdgpu 0000:00:06.0: amdgpu: 	 MAPPING_ERROR: 0x1
[   99.954502] amdgpu 0000:00:06.0: amdgpu: 	 RW: 0x1
[   99.955550] amdgpu 0000:00:06.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[   99.955559] amdgpu 0000:00:06.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   99.955566] amdgpu 0000:00:06.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[   99.955571] amdgpu 0000:00:06.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[   99.955577] amdgpu 0000:00:06.0: amdgpu: 	 MORE_FAULTS: 0x0
[   99.955581] amdgpu 0000:00:06.0: amdgpu: 	 WALKER_ERROR: 0x0
[   99.955585] amdgpu 0000:00:06.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[   99.955589] amdgpu 0000:00:06.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   99.955593] amdgpu 0000:00:06.0: amdgpu: 	 RW: 0x0
[   99.955601] amdgpu 0000:00:06.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[   99.955607] amdgpu 0000:00:06.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   99.955613] amdgpu 0000:00:06.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[   99.955618] amdgpu 0000:00:06.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[   99.955622] amdgpu 0000:00:06.0: amdgpu: 	 MORE_FAULTS: 0x0
[   99.955626] amdgpu 0000:00:06.0: amdgpu: 	 WALKER_ERROR: 0x0
[   99.955630] amdgpu 0000:00:06.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[   99.955634] amdgpu 0000:00:06.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   99.955638] amdgpu 0000:00:06.0: amdgpu: 	 RW: 0x0
[   99.955649] amdgpu 0000:00:06.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[   99.955655] amdgpu 0000:00:06.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   99.955660] amdgpu 0000:00:06.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[   99.955665] amdgpu 0000:00:06.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[   99.955669] amdgpu 0000:00:06.0: amdgpu: 	 MORE_FAULTS: 0x0
[   99.955673] amdgpu 0000:00:06.0: amdgpu: 	 WALKER_ERROR: 0x0
[   99.955677] amdgpu 0000:00:06.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[   99.955681] amdgpu 0000:00:06.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   99.955685] amdgpu 0000:00:06.0: amdgpu: 	 RW: 0x0
[   99.955696] amdgpu 0000:00:06.0: amdgpu: [gfxhub] page fault (src_id:0 ring:169 vmid:0 pasid:0)
[   99.955701] amdgpu 0000:00:06.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   99.955706] amdgpu 0000:00:06.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[   99.955711] amdgpu 0000:00:06.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[   99.955715] amdgpu 0000:00:06.0: amdgpu: 	 MORE_FAULTS: 0x0
[   99.955719] amdgpu 0000:00:06.0: amdgpu: 	 WALKER_ERROR: 0x0
[   99.955723] amdgpu 0000:00:06.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[   99.955727] amdgpu 0000:00:06.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   99.955731] amdgpu 0000:00:06.0: amdgpu: 	 RW: 0x0
[   99.955742] amdgpu 0000:00:06.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:0 pasid:0)
[   99.955747] amdgpu 0000:00:06.0: amdgpu:   in page starting at address 0x0000000000000000 from client 10
[   99.955752] amdgpu 0000:00:06.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00000000
[   99.955756] amdgpu 0000:00:06.0: amdgpu: 	 Faulty UTCL2 client ID: CB/DB (0x0)
[   99.955761] amdgpu 0000:00:06.0: amdgpu: 	 MORE_FAULTS: 0x0
[   99.955765] amdgpu 0000:00:06.0: amdgpu: 	 WALKER_ERROR: 0x0
[   99.955769] amdgpu 0000:00:06.0: amdgpu: 	 PERMISSION_FAULTS: 0x0
[   99.955773] amdgpu 0000:00:06.0: amdgpu: 	 MAPPING_ERROR: 0x0
[   99.955776] amdgpu 0000:00:06.0: amdgpu: 	 RW: 0x0
```
   

---

### 评论 #6 — rsta79 (2025-02-04T02:43:04Z)

Update: after testing, ROCm seems works ok in non-qubes xen environment (Xen4.19+fedora41, Xen4.17+fedora39, XCP-ng). its not ROCm's nor Xen's problem. its QubesOS specific. and XCP-ng was not working because of misconfiguration, adding `gfx_passthrough = 1` into xlconfig fix the problem.

 Please feel free to close this issue and internal issue.

---

### 评论 #7 — tcgu-amd (2025-02-04T14:45:10Z)

@rsta79 Thank you so much for your contribution! Glad you were able to figure it out! I will be closing this issue then. 

---
