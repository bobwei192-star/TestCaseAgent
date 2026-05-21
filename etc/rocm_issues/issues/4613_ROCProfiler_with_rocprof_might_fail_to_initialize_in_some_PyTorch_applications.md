# ROCProfiler with rocprof might fail to initialize in some PyTorch applications

> **Issue #4613**
> **状态**: open
> **创建时间**: 2025-04-11T23:19:15Z
> **更新时间**: 2025-04-11T23:19:15Z
> **作者**: prbasyal-amd
> **标签**: Verified Issue, ROCm 6.4.0
> **URL**: https://github.com/ROCm/ROCm/issues/4613

## 标签

- **Verified Issue** (颜色: #0052cc)
- **ROCm 6.4.0** (颜色: #aaaaaa)

## 负责人

- prbasyal-amd

## 描述

In some PyTorch applications, the `HSA_TOOLS_LIB` environment variable might fail to initialize the ROCProfiler library with the `rocprof` tool. As a result of the issue, `--stats` and the counter collection commands might fail to trace the execution of the application and collect hardware component performance during kernel execution, respectively. The issue might have originated from a change in the PyTorch library, causing an overwrite in the `HSA_TOOLS_LIB` environment variable. This issue will be fixed in a future ROCm release. However, consider that ROCprofiler and `rocprof` are being phased out in favor of ROCprofiler-SDK in upcoming ROCm releases. For details, see [ROCm upcoming changes](#roctracer-rocprofiler-rocprof-and-rocprofv2-deprecation).
As a workaround, add the following to the command you are running:

```
LD_PRELOAD=/opt/rocm-6.x.x/lib/librocprofiler64.so.1.
```

Alternatively, you can modify the `rocprof` script located at `/opt/rocm-6.x.x/bin/rocprof` by adding the following in line # 96:

```
ROCPROFV1_LD_PRELOAD=$MY_HSA_TOOLS_LIB
```
