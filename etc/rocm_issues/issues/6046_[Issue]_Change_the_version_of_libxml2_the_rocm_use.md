# [Issue]: Change the version of libxml2 the rocm use.

> **Issue #6046**
> **状态**: closed
> **创建时间**: 2026-03-19T01:46:50Z
> **更新时间**: 2026-04-09T18:24:06Z
> **关闭时间**: 2026-04-09T18:24:06Z
> **作者**: SuGotLand
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/6046

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- zichguan-amd

## 描述

### Problem Description

The ubuntu now use libxml2.so.16 but ROCm only use libxml2.so.2. Should upgrade the shared library ROCm use?

```bash 
$ ldd /opt/rocm-7.2.0/lib/llvm/bin/lld | grep libxml2
        libxml2.so.2 => not found
```
```bash
$ ldconfig -p | grep libxml2
        libxml2.so.16 (libc6,x86-64) => /lib/x86_64-linux-gnu/libxml2.so.16
        libxml2.so.16 (libc6) => /lib/i386-linux-gnu/libxml2.so.16
        libxml2.so (libc6,x86-64) => /lib/x86_64-linux-gnu/libxml2.so
```

### Operating System

Ubuntu 25.10 (Questing Quokka)

### CPU

AMD Ryzen 9 9950X 16-Core Processor

### GPU

Radeon RX 7900 XTX 

### ROCm Version

ROCm 7.2.0

### ROCm Component

llvm-project

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — chejh-amd (2026-03-19T05:49:14Z)

It looks like Ubuntu 25.10 upgraded libxml2 from libxml2.so.2 to libxml2.so.16, and that change breaks ABI compatibility. Because of that, applications depending on the older ABI—like ROCm 7.2.0’s LLVM/lld—can’t find the library they expect.
A simple workaround is to grab the older libxml2 package from Ubuntu 24.04 or Debian, extract just the libxml2.so.2 file, and put it somewhere on your system: `/usr/local/lib/libxml2.so.2`
Then update your LD_LIBRARY_PATH so ROCm can find it: `export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH`
This way, you don’t have to touch the system’s main libxml2 installation, and ROCm can still run with the older ABI it depends on.

---

### 评论 #2 — don-impactable (2026-03-31T05:03:31Z)

Yes, and also need to add this: https://packages.ubuntu.com/noble/amd64/libicu74/download

---

### 评论 #3 — zichguan-amd (2026-04-01T19:08:28Z)

Hi @SuGotLand, ROCm doesn't officially support Ubuntu 25 yet, but you can try TheRock nightly builds at https://rocm.nightlies.amd.com/ which should work on most distros with glibc 2.28 and above. Read more about TheRock at https://github.com/ROCm/TheRock/tree/main

---

### 评论 #4 — zichguan-amd (2026-04-01T19:12:13Z)

With gfx1100 + `7.13.0a20260401` wheels on 25.10 docker, `lld` doesn't depend on `libxml2` anymore.
```
# ldd /.venv/lib/python3.13/site-packages/_rocm_sdk_devel/llvm/bin/lld
        linux-vdso.so.1 (0x00007ffc009e9000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x0000736505540000)
        librocm_sysdeps_z.so.1 => /.venv/lib/python3.13/site-packages/_rocm_sdk_devel/lib/llvm/bin/../../rocm_sysdeps/lib/librocm_sysdeps_z.so.1 (0x0000736505521000)
        librocm_sysdeps_zstd.so.1 => /.venv/lib/python3.13/site-packages/_rocm_sdk_devel/lib/llvm/bin/../../rocm_sysdeps/lib/librocm_sysdeps_zstd.so.1 (0x0000736505450000)
        libLLVM.so.23.0git => /.venv/lib/python3.13/site-packages/_rocm_sdk_devel/lib/llvm/bin/../lib/libLLVM.so.23.0git (0x00007364fe2e0000)
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007364fe051000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007364fdf44000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007364fdf17000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007364fdcd4000)
        /lib64/ld-linux-x86-64.so.2 (0x0000736505557000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007364fdccd000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007364fdcc8000)
```

---
