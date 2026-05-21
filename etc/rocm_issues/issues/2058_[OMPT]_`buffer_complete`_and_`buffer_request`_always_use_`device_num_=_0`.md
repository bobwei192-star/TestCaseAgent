# [OMPT] `buffer_complete` and `buffer_request` always use `device_num = 0`

> **Issue #2058**
> **状态**: closed
> **创建时间**: 2023-04-17T12:00:47Z
> **更新时间**: 2023-09-21T16:14:12Z
> **关闭时间**: 2023-09-21T11:00:13Z
> **作者**: Thyre
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2058

## 负责人

- ronlieb

## 描述

**Description:**

The OMPT interface offers a way to enable actual tracing on a target device by utilizing the device tracing interface. Similar to the callbacks, callback functions can be registered for a device. Then, the interface can request buffers for each device and trigger a callback when the buffer has finished. 
The device tracing interface itself works fine in ROCm 5.4.x with [some important functions (see #1747)](https://github.com/RadeonOpenCompute/ROCm/issues/1747) still missing, mostly affecting the timestamps. However, while testing, I noticed that the `device_num` seemed off for both `buffer_request` and `buffer_complete` when utilizing multiple GPUs. 

**What is the issue?:**
The class `OmptTracingBufferMgr` contains the method `dispatchCallback` where the `buffer_complete` callback is invoked. Here, the device number of zero is [hard coded](https://github.com/RadeonOpenCompute/llvm-project/blob/amd-stg-open/openmp/libomptarget/src/ompt_buffer_mgr.cpp#L343). 
```C
ompt_device_callbacks.ompt_callback_buffer_complete(
    0 /* TODO device num */, buffer,
    /* bytes returned in this callback */
    (char *)getNextTR(last_cursor) - (char *)first_cursor,
    (ompt_buffer_cursor_t)first_cursor, false /* buffer_owned */);
```

This is the same case for requesting a buffer. Here, the number zero is [hard coded](https://github.com/RadeonOpenCompute/llvm-project/blob/amd-stg-open/openmp/libomptarget/src/ompt_buffer_mgr.cpp#L76) as well:
```C
  // TODO Move the buffer allocation to a helper thread
  ompt_device_callbacks.ompt_callback_buffer_request(0 /* device_num */,
                                                     &buffer, &total_bytes);
```

This issue affects the evaluation of the device tracing interface buffers significantly. We might be able to reconstruct the actual device using the invoked callbacks, but this is not ideal. Our current approach would be to support only one device until this issue (and #2057) is fixed.

---

## 评论 (3 条)

### 评论 #1 — ronlieb (2023-08-03T16:58:29Z)

assigning Dhruva, which i dont seem to have actual permission to do

---

### 评论 #2 — Thyre (2023-09-21T11:31:28Z)

Thanks a lot for fixing the issue! Will test it as soon as our node with multiple GPUs is running again.

Regarding the commit message:
> We don't do anything with the device id passed through
ompt_set_trace_ompt since using that information to filter out tracing
will introduce locking in the critical tracing path of OpenMP worker threads,
something we would like to avoid. If this feature is indeed very
important for the tool, we can introduce this feature later. The
downside of ignoring the device id is that a tool does not have the
ability to selectively control the events that get traced on a device
basis.

This shouldn't affect our development. We are interested in all callbacks we can get in the tracing interface and will not differentiate between devices (and probably also won't offer users to choose callbacks on a device bases, only for all devices). 

---

### 评论 #3 — dhruvachak (2023-09-21T16:14:12Z)

Thanks @Thyre for the information.

---
