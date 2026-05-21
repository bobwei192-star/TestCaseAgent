# Help:  how the rocm-cmake build the rocm-hip-sdk deb pakgage?

> **Issue #4381**
> **状态**: closed
> **创建时间**: 2025-02-15T13:34:24Z
> **更新时间**: 2025-03-23T23:51:19Z
> **关闭时间**: 2025-03-23T23:51:17Z
> **作者**: inevity
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4381

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Want to see the code doing the functioning of the deb packaging control files in the ROCm or its submodules dir. 

Such as the deb pkg define and its  depends config.

I find the rocm-hip-sdk string in the source dir, but cannot find any code.



---

## 评论 (5 条)

### 评论 #1 — ppanchad-amd (2025-02-18T15:59:17Z)

Hi @inevity. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — lucbruni-amd (2025-02-25T19:49:12Z)

Hi @inevity,

`rocm-hip-sdk` is a meta package. The package creation code is not public yet. I have confirmed with the team that we are planning to make it public in ROCm 6.4. I suppose you'll need to wait until 6.4 is released in order to see this code.

Does that answer your question? Let me know if I could help further. Thanks!

---

### 评论 #3 — inevity (2025-02-26T08:21:46Z)

I’m just curious—ROCm is much less popular than CUDA, so why does the ROCm team still keep parts of it closed-source, preventing external developers from contributing or modifying it? I’ve been stuck for half a month just trying to run DeepSeek. If I were using an NVIDIA GPU, I heard it wouldn’t be such a waste of time.


---

### 评论 #4 — lucbruni-amd (2025-02-28T14:54:30Z)

I don't have the precise answer to your question, but I know we are working to publicize more with each ROCm release, and become more transparent. We appreciate all the work contributed by external developers.

I'm also sorry to hear that you've run into trouble running DeepSeek. If it's okay with you, would you like to open up a new GitHub issue regarding your problem? We are happy to help.

-Luca

---

### 评论 #5 — lucbruni-amd (2025-03-23T23:51:17Z)

Closing this issue due to inactivity as the question has been answered above.

If you are still experiencing issues with DeepSeek, please feel free to open a new ticket and we'd be happy to help with that. Thanks!

---
