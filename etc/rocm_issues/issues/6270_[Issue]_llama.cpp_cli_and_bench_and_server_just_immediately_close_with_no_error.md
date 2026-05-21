# [Issue]: llama.cpp cli and bench and server just immediately close with no error at all

> **Issue #6270**
> **状态**: open
> **创建时间**: 2026-05-18T16:31:00Z
> **更新时间**: 2026-05-18T16:31:00Z
> **作者**: PCAssistSoftware
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6270

## 描述

### Problem Description

Using this version - https://repo.radeon.com/rocm/llama.cpp/windows/rocm-rel-7.2.1/llama-b8407-windows-rocm-7.2.1-gfx110X-gfx115X-gfx120X-x64.zip

Running any command e.g. 

.\llama-bench `
  -m "D:\Models\lmstudio-community\Qwen3.6-35B-A3B-GGUF\Qwen3.6-35B-A3B-Q4_K_M.gguf" `
 -ngl 999 `
  -fa on `
  -p 8192 `
  -n 512 `
  -b 1024 `
  -r 3

just results in immediately exiting and returning to terminal prompt with no indication of error etc

### Operating System

Windows 11 10.0.26200

### CPU

AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

AMD Radeon(TM) 8060S Graphics

### ROCm Version

-

### ROCm Component

_No response_

### Steps to Reproduce

as above

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_
