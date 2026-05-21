# [Issue]: .to("cuda") gets stuck on WSL2

> **Issue #3952**
> **状态**: closed
> **创建时间**: 2024-10-28T11:09:57Z
> **更新时间**: 2024-10-28T16:01:24Z
> **关闭时间**: 2024-10-28T15:59:30Z
> **作者**: Sidies
> **标签**: ROCm 6.1.0, AMD Radeon RX 6800 XT
> **URL**: https://github.com/ROCm/ROCm/issues/3952

## 标签

- **ROCm 6.1.0** (颜色: #ededed)
- **AMD Radeon RX 6800 XT** (颜色: #ededed)

## 描述

### Problem Description

Hi,

I am running a WSL2 instance and followed these two guides to get torch installed and rocm installed:
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html
https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html

The installation process worked without issues but when loading models from huggingface it gets stuck on the "Loading checkpoint shards" step.

This only happens when i use .to("cuda")
So this works:
```python
model = AutoModelForCausalLM.from_pretrained("sciphi/triplex", trust_remote_code=True).eval()
tokenizer = AutoTokenizer.from_pretrained("sciphi/triplex", trust_remote_code=True)
``` 

But this does not work:
```python
model = AutoModelForCausalLM.from_pretrained("sciphi/triplex", trust_remote_code=True).to("cuda").eval()
tokenizer = AutoTokenizer.from_pretrained("sciphi/triplex", trust_remote_code=True)
``` 

### Operating System

Ubuntu 22.04.5 LTS (Jammy Jellyfish)"

### CPU

AMD Ryzen 9 5900X 12-Core Processor

### GPU

AMD Radeon RX 6800 XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-10-28T15:59:30Z)

Hi @Sidies, this issue is due to the RX 6800 XT not currently being supported for usage on WSL. It's expected that the 6800 XT will be detected in rocminfo but hang when moving data to your GPU with `.to("cuda")`. Please refer to the [WSL Compatibility Matrix](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html#gpu-support-matrix) for a list of supported GPUs.

---
