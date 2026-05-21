# [Request]:  Missing c10::UndefinedTensorImpl::_singleton definition in libc10_hip.so

> **Issue #3928**
> **状态**: closed
> **创建时间**: 2024-10-21T11:01:42Z
> **更新时间**: 2024-10-23T08:05:40Z
> **关闭时间**: 2024-10-23T08:05:40Z
> **作者**: ZJLi2013
> **标签**: Under Investigation, ROCm 6.2.3, mi300
> **URL**: https://github.com/ROCm/ROCm/issues/3928

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **mi300** (颜色: #ededed)

## 描述

### Problem Description

hi, rocm expert, when building a rocm /torch project with following link flags:

```py
torch_libs = ["torch", "torch_hip", "torch_python", "c10", "c10_hip"]
torch_link_libs ="-L/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib/ " + " ".join([f"-l{lib}" for lib in torch_libs])
``` 

but get the following undefined error

```yml
/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib/libc10.so | grep _singleton
00000000000e3aa0 B c10::UndefinedTensorImpl::_singleton
``` 

rocm/torch image: rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0 

Thanks for clarifying
David 

### Operating System

Ubuntu 22.04

### CPU

Ryzen 

### GPU

mi300

### ROCm Version

ROCm 6.2.3

### ROCm Component

hipBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — schung-amd (2024-10-21T18:14:44Z)

Hi @ZJLi2013, is there an actual error occurring? `c10::UndefinedTensorImpl::_singleton` is not an error; it is from https://github.com/pytorch/pytorch/blob/main/c10/core/UndefinedTensorImpl.cpp and represents a tensor that has not been defined yet (i.e. declared with no constructor arguments).

---

### 评论 #2 — ZJLi2013 (2024-10-22T02:00:24Z)

hi @schung-amd , thanks for replying. it comes when build a rocm project, and at runtime it give errors:

```yml
ImportError: /opt/conda/envs/py_3.10/lib/python3.10/site-packages/backend.cpython-310-x86_64-linux-gnu.so: undefined symbol: _ZN3c1019UndefinedTensorImpl10_singletonE
``` 

the runtime error is the linker can't find the symbol for `c10::UndefinedTensorImpl::_singleton` with `c10_hip.so`  here is more details:

```sh
root@6a1d73c08dd2:/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib# nm -D libc10.so | grep _ZN3c1019UndefinedTensorImpl10_singletonE
00000000000e3aa0 B _ZN3c1019UndefinedTensorImpl10_singletonE
root@6a1d73c08dd2:/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib# nm -D libc10_hip.so | grep _ZN3c1019UndefinedTensorImpl10_singletonE
root@6a1d73c08dd2:/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib#
``` 

you can see,  `_ZN3c1019UndefinedTensorImpl10_singletonE` only defined in `libc10.so`, but not in `libc10_hip.so`, so what's the right way to link torch/c10 for hip/rocm env ?





---

### 评论 #3 — schung-amd (2024-10-22T13:54:33Z)

Thanks for the clarification. Can you share the code you're using when running into this? The usual sources of this error seem to be importing extensions before importing torch (i.e. https://pytorch.org/cppdocs/notes/faq.html#undefined-symbol-errors-from-pytorch-aten) or a torch version incompatibility with the library.

---

### 评论 #4 — ZJLi2013 (2024-10-23T08:05:40Z)

thanks, after fix build following (#3918)[https://github.com/ROCm/ROCm/issues/3918], the runtime can works as expected. 

even though still see:
```yml
nm -C /opt/conda/envs/py_3.10/lib/python3.10/site-packages/xxx-1.1.4-py3.10-linux-x86_64.egg/grouped_gemm_backend.cpython-310-x86_64-linux-gnu.so | grep "singleton"
                 U c10::UndefinedTensorImpl::_singleton
``` 

will close the issue for now


---
