# Omniperf out-of-the-box issues with ROCm 6.2.0

> **Issue #3498**
> **状态**: closed
> **创建时间**: 2024-08-02T18:43:42Z
> **更新时间**: 2024-12-05T19:53:15Z
> **关闭时间**: 2024-12-05T19:53:15Z
> **作者**: peterjunpark
> **标签**: Verified Issue, 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3498

## 标签

- **Verified Issue** (颜色: #0052cc)
- **6.2.0** (颜色: #31778C)

## 描述

**Error when running Omniperf with an application with command line arguments**. As a workaround, create an intermediary script to call the application with the necessary arguments, then call the script with Omniperf. This issue is fixed in a future release of Omniperf. See [#347](https://github.com/ROCm/omniperf/issues/347).

---

**Omniperf might not work with AMD Instinct MI300 accelerators out of the box**, resulting in the following error: “ERROR gfx942 is not enabled rocprofv1. Available profilers include: [‘rocprofv2’]”. As a workaround, add the environment variable export ROCPROF=rocprofv2.

---

**Omniperf’s Python dependencies may not be installed with your ROCm installation**, resulting in the following message:

“[ERROR] The ‘dash>=1.12.0’ package was not found in the current execution environment.

[ERROR] The ‘dash-bootstrap-components’ package was not found in the current execution environment.

Please verify all of the Python dependencies called out in the requirements file are installed locally prior to running omniperf.

See: /opt/rocm-6.2.0/libexec/omniperf/requirements.txt”

As a workaround, install these Python requirements manually: pip install /opt/rocm-6.2.0/libexec/omniperf/requirements.txt.

---

## 评论 (1 条)

### 评论 #1 — harkgill-amd (2024-12-05T19:53:15Z)

Both **Error when running Omniperf with an application with command line arguments** and **Omniperf might not work with AMD Instinct MI300 accelerators out of the box** have been resolved as of ROCm 6.3.0 and no longer require any workarounds. 

Installing Python dependencies using `requirements.txt` has also now been documented in the [ROCm Compute Profiler installation guide](https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/install/core-install.html#install-via-package-manager). This will avoid the errors highlighted in **Omniperf’s Python dependencies may not be installed with your ROCm installation**.

Closing out these known issues as they have been addressed.

---
