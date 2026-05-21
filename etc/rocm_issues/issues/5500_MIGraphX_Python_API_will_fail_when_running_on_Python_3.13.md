# MIGraphX Python API will fail when running on Python 3.13

> **Issue #5500**
> **状态**: open
> **创建时间**: 2025-10-10T22:46:38Z
> **更新时间**: 2025-12-02T12:56:04Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 7.0.2, ROCm 7.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/5500

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 7.0.2** (颜色: #aaaaaa)
- **ROCm 7.1.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

Applications using the MIGraphX Python API will fail when running on Python 3.13 and return the error message `AttributeError: module 'migraphx' has no attribute 'parse_onnx'`. The issue does not occur when you manually build MIGraphX. For detailed instructions, see [Building from source](https://rocm.docs.amd.com/projects/AMDMIGraphX/en/latest/install/install-migraphx.html#build-migraphx-from-source). As a workaround, change the Python version to the one found in the installed location:

```
ls -l /opt/rocm-7.0.0/lib/libmigraphx_py_*.so
```
The issue will be resolved in a future ROCm release.

---

## 评论 (1 条)

### 评论 #1 — jnolck (2025-12-02T12:56:04Z)

It's failing on 3.12 for me. I'm using the docker image rocm/pytorch​:latest, and the output of your command shows only _3.10.so. I didn't install 3.10 to test if it worked. 

---
