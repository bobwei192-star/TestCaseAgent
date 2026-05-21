# [Issue]: Cannot restrict devices in rootless containers: hsa_init fails with 1008

> **Issue #3144**
> **状态**: closed
> **创建时间**: 2024-05-21T17:52:34Z
> **更新时间**: 2024-07-14T08:53:12Z
> **关闭时间**: 2024-07-12T17:24:06Z
> **作者**: ckastner
> **标签**: Under Investigation, AMD Radeon Pro W7900, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3144

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon Pro W7900** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

On a host with more than one GPU, to perform tests on the cards individually, I followed the instructions regarding [Restricting GPU access](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html#restricting-gpu-access), but in a rootless podman container, I get an `hsa_init` failure. Compare this to other invocations:

- podman run by **user**, all `/dev/dri/renderD*` devices passed in 
  => OK
- podman run by **root**, one single `/dev/dri/renderD128` passed in 
  => OK
- podman run by **user**, one single `/dev/dri/renderD128` passed in 
  =>  `hsa_init` fails  with `1008`

The host is a Debian 12 box running Debian's 6.7.12 kernel with gfx1100, gfx1101, and gfx1102 cards attached. podman is at 4.3.1. I'm using the `rocm/dev-ubuntu-22.04` container image.

My test program is just a minimal example to get the device count: [device_count.c.txt](https://github.com/ROCm/ROCm/files/15389727/device_count.c.txt), but a simple call to `rocminfo` can also trigger this:

```
# rocminfo
ROCk module is loaded
hsa api call failure at: /long_pathname_so_that_rpms_can_package_the_debug_info/src/rocminfo/rocminfo.cc:1250
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
```

I looked at the strace of all three runs of my test program, and it seems that in the failing case (=rootless, with a single device), there is one extra `AMDKFD_IOC_SET_MEMORY_POLICY` ioctl and that one fails:

```
# One device, container run as root
openat(AT_FDCWD, "/sys/devices/virtual/kfd/kfd/topology/generation_id", O_RDONLY) = 4
newfstatat(4, "", {st_mode=S_IFREG|0444, st_size=4096, ...}, AT_EMPTY_PATH) = 0
read(4, "4\n", 4096)                    = 2
close(4)                                = 0
ioctl(3, AMDKFD_IOC_GET_PROCESS_APERTURES_NEW, 0x7fff94eeffc0) = 0
ioctl(3, AMDKFD_IOC_ACQUIRE_VM, 0x7fff94eeffc0) = 0
mmap(NULL, 12288, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_NORESERVE, -1, 0) = 0x7ff8a2a19000
munmap(0x7ff8a2a19000, 4096)            = 0
munmap(0x7ff8a2a1b000, 4096)            = 0
mbind(0x7ff8a2a1a000, 4096, MPOL_DEFAULT, NULL, 0, 0) = 0
munmap(0x7ff8a2a1a000, 4096)            = 0
ioctl(3, AMDKFD_IOC_SET_MEMORY_POLICY, 0x7fff94eeffc0) = 0

# One device, container run as user
openat(AT_FDCWD, "/sys/devices/virtual/kfd/kfd/topology/generation_id", O_RDONLY) = 4
newfstatat(4, "", {st_mode=S_IFREG|0444, st_size=4096, ...}, AT_EMPTY_PATH) = 0
read(4, "4\n", 4096)                    = 2
close(4)                                = 0
ioctl(3, AMDKFD_IOC_GET_PROCESS_APERTURES_NEW, 0x7ffde420d280) = 0
ioctl(3, AMDKFD_IOC_ACQUIRE_VM, 0x7ffde420d280) = 0
mmap(NULL, 12288, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_NORESERVE, -1, 0) = 0x7f6f5b48e000
munmap(0x7f6f5b48e000, 4096)            = 0
munmap(0x7f6f5b490000, 4096)            = 0
mbind(0x7f6f5b48f000, 4096, MPOL_DEFAULT, NULL, 0, 0) = 0
munmap(0x7f6f5b48f000, 4096)            = 0
ioctl(3, AMDKFD_IOC_SET_MEMORY_POLICY, 0x7ffde420d280) = 0
ioctl(3, AMDKFD_IOC_SET_MEMORY_POLICY, 0x7ffde420d280) = -1 ESRCH (No such process)

# Three devices, container run as user
openat(AT_FDCWD, "/sys/devices/virtual/kfd/kfd/topology/generation_id", O_RDONLY) = 4
newfstatat(4, "", {st_mode=S_IFREG|0444, st_size=4096, ...}, AT_EMPTY_PATH) = 0
read(4, "4\n", 4096)                    = 2
close(4)                                = 0
ioctl(3, AMDKFD_IOC_GET_PROCESS_APERTURES_NEW, 0x7fff25a5a540) = 0
ioctl(3, AMDKFD_IOC_ACQUIRE_VM, 0x7fff25a5a540) = 0
ioctl(3, AMDKFD_IOC_ACQUIRE_VM, 0x7fff25a5a540) = 0
ioctl(3, AMDKFD_IOC_ACQUIRE_VM, 0x7fff25a5a540) = 0
mmap(NULL, 12288, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_NORESERVE, -1, 0) = 0x7f029600d000
munmap(0x7f029600d000, 4096)            = 0
munmap(0x7f029600f000, 4096)            = 0
mbind(0x7f029600e000, 4096, MPOL_DEFAULT, NULL, 0, 0) = 0
munmap(0x7f029600e000, 4096)            = 0
ioctl(3, AMDKFD_IOC_SET_MEMORY_POLICY, 0x7fff25a5a540) = 0
ioctl(3, AMDKFD_IOC_SET_MEMORY_POLICY, 0x7fff25a5a540) = 0
ioctl(3, AMDKFD_IOC_SET_MEMORY_POLICY, 0x7fff25a5a540) = 0
```

As an uninformed observer, it's the first and second case that are unusual to me. It's the same invocation, so why is there only ioctl in the rootful case, and more than one in the rootless case?

I guess it's also possible that all three would have been attempted in the rootless single-card case, but the program aborted after the first failure.

### Operating System

Debian 12.5 with backported 6.7 kernel

### CPU

Ryzen 5900X, EPYC 9354P (tested on two systems)

### GPU

AMD Radeon Pro W7900

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

On a system with 2+ GPUs installed and podman as container/image management engine, pull the `rocm/dev-ubuntu-22.04` container image and run the three variations listed above:

```shell
$ sudo apt install podman
$ podman pull rocm/dev-ubuntu-22.04

# count program (below) returns 3 devices -> OK
user@host$ podman run --rm -it --group-add keep-groups --device=/dev/kfd --device=/dev/dri/renderD128 --device=/dev/dri/renderD129 --device=/dev/dri/renderD130 rocm/dev-ubuntu-22.04

# Drop all but one renderD -> hsa_init fails
user@host$ podman run --rm -it --group-add keep-groups --device=/dev/kfd --device=/dev/dri/renderD128  rocm/dev-ubuntu-22.04

# Drop all but one renderD, but run as root -> OK
root@host# podman run --rm -it --group-add keep-groups --device=/dev/kfd --device=/dev/dri/renderD128  rocm/dev-ubuntu-22.04
```

In each container, either run the attached `device_count.c`, or (easier) just run `rocminfo`.

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

[strace_all.txt](https://github.com/ROCm/ROCm/files/15393578/strace_all.txt)
[strace_single.txt](https://github.com/ROCm/ROCm/files/15393579/strace_single.txt)
[strace_single_rootful.txt](https://github.com/ROCm/ROCm/files/15393580/strace_single_rootful.txt)


---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2024-06-24T15:06:36Z)

@ckastner Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — jamesxu2 (2024-07-12T17:24:06Z)

Hi @ckastner ,

Thanks for your detailed issue description - I am able to reproduce your issue. Unfortunately, the functionality you're looking for in a _rootless_ Podman container does not seem possible at the moment - it has been reported previously https://github.com/containers/podman/issues/21454#issuecomment-1920058541.

 A feature request for this specific problem is currently open (https://github.com/ROCm/ROCm/issues/2860) so you can keep an eye on this for updates.

---

### 评论 #3 — ckastner (2024-07-14T08:53:11Z)

Thank you for having looked into this, the cause is clear to me now.

Sorry that I didn't catch the earlier bug report. 

---
