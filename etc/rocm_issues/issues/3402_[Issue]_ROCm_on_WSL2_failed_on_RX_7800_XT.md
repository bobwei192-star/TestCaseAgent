# [Issue]: ROCm on WSL2 failed on RX 7800 XT

> **Issue #3402**
> **状态**: closed
> **创建时间**: 2024-07-07T10:17:44Z
> **更新时间**: 2026-05-14T19:41:14Z
> **关闭时间**: 2024-07-09T18:07:32Z
> **作者**: LeoooChen
> **标签**: AMD Radeon RX 7900 XT, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3402

## 标签

- **AMD Radeon RX 7900 XT** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

Hello. I am planning to use ROCm 6.1.3 on Windows WSL2. As you can see, the latest 24.6.1 driver released by AMD officially supports the installation and use of ROCm on WSL2, but my RX 7800 XT, which I use, is not listed in the support list. However, my graphics card can use ROCm normally on the Linux platform and run PyTorch projects, so I wanted to see if it would work on WSL2 as well. After following the official guidance, I installed ROCm 6.1.3 on my WSL2, but the rocminfo command seems to fail to run successfully. It gave the following error:

```bash
ROCR: unsupported GPU
hsa api call failure at: ./sources/wsl/tools/rocminfo/rocminfo.cc:1087
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```

Furthermore, I wanted to know the specific details of the error, so I used the 'strace' tool for debugging:

```bash
strace -o rocminfo_trace.txt /opt/rocm/bin/rocminfo
```

I obtained the following results:

```bash
execve("/usr/bin/rocminfo", ["rocminfo"], 0x7ffd5d11cc30 /* 14 vars */) = 0
brk(NULL)                               = 0x585d5daba000
arch_prctl(0x3001 /* ARCH_??? */, 0x7ffd3ed39f80) = -1 EINVAL (Invalid argument)
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76f39a852000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/glibc-hwcaps/x86-64-v3/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/glibc-hwcaps/x86-64-v3", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/glibc-hwcaps/x86-64-v2/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/glibc-hwcaps/x86-64-v2", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls/haswell/x86_64/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls/haswell/x86_64", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls/haswell/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls/haswell", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls/x86_64/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls/x86_64", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/tls", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/haswell/x86_64/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/haswell/x86_64", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/haswell/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/haswell", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/x86_64/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/x86_64", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/home/foreman/build/hsa-runtime-rocr4wsl-amdgpu-1.13.0/../hsa-runtime-rocr4wsl-amdgpu-1.13.0/rocr4wsl", 0x7ffd3ed391a0, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=29383, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 29383, PROT_READ, MAP_PRIVATE, 3, 0) = 0x76f39a84a000
close(3)                                = 0
openat(AT_FDCWD, "/opt/rocm-6.1.3/lib/libhsa-runtime64.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=581064, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 590864, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a7b9000
mprotect(0x76f39a7ca000, 491520, PROT_NONE) = 0
mmap(0x76f39a7ca000, 360448, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x11000) = 0x76f39a7ca000
mmap(0x76f39a822000, 126976, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x69000) = 0x76f39a822000
mmap(0x76f39a842000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x88000) = 0x76f39a842000
mmap(0x76f39a848000, 5136, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x76f39a848000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libstdc++.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=2260296, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 2275520, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a400000
mprotect(0x76f39a49a000, 1576960, PROT_NONE) = 0
mmap(0x76f39a49a000, 1118208, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x9a000) = 0x76f39a49a000
mmap(0x76f39a5ab000, 454656, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1ab000) = 0x76f39a5ab000
mmap(0x76f39a61b000, 57344, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x21a000) = 0x76f39a61b000
mmap(0x76f39a629000, 10432, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x76f39a629000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libgcc_s.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=125488, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 127720, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a799000
mmap(0x76f39a79c000, 94208, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x76f39a79c000
mmap(0x76f39a7b3000, 16384, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1a000) = 0x76f39a7b3000
mmap(0x76f39a7b7000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1d000) = 0x76f39a7b7000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\237\2\0\0\0\0\0"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
pread64(3, "\4\0\0\0 \0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0"..., 48, 848) = 48
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0I\17\357\204\3$\f\221\2039x\324\224\323\236S"..., 68, 896) = 68
newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=2220400, ...}, AT_EMPTY_PATH) = 0
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
mmap(NULL, 2264656, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a000000
mprotect(0x76f39a028000, 2023424, PROT_NONE) = 0
mmap(0x76f39a028000, 1658880, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x28000) = 0x76f39a028000
mmap(0x76f39a1bd000, 360448, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1bd000) = 0x76f39a1bd000
mmap(0x76f39a216000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x215000) = 0x76f39a216000
mmap(0x76f39a21c000, 52816, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x76f39a21c000
close(3)                                = 0
openat(AT_FDCWD, "/usr/lib/wsl/lib/libdxcore.so", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0555, st_size=942048, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 968348, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a6ac000
mmap(0x76f39a70f000, 512000, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x62000) = 0x76f39a70f000
mmap(0x76f39a78c000, 32768, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xde000) = 0x76f39a78c000
mmap(0x76f39a794000, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xe5000) = 0x76f39a794000
mmap(0x76f39a795000, 13980, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x76f39a795000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libelf.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=117400, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76f39a6aa000
mmap(NULL, 119176, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a68c000
mprotect(0x76f39a68f000, 102400, PROT_NONE) = 0
mmap(0x76f39a68f000, 81920, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x76f39a68f000
mmap(0x76f39a6a3000, 16384, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x17000) = 0x76f39a6a3000
mmap(0x76f39a6a8000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1b000) = 0x76f39a6a8000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=940560, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 942344, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a319000
mmap(0x76f39a327000, 507904, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xe000) = 0x76f39a327000
mmap(0x76f39a3a3000, 372736, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x8a000) = 0x76f39a3a3000
mmap(0x76f39a3fe000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xe4000) = 0x76f39a3fe000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=21448, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 16424, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a687000
mmap(0x76f39a688000, 4096, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1000) = 0x76f39a688000
mmap(0x76f39a689000, 4096, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x76f39a689000
mmap(0x76f39a68a000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x76f39a68a000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=14432, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 16424, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a682000
mmap(0x76f39a683000, 4096, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1000) = 0x76f39a683000
mmap(0x76f39a684000, 4096, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x76f39a684000
mmap(0x76f39a685000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x76f39a685000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(3, "", {st_mode=S_IFREG|0644, st_size=108936, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 110776, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f39a666000
mprotect(0x76f39a668000, 98304, PROT_NONE) = 0
mmap(0x76f39a668000, 69632, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x2000) = 0x76f39a668000
mmap(0x76f39a679000, 24576, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x13000) = 0x76f39a679000
mmap(0x76f39a680000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x19000) = 0x76f39a680000
close(3)                                = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76f39a664000
mmap(NULL, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76f39a661000
arch_prctl(ARCH_SET_FS, 0x76f39a661740) = 0
set_tid_address(0x76f39a661a10)         = 5144
set_robust_list(0x76f39a661a20, 24)     = 0
rseq(0x76f39a6620e0, 0x20, 0, 0x53053053) = 0
mprotect(0x76f39a216000, 16384, PROT_READ) = 0
mprotect(0x76f39a680000, 4096, PROT_READ) = 0
mprotect(0x76f39a685000, 4096, PROT_READ) = 0
mprotect(0x76f39a68a000, 4096, PROT_READ) = 0
mprotect(0x76f39a3fe000, 4096, PROT_READ) = 0
mprotect(0x76f39a6a8000, 4096, PROT_READ) = 0
mprotect(0x76f39a78c000, 32768, PROT_READ) = 0
mprotect(0x76f39a7b7000, 4096, PROT_READ) = 0
mprotect(0x76f39a61b000, 45056, PROT_READ) = 0
mprotect(0x76f39a842000, 16384, PROT_READ) = 0
mprotect(0x585d5d21b000, 4096, PROT_READ) = 0
mprotect(0x76f39a88c000, 8192, PROT_READ) = 0
prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
munmap(0x76f39a84a000, 29383)           = 0
openat(AT_FDCWD, "/dev/dxg", O_RDONLY|O_CLOEXEC) = 3
getrandom("\x90\xe0\x8b\xfe\x82\xe4\x89\x51", 8, GRND_NONBLOCK) = 8
brk(NULL)                               = 0x585d5daba000
brk(0x585d5dadb000)                     = 0x585d5dadb000
futex(0x76f39a62977c, FUTEX_WAKE_PRIVATE, 2147483647) = 0
uname({sysname="Linux", nodename="DESKTOP-AUV4FO0", ...}) = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x14, 0x10), 0x7ffd3ed38aa0) = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x14, 0x10), 0x7ffd3ed38aa0) = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x9, 0x18), 0x7ffd3ed37990) = 0
ioctl(3, _IOC(_IOC_READ|_IOC_WRITE, 0x47, 0x9, 0x18), 0x7ffd3ed36d90) = 0
write(2, "ROCR: unsupported GPU\n", 22) = 22
newfstatat(1, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0x2), ...}, AT_EMPTY_PATH) = 0
write(1, "\33[31mhsa api call failure at: ./"..., 76) = 76
write(1, "\33[31mCall returned HSA_STATUS_ER"..., 228) = 228
write(1, "\33[0m", 4)                   = 4
exit_group(4104)                        = ?
+++ exited with 8 +++

```

I would like to know if anyone can help fix this issue?

### Operating System

Windows 11 Professional 23H2

### CPU

12th Gen Intel(R) Core(TM) i5-12600KF   3.70 GHz

### GPU

AMD Radeon RX 7900 XT

### ROCm Version

ROCm 6.1.0

### ROCm Component

rocminfo

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (14 条)

### 评论 #1 — EpicGazel (2024-07-07T10:47:28Z)

You listed two devices (7800XT & 7900XT) and ROCm version (6.1.3 & 6.1.0). 
Try giving `export HSA_OVERRIDE_GFX_VERSION=11.0.0` in wsl2 a shot.

---

### 评论 #2 — LeoooChen (2024-07-07T10:53:47Z)

> You listed two devices (7800XT & 7900XT) and ROCm version (6.1.3 & 6.1.0). Try giving `export HSA_OVERRIDE_GFX_VERSION=11.0.0` in wsl2 a shot.

Sorry, when creating the issue, I had to select the GPU model and ROCm version, but 7800 XT and 6.1.3 were not options, so I had to choose randomly. 

I tried setting the environment variable HSA_OVERRIDE_GFX_VERSION to 11.0.0, but it didn't change anything. I'm wondering if a similar override method is needed under Win11 as well.

---

### 评论 #3 — evshiron (2024-07-07T23:38:40Z)

@chenchong22 

Just curious: did you install that specified AMD driver on the Windows host as well?

---

### 评论 #4 — LeoooChen (2024-07-08T01:40:36Z)

> @chenchong22
> 
> Just curious: did you install that specified AMD driver on the Windows host as well?

Absolutely, I've installed the driver version 24.6.1.

---

### 评论 #5 — evshiron (2024-07-08T08:47:05Z)

> > @chenchong22
> > Just curious: did you install that specified AMD driver on the Windows host as well?
> 
> Absolutely, I've installed the driver version 24.6.1.

I set up ROCm on WSL 2 for my RX 7900 XTX successfully by following the instructions here:

* https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html

I wonder, maybe WSL 2 support comes with [AMD Software: Adrenalin Edition 24.10.21.01 for WSL 2](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-10-21-01-WSL-2.html), not 24.6.1?

EDIT: It looks like, `24.6.1` (june27) was released after `24.10.21.01` (june18) according to their filenames, and we can find `24.10.21.01` in `24.6.1`'s release notes as well. I am confused now.

---

### 评论 #6 — ghost (2024-07-09T13:33:13Z)

it doesn't work for 7800XT currently, I have one as well, same issue, waiting for an update

---

### 评论 #7 — harkgill-amd (2024-07-09T17:47:46Z)

Hi @chenchong22, ROCm on WSL is a beta release and only supports the following GPUs listed in the [compatibility matrices](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html). 

- AMD Radeon RX 7900 XTX
- AMD Radeon RX 7900 XT
- AMD Radeon RX 7900 GRE
- AMD Radeon PRO W7900
- AMD Radeon PRO W7900DS
- AMD Radeon PRO W7800

There will be additional SKUs supported in future releases of ROCm. Unfortunately, overriding the `HSA_OVERRIDE_GFX_VERSION` will not work as WSL relies on the Windows KMD driver rather than the Native Linux's driver implementation.


---

### 评论 #8 — sroller (2025-01-20T21:27:25Z)

another hint that I made a *big* mistake buying an AMD 7800 XT for AI :-(

---

### 评论 #9 — maximilienleclei (2025-03-19T01:48:51Z)

> Hi @chenchong22, ROCm on WSL is a beta release and only supports the following GPUs listed in the [compatibility matrices](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/compatibility/wsl/wsl_compatibility.html). 
> 
> 
> 
> - AMD Radeon RX 7900 XTX
> 
> - AMD Radeon RX 7900 XT
> 
> - AMD Radeon RX 7900 GRE
> 
> - AMD Radeon PRO W7900
> 
> - AMD Radeon PRO W7900DS
> 
> - AMD Radeon PRO W7800
> 
> 
> 
> There will be additional SKUs supported in future releases of ROCm. Unfortunately, overriding the `HSA_OVERRIDE_GFX_VERSION` will not work as WSL relies on the Windows KMD driver rather than the Native Linux's driver implementation.
> 
> 

hey! any plan to cover gpus like the 7800xt? I believe this GPU's architecture is owned by a large percentage of your userbase, and many of us would greatly benefit from rocm working with wsl. thanks!

---

### 评论 #10 — maximilienleclei (2025-05-20T18:49:23Z)

for anyone as impatient as I am, here is a `torch` + `rocm` windows wheel compiled for the 7800 xt: https://drive.proton.me/urls/4QRV647ZXC#RPyLKsYAOHIv

---

### 评论 #11 — maximilienleclei (2025-05-23T14:55:45Z)

GOOD NEWS EVERYONE, the 7800 XT is now supported on WSL. Just make sure to get the 6.4.1 docker image and to install `pytorch-triton-rocm` on top in order to get `torch.compile` and flash attention working!

---

### 评论 #12 — DaanSelen (2026-01-29T22:21:41Z)

Will there ever be support for 6000 series?

---

### 评论 #13 — nicetry001 (2026-05-14T19:34:49Z)

do we have update on 7800xt support? 

---

### 评论 #14 — harkgill-amd (2026-05-14T19:41:14Z)

Yes! Our official ROCm on WSL releases have came with 7800XT support for a while now - see https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html.

The new open source WSL backend (7.2.1+), [librocdxg](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/howto_wsl.html), has 7800XT support as well.

---
