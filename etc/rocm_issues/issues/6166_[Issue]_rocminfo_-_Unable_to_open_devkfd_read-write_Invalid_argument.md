# [Issue]: rocminfo - Unable to open /dev/kfd read-write: Invalid argument

> **Issue #6166**
> **状态**: closed
> **创建时间**: 2026-04-21T00:32:28Z
> **更新时间**: 2026-04-24T19:42:21Z
> **关闭时间**: 2026-04-24T19:42:21Z
> **作者**: x1unix
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/6166

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

The `rocminfo` command returns an error:

```
ROCk module is loaded
Unable to open /dev/kfd read-write: Invalid argument
x1unix is member of render group
```



### Operating System

Arch Linux (Linux 6.19.12-arch1-1)

### CPU

AMD Ryzen 5 7600X 6-Core Processor

### GPU

AMD Radeon RX 9070 XT

### ROCm Version

ROCm 7.2.2

### ROCm Component

rocminfo

### Steps to Reproduce

Run `rocminfo`

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

I am not able to run `rocminfo --support` due to a `/dev/kfd` error described in this issue.

### Additional Information

I'm already a member of `render` group:

```
$ stat /dev/kfd
  File: /dev/kfd
  Size: 0         	Blocks: 0          IO Block: 4096   character special file
Device: 0,6	Inode: 524         Links: 1     Device type: 237,0
Access: (0666/crw-rw-rw-)  Uid: (    0/    root)   Gid: (  989/  render)
Access: 2026-04-20 20:07:00.323751788 -0400
Modify: 2026-04-20 20:07:00.323751788 -0400
Change: 2026-04-20 20:07:00.323751788 -0400
 Birth: 2026-04-20 20:06:56.196999863 -0400

$ groups
x1unix sys lock vboxusers wireshark libvirt docker systemd-journal video uucp render kvm input disk wheel adm plugdev

$ lspci | grep VGA
03:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 48 [Radeon RX 9070/9070 XT/9070 GRE] (rev c0)
```

Here is the strace which might be helpful: [strace.txt](https://github.com/user-attachments/files/26996630/strace.txt)

---

## 评论 (6 条)

### 评论 #1 — harkgill-amd (2026-04-22T19:13:26Z)

Hey @x1unix, this looks similiar to https://github.com/ROCm/ROCm/issues/5379 where the same rocminfo `Unable to open /dev/kfd read-write: Invalid argument` showed up in a LXC container w/ Proxmox. To narrow this down to the same issue, could you please confirm if you're running in a baremetal or virtualized environment?

The strace output you shared doesn't seem to contain the actual trace, could you also share that again?

---

### 评论 #2 — x1unix (2026-04-23T04:12:02Z)

@harkgill-amd I'm running the command on bare metal, outside of any VM or container.

I apologize for providing a broken strace, here is a correct one: 

[strace.txt](https://github.com/user-attachments/files/26996625/strace.txt)

---

### 评论 #3 — harkgill-amd (2026-04-23T20:56:17Z)

No worries and thanks for sharing. From your strace, all the permissions/groups seem to be setup correctly. The Linux 6.19.12 kernel is fairly new and not technically supported, this may be leading to conflicting behavior with the amdgpu driver. Could you share the output of `sudo dmesg | egrep 'kfd|amdgpu'` after a reboot and run of `rocminfo`?

---

### 评论 #4 — x1unix (2026-04-24T04:03:49Z)

@harkgill-amd here is the dmesg: [dmesg.txt](https://github.com/user-attachments/files/27036212/dmesg.txt)

Please note that my CPU has an integrated GPU as well.
I have a separate systemd unit to disable it on boot to prevent it appearing in ROCm tooling:

```bash
IGPU="0000:13:00.0" # PCI ID of iGPU

echo none > "/sys/bus/pci/devices/$IGPU/driver_override"
if [[ -L "/sys/bus/pci/devices/$IGPU/driver" ]]; then
  echo "$IGPU" > /sys/bus/pci/drivers/amdgpu/unbind
fi

echo 1 > "/sys/bus/pci/devices/$IGPU/remove"
```

lmk if there is anything else I can provide

---

### 评论 #5 — harkgill-amd (2026-04-24T17:47:24Z)

> I have a separate systemd unit to disable it on boot to prevent it appearing in ROCm tooling:

Ah so this could definitely be a factor here. This device unbinding might be leaving `kfd` in a incorrect state leading to the error when `rocminfo` tries to access it. Can you disable that systemd unit from running (keeping the iGPU enabled), reboot and then try running `rocminfo`?

 If this works, you can always set the `HIP_VISIBLE_DEVICES` environment variable to limit ROCm to just your 9070XT - https://rocm.docs.amd.com/projects/HIP/en/latest/reference/env_variables.html#gpu-isolation-variables

---

### 评论 #6 — x1unix (2026-04-24T19:42:21Z)

@harkgill-amd thanks for suggestion! You were right - enabling the iGPU back helped to solve the issue.

I'm going to close the issue as the problem is resolved.

---
