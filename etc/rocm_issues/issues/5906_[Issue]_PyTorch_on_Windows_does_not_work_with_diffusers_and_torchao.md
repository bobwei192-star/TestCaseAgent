# [Issue]: PyTorch on Windows does not work with diffusers and torchao

> **Issue #5906**
> **状态**: open
> **创建时间**: 2026-01-26T19:27:13Z
> **更新时间**: 2026-03-26T23:34:57Z
> **作者**: andju
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5906

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- benrichard-amd

## 描述

### Problem Description

With these packages installed (`install -r requirements.txt`):
```
accelerate==1.12.0
diffusers==0.36.0
transformers==4.57.6
```
the following Python code runs without errors:
```
import torch
from diffusers import AutoPipelineForText2Image
```

However, if I add torchao (`pip install torchao==0.15.0`) the Python code exits with the following error:
```
ModuleNotFoundError                       Traceback (most recent call last)
File c:\Users\andju\rocm-test\venv\Lib\site-packages\diffusers\utils\import_utils.py:1016, in _LazyModule._get_module(self, module_name)
   1015 try:
-> 1016     return importlib.import_module("." + module_name, self.__name__)
   1017 except Exception as e:

File C:\Program Files\Python312\Lib\importlib\__init__.py:90, in import_module(name, package)
     89         level += 1
---> 90 return _bootstrap._gcd_import(name[level:], package, level)

File <frozen importlib._bootstrap>:1387, in _gcd_import(name, package, level)

File <frozen importlib._bootstrap>:1360, in _find_and_load(name, import_)

File <frozen importlib._bootstrap>:1331, in _find_and_load_unlocked(name, import_)

File <frozen importlib._bootstrap>:935, in _load_unlocked(spec)

File <frozen importlib._bootstrap_external>:999, in exec_module(self, module)

File <frozen importlib._bootstrap>:488, in _call_with_frames_removed(f, *args, **kwds)

File c:\Users\andju\rocm-test\venv\Lib\site-packages\diffusers\pipelines\auto_pipeline.py:21
     20 from ..configuration_utils import ConfigMixin
...
   1020         f" traceback):\n{e}"
   1021     ) from e

RuntimeError: Failed to import diffusers.pipelines.auto_pipeline because of the following error (look up to see its traceback):
No module named 'torch._C._distributed_c10d'; 'torch._C' is not a package
```

### Operating System

Windows 11 10.0.26200

### CPU

AMD Ryzen 7 7800X3D 8-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 7.2

### ROCm Component

_No response_

### Steps to Reproduce

1. Install Python 3.12.
2. Create and activate a venv.
3. Follow the steps described here: https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/install/installrad/windows/install-pytorch.html.
4. Follow the steps described in the "Problem Description".

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — abdullah-azab (2026-02-28T19:47:28Z)

Confirmed  , happened to me also , win 11 . same issue , i was installing https://github.com/xgen-universe/Capybara which had torchao as dependency , when running the python file . it crashed with torch._C._distributed_c10d missing . 

is it a missing flag during compilation use USE_DISTRIBUTED=1 instead of USE_DISTRIBUTED=0 , would this flag effect stability , why would i have to recompile C++ backend for PyTorch’s to use popular literary on AMD card.

my experience over all with RoCm pytorch is good despite complicated setup.

---

### 评论 #2 — chejh-amd (2026-03-03T02:35:34Z)

It doesn’t seem to be a compilation‑flag issue. It is probable that the ROCm‑on‑Windows PyTorch build simply doesn’t include those C++ backend components. The internal APIs that torchao expects just aren’t present in the Windows ROCm version of PyTorch.

---

### 评论 #3 — james58899 (2026-03-04T09:00:01Z)

Related to https://github.com/ROCm/ROCm/issues/5689 and https://github.com/pytorch/ao/issues/3452

---

### 评论 #4 — 0xDELUXA (2026-03-06T18:13:18Z)

I tracked down unguarded `torch.distributed` top-level imports that cause `import torchao` to crash on PyTorch builds without distributed support (Windows ROCm), and submitted a fix in [pytorch/ao#4017](https://github.com/pytorch/ao/pull/4017).

I also tracked down the same issue across the HuggingFace ecosystem and submitted fixes:
- [huggingface/transformers#44507](https://github.com/huggingface/transformers/pull/44507)
- [huggingface/accelerate#3962](https://github.com/huggingface/accelerate/pull/3962)

The `transformers` and `accelerate` fixes are already merged, but it looks like we still need [pytorch/ao#4017](https://github.com/pytorch/ao/pull/4017). Only after that will the chain of imports triggered by `from diffusers import AutoPipelineForText2Image` (and similar) no longer crash on PyTorch builds without distributed support.

---

### 评论 #5 — 0xDELUXA (2026-03-26T23:30:41Z)

Given TorchAO's structure, this issue will likely remain open until Windows ROCm supports full distributed. 

In the meantime, my fork conditionally imports `torch.distributed`, for anyone who wants to give it a try: https://github.com/0xDELUXA/torchao_win-rocm. I haven't updated it in a while, and keep in mind that it is in an experimental stage.

---
