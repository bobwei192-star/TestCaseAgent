# [Feature]: support image instructions for MI300X?

> **Issue #3420**
> **状态**: closed
> **创建时间**: 2024-07-15T10:14:26Z
> **更新时间**: 2024-10-17T16:10:01Z
> **关闭时间**: 2024-10-17T16:10:01Z
> **作者**: OudDriver
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/3420

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Suggestion Description

 This GPU does not support image instructions, resulting in compilation errors when trying to use image-based operations.

The log more or less looks like this (i am using blender cycles)
```
In file included from /snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/kernel.cpp:9:
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/compat.h:88:10: error: 'tex2D<HIP_vector_type<float, 4>, nullptr>' is unavailable: The image/texture API not supported on the device
   88 |   return tex2D<T>(texobj, x, y);
      |          ^
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/gpu/image.h:267:14: note: in instantiation of function template specialization 'ccl_gpu_tex_object_read_2D<HIP_vector_type<float, 4>>' requested here
  267 |       return ccl_gpu_tex_object_read_2D<float4>(tex, x, y);
      |              ^
/opt/rocm-6.1.2/include/hip/amd_detail/texture_indirect_functions.h:78:37: note: 'tex2D<HIP_vector_type<float, 4>, nullptr>' has been explicitly marked unavailable here
   78 | static __device__ __hip_img_chk__ T tex2D(hipTextureObject_t textureObject, float x, float y)
      |                                     ^
In file included from /snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/kernel.cpp:9:
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/compat.h:88:10: error: 'tex2D<float, nullptr>' is unavailable: The image/texture API not supported on the device
   88 |   return tex2D<T>(texobj, x, y);
      |          ^
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/gpu/image.h:279:11: note: in instantiation of function template specialization 'ccl_gpu_tex_object_read_2D<float>' requested here
  279 |       f = ccl_gpu_tex_object_read_2D<float>(tex, x, y);
      |           ^
/opt/rocm-6.1.2/include/hip/amd_detail/texture_indirect_functions.h:78:37: note: 'tex2D<float, nullptr>' has been explicitly marked unavailable here
   78 | static __device__ __hip_img_chk__ T tex2D(hipTextureObject_t textureObject, float x, float y)
      |                                     ^
In file included from /snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/kernel.cpp:9:
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/compat.h:97:10: error: 'tex3D<HIP_vector_type<float, 4>, nullptr>' is unavailable: The image/texture API not supported on the device
   97 |   return tex3D<T>(texobj, x, y, z);
      |          ^
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/gpu/image.h:331:14: note: in instantiation of function template specialization 'ccl_gpu_tex_object_read_3D<HIP_vector_type<float, 4>>' requested here
  331 |       return ccl_gpu_tex_object_read_3D<float4>(tex, x, y, z);
      |              ^
/opt/rocm-6.1.2/include/hip/amd_detail/texture_indirect_functions.h:96:37: note: 'tex3D<HIP_vector_type<float, 4>, nullptr>' has been explicitly marked unavailable here
   96 | static __device__ __hip_img_chk__ T tex3D(hipTextureObject_t textureObject, float x, float y, float z)
      |                                     ^
In file included from /snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/kernel.cpp:9:
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/hip/compat.h:97:10: error: 'tex3D<float, nullptr>' is unavailable: The image/texture API not supported on the device
   97 |   return tex3D<T>(texobj, x, y, z);
      |          ^
/snap/blender/4786/4.1/scripts/addons/cycles/source/kernel/device/gpu/image.h:342:11: note: in instantiation of function template specialization 'ccl_gpu_tex_object_read_3D<float>' requested here
  342 |       f = ccl_gpu_tex_object_read_3D<float>(tex, x, y, z);
      |           ^
/opt/rocm-6.1.2/include/hip/amd_detail/texture_indirect_functions.h:96:37: note: 'tex3D<float, nullptr>' has been explicitly marked unavailable here
   96 | static __device__ __hip_img_chk__ T tex3D(hipTextureObject_t textureObject, float x, float y, float z)
      |                                     ^
4 errors generated when compiling for gfx942.                         
```

To sum things up, the `'tex2D<HIP_vector_type<float, 4>, nullptr>`, `tex2D<float, nullptr>`, `tex3D<HIP_vector_type<float, 4>, nullptr>`, and `tex3D<float, nullptr>` is unavailable because The image/texture API is not supported on the device. 

I think this is more of a driver missing a feature. If you can add this kind of feature to this GPU, it can save me a lot of time.

### Operating System

_No response_

### GPU

MI300X

### ROCm Component

_No response_

---

## 评论 (4 条)

### 评论 #1 — b-sumner (2024-07-15T14:08:29Z)

MI-300 has no hardware support for image instructions.  Whatever you wanted to do with them could likely be accomplished faster by your code than a slow emulation layer.

---

### 评论 #2 — OudDriver (2024-07-15T15:30:29Z)

So, is it easier to just make my own way to render textures?

---

### 评论 #3 — romxero (2024-08-02T15:27:48Z)

I'm curious about this too. I was trying to compile a project that extensively used this API. 
How would we proceed in translating/porting these api calls to other means? 
Any pointers, guides, manuals, etc would be appreciated!


---

### 评论 #4 — schung-amd (2024-10-17T16:10:01Z)

As @b-sumner has stated, the MI300 does not have hardware support or instructions for image operations. Emulation of these operations without hardware support would be very involved and would end up being very slow, so we're not planning to support this. Rather than attempting to port these instructions to work without hardware support, I suggest using compatible hardware (i.e. not an MI card) for these workflows.

@romxero There aren't any specific resources I can provide that would help in emulating these instructions. At a minimum, you would need to implement your own texture mapping. If you really want to try porting this code, I suggest reading up on textures in general, and figuring out what your code is trying to do with textures so you can implement the relevant components.

I'm closing this issue as the relevant guidance has already been provided.  If you have further questions, feel free to comment.

---
