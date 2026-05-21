# [Issue]: The GPU cannot be loaded

> **Issue #4864**
> **状态**: closed
> **创建时间**: 2025-05-31T12:23:48Z
> **更新时间**: 2025-05-31T12:27:22Z
> **关闭时间**: 2025-05-31T12:27:22Z
> **作者**: zheliangzhi
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/4864

## 描述

### Problem Description

“RuntimeError: No HIP GPUs are available” for ComfuUI。
What can I do to improve it?

### Operating System

Ubuntu-24.04

### CPU

AMD Ryzen 7 5700X

### GPU

AMD radeon rx7900XT

### ROCm Version

ROCm6.4.1

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

(venv) root@CHUN:~/ComfyUI# python3 -m torch.utils.collect_env
<frozen runpy>:128: RuntimeWarning: 'torch.utils.collect_env' found in sys.modules after import of package 'torch.utils', but prior to execution of 'torch.utils.collect_env'; this may result in unpredictable behaviour
Collecting environment information...
PyTorch version: 2.8.0.dev20250529+rocm6.4
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.4.43482-0f2d60242

OS: Ubuntu 24.04.1 LTS (x86_64)
GCC version: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.39

Python version: 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] (64-bit runtime)
Python platform: Linux-6.6.87.1-microsoft-standard-WSL2-x86_64-with-glibc2.39
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
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        48 bits physical, 48 bits virtual
Byte Order:                           Little Endian
CPU(s):                               16
On-line CPU(s) list:                  0-15
Vendor ID:                            AuthenticAMD
Model name:                           AMD Ryzen 7 5700X 8-Core Processor
CPU family:                           25
Model:                                33
Thread(s) per core:                   2
Core(s) per socket:                   8
Socket(s):                            1
Stepping:                             2
BogoMIPS:                             6800.08
Flags:                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw topoext perfctr_core ssbd ibrs ibpb stibp vmmcall fsgsbase bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves clzero xsaveerptr arat umip vaes vpclmulqdq rdpid fsrm
Hypervisor vendor:                    Microsoft
Virtualization type:                  full
L1d cache:                            256 KiB (8 instances)
L1i cache:                            256 KiB (8 instances)
L2 cache:                             4 MiB (8 instances)
L3 cache:                             32 MiB (1 instance)
NUMA node(s):                         1
NUMA node0 CPU(s):                    0-15
Vulnerability Gather data sampling:   Not affected
Vulnerability Itlb multihit:          Not affected
Vulnerability L1tf:                   Not affected
Vulnerability Mds:                    Not affected
Vulnerability Meltdown:               Not affected
Vulnerability Mmio stale data:        Not affected
Vulnerability Reg file data sampling: Not affected
Vulnerability Retbleed:               Not affected
Vulnerability Spec rstack overflow:   Vulnerable: Safe RET, no microcode
Vulnerability Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:             Mitigation; Retpolines; IBPB conditional; IBRS_FW; STIBP always-on; RSB filling; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                  Not affected
Vulnerability Tsx async abort:        Not affected

Versions of relevant libraries:
[pip3] numpy==1.26.4
[pip3] nvidia-cublas-cu12==12.6.4.1
[pip3] nvidia-cuda-cupti-cu12==12.6.80
[pip3] nvidia-cuda-nvrtc-cu12==12.6.77
[pip3] nvidia-cuda-runtime-cu12==12.6.77
[pip3] nvidia-cudnn-cu12==9.5.1.17
[pip3] nvidia-cufft-cu12==11.3.0.4
[pip3] nvidia-curand-cu12==10.3.7.77
[pip3] nvidia-cusolver-cu12==11.7.1.2
[pip3] nvidia-cusparse-cu12==12.5.4.2
[pip3] nvidia-cusparselt-cu12==0.6.3
[pip3] nvidia-nccl-cu12==2.26.2
[pip3] nvidia-nvjitlink-cu12==12.6.85
[pip3] nvidia-nvtx-cu12==12.6.77
[pip3] onnx==1.18.0
[pip3] pytorch-triton-rocm==3.3.1+gitc8757738
[pip3] torch==2.8.0.dev20250529+rocm6.4
[pip3] torchaudio==2.6.0.dev20250530+rocm6.4
[pip3] torchsde==0.2.6
[pip3] torchvision==0.22.0.dev20250530+rocm6.4
[pip3] triton==3.3.0
[conda] Could not collect

### Additional Information

Sorry, maybe it's not very clear because I don't speak English very well
