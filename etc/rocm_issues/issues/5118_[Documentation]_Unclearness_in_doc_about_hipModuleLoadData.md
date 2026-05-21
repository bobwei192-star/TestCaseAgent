# [Documentation]: Unclearness in doc about hipModuleLoadData

> **Issue #5118**
> **状态**: closed
> **创建时间**: 2025-07-29T03:28:00Z
> **更新时间**: 2025-09-09T00:20:53Z
> **关闭时间**: 2025-09-09T00:20:52Z
> **作者**: FlagZhao
> **标签**: Under Investigation, Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/5118

## 标签

- **Under Investigation** (颜色: #0052cc)
- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

Hi, 

Do you guys have any more detailed describtion on the word image in hipModuleLoadData's doc? NVIDIA's dirver supports loading both ptx/sass/cubin with JIT inside. I am not very sure about does it support similar thing as well. 

Thanks very much for your help.

### Attach any links, screenshots, or additional evidence you think will be helpful.

ROCm Doc: 
https://rocm.docs.amd.com/projects/HIP/en/docs-develop/reference/hip_runtime_api/modules/module_management.html

CUDA driver Doc:
https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__MODULE.html#group__CUDA__MODULE_1g04ce266ce03720f479eab76136b90c0b

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-07-29T16:02:27Z)

Hi @FlagZhao. Internal ticket has been created to assist you. Thanks!

---

### 评论 #2 — FlagZhao (2025-07-29T23:22:42Z)

Thank you!

---

### 评论 #3 — harkgill-amd (2025-09-04T20:17:28Z)

Hi @FlagZhao, apologies for the lack of response. The `image` in `hipModuleLoadData(hipModule_t *module, const void *image)` can be either a code object or a fatbin that contains multiple code objects. Here's an example snippet from the hip-tests that better illustrates this.
```
  size_t codeSize;
  hiprtcGetCodeSize(prog, &codeSize);

  vector<char> code(codeSize);
  hiprtcGetCode(prog, code.data());

  hiprtcDestroyProgram(&prog);

  hipModule_t module;
  hipFunction_t kernel;

  checkHipErrors(hipModuleLoadData(&module, code.data()));
```
For reference, you can find the complete example at https://github.com/ROCm/hip-tests/blob/develop/samples/2_Cookbook/23_cmake_hiprtc/saxpy.cpp. For an example with passing in a fatbin, see https://github.com/ROCm/hip-tests/blob/develop/catch/unit/module/hipModuleLoadData.cc. We're also working on updating the documentation to better clarify what the function expects for the image argument - changes should be live sometime next week.

---

### 评论 #4 — FlagZhao (2025-09-09T00:20:52Z)

Thanks very much for your effort and example. I will try that. I think this issue is solved now.

---
