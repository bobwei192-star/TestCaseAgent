# [Feature]:  HIP Precompiled Headers Support

> **Issue #4174**
> **状态**: closed
> **创建时间**: 2024-12-19T22:43:52Z
> **更新时间**: 2025-01-06T17:02:20Z
> **关闭时间**: 2025-01-06T17:02:12Z
> **作者**: LunNova
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4174

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

I'd like to be able to use precompiled headers with cmake projects that are compiled with `amdclang++`.

It's not clear if this is supported so I'm not sure if this is a bug or a feature request.

It does not work with the standard way of enabling PCH support in cmake and causes errors that the PCH targets the wrong target:

```cmake
target_precompile_headers(target_name_here PRIVATE 
        "$<$<COMPILE_LANGUAGE:CXX>:${CMAKE_SOURCE_DIR}/include/pch.hpp>"
)
```

```log
error: __declspec keyword was disabled in PCH file but is currently enabled
error: PCH file was compiled for the target 'x86_64-unknown-linux-gnu' but the current translation unit is being compiled for target 'amdgcn-amd-amdhsa'
```

It looks like AMD does use PCH in ROCM/clr so it probably works at least in some scenarios, but it's not clear how to use this correctly in a cmake project.

https://github.com/ROCm/clr/blob/0640d360194ee961a52dcdcc439d7c45710ec7f8/hipamd/src/hip_embed_pch.sh#L147-L159

### Operating System

not OS specific, can be replicated in official ROCm dockers

### GPU

Not GPU specific

### ROCm Component

Not component specific

---

## 评论 (2 条)

### 评论 #1 — ppanchad-amd (2024-12-20T02:03:42Z)

Hi @LunNova. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — darren-amd (2025-01-06T17:02:12Z)

Hi @LunNova,

I had a chat with the internal team and currently precompiled headers are not supported for general use, and are currently only used in specific scenarios.

---
