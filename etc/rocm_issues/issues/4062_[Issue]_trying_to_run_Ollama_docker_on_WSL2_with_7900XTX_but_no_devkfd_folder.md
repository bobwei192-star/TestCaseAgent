# [Issue]: trying to run Ollama docker on WSL2 with 7900XTX but no "/dev/kfd" folder

> **Issue #4062**
> **状态**: closed
> **创建时间**: 2024-11-28T09:25:53Z
> **更新时间**: 2024-12-12T14:58:40Z
> **关闭时间**: 2024-12-12T14:58:40Z
> **作者**: Henry715
> **标签**: Under Investigation, ROCm 6.2.3, AMD Radeon 7900XTX
> **URL**: https://github.com/ROCm/ROCm/issues/4062

## 标签

- **Under Investigation** (颜色: #0052cc)
- **ROCm 6.2.3** (颜色: #ededed)
- **AMD Radeon 7900XTX** (颜色: #ededed)

## 描述

### Problem Description

I can confirm that I have installed the ROCm and PyTorch on WSL correctly (according to the official document and this: https://github.com/ROCm/ROCm/issues/3563), as all post install checks are passed (rocminfo command works and pytorch retuen "True" for checking CUDA). but when I run "docker run -d --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:rocm
", it says "ERROR:  /dev/kfd no such file or directory". 

However I have came across this issue: https://github.com/ROCm/ROCm/issues/3734, so I substitute "--device /dev/kfd" to "--device /dev/dxg", it still cannot recognize the GPU and run the model on CPU. But if I just installed the .exe from Ollama official website, that one does utilize the GPU. 

And I have also came across to this: https://github.com/ollama/ollama/issues/5275, which it basically says it is expected to have no directory called "/dev/kfd" by following the instructions, but I haven't try the poster's method for fear that the system would break. So is this a recognized issue and will be fixed in future or I am doing something wrong?  

P.S. I am sorry that I have deleted all the setups because it got me frustrated, but I will do this again and post the log of not finding the GPU here shortly after.

### Operating System

Ubuntu 22.04.5 LTS (WSL2) / Ubuntu 24.04.1 LTS (WSL2)

### CPU

Ryzen R7-7700X

### GPU

AMD Radeon 7900XTX

### ROCm Version

ROCm 6.2.3 / ROCm 6.1.3

### ROCm Component

_No response_

### Steps to Reproduce

_No response_

### (Optional for Linux users) Output of /opt/rocm/bin/rocminfo --support

_No response_

### Additional Information

_No response_

---

## 评论 (5 条)

### 评论 #1 — Henry715 (2024-11-28T09:45:01Z)

I will try to provide as much information as possible, and I don't know if the problem will just be solved itself, so this can be either a guidance or the problem description. So here is the results of step 1 in the official document:
![image](https://github.com/user-attachments/assets/16545552-5eb1-4710-b761-3ffe1462781c)
P.S. I found that ROCm 6.2.3 doesn't work on Ubuntu-22.04 so this time I will follow exactly what says in the instruction
Got a timed out error here, but rocmifo command works:
![image](https://github.com/user-attachments/assets/5e5aefe9-e41e-4011-8396-73a6f35f1e46)
![image](https://github.com/user-attachments/assets/4bd340b1-db74-4ef6-813e-06fe8904ce6c)
Now step 2, I'm going to use pytorch later so I just install it with pip:
![image](https://github.com/user-attachments/assets/c75ca64d-4ea7-49ad-b0be-1e53847a97c8)
Due to some internet connection problem, I pip installed pytorch for three times, but it eventually had been installed (the post installation check "python3 -c 'import torch' 2> /dev/null && echo 'Success' || echo 'Failure'" returns True), and I think I encounter this problem for the first time, I'm trying to downgrade the numpy package now:
![image](https://github.com/user-attachments/assets/0f35cf5b-1397-467b-b7c4-b8056fc492c9)
So it seems the downgrading is working: 
![image](https://github.com/user-attachments/assets/3d5fc7b9-fb56-4846-b375-00268329dc26)
Now here goes the error:
![image](https://github.com/user-attachments/assets/5278ae7c-7897-4c4b-8b28-5fcb7015defd)
Now if I swtich to /dev/dxg, the container starts, but it says no compatible GPU:
![image](https://github.com/user-attachments/assets/dcc12957-7020-4d63-8815-46806cf9d197)
![image](https://github.com/user-attachments/assets/1135f202-e224-4c95-8239-f3f979e34599)

By the way I am using adrenaline 24.8.1 driver, do I really need to downgrade this driver to 24.6.1? Since the instruction says the compatuble driver is 24.6.1






---

### 评论 #2 — tcgu-amd (2024-11-28T16:19:34Z)

Hi @Henry715, thanks for reaching out! Getting Ollama working in WSL docker is going to be a little bit complicated. 

First, please follow Option: B of [this guide](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html) to get docker with ROCm running on WSL. In addition to mapping /dev/dxg, the instructions also helps you map a couple core ROCm libraries. 

However, this does not fully help with getting Ollama to run because it stills looks for kfd explicitly under the hood. Hence, You might want to follow [these instructions](https://github.com/ollama/ollama/issues/5275#issuecomment-2270886785) in order to override this behavior. 

Since the modifications are mainly going to be focused on the Ollama code, I wouldn't be too worried about breaking anything in the system. 

Hope this helps. Please do not hesitate to reach out if you have any additional questions.

Cheers!

---

### 评论 #3 — Henry715 (2024-11-29T02:24:31Z)

> Hi @Henry715, thanks for reaching out! Getting Ollama working in WSL docker is going to be a little bit complicated.
> 
> First, please follow Option: B of [this guide](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html) to get docker with ROCm running on WSL. In addition to mapping /dev/dxg, the instructions also helps you map a couple core ROCm libraries.
> 
> However, this does not fully help with getting Ollama to run because it stills looks for kfd explicitly under the hood. Hence, You might want to follow [these instructions](https://github.com/ollama/ollama/issues/5275#issuecomment-2270886785) in order to override this behavior.
> 
> Since the modifications are mainly going to be focused on the Ollama code, I wouldn't be too worried about breaking anything in the system.
> 
> Hope this helps. Please do not hesitate to reach out if you have any additional questions.
> 
> Cheers!

Sure, I will definitely try those. If I installed the docker container with Pytorch, does that mean I should run Ollama in that Pytorch Docker container rather than using that Ollama:ROCm official docker image?

---

### 评论 #4 — evshiron (2024-12-06T03:46:40Z)

> Sure, I will definitely try those. If I installed the docker container with Pytorch, does that mean I should run Ollama in that Pytorch Docker container rather than using that Ollama:ROCm official docker image?

First of all, Ollama doesn't depend on PyTorch. The error occurs because it expects the normal AMD driver to be running, which in WSL is not.

ROCm (and CUDA) in WSL use custom tricky libraries (a.k.a. `libdxcore.so`) to redirect instructions to the host, which is why `--device=/dev/dxg -v /usr/lib/wsl/lib/libdxcore.so:/usr/lib/libdxcore.so -v /opt/rocm/lib/libhsa-runtime64.so.1:/opt/rocm/lib/libhsa-runtime64.so.1` will enable (PyTorch in) ROCm in Docker in WSL. As a result, the driver that provides the files needed by Ollama is not running in WSL.

Use the recommended Adrenalin version, otherwise `libdxcore.so` might not exist in WSL.

There is a temporary but simple solution for Ollama (I don't know when they will merge this):

* https://github.com/ollama/ollama/pull/6201

Just build and run it like this in WSL:

```bash
# clone
git clone https://github.com/evshiron/ollama
cd ollama
git checkout rocm-wsl-support

# build
go generate ./...
go build .

# when building is completed

# start service
./ollama serve

# start client
./ollama run phi3
```

---

### 评论 #5 — tcgu-amd (2024-12-12T14:58:27Z)

Thanks for chiming in @evshiron! @Henry715 I will be closing this ticket for now since there's no further actionable items. Please free free to post follow-up questions. Thanks! 

---
