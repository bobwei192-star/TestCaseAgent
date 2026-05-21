# Running BatchNorm2D causes miopenStatusUnknownError

> **Issue #6150**
> **状态**: open
> **创建时间**: 2026-04-15T13:03:35Z
> **更新时间**: 2026-04-15T14:17:26Z
> **作者**: mt88875
> **标签**: status: triage, project: miopen
> **URL**: https://github.com/ROCm/ROCm/issues/6150

## 标签

- **status: triage** (颜色: #585dd7)
- **project: miopen** (颜色: #962619)

## 负责人

- adityas-amd

## 描述

To whom it may concern,

When I run the function BatchNorm2D on my RX 9060 XT, it triggers the miopenStatusUnknownError. This is problematic since it makes it impossible for me to train data on many pretrained models. Is there a solution which resolves this issue? Thanks in advance.

**CPU:** i5-12400
**GPU:** RX 9060 XT 16GB
**OS:** Windows 11, version 25H2
**ROCm version:** 7.2.1

**Simple code causing the problem:**
```
import torch.nn as nn
import torch

gpu = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Device used:', torch.cuda.get_device_name())

f = nn.BatchNorm2d(100, device = gpu)
x = torch.randn(size = (20, 100, 35, 45), device = gpu)
output = f(x)
```
**Error message:**
```
MIOpen(HIP): Error [Compile] 'hiprtcCompileProgram(prog.get(), c_options.size(), c_options.data())' MIOpenBatchNormFwdTrainSpatialHIP.cpp: HIPRTC_ERROR_COMPILATION (6)
MIOpen(HIP): Error [BuildHip] HIPRTC status = HIPRTC_ERROR_COMPILATION (6), source file: MIOpenBatchNormFwdTrainSpatialHIP.cpp
MIOpen(HIP): Warning [BuildHip] In file included from C:\Users\matth\AppData\Local\Temp\comgr-2144-9-76ee63\input\MIOpenBatchNormFwdTrainSpatialHIP.cpp:31:
In file included from C:\Users\matth\AppData\Local\Temp\comgr-2144-9-76ee63\include\batchnorm_functions.hpp:30:
In file included from C:\Users\matth\AppData\Local\Temp\comgr-2144-9-76ee63\include\configuration.hpp:36:
C:\Users\matth\AppData\Local\Temp\comgr-2144-9-76ee63\include\miopen_type_traits.hpp:151:10: fatal error: 'type_traits' file not found
  151 | #include <type_traits>
      |          ^~~~~~~~~~~~~
1 error generated when compiling for gfx1200.
MIOpen Error: DESKTOP-FSHC0VD:C:/develop/TheRock/rocm-libraries/projects/miopen/src/hipoc/hipoc_program.cpp:299: Code object build failed. Source: MIOpenBatchNormFwdTrainSpatialHIP.cpp
Traceback (most recent call last):
  File "c:\Users\matth\Documents\Coding Files\Python Files\a.py", line 10, in <module>
    output = f(x)
             ^^^^
  File "C:\Users\matth\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py", line 1775, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\matth\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py", line 1786, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\matth\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\batchnorm.py", line 193, in forward
    return F.batch_norm(
           ^^^^^^^^^^^^^
  File "C:\Users\matth\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\functional.py", line 2813, in batch_norm
    return torch.batch_norm(
           ^^^^^^^^^^^^^^^^^
RuntimeError: miopenStatusUnknownError
```
