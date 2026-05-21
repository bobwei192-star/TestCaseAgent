# [Issue]:  [gfxhub] page fault on AMD GPU gfx1151

> **Issue #6139**
> **状态**: closed
> **创建时间**: 2026-04-10T22:02:09Z
> **更新时间**: 2026-05-11T21:08:55Z
> **关闭时间**: 2026-04-12T11:11:57Z
> **作者**: MaoxinYee
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/6139

## 描述

### Problem Description

[  327.803487] amdgpu 0000:c6:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:153 vmid:8 pasid:32770)
[  327.803532] amdgpu 0000:c6:00.0: amdgpu:  Process llama-cli pid 10890 thread llama-cli pid 10890
[  327.803544] amdgpu 0000:c6:00.0: amdgpu:   in page starting at address 0x00007f2fe7922000 from client 10
[  327.803555] amdgpu 0000:c6:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00800932
[  327.803564] amdgpu 0000:c6:00.0: amdgpu:      Faulty UTCL2 client ID: CPF (0x4)
[  327.803573] amdgpu 0000:c6:00.0: amdgpu:      MORE_FAULTS: 0x0
[  327.803580] amdgpu 0000:c6:00.0: amdgpu:      WALKER_ERROR: 0x1
[  327.803587] amdgpu 0000:c6:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  327.803594] amdgpu 0000:c6:00.0: amdgpu:      MAPPING_ERROR: 0x1
[  327.803601] amdgpu 0000:c6:00.0: amdgpu:      RW: 0x0


---
It worked fine initially, but suddenly my AMD GPU stopped working for inference with llama.cpp. It used to run without issues, so I suspect it was caused by an automatic HWE kernel update. I've tried reinstalling and switching the kernel to 6.17.0-19, but that didn't help. I also tried downgrading ROCm to 7.2.0 and 7.2.1, but neither version worked.

### Operating System

Ubuntu 24.04.3 LTS 

### CPU

 AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### GPU

 AMD RYZEN AI MAX+ 395 w/ Radeon 8060S

### ROCm Version

ROCm 7.2.0

### ROCm Component

_No response_

### Steps to Reproduce

git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp 
HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)"     cmake -S . -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1151 -DCMAKE_BUILD_TYPE=Debug

cmake --build build --config Debug -- -j 16

./build/bin/llama-cli -m ../models/codellama-13b.Q8_0.gguf -p "Hello World!"

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (2 条)

### 评论 #1 — MaoxinYee (2026-04-12T11:11:52Z)

follow [https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html)



---

### 评论 #2 — harkgill-amd (2026-05-11T21:08:55Z)

@MaoxinYee, we're seeing some more reports with a similar fail signature as to what you reported here. Do you recall what resolved the issue on your end specifically?

---
