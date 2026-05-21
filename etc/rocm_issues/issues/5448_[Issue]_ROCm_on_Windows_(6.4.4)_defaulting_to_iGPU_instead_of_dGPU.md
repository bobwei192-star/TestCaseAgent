# [Issue]: ROCm on Windows (6.4.4) defaulting to iGPU instead of dGPU

> **Issue #5448**
> **状态**: closed
> **创建时间**: 2025-09-30T07:00:43Z
> **更新时间**: 2025-12-30T15:47:29Z
> **关闭时间**: 2025-12-30T15:47:29Z
> **作者**: ruaruarua111
> **标签**: AMD Radeon RX 7900 XTX, status: triage
> **URL**: https://github.com/ROCm/ROCm/issues/5448

## 标签

- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **status: triage** (颜色: #585dd7)

## 负责人

- darren-amd

## 描述

### Problem Description

(base) PS C:\Users\10649> (Get-WmiObject Win32_OperatingSystem).Version
10.0.26100
(base) PS C:\Users\10649>   (Get-WmiObject win32_Processor).Name
AMD Ryzen 5 9600X 6-Core Processor
(base) PS C:\Users\10649>   (Get-WmiObject win32_VideoController).Name
Parsec Virtual Display Adapter
OrayIddDriver Device
Microsoft Remote Display Adapter
AMD Radeon(TM) Graphics
AMD Radeon RX 7900 XTX

<img width="1641" height="562" alt="Image" src="https://github.com/user-attachments/assets/c1bf02ff-d079-499d-ae0b-0522f8fcf8ee" />

<img width="2081" height="604" alt="Image" src="https://github.com/user-attachments/assets/852b8104-15ad-433c-89bf-2dec79cd331c" />

Cant find my gpu

### Operating System

10.0.26100

### CPU

9600x

### GPU

Rx 7900 xtx

### ROCm Version

6.4.50101-9a6572ae7

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (4 条)

### 评论 #1 — ppanchad-amd (2025-09-30T14:35:20Z)

Hi @ruaruarua111. Internal ticket has been created to investigate this issue. Thanks!

---

### 评论 #2 — ruaruarua111 (2025-09-30T15:47:23Z)

thx and waiting for reply. I have tried to use  

pip uninstall -y torch torchvision torchaudio

pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torch-2.8.0a0%2Bgitfc14c65-cp312-cp312-win_amd64.whl
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torchaudio-2.6.0a0%2B1a8f621-cp312-cp312-win_amd64.whl
pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torchvision-0.24.0a0%2Bc85f008-cp312-cp312-win_amd64.whl

but don't work.

<img width="855" height="264" alt="Image" src="https://github.com/user-attachments/assets/981abc88-db73-4c1f-be13-656bfda90275" />
(base) PS C:\Users\10649> pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torch-2.8.0a0%2Bgitfc14c65-cp312-cp312-win_amd64.whl
Collecting torch==2.8.0a0+gitfc14c65
  Downloading https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torch-2.8.0a0%2Bgitfc14c65-cp312-cp312-win_amd64.whl (781.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 781.7/781.7 MB 51.5 MB/s  0:00:14
Requirement already satisfied: filelock in d:\anaconda\lib\site-packages (from torch==2.8.0a0+gitfc14c65) (3.17.0)
Requirement already satisfied: typing-extensions>=4.10.0 in d:\anaconda\lib\site-packages (from torch==2.8.0a0+gitfc14c65) (4.15.0)
Requirement already satisfied: setuptools in d:\anaconda\lib\site-packages (from torch==2.8.0a0+gitfc14c65) (78.1.1)
Requirement already satisfied: sympy>=1.13.3 in d:\anaconda\lib\site-packages (from torch==2.8.0a0+gitfc14c65) (1.14.0)
Requirement already satisfied: networkx in d:\anaconda\lib\site-packages (from torch==2.8.0a0+gitfc14c65) (3.5)
Requirement already satisfied: jinja2 in d:\anaconda\lib\site-packages (from torch==2.8.0a0+gitfc14c65) (3.1.6)
Requirement already satisfied: fsspec in d:\anaconda\lib\site-packages (from torch==2.8.0a0+gitfc14c65) (2024.9.0)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in d:\anaconda\lib\site-packages (from sympy>=1.13.3->torch==2.8.0a0+gitfc14c65) (1.3.0)
Requirement already satisfied: MarkupSafe>=2.0 in d:\anaconda\lib\site-packages (from jinja2->torch==2.8.0a0+gitfc14c65) (3.0.2)
Installing collected packages: torch
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
lpips 0.1.4 requires torchvision>=0.2.1, which is not installed.
Successfully installed torch-2.8.0a0+gitfc14c65
(base) PS C:\Users\10649> pip install --no-cache-dir https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torchaudio-2.6.0a0%2B1a8f621-cp312-cp312-win_amd64.whl
Collecting torchaudio==2.6.0a0+1a8f621
  Downloading https://repo.radeon.com/rocm/windows/rocm-rel-6.4.4/torchaudio-2.6.0a0%2B1a8f621-cp312-cp312-win_amd64.whl (1.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 7.9 MB/s  0:00:00
Requirement already satisfied: torch in d:\anaconda\lib\site-packages (from torchaudio==2.6.0a0+1a8f621) (2.8.0a0+gitfc14c65)
Requirement already satisfied: filelock in d:\anaconda\lib\site-packages (from torch->torchaudio==2.6.0a0+1a8f621) (3.17.0)
Requirement already satisfied: typing-extensions>=4.10.0 in d:\anaconda\lib\site-packages (from torch->torchaudio==2.6.0a0+1a8f621) (4.15.0)
Requirement already satisfied: setuptools in d:\anaconda\lib\site-packages (from torch->torchaudio==2.6.0a0+1a8f621) (78.1.1)
Requirement already satisfied: sympy>=1.13.3 in d:\anaconda\lib\site-packages (from torch->torchaudio==2.6.0a0+1a8f621) (1.14.0)
Requirement already satisfied: networkx in d:\anaconda\lib\site-packages (from torch->torchaudio==2.6.0a0+1a8f621) (3.5)
Requirement already satisfied: jinja2 in d:\anaconda\lib\site-packages (from torch->torchaudio==2.6.0a0+1a8f621) (3.1.6)
Requirement already satisfied: fsspec in d:\anaconda\lib\site-packages (from torch->torchaudio==2.6.0a0+1a8f621) (2024.9.0)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in d:\anaconda\lib\site-packages (from sympy>=1.13.3->torch->torchaudio==2.6.0a0+1a8f621) (1.3.0)
Requirement already satisfied: MarkupSafe>=2.0 in d:\anaconda\lib\site-packages (from jinja2->torch->torchaudio==2.6.0a0+1a8f621) (3.0.2)
Installing collected packages: torchaudio
Successfully installed torchaudio-2.6.0a0+1a8f621
(base) PS C:\Users\10649> python -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
device name [0]: AMD Radeon(TM) Graphics 




it shows that

---

### 评论 #3 — ruaruarua111 (2025-09-30T15:48:35Z)

python --version
Python 3.12.7

---

### 评论 #4 — darren-amd (2025-10-01T19:14:00Z)

Hi @ruaruarua111,

It looks like your integrated graphics card is being picked up instead of the 7900 XTX. Could you please [disable your IGP](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html#disable-integrated-graphics-igp) and give it another try? If that doesn't work, could you provide more details on your workload as well as steps to reproduce so I can give it a try on my end? Thanks!

---
