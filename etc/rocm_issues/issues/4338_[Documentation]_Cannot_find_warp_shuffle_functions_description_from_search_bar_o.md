# [Documentation]: Cannot find warp shuffle functions description from search bar on home page

> **Issue #4338**
> **状态**: closed
> **创建时间**: 2025-02-04T21:12:32Z
> **更新时间**: 2025-03-20T21:58:42Z
> **关闭时间**: 2025-03-19T18:42:44Z
> **作者**: gsitaram
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/4338

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

A search for "shuffle" in the [home page of ROCm docs](https://rocm.docs.amd.com/en/latest/) yields one result, and not the actual page that I was looking for.

<img width="1265" alt="Image" src="https://github.com/user-attachments/assets/00bfd5ff-0cca-4b8c-a8a6-b7c3cf7a0805" />

The page I wanted to get to was the following:

[https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_cpp_language_extensions.html#warp-shuffle-functions](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_cpp_language_extensions.html#warp-shuffle-functions)

Please fix the search functionality so that it is easier to find what we want from the main page. Users would not know which sub-section of the docs to go and search in.

### Attach any links, screenshots, or additional evidence you think will be helpful.

Other similar examples: can't find `rocprofv3` documentation for instance. I was looking for the page on "[Using rocprofv3](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/how-to/using-rocprofv3.html#using-rocprofv3)", but see this instead:

<img width="1283" alt="Image" src="https://github.com/user-attachments/assets/c87c721b-7513-453a-ae1c-de045a642d79" />

or any HIP API call such as `hipMalloc` that should have returned [the API page](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/hip_runtime_api/modules/memory_management.html#_CPPv4I0E9hipMalloc10hipError_tPP1T6size_t), but search results show this instead: 

<img width="1187" alt="Image" src="https://github.com/user-attachments/assets/9284e391-34cc-46d4-87b3-8fe70bea93f2" />

---

## 评论 (9 条)

### 评论 #1 — harkgill-amd (2025-02-05T15:26:38Z)

Hi @gsitaram, this issue stems from changes to the search functionality made on the ReadTheDocs end. Our docs team is tracking this internally and are working towards improving the search workflow and results. 

As a workaround, you can utilize the search bar located in the flyout (bottom right of the docs). With this search, you can select to include subprojects. This will cover all the ROCm components including the `HIP` and `rocprofiler-sdk` documentation. 

![Image](https://github.com/user-attachments/assets/886402f5-a08b-4b70-8acb-edce5e1b7720)

---

### 评论 #2 — harkgill-amd (2025-02-26T20:41:12Z)

@gsitaram, the main search bar has been updated to integrate the "Include subprojects" filter which was previously available in the flyout. Could you please give it a try now?

---

### 评论 #3 — gsitaram (2025-02-27T01:43:28Z)

I tried `rocprofv3` and didn't get the page I was looking for which is the one called "Using rocprofv3"

---

### 评论 #4 — emotroshylov (2025-02-27T09:59:02Z)

> rocprofv3

Hi @gsitaram 
Use filter Include subprojects and Enter key

---

### 评论 #5 — harkgill-amd (2025-02-27T15:16:00Z)

As @emotroshylov mentioned, you'd have to select the "Include subprojects filter". This results in the following.

![Image](https://github.com/user-attachments/assets/974e4e69-d967-4e3f-9473-ec12f077250e)

---

### 评论 #6 — harkgill-amd (2025-03-19T18:42:44Z)

Closing this issue out as the main ROCm docs search now has the "Include subprojects filter", which when enabled, corrects the previously failing queries.

---

### 评论 #7 — gsitaram (2025-03-20T16:40:06Z)

@harkgill-amd , Just wanted to point out that this is an extra step, that is pretty much hidden, that you are expecting from our customers. We must find a way to avoid this and make it easier for our customers to access all the content that we have. This is not acceptable as a solution for me due to the above reason.


---

### 评论 #8 — harkgill-amd (2025-03-20T17:56:45Z)

We do agree that the current workflow is unintuitive and needs to be improved. The underlying issue is that the search backend is provided by RTD and the "Include subproject" filter is their status quo as you can see with the search bar at https://docs.readthedocs.com/platform/stable/index.html. 

We've already informed the ReadTheDocs team of our concerns and the need to have this filter set by default. They're working towards implementing this and we'll pick it up once it's ready. 

---

### 评论 #9 — gsitaram (2025-03-20T21:58:41Z)

Thank you, once this option is set by default, my concerns will have been addressed. 

---
