# ROCm multi-version installation might cause amd-smi CLI failure

> **Issue #5875**
> **状态**: open
> **创建时间**: 2026-01-21T21:57:48Z
> **更新时间**: 2026-01-21T22:05:44Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/5875

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.2.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Installing multiple versions of ROCm on the same system might result in the `amd-smi` CLI functioning incorrectly.
As a workaround, follow any of the preferred options:

**Option 1:** If only the CLI or C++ library are needed, uninstall the `amdsmi` Python package:
```bash
python3 -m pip uninstall amdsmi
```
**Option 2:** Reinstall the Python library from your target ROCm version:
```bash
# Remove previous installation
python3 -m pip uninstall amdsmi

# Install from target ROCm instance
cd /opt/rocm/share/amd_smi
python3 -m pip install --user .
```
```{note}
`sudo` might be required. Use flag `--break-system-packages` if `pip un/installation` fails.
```

For detailed instructions, see [Install the Python library for multiple ROCm instances](https://rocm.docs.amd.com/projects/amdsmi/en/latest/install/install.html#install-the-python-library-for-multiple-rocm-instances). The issue will be fixed in a future ROCm release.
