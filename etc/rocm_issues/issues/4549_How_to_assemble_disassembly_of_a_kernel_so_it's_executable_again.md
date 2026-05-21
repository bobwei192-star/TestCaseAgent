# How to assemble disassembly of a kernel so it's executable again?

> **Issue #4549**
> **状态**: closed
> **创建时间**: 2025-04-01T03:39:32Z
> **更新时间**: 2025-04-02T17:39:31Z
> **关闭时间**: 2025-04-02T17:39:31Z
> **作者**: mysoreanoop
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4549

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

I have a CK example binary (`build/bin/example_gemm_xdl_int8`) that I can disassemble to get the *.s (disassembly) file. If I now want to add a couple of assembly instructions there and restitch the unified binary back together, what are my options? 

---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-04-01T14:11:50Z)

Hi @mysoreanoop. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — schung-amd (2025-04-01T14:35:45Z)

Hi @mysoreanoop, I think the assembly-to-executable example in rocm-examples should have what you're looking for: https://github.com/ROCm/rocm-examples/tree/amd-staging/HIP-Basic/assembly_to_executable

---

### 评论 #3 — mysoreanoop (2025-04-01T23:21:07Z)

Hi @schung-amd , thank you!
I still need help; would greatly appreciate it if you can help:


This is my current compilation flow:

![Image](https://github.com/user-attachments/assets/4ac108d5-13b2-43a1-aec6-3495c21c6139)

If I change the `-emit-obj` to `-S`, I get the host and device disassemblies: `device.s` and `host.s`

I now have a modified device.s that I wish to compile and supplant device.o. How do I go about doing that?

---

### 评论 #4 — schung-amd (2025-04-02T12:59:12Z)

After you've modified `device.s`, something like `$ROCM_INSTALL_DIR/llvm/bin/clang -target amdgcn-amd-amdhsa -mcpu=<ARCH> device.s -o device.o` should work, where `<ARCH>` is your target architecture (e.g. gfx1030, gfx1100, etc.).

---

### 评论 #5 — mysoreanoop (2025-04-02T17:39:08Z)

Thank you, that worked (need to also carry over some flags from the original command)!

---
