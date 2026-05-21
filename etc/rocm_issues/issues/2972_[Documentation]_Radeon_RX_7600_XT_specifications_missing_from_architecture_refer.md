# [Documentation]: Radeon RX 7600 XT specifications missing from architecture reference

> **Issue #2972**
> **状态**: closed
> **创建时间**: 2024-03-21T22:41:57Z
> **更新时间**: 2024-12-30T19:43:13Z
> **关闭时间**: 2024-03-22T01:51:35Z
> **作者**: garrdbyrd
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2972

## 描述

### Description of errors

The Radeon RX 7600 XT specifications are missing from architecture reference. The following specifications should be correct and can just be pasted into `docs/reference/gpu-arch/gpu-arch-spec-overview.rst` at line ~468.

```
          - Radeon RX 7600 XT
          - RDNA3
          - gfx1102
          - 16 GiB
          - 32
          - 32
          - 128 KiB
          - 32 MiB
          - 2 MiB
          - 256 KiB
          - 32 KiB
          - 16 KiB
          - 32 KiB
          - 256 KiB
          - 20 KiB
```
![radeon7600xt-missing](https://github.com/ROCm/ROCm/assets/24244993/5bc386c0-e09e-4a43-af4c-1cd250a20876)


### Attach any links, screenshots, or additional evidence you think will be helpful.

_No response_

---

## 评论 (4 条)

### 评论 #1 — nartmada (2024-03-22T01:47:29Z)

Hi @garrdbyrd, Radeon RX 7600 XT is not a supported GPU.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html



---

### 评论 #2 — garrdbyrd (2024-03-22T06:15:36Z)

Understood, but then why are 7600, 7700 XT, and 7800 XT listed?

---

### 评论 #3 — DarkStar-DarkGold (2024-07-25T09:54:09Z)

> 明白了，但为什么会列出 7600、7700 XT 和 7800 XT？
hi，Is RX7600  supported by rocm?



---

### 评论 #4 — winfriedgerlach (2024-12-30T19:41:15Z)

@DarkStar-DarkGold at least RX 7600 is listed under [Windows supported GPUs](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html), see also #2788

---
