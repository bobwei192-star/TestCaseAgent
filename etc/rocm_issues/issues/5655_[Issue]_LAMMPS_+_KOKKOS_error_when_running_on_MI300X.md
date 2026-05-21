# [Issue]: LAMMPS + KOKKOS error when running on MI300X

> **Issue #5655**
> **状态**: closed
> **创建时间**: 2025-11-12T08:16:27Z
> **更新时间**: 2025-11-19T15:29:25Z
> **关闭时间**: 2025-11-19T15:29:25Z
> **作者**: dipietrantonio
> **标签**: AMD Instinct MI300X, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5655

## 标签

- **AMD Instinct MI300X** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- huanrwan-amd

## 描述

### Problem Description

I get the following error (`hipErrorInvalidKernelFile`) when I try to run a GPU accelerated build of  the LAMMPS molecular dynamics package on a MI300X.

```
  what():  hipMemcpyToSymbol( HIP_SYMBOL(::Kokkos::Impl::g_device_hip_lock_arrays), &::Kokkos::Impl::g_host_hip_lock_arrays, sizeof(::Kokkos::Impl::HIPLockArrays)) error( hipErrorInvalidKernelFile): invalid kernel file /tmp/root/spack-stage/spack-stage-kokkos-3.7.02-6hnbw7mnamym2c7knpyesuyiet2nrt6u/spack-src/core/src/HIP/Kokkos_HIP_Locks.cpp:96
```

I built the software within a container based on ROCm 7.0.2 (but I also tried 6.3.3) and the Spack package manager. [The recipe is available here.](https://github.com/PawseySC/pawsey-containers/blob/cdp-cxivars/benchmarking/bench.dockerfile)

I made sure the software was built for the gfx90a and gfx942 architectures. The container runs fine on Setonix (MI250X system), but fails on a MI300X cluster.

Any idea of what could be causing the error?

### Operating System

Ubuntu 22.04.5

### CPU

AMD Zen4 architecture

### GPU

MI300X

### ROCm Version

6.3.3 and 7.0.2

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — huanrwan-amd (2025-11-13T20:42:44Z)

Hi @dipietrantonio, thanks for posting the issue. I can build the docker image with the given docker file in a gfx942. 
Can you show the command you used to run " LAMMPS molecular dynamics". Thanks.

---

### 评论 #2 — dipietrantonio (2025-11-14T01:39:30Z)

Hi @huanrwan-amd , here is an archive with the input files.
[lammps_example.tar.gz](https://github.com/user-attachments/files/23537622/lammps_example.tar.gz)

The `submit.sh` script is used to launch the job on a GPU node. The call to the `lmp` executable is wrapped in a `run_lammps.sh` script so that I can export the right variables within the container to find the executable. A better way is to set those variables in the container recipe. Note that the path might be different from what you have in your container, and might need adjusting.

Thanks for looking into this.

---

### 评论 #3 — huanrwan-amd (2025-11-18T21:13:22Z)

Hi @dipietrantonio, checked [The recipe is available here.](https://github.com/PawseySC/pawsey-containers/blob/cdp-cxivars/benchmarking/bench.dockerfile). It builds towards both target amdgpu_target=gfx90a,gfx942. But only gfx90a kernels are built. 
I tried to just build against gfx942. It picked up with correct kernel. Can you please try on your side?
In a container created by the given image run 
`/spack/bin/spack install --fresh --verbose lammps@20230802.4 +kokkos +rocm amdgpu_target=gfx942 ^kokkos+rocm amdgpu_target=gfx942`

---

### 评论 #4 — dipietrantonio (2025-11-19T05:41:43Z)

Dear @huanrwan-amd thank you for your reply! Indeed that was the issue. It turns out that kokkos@3.7 does not support `gfx942`, whereas the latest version, `kokkos@4.2` does.  I confirm I am able to run lammps on a MI300X.

Thank you again for your valuable input!

---

### 评论 #5 — huanrwan-amd (2025-11-19T15:29:25Z)

@dipietrantonio Thanks for the feedback. It is great to see it works. 

---
