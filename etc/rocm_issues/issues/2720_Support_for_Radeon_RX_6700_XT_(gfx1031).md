# Support for Radeon RX 6700 XT (gfx1031)

> **Issue #2720**
> **状态**: closed
> **创建时间**: 2023-12-15T04:04:10Z
> **更新时间**: 2024-11-13T07:40:53Z
> **关闭时间**: 2024-02-14T02:33:30Z
> **作者**: paralin
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2720

## 描述

There is no TensileLibrary_lazy_gfx1031.dat which causes an error when trying to use rocBLAS with a RX 6700 XT.

How can I get this working with this GPU, or is this currently not supported? If it's not supported, will it be in the near future? Is it just HIP that's not working, or also the opencl integration?

I was able to get the opencl / clBLAST support to work with an older revision of rocm, fwiw.

### Operating System

Ubuntu 22.04.3 LTS

### ROCm Component

rocBLAS

---

## 评论 (6 条)

### 评论 #1 — danielzgtg (2023-12-15T06:48:44Z)

All 6000 GPUs should be (unofficially) supported. Have you tried `export HSA_OVERRIDE_GFX_VERSION=10.3.0` in `.bashrc` or before running the command you are trying to use?

---

### 评论 #2 — sorasoras (2023-12-15T14:07:33Z)

I was able to compiled for gfx1031 but nothing else.
[gfx1031.zip](https://github.com/ROCm/ROCm/files/13686062/gfx1031.zip)
but i really want to build gfx1032 for my friend through

---

### 评论 #3 — nartmada (2024-02-14T02:33:30Z)

Sorry, gfx1031 is not officially supported by AMD.

https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html


---

### 评论 #4 — ccidral (2024-07-17T17:28:48Z)

@nartmada Are there any plans to support gfx1031?

---

### 评论 #5 — wrobelda (2024-09-19T18:18:57Z)

It is supported on Windows as of latest release, so I'd imagine Linux support is coming eventually

---

### 评论 #6 — NatoBoram (2024-11-13T07:40:52Z)

I really puts into question why I bought this particular card if AMD hates it 

---
