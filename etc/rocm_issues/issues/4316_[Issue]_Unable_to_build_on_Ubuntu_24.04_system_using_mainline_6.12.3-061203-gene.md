# [Issue]: Unable to build on Ubuntu 24.04 system using mainline 6.12.3-061203-generic kernel

> **Issue #4316**
> **状态**: closed
> **创建时间**: 2025-01-30T01:39:46Z
> **更新时间**: 2025-03-10T10:30:32Z
> **关闭时间**: 2025-01-30T21:04:21Z
> **作者**: melroy89
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.3.0
> **URL**: https://github.com/ROCm/ROCm/issues/4316

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.3.0** (颜色: #ededed)

## 描述

### Problem Description

amdgpu-dkms build fails due to (please see `make.log` below!!): 

```
In file included from ./include/linux/rhashtable-types.h:12,
                 from ./include/linux/sched/ext.h:15,
                 from ./include/linux/sched.h:85,
                 from ./include/linux/dma-fence.h:21,
                 from /tmp/amd.jcuhIcCy/include/linux/dma-resv.h:43,
                 from /tmp/amd.jcuhIcCy/amd/amdkcl/dma-buf/dma-resv.c:37:
./include/linux/alloc_tag.h:212:2: error: expected identifier or ‘(’ before ‘{’ token
  212 | ({                                                                      \
      |  ^
./include/linux/slab.h:1053:49: note: in expansion of macro ‘alloc_hooks’
 1053 | #define kvrealloc(...)                          alloc_hooks(kvrealloc_noprof(__VA_ARGS__))
      |                                                 ^~~~~~~~~~~
/tmp/amd.jcuhIcCy/include/kcl/kcl_slab.h:42:14: note: in expansion of macro ‘kvrealloc’
   42 | extern void *kvrealloc(const void *p, size_t oldsize, size_t newsize, gfp_t flags);
      |              ^~~~~~~~~
  CC [M]  /tmp/amd.jcuhIcCy/amd/amdkcl/kcl_page_alloc.o
```


### Operating System

Linux Mint 22.1 (Ubuntu 24.04) kernel v6.12.3

### CPU

AMD Ryzen Threadripper 7960X 24-Cores

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.3.2

### ROCm Component

_No response_

### Steps to Reproduce

- Use Ubuntu 24.04
- Use the [latest mainline kernel](https://kernel.ubuntu.com/mainline/) (including headers and modules): v6.12.3-061203-generic
- Using gcc v14
- Following: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html#rocm-install-quick

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

[make.log](https://github.com/user-attachments/files/18596210/make.log)

---

## 评论 (6 条)

### 评论 #1 — ppanchad-amd (2025-01-30T15:28:20Z)

Hi @melroy89. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — darren-amd (2025-01-30T19:30:34Z)

Hi @melroy89,

We currently do not support kernel version 6.12.3 on Ubuntu 24.04. Please refer to our [Supported Distributions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-distributions), indicating support for kernel version 6.8 [GA] and 6.11 [HWE] for Ubuntu 24.04. Thanks!

---

### 评论 #3 — melroy89 (2025-01-30T21:04:22Z)

owh I see.

---

### 评论 #4 — melroy89 (2025-01-30T21:05:05Z)

However, at some point in time this kernel release will become the new LTS kernel. So at the end, you still might want to investigate the problem.

---

### 评论 #5 — melroy89 (2025-01-30T22:35:29Z)

Also also. You can't select ROCm v6.3.2 in the issue template. Just saying. I needed to update the issue description later. 

---

### 评论 #6 — e-minguez (2025-03-10T10:30:31Z)

Just in case this same error is happening if you are trying to make this work on Debian 12 with backported kernel (6.12)

---
