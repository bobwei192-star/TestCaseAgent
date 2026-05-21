# Disable "SetTensor/CopyTensor" console logging.

> **Issue #2250**
> **状态**: closed
> **创建时间**: 2023-06-17T11:23:16Z
> **更新时间**: 2023-07-07T11:21:38Z
> **关闭时间**: 2023-07-07T11:21:38Z
> **作者**: ZappaBoy
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2250

## 描述

### OS Platform, distribution and device
ArchLinux 6.1.32-1-lts - AMD Radeon RX 6700 XT - gfx1031

### Issue description
I'm training an LSTM neural network using `CuDNN`, training works perfectly but I cannot be able to disable some console logging about `SetTensor/CopyTensor`. This is quite annoying because the logs are printed during the entire training process surrounding Tensorflow logs. This doesn't happen if the same code run on CPU.

Logging example:
```shell
...
SetTensor
real descritor: 1, 1, 64
flat descritor: 64
SetTensor
real descritor: 1, 1, 64
flat descritor: 64
CopyTensor
src real descriptor: 1, 1, 64
src flat descriptor: 64
dst real descriptor: 1, 1, 64
dst flat descriptor: 64
...
```

I also tried to disable logging using the `MIOPEN_ENABLE_LOGGING`, `MIOPEN_ENABLE_LOGGING_CMD`, `MIOPEN_LOG_LEVEL`, and `TF_CPP_MAX_VLOG_LEVEL` without success.

```python
self.rocm_logging_level = -1  # -1 disable logging
os.environ['MIOPEN_ENABLE_LOGGING'] = f'{1 if self.rocm_logging_level > 0 else 0}'
os.environ['MIOPEN_ENABLE_LOGGING_CMD'] = f'{1 if self.rocm_logging_level > 0 else 0}'
os.environ['MIOPEN_LOG_LEVEL'] = f'{self.rocm_logging_level}'
os.environ['TF_CPP_MAX_VLOG_LEVEL'] = f'{self.rocm_logging_level}'
```

Here are the values of the environment variables above at running time:
```python
MIOPEN_ENABLE_LOGGING = '0'
MIOPEN_ENABLE_LOGGING_CMD = '0'
MIOPEN_LOG_LEVEL = '-1'
TF_CPP_MAX_VLOG_LEVEL = '-1'
```

I tried to train another model using `InceptionResNetV2` and the same issues happens.
Also, this happens even using the `model.predict()` method if using the GPU.
Probably this is an issue related to the `AMD Radeon RX 6700 XT` or some mine misconfiguration.


---

## 评论 (1 条)

### 评论 #1 — ZappaBoy (2023-07-07T11:21:38Z)

I found the source of the problem in the `MIOpen` repository. If it is of interest to anyone, I have opened a new issue on the `MIOpen` project https://github.com/ROCmSoftwarePlatform/MIOpen/issues/2247 in order to close this issue not directly related to this `ROCm` repository.

---
