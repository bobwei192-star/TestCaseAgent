# Missing ISO_Fortran_binding.h

> **Issue #3867**
> **状态**: closed
> **创建时间**: 2024-10-05T15:03:09Z
> **更新时间**: 2024-10-08T21:51:48Z
> **关闭时间**: 2024-10-08T21:51:48Z
> **作者**: rbberger
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3867

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

The `ISO_Fortran_binding.h` which is part of `flang`/`amdflang` is not part of the ROCm installation. It doesn't show up in any ROCm rpms. LLVM has the necessary install rule:
https://github.com/llvm/llvm-project/blob/main/flang/CMakeLists.txt#L543-L547
and apparently so does the ROCm/llvm-project:
https://github.com/ROCm/llvm-project/blob/rocm-6.2.2/flang/CMakeLists.txt#L508-L512
So it might just be a packaging error.

---

## 评论 (3 条)

### 评论 #1 — lamb-j (2024-10-08T15:27:55Z)

@bcornille 

---

### 评论 #2 — bcornille (2024-10-08T16:24:35Z)

Hi @rbberger,
Just for some clarification, https://github.com/ROCm/flang is the current implementation of `amdflang`. This is built on the "classic-flang" compiler, which is distinct from LLVM's flang. As you can see we are also working hard on the LLVM flang compiler via our fork of the upstream LLVM repo and so we have repos for both compilers named `flang` in the ROCm organization. From what I can tell, there is no `ISO_Fortran_binding.h` in the "classic-flang"-based `flang` repo. So I don't think there is any packaging error, just unfortunate overloading of the "flang" name and maybe some lack of clarity about which "flang" is included in ROCm.

---

### 评论 #3 — rbberger (2024-10-08T19:00:59Z)

@bcornille Thanks for the clarification. Hopefully `flang-new` or whatever it is called now will improve the situation. On the systems I'm on this currently means the only feasible compiler combo is `amdclang`, `amdclang++` and `crayftn`. The use case is C/C++ libraries (which do offloading via Kokkos) that expose a Fortran interface for production codes that are meant to run on El Capitan.

---
