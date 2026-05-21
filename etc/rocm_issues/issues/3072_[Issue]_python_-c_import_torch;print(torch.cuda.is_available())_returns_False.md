# [Issue]: python -c "import torch;print(torch.cuda.is_available())" returns False

> **Issue #3072**
> **状态**: closed
> **创建时间**: 2024-04-29T22:12:36Z
> **更新时间**: 2024-10-16T20:43:13Z
> **关闭时间**: 2024-10-16T20:43:13Z
> **作者**: Looong01
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3072

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

I restrictly Follow the steps [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/ubuntu.html#uninstalling) to install amdgpu driver and rocm-6.1.0 and hip sdk.

rocminfo and rocm-smi and amd-smi run successfully.

But when I try to run pytorch with conda environment, it cannot detect any GPUs.

I also tried docker from rocm/pytorch in docker hub. and it also failed.

I also tried to install all the driver and rocm and hip by using AMDGPU installer, an it also failed.

```
(PyTorch) loong@home:~$ python -c "import torch;print(torch.cuda.is_available())"
False
```

### Operating System

Ubuntu 22.04.4 LTS (Jammy Jellyfish)

### CPU

Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

1. Follow the steps [here](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/ubuntu.html#uninstalling) o install amdgpu driver and rocm-6.1.0 and hip sdk.
2. conda create -n PyTorch python=3.10 -y
3. conda activate PyTorch
4. wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1/torch-2.1.2%2Brocm6.1-cp310-cp310-linux_x86_64.whl
5. wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1/torchvision-0.16.1%2Brocm6.1-cp310-cp310-linux_x86_64.whl
6. wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.1/pytorch_triton_rocm-2.1.0%2Brocm6.1.4d510c3a44-cp310-cp310-linux_x86_64.whl
7. pip install --force-reinstall ./torch-2.1.2%2Brocm6.1-cp310-cp310-linux_x86_64.whl ./torchvision-0.16.1%2Brocm6.1-cp310-cp310-linux_x86_64.whl ./pytorch_triton_rocm-2.1.0%2Brocm6.1.4d510c3a44-cp310-cp310-linux_x86_64.whl
8. python -c "import torch;print(torch.cuda.is_available())"

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

ROCk module version 6.7.0 is loaded
=====================
HSA System Attributes
=====================
Runtime Version:         1.13
Runtime Ext Version:     1.4
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Uuid:                    CPU-XX
  Marketing Name:          Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Vendor Name:             CPU
  Feature:                 None specified
  Profile:                 FULL_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        0(0x0)
  Queue Min Size:          0(0x0)
  Queue Max Size:          0(0x0)
  Queue Type:              MULTI
  Node:                    0
  Device Type:             CPU
  Cache Info:
    L1:                      32768(0x8000) KB
  Chip ID:                 0(0x0)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   4700
  BDFID:                   0
  Internal Node ID:        0
  Compute Unit:            8
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  WatchPts on Addr. Ranges:1
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    65781560(0x3ebbf38) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    65781560(0x3ebbf38) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    65781560(0x3ebbf38) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
  ISA Info:
*******
Agent 2
*******
  Name:                    gfx1100
  Uuid:                    GPU-85631fd855c9cea1
  Marketing Name:          Radeon RX 7900 XTX
  Vendor Name:             AMD
  Feature:                 KERNEL_DISPATCH
  Profile:                 BASE_PROFILE
  Float Round Mode:        NEAR
  Max Queue Number:        128(0x80)
  Queue Min Size:          64(0x40)
  Queue Max Size:          131072(0x20000)
  Queue Type:              MULTI
  Node:                    1
  Device Type:             GPU
  Cache Info:
    L1:                      32(0x20) KB
    L2:                      6144(0x1800) KB
    L3:                      98304(0x18000) KB
  Chip ID:                 29772(0x744c)
  ASIC Revision:           0(0x0)
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2482
  BDFID:                   768
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  WatchPts on Addr. Ranges:4
  Coherent Host Access:    FALSE
  Features:                KERNEL_DISPATCH
  Fast F16 Operation:      TRUE
  Wavefront Size:          32(0x20)
  Workgroup Max Size:      1024(0x400)
  Workgroup Max Size per Dimension:
    x                        1024(0x400)
    y                        1024(0x400)
    z                        1024(0x400)
  Max Waves Per CU:        32(0x20)
  Max Work-item Per CU:    1024(0x400)
  Grid Max Size:           4294967295(0xffffffff)
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)
    y                        4294967295(0xffffffff)
    z                        4294967295(0xffffffff)
  Max fbarriers/Workgrp:   32
  Packet Processor uCode:: 92
  SDMA engine uCode::      20
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25149440(0x17fc000) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 3
      Segment:                 GROUP
      Size:                    64(0x40) KB
      Allocatable:             FALSE
      Alloc Granule:           0KB
      Alloc Recommended Granule:0KB
      Alloc Alignment:         0KB
      Accessible by all:       FALSE
  ISA Info:
    ISA 1
      Name:                    amdgcn-amd-amdhsa--gfx1100
      Machine Models:          HSA_MACHINE_MODEL_LARGE
      Profiles:                HSA_PROFILE_BASE
      Default Rounding Mode:   NEAR
      Default Rounding Mode:   NEAR
      Fast f16:                TRUE
      Workgroup Max Size:      1024(0x400)
      Workgroup Max Size per Dimension:
        x                        1024(0x400)
        y                        1024(0x400)
        z                        1024(0x400)
      Grid Max Size:           4294967295(0xffffffff)
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)
        y                        4294967295(0xffffffff)
        z                        4294967295(0xffffffff)
      FBarrier Max Size:       32
*** Done ***

### Additional Information

OS:
NAME="Ubuntu"
VERSION="22.04.4 LTS (Jammy Jellyfish)"

CPU:
model name      : Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz

GPU:
  Name:                    Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Marketing Name:          Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Name:                    gfx1100
  Marketing Name:          Radeon RX 7900 XTX
      Name:                    amdgcn-amd-amdhsa--gfx1100

---

## 评论 (16 条)

### 评论 #1 — briansp2020 (2024-04-29T22:32:59Z)

This may help
https://github.com/ROCm/pytorch/issues/1398#issuecomment-2078615130

---

### 评论 #2 — Looong01 (2024-04-29T23:14:25Z)

> This may help [ROCm/pytorch#1398 (comment)](https://github.com/ROCm/pytorch/issues/1398#issuecomment-2078615130)

No help.

---

### 评论 #3 — albcunha (2024-05-02T16:11:21Z)

I got the same problem. 
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0`
does not work.

`pip3 install --pre --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.0`
works! Maybe you need to  `--force-reinstall` your package.



---

### 评论 #4 — ppanchad-amd (2024-05-07T17:15:41Z)

@Looong01 Have you tried --force-reinstall to see if it works? Thanks!

---

### 评论 #5 — Looong01 (2024-05-08T12:11:51Z)

> @Looong01 Have you tried --force-reinstall to see if it works? Thanks!

I tried and no help.

---

### 评论 #6 — Looong01 (2024-05-08T12:12:02Z)

> I got the same problem. `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0` does not work.
> 
> `pip3 install --pre --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.0` works! Maybe you need to `--force-reinstall` your package.

I tried and no help. Thanks anyway

---

### 评论 #7 — Looong01 (2024-05-08T12:20:07Z)

Btw, I have 2 user accounts(A and B) in my system(Ubuntu 22.04.4). All of those have sudo Permissions. A runs this successfully and returns True, but B doesn't.

And I think this may help:
```
$ getent group
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog,A
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:
news:x:9:
uucp:x:10:
man:x:12:
proxy:x:13:
kmem:x:15:
dialout:x:20:
fax:x:21:
voice:x:22:
cdrom:x:24:A
floppy:x:25:
tape:x:26:
sudo:x:27:A,B
audio:x:29:
dip:x:30:A
www-data:x:33:
backup:x:34:
operator:x:37:
list:x:38:
irc:x:39:
src:x:40:
gnats:x:41:
shadow:x:42:
utmp:x:43:
video:x:44:A
sasl:x:45:
plugdev:x:46:A
staff:x:50:
games:x:60:
users:x:100:
nogroup:x:65534:
systemd-journal:x:101:
systemd-network:x:102:
systemd-resolve:x:103:
messagebus:x:104:
systemd-timesync:x:105:
input:x:106:
sgx:x:107:
kvm:x:108:
render:x:109:A
lxd:x:110:A
_ssh:x:111:
crontab:x:112:
syslog:x:113:
uuidd:x:114:
tcpdump:x:115:
tss:x:116:
landscape:x:117:
fwupd-refresh:x:118:
A:x:1000:
B:x:1001:
```

---

### 评论 #8 — alexschroeter (2024-05-11T12:46:13Z)

It looks to me like user B is not in the `render` group. At some point the user needed to be in the render and/or video group. I would suspect that this is the reason why user B is not working while user A is.

For pytorch I only use the instructions found on their page (https://pytorch.org/get-started/locally/), but I don't have your GPU.

---

### 评论 #9 — nairboon (2024-05-22T17:54:25Z)

`sudo usermod -a -G render,video B` or if logged in as user B: `sudo usermod -a -G render,video $LOGNAME`

---

### 评论 #10 — Looong01 (2024-06-14T15:15:43Z)

> `sudo usermod -a -G render,video B` or if logged in as user B: `sudo usermod -a -G render,video $LOGNAME`

Thank u very much! It works.
Btw, Could u AMD engineer add this command```sudo usermod -a -G render,video $LOGNAME``` and instructions in the docs of ROCm installation, like "https://rocm.docs.amd.com/"? Bc it is really confused for us to find the problems by ourselves. It has been there for half year!

---

### 评论 #11 — Looong01 (2024-10-15T17:17:11Z)

Hello, I keep encounter this problem in Docker.
1. I use ```rocm/pytorch:rocm6.1.3_ubuntu22.04_py3.10_pytorch_release-2.1.2``` this image which is pulled from docker hub. 
2. Run this image by ```docker run -itd --name rocm6.1.3 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device=/dev/kfd --device=/dev/dri --group-add video --group-add render --ipc=host --shm-size 32G rocm/pytorch:rocm6.1.3_ubuntu22.04_py3.10_pytorch_release-2.1.2```
3. Get in this container, Attach the shell. Then ```python -c "import torch; print(torch.cuda.is_available())"```.
4. Get ```False```

---

### 评论 #12 — ppanchad-amd (2024-10-15T17:37:37Z)

Hi @Looong01. Internal ticket has been created to investigate your issue. Thanks!

---

### 评论 #13 — Looong01 (2024-10-15T18:18:52Z)

I run my docker by rootless mode.

---

### 评论 #14 — jamesxu2 (2024-10-15T18:30:27Z)

Hi @Looong01, 

Can you try running docker without rootless mode? You might be running into a groups-related issue in rootless mode because of the way group IDs are remapped; so your container may think it's in render/video groups but those map to different groups from the perspective of the host (and therefore deny you access to the GPU hardware).

There is a somewhat similar limitation with Podman running in rootless mode discussed here: https://github.com/ROCm/ROCm/issues/3144

When I try running these commands: https://github.com/ROCm/ROCm/issues/3072#issuecomment-2414587611 in a rootful docker, there is no issue and my Pytorch reports:
```
# python -c "import torch; print(torch.cuda.is_available())"
True
```

---

### 评论 #15 — Looong01 (2024-10-15T19:01:18Z)

> Hi @Looong01,
> 
> Can you try running docker without rootless mode? You might be running into a groups-related issue in rootless mode because of the way group IDs are remapped; so your container may think it's in render/video groups but those map to different groups from the perspective of the host (and therefore deny you access to the GPU hardware).
> 
> There is a somewhat similar limitation with Podman running in rootless mode discussed here: #3144
> 
> When I try running these commands: [#3072 (comment)](https://github.com/ROCm/ROCm/issues/3072#issuecomment-2414587611) in a rootful docker, there is no issue and my Pytorch reports:
> 
> ```
> # python -c "import torch; print(torch.cuda.is_available())"
> True
> ```

Yeah, ur right. In docker without rootless mode, it works. But rootless mode doesn't. While rootless mode is necessary for me. Could u pls help to solve this problem?

---

### 评论 #16 — jamesxu2 (2024-10-16T17:33:02Z)

There are a number of existing issues discussing the use of ROCm in a rootless container. For example:

1. https://github.com/ROCm/ROCm/issues/1549
2. https://github.com/ROCm/ROCm-docker/issues/90

Please have a look at those discussions and let us know if that helps you. 

---
