# [Feature]: Intermediate bytecode to allow for forward compat, reduced build times and smaller binaries

> **Issue #3985**
> **状态**: open
> **创建时间**: 2024-11-03T04:26:49Z
> **更新时间**: 2024-12-18T23:03:55Z
> **作者**: LunNova
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3985

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

Do you have any plans to support an intermediary compile target a la PTX so code targeting AMD GPUs can be compiled for that intermediary and then at runtime it's translated as needed to machine code for whatever GPU is actually in use?

The current approach requires compiling machine code for all AMD GPUs ahead of time; forward compat without a recompile is impossible.

Compiling for each individual gfxXXX target in advance takes up a lot of space and takes a long time for any large ROCm project. This aspect of ROCm is significantly worse than CUDA.

---

## 评论 (8 条)

### 评论 #1 — sohaibnd (2024-12-11T17:00:07Z)

Hi @LunNova, there aren't any plans right now to support compiling to an intermediate bytecode like PTX. There are advantages to this approach including a smaller binary file size and forward compatibility without recompiling as you mentioned. However, compiling directly down to the ISA allows the compiler to better optimize the code and take advantage of more powerful instructions in newer architectures, which is important as GPUs are evolving rapidly. It also means lower overhead at runtime as there is no need convert the bytecode to machine code.

Let me know if you have any other questions!

---

### 评论 #2 — LunNova (2024-12-11T18:25:24Z)

> It also means lower overhead at runtime as there is no need convert the bytecode to machine code.

In practice this doesn't seem to play out. Launching a training run with pytorch of eg https://github.com/KellerJordan/modded-nanogpt or stable diffusion takes a few minutes before the first step on ROCm 6.2. CUDA's much faster.

Are there known deficiencies in this area that are being worked on?

---

### 评论 #3 — sohaibnd (2024-12-12T17:25:14Z)

Can you provide more information on the workflow you are running for stable diffusion? We can look into this further but this isn't something related to compiling down to ISA versus bytecode. Please create a separate issue for this.


---

### 评论 #4 — LunNova (2024-12-15T23:39:01Z)

@sohaibnd was this closed in error? It looks like there are already work in progress repos for using SPIR-V as an intermediate language for compute kernels: https://github.com/ROCm/SPIRV-LLVM-Translator

---

### 评论 #5 — sohaibnd (2024-12-16T17:00:01Z)

@LunNova Sorry about that, you are correct, there is work in progress to support compiling down to an AMDGCN flavoured SPIR-V. However, this will be a secondary option alongside the existing approach to compile down to ISA (which provides better optimization and lower overhead at runtime as mentioned above) rather than a replacement, so users will be able to choose between compiling to ISA or to SPIR-V. 

If you have any more follow-up questions, I can re-open this issue. Regarding the slow first step you are observing in the training run of modded-nanogpt or stable diffusion, it is not related to this issue so please create a separate issue for it (with more details).


---

### 评论 #6 — LunNova (2024-12-16T17:15:39Z)

Thanks for the info about the AMDGCN flavored SPIR-V. I think it might be worth keeping this issue open to track waiting for that to launch/be ready but up to you.

Regarding slow time to first step: I'm working on bumping all my deps to latest versions (rocm 6.3, pytorch 2.6 nightly, latest aotriton beta etc) and gathering some profiling traces before filing an issue in case it's already been fixed and so the report is actually useful.

---

### 评论 #7 — LunNova (2024-12-16T17:19:52Z)

> so users will be able to choose between compiling to ISA or to SPIR-V.

@sohaibnd  Is it going to be possible to compile to both some selected ISAs and have SPIR-V as a fallback option for forwardcompat or users using gfx targets you didn't choose to compile for to save on overall binary size?

This might help with eg pytorch dropping some arches to reduce the download size a few weeks ago and then having to revert because people still wanted to use those cards.  
Merged and then reverted in this thread https://github.com/pytorch/pytorch/pull/142827#issuecomment-2542507857 

Another example of binary size for lots of separate individual targets resulting in support being dropped is composable_kernel: https://github.com/ROCm/composable_kernel/issues/1020#issuecomment-1896740852

---

### 评论 #8 — sohaibnd (2024-12-18T23:03:55Z)

> Thanks for the info about the AMDGCN flavored SPIR-V. I think it might be worth keeping this issue open to track waiting for that to launch/be ready but up to you.

Sure, I can re-open this issue to track SPIR-V support but this could take a while.

> @sohaibnd Is it going to be possible to compile to both some selected ISAs and have SPIR-V as a fallback option for forwardcompat or users using gfx targets you didn't choose to compile for to save on overall binary size?

Yes, when it is supported, you should be able to specify --offload-arch=amdgcnspirv;gfx90a for example when compiling and at runtime the loader will chose the most specific object.


---
