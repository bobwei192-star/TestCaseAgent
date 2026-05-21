# Problems with using AMD GPUs in (wsl Ubuntu-24.04)

> **Issue #5003**
> **状态**: closed
> **创建时间**: 2025-07-07T06:43:26Z
> **更新时间**: 2025-07-07T06:50:08Z
> **关闭时间**: 2025-07-07T06:50:08Z
> **作者**: zheliangzhi
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/5003

## 描述

  Hello, the following conversation is from translation software. Please forgive any unclear expressions.
  
The problem occurs in the work project using ConfyUI.

 I am using an AMD Radeon™ RX 7900 XT GPU, so I am using it in (WSL) Ubuntu-24.04. I have carefully followed the installation and deployment instructions in the documentation, GitHub page, and ROCm documentation. However, contributors have released a FLUX model that integrates Clip, VAE, and other models to leverage this model via loader checkpoint. After that, even though all my models and workflows come from ComfyUI-Manager, the generated content remains completely noisy, even without errors. This issue also exists in previously functioning work projects. Interestingly, this does not happen in projects using the SDXL category model.

I recorded some information

<frozen runpy>:128: RuntimeWarning: 'torch.utils.collect_env' found in sys.modules after import of package 'torch.utils', but prior to execution of 'torch.utils.collect_env'; this may result in unpredictable behaviour
Collecting environment information...
PyTorch version: 2.9.0.dev20250706+rocm6.4
Is debug build: False
CUDA used to build PyTorch: N/A
ROCM used to build PyTorch: 6.4.43483-a187df25c

OS: Ubuntu 24.04.2 LTS (x86_64)
GCC version: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Clang version: Could not collect
CMake version: Could not collect
Libc version: glibc-2.39

Python version: 3.12.3 (main, Jun 18 2025, 17:59:45) [GCC 13.3.0] (64-bit runtime)
Python platform: Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39
Is CUDA available: True
CUDA runtime version: Could not collect
CUDA_MODULE_LOADING set to: LAZY
GPU models and configuration: AMD Radeon RX 7900 XT (gfx1100)
Nvidia driver version: Could not collect
cuDNN version: Could not collect
HIP runtime version: 6.4.43483
MIOpen runtime version: 3.4.0
Is XNNPACK available: True

CPU:
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        48 bits physical, 48 bits virtual
Byte Order:                           Little Endian
CPU(s):                               12
On-line CPU(s) list:                  0-11
Vendor ID:                            AuthenticAMD
Model name:                           AMD Ryzen 7 5700X 8-Core Processor
CPU family:                           25
Model:                                33
Thread(s) per core:                   2
Core(s) per socket:                   6
Socket(s):                            1
Stepping:                             2
BogoMIPS:                             6800.07
Flags:                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy svm cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw topoext perfctr_core ssbd ibrs ibpb stibp vmmcall fsgsbase bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves clzero xsaveerptr arat npt nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload umip vaes vpclmulqdq rdpid fsrm
Virtualization:                       AMD-V
Hypervisor vendor:                    Microsoft
Virtualization type:                  full
L1d cache:                            192 KiB (6 instances)
L1i cache:                            192 KiB (6 instances)
L2 cache:                             3 MiB (6 instances)
L3 cache:                             32 MiB (1 instance)
NUMA node(s):                         1
NUMA node0 CPU(s):                    0-11
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
[pip3] pytorch-triton-rocm==3.3.1+gitc8757738
[pip3] torch==2.9.0.dev20250706+rocm6.4
[pip3] torchaudio==2.8.0.dev20250706+rocm6.4
[pip3] torchsde==0.2.6
[pip3] torchvision==0.24.0.dev20250706+rocm6.4
[conda] Could not collect

I noticed this. Compared to the previous version before the issue occurred, the requirements.txt file includes an extra list of environment components showing alembic and SQLAlchemy. Is the problem I encountered related to this?

This is a comparison of environment-dependent projects：
Old：
comfyui-frontend-package==1.21.7
comfyui-workflow-templates==0.1.25
comfyui-embedded-docs==0.2.0
torch
torchsde
torchvision
torchaudio
numpy>=1.25.0
einops
transformers>=4.28.1
tokenizers>=0.13.3
sentencepiece
safetensors>=0.4.2
aiohttp>=3.11.8
yarl>=1.18.0
pyyaml
Pillow
scipy
tqdm
psutil

#non essential dependencies:
kornia>=0.7.1
spandrel
soundfile
av>=14.2.0
pydantic~=2.0

Now：#The difference is in ( )
comfyui-frontend-package==1.23.4
comfyui-workflow-templates==0.1.30
comfyui-embedded-docs==0.2.3
torch
torchsde
torchvision
torchaudio
numpy>=1.25.0
einops
transformers>=4.37.2
tokenizers>=0.13.3
sentencepiece
safetensors>=0.4.2
aiohttp>=3.11.8
yarl>=1.18.0
pyyaml
Pillow
scipy
tqdm
psutil
（alembic
SQLAlchemy）

#non essential dependencies:
kornia>=0.7.1
spandrel
soundfile
av>=14.2.0
pydantic~=2.0
pydantic-settings~=2.0


