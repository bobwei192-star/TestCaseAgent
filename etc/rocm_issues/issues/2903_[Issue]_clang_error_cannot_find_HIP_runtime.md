# [Issue]: clang: error: cannot find HIP runtime

> **Issue #2903**
> **状态**: closed
> **创建时间**: 2024-02-17T16:34:33Z
> **更新时间**: 2024-07-01T11:33:02Z
> **关闭时间**: 2024-02-22T02:03:49Z
> **作者**: nuliknol
> **标签**: Under Investigation, ROCm 6.0.0, AMD Radeon RX 7900 XT
> **URL**: https://github.com/ROCm/ROCm/issues/2903

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.0.0** (颜色: #ededed)
- **AMD Radeon RX 7900 XT** (颜色: #ededed)

## 描述

### Problem Description

Just installed ROCM and it doesn't work:

```
user@host :~/gpu/snippets/asm1$ /opt/rocm/bin/hipcc --save-temps -o test1 test1.cpp
clang: error: cannot find HIP runtime; provide its path via '--rocm-path', or pass '-nogpuinc' to build without HIP runtime
clang: error: cannot find HIP runtime; provide its path via '--rocm-path', or pass '-nogpuinc' to build without HIP runtime
user@host :~/gpu/snippets/asm1$ 
```


another attempt:

```
user@host :~/gpu/snippets/asm1$ /opt/rocm/bin/hipcc --rocm-path=/opt/rocm -o test1 test1.cpp
clang: error: cannot find HIP runtime; provide its path via '--rocm-path', or pass '-nogpuinc' to build without HIP runtime
clang: error: cannot find HIP runtime; provide its path via '--rocm-path', or pass '-nogpuinc' to build without HIP runtime
user@host :~/gpu/snippets/asm1$ 
```

I just downloaded amdgpu install and ran:
` amdgpu-install --usecase=graphics,rocm`
 
 didn't do anything extraordinary
 
```
 user@host :~/gpu/snippets/asm1$ /opt/rocm/bin/hipcc --version
HIP version: 5.7.0-0
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.0.2 24012 af27734ed982b52a9f1be0f035ac91726fc697e4)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm/llvm/bin
Configuration file: /opt/rocm-6.0.2/lib/llvm/bin/clang++.cfg

```

### Operating System

Ubuntu 22.04.4 LTS

### CPU

 Ryzen 7 3700X

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.0.0

### ROCm Component

HIP

### Steps to Reproduce

Follow official installation guide

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (6 条)

### 评论 #1 — nuliknol (2024-02-17T21:03:18Z)

additional note:
I have installed aomp-19 , it compiled clean and runs without any issues, so i was able to compile examples with this command:

` DEVICE_LIB_PATH=/home/user/rocm/aomp/amdgcn/bitcode /home/user/rocm/aomp/bin/hipcc --save-temps test1.cpp  -o test1 -std=c++11 -I/home/user/rocm/aomp/include -O1`
 
 So, I thought, maybe I will run the same command with default ROCm installation that is located in /opt? Nope, it doesn't compile:
 
```
 user@host :~/gpu/snippets/asm1$ ROCM_PATH=/opt/rocm DEVICE_LIB_PATH=/opt/rocm-6.0.2/lib/llvm/lib/clang/17.0.0/lib/amdgcn/bitcode /opt/rocm-6.0.2/bin/hipcc --save-temps test1.cpp  -o test1 -std=c++11 -I/opt/rocm-6.0.2/include -O1
clang: error: cannot find HIP runtime; provide its path via '--rocm-path', or pass '-nogpuinc' to build without HIP runtime
clang: error: cannot find HIP runtime; provide its path via '--rocm-path', or pass '-nogpuinc' to build without HIP runtime
user@host :~/gpu/snippets/asm1$ 
```

With AOMP it works, with default ROCm it doesn't.

---

### 评论 #2 — nartmada (2024-02-21T19:08:23Z)

Internal ticket has been created for investigation.

---

### 评论 #3 — nuliknol (2024-02-21T23:40:38Z)

I don't have the issue anymore, maybe that was due to some environment variables ,  which were pointing to wrong location. After a reboot it is compiling fine. We can close the issue @nartmada 

---

### 评论 #4 — nartmada (2024-02-22T02:03:49Z)

@nuliknol, thanks for getting back.  I will close the issue now.

---

### 评论 #5 — manu-web (2024-05-31T18:44:16Z)

Can you give more light on what environment variables are those?


---

### 评论 #6 — minzhezhou (2024-07-01T11:33:01Z)

Got same error here, my .bashrc has:
export PATH=$PATH:/opt/rocm/bin
export HIP_PLATFORM=amd
export USE_ROCM=1
export ROCM_PATH=/opt/rocm

export HIP_CLANG_PATH=/opt/rocm/llvm/bin
export DEVICE_LIB_PATH=/opt/rocm/lib
export LD_LIBRARY_PATH=/opt/rocm/lib:$LD_LIBRARY_PATH

export HIP_PATH=$ROCM_PATH/hip
export ROCM_DEVICE_LIB_PATH=$ROCM_PATH/lib

and hipconfig --cpp_config:
 -D__HIP_PLATFORM_HCC__= -D__HIP_PLATFORM_AMD__= -I/opt/rocm/hip/include -I/opt/rocm-6.1.3/lib/llvm/lib/clang/17

Is there anything wrong here?

---
