# No RDNA 3 support? Really?

> **Issue #2312**
> **状态**: closed
> **创建时间**: 2023-07-01T06:29:27Z
> **更新时间**: 2024-05-14T14:44:12Z
> **关闭时间**: 2024-05-14T14:44:11Z
> **作者**: sucaiji
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2312

## 描述

why?

---

## 评论 (6 条)

### 评论 #1 — sucaiji (2023-07-01T06:32:03Z)

When can I used my 7900xt to run stable diffusion on windows?

---

### 评论 #2 — kankan1322 (2023-07-01T14:07:32Z)

stable-diffusion-webui-directml

---

### 评论 #3 — yatagai63 (2023-07-01T23:46:06Z)

I run stable diffusion on linux

mkdir $HOME/AI 
cd $HOME/AI
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
apt update && apt install python3.8-venv
cd stable-diffusion-webui
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip wheel
export HIP_VISIBLE_DEVICES=0
export PYTORCH_ROCM_ARCH="gfx1100"
export CMAKE_PREFIX_PATH=$HOME/AI/stable-diffusion-webui/venv/
pip install -r requirements.txt
pip uninstall torch torchvision
mkdir repositories
cd repositories
git clone https://github.com/pytorch/pytorch
git clone https://github.com/pytorch/vision
cd pytorch
pip install cmake ninja
pip install -r requirements.txt
pip install mkl mkl-include
python3 tools/amd_build/build_amd.py
python3 setup.py install
cd ../vision
python3 setup.py install
cd $HOME/AI/stable-diffusion-webui
python3 launch.py --listen

---

### 评论 #4 — yamfun (2023-07-14T03:10:06Z)

> I run stable diffusion on linux
> 
> mkdir $HOME/AI cd $HOME/AI git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui apt update && apt install python3.8-venv cd stable-diffusion-webui python3 -m venv venv source venv/bin/activate python3 -m pip install --upgrade pip wheel export HIP_VISIBLE_DEVICES=0 export PYTORCH_ROCM_ARCH="gfx1100" export CMAKE_PREFIX_PATH=$HOME/AI/stable-diffusion-webui/venv/ pip install -r requirements.txt pip uninstall torch torchvision mkdir repositories cd repositories git clone https://github.com/pytorch/pytorch git clone https://github.com/pytorch/vision cd pytorch pip install cmake ninja pip install -r requirements.txt pip install mkl mkl-include python3 tools/amd_build/build_amd.py python3 setup.py install cd ../vision python3 setup.py install cd $HOME/AI/stable-diffusion-webui python3 launch.py --listen

Did you managed to make kohya ss Optimizer AdamW8bit bitsandbytes-rocm to work? 

---

### 评论 #5 — johnnynunez (2023-07-27T19:57:15Z)

https://rocm.docs.amd.com/en/latest/release/windows_support.html 

---

### 评论 #6 — ppanchad-amd (2024-05-14T14:44:11Z)

@sucaiji RDNA 3 is supported as of latest ROCm 6.1.1  (https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)

---
