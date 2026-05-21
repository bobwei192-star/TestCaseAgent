# [Issue]: Undefined reference to ncurses libraries

> **Issue #3574**
> **状态**: closed
> **创建时间**: 2024-08-13T03:13:38Z
> **更新时间**: 2024-08-14T15:57:28Z
> **关闭时间**: 2024-08-14T15:57:28Z
> **作者**: avickars
> **标签**: Under Investigation, AMD Radeon RX 7900 XT, ROCm 6.1.0, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3574

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

When compiling a very simple test program, whenever I link to any external library (i.e. anything not hip), I am getting the following error

```
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `tigetnum@NCURSES6_TINFO_5.0.19991023'
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `del_curterm@NCURSES6_TINFO_5.0.19991023'
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `setupterm@NCURSES6_TINFO_5.0.19991023'
/usr/bin/ld: /opt/rocm/lib/libamd_comgr.so.2: undefined reference to `set_curterm@NCURSES6_TINFO_5.0.19991023'
```



### Operating System

Ubuntu 22.04

### CPU

Ryzen 7900X

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.2.0, ROCm 6.1.0

### ROCm Component

HIP

### Steps to Reproduce

Unpack the following file: [rocm-ex.zip](https://github.com/user-attachments/files/16593948/rocm-ex.zip)

Run the following
```
mkdir build
cmake ..
make
```

Note, currently the cmake file uses opencv libraries as the external library, feel free to change that.

It **will** compile if you remove line 46 of the `CMakeLists.txt` file.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

I suspect it is something extremely small that I am doing incorrectly in my cmake but I can't figure out what it is for the life of me.

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2024-08-13T13:45:33Z)

@avickars Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — schung-amd (2024-08-13T15:17:53Z)

Hi @avickars, I was able to build this on my system without errors by adding a line to tell cmake where the HIP and opencv cmake modules are: `set(CMAKE_PREFIX_PATH /opt/rocm /usr/local/lib/cmake/opencv4/)` as the first line in your dependencies section (i.e. before `if ( ENABLE_HIP )`). The paths you need to pass may vary based on where you've installed HIP and opencv (or any other external library you'd like to use). Let me know if this solves your issue.

---

### 评论 #3 — avickars (2024-08-14T01:28:12Z)

Hi @schung-amd , I am still having this issue however I have determined that it is an issue with Conda.  I am building it inside a conda environment, which appears to be causing the issue  (if I build it outside of conda it builds fine).  Marking this as closed since conda isn't your problem!

---

### 评论 #4 — schung-amd (2024-08-14T15:17:47Z)

Hi @avickars, glad you have found the cause of your issue. Did you mean to reopen this? 

---
