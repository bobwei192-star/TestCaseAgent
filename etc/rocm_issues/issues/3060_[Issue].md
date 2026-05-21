# [Issue]: 

> **Issue #3060**
> **状态**: closed
> **创建时间**: 2024-04-23T16:16:08Z
> **更新时间**: 2024-04-24T21:28:06Z
> **关闭时间**: 2024-04-24T21:28:05Z
> **作者**: hbfreed
> **标签**: ROCm 6.0.0, AMD Radeon RX 7900 XTX
> **URL**: https://github.com/ROCm/ROCm/issues/3060

## 标签

- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)

## 描述

### Problem Description

After installing 6.1, when I use torch.compile, I get the following traceback (I can put the whole thing in a pastebin, it was just long):
If I don't compile, the train script runs just fine. Happy to provide any more details to get things sorted out.


  File "/usr/lib/python3.10/concurrent/futures/_base.py", line 403, in __get_result
    raise self._exception
torch._dynamo.exc.BackendCompilerFailed: backend='inductor' raised:
RuntimeError: Internal Triton PTX codegen error: 
ptxas fatal   : Value 'sm_110' is not defined for option 'gpu-name'


### Operating System

22.04.4 LTS (Jammy Jellyfish)

### CPU

EPYC 7402P

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.0.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — hbfreed (2024-04-23T16:17:08Z)

Update: just downgraded to 6.0.2, it did not fix this problem. I've tried both regular triton and the triton nightly, for context there.  

---

### 评论 #2 — hbfreed (2024-04-24T21:28:05Z)

I fixed this, I just fully reinstalled torch and triton, making sure to uninstall the triton that torch packages with it. 

---
