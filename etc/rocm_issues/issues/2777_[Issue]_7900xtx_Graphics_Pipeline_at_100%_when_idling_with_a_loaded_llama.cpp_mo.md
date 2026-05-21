# [Issue]: 7900xtx Graphics Pipeline at 100% when idling with a loaded llama.cpp model

> **Issue #2777**
> **状态**: closed
> **创建时间**: 2024-01-04T19:17:54Z
> **更新时间**: 2024-05-17T19:21:39Z
> **关闭时间**: 2024-05-17T19:21:39Z
> **作者**: sirmo
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2777

## 描述

### Problem Description

Not a major issue, but it would be nice to find a fix for this.

When I load an LLM model into GPU's VRAM, Radeon TOP shows the Graphics Pipeline at 100% all the time. `rocm-smi` shows 100-110 watt power use. I did not observe this behavior with my rx6600 and 6700xt on the same machine. On those RDNA2 GPUs, the Graphics Pipeline goes to 0% when the GPU is idling with the model loaded and occupying the VRAM. 

Exiting koboldCPP (which uses llama.cpp backend) returns the GPU to normal and it then idles at low ~20 watts.

I'm using https://github.com/YellowRoseCx/koboldcpp-rocm with hipBLAS support and I'm using ROCm 6:

```sh

rocm6.0.0/jammy 6.0.0.60000-91~22.04 amd64
```

My system info:

```sh

$ echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
OS:
NAME="Pop!_OS"
VERSION="22.04 LTS"
```

```sh

$ echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
CPU:
model name      : AMD Ryzen 9 3950X 16-Core Processor
```

```sh

$  echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
GPU:
  Name:                    AMD Ryzen 9 3950X 16-Core Processor
  Marketing Name:          AMD Ryzen 9 3950X 16-Core Processor
  Name:                    gfx1100
  Marketing Name:          Radeon RX 7900 XTX
      Name:                    amdgcn-amd-amdhsa--gfx1100


### Operating System

Pop_OS! (based on Ubuntu 22.04 LTS)

### CPU

Ryzen 9 3950X

### GPU

AMD Radeon RX 7900 XTX

### Other

_No response_

### ROCm Version

ROCm 6.0.0

### ROCm Component

ROCm

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (3 条)

### 评论 #1 — kentrussell (2024-01-04T19:20:37Z)

Very likely the same root cause as https://github.com/ROCm/ROCK-Kernel-Driver/issues/153 . Feel free to track that one since there's a bit more traction on it (and I'm bugging the reproducer dev about it too). I'll leave this open though until that one gets resolved and we can confirm if it fixes this too

---

### 评论 #2 — sirmo (2024-01-04T19:26:51Z)

@kentrussell The workaround of setting the env var `GPU_MAX_HW_QUEUES=1` suggested in that thread fixed the issue for me! Thank you so much! 

---

### 评论 #3 — nartmada (2024-02-05T21:23:11Z)

Hi @sirmo, it looks like your issue has been fixed.  Can I close the ticket?  

---
