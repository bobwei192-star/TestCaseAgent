# [Issue]: The rocblas of 6.4.0 release doesn't ship TensileLibrary files for gfx906

> **Issue #4625**
> **状态**: open
> **创建时间**: 2025-04-14T19:58:34Z
> **更新时间**: 2026-01-22T19:06:34Z
> **作者**: ye-luo
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4625

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

Getting an error
```
rocBLAS error: Cannot read /opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary.dat: No such file or directory for GPU arch : gfx906
 List of available TensileLibrary Files : 
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx1101.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx1102.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx1200.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx1030.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx1100.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx1201.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx942.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx90a.dat"
"/opt/rocm-6.4.0/lib/rocblas/library/TensileLibrary_lazy_gfx908.dat"
```
However, Radeon VII gfx906 still listed as deprecated instead of unsupported.
https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus
rocm 6.3 worked fine.

### Operating System

Ubuntu 24.04

### CPU

AMD CPU

### GPU

Radeon VII

### ROCm Version

6.4.0

### ROCm Component

rocBLAS

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (20 条)

### 评论 #1 — ppanchad-amd (2025-04-14T20:06:32Z)

Hi @ye-luo. Internal ticket has been created to look into this issue. Thanks!

---

### 评论 #2 — emerth (2025-04-14T20:42:49Z)

Can confirm. No gfx906 Tensile files.

```
emerth@5600x:~$ find /opt/rocm-6.4.0/ -type f | grep -i gfx906 | grep -i tensile
emerth@5600x:~$

```
Crickets.

---

### 评论 #3 — zichguan-amd (2025-04-22T18:17:46Z)

Hi @ye-luo @emerth, thanks for reporting this, we are looking into it. rocblas still supports gfx906, you can build from source to get the TensileLibrary file for gfx906 for now. You can edit [this line](https://github.com/ROCm/rocBLAS/blob/80e5394d6a68901ce48b03da47b33b1e69d58be7/CMakeLists.txt#L115C12-L115C13) to only build for gfx906, this should speed up the build.

---

### 评论 #4 — slavap (2025-04-26T06:41:29Z)

@zichguan-amd 
and please restore back **deprecated** status for mi50 (it is still supported) in https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus

---

### 评论 #5 — slavap (2025-05-22T04:08:43Z)

Just for anyone who won't be able to build from source. I think it is possible to take TensileLibrary_lazy_gfx906.dat from this package: https://archlinux.org/packages/extra/x86_64/rocblas/

Download it and extract.

---

### 评论 #6 — tdavie (2025-06-03T09:23:55Z)

> Just for anyone who won't be able to build from source. I think it is possible to take TensileLibrary_lazy_gfx906.dat from this package: https://archlinux.org/packages/extra/x86_64/rocblas/
> 
> Download it and extract.

I can confirm that this approach works, at least in inferencing llama cpp on ubuntu 24.04 lts with rocm 6.4. I copied everything that was expected in `/opt/rocm/lib/rocblas/library` and contained the string `gfx906`.

---

### 评论 #7 — 0seba (2025-06-03T18:53:14Z)

This is a very noob question but I spent all day trying to fix it and couldn't. I cloned rocBLAS to the `release/rocm-rel-6.3.0.2` branch and modified the lines to build for gfx906. I am using the command `./install.sh -idc --no_hipblaslt`, everything goes ok until the very end when it tries to install the package where I get the error
```
dpkg: dependency problems prevent configuration of rocblas:
 rocblas depends on hip-runtime-amd (>= 4.5.0); however:
  Package hip-runtime-amd is not installed.
 rocblas depends on rocm-core; however:
  Package rocm-core is not installed.
```
I installed rocm-6.3.3 with amdgpu-installer and works properly in pytorch and llama.cpp so I'd say it is correctly installed, but I don't know how to overwrite the included rocBLAS with the one I'm build. Both the dependencies seem to be installed
```
dpkg -l | grep hip-runtime-amd
ii  hip-runtime-amd6.3.3                           6.3.42134.60303-74~24.04                 amd64        HIP:Heterogenous-computing Interface for Portability
dpkg -l | grep rocm-core
ii  rocm-core6.3.3
```

---

### 评论 #8 — ye-luo (2025-06-04T00:14:26Z)

> > Just for anyone who won't be able to build from source. I think it is possible to take TensileLibrary_lazy_gfx906.dat from this package: https://archlinux.org/packages/extra/x86_64/rocblas/
> > Download it and extract.
> 
> I can confirm that this approach works, at least in inferencing llama cpp on ubuntu 24.04 lts with rocm 6.4. I copied everything that was expected in `/opt/rocm/lib/rocblas/library` and contained the string `gfx906`.

Unfortunately it doesn't work on my ubuntu 24.04.
```
rocBLAS error from hip error code: 'hipErrorInvalidDeviceFunction':98
```
I just manually built rocblas from source
```
cmake -DCMAKE_CXX_COMPILER=amdclang++ -DGPU_TARGETS=gfx906 -DCMAKE_INSTALL_PREFIX=/soft/AMD/rocm-gfx906/7.2.0 ..
```
and then use `export LD_LIBRARY_PATH=/soft/AMD/rocm-gfx906/7.2.0/lib:$LD_LIBRARY_PATH`

---

### 评论 #9 — slavap (2025-06-04T00:20:38Z)

@0seba 
>> I installed rocm-6.3.3 with amdgpu-installer and works properly in pytorch and llama.cpp

Yes, 6.3.3 works and does NOT need any additional manual builds or overrides.

With 6.4.0 you have to fix it with manual build or copy from pre-build package.

---

### 评论 #10 — FantasyMaster85 (2025-06-18T19:26:16Z)

> Just for anyone who won't be able to build from source. I think it is possible to take TensileLibrary_lazy_gfx906.dat from this package: https://archlinux.org/packages/extra/x86_64/rocblas/
> 
> Download it and extract.

Just wanted to chime in and say I can also confirm this works perfectly.  Ubuntu 24.04, AMD Instinct MI60 GPU built llama.cpp and followed these instructions...works perfectly.  I can't believe I spent 2 hours working through a mix of Google and ChatGPT when I just should have started on the Git logged issues.  My fault, lesson learned on that one.  The "old ways" still work! haha.

Thanks for this!!

---

### 评论 #11 — robertofrank-rgb (2025-08-16T04:59:51Z)

> Just for anyone who won't be able to build from source. I think it is possible to take TensileLibrary_lazy_gfx906.dat from this package: https://archlinux.org/packages/extra/x86_64/rocblas/
> 
> Download it and extract.

Has anyone managed to get rocm to work with the mi50 in windows? so could the mi50 card work with rocm in lmstudio for windows or with koboldccp-rocm for windows??

---

### 评论 #12 — narikm (2025-09-09T04:30:37Z)

> Just for anyone who won't be able to build from source. I think it is possible to take TensileLibrary_lazy_gfx906.dat from this package: https://archlinux.org/packages/extra/x86_64/rocblas/
> 
> Download it and extract.

What do you mean? Copy all of 'library' or just the file? The file alone failed for me.

---

### 评论 #13 — slavap (2025-09-09T06:59:30Z)

@narikm 
All files with 906 in filename (156 files in 6.4.0). Pay attention, on archlinux currently 6.4.3 package, which is not compatible with Rocm 6.4.0, so you have to try with Rocm 6.4.3 OR find the url for the previous archlinux package.

<img width="1134" height="1944" alt="Image" src="https://github.com/user-attachments/assets/6713fc30-f412-4f82-8ddd-f2c1035e281b" />

---

### 评论 #14 — MikeLP (2025-09-20T21:38:04Z)

@slavap  Will this trick work for ROCm7?

---

### 评论 #15 — stanus74 (2025-10-28T14:52:40Z)

### Problem

After applying the gfx906 TensileLibrary fix from #4625, llama.cpp still crashes on MI50 
with ROCm 6.4.3. Debug logs show:
```
Cannot find CO in the bundle /opt/rocm-6.4.3/lib/librocsolver.so.0.4.60403 
for ISA: gfx906:sramecc+:xnack-
```

### Question

Are other MI50/MI60 users hitting the same rocSOLVER gfx906 issue in 6.4.3? 
Is there a fix or should we use ROCm 6.3.3 instead?

### Details
- GPU: MI50 (gfx906)
- Ubuntu 22.04, ROCm 6.4.3
- Works fine with ROCm 6.3.3

---

### 评论 #16 — slavap (2025-10-29T00:26:16Z)

@stanus74 
Try to get it from here https://archlinux.org/packages/extra/x86_64/rocsolver/
And let us know if it helps.

---

### 评论 #17 — stanus74 (2025-10-31T19:18:14Z)


After applying the ArchLinux rocblas/rocsolver fix for gfx906, the ArchLinux `librocsolver.so.0.4` (622 MB) fails with linker errors on Ubuntu 22.04:

```
undefined reference to `std::ios_base_library_init()@GLIBCXX_3.4.32'
undefined reference to `__isoc23_strtol@GLIBC_2.38'
```

**Root Cause:** ArchLinux rocsolver compiled with newer C++ runtime incompatible with Ubuntu 22.04.

## Catch-22
- ❌ ROCm 6.4.3 rocsolver → Segfault (missing gfx906 CO)
- ❌ ArchLinux rocsolver → Linker Error (incompatible libc/libstdc++)



---

### 评论 #18 — slavap (2025-10-31T23:13:26Z)

@stanus74 
No wonder, Ubuntu 22 is old, try 24. Or you have to build Rocm by yourself.

---

### 评论 #19 — cpietsch (2025-11-02T20:13:04Z)

> [@slavap](https://github.com/slavap) Will this trick work for ROCm7?

I managed to compile rocblas for rocm7.1
https://drive.google.com/file/d/1Dmao7DRvS2IMkeUXSWDL5OyAU2TzEEZI/view?usp=sharing
copy them to /opt/rocm-7.1.0/lib/rocblas/library/



---

### 评论 #20 — cpietsch (2025-11-02T20:42:43Z)

- used: https://github.com/ROCm/rocBLAS/blob/release/rocm-rel-7.1/CMakeLists.txt#L183
- set TENSILE_VERSION to 4.45.0
- apt-get install -y libmsgpack-cxx-dev
- used: https://github.com/ROCm/rocBLAS with branch 'release/rocm-rel-7.1'
- ./install.sh -a gfx906:xnack-

---
