# [Issue]: RuntimeError: HIP error: invalid argument  when running  any model

> **Issue #3999**
> **状态**: closed
> **创建时间**: 2024-11-06T16:22:53Z
> **更新时间**: 2025-01-13T21:22:59Z
> **关闭时间**: 2025-01-13T21:22:58Z
> **作者**: atifkhanncl
> **标签**: Under Investigation, ROCm 5.7.0, AMD Instinct MI50 (Radeon Instinct MI50 32GB)
> **URL**: https://github.com/ROCm/ROCm/issues/3999

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 5.7.0** (颜色: #ededed)
- **AMD Instinct MI50 (Radeon Instinct MI50 32GB)** (颜色: #ededed)

## 描述

### Problem Description


**Error details:**
When I try to run any model (including the example: https://rocm.blogs.amd.com/artificial-intelligence/pytorch-lightning/README.html) it returns following error:

RuntimeError: HIP error: invalid argument
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


**Comments**
We have invested in  ROCm AMD instead of NVIDIA CUDA but this is stopping us from using these GPUs in any meaningful way. Can you please let me know how to fix this issue please?



**setup details**:

$  echo "OS:" && cat /etc/os-release | grep -E "^(NAME=|VERSION=)";
OS:
NAME="Rocky Linux"
VERSION="8.6 (Green Obsidian)"

$   echo "CPU: " && cat /proc/cpuinfo | grep "model name" | sort --unique;
CPU: 
model name      : AMD EPYC 7642 48-Core Processor

$   echo "GPU:" && /opt/rocm/bin/rocminfo | grep -E "^\s*(Name|Marketing Name)";
GPU:
  Name:                    AMD EPYC 7642 48-Core Processor    
  Marketing Name:          AMD EPYC 7642 48-Core Processor    
  Name:                    gfx906                             
  Marketing Name:          AMD Instinct MI50/MI60             
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
  Name:                    gfx906                             
  Marketing Name:          AMD Instinct MI50/MI60             
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
  Name:                    gfx906                             
  Marketing Name:          AMD Instinct MI50/MI60             
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-
  Name:                    gfx906                             
  Marketing Name:          AMD Instinct MI50/MI60             
      Name:                    amdgcn-amd-amdhsa--gfx906:sramecc+:xnack-


**ROCm details**:

$ rpm -qa | grep rocm
rocm-opencl-sdk-5.7.0.50700-63.el8.x86_64
rocm-hip-sdk-5.7.0.50700-63.el8.x86_64
rocm-core-5.7.0.50700-63.el8.x86_64
rocm-hip-runtime-5.7.0.50700-63.el8.x86_64
rocm-opencl-runtime-5.7.0.50700-63.el8.x86_64
rocm-cmake-0.10.0.50700-63.el8.x86_64
rocm-hip-runtime-devel-5.7.0.50700-63.el8.x86_64
rocm-hip-libraries-5.7.0.50700-63.el8.x86_64
rocm-llvm-17.0.0.23352.50700-63.el8.x86_64
rocm-ocl-icd-2.0.0.50700-63.el8.x86_64
rocm-device-libs-1.0.0.50700-63.el8.x86_64
rocm-llvm5.7.0-17.0.0.23352.50700-63.el8.x86_64
rocminfo-1.0.0.50700-63.el8.x86_64
rocm-opencl-2.0.0.50700-63.el8.x86_64
rocm-smi-lib-5.0.0.50700-63.el8.x86_64
rocminfo5.7.0-1.0.0.50700-63.el8.x86_64
rocm-language-runtime-5.7.0.50700-63.el8.x86_64
rocm-opencl-devel-2.0.0.50700-63.el8.x86_64
rocm-core5.7.0-5.7.0.50700-63.el8.x86_64




### Operating System

Rocky Linux(VERSION="8.6 (Green Obsidian)")

### CPU

model name      : AMD EPYC 7642 48-Core Processor

### GPU

AMD Instinct MI50 (Radeon Instinct MI50 32GB)

### ROCm Version

ROCm 5.7.0

### ROCm Component

_No response_

### Steps to Reproduce

just try to run your example code: https://rocm.blogs.amd.com/artificial-intelligence/pytorch-lightning/README.html

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (7 条)

### 评论 #1 — harkgill-amd (2024-11-06T21:42:15Z)

Hi @atifkhanncl, could you please provide the output of the following commands:

1. `python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'`
2.  `pip show torch`
3. `python3 -c 'import torch; print(torch.cuda.is_available())'`
4. `dkms status`

Also, is it possible to try running the sample on ROCm 6.2.2 either by upgrading your host or using the [rocm/pytorch](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-a-docker-image-with-pytorch-pre-installed) docker image? This will provide a better baseline for your configuration as there have been many changes since ROCm 5.7.0.

---

### 评论 #2 — atifkhanncl (2024-11-07T10:18:26Z)

Hi @harkgill-amd ,
**I have been told upgrading ROCm is not possible as  we are currently running the MI50 Instinct cards, which run the older GCN architecture. The last ROCm release that supports this architecture is the one we are running, 5.7.0**. Meanwhile following are the outputs of your queries

$ python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
Success
$ pip show torch
Name: torch
Version: 2.4.1+rocm6.1
Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
Home-page: https://pytorch.org/
Author: PyTorch Team
Author-email: packages@pytorch.org
License: BSD-3
Location: /home/user/miniconda3/envs/rocm_torch/lib/python3.10/site-packages
Requires: filelock, fsspec, jinja2, networkx, pytorch-triton-rocm, sympy, typing-extensions
Required-by: lightning, pytorch-lightning, torchaudio, torchmetrics, torchvision
$ python3 -c 'import torch; print(torch.cuda.is_available())'
True
$ dkms status
bash: dkms: command not found

---

### 评论 #3 — harkgill-amd (2024-11-07T16:08:58Z)

I gave this a run on my end with an AMD Radeon PRO VII, which is also gfx906/GCN 5.1. Was able to run the sample on both a ROCm 5.7.0 baremetal install and within the rocm/pytorch 6.2 docker container. I'll confirm what the recommended ROCm version is for PyTorch+MI50, but in the meantime, a few other things that'll help:

- Could you please provide the complete traceback? I see a few similar reports that were caused by a call to `torch.cuda.cudart().cudaMemGetInfo(device)`.
- Downgrade your torch installation to have parity with ROCm 5.7.0. This can be done with `pip uninstall torch torchvision torchaudio` and `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7/`
- Try the sample using the rocm/pytorch docker container. This worked with `gfx906` and will help eliminate any installation issues besides the dkms.
- `sudo dnf install dkms` prior to running `dkms status`. With this, we're trying to see if amdgpu-dkms was successfully installed and is the correct version. If the sample does not work within the docker container, the dkms would be the last component related to the host installation.

Any other details related to how ROCm was installed on your system would also be great.

---

### 评论 #4 — atifkhanncl (2024-11-08T15:31:25Z)

I took up your advice and created a clean new environment with following setup
`
conda create --name rocm python=3.11
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
wget https://raw.githubusercontent.com/wiki/ROCm/pytorch/files/install_kdb_files_for_pytorch_wheels.sh
export GFX_ARCH=gfx906
export ROCM_VERSION=5.7
./install_kdb_files_for_pytorch_wheels.s
pip install lightning transformers datasets torchmetrics
`
After this I tried to run the sample code:  https://rocm.blogs.amd.com/artificial-intelligence/pytorch-lightning/README.html. 

It detects all 4 GPUs

`print(f"number of GPUs: {torch.cuda.device_count()}")
print([torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())])
output: number of GPUs: 4
['AMD Instinct MI50/MI60', 'AMD Instinct MI50/MI60', 'AMD Instinct MI50/MI60', 'AMD Instinct MI50/MI60']
`
gives a warning : Using the `SDPA` attention implementation on multi-gpu setup with ROCM may lead to performance issues due to the FA backend. Disabling it to use alternative backends.

But when I move the model to gpus using model.to(device). It get stuck on this step with kernel status= busy. it does not get past this step.

I will try docker container next


---

### 评论 #5 — atifkhanncl (2024-11-19T14:13:08Z)

Hi @harkgill-amd ,
I am trying docker image as follows
1. I have to use singularity instead of docker due to our organisation's security policy. But this should not make any difference
2. I pull a rocm pytorch image (tried rocm/pytorch:latest, pytorch:latest-release, pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0
  )
3. run it as follows `
singularity exec --bind /path/to/mount:/mnt pytorch_rocm6.2_ubuntu20.04.sif /bin/bash`
4. This starts a container on GPU node but when i check if it has pytorch by  `python -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'` it returns Failure. The docker images I pulled says they should have pytorch pre-installed. Can you see what is happening here?

---

### 评论 #6 — harkgill-amd (2024-11-27T22:03:47Z)

I gave singularity a try with the `rocm/pytorch` image and was able to run both the MNIST and PyTorch Lightning samples on gfx908. 

> sudo dnf install dkms prior to running dkms status. With this, we're trying to see if amdgpu-dkms was successfully installed and is the correct version. If the sample does not work within the docker container, the dkms would be the last component related to the host installation.

Can you try the aforementioned steps to see if amdgpu-dkms is installed correctly? If possible, could you also set the environment variable `export AMD_LOG_LEVEL=3` and reproduce the `invalid device function` error either in the conda environment or container? This should provide a more detailed look at what's causing the error to be thrown.

---

### 评论 #7 — harkgill-amd (2025-01-13T21:22:58Z)

Closing this issue out for now. If you're still encountering the `RuntimeError: HIP error: invalid argument`, please provide the log output with `AMD_LOG_LEVEL=3` set. 

---
