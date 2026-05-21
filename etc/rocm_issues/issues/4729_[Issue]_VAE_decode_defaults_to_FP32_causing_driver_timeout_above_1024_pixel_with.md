# [Issue]: VAE decode defaults to FP32 causing driver timeout above 1024 pixel with default MIOPEN_FIND_MODE

> **Issue #4729**
> **状态**: open
> **创建时间**: 2025-05-09T11:33:03Z
> **更新时间**: 2026-01-11T09:36:47Z
> **作者**: OrsoEric
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4729

## 标签

- **Under Investigation** (颜色: #0052cc)

## 描述

### Problem Description

There is a persistent issue where the VAE decode stage of any ComfyUI workflow will use outsided VRAM compared to other modules and cause black screen, driver timeout, system crashes.

I can get most other nodes to run and accelerate fine, VAE encode, KSampler, CLIP, and even GGUF models in the latest version of ComfyUI now work in Q4 to Q8 quantization, but fixing the VAE decode has been elusive.

I'm using Adrenaline 25.5.1 but it's an issue that was present in previous versions of Adrenaline as well. I'm using ROCm 6.3.4

I suspect it has something to do with ROCm defaulting to FP32 while the models themselves should be BF16, causing an enormous VRAM overhead. EDIT: I'm not sure it's a FP32/VRAM issue. In mode 3 it fails while well under VRAM limit. 

I have been investigating the issue for a while
- [minimum workflow that replicates the issue](https://raw.githubusercontent.com/OrsoEric/HOWTO-ComfyUI/Master/workflows/bug-vae-decode-adrenaline-crash.png)
- [Additional information](https://github.com/OrsoEric/HOWTO-ComfyUI#bug-vae-defaults-to-fp32-instead-of-bf16)

________________________________________________________________

Default MIOPEN_FIND_MODE (5?) FAIL

```
soraka@TowerOfBabel:~$ python3 ComfyUI/main.py
```

Behaviour:

- 1024px both VAE encode and VAE decode work fine
- 1536px VAE encode works fine.
- 1536px VAE decode causes a driver timeout at 1536px filling the 24GB VRAM buffer

________________________________________________________________

MIOPEN_FIND_MODE=2 WORKS

Someone online suggested exporting a variable before executing ComfyUI

```
soraka@TowerOfBabel:~$ export MIOPEN_FIND_MODE=2
soraka@TowerOfBabel:~$ python3 ComfyUI/main.py
```

Behaviour:

- 1536px both VAE encode and VAE decode work fine using around 13GB VRAM
- 2048px both VAE encode and VAE decode work fine using around 18GB VRAM

![Image](https://github.com/user-attachments/assets/313d553d-b6a8-45dd-bdfa-80713595000d)

________________________________________________________________

MIOPEN_FIND_MODE=3 FAIL

This morning I tried mode 3, it fails, but in a different way from the default

```
soraka@TowerOfBabel:~$ export MIOPEN_FIND_MODE=3
soraka@TowerOfBabel:~$ python3 ComfyUI/main.py
```

Behaviour:

- 1536px both VAE encode and VAE decode work fine
- 2048px VAE encode works fine.
- 2048px VAE decode causes a driver timeout while using 16GB VRAM

![Image](https://github.com/user-attachments/assets/f0372de0-4a0d-4c99-a5f1-87fc805050f0)

________________________________________________________________

[I read documentation about this flag](https://rocmdocs.amd.com/projects/MIOpen/en/latest/how-to/find-and-immediate.html#find-modes)

It seems to change the way it finds the acceleration. The default seems mode 5? Mode 2 doesn't cause driver crashes. It seems to suggest worse performance, but I found no performance degradation so far, and other workflows seem to still work fine so far.

EDIT: It does seem somewhat slower E.g. 80s->90s but it's hard to tell for sure. There is lots of variance involved in running ComfyUI.

I don't really understand how HIP and ROCm do the acceleration, so I'm not sure why mode 5 causes issues with VAE decode, while mode 2 doesn't, so I opened a bug report with all the information I collected up to this point, hoping for it to be of some use in case it's a misbehaviour of mode 5, or the underlying issue is somewhere else.



### Operating System

22.04.5 LTS (Jammy Jellyfish)

### CPU

13th Gen Intel(R) Core(TM) i7-13700F

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

rocm6.3.4

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

soraka@TowerOfBabel:~$ rocminfo
WSL environment detected.
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
Runtime Ext Version:     1.6
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
  Name:                    13th Gen Intel(R) Core(TM) i7-13700F
  Uuid:                    CPU-XX
  Marketing Name:          13th Gen Intel(R) Core(TM) i7-13700F
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
    L1:                      49152(0xc000) KB
  Chip ID:                 0(0x0)
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Memory Properties:
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: FINE GRAINED
      Size:                    32779776(0x1f42e00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    32779776(0x1f42e00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 3
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    32779776(0x1f42e00) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 4
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    32779776(0x1f42e00) KB
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
  Marketing Name:          AMD Radeon RX 7900 XTX
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
  Cacheline Size:          64(0x40)
  Max Clock Freq. (MHz):   2482000
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
  Coherent Host Access:    FALSE
  Memory Properties:
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
  Packet Processor uCode:: 542
  SDMA engine uCode::      24
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25101988(0x17f06a4) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    25101988(0x17f06a4) KB
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
soraka@TowerOfBabel:~$ python3 -m torch.utils.collect_env
/usr/lib/python3.10/runpy.py:126: RuntimeWarning: 'torch.utils.collect_env' found in sys.modules after import of package 'torch.utils', but prior to execution of 'torch.utils.collect_env'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
Collecting environment information...
/home/soraka/.local/lib/python3.10/site-packages/torch/cuda/__init__.py:645: UserWarning: Can't initialize amdsmi - Error code: 34
  warnings.warn(f"Can't initialize amdsmi - Error code: {e.err_code}")
PyTorch version: 2.4.0+rocm6.3.4.git7cecbf6d
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.3.42134-a9a80e791

OS: Ubuntu 22.04.5 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0] (64-bit runtime)
Python platform: Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon RX 7900 XTX (gfx1100)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.3.42134
MIOpen runtime version: 3.3.0
Is XNNPACK available: True

CPU:
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        39 bits physical, 48 bits virtual
Byte Order:                           Little Endian
CPU(s):                               24
On-line CPU(s) list:                  0-23
Vendor ID:                            GenuineIntel
Model name:                           13th Gen Intel(R) Core(TM) i7-13700F
CPU family:                           6
Model:                                183
Thread(s) per core:                   2
Core(s) per socket:                   12
Socket(s):                            1
Stepping:                             1
BogoMIPS:                             4224.01
Flags:                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid pni pclmulqdq vmx ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves avx_vnni umip waitpkg gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear serialize flush_l1d arch_capabilities
Virtualization:                       VT-x
Hypervisor vendor:                    Microsoft
Virtualization type:                  full
L1d cache:                            576 KiB (12 instances)
L1i cache:                            384 KiB (12 instances)
L2 cache:                             24 MiB (12 instances)
L3 cache:                             30 MiB (1 instance)
Vulnerability Gather data sampling:   Not affected
Vulnerability Itlb multihit:          Not affected
Vulnerability L1tf:                   Not affected
Vulnerability Mds:                    Not affected
Vulnerability Meltdown:               Not affected
Vulnerability Mmio stale data:        Not affected
Vulnerability Reg file data sampling: Mitigation; Clear Register File
Vulnerability Retbleed:               Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow:   Not affected
Vulnerability Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl and seccomp
Vulnerability Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:             Mitigation; Enhanced / Automatic IBRS; IBPB conditional; RSB filling; PBRSB-eIBRS SW sequence; BHI BHI_DIS_S
Vulnerability Srbds:                  Not affected
Vulnerability Tsx async abort:        Not affected

Versions of relevant libraries:
[pip3] alias-free-torch==0.0.6
[pip3] clip-anytorch==2.6.0
[pip3] dctorch==0.1.2
[pip3] ema-pytorch==0.7.7
[pip3] kokoro-onnx==0.4.2
[pip3] mypy-extensions==1.0.0
[pip3] numpy==1.26.4
[pip3] onnxruntime==1.21.1
[pip3] pytorch-triton-rocm==3.0.0+rocm6.3.4.git75cc27c2
[pip3] torch==2.4.0+rocm6.3.4.git7cecbf6d
[pip3] torch-stoi==0.2.3
[pip3] torch-time-stretch==1.0.3
[pip3] torchaudio==2.4.0+rocm6.3.4.git69d40773
[pip3] torchdiffeq==0.2.5
[pip3] torchsde==0.2.6
[pip3] torchvision==0.19.0+rocm6.3.4.gitfab84886
[pip3] triton==3.2.0
[conda] Could not collect

---

## 评论 (31 条)

### 评论 #1 — Matthew-Jenkins (2025-05-12T05:04:06Z)

I tried rocm 6.4 with comfy. There is some kind of regression here. Even using PYTORCH_HIP_ALLOC_CONF=expandable_segments:True python main.py --use-split-cross-attention --fp16-vae causes oom. vram suddenly spikes and the vae takes a long time more often than not (300+ seconds). While rocm 6.3 uses fp32 vae and the entire image finishes in 55 seconds. 

I recommend not using the pytorch rocm 6.4 nightly. Use this one
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3

---

### 评论 #2 — zichguan-amd (2025-05-13T14:48:01Z)

Hi @OrsoEric, this is very likely related to https://github.com/ROCm/ROCm/issues/4119. We are aware of this issue and already working on a fix.

---

### 评论 #3 — Matthew-Jenkins (2025-05-13T15:19:31Z)

@zichguan-amd It doesn't seem related to WSL. I'm on F41 and it doesn't affect rocm6.3 or 6.0 on rx 6900 xt. 

# System Details Report
---

## Report details
- **Date generated:**                              2025-05-13 11:19:17

## Hardware Information:
- **Hardware Model:**                              ASRock X570S PG Riptide
- **Memory:**                                      64.0 GiB
- **Processor:**                                   AMD Ryzen™ 7 5700X × 16
- **Graphics:**                                    AMD Radeon™ RX 6900 XT
- **Disk Capacity:**                               10.2 TB

## Software Information:
- **Firmware Version:**                            P5.60
- **OS Name:**                                     Fedora Linux 41 (Workstation Edition)
- **OS Build:**                                    (null)
- **OS Type:**                                     64-bit
- **GNOME Version:**                               47
- **Windowing System:**                            X11
- **Kernel Version:**                              Linux 6.14.4-200.fc41.x86_64


---

### 评论 #4 — zichguan-amd (2025-05-13T15:25:53Z)

@Matthew-Jenkins I believe OP is on WSL. If you observed regression on Linux, can you please open another ticket?

---

### 评论 #5 — Matthew-Jenkins (2025-05-13T15:38:23Z)

@zichguan-amd why we wait and see if OP still has the problem on 6.3? If they don't, then it's an issue not isolated to wsl. If they do, then I'll open an issue for 6.4 on linux.

---

### 评论 #6 — OrsoEric (2025-05-14T17:59:23Z)

> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3

I tried but it bricked ComfyUI, I'm trying to bring it back

> Versions of relevant libraries:
> [pip3] alias-free-torch==0.0.6
> [pip3] clip-anytorch==2.6.0
> [pip3] dctorch==0.1.2
> [pip3] ema-pytorch==0.7.7
> [pip3] kokoro-onnx==0.4.2
> [pip3] mypy-extensions==1.0.0
> [pip3] numpy==1.26.4
> [pip3] onnxruntime==1.21.1
> [pip3] open_clip_torch==2.32.0
> [pip3] pytorch-lightning==2.5.1.post0
> [pip3] pytorch-triton-rocm==2.3.0+rocm6.2.3.5a02332983
> [pip3] torch==2.3.0+rocm6.2.3
> [pip3] torch-stoi==0.2.3
> [pip3] torch-time-stretch==1.0.3
> [pip3] torchaudio==2.7.0+rocm6.3
> [pip3] torchdiffeq==0.2.5
> [pip3] torchmetrics==1.7.1
> [pip3] torchsde==0.2.6
> [pip3] torchvision==0.18.0+rocm6.2.3
> [pip3] triton==3.2.0
> [conda] Could not collect

> *******
> Agent 2
> *******
>   Name:                    gfx1100
>   Marketing Name:          AMD Radeon RX 7900 XTX

> soraka@TowerOfBabel:~$ ./run-comfy.sh
> [START] Security scan
> [DONE] Security scan
> ## ComfyUI-Manager: installing dependencies done.
> ** ComfyUI startup time: 2025-05-14 19:57:21.301
> ** Platform: Linux
> ** Python version: 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0]
> ** Python executable: /usr/bin/python3
> ** ComfyUI Path: /home/soraka/ComfyUI
> ** ComfyUI Base Folder Path: /home/soraka/ComfyUI
> ** User directory: /home/soraka/ComfyUI/user
> ** ComfyUI-Manager config path: /home/soraka/ComfyUI/user/default/ComfyUI-Manager/config.ini
> ** Log path: /home/soraka/ComfyUI/user/comfyui.log
> 
> Prestartup times for custom nodes:
>    1.1 seconds: /home/soraka/ComfyUI/custom_nodes/comfyui-manager
> 
> Warning, you are using an old pytorch version and some ckpt/pt files might be loaded unsafely. Upgrading to 2.4 or above is recommended.
> Traceback (most recent call last):
>   File "/home/soraka/ComfyUI/main.py", line 137, in <module>
>     import execution
>   File "/home/soraka/ComfyUI/execution.py", line 13, in <module>
>     import nodes
>   File "/home/soraka/ComfyUI/nodes.py", line 22, in <module>
>     import comfy.diffusers_load
>   File "/home/soraka/ComfyUI/comfy/diffusers_load.py", line 3, in <module>
>     import comfy.sd
>   File "/home/soraka/ComfyUI/comfy/sd.py", line 7, in <module>
>     from comfy import model_management
>   File "/home/soraka/ComfyUI/comfy/model_management.py", line 221, in <module>
>     total_vram = get_total_memory(get_torch_device()) / (1024 * 1024)
>   File "/home/soraka/ComfyUI/comfy/model_management.py", line 172, in get_torch_device
>     return torch.device(torch.cuda.current_device())
>   File "/home/soraka/.local/lib/python3.10/site-packages/torch/cuda/__init__.py", line 789, in current_device
>     _lazy_init()
>   File "/home/soraka/.local/lib/python3.10/site-packages/torch/cuda/__init__.py", line 293, in _lazy_init
>     torch._C._cuda_init()
> RuntimeError: No HIP GPUs are available

This will take a while...

> ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
> gptqmodel 2.2.0 requires pillow>=11.1.0, but you have pillow 11.0.0 which is incompatible.
> gptqmodel 2.2.0 requires protobuf>=5.29.3, but you have protobuf 3.19.4 which is incompatible.
> zonos 0.1.0.dev0 requires numpy>=2.2.2, but you have numpy 1.26.4 which is incompatible.
> zonos 0.1.0.dev0 requires torch>=2.5.1, but you have torch 2.4.0+rocm6.3.4.git7cecbf6d which is incompatible.
> zonos 0.1.0.dev0 requires torchaudio>=2.5.1, but you have torchaudio 2.4.0+rocm6.3.4.git69d40773 which is incompatible.

---

### 评论 #7 — Matthew-Jenkins (2025-05-15T20:38:19Z)

I can freely remove torch torchaudio torchvision 
then install stable+rocm6.3 or nightly+6.4 without any issue. 

I see this:  Python executable: /usr/bin/python3

Don't do that. Never use the system python. Always use a virtualenv. That is why it broke. 

Do this

    cd home/soraka/ComfyUI
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pip uninstall torch torchaudio torchvision
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3
    python3 main.py

---

### 评论 #8 — OrsoEric (2025-05-16T06:41:58Z)

Yeah, I'm rebuilding WSL a different way now that I know more about it.

I built it like this because it was my tenth attempt to get ROCm to run, and I was running out of options. I didn't rebuild it in a venv when it started working. I'm always afraid of bricking it when I add a new node, once it bricked when I was trying a STT model, but that time I brought it back by redoing the torch rocm instructions. This time it looks easier o just rebuild it properly.

This time around, i'm planning to use virtualenv to have a separate pip and python, I think I'll do it in 3.12 instead of 3.10.

Then I'm planning to use a zip with differences to do a backup of the whole comfyui, so I can just unpack the full local env if something bricks, instead of messing with pip.

Also for the models, right now I'm storing them inside WSL, but I can store them in the local machine outside the ext4 partition with a yaml.

I'll also update my instructions.

---

### 评论 #9 — OrsoEric (2025-05-16T11:53:43Z)

So, I rebuilt WSL with a number of changes (https://github.com/OrsoEric/HOWTO-7900XTX-Win-ROCM?tab=readme-ov-file#step-1---wsl)

I'm using UV as virtual environment and did some changes to the AMD instruction to get it all local and I'm using Python 3.12 on Ubuntu 22.

SD1.5 workflow runs well.

Now I'll have to re add all custom nodes and test all the workflows, it'll take a while.

---

### 评论 #10 — Matthew-Jenkins (2025-05-16T13:08:24Z)

So it's working on rocm 6.3?

---

### 评论 #11 — OrsoEric (2025-05-17T08:04:02Z)

> So it's working on rocm 6.3?

It does not work, it's the same issue I have with ROCm 6.3.4. With ROcm 6.3 I get driver timeout on VAE decode above 1024px

For sanity I checked with ROCm 6.3.4 with MIOPEN_FIND_MODE=2 and it works, so I am sure the new UV portable environment at least doesn't cause regression. I am using Python 3.12 wheels this time around with Python 3.12 portable, I didn't touch the Python 3.10 that Ubuntu 22 uses internally.

As additional check I tried MIOPEN_FIND_MODE=2 on ROCm 6.3 and it works too! the behaviour is very similar between ROCm 6.3.4 and ROCm 6.3

    Adrenaline 25.5.1
    WSL
    Ubuntu 22.04
    Python 3.12
    UV portable environment

Tests:

    ROCm 6.3 + default MIOPEN_FIND_MODE : VAE decode driver timeout above 1024px
    ROCm 6.3.4 + default MIOPEN_FIND_MODE : VAE decode driver timeout above 1024px
    ROCm 6.3 + MIOPEN_FIND_MODE=2 : VAE decode works fine at 2048px
    ROCm 6.3.4 + MIOPEN_FIND_MODE=2 : VAE decode works fine at 2048px

# Installation ROCm 6.3 WSL

In order to make ROCm binaries work under WSL I need to remember to delete ```libhsa-runtime64.so*``` after downgrading. With UV, installation works a lot better, compared to bare pip.

```
cd
cd ComfyUI
source Dreamy/bin/activate
uv pip uninstall torch torchaudio torchvision
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3
location=$(pip show torch | grep Location | awk -F ": " '{print $2}')
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
```

```
(Dreamy) meridia@TowerOfBabel:~/ComfyUI$ uv pip uninstall torch torchaudio torchvision
Using Python 3.12.10 environment at: Dreamy
Uninstalled 3 packages in 285ms
 - torch==2.4.0+rocm6.3.4.git7cecbf6d (from file:///home/meridia/ComfyUI/torch-2.4.0+rocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl)
 - torchaudio==2.4.0+rocm6.3.4.git69d40773 (from file:///home/meridia/ComfyUI/torchaudio-2.4.0+rocm6.3.4.git69d40773-cp312-cp312-linux_x86_64.whl)
 - torchvision==0.19.0+rocm6.3.4.gitfab84886 (from file:///home/meridia/ComfyUI/torchvision-0.19.0+rocm6.3.4.gitfab84886-cp312-cp312-linux_x86_64.whl)
(Dreamy) meridia@TowerOfBabel:~/ComfyUI$ uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.3
Using Python 3.12.10 environment at: Dreamy
Resolved 15 packages in 3.82s
Prepared 5 packages in 10m 33s
Uninstalled 2 packages in 61ms
Installed 5 packages in 183ms
 - pytorch-triton-rocm==3.0.0+rocm6.3.4.git75cc27c2 (from file:///home/meridia/ComfyUI/pytorch_triton_rocm-3.0.0+rocm6.3.4.git75cc27c2-cp312-cp312-linux_x86_64.whl)
 + pytorch-triton-rocm==3.3.0
 - sympy==1.12.1
 + sympy==1.13.3
 + torch==2.7.0+rocm6.3
 + torchaudio==2.7.0+rocm6.3
 + torchvision==0.22.0+rocm6.3

(Dreamy) meridia@TowerOfBabel:~/ComfyUI$ location=$(pip show torch | grep Location | awk -F ": " '{print $2}')

cd ${location}/torch/lib/
(Dreamy) meridia@TowerOfBabel:~/ComfyUI/Dreamy/lib/python3.12/site-packages/torch/lib$ rm libhsa-runtime64.so*

(Dreamy) meridia@TowerOfBabel:~/ComfyUI/Dreamy/lib/python3.12/site-packages/torch/lib$ cd
(Dreamy) meridia@TowerOfBabel:~$ cd ComfyUI/
(Dreamy) meridia@TowerOfBabel:~/ComfyUI$ python -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
python -c 'import torch; print(torch.cuda.is_available())'
python -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
python -m torch.utils.collect_env
Success
True
device name [0]: AMD Radeon RX 7900 XTX
<frozen runpy>:128: RuntimeWarning: 'torch.utils.collect_env' found in sys.modules after import of package 'torch.utils', but prior to execution of 'torch.utils.collect_env'; this may result in unpredictable behaviour
Collecting environment information...
PyTorch version: 2.7.0+rocm6.3
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.3.42131-fa1d09cbd

OS: Ubuntu 22.04.5 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.12.10 (main, Apr  9 2025, 04:03:51) [Clang 20.1.0 ] (64-bit runtime)
Python platform: Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon RX 7900 XTX (gfx1100)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.3.42131
MIOpen runtime version: 3.3.0
Is XNNPACK available: True

CPU:
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        39 bits physical, 48 bits virtual
Byte Order:                           Little Endian
CPU(s):                               24
On-line CPU(s) list:                  0-23
Vendor ID:                            GenuineIntel
Model name:                           13th Gen Intel(R) Core(TM) i7-13700F
CPU family:                           6
Model:                                183
Thread(s) per core:                   2
Core(s) per socket:                   12
Socket(s):                            1
Stepping:                             1
BogoMIPS:                             4224.01
Flags:                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid pni pclmulqdq vmx ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves avx_vnni umip waitpkg gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear serialize flush_l1d arch_capabilities
Virtualization:                       VT-x
Hypervisor vendor:                    Microsoft
Virtualization type:                  full
L1d cache:                            576 KiB (12 instances)
L1i cache:                            384 KiB (12 instances)
L2 cache:                             24 MiB (12 instances)
L3 cache:                             30 MiB (1 instance)
Vulnerability Gather data sampling:   Not affected
Vulnerability Itlb multihit:          Not affected
Vulnerability L1tf:                   Not affected
Vulnerability Mds:                    Not affected
Vulnerability Meltdown:               Not affected
Vulnerability Mmio stale data:        Not affected
Vulnerability Reg file data sampling: Mitigation; Clear Register File
Vulnerability Retbleed:               Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow:   Not affected
Vulnerability Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl and seccomp
Vulnerability Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:             Mitigation; Enhanced / Automatic IBRS; IBPB conditional; RSB filling; PBRSB-eIBRS SW sequence; BHI BHI_DIS_S
Vulnerability Srbds:                  Not affected
Vulnerability Tsx async abort:        Not affected

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==3.3.0
[pip3] torch==2.7.0+rocm6.3
[pip3] torchaudio==2.7.0+rocm6.3
[pip3] torchsde==0.2.6
[pip3] torchvision==0.22.0+rocm6.3
[conda] Could not collect
```

## Workflow

[Minimal VAE encode decode bug workflow](https://raw.githubusercontent.com/OrsoEric/HOWTO-ComfyUI/Master/workflows/bug-vae-decode-adrenaline-crash.png)

_______________________________________________________________________________________________

## ROCm 6.3 WSL with default MIOPEN_FIND_MODE 1536px (FAIL)
FAIL DRIVER TIMEOUT on VAE decode

ROCm version
```
Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==3.3.0
[pip3] torch==2.7.0+rocm6.3
[pip3] torchaudio==2.7.0+rocm6.3
[pip3] torchsde==0.2.6
[pip3] torchvision==0.22.0+rocm6.3
```

Launch command
```
cd
cd ComfyUI
source Dreamy/bin/activate
python main.py
```

![Image](https://github.com/user-attachments/assets/3ed016fc-8fc5-4e97-b502-5f9eecddf562)

_______________________________________________________________________________________________

## ROCm 6.3 WSL with MIOPEN_FIND_MODE=2 2048px (SUCCESS)
FAIL DRIVER TIMEOUT on VAE decode

ROCm version
```
Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==3.3.0
[pip3] torch==2.7.0+rocm6.3
[pip3] torchaudio==2.7.0+rocm6.3
[pip3] torchsde==0.2.6
[pip3] torchvision==0.22.0+rocm6.3
```

Launch command
```
cd
cd ComfyUI
source Dreamy/bin/activate
export MIOPEN_FIND_MODE=2
python main.py
```

![Image](https://github.com/user-attachments/assets/36ea3ab6-f3b1-434b-8e93-739659871f08)

_______________________________________________________________________________________________

## ROCm 6.3.4 WSL with default MIOPEN_FIND_MODE 2048px (FAIL)
FAIL DRIVER TIMEOUT on VAE decode

ROCm version
```
Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==3.0.0+rocm6.3.4.git75cc27c2
[pip3] torch==2.4.0+rocm6.3.4.git7cecbf6d
[pip3] torchaudio==2.4.0+rocm6.3.4.git69d40773
[pip3] torchvision==0.19.0+rocm6.3.4.gitfab84886
```

Launch command
```
cd
cd ComfyUI
source Dreamy/bin/activate
python main.py
```

![Image](https://github.com/user-attachments/assets/b2ba8f97-b6ed-44aa-9d1f-56bfd28f842a)

_______________________________________________________________________________________________

## ROCm 6.3.4 WSL with default MIOPEN_FIND_MODE=2 2048px (SUCCESS)
SUCCESS 18GB used

Launch command
```
cd
cd ComfyUI
source Dreamy/bin/activate
export MIOPEN_FIND_MODE=2
python main.py
```

![Image](https://github.com/user-attachments/assets/5ea3e74f-ff18-4d15-8838-6ebc129a327a)

_______________________________________________________________________________________________






---

### 评论 #12 — jammm (2025-05-22T14:13:54Z)

@OrsoEric does `MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0` work?

---

### 评论 #13 — jammm (2025-05-22T14:15:27Z)

Can you also run with `MIOPEN_LOG_LEVEL=5` and `MIOPEN_ENABLE_LOGGING=1`  and `MIOPEN_ENABLE_LOGGING_CMD=1` for the case where you do get the driver timeout, and share the logs here?

In the log, I'd want to search for cases where it's trying to call `naive_conv_ab_nonpacked_fwd_nchw_float_double_float ` or anything that begins with `naive`. If that's the case, then setting `MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0` could be a workaround for that.

---

### 评论 #14 — OrsoEric (2025-05-22T14:38:04Z)

I'll try friday, I'll be busy diffusing today and I need it to work. Replicating the OOM on VAE decode is really easy.

I have had a regression in performance with the python 3.12 binaries. I'll also try with a VENV with the python 3.10 binaries. Hidream takes around 260s which is way too much.

---

### 评论 #15 — Disty0 (2025-05-22T20:37:33Z)

You don't need big models to reproduce this, this happens on SDXL and other models too.

VAE decode at 1024x1024 with BF16 tries to use 16 GB VRAM meanwhile FP16 uses 2 GB and FP32 uses 4 GB.
BF16 VRAM usage is insanely high and the speed is slower than both FP32 and FP16.

This is with PyTorch 2.7 on SDNext.
Using RX 7900 XTX on Arch Linux.

---

### 评论 #16 — jammm (2025-05-22T21:15:11Z)

> You don't need big models to reproduce this, this happens on SDXL and other models too.
> 
> VAE decode at 1024x1024 with BF16 tries to use 16 GB VRAM meanwhile FP16 uses 2 GB and FP32 uses 4 GB. BF16 VRAM usage is insanely high and the speed is slower than both FP32 and FP16.
> 
> This is with PyTorch 2.7 on SDNext. Using RX 7900 XTX on Arch Linux.

What happens if you set MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0 ?


---

### 评论 #17 — Disty0 (2025-05-22T21:53:01Z)

> > You don't need big models to reproduce this, this happens on SDXL and other models too.
> > VAE decode at 1024x1024 with BF16 tries to use 16 GB VRAM meanwhile FP16 uses 2 GB and FP32 uses 4 GB. BF16 VRAM usage is insanely high and the speed is slower than both FP32 and FP16.
> > This is with PyTorch 2.7 on SDNext. Using RX 7900 XTX on Arch Linux.
> 
> What happens if you set MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0 ?

No change.
The spike in the graph is the VAE Decode with SDXL at 1024x1024 with BF16.
Using offload so that usage is only the VAE, UNet and Text Encoders are not in the GPU VRAM in VAE Decode.

Default:

![Image](https://github.com/user-attachments/assets/f3cad123-920d-47f0-8702-2dc30c89ea46)

With MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0 :

![Image](https://github.com/user-attachments/assets/c65a3d24-fd8a-4d9b-96dd-537dae8d899d)

---

### 评论 #18 — jammm (2025-05-22T21:55:09Z)

Thanks for checking!

---

### 评论 #19 — OrsoEric (2025-05-24T09:40:12Z)

> I have had a regression in performance with the python 3.12 binaries. I'll also try with a VENV with the python 3.10 binaries. Hidream takes around 260s which is way too much.

[I investigated the regression, and it doesn't have anything to do with python or pytorch.](https://github.com/OrsoEric/HOWTO-7900XTX-Win-ROCM?tab=readme-ov-file#wsl-host-machine-folder-penality)

It's just that fetching the models from /mnt has an enormous penality, the bigger the models are. Flux degrades from 60s to 400s.

I put the models inside WSL $HOME and it works fine now

---

### 评论 #20 — OrsoEric (2025-05-24T10:22:31Z)

> What happens if you set MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0 ?


Here dumps on tests

```
#!/bin/bash
cd
cd ComfyUI
#activate UV virtual environment
source Dreamy/bin/activate

#Set ROCm FLAGS

#??? something to do with acceleration to use
#export MIOPEN_FIND_MODE=2

export MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0

export MIOPEN_LOG_LEVEL=5
export MIOPEN_ENABLE_LOGGING=1
export MIOPEN_ENABLE_LOGGING_CMD=1

#Run ComfyUI
python main.py
```

This worked better, I dno't know why
```
VAE decode issue, I did a Flux run and a VAE only run at 1536 pixel that went 24GB, froze, but avoided a crash

#!/bin/bash
cd
cd ComfyUI
#activate UV virtual environment
source Dreamy/bin/activate

#Set ROCm FLAGS

#??? something to do with acceleration to use
#export MIOPEN_FIND_MODE=2

#export MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0

export MIOPEN_LOG_LEVEL=5
export MIOPEN_ENABLE_LOGGING=1
export MIOPEN_ENABLE_LOGGING_CMD=1

#Run ComfyUI
python main.py
```

https://gist.github.com/OrsoEric/5dd3a98e203fb2b34e676097f877db8c




---

### 评论 #21 — jammm (2025-05-24T10:28:30Z)

@OrsoEric it doesn't seem like the naive conv is being used in either case. So `MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0` has no effect here. MIOPEN_FIND_MODE=2 must be the difference maker.

---

### 评论 #22 — markg85 (2025-08-08T15:41:14Z)

This thread has some golden nuggets of information that i could use to make it work! Finally.
I'm on a 7900XT and that dreaded OOM error just keeps creeping up every damn time on every version. And that is with the official [rocm/pytorch](https://hub.docker.com/r/rocm/pytorch) docker container.

The above VAE Decode images and notion that it defaults to bf16 was key! Thank you for those images!

My, now working, setup:
```
export MIOPEN_FIND_MODE=2
python main.py --listen "0.0.0.0" --use-pytorch-cross-attention --fp16-vae
```

You **need** `--use-pytorch-cross-attention` for `--fp16-vae` to work properly. Without `--use-pytorch-cross-attention` your resulting image will be black. And without `--fp16-vae` you will get that OOM. You can omit `MIOPEN_FIND_MODE=2` but it will just be a looooot slower. I'm using the default Flux 1 Krea Dev workflow with no settings changed other then to show latent previews (TAESD).

As an aside, i also tried wit h`--fp32-vae`, works just fine too, no OOM. It just seems like not providing anything (whatever that defaults too) nukes AMD GPUs.

On Flux krea (fp8 quant) i get a whopping fast ~2s/it .... 🐌 ... well, it works at least.

---

### 评论 #23 — zichguan-amd (2025-09-11T21:02:06Z)

The driver time out issue should be fixed in the [25.8.1 driver](https://www.amd.com/en/resources/support-articles/release-notes/rn-rad-win-25-8-1.html).

---

### 评论 #24 — OrsoEric (2025-09-12T06:51:21Z)

I'm going to test it!


---

### 评论 #25 — OrsoEric (2025-12-08T16:49:58Z)

Good news. @zichguan-amd I got around to test the [preview driver 25.20.01.17](https://github.com/ROCm/ROCm/issues/4729) under bare windows 11 with python 3.12 and ComfyUI and so far lots of things work.

On the installation side. Pip no longer try to brick pytorch with the CUDA binaries. Tough the instructions really ought to use UV and a local python interpreter. Too many things can go wrong with a system interpreter.

And the VAE decode seems to be a lot faster and no longer crashes the driver, even without setting MIOPEN_FIND_MODE=2

I made a table with the tests

| Configuration | Workaround           | Size        | Max VRAM | Time  | Result  |
|---------------|----------------------|-------------|----------|-------|---------|
| 6.3.4 WSL       | —                    | 1024 × 1024 | 10.2 GB  | N.A.  | SUCCESS |
| 6.3.4 WSL       | —                    | 1536 × 1536 | 23.3 GB  | N.A.  | CRASH   |
| 6.3.4 WSL       | MIOPEN_FIND_MODE=2   | 2048 × 2048 | 18.5 GB  | 42.3s | SUCCESS |
| 6.3.4 WSL       | MIOPEN_FIND_MODE=3   | 1536 × 1536 | N.A.     | N.A.  | SUCCESS |
| 6.3.4 WSL       | MIOPEN_FIND_MODE=3   | 2048 × 2048 | 19 GB    | N.A.  | CRASH   |
| 7.11          | —                    | 2048 × 2048 | 23GB     | 15.0s | SUCCESS |

[additional logs](https://github.com/OrsoEric/HOWTO-ComfyUI/blob/Master/logs/2025-12-08%20Trying%20ROCm%20Windows.md)

I'll do more testing with the actual hard stuff that uses audio models and xformers but so far VAE decode is behaving pretty well!

---

### 评论 #26 — markg85 (2025-12-08T17:01:10Z)

@OrsoEric How does it run on a subsequent run _without_ restarting ComfyUI?
I'm asking because i've also had it working seemingly ok'ish on the first run. But then when running it again all hell breaks loose and i had to restart ComfyUI. Later i found different tricks like installing a module to clear out all vram before each run which isn't ideal because that slows it down too but made it work at least a little more stable.

---

### 评论 #27 — OrsoEric (2025-12-08T17:11:14Z)

I haven't gotten that far, I did maybe five generations in a row. I setup the STL workflow.

I'll be testing that.

---

### 评论 #28 — OrsoEric (2026-01-05T11:07:23Z)

> [@OrsoEric](https://github.com/OrsoEric) How does it run on a subsequent run _without_ restarting ComfyUI? I'm asking because i've also had it working seemingly ok'ish on the first run. But then when running it again all hell breaks loose and i had to restart ComfyUI. Later i found different tricks like installing a module to clear out all vram before each run which isn't ideal because that slows it down too but made it work at least a little more stable.

It's very inconsistent

```cmd
got prompt
Requested to load ZImageTEModel_
loaded completely; 22556.67 MB usable, 7672.25 MB loaded, full load: True
Requested to load Lumina2
loaded completely; 18462.67 MB usable, 11739.54 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:08<00:00,  1.02it/s]
Requested to load AutoencodingEngine
Unloaded partially: 1108.29 MB freed, 10631.27 MB remains loaded, 84.38 MB buffer reserved, lowvram patches: 0
loaded completely; 5305.04 MB usable, 159.87 MB loaded, full load: True
Prompt executed in 18.14 seconds
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load ZImageTEModel_
loaded completely; 22556.67 MB usable, 7672.25 MB loaded, full load: True
model weight dtype torch.bfloat16, manual cast: None
model_type FLOW
Requested to load Lumina2
Unloaded partially: 7672.25 MB freed, 0.00 MB remains loaded, 2320.62 MB buffer reserved, lowvram patches: 0
loaded completely; 18462.67 MB usable, 11739.54 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:09<00:00,  1.00s/it]
Requested to load AutoencodingEngine
Unloaded partially: 1520.79 MB freed, 10218.77 MB remains loaded, 225.00 MB buffer reserved, lowvram patches: 0
loaded completely; 5500.44 MB usable, 159.87 MB loaded, full load: True
Prompt executed in 24.11 seconds
got prompt
loaded completely; 18197.79 MB usable, 11739.54 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:34<00:00,  3.88s/it]
Unloaded partially: 602.04 MB freed, 11137.52 MB remains loaded, 84.38 MB buffer reserved, lowvram patches: 0
Prompt executed in 36.67 seconds
got prompt
loaded completely; 18193.79 MB usable, 11739.54 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:35<00:00,  3.96s/it]
Unloaded partially: 602.04 MB freed, 11137.52 MB remains loaded, 84.38 MB buffer reserved, lowvram patches: 0
Prompt executed in 37.23 seconds
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load ZImageTEModel_
loaded completely; 22556.67 MB usable, 7672.25 MB loaded, full load: True
model weight dtype torch.bfloat16, manual cast: None
model_type FLOW
Requested to load Lumina2
loaded completely; 18462.67 MB usable, 11739.54 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:09<00:00,  1.06s/it]
Requested to load AutoencodingEngine
Unloaded partially: 1520.79 MB freed, 10218.77 MB remains loaded, 225.00 MB buffer reserved, lowvram patches: 0
loaded completely; 5500.44 MB usable, 159.87 MB loaded, full load: True
Prompt executed in 41.71 seconds
got prompt
Requested to load Lumina2
loaded completely; 18462.67 MB usable, 11739.54 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:09<00:00,  1.05s/it]
Requested to load AutoencodingEngine
Unloaded partially: 602.04 MB freed, 11137.52 MB remains loaded, 84.38 MB buffer reserved, lowvram patches: 0
loaded completely; 5135.34 MB usable, 159.87 MB loaded, full load: True
Prompt executed in 15.14 seconds
got prompt
loaded completely; 18203.79 MB usable, 11739.54 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:09<00:00,  1.02s/it]
Unloaded partially: 573.92 MB freed, 11165.64 MB remains loaded, 84.38 MB buffer reserved, lowvram patches: 0
Prompt executed in 13.79 seconds
```

---

### 评论 #29 — OrsoEric (2026-01-05T13:34:26Z)

@markg85 

https://github.com/ROCm/ROCm/issues/5834

It took lots of testing but a workaround seems to work for me. I tried in Zimage, I'll have to try in Hunyuan 3D and other workflows.

Try running comfyui with this flag: ```uv run main.py --use-pytorch-cross-attention```

---

### 评论 #30 — markg85 (2026-01-05T14:32:48Z)

Thank you @OrsoEric that is much appreciated!

When i was using AMD i was also confined to a mandatory use of the `--use-pytorch-cross-attention` flag for an even usable environment. Still unusable but it worked for one or two generations before it had to be rebooted. OR more technically correct, before vram had to be cleared.

Anyhow, i've given up on ROCm. Getting it to work seems to be a matter of planetary alignment aligning just right within nanometers before it works. And if it works it breaks alignment. Every time i try this fresh i spend days getting it to work. That's not just this flag but also the python environment ant it not breaking or auto-falling-back-to nvidia (which it does if you're just not paying attention for a microsecond).

Now i'm "just" renting a gpu from team green on one of these gpu hourly rent sites like vast.ai. It's a hassle on it's own but much less and i'm up and running within 10 minutes or so (comfyui and models included) if i want to at a price that is barely higher then m electricity price. I don't prefer this route at all but if i want to do anything with images or video then this is the only usable route for an otherwise AMD user. **Unfortunately!**

Note that even with team green comfyui still has OOM issues. Just less.



---

### 评论 #31 — OrsoEric (2026-01-11T08:55:27Z)

@zichguan-amd I have been trying hard to make Qwen Edit work for a month, to no avail, 2509, 2511 and 2512 Image and Edit models. Today I was able to diffuse one image even tough ComfyUI badly crashed at the end with VAE decode. The desktop froze for a few second, but recovered, and the driver itself seem to have survived.

https://huggingface.co/unsloth/Qwen-Image-2512-GGUF/tree/main

I feel there is no hope in making the FP8 work, it wants to use BF16 and I'm not really sure if the 7900XTX even support FP8 in hardware. With Flux I never managed to do it, but the BF16 does fit so it works. Qwen is much larger and just doesn't fit if it uses BF16.

INT8 should be supported, and under Vulkan quantized LLM do work, so I feel GGUF Q4 to Q8 version of the models SHOULD work.

I used [city96](https://github.com/city96/ComfyUI-GGUF) node to load the GGUF model. Lighting LORA to do it in 4 iterations.

Diffusion went fine, I had a severe RAM spike in VAE decode, with the Qwen Image VAE, and the stack finally gave up with Exception Code: 0xC0000005 just after the VAE decode. Meaning finally I have some feedback on what failed!

```
got prompt
Requested to load QwenImage
loaded completely; 22452.99 MB usable, 20861.48 MB loaded, full load: True
100%|████████████████████████████████████████████████████████████████████████████████████| 4/4 [03:03<00:00, 45.84s/it]
Requested to load WanVAE
Unloaded partially: 2463.64 MB freed, 18397.88 MB remains loaded, 67.72 MB buffer reserved, lowvram patches: 253
loaded completely; 2211.39 MB usable, 242.03 MB loaded, full load: True
Prompt executed in 214.23 seconds
Exception Code: 0xC0000005
0x00007FFB5FDF1A89, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\VCRUNTIME140.dll(0x00007FFB5FDE0000) + 0x11A89 byte(s), memmove() + 0x699 byte(s)
0x00007FFAD0FC4807, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xC4807 byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0xC3F7 byte(s)
0x00007FFAD0FC3080, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xC3080 byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0xAC70 byte(s)
0x00007FFAD0FBE989, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xBE989 byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0x6579 byte(s)
0x00007FFAD0FBE8DA, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xBE8DA byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0x64CA byte(s)
0x00007FFAD0FBE312, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xBE312 byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0x5F02 byte(s)
0x00007FFAD0FBDC06, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xBDC06 byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0x57F6 byte(s)
0x00007FFAD0FBA4F1, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xBA4F1 byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0x20E1 byte(s)
0x00007FFAD0FBA3A3, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0xBA3A3 byte(s), ?_ThrowRuntimeTypeLogicError@detail@caffe2@@YAXAEBV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z() + 0x1F93 byte(s)
0x00007FFAD0F7C640, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0x7C640 byte(s), ?alloc_cpu@c10@@YAPEAX_K@Z() + 0x40 byte(s)
0x00007FFAD0F10CB9, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0x10CB9 byte(s), ?allocate@DefaultCPUAllocator@c10@@UEAA?AVDataPtr@2@_K@Z() + 0x29 byte(s)
0x00007FFAD0F2BE73, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\c10.dll(0x00007FFAD0F00000) + 0x2BE73 byte(s), ??0StorageImpl@c10@@QEAA@Uuse_byte_size_t@01@AEBVSymInt@1@PEAUAllocator@1@_N@Z() + 0x43 byte(s)
0x00007FFAC3AC35D3, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x835D3 byte(s)
0x00007FFAC3AC4045, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x84045 byte(s)
0x00007FFAC3AC4B18, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x84B18 byte(s)
0x00007FFAC435623D, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x91623D byte(s)
0x00007FFAC57A7F48, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x1D67F48 byte(s)
0x00007FFAC57A7A1E, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x1D67A1E byte(s)
0x00007FFAC4E33569, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x13F3569 byte(s)
0x00007FFAC4E332A4, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x13F32A4 byte(s)
0x00007FFAC5332471, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x18F2471 byte(s)
0x00007FFAC4E315F4, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x13F15F4 byte(s)
0x00007FFAC4319F0E, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x8D9F0E byte(s)
0x00007FFAC43193E2, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x8D93E2 byte(s)
0x00007FFAC54439E3, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x1A039E3 byte(s)
0x00007FFAC4A3D0BE, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0xFFD0BE byte(s)
0x00007FFAC534D902, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x190D902 byte(s)
0x00007FFAC4A3B973, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0xFFB973 byte(s)
0x00007FFAC4319C5D, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x8D9C5D byte(s)
0x00007FFAC566365E, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x1C2365E byte(s)
0x00007FFAC4C64AE6, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x1224AE6 byte(s)
0x00007FFAC534DF84, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x190DF84 byte(s)
0x00007FFAC4B9AA8C, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x115AA8C byte(s)
0x00007FFAC3A48028, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_cpu.dll(0x00007FFAC3A40000) + 0x8028 byte(s)
0x00007FFAB9E9F4B6, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_python.dll(0x00007FFAB9D30000) + 0x16F4B6 byte(s), ??0?$THPPointer@UTHPGenerator@@@@QEAA@PEAUTHPGenerator@@@Z() + 0x19666 byte(s)
0x00007FFAB9DA9CCD, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_python.dll(0x00007FFAB9D30000) + 0x79CCD byte(s), ?pyobject@PythonArgs@torch@@QEAAPEAU_object@@H@Z() + 0x10FAD byte(s)
0x00007FFB097965CB, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0xA65CB byte(s), PyType_Modified() + 0x863 byte(s)
0x00007FFB097639E1, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x739E1 byte(s), PyObject_Call() + 0x125 byte(s)
0x00007FFB0976392B, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x7392B byte(s), PyObject_Call() + 0x6F byte(s)
0x00007FFB0971E192, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x2E192 byte(s), _PyEval_EvalFrameDefault() + 0x4352 byte(s)
0x00007FFB0971874C, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x2874C byte(s), _PyFunction_Vectorcall() + 0x17C byte(s)
0x00007FFB09713A8A, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x23A8A byte(s), _PyArg_CheckPositional() + 0x5D2 byte(s)
0x00007FFB09719290, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x29290 byte(s), PyObject_Vectorcall() + 0xD0 byte(s)
0x00007FFB097BE876, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0xCE876 byte(s), PyObject_CallMethodObjArgs() + 0x14E byte(s)
0x00007FFB09737CD6, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x47CD6 byte(s), PyObject_CallFunctionObjArgs() + 0x42 byte(s)
0x00007FFABA93151A, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_python.dll(0x00007FFAB9D30000) + 0xC0151A byte(s), ?handle_torch_function_no_python_arg_parser@torch@@YAPEAU_object@@V?$ArrayRef@PEAU_object@@@c10@@PEAU2@1PEBD12W4TorchFunctionName@1@@Z() + 0xD8A byte(s)
0x00007FFABA932953, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_python.dll(0x00007FFAB9D30000) + 0xC02953 byte(s), ?handle_torch_function_no_python_arg_parser@torch@@YAPEAU_object@@V?$ArrayRef@PEAU_object@@@c10@@PEAU2@1PEBD12W4TorchFunctionName@1@@Z() + 0x21C3 byte(s)
0x00007FFAB9DA9A0B, F:\ComfyUI-Windows-2026-01-05-P312-therock\.venv\Lib\site-packages\torch\lib\torch_python.dll(0x00007FFAB9D30000) + 0x79A0B byte(s), ?pyobject@PythonArgs@torch@@QEAAPEAU_object@@H@Z() + 0x10CEB byte(s)
0x00007FFB09763D08, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x73D08 byte(s), PyObject_Call() + 0x44C byte(s)
0x00007FFB09763972, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x73972 byte(s), PyObject_Call() + 0xB6 byte(s)
0x00007FFB0971E192, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x2E192 byte(s), _PyEval_EvalFrameDefault() + 0x4352 byte(s)
0x00007FFB0971874C, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x2874C byte(s), _PyFunction_Vectorcall() + 0x17C byte(s)
0x00007FFB09713B6F, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x23B6F byte(s), _PyArg_CheckPositional() + 0x6B7 byte(s)
0x00007FFB097639E1, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x739E1 byte(s), PyObject_Call() + 0x125 byte(s)
0x00007FFB0976392B, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x7392B byte(s), PyObject_Call() + 0x6F byte(s)
0x00007FFB0972F9F4, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x3F9F4 byte(s), _PyThreadState_Bind() + 0x11C byte(s)
0x00007FFB0972F85A, C:\Users\FatherOfMachines\AppData\Roaming\uv\python\cpython-3.12.10-windows-x86_64-none\python312.dll(0x00007FFB096F0000) + 0x3F85A byte(s), PyThreadState_Clear() + 0x23A byte(s)
0x00007FFB7AFC9333, C:\Windows\System32\ucrtbase.dll(0x00007FFB7AFA0000) + 0x29333 byte(s), _recalloc() + 0xA3 byte(s)
0x00007FFB7CB5259D, C:\Windows\System32\KERNEL32.DLL(0x00007FFB7CB40000) + 0x1259D byte(s), BaseThreadInitThunk() + 0x1D byte(s)
0x00007FFB7DD2AF38, C:\Windows\SYSTEM32\ntdll.dll(0x00007FFB7DCD0000) + 0x5AF38 byte(s)
```

<img width="728" height="860" alt="Image" src="https://github.com/user-attachments/assets/ddda1c9c-dc15-47d6-876b-d681149ddba0" />

For the first time I was able to diffuse a full image right before the crash.

<img width="2560" height="1237" alt="Image" src="https://github.com/user-attachments/assets/0d1ac5c6-f42c-4f59-90f7-5eb6a7754a8e" />

I did more testing, and the problem seems to happen with the Qwen Image VAE, and not with other VAEs, I have no idea why.

Workflow

[ZDEBUG-QI-VAE.json](https://github.com/user-attachments/files/24549389/ZDEBUG-QI-VAE.json)

Zimage VAE

<img width="711" height="827" alt="Image" src="https://github.com/user-attachments/assets/274f8c86-1980-4e91-a02b-f81dc168bc74" />

<img width="2012" height="688" alt="Image" src="https://github.com/user-attachments/assets/2489eef1-06e6-4532-9c51-506ed91ee2ba" />

[Qwen Image VAE](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors)

Execution with fresh launch seems to work, even if it wildly spill into RAM

<img width="715" height="812" alt="Image" src="https://github.com/user-attachments/assets/b78a7653-11be-47dc-8da5-fb84060bedc1" />

Second execution causes severe freezing issues where for around a minute the desktop is frozen, typical OOM issue.

<img width="711" height="1807" alt="Image" src="https://github.com/user-attachments/assets/82a01206-6a47-42ac-b80a-97ff3cbf6cf2" />

```
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Requested to load AutoencodingEngine
0 models unloaded.
loaded completely; 9764.51 MB usable, 159.87 MB loaded, full load: True
0 models unloaded.
Prompt executed in 7.83 seconds
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Requested to load WanVAE
loaded completely; 11572.38 MB usable, 242.03 MB loaded, full load: True
Prompt executed in 38.56 seconds
got prompt
Prompt executed in 0.00 seconds
got prompt
Prompt executed in 0.00 seconds
got prompt
Prompt executed in 0.00 seconds
got prompt
Using split attention in VAE
Using split attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Requested to load WanVAE
0 models unloaded.
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
0 models unloaded.
loaded partially; 0.00 MB usable, 0.00 MB loaded, 242.00 MB offloaded, 22.78 MB buffer reserved, lowvram patches: 0
Prompt executed in 236.27 seconds
```

---
