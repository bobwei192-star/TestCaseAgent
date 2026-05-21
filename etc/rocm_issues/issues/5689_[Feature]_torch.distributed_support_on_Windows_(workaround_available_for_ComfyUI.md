# [Feature]: torch.distributed support on Windows (workaround available for ComfyUI)

> **Issue #5689**
> **状态**: closed
> **创建时间**: 2025-11-24T03:01:13Z
> **更新时间**: 2025-12-16T16:04:02Z
> **关闭时间**: 2025-12-16T16:04:02Z
> **作者**: boofheadd
> **标签**: Feature Request, application:pytorch, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5689

## 标签

- **Feature Request** (颜色: #fbca04)
- **application:pytorch** (颜色: #bfdadc)
- **status: triage** (颜色: #585dd7)

## 负责人

- schung-amd

## 描述

### Suggestion Description

## Description
After years of waiting for ROCm to arrive on Windows, the preview release does not include `torch.distributed` or RCCL/Gloo backends for multi‑GPU training. This is a critical gap: developers and researchers expect multi‑GPU support as a baseline, not an optional feature.

Without it, ROCm on Windows is limited to single‑GPU experiments. Anyone with real workloads is forced back to Linux or to NVIDIA hardware. This undermines the potential of ROCm on Windows and makes it difficult to recommend for serious use.

## Expected Behavior
- `torch.distributed` should be available in ROCm Windows builds.
- RCCL or Gloo backends should be enabled so dual‑GPU and cluster systems can be used for training.

## Actual Behavior
- On Windows ROCm preview (Pro Edition HIP driver), multiple GPUs are enumerated (`torch.cuda.device_count()` shows both), but `torch.distributed` is missing.
- DistributedDataParallel cannot be used.

## Environment
- Windows 11
- Dual Radeon RX 7900 XTX
- AMD Software: Pro Edition for HIP (25.Q3)

## Request
Please prioritize enabling `torch.distributed` with RCCL/Gloo backends in ROCm for Windows. Multi‑GPU support is essential for serious AI workloads and should be part of the baseline feature set.

### Operating System

_No response_

### GPU

_No response_

### ROCm Component

_No response_

---

## 评论 (7 条)

### 评论 #1 — schung-amd (2025-11-24T18:45:51Z)

Hi @boofheadd, can you clarify what you're referring to by

> Windows ROCm preview (Pro Edition HIP driver)

?

---

### 评论 #2 — redo33 (2025-11-30T03:04:35Z)

Additional error messages on 9070:

```
  File "C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-multigpu\__init__.py", line 249, in <module>
    from .wanvideo import (
  File "C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-multigpu\wanvideo.py", line 14, in <module>
    from accelerate import init_empty_weights
ModuleNotFoundError: No module named 'accelerate'

Cannot import C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-multigpu module for custom nodes: No module named 'accelerate'
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/alter-list.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/model-list.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/extension-node-map.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/github-stats.json
[ComfyUI-Manager] default cache updated: https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/custom-node-list.json
C:\ComfyUI_windows_portable\python_embeded\Lib\site-packages\timm\models\layers\__init__.py:48: FutureWarning: Importing from timm.models.layers is deprecated, please import via timm.layers
  warnings.warn(f"Importing from {__name__} is deprecated, please import via timm.layers", FutureWarning)
Error loading AILab_SAM3Segment.py: No module named 'triton'
```

---

### 评论 #3 — yanite (2025-12-04T16:19:17Z)

Yes, many projects depend on torch.distributed, but it cannot be imported.

File D:\languages\python\Lib\site-packages\transformers\model_debugging_utils.py:29
        27 if is_torch_available():
        28     import torch
---> 29     import torch.distributed.tensor
        30     from safetensors.torch import save_file
        32     # Note to code inspectors: this toolbox is intended for people who add models to `transformers`.

File D:\languages\python\Lib\site-packages\torch\distributed\tensor\__init__.py:4
         1 # Copyright (c) Meta Platforms, Inc. and affiliates
         3 import torch
----> 4 import torch.distributed.tensor._ops  # force import all built-in dtensor ops
         5 from torch.distributed.device_mesh import DeviceMesh, init_device_mesh  # noqa: F401
         6 from torch.distributed.tensor._api import (
         7     distribute_module,
         8     distribute_tensor,
 (...)     15     zeros,
       16 )

......

ModuleNotFoundError: No module named 'torch._C._distributed_c10d'; 'torch._C' is not a package

---

### 评论 #4 — schung-amd (2025-12-04T18:06:42Z)

Thanks for all of the reports, but I'm still not clear on which release this issue pertains to; can someone link me to the relevant release or docs?

---

### 评论 #5 — yanite (2025-12-05T04:06:58Z)

> 感谢所有的报告，但我仍然不清楚这个问题涉及哪个版本;有人能给我相关的发布或文档链接吗？

Windows 
>>> torch.__version__
'2.9.0+rocmsdk20251116'

install from https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html

$ python
Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> torch.distributed.tensor
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'torch' is not defined
>>> import torch
>>> torch.__version__
'2.9.0+rocmsdk20251116'
>>> import torch.distributed.tensor
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "D:\languages\python\Lib\site-packages\torch\distributed\tensor\__init__.py", line 4, in <module>
    import torch.distributed.tensor._ops  # force import all built-in dtensor ops
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\languages\python\Lib\site-packages\torch\distributed\tensor\_ops\__init__.py", line 2, in <module>
    from ._conv_ops import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\languages\python\Lib\site-packages\torch\distributed\tensor\_ops\_conv_ops.py", line 5, in <module>
    from torch.distributed.tensor._dtensor_spec import DTensorSpec, TensorMeta
  File "D:\languages\python\Lib\site-packages\torch\distributed\tensor\_dtensor_spec.py", line 6, in <module>
    from torch.distributed.tensor.placement_types import (
  File "D:\languages\python\Lib\site-packages\torch\distributed\tensor\placement_types.py", line 8, in <module>
    import torch.distributed._functional_collectives as funcol
  File "D:\languages\python\Lib\site-packages\torch\distributed\_functional_collectives.py", line 9, in <module>
    import torch.distributed.distributed_c10d as c10d
  File "D:\languages\python\Lib\site-packages\torch\distributed\distributed_c10d.py", line 23, in <module>
    from torch._C._distributed_c10d import (
ModuleNotFoundError: No module named 'torch._C._distributed_c10d'; 'torch._C' is not a package
>>>


---

### 评论 #6 — yanite (2025-12-06T09:51:18Z)

Cell In[28], line 3
      1 torch.backends.openmp.is_available()
      2 torch.backends.mkl.is_available()
----> 3 torch.backends.openblas.is_available()

File D:\languages\python\Lib\site-packages\torch\backends\__init__.py:60, in PropModule.__getattr__(self, attr)
     59 def __getattr__(self, attr):
---> 60     return self.m.__getattribute__(attr)

AttributeError: module 'torch.backends' has no attribute 'openblas'

---

### 评论 #7 — schung-amd (2025-12-08T20:23:48Z)

Ah, thanks, this refers to Pytorch specifically. I'll rename this issue to be more specific.

Currently we don't have `torch.distributed` support on Windows as you've seen. However, in particular for the reports by @yanite and @redo33 for `transformers` and ComfyUI respectively, we saw this issue being caused by a specific version of `transformers`. The workaround is to upgrade `transformers` as this has since been fixed; see https://github.com/huggingface/transformers/pull/40038; however I'm not sure if this enables an alternate path to multi-GPU support or if it just fixes an error emitted in all cases. Please give this a try and see if it resolves your issues.

Either way, in the bigger picture this issue is still relevant, as it is true we don't have `torch.distributed` support yet. I'll check with internal teams to see if we have this on the roadmap, and if not, whether we can start scoping it out.

---
