# [Feature]: Add torch.device.rocm and torch.rocm.is_available()

> **Issue #4231**
> **状态**: open
> **创建时间**: 2025-01-06T18:19:20Z
> **更新时间**: 2025-02-05T21:39:16Z
> **作者**: Qubitium
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/4231

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

Some of us want to write code that exclusively use `rocm` device in pytorch and use explicit torch.rocm.is_available() api to check and run rocm targetting code. Cuda, xpu, xps has same device and check api in torch but torch(rocm edition) just wants to override anything cuda.This is fine for cuda compat but there should also be a parallel explicit api that needs no remapping. Device.rocm comes to mind.

Writing and checking `torch.device.cuda` is real nvidia or fake mapping to internal rocm device makes code impossible to read/decipher and prone to errors.

We added rocm support to [GPTQModel](https://github.com/modelcloud/gptqmodel) and our api accepts `load(..., device="rocm")` not only makes it clean/explicit but necessary as we do internal checks on what kernels are available or not under hipified env. 

---

## 评论 (4 条)

### 评论 #1 — Qubitium (2025-01-11T17:43:40Z)

For more context:

It is not possible to declare that your code supports ROCM in a static manner. 

A: 
```py
# supports execution on Nvidia and AMD
SUPPORTS_DEVICES = [ device.CUDA, device.ROCM ]
```

Current state of affairs make the above declaration impossible without secondary remapping by the developer to map a unique device.rocm because it becomes this otherwise:

B: 
```py
# supports execution on Nvidia and AMD
SUPPORTS_DEVICES = [ device.CUDA ]
```

They (A and B) are not equivalent. The first one is telling the world I support NVIDIA and AMD gpus. The second is ambiguous. 


You need A because sometimes you need C:

C: 
```py
# supports execution on Nvidia only
SUPPORTS_DEVICES = [ device.CUDA ]
``` 
Where C means exactly as it implies: this code only supports NVIDA CUDA. You can do dynamic/run-time alterations of the SUPPORTS_DEVICES variable to fix this but why? This is super clear  to read and write. 

Also, at some point, AMD `must` move away from `cuda` backpacking: Unified Pytorch: https://github.com/pytorch/pytorch/issues/144617

Above are actually code/scenario from a real-world usage:

https://github.com/ModelCloud/GPTQModel/blob/37018fc4bbb3ab9fb7eb423e36a2dfc8959dec3c/gptqmodel/nn_modules/qlinear/dynamic_cuda.py#L46

@fxmarty-amd 


---

### 评论 #2 — Qubitium (2025-01-11T18:28:26Z)

Also the fact that AMD doesn't allow you to write D is basically asking people to use and write CUDA code as top priority than ROCM. Some of us actually want to write clean ROCM only targeting code and expand ROCM influence. 

D:
```
# supports execution on AMD only
SUPPORTS_DEVICES = [ device.ROCM ]
```

---

### 评论 #3 — naromero77amd (2025-01-16T20:07:27Z)

@Qubitium This topic of having a separate and distinct ROCm device in PyTorch comes up periodically. The technical leadership concluded it would cost a lot of engineering hours for a result that has a net negative result – no more getting new CUDA torch features nearly for free, harder to track upstream differences between vendors, etc.


---

### 评论 #4 — Qubitium (2025-02-05T21:32:08Z)

@naromero77amd I want amd to win! And also understand the leadership decision, if it was still 2020. Ship fast and asap. 

Pytorch needs to be less CUDA centric and AMD needs to stop calling itself CUDA. 

AMD needs to do everything it can to merge itself to `main` aka Nvidia branch for all intends and purposes. But this is impossible now and in forseeable future if AMD keeps calling itself cuda and hijacks it from top to bottom.

If Pytorch code is over optimizing for cuda, then that is a also a problem that needs to be dealt with at pytorch. It should have better hooks for devices, kernels, dtypes, not monolithic code paths as it appears now. 

p.s I am not asking Rocm to abandon CUDA hijacks but offer the devs the option to use device.rocm as option. It can map back to cuda for all we care. It has to happen, might as well trickle it in?






---
