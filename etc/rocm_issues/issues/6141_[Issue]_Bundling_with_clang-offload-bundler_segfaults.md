# [Issue]: Bundling with clang-offload-bundler segfaults.

> **Issue #6141**
> **状态**: closed
> **创建时间**: 2026-04-11T18:15:23Z
> **更新时间**: 2026-04-14T21:56:18Z
> **关闭时间**: 2026-04-14T21:56:18Z
> **作者**: eliphatfs
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6141

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- david-salinas
- zichguan-amd

## 描述

### Problem Description

Using OS: (in container on github actions)
CPU: virtualized, unknown.
ROCM version: 7.2.1
Container Image: rocm/dev-ubuntu-22.04:7.2.1
No GPU available or needed in compilation environment.


### Operating System

Ubuntu 22.04 Container, Unknown Host

### CPU

Unknown Virtualized

### GPU

No GPU available or needed in compilation environment

### ROCm Version

7.2.1

### ROCm Component

llvm-project

### Steps to Reproduce

https://github.com/eliphatfs/gint/actions/runs/24288414482

clang-offload-bundler --type=o --targets=hipv4-amdgcn-amd-amdhsa--gfx1100,hipv4-amdgcn-amd-amdhsa--gfx1101,hipv4-amdgcn-amd-amdhsa--gfx1102,hipv4-amdgcn-amd-amdhsa--gfx11-generic,hipv4-amdgcn-amd-amdhsa--gfx12-generic --input=artifact/gint_gfx1100.hsaco --input=artifact/gint_gfx1101.hsaco --input=artifact/gint_gfx1102.hsaco --input=artifact/gint_gfx11-generic.hsaco --input=artifact/gint_gfx12-generic.hsaco --output=artifact/gint.hipfb
 #0 0x000055f79ae01880 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/rocm-7.2.1/lib/llvm/bin/clang-offload-bundler+0x7c880)
 #1 0x000055f79adfebbd SignalHandler(int, siginfo_t*, void*) Signals.cpp:0:0
 #2 0x00007fd64f16b520 (/lib/x86_64-linux-gnu/libc.so.6+0x42520)
 #3 0x000055f79ae31bff (anonymous namespace)::ObjectFileHandler::finalizeOutputFile() OffloadBundler.cpp:0:0
 #4 0x000055f79ae2fe3f clang::OffloadBundler::BundleFiles() (/opt/rocm-7.2.1/lib/llvm/bin/clang-offload-bundler+0xaae3f)
 #5 0x000055f79adb4739 std::_Function_handler<llvm::Error (), main::'lambda3'()>::_M_invoke(std::_Any_data const&) ClangOffloadBundler.cpp:0:0
 #6 0x000055f79adb4a0c main::'lambda0'(std::function<llvm::Error ()>)::operator()(std::function<llvm::Error ()>) const ClangOffloadBundler.cpp:0:0
 #7 0x000055f79adaaa12 main (/opt/rocm-7.2.1/lib/llvm/bin/clang-offload-bundler+0x25a12)
 #8 0x00007fd64f152d90 (/lib/x86_64-linux-gnu/libc.so.6+0x29d90)
 #9 0x00007fd64f152e40 __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x29e40)
#10 0x000055f79adb42e5 _start (/opt/rocm-7.2.1/lib/llvm/bin/clang-offload-bundler+0x2f2e5)
generate_amdgcn.sh: line 23:   562 Segmentation fault

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (1 条)

### 评论 #1 — zichguan-amd (2026-04-14T20:06:29Z)

Hi @eliphatfs, the offload-bundler requires a dummy host for `--type=o`. You can use `--targets=host-x86_64-unknown-linux-gnu,...`  and `--input=/dev/null`
```
clang-offload-bundler --type=o \
  --targets=host-x86_64-unknown-linux-gnu,hipv4-amdgcn-amd-amdhsa--gfx1100,hipv4-amdgcn-amd-amdhsa--gfx1101,hipv4-amdgcn-amd-amdhsa--gfx1102,hipv4-amdgcn-amd-amdhsa--gfx11-generic,hipv4-amdgcn-amd-amdhsa--gfx12-generic \
  --input=/dev/null \
  --input=artifact/gint_gfx1100.hsaco \
  --input=artifact/gint_gfx1101.hsaco \
  --input=artifact/gint_gfx1102.hsaco \
  --input=artifact/gint_gfx11-generic.hsaco \
  --input=artifact/gint_gfx12-generic.hsaco \
  --output=artifact/gint.hipfb
```

---
