# How to declare and implement a new HIP runtime API?

> **Issue #2309**
> **状态**: closed
> **创建时间**: 2023-06-30T09:05:52Z
> **更新时间**: 2023-07-01T03:55:30Z
> **关闭时间**: 2023-07-01T03:54:33Z
> **作者**: xuantengh
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2309

## 描述

Suppose I want to declare and implement a new HIP runtime API related to HIP stream named `hipStreamXXX`. I declare it in [hip_runtime_api.h](https://github.com/ROCm-Developer-Tools/HIP/blob/develop/include/hip/hip_runtime_api.h) and implement it in [hip_stream.cpp](https://github.com/ROCm-Developer-Tools/hipamd/blob/develop/src/hip_stream.cpp) like this:

```cpp
hipError_t hipStreamXXX(hipStream_t stream) {
  HIP_INIT_API(hipStreamXXX, stream);
  std::printf("This is a newly added HIP runtime API\n");
  HIP_RETURN(hipSuccess);
}
```

The compiler reports errors from the `HIP_INIT_API` macro, saying that `HIP_CB_SPAWNER_OBJECT` needs a `operation_id` for this runtime API.
After inspecting the [`CMakeLists.txt`](https://github.com/ROCm-Developer-Tools/hipamd/blob/develop/src/CMakeLists.txt#L233-L236), I know that the include header is generated from a Python script [`hip_prof_gen.py`](https://github.com/ROCm-Developer-Tools/hipamd/blob/develop/src/hip_prof_gen.py), but I can't figure out how the `operation_id` is defined. Is there any file I missed to define and implement a newly added HIP runtime API?

---

## 评论 (3 条)

### 评论 #1 — xuantengh (2023-06-30T09:06:45Z)

Since there are files listing HIP runtime APIs, I'm wondering whether they are related to define a new runtime API?
- https://github.com/ROCm-Developer-Tools/hipamd/blob/develop/src/amdhip.def
- https://github.com/ROCm-Developer-Tools/hipamd/blob/develop/src/hip_hcc.def.in
- https://github.com/ROCm-Developer-Tools/hipamd/blob/develop/src/hip_hcc.map.in

---

### 评论 #2 — xuantengh (2023-07-01T03:24:35Z)

I add `-DUSE_PROF_API=OFF` in CMake configure option but the error still occurs:

```
hip/src/hip_stream.cpp: In function ‘hipError_t hipStreamUpda
teCUMask(hipStream_t, uint32_t, uint32_t*)’:
hip/src/hip_prof_api.h:45:27: error: ‘HIP_API_ID_hipStreamUpd
ateCUMask’ was not declared in this scope; did you mean ‘HIP_API_ID_hipExtStreamGetCUMask’?
   45 |   api_callbacks_spawner_t<HIP_API_ID_##operation_id> __api_tracer(
  \
      |                           ^~~~~~~~~~~
```

---

### 评论 #3 — xuantengh (2023-07-01T03:54:33Z)

```diff
-  HIP_API_ID_LAST = 359,
+  HIP_API_ID_hipStreamXXX = 360,
+  HIP_API_ID_LAST = 360,
```

After insert a `HIP_API_ID` for the new API and update the value of `HIP_API_ID_LAST` in `include/amd_detail/hip_prof_str.h`, and then rerun the CMake build process, I successfully add a new HIP runtime API.
Close this issue as complete.

---
