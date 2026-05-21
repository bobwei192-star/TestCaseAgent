# How can we figure out which devices we have to pass to Docker for individual MI300 partitions?

> **Issue #4261**
> **状态**: closed
> **创建时间**: 2025-01-15T07:13:49Z
> **更新时间**: 2025-01-24T05:55:00Z
> **关闭时间**: 2025-01-24T05:55:00Z
> **作者**: maxweiss
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4261

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

Individual GPUs can be mounted in Docker containers with the --device switch (as described here: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/docker.html#docker-restrict-gpus).
To figure out which device path belongs to which GPU, we get the BDF id of each GPU via ROCm and then compare it with the files in /dev/dri/by-path.

Unfortunately, ROCm and AMD-SMI report the same BDF id for all partitions of a MI300 (which makes sense, because there are no individual PCI devices for the partitions).

How can we figure out which device/path we have to use to mount individual partitions in Docker? Is there another API function that we can use?

This is from our host with one MI300 (in TPX mode):
```
============================ ROCm System Management Interface ============================
======================================= PCI Bus ID =======================================
GPU[0]		: PCI Bus: 0000:01:00.0
GPU[1]		: PCI Bus: 0000:01:00.1
GPU[2]		: PCI Bus: 0000:01:00.2
==========================================================================================
================================== End of ROCm SMI Log ===================================

$ ls -l /dev/dri/by-path/
total 0
lrwxrwxrwx 1 root root  8 Dec 11 01:56 pci-0000:01:00.0-card -> ../card1
lrwxrwxrwx 1 root root 13 Dec 11 01:56 pci-0000:01:00.0-render -> ../renderD128
lrwxrwxrwx 1 root root  8 Dec 10 14:39 pci-0000:c2:00.0-card -> ../card0
lrwxrwxrwx 1 root root  8 Dec 11 01:56 platform-amdgpu_xcp_0-card -> ../card2
lrwxrwxrwx 1 root root 13 Dec 11 01:56 platform-amdgpu_xcp_0-render -> ../renderD129
lrwxrwxrwx 1 root root  8 Dec 11 01:56 platform-amdgpu_xcp_1-card -> ../card3
lrwxrwxrwx 1 root root 13 Dec 11 01:56 platform-amdgpu_xcp_1-render -> ../renderD130
lrwxrwxrwx 1 root root  8 Dec 11 01:56 platform-amdgpu_xcp_2-card -> ../card4
lrwxrwxrwx 1 root root 13 Dec 11 01:56 platform-amdgpu_xcp_2-render -> ../renderD131
lrwxrwxrwx 1 root root  8 Dec 11 01:56 platform-amdgpu_xcp_3-card -> ../card5
lrwxrwxrwx 1 root root 13 Dec 11 01:56 platform-amdgpu_xcp_3-render -> ../renderD132
lrwxrwxrwx 1 root root  8 Dec 11 01:56 platform-amdgpu_xcp_4-card -> ../card6
lrwxrwxrwx 1 root root 13 Dec 11 01:56 platform-amdgpu_xcp_4-render -> ../renderD133
lrwxrwxrwx 1 root root  8 Dec 11 01:56 platform-amdgpu_xcp_5-card -> ../card7
lrwxrwxrwx 1 root root 13 Dec 11 01:56 platform-amdgpu_xcp_5-render -> ../renderD134
lrwxrwxrwx 1 root root  8 Dec 11 01:56 platform-amdgpu_xcp_6-card -> ../card8
lrwxrwxrwx 1 root root 13 Dec 11 01:56 platform-amdgpu_xcp_6-render -> ../renderD135
```
It looks like if

/dev/dri/renderD128 is partition 0
/dev/dri/renderD129 is partition 1
/dev/dri/renderD130 is partition 2
/dev/dri/renderD131 etc. are just "blanks"

Can we just assume that if partition 0 is /dev/dri/renderD128, then partition 1 must be /dev/dri/renderD129 etc.?

Thank you!

---

## 评论 (3 条)

### 评论 #1 — ppanchad-amd (2025-01-15T14:00:15Z)

Hi @maxweiss. Internal ticket has been created to assist with your issue. Thanks!

---

### 评论 #2 — jamesxu2 (2025-01-20T16:24:19Z)

Hi @maxweiss, 
`ls /sys/class/kfd/kfd/topology/nodes/` will show you what nodes are available, and you can grep for drm_render_minor in their properties to see what renderDXXX should be used. This will return some number >= 128 if it's a usable render node (i.e. a partition).



For example:

```shell
$ cat /sys/class/kfd/kfd/topology/nodes/2/properties | grep drm_render_minor
drm_render_minor 128
$ cat /sys/class/kfd/kfd/topology/nodes/3/properties | grep drm_render_minor
drm_render_minor 136
$ cat /sys/class/kfd/kfd/topology/nodes/4/properties | grep drm_render_minor
drm_render_minor 144
$ cat /sys/class/kfd/kfd/topology/nodes/5/properties | grep drm_render_minor
drm_render_minor 152
```

You can then pass this device to docker using the device switch.

There are two caveats though:
1. Regarding the BDF IDs reported by rocm-smi for partitions, there is some hidden complexity that you may want to be aware of, as discussed in https://github.com/ROCm/rocm_smi_lib/issues/208
2. rocm-smi will not correctly report the GFX utilization when you pass through a partition. In TPX for example, if you pass one partition to a docker image and load it to 100%, you'll see that running rocm-smi outside the container shows 33% utilization for all 3 partitions. This is not correct, and only 2/6 XCDs on the MI300A are actually loaded. I'm looking into that issue now.
3. rocm-smi in the container may not report the presence of any GPUs but they are still usable. That is also being looked into by the team. rocminfo should correctly report the partitions you've passed through.

---

### 评论 #3 — maxweiss (2025-01-24T05:54:57Z)

Thank you @jamesxu2! This helps a lot!

---
