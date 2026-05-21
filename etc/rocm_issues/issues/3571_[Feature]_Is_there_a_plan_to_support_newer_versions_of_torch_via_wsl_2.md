# [Feature]: Is there a plan to support newer versions of torch via wsl 2

> **Issue #3571**
> **状态**: closed
> **创建时间**: 2024-08-12T14:59:14Z
> **更新时间**: 2024-12-05T18:25:43Z
> **关闭时间**: 2024-12-05T18:25:43Z
> **作者**: Kademo15
> **标签**: Feature Request
> **URL**: https://github.com/ROCm/ROCm/issues/3571

## 标签

- **Feature Request** (颜色: #fbca04)

## 描述

### Suggestion Description

Currently, only PyTorch 2.1 is supported via WSL 2. However, there have been significant improvements in newer versions of PyTorch that would greatly benefit users working with WSL 2.

Could you please provide any information or roadmap regarding when or if support for these newer versions might be available? 

### Operating System

windows via wsl 2

### GPU

rx7900xtx

### ROCm Component

_No response_

---

## 评论 (22 条)

### 评论 #1 — harkgill-amd (2024-08-12T20:23:49Z)

Hi @Kademo15, the latest ROCm release that supports WSL2 is ROCm 6.1.3. Support will be extended to ROCm 6.2 in the future and with that there will be additional/newer PyTorch versions supported.

---

### 评论 #2 — Kademo15 (2024-08-12T21:12:42Z)

> Hi @Kademo15, the latest ROCm release that supports WSL2 is ROCm 6.1.3. Support will be extended to ROCm 6.2 in the future and with that there will be additional/newer PyTorch versions supported.

Thank you for the fast answer. I am aware that only rocm 6.1.3 is supported. Is there some sort of broad eta that you could give me.

---

### 评论 #3 — harkgill-amd (2024-08-26T15:35:52Z)

@Kademo15, unfortunately, I can't provide a timeline at this moment. There is currently work being done to extend support to 6.2 and I will provide more updates as soon as they're available. 

---

### 评论 #4 — evshiron (2024-09-05T16:36:04Z)

You can install newer PyTorch from PyPI in WSL by running the command for Linux, as long as you replace that `libhsa-runtime64.so` after installing with the script ([source](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html)):

```
location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
cd ${location}/torch/lib/
rm libhsa-runtime64.so*
cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
```

If you compile PyTorch in WSL, the above steps can be skipped.

---

### 评论 #5 — githust66 (2024-09-10T17:23:42Z)

> You can install newer PyTorch from PyPI in WSL by running the command for Linux, as long as you replace that `libhsa-runtime64.so` after installing with the script ([source](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html)):
> 
> ```
> location=`pip show torch | grep Location | awk -F ": " '{print $2}'`
> cd ${location}/torch/lib/
> rm libhsa-runtime64.so*
> cp /opt/rocm/lib/libhsa-runtime64.so.1.2 libhsa-runtime64.so
> ```
> 
> If you compile PyTorch in WSL, the above steps can be skipped.

Hi, is it possible to use rocm 6.1 with a higher version of pytorch on wsl, such as 2.4.0?

---

### 评论 #6 — evshiron (2024-09-10T17:26:11Z)

> Hi, is it possible to use rocm 6.1 with a higher version of pytorch on wsl, such as 2.4.0?

Definitely. Just install PyTorch for ROCm and run the script above.

---

### 评论 #7 — githust66 (2024-09-10T17:45:28Z)

> > Hi, is it possible to use rocm 6.1 with a higher version of pytorch on wsl, such as 2.4.0?
> 
> Definitely. Just install PyTorch for ROCm and run the script above.

I tried it today, and after upgrading pytorch, Execute python 3-c' import torch; print (torch.cuda. is _ available () output is false. can you give me an upgrade step

---

### 评论 #8 — evshiron (2024-09-10T18:38:02Z)

@githust66 

https://asciinema.org/a/VRT7DVw2QZxq0DlIgzoAOeiv2

---

### 评论 #9 — Kademo15 (2024-09-10T18:39:14Z)

@githust66 i just tried it following the normal steps and it worked without any issues. Make sure you are still in the venv when doing the runtime64 patch. 

---

### 评论 #10 — githust66 (2024-09-11T10:48:59Z)

> @githust66
> 
> https://asciinema.org/a/VRT7DVw2QZxq0DlIgzoAOeiv2



> @githust66
> 
> https://asciinema.org/a/VRT7DVw2QZxq0DlIgzoAOeiv2

Thank you very much, the upgrade is good, execute python 3-c' import torch; print （torch.cuda. is _ available () output is true, but python3 -c "import torch; print(f'device_name[0]:', torch.cuda.get_device_name(0))" with error /usr/local/lib/python3.10/dist-packages/torch/cuda/init.py:641: UserWarning: Can't initialize amdsmi - Error code: 34 warnings.warn（f”Can't initialize amdsmi - Error code： {e.err_code}”）

---

### 评论 #11 — evshiron (2024-09-11T12:13:20Z)

@githust66 

https://github.com/pytorch/pytorch/issues/133259

---

### 评论 #12 — githust66 (2024-09-11T12:55:50Z)

> @githust66
> 
> [pytorch/pytorch#133259](https://github.com/pytorch/pytorch/issues/133259)
I can't use amd-smi and rocm-smi on wsl, only rocminfo can. But I can run SD normally with gpu.

---

### 评论 #13 — evshiron (2024-09-11T13:28:10Z)

@githust66 

> I can't use amd-smi and rocm-smi on wsl, only rocminfo can.

Me too. Could you read the discover part in that issue again?

<details>
<summary></summary>
<pre>pip3 uninstall amdsmi nvidia-ml-py</pre>
</details>

---

### 评论 #14 — githust66 (2024-09-11T13:39:12Z)

> @githust66
> 
> > I can't use amd-smi and rocm-smi on wsl, only rocminfo can.
> 
> Me too. Could you read the discover part in that issue again?
> 
> pip3 uninstall amdsmi nvidia-ml-py

![image](https://github.com/user-attachments/assets/4ca7f3c0-b629-4bbf-a417-883536ae1e31)
Will there be any impact if you uninstall it?,If there is a problem, will the environment become normal if you install it back?

---

### 评论 #15 — evshiron (2024-09-11T13:46:08Z)

@githust66 

> Will there be any impact if you uninstall it?

As far as I know, no if you are using ROCm in WSL, because it's broken in the first place.

> If there is a problem, will the environment become normal if you install it back?

No. Building it in WSL will not succeed. If you are afraid of breaking things, use virtual environments (e.g. `python3 -m venv venv`), which is the best practice to use Python.

---

### 评论 #16 — githust66 (2024-09-11T14:10:45Z)

> @githust66
> 
> > Will there be any impact if you uninstall it?
> 
> As far as I know, no if you are using ROCm in WSL, because it's broken in the first place.
> 
> > If there is a problem, will the environment become normal if you install it back?
> 
> No. Building it in WSL will not succeed. If you are afraid of breaking things, use virtual environments (e.g. `python3 -m venv venv`), which is the best practice to use Python.

I don't know how to use the virtual environment yet, so I'll just uninstall it，After uninstalling, the GPU name will no longer be output when print(torch.cuda.get_device_name(0)) is executed
![image](https://github.com/user-attachments/assets/d9b4fb9b-2c06-4778-8655-26470b427ed2)


---

### 评论 #17 — evshiron (2024-09-11T14:36:34Z)

Activating a virtual environment is only 1 or 2 lines of code, and I have demonstrated it in [that asciinema link](https://asciinema.org/a/VRT7DVw2QZxq0DlIgzoAOeiv2).

You can run `pip3 uninstall pynvml` and try again.


---

### 评论 #18 — githust66 (2024-09-11T14:53:10Z)

> pip3 uninstall pynvml

![image](https://github.com/user-attachments/assets/eeb39b64-abb5-484d-8866-54e8c0e4e469)
That's it, thanks

---

### 评论 #19 — githust66 (2024-09-11T15:02:38Z)

> Activating a virtual environment is only 1 or 2 lines of code, and I have demonstrated it in [that asciinema link](https://asciinema.org/a/VRT7DVw2QZxq0DlIgzoAOeiv2).
> 
> You can run `pip3 uninstall pynvml` and try again.

I still can t uninstall pynvml and I have other apps that need this

---

### 评论 #20 — evshiron (2024-09-11T15:05:48Z)

Use a new virtual environment for each app.

Btw, there is a bug in PyTorch: when you have `pynvml` installed, `amdsmi` will be used, as described in [that issue link](https://github.com/pytorch/pytorch/issues/133259). Building PyTorch with the latest source code should have this issue fixed.

---

### 评论 #21 — githust66 (2024-09-11T15:09:46Z)

> Use a new virtual environment for each app.

Ok, I'll study. thanks

---

### 评论 #22 — harkgill-amd (2024-12-05T18:25:43Z)

With the release official release of ROCm 6.2.3 for WSL, support for torch has been extended to torch 2.3.0. You can find the install instructions at [Install PyTorch for ROCm](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/install-pytorch.html) and the relevant packages at https://repo.radeon.com/rocm/manylinux/rocm-rel-6.2.3/. Thanks!

---
