# [Issue]: "rocminfo" works but device count "0" and cuda is_available "false"

> **Issue #5461**
> **状态**: closed
> **创建时间**: 2025-10-02T08:59:56Z
> **更新时间**: 2025-10-06T11:07:01Z
> **关闭时间**: 2025-10-06T11:07:01Z
> **作者**: ImWarcy
> **标签**: status: assessed
> **URL**: https://github.com/ROCm/ROCm/issues/5461

## 标签

- **status: assessed** (颜色: #e6d813)

## 负责人

- harkgill-amd

## 描述

### Problem Description

I have a Ubuntu WSL installation and im trying to use TTS-Webui with chatterbox but i can't generate audio at all. With the help of the developer of TTS-Webui i did some checks and rocm is installed properly but when using `python -c "import torch; print(f'CUDA/ROCm available: {torch.cuda.is_available()}, Device count: {torch.cuda.device_count()}')"` the output is `CUDA/ROCm available: False, Device count: 0`. On WSL i installed the driver with `amdgpu-install -y --usecase=wsl,rocm --no-dkmsI`. On Windows i originally was on Adrenalin 25.9.2 and it didn't work. I installed 25.3.1 as in this page (https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-6.3.4/docs/compatibility/wsl/wsl_compatibility.html) says that this driver officially supports wsl2 with rocm 6.3.4 but it still doesn't work.

The output of `AMD_LOG_LEVEL=3 python -c "import torch; print(torch.cuda.is_available())"` is 

:3:rocdevice.cpp            :469 : 1341533546d us:  Initializing HSA stack.
:3:hip_context.cpp          :49  : 1341534453d us:  Direct Dispatch: 1
:3:hip_device_runtime.cpp   :649 : 1341534484d us:   hipGetDeviceCount ( 0x7ffee00c60dc )
:3:hip_device_runtime.cpp   :651 : 1341534510d us:  hipGetDeviceCount: Returned hipErrorNoDevice :
:3:hip_error.cpp            :36  : 1341534532d us:   hipGetLastError (  )
:3:hip_error.cpp            :36  : 1341534554d us:  hipGetLastError: Returned hipErrorNoDevice :
False
:3:hip_device_runtime.cpp   :618 : 1341630470d us:   hipDeviceSynchronize (  )
:3:hip_device_runtime.cpp   :618 : 1341630503d us:  hipDeviceSynchronize: Returned hipErrorNoDevice :


### Operating System

Windows 11 Pro / WSL 

### CPU

AMD Ryzen 7 5800x3D

### GPU

AMD Radeon RX 7900GRE

### ROCm Version

ROCm 6.3.42131-fa1d09cbd

### ROCm Component

_No response_

### Steps to Reproduce

wget https://repo.radeon.com/amdgpu-install/6.4.2.1/ubuntu/noble/amdgpu-install_6.4.60402-1_all.deb
sudo apt install ./amdgpu-install_6.4.60402-1_all.deb
amdgpu-install -y --usecase=wsl,rocm --no-dkms

git clone https://github.com/rsxdalv/TTS-WebUI.git
cd TTS-WebUI
sh tools/conda_env_bash.sh
cd ..
AMD_LOG_LEVEL=3 python -c "import torch; print(torch.cuda.is_available())"



### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (15 条)

### 评论 #1 — harkgill-amd (2025-10-02T14:11:15Z)

Hi @ImWarcy, just wanted to confirm, are you using the torch wheels specified at https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-pytorch.html#install-pytorch-via-pip?

---

### 评论 #2 — ImWarcy (2025-10-02T14:29:42Z)

No, im using this one `pip3 install torch torchvision --index-url https://download.pytorch.org/whl/rocm6.3
`

---

### 评论 #3 — harkgill-amd (2025-10-02T14:36:41Z)

Ah that's likely the issue. WSL on ROCm requires the wheels I shared above. The `https://download.pytorch.org/whl/rocm6.3` wheels are meant for use on regular Linux. Could you try running the following,
```
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/torch-2.6.0%2Brocm6.4.2.git76481f7c-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/torchvision-0.21.0%2Brocm6.4.2.git4040d51f-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/pytorch_triton_rocm-3.2.0%2Brocm6.4.2.git7e948ebf-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/torchaudio-2.6.0%2Brocm6.4.2.gitd8831425-cp312-cp312-linux_x86_64.whl
pip3 uninstall torch torchvision pytorch-triton-rocm
pip3 install torch-2.6.0+rocm6.4.2.git76481f7c-cp312-cp312-linux_x86_64.whl torchvision-0.21.0+rocm6.4.2.git4040d51f-cp312-cp312-linux_x86_64.whl torchaudio-2.6.0+rocm6.4.2.gitd8831425-cp312-cp312-linux_x86_64.whl pytorch_triton_rocm-3.2.0+rocm6.4.2.git7e948ebf-cp312-cp312-linux_x86_64.whl
```
This will uninstall your current torch wheels and reinstall the correct ones for ROCm on WSL. Make sure to also run step 4 from the instructions after this as well,
```
location=$(pip show torch | grep Location | awk -F ": " '{print $2}')
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
```
Once this is done, give the `torch.cuda.is_available` and `torch.cuda.device_count` commands a try.



---

### 评论 #4 — ImWarcy (2025-10-02T15:03:44Z)

the last command
`pip3 install torch-2.4.0+rocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl torchvision-0.19.0+rocm6.3.4.gitfab84886-cp312-cp312-linux_x86_64.whl torchaudio-2.4.0+rocm6.3.4.git69d40773-cp312-cp312-linux_x86_64.whl pytorch_triton_rocm-3.0.0+rocm6.3.4.git75cc27c2-cp312-cp312-linux_x86_64.whl
`
says
`
ERROR: torch-2.4.0+rocm6.3.4.git7cecbf6d-cp312-cp312-linux_x86_64.whl is not a supported wheel on this platform.`

---

### 评论 #5 — harkgill-amd (2025-10-02T15:22:03Z)

Are you on Ubuntu 24.04 or 22.04 through WSL? I assumed it was 24.04 based on the amdgpu-install command you ran but the `is not a supported wheel on this platform` error points to a python mismatch between the wheels and your environment. A virtual environment setup with any python version other than 3.12 would also cause this error.

---

### 评论 #6 — ImWarcy (2025-10-02T15:25:16Z)

im gonna check tomorrow i can't at the moment

---

### 评论 #7 — harkgill-amd (2025-10-02T15:39:11Z)

Sure, I also updated the commands in my previous message to highlight the 6.4.2 docs which match your ROCm installation https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-pytorch.html#install-pytorch-via-pip.

Same process still applies, run the first block then the second and give the commands a try.

---

### 评论 #8 — ImWarcy (2025-10-03T13:55:22Z)

Hey, i checked and i'm on Ubuntu 24.04.3 LTS on WSL2. Im going to do the process again and see if now works.

---

### 评论 #9 — ImWarcy (2025-10-03T14:00:21Z)

Ok i tried again and the last command :
`pip3 install torch-2.6.0+rocm6.4.2.git76481f7c-cp312-cp312-linux_x86_64.whl torchvision-0.21.0+rocm6.4.2.git4040d51f-cp312-cp312-linux_x86_64.whl torchaudio-2.6.0+rocm6.4.2.gitd8831425-cp312-cp312-linux_x86_64.whl pytorch_triton_rocm-3.2.0+rocm6.4.2.git7e948ebf-cp312-cp312-linux_x86_64.whl`
gives the same error:
`ERROR: torch-2.6.0+rocm6.4.2.git76481f7c-cp312-cp312-linux_x86_64.whl is not a supported wheel on this platform.`

---

### 评论 #10 — harkgill-amd (2025-10-03T14:24:09Z)

Could you share the `out.txt` file generated by running command `python3 -m pip debug --verbose -> out.txt`? Also, try running `sudo apt install python3-pip -y` and `pip3 install --upgrade pip wheel` prior to pip installing the 6.4.2 wheels.

---

### 评论 #11 — ImWarcy (2025-10-03T16:29:26Z)

Here is the output of the commands `sudo apt install python3-pip -y` and `pip3 install --upgrade pip wheel`

```
warcy@WARCYPC:~$ sudo apt install python3-pip -y
[sudo] password for warcy:
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
python3-pip is already the newest version (24.0+dfsg-1ubuntu1.3).
python3-pip set to manually installed.
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
warcy@WARCYPC:~$ pip3 install --upgrade pip wheel
Requirement already satisfied: pip in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (25.2)
Requirement already satisfied: wheel in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (0.45.1)
```



Here are the contents of `out.txt`

```
pip version: pip 25.2 from /home/warcy/TTS-WebUI/installer_files/env/lib/python3.10/site-packages/pip (python 3.10)
sys.version: 3.10.11 | packaged by conda-forge | (main, May 10 2023, 18:58:44) [GCC 11.3.0]
sys.executable: /home/warcy/TTS-WebUI/installer_files/env/bin/python3
sys.getdefaultencoding: utf-8
sys.getfilesystemencoding: utf-8
locale.getpreferredencoding: UTF-8
sys.platform: linux
sys.implementation:
  name: cpython
'cert' config value: global
REQUESTS_CA_BUNDLE: None
CURL_CA_BUNDLE: None
pip._vendor.certifi.where(): /home/warcy/TTS-WebUI/installer_files/env/lib/python3.10/site-packages/pip/_vendor/certifi/cacert.pem
pip._vendor.DEBUNDLED: False
vendored library versions:
  CacheControl==0.14.3
  distlib==0.4.0
  distro==1.9.0
  msgpack==1.1.1
  packaging==25.0
  platformdirs==4.3.8
  pyproject-hooks==1.2.0
  requests==2.32.4
  certifi==2025.07.14
  idna==3.10
  urllib3==1.26.20
  rich==14.1.0 (Unable to locate actual module version, using vendor.txt specified version)
  pygments==2.19.2
  resolvelib==1.2.0
  setuptools==70.3.0 (Unable to locate actual module version, using vendor.txt specified version)
  tomli==2.2.1
  tomli-w==1.2.0
  truststore==0.10.1
  dependency-groups==1.3.1 (Unable to locate actual module version, using vendor.txt specified version)
Compatible tags: 910
  cp310-cp310-manylinux_2_39_x86_64
  cp310-cp310-manylinux_2_38_x86_64
  cp310-cp310-manylinux_2_37_x86_64
  cp310-cp310-manylinux_2_36_x86_64
  cp310-cp310-manylinux_2_35_x86_64
  cp310-cp310-manylinux_2_34_x86_64
  cp310-cp310-manylinux_2_33_x86_64
  cp310-cp310-manylinux_2_32_x86_64
  cp310-cp310-manylinux_2_31_x86_64
  cp310-cp310-manylinux_2_30_x86_64
  cp310-cp310-manylinux_2_29_x86_64
  cp310-cp310-manylinux_2_28_x86_64
  cp310-cp310-manylinux_2_27_x86_64
  cp310-cp310-manylinux_2_26_x86_64
  cp310-cp310-manylinux_2_25_x86_64
  cp310-cp310-manylinux_2_24_x86_64
  cp310-cp310-manylinux_2_23_x86_64
  cp310-cp310-manylinux_2_22_x86_64
  cp310-cp310-manylinux_2_21_x86_64
  cp310-cp310-manylinux_2_20_x86_64
  cp310-cp310-manylinux_2_19_x86_64
  cp310-cp310-manylinux_2_18_x86_64
  cp310-cp310-manylinux_2_17_x86_64
  cp310-cp310-manylinux2014_x86_64
  cp310-cp310-manylinux_2_16_x86_64
  cp310-cp310-manylinux_2_15_x86_64
  cp310-cp310-manylinux_2_14_x86_64
  cp310-cp310-manylinux_2_13_x86_64
  cp310-cp310-manylinux_2_12_x86_64
  cp310-cp310-manylinux2010_x86_64
  cp310-cp310-manylinux_2_11_x86_64
  cp310-cp310-manylinux_2_10_x86_64
  cp310-cp310-manylinux_2_9_x86_64
  cp310-cp310-manylinux_2_8_x86_64
  cp310-cp310-manylinux_2_7_x86_64
  cp310-cp310-manylinux_2_6_x86_64
  cp310-cp310-manylinux_2_5_x86_64
  cp310-cp310-manylinux1_x86_64
  cp310-cp310-linux_x86_64
  cp310-abi3-manylinux_2_39_x86_64
  cp310-abi3-manylinux_2_38_x86_64
  cp310-abi3-manylinux_2_37_x86_64
  cp310-abi3-manylinux_2_36_x86_64
  cp310-abi3-manylinux_2_35_x86_64
  cp310-abi3-manylinux_2_34_x86_64
  cp310-abi3-manylinux_2_33_x86_64
  cp310-abi3-manylinux_2_32_x86_64
  cp310-abi3-manylinux_2_31_x86_64
  cp310-abi3-manylinux_2_30_x86_64
  cp310-abi3-manylinux_2_29_x86_64
  cp310-abi3-manylinux_2_28_x86_64
  cp310-abi3-manylinux_2_27_x86_64
  cp310-abi3-manylinux_2_26_x86_64
  cp310-abi3-manylinux_2_25_x86_64
  cp310-abi3-manylinux_2_24_x86_64
  cp310-abi3-manylinux_2_23_x86_64
  cp310-abi3-manylinux_2_22_x86_64
  cp310-abi3-manylinux_2_21_x86_64
  cp310-abi3-manylinux_2_20_x86_64
  cp310-abi3-manylinux_2_19_x86_64
  cp310-abi3-manylinux_2_18_x86_64
  cp310-abi3-manylinux_2_17_x86_64
  cp310-abi3-manylinux2014_x86_64
  cp310-abi3-manylinux_2_16_x86_64
  cp310-abi3-manylinux_2_15_x86_64
  cp310-abi3-manylinux_2_14_x86_64
  cp310-abi3-manylinux_2_13_x86_64
  cp310-abi3-manylinux_2_12_x86_64
  cp310-abi3-manylinux2010_x86_64
  cp310-abi3-manylinux_2_11_x86_64
  cp310-abi3-manylinux_2_10_x86_64
  cp310-abi3-manylinux_2_9_x86_64
  cp310-abi3-manylinux_2_8_x86_64
  cp310-abi3-manylinux_2_7_x86_64
  cp310-abi3-manylinux_2_6_x86_64
  cp310-abi3-manylinux_2_5_x86_64
  cp310-abi3-manylinux1_x86_64
  cp310-abi3-linux_x86_64
  cp310-none-manylinux_2_39_x86_64
  cp310-none-manylinux_2_38_x86_64
  cp310-none-manylinux_2_37_x86_64
  cp310-none-manylinux_2_36_x86_64
  cp310-none-manylinux_2_35_x86_64
  cp310-none-manylinux_2_34_x86_64
  cp310-none-manylinux_2_33_x86_64
  cp310-none-manylinux_2_32_x86_64
  cp310-none-manylinux_2_31_x86_64
  cp310-none-manylinux_2_30_x86_64
  cp310-none-manylinux_2_29_x86_64
  cp310-none-manylinux_2_28_x86_64
  cp310-none-manylinux_2_27_x86_64
  cp310-none-manylinux_2_26_x86_64
  cp310-none-manylinux_2_25_x86_64
  cp310-none-manylinux_2_24_x86_64
  cp310-none-manylinux_2_23_x86_64
  cp310-none-manylinux_2_22_x86_64
  cp310-none-manylinux_2_21_x86_64
  cp310-none-manylinux_2_20_x86_64
  cp310-none-manylinux_2_19_x86_64
  cp310-none-manylinux_2_18_x86_64
  cp310-none-manylinux_2_17_x86_64
  cp310-none-manylinux2014_x86_64
  cp310-none-manylinux_2_16_x86_64
  cp310-none-manylinux_2_15_x86_64
  cp310-none-manylinux_2_14_x86_64
  cp310-none-manylinux_2_13_x86_64
  cp310-none-manylinux_2_12_x86_64
  cp310-none-manylinux2010_x86_64
  cp310-none-manylinux_2_11_x86_64
  cp310-none-manylinux_2_10_x86_64
  cp310-none-manylinux_2_9_x86_64
  cp310-none-manylinux_2_8_x86_64
  cp310-none-manylinux_2_7_x86_64
  cp310-none-manylinux_2_6_x86_64
  cp310-none-manylinux_2_5_x86_64
  cp310-none-manylinux1_x86_64
  cp310-none-linux_x86_64
  cp39-abi3-manylinux_2_39_x86_64
  cp39-abi3-manylinux_2_38_x86_64
  cp39-abi3-manylinux_2_37_x86_64
  cp39-abi3-manylinux_2_36_x86_64
  cp39-abi3-manylinux_2_35_x86_64
  cp39-abi3-manylinux_2_34_x86_64
  cp39-abi3-manylinux_2_33_x86_64
  cp39-abi3-manylinux_2_32_x86_64
  cp39-abi3-manylinux_2_31_x86_64
  cp39-abi3-manylinux_2_30_x86_64
  cp39-abi3-manylinux_2_29_x86_64
  cp39-abi3-manylinux_2_28_x86_64
  cp39-abi3-manylinux_2_27_x86_64
  cp39-abi3-manylinux_2_26_x86_64
  cp39-abi3-manylinux_2_25_x86_64
  cp39-abi3-manylinux_2_24_x86_64
  cp39-abi3-manylinux_2_23_x86_64
  cp39-abi3-manylinux_2_22_x86_64
  cp39-abi3-manylinux_2_21_x86_64
  cp39-abi3-manylinux_2_20_x86_64
  cp39-abi3-manylinux_2_19_x86_64
  cp39-abi3-manylinux_2_18_x86_64
  cp39-abi3-manylinux_2_17_x86_64
  cp39-abi3-manylinux2014_x86_64
  cp39-abi3-manylinux_2_16_x86_64
  cp39-abi3-manylinux_2_15_x86_64
  cp39-abi3-manylinux_2_14_x86_64
  cp39-abi3-manylinux_2_13_x86_64
  cp39-abi3-manylinux_2_12_x86_64
  cp39-abi3-manylinux2010_x86_64
  cp39-abi3-manylinux_2_11_x86_64
  cp39-abi3-manylinux_2_10_x86_64
  cp39-abi3-manylinux_2_9_x86_64
  cp39-abi3-manylinux_2_8_x86_64
  cp39-abi3-manylinux_2_7_x86_64
  cp39-abi3-manylinux_2_6_x86_64
  cp39-abi3-manylinux_2_5_x86_64
  cp39-abi3-manylinux1_x86_64
  cp39-abi3-linux_x86_64
  cp38-abi3-manylinux_2_39_x86_64
  cp38-abi3-manylinux_2_38_x86_64
  cp38-abi3-manylinux_2_37_x86_64
  cp38-abi3-manylinux_2_36_x86_64
  cp38-abi3-manylinux_2_35_x86_64
  cp38-abi3-manylinux_2_34_x86_64
  cp38-abi3-manylinux_2_33_x86_64
  cp38-abi3-manylinux_2_32_x86_64
  cp38-abi3-manylinux_2_31_x86_64
  cp38-abi3-manylinux_2_30_x86_64
  cp38-abi3-manylinux_2_29_x86_64
  cp38-abi3-manylinux_2_28_x86_64
  cp38-abi3-manylinux_2_27_x86_64
  cp38-abi3-manylinux_2_26_x86_64
  cp38-abi3-manylinux_2_25_x86_64
  cp38-abi3-manylinux_2_24_x86_64
  cp38-abi3-manylinux_2_23_x86_64
  cp38-abi3-manylinux_2_22_x86_64
  cp38-abi3-manylinux_2_21_x86_64
  cp38-abi3-manylinux_2_20_x86_64
  cp38-abi3-manylinux_2_19_x86_64
  cp38-abi3-manylinux_2_18_x86_64
  cp38-abi3-manylinux_2_17_x86_64
  cp38-abi3-manylinux2014_x86_64
  cp38-abi3-manylinux_2_16_x86_64
  cp38-abi3-manylinux_2_15_x86_64
  cp38-abi3-manylinux_2_14_x86_64
  cp38-abi3-manylinux_2_13_x86_64
  cp38-abi3-manylinux_2_12_x86_64
  cp38-abi3-manylinux2010_x86_64
  cp38-abi3-manylinux_2_11_x86_64
  cp38-abi3-manylinux_2_10_x86_64
  cp38-abi3-manylinux_2_9_x86_64
  cp38-abi3-manylinux_2_8_x86_64
  cp38-abi3-manylinux_2_7_x86_64
  cp38-abi3-manylinux_2_6_x86_64
  cp38-abi3-manylinux_2_5_x86_64
  cp38-abi3-manylinux1_x86_64
  cp38-abi3-linux_x86_64
  cp37-abi3-manylinux_2_39_x86_64
  cp37-abi3-manylinux_2_38_x86_64
  cp37-abi3-manylinux_2_37_x86_64
  cp37-abi3-manylinux_2_36_x86_64
  cp37-abi3-manylinux_2_35_x86_64
  cp37-abi3-manylinux_2_34_x86_64
  cp37-abi3-manylinux_2_33_x86_64
  cp37-abi3-manylinux_2_32_x86_64
  cp37-abi3-manylinux_2_31_x86_64
  cp37-abi3-manylinux_2_30_x86_64
  cp37-abi3-manylinux_2_29_x86_64
  cp37-abi3-manylinux_2_28_x86_64
  cp37-abi3-manylinux_2_27_x86_64
  cp37-abi3-manylinux_2_26_x86_64
  cp37-abi3-manylinux_2_25_x86_64
  cp37-abi3-manylinux_2_24_x86_64
  cp37-abi3-manylinux_2_23_x86_64
  cp37-abi3-manylinux_2_22_x86_64
  cp37-abi3-manylinux_2_21_x86_64
  cp37-abi3-manylinux_2_20_x86_64
  cp37-abi3-manylinux_2_19_x86_64
  cp37-abi3-manylinux_2_18_x86_64
  cp37-abi3-manylinux_2_17_x86_64
  cp37-abi3-manylinux2014_x86_64
  cp37-abi3-manylinux_2_16_x86_64
  cp37-abi3-manylinux_2_15_x86_64
  cp37-abi3-manylinux_2_14_x86_64
  cp37-abi3-manylinux_2_13_x86_64
  cp37-abi3-manylinux_2_12_x86_64
  cp37-abi3-manylinux2010_x86_64
  cp37-abi3-manylinux_2_11_x86_64
  cp37-abi3-manylinux_2_10_x86_64
  cp37-abi3-manylinux_2_9_x86_64
  cp37-abi3-manylinux_2_8_x86_64
  cp37-abi3-manylinux_2_7_x86_64
  cp37-abi3-manylinux_2_6_x86_64
  cp37-abi3-manylinux_2_5_x86_64
  cp37-abi3-manylinux1_x86_64
  cp37-abi3-linux_x86_64
  cp36-abi3-manylinux_2_39_x86_64
  cp36-abi3-manylinux_2_38_x86_64
  cp36-abi3-manylinux_2_37_x86_64
  cp36-abi3-manylinux_2_36_x86_64
  cp36-abi3-manylinux_2_35_x86_64
  cp36-abi3-manylinux_2_34_x86_64
  cp36-abi3-manylinux_2_33_x86_64
  cp36-abi3-manylinux_2_32_x86_64
  cp36-abi3-manylinux_2_31_x86_64
  cp36-abi3-manylinux_2_30_x86_64
  cp36-abi3-manylinux_2_29_x86_64
  cp36-abi3-manylinux_2_28_x86_64
  cp36-abi3-manylinux_2_27_x86_64
  cp36-abi3-manylinux_2_26_x86_64
  cp36-abi3-manylinux_2_25_x86_64
  cp36-abi3-manylinux_2_24_x86_64
  cp36-abi3-manylinux_2_23_x86_64
  cp36-abi3-manylinux_2_22_x86_64
  cp36-abi3-manylinux_2_21_x86_64
  cp36-abi3-manylinux_2_20_x86_64
  cp36-abi3-manylinux_2_19_x86_64
  cp36-abi3-manylinux_2_18_x86_64
  cp36-abi3-manylinux_2_17_x86_64
  cp36-abi3-manylinux2014_x86_64
  cp36-abi3-manylinux_2_16_x86_64
  cp36-abi3-manylinux_2_15_x86_64
  cp36-abi3-manylinux_2_14_x86_64
  cp36-abi3-manylinux_2_13_x86_64
  cp36-abi3-manylinux_2_12_x86_64
  cp36-abi3-manylinux2010_x86_64
  cp36-abi3-manylinux_2_11_x86_64
  cp36-abi3-manylinux_2_10_x86_64
  cp36-abi3-manylinux_2_9_x86_64
  cp36-abi3-manylinux_2_8_x86_64
  cp36-abi3-manylinux_2_7_x86_64
  cp36-abi3-manylinux_2_6_x86_64
  cp36-abi3-manylinux_2_5_x86_64
  cp36-abi3-manylinux1_x86_64
  cp36-abi3-linux_x86_64
  cp35-abi3-manylinux_2_39_x86_64
  cp35-abi3-manylinux_2_38_x86_64
  cp35-abi3-manylinux_2_37_x86_64
  cp35-abi3-manylinux_2_36_x86_64
  cp35-abi3-manylinux_2_35_x86_64
  cp35-abi3-manylinux_2_34_x86_64
  cp35-abi3-manylinux_2_33_x86_64
  cp35-abi3-manylinux_2_32_x86_64
  cp35-abi3-manylinux_2_31_x86_64
  cp35-abi3-manylinux_2_30_x86_64
  cp35-abi3-manylinux_2_29_x86_64
  cp35-abi3-manylinux_2_28_x86_64
  cp35-abi3-manylinux_2_27_x86_64
  cp35-abi3-manylinux_2_26_x86_64
  cp35-abi3-manylinux_2_25_x86_64
  cp35-abi3-manylinux_2_24_x86_64
  cp35-abi3-manylinux_2_23_x86_64
  cp35-abi3-manylinux_2_22_x86_64
  cp35-abi3-manylinux_2_21_x86_64
  cp35-abi3-manylinux_2_20_x86_64
  cp35-abi3-manylinux_2_19_x86_64
  cp35-abi3-manylinux_2_18_x86_64
  cp35-abi3-manylinux_2_17_x86_64
  cp35-abi3-manylinux2014_x86_64
  cp35-abi3-manylinux_2_16_x86_64
  cp35-abi3-manylinux_2_15_x86_64
  cp35-abi3-manylinux_2_14_x86_64
  cp35-abi3-manylinux_2_13_x86_64
  cp35-abi3-manylinux_2_12_x86_64
  cp35-abi3-manylinux2010_x86_64
  cp35-abi3-manylinux_2_11_x86_64
  cp35-abi3-manylinux_2_10_x86_64
  cp35-abi3-manylinux_2_9_x86_64
  cp35-abi3-manylinux_2_8_x86_64
  cp35-abi3-manylinux_2_7_x86_64
  cp35-abi3-manylinux_2_6_x86_64
  cp35-abi3-manylinux_2_5_x86_64
  cp35-abi3-manylinux1_x86_64
  cp35-abi3-linux_x86_64
  cp34-abi3-manylinux_2_39_x86_64
  cp34-abi3-manylinux_2_38_x86_64
  cp34-abi3-manylinux_2_37_x86_64
  cp34-abi3-manylinux_2_36_x86_64
  cp34-abi3-manylinux_2_35_x86_64
  cp34-abi3-manylinux_2_34_x86_64
  cp34-abi3-manylinux_2_33_x86_64
  cp34-abi3-manylinux_2_32_x86_64
  cp34-abi3-manylinux_2_31_x86_64
  cp34-abi3-manylinux_2_30_x86_64
  cp34-abi3-manylinux_2_29_x86_64
  cp34-abi3-manylinux_2_28_x86_64
  cp34-abi3-manylinux_2_27_x86_64
  cp34-abi3-manylinux_2_26_x86_64
  cp34-abi3-manylinux_2_25_x86_64
  cp34-abi3-manylinux_2_24_x86_64
  cp34-abi3-manylinux_2_23_x86_64
  cp34-abi3-manylinux_2_22_x86_64
  cp34-abi3-manylinux_2_21_x86_64
  cp34-abi3-manylinux_2_20_x86_64
  cp34-abi3-manylinux_2_19_x86_64
  cp34-abi3-manylinux_2_18_x86_64
  cp34-abi3-manylinux_2_17_x86_64
  cp34-abi3-manylinux2014_x86_64
  cp34-abi3-manylinux_2_16_x86_64
  cp34-abi3-manylinux_2_15_x86_64
  cp34-abi3-manylinux_2_14_x86_64
  cp34-abi3-manylinux_2_13_x86_64
  cp34-abi3-manylinux_2_12_x86_64
  cp34-abi3-manylinux2010_x86_64
  cp34-abi3-manylinux_2_11_x86_64
  cp34-abi3-manylinux_2_10_x86_64
  cp34-abi3-manylinux_2_9_x86_64
  cp34-abi3-manylinux_2_8_x86_64
  cp34-abi3-manylinux_2_7_x86_64
  cp34-abi3-manylinux_2_6_x86_64
  cp34-abi3-manylinux_2_5_x86_64
  cp34-abi3-manylinux1_x86_64
  cp34-abi3-linux_x86_64
  cp33-abi3-manylinux_2_39_x86_64
  cp33-abi3-manylinux_2_38_x86_64
  cp33-abi3-manylinux_2_37_x86_64
  cp33-abi3-manylinux_2_36_x86_64
  cp33-abi3-manylinux_2_35_x86_64
  cp33-abi3-manylinux_2_34_x86_64
  cp33-abi3-manylinux_2_33_x86_64
  cp33-abi3-manylinux_2_32_x86_64
  cp33-abi3-manylinux_2_31_x86_64
  cp33-abi3-manylinux_2_30_x86_64
  cp33-abi3-manylinux_2_29_x86_64
  cp33-abi3-manylinux_2_28_x86_64
  cp33-abi3-manylinux_2_27_x86_64
  cp33-abi3-manylinux_2_26_x86_64
  cp33-abi3-manylinux_2_25_x86_64
  cp33-abi3-manylinux_2_24_x86_64
  cp33-abi3-manylinux_2_23_x86_64
  cp33-abi3-manylinux_2_22_x86_64
  cp33-abi3-manylinux_2_21_x86_64
  cp33-abi3-manylinux_2_20_x86_64
  cp33-abi3-manylinux_2_19_x86_64
  cp33-abi3-manylinux_2_18_x86_64
  cp33-abi3-manylinux_2_17_x86_64
  cp33-abi3-manylinux2014_x86_64
  cp33-abi3-manylinux_2_16_x86_64
  cp33-abi3-manylinux_2_15_x86_64
  cp33-abi3-manylinux_2_14_x86_64
  cp33-abi3-manylinux_2_13_x86_64
  cp33-abi3-manylinux_2_12_x86_64
  cp33-abi3-manylinux2010_x86_64
  cp33-abi3-manylinux_2_11_x86_64
  cp33-abi3-manylinux_2_10_x86_64
  cp33-abi3-manylinux_2_9_x86_64
  cp33-abi3-manylinux_2_8_x86_64
  cp33-abi3-manylinux_2_7_x86_64
  cp33-abi3-manylinux_2_6_x86_64
  cp33-abi3-manylinux_2_5_x86_64
  cp33-abi3-manylinux1_x86_64
  cp33-abi3-linux_x86_64
  cp32-abi3-manylinux_2_39_x86_64
  cp32-abi3-manylinux_2_38_x86_64
  cp32-abi3-manylinux_2_37_x86_64
  cp32-abi3-manylinux_2_36_x86_64
  cp32-abi3-manylinux_2_35_x86_64
  cp32-abi3-manylinux_2_34_x86_64
  cp32-abi3-manylinux_2_33_x86_64
  cp32-abi3-manylinux_2_32_x86_64
  cp32-abi3-manylinux_2_31_x86_64
  cp32-abi3-manylinux_2_30_x86_64
  cp32-abi3-manylinux_2_29_x86_64
  cp32-abi3-manylinux_2_28_x86_64
  cp32-abi3-manylinux_2_27_x86_64
  cp32-abi3-manylinux_2_26_x86_64
  cp32-abi3-manylinux_2_25_x86_64
  cp32-abi3-manylinux_2_24_x86_64
  cp32-abi3-manylinux_2_23_x86_64
  cp32-abi3-manylinux_2_22_x86_64
  cp32-abi3-manylinux_2_21_x86_64
  cp32-abi3-manylinux_2_20_x86_64
  cp32-abi3-manylinux_2_19_x86_64
  cp32-abi3-manylinux_2_18_x86_64
  cp32-abi3-manylinux_2_17_x86_64
  cp32-abi3-manylinux2014_x86_64
  cp32-abi3-manylinux_2_16_x86_64
  cp32-abi3-manylinux_2_15_x86_64
  cp32-abi3-manylinux_2_14_x86_64
  cp32-abi3-manylinux_2_13_x86_64
  cp32-abi3-manylinux_2_12_x86_64
  cp32-abi3-manylinux2010_x86_64
  cp32-abi3-manylinux_2_11_x86_64
  cp32-abi3-manylinux_2_10_x86_64
  cp32-abi3-manylinux_2_9_x86_64
  cp32-abi3-manylinux_2_8_x86_64
  cp32-abi3-manylinux_2_7_x86_64
  cp32-abi3-manylinux_2_6_x86_64
  cp32-abi3-manylinux_2_5_x86_64
  cp32-abi3-manylinux1_x86_64
  cp32-abi3-linux_x86_64
  py310-none-manylinux_2_39_x86_64
  py310-none-manylinux_2_38_x86_64
  py310-none-manylinux_2_37_x86_64
  py310-none-manylinux_2_36_x86_64
  py310-none-manylinux_2_35_x86_64
  py310-none-manylinux_2_34_x86_64
  py310-none-manylinux_2_33_x86_64
  py310-none-manylinux_2_32_x86_64
  py310-none-manylinux_2_31_x86_64
  py310-none-manylinux_2_30_x86_64
  py310-none-manylinux_2_29_x86_64
  py310-none-manylinux_2_28_x86_64
  py310-none-manylinux_2_27_x86_64
  py310-none-manylinux_2_26_x86_64
  py310-none-manylinux_2_25_x86_64
  py310-none-manylinux_2_24_x86_64
  py310-none-manylinux_2_23_x86_64
  py310-none-manylinux_2_22_x86_64
  py310-none-manylinux_2_21_x86_64
  py310-none-manylinux_2_20_x86_64
  py310-none-manylinux_2_19_x86_64
  py310-none-manylinux_2_18_x86_64
  py310-none-manylinux_2_17_x86_64
  py310-none-manylinux2014_x86_64
  py310-none-manylinux_2_16_x86_64
  py310-none-manylinux_2_15_x86_64
  py310-none-manylinux_2_14_x86_64
  py310-none-manylinux_2_13_x86_64
  py310-none-manylinux_2_12_x86_64
  py310-none-manylinux2010_x86_64
  py310-none-manylinux_2_11_x86_64
  py310-none-manylinux_2_10_x86_64
  py310-none-manylinux_2_9_x86_64
  py310-none-manylinux_2_8_x86_64
  py310-none-manylinux_2_7_x86_64
  py310-none-manylinux_2_6_x86_64
  py310-none-manylinux_2_5_x86_64
  py310-none-manylinux1_x86_64
  py310-none-linux_x86_64
  py3-none-manylinux_2_39_x86_64
  py3-none-manylinux_2_38_x86_64
  py3-none-manylinux_2_37_x86_64
  py3-none-manylinux_2_36_x86_64
  py3-none-manylinux_2_35_x86_64
  py3-none-manylinux_2_34_x86_64
  py3-none-manylinux_2_33_x86_64
  py3-none-manylinux_2_32_x86_64
  py3-none-manylinux_2_31_x86_64
  py3-none-manylinux_2_30_x86_64
  py3-none-manylinux_2_29_x86_64
  py3-none-manylinux_2_28_x86_64
  py3-none-manylinux_2_27_x86_64
  py3-none-manylinux_2_26_x86_64
  py3-none-manylinux_2_25_x86_64
  py3-none-manylinux_2_24_x86_64
  py3-none-manylinux_2_23_x86_64
  py3-none-manylinux_2_22_x86_64
  py3-none-manylinux_2_21_x86_64
  py3-none-manylinux_2_20_x86_64
  py3-none-manylinux_2_19_x86_64
  py3-none-manylinux_2_18_x86_64
  py3-none-manylinux_2_17_x86_64
  py3-none-manylinux2014_x86_64
  py3-none-manylinux_2_16_x86_64
  py3-none-manylinux_2_15_x86_64
  py3-none-manylinux_2_14_x86_64
  py3-none-manylinux_2_13_x86_64
  py3-none-manylinux_2_12_x86_64
  py3-none-manylinux2010_x86_64
  py3-none-manylinux_2_11_x86_64
  py3-none-manylinux_2_10_x86_64
  py3-none-manylinux_2_9_x86_64
  py3-none-manylinux_2_8_x86_64
  py3-none-manylinux_2_7_x86_64
  py3-none-manylinux_2_6_x86_64
  py3-none-manylinux_2_5_x86_64
  py3-none-manylinux1_x86_64
  py3-none-linux_x86_64
  py39-none-manylinux_2_39_x86_64
  py39-none-manylinux_2_38_x86_64
  py39-none-manylinux_2_37_x86_64
  py39-none-manylinux_2_36_x86_64
  py39-none-manylinux_2_35_x86_64
  py39-none-manylinux_2_34_x86_64
  py39-none-manylinux_2_33_x86_64
  py39-none-manylinux_2_32_x86_64
  py39-none-manylinux_2_31_x86_64
  py39-none-manylinux_2_30_x86_64
  py39-none-manylinux_2_29_x86_64
  py39-none-manylinux_2_28_x86_64
  py39-none-manylinux_2_27_x86_64
  py39-none-manylinux_2_26_x86_64
  py39-none-manylinux_2_25_x86_64
  py39-none-manylinux_2_24_x86_64
  py39-none-manylinux_2_23_x86_64
  py39-none-manylinux_2_22_x86_64
  py39-none-manylinux_2_21_x86_64
  py39-none-manylinux_2_20_x86_64
  py39-none-manylinux_2_19_x86_64
  py39-none-manylinux_2_18_x86_64
  py39-none-manylinux_2_17_x86_64
  py39-none-manylinux2014_x86_64
  py39-none-manylinux_2_16_x86_64
  py39-none-manylinux_2_15_x86_64
  py39-none-manylinux_2_14_x86_64
  py39-none-manylinux_2_13_x86_64
  py39-none-manylinux_2_12_x86_64
  py39-none-manylinux2010_x86_64
  py39-none-manylinux_2_11_x86_64
  py39-none-manylinux_2_10_x86_64
  py39-none-manylinux_2_9_x86_64
  py39-none-manylinux_2_8_x86_64
  py39-none-manylinux_2_7_x86_64
  py39-none-manylinux_2_6_x86_64
  py39-none-manylinux_2_5_x86_64
  py39-none-manylinux1_x86_64
  py39-none-linux_x86_64
  py38-none-manylinux_2_39_x86_64
  py38-none-manylinux_2_38_x86_64
  py38-none-manylinux_2_37_x86_64
  py38-none-manylinux_2_36_x86_64
  py38-none-manylinux_2_35_x86_64
  py38-none-manylinux_2_34_x86_64
  py38-none-manylinux_2_33_x86_64
  py38-none-manylinux_2_32_x86_64
  py38-none-manylinux_2_31_x86_64
  py38-none-manylinux_2_30_x86_64
  py38-none-manylinux_2_29_x86_64
  py38-none-manylinux_2_28_x86_64
  py38-none-manylinux_2_27_x86_64
  py38-none-manylinux_2_26_x86_64
  py38-none-manylinux_2_25_x86_64
  py38-none-manylinux_2_24_x86_64
  py38-none-manylinux_2_23_x86_64
  py38-none-manylinux_2_22_x86_64
  py38-none-manylinux_2_21_x86_64
  py38-none-manylinux_2_20_x86_64
  py38-none-manylinux_2_19_x86_64
  py38-none-manylinux_2_18_x86_64
  py38-none-manylinux_2_17_x86_64
  py38-none-manylinux2014_x86_64
  py38-none-manylinux_2_16_x86_64
  py38-none-manylinux_2_15_x86_64
  py38-none-manylinux_2_14_x86_64
  py38-none-manylinux_2_13_x86_64
  py38-none-manylinux_2_12_x86_64
  py38-none-manylinux2010_x86_64
  py38-none-manylinux_2_11_x86_64
  py38-none-manylinux_2_10_x86_64
  py38-none-manylinux_2_9_x86_64
  py38-none-manylinux_2_8_x86_64
  py38-none-manylinux_2_7_x86_64
  py38-none-manylinux_2_6_x86_64
  py38-none-manylinux_2_5_x86_64
  py38-none-manylinux1_x86_64
  py38-none-linux_x86_64
  py37-none-manylinux_2_39_x86_64
  py37-none-manylinux_2_38_x86_64
  py37-none-manylinux_2_37_x86_64
  py37-none-manylinux_2_36_x86_64
  py37-none-manylinux_2_35_x86_64
  py37-none-manylinux_2_34_x86_64
  py37-none-manylinux_2_33_x86_64
  py37-none-manylinux_2_32_x86_64
  py37-none-manylinux_2_31_x86_64
  py37-none-manylinux_2_30_x86_64
  py37-none-manylinux_2_29_x86_64
  py37-none-manylinux_2_28_x86_64
  py37-none-manylinux_2_27_x86_64
  py37-none-manylinux_2_26_x86_64
  py37-none-manylinux_2_25_x86_64
  py37-none-manylinux_2_24_x86_64
  py37-none-manylinux_2_23_x86_64
  py37-none-manylinux_2_22_x86_64
  py37-none-manylinux_2_21_x86_64
  py37-none-manylinux_2_20_x86_64
  py37-none-manylinux_2_19_x86_64
  py37-none-manylinux_2_18_x86_64
  py37-none-manylinux_2_17_x86_64
  py37-none-manylinux2014_x86_64
  py37-none-manylinux_2_16_x86_64
  py37-none-manylinux_2_15_x86_64
  py37-none-manylinux_2_14_x86_64
  py37-none-manylinux_2_13_x86_64
  py37-none-manylinux_2_12_x86_64
  py37-none-manylinux2010_x86_64
  py37-none-manylinux_2_11_x86_64
  py37-none-manylinux_2_10_x86_64
  py37-none-manylinux_2_9_x86_64
  py37-none-manylinux_2_8_x86_64
  py37-none-manylinux_2_7_x86_64
  py37-none-manylinux_2_6_x86_64
  py37-none-manylinux_2_5_x86_64
  py37-none-manylinux1_x86_64
  py37-none-linux_x86_64
  py36-none-manylinux_2_39_x86_64
  py36-none-manylinux_2_38_x86_64
  py36-none-manylinux_2_37_x86_64
  py36-none-manylinux_2_36_x86_64
  py36-none-manylinux_2_35_x86_64
  py36-none-manylinux_2_34_x86_64
  py36-none-manylinux_2_33_x86_64
  py36-none-manylinux_2_32_x86_64
  py36-none-manylinux_2_31_x86_64
  py36-none-manylinux_2_30_x86_64
  py36-none-manylinux_2_29_x86_64
  py36-none-manylinux_2_28_x86_64
  py36-none-manylinux_2_27_x86_64
  py36-none-manylinux_2_26_x86_64
  py36-none-manylinux_2_25_x86_64
  py36-none-manylinux_2_24_x86_64
  py36-none-manylinux_2_23_x86_64
  py36-none-manylinux_2_22_x86_64
  py36-none-manylinux_2_21_x86_64
  py36-none-manylinux_2_20_x86_64
  py36-none-manylinux_2_19_x86_64
  py36-none-manylinux_2_18_x86_64
  py36-none-manylinux_2_17_x86_64
  py36-none-manylinux2014_x86_64
  py36-none-manylinux_2_16_x86_64
  py36-none-manylinux_2_15_x86_64
  py36-none-manylinux_2_14_x86_64
  py36-none-manylinux_2_13_x86_64
  py36-none-manylinux_2_12_x86_64
  py36-none-manylinux2010_x86_64
  py36-none-manylinux_2_11_x86_64
  py36-none-manylinux_2_10_x86_64
  py36-none-manylinux_2_9_x86_64
  py36-none-manylinux_2_8_x86_64
  py36-none-manylinux_2_7_x86_64
  py36-none-manylinux_2_6_x86_64
  py36-none-manylinux_2_5_x86_64
  py36-none-manylinux1_x86_64
  py36-none-linux_x86_64
  py35-none-manylinux_2_39_x86_64
  py35-none-manylinux_2_38_x86_64
  py35-none-manylinux_2_37_x86_64
  py35-none-manylinux_2_36_x86_64
  py35-none-manylinux_2_35_x86_64
  py35-none-manylinux_2_34_x86_64
  py35-none-manylinux_2_33_x86_64
  py35-none-manylinux_2_32_x86_64
  py35-none-manylinux_2_31_x86_64
  py35-none-manylinux_2_30_x86_64
  py35-none-manylinux_2_29_x86_64
  py35-none-manylinux_2_28_x86_64
  py35-none-manylinux_2_27_x86_64
  py35-none-manylinux_2_26_x86_64
  py35-none-manylinux_2_25_x86_64
  py35-none-manylinux_2_24_x86_64
  py35-none-manylinux_2_23_x86_64
  py35-none-manylinux_2_22_x86_64
  py35-none-manylinux_2_21_x86_64
  py35-none-manylinux_2_20_x86_64
  py35-none-manylinux_2_19_x86_64
  py35-none-manylinux_2_18_x86_64
  py35-none-manylinux_2_17_x86_64
  py35-none-manylinux2014_x86_64
  py35-none-manylinux_2_16_x86_64
  py35-none-manylinux_2_15_x86_64
  py35-none-manylinux_2_14_x86_64
  py35-none-manylinux_2_13_x86_64
  py35-none-manylinux_2_12_x86_64
  py35-none-manylinux2010_x86_64
  py35-none-manylinux_2_11_x86_64
  py35-none-manylinux_2_10_x86_64
  py35-none-manylinux_2_9_x86_64
  py35-none-manylinux_2_8_x86_64
  py35-none-manylinux_2_7_x86_64
  py35-none-manylinux_2_6_x86_64
  py35-none-manylinux_2_5_x86_64
  py35-none-manylinux1_x86_64
  py35-none-linux_x86_64
  py34-none-manylinux_2_39_x86_64
  py34-none-manylinux_2_38_x86_64
  py34-none-manylinux_2_37_x86_64
  py34-none-manylinux_2_36_x86_64
  py34-none-manylinux_2_35_x86_64
  py34-none-manylinux_2_34_x86_64
  py34-none-manylinux_2_33_x86_64
  py34-none-manylinux_2_32_x86_64
  py34-none-manylinux_2_31_x86_64
  py34-none-manylinux_2_30_x86_64
  py34-none-manylinux_2_29_x86_64
  py34-none-manylinux_2_28_x86_64
  py34-none-manylinux_2_27_x86_64
  py34-none-manylinux_2_26_x86_64
  py34-none-manylinux_2_25_x86_64
  py34-none-manylinux_2_24_x86_64
  py34-none-manylinux_2_23_x86_64
  py34-none-manylinux_2_22_x86_64
  py34-none-manylinux_2_21_x86_64
  py34-none-manylinux_2_20_x86_64
  py34-none-manylinux_2_19_x86_64
  py34-none-manylinux_2_18_x86_64
  py34-none-manylinux_2_17_x86_64
  py34-none-manylinux2014_x86_64
  py34-none-manylinux_2_16_x86_64
  py34-none-manylinux_2_15_x86_64
  py34-none-manylinux_2_14_x86_64
  py34-none-manylinux_2_13_x86_64
  py34-none-manylinux_2_12_x86_64
  py34-none-manylinux2010_x86_64
  py34-none-manylinux_2_11_x86_64
  py34-none-manylinux_2_10_x86_64
  py34-none-manylinux_2_9_x86_64
  py34-none-manylinux_2_8_x86_64
  py34-none-manylinux_2_7_x86_64
  py34-none-manylinux_2_6_x86_64
  py34-none-manylinux_2_5_x86_64
  py34-none-manylinux1_x86_64
  py34-none-linux_x86_64
  py33-none-manylinux_2_39_x86_64
  py33-none-manylinux_2_38_x86_64
  py33-none-manylinux_2_37_x86_64
  py33-none-manylinux_2_36_x86_64
  py33-none-manylinux_2_35_x86_64
  py33-none-manylinux_2_34_x86_64
  py33-none-manylinux_2_33_x86_64
  py33-none-manylinux_2_32_x86_64
  py33-none-manylinux_2_31_x86_64
  py33-none-manylinux_2_30_x86_64
  py33-none-manylinux_2_29_x86_64
  py33-none-manylinux_2_28_x86_64
  py33-none-manylinux_2_27_x86_64
  py33-none-manylinux_2_26_x86_64
  py33-none-manylinux_2_25_x86_64
  py33-none-manylinux_2_24_x86_64
  py33-none-manylinux_2_23_x86_64
  py33-none-manylinux_2_22_x86_64
  py33-none-manylinux_2_21_x86_64
  py33-none-manylinux_2_20_x86_64
  py33-none-manylinux_2_19_x86_64
  py33-none-manylinux_2_18_x86_64
  py33-none-manylinux_2_17_x86_64
  py33-none-manylinux2014_x86_64
  py33-none-manylinux_2_16_x86_64
  py33-none-manylinux_2_15_x86_64
  py33-none-manylinux_2_14_x86_64
  py33-none-manylinux_2_13_x86_64
  py33-none-manylinux_2_12_x86_64
  py33-none-manylinux2010_x86_64
  py33-none-manylinux_2_11_x86_64
  py33-none-manylinux_2_10_x86_64
  py33-none-manylinux_2_9_x86_64
  py33-none-manylinux_2_8_x86_64
  py33-none-manylinux_2_7_x86_64
  py33-none-manylinux_2_6_x86_64
  py33-none-manylinux_2_5_x86_64
  py33-none-manylinux1_x86_64
  py33-none-linux_x86_64
  py32-none-manylinux_2_39_x86_64
  py32-none-manylinux_2_38_x86_64
  py32-none-manylinux_2_37_x86_64
  py32-none-manylinux_2_36_x86_64
  py32-none-manylinux_2_35_x86_64
  py32-none-manylinux_2_34_x86_64
  py32-none-manylinux_2_33_x86_64
  py32-none-manylinux_2_32_x86_64
  py32-none-manylinux_2_31_x86_64
  py32-none-manylinux_2_30_x86_64
  py32-none-manylinux_2_29_x86_64
  py32-none-manylinux_2_28_x86_64
  py32-none-manylinux_2_27_x86_64
  py32-none-manylinux_2_26_x86_64
  py32-none-manylinux_2_25_x86_64
  py32-none-manylinux_2_24_x86_64
  py32-none-manylinux_2_23_x86_64
  py32-none-manylinux_2_22_x86_64
  py32-none-manylinux_2_21_x86_64
  py32-none-manylinux_2_20_x86_64
  py32-none-manylinux_2_19_x86_64
  py32-none-manylinux_2_18_x86_64
  py32-none-manylinux_2_17_x86_64
  py32-none-manylinux2014_x86_64
  py32-none-manylinux_2_16_x86_64
  py32-none-manylinux_2_15_x86_64
  py32-none-manylinux_2_14_x86_64
  py32-none-manylinux_2_13_x86_64
  py32-none-manylinux_2_12_x86_64
  py32-none-manylinux2010_x86_64
  py32-none-manylinux_2_11_x86_64
  py32-none-manylinux_2_10_x86_64
  py32-none-manylinux_2_9_x86_64
  py32-none-manylinux_2_8_x86_64
  py32-none-manylinux_2_7_x86_64
  py32-none-manylinux_2_6_x86_64
  py32-none-manylinux_2_5_x86_64
  py32-none-manylinux1_x86_64
  py32-none-linux_x86_64
  py31-none-manylinux_2_39_x86_64
  py31-none-manylinux_2_38_x86_64
  py31-none-manylinux_2_37_x86_64
  py31-none-manylinux_2_36_x86_64
  py31-none-manylinux_2_35_x86_64
  py31-none-manylinux_2_34_x86_64
  py31-none-manylinux_2_33_x86_64
  py31-none-manylinux_2_32_x86_64
  py31-none-manylinux_2_31_x86_64
  py31-none-manylinux_2_30_x86_64
  py31-none-manylinux_2_29_x86_64
  py31-none-manylinux_2_28_x86_64
  py31-none-manylinux_2_27_x86_64
  py31-none-manylinux_2_26_x86_64
  py31-none-manylinux_2_25_x86_64
  py31-none-manylinux_2_24_x86_64
  py31-none-manylinux_2_23_x86_64
  py31-none-manylinux_2_22_x86_64
  py31-none-manylinux_2_21_x86_64
  py31-none-manylinux_2_20_x86_64
  py31-none-manylinux_2_19_x86_64
  py31-none-manylinux_2_18_x86_64
  py31-none-manylinux_2_17_x86_64
  py31-none-manylinux2014_x86_64
  py31-none-manylinux_2_16_x86_64
  py31-none-manylinux_2_15_x86_64
  py31-none-manylinux_2_14_x86_64
  py31-none-manylinux_2_13_x86_64
  py31-none-manylinux_2_12_x86_64
  py31-none-manylinux2010_x86_64
  py31-none-manylinux_2_11_x86_64
  py31-none-manylinux_2_10_x86_64
  py31-none-manylinux_2_9_x86_64
  py31-none-manylinux_2_8_x86_64
  py31-none-manylinux_2_7_x86_64
  py31-none-manylinux_2_6_x86_64
  py31-none-manylinux_2_5_x86_64
  py31-none-manylinux1_x86_64
  py31-none-linux_x86_64
  py30-none-manylinux_2_39_x86_64
  py30-none-manylinux_2_38_x86_64
  py30-none-manylinux_2_37_x86_64
  py30-none-manylinux_2_36_x86_64
  py30-none-manylinux_2_35_x86_64
  py30-none-manylinux_2_34_x86_64
  py30-none-manylinux_2_33_x86_64
  py30-none-manylinux_2_32_x86_64
  py30-none-manylinux_2_31_x86_64
  py30-none-manylinux_2_30_x86_64
  py30-none-manylinux_2_29_x86_64
  py30-none-manylinux_2_28_x86_64
  py30-none-manylinux_2_27_x86_64
  py30-none-manylinux_2_26_x86_64
  py30-none-manylinux_2_25_x86_64
  py30-none-manylinux_2_24_x86_64
  py30-none-manylinux_2_23_x86_64
  py30-none-manylinux_2_22_x86_64
  py30-none-manylinux_2_21_x86_64
  py30-none-manylinux_2_20_x86_64
  py30-none-manylinux_2_19_x86_64
  py30-none-manylinux_2_18_x86_64
  py30-none-manylinux_2_17_x86_64
  py30-none-manylinux2014_x86_64
  py30-none-manylinux_2_16_x86_64
  py30-none-manylinux_2_15_x86_64
  py30-none-manylinux_2_14_x86_64
  py30-none-manylinux_2_13_x86_64
  py30-none-manylinux_2_12_x86_64
  py30-none-manylinux2010_x86_64
  py30-none-manylinux_2_11_x86_64
  py30-none-manylinux_2_10_x86_64
  py30-none-manylinux_2_9_x86_64
  py30-none-manylinux_2_8_x86_64
  py30-none-manylinux_2_7_x86_64
  py30-none-manylinux_2_6_x86_64
  py30-none-manylinux_2_5_x86_64
  py30-none-manylinux1_x86_64
  py30-none-linux_x86_64
  cp310-none-any
  py310-none-any
  py3-none-any
  py39-none-any
  py38-none-any
  py37-none-any
  py36-none-any
  py35-none-any
  py34-none-any
  py33-none-any
  py32-none-any
  py31-none-any
  py30-none-any
```

---

### 评论 #12 — harkgill-amd (2025-10-03T17:30:14Z)

You're using a conda environment with Python 3.10
```
sys.version: 3.10.11 | packaged by conda-forge
```
The wheels I had shared previously are for Python 3.12, this comes standard with Ubuntu 24.04. Installing the Python 3.10 wheels with the commands below will resolve the mismatch,
```
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/torch-2.6.0%2Brocm6.4.2.git76481f7c-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/torchvision-0.21.0%2Brocm6.4.2.git4040d51f-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/pytorch_triton_rocm-3.2.0%2Brocm6.4.2.git7e948ebf-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.2/torchaudio-2.6.0%2Brocm6.4.2.gitd8831425-cp310-cp310-linux_x86_64.whl
pip3 uninstall torch torchvision pytorch-triton-rocm
pip3 install torch-2.6.0+rocm6.4.2.git76481f7c-cp310-cp310-linux_x86_64.whl torchvision-0.21.0+rocm6.4.2.git4040d51f-cp310-cp310-linux_x86_64.whl torchaudio-2.6.0+rocm6.4.2.gitd8831425-cp310-cp310-linux_x86_64.whl pytorch_triton_rocm-3.2.0+rocm6.4.2.git7e948ebf-cp310-cp310-linux_x86_64.whl
```

---

### 评论 #13 — ImWarcy (2025-10-03T18:13:17Z)

It worked but gives an error at the end 

```
Processing ./torch-2.6.0+rocm6.4.2.git76481f7c-cp310-cp310-linux_x86_64.whl
Processing ./torchvision-0.21.0+rocm6.4.2.git4040d51f-cp310-cp310-linux_x86_64.whl
Processing ./torchaudio-2.6.0+rocm6.4.2.gitd8831425-cp310-cp310-linux_x86_64.whl
Processing ./pytorch_triton_rocm-3.2.0+rocm6.4.2.git7e948ebf-cp310-cp310-linux_x86_64.whl
Requirement already satisfied: filelock in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from torch==2.6.0+rocm6.4.2.git76481f7c) (3.12.4)
Requirement already satisfied: typing-extensions>=4.10.0 in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from torch==2.6.0+rocm6.4.2.git76481f7c) (4.15.0)
Collecting sympy==1.13.1 (from torch==2.6.0+rocm6.4.2.git76481f7c)
  Downloading sympy-1.13.1-py3-none-any.whl.metadata (12 kB)
Requirement already satisfied: networkx in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from torch==2.6.0+rocm6.4.2.git76481f7c) (2.8.8)
Requirement already satisfied: jinja2 in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from torch==2.6.0+rocm6.4.2.git76481f7c) (3.1.4)
Requirement already satisfied: fsspec in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from torch==2.6.0+rocm6.4.2.git76481f7c) (2024.6.1)
Requirement already satisfied: numpy in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from torchvision==0.21.0+rocm6.4.2.git4040d51f) (1.23.5)
Requirement already satisfied: pillow!=8.3.*,>=5.3.0 in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from torchvision==0.21.0+rocm6.4.2.git4040d51f) (10.3.0)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from sympy==1.13.1->torch==2.6.0+rocm6.4.2.git76481f7c) (1.3.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./TTS-WebUI/installer_files/env/lib/python3.10/site-packages (from jinja2->torch==2.6.0+rocm6.4.2.git76481f7c) (2.1.5)
Downloading sympy-1.13.1-py3-none-any.whl (6.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.2/6.2 MB 44.9 MB/s  0:00:00
Installing collected packages: pytorch-triton-rocm, sympy, torch, torchvision, torchaudio
  Attempting uninstall: sympy
    Found existing installation: sympy 1.13.3
    Uninstalling sympy-1.13.3:
      Successfully uninstalled sympy-1.13.3
  Attempting uninstall: torchaudio
    Found existing installation: torchaudio 2.7.0+rocm6.3
    Uninstalling torchaudio-2.7.0+rocm6.3:
      Successfully uninstalled torchaudio-2.7.0+rocm6.3
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
xformers 0.0.30 requires torch==2.7.0, but you have torch 2.6.0+rocm6.4.2.git76481f7c which is incompatible.
Successfully installed pytorch-triton-rocm-3.2.0+rocm6.4.2.git7e948ebf sympy-1.13.1 torch-2.6.0+rocm6.4.2.git76481f7c torchaudio-2.6.0+rocm6.4.2.gitd8831425 torchvision-0.21.0+rocm6.4.2.git4040d51f
```

---

### 评论 #14 — harkgill-amd (2025-10-03T19:42:24Z)

Can you finish up with 
```
location=$(pip show torch | grep Location | awk -F ": " '{print $2}')
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
```
and give the `torch.cuda.is_available` and `torch.cuda.device_count` commands a run? I recreated the steps that you've taken on your side with the TTS-webUI installer and these commands now work correctly in the conda env.

As for the xformers dependency errors, I'm not sure to what extent TTS-webUI requires this. From their requirements.txt, support looks to be experimental. I was able to start up a server with `python server.py --no-react` and successfully generate audio with the Vall-E-X model despite this. 

---

### 评论 #15 — ImWarcy (2025-10-03T19:49:44Z)

It works, `CUDA/ROCm available: True, Device count: 1`
Tomorrow i will check if TTS-webUI works
Thanks for your patience

---
