# [Issue]: HIP error: no kernel image is available for execution on the device

> **Issue #3894**
> **状态**: closed
> **创建时间**: 2024-10-14T05:19:13Z
> **更新时间**: 2024-10-23T12:36:15Z
> **关闭时间**: 2024-10-23T12:36:14Z
> **作者**: AtiqurRahmanAni
> **标签**: Under Investigation, AMD Radeon VII, ROCm 6.1.0
> **URL**: https://github.com/ROCm/ROCm/issues/3894

## 标签

- **Under Investigation** (颜色: #0052cc)
- **AMD Radeon VII** (颜色: #ededed)
- **ROCm 6.1.0** (颜色: #ededed)

## 描述

### Problem Description

My configuration is
OS: Ubuntu 24.04.1 LTS
GPU: AMD Radeon RX 6600
Python version: 3.12.3
Rocm version: 6.1.3.60103-122~20.04

The problem is following:
![image](https://github.com/user-attachments/assets/a69e4e82-9925-4b4f-b05a-5c1b8cbed430)

This works fine if I run this code on the Ubuntu OS disk, more specifically, where the ROCm is installed. But I am running out of Ubuntu system disk space. That's why I created a virtual environment on another disk, which is a mounted volume, installed PyTorch ROCm, . When I try to run this code I get the error shown in the image. How to solve this issue. Basically I am trying to run code on another volume.

**Note: I have seleted AMD Radeon VII because my GPU is not listed there.**

### Operating System

Ubuntu 24.04.1 LTS

### CPU

Intel core i5 10400

### GPU

AMD Radeon VII

### ROCm Version

ROCm 6.1.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (9 条)

### 评论 #1 — harkgill-amd (2024-10-15T13:50:24Z)

Hi @AtiqurRahmanAni, thank you for the report. An internal ticket has been created to further investigate this issue.

---

### 评论 #2 — tcgu-amd (2024-10-15T15:09:55Z)

Hi @AtiqurRahmanAni, thanks for reporting! The issue is odd for sure. As long as rocm is installed properly, it shouldn't matter where rocm-pytorch is installed. Would you mind providing some additional context? How did you set up the virtual environment? It looks like you are running a notebook as well, sometimes it could also be a misconfiguration of the notebook, please double check if the notebook is set to use the python environment on your mounted disk. 

On a side note, it might be easier to run rocm with pytorch on docker. You can configure docker's root directory on your mounted disk and install rocm/pytorch there. 

---

### 评论 #3 — AtiqurRahmanAni (2024-10-16T04:07:59Z)

I created the virtual environment using `python3 -m venv <myenvname>` this command. The notebook is detecting the virtual environment just fine. Even you can see from my screenshot that `cuda` is available. That means `PyTorch ROCm` is installed successfully. I also changed permission  of all the files that disk, but no luck. Now what I am doing is creating the virtual environment on the system drive where the ROCm and Ubuntu are installed and using that virtual env . It works fine, but I have to create the virtual environment on the same drive where ROCm is installed.

And another question: how long will ROCm support the RDNA2 GPUs? Many people use old 6000 series GPUs and tying to run deep learning models on their GPUs. 
Thank you so much for identifying my issue. Please let me know if you need more information regarding this issue.

---

### 评论 #4 — tcgu-amd (2024-10-16T14:43:22Z)

> I created the virtual environment using `python3 -m venv <myenvname>` this command. The notebook is detecting the virtual environment just fine. Even you can see from my screenshot that `cuda` is available. That means `PyTorch ROCm` is installed successfully. I also changed permission of all the files that disk, but no luck. Now what I am doing is creating the virtual environment on the system drive where the ROCm and Ubuntu are installed and using that virtual env . It works fine, but I have to create the virtual environment on the same drive where ROCm is installed.

I see. In that case, can you try running the following lines in python on your external drive environment and let us know the outputs?
```
import torch
print(torch.cuda.get_device_name())
```
Just wanted to see if it is recognizing your dgpu properly. Sometimes it can mistakenly target the iGPU.
also
```
import sys
print(sys.path)
```
to show that the venv is properly including the python path;
and finally
```
import os
print(os.listdir("/opt/rocm"))
```
To see if it has permission to access the ROCM path. 

> And another question: how long will ROCm support the RDNA2 GPUs? Many people use old 6000 series GPUs and tying to run deep learning models on their GPUs.  Thank you so much for identifying my issue. Please let me know if you need more information regarding this issue.

Unfortunately, I can't give you a definite answer to this. However, many older cards and cards that are not "officially" supported can still run ROCm just fine for the most part, and if you encounter any issues you can always reach out to us on Github and we will try our best to help you diagnose and solve those problems.

Hope this helps!


---

### 评论 #5 — AtiqurRahmanAni (2024-10-17T05:51:30Z)

I deleted the previously created virtual environment and created it again. Then installed PyTorch ROCm. Then I ran the following code to test, and surprisingly, it worked.
  
![test](https://github.com/user-attachments/assets/a3d5f77f-65e2-42c6-8c60-b85bc45ada33)


---

### 评论 #6 — AtiqurRahmanAni (2024-10-17T07:12:27Z)

Ok, I tried to run this code on the environment which I created on another mounted volume. The code is:

```
import os
import torch
import sys

os.environ['HSA_OVERRIDE_GFX_VERSION'] = '10.3.0'
os.environ['HIP_VISIBLE_DEVICES'] = '0'

from torchvision.models import resnet152
from torch import nn

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(DEVICE)
print()

print(torch.cuda.get_device_name())
print()

print(sys.path)
print()

print(os.listdir("/opt/rocm"))
print()

x = torch.tensor([1., 2.]).to(DEVICE)

#-------------this part is causing the issue--------------#
print(x + x)
print()


#-------------this part is causing the issue--------------#
model = resnet152(weights=None)
model.fc = nn.Linear(model.fc.in_features, 2)
model = model.to(DEVICE).eval()

inp = torch.randn((1, 3, 224, 224)).to(DEVICE)

with torch.no_grad():
    logits = model(inp)
    pred = torch.argmax(logits, dim=1).cpu().item()
    print(logits, pred)
```

Output of this code:
```
cuda

AMD Radeon RX 6600

['/media/atiqur/Study/Study Materials/Paper works/AS-Project', '/usr/lib/python312.zip', '/usr/lib/python3.12', '/usr/lib/python3.12/lib-dynload', '/media/atiqur/Study/Study Materials/Paper works/AS-Project/linuxvenv/lib/python3.12/site-packages', '/tmp/tmpi8xzg0hd']

['amdgcn', 'sbin', 'bin', 'lib', 'llvm', 'libexec', '.info', 'include', 'share']

Traceback (most recent call last):
  File "/media/atiqur/Study/Study Materials/Paper works/AS-Project/test.py", line 25, in <module>
    print(x * x)
          ~~^~~
RuntimeError: HIP error: no kernel image is available for execution on the device
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

(linuxvenv) atiqur@atiqur-MS-7D20:/media/atiqur/Study/Study Materials/Paper works/AS-Project$ python3 test.py
cuda

AMD Radeon RX 6600

['/media/atiqur/Study/Study Materials/Paper works/AS-Project', '/usr/lib/python312.zip', '/usr/lib/python3.12', '/usr/lib/python3.12/lib-dynload', '/media/atiqur/Study/Study Materials/Paper works/AS-Project/linuxvenv/lib/python3.12/site-packages', '/tmp/tmpndj20bb1']

['amdgcn', 'sbin', 'bin', 'lib', 'llvm', 'libexec', '.info', 'include', 'share']

Traceback (most recent call last):
  File "/media/atiqur/Study/Study Materials/Paper works/AS-Project/test.py", line 27, in <module>
    print(x + x)
          ~~^~~
RuntimeError: HIP error: no kernel image is available for execution on the device
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
```

The model forward pass and tensor operations are causing this error. I can not understand why this is happening. In another mounted volume, which I reported yesterday was causing an issue. But today I delete the virtual env and create it again. It is now working. To double check this, I created another virtual env on another mounted volume in the same way and installed everything. And again, I am facing this issue.

---

### 评论 #7 — tcgu-amd (2024-10-21T14:27:29Z)

@AtiqurRahmanAni Thanks for the update! I am glad that you were able to make it work. As to why it doesn't work again following your old setup, the only thing I can think of is the spaces in your venv path. Would you be able to remove them and see if anything changes! Thanks again!

---

### 评论 #8 — tcgu-amd (2024-10-21T14:43:24Z)

@AtiqurRahmanAni I am able to confirm that it is likely the space.. I was able to reproduce it on my end as well... 

---

### 评论 #9 — AtiqurRahmanAni (2024-10-23T12:36:14Z)

I got it; this is very strange, and I did not figure out it before. In my old setup where it was working, before creating this environment, I changed the disk name with no space for other reasons. Basically, in my old setup, there were no spaces between the paths. Now, I can understand why on my new disk I am facing the same error. Thank you so much. I am closing the issue. 

---
