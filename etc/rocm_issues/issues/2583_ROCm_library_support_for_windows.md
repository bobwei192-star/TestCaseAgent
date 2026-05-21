# ROCm library support for windows

> **Issue #2583**
> **状态**: open
> **创建时间**: 2023-10-19T13:36:48Z
> **更新时间**: 2024-11-10T07:28:48Z
> **作者**: alvin546
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2583

## 标签

- **Documentation** (颜色: #5319e7)

## 负责人

- Naraenda

## 描述

As AMD has announced ROCm support for windows in the release of 5.5.1, can you please confirm **if all the APIs of ROCm/HIP** libraries (rocBlas/hipBlas, rocSolver/hipSolver, rocfft/hipfft, rocsparse/hipsparse, rocrand/hiprand, rocprim/hipCUB and rocthrust/hipthrust) are supported on windows as well.

If yes, can you please point me to relevant documentation for any limitations

---

## 评论 (8 条)

### 评论 #1 — johnnynunez (2023-10-19T14:13:18Z)

> As AMD has announced ROCm support for windows in the release of 5.5.1, can you please confirm **if all the APIs of ROCm/HIP** libraries (rocBlas/hipBlas, rocSolver/hipSolver, rocfft/hipfft, rocsparse/hipsparse, rocrand/hiprand, rocprim/hipCUB and rocthrust/hipthrust) are supported on windows as well.
> 
> If yes, can you please point me to relevant documentation for any limitations

for AI, it’s needed MiOpen and AMDGraphX. See PR that are open

---

### 评论 #2 — alvin546 (2023-10-19T14:17:05Z)

@johnnynunez 

Thanks for confirming the status of MiOpen and AMDGraphX support on windows.
Can you please confirm the same for the following libraries (rocBlas/hipBlas, rocSolver/hipSolver, rocfft/hipfft, rocsparse/hipsparse, rocrand/hiprand, rocprim/hipCUB and rocthrust/hipthrust)

---

### 评论 #3 — pramenku (2023-10-21T16:18:12Z)

@alvin546 You can refer this page for supported libraries 

https://rocm.docs.amd.com/en/docs-5.5.1/reference/gpu_libraries/math.html

---

### 评论 #4 — pramenku (2023-10-23T17:37:04Z)

Reopen if you don't get what you need from above lage

---

### 评论 #5 — saadrahim (2023-10-23T17:50:18Z)

We do not have a comprehensive list of differences between libraries enabled on Windows and Linux. A high level list is available at https://rocmdocs.amd.com/en/develop/about/whats-new/whats-new.html.

A more detailed list is needed. We need to enable the operating system info listing for all libraries as well.


---

### 评论 #6 — ppanchad-amd (2024-05-15T15:15:43Z)

Internal ticket has been created to include OS info listing for all libraries. Thanks!

---

### 评论 #7 — briansp2020 (2024-06-19T17:26:05Z)

https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html
![its_happening](https://github.com/ROCm/ROCm/assets/3746601/d3b13223-3b2d-4452-92c8-634afc8e4e5f)


---

### 评论 #8 — johnnynunez (2024-11-10T07:28:47Z)

Pytorch: https://github.com/pytorch/pytorch/pull/137279

---
