# Doesn't ROCm support AMD's integrated GPU (APU)?

> **Issue #2216**
> **状态**: closed
> **创建时间**: 2023-06-02T10:37:03Z
> **更新时间**: 2025-12-11T06:58:24Z
> **关闭时间**: 2023-07-27T22:51:40Z
> **作者**: nav9
> **标签**: 
> **URL**: https://github.com/ROCm/ROCm/issues/2216

## 描述

I have an AMD Ryzen 5 5600G processor which has an integrated GPU, and I do not have a separate graphics card. Am using `Linux Mint 21` Cinnamon.  
I installed PyTorch with this command `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
` and according to posts on a forum, running the following command is supposed to tell me if PyTorch can use ROCm to perform CUDA equivalent processing.  
```
import torch.cuda
print(f'CUDA available? : {torch.cuda.is_available()}')
```
The output is `False`.  
   
PyTorch redirects people to this repository's readme page to check for compatible GPU information, but I didn't see any. So for the sake of anyone searching for this info:  
1. Could you publish a list of what hardware you support and which can be used with PyTorch or any other deep learning library, as an alternative to CUDA?  
2. Could you please support integrated GPU's? Mine is supposed to be as powerful as an NVidia GT 1030. When it is so powerful, it just isn't right to expect Users to purchase a separate graphics card. I do hope ROCm bridges NVidia's monopoly on CUDA.  
  
---
**Update:** Tried [this script](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533) too, but the output is 
```
Checking ROCM support...
Cannot find rocminfo command information. Unable to determine if AMDGPU drivers with ROCM support were installed.
```  
Tried installing ROCm via instructions on [this](https://docs.amd.com/bundle/ROCm-Installation-Guide-v5.1/page/How_to_Install_ROCm.html) page (tried with the `deb` file for bionic and focal).  
On running `sudo rocminfo`, I get:  
```
ROCk module is loaded
Segmentation fault
```
On running `rocminfo`:  
```
ROCk module is loaded
Unable to open /dev/kfd read-write: Permission denied
navin is not member of "render" group, the default DRM access group. Users must be a member of the "render" group or another DRM access group in order for ROCm applications to run successfully.
```
 [This script](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533) now outputs:  
```
Checking ROCM support...
BAD: No ROCM devices found.
Checking PyTorch...
GOOD: PyTorch is working fine.
Checking user groups...
Cannot find rocminfo command information. Unable to determine if AMDGPU drivers with ROCM support were installed.
```


---

## 评论 (30 条)

### 评论 #1 — langyuxf (2023-06-07T06:52:30Z)

Run like following,
```
# HSA_OVERRIDE_GFX_VERSION=9.0.0 python3
Python 3.8.16 (default, Mar  2 2023, 03:21:46)
[GCC 11.2.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch.cuda
>>> print(f'CUDA available? : {torch.cuda.is_available()}')
CUDA available? : True

```

---

### 评论 #2 — nav9 (2023-06-07T12:54:58Z)

Thank you @xfyucg , but isn't that the same code I posted above? It returned `False`. Also, it'd help to know which software to install. Since as you can see from the outputs above, running `rocminfo` results in a segmentation fault. As of now I've uninstalled those extra packages. So it'd help to know exactly what to install to get things working.

---

### 评论 #3 — nav9 (2023-07-01T17:58:50Z)

Somebody mentioned that I missed the `HSA_OVERRIDE_GFX_VERSION=9.0.0` environment variable, and then deleted their comment. Well, I tried with the environment variable, and now it works! CUDA available shows `True`. So thank you very much.   
However, `sudo rocminfo` still shows:  
```
ROCk module is loaded
Segmentation fault
```  
and [this](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533) script run as `HSA_OVERRIDE_GFX_VERSION=9.0.0 python3 trial.py` outputs:  
```
Checking ROCM support...
BAD: No ROCM devices found.
Checking PyTorch...
GOOD: PyTorch is working fine.
Checking user groups...
GOOD: The user nav is in RENDER and VIDEO groups.
GOOD: PyTorch ROCM support found.
Testing PyTorch ROCM support...
Everything fine! You can run PyTorch code inside of: 
```
Which is surprising, because if no ROCM devices were found, then how is everything fine?  
  

And during installation, the commands `amdgpu-install -y --usecase=rocm` and `sudo apt install rocm-hip-sdk` result in the error:  
```
The following packages have unmet dependencies:
 rocm-hip-runtime : Depends: rocminfo (= 1.0.0.50403-121~22.04) but 5.0.0-1 is to be installed
 rocm-utils : Depends: rocminfo (= 1.0.0.50403-121~22.04) but 5.0.0-1 is to be installed
E: Unable to correct problems, you have held broken packages.
```
  
**Distribution:**  
[This](https://docs.amd.com/en/latest/release/gpu_os_support.html#supported-distributions) page says `Ubuntu 22.04.2` is supported, and that's what I believe my `LinuxMint 21.1  x86_64` uses, because it shows `UBUNTU_CODENAME=jammy`, which is supposed to be `Ubuntu 22.04.2`. However, the supported kernels are `5.19.0-45-generic` and `5.15.0-75-generic`, but my kernel is `Linux 5.15.0-72-generic #79-Ubuntu SMP`. So I wonder if this could have also been a source of the problem.  
   
_ps: I really hope AMD could do something about making this install and use simple. It's such a good chance to compete, now that AI is going really big._

---

### 评论 #4 — nav9 (2023-07-16T11:06:38Z)

Good news guys. I found the solution. The problem was with a version mismatch, and I don't think I had run this command `sudo amdgpu-install --usecase=hiplibsdk,rocm,dkms`. I had to uninstall the installed PyTorch, and select PyTorch's Nightly version, which matched with my RoCm version. So here's the full procedure:   
`pip uninstall torch torchaudio torchdata torchvision`
`sudo apt-get install ./amdgpu-install_5.4.50403-1_all.deb` or `sudo dpkg -i amdgpu-install_5.5.50502-1_all.deb`
`sudo amdgpu-install --usecase=hiplibsdk,rocm,dkms,graphics`
`sudo amdgpu-install --list-usecase`
`sudo reboot`
`rocm-smi`
`sudo rocminfo`
  
You have to run this after installing:
`sudo usermod -a -G video <your_username>`
`sudo usermod -a -G render <your_username>`  
   
Check the RoCm version with:  
`apt show rocm-libs -a`  
   
Now select the Nightly version of PyTorch (or whichever version matches your RoCm version):  
![pytorchSelection](https://github.com/RadeonOpenCompute/ROCm/assets/2093933/29530cb1-cfab-4f54-984d-bde3f866f0d7)

and install PyTorch.  
  
Now if you run [this script](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533), it'll show:  
```
Checking ROCM support...
GOOD: ROCM devices found:  2
Checking PyTorch...
GOOD: PyTorch is working fine.
Checking user groups...
GOOD: The user nav is in RENDER and VIDEO groups.
GOOD: PyTorch ROCM support found.
Testing PyTorch ROCM support...
Everything fine! You can run PyTorch code inside of: 
--->  AMD Ryzen 5 5600G with Radeon Graphics  
--->  gfx90c  
```
  
and you can even run this script without the environment variable.  
```
import torch.cuda
print(f'CUDA available? : {torch.cuda.is_available()}')
```
  
# Note to the Radeon Open Compute developers:   
When you close this issue, I'll know that you've seen it. Please close it. However, I hope you realize two things:  

1. The process of installation is complex. So it's not just me, but many others who will end up being unable to solve the problem, and will raise an issue here or ask on StackOverflow. So please build a script which would auto-detect the system configuration and automatically install all necessary components and also create the user groups automatically. After RoCm gets installed, y'all could even show a message to the user about what they need to do to get the right version of PyTorch, if they intend to use PyTorch.   
2. CUDA is mentioned and advertised so much on the internet, that even an experienced developer like me initially didn't know that RoCm was a way to use the GPU on AMD. You guys need to do a lot more advertising and blogging to make developers aware of RoCm. I'm looking forward to using it with Modular's Mojo framework for AI.
  
Thanks for trying to help. Hope y'all would automate the install process.

---

### 评论 #5 — nav9 (2023-07-17T09:21:13Z)

One more thing. In the way that NVIDIA created a CUDA toolkit, it would help if AMD also created a module or interface which would help any application seamlessly use the GPU, whether the GPU is on a graphics card or on the processor. Also, it should work irrespective of the version.  

- I tried [OpenLLM](https://github.com/openlm-research/open_llama)'s basic example code, and it crashes with `Segmentation fault (core dumped)`.

- Tried Vicuna via [these instructions](https://huggingface.co/blog/chatbot-amd-gpu), but end up with `FAILED: GPTQ-for-LLaMa/build/temp.linux-x86_64-3.9/quant_hip_kernel.o`, which I found out, happens when the GPU version isn't the correct one.

- Tried a simple Convolutional Neural Network with PyTorch, after ensuring I moved my [models](https://wandb.ai/wandb/common-ml-errors/reports/How-To-Use-GPU-with-PyTorch---VmlldzozMzAxMDk) and [data](https://saturncloud.io/blog/how-to-force-pytorch-to-use-gpu/) to the GPU, and got this error: `rocBLAS error: Cannot read /home/nav/.pyenv/versions/3.9.17/lib/python3.9/site-packages/torch/lib/rocblas/library/TensileLibrary.dat: Illegal seek. Aborted (core dumped)`.  
  
[This](https://github.com/pytorch/pytorch/issues/96964) and [this](https://github.com/RadeonOpenCompute/ROCm/issues/1698) issue speak volumes about how much more needs to be done to improve RoCm support. People are feeling cheated.  
  
This is the right time to ask your managers to provide you more time and resources to build a good architecture for RoCm, to support Machine Learning. Please do so.

---

### 评论 #6 — langyuxf (2023-07-17T09:27:18Z)

HSA_OVERRIDE_GFX_VERSION=9.0.0 python3 app.py


---

### 评论 #7 — nav9 (2023-07-18T14:30:12Z)

Thank you xfyucg. It works. Verified with `radeontop`. There was an [issue](https://discuss.pytorch.org/t/need-help-with-getting-results-on-ryzen-5600g-with-rocm-5-5/184408), but that's related to PyTorch. Thanks for helping. Looking forward to the use of RoCm being simpler to use in future. 

---

### 评论 #8 — hongxiayang (2023-07-27T22:51:40Z)

> 

Thank you for your feedback and persistence to get this resolved. Good job! We will close this issue. 

---

### 评论 #9 — mzimmerm (2024-03-16T09:57:39Z)

On gfx902, using amdgpu-install-6.0.60002-1, I am getting a HIP error when referencing a device , even though I am using HSA_OVERRIDE_GFX_VERSION=9.0.0 (see example below)

@nav9, were you only succesfull with amdgpu-install-5.5 or should higher version work as well? Thanks

--------- Failure 
HSA_OVERRIDE_GFX_VERSION=9.0.0 python
Python 3.10.7 (main, Mar 16 2024, 00:24:41) [GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.cuda.device_count())
1
>>> cuda0 = torch.device('cuda:0')
>>> torch.ones([2, 4], dtype=torch.float64, device=cuda0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: HIP error: shared object initialization failed
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.



---

### 评论 #10 — nav9 (2024-03-16T13:04:38Z)

@mzimmerm : I just did a fresh install using `ROCm Version: 6.0.2.60002-115~22.04` via the [native package manager](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html#package-man-ubuntu) guide and `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.0`. Everything works fine. Just make sure that you choose PyTorch's Nightly build, since that's what supports ROCm version 6 as of now. Apart from this, I don't know what could be causing your problem. Hope the AMD team could help you. 

---

### 评论 #11 — mzimmerm (2024-03-16T17:06:20Z)

@nav9: Many thanks for the quick confirmation. I will deinstall and reinstall everything from 6.0.2 following steps as you described exactly and will report here. For early full disclosure (I did not mention earlier) I am running OpenSUSE Leap 15.5.

---

### 评论 #12 — mzimmerm (2024-03-16T19:45:40Z)

@nav9: Unfortunately, my reinstall attempt lead to the same result. 
- AMD Ryzen 5 2500U
-OpenSUSE Leap 15.5. 
- ROCm 6.0.2.60002-115 installed via [native package](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/sles.html) 
- Pytorch using nightly pytorch as you did `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.0`. 
- rocminfo | grep Name
  ```
  Name:                    AMD Ryzen 5 2500U with Radeon Vega Mobile Gfx
  Name:                    gfx902                             
  Name:                    amdgcn-amd-amdhsa--gfx902:xnack+  
  ```
**Same error regarding HIP when running python torch with 'device='**

HSA_OVERRIDE_GFX_VERSION=9.0.0 python
Python 3.10.7 (main, Mar 16 2024, 15:06:11) [GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> print(torch.cuda.device_count())
1
>>> cuda0 = torch.device('cuda:0')
>>> torch.ones([2, 4], dtype=torch.float64, device=cuda0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: HIP error: shared object initialization failed
HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing HIP_LAUNCH_BLOCKING=1.
Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.

**Can a AMD team member help, to narrow it further please? Thanks.** 

*Rant: I realize gfx902 is unsupported, but AMD only supports like 6 cards. Not supporting APUs is detrimental for people trying to start with machine learning tuning mini models etc.*


---

### 评论 #13 — mzimmerm (2024-03-19T05:24:55Z)

@nav9, I appologize, feel free to ignore, but in case you have time and opportunity, would you mind running on your gfx902 build the following to see if there are no errors:
``` shell
HSA_OVERRIDE_GFX_VERSION=9.0.0 python -c "import torch; cuda0 = torch.device('cuda:0');print(torch.ones([2, 4], dtype=torch.float64, device=cuda0)); print('done')"
```
I am getting consistent errors on the ROCm 6.0.2 on 3 OSs I tried (Leap 15.5, Tumbleweed, Ubuntu 22.04) both with the AMD versions and Pytorch versions of Pytorch. I am trying building PyTorch from source now, but there are issues as well. 

Thanks


---

### 评论 #14 — nav9 (2024-03-19T10:53:21Z)

@mzimmerm : I need to apologise here. I had only tried the simple script and the rocm checks. When I ran your script and [this script](https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533), it just hung. I don't know what could solve this. The AMD team needs to look into it.

---

### 评论 #15 — mzimmerm (2024-03-20T06:59:37Z)

@nav9 : Many thanks for the follow up. Yeah, I also experienced hanging in some builds - I tried a massive amount of combinations, with no luck. Well, at least I know I am not going crazy thanks to your response. I found several claims of people got gfx902 working but I doubt it now.

Unfortunately I also doubt AMD will help. For any ML stuff, they are driving people to NVIDIA in herds... Why would I buy AMD card or even APU when high chances are it is a dead metal for any ML/AI stuff.

Thanks again for your help here.

---

### 评论 #16 — serhii-nakon (2024-03-24T23:14:29Z)

@nav9 I can confirm that it also does not works with `rocm/pytorch:rocm6.0.2_ubuntu22.04_py3.10_pytorch_2.1.2`
I got error `RuntimeError: No HIP GPUs are available` while try to use `gfx90c` with `HSA_OVERRIDE_GFX_VERSION=9.0.0`

I also attach rocminfo output (looks like all good) [rocminfo.txt](https://github.com/ROCm/ROCm/files/14737127/rocminfo.txt)


---

### 评论 #17 — nav9 (2024-03-25T14:52:10Z)

Thanks serhii-nakon. I wonder if this issue needs to be re-opened or a fresh issue needs to be created. I really hope the AMD team would consider it prudent to build the necessary functionality to allow GPU use seamlessly.

---

### 评论 #18 — mzimmerm (2024-03-25T18:43:28Z)

@nav9 @serhii-nakon : For one, I would like this re-open as a new issue. It is such a waste for AMD APUs (and many other inexpensive AMD cards) to be useless for ML/AI training and inference. I started (and now officially concluded as failed) my quest to run on APUs to answer a few questions: 1) Can APUs be useful for running inference on tiny LLM models? 2) Can APUs be useful for running training on some tiny LLM models? . If one of you opens it, please Cc me there, I'd provide supporting info of things I tried and failed to run Pytorch on ROCm gfx902 (which would cover a good portion of APUs).

---

### 评论 #19 — nav9 (2024-03-25T19:19:13Z)

Among the open issues, there are already some that speak of ROCm 6 not working. 
An APU can be used for LLM inferencing, but training models would require a lot more computing power. 
If you think it's prudent to open a new issue, please do. I'm unable to reopen this issue since I'm [not a collaborator](https://github.com/orgs/community/discussions/41926#discussioncomment-6975082).

---

### 评论 #20 — barishandas (2024-06-15T11:12:28Z)

How much space did you need to install pytorch with ROCm, because every time I try to install it shows an error message: not enough space.

---

### 评论 #21 — nav9 (2024-06-15T11:57:39Z)

@berrieshawn: You could have just Googled it to [find out](https://stackoverflow.com/questions/61971817/i-can-not-install-pytorch-with-anaconda-just-because-i-ran-out-of-disk-space-the). 

---

### 评论 #22 — barishandas (2024-06-15T12:14:39Z)

I have more than 3GB free on my device, around 37 GB free, but the error still persists; and all the stackoverflow thread states is that you need at least 3GB space which is not the issue at all

---

### 评论 #23 — FlorianHeigl (2024-06-17T00:19:38Z)

Does AMD really believe that if someone runs into this they'll add an AMD card to fix the issue after spending hours to make their existing (i)GPU work? It's just not plausible. I wanted to play and learn the hard way, and **luckily** 5.4 does the job for now. But it's clear that getting this to work took as much time as just going do my normal work and buy a T4 or similar.
Do they think someone would advise using AMD for professional purposes if the toolstack is so picky, either?
And, the worst is the contradiction: the performance is tolerable as you can see when using 5.4, so that's not the argument in question here either. The VRAM issues - just tiny bugs in ROCm are just _software_ so, to put it short, they're limiting their own achievements. that is so sad.

---

### 评论 #24 — serhii-nakon (2024-06-17T10:43:47Z)

@FlorianHeigl I think AMD will support upcoming AMD AI 300 due it has really powerful iGPU and VRAM bus bandwidth. Regular 7800G not even enough to run some Llama 7B. 

Also I can confirm that ROCm works with 7800X iGPU (RDNA2). Looks like problem with Vega based iGPUs.
Also AMD does not support this hardware - so I think they did not write and test it. 

I think that ROCm won't support older hardware than RDNA2 due low performance and many issues compare to new hardware. Technically you can use ROCm from Debian team that built ROCm with older hardware and some patches and workarounds.

---

### 评论 #25 — chnhkk (2024-07-03T22:38:51Z)

> How much space did you need to install pytorch with ROCm, because every time I try to install it shows an error message: not enough space.

It's because you don't have enough space in tmp. Try doing this before running pip.
`mkdir -p $HOME/tmpdir`
`export TMPDIR=$HOME/tmpdir`

---

### 评论 #26 — thawkins (2024-07-16T00:02:46Z)

Folks remember that posting in any support board, is not the same as talking to AMD, support teams only care about closing tickets, the moment you say that you got something to partialy work, they will pressure to say the issue is fidex so they can close it. It wont go anywhere near a dev team, or even anybody who can decide its an important issue
 

---

### 评论 #27 — FlorianHeigl (2024-07-16T00:48:44Z)

@thawkins that's their own choice if they monitor their projects and collect feedback from the rocm devs or not.
and it certainly translates to units sold.

---

### 评论 #28 — nav9 (2024-07-19T14:04:27Z)

Came across the [SCALE toolkit](https://wccftech.com/nvidia-cuda-directly-run-on-amd-gpus-using-scale-toolkit/), but they support a [limited number of GPUs](https://docs.scale-lang.com/#which-gpus-are-supported). ZLUDA was also [attempted](https://www.phoronix.com/review/radeon-cuda-zluda). Given that LLMs are planned to be at the core of computing soon, it would really help for AMD to release a universal solution which will help APU's and graphics cards to be compatible with whatever is used to run or train LLMs.

---

### 评论 #29 — JimFairway (2025-03-13T00:41:12Z)

Hi, @nav9 
This is very promising, but I can't seem to get it work on Windows Subsystem for Linux (WSL) running Ubuntu Ubuntu 22.04.
Do you think WSL is the problem?

Thanks,

JF


---

### 评论 #30 — nav9 (2025-05-11T08:29:58Z)

@JimFairway : I asked [DeepAI](https://deepai.org/chat), and this is the response I got:
The primary reason the ROCm stack does not work under WSL (Windows Subsystem for Linux) on Ubuntu 22.04 is due to fundamental differences in how hardware access and kernel drivers are managed between native Linux and WSL. Here are the key points:

1. **Limited Hardware Access in WSL:**
   - WSL (especially versions before WSL 2) does not provide direct access to hardware devices like GPUs. It relies on Windows drivers and does not expose the GPU hardware directly to the Linux environment.
   - Even WSL 2, which uses a lightweight VM, has limited support for GPU passthrough, and GPU acceleration is primarily targeted at NVIDIA GPUs with WSLg and Windows-specific drivers.

2. **ROCm Requires Native Kernel Support:**
   - ROCm depends heavily on specific kernel modules and drivers that must be loaded into the Linux kernel.
   - In WSL, the Linux kernel is a modified version provided by Microsoft, and users cannot install or modify kernel modules in the same way as on a native Linux system.
   - Without the ability to load the necessary AMD GPU driver modules into the kernel, ROCm cannot function.

3. **GPU Driver Compatibility:**
   - AMD's ROCm stack requires compatible AMD GPU drivers and kernel modules that are tightly integrated with the Linux kernel.
   - Windows drivers, even with WSL GPU support, do not directly translate to the Linux kernel environment inside WSL.

4. **Official Support Limitations:**
   - AMD officially supports ROCm on certain Linux distributions running on native hardware.
   - Support for ROCm under WSL is not provided or documented, and current WSL GPU acceleration is primarily focused on NVIDIA GPUs with WSLg, not AMD.

**Summary:**
- ROCm 5.4.2 cannot work under WSL because WSL does not provide the necessary kernel-level access to AMD GPU hardware and does not support the required kernel modules.
- To run ROCm with AMD hardware, a native Linux environment (e.g., a dual boot setup or a dedicated Linux machine) is necessary.

**Recommendation:**
- Use a native Linux installation for GPU computing with AMD ROCm.
- If you need Windows, consider dual-booting or using a virtual machine with PCI passthrough support (e.g., with KVM/QEMU) for GPU access, but note that performance and compatibility might vary.


---
