# [Issue]: ROCm 5.7 + RX 7600 (RDNA3/gfx1102) on Ubuntu 24.04: PyTorch sees GPU, but first HIP kernel fails (“shared object initialization failed”)

> **Issue #5555**
> **状态**: closed
> **创建时间**: 2025-10-21T18:40:06Z
> **更新时间**: 2025-11-18T10:53:53Z
> **关闭时间**: 2025-11-17T16:52:51Z
> **作者**: shifrin8101
> **标签**: status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5555

## 标签

- **status: triage** (颜色: #585dd7)

## 负责人

- harkgill-amd

## 描述

### Problem Description

Pytorch fails with GPU after kernel upgrade.
After routine Ubuntu updates on a system running ROCm 5.7 with an AMD Radeon RX 7600 XT (RDNA3 / gfx1102), PyTorch still detects the GPU (torch.cuda.is_available() == True, get_device_name(0) -> "AMD Radeon RX 7600 XT"), but the first GPU kernel fails with:

RuntimeError: HIP error: shared object initialization failed

This happens on the first operation that actually launches a kernel (e.g., tensor.fill_(0) or torch.zeros(...)). Pure allocations like torch.empty(..., device="cuda") succeed (no kernel launch). Earlier, this setup required HSA_OVERRIDE_GFX_VERSION=11.0.0 and worked; after the updates it no longer does.

### Operating System

OS: NAME="Ubuntu" VERSION="24.04.3 LTS  6.14.0-29-generic  (Noble Numbat)"

### CPU

CPU:  model name	: Intel(R) Core(TM) i5-14400

### GPU

Radeon RX 7600 XT (gfx1102)

### ROCm Version

5.7

### ROCm Component

_No response_

### Steps to Reproduce

ROCm 5.7 + RX 7600 (RDNA3/gfx1102) on Ubuntu 24.04: PyTorch sees GPU, but first HIP kernel fails (“shared object initialization failed”)

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

PyTorch build tag: 2.3.1+rocm5.7

HIP runtime (torch): 5.7.31921-d1770ee1b

hip-runtime-amd: 5.7.31921.50700-63~22.04

libhsa-runtime64-1: 5.7.1-2build1

hsa-rocr-dev: 1.11.0.50700-63~22.04 (this 1.11.0 corresponds to ROCm 5.7)

rocminfo: 1.0.0.50700-63~22.04

---

## 评论 (29 条)

### 评论 #1 — shifrin8101 (2025-10-21T19:26:15Z)

adding output of 
sudo dmesg | grep -i -e kfd -e amdgpu | tail -n 200
in dmesg.txt
and summary of the system in more_info.txt

[more_info.txt](https://github.com/user-attachments/files/23030364/more_info.txt)

[dmesg.txt](https://github.com/user-attachments/files/23030323/dmesg.txt)

---

### 评论 #2 — harkgill-amd (2025-10-21T19:40:01Z)

Hey @shifrin8101, we actually ship `gfx1102` supported ROCm and torch wheels through TheRock making it so that you don't need the `HSA_OVERRIDE_GFX_VERSION` workaround anymore. Could you remove this environment variable and give the steps from https://github.com/ROCm/TheRock/blob/main/RELEASES.md#installing-releases-using-pip a try? Specifically,
```
python -m venv .venv
source .venv/bin/activate

python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ \
  "rocm[libraries,devel]"

python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ \
  --pre torch torchaudio torchvision
```
Then run `python3 -c 'import torch; print(torch.cuda.is_available())'` to see if your ROCm + torch installation is working correctly. If everything looks good at this point, give the previously failing workload another try with this setup. If you have any questions please let me know.

---

### 评论 #3 — shifrin8101 (2025-10-23T13:44:48Z)

Hello, thanks for the response,
I tried all this, and the last command returned True.
but then , when I changed the run config in Pycharm to use the new env - linux crashed.
After I restarted - it was no longer returning True.
I repeated all steps and the output is below.
I also suspect that I made some mess within pycharm environment options. Because it is suspicious that after reboot it stopped even recognizing GPU. however, also any new kernel updates could take effect. 
just for the clarity it is now:
Distro: Ubuntu 24.04.3 LTS
Kernel: 6.14.0-33-generic
Build: #33~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Sep 19 17:02:30 UTC 2
Arch: x86_64



 python -m vpython -m venv .venv
source .venv/bin/activate



python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ \
  "rocm[libraries,devel]"

python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ \
  --pre torch torchaudio torchvision
Looking in indexes: https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/
Requirement already satisfied: rocm[devel,libraries] in ./.venv/lib/python3.12/site-packages (7.10.0a20251015)
Requirement already satisfied: rocm-sdk-core==7.10.0a20251015 in ./.venv/lib/python3.12/site-packages (from rocm[devel,libraries]) (7.10.0a20251015)
Requirement already satisfied: rocm-sdk-libraries-gfx110X-dgpu==7.10.0a20251015 in ./.venv/lib/python3.12/site-packages (from rocm[devel,libraries]) (7.10.0a20251015)
Collecting rocm-sdk-devel==7.10.0a20251015 (from rocm[devel,libraries])
  Downloading https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/rocm_sdk_devel-7.10.0a20251015-py3-none-linux_x86_64.whl (1698.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 GB 7.0 MB/s eta 0:00:00
Installing collected packages: rocm-sdk-devel
  Attempting uninstall: rocm-sdk-devel
    Found existing installation: rocm-sdk-devel 7.10.0a20251022
    Uninstalling rocm-sdk-devel-7.10.0a20251022:
      Successfully uninstalled rocm-sdk-devel-7.10.0a20251022
Successfully installed rocm-sdk-devel-7.10.0a20251015
Looking in indexes: https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/
Requirement already satisfied: torch in ./.venv/lib/python3.12/site-packages (2.10.0a0+rocm7.10.0a20251015)
Requirement already satisfied: torchaudio in ./.venv/lib/python3.12/site-packages (2.8.0a0+rocm7.10.0a20251015)
Requirement already satisfied: torchvision in ./.venv/lib/python3.12/site-packages (0.25.0a0+rocm7.10.0a20251015)
Requirement already satisfied: filelock in ./.venv/lib/python3.12/site-packages (from torch) (3.19.1)
Requirement already satisfied: typing-extensions>=4.10.0 in ./.venv/lib/python3.12/site-packages (from torch) (4.14.1)
Requirement already satisfied: setuptools in ./.venv/lib/python3.12/site-packages (from torch) (80.9.0)
Requirement already satisfied: sympy>=1.13.3 in ./.venv/lib/python3.12/site-packages (from torch) (1.14.0)
Requirement already satisfied: networkx>=2.5.1 in ./.venv/lib/python3.12/site-packages (from torch) (3.5)
Requirement already satisfied: jinja2 in ./.venv/lib/python3.12/site-packages (from torch) (3.1.6)
Requirement already satisfied: fsspec>=0.8.5 in ./.venv/lib/python3.12/site-packages (from torch) (2025.7.0)
Requirement already satisfied: rocm==7.10.0a20251015 in ./.venv/lib/python3.12/site-packages (from rocm[libraries]==7.10.0a20251015->torch) (7.10.0a20251015)
Requirement already satisfied: pytorch-triton-rocm==3.5.0+gitc79db9c3.rocm7.10.0a20251015 in ./.venv/lib/python3.12/site-packages (from torch) (3.5.0+gitc79db9c3.rocm7.10.0a20251015)
Requirement already satisfied: rocm-sdk-core==7.10.0a20251015 in ./.venv/lib/python3.12/site-packages (from rocm==7.10.0a20251015->rocm[libraries]==7.10.0a20251015->torch) (7.10.0a20251015)
Requirement already satisfied: rocm-sdk-libraries-gfx110X-dgpu==7.10.0a20251015 in ./.venv/lib/python3.12/site-packages (from rocm[libraries]==7.10.0a20251015->torch) (7.10.0a20251015)
Requirement already satisfied: numpy in ./.venv/lib/python3.12/site-packages (from torchvision) (2.3.2)
Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in ./.venv/lib/python3.12/site-packages (from torchvision) (11.3.0)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./.venv/lib/python3.12/site-packages (from sympy>=1.13.3->torch) (1.3.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./.venv/lib/python3.12/site-packages (from jinja2->torch) (3.0.2)
(.venv) mark$:14:45:15:~/PycharmProjects/WSN-MA > python3 -c 'import torch; print(torch.cuda.is_available())'
False
(.venv) mark$:14:45:43:~/PycharmProjects/WSN-MA > 



in addition 

the following is also not looking good:
import torch
torch.cuda.init()
Failed to parse CPUID
Traceback (most recent call last):
  File "/home/mark/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/plugins/python/helpers-pro/pydevd_asyncio/pydevd_asyncio_utils.py", line 117, in _exec_async_code
    result = func()
             ^^^^^^
  File "<input>", line 1, in <module>
  File "/home/mark/PycharmProjects/WSN-MA/venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 269, in init
    _lazy_init()
  File "/home/mark/PycharmProjects/WSN-MA/venv/lib/python3.12/site-packages/torch/cuda/__init__.py", line 302, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No HIP GPUs are available





---

### 评论 #4 — harkgill-amd (2025-10-23T20:12:32Z)

Does your regular ROCm 5.7 installation still see the GPU with `rocminfo`? 

> I tried all this, and the last command returned True.

Looks like everything was fine at first. If you're thinking Pycharm may have corrupted the environment, maybe try creating a new venv with a different name and running the install again.

---

### 评论 #5 — shifrin8101 (2025-10-24T16:43:57Z)

Hello,
updating, reminding on system details:
OS / Kernel: Ubuntu 24.04 (noble), kernel 6.14.0-29-generic.

GPU: Radeon RX 7600 XT (RDNA3, gfx1102).

Device nodes / perms: /dev/kfd and /dev/dri/renderD129 exist; both group render; my user is in render.

ROCm userspace (5.7) from jammy repo on noble:

hip-runtime-amd 5.7.31921.50700-63~22.04

hsa-rocr-dev 1.11.0.50700-63~22.04

libhsa-runtime64-1 5.7.1-2build1

rocminfo 1.0.0.50700-63~22.04

Libraries at /opt/rocm-5.7.0/hip/lib and /opt/rocm-5.7.0/lib.

PyTorch (ROCm 5.7 wheels): torch 2.3.1+rocm5.7 shows hip 5.7.31921-… but torch.cuda.is_available() = False (device count 0), even with

export LD_LIBRARY_PATH=/opt/rocm-5.7.0/hip/lib:/opt/rocm-5.7.0/lib:$LD_LIBRARY_PATH
export HSA_OVERRIDE_GFX_VERSION=11.0.0

(not sure it that was a good step to do)

rocminfo: previously failed with HSA_STATUS_ERROR_OUT_OF_RESOURCES.

so now nothing even starts with gpu, after this unfortunate linux crash.

so may I also ask the following questions:
Is ROCm 5.7 userspace on noble (via jammy repo) supported for gfx1102, or do I need a specific kernel/ROCr combo?
Which minimal packages (and versions) should be present for HIP runtime/ROCr on noble?
Any preferred diagnostics beyond rocminfo (which currently errors) to pinpoint why KFD/ROCr

As of pycharm envs, I reinstalled new env according to your instructions, I so not think it is a pycharm issue. but this is only my opinion

---

### 评论 #6 — harkgill-amd (2025-10-24T17:53:50Z)

Just to confirm, your ROCm 5.7 installation was previously correctly running `rocminfo` w/ your GPU listed but is now erroring with `HSA_STATUS_ERROR_OUT_OF_RESOURCES`? This is outside the venv correct?


> Is ROCm 5.7 userspace on noble (via jammy repo) supported for gfx1102, or do I need a specific kernel/ROCr combo?

ROCm 5.7 does not support gfx1102. The wheels from TheRock I shared with you earlier are the recommended approach for running ROCm with gfx1102. These contain all the necessary dependencies to get started with ROCm + Torch. You don't need a specific kernel, 6.14.0-29-generic is fine. 

> Which minimal packages (and versions) should be present for HIP runtime/ROCr on noble?

All the packaging for the TheRock wheels is handled via pip in the venv. The only packages you need should already be installed in your virtual environment after running the pip install commands. They should look something like this 
```
pip list
Package                         Version
------------------------------- -------------------------------------
...
pytorch-triton-rocm             3.5.0+gitc79db9c3.rocm7.10.0a20251015
rocm                            7.10.0a20251015
rocm-sdk-core                   7.10.0a20251015
rocm-sdk-devel                  7.10.0a20251022
rocm-sdk-libraries-gfx110X-dgpu 7.10.0a20251015
...
torch                           2.10.0a0+rocm7.10.0a20251015
torchaudio                      2.8.0a0+rocm7.10.0a20251015
torchvision                     0.25.0a0+rocm7.10.0a20251015
```

> Any preferred diagnostics beyond rocminfo (which currently errors) to pinpoint why KFD/ROCr

If `rocminfo` is failing both inside and outside the venv, we'd want to first check if your GPU is detected at the HW level. Do you see your GPU listed in the output of `lspci | grep VGA`? Please also share the outputs of `lsmod | grep amdgpu` and `modinfo amdgpu -n`.

---

### 评论 #7 — shifrin8101 (2025-10-24T19:08:25Z)

Previously I didn’t run rocminfo; PyTorch worked on ROCm 5.7 only with HSA_OVERRIDE_GFX_VERSION=11.0.0. (was ur advise amd it was perfect) Now, outside any venv, rocminfo fails with HSA_STATUS_ERROR_OUT_OF_RESOURCES.

here are the outputs:

(WSN) mark$:19:32:28:~/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/bin > lspci | grep VGA
03:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Navi 33 [Radeon RX 7700S/7600/7600S/7600M XT/PRO W7600] (rev c0)

(WSN) mark$:21:27:40:~/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/bin > lsmod | grep amdgpu
amdgpu              19718144  0
amdxcp                 12288  1 amdgpu
gpu_sched              61440  2 amdgpu,xe
drm_panel_backlight_quirks    12288  1 amdgpu
drm_buddy              24576  3 amdgpu,xe,i915
drm_ttm_helper         16384  2 amdgpu,xe
drm_exec               12288  3 drm_gpuvm,amdgpu,xe
ttm                   118784  4 amdgpu,drm_ttm_helper,xe,i915
drm_suballoc_helper    20480  2 amdgpu,xe
drm_display_helper    278528  3 amdgpu,xe,i915
cec                    94208  4 drm_display_helper,amdgpu,xe,i915
i2c_algo_bit           16384  3 amdgpu,xe,i915
video                  77824  3 amdgpu,xe,i915

(WSN) mark$:21:28:18:~/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/bin > modinfo amdgpu -n
/lib/modules/6.14.0-33-generic/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko.zst




---

### 评论 #8 — harkgill-amd (2025-10-24T19:11:15Z)

Everything looks fine from HW/driver side. Can you try to run `rocminfo` and `which rocminfo` inside the venv and share the output?

---

### 评论 #9 — shifrin8101 (2025-10-25T12:17:25Z)

same answer whatever env is loaded

(WSN) mark$:11:58:31:~/PycharmProjects/WSN-MA > rocminfo
ROCk module is loaded
hsa api call failure at: /therock/src/rocm-systems/projects/rocminfo/rocminfo.cc:1324
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.

(WSN) mark$:15:10:09:~/PycharmProjects/WSN-MA > which rocminfo
/home/mark/PycharmProjects/WSN-MA/.venv/bin/rocminfo


(base) (.venv) mark$:15:15:36:~/PycharmProjects/WSN-MA > rocminfo
ROCk module is loaded

hsa api call failure at: /therock/src/rocm-systems/projects/rocminfo/rocminfo.cc:1324
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.
(base) (.venv) mark$:15:16:11:~/PycharmProjects/WSN-MA > which rocminfo
/home/mark/PycharmProjects/WSN-MA/.venv/bin/rocminfo



---

### 评论 #10 — harkgill-amd (2025-10-27T20:47:10Z)

Could you uninstall the ROCm 5.7 on your baremetal system with the following commands,
```
sudo amdgpu-install --uninstall --rocmrelease=all
sudo apt purge amdgpu-install
sudo apt autoremove
```
Then could you share the output of the following commands within the previously setup venv,

- ls -l /dev/kfd
- groups
- rocm-smi
- sudo rocminfo

---

### 评论 #11 — shifrin8101 (2025-10-28T08:01:13Z)

Hi,
I made the installations first on scratch linux terminal outside pycharm.
I reinstalled then again the venv again according to the instructions you earlier sent.
note that I created this venv from some (base) environment becuase otherwise would not even have pip
then I just deactivated that base
please let me know if you think I did this wrong.
below is the ouput from pycharm terminal.

(.venv) mark$:09:57:13:~ > ls -l /dev/kfd
crw-rw---- 1 root render 511, 0 Oct 21 19:44 /dev/kfd
(.venv) mark$:09:57:34:~ > groups
mark adm cdrom sudo dip video plugdev users lpadmin render
(.venv) mark$:09:57:46:~ > rocm-smi


WARNING: AMD GPU device(s) is/are in a low-power state. Check power control/runtime_status

======================================== 

ROCm System Management Interface
 ========================================
================================================== Concise Info ==================================================
Device  Node  IDs              Temp    Power  Partitions          SCLK  MCLK  Fan  Perf     PwrCap  VRAM%  GPU%  
              (DID,     GUID)  (Edge)  (Avg)  (Mem, Compute, ID)                                                 
==================================================================================================================
0       1     0x7480,   42634  N/A     N/A    N/A, N/A, 0         N/A   N/A   0%   unknown  N/A     0%     0%    
==================================================================================================================
============================================== End of ROCm SMI Log ===============================================
(.venv) mark$:09:57:58:~ > sudo rocminfo
sudo: rocminfo: command not found
(.venv) mark$:09:58:11:~ > 

<img width="1441" height="666" alt="Image" src="https://github.com/user-attachments/assets/db1e7e20-9281-4e64-ab7e-9bf7669c225e" />

added screenshot for clarity

---

### 评论 #12 — harkgill-amd (2025-10-30T20:49:07Z)

> note that I created this venv from some (base) environment becuase otherwise would not even have pip
then I just deactivated that base

The base environment that you're referring to might be coming from conda - can you try to create the venv from scratch without this. On Ubuntu 24.04, you should be able to run the commands in https://github.com/ROCm/ROCm/issues/5555#issuecomment-3429209542 in a standard terminal. If you're seeing `python not found` errors, use `python3` for the initial venv creation command.

---

### 评论 #13 — shifrin8101 (2025-11-01T12:03:43Z)

Hi,
the point is that I have python and python3 associated with anaconda,  see this:

mark$:14:01:02:~/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/bin > python3
Python 3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 15:12:24) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

do you have an idea how to fix this and to have a regular python instead? trying to figure out, meanwhile



---

### 评论 #14 — shifrin8101 (2025-11-01T16:48:06Z)

Hello, I removed the anaconda python from bashrc at all, and used the default python, just in a terminal outside pycharm, as u advised.
Unfortunately, I still get "False"
I am pasting below the entire installation output, in the case maybe you see there something suspicious.
There were some warnings but it looked as installation succeeded, so at the moment I do not know how to proceed. :(
Thank you!

(.venv) mark$:18:35:41:~/PycharmProjects/WSN-MA > python -m ppython -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ \
  "rocm[libraries,devel]"
Looking in indexes: https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7742e2bdc6b0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution')': /v2/gfx110X-dgpu/rocm/
Collecting rocm[devel,libraries]
  Using cached rocm-7.10.0a20251022-py3-none-any.whl
Collecting rocm-sdk-core==7.10.0a20251022 (from rocm[devel,libraries])
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/rocm_sdk_core-7.10.0a20251022-py3-none-linux_x86_64.whl (277.4 MB)
Collecting rocm-sdk-libraries-gfx110X-dgpu==7.10.0a20251022 (from rocm[devel,libraries])
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/rocm_sdk_libraries_gfx110x_dgpu-7.10.0a20251022-py3-none-linux_x86_64.whl (351.4 MB)
Collecting rocm-sdk-devel==7.10.0a20251022 (from rocm[devel,libraries])
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/rocm_sdk_devel-7.10.0a20251022-py3-none-linux_x86_64.whl (1724.3 MB)
Installing collected packages: rocm-sdk-libraries-gfx110X-dgpu, rocm-sdk-devel, rocm-sdk-core, rocm
Successfully installed rocm-7.10.0a20251022 rocm-sdk-core-7.10.0a20251022 rocm-sdk-devel-7.10.0a20251022 rocm-sdk-libraries-gfx110X-dgpu-7.10.0a20251022
(.venv) mark$:18:36:55:~/PycharmProjects/WSN-MA > python -m ppython -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ \
  --pre torch torchaudio torchvision
Looking in indexes: https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/
Collecting torch
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/torch-2.10.0a0%2Brocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (236.2 MB)
Collecting torchaudio
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/torchaudio-2.8.0a0%2Brocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (491 kB)
Collecting torchvision
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/torchvision-0.25.0a0%2Brocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (1.8 MB)
Collecting filelock (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/filelock-3.19.1-py3-none-any.whl (15 kB)
Collecting typing-extensions>=4.10.0 (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/typing_extensions-4.14.1-py3-none-any.whl (43 kB)
Collecting setuptools (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/setuptools-80.9.0-py3-none-any.whl (1.2 MB)
Collecting sympy>=1.13.3 (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/sympy-1.14.0-py3-none-any.whl (6.3 MB)
Collecting networkx>=2.5.1 (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/networkx-3.5-py3-none-any.whl (2.0 MB)
Collecting jinja2 (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/jinja2-3.1.6-py3-none-any.whl (134 kB)
Collecting fsspec>=0.8.5 (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/fsspec-2025.7.0-py3-none-any.whl (199 kB)
Collecting rocm==7.10.0a20251015 (from rocm[libraries]==7.10.0a20251015->torch)
  Using cached rocm-7.10.0a20251015-py3-none-any.whl
Collecting pytorch-triton-rocm==3.5.0+gitc79db9c3.rocm7.10.0a20251015 (from torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/pytorch_triton_rocm-3.5.0%2Bgitc79db9c3.rocm7.10.0a20251015-cp312-cp312-linux_x86_64.whl (317.1 MB)
Collecting rocm-sdk-core==7.10.0a20251015 (from rocm==7.10.0a20251015->rocm[libraries]==7.10.0a20251015->torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/rocm_sdk_core-7.10.0a20251015-py3-none-linux_x86_64.whl (265.8 MB)
Collecting rocm-sdk-libraries-gfx110X-dgpu==7.10.0a20251015 (from rocm[libraries]==7.10.0a20251015->torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/rocm_sdk_libraries_gfx110x_dgpu-7.10.0a20251015-py3-none-linux_x86_64.whl (351.5 MB)
Collecting numpy (from torchvision)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/numpy-2.3.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.6 MB)
Collecting pillow!=8.3.*,>=5.3.0 (from torchvision)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/pillow-11.3.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
Collecting mpmath<1.4,>=1.1.0 (from sympy>=1.13.3->torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/mpmath-1.3.0-py3-none-any.whl (536 kB)
Collecting MarkupSafe>=2.0 (from jinja2->torch)
  Using cached https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/MarkupSafe-3.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (23 kB)
Installing collected packages: rocm-sdk-libraries-gfx110X-dgpu, rocm-sdk-core, mpmath, typing-extensions, sympy, setuptools, pytorch-triton-rocm, pillow, numpy, networkx, MarkupSafe, fsspec, filelock, jinja2, rocm, torch, torchvision, torchaudio
  Attempting uninstall: rocm-sdk-libraries-gfx110X-dgpu
    Found existing installation: rocm-sdk-libraries-gfx110X-dgpu 7.10.0a20251022
    Uninstalling rocm-sdk-libraries-gfx110X-dgpu-7.10.0a20251022:
      Successfully uninstalled rocm-sdk-libraries-gfx110X-dgpu-7.10.0a20251022
  Attempting uninstall: rocm-sdk-core
    Found existing installation: rocm-sdk-core 7.10.0a20251022
    Uninstalling rocm-sdk-core-7.10.0a20251022:
      Successfully uninstalled rocm-sdk-core-7.10.0a20251022
  Attempting uninstall: rocm
    Found existing installation: rocm 7.10.0a20251022
    Uninstalling rocm-7.10.0a20251022:
      Successfully uninstalled rocm-7.10.0a20251022
Successfully installed MarkupSafe-3.0.2 filelock-3.19.1 fsspec-2025.7.0 jinja2-3.1.6 mpmath-1.3.0 networkx-3.5 numpy-2.3.2 pillow-11.3.0 pytorch-triton-rocm-3.5.0+gitc79db9c3.rocm7.10.0a20251015 rocm-7.10.0a20251015 rocm-sdk-core-7.10.0a20251015 rocm-sdk-libraries-gfx110X-dgpu-7.10.0a20251015 setuptools-80.9.0 sympy-1.14.0 torch-2.10.0a0+rocm7.10.0a20251015 torchaudio-2.8.0a0+rocm7.10.0a20251015 torchvision-0.25.0a0+rocm7.10.0a20251015 typing-extensions-4.14.1
(.venv) mark$:18:42:53:~/PycharmProjects/WSN-MA > python3 -c 'import torch; print(torch.cuda.is_available())'
False


---

### 评论 #15 — harkgill-amd (2025-11-04T22:03:50Z)

Thanks for trying that out. The `HSA_STATUS_ERROR_OUT_OF_RESOURCES` is likely the culprit of why cuda.is_available is reporting false - if ROCm can't detect your GPU, higher level frameworks like PyTorch won't be able to either. The outputs of lsmod | grep amdgpu and modinfo amdgpu -n indicate that the amdpgu driver from your Linux kernel was loaded correctly . Can you share the outputs of `sudo dmesg | grep amdgpu` and `printenv` for one last data point?


Also, give the ROCm docker image a try, this'll help eliminate any user space discrepancies.
```
docker run -it \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add video \
    --ipc=host \
    --shm-size 8G \
   rocm/dev-ubuntu-24.04:latest
```
This should launch the container and give you terminal access where you can try to run `rocminfo` and check to see if it works.

---

### 评论 #16 — shifrin8101 (2025-11-05T09:55:15Z)

[amdgpu.txt](https://github.com/user-attachments/files/23356212/amdgpu.txt)


[printemv.txt](https://github.com/user-attachments/files/23356256/printemv.txt)


Hello,
Attached output of the 2 commands as txt files.

I am not acknowledged in working with docker work. 
I think this should be the output:
root@134179dd001d:/# rocminfo
ROCk module is loaded
hsa api call failure at: /longer_pathname_so_that_rpms_can_support_packaging_the_debug_info_for_all_os_profiles/src/rocm-systems/projects/rocminfo/rocminfo.cc:1324
Call returned HSA_STATUS_ERROR_OUT_OF_RESOURCES: The runtime failed to allocate the necessary resources. This error may also occur when the core runtime library needs to spawn threads or create internal OS-specific events.


If you think I did something wrong about the docker please let me know and Iw ill proceed as you say, 
thanks!

---

### 评论 #17 — harkgill-amd (2025-11-05T20:05:19Z)

These errors from your dmesg are potentially causing the HSA_STATUS_ERROR_OUT_OF_RESOURCES.
```
amdgpu 0000:03:00.0: amdgpu: MES failed to respond to msg=ADD_QUEUE
[146328.903574] [drm:amdgpu_mes_add_hw_queue [amdgpu]] *ERROR* failed to add hardware queue to MES, doorbell=0x80a
[146331.041805] amdgpu 0000:03:00.0: amdgpu: MES ring buffer is full.
[146333.179237] amdgpu 0000:03:00.0: amdgpu: MES ring buffer is full.
[146333.179268] [drm:amdgpu_mes_self_test [amdgpu]] *ERROR* failed to add ring
[146335.316582] amdgpu 0000:03:00.0: amdgpu: MES ring buffer is full.
[146337.453492] amdgpu 0000:03:00.0: amdgpu: MES ring buffer is full.
```
We've seen these errors on earlier builds of ROCm but they've since been root caused and resolved in the latest releases. Do these errors, and by extension the HSA_STATUS_ERROR_OUT_OF_RESOURCES with rocminfo, persist after rebooting? If so, can you try installing the latest `amdgpu-dkms` package and rebooting as well?
```
wget https://repo.radeon.com/amdgpu-install/7.1/ubuntu/noble/amdgpu-install_7.1.70100-1_all.deb
sudo apt install ./amdgpu-install_7.1.70100-1_all.deb
sudo apt update
sudo apt install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
sudo apt install amdgpu-dkms
```

---

### 评论 #18 — shifrin8101 (2025-11-06T06:52:44Z)

Hello,
The outputs are different after reboot, 
I tried both just terminal and the docker again.
the MES ring error is not seen, but it does not look clean of errors either.
Hence, so far, I did not apply the wget set of commands with amdgpu-dkms reinstallation, waiting for your advice.
Thanks!

[rocminfo_blank_terminal.txt](https://github.com/user-attachments/files/23383517/rocminfo_blank_terminal.txt)
[printemv2.txt](https://github.com/user-attachments/files/23383519/printemv2.txt)
[amdgpu2.txt](https://github.com/user-attachments/files/23383518/amdgpu2.txt)

docker rocminfo output is right below:
mark$:08:45:46:~ > docker run docker run -it \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --device=/dev/kfd \
    --device=/dev/dri \
    --group-add video \
    --ipc=host \
    --shm-size 8G \
   rocm/dev-ubuntu-24.04:latest
root@24e1f96dce79:/# rocminfo
ROCk module is loaded
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.18
Runtime Ext Version:     1.14
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             
Mwaitx:                  DISABLED
XNACK enabled:           NO
DMAbuf Support:          YES
VMM Support:             YES

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    Intel(R) Core(TM) i5-14400         
  Uuid:                    CPU-XX                             
  Marketing Name:          Intel(R) Core(TM) i5-14400         
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
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   4700                               
  BDFID:                   0                                  
  Internal Node ID:        0                                  
  Compute Unit:            16                                 
  SIMDs per CU:            0                                  
  Shader Engines:          0                                  
  Shader Arrs. per Eng.:   0                                  
  WatchPts on Addr. Ranges:1                                  
  Memory Properties:       
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: FINE GRAINED        
      Size:                    16138032(0xf63f30) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16138032(0xf63f30) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 3                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16138032(0xf63f30) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
    Pool 4                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16138032(0xf63f30) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
*******                  
Agent 2                  
*******                  
  Name:                    gfx1102                            
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Radeon RX 7600 XT              
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
    L2:                      2048(0x800) KB                     
  Chip ID:                 29824(0x7480)                      
  ASIC Revision:           0(0x0)                             
  Cacheline Size:          128(0x80)                          
  Max Clock Freq. (MHz):   2539                               
  BDFID:                   768                                
  Internal Node ID:        1                                  
  Compute Unit:            32                                 
  SIMDs per CU:            2                                  
  Shader Engines:          2                                  
  Shader Arrs. per Eng.:   2                                  
  WatchPts on Addr. Ranges:4                                  
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
    x                        2147483647(0x7fffffff)             
    y                        65535(0xffff)                      
    z                        65535(0xffff)                      
  Max fbarriers/Workgrp:   32                                 
  Packet Processor uCode:: 550                                
  SDMA engine uCode::      16                                 
  IOMMU Support::          None                               
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: COARSE GRAINED      
      Size:                    16760832(0xffc000) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Recommended Granule:2048KB                             
      Alloc Alignment:         4KB                                
      Accessible by all:       FALSE                              
    Pool 2                   
      Segment:                 GLOBAL; FLAGS: EXTENDED FINE GRAINED
      Size:                    16760832(0xffc000) KB              
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
      Name:                    amdgcn-amd-amdhsa--gfx1102         
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
    ISA 2                    
      Name:                    amdgcn-amd-amdhsa--gfx11-generic   
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
        x                        2147483647(0x7fffffff)             
        y                        65535(0xffff)                      
        z                        65535(0xffff)                      
      FBarrier Max Size:       32                                 
*** Done ***             


---

### 评论 #19 — harkgill-amd (2025-11-06T15:39:44Z)

Your new dmesg + rocminfo output looks good - can you try running `torch.cuda.is_available()` in your venv now?

---

### 评论 #20 — shifrin8101 (2025-11-06T20:04:25Z)

It returned true, but now I am back to this
import sys; print('Python %s on %s' % (sys.version, sys.platform))
/home/mark/anaconda3/envs/WSN/bin/python /home/mark/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/plugins/python-ce/helpers/pydev/pydevd.py --multiprocess --qt-support=auto --port 29781 --file /home/mark/PycharmProjects/WSN-MA/mainSimLinux.py 
device name [0]: AMD Radeon RX 7600 XT  GPU is available
Traceback (most recent call last):
  File "/home/mark/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/plugins/python-ce/helpers/pydev/pydevd.py", line 1570, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/plugins/python-ce/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/home/mark/PycharmProjects/WSN-MA/mainSimLinux.py", line 49, in <module>
    _tmp.fill_(0)
RuntimeError: HIP error: shared object initialization failed
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


 for some reason I am stuck with this anaconda on top of any env I create

---

### 评论 #21 — shifrin8101 (2025-11-06T20:19:16Z)

Update -  i purged the Anaconda for good, but still have the error. 
Radeon 7600 is recognized though.

[rocminfo_latest.txt](https://github.com/user-attachments/files/23401758/rocminfo_latest.txt)

device name [0]: AMD Radeon RX 7600 XT  GPU is available
Traceback (most recent call last):
  File "/home/mark/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/plugins/python-ce/helpers/pydev/pydevd.py", line 1570, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/pycharm-professional-2024.1.4/pycharm-2024.2.0.1/plugins/python-ce/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/home/mark/PycharmProjects/WSN-MA/mainSimLinux.py", line 49, in <module>
    _tmp.fill_(0)
RuntimeError: HIP error: shared object initialization failed
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.


---

### 评论 #22 — harkgill-amd (2025-11-06T21:09:57Z)

Could you share the output of `python -c "import sys; print(sys.executable)"` and `pip list`, just want to confirm you're venv is configured correctly and in use. Also, if you could share the `mainSimLinux.py` script or a small reproducer, I can give it a try on my end as well.

---

### 评论 #23 — shifrin8101 (2025-11-07T19:35:02Z)


Hi, thanks for you help, 
I attach here a simpler file that fails with the same error, sample_prog.py.
The mainSimLinux.py is just too heavy and includes plenty of imports I do not want you to get confused over all the additional unrelated files.
Note that the error is different if I include/exclude 
os.environ['HSA_OVERRIDE_GFX_VERSION'] = '11.0.0'
The line you previously recommended.

Here are the other outputs:

[sample_prog.py](https://github.com/user-attachments/files/23424622/sample_prog.py)

(venv) mark$:22:18:18:~ > python -c "python -c "import sys; print(sys.executable)"
/home/mark/PycharmProjects/WSN-MA/venv/bin/python
(venv) mark$:21:26:01:~ > pip list
Package               Version
--------------------- --------------
attrs                 23.2.0
Babel                 2.10.3
bcc                   0.29.1
bcrypt                3.2.2
blinker               1.7.0
Brlapi                0.8.5
certifi               2023.11.17
chardet               5.2.0
click                 8.1.6
cloud-init            25.2
colorama              0.4.6
command-not-found     0.3
configobj             5.0.8
contourpy             1.2.1
cryptography          41.0.7
cupshelpers           1.0
cycler                0.12.1
dbus-python           1.3.2
defer                 1.0.6
dill                  0.4.0
distro                1.9.0
distro-info           1.7+build1
duplicity             2.1.4
executing             2.0.1
fasteners             0.18
filelock              3.13.1
fonttools             4.53.1
fsspec                2024.2.0
httplib2              0.20.4
idna                  3.6
Jinja2                3.1.2
joblib                1.4.2
jsonpatch             1.32
jsonpickle            3.2.2
jsonpointer           2.0
jsonschema            4.10.3
kiwisolver            1.4.5
kmeans                1.0.2
language-selector     0.1
launchpadlib          1.11.0
lazr.restfulclient    0.14.6
lazr.uri              1.0.6
louis                 3.29.0
Mako                  1.3.2.dev0
markdown-it-py        3.0.0
MarkupSafe            2.1.5
matplotlib            3.9.2
mdurl                 0.1.2
monotonic             1.6
mpmath                1.3.0
netaddr               0.8.0
networkx              3.2.1
numpy                 1.26.4
oauthlib              3.2.2
olefile               0.46
packaging             24.1
pandas                2.2.3
paramiko              2.12.0
pexpect               4.9.0
pillow                10.2.0
pip                   24.2
ptyprocess            0.7.0
pycairo               1.25.1
pycups                2.0.1
Pygments              2.17.2
PyGObject             3.48.2
PyJWT                 2.7.0
PyNaCl                1.5.0
pyparsing             3.1.1
pyrsistent            0.20.0
pyserial              3.5
python-apt            2.7.7+ubuntu5
python-dateutil       2.8.2
python-debian         0.1.49+ubuntu2
pytorch-triton-rocm   3.0.0
pytz                  2024.1
pyxdg                 0.28
PyYAML                6.0.1
requests              2.31.0
rich                  13.7.1
scikit-learn          1.5.2
scipy                 1.14.1
setuptools            70.0.0
six                   1.16.0
sympy                 1.12
systemd-python        235
threadpoolctl         3.5.0
torch                 2.2.2+rocm5.6
torchaudio            2.2.2+rocm5.6
torchvision           0.17.2+rocm5.6
typing_extensions     4.10.0
tzdata                2024.2
ubuntu-drivers-common 0.0.0
ubuntu-pro-client     8001
ufw                   0.36.2
unattended-upgrades   0.1
urllib3               2.0.7
usb-creator           0.3.16
varname               0.13.3
wadllib               1.3.6
xdg                   5
xkit                  0.0.0


---

### 评论 #24 — harkgill-amd (2025-11-11T15:48:40Z)

The test script worked fine on my end.
```
python test.py 
device name [0]: AMD Radeon Pro W7600  GPU is available
cuda:0
tensor([[ 0.6705, -1.3109],
        [-0.7751, -1.4209]], device='cuda:0', requires_grad=True)
```

Your `pip list` output doesn't have any of the actual TheRock wheels installed - you should be seeing 7.10 ROCm packages similiar to the output shared here https://github.com/ROCm/ROCm/issues/5555#issuecomment-3444263329. Can you remove the 5.6 ROCm packages in your venv with,
```
python -m pip uninstall -y torch torchaudio torchvision pytorch-triton-rocm
```
Then install the latest wheels,
```
python -m pip install \
  --index-url https://rocm.nightlies.amd.com/v2/gfx110X-dgpu/ \
  --pre torch torchaudio torchvision
```
Also remove the HSA_OVERRIDE_GFX_VERSION environment variable, this is no longer needed. Once you've done this, give the script a try. If you're still seeing issues, please share the pip list output and the error message.

---

### 评论 #25 — shifrin8101 (2025-11-12T22:12:18Z)

The program script is RUNNING now
However:
1. I have these annoying warnings at start
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.
/home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: `torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.

even though this directory does not even exist! I thought I purged all anaconda...
2. I am not sure, is it possible I somewhere have 5.7 ROCm remainings?  can it be any mismatch?
I afaid with all thes install/reinstall, ththere is too much junk left on the system

3. Do you think his 7.1 has a longlasting chances on my lame machine? Please advise what should I DO/NOT TO DO to have this going for some time...

4. I consider to remove Pycharm and just to run all from terminal. I will do development elsewhere. do you think pycharm IS THE problem? 


---

### 评论 #26 — harkgill-amd (2025-11-14T15:30:25Z)

> /home/mark/anaconda3/lib/python3.12/site-packages/torch/optim/optimizer.py:412: UserWarning: torch._utils.is_compiling is deprecated. Use torch.compiler.is_compiling instead.

> I am not sure, is it possible I somewhere have 5.7 ROCm remainings? can it be any mismatch?
I afaid with all thes install/reinstall, ththere is too much junk left on the system

Both your ROCm and torch installations should be isolated within the venv. Could you share the ouptut of pip list once last time - just want to confirm the correct packages are installed and the 5.6 ones were removed. The warnings point to an older torch version in use.

> Do you think his 7.1 has a longlasting chances on my lame machine? Please advise what should I DO/NOT TO DO to have this going for some time...

Yes - now that you've switched to using TheRock wheels that actually support your GPU instead of the override, you're getting the latest features and a more stable install. You can choose to stay with ROCm 7.1 if it suits your workflow but you're also free to upgrade your wheels when a new release comes out - simply uninstall the 7.1 wheels and install the latest wheels with the command from https://github.com/ROCm/ROCm/issues/5555#issuecomment-3517540743. 

> I consider to remove Pycharm and just to run all from terminal. I will do development elsewhere. do you think pycharm IS THE problem?

No, I don't think Pycharm directly caused any of the issues here. Your main focus should be on keeping a clean and up to date virtual environment. You can always spin up a fresh venv and quickly install the ROCm/torch packages to get a baseline on whether the user space installation is a problem.

---

### 评论 #27 — shifrin8101 (2025-11-16T07:21:53Z)

[pip_list.txt](https://github.com/user-attachments/files/23566285/pip_list.txt)

Hello,
Thanks again, the pip list output is attached.  I think it is a correct installation now (please correct me if I am wrong)

The point that now I am getting pretty soon the 137 code kill (Process finished with exit code 137 (interrupted by signal 9:SIGKILL))

Which I think is associated with memory difficulties. I know this is not the topic of this thread, but it was not happening with 5.7 before.
I could postpone this event by some garbage collector (gc) commands but it still comes. Are there any known issues with 7.1 on that? 
If you know nothing on that I will just try to somehow debug that.

---

### 评论 #28 — harkgill-amd (2025-11-17T16:52:51Z)

The pip list output looks good now. As for the SIGKILL termination, I haven't seen that reported before against ROCm 7.1 - could you open a new issue with some more information on what the mainSimLinux.py script is doing and how it arrives at the error? Without this, it'll be difficult to debug what the actual root cause of the termination is.

As the originally reported issue in this thread is no longer seen using TheRock wheels, I'm going to close this issue out for the sake of clarity.

---

### 评论 #29 — shifrin8101 (2025-11-18T10:53:53Z)

Yes, you are right, it is possibly another issue.
It runs into this sigkill after several thousands learning steps, so obviously is another issue.
Thanks for dealing with that one, hope it will last working :) 

---
