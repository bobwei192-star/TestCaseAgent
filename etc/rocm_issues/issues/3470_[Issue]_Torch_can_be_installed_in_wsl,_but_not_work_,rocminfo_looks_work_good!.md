# [Issue]: Torch can be installed in wsl, but not work ,rocminfo looks work good!

> **Issue #3470**
> **状态**: open
> **创建时间**: 2024-07-29T00:38:02Z
> **更新时间**: 2025-02-25T15:40:25Z
> **作者**: Lookforworld
> **标签**: Under Investigation, AMD Radeon RX 7900 XTX, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3470

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description


I followed the process of the page :https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html.
The ROCM 6.1.3 can  be installed and the torch can be installed too. The  rocminfo is worked, but  the output of the `torch.cuda.is_available()`  is FALSE.
The hipcc also looks doesn't work fine!
```
(torch) root007@DEEPER:~$ hipcc --version
Can't exec "/opt/rocm/bin/rocm_agent_enumerator": No such file or directory at /usr/bin//hipcc.pl line 488.
Use of uninitialized value $targetsStr in substitution (s///) at /usr/bin//hipcc.pl line 489.
Use of uninitialized value $targetsStr in split at /usr/bin//hipcc.pl line 495.
HIP version: 6.1.40093-bd86f1708
AMD clang version 17.0.0 (https://github.com/RadeonOpenCompute/llvm-project roc-6.1.3 24193 669db884972e769450470020c06a6f132a8a065b)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/rocm/llvm/bin
Configuration file: /opt/rocm-6.1.3/lib/llvm/bin/clang++.cfg
```

My windows  is win11 23H2,  wsl kernel is 5.15.153.1-microsoft-standard-WSL2.

### Operating System

WSL(Ubuntu22.04.2 LTS)

### CPU

i5-11400F

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.1.0

### ROCm Component

ROCm

### Steps to Reproduce


```
Python 3.10.0 (default, Mar  3 2022, 09:58:08) [GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.is_available()
False
>>>

```

```
(torch) root007@DEEPER:~$ amd-smi
ERROR:root:Unable to get devices, driver not initialized (amdgpu not found in modules)
ERROR:root:Unable to detect any GPU devices, check amdgpu version and module status
ERROR:root:Unable to detect any CPU devices, check amd_hsmp version and module statu

```

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support


```
(base) root007@DEEPER:~$ rocminfo
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          NO

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    CPU
  Uuid:                    CPU-XX
  Marketing Name:          CPU
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
  Chip ID:                 0(0x0)
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            12
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    24614072(0x17794b8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    24614072(0x17794b8) KB
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
  Max Queue Number:        16(0x10)
  Queue Min Size:          4096(0x1000)
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
  Max Clock Freq. (MHz):   2304
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
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
  Packet Processor uCode:: 2250
  SDMA engine uCode::      20
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25100140(0x17eff6c) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
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


```

### Additional Information

_No response_

---

## 评论 (35 条)

### 评论 #1 — waheedi (2024-07-29T06:31:51Z)

What does` modprobe amdgpu` returns?

---

### 评论 #2 — harkgill-amd (2024-07-29T14:27:08Z)

Hi @Lookforworld, could you please confirm if you have the WSL compatible Windows driver installed? 

You can find it at [AMD Software: Adrenalin Edition™ 24.6.1 for WSL 2](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-6-1.html).

---

### 评论 #3 — Lookforworld (2024-07-30T03:40:37Z)

> What does` modprobe amdgpu` returns?
@waheedi  The output is:
`modprobe: FATAL: Module amdgpu not found in directory /lib/modules/5.15.153.1-microsoft-standard-WSL2`

---

### 评论 #4 — Lookforworld (2024-07-30T03:47:42Z)

> Hi @Lookforworld, could you please confirm if you have the WSL compatible Windows driver installed?
> 
> You can find it at [AMD Software: Adrenalin Edition™ 24.6.1 for WSL 2](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-6-1.html).

@harkgill-amd Yes, I do! `rocminfo` can give  the right  information.

---

### 评论 #5 — waheedi (2024-07-30T06:49:18Z)

> > What does` modprobe amdgpu` returns?
> > @waheedi  The output is:
> > `modprobe: FATAL: Module amdgpu not found in directory /lib/modules/5.15.153.1-microsoft-standard-WSL2`

I'm afraid i cant help much with WSL, i think that is the expected output as I understand the modules are embedded in WSL2. 

---

### 评论 #6 — harkgill-amd (2024-07-30T13:55:45Z)

Thank you for confirming @Lookforworld. 

I see an older issue reported with a very similar error to yours here https://github.com/ROCm/ROCm/issues/2767. Looks like it was resolved by adding the `--no-dkms` flag to the installation command. The WSL installation also specifies this flag in `amdgpu-install -y --usecase=wsl,rocm --no-dkms`, could you also confirm if this is what was ran?

---

### 评论 #7 — Lookforworld (2024-07-30T14:09:43Z)

>Thank you for confirming @Lookforworld.
> 
> I see an older issue reported with a very similar error to yours here #2767. Looks like it was resolved by adding the `--no-dkms` flag to the installation command. The WSL installation also specifies this flag in `amdgpu-install -y --usecase=wsl,rocm --no-dkms`, could you also confirm if this is what was ran?

@harkgill-amd Yes, I'm pretty sure I did. I carefully followed the documentation to install it. In order to rule out the problem of torch, I specially compiled the llama.cpp for testing today, and the compilation passed successfully, but it could not run correctly when running inference, and after the model was loaded into memory, it stuck there, but it did not throw any error. There must be a bug here, but I don't know how to troubleshoot it。
![221121](https://github.com/user-attachments/assets/aeafb66b-5e5b-4bc8-a74f-395649e18e95)


---

### 评论 #8 — ppanchad-amd (2024-07-31T19:51:43Z)

@Lookforworld Internal ticket has been created to further investigate this issue. Thanks!

---

### 评论 #9 — Lookforworld (2024-08-01T08:30:00Z)

@ppanchad-amd 
Thanks, looking forward to your good news.

---

### 评论 #10 — schung-amd (2024-08-01T18:56:03Z)

Hi @Lookforworld, thanks for the detailed report. I believe the error messages you're seeing in `hipcc --version` and `amd-smi` are normal for WSL2 configurations and unrelated to your issue. I also suspect the llama hang that you're experiencing is related to a different issue we're currently investigating (involving some operations hanging in ROCm + WSL2 setups) and is unrelated to your installation issues, but thanks for noting it.

Can you post the output of `python3 -m torch.utils.collect_env` and the output of `groups`?

---

### 评论 #11 — Lookforworld (2024-08-02T14:13:53Z)

> Hi @Lookforworld, thanks for the detailed report. I believe the error messages you're seeing in `hipcc --version` and `amd-smi` are normal for WSL2 configurations and unrelated to your issue. I also suspect the llama hang that you're experiencing is related to a different issue we're currently investigating (involving some operations hanging in ROCm + WSL2 setups) and is unrelated to your installation issues, but thanks for noting it.
> 
> Can you post the output of `python3 -m torch.utils.collect_env` and the output of `groups`?

@schung-amd Yes, thanks for your reply.

```
root@DEEPER:~# python3 -m torch.utils.collect_env
/usr/lib/python3.10/runpy.py:126: RuntimeWarning: 'torch.utils.collect_env' found in sys.modules after import of package 'torch.utils', but prior to execution of 'torch.utils.collect_env'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
Collecting environment information...
Traceback (most recent call last):
  File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/usr/local/lib/python3.10/dist-packages/torch/utils/collect_env.py", line 651, in <module>
    main()
  File "/usr/local/lib/python3.10/dist-packages/torch/utils/collect_env.py", line 634, in main
    output = get_pretty_env_info()
  File "/usr/local/lib/python3.10/dist-packages/torch/utils/collect_env.py", line 629, in get_pretty_env_info
    return pretty_str(get_env_info())
  File "/usr/local/lib/python3.10/dist-packages/torch/utils/collect_env.py", line 454, in get_env_info
    pip_version, pip_list_output = get_pip_packages(run_lambda)
  File "/usr/local/lib/python3.10/dist-packages/torch/utils/collect_env.py", line 411, in get_pip_packages
    out = run_with_pip([sys.executable, '-mpip'])
  File "/usr/local/lib/python3.10/dist-packages/torch/utils/collect_env.py", line 406, in run_with_pip
    for line in out.splitlines()
AttributeError: 'NoneType' object has no attribute 'splitlines'
```
```
root@DEEPER:~# groups
root
```



---

### 评论 #12 — fabiano-amaral (2024-08-02T14:44:45Z)

I'm facing the same issue, rocminfo works well 

```(venv) fabz@desktop:~/git/faster-whisper-webui$ rocminfo
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  ENABLED
DMAbuf Support:          YES

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    CPU
  Uuid:                    CPU-XX
  Marketing Name:          CPU
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
  Chip ID:                 0(0x0)
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            24
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16289304(0xf88e18) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    16289304(0xf88e18) KB
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
  Max Queue Number:        16(0x10)
  Queue Min Size:          4096(0x1000)
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
  Max Clock Freq. (MHz):   2371
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
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
  Packet Processor uCode:: 2150
  SDMA engine uCode::      20
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25101480(0x17f04a8) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
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
```

### rocm-smi

```
(venv) fabz@desktop:~/git/faster-whisper-webui$ rocm-smi
cat: /sys/module/amdgpu/initstate: No such file or directory
ERROR:root:Driver not initialized (amdgpu not found in modules)
```

---

### 评论 #13 — schung-amd (2024-08-02T14:49:01Z)

@Lookforworld I noticed you're doing all of this as the root user inside WSL. While the guide doesn't explicitly forbid you from being root, it's intended to be followed as a non-root user, and specifically pip warns that running as root could result in broken packages. Can you try reinstalling by following the guide as a non-root user inside WSL? You may have to uninstall ROCm and torch and/or reset WSL first.

@fabiano-amaral To clarify, you're experiencing the same `torch.cuda.is_available()` returning `false`? If so, can you also provide the output of `python3 -m torch.utils.collect_env` and `groups`? The `rocm-smi` error output is expected. Thanks!

---

### 评论 #14 — Lookforworld (2024-08-02T15:01:34Z)

> @Lookforworld I noticed you're doing all of this as the root user inside WSL. While the guide doesn't explicitly forbid you from being root, it's intended to be followed as a non-root user, and specifically pip warns that running as root could result in broken packages. Can you try reinstalling by following the guide as a non-root user inside WSL? You may have to uninstall ROCm and torch and/or reset WSL first.
> 
> @fabiano-amaral To clarify, you're experiencing the same `torch.cuda.is_available()` returning `false`? If so, can you also provide the output of `python3 -m torch.utils.collect_env` and `groups`? The `rocm-smi` error output is expected. Thanks!

@schung-amd Okey, I will reinstall all of them, after that I will give you something.

---

### 评论 #15 — fabiano-amaral (2024-08-02T15:03:57Z)

@schung-amd yes

```
(venv) fabz@desktop:~$ python -c 'import torch; print(torch.cuda.is_available())'
False
```
```
(venv) fabz@desktop:~$ python3 -m torch.utils.collect_env
/usr/lib/python3.10/runpy.py:126: RuntimeWarning: 'torch.utils.collect_env' found in sys.modules after import of package 'torch.utils', but prior to execution of 'torch.utils.collect_env'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
Collecting environment information...
PyTorch version: 2.5.0.dev20240802+rocm6.1
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.1.40091-a8dbc0c19

OS: Ubuntu 22.04.2 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.10.12 (main, Jul 29 2024, 16:56:48) [GCC 11.4.0] (64-bit runtime)
Python platform: Linux-5.15.153.1-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: False
CUDA runtime version: No CUDA
CUDA_MODULE_LOADING set to: N/A
GPU models and configuration: No CUDA
Nvidia driver version: No CUDA
cuDNN version: No CUDA
HIP runtime version: N/A
MIOpen runtime version: N/A
Is XNNPACK available: True

CPU:
Architecture:                       x86_64
CPU op-mode(s):                     32-bit, 64-bit
Address sizes:                      46 bits physical, 48 bits virtual
Byte Order:                         Little Endian
CPU(s):                             24
On-line CPU(s) list:                0-23
Vendor ID:                          GenuineIntel
Model name:                         13th Gen Intel(R) Core(TM) i7-13700K
CPU family:                         6
Model:                              183
Thread(s) per core:                 2
Core(s) per socket:                 12
Socket(s):                          1
Stepping:                           1
BogoMIPS:                           6835.19
Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid pni pclmulqdq vmx ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves avx_vnni umip waitpkg gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear serialize flush_l1d arch_capabilities
Virtualization:                     VT-x
Hypervisor vendor:                  Microsoft
Virtualization type:                full
L1d cache:                          576 KiB (12 instances)
L1i cache:                          384 KiB (12 instances)
L2 cache:                           24 MiB (12 instances)
L3 cache:                           30 MiB (1 instance)
Vulnerability Gather data sampling: Not affected
Vulnerability Itlb multihit:        Not affected
Vulnerability L1tf:                 Not affected
Vulnerability Mds:                  Not affected
Vulnerability Meltdown:             Not affected
Vulnerability Mmio stale data:      Not affected
Vulnerability Retbleed:             Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow: Not affected
Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccomp
Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:           Mitigation; Enhanced IBRS, IBPB conditional, RSB filling, PBRSB-eIBRS SW sequence
Vulnerability Srbds:                Not affected
Vulnerability Tsx async abort:      Not affected

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] onnxruntime==1.18.1
[pip3] pytorch-lightning==2.3.3
[pip3] pytorch-metric-learning==2.6.0
[pip3] pytorch-triton-rocm==3.0.0+21eae954ef
[pip3] torch==2.5.0.dev20240802+rocm6.1
[pip3] torch-audiomentations==0.11.1
[pip3] torch-pitch-shift==1.2.4
[pip3] torchaudio==2.4.0.dev20240802+rocm6.1
[pip3] torchmetrics==1.4.0.post0
[pip3] torchvision==0.20.0.dev20240802+rocm6.1
[conda] Could not collect
```

### groups
```
(venv) fabz@desktop:~$ groups
fabz adm dialout cdrom floppy sudo audio dip video plugdev netdev
```


---

### 评论 #16 — fabiano-amaral (2024-08-02T15:08:12Z)

And my version of adrenalin 
![image](https://github.com/user-attachments/assets/f644625a-384e-4481-8dbc-85b974e3e8b1)


---

### 评论 #17 — schung-amd (2024-08-02T15:17:50Z)

@fabiano-amaral Please reinstall using the instructions in https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html. Afterward, `python3 -m torch.utils.collect_env` should show `PyTorch version: 2.1.2+rocm6.1.3` (you have `2.5.0.dev20240802+rocm6.1` here), and a special version of Adrenalin 24.6.1 with WSL support. Your user should also be part of the `render` group, but I believe this is automatically set by following the guide.

---

### 评论 #18 — fabiano-amaral (2024-08-02T16:01:14Z)

@schung-amd ok, I installed this one, using link for WSL version and after I updated using the adrenalin interface, so I should not update after install?

---

### 评论 #19 — schung-amd (2024-08-02T16:06:57Z)

@fabiano-amaral Correct, after manually installing 24.6.1 with WSL support from the link in the guide, you should not update in the software.

---

### 评论 #20 — fabiano-amaral (2024-08-02T16:21:45Z)

@schung-amd thank you man, you saved my time a lot, now its working (the tests, at least)

```
(venv) fabz@desktop:~/venv/lib/python3.10/site-packages/torch/lib$ python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
Success
(venv) fabz@desktop:~/venv/lib/python3.10/site-packages/torch/lib$ python3 -c 'import torch; print(torch.cuda.is_available())'
True
(venv) fabz@desktop:~/venv/lib/python3.10/site-packages/torch/lib$ python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
device name [0]: AMD Radeon RX 7900 XTX
(venv) fabz@desktop:~/venv/lib/python3.10/site-packages/torch/lib$ python3 -m torch.utils.collect_env
Collecting environment information...
PyTorch version: 2.1.2+rocm6.1.3
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.1.40093-bd86f1708

OS: Ubuntu 22.04.2 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.10.12 (main, Jul 29 2024, 16:56:48) [GCC 11.4.0] (64-bit runtime)
Python platform: Linux-5.15.153.1-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon RX 7900 XTX
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.1.40093
MIOpen runtime version: 3.1.0
Is XNNPACK available: True

CPU:
Architecture:                       x86_64
CPU op-mode(s):                     32-bit, 64-bit
Address sizes:                      46 bits physical, 48 bits virtual
Byte Order:                         Little Endian
CPU(s):                             24
On-line CPU(s) list:                0-23
Vendor ID:                          GenuineIntel
Model name:                         13th Gen Intel(R) Core(TM) i7-13700K
CPU family:                         6
Model:                              183
Thread(s) per core:                 2
Core(s) per socket:                 12
Socket(s):                          1
Stepping:                           1
BogoMIPS:                           6835.20
Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid pni pclmulqdq vmx ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves avx_vnni umip waitpkg gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear serialize flush_l1d arch_capabilities
Virtualization:                     VT-x
Hypervisor vendor:                  Microsoft
Virtualization type:                full
L1d cache:                          576 KiB (12 instances)
L1i cache:                          384 KiB (12 instances)
L2 cache:                           24 MiB (12 instances)
L3 cache:                           30 MiB (1 instance)
Vulnerability Gather data sampling: Not affected
Vulnerability Itlb multihit:        Not affected
Vulnerability L1tf:                 Not affected
Vulnerability Mds:                  Not affected
Vulnerability Meltdown:             Not affected
Vulnerability Mmio stale data:      Not affected
Vulnerability Retbleed:             Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow: Not affected
Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccomp
Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:           Mitigation; Enhanced IBRS, IBPB conditional, RSB filling, PBRSB-eIBRS SW sequence
Vulnerability Srbds:                Not affected
Vulnerability Tsx async abort:      Not affected

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==2.1.0+rocm6.1.3.4d510c3a44
[pip3] torch==2.1.2+rocm6.1.3
[pip3] torchvision==0.16.1+rocm6.1.3
[conda] Could not collect
```

---

### 评论 #21 — Lookforworld (2024-08-02T16:49:47Z)

> @Lookforworld I noticed you're doing all of this as the root user inside WSL. While the guide doesn't explicitly forbid you from being root, it's intended to be followed as a non-root user, and specifically pip warns that running as root could result in broken packages. Can you try reinstalling by following the guide as a non-root user inside WSL? You may have to uninstall ROCm and torch and/or reset WSL first.
> 
> @fabiano-amaral To clarify, you're experiencing the same `torch.cuda.is_available()` returning `false`? If so, can you also provide the output of `python3 -m torch.utils.collect_env` and `groups`? The `rocm-smi` error output is expected. Thanks!

@schung-amd  

I'm not using sudo,  but:
```
(base) root001@DEEPER:~$ amdgpu-install -y --usecase=wsl,rocm --no-dkms
[sudo] password for root001:
```
Still running with root privileges, it looks like some libraries still aren't installed in my virtual environment：
```
Setting up amd-smi-lib (24.5.1.60103-122~22.04) ...
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Installing bash completion script /etc/bash_completion.d/python-argcomplete.sh
```




---

### 评论 #22 — schung-amd (2024-08-02T18:01:51Z)

To clarify, were you able to follow the whole guide as a non-root user, and if so, are you still experiencing the issue with torch.cuda.is_available() afterward?

---

### 评论 #23 — Lookforworld (2024-08-03T03:36:14Z)

> To clarify, were you able to follow the whole guide as a non-root user, and if so, are you still experiencing the issue with torch.cuda.is_available() afterward?

@schung-amd 
Yes, my username is `root001` not `root`.

I found the cause, it's a problem with conda. conda's C++ library version 6.0.29 but
Torch looks for version 6.0.30.
But other issues remain unresolved. `amd-smi` and `hipcc` are still the same as before.
When I use torch to load the model, it still gets stuck like llama.cpp, without any error throwing.

---

### 评论 #24 — schung-amd (2024-08-06T13:32:57Z)

Interesting, glad you were able to track the issue down on your end @Lookforworld. Does `torch.cuda.is_available()` now output true as expected, and do you get meaningful output from `python3 -m torch.utils.collect_env`?

As I mentioned, I believe the `amd-smi` and `hipcc --version` errors you're seeing are expected in WSL2. `amd-smi` specifically will not work as it relies on the amdgpu driver module which is not present in the WSL2 environment. 

Thanks for reporting that the torch and llama hangs are still occurring for you; this is a known issue we've reproduced in WSL2 and are investigating internally.

---

### 评论 #25 — Lookforworld (2024-08-06T20:11:18Z)

> Interesting, glad you were able to track the issue down on your end @Lookforworld. Does `torch.cuda.is_available()` now output true as expected, and do you get meaningful output from `python3 -m torch.utils.collect_env`?
> 
> As I mentioned, I believe the `amd-smi` and `hipcc --version` errors you're seeing are expected in WSL2. `amd-smi` specifically will not work as it relies on the amdgpu driver module which is not present in the WSL2 environment.
> 
> Thanks for reporting that the torch and llama hangs are still occurring for you; this is a known issue we've reproduced in WSL2 and are investigating internally.

@schung-amd Thanks, `torch.cuda.is_available()` and `python3 -m torch.utils.collect_env`  give the right information. Waiting for your good news！

---

### 评论 #26 — schung-amd (2024-08-21T14:17:04Z)

Hi @Lookforworld, are you still hanging in torch and llama? If so, can you provide some more system information? We're looking for:

- Motherboard model, BIOS version/date and SMBIOS version (viewable in msinfo32)
- PCI bus/device/function of the GPU (viewable in Device Manager)
- PCIe version, lanes, which PCIe slot the GPU is plugged into (i.e. top or lower)

On our repro this hang is caused by missing PCIe atomics support, which is difficult to check for and set on Windows. We're currently discussing this internally, as ideally there should be some documentation on this. In the meanwhile, we'd like to figure out if there's something in common with the systems that we're seeing these hangs on. Thanks!

---

### 评论 #27 — Lookforworld (2024-08-22T01:56:54Z)

> Hi @Lookforworld, are you still hanging in torch and llama? If so, can you provide some more system information? We're looking for:
> 
> * Motherboard model, BIOS version/date and SMBIOS version (viewable in msinfo32)
> * PCI bus/device/function of the GPU (viewable in Device Manager)
> * PCIe version, lanes, which PCIe slot the GPU is plugged into (i.e. top or lower)
> 
> On our repro this hang is caused by missing PCIe atomics support, which is difficult to check for and set on Windows. We're currently discussing this internally, as ideally there should be some documentation on this. In the meanwhile, we'd like to figure out if there's something in common with the systems that we're seeing these hangs on. Thanks!

@schung-amd 
Yes, I'm still hanging in torch and llama.cpp!
1. Motherboard model, BIOS version/date and SMBIOS version
![093905](https://github.com/user-attachments/assets/124d6c69-d27a-42f2-bcba-c134d46f24be)
2. PCI bus/device/function of the GPU
![094026](https://github.com/user-attachments/assets/dcf287cd-bdaa-433a-9025-f05e82aa0cea)
3. PCIe version, lanes, which PCIe slot the GPU is plugged into
 The  GPU is plugged into top, PCIe 4.0 x 16

![094708](https://github.com/user-attachments/assets/63206085-ecd0-487d-a65a-dc5179edb74a)


---

### 评论 #28 — schung-amd (2024-08-22T13:32:10Z)

Thanks for the info! Can you also provide the output of `wsl --version` from the Windows side, and `python3 -m torch.utils.collect_env` inside WSL (if that's working for you now, I know this was broken before)?

---

### 评论 #29 — Lookforworld (2024-08-22T14:50:02Z)

> Thanks for the info! Can you also provide the output of `wsl --version` from the Windows side, and `python3 -m torch.utils.collect_env` inside WSL (if that's working for you now, I know this was broken before)?

@schung-amd 
Okey.
WSL version:
```
PS C:\Users\Deeper> wsl --version
WSL 版本： 2.2.4.0
内核版本： 5.15.153.1-2
WSLg 版本： 1.0.61
MSRDC 版本： 1.2.5326
Direct3D 版本： 1.611.1-81528511
DXCore 版本： 10.0.26091.1-240325-1447.ge-release
Windows 版本： 10.0.22631.3880
```
The collect_env:
```
Collecting environment information...
PyTorch version: 2.1.2+rocm6.1.3
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.1.40093-bd86f1708

OS: Ubuntu 22.04.2 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.10.0 (default, Mar  3 2022, 09:58:08) [GCC 7.5.0] (64-bit runtime)
Python platform: Linux-5.15.153.1-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon RX 7900 XTX
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.1.40093
MIOpen runtime version: 3.1.0
Is XNNPACK available: True

CPU:
Architecture:                       x86_64
CPU op-mode(s):                     32-bit, 64-bit
Address sizes:                      39 bits physical, 48 bits virtual
Byte Order:                         Little Endian
CPU(s):                             12
On-line CPU(s) list:                0-11
Vendor ID:                          GenuineIntel
Model name:                         11th Gen Intel(R) Core(TM) i5-11400F @ 2.60GHz
CPU family:                         6
Model:                              167
Thread(s) per core:                 2
Core(s) per socket:                 6
Socket(s):                          1
Stepping:                           1
BogoMIPS:                           5183.99
Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid pni pclmulqdq vmx ssse3 fma cx16 pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid avx512f avx512dq rdseed adx smap avx512ifma clflushopt avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves avx512vbmi umip avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid fsrm md_clear flush_l1d arch_capabilities
Virtualization:                     VT-x
Hypervisor vendor:                  Microsoft
Virtualization type:                full
L1d cache:                          288 KiB (6 instances)
L1i cache:                          192 KiB (6 instances)
L2 cache:                           3 MiB (6 instances)
L3 cache:                           12 MiB (1 instance)
Vulnerability Gather data sampling: Unknown: Dependent on hypervisor status
Vulnerability Itlb multihit:        Not affected
Vulnerability L1tf:                 Not affected
Vulnerability Mds:                  Not affected
Vulnerability Meltdown:             Not affected
Vulnerability Mmio stale data:      Mitigation; Clear CPU buffers; SMT Host state unknown
Vulnerability Retbleed:             Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow: Not affected
Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccomp
Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:           Mitigation; Enhanced IBRS, IBPB conditional, RSB filling, PBRSB-eIBRS SW sequence
Vulnerability Srbds:                Not affected
Vulnerability Tsx async abort:      Not affected

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==2.1.0+rocm6.1.3.4d510c3a44
[pip3] torch==2.1.2+rocm6.1.3
[pip3] torchvision==0.16.1+rocm6.1.3
[conda] numpy                     1.26.4                   pypi_0    pypi
[conda] pytorch-triton-rocm       2.1.0+rocm6.1.3.4d510c3a44          pypi_0    pypi
[conda] torch                     2.1.2+rocm6.1.3          pypi_0    pypi
[conda] torchvision               0.16.1+rocm6.1.3          pypi_0    pypi
```


---

### 评论 #30 — Lookforworld (2024-09-03T07:56:25Z)

@schung-amd 
Hello, is there any news about this issue?

---

### 评论 #31 — schung-amd (2024-09-03T13:41:52Z)

Hi @Lookforworld, thanks for keeping up with this. We are working on improved documentation for WSL and a new feature to check for/enable PCIe atomics support, which should address this issue that you and others are seeing. However, these will likely not be ready until the next major release of ROCm on WSL. I will update once this feature is ready or if we find an acceptable workaround before then.

---

### 评论 #32 — Lookforworld (2024-09-03T18:23:06Z)

@schung-amd Thanks, hats off.

---

### 评论 #33 — Charmandrigo (2024-09-27T20:23:39Z)

I need some guidance because I followed AMD's guide for ROCm and Torch and I still get `Is CUDA available: False`

```
drigo@DrigoGamingPC:~/.local/lib/python3.10/site-packages/torch/lib$ rocminfo
=====================
HSA System Attributes
=====================
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE
System Endianness:       LITTLE
Mwaitx:                  DISABLED
DMAbuf Support:          NO

==========
HSA Agents
==========
*******
Agent 1
*******
  Name:                    CPU
  Uuid:                    CPU-XX
  Marketing Name:          CPU
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
  Chip ID:                 0(0x0)
  Cacheline Size:          64(0x40)
  Internal Node ID:        0
  Compute Unit:            16
  SIMDs per CU:            0
  Shader Engines:          0
  Shader Arrs. per Eng.:   0
  Features:                None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    15921496(0xf2f158) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:4KB
      Alloc Alignment:         4KB
      Accessible by all:       TRUE
    Pool 2
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    15921496(0xf2f158) KB
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
  Max Queue Number:        16(0x10)
  Queue Min Size:          4096(0x1000)
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
  Max Clock Freq. (MHz):   2371
  Internal Node ID:        1
  Compute Unit:            96
  SIMDs per CU:            2
  Shader Engines:          6
  Shader Arrs. per Eng.:   2
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
  Packet Processor uCode:: 2250
  SDMA engine uCode::      20
  IOMMU Support::          None
  Pool Info:
    Pool 1
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED
      Size:                    25100460(0x17f00ac) KB
      Allocatable:             TRUE
      Alloc Granule:           4KB
      Alloc Recommended Granule:2048KB
      Alloc Alignment:         4KB
      Accessible by all:       FALSE
    Pool 2
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
```
Then

```
drigo@DrigoGamingPC:~/.local/lib/python3.10/site-packages/torch/lib$ python3 -m torch.utils.collect_env
Collecting environment information...
PyTorch version: 2.1.2+rocm6.1.3
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.1.40093-bd86f1708

OS: Ubuntu 22.04.3 LTS (x86_64)
GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.35

Python version: 3.10.12 (main, Jul 29 2024, 16:56:48) [GCC 11.4.0] (64-bit runtime)
Python platform: Linux-5.15.153.1-microsoft-standard-WSL2-x86_64-with-glibc2.35
Is CUDA available: False
CUDA runtime version: No CUDA
CUDA_MODULE_LOADING set to: N/A
GPU models and configuration: No CUDA
Nvidia driver version: No CUDA
cuDNN version: No CUDA
HIP runtime version: N/A
MIOpen runtime version: N/A
Is XNNPACK available: True

CPU:
Architecture:                       x86_64
CPU op-mode(s):                     32-bit, 64-bit
Address sizes:                      48 bits physical, 48 bits virtual
Byte Order:                         Little Endian
CPU(s):                             16
On-line CPU(s) list:                0-15
Vendor ID:                          AuthenticAMD
Model name:                         AMD Ryzen 7 7800X3D 8-Core Processor
CPU family:                         25
Model:                              97
Thread(s) per core:                 2
Core(s) per socket:                 8
Socket(s):                          1
Stepping:                           2
BogoMIPS:                           8399.81
Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy svm cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw topoext perfctr_core ssbd ibrs ibpb stibp vmmcall fsgsbase bmi1 avx2 smep bmi2 erms invpcid avx512f avx512dq rdseed adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves avx512_bf16 clzero xsaveerptr arat npt nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload avx512vbmi umip avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid fsrm
Virtualization:                     AMD-V
Hypervisor vendor:                  Microsoft
Virtualization type:                full
L1d cache:                          256 KiB (8 instances)
L1i cache:                          256 KiB (8 instances)
L2 cache:                           8 MiB (8 instances)
L3 cache:                           96 MiB (1 instance)
Vulnerability Gather data sampling: Not affected
Vulnerability Itlb multihit:        Not affected
Vulnerability L1tf:                 Not affected
Vulnerability Mds:                  Not affected
Vulnerability Meltdown:             Not affected
Vulnerability Mmio stale data:      Not affected
Vulnerability Retbleed:             Not affected
Vulnerability Spec rstack overflow: Mitigation; safe RET
Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccomp
Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:           Mitigation; Retpolines, IBPB conditional, IBRS_FW, STIBP conditional, RSB filling, PBRSB-eIBRS Not affected
Vulnerability Srbds:                Not affected
Vulnerability Tsx async abort:      Not affected

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] pytorch-triton-rocm==2.1.0+rocm6.1.3.4d510c3a44
[pip3] torch==2.1.2+rocm6.1.3
[pip3] torchvision==0.16.1+rocm6.1.3
[conda] Could not collect
```
So I cannot use any pytorch appliactions because it keeps reporting there's no GPU

---

### 评论 #34 — schung-amd (2024-09-30T17:50:35Z)

Hi @Charmandrigo, what is your Adrenalin driver version? Also, are you using a conda environment?

---

### 评论 #35 — sorasoras (2024-10-26T19:10:49Z)

> I need some guidance because I followed AMD's guide for ROCm and Torch and I still get `Is CUDA available: False`
> 
> ```
> drigo@DrigoGamingPC:~/.local/lib/python3.10/site-packages/torch/lib$ rocminfo
> =====================
> HSA System Attributes
> =====================
> Runtime Version:         1.1
> System Timestamp Freq.:  1000.000000MHz
> Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
> Machine Model:           LARGE
> System Endianness:       LITTLE
> Mwaitx:                  DISABLED
> DMAbuf Support:          NO
> 
> ==========
> HSA Agents
> ==========
> *******
> Agent 1
> *******
>   Name:                    CPU
>   Uuid:                    CPU-XX
>   Marketing Name:          CPU
>   Vendor Name:             CPU
>   Feature:                 None specified
>   Profile:                 FULL_PROFILE
>   Float Round Mode:        NEAR
>   Max Queue Number:        0(0x0)
>   Queue Min Size:          0(0x0)
>   Queue Max Size:          0(0x0)
>   Queue Type:              MULTI
>   Node:                    0
>   Device Type:             CPU
>   Cache Info:
>   Chip ID:                 0(0x0)
>   Cacheline Size:          64(0x40)
>   Internal Node ID:        0
>   Compute Unit:            16
>   SIMDs per CU:            0
>   Shader Engines:          0
>   Shader Arrs. per Eng.:   0
>   Features:                None
>   Pool Info:
>     Pool 1
>       Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
>       Size:                    15921496(0xf2f158) KB
>       Allocatable:             TRUE
>       Alloc Granule:           4KB
>       Alloc Recommended Granule:4KB
>       Alloc Alignment:         4KB
>       Accessible by all:       TRUE
>     Pool 2
>       Segment:                 GLOBAL; FLAGS: COARSE GRAINED
>       Size:                    15921496(0xf2f158) KB
>       Allocatable:             TRUE
>       Alloc Granule:           4KB
>       Alloc Recommended Granule:4KB
>       Alloc Alignment:         4KB
>       Accessible by all:       TRUE
>   ISA Info:
> *******
> Agent 2
> *******
>   Name:                    gfx1100
>   Marketing Name:          AMD Radeon RX 7900 XTX
>   Vendor Name:             AMD
>   Feature:                 KERNEL_DISPATCH
>   Profile:                 BASE_PROFILE
>   Float Round Mode:        NEAR
>   Max Queue Number:        16(0x10)
>   Queue Min Size:          4096(0x1000)
>   Queue Max Size:          131072(0x20000)
>   Queue Type:              MULTI
>   Node:                    1
>   Device Type:             GPU
>   Cache Info:
>     L1:                      32(0x20) KB
>     L2:                      6144(0x1800) KB
>     L3:                      98304(0x18000) KB
>   Chip ID:                 29772(0x744c)
>   Cacheline Size:          64(0x40)
>   Max Clock Freq. (MHz):   2371
>   Internal Node ID:        1
>   Compute Unit:            96
>   SIMDs per CU:            2
>   Shader Engines:          6
>   Shader Arrs. per Eng.:   2
>   Coherent Host Access:    FALSE
>   Features:                KERNEL_DISPATCH
>   Fast F16 Operation:      TRUE
>   Wavefront Size:          32(0x20)
>   Workgroup Max Size:      1024(0x400)
>   Workgroup Max Size per Dimension:
>     x                        1024(0x400)
>     y                        1024(0x400)
>     z                        1024(0x400)
>   Max Waves Per CU:        32(0x20)
>   Max Work-item Per CU:    1024(0x400)
>   Grid Max Size:           4294967295(0xffffffff)
>   Grid Max Size per Dimension:
>     x                        4294967295(0xffffffff)
>     y                        4294967295(0xffffffff)
>     z                        4294967295(0xffffffff)
>   Max fbarriers/Workgrp:   32
>   Packet Processor uCode:: 2250
>   SDMA engine uCode::      20
>   IOMMU Support::          None
>   Pool Info:
>     Pool 1
>       Segment:                 GLOBAL; FLAGS: COARSE GRAINED
>       Size:                    25100460(0x17f00ac) KB
>       Allocatable:             TRUE
>       Alloc Granule:           4KB
>       Alloc Recommended Granule:2048KB
>       Alloc Alignment:         4KB
>       Accessible by all:       FALSE
>     Pool 2
>       Segment:                 GROUP
>       Size:                    64(0x40) KB
>       Allocatable:             FALSE
>       Alloc Granule:           0KB
>       Alloc Recommended Granule:0KB
>       Alloc Alignment:         0KB
>       Accessible by all:       FALSE
>   ISA Info:
>     ISA 1
>       Name:                    amdgcn-amd-amdhsa--gfx1100
>       Machine Models:          HSA_MACHINE_MODEL_LARGE
>       Profiles:                HSA_PROFILE_BASE
>       Default Rounding Mode:   NEAR
>       Default Rounding Mode:   NEAR
>       Fast f16:                TRUE
>       Workgroup Max Size:      1024(0x400)
>       Workgroup Max Size per Dimension:
>         x                        1024(0x400)
>         y                        1024(0x400)
>         z                        1024(0x400)
>       Grid Max Size:           4294967295(0xffffffff)
>       Grid Max Size per Dimension:
>         x                        4294967295(0xffffffff)
>         y                        4294967295(0xffffffff)
>         z                        4294967295(0xffffffff)
>       FBarrier Max Size:       32
> *** Done ***
> ```
> 
> Then
> 
> ```
> drigo@DrigoGamingPC:~/.local/lib/python3.10/site-packages/torch/lib$ python3 -m torch.utils.collect_env
> Collecting environment information...
> PyTorch version: 2.1.2+rocm6.1.3
> Is debug build: False
> CUDA used to build PyTorch: N/A
> ROCM used to build PyTorch: 6.1.40093-bd86f1708
> 
> OS: Ubuntu 22.04.3 LTS (x86_64)
> GCC version: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
> Clang version: Could not collect
> CMake version: Could not collect
> Libc version: glibc-2.35
> 
> Python version: 3.10.12 (main, Jul 29 2024, 16:56:48) [GCC 11.4.0] (64-bit runtime)
> Python platform: Linux-5.15.153.1-microsoft-standard-WSL2-x86_64-with-glibc2.35
> Is CUDA available: False
> CUDA runtime version: No CUDA
> CUDA_MODULE_LOADING set to: N/A
> GPU models and configuration: No CUDA
> Nvidia driver version: No CUDA
> cuDNN version: No CUDA
> HIP runtime version: N/A
> MIOpen runtime version: N/A
> Is XNNPACK available: True
> 
> CPU:
> Architecture:                       x86_64
> CPU op-mode(s):                     32-bit, 64-bit
> Address sizes:                      48 bits physical, 48 bits virtual
> Byte Order:                         Little Endian
> CPU(s):                             16
> On-line CPU(s) list:                0-15
> Vendor ID:                          AuthenticAMD
> Model name:                         AMD Ryzen 7 7800X3D 8-Core Processor
> CPU family:                         25
> Model:                              97
> Thread(s) per core:                 2
> Core(s) per socket:                 8
> Socket(s):                          1
> Stepping:                           2
> BogoMIPS:                           8399.81
> Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy svm cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw topoext perfctr_core ssbd ibrs ibpb stibp vmmcall fsgsbase bmi1 avx2 smep bmi2 erms invpcid avx512f avx512dq rdseed adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves avx512_bf16 clzero xsaveerptr arat npt nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload avx512vbmi umip avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid fsrm
> Virtualization:                     AMD-V
> Hypervisor vendor:                  Microsoft
> Virtualization type:                full
> L1d cache:                          256 KiB (8 instances)
> L1i cache:                          256 KiB (8 instances)
> L2 cache:                           8 MiB (8 instances)
> L3 cache:                           96 MiB (1 instance)
> Vulnerability Gather data sampling: Not affected
> Vulnerability Itlb multihit:        Not affected
> Vulnerability L1tf:                 Not affected
> Vulnerability Mds:                  Not affected
> Vulnerability Meltdown:             Not affected
> Vulnerability Mmio stale data:      Not affected
> Vulnerability Retbleed:             Not affected
> Vulnerability Spec rstack overflow: Mitigation; safe RET
> Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccomp
> Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitization
> Vulnerability Spectre v2:           Mitigation; Retpolines, IBPB conditional, IBRS_FW, STIBP conditional, RSB filling, PBRSB-eIBRS Not affected
> Vulnerability Srbds:                Not affected
> Vulnerability Tsx async abort:      Not affected
> 
> Versions of relevant libraries:
> [pip3] numpy==1.26.4
> [pip3] pytorch-triton-rocm==2.1.0+rocm6.1.3.4d510c3a44
> [pip3] torch==2.1.2+rocm6.1.3
> [pip3] torchvision==0.16.1+rocm6.1.3
> [conda] Could not collect
> ```
> 
> So I cannot use any pytorch appliactions because it keeps reporting there's no GPU

I think you miss the part.


```
location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
```
without this part, my pytorch would not work at all.
and I am using pytorch 2.5

---
