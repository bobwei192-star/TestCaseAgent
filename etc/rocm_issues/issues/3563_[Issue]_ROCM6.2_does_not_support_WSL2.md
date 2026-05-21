# [Issue]: ROCM6.2 does not support WSL2

> **Issue #3563**
> **状态**: closed
> **创建时间**: 2024-08-12T13:47:45Z
> **更新时间**: 2024-12-07T09:30:21Z
> **关闭时间**: 2024-12-05T16:31:07Z
> **作者**: moyutegong
> **标签**: Feature Request, AMD Radeon RX 7900 XTX, ROCm 6.2.0
> **URL**: https://github.com/ROCm/ROCm/issues/3563

## 标签

- **Feature Request** (颜色: #fbca04)
- **AMD Radeon RX 7900 XTX** (颜色: #ededed)
- **ROCm 6.2.0** (颜色: #ededed)

## 描述

### Problem Description

ROCM6.2 does not support WSL2, running amdgpu-install-y -- usecase=wsl, rocm -- no dkms prompts missing Unable to locate package hsa-runtime-rocr4wsl-amdgpu ,running amdgpu-install 6.13 was successful

### Operating System

Ubuntu 22.04.3 LTS (Jammy Jellyfish)

### CPU

7800x3D

### GPU

AMD Radeon RX 7900 XTX

### ROCm Version

ROCm 6.2.0

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (28 条)

### 评论 #1 — Keshav-Pandey (2024-08-12T16:19:30Z)

+1. Looks like it is like https://github.com/ROCm/ROCm/issues/3051 
From the previous thread it seems like the equivalent package for [hsa-runtime-rocr4wsl-amdgpu](https://repo.radeon.com/amdgpu/6.1.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/) is not available on 6.2 or not uploaded to the repository as of now. The current [documentation](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html) asks us to use `6.1.3` so that might be the way to go while `6.2` gets sorted out.

```
amdgpu-install -y --usecase=wsl,rocm --no-dkms
Hit:1 https://repo.radeon.com/amdgpu/6.2/ubuntu jammy InRelease
Hit:2 https://repo.radeon.com/rocm/apt/6.2 jammy InRelease
Hit:3 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:4 http://archive.ubuntu.com/ubuntu noble InRelease
Hit:5 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:6 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu
E: Unable to locate package hsa-runtime-rocr4wsl-amdgpu
```

---

### 评论 #2 — harkgill-amd (2024-08-12T20:01:48Z)

Hi @moyutegong, unfortunately ROCm 6.2 does not currently support WSL2. As @Keshav-Pandey mentioned, the `hsa-runtime-rocr4wsl-amdgpu` package is not available for 6.2 and is causing the issue you are seeing.  

The latest ROCm release that supports WSL2 is 6.1.3 which you mentioned you had working previously. Support for WSL2 will be extended to ROCm 6.2 in a future point release.

---

### 评论 #3 — harkgill-amd (2024-08-12T20:09:16Z)

Closing this issue out for now. Please open a new ticket if you encounter any issues once support is extended to ROCm 6.2.

---

### 评论 #4 — supernovae (2024-09-10T16:16:56Z)

6.2.0 is required for Ubuntu 24.0.4 support and WSL2 is important to many developers - especially with 24.0.4. Any ETA to address this issue?

---

### 评论 #5 — professorf (2024-09-11T05:30:09Z)

I just ran into this issue today (9/10/2024) As @harkgill-amd mentioned downgrading to RocM 6.1 fixes it. 

BTW, I also had to downgrade python from 3.12 to 3.10.

So disappointing. I've never had any problems with Nvidia GPUs. They keep their drivers up-to-date.

---

### 评论 #6 — supernovae (2024-09-14T17:49:10Z)

It's extremely disappointing as downgrading means redoing OS image since 24.0.4 doesn't support 6.1.3 and this is the first time I've ever seen a feature come out only to not be supported by the next release. I mean seriously, why deliver something in 6.1.3 and remove it in 6.2?

---

### 评论 #7 — supernovae (2024-09-14T17:50:18Z)

@harkgill-amd can we get this re-opened? closing it seems in the worst interest of the community unless you have another issue tracking WSL2 support coming back.

---

### 评论 #8 — professorf (2024-09-14T22:25:07Z)

Yeah, come on @harkgill-amd I took a chance and bought the AMD-7900-XTX to do local AI dev. Previously I was using all Nvidia. I could have applied that $1000 to an NVidia 4090 if I knew AMD wasn't really serious about supporting prosumer AI devs, which could be a big market for your cards.

---

### 评论 #9 — harkgill-amd (2024-09-16T14:07:27Z)

Hi @supernovae and @professorf, let's use this issue to track the enablement of ROCm 6.2 on WSL. 

---

### 评论 #10 — supernovae (2024-09-18T13:51:41Z)

Is it possible to build the WSL2 components for 6.2 or would this come in a 6.2.1 or 6.3 release in future? any way i can help test/verify anything? The other issue that may be linked is Ubuntu 24.0.4.1 kernel since you can only install .1 releases now since its LTS - ubuntu 24.x support is what got me in limbo with WSL2 (caught off guard it would have regressed in a newer release)

---

### 评论 #11 — supernovae (2024-10-04T19:20:27Z)

Is there a branch i can pull and merge with newer rocm to get WSL2 support for Ubuntu 24.04.1?

---

### 评论 #12 — mcordery (2024-10-14T18:42:52Z)

Just adding in here that many developers require the fixes that you are putting in to the latest compiler releases and that many of us work on wsl enabled machines running Ubuntu so delays on the AMD side for delivering up to date compiler options means delay of products on the customer side as well.

---

### 评论 #13 — healy-hub (2024-10-19T07:58:59Z)

**ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!**

#WSL2 release version
lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.1 LTS
Release:        24.04
Codename:       noble

#AMD Sofware 
24.10.1

#Install GPU driver in WSL2 for all
wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb
 sudo apt install ./amdgpu-install_6.2.60203-1_all.deb
wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb
sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb
amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr  --vulkan=amdvlk,pro --no-dkms --accept-eula

#Anaconda Python Environment
#Installing pytorch, torchvision,  pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm'  from AMD source.
conda create -n pytorch python==3.10
conda activate pytorch
pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/
location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so

#Anaconda small problem
python
Python 3.10.0 (default, Mar  3 2022, 09:58:08) [GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/__init__.py", line 237, in <module>
    from torch._C import *  # noqa: F403
ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)
>>> exit()

-----solving method-----
sudo updatedb --prunepaths='/mnt'
sudo apt install plocate
locate libstdc++.so.6
cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back
cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back
sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6
sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29

#Pytorch Verification
python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'
Success
python3 -c 'import torch; print(torch.cuda.is_available())'
True
python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))"
device name [0]: AMD Radeon RX 7900 XTX


---

### 评论 #14 — Arthegor (2024-10-19T16:16:15Z)

> **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!**
> 
> #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble
> 
> #AMD Sofware 24.10.1
> 
> #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> 
> #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> 
> #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.
> 
> > > > import torch
> > > > Traceback (most recent call last):
> > > > File "", line 1, in 
> > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in 
> > > > from torch._C import *  # noqa: F403
> > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)
> > > > exit()
> 
> -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> 
> #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX

Work great, thank you. just 2  advice for everyone : 

- If you encounter some issue with installation of hsa runtime or amdgpu (notably one I have encounter with a missing AMDGPU-Core dependencie), repeat these two step (like install HSA -> install amdgpu -> install HSA -> install amdgpu). It solved the dependecie problem for me.
- Don't forget to replace the solving method path with your own path, and not just the user directorie if you use other conda like miniconda (use the provided  locate libstdc++.so.6 cp  command for find this path)

---

### 评论 #15 — moyutegong (2024-10-21T06:39:28Z)

> **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!**
> 
> #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble
> 
> #AMD Sofware 24.10.1
> 
> #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> 
> #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> 
> #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.
> 
> > > > import torch
> > > > Traceback (most recent call last):
> > > > File "", line 1, in 
> > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in 
> > > > from torch._C import *  # noqa: F403
> > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)
> > > > exit()
> 
> -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> 
> #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX

This can work, but loading the model into the GPU memory causes the computer to lag. Checking the usage rates of the GPU and CPU shows they are not reaching 100%. The version of PyTorch being used is torch 2.5.0+rocm6.2, and the system version is Ubuntu 24.04.1 LTS.

---

### 评论 #16 — swtrse (2024-10-31T00:49:25Z)

This is a joke. Nothing works. My next GPU will be an NVIDIA.

when I want to run the amdgpu-install command I get the message
E: Failed to fetch https://repo.radeon.com/amdgpu/6.2.3/ubuntu/dists/noble/main/binary-amd64/Packages.gz  File has unexpected size (13215 != 12901). Mirror sync in progress? [IP: 2.16.16.162 443]

---

### 评论 #17 — imkow (2024-11-08T21:27:47Z)

r u kidding me?
Err:7 https://repo.radeon.com/rocm/apt/6.2.4 noble/main amd64 Packages
  File has unexpected size (68560 != 29552). Mirror sync in progress?

---

### 评论 #18 — githust66 (2024-11-19T15:20:02Z)

> **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!**
> 
> #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble
> 
> #AMD Sofware 24.10.1
> 
> #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> 
> #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> 
> #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.
> 
> > > > import torch
> > > > Traceback (most recent call last):
> > > > File "", line 1, in 
> > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in 
> > > > from torch._C import *  # noqa: F403
> > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)
> > > > exit()
> 
> -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> 
> #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX

![image](https://github.com/user-attachments/assets/217b9fe1-d0a2-49e7-9519-734de48d3317)
Really can, the official website has not released the official support

---

### 评论 #19 — githust66 (2024-11-19T15:25:47Z)

> > **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!**
> > #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble
> > #AMD Sofware 24.10.1
> > #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> > #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> > #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.
> > > > > import torch
> > > > > Traceback (most recent call last):
> > > > > File "", line 1, in
> > > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in
> > > > > from torch._C import *  # noqa: F403
> > > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)
> > > > > exit()
> > 
> > 
> > -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> > #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX
> 
> This can work, but loading the model into the GPU memory causes the computer to lag. Checking the usage rates of the GPU and CPU shows they are not reaching 100%. The version of PyTorch being used is torch 2.5.0+rocm6.2, and the system version is Ubuntu 24.04.1 LTS.

The latest 10.1 drive has bugs that can't run up to 100%, you can try the 9.1 drive


---

### 评论 #20 — moyutegong (2024-11-19T15:30:02Z)

> > > **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 现在可以了！**
> > > #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble#WSL2 版本信息 lsb_release -a 没有可用的 LSB 模块。发行版 ID：Ubuntu 描述：Ubuntu 24.04.1 LTS 版本：24.04 代号：noble
> > > #AMD Sofware 24.10.1 AMD 软件 24.10.1
> > > #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula# 在 WSL2 中为所有安装 GPU 驱动程序 wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> > > #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so#Anaconda Python 环境 #从 AMD 源安装 pytorch、torchvision、pytorch_triton_rocm、onnxruntime_rocm、tensorflow_rocm。conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location= `pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> > > #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.Anaconda 小问题 python Python 3.10.0（默认，2022 年 3 月 3 日，09:58:08）[GCC 7.5.0] 在 linux 上。输入"help"、"版权"、"致谢"或"license"获取更多信息。
> > > > > > import torch
> > > > > > Traceback (most recent call last):跟踪回溯（最后调用）：
> > > > > > File "", line 1, in文件 "", 行 1，在
> > > > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in文件 "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/init.py"，第 237 行，在
> > > > > > from torch._C import *  # noqa: F403从 torch._C 导入所有内容 # noqa: F403
> > > > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)导入错误：/home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6：找不到版本`GLIBCXX_3.4.32'（由/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so 要求）
> > > > > > exit() 退出()
> > > 
> > > 
> > > -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29-----解决方法----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> > > #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX#Pytorch 验证 python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' 成功 python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" 设备名称 [0]: AMD Radeon RX 7900 XTX
> > 
> > 
> > This can work, but loading the model into the GPU memory causes the computer to lag. Checking the usage rates of the GPU and CPU shows they are not reaching 100%. The version of PyTorch being used is torch 2.5.0+rocm6.2, and the system version is Ubuntu 24.04.1 LTS.这可以工作，但将模型加载到 GPU 内存中会导致电脑卡顿。检查 GPU 和 CPU 的使用率显示它们没有达到 100%。使用的 PyTorch 版本是 torch 2.5.0+rocm6.2，系统版本是 Ubuntu 24.04.1 LTS。
> 
> The latest 10.1 drive has bugs that can't run up to 100%, you can try the 9.1 drive最新 10.1 驱动存在无法运行至 100%的 bug，您可以尝试使用 9.1 驱动

You're right, there is a bug in the 10.1 driver. I rolled back to 8.1 and it's working fine now.

---

### 评论 #21 — githust66 (2024-11-19T15:44:40Z)

> > > > **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 现在可以了！**
> > > > #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble#WSL2 版本信息 lsb_release -a 没有可用的 LSB 模块。发行版 ID：Ubuntu 描述：Ubuntu 24.04.1 LTS 版本：24.04 代号：noble
> > > > #AMD Sofware 24.10.1 AMD 软件 24.10.1
> > > > #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula# 在 WSL2 中为所有安装 GPU 驱动程序 wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> > > > #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so#Anaconda Python 环境 #从 AMD 源安装 pytorch、torchvision、pytorch_triton_rocm、onnxruntime_rocm、tensorflow_rocm。conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location= `pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> > > > #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.Anaconda 小问题 python Python 3.10.0（默认，2022 年 3 月 3 日，09:58:08）[GCC 7.5.0] 在 linux 上。输入"help"、"版权"、"致谢"或"license"获取更多信息。
> > > > > > > import torch
> > > > > > > Traceback (most recent call last):跟踪回溯（最后调用）：
> > > > > > > File "", line 1, in文件 "", 行 1，在
> > > > > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in文件 "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/init.py"，第 237 行，在
> > > > > > > from torch._C import *  # noqa: F403从 torch._C 导入所有内容 # noqa: F403
> > > > > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)导入错误：/home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6：找不到版本`GLIBCXX_3.4.32'（由/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so 要求）
> > > > > > > exit() 退出()
> > > > 
> > > > 
> > > > -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29-----解决方法----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> > > > #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX#Pytorch 验证 python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' 成功 python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" 设备名称 [0]: AMD Radeon RX 7900 XTX
> > > 
> > > 
> > > This can work, but loading the model into the GPU memory causes the computer to lag. Checking the usage rates of the GPU and CPU shows they are not reaching 100%. The version of PyTorch being used is torch 2.5.0+rocm6.2, and the system version is Ubuntu 24.04.1 LTS.这可以工作，但将模型加载到 GPU 内存中会导致电脑卡顿。检查 GPU 和 CPU 的使用率显示它们没有达到 100%。使用的 PyTorch 版本是 torch 2.5.0+rocm6.2，系统版本是 Ubuntu 24.04.1 LTS。
> > 
> > 
> > The latest 10.1 drive has bugs that can't run up to 100%, you can try the 9.1 drive最新 10.1 驱动存在无法运行至 100%的 bug，您可以尝试使用 9.1 驱动
> 
> You're right, there is a bug in the 10.1 driver. I rolled back to 8.1 and it's working fine now.

Is rocm6.2 now really available for wsl 2, Ubuntu 22.04, Still Only Ubuntu 24.04

---

### 评论 #22 — moyutegong (2024-11-19T15:56:32Z)

> > > > > **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 现在可以了！**
> > > > > #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble#WSL2 版本信息 lsb_release -a 没有可用的 LSB 模块。发行版 ID：Ubuntu 描述：Ubuntu 24.04.1 LTS 版本：24.04 代号：noble
> > > > > #AMD Sofware 24.10.1 AMD 软件 24.10.1
> > > > > #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula# 在 WSL2 中为所有安装 GPU 驱动程序 wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> > > > > #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so#Anaconda Python 环境 #从 AMD 源安装 pytorch、torchvision、pytorch_triton_rocm、onnxruntime_rocm、tensorflow_rocm。conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location= `pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> > > > > #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.Anaconda 小问题 python Python 3.10.0（默认，2022 年 3 月 3 日，09:58:08）[GCC 7.5.0] 在 linux 上。输入"help"、"版权"、"致谢"或"license"获取更多信息。
> > > > > > > > import torch
> > > > > > > > Traceback (most recent call last):跟踪回溯（最后调用）：
> > > > > > > > File "", line 1, in文件 "", 行 1，在
> > > > > > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in文件 "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/init.py"，第 237 行，在
> > > > > > > > from torch._C import *  # noqa: F403从 torch._C 导入所有内容 # noqa: F403
> > > > > > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)导入错误：/home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6：找不到版本`GLIBCXX_3.4.32'（由/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so 要求）
> > > > > > > > exit() 退出()
> > > > > 
> > > > > 
> > > > > -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29-----解决方法----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> > > > > #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX#Pytorch 验证 python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' 成功 python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" 设备名称 [0]: AMD Radeon RX 7900 XTX
> > > > 
> > > > 
> > > > This can work, but loading the model into the GPU memory causes the computer to lag. Checking the usage rates of the GPU and CPU shows they are not reaching 100%. The version of PyTorch being used is torch 2.5.0+rocm6.2, and the system version is Ubuntu 24.04.1 LTS.这可以工作，但将模型加载到 GPU 内存中会导致电脑卡顿。检查 GPU 和 CPU 的使用率显示它们没有达到 100%。使用的 PyTorch 版本是 torch 2.5.0+rocm6.2，系统版本是 Ubuntu 24.04.1 LTS。
> > > 
> > > 
> > > The latest 10.1 drive has bugs that can't run up to 100%, you can try the 9.1 drive最新 10.1 驱动存在无法运行至 100%的 bug，您可以尝试使用 9.1 驱动
> > 
> > 
> > You're right, there is a bug in the 10.1 driver. I rolled back to 8.1 and it's working fine now.
> 
> Is rocm6.2 now really available for wsl 2, Ubuntu 22.04, Still Only Ubuntu 24.04

Yes, ROCm 6.2 is now available, but the official documentation has not been updated, and hsa-runtime-rocr4wsl-amdgpu has not been merged into the installation script. There might be some unknown bugs, but it does work. Ubuntu 22.04 is supported. You just need to download the version for Ubuntu 22.04 from https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/. Additionally, there is a version of hsa-runtime-rocr4wsl-amdgpu that supports Ubuntu 22.04, which can be downloaded by entering https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/ and selecting the appropriate version.

---

### 评论 #23 — githust66 (2024-11-19T16:03:44Z)

> > > > > > **ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 is OK now!ROCm 6.2.3 for WSL2 Ubuntu 24.04.1 现在可以了！**
> > > > > > #WSL2 release version lsb_release -a No LSB modules are available. Distributor ID: Ubuntu Description: Ubuntu 24.04.1 LTS Release: 24.04 Codename: noble#WSL2 版本信息 lsb_release -a 没有可用的 LSB 模块。发行版 ID：Ubuntu 描述：Ubuntu 24.04.1 LTS 版本：24.04 代号：noble
> > > > > > #AMD Sofware 24.10.1 AMD 软件 24.10.1
> > > > > > #Install GPU driver in WSL2 for all wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula# 在 WSL2 中为所有安装 GPU 驱动程序 wget https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/noble/amdgpu-install_6.2.60203-1_all.deb sudo apt install ./amdgpu-install_6.2.60203-1_all.deb wget https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb sudo apt install ./hsa-runtime-rocr4wsl-amdgpu_1.14.0-2057403.24.04_amd64.deb amdgpu-install -y --usecase=wsl,rocm,amf --opencl=rocr --vulkan=amdvlk,pro --no-dkms --accept-eula
> > > > > > #Anaconda Python Environment #Installing pytorch, torchvision, pytorch_triton_rocm, onnxruntime_rocm, tensorflow_rocm' from AMD source. conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location=`pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so#Anaconda Python 环境 #从 AMD 源安装 pytorch、torchvision、pytorch_triton_rocm、onnxruntime_rocm、tensorflow_rocm。conda create -n pytorch python==3.10 conda activate pytorch pip3 install torch==2.3.0 torchvision==0.18.0 pytorch_triton_rocm==2.3.0 onnxruntime_rocm==1.18.0 tensorflow_rocm==2.16.2 -f https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/ location= `pip show torch | grep Location | awk -F ": " '{print $2}'` cd ${location}/torch/lib/ rm libhsa-runtime64.so* cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> > > > > > #Anaconda small problem python Python 3.10.0 (default, Mar 3 2022, 09:58:08) [GCC 7.5.0] on linux Type "help", "copyright", "credits" or "license" for more information.Anaconda 小问题 python Python 3.10.0（默认，2022 年 3 月 3 日，09:58:08）[GCC 7.5.0] 在 linux 上。输入"help"、"版权"、"致谢"或"license"获取更多信息。
> > > > > > > > > import torch
> > > > > > > > > Traceback (most recent call last):跟踪回溯（最后调用）：
> > > > > > > > > File "", line 1, in文件 "", 行 1，在
> > > > > > > > > File "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/**init**.py", line 237, in文件 "/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/init.py"，第 237 行，在
> > > > > > > > > from torch._C import *  # noqa: F403从 torch._C 导入所有内容 # noqa: F403
> > > > > > > > > ImportError: /home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so)导入错误：/home/tao/anaconda3/envs/pytorch/bin/../lib/libstdc++.so.6：找不到版本`GLIBCXX_3.4.32'（由/home/tao/anaconda3/envs/pytorch/lib/python3.10/site-packages/torch/lib/libhsa-runtime64.so 要求）
> > > > > > > > > exit() 退出()
> > > > > > 
> > > > > > 
> > > > > > -----solving method----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29-----解决方法----- sudo updatedb --prunepaths='/mnt' sudo apt install plocate locate libstdc++.so.6 cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.back cp /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29.back sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6 sudo cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.33 /home/tao/anaconda3/envs/pytorch/lib/libstdc++.so.6.0.29
> > > > > > #Pytorch Verification python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' Success python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" device name [0]: AMD Radeon RX 7900 XTX#Pytorch 验证 python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure' 成功 python3 -c 'import torch; print(torch.cuda.is_available())' True python3 -c "import torch; print(f'device name [0]:', torch.cuda.get_device_name(0))" 设备名称 [0]: AMD Radeon RX 7900 XTX
> > > > > 
> > > > > 
> > > > > This can work, but loading the model into the GPU memory causes the computer to lag. Checking the usage rates of the GPU and CPU shows they are not reaching 100%. The version of PyTorch being used is torch 2.5.0+rocm6.2, and the system version is Ubuntu 24.04.1 LTS.这可以工作，但将模型加载到 GPU 内存中会导致电脑卡顿。检查 GPU 和 CPU 的使用率显示它们没有达到 100%。使用的 PyTorch 版本是 torch 2.5.0+rocm6.2，系统版本是 Ubuntu 24.04.1 LTS。
> > > > 
> > > > 
> > > > The latest 10.1 drive has bugs that can't run up to 100%, you can try the 9.1 drive最新 10.1 驱动存在无法运行至 100%的 bug，您可以尝试使用 9.1 驱动
> > > 
> > > 
> > > You're right, there is a bug in the 10.1 driver. I rolled back to 8.1 and it's working fine now.
> > 
> > 
> > Is rocm6.2 now really available for wsl 2, Ubuntu 22.04, Still Only Ubuntu 24.04
> 
> Yes, ROCm 6.2 is now available, but the official documentation has not been updated, and hsa-runtime-rocr4wsl-amdgpu has not been merged into the installation script. There might be some unknown bugs, but it does work. Ubuntu 22.04 is supported. You just need to download the version for Ubuntu 22.04 from https://repo.radeon.com/amdgpu-install/6.2.3/ubuntu/jammy/. Additionally, there is a version of hsa-runtime-rocr4wsl-amdgpu that supports Ubuntu 22.04, which can be downloaded by entering https://repo.radeon.com/amdgpu/6.2.3/ubuntu/pool/main/h/hsa-runtime-rocr4wsl-amdgpu/ and selecting the appropriate version.

Thank you, I try to see the official documents that do not support it, anxious to use vllm, need rocm 6.2 haha

---

### 评论 #24 — harkgill-amd (2024-12-05T16:31:07Z)

Thank you all for your patience. ROCm 6.2.3 support for WSL has officially been released. Head over to [Install Radeon software for WSL with ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-radeon.html) for the latest installation instructions. If you encounter any issues with the release, please open a new issue so we can further investigate. Thanks again!

---

### 评论 #25 — briansp2020 (2024-12-05T16:40:36Z)

ROCm 6.3 is now released. Does  AMD plan to keep WSL support in sync with the latest ROCm release? Or how soon after new release of ROCm Linux can we expect the WSL support?

---

### 评论 #26 — Keshav-Pandey (2024-12-05T17:50:50Z)

Agree with @briansp2020 . The new release of ROCm should ideally come with support from WSL.
Even the current installation instructions and scripts do not support an easy transition from a previous version to the latest one.

---

### 评论 #27 — harkgill-amd (2024-12-06T20:03:26Z)

While I can't provide any timelines, I assure you we are actively working on the next release as well and it will be out soon. As for the release structure, I understand your frustrations with the staggered approach. We are reassessing our current approach and the delay between Linux and WSL release.

---

### 评论 #28 — githust66 (2024-12-07T09:30:21Z)

> While I can't provide any timelines, I assure you we are actively working on the next release as well and it will be out soon. As for the release structure, I understand your frustrations with the staggered approach. We are reassessing our current approach and the delay between Linux and WSL release.

Hello, I tried to use rocm6.3 on wsl2, and the result is normal. Is there any hidden problem that Linux and wsl rocm are not released together?

---
