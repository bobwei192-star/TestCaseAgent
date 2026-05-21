# Segmentation fault with rocm

> **Issue #2270**
> **状态**: closed
> **创建时间**: 2023-06-26T10:35:57Z
> **更新时间**: 2024-04-07T17:48:25Z
> **关闭时间**: 2024-04-07T17:48:25Z
> **作者**: rrcgat
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2270

## 描述

I encountered a segmentation fault when I attempted to load a model using Python's `transformers` package. Both PyTorch with rocm 5.4 and 5.5 nightly will cause the issue. GPU: 6750 XT.

System packages:

```
hip-runtime-amd 5.4.3-1
hipblas 5.4.3-1
hipcub 5.4.3-1
hipfft 5.4.3-1
hipsolver 5.4.3-1
hipsparse 5.4.3-1
miopen-hip 5.4.3-1
rocm-clang-ocl 5.4.3-1
rocm-cmake 5.4.3-1
rocm-core 5.4.3-4
rocm-device-libs 5.4.3-1
rocm-hip-libraries 5.4.3-2
rocm-hip-runtime 5.4.3-2
rocm-hip-sdk 5.4.3-2
rocm-language-runtime 5.4.3-2
rocm-llvm 5.4.3-1
rocm-opencl-runtime 5.4.3-1
rocm-smi-lib 5.4.3-1
rocminfo 5.4.3-1
```

Code to reproduce:

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("THUDM/chatglm2-6b-int4", trust_remote_code=True, device='cuda')
```

Here is the call stack:

```
(lldb) bt
* thread #1, name = 'python', stop reason = signal SIGSEGV
  * frame #0: 0x00007effdaeb0527 libamdhip64.so`hip::FatBinaryInfo::AddDevProgram(int) + 103
    frame #1: 0x00007effdaeb0780 libamdhip64.so`hip::FatBinaryInfo::BuildProgram(int) + 80
    frame #2: 0x00007effdaeb3ade libamdhip64.so`hip::Function::getStatFunc(ihipModuleSymbol_t**, int) + 46
    frame #3: 0x00007effdae6e37b libamdhip64.so`hip::StatCO::getStatFunc(ihipModuleSymbol_t**, void const*, int) + 187
    frame #4: 0x00007effdafd6708 libamdhip64.so`ihipLaunchKernel(void const*, dim3, dim3, void**, unsigned long, ihipStream_t*, ihipEvent_t*, ihipEvent_t*, int) + 88
    frame #5: 0x00007effdafaf5a2 libamdhip64.so`hipLaunchKernel_common + 114
    frame #6: 0x00007effdafbde12 libamdhip64.so`hipLaunchKernel + 562
    frame #7: 0x00007effdd7dbab9 libtorch_hip.so`at::native::arange_cuda_out(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, at::Tensor&)::'lambda'()::operator()() const + 11657
    frame #8: 0x00007effdd7d8d23 libtorch_hip.so`at::native::arange_cuda_out(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, at::Tensor&) + 35
    frame #9: 0x00007effddf9213f libtorch_hip.so`at::(anonymous namespace)::(anonymous namespace)::wrapper_CUDA_start_out_arange_out(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, at::Tensor&) + 159
    frame #10: 0x00007f0012362ace libtorch_cpu.so`at::_ops::arange_start_out::call(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, at::Tensor&) + 366
    frame #11: 0x00007f00119d0552 libtorch_cpu.so`at::native::arange(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>) + 354
    frame #12: 0x00007f00126ff8ef libtorch_cpu.so`c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd_start_step_arange(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>)>, at::Tensor, c10::guts::typelist::typelist<c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>>>, at::Tensor (c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>) + 63
    frame #13: 0x00007f001232d0bb libtorch_cpu.so`at::_ops::arange_start_step::redispatch(c10::DispatchKeySet, c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>) + 235
    frame #14: 0x00007f0012536682 libtorch_cpu.so`c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>), &at::(anonymous namespace)::arange_start_step(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>)>, at::Tensor, c10::guts::typelist::typelist<c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>>>, at::Tensor (c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>)>::call(c10::OperatorKernel*, c10::DispatchKeySet, c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>) + 146
    frame #15: 0x00007f001236215e libtorch_cpu.so`at::_ops::arange_start_step::call(c10::Scalar const&, c10::Scalar const&, c10::Scalar const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>) + 414
    frame #16: 0x00007f002a0f8d22 libtorch_python.so`torch::autograd::THPVariable_arange(_object*, _object*, _object*) + 7106
    frame #17: 0x00007f0059f0eef3 libpython3.10.so.1.0`cfunction_call(func=0x00007f002efd1fd0, args=<unavailable>, kwargs=<unavailable>) at methodobject.c:543:19
    frame #18: 0x00007f0059ec496e libpython3.10.so.1.0`_PyObject_MakeTpCall(tstate=0x00005571f3cd07e0, callable=0x00007f002efd1fd0, args=<unavailable>, nargs=3, keywords=0x00007efeeae8c430) at call.c:215:18
    frame #19: 0x00007f0059e6d7f9 libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:112:16
    frame #20: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:99:1
    frame #21: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:123:12
    frame #22: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at ceval.c:5893:13
    frame #23: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault(tstate=<unavailable>, f=<unavailable>, throwflag=<unavailable>) at ceval.c:4231:19
    frame #24: 0x00007f0059fb9fc0 libpython3.10.so.1.0`_PyEval_Vector [inlined] _PyEval_EvalFrame(throwflag=0, f=0x00005571fb26ff30, tstate=0x00005571f3cd07e0) at pycore_ceval.h:46:12
    frame #25: 0x00007f0059fb9fae libpython3.10.so.1.0`_PyEval_Vector(tstate=0x00005571f3cd07e0, con=0x00007efeea2c4cb0, locals=<unavailable>, args=<unavailable>, argcount=<unavailable>, kwnames=<unavailable>) at ceval.c:5067:24
    frame #26: 0x00007f0059ec4b76 libpython3.10.so.1.0`_PyObject_FastCallDictTstate(tstate=0x00005571f3cd07e0, callable=0x00007efeea2c4ca0, args=0x00007ffc9ef0a9e0, nargsf=2, kwargs=0x00007efeea111280) at call.c:153:15
    frame #27: 0x00007f0059ec4e08 libpython3.10.so.1.0`_PyObject_Call_Prepend(tstate=0x00005571f3cd07e0, callable=0x00007efeea2c4ca0, obj=0x00007efeea137640, args=0x00007efeeae5f610, kwargs=0x00007efeea111280) at call.c:431:24
    frame #28: 0x00007f0059f343d9 libpython3.10.so.1.0`slot_tp_init(self=0x00007efeea137640, args=0x00007efeeae5f610, kwds=0x00007efeea111280) at typeobject.c:7734:15
    frame #29: 0x00007f0059f2a71c libpython3.10.so.1.0`type_call(type=<unavailable>, args=0x00007efeeae5f610, kwds=0x00007efeea111280) at typeobject.c:1135:19
    frame #30: 0x00007f0059ec496e libpython3.10.so.1.0`_PyObject_MakeTpCall(tstate=0x00005571f3cd07e0, callable=0x00005571fb2ca240, args=<unavailable>, nargs=1, keywords=0x00007efeeae92040) at call.c:215:18
    frame #31: 0x00007f0059e6d7f9 libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:112:16
    frame #32: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:99:1
    frame #33: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:123:12
    frame #34: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at ceval.c:5893:13
    frame #35: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault(tstate=<unavailable>, f=<unavailable>, throwflag=<unavailable>) at ceval.c:4231:19
    frame #36: 0x00007f0059fb9fc0 libpython3.10.so.1.0`_PyEval_Vector [inlined] _PyEval_EvalFrame(throwflag=0, f=0x00007efeea435b60, tstate=0x00005571f3cd07e0) at pycore_ceval.h:46:12
    frame #37: 0x00007f0059fb9fae libpython3.10.so.1.0`_PyEval_Vector(tstate=0x00005571f3cd07e0, con=0x00007efeea2c7e30, locals=<unavailable>, args=<unavailable>, argcount=<unavailable>, kwnames=<unavailable>) at ceval.c:5067:24
    frame #38: 0x00007f0059ec4b76 libpython3.10.so.1.0`_PyObject_FastCallDictTstate(tstate=0x00005571f3cd07e0, callable=0x00007efeea2c7e20, args=0x00007ffc9ef0ad20, nargsf=2, kwargs=0x00007efeea111d40) at call.c:153:15
    frame #39: 0x00007f0059ec4e08 libpython3.10.so.1.0`_PyObject_Call_Prepend(tstate=0x00005571f3cd07e0, callable=0x00007efeea2c7e20, obj=0x00007efeea137760, args=0x00007efeeae5fb80, kwargs=0x00007efeea111d40) at call.c:431:24
    frame #40: 0x00007f0059f343d9 libpython3.10.so.1.0`slot_tp_init(self=0x00007efeea137760, args=0x00007efeeae5fb80, kwds=0x00007efeea111d40) at typeobject.c:7734:15
    frame #41: 0x00007f0059f2a71c libpython3.10.so.1.0`type_call(type=<unavailable>, args=0x00007efeeae5fb80, kwds=0x00007efeea111d40) at typeobject.c:1135:19
    frame #42: 0x00007f0059ec496e libpython3.10.so.1.0`_PyObject_MakeTpCall(tstate=0x00005571f3cd07e0, callable=0x00005571fb30c5d0, args=<unavailable>, nargs=1, keywords=0x00007efeeae92300) at call.c:215:18
    frame #43: 0x00007f0059e6d7f9 libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:112:16
    frame #44: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:99:1
    frame #45: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:123:12
    frame #46: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault at ceval.c:5893:13
    frame #47: 0x00007f0059e6d7de libpython3.10.so.1.0`_PyEval_EvalFrameDefault(tstate=<unavailable>, f=<unavailable>, throwflag=<unavailable>) at ceval.c:4231:19
    frame #48: 0x00007f0059fb9fc0 libpython3.10.so.1.0`_PyEval_Vector [inlined] _PyEval_EvalFrame(throwflag=0, f=0x00007efeea381f10, tstate=0x00005571f3cd07e0) at pycore_ceval.h:46:12
    frame #49: 0x00007f0059fb9fae libpython3.10.so.1.0`_PyEval_Vector(tstate=0x00005571f3cd07e0, con=0x00007efeea2fc050, locals=<unavailable>, args=<unavailable>, argcount=<unavailable>, kwnames=<unavailable>) at ceval.c:5067:24
    frame #50: 0x00007f0059ec4b76 libpython3.10.so.1.0`_PyObject_FastCallDictTstate(tstate=0x00005571f3cd07e0, callable=0x00007efeea2fc040, args=0x00007ffc9ef0b060, nargsf=2, kwargs=0x00007efeea112300) at call.c:153:15
    frame #51: 0x00007f0059ec4e08 libpython3.10.so.1.0`_PyObject_Call_Prepend(tstate=0x00005571f3cd07e0, callable=0x00007efeea2fc040, obj=0x00007efeea137ee0, args=0x00007efeeb280f10, kwargs=0x00007efeea112300) at call.c:431:24
    frame #52: 0x00007f0059f343d9 libpython3.10.so.1.0`slot_tp_init(self=0x00007efeea137ee0, args=0x00007efeeb280f10, kwds=0x00007efeea112300) at typeobject.c:7734:15
    frame #53: 0x00007f0059f2a71c libpython3.10.so.1.0`type_call(type=<unavailable>, args=0x00007efeeb280f10, kwds=0x00007efeea112300) at typeobject.c:1135:19
    frame #54: 0x00007f0059ec472d libpython3.10.so.1.0`_PyObject_Call(tstate=0x00005571f3cd07e0, callable=0x00005571fb30c990, args=0x00007efeeb280f10, kwargs=<unavailable>) at call.c:305:19
    frame #55: 0x00007f0059e6a79c libpython3.10.so.1.0`_PyEval_EvalFrameDefault at ceval.c:5945:12
    frame #56: 0x00007f0059e6a761 libpython3.10.so.1.0`_PyEval_EvalFrameDefault(tstate=<unavailable>, f=<unavailable>, throwflag=<unavailable>) at ceval.c:4277:22
    frame #57: 0x00007f0059fb9fc0 libpython3.10.so.1.0`_PyEval_Vector [inlined] _PyEval_EvalFrame(throwflag=0, f=0x00005571fb303530, tstate=0x00005571f3cd07e0) at pycore_ceval.h:46:12
    frame #58: 0x00007f0059fb9fae libpython3.10.so.1.0`_PyEval_Vector(tstate=0x00005571f3cd07e0, con=0x00007efeea2bfda0, locals=<unavailable>, args=<unavailable>, argcount=<unavailable>, kwnames=<unavailable>) at ceval.c:5067:24
    frame #59: 0x00007f0059ec7538 libpython3.10.so.1.0`method_vectorcall at abstract.h:114:11
    frame #60: 0x00007f0059ec7518 libpython3.10.so.1.0`method_vectorcall(method=<unavailable>, args=0x00007efeeafbffd8, nargsf=<unavailable>, kwnames=0x00007efeeb29e280) at classobject.c:53:18
    frame #61: 0x00007f0059ec45f0 libpython3.10.so.1.0`PyVectorcall_Call(callable=0x00007efeeae83500, tuple=<unavailable>, kwargs=<unavailable>) at call.c:267:24
    frame #62: 0x00007f0059e6a79c libpython3.10.so.1.0`_PyEval_EvalFrameDefault at ceval.c:5945:12
    frame #63: 0x00007f0059e6a761 libpython3.10.so.1.0`_PyEval_EvalFrameDefault(tstate=<unavailable>, f=<unavailable>, throwflag=<unavailable>) at ceval.c:4277:22
    frame #64: 0x00007f0059fb9fc0 libpython3.10.so.1.0`_PyEval_Vector [inlined] _PyEval_EvalFrame(throwflag=0, f=0x00005571f94135b0, tstate=0x00005571f3cd07e0) at pycore_ceval.h:46:12
    frame #65: 0x00007f0059fb9fae libpython3.10.so.1.0`_PyEval_Vector(tstate=0x00005571f3cd07e0, con=0x00007f002ef50d40, locals=<unavailable>, args=<unavailable>, argcount=<unavailable>, kwnames=<unavailable>) at ceval.c:5067:24
    frame #66: 0x00007f0059ec7538 libpython3.10.so.1.0`method_vectorcall at abstract.h:114:11
    frame #67: 0x00007f0059ec7518 libpython3.10.so.1.0`method_vectorcall(method=<unavailable>, args=0x00007f0059a55ba8, nargsf=<unavailable>, kwnames=0x00007f00593af8c0) at classobject.c:53:18
    frame #68: 0x00007f0059e6c427 libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:114:11
    frame #69: 0x00007f0059e6c425 libpython3.10.so.1.0`_PyEval_EvalFrameDefault at abstract.h:123:12
    frame #70: 0x00007f0059e6c425 libpython3.10.so.1.0`_PyEval_EvalFrameDefault at ceval.c:5893:13
    frame #71: 0x00007f0059fb9dee libpython3.10.so.1.0`PyEval_EvalCode [inlined] _PyEval_EvalFrame(throwflag=0, f=0x00007f0059a55a40, tstate=0x00005571f3cd07e0) at pycore_ceval.h:46:12
    frame #72: 0x00007f0059fb9ddb libpython3.10.so.1.0`PyEval_EvalCode at ceval.c:5067:24
    frame #73: 0x00007f0059fb9db7 libpython3.10.so.1.0`PyEval_EvalCode(co=0x00007f005933f3c0, globals=<unavailable>, locals=0x00007f0059341fc0) at ceval.c:1134:12
    frame #74: 0x00007f0059ffff59 libpython3.10.so.1.0`run_mod at pythonrun.c:1291:9
    frame #75: 0x00007f0059ffff21 libpython3.10.so.1.0`run_mod(mod=<unavailable>, filename=<unavailable>, globals=0x00007f0059341fc0, locals=0x00007f0059341fc0, flags=<unavailable>, arena=<unavailable>) at pythonrun.c:1312:19
    frame #76: 0x00007f005a0011aa libpython3.10.so.1.0`_PyRun_SimpleFileObject at pythonrun.c:1208:15
    frame #77: 0x00007f005a001137 libpython3.10.so.1.0`_PyRun_SimpleFileObject(fp=0x00005571f3ccc470, filename=0x00007f0059369170, closeit=1, flags=0x00007ffc9ef0b948) at pythonrun.c:456:13
    frame #78: 0x00007f005a00182c libpython3.10.so.1.0`_PyRun_AnyFileObject(fp=0x00005571f3ccc470, filename=0x00007f0059369170, closeit=1, flags=0x00007ffc9ef0b948) at pythonrun.c:90:15
    frame #79: 0x00007f005a02250b libpython3.10.so.1.0`Py_RunMain at main.c:353:15
    frame #80: 0x00007f005a022475 libpython3.10.so.1.0`Py_RunMain at main.c:372:15
    frame #81: 0x00007f005a022428 libpython3.10.so.1.0`Py_RunMain at main.c:587:21
    frame #82: 0x00007f005a0223a8 libpython3.10.so.1.0`Py_RunMain at main.c:666:5
    frame #83: 0x00007f005a022a5a libpython3.10.so.1.0`Py_BytesMain at main.c:696:12
    frame #84: 0x00007f005a022a3f libpython3.10.so.1.0`Py_BytesMain(argc=<unavailable>, argv=<unavailable>) at main.c:720:12
    frame #85: 0x00007f0059b4c850 libc.so.6`___lldb_unnamed_symbol3141 + 128
    frame #86: 0x00007f0059b4c90a libc.so.6`__libc_start_main + 138
    frame #87: 0x00005571f3763075 python`_start + 37
```

---

## 评论 (4 条)

### 评论 #1 — WenJieLife (2023-07-11T19:08:25Z)

我也遇到这个错误，但我通过导入变量解决了该问题：
export HSA_OVERRIDE_GFX_VERSION=10.3.0 HCC_AMDGPU_TARGET=gfx1030

---

### 评论 #2 — quuee (2023-09-28T12:17:02Z)

I also encountered this problem when launching stable-diffusion-webui.

```hread 27 "python3" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7ffcd25ff640 (LWP 61280)]
0x00007fffae2b40a7 in hip::FatBinaryInfo::AddDevProgram(int) () from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
(gdb) bt
#0  0x00007fffae2b40a7 in hip::FatBinaryInfo::AddDevProgram(int) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
#1  0x00007fffae2b4300 in hip::FatBinaryInfo::BuildProgram(int) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
#2  0x00007fffae2b604e in hip::Function::getStatFunc(ihipModuleSymbol_t**, int) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
#3  0x00007fffae26edbb in hip::StatCO::getStatFunc(ihipModuleSymbol_t**, void const*, int) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
#4  0x00007fffae3e2e48 in ihipLaunchKernel(void const*, dim3, dim3, void**, unsigned long, ihipStream_t*, ihipEvent_t*, ihipEvent_t*, int) () from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
#5  0x00007fffae3babd2 in hipLaunchKernel_common ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
#6  0x00007fffae3c93e4 in hipLaunchKernel () from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libamdhip64.so
#7  0x00007fffb02ddec0 in void at::native::gpu_kernel_impl<at::native::direct_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda()#2}::operator()() const::{lambda()#10}::operator()() const::{lambda(c10::Half)#1}>(at::TensorIteratorBase&, at::native::direct_copy_kernel_cuda(at::TensorIteratorBase&)::{lambda()#2}::operator()() const::{lambda()#10}::operator()() const::{lambda(c10::Half)#1} const&)
    () from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libtorch_hip.so
#8  0x00007fffb02d1814 in at::native::direct_copy_kernel_cuda(at::TensorIteratorBase&) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libtorch_hip.so
#9  0x00007fffb02d1f46 in at::native::copy_device_to_device(at::TensorIterator&, bool, bool) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libtorch_hip.so
#10 0x00007fffdd244c10 in at::native::copy_impl(at::Tensor&, at::Tensor const&, bool) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#11 0x00007fffdd245da2 in at::native::copy_(at::Tensor&, at::Tensor const&, bool) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#12 0x00007fffddeb551f in at::_ops::copy_::call(at::Tensor&, at::Tensor const&, bool) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#13 0x00007fffdd538d2b in at::native::_to_copy(at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::optional<bool>, bool, c10::optional<c10::MemoryFormat>) ()
   from /home/xx/anaconda3/envs/sd1/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so
#14 0x00007fffde21bdcb in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, c10::optional<c10::ScalarType>, c10::optional<c10::Layout>, c10::optional<c10::Device>, c10::
```

---

### 评论 #3 — piotrjaromin (2023-12-22T10:14:55Z)

> 我也遇到这个错误，但我通过导入变量解决了该问题： export HSA_OVERRIDE_GFX_VERSION=10.3.0 HCC_AMDGPU_TARGET=gfx1030

I had them same problem with rocm 5.6.1 and segmentation fault when using GPU with pytorch. Do you mind pointing me in direction why those flags are fixing this issue? 


---

### 评论 #4 — nartmada (2024-04-07T17:48:25Z)

Apologies for the lack of response.  @piotrjaromin, original issue was reported on GPU: 6750XT (gfx1031).  This is a non-supported GPU, please refer to https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html.

Unofficially, some people have overridden the gfx version to 1030 (supported version) by exporting HSA_OVERRIDE_GFX_VERSION=10.3.0.  Not supported by AMD, but some people have had success with HSA_OVERRIDE_GFX_VERSION flag.


---
