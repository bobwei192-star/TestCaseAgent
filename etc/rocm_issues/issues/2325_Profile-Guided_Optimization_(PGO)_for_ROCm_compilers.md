# Profile-Guided Optimization (PGO) for ROCm compilers

> **Issue #2325**
> **状态**: open
> **创建时间**: 2023-07-18T22:35:12Z
> **更新时间**: 2023-07-19T01:42:40Z
> **作者**: zamazan4ik
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2325

## 描述

Hi!

Recently I checked Profile-Guided Optimization (PGO) improvements on multiple projects. The results are [here](https://github.com/zamazan4ik/awesome-pgo/).

Since PGO showed measurable improvements in compiler-like loads (Clang, Clangd, clang-format, GCC, Rustc, etc.) I think it could be useful to check PGO on ROCm compilers (https://rocm.docs.amd.com/en/latest/reference/rocmcc/rocmcc.html) as well.

We need to perform PGO benchmarks on ROCm. And if it shows improvements - add a note about possible improvements ROCm performance with PGO. Providing an easier way (e.g. a build option) to build scripts with PGO can be useful for the end-users too.

Also, I think would be better if AMD will distribute already PGO-optimized binaries for the end-users. It will reduce users' compilation time (it's important for CI workloads and local development cycles).

---

## 评论 (4 条)

### 评论 #1 — keryell (2023-07-19T00:25:07Z)

Interesting.
But could you clarify where you want this PGO to happen?
- to ship ROCm compiler with PGO mode option so the end-user can compile with better optimization for its own hardware + data when enabling PGO mode?
- to ship ROCm itself with all its components (including the compiler) already PGO optimized for some standard input program/data/CPU/GPU/...?
- to ship many PGO-optimized ROCm distributions, one per famous application for some standard data?

---

### 评论 #2 — zamazan4ik (2023-07-19T00:38:01Z)

That's a very good question.

There are multiple ways to do it - and every mentioned by you way has some pros and cons (and they even can be combined). Let's discuss all of them.

> to ship ROCm compiler with PGO mode option so the end-user can compile with better optimization for its own hardware + data when enabling PGO mode?

Am I right that here you mention not compiling ROCm compiler itself but using a ROCm compiler to compile a user code with PGO? Something similar to what e.g. Clang has here - https://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization . If yes - it's very important to have  an ability to apply PGO to a user code with ROCm compiler. Not sure, is it possible to do it right now with ROCm compiler or not.

> to ship ROCm itself with all its components (including the compiler) already PGO optimized for some standard input program/data/CPU/GPU/...?

Yes! Exactly in this way, Rustc (the default Rust compiler) is shipped to the users. They prepared some standard inputs (most popular open-source applications and binaries in Rust AFAIK), collect profiles from them on their Release CI, optimize binaries and then distribute PGOed Rust compiler (and some other Rust-dependent tooling) to the users via `rustup`. Having something similar to ROCm would be great to see. How exactly - a good point for discussion. Maybe PGOed ROCm compiler will just replace the current "default" build, maybe - at least at the beginning prepare two builds like `rocmcc-default` and `rocmcc-optimized`. That's a question of risks, maintenance costs and other stuff.

> to ship many PGO-optimized ROCm distributions, one per famous application for some standard data?

That's a tricky point. Yes, for some specific workloads, this way can bring even more performance. But from my experience - it's a too complicated way (at least at the start of PGO) because have too much maintenance cost compared to the one "general" PGO build. E.g. Rust project uses only one general profile. Instead of it, I can recommend invest resources into BOLTing (applying LLVM BOLT optimizer) ROCm binaries after PGO (like Rustc already does on their release pipelines as well + I confirmed on multiple projects measurable positive effects of LLVM BOLT as well).

---

### 评论 #3 — b-sumner (2023-07-19T01:37:24Z)

We've been thinking about PGO for some time.  One of the first steps we want to take is to move the ROCm build, including clang itself, to clang.  Fortunately we've had to do this already for other special builds, but here we will have more hurdles to pass to make it the default. Once there, I do expect some ROCm components to eventually make use of PGO.

---

### 评论 #4 — zamazan4ik (2023-07-19T01:42:40Z)

@b-sumner thanks for the insight!

I suggest leaving this issue open, so the users would be able to track the progress of the work. And if you are considering moving the build to Clang itself, I propose to investigate the applicability of LLVM BOLT to ROCm as well. Because Clang infra already [has](https://github.com/llvm/llvm-project/blob/main/clang/cmake/caches/BOLT.cmake) ready-to-use CMake scripts for that. And according to Facebook [benchmarks](https://llvm.org/devmtg/2022-11/slides/Lightning15-OptimizingClangWithBOLTUsingCMake.pdf) and Rustc experience - BOLT brings a lot to the compilers too even after PGO.

---
