# Installing CUDA Toolkit broke ROCm installation

> **Issue #2106**
> **状态**: closed
> **创建时间**: 2023-05-03T23:08:16Z
> **更新时间**: 2024-02-16T20:24:55Z
> **关闭时间**: 2024-02-16T20:24:55Z
> **作者**: kaustubhcs
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2106

## 描述

Command rocminfo was working great until I installed the CUDA Toolkit 12.0
(The server blade has both AMD MI100 and NVIDIA V100 GPUs)
Now cuda works fine but I get the following error when running the command `rocminfo`
```
ktb@server:~ rocminfo
ROCk module is loaded
Unable to open /dev/kfd read-write: Cannot allocate memory
ktb is member of video group
```

Any suggestions?

---

## 评论 (3 条)

### 评论 #1 — nartmada (2024-02-16T16:27:34Z)

Hi @kaustubhcs, have you tried re-installing ROCm to see if it fixes the issue?  Latest ROCm is 6.0.2.  Thanks.

---

### 评论 #2 — kaustubhcs (2024-02-16T17:54:59Z)

Hello @nartmada 
I was able to fix the issue. I updated my OS to Ubuntu 22 and installed latest versions of rocm and CUDA toolkit. 

Works smoothly now. Thanks 

---

### 评论 #3 — nartmada (2024-02-16T20:24:55Z)

@kaustubhcs, glad to hear.  I will close the ticket.  Thanks.

---
