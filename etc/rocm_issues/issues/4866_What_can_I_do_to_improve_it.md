# What can I do to improve it?

> **Issue #4866**
> **状态**: closed
> **创建时间**: 2025-05-31T12:52:04Z
> **更新时间**: 2025-06-08T17:02:16Z
> **关闭时间**: 2025-06-08T17:02:16Z
> **作者**: zheliangzhi
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/4866

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- alexrosen45

## 描述

“RuntimeError: No HIP GPUs are available” for ComfuUI


“Ubuntu-24.04” “AMD Ryzen 7 5700X” “AMD Radeon RX 7900 XT” “ROCm 6.4.1” ....... This is the result that can be obtained after running each test. When I start “ComfyUI”, I still can't load the GPU.
 
I followed the operational steps about 'GPU' and 'ComfyUI' on the website. From 'rocm.docs.amd.com'.

---

## 评论 (2 条)

### 评论 #1 — harkgill-amd (2025-06-02T13:46:23Z)

Hey @zheliangzhi, left a comment on https://github.com/ROCm/ROCm/issues/4851 but am just now noticing you mentioned that the GPU was detected with rocminfo/pytorch. Will try reproducing the ComfyUI specific detection error and get back to you on this. Thanks!

---

### 评论 #2 — alexrosen45 (2025-06-04T15:59:43Z)

Hi @zheliangzhi, we were unable to reproduce your issue on the 7900 XT. One possibility is that you installed ComfyUI requirements after PyTorch with ROCm, which may have overwritten the previous ROCm-PyTorch installation. Please follow the steps below in-order to setup ComfyUI

## Setup ROCm in WSL2

Install rocm by following all the steps [here]( https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html) from Prerequisites to Post-install verification check. In your case this would be installing the latest version of Ubuntu in wsl with `wsl --install`, making sure the correct drivers are installed, then running
```
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.4/ubuntu/noble/amdgpu-install_6.3.60304-1_all.deb
sudo apt install ./amdgpu-install_6.3.60304-1_all.deb
amdgpu-install -y --usecase=wsl,rocm --no-dkms
```
Run `rocminfo` to verify the installation.

## Make a Python virtual environment
```
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
pip install –-upgrade pip
```
The following should work with conda too, but use pip installs instead of conda installs since it matches the commands we used to try to reproduce your issue.

## Clone ComfyUI and install requirements
```
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI && pip install -r requirements.txt
```

## Replace the current PyTorch installation with ROCm PyTorch
Follow the instructions [here]( https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html) to install via pip. In your case this would be:
```
pip3 install –upgrade pip wheel
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/torch-2.6.0%2Brocm6.4.1.git1ded221d-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/torchvision-0.21.0%2Brocm6.4.1.git4040d51f-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/pytorch_triton_rocm-3.2.0%2Brocm6.4.1.git6da9e660-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-6.4.1/torchaudio-2.6.0%2Brocm6.4.1.gitd8831425-cp312-cp312-linux_x86_64.whl
pip3 uninstall torch torchvision pytorch-triton-rocm
pip3 install torch-2.6.0+rocm6.4.1.git1ded221d-cp312-cp312-linux_x86_64.whl torchvision-0.21.0+rocm6.4.1.git4040d51f-cp312-cp312-linux_x86_64.whl torchaudio-2.6.0+rocm6.4.1.gitd8831425-cp312-cp312-linux_x86_64.whl pytorch_triton_rocm-3.2.0+rocm6.4.1.git6da9e660-cp312-cp312-linux_x86_64.whl
```
Running `python3 -c “import torch; print(torch.cuda.is_available())"` should print True if the installation worked correctly. If you get False, run
```
location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
cp /opt/rocm/lib/libhsa-runtime64.so.1 libhsa-runtime64.so
cd ~
```

## Run ComfyUI
ComfyUI should work now; run it with `cd ComfyUI && python3 main.py`.

Please let us know if any of the steps went wrong.


---
