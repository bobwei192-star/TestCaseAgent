# [WSL] PyTorch ROCm 7.2 fails to import due to missing libroctx64.so.4 library

> **Issue #6053**
> **状态**: closed
> **创建时间**: 2026-03-21T16:30:05Z
> **更新时间**: 2026-05-01T18:43:34Z
> **关闭时间**: 2026-05-01T18:43:34Z
> **作者**: bobcy2015
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6053

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- lucbruni-amd

## 描述

### Problem Description

### Description

PyTorch ROCm 7.2 wheel package cannot be imported on WSL2 because the WSL ROCm runtime package (`hsa-runtime-rocr4wsl-amdgpu`) is missing required libraries that PyTorch depends on.

### System Information

- **OS**: Ubuntu 24.04 (WSL2)
- **Kernel**: 6.6.87.2-microsoft-standard-WSL2
- **Python**: 3.12.3
- **PyTorch**: 2.9.1+rocm7.2.0.lw.git7e1940d4
- **Windows Driver**: AMD Software: Adrenalin Edition 26.1.1
- **GPU**: AMD Radeon RX 7900 XTX

### Installed Packages

```bash
# ROCm packages installed via amdgpu-install
ii  hsa-runtime-rocr4wsl-amdgpu:amd64  25.30.13-2281980.24.04
ii  rocm-core                          7.2.0.70200-43~24.04
```

### Error Message

```python
>>> import torch
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/path/to/venv/lib/python3.12/site-packages/torch/__init__.py", line 427, in <module>
    from torch._C import *
ImportError: libroctx64.so.4: cannot open shared object file: No such file or directory
```

### Missing Libraries

The following libraries are required by PyTorch ROCm but are NOT included in the WSL ROCm package:

- `libroctx64.so.4` (ROCm Tracer/ROCTX)
- `librocprofiler64.so` (ROCm Profiler)
- `librocm_smi64.so` (ROCm SMI)

### Steps to Reproduce

1. Install Windows with AMD Adrenalin 26.1.1 driver
2. Install WSL2 with Ubuntu 24.04
3. Install ROCm for WSL:
   ```bash
   wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/noble/amdgpu-install_7.2.70200-1_all.deb
   apt install ./amdgpu-install_7.2.70200-1_all.deb
   amdgpu-install -y --usecase=wsl,rocm --no-dkms
   ```
4. Install PyTorch ROCm wheel from AMD repo
5. Try to import torch:
   ```bash
   python -c "import torch"
   ```

### Expected Behavior

PyTorch should import successfully and detect the AMD GPU through WSL2 GPU passthrough.

### Actual Behavior

Import fails with `ImportError: libroctx64.so.4: cannot open shared object file`

### Workaround

Currently, the only working workaround is to use Docker container with full ROCm stack.

### Request

Please either:

1. **Include the missing libraries** (`libroctx64.so.4`, etc.) in the WSL ROCm package
2. **OR** Update the PyTorch ROCm wheel to make these libraries optional
3. **OR** Provide a separate WSL-compatible PyTorch wheel

### References

- AMD WSL Installation Guide: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html
- AMD PyTorch Installation Guide: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-pytorch.html

---

### Operating System

Ubuntu 24.04 (WSL2)

### CPU

AMD Ryzen 7 9700X

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

rocm7.2.0.lw.git7e1940d4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — lucbruni-amd (2026-04-01T18:14:45Z)

Hi @bobcy2015, thanks for reporting.

I am unable to reproduce this issue with the `pip` Pytorch installation in the `venv`, documented [here](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/install/installrad/wsl/install-pytorch.html#option-a-pytorch-via-pip-installation) for 7.2. The import is successful and the GPU is recognized.

If you're still encountering the issue, please post your exact installation steps starting from the Adrenalin driver through to your Pytorch installation. I believe there is a mix-up somewhere during installation and one hint is in your traceback, specifically your `venv` path:

```
...
File "/path/to/venv/lib/python3.12/site-packages/torch/__init__.py", line 427, in <module>
...
```

Thanks!

---

### 评论 #2 — lucbruni-amd (2026-04-15T20:28:04Z)

@bobcy2015 are you still encountering this issue? If so, let me know your installation steps and I'd be happy to help.

---

### 评论 #3 — lucbruni-amd (2026-05-01T18:43:34Z)

Closing this due to inactivity and as the issue appears to be resolved through proper installation. Please feel free to reopen or open a new issue if you encounter any troubles during installation and use. Thanks!

---
